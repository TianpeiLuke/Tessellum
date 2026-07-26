# `tessellum.runtime` — Reference

API, symbols, paths, and command surfaces for the durable automatic runtime.
For the design and recovery model, see [../runtime.md](../runtime.md).

## File to role

| File | Role |
|---|---|
| `models.py` | Job states, transition graph, immutable request/job/lease/event records. |
| `schema.sql` | WAL-mode runtime schema: `jobs`, `job_events`, reserved `tool_calls`, and the P1 `plan_revisions`, `commit_capsules`, `capsule_artifacts` tables. |
| `paths.py` | Cwd-independent path discovery and content-addressed path helpers. |
| `store.py` | Transactional SQLite queue, events, state transitions, claims, lease fencing, retry, cancellation. |
| `admission.py` | Inbox confinement, stable-file checks, spool-before-admit, source archival. |
| `routing.py` | Explicit eight-lane routing to `native_digestion` and phase-skill digesting. |
| `policy.py` | `default` and `fast` unattended-execution profiles. |
| `executor.py` | Source extraction, backend construction, native Composer adapter, and durable vault-effect journal. |
| `supervisor.py` | Claim/route/execute/heartbeat/retry/commit orchestration. |
| `commit_tail.py` | Atomic index rebuild and idempotent source acknowledgement. |
| `inbox.py` | Sorted recursive reconciliation of the eight inbox lanes. |
| `service.py` | Foreground scan/work loop with `SIGINT`/`SIGTERM` shutdown. |
| `locking.py` | Cross-process live-vault transaction lock. |
| `tool_broker.py` | Standalone allowlisted, bounded tool execution; not wired into Composer. |
| `__init__.py` | Stable package exports listed below. |

## Paths

`RuntimePaths.discover(root=None, *, env=None) -> RuntimePaths` resolves every
path to an absolute path. Precedence is environment variable, explicit `root`
where applicable, then the default.

| Field | Environment override | Default |
|---|---|---|
| `root` | `TESSELLUM_ROOT` | explicit `root`, else cwd |
| `vault` | `TESSELLUM_VAULT` | `<root>` for a directly scaffolded vault, otherwise `<root>/vault` |
| `inbox` | `TESSELLUM_INBOX` | `<root>/inbox` |
| `skills` | `TESSELLUM_SKILLS` | `<vault>/resources/skills` |
| `runs` | `TESSELLUM_RUNS` | `<root>/runs` |
| `db` | `TESSELLUM_RUNTIME_DB` | `<runs>/runtime/runtime.db` |
| `spool` | none | `<runs>/runtime/spool` |
| `artifacts` | none | `<runs>/runtime/artifacts` |
| `archive` | none | `<runs>/runtime/archive` |
| `events` | none | `<runs>/runtime/events` |
| `index_db` | `TESSELLUM_INDEX_DB` | `<root>/data/tessellum.db` |

Methods:

- `ensure_runtime_dirs() -> None`
- `spool_path(payload_ref: str) -> Path` — accepts only
  `sha256:<64-character-digest>`-shaped references. The implementation checks
  the prefix and length but does not validate that the digest is hexadecimal;
  callers should pass refs produced by admission.
- `job_artifacts(job_id: str) -> Path`

The runtime CLI's `--db` overrides only `RuntimePaths.db` after discovery.
`events` is currently created as a reserved directory; job events live in
SQLite and Composer events live under each job's artifact directory.

## Models and states

`JobState` values:

`received`, `admitted`, `routed`, `planning`, `ready`, `running`,
`validating`, `committing`, `retry_wait`, `paused`, `complete`, `cancelled`,
and `dead_letter`.

`TERMINAL_STATES` is `{complete, cancelled, dead_letter}`.
`ALLOWED_TRANSITIONS` is:

| From | Allowed targets |
|---|---|
| `received` | `admitted`, `dead_letter` |
| `admitted` | `routed`, `paused`, `cancelled`, `dead_letter` |
| `routed` | `planning`, `ready`, `paused`, `cancelled`, `dead_letter` |
| `planning` | `ready`, `retry_wait`, `paused`, `cancelled`, `dead_letter` |
| `ready` | `running`, `paused`, `cancelled`, `dead_letter` |
| `running` | `validating`, `committing`, `retry_wait`, `paused`, `cancelled`, `dead_letter` |
| `validating` | `committing`, `retry_wait`, `paused`, `cancelled`, `dead_letter` |
| `committing` | `complete`, `retry_wait`, `cancelled`, `dead_letter` |
| `retry_wait` | `ready`, `paused`, `cancelled`, `dead_letter` |
| `paused` | `ready`, `cancelled`, `dead_letter` |
| terminal states | none |

Current inbox admission inserts `admitted` directly. The current supervisor
does not emit `received`, `validating`, or `paused`.

Immutable dataclasses:

```python
WorkRequest(
    source: str,
    source_event_id: str,
    intent: str,
    payload_ref: str,
    original_path: str,
    lane: str,
    source_device: int | None = None,
    source_inode: int | None = None,
    source_size: int | None = None,
    source_mtime_ns: int | None = None,
    policy_profile: str = "default",
    priority: int = 50,
    not_before: float | None = None,
    requested_capability: str | None = None,
)

Lease(owner_id: str, generation: int, expires_at: float)

Job(
    job_id: str,
    idempotency_key: str,
    request: WorkRequest,
    state: JobState,
    created_at: float,
    updated_at: float,
    lease: Lease | None = None,
    capability: str | None = None,
    skill_digest: str | None = None,
    plan_hash: str | None = None,
    execution_generation: int = 1,
    attempts: int = 0,
    commit_attempts: int = 0,
    cancel_requested: bool = False,
    last_error: str | None = None,
    result_path: str | None = None,
    supersedes_job_id: str | None = None,
    accepted_revision_id: str | None = None,
    active_capsule_id: str | None = None,
)

JobEvent(
    job_id: str,
    sequence: int,
    event_type: str,
    at: float,
    detail: dict,
)

PlanRevision(
    revision_id: str,
    parent_revision_id: str | None,
    canonical_bytes: bytes,
    decision: str,
    evidence: dict,
    created_at: float,
)

CommitCapsule(
    capsule_id: str,
    revision_id: str,
    base_generation: int,
    state: str,
    artifact_root: str,
    created_at: float,
)

CapsuleArtifact(
    capsule_id: str,
    artifact_class: str,
    address: str,
    size: int,
    created_at: float,
)
```

`PlanRevision`, `CommitCapsule`, and `CapsuleArtifact` (P1 schema v5) are the
durable substrate for snapshot-pinned knowledge transactions and are returned by
the revision/capsule store methods below. `revision_id` and `capsule_id` are
caller-supplied content hashes the store never recomputes; `canonical_bytes` is
a BLOB that round-trips byte-identically. These records are not yet wired to
promotion (A1.4 deferred), so no code path consults them during a live job.

`Job.payload_path` is not a resolver and always raises; use
`RuntimePaths.spool_path(job.request.payload_ref)`.
`plan_hash` and `requested_capability` are represented in durable models but
are not populated or consulted by the current inbox supervisor.
`execution_generation` defaults to 1 and has no public store mutation method.

## SQLite schema

Schema version is `5`. Connections enable foreign keys and a 2-second busy
timeout; schema initialization enables WAL.

- `runtime_schema`: one schema-version row.
- `jobs`: one row per idempotency key. The claim index is
  `(state, not_before, priority DESC, created_at)`. Two nullable P1 columns,
  `accepted_revision_id` and `active_capsule_id`, forward-reference
  `plan_revisions(revision_id)` and `commit_capsules(capsule_id)`.
- `job_events`: `(job_id, sequence)` primary key, cascade-deleted with its job.
  Event details are sorted JSON.
