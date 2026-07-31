---
tags:
  - resource
  - documentation
  - hermes_agent
  - kanban
  - multi_agent
keywords:
  - hermes kanban
  - kanban.db
  - multi-agent task board
  - task runs
  - task_events
  - delegate_task vs kanban
  - durable work queue
topics:
  - Hermes Agent
  - Multi-Agent Coordination
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
access_control_group: ["general"]
---

# Hermes Kanban — Multi-Agent Board Data Model

## Overview

Hermes Kanban **is a durable task board, backed by a single SQLite database (`~/.hermes/kanban.db`), shared across all of an install's Hermes profiles** so multiple named agents can collaborate on work without fragile in-process subagent swarms. Every task is a row in the DB; every handoff is a row anyone (agent or human) can read and write; every worker is a full OS process with its own identity. This note documents the **data model** — the entities (board, task, link, comment, workspace, dispatcher, tenant), the tool-surface vs CLI-surface duality, how Kanban contrasts with `delegate_task`, multi-board isolation, file attachments, the two-table task↔run model with structured handoff, the full `task_events` vocabulary, and the single-host scope boundary. How agents *drive* the board (worker/orchestrator lifecycle) and how humans operate it (dashboard, CLI, slash command) are documented in the sibling procedure notes.

The board has **two front doors over the same `kanban_db` layer**: the model talks to it through a `kanban_*` toolset, while humans/scripts/cron talk through `hermes kanban …`, `/kanban …`, or the dashboard. Both route through the same kernel so reads see a consistent view and writes cannot drift.

## Kanban vs. `delegate_task`

They look similar but are different primitives. `delegate_task` is a function call (fork → join); Kanban is a durable work queue where every handoff is a row any profile (or human) can see and edit. The source's contrast table:

| | `delegate_task` | Kanban |
|---|---|---|
| Shape | RPC call (fork → join) | Durable message queue + state machine |
| Parent | Blocks until child returns | Fire-and-forget after `create` |
| Child identity | Anonymous subagent | Named profile with persistent memory |
| Resumability | None — failed = failed | Block → unblock → re-run; crash → reclaim |
| Human in the loop | Not supported | Comment / unblock at any point |
| Agents per task | One call = one subagent | N agents over task's life (retry, review, follow-up) |
| Audit trail | Lost on context compression | Durable rows in SQLite forever |
| Coordination | Hierarchical (caller → callee) | Peer — any profile reads/writes any task |

Use `delegate_task` when the parent needs a short reasoning answer before continuing, no humans involved, result goes back into the parent's context. Use Kanban when work crosses agent boundaries, must survive restarts, might need human input, might be picked up by a different role, or needs to be discoverable after the fact. They coexist — a kanban worker may call `delegate_task` internally during its run. Workloads Kanban covers that `delegate_task` can't: research triage, scheduled ops, persistent digital twins, engineering pipelines, and fleet work.

## Core concepts

The board's entities (full design rationale lives in `docs/hermes-kanban-v1-spec.pdf`):

- **Board** — a standalone queue of tasks with its own SQLite DB, workspaces directory, and dispatcher loop. One install can have many boards; single-project users stay on the `default` board.
- **Task** — a row with title, optional body, one assignee (a profile name), status (`triage | todo | ready | running | blocked | done | archived`), optional tenant namespace, and optional idempotency key (dedup for retried automation).
- **Link** — a `task_links` row recording a parent → child dependency. The dispatcher promotes `todo → ready` when all parents are `done`.
- **Comment** — the inter-agent protocol. Agents and humans append comments; a (re-)spawned worker reads the full comment thread as part of its context.
- **Workspace** — the directory a worker operates in, of three kinds: `scratch` (default fresh tmp dir under `~/.hermes/kanban/workspaces/<id>/`, **deleted on completion** — first scratch use emits a `tip_scratch_workspace` event), `dir:<path>` (an existing shared dir; **must be absolute** — relative paths are rejected as a confused-deputy escape vector; **preserved on completion**), and `worktree` (a git worktree under `.worktrees/<id>/` for coding tasks; **preserved on completion**).
- **Dispatcher** — a long-lived loop that every N seconds (default 60) reclaims stale claims, reclaims crashed workers (PID gone but TTL not yet expired), promotes ready tasks, atomically claims, and spawns assigned profiles. Runs **inside the gateway** by default (`kanban.dispatch_in_gateway: true`). After `kanban.failure_limit` consecutive spawn failures on the same task (default 2) it auto-blocks the task with the last error — preventing thrashing.
- **Tenant** — an optional string namespace *within* a board. One specialist fleet can serve multiple businesses (`--tenant business-a`) with data isolation by workspace path and memory key prefix. Tenants are a soft filter; **boards are the hard isolation boundary.**

