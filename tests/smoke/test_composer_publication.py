"""P5 — versioned publication + snapshot CAS (A5.1-A5.4).

Proves the atomic reader-visible commit point: PREPARED → PUBLISHED →
ACKNOWLEDGED with a single-os.replace CURRENT-pointer swap; no partial reader
visibility; snapshot CAS aborts on a moved base or a read-set mutation/phantom
(the lost-update hazard); recovery completes a published-unacknowledged
generation idempotently and collects unreferenced staging; bounded retry
terminates as blocked (never livelock).
"""

from __future__ import annotations

import pytest
from pathlib import Path

from tessellum.composer.publication import (
    ABSENT,
    KnowledgeCapsule,
    PublicationError,
    RetryPolicy,
    VaultSnapshot,
    VersionedVault,
    publish_with_cas,
    read_set_matches,
)
from tessellum.composer.write_closure import WriteClosure, WriteEffect


def _capsule(cid: str = "cap1") -> KnowledgeCapsule:
    wc = WriteClosure(writes=(WriteEffect("areas/n1.md", "note", "areas/n1.md"),))
    return KnowledgeCapsule(
        capsule_id=cid, source_bundle_hash="sb", vault_snapshot_id="snap",
        knowledge_plan_hash="kp", write_closure=wc,
    )


def _vault(tmp_path: Path) -> VersionedVault:
    v = VersionedVault(tmp_path / "pub")
    v.initialize()
    return v


# ── A5.1 snapshot id ────────────────────────────────────────────────────────


def test_snapshot_id_deterministic_and_order_independent() -> None:
    a = VaultSnapshot(base_generation="g", index_hash="h",
                      read_set={"a": "1", "b": "2"}, candidate_query_hashes=("q1", "q2"))
    b = VaultSnapshot(base_generation="g", index_hash="h",
                      read_set={"b": "2", "a": "1"}, candidate_query_hashes=("q2", "q1"))
    assert a.snapshot_id == b.snapshot_id


# ── A5.2 capsule well-formedness ─────────────────────────────────────────────


def test_capsule_well_formed_iff_write_set_matches_closure() -> None:
    cap = _capsule()
    assert cap.well_formed(cap.write_closure)
    other = WriteClosure(writes=(WriteEffect("areas/other.md", "note", "areas/other.md"),))
    assert not cap.well_formed(other)


# ── A5.3 protocol + atomic pointer swap ──────────────────────────────────────


