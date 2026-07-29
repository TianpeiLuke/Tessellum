from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.runtime.models import JobState, Lease, WorkRequest
from tessellum.runtime.store import LeaseLostError, RuntimeStore, TransitionError


def _request(event: str = "papers/a.md") -> WorkRequest:
    return WorkRequest(
        source="inbox",
        source_event_id=event,
        intent="digest",
        payload_ref="sha256:" + "a" * 64,
        original_path=f"/tmp/{event}",
        lane="papers",
    )


def test_admit_is_idempotent_and_appends_event(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    first, created = store.admit(_request(), now=10.0)
    second, duplicate = store.admit(_request(), now=11.0)
    assert created is True
    assert duplicate is False
    assert second.job_id == first.job_id
    assert [event.event_type for event in store.events(first.job_id)] == ["admitted"]


def test_claim_is_single_owner_and_generation_fenced(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=20.0)
    assert claimed is not None
    assert claimed.job_id == job.job_id
    assert claimed.state == JobState.ROUTED
    assert claimed.lease == Lease("worker-a", 1, 31.0)
    assert store.claim_next("worker-b", now=12.0) is None
    with pytest.raises(LeaseLostError):
        store.set_routing(
            job.job_id,
            Lease("worker-b", 1, 31.0),
            capability="native_digestion",
            skill_digest="x",
        )


def test_lease_assertion_and_guard_check_expiry(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=20.0)
    assert claimed is not None
    assert claimed.lease is not None

    assert store.assert_lease(job.job_id, claimed.lease, now=30.0).job_id == job.job_id
    effects: list[str] = []
    with store.lease_guard(job.job_id, claimed.lease, now=30.0):
        effects.append("published")
    assert effects == ["published"]

    with pytest.raises(LeaseLostError):
        store.assert_lease(job.job_id, claimed.lease, now=31.0)
    with pytest.raises(LeaseLostError):
        with store.lease_guard(job.job_id, claimed.lease, now=31.0):
            effects.append("must-not-run")
    assert effects == ["published"]


def test_leased_transition_requires_matching_lease(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=20.0)
    assert claimed is not None

    with pytest.raises(LeaseLostError, match="lease required"):
        store.transition(
            job.job_id,
            expected=JobState.ROUTED,
            target=JobState.PLANNING,
            now=12.0,
        )


def test_terminal_transition_clears_lease_atomically(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=20.0)
    assert claimed is not None
    assert claimed.lease is not None

    dead = store.transition(
        job.job_id,
        expected=JobState.ROUTED,
        target=JobState.DEAD_LETTER,
        lease=claimed.lease,
        now=12.0,
    )

    assert dead.lease is None


def test_stale_leased_cancellation_becomes_cancelled(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=5.0)
    assert claimed is not None

    requested = store.request_cancel(job.job_id, now=12.0)
    assert requested.cancel_requested is True
    assert requested.state == JobState.ROUTED
    assert store.claim_next("worker-b", now=16.0) is None

    cancelled = store.get(job.job_id)
    assert cancelled is not None
    assert cancelled.state == JobState.CANCELLED
    assert cancelled.lease is None


def test_reap_expired_leases_requeues_stranded_running_job(tmp_path: Path) -> None:
    """T4 (FZ 20k9d6a): an active sweep reclaims an expired-lease in-flight job
    even when NO claim happens (a dead worker's leaf would otherwise strand)."""
    store = RuntimeStore.open(tmp_path / "runtime.db")
    store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=5.0)  # expires 16.0
    assert claimed is not None and claimed.state == JobState.ROUTED

    # No new claim; sweep AFTER the lease expires.
    reaped = store.reap_expired_leases(now=100.0)
    assert reaped == 1
    job = store.get(claimed.job_id)
    # capability/skill not yet set (never routed to READY) → back to ADMITTED, claimable.
    assert job.state in {JobState.ADMITTED, JobState.READY}
    assert job.lease is None
    assert "lease_reclaimed" in {e.event_type for e in store.events(claimed.job_id)}


