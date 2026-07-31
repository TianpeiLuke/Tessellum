---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - multi_agent
keywords:
  - kanban worker lane
  - assignee spawn terminator
  - kanban dispatcher
  - review-required convention
  - task_runs task_events
  - stale claim TTL
topics:
  - Hermes Agent
  - Kanban Automation
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-worker-lanes
access_control_group: ["general"]
---

# Hermes Agent — Kanban Worker Lanes

## Overview

A **worker lane** is a class of process that the Hermes kanban dispatcher can route tasks to — the unit of execution capacity behind a board. This page is the **lane contract**: it specifies the minimal interface any integration must satisfy to act as a worker, so that an operator can wire lanes into a board and a plugin/integration author can add a new lane shape (a CLI worker wrapping Codex / Claude Code / OpenCode, a containerised review worker, or a non-Hermes service that pulls tasks via the API). A lane is defined by exactly three things — an **assignee string** (identity), a **spawn mechanism** (how the dispatcher starts it), and a **lifecycle terminator** (how its run ends) — plus the audit trail that records each attempt. The kanban kernel owns lifecycle truth (`ready` → `running` → `blocked` / `done` / `archived`); lanes execute work but never own that truth, flowing everything back through the `kanban_*` tools (or the API for non-Hermes workers). The worker code that runs *inside* a lane is documented separately in the [`kanban-worker`](https://github.com/NousResearch/hermes-agent/blob/main/skills/devops/kanban-worker/SKILL.md) skill; this note describes the lane as a model — its parts, the review-required convention, and the failure modes the dispatcher absorbs so lane authors don't reimplement them.

## The Hierarchy

The contract sits inside a four-layer hierarchy that separates lifecycle truth from execution from review:

```text
Hermes Kanban  =  canonical task lifecycle + audit trail
Worker lane    =  implementation executor for one assigned card
Reviewer       =  human or human-proxy that gates "done"
GitHub PR      =  upstreamable artifact (optional, for code lanes)
```

Hermes Kanban owns lifecycle truth (`ready` → `running` → `blocked` / `done` / `archived`). Worker lanes execute work but never own that truth — everything they do flows back through the kanban kernel via the `kanban_*` tools (or, for non-Hermes external workers, via the API). Reviewers gate the transition from "code change written" to "task done."

## What a Lane Provides

To be a kanban worker lane, an integration must provide three things.

**1. An assignee string.** The dispatcher matches `task.assignee` against either a Hermes profile name (the default lane shape) or a registered non-spawnable identifier (the plugin lane shape). Tasks whose assignee doesn't resolve are left on `ready` with a `skipped_nonspawnable` event so a board operator can fix them — they are *not* silently dropped or executed by an arbitrary fallback.

**2. A spawn mechanism.** For Hermes profile lanes, the dispatcher's `_default_spawn` runs `hermes -p <assignee> chat -q <prompt>` (or the equivalent module form when the `hermes` shim isn't on `$PATH`) inside the task's pinned workspace, with these env vars set:

| Variable | Carries |
|---|---|
| `HERMES_KANBAN_TASK` | the task id the worker is operating on |
| `HERMES_KANBAN_DB` | absolute path to the per-board SQLite file |
| `HERMES_KANBAN_BOARD` | board slug |
| `HERMES_KANBAN_WORKSPACES_ROOT` | root of the board's workspace tree |
| `HERMES_KANBAN_WORKSPACE` | absolute path to *this* task's workspace |
| `HERMES_KANBAN_RUN_ID` | the current run's id (for the lifecycle gate) |
| `HERMES_KANBAN_CLAIM_LOCK` | the claim lock string (`<host>:<pid>:<uuid>`) |
| `HERMES_PROFILE` | the worker's own profile name (for `kanban_comment` author attribution) |
| `HERMES_TENANT` | tenant namespace, if the task has one |

For non-Hermes lanes (registered via a plugin), the plugin supplies its own `spawn_fn` callable that gets `task`, `workspace`, and `board`, and returns an optional pid for crash detection.

**3. A lifecycle terminator.** Every claim must end in exactly one of:

- `kanban_complete(summary=..., metadata=...)` — task succeeds, status flips to `done`.
- `kanban_block(reason=...)` — task waits for human input, status flips to `blocked`; the dispatcher respawns when `kanban_unblock` runs.
- The worker process exits without a tool call — the kernel reaps it and emits `crashed` (PID died), `gave_up` (consecutive-failure breaker tripped), or `timed_out` (max_runtime exceeded). This is the failure path; healthy workers don't end here.

The kanban kernel enforces that exactly one of these terminates each run. A worker that calls neither and exits normally is treated as crashed.

## Outputs and the Review-Required Convention

For most code-changing tasks, the work isn't truly *done* the moment the worker finishes — it needs a human reviewer. The kanban kernel doesn't enforce this distinction (a "code-changing task" is fuzzy, and forcing block-instead-of-complete on every code worker would break flows where no review is wanted). It is a convention layered on top:

- **Block instead of complete**, with `reason` prefixed `review-required: ` so the dashboard / `hermes kanban show` surfaces the row as awaiting review.
- **Drop structured metadata into a `kanban_comment` first**, since `kanban_block` only carries the human-readable `reason`. Comments are the durable annotation channel — every audit-relevant field (changed_files, tests_run, diff_path or PR url, decisions) belongs there.
- **Reviewer either approves and unblocks** (respawning the worker with the comment thread for follow-ups) **or asks for changes via another comment**, which the next worker run sees as part of `kanban_show`'s context.

