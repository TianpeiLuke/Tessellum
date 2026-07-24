from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from tessellum.runtime.admission import admit_path
from tessellum.runtime.executor import VaultEffectJournal
from tessellum.runtime.models import JobState
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.policy import RuntimePolicy
from tessellum.runtime.routing import LANE_HINTS, route_lane
from tessellum.runtime.store import LeaseLostError, RuntimeStore
from tessellum.runtime.supervisor import Supervisor


@dataclass
class _Result:
    completed: bool = True
    stopped_at: str | None = None


class _Executor:
    cancellation_check = None
    effect_guard = None

    def execute(self, job, lease, route, policy):
        assert route.capability == "native_digestion"
        assert lease.generation == 1
        assert self.effect_guard is not None
        with self.effect_guard():
            pass
        return _Result()


def _runtime(tmp_path: Path) -> tuple[RuntimePaths, RuntimeStore, Path]:
    paths = RuntimePaths.discover(tmp_path)
    paths.ensure_runtime_dirs()
    paths.inbox.mkdir()
    paths.vault.mkdir()
    paths.skills.mkdir(parents=True)
    for skill in (
        "skill_tessellum_plan_digestion",
        "skill_tessellum_augment_digestion_plan",
        "skill_tessellum_review_digestion_plan",
        "skill_tessellum_execute_digestion_plan",
    ):
        (paths.skills / f"{skill}.md").write_text(skill, encoding="utf-8")
    for lane in LANE_HINTS:
        (paths.inbox / lane).mkdir()
    source = paths.inbox / "papers" / "paper.md"
    source.write_text("evidence", encoding="utf-8")
    store = RuntimeStore.open(paths.db)
    return paths, store, source


def test_supervisor_closes_admit_to_archive_loop(tmp_path: Path) -> None:
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store)

    outcome = Supervisor(
        store=store,
        paths=paths,
        executor=_Executor(),  # type: ignore[arg-type]
        owner_id="test-worker",
        rebuild_index=False,
    ).work_once()

    completed = store.get(admitted.job_id)
    assert outcome.status == "complete"
    assert completed is not None
    assert completed.state == JobState.COMPLETE
    assert completed.lease is None
    assert completed.capability == "native_digestion"
    assert completed.skill_digest is not None
    assert not source.exists()
    assert Path(completed.result_path).read_text() == "evidence"


class _RecoveryObservingExecutor(_Executor):
    def __init__(self, observed: Path) -> None:
        self.observed = observed

    def execute(self, job, lease, route, policy):
        assert self.observed.read_text(encoding="utf-8") == "before"
        return super().execute(job, lease, route, policy)


def test_supervisor_recovers_abandoned_vault_effects_before_execution(
    tmp_path: Path,
) -> None:
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store)
    observed = paths.vault / "existing.md"
    observed.write_text("before", encoding="utf-8")
    journal = VaultEffectJournal(
        paths.vault,
        effect_guard=None,
        journal_dir=paths.artifacts / "crashed-job" / "vault-effects" / "1",
    )
    journal.record(observed)
    journal.record_postimage(observed, b"partial")
    observed.write_text("partial", encoding="utf-8")

    outcome = Supervisor(
        store=store,
        paths=paths,
        executor=_RecoveryObservingExecutor(observed),  # type: ignore[arg-type]
        owner_id="test-worker",
        rebuild_index=False,
    ).work_once()

    assert outcome.status == "complete"
    assert store.get(admitted.job_id).state == JobState.COMPLETE  # type: ignore[union-attr]


class _CommitDecisionExecutor(_Executor):
    def __init__(self, store: RuntimeStore) -> None:
        self.store = store
        self.job_id = ""
        self.accepted_state = None

    def execute(self, job, lease, route, policy):
        self.job_id = job.job_id
        return super().execute(job, lease, route, policy)

    def accept_uncommitted(self):
        current = self.store.get(self.job_id)
        assert current is not None
        self.accepted_state = current.state