- `tool_calls`: call identity, job, tool, arguments, result hash, policy
  decision, duration, error, and creation time. No current runtime path inserts
  rows into this table.
- `plan_revisions` (P1 A1.1): `revision_id` primary key, nullable
  `parent_revision_id` content pointer (deliberately not a self-FK),
  `canonical_bytes` BLOB, `decision` TEXT, `evidence` JSON TEXT, `created_at`.
- `commit_capsules` (P1 A1.1): `capsule_id` primary key, `revision_id`
  referencing `plan_revisions`, `base_generation`, `state`, `artifact_root`,
  `created_at`. Indexed by `revision_id` (`commit_capsules_by_revision`).
- `capsule_artifacts` (P1 A1.2): CAS manifest with primary key
  `(capsule_id, artifact_class, address)`, `capsule_id` referencing
  `commit_capsules` with `ON DELETE CASCADE`, plus `size` and `created_at`.
  Indexed by `capsule_id` (`capsule_artifacts_by_capsule`).

`RuntimeStore.open()` migrates older `jobs` tables by adding
`execution_generation`, the four source-identity columns, `commit_attempts`,
and the P1 `accepted_revision_id` / `active_capsule_id` link columns when
absent, then records schema version 5. The `executescript(schema)` step creates
`plan_revisions` and `commit_capsules` first, so the two `ALTER TABLE ... ADD
COLUMN ... REFERENCES` migrations have their FK targets in place.

## Store API

Exceptions:

- `RuntimeStoreError(RuntimeError)`
- `TransitionError(RuntimeStoreError)`
- `LeaseLostError(RuntimeStoreError)`

Construction and reads:

```python
RuntimeStore(path: Path | str)
RuntimeStore.open(path: Path | str) -> RuntimeStore
RuntimeStore.idempotency_key(request: WorkRequest) -> str
store.get(job_id: str) -> Job | None
store.list(*, states: Iterable[JobState] | None = None, limit: int = 100) -> list[Job]
store.events(job_id: str, *, after: int = 0, limit: int = 500) -> list[JobEvent]
```

Admission and state:

```python
store.admit(
    request: WorkRequest,
    *,
    now: float | None = None,
    supersedes_job_id: str | None = None,
) -> tuple[Job, bool]

store.transition(
    job_id: str,
    *,
    expected: JobState,
    target: JobState,
    now: float | None = None,
    lease: Lease | None = None,
    detail: dict | None = None,
    last_error: str | None = None,
    result_path: str | None = None,
) -> Job

store.request_cancel(job_id: str, *, now: float | None = None) -> Job
store.retry_terminal(job_id: str, *, now: float | None = None) -> Job
```

`admit()` returns `(existing_job, False)` on an idempotency collision.
`retry_terminal()` accepts only `dead_letter` and `cancelled`; it creates a new
job whose `source_event_id` has a random retry suffix and whose
`supersedes_job_id` points to the prior job.

Claims and leases:

```python
store.claim_next(
    owner_id: str,
    *,
    now: float | None = None,
    lease_ttl: float = 60.0,
    max_attempts: int = 3,
) -> Job | None

store.heartbeat(
    job_id: str,
    lease: Lease,
    *,
    now: float | None = None,
    lease_ttl: float = 60.0,
) -> Lease

store.release_lease(job_id: str, lease: Lease) -> None
store.assert_lease(job_id: str, lease: Lease, *, now: float | None = None) -> Job

with store.lease_guard(
    job_id: str,
    lease: Lease,
    *,
    now: float | None = None,
) -> Iterator[Job]:
    ...
```

`claim_next()` first reclaims expired execution leases in `routed`, `planning`,
`running`, or `validating` to `ready` when routing identity is complete, or
`admitted` when routing metadata must be repaired. An expired `committing` job
stays `committing`, so it can resume only the idempotent commit tail. Execution
claims are bounded by `attempts`; commit claims are independently bounded by
`commit_attempts`. Exhaustion dead-letters the row. Cancel-requested expired
execution rows become `cancelled`, while cancellation is ignored after commit
starts. The eligible set is due `admitted`, `ready`, and `committing` jobs,
ordered by descending priority and ascending creation time. Every claim
increments `lease_generation`; execution claims increment `attempts`, and
commit-only claims increment `commit_attempts`.

