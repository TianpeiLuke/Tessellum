"""SQLite-backed durable job queue with lease-generation fencing."""

from __future__ import annotations

import json
import sqlite3
import time
import uuid
from contextlib import contextmanager
from dataclasses import replace
from importlib.resources import files
from pathlib import Path
from typing import Iterable, Iterator

from tessellum.runtime.models import (
    ALLOWED_TRANSITIONS,
    Job,
    JobEvent,
    JobState,
    Lease,
    TERMINAL_STATES,
    WorkRequest,
)


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
            }
            for column, declaration in migrations.items():
                if column not in columns:
                    conn.execute(
                        f"ALTER TABLE jobs ADD COLUMN {column} {declaration}"
                    )
            conn.execute("UPDATE runtime_schema SET version = 4")
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
        )
