"""R2.1 (FZ 20k9c1a1a1b7c2k2a1b) — the hardened renewal actor.

Run 6's lease death was undiagnosable because the renewal thread could die
silently (one-shot-fatal) and left no record. These tests pin the new
contract: transient errors retry on cadence; escalation only when no renewal
lands within one TTL; LeaseLostError terminal immediately; every beat
journaled; and — the schedule test that structurally refutes the original F6
narrative — a blocked main thread longer than the TTL survives under a live
renewal actor.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from tessellum.runtime.admission import admit_path
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.routing import LANE_HINTS
from tessellum.runtime.store import LeaseLostError, RuntimeStore
from tessellum.runtime.supervisor import Supervisor


def _runtime(tmp_path: Path):
    paths = RuntimePaths.discover(tmp_path)
    paths.ensure_runtime_dirs()
    paths.inbox.mkdir()
    paths.vault.mkdir()
    paths.skills.mkdir(parents=True)
    for lane in LANE_HINTS:
        (paths.inbox / lane).mkdir()
    source = paths.inbox / "papers" / "p.md"
    source.write_text("evidence", encoding="utf-8")
    store = RuntimeStore.open(paths.db)
    admitted, _ = admit_path(source, paths=paths, store=store)
    job = store.claim_next("w", lease_ttl=60.0, max_attempts=3)
    assert job is not None and job.lease is not None
    sup = Supervisor(
        store=store, paths=paths, executor=object(),  # type: ignore[arg-type]
        owner_id="w", rebuild_index=False,
    )
    return paths, store, sup, job


def _journal(paths: RuntimePaths, job_id: str) -> list[dict]:
    fp = paths.job_artifacts(job_id) / "runs" / "heartbeats.jsonl"
    if not fp.is_file():
        return []
    return [json.loads(line) for line in fp.read_text().splitlines()]


def test_renewal_survives_transient_error(tmp_path: Path) -> None:
    paths, store, sup, job = _runtime(tmp_path)
    real = store.heartbeat
    calls = {"n": 0}

    def flaky(job_id, lease, *, lease_ttl):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("transient db hiccup")
        return real(job_id, lease, lease_ttl=lease_ttl)

    store.heartbeat = flaky  # type: ignore[method-assign]
    with sup._heartbeat(job.job_id, job.lease, 0.6) as assert_healthy:
        time.sleep(0.9)  # spans several 0.2s cadence ticks
        assert_healthy()  # transient error did NOT kill the actor
    recs = _journal(paths, job.job_id)
    assert any(not r["ok"] for r in recs)   # the failure was journaled
    assert any(r["ok"] for r in recs)       # and renewal resumed


def test_renewal_escalates_when_no_beat_lands_within_ttl(tmp_path: Path) -> None:
    paths, store, sup, job = _runtime(tmp_path)

    def always_fail(job_id, lease, *, lease_ttl):
        raise RuntimeError("db down")

    store.heartbeat = always_fail  # type: ignore[method-assign]
    with pytest.raises(RuntimeError, match="could not land within one TTL"):
        with sup._heartbeat(job.job_id, job.lease, 0.45):
            time.sleep(1.2)  # > TTL of continuous failure → escalation
    assert all(not r["ok"] for r in _journal(paths, job.job_id))


def test_lease_lost_is_terminal_immediately(tmp_path: Path) -> None:
    paths, store, sup, job = _runtime(tmp_path)

    def fenced(job_id, lease, *, lease_ttl):
        raise LeaseLostError("fenced out")

    store.heartbeat = fenced  # type: ignore[method-assign]
    with pytest.raises(LeaseLostError):
        with sup._heartbeat(job.job_id, job.lease, 0.6):
            time.sleep(0.5)  # well under TTL: terminal class escalates anyway
    recs = _journal(paths, job.job_id)
    assert any(r["error"] and r["error"].startswith("terminal:") for r in recs)


def test_blocked_main_thread_longer_than_ttl_survives(tmp_path: Path) -> None:
    """The run-6 schedule test: with a LIVE renewal actor, a 'blocked call'
    2.5x the TTL keeps the lease valid throughout — structurally refuting the
    original F6 narrative ('no heartbeat can renew inside a blocked call')."""
    paths, store, sup, job = _runtime(tmp_path)
    # re-lease tight so the claim TTL (60s) doesn't mask the schedule
    store.heartbeat(job.job_id, job.lease, lease_ttl=1.0)
    with sup._heartbeat(job.job_id, job.lease, 1.0) as assert_healthy:
        time.sleep(2.5)  # the "blocked call", 2.5x TTL
        assert_healthy()
        row = store.get(job.job_id)
        assert row.lease is not None
        assert row.lease.expires_at > time.time()  # renewed THROUGH the block