Any transition of an owned row requires the matching lease; terminal
transitions clear that lease atomically. `assert_lease()` verifies owner,
generation, and expiry. `lease_guard()` does
the same under `BEGIN IMMEDIATE` and holds that transaction across one external
effect, preventing another process from reclaiming the job until publication
finishes.

Owner-fenced updates:

```python
store.set_routing(
    job_id: str,
    lease: Lease,
    *,
    capability: str,
    skill_digest: str,
    now: float | None = None,
) -> Job

store.schedule_retry(
    job_id: str,
    lease: Lease,
    *,
    error: str,
    not_before: float,
    now: float | None = None,
) -> Job

store.schedule_commit_retry(
    job_id: str,
    lease: Lease,
    *,
    error: str,
    not_before: float,
    now: float | None = None,
) -> Job

store.promote_due_retries(*, now: float | None = None) -> int
```

Lease checks compare owner, generation, and expiry. `schedule_retry()` clears
the lease; if cancellation was requested it terminalizes the job instead.
`schedule_commit_retry()` releases a failed commit lease but preserves
`committing`, ensuring digestion is not rerun. `promote_due_retries()` moves
due, uncancelled execution rows to `ready`.

Revisions and capsules (schema v5):

```python
store.record_plan_revision(
    revision_id: str,
    *,
    parent_revision_id: str | None,
    canonical_bytes: bytes,
    decision: str,
    evidence: dict | None = None,
    now: float | None = None,
) -> PlanRevision

store.get_plan_revision(revision_id: str) -> PlanRevision | None

RuntimeStore.capsule_identity(
    revision_id: str,
    base_generation: int,
    policy_version: str,
) -> str

store.create_commit_capsule(
    *,
    revision_id: str,
    base_generation: int,
    policy_version: str,
    state: str = "open",
    now: float | None = None,
) -> CommitCapsule

store.get_commit_capsule(capsule_id: str) -> CommitCapsule | None

store.set_capsule_state(
    capsule_id: str,
    state: str,
    *,
    now: float | None = None,
) -> CommitCapsule

store.put_capsule_artifact(
    capsule_id: str,
    artifact_class: str,
    blob: bytes,
    *,
    now: float | None = None,
) -> str

store.get_capsule_artifact(capsule_id: str, address: str) -> bytes | None
store.list_capsule_artifacts(capsule_id: str) -> list[CapsuleArtifact]

store.link_job_revision(
    job_id: str,
    *,
    accepted_revision_id: str | None = None,
    active_capsule_id: str | None = None,
    plan_hash: str | None = None,
    lease: Lease | None = None,
    now: float | None = None,
) -> Job
```

These ten methods are the durable substrate for snapshot-pinned knowledge
transactions — the persistence for the composer P0–P9 transaction track — not an
active promotion path (A1.4 is deferred, so none of them mutate `state`,
`execution_generation`, or any lease field).

- `record_plan_revision()` persists a caller-supplied accepted-intent record,
  idempotent by `revision_id` (a re-record updates only `decision` /
  `evidence`); the store never recomputes the hash or `canonical_bytes`.
- `get_plan_revision()` reloads one revision, returning `canonical_bytes` as
  `bytes` for a byte-identical round-trip.
- `capsule_identity()` is a staticmethod returning the deterministic
  `sha256(revision_id \0 base_generation \0 policy_version)` capsule id with no
  clock in the hash.
- `create_commit_capsule()` inserts-or-ignores a capsule keyed by
  `capsule_identity()`; the `revision_id` FK is enforced. `artifact_root` is
  `<db_dir>/capsules/<capsule_id>`, created lazily.
