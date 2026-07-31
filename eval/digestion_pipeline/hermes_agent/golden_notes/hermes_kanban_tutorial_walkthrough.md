---
tags:
  - resource
  - documentation
  - hermes_agent
  - kanban
  - multi_agent
keywords:
  - kanban tutorial
  - four stories walkthrough
  - dependency promotion
  - structured handoff
  - circuit breaker crash recovery
  - task_runs attempt history
topics:
  - Hermes Agent
  - Kanban Multi-Agent Board
language: markdown
date of note: 2026-06-19
status: active
building_block: empirical_observation
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial
access_control_group: ["general"]
---

# Hermes Kanban Tutorial Walkthrough

## Overview

This is a **narrated, four-story walkthrough of the Hermes Kanban board in action** — a record of what the board actually does across the four use-cases it was designed for, watched with the dashboard open in a browser. Each story is an empirical demonstration: you (the human) run a few `hermes kanban` commands to seed work, the gateway's embedded dispatcher spawns worker agents that drive the board through the `kanban_*` toolset, and the dashboard/CLI show the resulting state. The tutorial assumes you know what a task, run, assignee, and dispatcher are (see the [Kanban overview](hermes_kanban_multi_agent_board.md)) and uses the `default` board throughout. The throughline across all four stories: **dependency promotion** moves work forward automatically, **structured `summary`/`metadata` handoff** carries context between stages, and **`task_runs` attempt history** records every try — block-then-retry, circuit-breaker give-up, and crash-then-recover are all just rows in `task_runs`, not afterthoughts.

A convention runs through every code block below: blocks labelled `bash` are commands **you** run; blocks labelled `# worker tool calls` are what a spawned worker's model emits — shown so the loop is visible end-to-end, not something you would run.

## Setup

```bash
hermes kanban init           # optional; first `hermes kanban <anything>` auto-inits
hermes dashboard             # opens http://127.0.0.1:9119 in your browser
# click Kanban in the left nav
```

The dashboard is the comfortable place for **you** to watch the system; the worker agents the dispatcher spawns never see the dashboard or the CLI — they drive the board only through the dedicated `kanban_*` toolset (`kanban_show`, `kanban_list`, `kanban_complete`, `kanban_block`, `kanban_heartbeat`, `kanban_comment`, `kanban_create`, `kanban_link`, `kanban_unblock`). All three surfaces route through the same per-board SQLite DB (`~/.hermes/kanban.db` for the default board, `~/.hermes/kanban/boards/<slug>/kanban.db` for any board created later), so each board stays consistent regardless of which side a change came from. Multiple isolated queues (one per project/repo/domain) are possible via separate boards, and workers physically cannot see tasks on other boards.

## The Board at a Glance

Six columns, left to right: **Triage** (raw ideas; by default the dispatcher auto-runs the decomposer here — it uses `auxiliary.kanban_decomposer`, reads the profile roster, and produces a graph of child tasks routed to best-fit specialists, holding the original alive as the parent so its assignee — `kanban.orchestrator_profile`, or the active default profile when unset — wakes back up to judge completion). The **Orchestration: Auto/Manual** pill switches modes; in Manual mode you click **⚗ Decompose** (or run `hermes kanban decompose <id>` / `/kanban decompose <id>`), while **✨ Specify** does a one-shot spec rewrite and promotes to `todo`. **Todo** (waiting on dependencies, or unassigned), **Ready** (assigned, waiting for the dispatcher to claim), **In progress** (a worker running; with "Lanes by profile" on — the default — sub-grouped by assignee), **Blocked** (a worker asked for human input, or the circuit breaker tripped), and **Done**.

The top bar filters by search, tenant, and assignee, plus a `Lanes by profile` toggle and a `Nudge dispatcher` button that runs one dispatch tick immediately instead of waiting for the daemon's next interval. Clicking any card opens its drawer. Toggling "Lanes by profile" off collapses In Progress to a single flat list ordered by claim time.

## Story 1 — Solo Dev Shipping a Feature

A classic feature flow — design a schema, implement the API, write the tests — modelled as three tasks with parent→child dependencies:

```bash
SCHEMA=$(hermes kanban create "Design auth schema" \
    --assignee backend-dev --tenant auth-project --priority 2 \
    --body "Design the user/session/token schema for the auth module." \
    --json | jq -r .id)

API=$(hermes kanban create "Implement auth API endpoints" \
    --assignee backend-dev --tenant auth-project --priority 2 \
    --parent $SCHEMA \
    --body "POST /register, POST /login, POST /refresh, POST /logout." \
    --json | jq -r .id)

hermes kanban create "Write auth integration tests" \
    --assignee qa-dev --tenant auth-project --priority 2 \
    --parent $API \
    --body "Cover happy path, wrong password, expired token, concurrent refresh."
```