The [`kanban-worker`](https://github.com/NousResearch/hermes-agent/blob/main/skills/devops/kanban-worker/SKILL.md) skill has worked examples for both `kanban_complete` (truly terminal tasks — typo fixes, docs changes, research writeups) and the `review-required` block pattern.

## Logs and Audit Trail

The dispatcher writes per-task worker stdout/stderr to `<board-root>/logs/<task_id>.log`. Logs are auditable from kanban metadata:

- **`task_runs`** rows carry the `log_path`, exit code (where available), summary, and metadata.
- **`task_events`** rows carry every state transition — `promoted`, `claimed`, `heartbeat`, `completed`, `blocked`, `gave_up`, `crashed`, `timed_out`, `reclaimed`, `claim_extended`.
- **`kanban_show`** returns both, so a reviewer (or a follow-up worker) reading the task gets the full history without needing dashboard access.

The dashboard renders run history with summaries, metadata blocks, and exit-status badges. CLI users can run `hermes kanban tail <task_id>` to follow live, or `hermes kanban runs <task_id>` for the historical attempt list.

## Existing Lane Shapes

**Hermes profile lane (default).** The shape every kanban worker takes today: the assignee is a profile name, the dispatcher spawns `hermes -p <profile>`, the worker auto-loads the [`kanban-worker`](https://github.com/NousResearch/hermes-agent/blob/main/skills/devops/kanban-worker/SKILL.md) skill plus the `KANBAN_GUIDANCE` system-prompt block, and uses the `kanban_*` tools to terminate the run. No setup beyond defining the profile. When you create profiles for your fleet, choose names that match the *role* you want the orchestrator to route to. The orchestrator (when there is one) discovers your profile names via `hermes profile list` — there's no fixed roster the system assumes.

**Orchestrator profile lane.** A specialisation of the profile lane: an orchestrator is a Hermes profile whose toolset includes `kanban` but *excludes* `terminal` / `file` / `code` / `web` for implementation. Its job is decomposing a high-level goal into child tasks via `kanban_create` + `kanban_link` and stepping back. The [`kanban-orchestrator`](https://github.com/NousResearch/hermes-agent/blob/main/skills/devops/kanban-orchestrator/SKILL.md) skill encodes the anti-temptation rules.

## Adding an External CLI Worker Lane

Wiring a non-Hermes CLI tool (Codex CLI, Claude Code CLI, OpenCode CLI, a local coding-model runner, etc.) as a kanban worker lane is *not yet a paved path*. The dispatcher's spawn function is pluggable (`spawn_fn` is a parameter on `dispatch_once`), and a plugin could register its own `spawn_fn` for a non-Hermes assignee — but the surrounding integration work is still per-integration design: wrapping the CLI's exit code into `kanban_complete` / `kanban_block` calls, mapping the CLI's workspace/sandbox conventions onto the dispatcher's `HERMES_KANBAN_WORKSPACE` env, and handling auth and per-CLI policy.

If you're considering adding a CLI lane, the source advises opening an issue describing the specific CLI and the workflow you're trying to enable. The contract above is the set of constraints any such lane must satisfy; the implementation shape (one plugin per CLI vs a generic CLI-runner plugin parameterised by config) is open. The historical issue for this is [#19931](https://github.com/NousResearch/hermes-agent/issues/19931) and the closed-not-merged Codex-specific PR [#19924](https://github.com/NousResearch/hermes-agent/pull/19924) — those describe the original architecture proposal but didn't land a runner.

## Failure Modes the Dispatcher Handles

So lane authors don't have to reimplement these:

- **Stale claim TTL** — a worker that claims and then never heartbeats / completes / blocks gets reclaimed after `DEFAULT_CLAIM_TTL_SECONDS` (15 min default), but *only if the worker process has actually died*. A live worker (a slow model spending 20+ min in one tool-free LLM call) gets the claim *extended* instead of killed; only a dead PID is reclaimed.
- **Crashed worker** — a worker whose host-local PID has vanished is detected by `detect_crashed_workers` and reaped; the task increments `consecutive_failures` and may auto-block when the breaker trips.
- **Run-level retry** — when a task is retried (post-block, post-crash, post-reclaim), the worker can use the `expected_run_id` parameter on terminating tools to fail fast if its own run was already superseded.
- **Per-task max runtime** — `task.max_runtime_seconds` hard-caps wall-clock time per run regardless of PID liveness, catching genuinely-deadlocked workers that the live-PID extension would otherwise keep running.
- **Stranded-task detection** — a ready task whose assignee never produces a claim within `kanban.stranded_threshold_seconds` (default 30 min) shows up in `hermes kanban diagnostics` as a `stranded_in_ready` warning. Severity escalates to error at 2x the threshold and critical at 6x. Catches typo'd assignees, deleted profiles, and down external worker pools in one identity-agnostic signal — no per-board allowlist to curate.

**Source**: `inbox/hermes_agent_docs/user-guide/features/kanban-worker-lanes.md`
**Last Updated**: 2026-06-19
**Status**: Active