- `get_commit_capsule()` reloads one capsule.
- `set_capsule_state()` advances the open→sealed lifecycle marker.
- `put_capsule_artifact()` content-addresses a blob
  (`address = sha256(blob).hexdigest()`), writes it atomically under the
  capsule CAS, records the manifest row, and returns the address.
- `get_capsule_artifact()` reads a manifested blob back byte-for-byte, or
  `None` when no `(capsule_id, address)` manifest row exists.
- `list_capsule_artifacts()` returns manifest rows ordered by
  `(artifact_class, address)`.
- `link_job_revision()` `COALESCE`-sets the job's `accepted_revision_id` /
  `active_capsule_id` / `plan_hash` columns; `plan_hash` stays CAPABILITY
  identity supplied by the caller, never derived from a revision. It is pure
  bookkeeping (no state or lease mutation).

`plan_revision_recorder()` is a module-level factory:

```python
plan_revision_recorder(
    store: RuntimeStore,
    *,
    revision_id: str,
    parent_revision_id: str | None,
    canonical_bytes: bytes,
    evidence: dict | None = None,
) -> Callable[[SignOffResult], None]
```

It returns a closure for `composer.signoff.run_sign_off`'s `revision_recorder`
seam that maps a terminal sign-off decision (`approved`→`accept`,
`needs_human`→`needs_human`, else→`reject`) onto `record_plan_revision()`. It
lives in `runtime` so `composer.signoff` never imports `runtime`.

## Admission API

```python
is_eligible_source(path: Path, inbox_root: Path) -> bool
is_stable_file(path: Path, *, settle_seconds: float = 1.0) -> bool

admit_path(
    source_path: Path | str,
    *,
    paths: RuntimePaths,
    store: RuntimeStore,
    settle_seconds: float = 0.0,
    policy_profile: str | None = None,
    now: float | None = None,
) -> tuple[Job, bool]

archive_source(
    job: Job,
    *,
    paths: RuntimePaths,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
) -> Path
```

`IGNORED_SUFFIXES` is `{".tmp", ".part", ".swp", ".crdownload"}`.
`AdmissionError(ValueError)` reports confinement, eligibility, unstable-file,
and spool failures. `admit_path()` chooses profile `fast` for lane `flash` and
`default` otherwise unless explicitly overridden.

Eligibility rejects a symbolic-link candidate before resolution, then resolves
the candidate and inbox root for confinement and regular-file checks.
Admission persists device, inode, size, and mtime identity and includes it in
idempotency, so replacing a path creates a new event even for identical bytes.
Existing spool objects must be regular non-symlink files whose SHA-256 matches
their content address; new temporary objects are verified before publication
and the published object is verified before the database admit. Archival
re-verifies the spool and its temporary copy before publication. It atomically
quarantines the current inbox entry and deletes it only when hash plus persisted
identity match; mismatches are restored or recovered under a collision-safe
lane name. A retry replays this job's hidden quarantine if the prior process
died between rename and acknowledgement and fsyncs every replay mutation.

## Routing API

`LANE_HINTS`:

| Lane | Building-block hint | Source kind |
|---|---|---|
| `papers` | `empirical_observation` | `scholarly source` |
| `book` | none | `long-form source` |
| `podcast` | none | `transcript` |
| `sops` | `procedure` | `policy or procedure` |
| `manual_retrieved` | none | `externally retrieved evidence` |
| `general` | none | `general source` |
| `latex` | none | `technical manuscript` |
| `flash` | none | `low-latency capture` |

```python
route_lane(lane: str, *, skills_dir: Path | str) -> DigestionRoute

DigestionRoute(
    capability: str,
    skill_digest: str,
    building_block_hint: str | None,
    source_kind: str,
)
```

The capability is always `native_digestion`. The skill digest covers phase
labels and bytes for `plan`, `augment`, `review`, and `execute`.
`RoutingError(ValueError)` is raised for an unknown lane or missing phase skill.

