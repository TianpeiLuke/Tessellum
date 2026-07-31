---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - tasks
keywords:
  - openclaw tasks command
  - background task ledger
  - task flow state
  - tasks audit maintenance
  - runtime filter subagent acp cron cli
  - task status queued running lost
  - cron run session registry cleanup
  - tasks cancel notify
topics:
  - OpenClaw
  - CLI tasks command
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/tasks
access_control_group: ["general"]
---

# OpenClaw — The `openclaw tasks` Command

## Overview

This note documents the `openclaw tasks` CLI command — the operator surface for inspecting, auditing, and cancelling durable background tasks and Task Flow state in OpenClaw. It mirrors the `cli/tasks` source page: the default behavior, the root filter options (`--json`, `--runtime`, `--status`), and the seven subcommands (`list`, `show`, `notify`, `cancel`, `audit`, `maintenance`, `flow`). Background tasks are durable records of work run by the Gateway's runtimes; this command reads and reconciles that ledger from the CLI.

With no subcommand, `openclaw tasks` is equivalent to `openclaw tasks list`. The lifecycle and delivery model for background tasks live on the linked-out Background Tasks page (`/automation/tasks`); this command is the read/audit/cancel surface over that ledger, not the lifecycle definition.

## Usage

The full invocation surface (reproduced verbatim from source):

```bash
openclaw tasks
openclaw tasks list
openclaw tasks list --runtime acp
openclaw tasks list --status running
openclaw tasks show <lookup>
openclaw tasks notify <lookup> state_changes
openclaw tasks cancel <lookup>
openclaw tasks audit
openclaw tasks maintenance
openclaw tasks maintenance --apply
openclaw tasks flow list
openclaw tasks flow show <lookup>
openclaw tasks flow cancel <lookup>
```

## Root Options

These options apply at the root `openclaw tasks` level (verbatim from source):

- `--json`: output JSON.
- `--runtime <name>`: filter by kind: `subagent`, `acp`, `cron`, or `cli`.
- `--status <name>`: filter by status: `queued`, `running`, `succeeded`, `failed`, `timed_out`, `cancelled`, or `lost`.

The four `--runtime` kinds correspond to the runtime that produced the task: `subagent` (a delegated child agent), `acp` (an Agent Client Protocol routed task), `cron` (a scheduled job run), and `cli` (a CLI-launched task). The seven `--status` values are the task ledger's lifecycle states from `queued` through the terminal states (`succeeded`, `failed`, `timed_out`, `cancelled`, `lost`).

## Subcommands

### `list`

```bash
openclaw tasks list [--runtime <name>] [--status <name>] [--json]
```

Lists tracked background tasks newest first. This is the default action when `openclaw tasks` is run with no subcommand.

### `show`

`openclaw tasks show <lookup> [--json]` shows one task by task ID, run ID, or session key. The `<lookup>` selector accepts any of those three identifiers.

### `notify`

`openclaw tasks notify <lookup> <done_only|state_changes|silent>` changes the notification policy for a running task. The policy argument is one of `done_only`, `state_changes`, or `silent`.

### `cancel`

`openclaw tasks cancel <lookup>` cancels a running background task identified by `<lookup>`.

### `audit`

```bash
openclaw tasks audit [--severity <warn|error>] [--code <name>] [--limit <n>] [--json]
```

Surfaces stale, lost, delivery-failed, or otherwise inconsistent task and Task Flow records. Lost tasks retained until `cleanupAfter` are warnings; expired or unstamped lost tasks are errors. The `--severity` flag filters between `warn` and `error`, `--code <name>` filters by a specific finding code, and `--limit <n>` bounds the number of returned records.

### `maintenance`

```bash
openclaw tasks maintenance [--apply] [--json]
```

Previews or applies task and Task Flow reconciliation, cleanup stamping, pruning, and stale cron run session registry cleanup. Without `--apply` it previews; with `--apply` it performs the changes.

For cron tasks, reconciliation uses persisted run logs/job state before marking an old active task `lost`, so completed cron runs do not become false audit errors just because the in-memory Gateway runtime state is gone. Offline CLI audit is not authoritative for the Gateway's process-local cron active-job set. CLI tasks with a run id/source id are marked `lost` when their live Gateway run context is gone, even if an old child-session row remains.

When applied, maintenance also prunes `cron:<jobId>:run:<uuid>` session registry rows older than 7 days while preserving currently running cron jobs and leaving non-cron session rows untouched.

### `flow`

```bash
openclaw tasks flow list [--status <name>] [--json]
openclaw tasks flow show <lookup> [--json]
openclaw tasks flow cancel <lookup>
```

Inspects or cancels durable Task Flow state under the task ledger. `flow list` enumerates Task Flow records (optionally filtered by `--status <name>`), `flow show <lookup>` shows one record, and `flow cancel <lookup>` cancels it.

**Source**: OpenClaw documentation — `cli/tasks` (mirror `inbox/openclaw_docs/cli/tasks.md`)
**Last Updated**: 2026-06-22
**Status**: Active