def test_supervisor_persists_committing_before_accepting_vault_effects(
    tmp_path: Path,
) -> None:
    paths, store, source = _runtime(tmp_path)
    admit_path(source, paths=paths, store=store)
    executor = _CommitDecisionExecutor(store)

    outcome = Supervisor(
        store=store,
        paths=paths,
        executor=executor,  # type: ignore[arg-type]
        owner_id="test-worker",
        rebuild_index=False,
    ).work_once()

    assert outcome.status == "complete"
    assert executor.accepted_state == JobState.COMMITTING


class _AcceptanceFailureExecutor(_Executor):
    def __init__(self, paths: RuntimePaths) -> None:
        self.paths = paths
        self.journal = None
        self.note = paths.vault / "accepted.md"
        self.rolled_back = False

    def execute(self, job, lease, route, policy):
        self.journal = VaultEffectJournal(
            self.paths.vault,
            effect_guard=self.effect_guard,
            journal_dir=(
                self.paths.artifacts
                / job.job_id
                / "vault-effects"
                / str(lease.generation)
            ),
        )
        self.journal.record(self.note)
        self.journal.record_postimage(self.note, b"accepted")
        self.note.write_text("accepted", encoding="utf-8")
        return super().execute(job, lease, route, policy)

    def accept_uncommitted(self):
        raise RuntimeError("acceptance marker failed")

    def rollback_uncommitted(self):
        self.rolled_back = True
        assert self.journal is not None
        self.journal.rollback()


def test_acceptance_marker_failure_preserves_committing_output(
    tmp_path: Path,
    monkeypatch,
) -> None:
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store)
    executor = _AcceptanceFailureExecutor(paths)
    monkeypatch.setattr(
        "tessellum.runtime.supervisor.full_jitter_backoff",
        lambda *args, **kwargs: 0.0,
    )

    first = Supervisor(
        store=store,
        paths=paths,
        executor=executor,  # type: ignore[arg-type]
        owner_id="execute-worker",
        rebuild_index=False,
    ).work_once()

    accepted = store.get(admitted.job_id)
    assert first.status == "retry_wait"
    assert accepted is not None
    assert accepted.state == JobState.COMMITTING
    assert executor.rolled_back is False
    assert executor.note.read_text(encoding="utf-8") == "accepted"

    second_executor = _RecordingExecutor()
    second = Supervisor(
        store=store,
        paths=paths,
        executor=second_executor,  # type: ignore[arg-type]
        owner_id="commit-worker",
        rebuild_index=False,
    ).work_once()

    assert second.status == "complete"
    assert second_executor.calls == 0
    assert executor.note.read_text(encoding="utf-8") == "accepted"
    assert not source.exists()


class _RollbackObservingExecutor(_Executor):
    def __init__(self, lock_active: list[bool]) -> None:
        self.lock_active = lock_active
        self.rolled_back = False

    def rollback_uncommitted(self):
        assert self.lock_active
        self.rolled_back = True


def test_post_execution_failure_rolls_back_inside_vault_transaction(
    tmp_path: Path,
    monkeypatch,
) -> None:
    paths, store, source = _runtime(tmp_path)
    admit_path(source, paths=paths, store=store)
    lock_active: list[bool] = []
    executor = _RollbackObservingExecutor(lock_active)
    original_transition = store.transition

    @contextmanager
    def tracking_lock(_paths):
        lock_active.append(True)
        try:
            yield
        finally:
            lock_active.pop()

    def fail_committing(*args, **kwargs):
        if kwargs.get("target") == JobState.COMMITTING:
            raise RuntimeError("commit transition failed")
        return original_transition(*args, **kwargs)

    monkeypatch.setattr(store, "transition", fail_committing)
    monkeypatch.setattr(
        "tessellum.runtime.supervisor.vault_write_lock",
        tracking_lock,
    )
    outcome = Supervisor(
        store=store,
        paths=paths,
        executor=executor,  # type: ignore[arg-type]
        owner_id="test-worker",
        rebuild_index=False,
    ).work_once()

    assert outcome.status == "retry_wait"
    assert executor.rolled_back is True


