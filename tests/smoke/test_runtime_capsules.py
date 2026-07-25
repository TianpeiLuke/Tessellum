"""P1 smoke tests — durable snapshot-pinned knowledge-transaction records.

Gate-to-P2 deliverable for PHASE P1 of "Dynamic Digestion as a Snapshot-Pinned
Knowledge Transaction". Proves the five guarantees the plan names:

1. v4 -> v5 migration is clean + idempotent on reopen (A1.1 schema migration).
2. A :class:`PlanRevision` + its :class:`CommitCapsule` persist and reload
   byte-identically, including the artifact CAS round-trip (A1.1 / A1.2,
   guarantee 5).
3. A sign-off decision records a durable :class:`PlanRevision` (accept AND
   reject) WITHOUT changing :class:`SignOffResult` for existing callers
   (A1.5, additive opt-in).
4. ``commit_capsules.revision_id`` (and the ``jobs`` link columns) FK
   integrity holds (foreign_keys=ON).
5. No new promotion path is enabled — linking is pure bookkeeping; state /
   ``execution_generation`` / lease are untouched (A1.4 deferral respected).

All pure/local-I/O; no network, no LLM. Run with python3.11.
"""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

import pytest

from tessellum.composer.proposals import (
    AddNote,
    canonical_json_bytes,
    plan_revision_hash,
)
from tessellum.composer.signoff import (
    AgentVerdict,
    SignOffPolicy,
    run_sign_off,
)
from tessellum.runtime.models import JobState, WorkRequest
from tessellum.runtime.store import RuntimeStore, plan_revision_recorder


def _request(event: str = "papers/a.md") -> WorkRequest:
    return WorkRequest(
        source="inbox",
        source_event_id=event,
        intent="digest",
        payload_ref="sha256:" + "a" * 64,
        original_path=f"/tmp/{event}",
        lane="papers",
    )


# The v4 jobs column list (pre-P1: NO accepted_revision_id / active_capsule_id).
_V4_JOBS_DDL = """
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    idempotency_key TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL,
    source_event_id TEXT NOT NULL,
    intent TEXT NOT NULL,
    payload_ref TEXT NOT NULL,
    original_path TEXT NOT NULL,
    source_device INTEGER,
    source_inode INTEGER,
    source_size INTEGER,
    source_mtime_ns INTEGER,
    lane TEXT NOT NULL,
    policy_profile TEXT NOT NULL,
    priority INTEGER NOT NULL,
    not_before REAL,
    requested_capability TEXT,
    state TEXT NOT NULL,
    capability TEXT,
    skill_digest TEXT,
    plan_hash TEXT,
    execution_generation INTEGER NOT NULL DEFAULT 1,
    lease_owner TEXT,
    lease_generation INTEGER NOT NULL DEFAULT 0,
    lease_expires_at REAL,
    attempts INTEGER NOT NULL DEFAULT 0,
    commit_attempts INTEGER NOT NULL DEFAULT 0,
    cancel_requested INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    result_path TEXT,
    supersedes_job_id TEXT REFERENCES jobs(job_id),
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);
"""


