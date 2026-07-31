---
tags:
  - resource
  - documentation
  - claude_code
  - scheduling
  - cron
keywords:
  - scheduled task execution
  - between-turns firing
  - jitter
  - seven-day expiry
  - cron expression reference
  - croncreate cronlist crondelete
  - 50-task cap
  - claude_code_disable_cron
  - session-scoped scheduling limitations
topics:
  - Claude Code
  - Automation & Scheduling
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/scheduled-tasks
access_control_group: ["general"]
---

# Claude Code — Scheduled Task Execution Model

## Overview

This note describes how Claude Code's **session-scoped scheduled tasks** actually fire and the rules that bound them: the between-turns scheduling loop, deterministic jitter, the seven-day expiry, the cron tools Claude uses under the hood, the 5-field cron expression grammar, the disable flag, and the inherent limitations of session-scoped scheduling. These are the runtime semantics behind the user-facing [`/loop` and one-time reminders](cc_loop_scheduled_tasks.md); for how to choose between session-scoped tasks and the durable alternatives, see the [scheduling options comparison](cc_scheduling_options_comparison.md).

Scheduled tasks require Claude Code v2.1.72 or later (check with `claude --version`). They are session-scoped: they live in the current conversation, stop when you start a new one, and are restored on `--resume`/`--continue` only if unexpired.

## How scheduled tasks run

The scheduler checks every second for due tasks and enqueues them at **low priority**. A scheduled prompt fires **between your turns, not while Claude is mid-response**. If Claude is busy when a task comes due, the prompt waits until the current turn ends.

All times are interpreted in your **local timezone**. A cron expression like `0 9 * * *` means 9am wherever you're running Claude Code, not UTC.

### Jitter

To avoid every session hitting the API at the same wall-clock moment, the scheduler adds a **deterministic offset** to fire times:

- **Recurring tasks** fire up to 30 minutes after the scheduled time (or up to half the interval, for tasks that run more often than hourly). An hourly job scheduled for `:00` may fire anywhere up to `:30`.
- **One-shot tasks** scheduled for the top or bottom of the hour fire up to 90 seconds early.

The offset is derived from the **task ID**, so the same task always gets the same offset. If exact timing matters, pick a minute that is not `:00` or `:30` — for example `3 9 * * *` instead of `0 9 * * *` — and the one-shot jitter will not apply.

### Seven-day expiry

Recurring tasks automatically **expire 7 days after creation**. The task fires one final time, then deletes itself. This bounds how long a forgotten loop can run. If you need a recurring task to last longer, cancel and recreate it before it expires, or use [Routines](https://code.claude.com/docs/en/routines) or [Desktop scheduled tasks](cc_desktop_scheduled_tasks.md) for durable scheduling.

## Manage scheduled tasks

Ask Claude in natural language to list or cancel tasks (for example, "what scheduled tasks do I have?" or "cancel the deploy check job"), or reference the underlying tools directly. Under the hood, Claude uses these tools:

| Tool | Purpose |
| :--- | :--- |
| `CronCreate` | Schedule a new task. Accepts a 5-field cron expression, the prompt to run, and whether it recurs or fires once. |
| `CronList` | List all scheduled tasks with their IDs, schedules, and prompts. |
| `CronDelete` | Cancel a task by ID. |

Each scheduled task has an **8-character ID** you can pass to `CronDelete`. A session can hold **up to 50 scheduled tasks at once**.

## Cron expression reference

`CronCreate` accepts standard 5-field cron expressions: `minute hour day-of-month month day-of-week`. All fields support wildcards (`*`), single values (`5`), steps (`*/15`), ranges (`1-5`), and comma-separated lists (`1,15,30`).

| Example | Meaning |
| :--- | :--- |
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour on the hour |
| `7 * * * *` | Every hour at 7 minutes past |
| `0 9 * * *` | Every day at 9am local |
| `0 9 * * 1-5` | Weekdays at 9am local |
| `30 14 15 3 *` | March 15 at 2:30pm local |

Day-of-week uses `0` or `7` for Sunday through `6` for Saturday. Extended syntax like `L`, `W`, `?`, and name aliases such as `MON` or `JAN` is **not supported**.

When both day-of-month and day-of-week are constrained, a date matches if **either** field matches. This follows standard vixie-cron semantics.

## Disable scheduled tasks

Set `CLAUDE_CODE_DISABLE_CRON=1` in your environment to disable the scheduler entirely. The cron tools and `/loop` become unavailable, and any already-scheduled tasks stop firing. See [Environment variables](https://code.claude.com/docs/en/env-vars) for the full list of disable flags.

## Limitations

Session-scoped scheduling has inherent constraints:

- Tasks only fire while Claude Code is running and **idle**. Closing the terminal or letting the session exit stops them firing.
- **No catch-up for missed fires.** If a task's scheduled time passes while Claude is busy on a long-running request, it fires once when Claude becomes idle, not once per missed interval.
- Starting a fresh conversation clears all session-scoped tasks. Resuming with `claude --resume` or `claude --continue` restores tasks that have **not expired**: recurring tasks within seven days of creation, and one-shot tasks whose scheduled time has not yet passed. Background Bash and monitor tasks are **never restored** on resume.

For cron-driven automation that needs to run unattended, the docs point to durable alternatives:

- [Routines](https://code.claude.com/docs/en/routines): run on Anthropic-managed infrastructure on a schedule, via API call, or on GitHub events
- [GitHub Actions](https://code.claude.com/docs/en/github-actions): use a `schedule` trigger in CI
- [Desktop scheduled tasks](cc_desktop_scheduled_tasks.md): run locally on your machine

**Source**: https://code.claude.com/docs/en/scheduled-tasks
**Last Updated**: 2026-06-13
**Status**: Active