def test_reap_expired_leases_dead_letters_at_max_attempts(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    store.admit(_request(), now=10.0)
    # burn the attempts so the next reap dead-letters instead of requeuing
    for i in range(3):
        c = store.claim_next("w", now=11.0 + i, lease_ttl=1.0, max_attempts=99)
        assert c is not None
    reaped = store.reap_expired_leases(now=1000.0, max_attempts=1)
    assert reaped == 1
    job = store.get(c.job_id)
    assert job.state == JobState.DEAD_LETTER
    assert "state:dead_letter" in {e.event_type for e in store.events(c.job_id)}


def test_reap_expired_leases_noop_when_lease_live(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=100.0)  # LIVE
    assert claimed is not None
    reaped = store.reap_expired_leases(now=12.0)  # lease not yet expired
    assert reaped == 0
    assert store.get(claimed.job_id).state == JobState.ROUTED


def test_force_cancel_fences_live_worker_and_cancels(tmp_path: Path) -> None:
    """T2 (FZ 20k9d6a): force_cancel on a job with a LIVE lease bumps the lease
    generation + nulls the owner, so the in-flight worker's next transition
    fails _check_lease (the SIGKILL fence), and the job lands CANCELLED."""
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=100.0)  # lease still LIVE
    assert claimed is not None and claimed.lease is not None
    stale_lease = claimed.lease  # the worker holds this

    forced = store.force_cancel(job.job_id, now=12.0)
    assert forced.state == JobState.CANCELLED
    assert forced.lease is None  # the fence: owner nulled + generation bumped
    assert forced.cancel_requested is True

    # The fenced worker can no longer advance the job — its transition is
    # rejected (the state is now `cancelled`, not the `routed` it expects, AND
    # its lease no longer matches). Either rejection proves the SIGKILL held.
    with pytest.raises((TransitionError, LeaseLostError)):
        store.transition(
            job.job_id,
            expected=JobState.ROUTED,
            target=JobState.PLANNING,
            lease=stale_lease,
            now=13.0,
        )
    assert "state:cancelled" in {e.event_type for e in store.events(job.job_id)}


