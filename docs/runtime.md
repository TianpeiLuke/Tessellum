# Automatic runtime

The automatic runtime turns files dropped into `inbox/` into durable, supervised
Composer digestion jobs. It is an operational control plane around the existing
Composer, not a replacement for Composer and not another knowledge store.
Composer still authors markdown into the vault, and the vault remains the only
authority for Tessellum knowledge.

The runtime adds the machinery that an unattended process needs: stable-file
admission, content-addressed spooling, idempotent job creation, deterministic
routing, leases and heartbeats, retry and cancellation policy, atomic index
replacement, source acknowledgement, and queryable job history.

## End-to-end flow

```text
inbox/<lane>/<source>
        |
        | stable-file check, SHA-256, spool-before-admit
        v
runs/runtime/spool/ + runtime.db
        |
        | explicit lane route, leased claim
        v
native Composer digestion
  plan -> augment -> review -> execute fan-out
        |
        | format close gate, wave gate, manifest resume
        v
vault/ new markdown
        |
        | build temporary index, atomic replace
        v
data/tessellum.db
        |
        | archive admitted spool bytes, acknowledge matching source
        v
runs/runtime/archive/<job-id>/source/
```

`tessellum runtime serve` repeats two deterministic operations: scan all known
inbox lanes, then claim and process one available job. It sleeps only when no
job is available and stops cleanly on `SIGINT` or `SIGTERM`. Filesystem events
are not trusted as state; polling and full rescans are the recovery mechanism.
Multiple service processes cannot own the same job generation because claims
are serialized and fenced in SQLite. A cross-process live-vault lock spans one
job's Composer writes through index publication, preventing another runtime
job from observing or indexing partial output. Within that transaction,
Composer's execute phase still fans planned notes out across the policy's
worker pool. Before each vault mutation, a durable per-job effect journal
records the original bytes and intended postimage hash under the job artifact
directory. A replacement worker replays an unaccepted journal while holding
the vault lock. Recovery restores only known original/runtime states and stops
on unknown manual edits rather than overwriting them.

## Admission: preserve bytes before intent

Admission rejects symbolic-link entries, then resolves each regular-file
candidate and confines it under a named inbox lane. Hidden resolved names,
`.gitkeep`, and common partial-write suffixes such as `.tmp`, `.part`, `.swp`,
and `.crdownload` are ignored. The scanner waits the settle interval, reads the
candidate, and verifies device, inode, size, and mtime before and after the
read.

The file's bytes are SHA-256 hashed and written to a content-addressed spool:

```text
runs/runtime/spool/<first-two-hex>/<sha256>
```

The write goes through a process-specific temporary file, digest verification,
`fsync`, and atomic rename. Admission also verifies any pre-existing object is
a regular, non-symlink file with the addressed digest. Only after that
verification does it insert the job into SQLite. Execution always reads the
spool, so later movement or deletion of the inbox file cannot change the
admitted payload.

The job idempotency key hashes:

```text
source + source_event_id + intent + payload_ref + lane + source identity
```

For inbox work, `source_event_id` is the path relative to `inbox/`,
`payload_ref` is the content hash, and source identity is the admitted
device/inode/size/mtime tuple. A rescan of the same directory entry returns the
existing job. Replacing that entry creates a new job even when the bytes are
identical; equal payloads still share the same spool object.

Per-file admission remains the default, but a coordinated multi-source
bundle-admission entry point also exists. It admits an explicitly-supplied,
ordered list of member paths as one objective, inherits each member's payload
idempotency, and records the group as a content-addressed `SourceBundle` under a
durable manifest in `runs/runtime/bundles`. It is opt-in and leaves the ordinary
per-file scan untouched.

## Durable state machine

`runtime.db` is a WAL-mode SQLite database (schema version 5) with schema
metadata and six tables:

- `jobs` holds requests, state, routing identity, separate execution/commit
  attempt counts, cancellation, lease fencing, results, linked-retry ancestry,
  and nullable links to a job's accepted plan revision and active commit
  capsule.
