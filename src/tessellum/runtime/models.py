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
    # P1 A1.3: durable links to the accepted plan revision + active commit
    # capsule. Both default None so every existing keyword construction
    # (only store._row_to_job builds Job) is unaffected.
    accepted_revision_id: str | None = None
    active_capsule_id: str | None = None

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


# ── P1 A1.1/A1.2: durable revision + capsule records ────────────────────────
# Dataclass-style parity with WorkRequest / Job / JobEvent. Returned by the
# new RuntimeStore getters (record_plan_revision / get_plan_revision /
# create_commit_capsule / get_commit_capsule / list_capsule_artifacts).


@dataclass(frozen=True)
class PlanRevision:
    """A durable accepted-intent record (P1 A1.1).

    ``revision_id`` is the accepted-effect set hash the caller supplies (i.e.
    :func:`tessellum.composer.proposals.plan_revision_hash`); the store never
    recomputes it. ``canonical_bytes`` is the accepted canonical serialization
    (a BLOB — bytes in, bytes out, byte-identical). ``decision`` is
    ``"accept"`` | ``"reject"`` (free TEXT). ``evidence`` is provenance
    (round-trips via JSON). ``created_at`` is a row clock only — never a hash
    input.
    """

    revision_id: str
    parent_revision_id: str | None
    canonical_bytes: bytes
    decision: str
    evidence: dict
    created_at: float


@dataclass(frozen=True)
class CommitCapsule:
    """A content-addressed artifact bundle for one accepted revision (P1 A1.1).

    ``capsule_id`` is deterministic: ``sha256(revision_id \\0 base_generation
    \\0 policy_version)`` — the plan's "accepted intent + base generation +
    policy/version", with no clock in the hash. ``artifact_root`` is the
    per-capsule filesystem CAS root; ``state`` is the open→sealed lifecycle
    marker.
    """

    capsule_id: str
    revision_id: str
    base_generation: int
    state: str
    artifact_root: str
    created_at: float


@dataclass(frozen=True)
class CapsuleArtifact:
    """One manifest row of the A1.2 content-addressed artifact store.

    ``address`` is ``sha256(blob).hexdigest()`` (the 64-hex CAS convention);
    ``artifact_class`` is one of the five A1.2 payload kinds (free TEXT open
    set); ``size`` is ``len(blob)``.
    """

    capsule_id: str
    artifact_class: str
    address: str
    size: int
    created_at: float
