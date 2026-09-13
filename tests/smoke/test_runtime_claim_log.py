"""P3 smoke tests — the append-only claim/edge log and the Tier-A schema.

Covers each clause of the phase's acceptance line:

1. An episode's derivations ROUND-TRIP through the log (every column, unicode
   text and locators included).
2. Replay is IDEMPOTENT under content-hashed ids — a re-append writes nothing
   and returns the already-logged records.
3. The append module contains ZERO rewrite and ZERO removal statements, proved
   both by scanning its source for SQL statement shapes and by snapshotting
   every row before and after three further operator appends.
4. Revising an ATTACKED claim leaves it ``challenged`` until a discharge is
   appended.
5. A revision is ``proposed`` until re-asserted supports land.
6. The FOLDED graph contains no edge without a log record — and, specifically,
   no support is inherited by a revision that was not re-logged.

Plus the operator semantics the clauses rest on: the keep/drop decision is
explicit and complete, carried attacks are logged, "current" is the supersession
chain head, and the retired relation labels collapse onto the four operators.

Clauses 4 and 5 are status-dependent, and the status module is a later phase.
They are asserted here over the shipped fixed point (``dks.dung``) plus the
three-line pre-filter/post-classification the plan specifies — see
:func:`_status`, which is a test-local reading, not a second status engine.

All pure/local-I/O; no network, no model.
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

import pytest

from tessellum.dks.dung import DungAF, grounded_labelling
from tessellum.runtime.claim_log import (
    ClaimDraft,
    ClaimLog,
    ClaimLogError,
    EdgeDraft,
    FoldedGraph,
    OPERATORS,
    ORIGIN_CARRIED,
    ORIGIN_PROJECTED,
    ORIGIN_QUERY,
    ORIGIN_REASSERTED,
    claim_identity,
    edge_identity,
    edgeset_digest,
    fold_log,
    operator_for_legacy_relation,
    text_digest,
)
from tessellum.runtime.store import RuntimeStore

CLAIM_LOG_SOURCE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "tessellum"
    / "runtime"
    / "claim_log.py"
)


# ── helpers ─────────────────────────────────────────────────────────────────


def _log(tmp_path: Path) -> ClaimLog:
    return ClaimLog.open(tmp_path / "runtime.db")


def _claim(name: str, text: str, *, locator: str = "h2:Claim") -> ClaimDraft:
    """A constructed claim, one per source note, with a span locator."""
    return ClaimDraft(
        derivation_id=f"derivation-{name}",
        text=text,
        note_id=f"note-{name}",
        locator=locator,
        provenance="constructed",
        source_note_hash="0" * 64,
    )


def _columns(path: Path, table: str) -> set[str]:
    conn = sqlite3.connect(path)
    try:
        return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
    finally:
        conn.close()


def _tables(path: Path) -> set[str]:
    conn = sqlite3.connect(path)
    try:
        return {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
    finally:
        conn.close()


def _raw_rows(path: Path, table: str) -> list[tuple]:
    conn = sqlite3.connect(path)
    try:
        return list(conn.execute(f"SELECT * FROM {table} ORDER BY seq"))
    finally:
        conn.close()


def _status(graph: FoldedGraph, claim_id: str) -> str:
    """The plan's three-layer read, applied over the SHIPPED fixed point.

    Deliberately not a status engine: the least-fixed-point labelling is
    ``dks.dung.grounded_labelling`` (correct and live), and all this adds is the
    documented ``supersede`` pre-filter and ``support`` post-classification so
    P3's operator semantics can be asserted before the status phase lands. The
    real, cached, stub-refusing implementation belongs to that phase.
    """
    live = graph.live_claim_ids()
    if claim_id not in live:
        return "superseded"
    labels = grounded_labelling(DungAF(arguments=live, attacks=graph.attack_pairs()))
    if labels.get(claim_id, "undec") != "in":
        return "challenged"  # `out` and `undec` both answer the same way
    return "warranted" if graph.supporters_of(claim_id) else "proposed"


# ── part (a)/(b): the schema ─────────────────────────────────────────────────


def test_schema_adds_the_log_tables_without_touching_the_existing_ones(
    tmp_path: Path,
) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    tables = _tables(store.path)
    assert {"claims", "edges", "relations", "status_cache"} <= tables
    # Additive: every shipped table is still present and jobs is unchanged.
    assert {
        "jobs",
        "job_events",
        "tool_calls",
        "plan_revisions",
        "commit_capsules",
        "capsule_artifacts",
    } <= tables
    assert "created_at" in _columns(store.path, "jobs")

    assert _columns(store.path, "claims") == {
        "claim_id",
        "derivation_id",
        "text",
        "note_id",
        "locator",
        "provenance",
        "source_note_hash",
        "text_hash",
        "seq",
        "created_at",
    }
    assert _columns(store.path, "edges") == {
        "edge_id",
        "op",
        "src",
        "dst",
        "evidence_locator",
        "origin",
        "seq",
        "created_at",
    }
    assert _columns(store.path, "status_cache") == {
        "edgeset_digest",
        "claim_id",
        "status",
    }

    # Reopening is idempotent and the log survives.
    log = ClaimLog.for_store(store)
    log.append_claim(_claim("a", "The cache is a projection."))
    RuntimeStore.open(store.path)
    assert len(log.read_claims()) == 1


def test_tier_a_relations_cache_carries_a_validity_interval(tmp_path: Path) -> None:
    """A role-style relation without a validity interval confidently returns a
    former holder, so both interval columns are part of the schema, not an
    optional extra.

    The column set is the reconciled one: this table has a single definition (the
    ``tier_a_relations`` section of ``schema.sql``) applied to both the runtime
    database and the registry sidecar, which is where ``object_kind`` comes from —
    an object that may be an entity *or* a literal has to say which, or a reader
    cannot tell a reference from a value."""
    store = RuntimeStore.open(tmp_path / "runtime.db")
    assert _columns(store.path, "relations") == {
        "relation_id",
        "subject_id",
        "predicate",
        "object_ref",
        "object_kind",
        "valid_from",
        "valid_to",
        "evidence_note",
        "evidence_locator",
        "epistemic_status",
        "origin",
        "superseded_by",
        "content_hash",
    }
    conn = sqlite3.connect(store.path)
    try:
        indexes = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
        }
    finally:
        conn.close()
    # Read BY SUBJECT, never enumerated across pairs.
    assert "relations_by_subject" in indexes


def test_column_checks_close_the_two_vocabularies(tmp_path: Path) -> None:
    log = _log(tmp_path)
    kept = log.append_claim(_claim("a", "Append is the only write."))

    conn = sqlite3.connect(log.path)
    conn.execute("PRAGMA foreign_keys = ON")  # before any DML opens a transaction
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO claims(claim_id, derivation_id, text, note_id, "
                "provenance, text_hash, seq, created_at) "
                "VALUES ('c9', 'd9', 't', 'n', 'guessed', 'h', 900, 1.0)"
            )
        conn.rollback()
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO edges(edge_id, op, src, dst, origin, seq, created_at) "
                "VALUES ('e9', 'rebuts', ?, ?, 'query', 901, 1.0)",
                (kept.claim_id, kept.claim_id),
            )
        conn.rollback()
        # An edge naming a claim the log does not hold is refused outright.
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO edges(edge_id, op, src, dst, origin, seq, created_at) "
                "VALUES ('e8', 'support', 'ghost', ?, 'query', 902, 1.0)",
                (kept.claim_id,),
            )
        conn.rollback()
    finally:
        conn.close()

    # And the module refuses both before the database is reached.
    with pytest.raises(ClaimLogError):
        log.append_edge(
            EdgeDraft("rebuts", kept.claim_id, kept.claim_id, ORIGIN_QUERY)
        )
    with pytest.raises(ClaimLogError):
        log.append_claim(
            ClaimDraft(
                derivation_id="d",
                text="t",
                note_id="n",
                provenance="guessed",
            )
        )


def test_retired_relation_labels_collapse_onto_the_four_operators() -> None:
    """Part (c), storage side: the retired vocabularies get a disposition rather
    than a parallel life. The kernel-side removals belong to the modules that
    define those labels."""
    assert operator_for_legacy_relation("supports") == "support"
    assert operator_for_legacy_relation("attacks") == "attack"
    # Two ways of attacking, one operator — the distinction lives in the
    # attacking claim's text and locator, not in a fifth edge label.
    assert operator_for_legacy_relation("rebuts") == "attack"
    assert operator_for_legacy_relation("undercuts") == "attack"
    assert operator_for_legacy_relation("revised") == "revise"
    assert operator_for_legacy_relation("superseded") == "supersede"
    # Asserting a claim is logging the claim, not an edge about it.
    assert operator_for_legacy_relation("added") is None
    assert operator_for_legacy_relation("elaborates") is None
    assert set(operator_for_legacy_relation(r) for r in ("supports", "rebuts")) <= (
        set(OPERATORS)
    )


# ── clause 1: round-trip ────────────────────────────────────────────────────


def test_an_episodes_derivations_round_trip(tmp_path: Path) -> None:
    log = _log(tmp_path)
    a = ClaimDraft(
        derivation_id="derivation-a",
        text="Le cache est une projection — jamais une source de vérité.",
        note_id="note-a",
        locator="lines:12-14",
        provenance="constructed",
        source_note_hash="a" * 64,
    )
    b = ClaimDraft(
        derivation_id="derivation-b",
        text="A heading is a topic, not a proposition.",
        note_id="note-b",
        locator=None,
        provenance="stub",
    )
    result = log.append(
        (
            a,
            b,
            EdgeDraft(
                op="support",
                src=b.claim_id,
                dst=a.claim_id,
                origin=ORIGIN_PROJECTED,
                evidence_locator="note-b#lines:3-5",
            ),
        ),
        now=1_700_000_000.0,
    )
    assert result.appended == 3

    claims = log.read_claims()
    edges = log.read_edges()
    assert claims == result.claims
    assert edges == result.edges

    stored_a, stored_b = claims
    assert stored_a.claim_id == claim_identity("derivation-a", text_digest(a.text))
    assert stored_a.text == a.text  # unicode round-trips
    assert stored_a.locator == "lines:12-14"
    assert stored_a.provenance == "constructed"
    assert stored_a.source_note_hash == "a" * 64
    assert stored_a.created_at == 1_700_000_000.0
    assert stored_b.locator is None
    assert stored_b.provenance == "stub"  # the conservative default

    edge = edges[0]
    assert edge.edge_id == edge_identity(
        "support", b.claim_id, a.claim_id, "note-b#lines:3-5"
    )
    assert (edge.op, edge.origin) == ("support", ORIGIN_PROJECTED)
    assert edge.evidence_locator == "note-b#lines:3-5"

    # One shared, monotonic log position across claims AND edges.
    assert [record.seq for record in claims] == [1, 2]
    assert [record.seq for record in edges] == [3]

    assert log.claims_for_derivation("derivation-a") == (stored_a,)


# ── clause 2: idempotent replay ─────────────────────────────────────────────


def test_replay_is_idempotent_under_content_hashed_ids(tmp_path: Path) -> None:
    log = _log(tmp_path)
    a = _claim("a", "Status is computed, never stored.")
    b = _claim("b", "The graph is the fold of the log.")
    batch = (
        a,
        b,
        EdgeDraft("support", b.claim_id, a.claim_id, ORIGIN_QUERY, "note-b#L4"),
    )

    first = log.append(batch, now=10.0)
    before = (_raw_rows(log.path, "claims"), _raw_rows(log.path, "edges"))

    replay = log.append(batch, now=99.0)
    assert replay.appended == 0
    assert replay.claims == first.claims  # the already-logged records, original seq
    assert replay.edges == first.edges
    assert (_raw_rows(log.path, "claims"), _raw_rows(log.path, "edges")) == before

    # A differently-worded derivation of the same span is a DIFFERENT claim
    # sharing one derivation identity, so recurrence stays countable.
    reworded = ClaimDraft(
        derivation_id=a.derivation_id,
        text="Status is a computed function, not a stored field.",
        note_id=a.note_id,
        locator=a.locator,
        provenance="constructed",
        source_note_hash=a.source_note_hash,
    )
    assert reworded.claim_id != a.claim_id
    log.append((reworded,), now=11.0)
    for_derivation = log.claims_for_derivation(a.derivation_id)
    assert len(for_derivation) == 2
    assert {record.derivation_id for record in for_derivation} == {a.derivation_id}


# ── clause 3: no rewrite, no removal ────────────────────────────────────────


def test_the_append_module_has_no_rewrite_or_removal_statement() -> None:
    """Scan for SQL statement SHAPES rather than bare keywords, so prose about
    the discipline is not mistaken for a violation of it."""
    source = CLAIM_LOG_SOURCE.read_text(encoding="utf-8")
    forbidden = (
        r"\bUPDATE\s+\w+\s+SET\b",
        r"\bDELETE\s+FROM\b",
        r"\bDROP\s+(TABLE|INDEX)\b",
        r"\bINSERT\s+OR\s+REPLACE\b",
        r"\bON\s+CONFLICT[^\n]*DO\s+UPDATE\b",
    )
    for pattern in forbidden:
        assert not re.search(pattern, source, re.IGNORECASE), pattern


def test_further_appends_never_rewrite_an_existing_row(tmp_path: Path) -> None:
    log = _log(tmp_path)
    a = log.append_claim(_claim("a", "The owner is the accountable team."), now=1.0)
    attacker = log.append_claim(_claim("x", "The listed owner left the role."), now=2.0)
    log.append_edge(
        EdgeDraft("attack", attacker.claim_id, a.claim_id, ORIGIN_QUERY, "note-x#L9"),
        now=3.0,
    )
    snapshot = (_raw_rows(log.path, "claims"), _raw_rows(log.path, "edges"))

    revised = log.revise(
        a.claim_id,
        _claim("a2", "The owner is the accountable team as of the last handover."),
        keep_supports=(),
        drop_supports=(),
        origin=ORIGIN_QUERY,
        now=4.0,
    )
    rebuttal = _claim("r", "The handover note post-dates that departure.")
    log.discharge_attack(
        attacking_claim_id=attacker.claim_id,
        rebuttal=rebuttal,
        origin=ORIGIN_QUERY,
        evidence_locator="note-r#L2",
        now=5.0,
    )
    log.supersede(
        superseding_claim_id=revised.revision.claim_id,
        superseded_claim_id=a.claim_id,
        origin=ORIGIN_QUERY,
        now=6.0,
    )

    after = (_raw_rows(log.path, "claims"), _raw_rows(log.path, "edges"))
    # Every pre-existing row survives byte-identically; the log only grew.
    assert after[0][: len(snapshot[0])] == snapshot[0]
    assert after[1][: len(snapshot[1])] == snapshot[1]
    assert len(after[0]) > len(snapshot[0])
    assert len(after[1]) > len(snapshot[1])


# ── part (d): the operator semantics ────────────────────────────────────────


def test_revise_requires_a_complete_and_unambiguous_keep_drop_decision(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    target = log.append_claim(_claim("a", "Promotion is coexistence."))
    s1 = log.append_claim(_claim("s1", "The batch is reviewed."))
    s2 = log.append_claim(_claim("s2", "The diff is human-gated."))
    for supporter in (s1, s2):
        log.append_edge(
            EdgeDraft(
                "support",
                supporter.claim_id,
                target.claim_id,
                ORIGIN_PROJECTED,
                f"{supporter.note_id}#L1",
            )
        )
    revision = _claim("a2", "Promotion is coexistence, never a rewrite.")

    # Silence is refused: an undecided support is how inheritance happens.
    with pytest.raises(ClaimLogError, match="undecided"):
        log.revise(
            target.claim_id,
            revision,
            keep_supports=(s1.claim_id,),
            drop_supports=(),
            origin=ORIGIN_QUERY,
        )
    with pytest.raises(ClaimLogError, match="both kept and dropped"):
        log.revise(
            target.claim_id,
            revision,
            keep_supports=(s1.claim_id, s2.claim_id),
            drop_supports=(s2.claim_id,),
            origin=ORIGIN_QUERY,
        )
    with pytest.raises(ClaimLogError, match="not an incoming support"):
        log.revise(
            target.claim_id,
            revision,
            keep_supports=(s1.claim_id, s2.claim_id, "ghost"),
            drop_supports=(),
            origin=ORIGIN_QUERY,
        )
    with pytest.raises(ClaimLogError, match="not in the log"):
        log.revise(
            "ghost",
            revision,
            keep_supports=(),
            drop_supports=(),
            origin=ORIGIN_QUERY,
        )
    # Nothing partial was written by any refusal.
    assert len(log.read_claims()) == 3
    assert len(log.read_edges()) == 2


def test_revise_relogs_every_kept_support_and_inherits_nothing(tmp_path: Path) -> None:
    log = _log(tmp_path)
    target = log.append_claim(_claim("a", "The hot set is read by subject."))
    keep = log.append_claim(_claim("s1", "Reads are keyed on the subject id."))
    drop = log.append_claim(_claim("s2", "Pairs are never enumerated."))
    for supporter in (keep, drop):
        log.append_edge(
            EdgeDraft(
                "support",
                supporter.claim_id,
                target.claim_id,
                ORIGIN_PROJECTED,
                f"{supporter.note_id}#L7",
            )
        )

    result = log.revise(
        target.claim_id,
        _claim("a2", "The hot set is read by subject, at a pinned snapshot."),
        keep_supports=(keep.claim_id,),
        drop_supports=(drop.claim_id,),
        origin=ORIGIN_QUERY,
        evidence_locator="note-a2#L3",
    )
    assert result.appended == 3  # 1 claim + 1 revise edge + 1 re-asserted support
    assert result.dropped_supports == (drop.claim_id,)

    graph = log.fold()
    revision_id = result.revision.claim_id
    # Exactly ONE support on the revision, and it is a new logged act.
    assert graph.supporters_of(revision_id) == (keep.claim_id,)
    (reasserted,) = result.reasserted_supports
    assert reasserted.origin == ORIGIN_REASSERTED
    assert reasserted.evidence_locator == f"{keep.note_id}#L7"
    assert reasserted in log.read_edges()
    # The dropped support has no edge on the revision at all...
    assert drop.claim_id not in graph.supporters_of(revision_id)
    # ...while the target keeps both of its own — the log is append-only, so a
    # revise never retracts what it revises.
    assert set(graph.supporters_of(target.claim_id)) == {keep.claim_id, drop.claim_id}
    # A revise is not a supersession.
    assert graph.chain_head(target.claim_id) == target.claim_id
    assert not graph.is_superseded(target.claim_id)

    # Replaying the whole operator is a no-op, records and all.
    again = log.revise(
        target.claim_id,
        _claim("a2", "The hot set is read by subject, at a pinned snapshot."),
        keep_supports=(keep.claim_id,),
        drop_supports=(drop.claim_id,),
        origin=ORIGIN_QUERY,
        evidence_locator="note-a2#L3",
    )
    assert again.appended == 0
    assert again.revision == result.revision
    assert again.revise_edge == result.revise_edge
    assert again.reasserted_supports == result.reasserted_supports
    assert log.fold() == graph


def test_revise_carries_incoming_attacks_as_logged_edges(tmp_path: Path) -> None:
    log = _log(tmp_path)
    target = log.append_claim(_claim("a", "The gate is scheduled and required."))
    attacker = log.append_claim(_claim("x", "The gate has never been scheduled."))
    log.append_edge(
        EdgeDraft("attack", attacker.claim_id, target.claim_id, ORIGIN_QUERY, "note-x#L4")
    )

    result = log.revise(
        target.claim_id,
        _claim("a2", "The gate is required and runs on a dwell window."),
        keep_supports=(),
        drop_supports=(),
        origin=ORIGIN_QUERY,
    )
    (carried,) = result.carried_attacks
    assert carried.op == "attack"
    assert carried.src == attacker.claim_id
    assert carried.dst == result.revision.claim_id
    assert carried.origin == ORIGIN_CARRIED
    assert carried.evidence_locator == "note-x#L4"  # the evidence travels with it
    assert carried in log.read_edges()  # a real record, not an inference
    graph = log.fold()
    assert graph.attackers_of(result.revision.claim_id) == (attacker.claim_id,)


def test_supersede_makes_the_chain_head_current(tmp_path: Path) -> None:
    log = _log(tmp_path)
    first = log.append_claim(_claim("v1", "The dwell window is seven days."))
    second = log.append_claim(_claim("v2", "The dwell window is ten days."))
    third = log.append_claim(_claim("v3", "The dwell window is fourteen days."))

    log.supersede(
        superseding_claim_id=second.claim_id,
        superseded_claim_id=first.claim_id,
        origin=ORIGIN_QUERY,
        evidence_locator="note-v2#L1",
    )
    graph = log.fold()
    assert graph.is_superseded(first.claim_id)
    assert graph.chain_head(first.claim_id) == second.claim_id

    log.supersede(
        superseding_claim_id=third.claim_id,
        superseded_claim_id=second.claim_id,
        origin=ORIGIN_QUERY,
    )
    graph = log.fold()
    # "Current" is the chain head, not the row that happens to be newest.
    assert graph.chain_head(first.claim_id) == third.claim_id
    assert graph.chain_head(third.claim_id) == third.claim_id
    # A superseded claim LEAVES the framework; it is not labelled defeated.
    assert graph.live_claim_ids() == (third.claim_id,)
    assert _status(graph, first.claim_id) == "superseded"

    # The supersession only counts when the superseding claim is warranted; the
    # warrant test is injected, so the log never second-guesses the labelling.
    unwarranted = graph.chain_head(first.claim_id, is_warranted=lambda _cid: False)
    assert unwarranted == first.claim_id
    assert not graph.is_superseded(first.claim_id, is_warranted=lambda _cid: False)


def test_supersede_refuses_a_self_reference_or_a_cycle(tmp_path: Path) -> None:
    log = _log(tmp_path)
    a = log.append_claim(_claim("a", "Retraction is an append."))
    b = log.append_claim(_claim("b", "Nothing is hard-deleted."))
    with pytest.raises(ClaimLogError, match="cannot supersede itself"):
        log.supersede(
            superseding_claim_id=a.claim_id,
            superseded_claim_id=a.claim_id,
            origin=ORIGIN_QUERY,
        )
    with pytest.raises(ClaimLogError, match="unlogged claim"):
        log.supersede(
            superseding_claim_id="ghost",
            superseded_claim_id=a.claim_id,
            origin=ORIGIN_QUERY,
        )
    log.supersede(
        superseding_claim_id=b.claim_id,
        superseded_claim_id=a.claim_id,
        origin=ORIGIN_QUERY,
    )
    with pytest.raises(ClaimLogError, match="cycle"):
        log.supersede(
            superseding_claim_id=a.claim_id,
            superseded_claim_id=b.claim_id,
            origin=ORIGIN_QUERY,
        )
    assert len(log.read_edges()) == 1


# ── clause 6: no edge without a log record ──────────────────────────────────


def test_an_edge_naming_an_unlogged_claim_cannot_be_appended(tmp_path: Path) -> None:
    """The write half of the invariant: the fold cannot contain an edge without
    a record because the append path will not create one."""
    log = _log(tmp_path)
    known = log.append_claim(_claim("a", "Every edge names two logged claims."))
    with pytest.raises(sqlite3.IntegrityError):
        log.append_edge(EdgeDraft("support", "ghost", known.claim_id, ORIGIN_QUERY))
    # An edge submitted BEFORE the claim it names is refused for the same reason,
    # so batch order is part of the contract rather than a convention.
    orphan = _claim("b", "Claims precede the edges that name them.")
    with pytest.raises(sqlite3.IntegrityError):
        log.append(
            (
                EdgeDraft("support", orphan.claim_id, known.claim_id, ORIGIN_QUERY),
                orphan,
            )
        )
    assert log.read_edges() == ()
    assert len(log.read_claims()) == 1  # the failed transaction wrote nothing


def test_the_folded_graph_contains_no_edge_without_a_log_record(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    target = log.append_claim(_claim("a", "The re-derivation gate is required."))
    supporter = log.append_claim(_claim("s", "The gate is scheduled."))
    attacker = log.append_claim(_claim("x", "The gate is optional."))
    log.append_edge(
        EdgeDraft("support", supporter.claim_id, target.claim_id, ORIGIN_PROJECTED, "s#1")
    )
    log.append_edge(
        EdgeDraft("attack", attacker.claim_id, target.claim_id, ORIGIN_QUERY, "x#1")
    )
    revised = log.revise(
        target.claim_id,
        _claim("a2", "The re-derivation gate is required and scheduled."),
        keep_supports=(supporter.claim_id,),
        drop_supports=(),
        origin=ORIGIN_QUERY,
    )
    log.discharge_attack(
        attacking_claim_id=attacker.claim_id,
        rebuttal=_claim("r", "The schedule is in the batch config."),
        origin=ORIGIN_QUERY,
        evidence_locator="r#1",
    )
    log.supersede(
        superseding_claim_id=revised.revision.claim_id,
        superseded_claim_id=target.claim_id,
        origin=ORIGIN_QUERY,
    )

    graph = log.fold()
    logged_edge_ids = {row[0] for row in _raw_rows(log.path, "edges")}
    logged_claim_ids = {row[0] for row in _raw_rows(log.path, "claims")}
    assert {edge.edge_id for edge in graph.edges} == logged_edge_ids
    assert {record.claim_id for record in graph.claims} == logged_claim_ids
    assert graph.dangling_edges() == ()
    # The fold of the records IS the graph — no derivation step in between.
    assert fold_log(log.read_claims(), log.read_edges()) == graph

    # Every edge on the revision traces to a row, including the two the revise
    # produced; nothing appeared that no record accounts for.
    revision_id = revised.revision.claim_id
    incoming = graph.incoming(revision_id)
    assert {edge.edge_id for edge in incoming} <= logged_edge_ids
    assert sorted(edge.op for edge in incoming) == ["attack", "support"]

    # The digest that keys the status cache moves on append and not on replay.
    digest = edgeset_digest(graph.edges)
    log.append_edge(
        EdgeDraft("support", supporter.claim_id, target.claim_id, ORIGIN_PROJECTED, "s#1")
    )
    assert edgeset_digest(log.fold().edges) == digest  # replayed: same edge set
    log.append_edge(
        EdgeDraft("support", supporter.claim_id, revision_id, ORIGIN_QUERY, "s#2")
    )
    assert edgeset_digest(log.fold().edges) != digest


# ── clauses 4 and 5: the two status-dependent clauses ───────────────────────


def test_revising_an_attacked_claim_stays_challenged_until_discharged(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    target = log.append_claim(_claim("a", "The mapping is reinforced by feedback."))
    supporter = log.append_claim(_claim("s", "Two positive verdicts were recorded."))
    attacker = log.append_claim(_claim("x", "A negative verdict was recorded later."))
    log.append_edge(
        EdgeDraft("support", supporter.claim_id, target.claim_id, ORIGIN_PROJECTED, "s#1")
    )
    log.append_edge(
        EdgeDraft("attack", attacker.claim_id, target.claim_id, ORIGIN_QUERY, "x#1")
    )
    assert _status(log.fold(), target.claim_id) == "challenged"

    revised = log.revise(
        target.claim_id,
        _claim("a2", "The mapping is reinforced, and demotable, by feedback."),
        keep_supports=(supporter.claim_id,),
        drop_supports=(),
        origin=ORIGIN_QUERY,
    )
    revision_id = revised.revision.claim_id
    # The attack was carried, so revising did not escape the criticism.
    assert _status(log.fold(), revision_id) == "challenged"

    log.discharge_attack(
        attacking_claim_id=attacker.claim_id,
        rebuttal=_claim("r", "That verdict was superseded by the corrected label."),
        origin=ORIGIN_QUERY,
        evidence_locator="r#1",
    )
    graph = log.fold()
    # Only now — and by reinstatement, from the appended discharge alone.
    assert _status(graph, revision_id) == "warranted"
    assert _status(graph, attacker.claim_id) == "challenged"


def test_a_revision_is_proposed_until_reasserted_supports_land(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    target = log.append_claim(_claim("a", "The cache is demotable."))
    supporter = log.append_claim(_claim("s", "A negative verdict evicts a mapping."))
    log.append_edge(
        EdgeDraft("support", supporter.claim_id, target.claim_id, ORIGIN_PROJECTED, "s#1")
    )
    assert _status(log.fold(), target.claim_id) == "warranted"

    # Drop the support: the revision inherits nothing, so it is only proposed.
    revised = log.revise(
        target.claim_id,
        _claim("a2", "The cache is demotable before it is reinforceable."),
        keep_supports=(),
        drop_supports=(supporter.claim_id,),
        origin=ORIGIN_QUERY,
    )
    revision_id = revised.revision.claim_id
    assert log.fold().supporters_of(revision_id) == ()
    assert _status(log.fold(), revision_id) == "proposed"

    # Re-asserting the support is a further append, and only then is it warranted.
    log.append_edge(
        EdgeDraft(
            "support", supporter.claim_id, revision_id, ORIGIN_REASSERTED, "s#1"
        )
    )
    assert _status(log.fold(), revision_id) == "warranted"
