"""Typed runtime state shared by the CLI, supervisor, inbox, and MCP."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class JobState(StrEnum):
    RECEIVED = "received"
    ADMITTED = "admitted"
    ROUTED = "routed"
    PLANNING = "planning"
    READY = "ready"
    RUNNING = "running"
    VALIDATING = "validating"
    COMMITTING = "committing"
    RETRY_WAIT = "retry_wait"
    PAUSED = "paused"
    COMPLETE = "complete"
    CANCELLED = "cancelled"
    DEAD_LETTER = "dead_letter"


TERMINAL_STATES = frozenset(
    {JobState.COMPLETE, JobState.CANCELLED, JobState.DEAD_LETTER}
)

ALLOWED_TRANSITIONS: dict[JobState, frozenset[JobState]] = {
    JobState.RECEIVED: frozenset({JobState.ADMITTED, JobState.DEAD_LETTER}),
    JobState.ADMITTED: frozenset(
        {JobState.ROUTED, JobState.PAUSED, JobState.CANCELLED, JobState.DEAD_LETTER}
    ),
    JobState.ROUTED: frozenset(
        {JobState.PLANNING, JobState.READY, JobState.PAUSED, JobState.CANCELLED,
         JobState.DEAD_LETTER}
    ),
    JobState.PLANNING: frozenset(
        {JobState.READY, JobState.RETRY_WAIT, JobState.PAUSED, JobState.CANCELLED,
         JobState.DEAD_LETTER}
    ),
    JobState.READY: frozenset(
        {JobState.RUNNING, JobState.PAUSED, JobState.CANCELLED, JobState.DEAD_LETTER}
    ),
    JobState.RUNNING: frozenset(
        {JobState.VALIDATING, JobState.COMMITTING, JobState.RETRY_WAIT,
         JobState.PAUSED, JobState.CANCELLED, JobState.DEAD_LETTER}
    ),
    JobState.VALIDATING: frozenset(
        {JobState.COMMITTING, JobState.RETRY_WAIT, JobState.PAUSED,
         JobState.CANCELLED, JobState.DEAD_LETTER}
    ),
    JobState.COMMITTING: frozenset(
        {
            JobState.COMPLETE,
            JobState.RETRY_WAIT,
            JobState.CANCELLED,
            JobState.DEAD_LETTER,
        }
    ),
    JobState.RETRY_WAIT: frozenset(
        {JobState.READY, JobState.PAUSED, JobState.CANCELLED, JobState.DEAD_LETTER}
    ),
    JobState.PAUSED: frozenset(
        {JobState.READY, JobState.CANCELLED, JobState.DEAD_LETTER}
    ),
    JobState.COMPLETE: frozenset(),
    JobState.CANCELLED: frozenset(),
    JobState.DEAD_LETTER: frozenset(),
}


@dataclass(frozen=True)
class WorkRequest:
    source: str
    source_event_id: str
    intent: str
    payload_ref: str
    original_path: str
    lane: str
    source_device: int | None = None
    source_inode: int | None = None
    source_size: int | None = None
    source_mtime_ns: int | None = None
    policy_profile: str = "default"
    priority: int = 50
    not_before: float | None = None
    requested_capability: str | None = None


@dataclass(frozen=True)
class Lease:
    owner_id: str
    generation: int
    expires_at: float


@dataclass(frozen=True)
class Job:
    job_id: str
    idempotency_key: str
    request: WorkRequest
    state: JobState
    created_at: float
    updated_at: float
    lease: Lease | None = None
    capability: str | None = None
    skill_digest: str | None = None
    plan_hash: str | None = None
    execution_generation: int = 1
    attempts: int = 0
    commit_attempts: int = 0
    cancel_requested: bool = False
    last_error: str | None = None
    result_path: str | None = None
    supersedes_job_id: str | None = None

    @property
    def payload_path(self) -> Path:
        prefix = "sha256:"
        if not self.request.payload_ref.startswith(prefix):
            raise ValueError(f"unsupported payload ref: {self.request.payload_ref}")
        raise ValueError("payload_path requires RuntimePaths.spool_path(job.request.payload_ref)")


@dataclass(frozen=True)
class JobEvent:
    job_id: str
    sequence: int
    event_type: str
    at: float
    detail: dict
