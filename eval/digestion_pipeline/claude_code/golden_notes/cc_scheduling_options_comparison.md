---
tags:
  - resource
  - documentation
  - claude_code
  - scheduling
  - automation
keywords:
  - scheduling options comparison
  - cloud routines
  - desktop scheduled tasks
  - loop scheduled tasks
  - session-scoped scheduling
  - minimum interval
  - requires machine on
  - requires open session
topics:
  - Claude Code
  - Scheduling
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/scheduled-tasks
access_control_group: ["general"]
---

# Claude Code — Comparing Scheduling Options

## Overview

Claude Code offers **three ways to schedule recurring or one-off work**: **Cloud** routines (run on Anthropic-managed infrastructure), **Desktop** scheduled tasks (run locally on your machine), and **`/loop`** (session-scoped scheduling inside an open conversation). They differ along several axes — where the run executes, whether the machine must be on, whether a session must be open, persistence across restarts, access to local files, MCP-server source, permission handling, schedule customization, and the minimum interval. This note is the hub for the scheduling theme: it tabulates the trade-offs and points to the dedicated note for each option.

`/loop` tasks are the only ones that are **session-scoped**: they live in the current conversation and stop when you start a new one. Resuming with `--resume` or `--continue` brings back any task that has not expired (a recurring task created within the last 7 days, or a one-shot whose scheduled time has not passed). For scheduling that survives independently of any session, the docs direct you to Cloud routines, Desktop scheduled tasks, or GitHub Actions.

## Compare scheduling options

The same comparison table appears on both the `/loop` (scheduled-tasks) and Desktop scheduled-tasks pages:

|                            | Cloud          | Desktop | `/loop`      |
| :------------------------- | :----------------------------- | :------------------------------------- | :---------------------------------- |
| Runs on                    | Anthropic cloud                | Your machine                           | Your machine                        |
| Requires machine on        | No                             | Yes                                    | Yes                                 |
| Requires open session      | No                             | No                                     | Yes                                 |
| Persistent across restarts | Yes                            | Yes                                    | Restored on `--resume` if unexpired |
| Access to local files      | No (fresh clone)               | Yes                                    | Yes                                 |
| MCP servers                | Connectors configured per task | Config files and connectors            | Inherits from session               |
| Permission prompts         | No (runs autonomously)         | Configurable per task                  | Inherits from session               |
| Customizable schedule      | Via `/schedule` in the CLI     | Yes                                    | Yes                                 |
| Minimum interval           | 1 hour                         | 1 minute                               | 1 minute                            |

## How to choose

The docs give a one-line heuristic for each option:

- **Cloud tasks** — for work that should run reliably without your machine. Cloud routines run on Anthropic cloud infrastructure even when your computer is off, with the longest minimum interval (1 hour) and a fresh clone (no local-file access).
- **Desktop tasks** — when you need access to local files and tools. A Desktop task runs on your machine with direct access to your files, but only fires while the app is open and your computer is awake (1-minute minimum interval).
- **`/loop`** — for quick polling during a session. It runs on your machine, requires an open session, inherits the session's MCP servers and permissions, and is restored on `--resume` if unexpired (1-minute minimum interval).

For the full mechanics of each option, see its dedicated note: cloud routines in [cc_routines_overview](cc_routines_overview.md), session-scoped `/loop` in [cc_loop_scheduled_tasks](cc_loop_scheduled_tasks.md), and local Desktop tasks in [cc_desktop_scheduled_tasks](cc_desktop_scheduled_tasks.md). To react to events as they happen instead of polling, the source points to Channels (https://code.claude.com/docs/en/channels); to keep a session working until a condition is met rather than on an interval, it points to `/goal` (https://code.claude.com/docs/en/goal). For unattended CI scheduling, it points to GitHub Actions (https://code.claude.com/docs/en/github-actions).

**Source**: https://code.claude.com/docs/en/scheduled-tasks
**Last Updated**: 2026-06-13
**Status**: Active
