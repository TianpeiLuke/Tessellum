"""Composer v4 Phase 1 smoke — resume manifest.

Covers:
  - Delta-patch upsert / add_attempt / mark_* transitions.
  - Atomic write + ``.bak`` rotation (last-3 kept).
  - Corrupt main file → recovers from newest good ``.bak``.
  - Orphaned ``.tmp`` sweep on load.
  - ``reclaim_stale``: own rows untouched, stale foreign rows requeued,
    fresh foreign rows spared, terminal rows never touched.
  - ``claim`` contention: second claim on a live leaf fails.
  - ``rebuild_from_vault``: done-status derived from files on disk.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tessellum.composer import (
    AttemptRecord,
    Manifest,
    ManifestEntry,
    ManifestError,
)


# ── Delta-patch by id (1.1) ────────────────────────────────────────────────


def test_upsert_entry_delta_patches_one_key() -> None:
    m = Manifest()
    m.upsert_entry(ManifestEntry(leaf_id="a"))
    m.upsert_entry(ManifestEntry(leaf_id="b", status="done"))
    assert set(m.entries) == {"a", "b"}
    assert m.entries["a"].status == "pending"
    assert m.entries["b"].status == "done"

    # Patching one leaf leaves the other object identity intact.
    a_before = m.entries["a"]
    m.mark_done("b")
    assert m.entries["a"] is a_before
    assert m.entries["b"].status == "done"


def test_upsert_rejects_unknown_status() -> None:
    m = Manifest()
    with pytest.raises(ManifestError):
        m.upsert_entry(ManifestEntry(leaf_id="a", status="frobnicated"))


def test_add_attempt_appends_and_autocreates() -> None:
    m = Manifest()
    # Leaf is unknown → add_attempt creates a pending entry first.
    m.add_attempt("a", AttemptRecord(attempt_n=1, outcome="logic", gates_failed=("schema",)))
    m.add_attempt("a", AttemptRecord(attempt_n=2, outcome="success", cost=3.0, at=100.0))
    entry = m.entries["a"]
    assert entry.status == "pending"
    assert len(entry.attempts) == 2
    assert entry.attempts[0].outcome == "logic"
    assert entry.attempts[0].gates_failed == ("schema",)
    assert entry.attempts[1].outcome == "success"
    assert entry.attempts[1].cost == 3.0


def test_mark_transitions() -> None:
    m = Manifest()
    m.mark_in_progress("a", run_id="run-1", now=10.0)
    assert m.entries["a"].status == "in_progress"
    assert m.entries["a"].run_id == "run-1"
    assert m.entries["a"].heartbeat == 10.0

    m.mark_blocked("b", blocked_by=["a", "c"])
    assert m.entries["b"].status == "blocked"
    assert m.entries["b"].blocked_by == ("a", "c")

    m.mark_done("a")
    assert m.entries["a"].status == "done"
    # mark_done clears heartbeat (no longer running) but keeps provenance.
    assert m.entries["a"].heartbeat is None
    assert m.entries["a"].run_id == "run-1"


# ── Atomic write + rotation (1.2 / 1.3) ────────────────────────────────────


def test_save_writes_atomically_and_loads_back(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    m = Manifest(path=path)
    m.mark_in_progress("a", run_id="run-1", now=5.0)
    m.add_attempt("a", AttemptRecord(attempt_n=1, outcome="success", at=5.0))
    m.save()

    assert path.exists()
    # No orphan .tmp left behind after a clean save.
    assert list(tmp_path.glob("*.tmp")) == []

    reloaded = Manifest.load(path)
    assert reloaded.entries["a"].status == "in_progress"
    assert reloaded.entries["a"].run_id == "run-1"
    assert reloaded.entries["a"].heartbeat == 5.0
    assert reloaded.entries["a"].attempts[0].outcome == "success"


def test_save_rotates_backups_last_three(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    bak = path.with_name("manifest.json.bak")
    bak1 = path.with_name("manifest.json.bak.1")
    bak2 = path.with_name("manifest.json.bak.2")

    m = Manifest(path=path)
    # Save v1 (no prior file → no backup yet).
    m.mark_done("v1")
    m.save()
    assert not bak.exists()

    # Save v2 → v1 rotates to .bak.
    m.mark_done("v2")
    m.save()
    assert bak.exists()
    assert not bak1.exists()

    # Save v3 → .bak→.bak.1, current→.bak.
    m.mark_done("v3")
    m.save()
    assert bak.exists() and bak1.exists()
    assert not bak2.exists()

    # Save v4 → three backups now present, no .bak.3.
    m.mark_done("v4")
    m.save()
    assert bak.exists() and bak1.exists() and bak2.exists()
    assert not path.with_name("manifest.json.bak.3").exists()

    # .bak is the most-recent prior version (has v1..v3 but not v4).
    bak_payload = json.loads(bak.read_text(encoding="utf-8"))
    assert "v3" in bak_payload["entries"]
    assert "v4" not in bak_payload["entries"]
    # .bak.2 is the oldest kept version (v1 only).
    bak2_payload = json.loads(bak2.read_text(encoding="utf-8"))
    assert "v1" in bak2_payload["entries"]
    assert "v2" not in bak2_payload["entries"]


def test_save_without_path_raises() -> None:
    with pytest.raises(ManifestError):
        Manifest().save()


# ── Corruption recovery + orphan sweep ─────────────────────────────────────


def test_corrupt_main_recovers_from_bak(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    m = Manifest(path=path)
    m.mark_done("good")
    m.save()  # v1
    m.mark_in_progress("later", run_id="r", now=1.0)
    m.save()  # v2 → v1 (with "good", without "later") rotated to .bak

    # Corrupt the main file.
    path.write_text("}{ not json", encoding="utf-8")

    recovered = Manifest.load(path)
    # Falls back to the newest good backup (v1: has "good", not "later").
    assert "good" in recovered.entries
    assert "later" not in recovered.entries
    assert recovered.entries["good"].status == "done"


def test_corrupt_everything_starts_empty(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text("garbage", encoding="utf-8")
    path.with_name("manifest.json.bak").write_text("also garbage", encoding="utf-8")

    recovered = Manifest.load(path)
    assert recovered.entries == {}
    assert recovered.path == path


def test_shape_invalid_json_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    # Valid JSON, wrong shape (bad status) → must be rejected, empty start.
    path.write_text(
        json.dumps({"version": "1.0", "entries": {"a": {"leaf_id": "a", "status": "??"}}}),
        encoding="utf-8",
    )
    recovered = Manifest.load(path)
    assert recovered.entries == {}


def test_orphan_tmp_swept_on_load(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    m = Manifest(path=path)
    m.mark_done("a")
    m.save()

    # Simulate a crashed writer's leftover temp files.
    orphan1 = path.with_name("manifest.json.12345.deadbeef.tmp")
    orphan2 = path.with_name("manifest.json.999.cafef00d.tmp")
    orphan1.write_text("partial", encoding="utf-8")
    orphan2.write_text("partial", encoding="utf-8")
    assert orphan1.exists() and orphan2.exists()

    Manifest.load(path)
    assert not orphan1.exists()
    assert not orphan2.exists()
    # The real manifest is untouched.
    assert path.exists()


# ── Owner-scoped reclaim (1.2) ─────────────────────────────────────────────


def test_reclaim_stale_requeues_foreign_stale_only() -> None:
    m = Manifest()
    # Own row — must never be reclaimed even if "stale".
    m.mark_in_progress("own", run_id="run-current", now=0.0)
    # Foreign stale row — should be requeued.
    m.mark_in_progress("foreign_stale", run_id="run-dead", now=0.0)
    # Foreign fresh row — recent heartbeat, spared.
    m.mark_in_progress("foreign_fresh", run_id="run-other", now=95.0)
    # Terminal rows — never touched.
    m.mark_done("done_row")
    m.mark_blocked("blocked_row", blocked_by=["x"])

    reclaimed = m.reclaim_stale(
        current_run_id="run-current", now=100.0, stale_secs=30.0
    )

    assert reclaimed == ["foreign_stale"]
    # Own row untouched.
    assert m.entries["own"].status == "in_progress"
    assert m.entries["own"].run_id == "run-current"
    # Foreign stale requeued + de-owned.
    assert m.entries["foreign_stale"].status == "pending"
    assert m.entries["foreign_stale"].run_id is None
    assert m.entries["foreign_stale"].heartbeat is None
    # Foreign fresh spared.
    assert m.entries["foreign_fresh"].status == "in_progress"
    # Terminal rows spared.
    assert m.entries["done_row"].status == "done"
    assert m.entries["blocked_row"].status == "blocked"


def test_reclaim_stale_treats_missing_heartbeat_as_stale() -> None:
    m = Manifest()
    # Foreign in_progress with no heartbeat can't prove liveness → stale.
    m.upsert_entry(
        ManifestEntry(
            leaf_id="foreign", status="in_progress", run_id="run-dead", heartbeat=None
        )
    )
    reclaimed = m.reclaim_stale(current_run_id="me", now=100.0, stale_secs=30.0)
    assert reclaimed == ["foreign"]
    assert m.entries["foreign"].status == "pending"


# ── Atomic claim + double-dispatch (1.2) ───────────────────────────────────


def test_claim_contention_second_claim_fails() -> None:
    m = Manifest()
    assert m.claim("a", run_id="run-1", now=1.0) is True
    assert m.entries["a"].status == "in_progress"
    assert m.entries["a"].run_id == "run-1"

    # A second worker (even a different run) cannot claim a live leaf.
    assert m.claim("a", run_id="run-2", now=2.0) is False
    assert m.entries["a"].run_id == "run-1"  # unchanged


def test_claim_absent_and_pending_succeed_terminal_fail() -> None:
    m = Manifest()
    # Absent → claimable.
    assert m.claim("absent", run_id="r", now=1.0) is True

    # Explicitly pending → claimable.
    m.upsert_entry(ManifestEntry(leaf_id="pend", status="pending"))
    assert m.claim("pend", run_id="r", now=1.0) is True

    # done / blocked → not claimable.
    m.mark_done("dn")
    m.mark_blocked("bl", blocked_by=["x"])
    assert m.claim("dn", run_id="r", now=1.0) is False
    assert m.claim("bl", run_id="r", now=1.0) is False


def test_double_dispatch_mark_done_before_release_closes_window() -> None:
    """mark_done (durable-commit) removes the leaf from the claimable set."""
    m = Manifest()
    assert m.claim("a", run_id="run-1", now=1.0) is True
    # Worker commits done BEFORE releasing — the correct discipline.
    m.mark_done("a")
    # A late second worker can no longer claim it → no redundant redo.
    assert m.claim("a", run_id="run-2", now=2.0) is False
    assert m.entries["a"].status == "done"


def test_touch_only_own_in_progress() -> None:
    m = Manifest()
    m.mark_in_progress("a", run_id="run-1", now=1.0)
    assert m.touch("a", run_id="run-1", now=5.0) is True
    assert m.entries["a"].heartbeat == 5.0
    # Wrong owner → no-op.
    assert m.touch("a", run_id="run-2", now=9.0) is False
    assert m.entries["a"].heartbeat == 5.0
    # Non-in_progress → no-op.
    m.mark_done("a")
    assert m.touch("a", run_id="run-1", now=12.0) is False


# ── Rebuildable projection (IDENT-2) ───────────────────────────────────────


def test_rebuild_from_vault_derives_done_from_disk(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / "notes").mkdir(parents=True)
    existing = vault / "notes" / "leaf_a.md"
    existing.write_text("# a", encoding="utf-8")

    expected = {
        "a": Path("notes/leaf_a.md"),   # exists → done
        "b": Path("notes/leaf_b.md"),   # missing → pending
    }
    m = Manifest.rebuild_from_vault(vault, expected, path=tmp_path / "m.json")
    assert m.entries["a"].status == "done"
    assert m.entries["b"].status == "pending"
    assert m.path == tmp_path / "m.json"


def test_rebuild_from_vault_absolute_paths(tmp_path: Path) -> None:
    target = tmp_path / "abs_leaf.md"
    target.write_text("x", encoding="utf-8")
    m = Manifest.rebuild_from_vault(
        tmp_path, {"a": target, "b": tmp_path / "nope.md"}
    )
    assert m.entries["a"].status == "done"
    assert m.entries["b"].status == "pending"


def test_rebuild_roundtrips_through_save_load(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "a.md").write_text("x", encoding="utf-8")
    path = tmp_path / "m.json"
    m = Manifest.rebuild_from_vault(
        vault, {"a": Path("a.md"), "b": Path("b.md")}, path=path
    )
    m.save()
    reloaded = Manifest.load(path)
    assert reloaded.entries["a"].status == "done"
    assert reloaded.entries["b"].status == "pending"
