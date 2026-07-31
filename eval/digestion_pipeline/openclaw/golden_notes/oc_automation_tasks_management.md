---
tags:
  - resource
  - documentation
  - openclaw
  - automation
  - tasks
keywords:
  - openclaw tasks cli
  - openclaw tasks list audit maintenance
  - chat task board /tasks
  - task pressure status integration
  - tasks runs.sqlite storage
  - automatic maintenance sweeper
  - task reconciliation pruning
topics:
  - OpenClaw
  - Background Tasks
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/automation/tasks
access_control_group: ["general"]
---

# OpenClaw — Managing Background Tasks (CLI, Chat Board, Storage & Maintenance)

## Overview

This note is the **management** procedure for OpenClaw background tasks: the operator tooling that inspects, cancels, audits, and reconciles the activity ledger of detached work (ACP runs, subagent spawns, isolated cron executions, and CLI agent commands). It covers the `openclaw tasks` CLI (`list`, `show`, `cancel`, `notify`, `audit`, `maintenance`, and `tasks flow`), the in-chat `/tasks` board, the `openclaw status` task-pressure summary, the on-disk SQLite storage layout (`runs.sqlite`), the 60-second automatic-maintenance sweeper, and how tasks relate to Task Flow, cron, heartbeat, sessions, and agent runs. It mirrors the management half of the `automation/tasks` source page; the task model, lifecycle states, and delivery/notification policies are documented in the sibling note [oc_automation_tasks_lifecycle](oc_automation_tasks_lifecycle.md).

## CLI reference

The `openclaw tasks` command surface inspects and manages individual task records.

`openclaw tasks list` lists all tasks newest-first and accepts optional filters:

```bash
openclaw tasks list [--runtime <acp|subagent|cron|cli>] [--status <status>] [--json]
```

Output columns are Task ID, Kind, Status, Delivery, Run ID, Child Session, and Summary.

`openclaw tasks show <lookup>` shows the full record for one task — timing, delivery state, error, and terminal summary. The `<lookup>` token accepts a task ID, run ID, or session key:

```bash
openclaw tasks show <lookup>
```

`openclaw tasks cancel <lookup>` cancels a task. For ACP and subagent tasks this **kills the child session**; for CLI-tracked tasks, cancellation is recorded in the task registry (there is no separate child runtime handle). Status transitions to `cancelled` and a delivery notification is sent when applicable.

`openclaw tasks notify <lookup> <policy>` changes a running task's notification policy:

```bash
openclaw tasks notify <lookup> <done_only|state_changes|silent>
```

`openclaw tasks audit` surfaces operational issues; findings also appear in `openclaw status` when issues are detected. The audit findings, their severity, and trigger are:

| Finding | Severity | Trigger |
| --- | --- | --- |
| `stale_queued` | warn | Queued for more than 10 minutes |
| `stale_running` | error | Running for more than 30 minutes |
| `lost` | warn/error | Runtime-backed task ownership disappeared; retained lost tasks warn until `cleanupAfter`, then become errors |
| `delivery_failed` | warn | Delivery failed and notify policy is not `silent` |
| `missing_cleanup` | warn | Terminal task with no cleanup timestamp |
| `inconsistent_timestamps` | warn | Timeline violation (for example ended before started) |

`openclaw tasks maintenance` previews reconciliation, cleanup stamping, and pruning; adding `--apply` performs them for tasks, Task Flow state, and stale cron run session-registry rows:

```bash
openclaw tasks maintenance [--json]
openclaw tasks maintenance --apply [--json]
```

Reconciliation is runtime-aware: ACP/subagent tasks check their backing child session; subagent tasks whose child session has a restart-recovery tombstone are marked lost instead of treated as recoverable; cron tasks check whether the cron runtime still owns the job, then recover terminal status from persisted cron run logs/job state before falling back to `lost` (only the Gateway process is authoritative for the in-memory cron active-job set — offline CLI audit uses durable history but does not mark a cron task lost solely because that local Set is empty); CLI tasks with run identity check the owning live run context, not just child-session or chat-session rows. Completion cleanup is also runtime-aware: subagent completion best-effort closes tracked browser tabs/processes for the child session before announce cleanup continues; isolated cron completion best-effort closes tracked browser tabs/processes for the cron session before the run fully tears down; isolated cron delivery waits out descendant subagent follow-up when needed and suppresses stale parent acknowledgement text instead of announcing it; subagent completion delivery uses the child's latest visible assistant text only (tool/toolResult output is not promoted into child result text, and terminal failed runs announce failure status without replaying captured reply text); cleanup failures do not mask the real task outcome. When applying maintenance, OpenClaw also removes stale `cron:<jobId>:run:<uuid>` session registry rows older than 7 days, while preserving rows for currently running cron jobs and leaving non-cron session rows untouched.