## Policy API

```python
RuntimePolicy(
    max_workers: int = 4,
    max_invocations: int = 100,
    max_cost: float | None = None,
    max_fix_rounds: int = 1,
    context_strategy: str = "windowed",
    context_max_chars: int = 120_000,
    close_gate: bool = True,
    wave_gate: bool = True,
    tools_enabled: bool = False,
    max_attempts: int = 3,
    lease_ttl: float = 120.0,
)

RuntimePolicy.for_profile(profile: str) -> RuntimePolicy
```

`fast` overrides `max_workers=2`, `max_invocations=30`, and
`max_fix_rounds=0`. `default` uses the constructor defaults. Any other profile
raises `ValueError`.

## Executor API

```python
BackendConfig(
    kind: str = "mock",
    model: str | None = None,
    region: str = "us-east-1",
    aws_profile: str | None = None,
    mock_responses: dict[str, str] | None = None,
)

build_backend(config: BackendConfig) -> LLMBackend

DigestionExecutor(
    paths: RuntimePaths,
    backend: LLMBackend,
    cancellation_check: Callable[[], bool] | None = None,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
)

executor.execute(
    job: Job,
    lease: Lease,
    route: DigestionRoute,
    policy: RuntimePolicy,
) -> DigestionResult

executor.rollback_uncommitted() -> None
executor.accept_uncommitted() -> None

VaultEffectJournal(
    root: Path,
    *,
    effect_guard: Callable[[], ContextManager[None]] | None,
    journal_dir: Path | None = None,
)

journal.record(path: Path) -> None
journal(path: Path) -> None
journal.record_postimage(path: Path, content: bytes) -> None
journal.rollback() -> None
journal.accept() -> None
VaultEffectJournal.recover_pending(
    root: Path,
    artifacts_dir: Path,
    *,
    is_accepted_job: Callable[[str], bool] | None = None,
) -> int
```

Backend kinds and defaults:

| Kind | Default model |
|---|---|
| `mock` | `MockBackend` canned/default responses |
| `anthropic` | `claude-sonnet-4-6` |
| `bedrock` | `us.anthropic.claude-sonnet-4-6`, region `us-east-1` |

Supported UTF-8 text suffixes are `.md`, `.txt`, `.tex`, `.json`, `.jsonl`,
and `.csv`. `.pdf` requires `pdfplumber` from the `ingest` extra.
`UnsupportedSourceError(ValueError)` rejects unavailable PDF support and other
suffixes.

The executor calls `run_digestion_pipeline()` with a per-job manifest, run id
`<job-id>:<lease-generation>`, the job's `execution_generation`,
per-backend-call invocation budget, context assembler, optional format-only
close gate/fixer, optional wave gate, zero-delay reclaim of prior job-lease leaf
claims, cancellation/effect guards, a vault-effect journal, and Composer
event/statistics paths. The shared budget covers retries and fixer calls across
all four phases; the context assembler also covers all four. With a
`journal_dir`, the
journal fsyncs originals, every intended postimage hash, and an atomic manifest
before each vault mutation. Rejected or raised digestion restores every
materializer-touched path only when its current bytes match the original or a
recorded runtime postimage; unknown manual edits raise a recovery conflict and
are preserved. The supervisor persists `committing` before accepting the
journal. `recover_pending()` therefore treats an open journal for a durably
accepted job as accepted, while replaying other open journals and discarding
accepted/rolled-back cleanup leftovers under the cross-process vault lock.

## Supervisor and service API

```python
Supervisor(
    *,
    store: RuntimeStore,
    paths: RuntimePaths,
    executor: DigestionExecutor,
    owner_id: str | None = None,
    rebuild_index: bool = True,
    sleep_fn=time.sleep,
)

supervisor.work_once() -> WorkOutcome
supervisor.run_forever(*, poll_seconds: float = 2.0, stop: callable | None = None) -> None

WorkOutcome(job_id: str | None, status: str, detail: str | None = None)
```

