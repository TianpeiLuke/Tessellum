"""SQLite-backed durable job queue with lease-generation fencing.

P1 ("Dynamic Digestion as a Snapshot-Pinned Knowledge Transaction") adds the
durable revision/capsule records and their store API on top of the shipped
job queue:

* **A1.1** — ``plan_revisions`` + ``commit_capsules`` tables (plus the A1.2
  ``capsule_artifacts`` manifest) and two nullable link columns on ``jobs``
  (``accepted_revision_id`` / ``active_capsule_id``).
* **A1.2** — a content-addressed capsule artifact store (a per-capsule
  filesystem CAS + a SQLite manifest), byte-identical round-trip.
* **A1.3** — :meth:`RuntimeStore.link_job_revision` wires the link columns +
  a program digest into ``plan_hash`` (kept as CAPABILITY identity — passed
  in by the caller, never derived from a revision).
* **A1.5** — :func:`plan_revision_recorder`, the additive durable sign-off
  recorder factory (a no-op-by-default seam consumed by
  :func:`tessellum.composer.signoff.run_sign_off`).

A1.4 (the epoch accept-point generation bump + admission stale-revision
fence) is DEFERRED: nothing here mutates ``state`` /
``execution_generation`` / any lease field, and no new promotion path is
enabled. This module adds only durable records + the store API.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import time
import uuid
from contextlib import contextmanager
from dataclasses import replace
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Iterable, Iterator

from tessellum.runtime.models import (
    ALLOWED_TRANSITIONS,
    CapsuleArtifact,
    CommitCapsule,
    Job,
    JobEvent,
    JobState,
    Lease,
    PlanRevision,
    TERMINAL_STATES,
    WorkRequest,
)

if TYPE_CHECKING:  # pragma: no cover - typing only, no runtime import cost/cycle
    from tessellum.composer.signoff import SignOffResult


class RuntimeStoreError(RuntimeError):
    pass


class TransitionError(RuntimeStoreError):
    pass


class LeaseLostError(RuntimeStoreError):
    pass


class RuntimeStore:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path).expanduser().resolve()

    @classmethod
    def open(cls, path: Path | str) -> "RuntimeStore":
        store = cls(path)
        store.path.parent.mkdir(parents=True, exist_ok=True)
        schema = files("tessellum.runtime").joinpath("schema.sql").read_text(encoding="utf-8")
        with store._connect() as conn:
            conn.executescript(schema)
            columns = {
                row["name"] for row in conn.execute("PRAGMA table_info(jobs)").fetchall()
            }
            migrations = {
                "execution_generation": (
                    "INTEGER NOT NULL DEFAULT 1"
                ),
                "source_device": "INTEGER",
                "source_inode": "INTEGER",
                "source_size": "INTEGER",
                "source_mtime_ns": "INTEGER",
                "commit_attempts": "INTEGER NOT NULL DEFAULT 0",
                # P1 A1.3: link an existing v4 jobs table to the new durable
                # records. Nullable + implicit-NULL default, so ADD COLUMN
                # with a REFERENCES clause is legal; executescript(schema)
                # ran first, so plan_revisions/commit_capsules already exist
                # as FK targets before this loop issues the ALTER.
                "accepted_revision_id": "TEXT REFERENCES plan_revisions(revision_id)",
                "active_capsule_id": "TEXT REFERENCES commit_capsules(capsule_id)",
            }
            for column, declaration in migrations.items():
                if column not in columns:
                    conn.execute(
                        f"ALTER TABLE jobs ADD COLUMN {column} {declaration}"
                    )
            conn.execute("UPDATE runtime_schema SET version = 5")
        return store

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=2.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 2000")
        return conn

    @staticmethod
    def idempotency_key(request: WorkRequest) -> str:
        import hashlib

        raw = "\0".join(
            (
                request.source,
                request.source_event_id,
                request.intent,
                request.payload_ref,
                request.lane,
                str(request.source_device),
                str(request.source_inode),
                str(request.source_size),
                str(request.source_mtime_ns),
            )
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def admit(
        self,
        request: WorkRequest,
        *,
        now: float | None = None,
        supersedes_job_id: str | None = None,
    ) -> tuple[Job, bool]:
        timestamp = time.time() if now is None else now
        key = self.idempotency_key(request)
        job_id = uuid.uuid4().hex
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            existing = conn.execute(
                "SELECT * FROM jobs WHERE idempotency_key = ?", (key,)
            ).fetchone()
            if existing is not None:
                return self._row_to_job(existing), False
            conn.execute(
                """
                INSERT INTO jobs(
                    job_id, idempotency_key, source, source_event_id, intent,
                    payload_ref, original_path, source_device, source_inode,
                    source_size, source_mtime_ns, lane, policy_profile, priority,
                    not_before, requested_capability, state, supersedes_job_id,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_id, key, request.source, request.source_event_id,
                    request.intent, request.payload_ref, request.original_path,
                    request.source_device, request.source_inode,
                    request.source_size, request.source_mtime_ns,
                    request.lane, request.policy_profile, request.priority,
                    request.not_before, request.requested_capability,
                    JobState.ADMITTED.value, supersedes_job_id, timestamp, timestamp,
                ),
            )
            self._append_event(
                conn, job_id, "admitted", timestamp,
                {"source": request.source, "lane": request.lane},
            )
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        assert row is not None
        return self._row_to_job(row), True

    def get(self, job_id: str) -> Job | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        return None if row is None else self._row_to_job(row)

    def list(
        self,
        *,
        states: Iterable[JobState] | None = None,
        limit: int = 100,
    ) -> list[Job]:
        params: list[object] = []
        where = ""
        if states:
            values = [state.value for state in states]
            where = f"WHERE state IN ({','.join('?' for _ in values)})"
            params.extend(values)
        params.append(limit)
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM jobs {where} ORDER BY created_at DESC LIMIT ?",
                params,
            ).fetchall()
        return [self._row_to_job(row) for row in rows]

    def events(self, job_id: str, *, after: int = 0, limit: int = 500) -> list[JobEvent]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM job_events
                WHERE job_id = ? AND sequence > ?
                ORDER BY sequence LIMIT ?
                """,
                (job_id, after, limit),
            ).fetchall()
        return [
            JobEvent(
                job_id=row["job_id"],
                sequence=row["sequence"],
                event_type=row["event_type"],
                at=row["at"],
                detail=json.loads(row["detail_json"]),
            )
            for row in rows
        ]

    def transition(
        self,
        job_id: str,
        *,
        expected: JobState,
        target: JobState,
        now: float | None = None,
        lease: Lease | None = None,
        detail: dict | None = None,
        last_error: str | None = None,
        result_path: str | None = None,
    ) -> Job:
        if target not in ALLOWED_TRANSITIONS[expected]:
            raise TransitionError(f"illegal transition {expected.value} -> {target.value}")
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            if JobState(row["state"]) != expected:
                raise TransitionError(
                    f"job {job_id} is {row['state']}, expected {expected.value}"
                )
            self._check_lease(row, lease, now=timestamp)
            if target == JobState.COMMITTING and row["cancel_requested"]:
                raise TransitionError(f"job {job_id} was cancelled before commit")
            if target == JobState.COMMITTING:
                conn.execute(
                    """
                    UPDATE jobs SET state = ?, updated_at = ?,
                        last_error = COALESCE(?, last_error),
                        result_path = COALESCE(?, result_path),
                        commit_attempts = commit_attempts + 1,
                        cancel_requested = 0
                    WHERE job_id = ?
                    """,
                    (target.value, timestamp, last_error, result_path, job_id),
                )
            elif target in TERMINAL_STATES:
                conn.execute(
                    """
                    UPDATE jobs SET state = ?, updated_at = ?,
                        last_error = COALESCE(?, last_error),
                        result_path = COALESCE(?, result_path),
                        not_before = NULL, lease_owner = NULL,
                        lease_expires_at = NULL
                    WHERE job_id = ?
                    """,
                    (target.value, timestamp, last_error, result_path, job_id),
                )
            else:
                conn.execute(
                    """
                    UPDATE jobs SET state = ?, updated_at = ?,
                        last_error = COALESCE(?, last_error),
                        result_path = COALESCE(?, result_path)
                    WHERE job_id = ?
                    """,
                    (target.value, timestamp, last_error, result_path, job_id),
                )
            self._append_event(
                conn, job_id, f"state:{target.value}", timestamp,
                detail or {"from": expected.value},
            )
            updated = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def reap_expired_leases(
        self, *, now: float | None = None, max_attempts: int = 3
    ) -> int:
        """Actively reclaim every stranded lease NOW, independent of a claim
        (T4 liveness, FZ 20k9d6a). Runs the same reclaim the claim path does
        lazily — finalize cancel-requested stale-lease jobs, and requeue (or
        dead-letter at ``max_attempts``) expired-lease ``in_progress`` jobs — but
        as its OWN sweep, so a dead worker's leaf can't sit stranded when no new
        work arrives to trigger :meth:`claim_next`. Returns the number of jobs
        reaped. The serve loop calls this each idle cycle."""
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            reaped = self._reap_stale_leases(conn, timestamp, max_attempts)
        return reaped

    def _reap_stale_leases(
        self, conn: sqlite3.Connection, timestamp: float, max_attempts: int
    ) -> int:
        """The shared reclaim body (single source of truth for lease liveness):
        (1) finalize cancel-requested jobs whose lease is stale/absent, and
        (2) requeue or dead-letter expired-lease jobs. Operates on an OPEN
        transaction ``conn``; called by both :meth:`claim_next` (lazy, before a
        claim) and :meth:`reap_expired_leases` (active sweep). Returns the count
        of jobs whose state changed."""
        reaped = 0
        cancelled = conn.execute(
            """
            SELECT job_id FROM jobs
            WHERE cancel_requested = 1
              AND state NOT IN (?, ?, ?)
              AND state != ?
              AND (
                lease_owner IS NULL
                OR lease_expires_at IS NULL
                OR lease_expires_at <= ?
              )
            """,
            (
                JobState.COMPLETE.value,
                JobState.CANCELLED.value,
                JobState.DEAD_LETTER.value,
                JobState.COMMITTING.value,
                timestamp,
            ),
        ).fetchall()
        for cancelled_row in cancelled:
            conn.execute(
                """
                UPDATE jobs SET state = ?, not_before = NULL,
                    lease_owner = NULL, lease_expires_at = NULL, updated_at = ?
                WHERE job_id = ?
                """,
                (
                    JobState.CANCELLED.value,
                    timestamp,
                    cancelled_row["job_id"],
                ),
            )
            self._append_event(
                conn,
                cancelled_row["job_id"],
                "state:cancelled",
                timestamp,
                {"reason": "cancel_requested"},
            )
            reaped += 1
        stale = conn.execute(
            """
            SELECT job_id, state, capability, skill_digest, attempts,
                   commit_attempts
            FROM jobs
            WHERE state IN (?, ?, ?, ?, ?)
              AND lease_expires_at IS NOT NULL
              AND lease_expires_at <= ?
              AND cancel_requested = 0
            """,
            (
                JobState.ROUTED.value,
                JobState.PLANNING.value,
                JobState.RUNNING.value,
                JobState.VALIDATING.value,
                JobState.COMMITTING.value,
                timestamp,
            ),
        ).fetchall()
        for stale_row in stale:
            stale_state = JobState(stale_row["state"])
            attempt_count = (
                stale_row["commit_attempts"]
                if stale_state == JobState.COMMITTING
                else stale_row["attempts"]
            )
            if attempt_count >= max_attempts:
                conn.execute(
                    """
                    UPDATE jobs SET state = ?, not_before = NULL,
                        lease_owner = NULL, lease_expires_at = NULL,
                        last_error = ?, updated_at = ?
                    WHERE job_id = ?
                    """,
                    (
                        JobState.DEAD_LETTER.value,
                        (
                            "commit lease expired after maximum attempts"
                            if stale_state == JobState.COMMITTING
                            else "lease expired after maximum attempts"
                        ),
                        timestamp,
                        stale_row["job_id"],
                    ),
                )
                self._append_event(
                    conn,
                    stale_row["job_id"],
                    "state:dead_letter",
                    timestamp,
                    {
                        "reason": "lease_expired",
                        "attempts": attempt_count,
                        "phase": (
                            "commit"
                            if stale_state == JobState.COMMITTING
                            else "execute"
                        ),
                    },
                )
                reaped += 1
                continue
            target = stale_state
            if stale_state != JobState.COMMITTING:
                target = (
                    JobState.READY
                    if stale_row["capability"] and stale_row["skill_digest"]
                    else JobState.ADMITTED
                )
            conn.execute(
                """
                UPDATE jobs SET state = ?, lease_owner = NULL,
                    lease_expires_at = NULL, updated_at = ?
                WHERE job_id = ?
                """,
                (target.value, timestamp, stale_row["job_id"]),
            )
            self._append_event(
                conn,
                stale_row["job_id"],
                "lease_reclaimed",
                timestamp,
                {"target": target.value},
            )
            reaped += 1
        return reaped

    def claim_next(
        self,
        owner_id: str,
        *,
        now: float | None = None,
        lease_ttl: float = 60.0,
        max_attempts: int = 3,
    ) -> Job | None:
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            self._reap_stale_leases(conn, timestamp, max_attempts)
            row = conn.execute(
                """
                SELECT * FROM jobs
                WHERE (
                    (state IN (?, ?) AND attempts < ?)
                    OR (state = ? AND commit_attempts < ?)
                )
                  AND cancel_requested = 0
                  AND (not_before IS NULL OR not_before <= ?)
                  AND (lease_expires_at IS NULL OR lease_expires_at <= ?)
                ORDER BY priority DESC, created_at
                LIMIT 1
                """,
                (
                    JobState.ADMITTED.value,
                    JobState.READY.value,
                    max_attempts,
                    JobState.COMMITTING.value,
                    max_attempts,
                    timestamp,
                    timestamp,
                ),
            ).fetchone()
            if row is None:
                return None
            generation = row["lease_generation"] + 1
            claimed_state = JobState(row["state"])
            target = {
                JobState.ADMITTED: JobState.ROUTED,
                JobState.READY: JobState.RUNNING,
                JobState.COMMITTING: JobState.COMMITTING,
            }[claimed_state]
            execution_increment = 0 if claimed_state == JobState.COMMITTING else 1
            commit_increment = 1 if claimed_state == JobState.COMMITTING else 0
            conn.execute(
                """
                UPDATE jobs SET state = ?, lease_owner = ?, lease_generation = ?,
                    lease_expires_at = ?, attempts = attempts + ?,
                    commit_attempts = commit_attempts + ?, not_before = NULL,
                    updated_at = ?
                WHERE job_id = ?
                """,
                (
                    target.value, owner_id, generation, timestamp + lease_ttl,
                    execution_increment, commit_increment, timestamp, row["job_id"],
                ),
            )
            self._append_event(
                conn, row["job_id"], "claimed", timestamp,
                {"owner_id": owner_id, "generation": generation},
            )
            updated = conn.execute(
                "SELECT * FROM jobs WHERE job_id = ?", (row["job_id"],)
            ).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def heartbeat(
        self,
        job_id: str,
        lease: Lease,
        *,
        now: float | None = None,
        lease_ttl: float = 60.0,
    ) -> Lease:
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            self._check_lease(row, lease, now=timestamp)
            expires = timestamp + lease_ttl
            conn.execute(
                "UPDATE jobs SET lease_expires_at = ?, updated_at = ? WHERE job_id = ?",
                (expires, timestamp, job_id),
            )
        return replace(lease, expires_at=expires)

    def request_cancel(self, job_id: str, *, now: float | None = None) -> Job:
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            state = JobState(row["state"])
            if state in TERMINAL_STATES:
                return self._row_to_job(row)
            if state == JobState.COMMITTING:
                return self._row_to_job(row)
            lease_is_stale = (
                row["lease_owner"] is not None
                and (
                    row["lease_expires_at"] is None
                    or row["lease_expires_at"] <= timestamp
                )
            )
            if (
                lease_is_stale
                or (
                    row["lease_owner"] is None
                    and JobState.CANCELLED in ALLOWED_TRANSITIONS[state]
                )
            ):
                conn.execute(
                    """
                    UPDATE jobs SET state = ?, cancel_requested = 1,
                        not_before = NULL, lease_owner = NULL,
                        lease_expires_at = NULL, updated_at = ?
                    WHERE job_id = ?
                    """,
                    (JobState.CANCELLED.value, timestamp, job_id),
                )
                self._append_event(conn, job_id, "state:cancelled", timestamp, {})
            else:
                conn.execute(
                    "UPDATE jobs SET cancel_requested = 1, updated_at = ? WHERE job_id = ?",
                    (timestamp, job_id),
                )
                self._append_event(conn, job_id, "cancel_requested", timestamp, {})
            updated = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def force_cancel(self, job_id: str, *, now: float | None = None) -> Job:
        """Force-kill a job by FENCING its worker out, then marking it cancelled
        (T2, FZ 20k9d6a) — the escalation past :meth:`request_cancel` for a job
        whose worker is ignoring the cooperative signal (or is dead but still
        holds a live lease).

        The fence: bump ``lease_generation`` and null the lease owner. Any
        in-flight worker still holding the OLD ``(owner, generation)`` lease
        fails :meth:`_check_lease` on its next ``transition`` (generation
        mismatch AND owner-now-null → ``LeaseLostError``), so it can neither
        commit nor advance the job — the OS "SIGKILL" after cooperative
        "SIGTERM". Idempotent on a terminal job (returned unchanged). Uses the
        same fenced, single-writer UPDATE path as every other state change, so
        it cannot corrupt run state."""
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            if JobState(row["state"]) in TERMINAL_STATES:
                return self._row_to_job(row)
            new_generation = row["lease_generation"] + 1
            conn.execute(
                """
                UPDATE jobs SET state = ?, cancel_requested = 1,
                    lease_generation = ?, lease_owner = NULL,
                    lease_expires_at = NULL, not_before = NULL, updated_at = ?
                WHERE job_id = ?
                """,
                (JobState.CANCELLED.value, new_generation, timestamp, job_id),
            )
            self._append_event(
                conn, job_id, "state:cancelled", timestamp,
                {"reason": "force_cancel", "fenced_generation": new_generation},
            )
            updated = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def promote_paused(self, job_id: str, *, now: float | None = None) -> Job:
        """Promote an INSPECTED, PAUSED job back into the work queue (T3
        `promote`, FZ 20k9d6a): PAUSED → READY, clearing any stale lease so
        :meth:`claim_next` re-claims it fresh. The next claim resumes the
        execute wave over the accepted plan (the supervisor routes a job whose
        plan.json exists through ``resume_execute``). Raises if the job is not
        PAUSED (only a parked-for-inspection job is promotable)."""
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            state = JobState(row["state"])
            if state != JobState.PAUSED:
                raise TransitionError(
                    f"job {job_id} is {state.value}, expected paused to promote"
                )
            conn.execute(
                """
                UPDATE jobs SET state = ?, lease_owner = NULL,
                    lease_expires_at = NULL, not_before = NULL, updated_at = ?
                WHERE job_id = ?
                """,
                (JobState.READY.value, timestamp, job_id),
            )
            self._append_event(
                conn, job_id, f"state:{JobState.READY.value}", timestamp,
                {"reason": "promote_after_inspect", "from": state.value},
            )
            updated = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def reject_paused(self, job_id: str, *, now: float | None = None) -> Job:
        """Reject an INSPECTED, PAUSED job (T3 `reject`, FZ 20k9d6a): PAUSED →
        CANCELLED, discarding the accepted-but-unexecuted plan. Idempotent on a
        terminal job; raises if the job is neither PAUSED nor terminal."""
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            state = JobState(row["state"])
            if state in TERMINAL_STATES:
                return self._row_to_job(row)
            if state != JobState.PAUSED:
                raise TransitionError(
                    f"job {job_id} is {state.value}, expected paused to reject"
                )
            conn.execute(
                """
                UPDATE jobs SET state = ?, cancel_requested = 1, lease_owner = NULL,
                    lease_expires_at = NULL, not_before = NULL, updated_at = ?
                WHERE job_id = ?
                """,
                (JobState.CANCELLED.value, timestamp, job_id),
            )
            self._append_event(
                conn, job_id, "state:cancelled", timestamp,
                {"reason": "reject_after_inspect"},
            )
            updated = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def retry_terminal(
        self,
        job_id: str,
        *,
        now: float | None = None,
    ) -> Job:
        prior = self.get(job_id)
        if prior is None:
            raise KeyError(job_id)
        if prior.state not in {JobState.DEAD_LETTER, JobState.CANCELLED}:
            raise TransitionError(
                f"job {job_id} is {prior.state.value}, expected terminal retry state"
            )
        nonce = uuid.uuid4().hex
        request = replace(
            prior.request,
            source_event_id=f"{prior.request.source_event_id}#retry:{nonce}",
        )
        retried, created = self.admit(
            request,
            now=now,
            supersedes_job_id=prior.job_id,
        )
        assert created
        return retried

    def release_lease(
        self,
        job_id: str,
        lease: Lease,
        *,
        now: float | None = None,
    ) -> None:
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            self._check_lease(row, lease, now=timestamp)
            conn.execute(
                """
                UPDATE jobs SET lease_owner = NULL, lease_expires_at = NULL
                WHERE job_id = ?
                """,
                (job_id,),
            )

    def assert_lease(
        self,
        job_id: str,
        lease: Lease,
        *,
        now: float | None = None,
    ) -> Job:
        """Assert current ownership, generation, and expiry."""
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        if row is None:
            raise KeyError(job_id)
        timestamp = time.time() if now is None else now
        self._check_lease(row, lease, now=timestamp)
        return self._row_to_job(row)

    @contextmanager
    def lease_guard(
        self,
        job_id: str,
        lease: Lease,
        *,
        now: float | None = None,
    ) -> Iterator[Job]:
        """Fence one external effect against lease reclaim."""
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            timestamp = time.time() if now is None else now
            row = conn.execute(
                "SELECT * FROM jobs WHERE job_id = ?", (job_id,)
            ).fetchone()
            if row is None:
                raise KeyError(job_id)
            self._check_lease(row, lease, now=timestamp)
            yield self._row_to_job(row)
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            conn.close()

    def set_routing(
        self,
        job_id: str,
        lease: Lease,
        *,
        capability: str,
        skill_digest: str,
        now: float | None = None,
    ) -> Job:
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            self._check_lease(row, lease, now=timestamp)
            conn.execute(
                """
                UPDATE jobs SET capability = ?, skill_digest = ?, updated_at = ?
                WHERE job_id = ?
                """,
                (capability, skill_digest, timestamp, job_id),
            )
            self._append_event(
                conn, job_id, "routed", timestamp,
                {"capability": capability, "skill_digest": skill_digest},
            )
            updated = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def schedule_retry(
        self,
        job_id: str,
        lease: Lease,
        *,
        error: str,
        not_before: float,
        now: float | None = None,
    ) -> Job:
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            self._check_lease(row, lease, now=timestamp)
            if row["cancel_requested"]:
                conn.execute(
                    """
                    UPDATE jobs SET state = ?, not_before = NULL,
                        lease_owner = NULL, lease_expires_at = NULL, updated_at = ?
                    WHERE job_id = ?
                    """,
                    (JobState.CANCELLED.value, timestamp, job_id),
                )
                self._append_event(
                    conn,
                    job_id,
                    "state:cancelled",
                    timestamp,
                    {"from": row["state"], "reason": "cancel_requested"},
                )
                updated = conn.execute(
                    "SELECT * FROM jobs WHERE job_id = ?", (job_id,)
                ).fetchone()
                assert updated is not None
                return self._row_to_job(updated)
            conn.execute(
                """
                UPDATE jobs SET state = ?, not_before = ?, last_error = ?,
                    lease_owner = NULL, lease_expires_at = NULL, updated_at = ?
                WHERE job_id = ?
                """,
                (JobState.RETRY_WAIT.value, not_before, error, timestamp, job_id),
            )
            self._append_event(
                conn, job_id, "retry_scheduled", timestamp,
                {"not_before": not_before, "error": error},
            )
            updated = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def schedule_commit_retry(
        self,
        job_id: str,
        lease: Lease,
        *,
        error: str,
        not_before: float,
        now: float | None = None,
    ) -> Job:
        """Release a failed commit claim without rerunning digestion."""
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT * FROM jobs WHERE job_id = ?",
                (job_id,),
            ).fetchone()
            if row is None:
                raise KeyError(job_id)
            if JobState(row["state"]) != JobState.COMMITTING:
                raise TransitionError(
                    f"job {job_id} is {row['state']}, expected committing"
                )
            self._check_lease(row, lease, now=timestamp)
            conn.execute(
                """
                UPDATE jobs SET not_before = ?, last_error = ?,
                    lease_owner = NULL, lease_expires_at = NULL, updated_at = ?
                WHERE job_id = ?
                """,
                (not_before, error, timestamp, job_id),
            )
            self._append_event(
                conn,
                job_id,
                "commit_retry_scheduled",
                timestamp,
                {"not_before": not_before, "error": error},
            )
            updated = conn.execute(
                "SELECT * FROM jobs WHERE job_id = ?",
                (job_id,),
            ).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def promote_due_retries(self, *, now: float | None = None) -> int:
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            cancelled = conn.execute(
                """
                SELECT job_id FROM jobs
                WHERE state = ? AND cancel_requested = 1
                """,
                (JobState.RETRY_WAIT.value,),
            ).fetchall()
            for row in cancelled:
                conn.execute(
                    """
                    UPDATE jobs SET state = ?, not_before = NULL, updated_at = ?
                    WHERE job_id = ?
                    """,
                    (JobState.CANCELLED.value, timestamp, row["job_id"]),
                )
                self._append_event(
                    conn,
                    row["job_id"],
                    "state:cancelled",
                    timestamp,
                    {"from": JobState.RETRY_WAIT.value},
                )
            rows = conn.execute(
                """
                SELECT job_id, capability, skill_digest FROM jobs
                WHERE state = ? AND not_before <= ? AND cancel_requested = 0
                """,
                (JobState.RETRY_WAIT.value, timestamp),
            ).fetchall()
            for row in rows:
                target = (
                    JobState.READY
                    if row["capability"] and row["skill_digest"]
                    else JobState.ADMITTED
                )
                conn.execute(
                    """
                    UPDATE jobs SET state = ?, not_before = NULL, updated_at = ?
                    WHERE job_id = ?
                    """,
                    (target.value, timestamp, row["job_id"]),
                )
                self._append_event(
                    conn, row["job_id"], f"state:{target.value}", timestamp,
                    {"from": JobState.RETRY_WAIT.value},
                )
        return len(rows)

    # ── P1 A1.1: durable plan-revision records ──────────────────────────────

    def record_plan_revision(
        self,
        revision_id: str,
        *,
        parent_revision_id: str | None,
        canonical_bytes: bytes,
        decision: str,
        evidence: dict | None = None,
        now: float | None = None,
    ) -> PlanRevision:
        """Persist an accepted-intent :class:`PlanRevision` (P1 A1.1 / A1.5).

        ``revision_id`` and ``canonical_bytes`` are supplied by the caller
        (which ran :func:`composer.proposals.merge_proposals`) — the store
        does NOT recompute :func:`composer.proposals.plan_revision_hash`, so
        it takes no dependency on the composer package and no clock enters any
        hash input. ``decision`` is ``"accept"`` | ``"reject"`` (free TEXT).

        Idempotent by ``revision_id``: a re-record updates only the
        latest-write ``decision`` / ``evidence`` (the content-derived
        ``canonical_bytes`` / ``parent_revision_id`` are effectively
        immutable). Returns the reloaded record.
        """
        timestamp = time.time() if now is None else now
        evidence_json = json.dumps(evidence or {}, sort_keys=True)
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute(
                """
                INSERT INTO plan_revisions(
                    revision_id, parent_revision_id, canonical_bytes,
                    decision, evidence, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(revision_id) DO UPDATE SET
                    decision = excluded.decision,
                    evidence = excluded.evidence
                """,
                (
                    revision_id,
                    parent_revision_id,
                    canonical_bytes,
                    decision,
                    evidence_json,
                    timestamp,
                ),
            )
        reloaded = self.get_plan_revision(revision_id)
        assert reloaded is not None
        return reloaded

    def get_plan_revision(self, revision_id: str) -> PlanRevision | None:
        """Load a :class:`PlanRevision` (P1 A1.1).

        ``canonical_bytes`` comes back as ``bytes`` (BLOB column) for a
        byte-identical round-trip (guarantee 5)."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM plan_revisions WHERE revision_id = ?",
                (revision_id,),
            ).fetchone()
        return None if row is None else self._row_to_plan_revision(row)

    # ── P1 A1.1/A1.2: commit capsules + content-addressed artifact CAS ──────

    def _capsules_root(self) -> Path:
        """The CAS root — a sibling of spool/artifacts under the DB dir."""
        return self.path.parent / "capsules"

    @staticmethod
    def capsule_identity(
        revision_id: str, base_generation: int, policy_version: str
    ) -> str:
        """Deterministic capsule id (P1 A1.1) — no clock in the hash.

        ``sha256(revision_id \\0 base_generation \\0 policy_version)`` — the
        plan's "accepted intent + base generation + policy/version".
        ``policy_version`` encodes the policy profile + renderer/parser
        versions. Reuses the store's own sha256-hex convention (mirroring
        :meth:`idempotency_key`)."""
        raw = "\0".join((revision_id, str(base_generation), policy_version))
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def create_commit_capsule(
        self,
        *,
        revision_id: str,
        base_generation: int,
        policy_version: str,
        state: str = "open",
        now: float | None = None,
    ) -> CommitCapsule:
        """Create (or idempotently return) a :class:`CommitCapsule` (P1 A1.1).

        ``capsule_id`` is deterministic via :meth:`capsule_identity`, so a
        re-create with identical inputs converges (``INSERT OR IGNORE``).
        ``artifact_root`` is the per-capsule CAS root
        (``<db_dir>/capsules/<capsule_id>``); directory creation is lazy (in
        :meth:`put_capsule_artifact`). The ``revision_id`` FK is enforced
        (``foreign_keys=ON``) — a nonexistent revision raises
        :class:`sqlite3.IntegrityError`.
        """
        timestamp = time.time() if now is None else now
        capsule_id = self.capsule_identity(
            revision_id, base_generation, policy_version
        )
        artifact_root = str(self._capsules_root() / capsule_id)
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute(
                """
                INSERT OR IGNORE INTO commit_capsules(
                    capsule_id, revision_id, base_generation, state,
                    artifact_root, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    capsule_id,
                    revision_id,
                    base_generation,
                    state,
                    artifact_root,
                    timestamp,
                ),
            )
        reloaded = self.get_commit_capsule(capsule_id)
        assert reloaded is not None
        return reloaded

    def get_commit_capsule(self, capsule_id: str) -> CommitCapsule | None:
        """Load a :class:`CommitCapsule` (P1 A1.1)."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM commit_capsules WHERE capsule_id = ?",
                (capsule_id,),
            ).fetchone()
        return None if row is None else self._row_to_commit_capsule(row)

    def set_capsule_state(
        self, capsule_id: str, state: str, *, now: float | None = None
    ) -> CommitCapsule:
        """Advance a capsule's open→sealed lifecycle (P1 A1.1).

        A small lease-free UPDATE that keeps :meth:`create_commit_capsule`
        idempotent while allowing state progression. Additive."""
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT * FROM commit_capsules WHERE capsule_id = ?",
                (capsule_id,),
            ).fetchone()
            if row is None:
                raise KeyError(capsule_id)
            conn.execute(
                "UPDATE commit_capsules SET state = ? WHERE capsule_id = ?",
                (state, capsule_id),
            )
        reloaded = self.get_commit_capsule(capsule_id)
        assert reloaded is not None
        return reloaded

    def put_capsule_artifact(
        self,
        capsule_id: str,
        artifact_class: str,
        blob: bytes,
        *,
        now: float | None = None,
    ) -> str:
        """Content-address + persist one capsule artifact (P1 A1.2).

        The A1.2 content-addressed CAS. ``address = sha256(blob).hexdigest()``
        (the 64-hex convention shared with
        :func:`composer.proposals.content_hash`). The blob is written to
        ``<artifact_root>/blobs/<address[:2]>/<address>`` as raw bytes (no
        text encoding / newline translation — arbitrary bytes round-trip),
        atomically via a tmp-file + :func:`os.replace` (the
        :mod:`admission` write pattern) so a crash never leaves a half blob.
        A hash-named file that already exists is content-identical by
        construction, so the write is skipped (idempotent). Then an
        ``INSERT OR IGNORE`` records the manifest row.

        ``artifact_class`` is free TEXT (the five A1.2 kinds
        ``accepted_canonical`` | ``postimage`` | ``source_extraction`` |
        ``gate_evidence`` | ``renderer_versions``, an open set). The
        ``PK(capsule_id, address)`` allows many postimages + many classes per
        capsule. Returns the content address.
        """
        timestamp = time.time() if now is None else now
        capsule = self.get_commit_capsule(capsule_id)
        if capsule is None:
            raise KeyError(capsule_id)
        address = hashlib.sha256(blob).hexdigest()
        blob_path = Path(capsule.artifact_root) / "blobs" / address[:2] / address
        if not blob_path.exists():
            blob_path.parent.mkdir(parents=True, exist_ok=True)
            tmp = blob_path.with_name(
                f"{blob_path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
            )
            try:
                with tmp.open("xb") as handle:
                    handle.write(blob)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(tmp, blob_path)
            finally:
                tmp.unlink(missing_ok=True)
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute(
                """
                INSERT OR IGNORE INTO capsule_artifacts(
                    capsule_id, artifact_class, address, size, created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (capsule_id, artifact_class, address, len(blob), timestamp),
            )
        return address

    def get_capsule_artifact(self, capsule_id: str, address: str) -> bytes | None:
        """Read a capsule artifact back byte-for-byte (P1 A1.2, guarantee 5).

        Returns ``None`` when no manifest row for ``(capsule_id, address)``
        exists (so a foreign blob on disk is never returned)."""
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT capsule_id FROM capsule_artifacts
                WHERE capsule_id = ? AND address = ?
                """,
                (capsule_id, address),
            ).fetchone()
        if row is None:
            return None
        capsule = self.get_commit_capsule(capsule_id)
        if capsule is None:
            return None
        blob_path = Path(capsule.artifact_root) / "blobs" / address[:2] / address
        if not blob_path.exists():
            return None
        return blob_path.read_bytes()

    def list_capsule_artifacts(self, capsule_id: str) -> list[CapsuleArtifact]:
        """Manifest rows for a capsule, ordered by (class, address) (P1 A1.2)."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM capsule_artifacts
                WHERE capsule_id = ?
                ORDER BY artifact_class, address
                """,
                (capsule_id,),
            ).fetchall()
        return [self._row_to_capsule_artifact(row) for row in rows]

    # ── P1 A1.3: link a job to its revision/capsule (pure bookkeeping) ──────

    def link_job_revision(
        self,
        job_id: str,
        *,
        accepted_revision_id: str | None = None,
        active_capsule_id: str | None = None,
        plan_hash: str | None = None,
        lease: Lease | None = None,
        now: float | None = None,
    ) -> Job:
        """Link a job to its accepted revision + active capsule (P1 A1.3).

        Sets only the provided columns (``COALESCE``-style — a ``None`` arg
        leaves the existing value). ``plan_hash`` stays CAPABILITY identity:
        the caller passes the scheduler's value (``scheduler.py`` computes it);
        it is NEVER derived from a revision. The FK on
        ``accepted_revision_id`` / ``active_capsule_id`` is enforced
        (``foreign_keys=ON``).

        A1.4 DEFERRAL: this is pure bookkeeping. It does NOT touch ``state``,
        ``execution_generation``, or any lease / ``not_before`` field, so it
        enables no promotion path. ``lease`` is optional with the shipped
        :meth:`set_routing` / :meth:`transition` semantics (``None`` is
        allowed only when no active lease owner); pass it for mid-run linking.
        """
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT * FROM jobs WHERE job_id = ?", (job_id,)
            ).fetchone()
            if row is None:
                raise KeyError(job_id)
            self._check_lease(row, lease, now=timestamp)
            conn.execute(
                """
                UPDATE jobs SET
                    accepted_revision_id = COALESCE(?, accepted_revision_id),
                    active_capsule_id = COALESCE(?, active_capsule_id),
                    plan_hash = COALESCE(?, plan_hash),
                    updated_at = ?
                WHERE job_id = ?
                """,
                (
                    accepted_revision_id,
                    active_capsule_id,
                    plan_hash,
                    timestamp,
                    job_id,
                ),
            )
            self._append_event(
                conn,
                job_id,
                "revision_linked",
                timestamp,
                {
                    "accepted_revision_id": accepted_revision_id,
                    "active_capsule_id": active_capsule_id,
                },
            )
            updated = conn.execute(
                "SELECT * FROM jobs WHERE job_id = ?", (job_id,)
            ).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def _append_event(
        self,
        conn: sqlite3.Connection,
        job_id: str,
        event_type: str,
        at: float,
        detail: dict,
    ) -> None:
        sequence = conn.execute(
            "SELECT COALESCE(MAX(sequence), 0) + 1 FROM job_events WHERE job_id = ?",
            (job_id,),
        ).fetchone()[0]
        conn.execute(
            """
            INSERT INTO job_events(job_id, sequence, event_type, at, detail_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (job_id, sequence, event_type, at, json.dumps(detail, sort_keys=True)),
        )

    @staticmethod
    def _check_lease(
        row: sqlite3.Row,
        lease: Lease | None,
        *,
        now: float,
    ) -> None:
        if lease is None and row["lease_owner"] is not None:
            raise LeaseLostError(f"lease required for job {row['job_id']}")
        if lease is None:
            return
        if (
            row["lease_owner"] != lease.owner_id
            or row["lease_generation"] != lease.generation
            or row["lease_expires_at"] is None
            or row["lease_expires_at"] <= now
        ):
            raise LeaseLostError(f"lease lost for job {row['job_id']}")

    @staticmethod
    def _row_to_job(row: sqlite3.Row) -> Job:
        lease = None
        if row["lease_owner"] is not None:
            lease = Lease(
                owner_id=row["lease_owner"],
                generation=row["lease_generation"],
                expires_at=row["lease_expires_at"],
            )
        return Job(
            job_id=row["job_id"],
            idempotency_key=row["idempotency_key"],
            request=WorkRequest(
                source=row["source"],
                source_event_id=row["source_event_id"],
                intent=row["intent"],
                payload_ref=row["payload_ref"],
                original_path=row["original_path"],
                lane=row["lane"],
                source_device=row["source_device"],
                source_inode=row["source_inode"],
                source_size=row["source_size"],
                source_mtime_ns=row["source_mtime_ns"],
                policy_profile=row["policy_profile"],
                priority=row["priority"],
                not_before=row["not_before"],
                requested_capability=row["requested_capability"],
            ),
            state=JobState(row["state"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            lease=lease,
            capability=row["capability"],
            skill_digest=row["skill_digest"],
            plan_hash=row["plan_hash"],
            execution_generation=row["execution_generation"],
            attempts=row["attempts"],
            commit_attempts=row["commit_attempts"],
            cancel_requested=bool(row["cancel_requested"]),
            last_error=row["last_error"],
            result_path=row["result_path"],
            supersedes_job_id=row["supersedes_job_id"],
            accepted_revision_id=row["accepted_revision_id"],
            active_capsule_id=row["active_capsule_id"],
        )

    @staticmethod
    def _row_to_plan_revision(row: sqlite3.Row) -> PlanRevision:
        return PlanRevision(
            revision_id=row["revision_id"],
            parent_revision_id=row["parent_revision_id"],
            canonical_bytes=row["canonical_bytes"],
            decision=row["decision"],
            evidence=json.loads(row["evidence"]),
            created_at=row["created_at"],
        )

    @staticmethod
    def _row_to_commit_capsule(row: sqlite3.Row) -> CommitCapsule:
        return CommitCapsule(
            capsule_id=row["capsule_id"],
            revision_id=row["revision_id"],
            base_generation=row["base_generation"],
            state=row["state"],
            artifact_root=row["artifact_root"],
            created_at=row["created_at"],
        )

    @staticmethod
    def _row_to_capsule_artifact(row: sqlite3.Row) -> CapsuleArtifact:
        return CapsuleArtifact(
            capsule_id=row["capsule_id"],
            artifact_class=row["artifact_class"],
            address=row["address"],
            size=row["size"],
            created_at=row["created_at"],
        )


# ── P1 A1.5: durable sign-off recorder factory ──────────────────────────────


def plan_revision_recorder(
    store: RuntimeStore,
    *,
    revision_id: str,
    parent_revision_id: str | None,
    canonical_bytes: bytes,
    evidence: dict | None = None,
) -> Callable[["SignOffResult"], None]:
    """Build the additive durable sign-off recorder (P1 A1.5).

    Returns a ``Callable[[SignOffResult], None]`` closure to inject into
    :func:`tessellum.composer.signoff.run_sign_off` via its
    ``revision_recorder`` param. When the ladder yields a terminal result the
    closure maps the decision faithfully — ``"approved"`` → ``"accept"``,
    ``"needs_human"`` → ``"needs_human"`` (an escalation that reached no
    terminal accept/reject, NOT a rejection), everything else
    (``"rejected"``) → ``"reject"`` — and calls
    :meth:`RuntimeStore.record_plan_revision`, enriching the seed evidence
    with the deciding rung + reason.

    Kept in ``runtime`` (not ``composer``) so ``composer.signoff`` never
    imports ``runtime`` — there is no import cycle. ``runtime`` may freely
    import ``composer.signoff`` for the type hint. ``revision_id`` +
    ``canonical_bytes`` come from the caller's ``MergeResult``
    (:func:`composer.proposals.merge_proposals`), so the recorded
    accepted-intent identity is exactly
    :func:`composer.proposals.plan_revision_hash`.
    """
    seed = dict(evidence or {})

    _DECISION_MAP = {
        "approved": "accept",
        "needs_human": "needs_human",
        "rejected": "reject",
    }

    def _record(result: "SignOffResult") -> None:
        # Faithful three-way map; unknown decisions fall back to "reject"
        # (fail-closed — an unrecognised terminal state is not an accept).
        decision = _DECISION_MAP.get(result.decision, "reject")
        store.record_plan_revision(
            revision_id,
            parent_revision_id=parent_revision_id,
            canonical_bytes=canonical_bytes,
            decision=decision,
            evidence={
                **seed,
                "rung": result.deciding_rung,
                "reason": result.reason,
            },
        )

    return _record