- `job_events` is an ordered per-job event journal.
- `tool_calls` reserves durable audit fields for policy-bound tool calls.
  The current standalone broker does not yet write this table.
- `plan_revisions`, `commit_capsules`, and `capsule_artifacts` are the P1
  durable substrate for snapshot-pinned knowledge transactions: an
  accepted-intent record, a content-addressed artifact bundle per accepted
  revision, and that bundle's content-addressed artifact manifest. They are the
  persistence for the Composer transaction track and are not yet wired to
  promotion, so no live job path reads or writes them today.

The modeled lifecycle is:

```text
received -> admitted -> routed -> planning -> ready -> running
                                                   |       |
                                                   |       v
                                                   |   validating
                                                   |       |
                                                   v       v
                                                committing -> complete

active states -> retry_wait -> ready
active states -> paused -> ready
cancellable states -> cancelled
nonterminal states -> dead_letter
```

The current inbox admission starts directly at `admitted`, and the supervisor
uses `routed`, `planning`, `ready`, `running`, `committing`, and the terminal or
retry states. `received`, `validating`, and `paused` are modeled extension
points, not states emitted by the current supervisor. Every general transition
is compare-and-check against an expected state; specialized retry and claim
updates are transactional.

This database is authoritative for operational coordination while a job is in
flight. It is not System D's knowledge projection and does not compete with the
vault. Losing it loses queue and event history, but does not invalidate notes
already committed to the vault.

## Leases, generations, and recovery

A claim runs under `BEGIN IMMEDIATE`, chooses the highest-priority oldest
eligible job, increments its applicable attempt counter and lease generation,
and records an owner and expiry. An admitted job is claimed into `routed`; an already prepared job is
claimed from `ready` into `running`. A `committing` job is reclaimed in place
and resumes only the idempotent commit tail, without rerunning routing,
planning, or model calls. Execution and commit attempts have independent
bounded counters.

All owner-sensitive writes require and compare the supplied owner and lease
generation with the current row. Once another worker reclaims the job, a stale
worker receives `LeaseLostError` rather than committing through an obsolete
claim. Terminal transitions clear the lease in the same transaction. A
heartbeat thread extends the expiry while Composer is running.

The fence reaches the filesystem boundary. `lease_guard()` holds a SQLite
write transaction while one materializer/fixer write, manifest save, index
replace, rollback, or source acknowledgement publishes. Reclaim waits for that
short effect; an expired or superseded owner cannot enter it. Heartbeat failure
surfaces at the next cancellation or effect boundary; a synchronous backend
call cannot be interrupted in place. Checks run before backend dispatch and
again before materialization in both linear and fan-out phases.

Before each claim, expired execution leases return to `ready` when routing
metadata is complete or `admitted` when routing must be repaired; expired
commit leases remain `committing`. Each records a `lease_reclaimed` event. A
claim already at the applicable execution or commit attempt limit moves to
`dead_letter` instead of retrying forever. The next claim receives a new lease
generation. Lease generation fences worker ownership; the separate
`execution_generation` identifies the logical Composer execution generation and
is passed to the Composer manifest. It is initialized to 1 and the current
store exposes no mutation operation; unlike lease generation, it therefore
stays stable across process-level reclaim.

Recovery is layered:

- The runtime lease recovers a whole job abandoned by a process.
- The per-job Composer manifest recovers verified execute leaves and fences
  leaf-level ownership. A new job lease can immediately reclaim the old
  lease's leaf claims; standalone Composer keeps a conservative stale timeout.
- The durable vault-effect journal restores overwritten files and removes new
  files when a process dies before the commit decision. It records every
  intended postimage before publication and preserves unknown post-crash edits.
  Durable `committing` state is the acceptance decision, so recovery also
  accepts an open journal when a process dies between that transition and
  journal cleanup.