Observed status values are `idle`, `complete`, `cancelled`, `lease_lost`,
`retry_wait`, and `dead_letter`.

The default owner id is `<hostname>:<uuid>`. The supervisor holds the
cross-process live-vault lock from crash-journal recovery through execution and
commit, while execute leaves still fan out internally. It classifies failures
with Composer's `classify_error()` and schedules Composer's full-jitter delay
for `transient`, `rate_limit`, `auth`, and `crash`. The jitter PRNG is seeded
from job id and attempt, making the chosen delay repeatable for that attempt.
Persisted capability and skill digest are checked before reclaimed work runs;
a mismatch raises `RoutingPinError` and dead-letters without dispatch.
Jobs claimed in `committing` bypass routing, planning, and execution and resume
only `commit_job()`. Commit failures use a separate full-jitter schedule and
`commit_attempts` budget while remaining in `committing`.

```python
InboxScanner(
    *,
    paths: RuntimePaths,
    store: RuntimeStore,
    settle_seconds: float = 1.0,
)

scanner.scan_once() -> ScanResult

scanner.admit_bundle(
    members: list[Path | str],
    *,
    objective: str,
    settle_seconds: float | None = None,
) -> BundleAdmission

ScanResult(
    admitted: tuple[Job, ...],
    deduplicated: tuple[Job, ...],
    rejected: tuple[tuple[Path, str], ...],
)

BundleAdmission(
    bundle: SourceBundle,
    jobs: tuple[Job, ...],
    manifest_path: Path,
    created: bool,
)

RuntimeService(
    scanner: InboxScanner,
    supervisor: Supervisor,
    scan_seconds: float = 2.0,
)

service.run() -> None
```

The scanner recursively visits each existing lane in `LANE_HINTS` order and
sorts paths within a lane. The service scans, performs one supervisor iteration,
and waits only after an `idle` outcome.

`admit_bundle()` is a separate, opt-in entry point that admits an
explicitly-supplied ordered list of member paths as one coordinated objective
(P2b/A2.1). Each member is admitted via `admit_path()`, inheriting per-member
`sha256` payload-ref idempotency; the members plus objective become a typed
`SourceBundle` (from `composer.knowledge_plan`) whose content-addressed
`bundle_id` keys a durable JSON manifest written atomically under
`runs/runtime/bundles/<bundle_id>.json`. Re-admitting the same members and
objective is idempotent (same `bundle_id`, no duplicate jobs, `created=False`).
`scan_once()` is untouched — per-file admission remains the default.

## Commit API

```python
rebuild_index_atomically(
    paths: RuntimePaths,
    *,
    with_dense: bool = True,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    lock_vault: bool = True,
) -> tuple[Path, bool]   # (index_path, dense_degraded)

commit_job(
    job: Job,
    *,
    paths: RuntimePaths,
    rebuild_index: bool = True,
    with_dense: bool = True,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    lock_vault: bool = True,
) -> CommitResult

CommitResult(archive_path: Path, index_path: Path, dense_degraded: bool | None = None)
```

`rebuild_index_atomically()` holds a thread lock plus a POSIX advisory index
lock and, by default, the live-vault lock across snapshot construction and
publication, always acquiring the vault lock before the index lock. It builds
to a sibling temporary database, fsyncs it, calls `os.replace()` only after
success, and fsyncs the parent directory. The effect guard fences publication,
not the expensive build. `commit_job()` rebuilds first, then durably archives
admitted spool bytes. Source acknowledgement replays a prior job-owned hidden
quarantine after process death. The supervisor already owns the live-vault
transaction, so it invokes the commit tail with
`with_dense=True, lock_vault=False` (R1 — the published live index now carries a
dense vector surface, not BM25-only). The build is **fail-soft**: a missing
`sentence-transformers` dep or an encoder failure degrades to a BM25-only index
with `dense_degraded=True`, which `rebuild_index_atomically` returns, `commit_job`
carries on `CommitResult.dense_degraded`, and the supervisor threads into the
job-completion `detail` — so a degraded live index is visible, never silent.

