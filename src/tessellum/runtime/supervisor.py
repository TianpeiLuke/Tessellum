"""Leased job supervisor around the native digestion executor."""

from __future__ import annotations

import random
import sqlite3
import socket
import threading
import time
import uuid
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from tessellum.composer.executor import classify_error, full_jitter_backoff
from tessellum.runtime.commit_tail import commit_job
from tessellum.runtime.executor import (
    DigestionExecutor,
    DigestionIncompleteError,
    VaultEffectJournal,
)
from tessellum.runtime.locking import vault_write_lock
from tessellum.runtime.models import ALLOWED_TRANSITIONS, Job, JobState, Lease
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.policy import RuntimePolicy
from tessellum.runtime.routing import DigestionRoute, route_lane
from tessellum.runtime.store import LeaseLostError, RuntimeStore


@dataclass(frozen=True)
class WorkOutcome:
    job_id: str | None
    status: str
    detail: str | None = None


class RoutingPinError(RuntimeError):
    pass


class Supervisor:
    def __init__(
        self,
        *,
        store: RuntimeStore,
        paths: RuntimePaths,
        executor: DigestionExecutor,
        owner_id: str | None = None,
        rebuild_index: bool = True,
        with_dense: bool = True,
        sleep_fn=time.sleep,
    ) -> None:
        self.store = store
        self.paths = paths
        self.executor = executor
        self.owner_id = owner_id or f"{socket.gethostname()}:{uuid.uuid4().hex}"
        self.rebuild_index = rebuild_index
        # Build the runtime index WITH dense embeddings by default so the dense
        # retrieval surface is populated on the live path (build() is fail-soft:
        # a missing encoder degrades to BM25-only, never crashes the commit).
        # Opt out (BM25-only, faster / no ML deps) via with_dense=False.
        self.with_dense = with_dense
        self.sleep_fn = sleep_fn
        self._active_job_id: str | None = None

    def work_once(self) -> WorkOutcome:
        self.store.promote_due_retries()
        self._active_job_id = None
        job: Job | None = None
        lease: Lease | None = None
        try:
            with self._vault_transaction():
                VaultEffectJournal.recover_pending(
                    self.paths.vault,
                    self.paths.artifacts,
                    is_accepted_job=self._journal_job_is_accepted,
                )
                queue_policy = RuntimePolicy()
                job = self.store.claim_next(
                    self.owner_id,
                    lease_ttl=queue_policy.lease_ttl,
                    max_attempts=queue_policy.max_attempts,
                )
                if job is None:
                    return WorkOutcome(job_id=None, status="idle")
                self._active_job_id = job.job_id
                assert job.lease is not None
                lease = job.lease
                if job.cancel_requested:
                    self._cancel(job, lease)
                    return WorkOutcome(job.job_id, "cancelled")
                if job.state == JobState.COMMITTING:
                    return self._resume_commit(job, lease)

                route = route_lane(job.request.lane, skills_dir=self.paths.skills)
                job = self._enforce_routing(job, lease, route)
                if job.state == JobState.ROUTED:
                    job = self.store.transition(
                        job.job_id,
                        expected=JobState.ROUTED,
                        target=JobState.PLANNING,
                        lease=lease,
                    )
                    job = self.store.transition(
                        job.job_id,
                        expected=JobState.PLANNING,
                        target=JobState.READY,
                        lease=lease,
                    )
                    job = self.store.transition(
                        job.job_id,
                        expected=JobState.READY,
                        target=JobState.RUNNING,
                        lease=lease,
                    )

                policy = RuntimePolicy.for_profile(job.request.policy_profile)
                with self._heartbeat(
                    job.job_id, lease, policy.lease_ttl
                ) as assert_heartbeat:
                    def cancellation_check() -> bool:
                        assert_heartbeat()
                        return self.store.assert_lease(
                            job.job_id, lease
                        ).cancel_requested

                    self.executor.cancellation_check = cancellation_check

                    def effect_guard():
                        return self.store.lease_guard(job.job_id, lease)

                    self.executor.effect_guard = effect_guard
                    if cancellation_check():
                        self._cancel(job, lease)
                        return WorkOutcome(job.job_id, "cancelled")
                    result = self.executor.execute(job, lease, route, policy)
                    if cancellation_check():
                        rollback = getattr(
                            self.executor, "rollback_uncommitted", None
                        )
                        if rollback is not None:
                            rollback()
                        current = self.store.get(job.job_id) or job
                        self._cancel(current, lease)
                        return WorkOutcome(job.job_id, "cancelled")
                    if not result.completed:
                        raise DigestionIncompleteError.from_result(result)
                    job = self.store.transition(
                        job.job_id,
                        expected=JobState.RUNNING,
                        target=JobState.COMMITTING,
                        lease=lease,
                    )
                    accept = getattr(self.executor, "accept_uncommitted", None)
                    if accept is not None:
                        accept()
                    committed = commit_job(
                        job,
                        paths=self.paths,
                        rebuild_index=self.rebuild_index,
                        with_dense=self.with_dense,
                        effect_guard=effect_guard,
                        lock_vault=False,
                    )
                self.store.transition(
                    job.job_id,
                    expected=JobState.COMMITTING,
                    target=JobState.COMPLETE,
                    lease=lease,
                    result_path=str(committed.archive_path),
                    detail=self._commit_detail(committed),
                )
                return WorkOutcome(job.job_id, "complete")
        except LeaseLostError:
            assert job is not None
            return WorkOutcome(job.job_id, "lease_lost")
        except InterruptedError as exc:
            assert job is not None
            assert lease is not None
            latest = self.store.get(job.job_id)
            if latest is not None:
                try:
                    self._cancel(latest, lease)
                except LeaseLostError:
                    return WorkOutcome(job.job_id, "lease_lost", str(exc))
            return WorkOutcome(job.job_id, "cancelled", str(exc))
        except Exception as exc:  # noqa: BLE001 - classify into durable state
            if job is None or lease is None:
                raise
            return self._handle_failure(job, lease, exc)
        finally:
            self._active_job_id = None

    @contextmanager
    def _heartbeat(
        self,
        job_id: str,
        lease: Lease,
        ttl: float,
    ) -> Iterator[Callable[[], None]]:
        stopped = threading.Event()
        failed = threading.Event()
        errors: list[Exception] = []

        def _assert_healthy() -> None:
            if failed.is_set():
                raise errors[0]

        def _run() -> None:
            while not stopped.wait(max(0.05, ttl / 3.0)):
                try:
                    self.store.heartbeat(job_id, lease, lease_ttl=ttl)
                except sqlite3.OperationalError as exc:
                    # A lease_guard held by this worker may temporarily own the
                    # SQLite write lock while publishing an external effect.
                    if "locked" in str(exc).lower() or "busy" in str(exc).lower():
                        continue
                    errors.append(exc)
                    failed.set()
                    return
                except Exception as exc:  # noqa: BLE001 - surfaced to executor
                    errors.append(exc)
                    failed.set()
                    return

        thread = threading.Thread(
            target=_run,
            name=f"runtime-heartbeat-{job_id[:8]}",
            daemon=True,
        )
        thread.start()
        try:
            yield _assert_healthy
        finally:
            stopped.set()
            thread.join(timeout=2.0)
        _assert_healthy()

    @contextmanager
    def _vault_transaction(self) -> Iterator[None]:
        """Keep unaccepted rollback inside the cross-process vault lock."""
        with vault_write_lock(self.paths):
            try:
                yield
            except BaseException:
                state_known_unaccepted = self._active_job_id is None
                if self._active_job_id is not None:
                    try:
                        active = self.store.get(self._active_job_id)
                    except Exception:  # preserve output when state is unknown
                        active = None
                    state_known_unaccepted = (
                        active is not None
                        and active.state
                        not in {JobState.COMMITTING, JobState.COMPLETE}
                    )
                if state_known_unaccepted:
                    rollback = getattr(
                        self.executor,
                        "rollback_uncommitted",
                        None,
                    )
                    if rollback is not None:
                        rollback()
                raise

    def _enforce_routing(
        self,
        job: Job,
        lease: Lease,
        route: DigestionRoute,
    ) -> Job:
        if job.capability is not None and job.capability != route.capability:
            raise RoutingPinError(
                "persisted capability does not match the current lane route"
            )
        if job.skill_digest is not None and job.skill_digest != route.skill_digest:
            raise RoutingPinError(
                "persisted skill digest does not match the current skill set"
            )
        if job.capability is None or job.skill_digest is None:
            return self.store.set_routing(
                job.job_id,
                lease,
                capability=route.capability,
                skill_digest=route.skill_digest,
            )
        return job

    def _journal_job_is_accepted(self, job_id: str) -> bool:
        job = self.store.get(job_id)
        return job is not None and job.state in {
            JobState.COMMITTING,
            JobState.COMPLETE,
        }

    def _resume_commit(self, job: Job, lease: Lease) -> WorkOutcome:
        """Resume only the idempotent commit tail for accepted output."""
        policy = RuntimePolicy.for_profile(job.request.policy_profile)
        with self._heartbeat(
            job.job_id,
            lease,
            policy.lease_ttl,
        ) as assert_heartbeat:
            assert_heartbeat()

            def effect_guard():
                return self.store.lease_guard(job.job_id, lease)

            committed = commit_job(
                job,
                paths=self.paths,
                rebuild_index=self.rebuild_index,
                with_dense=self.with_dense,
                effect_guard=effect_guard,
                lock_vault=False,
            )
        self.store.transition(
            job.job_id,
            expected=JobState.COMMITTING,
            target=JobState.COMPLETE,
            lease=lease,
            result_path=str(committed.archive_path),
            detail=self._commit_detail(committed),
        )
        return WorkOutcome(job.job_id, "complete")

    @staticmethod
    def _commit_detail(committed) -> dict:
        """Completion detail recorded in job state. Includes the published
        index path and — when the index was rebuilt with dense degraded to
        BM25-only — a visible ``dense_degraded`` flag so a degraded live
        retrieval surface is diagnosable from job state, not silent."""
        detail: dict = {"index_path": str(committed.index_path)}
        if committed.dense_degraded:
            detail["dense_degraded"] = True
        return detail

    def _cancel(self, job: Job, lease: Lease) -> None:
        if JobState.CANCELLED in ALLOWED_TRANSITIONS[job.state]:
            self.store.transition(
                job.job_id,
                expected=job.state,
                target=JobState.CANCELLED,
                lease=lease,
            )

    def _handle_failure(
        self,
        job: Job,
        lease: Lease,
        exc: Exception,
    ) -> WorkOutcome:
        latest = self.store.get(job.job_id) or job
        error = f"{type(exc).__name__}: {exc}"
        policy = RuntimePolicy.for_profile(job.request.policy_profile)
        if latest.state == JobState.COMMITTING:
            if latest.commit_attempts < policy.max_attempts:
                delay = full_jitter_backoff(
                    max(1, latest.commit_attempts),
                    rng=random.Random(
                        f"{job.job_id}:commit:{latest.commit_attempts}"
                    ),
                )
                self.store.schedule_commit_retry(
                    job.job_id,
                    lease,
                    error=error,
                    not_before=time.time() + delay,
                )
                return WorkOutcome(job.job_id, "retry_wait", error)
            self.store.transition(
                job.job_id,
                expected=JobState.COMMITTING,
                target=JobState.DEAD_LETTER,
                lease=lease,
                last_error=error,
            )
            return WorkOutcome(job.job_id, "dead_letter", error)
        if latest.cancel_requested:
            try:
                self._cancel(latest, lease)
            except LeaseLostError:
                return WorkOutcome(job.job_id, "lease_lost", error)
            return WorkOutcome(job.job_id, "cancelled", error)
        error_class = (
            exc.error_class
            if isinstance(exc, DigestionIncompleteError)
            else classify_error(error)
        )
        retryable = (
            not isinstance(exc, RoutingPinError)
            and error_class in {"transient", "rate_limit", "auth", "crash"}
        )
        if retryable and latest.attempts < policy.max_attempts:
            delay = full_jitter_backoff(
                max(1, latest.attempts),
                rng=random.Random(f"{job.job_id}:{latest.attempts}"),
            )
            scheduled = self.store.schedule_retry(
                job.job_id,
                lease,
                error=error,
                not_before=time.time() + delay,
            )
            if scheduled.state == JobState.CANCELLED:
                return WorkOutcome(job.job_id, "cancelled", error)
            return WorkOutcome(job.job_id, "retry_wait", error)
        if JobState.DEAD_LETTER in ALLOWED_TRANSITIONS[latest.state]:
            self.store.transition(
                job.job_id,
                expected=latest.state,
                target=JobState.DEAD_LETTER,
                lease=lease,
                last_error=error,
            )
        return WorkOutcome(job.job_id, "dead_letter", error)

    def run_forever(
        self,
        *,
        poll_seconds: float = 2.0,
        stop: callable | None = None,
    ) -> None:
        should_stop = stop or (lambda: False)
        while not should_stop():
            outcome = self.work_once()
            if outcome.status == "idle":
                self.sleep_fn(poll_seconds)