- The content-addressed spool recovers source bytes independently of the inbox.
- The commit tail can be repeated: index replacement is atomic and source
  archival is reconstructed from the spool. A job-owned hidden source
  quarantine is replayed if the prior process died during acknowledgement.

## Routing and policy

Routing is intentionally explicit. The eight supported lanes are:

`papers`, `book`, `podcast`, `sops`, `manual_retrieved`, `general`, `latex`,
and `flash`.

Every lane currently selects the pinned `native_digestion` capability. Routing
does not call an LLM and does not use the heuristic `CapabilityRegistry`.
`papers` contributes an `empirical_observation` building-block hint, `sops`
contributes `procedure`, and the other lanes leave the hint unset. Each lane
also provides a source-kind label. The route's `skill_digest` hashes the names
and bytes of the four required digestion skills, so the job records which
procedure it was routed against. Reclaimed and automatic retries must match
that persisted capability and digest; mutable skill drift fails closed before
execution. An explicit linked retry is a new job and may route against the new
skill set.

Two policy profiles ship:

| Profile | Workers | Invocation budget | Fix rounds | Other defaults |
|---|---:|---:|---:|---|
| `default` | 4 | 100 | 1 | windowed context, format close gate, wave gate, 3 job attempts |
| `fast` | 2 | 30 | 0 | otherwise inherits `default`; selected automatically for `flash` |

Both profiles cap assembled context at 120,000 characters across every
digestion phase, disable runtime tools, leave the optional cost cap unset, and
use a 120-second initial and renewed lease TTL. The invocation budget is shared
by plan, augment, review, and execute and charges every backend call, including
Composer retries and close-gate repair calls. Profiles are code-defined and
unknown names fail closed.

## Native Composer execution

The executor reads text sources (`.md`, `.txt`, `.tex`, `.json`, `.jsonl`,
`.csv`) as UTF-8. PDF input requires the `ingest` extra and is extracted with
`pdfplumber`. Other suffixes are rejected.

It writes a normalized `source_leaf.json` under the job artifact directory,
loads that job's Composer manifest, and calls
`run_digestion_pipeline()` directly:

1. `plan`, `augment`, and `review` run as linear Composer phases.
2. The program sign-off gate checks plan structure and the review verdict.
3. `execute` runs as Composer's dynamic fan-out over `execute_leaves`, or one
   leaf carrying the full plan when the plan does not provide leaves.
4. The runtime supplies one shared per-backend-call invocation budget and
   context assembler to all phases, plus cancellation checks, manifest
   identity, statistics, events, wave deduplication, and a close gate.

The unattended close gate is deliberately format-only. Composer's full close
gate also supports grounding, but the runtime has no independent grounding
verifier to supply that verdict; pretending otherwise would turn an unavailable
check into false assurance. With the default policy, one informed LLM fix round
may repair a format failure. Composer backends remain tool-free.

All agent-supplied materializer paths must be relative and resolve beneath the
vault root. Multi-edit responses preflight every target before the first write.
Successful resume entries become durable only after the close and wave gates
accept them; they record computation identity, structured output, and artifact
hashes. A failed gate rolls every materializer-touched path back to its pre-job
bytes and returns the leaf to executable work. The originals and journal state
are fsynced before each mutation, so the same rollback occurs after process
death. Changed input, changed skill, or modified artifacts also re-execute
rather than trapping a leaf in a terminal manifest row.

Artifacts live at `runs/runtime/artifacts/<job-id>/`: source metadata,
`manifest.json`, Composer events and statistics, the final `plan.json`, and
generation-scoped `vault-effects/` journals while publication is unaccepted.

## Cancellation, retry, and dead letter

Cancellation is cooperative. An unleased cancellable job becomes `cancelled`
immediately. A leased job records `cancel_requested`; the supervisor checks it
before execution, between digestion phases, during dynamic leaf dispatch, and
before entering the commit tail. The commit tail itself is not interruptible,
so a request arriving after commit begins does not roll back authored notes.