Because `API` has `SCHEMA` as parent and `tests` has `API` as parent, only `SCHEMA` starts in `ready`; the other two sit in `todo` until their parents complete. This is the **dependency-promotion engine** — no worker picks up test-writing until there is an API to test. On the next dispatcher tick (60s by default, or immediately via **Nudge dispatcher**), the `backend-dev` profile spawns as a worker with `HERMES_KANBAN_TASK=$SCHEMA` in its env, and its tool-call loop reads, works, heartbeats, then completes with a structured handoff:

```python
# worker tool calls — NOT commands you run
kanban_show()
# → returns title, body, worker_context, parents, prior attempts, comments

# (worker reads worker_context, uses terminal/file tools to design the schema,
#  write migrations, run its own checks, commit — the real work happens here)

kanban_heartbeat(note="schema drafted, writing migrations now")

kanban_complete(
    summary="users(id, email, pw_hash), sessions(id, user_id, jti, expires_at); "
            "refresh tokens stored as sessions with type='refresh'",
    metadata={
        "changed_files": ["migrations/001_users.sql", "migrations/002_sessions.sql"],
        "decisions": ["bcrypt for hashing", "JWT for session tokens",
                      "7-day refresh, 15-min access"],
    },
)
```

`kanban_show` defaults `task_id` to `$HERMES_KANBAN_TASK`, so the worker need not know its own id. `kanban_complete` writes the summary + metadata onto the current `task_runs` row, closes that run, and transitions the task to `done` — one atomic hop through `kanban_db`. When `SCHEMA` hits `done`, the dependency engine promotes `API` to `ready`; the API worker, on pickup, calls `kanban_show()` and sees `SCHEMA`'s summary/metadata in the parent handoff, so it knows the schema decisions without re-reading a design doc. The completed task's drawer shows a Run History with one attempt — outcome `completed`, worker `@backend-dev`, duration, timestamp, full handoff summary — and the metadata blob (`changed_files`, `decisions`) is stored on the run and surfaced to any downstream worker. You can peek at the same data with `hermes kanban show $SCHEMA` and `hermes kanban runs $SCHEMA`.

## Story 2 — Fleet Farming

Three workers (translator, transcriber, copywriter) and a pile of independent tasks, all pulling in parallel — the simplest use-case and the one the original design optimized for. Seed the work as independent tasks (no parents), then start the gateway and walk away; it hosts the embedded dispatcher that picks up all three specialist profiles' tasks on the same `kanban.db`:

```bash
for lang in Spanish French German; do
    hermes kanban create "Translate homepage to $lang" \
        --assignee translator --tenant content-ops
done
hermes gateway start
```

Filtering the board to `content-ops` shows the In Progress column grouped by profile (the "Lanes by profile" default), so you see each worker's active task without scanning a mixed list; the dispatcher promotes the next ready task as soon as the current one completes. With three daemons on three assignee pools in parallel, the whole queue drains without further human input. **Structured handoff still applies** — a translator completing a call emits `kanban_complete(summary="translated 4 pages, style matched existing marketing voice", metadata={"duration_seconds": 720, "tokens_used": 2100})`, useful for analytics and any downstream dependent task.

## Story 3 — Role Pipeline with Retry

This is where Kanban earns its keep over a flat TODO list: a PM writes a spec, an engineer implements it, a reviewer rejects the first attempt, the engineer retries, and the reviewer approves — a three-stage chain (`Spec` DONE pm → `Implement` DONE backend-dev → `Review` READY reviewer). The interesting task is the implementation, because it was **blocked and retried** — the choreography as worker tool calls:

```python
# --- Engineer worker spawns on $IMPL (first attempt) ---
# worker tool calls
kanban_show()   # reads $SPEC's summary + acceptance metadata in worker_context
# (engineer writes code, runs tests, opens PR)
# Reviewer feedback arrives — engineer decides the concerns are valid and blocks
kanban_block(
    reason="Review: password strength check missing, reset link isn't "
           "single-use (can be replayed within 30min)",
)
# → $IMPL transitions to blocked; run 1 closes with outcome='blocked'
```