class _CancellingExecutor:
    cancellation_check = None

    def __init__(self, store: RuntimeStore) -> None:
        self.store = store

    def execute(self, job, lease, route, policy):
        self.store.request_cancel(job.job_id)
        raise RuntimeError("backend disconnected")


def test_failure_honours_concurrent_cancellation(tmp_path: Path) -> None:
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store)

    outcome = Supervisor(
        store=store,
        paths=paths,
        executor=_CancellingExecutor(store),  # type: ignore[arg-type]
        owner_id="test-worker",
        rebuild_index=False,
    ).work_once()

    cancelled = store.get(admitted.job_id)
    assert outcome.status == "cancelled"
    assert cancelled is not None
    assert cancelled.state == JobState.CANCELLED
    assert cancelled.lease is None
    assert "retry_scheduled" not in {
        event.event_type for event in store.events(admitted.job_id)
    }


class _PollingExecutor:
    cancellation_check = None
    completed_normally = False

    def execute(self, job, lease, route, policy):
        deadline = time.monotonic() + 2.0
        while time.monotonic() < deadline:
            assert self.cancellation_check is not None
            self.cancellation_check()
            time.sleep(0.005)
        self.completed_normally = True
        return _Result()


def test_heartbeat_loss_reaches_running_execution(
    tmp_path: Path,
    monkeypatch,
) -> None:
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store)
    executor = _PollingExecutor()

    def lose_heartbeat(*args, **kwargs):
        raise LeaseLostError("reclaimed")

    monkeypatch.setattr(store, "heartbeat", lose_heartbeat)
    monkeypatch.setattr(
        RuntimePolicy,
        "for_profile",
        classmethod(lambda cls, profile: RuntimePolicy(lease_ttl=0.06)),
    )
    started = time.monotonic()
    outcome = Supervisor(
        store=store,
        paths=paths,
        executor=executor,  # type: ignore[arg-type]
        owner_id="test-worker",
        rebuild_index=False,
    ).work_once()

    assert outcome.status == "lease_lost"
    assert time.monotonic() - started < 0.5
    assert executor.completed_normally is False
    current = store.get(admitted.job_id)
    assert current is not None
    assert current.state == JobState.RUNNING


def test_completion_stops_heartbeat_before_lease_is_cleared(
    tmp_path: Path,
    monkeypatch,
) -> None:
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store)
    original_heartbeat = store.heartbeat
    original_transition = store.transition

    def heartbeat(*args, **kwargs):
        current = store.get(admitted.job_id)
        if current is not None and current.state == JobState.COMPLETE:
            raise LeaseLostError("heartbeat ran after completion")
        return original_heartbeat(*args, **kwargs)

    def slow_complete(*args, **kwargs):
        result = original_transition(*args, **kwargs)
        if kwargs.get("target") == JobState.COMPLETE:
            time.sleep(0.12)
        return result

    monkeypatch.setattr(store, "heartbeat", heartbeat)
    monkeypatch.setattr(store, "transition", slow_complete)
    monkeypatch.setattr(
        RuntimePolicy,
        "for_profile",
        classmethod(lambda cls, profile: RuntimePolicy(lease_ttl=0.06)),
    )

    outcome = Supervisor(
        store=store,
        paths=paths,
        executor=_Executor(),  # type: ignore[arg-type]
        owner_id="test-worker",
        rebuild_index=False,
    ).work_once()

    assert outcome.status == "complete"
    assert store.get(admitted.job_id).state == JobState.COMPLETE  # type: ignore[union-attr]


class _RecordingExecutor:
    cancellation_check = None

    def __init__(self) -> None:
        self.calls = 0

    def execute(self, job, lease, route, policy):
        self.calls += 1
        return _Result()