Failures use Composer's existing error classifier and full-jitter backoff.
`transient`, `rate_limit`, `auth`, and `crash` failures are scheduled in
`retry_wait` until the policy's attempt limit is reached. Due retries are
promoted to `ready`. Cancellation wins over failure scheduling, and cancelled
or expired leased rows are terminalized rather than left unclaimable.
Non-retryable failures, routing-pin changes, and exhausted attempts become
`dead_letter`, retaining their spool object, any artifacts produced so far,
error, and event history for inspection.

After the job enters `committing`, cancellation no longer applies. Commit-tail
failures remain `committing`, receive full-jitter retry deadlines, and consume
the separate `commit_attempts` budget. A later worker therefore resumes index
publication and source acknowledgement only; it never regenerates accepted
notes.

`retry` does not mutate terminal history. It creates a new admitted job with a
fresh source-event nonce and `supersedes_job_id` pointing to the cancelled or
dead-letter job. Completed jobs are not retryable through this operation.

## Commit tail

After Composer reports a clean result, the supervisor enters `committing`.
The same cross-process live-vault transaction remains held. Unless
`--no-index` was requested, it copies the live index to a unique temporary
database and re-indexes only the notes that changed — an incremental delta build
proven equal to a from-scratch rebuild, so a one-note commit no longer re-parses
and re-embeds the whole vault — then atomically replaces `data/tessellum.db`. The
live index is never mutated in place; a full rebuild is still used when no index
exists yet or a schema change demands it. The build carries the dense vector
surface and is fail-soft — a missing encoder degrades to a BM25-only index and
sets `dense_degraded`, which the supervisor threads into the job-completion detail
so a degraded live index is visible, never silent. File and parent-directory
fsyncs make publication durable.
A separate index lock serializes standalone rebuild calls, with the vault lock
always acquired first to avoid lock-order inversion. A failed build leaves the
previous index in place.

Only after the index succeeds does the runtime verify and copy the job's
immutable spool bytes to `runs/runtime/archive/<job-id>/source/<name>`,
verifying the temporary copy before publication. It atomically renames
the current inbox entry to a private quarantine name, then removes it only when
its hash and persisted device/inode/size/mtime identity match admission. A
replacement is restored, or recovered under a collision-safe lane name if
another writer already recreated the path. The job is marked `complete` last,
with the archive and configured index paths recorded. If a process dies after
the private quarantine rename, commit-only recovery finds that job-owned hidden
entry and finishes the same acknowledgement.

## Tool boundary

`ToolBroker` is a separate policy primitive. It supports an explicit allowlist,
JSON Schema input validation, a per-broker call budget, workspace confinement
for arguments whose keys end in `path`, per-tool timeouts, output byte limits,
and result hashing. The standalone broker accepts only `read_only=True` tools;
mutating tools require a future transactional executor. Call-budget reservation
is synchronized across threads. Because Python cannot kill a running thread, a
timed-out trusted read is allowed to drain before the broker reports timeout,
so it cannot continue after control returns to the caller.

The broker is intentionally not passed to Composer's LLM backends, and runtime
policies default `tools_enabled` to false. It is also not wired to the
`tool_calls` SQLite table yet. This preserves the current boundary: Composer
generates typed content, while any future external action must pass through an
independently authorized and audited broker.

## Operating surfaces

The CLI exposes `tessellum runtime` with `init`, `submit`, `work`, `serve`,
`get`, `list`, `cancel`, `retry`, and `doctor`. `work` processes at most one
claim; `serve` is the polling scanner plus supervisor loop.

The MCP server exposes five matching job-control tools:
`tessellum_submit_job`, `tessellum_get_job`, `tessellum_list_jobs`,
`tessellum_cancel_job`, and `tessellum_retry_job`. MCP submits only files
already inside an inbox lane; it does not bypass admission confinement.

For exact paths, signatures, state transitions, and flags, see
[reference/runtime.md](reference/runtime.md).