You (or a separate reviewer profile) read the block reason and unblock from the dashboard's "Unblock" button, or `hermes kanban unblock $IMPL` (or `/kanban unblock $IMPL` from chat). The dispatcher promotes `$IMPL` back to `ready` and, on the next tick, respawns the `backend-dev` worker — a **new run** on the same task whose `worker_context` now includes the run-1 block reason, so the second-pass worker knows which two things to fix instead of re-reading the whole spec, then `kanban_complete`s with fresh metadata (`review_iteration: 2`). The drawer shows **two attempts**: Run 1 `blocked` (review feedback under the outcome), Run 2 `completed` (fresh summary/metadata). Each run is a `task_runs` row with its own outcome/summary/metadata — **retry history is the primary representation, not a layer on top of "latest state."** When the reviewer's worker spawns and calls `kanban_show()`, its `worker_context` includes the parent's most-recent-completed-run summary + metadata, so it reads "added zxcvbn strength check, reset tokens are now single-use" with the changed-files list in hand before opening a diff.

## Story 4 — Circuit Breaker and Crash Recovery

Real workers fail (missing credentials, OOM kills, transient network errors), and the dispatcher has two defenses: a **circuit breaker** that auto-blocks after N consecutive failures so the board doesn't thrash, and **crash detection** that reclaims a task whose worker PID went away before its TTL expired.

```bash
hermes kanban create "Deploy to staging (missing creds)" \
    --assignee deploy-bot --tenant ops \
    --max-retries 3
```

The dispatcher tries to spawn the worker; spawn fails (`RuntimeError: AWS_ACCESS_KEY_ID not set`), so it releases the claim, increments a failure counter, and retries next tick. With `--max-retries 3`, the circuit trips after three consecutive failures: the task goes to `blocked` with outcome `gave_up` (omit the flag and Hermes uses `kanban.failure_limit`, default 2). The drawer shows three runs — first two `spawn_failed` (retryable), third `gave_up` (terminal) — and the event log shows `created → claimed → spawn_failed → claimed → spawn_failed → claimed → gave_up`. If Telegram/Discord/Slack is wired in, a gateway notification fires on `gave_up` so you hear about the outage without checking the board.

**Crash recovery** covers the spawn-succeeds-but-worker-dies-later case (segfault, OOM, `systemctl stop`): the dispatcher polls `kill(pid, 0)`, detects the dead pid, releases the claim, sends the task back to `ready`, and the next tick gives it to a fresh worker. The seed-data example is a migration OOM-killed at ~2.3M of 2.4M rows; the drawer shows Run 1 `crashed` (`OOM kill at row 2.3M (process 99999 gone)`) and Run 2 `completed` with `"strategy": "chunked with LIMIT + WHERE id > last_id"` in metadata — the retrying worker saw run 1's crash in its context and picked a safer strategy, making the change obvious to a future observer.

## Structured Handoff — Why `summary` and `metadata` Matter

In every story, workers call `kanban_complete(summary=..., metadata=...)` at the end — not decoration, but the **primary handoff channel between workflow stages**. When a worker on task B spawns and calls `kanban_show()`, the `worker_context` includes B's **prior attempts** (previous runs' outcome/summary/error/metadata — so a retrying worker doesn't repeat a failed path) and **parent task results** (for each parent, the most-recent completed run's summary + metadata — so downstream workers see why and how upstream work was done). This replaces the "dig through comments and work output" dance of flat kanban systems. The bulk-close guard exists because this data is per-run — `hermes kanban complete a b c --summary X` is refused (one summary copy-pasted to three tasks is almost always wrong), and `kanban_complete` is always single-task-at-a-time.

## Inspecting a Task Currently Running

For completeness: a task still in flight (the Story 1 API implementation, claimed by `backend-dev` but not yet complete) has status `Running`, and the active run appears in Run History with outcome `active` and no `ended_at`. If the worker dies or times out, the dispatcher closes this run and opens a new one on the next claim — the attempt row never disappears.

## Next Steps

The source closes with operator pointers: the [Kanban overview](hermes_kanban_multi_agent_board.md) for the full data model, event vocabulary, and CLI reference; `hermes kanban --help`; `hermes kanban watch --kinds completed,gave_up,timed_out` to live-stream terminal events across the board; and `hermes kanban notify-subscribe <task> --platform telegram --chat-id <id>` for a gateway ping when a specific task finishes.

**Source**: `inbox/hermes_agent_docs/user-guide/features/kanban-tutorial.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial
**Last Updated**: 2026-06-19
**Status**: Active