def test_supervisor_resumes_committing_without_rerunning_execution(
    tmp_path: Path,
) -> None:
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store)
    claimed = store.claim_next("first-worker")
    assert claimed is not None
    assert claimed.lease is not None
    route = route_lane("papers", skills_dir=paths.skills)
    store.set_routing(
        admitted.job_id,
        claimed.lease,
        capability=route.capability,
        skill_digest=route.skill_digest,
    )
    planning = store.transition(
        admitted.job_id,
        expected=JobState.ROUTED,
        target=JobState.PLANNING,
        lease=claimed.lease,
    )
    ready = store.transition(
        admitted.job_id,
        expected=planning.state,
        target=JobState.READY,
        lease=claimed.lease,
    )
    running = store.transition(
        admitted.job_id,
        expected=ready.state,
        target=JobState.RUNNING,
        lease=claimed.lease,
    )
    accepted_note = paths.vault / "accepted.md"
    accepted_note.write_text("before", encoding="utf-8")
    journal = VaultEffectJournal(
        paths.vault,
        effect_guard=None,
        journal_dir=(
            paths.artifacts
            / admitted.job_id
            / "vault-effects"
            / str(claimed.lease.generation)
        ),
    )
    journal.record(accepted_note)
    journal.record_postimage(accepted_note, b"accepted")
    accepted_note.write_text("accepted", encoding="utf-8")
    committing = store.transition(
        admitted.job_id,
        expected=running.state,
        target=JobState.COMMITTING,
        lease=claimed.lease,
    )
    store.release_lease(admitted.job_id, committing.lease)  # type: ignore[arg-type]
    executor = _RecordingExecutor()

    outcome = Supervisor(
        store=store,
        paths=paths,
        executor=executor,  # type: ignore[arg-type]
        owner_id="commit-worker",
        rebuild_index=False,
    ).work_once()

    completed = store.get(admitted.job_id)
    assert outcome.status == "complete"
    assert executor.calls == 0
    assert completed is not None
    assert completed.state == JobState.COMPLETE
    assert completed.commit_attempts == 2
    assert not source.exists()
    assert accepted_note.read_text(encoding="utf-8") == "accepted"


def test_changed_skill_digest_fails_closed_before_retry_execution(
    tmp_path: Path,
) -> None:
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store)
    claimed = store.claim_next("first-worker")
    assert claimed is not None
    assert claimed.lease is not None
    route = route_lane("papers", skills_dir=paths.skills)
    store.set_routing(
        admitted.job_id,
        claimed.lease,
        capability=route.capability,
        skill_digest=route.skill_digest,
    )
    planning = store.transition(
        admitted.job_id,
        expected=JobState.ROUTED,
        target=JobState.PLANNING,
        lease=claimed.lease,
    )
    ready = store.transition(
        admitted.job_id,
        expected=planning.state,
        target=JobState.READY,
        lease=claimed.lease,
    )
    running = store.transition(
        admitted.job_id,
        expected=ready.state,
        target=JobState.RUNNING,
        lease=claimed.lease,
    )
    store.schedule_retry(
        admitted.job_id,
        claimed.lease,
        error="RuntimeError: backend disconnected",
        not_before=0.0,
    )
    assert running.skill_digest == route.skill_digest
    skill = paths.skills / "skill_tessellum_execute_digestion_plan.md"
    skill.write_text("changed skill", encoding="utf-8")
    executor = _RecordingExecutor()

    outcome = Supervisor(
        store=store,
        paths=paths,
        executor=executor,  # type: ignore[arg-type]
        owner_id="retry-worker",
        rebuild_index=False,
    ).work_once()

    failed = store.get(admitted.job_id)
    assert outcome.status == "dead_letter"
    assert executor.calls == 0
    assert failed is not None
    assert failed.state == JobState.DEAD_LETTER
    assert "persisted skill digest" in (failed.last_error or "")