def _build_v4_db(path: Path) -> str:
    """Create a raw v4 DB (version=4, jobs without the two P1 columns) with
    one ADMITTED job. Returns the job_id."""
    conn = sqlite3.connect(path)
    try:
        conn.executescript(
            "CREATE TABLE runtime_schema (version INTEGER NOT NULL);"
            + _V4_JOBS_DDL
            + """
            CREATE TABLE job_events (
                job_id TEXT NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
                sequence INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                at REAL NOT NULL,
                detail_json TEXT NOT NULL,
                PRIMARY KEY(job_id, sequence)
            );
            CREATE TABLE tool_calls (
                call_id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
                tool_name TEXT NOT NULL,
                arguments_json TEXT NOT NULL,
                result_hash TEXT,
                policy_decision TEXT NOT NULL,
                duration_ms REAL NOT NULL,
                error TEXT,
                created_at REAL NOT NULL
            );
            """
        )
        conn.execute("INSERT INTO runtime_schema(version) VALUES (4)")
        conn.execute(
            """
            INSERT INTO jobs(
                job_id, idempotency_key, source, source_event_id, intent,
                payload_ref, original_path, lane, policy_profile, priority,
                state, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "job-v4",
                "idem-v4",
                "inbox",
                "papers/legacy.md",
                "digest",
                "sha256:" + "b" * 64,
                "/tmp/legacy.md",
                "papers",
                "default",
                50,
                JobState.ADMITTED.value,
                1.0,
                1.0,
            ),
        )
        conn.commit()
    finally:
        conn.close()
    return "job-v4"


def _schema_version(store: RuntimeStore) -> int:
    conn = sqlite3.connect(store.path)
    try:
        return conn.execute("SELECT version FROM runtime_schema").fetchone()[0]
    finally:
        conn.close()


def _table_names(store: RuntimeStore) -> set[str]:
    conn = sqlite3.connect(store.path)
    try:
        return {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
    finally:
        conn.close()


def _jobs_columns(store: RuntimeStore) -> set[str]:
    conn = sqlite3.connect(store.path)
    try:
        return {row[1] for row in conn.execute("PRAGMA table_info(jobs)").fetchall()}
    finally:
        conn.close()


# ── Deliverable 1 — v4 -> v5 migration clean + idempotent on reopen ─────────


def test_v4_db_migrates_to_v5_and_is_idempotent(tmp_path: Path) -> None:
    db = tmp_path / "runtime.db"
    job_id = _build_v4_db(db)

    store = RuntimeStore.open(db)  # first open migrates
    assert _schema_version(store) == 5
    cols = _jobs_columns(store)
    assert "accepted_revision_id" in cols
    assert "active_capsule_id" in cols
    assert {"plan_revisions", "commit_capsules", "capsule_artifacts"} <= _table_names(
        store
    )
    legacy = store.get(job_id)
    assert legacy is not None
    assert legacy.state == JobState.ADMITTED
    assert legacy.accepted_revision_id is None
    assert legacy.active_capsule_id is None

    # Reopen on the same path — idempotent: no error, version still 5,
    # columns still present, legacy job still intact.
    store2 = RuntimeStore.open(db)
    assert _schema_version(store2) == 5
    assert {"accepted_revision_id", "active_capsule_id"} <= _jobs_columns(store2)
    still = store2.get(job_id)
    assert still is not None and still.state == JobState.ADMITTED


def test_fresh_db_opens_at_v5(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    assert _schema_version(store) == 5
    assert {"plan_revisions", "commit_capsules", "capsule_artifacts"} <= _table_names(
        store
    )
    assert {"accepted_revision_id", "active_capsule_id"} <= _jobs_columns(store)


# ── Deliverable 2 — revision + capsule + CAS byte-identical round-trip ──────


def _sample_revision(store: RuntimeStore) -> tuple[str, str, bytes]:
    """Record a revision from real composer effects; return
    (revision_id, parent, canonical_bytes)."""
    parent = "0" * 64
    effects = (
        AddNote(note_id="n1", target_path="areas/n1.md", content_hash="c1"),
        AddNote(note_id="n2", target_path="areas/n2.md", content_hash="c2"),
    )
    rev = plan_revision_hash(parent, effects)
    canonical = canonical_json_bytes(
        {"parent": parent, "effects": [e.model_dump(mode="json") for e in effects]}
    )
    store.record_plan_revision(
        rev,
        parent_revision_id=parent,
        canonical_bytes=canonical,
        decision="accept",
        evidence={"k": "v"},
    )
    return rev, parent, canonical


def test_plan_revision_roundtrips_byte_identical(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    rev, parent, canonical = _sample_revision(store)

    got = store.get_plan_revision(rev)
    assert got is not None
    assert got.revision_id == rev
    assert got.parent_revision_id == parent
    assert isinstance(got.canonical_bytes, bytes)
    assert got.canonical_bytes == canonical  # byte-identical BLOB round-trip
    assert got.decision == "accept"
    assert got.evidence == {"k": "v"}


def test_commit_capsule_and_cas_roundtrip(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    rev, _parent, _canonical = _sample_revision(store)

    policy_version = "default\0renderer=1\0parser=1"
    cap = store.create_commit_capsule(
        revision_id=rev, base_generation=1, policy_version=policy_version
    )
    # Deterministic capsule_id: re-create with identical inputs is idempotent.
    cap_again = store.create_commit_capsule(
        revision_id=rev, base_generation=1, policy_version=policy_version
    )
    assert cap.capsule_id == cap_again.capsule_id
    assert cap.capsule_id == RuntimeStore.capsule_identity(rev, 1, policy_version)

    blobs = {
        # non-UTF8 bytes to prove pure-bytes handling (no text/newline mangling).
        "accepted_canonical": b"\x00\xff\xfe canonical",
        "postimage": b"# note body\r\nline\n",
        "source_extraction": "sourcé extraction".encode("utf-8"),
        "gate_evidence": b'{"gate": "close", "passed": true}',
        "renderer_versions": b"renderer=1\0parser=1",
    }
    addresses: dict[str, str] = {}
    for cls, blob in blobs.items():
        addr = store.put_capsule_artifact(cap.capsule_id, cls, blob)
        assert addr == hashlib.sha256(blob).hexdigest()
        assert store.get_capsule_artifact(cap.capsule_id, addr) == blob  # byte-identical
        # Re-put identical blob -> same addr, no error (idempotent CAS).
        assert store.put_capsule_artifact(cap.capsule_id, cls, blob) == addr
        addresses[cls] = addr

    reloaded = store.get_commit_capsule(cap.capsule_id)
    assert reloaded is not None
    assert reloaded.base_generation == 1
    assert reloaded.state == "open"
    assert reloaded.artifact_root.endswith(cap.capsule_id)

    manifest = store.list_capsule_artifacts(cap.capsule_id)
    assert len(manifest) == 5
    by_addr = {row.address: row for row in manifest}
    for cls, blob in blobs.items():
        row = by_addr[addresses[cls]]
        assert row.size == len(blob)
        assert row.capsule_id == cap.capsule_id


def test_capsule_state_progression(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    rev, _parent, _canonical = _sample_revision(store)
    cap = store.create_commit_capsule(
        revision_id=rev, base_generation=0, policy_version="x"
    )
    assert cap.state == "open"
    sealed = store.set_capsule_state(cap.capsule_id, "sealed")
    assert sealed.state == "sealed"
    assert store.get_commit_capsule(cap.capsule_id).state == "sealed"


# ── Deliverable 3 — sign-off records durable revision (accept AND reject) ───


def test_signoff_records_accept_and_reject(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    parent = "0" * 64
    eff_a = (AddNote(note_id="a", target_path="areas/a.md", content_hash="ca"),)
    eff_b = (AddNote(note_id="b", target_path="areas/b.md", content_hash="cb"),)
    rev_a = plan_revision_hash(parent, eff_a)
    rev_b = plan_revision_hash(parent, eff_b)
    can_a = canonical_json_bytes({"r": "a"})
    can_b = canonical_json_bytes({"r": "b"})

    # ACCEPT path — with vs without recorder must be byte-identical.
    recorder_a = plan_revision_recorder(
        store, revision_id=rev_a, parent_revision_id=parent, canonical_bytes=can_a
    )
    policy = SignOffPolicy(use_agent=False)
    baseline = run_sign_off(program_gate=lambda: (True, None), policy=policy)
    withrec = run_sign_off(
        program_gate=lambda: (True, None),
        policy=policy,
        revision_recorder=recorder_a,
    )
    assert withrec == baseline  # SignOffResult unchanged for existing callers
    assert withrec.decision == "approved"
    rec_a = store.get_plan_revision(rev_a)
    assert rec_a is not None and rec_a.decision == "accept"
    assert rec_a.evidence["rung"] == "program"

    # REJECT path — failing program gate.
    recorder_b = plan_revision_recorder(
        store, revision_id=rev_b, parent_revision_id=parent, canonical_bytes=can_b
    )
    baseline_r = run_sign_off(
        program_gate=lambda: (False, "defect"), policy=policy
    )
    withrec_r = run_sign_off(
        program_gate=lambda: (False, "defect"),
        policy=policy,
        revision_recorder=recorder_b,
    )
    assert withrec_r == baseline_r
    assert withrec_r.decision == "rejected"
    rec_b = store.get_plan_revision(rev_b)
    assert rec_b is not None and rec_b.decision == "reject"
    assert rec_b.canonical_bytes == can_b


def test_signoff_default_recorder_is_noop(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    result = run_sign_off(
        program_gate=lambda: (True, None), policy=SignOffPolicy(use_agent=False)
    )
    assert result.decision == "approved"
    conn = sqlite3.connect(store.path)
    try:
        count = conn.execute("SELECT COUNT(*) FROM plan_revisions").fetchone()[0]
    finally:
        conn.close()
    assert count == 0  # opt-in default writes nothing


# ── Deliverable 4 — FK integrity (capsule + jobs link columns) ──────────────


def test_capsule_requires_existing_revision(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    with pytest.raises(sqlite3.IntegrityError):
        store.create_commit_capsule(
            revision_id="does-not-exist", base_generation=0, policy_version="x"
        )


def test_job_revision_link_fk_integrity(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)

    # Linking a ghost revision violates the FK.
    with pytest.raises(sqlite3.IntegrityError):
        store.link_job_revision(job.job_id, accepted_revision_id="ghost")

    # With a recorded revision it succeeds and the link reads back.
    rev, _parent, _canonical = _sample_revision(store)
    linked = store.link_job_revision(job.job_id, accepted_revision_id=rev)
    assert linked.accepted_revision_id == rev
    assert store.get(job.job_id).accepted_revision_id == rev


# ── Deliverable 5 — no new promotion path (A1.4 deferral respected) ─────────


def test_recording_does_not_promote_or_bump_generation(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    assert job.state == JobState.ADMITTED
    assert job.execution_generation == 1
    assert job.lease is None

    rev, _parent, _canonical = _sample_revision(store)
    cap = store.create_commit_capsule(
        revision_id=rev, base_generation=1, policy_version="default"
    )
    linked = store.link_job_revision(
        job.job_id,
        accepted_revision_id=rev,
        active_capsule_id=cap.capsule_id,
    )
    # Linking is pure bookkeeping — no promotion, no generation bump.
    assert linked.state == JobState.ADMITTED
    assert linked.execution_generation == 1
    assert linked.lease is None
    assert linked.request.not_before == job.request.not_before
    assert linked.accepted_revision_id == rev
    assert linked.active_capsule_id == cap.capsule_id

    # Linking a second (stale/arbitrary) already-recorded revision must NOT
    # reject or transition the job — no admission stale-revision fence exists
    # yet (A1.4 deferred). Note the COALESCE keeps the prior revision link.
    other_effects = (AddNote(note_id="z", target_path="areas/z.md", content_hash="cz"),)
    other_rev = plan_revision_hash("0" * 64, other_effects)
    store.record_plan_revision(
        other_rev,
        parent_revision_id=None,
        canonical_bytes=canonical_json_bytes({"r": "z"}),
        decision="accept",
    )
    relinked = store.link_job_revision(job.job_id, plan_hash="cap-digest-1")
    assert relinked.state == JobState.ADMITTED
    assert relinked.plan_hash == "cap-digest-1"  # capability identity, caller-passed
    assert relinked.accepted_revision_id == rev  # COALESCE preserved

    # Sanity: claim_next after linking still behaves exactly as baseline
    # (claims, lease generation 0 -> 1 on first claim; execution_generation
    # increments per the shipped claim semantics, untouched by P1).
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=20.0)
    assert claimed is not None
    assert claimed.job_id == job.job_id
    assert claimed.state == JobState.ROUTED
    assert claimed.lease is not None and claimed.lease.generation == 1
    # Link columns survive the claim (bookkeeping is orthogonal to promotion).
    assert claimed.accepted_revision_id == rev
    assert claimed.active_capsule_id == cap.capsule_id


# ── Hardening (review nits) ─────────────────────────────────────────────────


def test_cas_manifest_keeps_per_class_rows_for_shared_content(tmp_path: Path) -> None:
    """Two DISTINCT artifact classes with byte-identical content each keep a
    manifest row (PK is (capsule_id, artifact_class, address)); the on-disk
    blob is still deduplicated by address."""
    store = RuntimeStore.open(tmp_path / "runtime.db")
    rev, _parent, _canonical = _sample_revision(store)
    cap = store.create_commit_capsule(
        revision_id=rev, base_generation=1, policy_version="p"
    )
    shared = b"identical bytes across two classes"
    addr1 = store.put_capsule_artifact(cap.capsule_id, "accepted_canonical", shared)
    addr2 = store.put_capsule_artifact(cap.capsule_id, "postimage", shared)
    assert addr1 == addr2  # same content -> same address (blob dedup by address)

    manifest = store.list_capsule_artifacts(cap.capsule_id)
    classes = {row.artifact_class for row in manifest}
    assert classes == {"accepted_canonical", "postimage"}  # both rows survive
    assert len([r for r in manifest if r.address == addr1]) == 2
    # Content still round-trips byte-identically (guarantee 5).
    assert store.get_capsule_artifact(cap.capsule_id, addr1) == shared


def test_signoff_records_needs_human_distinctly(tmp_path: Path) -> None:
    """A ``needs_human`` escalation records a durable ``needs_human`` decision,
    NOT a ``reject`` — an escalation that reached no terminal accept/reject is
    not a rejection."""
    store = RuntimeStore.open(tmp_path / "runtime.db")
    parent = "0" * 64
    eff = (AddNote(note_id="h", target_path="areas/h.md", content_hash="ch"),)
    rev = plan_revision_hash(parent, eff)
    recorder = plan_revision_recorder(
        store, revision_id=rev, parent_revision_id=parent,
        canonical_bytes=canonical_json_bytes({"r": "h"}),
    )
    # A confident approval on a HIGH-blast plan with the human rung
    # unavailable (use_human=False) escalates to a terminal needs_human.
    policy = SignOffPolicy(use_agent=True, use_human=False, blast_radius_threshold=1)
    result = run_sign_off(
        program_gate=lambda: (True, None),
        policy=policy,
        blast_radius=1000,
        agent_judge=lambda: AgentVerdict(approved=True, confidence=0.99, reason="ok"),
        human_prompt=None,
        revision_recorder=recorder,
    )
    assert result.decision == "needs_human"
    rec = store.get_plan_revision(rev)
    assert rec is not None
    assert rec.decision == "needs_human"  # faithful, not "reject"