def test_prepare_does_not_change_current(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    genesis = v.current_generation()
    gen = v.prepare(_capsule(), {"areas/n1.md": b"# N1\n"})
    # PREPARED is invisible to readers — CURRENT still the genesis.
    assert v.current_generation() == genesis
    assert gen != genesis


def test_publish_swaps_current_atomically(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    genesis = v.current_generation()
    gen = v.prepare(_capsule(), {"areas/n1.md": b"# N1\n"})
    res = v.publish(gen, expected_current=genesis)
    assert res.outcome == "published"
    assert v.current_generation() == gen
    # the published generation dir holds the note bytes.
    assert (v.generation_dir(gen) / "areas/n1.md").read_bytes() == b"# N1\n"


def test_prepare_is_idempotent_content_addressed(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    g1 = v.prepare(_capsule(), {"areas/n1.md": b"# N1\n"})
    g2 = v.prepare(_capsule(), {"areas/n1.md": b"# N1\n"})
    assert g1 == g2  # same capsule + files → same generation id


def test_acknowledge_idempotent(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    genesis = v.current_generation()
    gen = v.prepare(_capsule(), {"areas/n1.md": b"# N1\n"})
    v.publish(gen, expected_current=genesis)
    assert not v.is_acknowledged(gen)
    v.acknowledge(gen)
    v.acknowledge(gen)  # no-op second time
    assert v.is_acknowledged(gen)


# ── A5.4 snapshot CAS ────────────────────────────────────────────────────────


def test_publish_cas_conflict_when_current_moved(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    genesis = v.current_generation()
    # first transaction publishes.
    g1 = v.prepare(_capsule("cap1"), {"areas/n1.md": b"# N1\n"})
    v.publish(g1, expected_current=genesis)
    # second transaction planned against the (now stale) genesis → conflict.
    g2 = v.prepare(_capsule("cap2"), {"areas/n2.md": b"# N2\n"})
    res = v.publish(g2, expected_current=genesis)
    assert res.outcome == "cas_conflict"
    assert v.current_generation() == g1  # CURRENT untouched by the aborted publish


def test_read_set_matches_detects_mutation_and_phantom() -> None:
    snap = VaultSnapshot(base_generation="g", index_hash="h",
                         read_set={"areas/a.md": "hashA", "areas/absent.md": ABSENT})
    # unchanged → matches.
    assert read_set_matches(snap, {"areas/a.md": "hashA", "areas/absent.md": None})
    # a.md mutated → lost-update hazard.
    assert not read_set_matches(snap, {"areas/a.md": "hashB", "areas/absent.md": None})
    # a phantom appeared where absence was relied on.
    assert not read_set_matches(snap, {"areas/a.md": "hashA", "areas/absent.md": "new"})


def test_publish_cas_check_read_set_abort(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    genesis = v.current_generation()
    gen = v.prepare(_capsule(), {"areas/n1.md": b"# N1\n"})
    # cas_check returns False (a read-set path changed under us) → abort.
    res = v.publish(gen, expected_current=genesis, cas_check=lambda: False)
    assert res.outcome == "cas_conflict"
    assert v.current_generation() == genesis


# ── recovery + GC ────────────────────────────────────────────────────────────


def test_recover_completes_published_unacknowledged(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    genesis = v.current_generation()
    gen = v.prepare(_capsule(), {"areas/n1.md": b"# N1\n"})
    v.publish(gen, expected_current=genesis)  # published but NOT acknowledged
    assert not v.is_acknowledged(gen)
    # a fresh handle simulates a restart; recovery completes the commit.
    v2 = VersionedVault(tmp_path / "pub")
    live = v2.recover()
    assert live == gen
    assert v2.is_acknowledged(gen)


def test_collect_staging_drops_unpublished_only(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    genesis = v.current_generation()
    published_gen = v.prepare(_capsule("cap1"), {"areas/n1.md": b"# N1\n"})
    v.publish(published_gen, expected_current=genesis)
    # an abandoned PREPARED generation (never published).
    orphan = v.prepare(_capsule("cap2"), {"areas/n2.md": b"# N2\n"})
    collected = v.collect_staging()
    assert orphan in collected
    # the published generation survives (it was promoted out of staging).
    assert (v.generation_dir(published_gen) / "areas/n1.md").is_file()


# ── bounded retry → blocked ──────────────────────────────────────────────────


def test_publish_with_cas_retries_then_blocks(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    genesis = v.current_generation()
    # occupy CURRENT so the target's expected_current is always stale.
    occupant = v.prepare(_capsule("occupant"), {"areas/occ.md": b"# occ\n"})
    v.publish(occupant, expected_current=genesis)

    gen = v.prepare(_capsule("cap"), {"areas/n1.md": b"# N1\n"})
    attempts = {"n": 0}

    def replan():
        attempts["n"] += 1
        # always re-plan against the stale genesis → perpetual conflict.
        return (gen, genesis, VaultSnapshot(base_generation=genesis, index_hash="h"))

    res = publish_with_cas(
        v, gen, expected_current=genesis,
        snapshot=VaultSnapshot(base_generation=genesis, index_hash="h"),
        read_current=lambda: {}, replan=replan,
        policy=RetryPolicy(max_attempts=3),
    )
    assert res.outcome == "blocked"  # terminal, not a livelock
    assert attempts["n"] >= 1


def test_concurrent_publishers_serialize_no_lost_generation(tmp_path: Path) -> None:
    # Review BUG1 regression: two publishers both plan against genesis. The
    # publish lock makes CAS a real test-and-set — one publishes, the other
    # sees CURRENT moved and aborts (never both succeed / silently lose one).
    v = _vault(tmp_path)
    genesis = v.current_generation()
    gA = v.prepare(_capsule("capA"), {"areas/a.md": b"# A\n"})
    gB = v.prepare(_capsule("capB"), {"areas/b.md": b"# B\n"})
    rA = v.publish(gA, expected_current=genesis)
    rB = v.publish(gB, expected_current=genesis)  # stale base now
    outcomes = sorted([rA.outcome, rB.outcome])
    assert outcomes == ["cas_conflict", "published"]
    # CURRENT is exactly the one that published; nothing silently lost.
    winner = gA if rA.outcome == "published" else gB
    assert v.current_generation() == winner


def test_recover_gcs_orphan_uncommitted_generation(tmp_path: Path) -> None:
    # Review BUG2 regression: simulate a crash between promote and pointer swap
    # — a generations/<gen> dir with NO COMMITTED marker and not CURRENT. It
    # never committed, so recover() collects it (no permanent leak).
    v = _vault(tmp_path)
    genesis = v.current_generation()
    orphan_dir = v.generation_dir("gen_orphan")
    orphan_dir.mkdir(parents=True)
    (orphan_dir / "areas/x.md").parent.mkdir(parents=True, exist_ok=True)
    (orphan_dir / "areas/x.md").write_bytes(b"# orphan\n")  # promoted, never committed
    assert orphan_dir.is_dir()
    v2 = VersionedVault(tmp_path / "pub")
    v2.recover()
    assert not orphan_dir.exists()  # orphan collected
    assert v2.generation_dir(genesis).is_dir()  # committed genesis survives


def test_recover_keeps_committed_superseded_generation(tmp_path: Path) -> None:
    # A committed generation that is no longer CURRENT (superseded) must NOT be
    # GC'd — readers may still hold it.
    v = _vault(tmp_path)
    genesis = v.current_generation()
    g1 = v.prepare(_capsule("cap1"), {"areas/n1.md": b"# N1\n"})
    v.publish(g1, expected_current=genesis)
    g2 = v.prepare(_capsule("cap2"), {"areas/n2.md": b"# N2\n"})
    v.publish(g2, expected_current=g1)  # supersedes g1; g1 still committed
    v.recover()
    assert v.generation_dir(g1).is_dir()  # committed-but-superseded survives
    assert v.current_generation() == g2


def test_prepare_rejects_self_referential_path_cleanly(tmp_path: Path) -> None:
    # Review BUG3 regression: a rel path resolving to the gen dir itself must
    # raise a clean PublicationError, not an uncaught IsADirectoryError.
    v = _vault(tmp_path)
    for bad in (".", "", "a/.."):
        with pytest.raises(PublicationError):
            v.prepare(_capsule(), {bad: b"x"})


def test_prepare_rejects_reserved_control_filenames(tmp_path: Path) -> None:
    # Review nit: a write-set path colliding with a control marker at the gen
    # root must be rejected (else it could mask an uncommitted orphan from GC).
    v = _vault(tmp_path)
    for reserved in ("COMMITTED", "ACKNOWLEDGED", "capsule.json"):
        with pytest.raises(PublicationError):
            v.prepare(_capsule(), {reserved: b"x"})
    # the same names UNDER a subdir are fine (only the root is reserved).
    gen = v.prepare(_capsule(), {"areas/COMMITTED": b"ok"})
    assert (v._staging / gen / "areas/COMMITTED").read_bytes() == b"ok"


def test_publish_with_cas_succeeds_when_replan_resolves(tmp_path: Path) -> None:
    v = _vault(tmp_path)
    genesis = v.current_generation()
    gen = v.prepare(_capsule(), {"areas/n1.md": b"# N1\n"})
    # first attempt: expected_current is wrong; replan supplies the correct one.
    def replan():
        return (gen, genesis, VaultSnapshot(base_generation=genesis, index_hash="h"))
    res = publish_with_cas(
        v, gen, expected_current="WRONG",
        snapshot=VaultSnapshot(base_generation=genesis, index_hash="h"),
        read_current=lambda: {}, replan=replan,
        policy=RetryPolicy(max_attempts=3),
    )
    assert res.outcome == "published"
    assert v.current_generation() == gen