## Boards (multi-project)

Boards separate unrelated streams of work into isolated queues. A new install has exactly one board, `default` (DB at `~/.hermes/kanban.db` for back-compat); boards are opt-in. Per-board isolation is absolute:

- Separate SQLite DB per board (`~/.hermes/kanban/boards/<slug>/kanban.db`).
- Separate `workspaces/` and `logs/` directories.
- Workers spawned for a task see **only** their board's tasks — the dispatcher sets `HERMES_KANBAN_BOARD` in the child env and every `kanban_*` tool reads it.
- Linking tasks across boards is not allowed (keeps the schema simple).

Board resolution order (highest precedence first): explicit `--board <slug>` → `HERMES_KANBAN_BOARD` env var → `~/.hermes/kanban/current` (persisted by `boards switch`) → `default`. Slugs are validated as lowercase alphanumerics + hyphens + underscores, 1-64 chars, must start with alphanumeric; slashes, spaces, dots, and `..` are rejected at the CLI layer so path-traversal tricks can't name a board. Archiving a board moves its dir to `boards/_archived/<slug>-<ts>/` (recoverable); `--delete` hard-deletes with no recovery.

## File attachments

Tasks can carry file attachments (PDFs, images, source documents) so a worker has its source material without pasting paths into the body. Upload via the dashboard drawer's **Attachments** section (multiple files, each capped at 25 MB). Files land under `<hermes-home>/kanban/attachments/<task_id>/` (or the per-board `boards/<slug>/attachments/<task_id>/`); set `HERMES_KANBAN_ATTACHMENTS_ROOT` to pin a custom location. When the dispatcher hands a task to a worker, the worker's context includes an **Attachments** section listing each file's name and **absolute path**, which the worker reads directly via file/terminal tools (`read_file`, `pdftotext`). Removing an attachment deletes both the metadata row and the on-disk file. On remote terminal backends (Docker, Modal), mount the board's `attachments/` directory into the sandbox so the absolute paths are reachable.

## Runs — one row per attempt

A task is a logical unit of work; a **run** is one attempt to execute it. When the dispatcher claims a ready task it creates a `task_runs` row and points `tasks.current_run_id` at it. When the attempt ends (completed, blocked, crashed, timed out, spawn-failed, reclaimed) the run row closes with an `outcome` and the task's pointer clears. A task attempted three times has three `task_runs` rows. Two tables (not just mutating the task) give **full attempt history** for postmortems and a clean place to hang per-attempt metadata (which files changed, which tests ran) — run facts, not task facts.

Runs are where **structured handoff** lives. On completion (`kanban_complete(...)`) a worker can pass `summary` (human handoff on the run; downstream children see it in `build_worker_context`), `metadata` (free-form JSON dict on the run, serialized alongside the summary for children), and `result` (a short log line on the task row, a legacy back-compat field). Downstream children read the most recent completed run's summary + metadata per parent; retrying workers read prior attempts on their own task so they don't repeat a failed path.

```
# What a worker actually does — a tool call, from inside the agent loop:
kanban_complete(
    summary="implemented token bucket, keys on user_id with IP fallback, all tests pass",
    metadata={"changed_files": ["limiter.py", "tests/test_limiter.py"], "tests_run": 14},
    result="rate limiter shipped",
)
```

