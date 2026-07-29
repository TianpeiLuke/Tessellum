"""T1 (FZ 20k9d6a) — the runtime task-manager status read surface.

Covers the aggregate per-job view, the single-job per-leaf drill-down (from the
durable Manifest), lease-expiry flagging, and the read-only guarantee. Uses the
real RuntimeStore + Manifest, no LLM/backend.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from tessellum.cli.runtime import (
    _leaf_status_for_job,
    _render_status,
    _status_row,
)
from tessellum.composer.manifest import Manifest, ManifestEntry
from tessellum.runtime.models import JobState, WorkRequest
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.store import RuntimeStore


def _request(event: str) -> WorkRequest:
    return WorkRequest(
        source="inbox",
        source_event_id=event,
        intent="digest",
        payload_ref="sha256:" + "a" * 64,
        original_path=f"/tmp/{event}",
        lane="papers",
    )


def _paths(tmp: Path) -> RuntimePaths:
    paths = RuntimePaths.discover(tmp)
    paths.ensure_runtime_dirs()
    return paths


def _args(paths: RuntimePaths, *, job: str | None = None, limit: int = 100) -> argparse.Namespace:
    return argparse.Namespace(job=job, limit=limit, watch=False, json=True, interval=1.0)


def test_status_aggregate_lists_active_jobs(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    store = RuntimeStore.open(paths.db)
    store.admit(_request("a.md"), now=10.0)
    store.admit(_request("b.md"), now=11.0)
    snap = _render_status(paths, store, _args(paths))
    assert snap["counts"]["active"] == 2
    assert {r["phase"] for r in snap["active"]} == {JobState.ADMITTED.value}
    assert all("job_id" in r for r in snap["active"])


def test_status_flags_expired_lease(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    store = RuntimeStore.open(paths.db)
    store.admit(_request("a.md"), now=10.0)
    # claim → a lease expiring at now+ttl; render with now WELL past expiry
    store.claim_next("worker-a", now=11.0, lease_ttl=20.0)  # expires_at 31.0
    snap = _render_status(paths, store, _args(paths))
    row = snap["active"][0]
    # render uses real time.time() >> 31.0, so the lease reads expired
    assert row["lease_owner"] == "worker-a"
    assert row["lease_expired"] is True


def test_status_single_job_drilldown_no_manifest(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    store = RuntimeStore.open(paths.db)
    job, _ = store.admit(_request("a.md"), now=10.0)
    snap = _render_status(paths, store, _args(paths, job=job.job_id))
    assert snap["job_id"] == job.job_id
    assert snap["phase"] == JobState.ADMITTED.value
    assert snap["leaves"] is None  # pre-execute: no manifest yet
    assert snap["events"]  # the 'admitted' event is present


def test_status_single_job_drilldown_with_manifest(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    store = RuntimeStore.open(paths.db)
    job, _ = store.admit(_request("a.md"), now=10.0)
    # seed a per-leaf manifest at the job's artifact dir
    art = paths.job_artifacts(job.job_id)
    art.mkdir(parents=True, exist_ok=True)
    m = Manifest(path=art / "manifest.json")
    m.upsert_entry(ManifestEntry(leaf_id="note-1", status="done"))
    m.upsert_entry(ManifestEntry(leaf_id="note-2", status="in_progress",
                                 run_id="run-x", heartbeat=10.0))
    m.upsert_entry(ManifestEntry(leaf_id="note-3", status="pending"))
    m.save()

    leaves = _leaf_status_for_job(paths, job.job_id)
    assert leaves is not None
    assert leaves["counts"] == {"done": 1, "in_progress": 1, "pending": 1}
    by_id = {lf["leaf_id"]: lf for lf in leaves["leaves"]}
    assert by_id["note-2"]["status"] == "in_progress"
    assert by_id["note-2"]["heartbeat_age"] is not None  # in_progress carries a heartbeat
    assert by_id["note-1"]["heartbeat_age"] is None       # done has none


def test_status_job_not_found(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    store = RuntimeStore.open(paths.db)
    snap = _render_status(paths, store, _args(paths, job="nope"))
    assert "error" in snap


def test_status_row_is_read_only(tmp_path: Path) -> None:
    """The status surface must never mutate a job (read plane is read-only)."""
    paths = _paths(tmp_path)
    store = RuntimeStore.open(paths.db)
    job, _ = store.admit(_request("a.md"), now=10.0)
    _render_status(paths, store, _args(paths))
    _render_status(paths, store, _args(paths, job=job.job_id))
    after = store.get(job.job_id)
    assert after.state == JobState.ADMITTED  # unchanged
    assert [e.event_type for e in store.events(job.job_id)] == ["admitted"]  # no new events

    _ = _status_row(after, now=999999.0)  # pure projection, no side effect
    assert store.get(job.job_id).state == JobState.ADMITTED


# ── J1 (FZ 20k9c1a1a1b7c2k2): the composer-grain episodic view ───────────────


def test_composer_status_reads_checkpoints_and_attempts(tmp_path: Path) -> None:
    import json

    from tessellum.cli.runtime import _composer_status_for_job

    paths = _paths(tmp_path)
    runs = paths.job_artifacts("job-x") / "runs"
    (runs / "checkpoints").mkdir(parents=True)
    (runs / "checkpoints" / "01_plan.json").write_text("{}", encoding="utf-8")
    (runs / "checkpoints" / "02_augment.json").write_text("{}", encoding="utf-8")
    (runs / "attempts.jsonl").write_text(
        "\n".join([
            json.dumps({"kind": "success", "section_id": "write_plan", "attempt": 1}),
            json.dumps({"kind": "empty", "section_id": "read_draft", "attempt": 1,
                        "error": "empty response (stop_reason=end_turn)"}),
            json.dumps({"kind": "success", "section_id": "read_draft", "attempt": 2}),
        ]) + "\n",
        encoding="utf-8",
    )
    out = _composer_status_for_job(paths, "job-x")
    assert out["checkpoint"] == "02_augment"
    assert out["checkpoints"] == 2
    assert out["attempts"]["total"] == 3
    assert out["attempts"]["kinds"] == {"success": 2, "empty": 1}
    # the last NON-success record is what the operator needs first
    assert out["attempts"]["last_failure"] == {
        "step": "read_draft", "kind": "empty", "attempt": 1,
        "error": "empty response (stop_reason=end_turn)",
    }


def test_composer_status_absent_is_none(tmp_path: Path) -> None:
    from tessellum.cli.runtime import _composer_status_for_job

    paths = _paths(tmp_path)
    assert _composer_status_for_job(paths, "no-such-job") is None