`openclaw tasks flow list | show | cancel` inspect the orchestrating Task Flow rather than one individual background-task record:

```bash
openclaw tasks flow list [--status <status>] [--json]
openclaw tasks flow show <lookup> [--json]
openclaw tasks flow cancel <lookup>
```

## Chat task board (`/tasks`)

Use `/tasks` in any chat session to see background tasks **linked to that session**. The board shows active and recently completed tasks with runtime, status, timing, and progress or error detail. When the current session has no visible linked tasks, `/tasks` falls back to agent-local task counts so you still get an overview without leaking other-session details. For the full operator ledger, use the CLI: `openclaw tasks list`.

## Status integration (task pressure)

`openclaw status` includes an at-a-glance task summary that surfaces "task pressure", for example:

```
Tasks: 3 queued · 2 running · 1 issues
```

The summary reports three aggregates: **active** is the count of `queued` + `running`; **failures** is the count of `failed` + `timed_out` + `lost`; and **byRuntime** is a breakdown by `acp`, `subagent`, `cron`, and `cli`. Both `/status` and the `session_status` tool use a cleanup-aware task snapshot — active tasks are preferred, stale completed rows are hidden, and recent failures only surface when no active work remains — keeping the status card focused on what matters right now.

## Storage and maintenance

### Where tasks live

Task records persist in SQLite at `$OPENCLAW_STATE_DIR/tasks/runs.sqlite`. The registry loads into memory at gateway start and syncs writes to SQLite for durability across restarts. The Gateway keeps the SQLite write-ahead log bounded by using SQLite's default autocheckpoint threshold plus periodic `PASSIVE` checkpoints; shutdown and explicit maintenance checkpoints still use `TRUNCATE` so normal closes can reclaim WAL space without making the background sweeper wait on active readers.

### Automatic maintenance

A sweeper runs every **60 seconds** and handles four things, in order:

1. **Reconciliation** — checks whether active tasks still have authoritative runtime backing. ACP/subagent tasks use child-session state, cron tasks use active-job ownership, and CLI tasks with run identity use the owning run context. If that backing state is gone for more than 5 minutes, the task is marked `lost`.
2. **ACP session repair** — closes terminal or orphaned parent-owned one-shot ACP sessions, and closes stale terminal or orphaned persistent ACP sessions only when no active conversation binding remains.
3. **Cleanup stamping** — sets a `cleanupAfter` timestamp on terminal tasks (`endedAt` + 7 days). During retention, lost tasks still appear in audit as warnings; after `cleanupAfter` expires or when cleanup metadata is missing, they are errors.
4. **Pruning** — deletes records past their `cleanupAfter` date.

For **retention**: terminal task records are kept for **7 days**, then automatically pruned, with no configuration needed.

## How tasks relate to other systems

**Tasks and Task Flow** — [Task Flow](oc_automation_taskflow.md) is the flow-orchestration layer above background tasks. A single flow may coordinate multiple tasks over its lifetime using managed or mirrored sync modes. Use `openclaw tasks` to inspect individual task records and `openclaw tasks flow` to inspect the orchestrating flow.

**Tasks and cron** — cron job definitions, runtime execution state, and run history live in OpenClaw's shared SQLite state database. **Every** cron execution creates a task record — both main-session and isolated — and main-session cron tasks default to the `silent` notify policy so they track without generating notifications.

**Tasks and heartbeat** — heartbeat runs are main-session turns, so they do not create task records; when a task completes, it can trigger a heartbeat wake so you see the result promptly.

**Tasks and sessions** — a task may reference a `childSessionKey` (where work runs) and a `requesterSessionKey` (who started it); its `agentId` identifies the agent executing the work, while the requester and owner fields preserve launch and control context. Sessions are conversation context; tasks are activity tracking on top of that.

**Tasks and agent runs** — a task's `runId` links to the agent run doing the work. Agent lifecycle events (start, end, error) automatically update the task status, so you do not need to manage the lifecycle manually.

**Source**: OpenClaw documentation — `automation/tasks` (mirror `inbox/openclaw_docs/automation/tasks.md`), management sections
**Last Updated**: 2026-06-22
**Status**: Active