Runs surface on the dashboard (Run History) and REST API (`GET /api/plugins/kanban/tasks/:id` returns a `runs[]` array). The `completed` event embeds the first-line summary (400-char cap). Key invariants: **bulk close with `--summary` is refused** (structured handoff is per-run); dragging a running task off `running` closes the in-flight run with `outcome='reclaimed'` rather than orphaning it; and completing/blocking a never-claimed task synthesizes a zero-duration run (`started_at == ended_at`) so attempt history stays complete. The terminal invariant: **`task_runs` is in a terminal state when `tasks.current_run_id` is `NULL`, and vice versa** — across CLI, dashboard, dispatcher, and notifier.

### Forward compatibility

Two nullable columns on `tasks` are reserved for v2 workflow routing: `workflow_template_id` (which template the task belongs to) and `current_step_key` (which step is active). The v1 kernel ignores them for routing but lets clients write them, so a v2 release can add the routing machinery without another schema migration.

## Event reference

Every transition appends a row to `task_events`; each carries an optional `run_id` so UIs can group events by attempt. Kinds cluster into three groups for filtering (`hermes kanban watch --kinds completed,gave_up,timed_out`).

**Lifecycle** (what changed about the task as a logical unit): `created` (`{assignee, status, parents, tenant}`, `run_id` NULL), `promoted` (`todo → ready` once all parents hit `done`, `run_id` NULL), `claimed` (`{lock, expires, run_id}` — atomic claim), `completed` (`{result_len, summary?}` — 400-char first-line handoff; full version on the run), `blocked` (`{reason}`), `unblocked` (`blocked → ready`), `archived` (carries the reclaimed `run_id` if the task was still running).

**Edits** (human-driven, not transitions): `assigned` (`{assignee}`), `edited` (`{fields}` — title/body), `reprioritized` (`{priority}`), `status` (`{status}` — dashboard drag-drop wrote a status directly; carries the reclaimed `run_id` when dragging off `running`).

**Worker telemetry** (about the execution process): `spawned` (`{pid}`), `heartbeat` (`{note?}`), `reclaimed` (`{stale_lock}` — TTL expired without completion), `crashed` (`{pid, claimer}` — PID dead but TTL not expired), `timed_out` (`{pid, elapsed_seconds, limit_seconds, sigkill}`), `stale` (ran past `kanban.dispatch_stale_timeout_seconds` default 4 h AND no heartbeat in the last hour — does NOT tick the failure counter), `respawn_guarded` (`{reason}` — `blocker_auth` / `recent_success` / `active_pr`; task stays `ready`), `spawn_failed` (`{error, failures}` — counter increments, task returns to `ready`), `protocol_violation` (`{pid, claimer, exit_code}` — worker exited 0 while task still `running`; dispatcher also emits `gave_up` and auto-blocks), `gave_up` (`{failures, effective_limit, limit_source, error}` — circuit breaker fired; effective limit resolves as task `max_retries` → dispatcher `failure_limit` → built-in default).

`hermes kanban tail <id>` shows these for one task; `hermes kanban watch` streams them board-wide.

## Out of scope

Kanban is deliberately **single-host**. `~/.hermes/kanban.db` is a local SQLite file and the dispatcher spawns workers on the same machine. Running a shared board across two hosts is not supported — there is no coordination primitive for "worker X on host A, worker Y on host B," and crash detection assumes PIDs are host-local. For multi-host, run an independent board per host and bridge them with `delegate_task` / a message queue. This is the trusted-local-user threat model: the same user owns all profiles, the worker runs with your uid, and `dir:` workspace paths are trusted (only relative-path traversal is rejected).

## Design spec

The complete design — architecture, concurrency correctness, comparison with Cline Kanban / Paperclip / NanoClaw / Google Gemini Enterprise, implementation plan, risks, and open questions — lives in `docs/hermes-kanban-v1-spec.pdf` in the repository. The source directs readers to read that before filing any behavior-change PR; the eight (plus a ninth triage-specifier) canonical collaboration patterns are documented there and in the worker/orchestrator procedure note.

**Source**: `inbox/hermes_agent_docs/user-guide/features/kanban.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
**Last Updated**: 2026-06-19
**Status**: Active
