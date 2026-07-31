---
tags:
  - resource
  - documentation
  - openclaw
  - automation
  - taskflow
keywords:
  - openclaw task flow
  - durable scheduled workflow
  - managed mode mirrored mode
  - revision tracking conflict detection
  - openclaw tasks flow cli
  - reliable scheduled workflow pattern
  - flow registry sqlite wal
topics:
  - OpenClaw
  - Task Flow
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/automation/taskflow
access_control_group: ["general"]
---

# OpenClaw — Task Flow (Durable Scheduled-Workflow Orchestration)

## Overview

This note models **Task Flow**, OpenClaw's flow-orchestration substrate that sits above [background tasks](https://docs.openclaw.ai/automation/tasks) and manages durable multi-step flows with their own state, revision tracking, and sync semantics, while individual tasks remain the unit of detached work. It mirrors the `automation/taskflow` source page: when to reach for Task Flow versus a plain task or cron job, the reliable-scheduled-workflow layering pattern, the two sync modes (managed and mirrored), durable state plus revision tracking, cancel behavior, the `openclaw tasks flow` CLI, and how flows relate to tasks.

## When to Use Task Flow

Use Task Flow when work spans multiple sequential or branching steps and you need durable progress tracking across gateway restarts. For single background operations, a plain [task](https://docs.openclaw.ai/automation/tasks) is sufficient. The source page gives a four-row decision table:

| Scenario | Use |
| --- | --- |
| Single background job | Plain task |
| Multi-step pipeline (A then B then C) | Task Flow (managed) |
| Observe externally created tasks | Task Flow (mirrored) |
| One-shot reminder | Cron job |

## Reliable Scheduled Workflow Pattern

For recurring workflows such as market intelligence briefings, the page recommends treating the schedule, orchestration, and reliability checks as separate layers rather than one monolithic prompt. The four layers are: (1) use [Scheduled Tasks](https://docs.openclaw.ai/automation/cron-jobs) for timing; (2) use a persistent cron session when the workflow should build on prior context; (3) use [Lobster](https://docs.openclaw.ai/tools/lobster) for deterministic steps, approval gates, and resume tokens; and (4) use Task Flow to track the multi-step run across child tasks, waits, retries, and gateway restarts. The example cron shape that drives such a workflow:

```bash
openclaw cron add \
  --name "Market intelligence brief" \
  --cron "0 7 * * 1-5" \
  --tz "America/New_York" \
  --session session:market-intel \
  --message "Run the market-intel Lobster workflow. Verify source freshness before summarizing." \
  --announce \
  --channel slack \
  --to "channel:C1234567890"
```

Use `session:<id>` instead of `isolated` when the recurring workflow needs deliberate history, previous run summaries, or standing context; use `isolated` when each run should start fresh and all required state is explicit in the workflow. Inside the workflow, reliability checks go *before* the LLM summary step. The page's example workflow definition places a `preflight` and `collect` step ahead of `summarize`, then an `approve` step gated by `approval: required`, and a final `deliver` step gated by `condition: $approve.approved`:

```yaml
name: market-intel-brief
steps:
  - id: preflight
    command: market-intel check --json
  - id: collect
    command: market-intel collect --json
    stdin: $preflight.json
  - id: summarize
    command: market-intel summarize --json
    stdin: $collect.json
  - id: approve
    command: market-intel deliver --preview
    stdin: $summarize.json
    approval: required
  - id: deliver
    command: market-intel deliver --execute
    stdin: $summarize.json
    condition: $approve.approved
```

The page lists recommended preflight checks: browser availability and profile choice (for example `openclaw` for managed state or `user` when a signed-in Chrome session is required — see [Browser](https://docs.openclaw.ai/tools/browser)); API credentials and quota for each source; network reachability for required endpoints; required tools enabled for the agent, such as `lobster`, `browser`, and `llm-task`; and a failure destination configured for cron so preflight failures are visible (see [Scheduled Tasks](https://docs.openclaw.ai/automation/cron-jobs#delivery-and-output)). It also recommends attaching data-provenance fields to every collected item, with `sourceUrl`, `retrievedAt`, `asOf`, `title`, and `content`. The workflow should reject or mark stale items before summarization, and the LLM step should receive only structured JSON and be asked to preserve `sourceUrl`, `retrievedAt`, and `asOf` in its output; use [LLM Task](https://docs.openclaw.ai/tools/llm-task) when a schema-validated model step is needed inside the workflow. For reusable team or community workflows, package the CLI, `.lobster` files, and any setup notes as a skill or plugin and publish it through [ClawHub](https://docs.openclaw.ai/clawhub), keeping workflow-specific guardrails in that package unless the plugin API is missing a needed generic capability.

## Sync Modes

Task Flow has two sync modes that differ in whether the flow owns task creation.

### Managed mode

In managed mode, Task Flow owns the lifecycle end-to-end: it creates tasks as flow steps, drives them to completion, and advances the flow state automatically. The page's example is a weekly report flow that (1) gathers data, (2) generates the report, and (3) delivers it — Task Flow creates each step as a background task, waits for completion, then moves to the next step:

```
Flow: weekly-report
  Step 1: gather-data     → task created → succeeded
  Step 2: generate-report → task created → succeeded
  Step 3: deliver         → task created → running
```

### Mirrored mode

In mirrored mode, Task Flow observes externally created tasks and keeps flow state in sync without taking ownership of task creation. This is useful when tasks originate from cron jobs, CLI commands, or other sources and you want a unified view of their progress as a flow. The page's example is three independent cron jobs that together form a "morning ops" routine: a mirrored flow tracks their collective progress without controlling when or how they run.

## Durable State and Revision Tracking

Each flow persists its own state and tracks revisions so progress survives gateway restarts. Revision tracking enables conflict detection when multiple sources attempt to advance the same flow concurrently. The flow registry uses SQLite with bounded write-ahead-log maintenance, including periodic and shutdown checkpoints, so long-running gateways do not retain unbounded `registry.sqlite-wal` sidecar files.

## Cancel Behavior

`openclaw tasks flow cancel` sets a sticky cancel intent on the flow. Active tasks within the flow are cancelled, and no new steps are started. The cancel intent persists across restarts, so a cancelled flow stays cancelled even if the gateway restarts before all child tasks have terminated.

## CLI Commands

The page documents three `openclaw tasks flow` subcommands:

```bash
# List active and recent flows
openclaw tasks flow list

# Show details for a specific flow
openclaw tasks flow show <lookup>

# Cancel a running flow and its active tasks
openclaw tasks flow cancel <lookup>
```

| Command | Description |
| --- | --- |
| `openclaw tasks flow list` | Shows tracked flows with status and sync mode |
| `openclaw tasks flow show <id>` | Inspect one flow by flow id or lookup key |
| `openclaw tasks flow cancel <id>` | Cancel a running flow and its active tasks |

## How Flows Relate to Tasks

Flows coordinate tasks; they do not replace them. A single flow may drive multiple background tasks over its lifetime. Use `openclaw tasks` to inspect individual task records and `openclaw tasks flow` to inspect the orchestrating flow.

**Source**: OpenClaw documentation — `automation/taskflow` (mirror `inbox/openclaw_docs/automation/taskflow.md`)
**Last Updated**: 2026-06-22
**Status**: Active