## Tool broker API

```python
ToolSpec(
    name: str,
    input_schema: dict,
    handler: Callable[[dict[str, Any]], Any],
    read_only: bool = True,
    timeout_seconds: float = 30.0,
    max_output_bytes: int = 1_000_000,
)

ToolBroker(
    *,
    allowed: set[str],
    workspace_root: Path | str,
    max_calls: int = 20,
)

broker.register(spec: ToolSpec) -> None
broker.call(name: str, arguments: dict[str, Any]) -> ToolCallResult

ToolCallResult(
    call_id: str,
    tool_name: str,
    value: Any,
    result_hash: str,
    duration_ms: float,
)
```

`ToolPolicyError(PermissionError)` covers authorization, call-budget, path,
timeout, and output-size failures. Inputs are validated with `jsonschema`.
String values under dictionary keys ending in `path` must resolve beneath
`workspace_root`; nested dictionaries and lists are checked recursively.

`register()` rejects `read_only=False`; mutating tools require a transactional
executor. Call-budget reservation is lock-protected. A timed-out trusted read
is drained before `ToolPolicyError` returns because Python threads cannot be
safely killed. The broker is not passed to Composer, does not consult
`RuntimePolicy.tools_enabled`, and does not persist the result to `tool_calls`.

## Package exports

`from tessellum.runtime import ...` exports:

`AdmissionError`, `CapsuleArtifact`, `CommitCapsule`, `Job`, `JobEvent`,
`JobState`, `Lease`, `LeaseLostError`, `PlanRevision`, `RuntimePaths`,
`RuntimeStore`, `TransitionError`, `WorkRequest`, `admit_path`, and
`plan_revision_recorder`.

The executor, supervisor, scanner, service, routing, policy, commit, and broker
APIs are imported from their respective submodules.

## CLI

All runtime commands accept `--root` and `--db`. Commands that execute work also
accept `--backend {mock,anthropic,bedrock}`, `--model`, `--region`,
`--aws-profile`, and `--mock-responses`.

| Command | Purpose | Additional flags |
|---|---|---|
| `tessellum runtime init` | Initialize runtime directories, DB, and all eight inbox lanes. | none |
| `tessellum runtime submit <path>` | Spool and admit one existing inbox file. | `--settle-seconds` (default `0`) |
| `tessellum runtime work` | Promote retries, claim, and process at most one job. | backend flags, `--no-index` |
| `tessellum runtime serve` | Poll inbox lanes and supervise until signalled. | backend flags, `--scan-seconds` (2), `--settle-seconds` (1), `--no-index` |
| `tessellum runtime get <job-id>` | Print one job as JSON. | `--events` |
| `tessellum runtime list` | Print jobs newest-first as JSON. | repeatable `--state`, `--limit` (100) |
| `tessellum runtime cancel <job-id>` | Request cooperative cancellation. | none |
| `tessellum runtime retry <job-id>` | Create a linked retry of cancelled/dead-letter work. | none |
| `tessellum runtime doctor` | Check resolved paths, index-parent writability, and DB readability. | none |

The default backend is `mock`. `--mock-responses` names a JSON file containing
the mock response mapping.

## MCP

The MCP server has five runtime job tools:

| Tool | Required input | Optional input |
|---|---|---|
| `tessellum_submit_job` | `path` | `root` (default `"."`) |
| `tessellum_get_job` | `job_id` | `root` |
| `tessellum_list_jobs` | none | `root`, `state`, `limit` (100) |
| `tessellum_cancel_job` | `job_id` | `root` |
| `tessellum_retry_job` | `job_id` | `root` |

These tools operate on the same `RuntimePaths` and `RuntimeStore` as the CLI.
They submit and control jobs; no MCP runtime tool executes a supervisor loop.