def test_force_cancel_is_idempotent_on_terminal(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    store.claim_next("worker-a", now=11.0, lease_ttl=100.0)
    store.force_cancel(job.job_id, now=12.0)
    again = store.force_cancel(job.job_id, now=13.0)  # no error, unchanged
    assert again.state == JobState.CANCELLED


def test_force_cancel_unknown_job_raises(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    with pytest.raises(KeyError):
        store.force_cancel("nope", now=10.0)


def test_cancelled_failure_is_not_scheduled_for_retry(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=20.0)
    assert claimed is not None
    assert claimed.lease is not None
    store.request_cancel(job.job_id, now=12.0)

    scheduled = store.schedule_retry(
        job.job_id,
        claimed.lease,
        error="RuntimeError: transient",
        not_before=30.0,
        now=13.0,
    )

    assert scheduled.state == JobState.CANCELLED
    assert scheduled.lease is None
    assert "retry_scheduled" not in {
        event.event_type for event in store.events(job.job_id)
    }


def test_cancelled_retry_wait_does_not_strand(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=20.0)
    assert claimed is not None
    assert claimed.lease is not None
    waiting = store.schedule_retry(
        job.job_id,
        claimed.lease,
        error="RuntimeError: transient",
        not_before=30.0,
        now=12.0,
    )
    assert waiting.state == JobState.RETRY_WAIT

    cancelled = store.request_cancel(job.job_id, now=13.0)
    assert cancelled.state == JobState.CANCELLED
    assert store.promote_due_retries(now=31.0) == 0
    assert store.get(job.job_id).state == JobState.CANCELLED  # type: ignore[union-attr]


def test_reclaim_preserves_complete_routing_pin(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=5.0)
    assert claimed is not None
    assert claimed.lease is not None
    store.set_routing(
        job.job_id,
        claimed.lease,
        capability="native_digestion",
        skill_digest="pinned",
        now=12.0,
    )

    reclaimed = store.claim_next("worker-b", now=16.0, lease_ttl=5.0)
    assert reclaimed is not None
    assert reclaimed.state == JobState.RUNNING
    assert reclaimed.capability == "native_digestion"
    assert reclaimed.skill_digest == "pinned"
    assert reclaimed.lease == Lease("worker-b", 2, 21.0)


def test_reclaim_repairs_absent_routing_metadata(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=5.0)
    assert claimed is not None

    reclaimed = store.claim_next("worker-b", now=16.0, lease_ttl=5.0)
    assert reclaimed is not None
    assert reclaimed.state == JobState.ROUTED
    assert reclaimed.capability is None
    assert reclaimed.skill_digest is None
    assert reclaimed.lease == Lease("worker-b", 2, 21.0)


def test_expired_claim_dead_letters_at_attempt_limit(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next(
        "worker-a",
        now=11.0,
        lease_ttl=5.0,
        max_attempts=1,
    )
    assert claimed is not None

    assert (
        store.claim_next(
            "worker-b",
            now=16.0,
            lease_ttl=5.0,
            max_attempts=1,
        )
        is None
    )
    exhausted = store.get(job.job_id)
    assert exhausted is not None
    assert exhausted.state == JobState.DEAD_LETTER
    assert exhausted.lease is None
    assert exhausted.last_error == "lease expired after maximum attempts"


def test_stale_committing_claim_resumes_commit_and_is_bounded(
    tmp_path: Path,
) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next(
        "worker-a",
        now=11.0,
        lease_ttl=5.0,
        max_attempts=2,
    )
    assert claimed is not None
    assert claimed.lease is not None
    routed = store.set_routing(
        job.job_id,
        claimed.lease,
        capability="native_digestion",
        skill_digest="pinned",
        now=12.0,
    )
    planning = store.transition(
        job.job_id,
        expected=routed.state,
        target=JobState.PLANNING,
        lease=claimed.lease,
        now=12.1,
    )
    ready = store.transition(
        job.job_id,
        expected=planning.state,
        target=JobState.READY,
        lease=claimed.lease,
        now=12.2,
    )
    running = store.transition(
        job.job_id,
        expected=ready.state,
        target=JobState.RUNNING,
        lease=claimed.lease,
        now=12.3,
    )
    committing = store.transition(
        job.job_id,
        expected=running.state,
        target=JobState.COMMITTING,
        lease=claimed.lease,
        now=12.4,
    )
    assert committing.commit_attempts == 1

    resumed = store.claim_next(
        "worker-b",
        now=16.0,
        lease_ttl=5.0,
        max_attempts=2,
    )
    assert resumed is not None
    assert resumed.state == JobState.COMMITTING
    assert resumed.attempts == 1
    assert resumed.commit_attempts == 2

    assert store.claim_next(
        "worker-c",
        now=21.0,
        lease_ttl=5.0,
        max_attempts=2,
    ) is None
    exhausted = store.get(job.job_id)
    assert exhausted is not None
    assert exhausted.state == JobState.DEAD_LETTER
    assert exhausted.last_error == "commit lease expired after maximum attempts"


def test_commit_retry_remains_committing(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    claimed = store.claim_next("worker-a", now=11.0, lease_ttl=5.0)
    assert claimed is not None
    assert claimed.lease is not None
    routed = store.set_routing(
        job.job_id,
        claimed.lease,
        capability="native_digestion",
        skill_digest="pinned",
        now=12.0,
    )
    planning = store.transition(
        job.job_id,
        expected=routed.state,
        target=JobState.PLANNING,
        lease=claimed.lease,
        now=12.1,
    )
    ready = store.transition(
        job.job_id,
        expected=planning.state,
        target=JobState.READY,
        lease=claimed.lease,
        now=12.2,
    )
    running = store.transition(
        job.job_id,
        expected=ready.state,
        target=JobState.RUNNING,
        lease=claimed.lease,
        now=12.3,
    )
    committing = store.transition(
        job.job_id,
        expected=running.state,
        target=JobState.COMMITTING,
        lease=claimed.lease,
        now=12.4,
    )

    waiting = store.schedule_commit_retry(
        job.job_id,
        committing.lease,  # type: ignore[arg-type]
        error="OSError: interrupted",
        not_before=30.0,
        now=13.0,
    )

    assert waiting.state == JobState.COMMITTING
    assert waiting.lease is None
    assert waiting.request.not_before == 30.0


def test_transition_table_fails_closed(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    with pytest.raises(TransitionError):
        store.transition(
            job.job_id,
            expected=JobState.ADMITTED,
            target=JobState.COMPLETE,
        )


def test_terminal_retry_creates_linked_generation(tmp_path: Path) -> None:
    store = RuntimeStore.open(tmp_path / "runtime.db")
    job, _ = store.admit(_request(), now=10.0)
    dead = store.transition(
        job.job_id,
        expected=JobState.ADMITTED,
        target=JobState.DEAD_LETTER,
        now=11.0,
    )
    retried = store.retry_terminal(dead.job_id, now=12.0)
    assert retried.job_id != dead.job_id
    assert retried.supersedes_job_id == dead.job_id
    assert retried.state == JobState.ADMITTED
