---
tags:
  - resource
  - documentation
  - hermes_agent
  - kanban
  - multi_agent
keywords:
  - kanban worker orchestrator
  - kanban_ toolset
  - kanban-worker skill
  - kanban-orchestrator skill
  - goal-mode cards
  - structured handoff
  - multi-tenant
  - collaboration patterns
topics:
  - Hermes Agent
  - Kanban
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
access_control_group: ["general"]
---

# Hermes Kanban — Workers & Orchestrators

## Overview

This note is the **operating procedure for the Hermes Kanban board**: how a human sets it up and how agents — both single-task **workers** and fan-out **orchestrators** — drive it. The board itself (the durable `~/.hermes/kanban.db` data model, tasks/runs/events) is documented in [hermes_kanban_multi_agent_board](hermes_kanban_multi_agent_board.md); this note covers the *verbs*. The board has two front doors over the same `kanban_db` layer: **you** (and scripts and cron) drive it through `hermes kanban …` on the CLI; **the model** drives it through a dedicated `kanban_*` toolset, *not* by shelling out to `hermes kanban`. Workers follow a fixed `kanban_show()` → work → `kanban_heartbeat()` → `kanban_complete()`/`kanban_block()` lifecycle taught by the bundled `kanban-worker` skill; orchestrators decompose, link, and assign without doing the work themselves, taught by `kanban-orchestrator`. Goal-mode cards (`--goal`) run a worker in a Ralph-style loop until a judge agrees, and tenant tagging lets one fleet serve multiple businesses.

## Quick start

The commands below are **you** (the human) setting up the board and creating tasks. Once a task is assigned, the dispatcher spawns the assigned profile as a worker, and from there the model drives the task through `kanban_*` tool calls, not CLI commands.

```bash
# 1. Create the board (you)
hermes kanban init

# 2. Start the gateway (hosts the embedded dispatcher)
hermes gateway start

# 3. Create a task (you — or an orchestrator agent via kanban_create)
hermes kanban create "research AI funding landscape" --assignee researcher

# 4. Watch activity live (you)
hermes kanban watch

# 5. See the board (you)
hermes kanban list
hermes kanban stats
```

When the dispatcher picks up `t_abcd` and spawns the `researcher` profile, the very first thing that worker's model does is call `kanban_show()` to read its task — it does **not** run `hermes kanban show t_abcd`.

**Gateway-embedded dispatcher (default).** The dispatcher runs inside the gateway process (`kanban.dispatch_in_gateway: true`, `dispatch_interval_seconds: 60`); if the gateway is up, ready tasks get picked up on the next 60 s tick. Override with `HERMES_KANBAN_DISPATCH_IN_GATEWAY=0` for debugging. Without a running gateway, `ready` tasks stay put and `hermes kanban create` warns at creation time. Running `hermes kanban daemon` as a separate process is **deprecated** in favor of the gateway; a `--force` escape hatch keeps the standalone daemon alive for one release cycle, but running both against the same `kanban.db` causes claim races and is unsupported.

**Idempotent create (automation / webhooks).** Passing `--idempotency-key "<key>"` makes the first call create the task while any subsequent call with the same key returns the existing task id instead of duplicating — e.g. `hermes kanban create "nightly ops review" --assignee ops --idempotency-key "nightly-ops-$(date -u +%Y-%m-%d)" --json`.

**Bulk CLI verbs.** All lifecycle verbs accept multiple ids so you can clean up a batch at once: `hermes kanban complete t_abc t_def --result "batch wrap"`, `hermes kanban archive t_abc t_def`, `hermes kanban unblock t_abc t_def`, and `hermes kanban block t_abc "need input" --ids t_def t_hij`.

## How workers interact with the board

**Workers do not shell out to `hermes kanban`.** When the dispatcher spawns a worker it sets `HERMES_KANBAN_TASK=t_abcd` in the child's env, and that env var flips on a dedicated **kanban toolset** in the model's schema. The same toolset is available to orchestrator profiles that enable `kanban` in their toolsets config. These tools read and mutate the board directly via the Python `kanban_db` layer — the same code path as the CLI.

| Tool | Purpose | Required params |
|---|---|---|
| `kanban_show` | Read the current task (title, body, prior attempts, parent handoffs, comments, pre-formatted `worker_context`). Defaults to the env's task id. | — |
| `kanban_list` | List task summaries with filters for `assignee`, `status`, `tenant`, archived visibility, limit. For orchestrators discovering work. | — |
| `kanban_complete` | Finish with `summary` + `metadata` structured handoff. | at least one of `summary` / `result` |
| `kanban_block` | Escalate for human input with a `reason`. | `reason` |
| `kanban_heartbeat` | Signal liveness during long operations. Pure side-effect. | — |
| `kanban_comment` | Append a durable note to the task thread. | `task_id`, `body` |
| `kanban_create` | (Orchestrators) fan out into child tasks with an `assignee`, optional `parents`, `skills`. | `title`, `assignee` |
| `kanban_link` | (Orchestrators) add a `parent_id → child_id` dependency edge after the fact. | `parent_id`, `child_id` |
| `kanban_unblock` | (Orchestrators) move a blocked task back to `ready`. | `task_id` |

A typical **worker** turn calls `kanban_show()` (no args — uses `HERMES_KANBAN_TASK`), does the work via terminal/file tools, heartbeats partway through, and finishes:

```
kanban_show()                                     # no args — uses HERMES_KANBAN_TASK
# (model reads worker_context, does the work via terminal/file tools)
kanban_heartbeat(note="halfway through — 4 of 8 files transformed")
kanban_complete(
    summary="migrated limiter.py to token-bucket; added 14 tests, all pass",
    metadata={"changed_files": ["limiter.py", "tests/test_limiter.py"], "tests_run": 14},
)
```

The "(Orchestrators)" tools (`kanban_list`, `kanban_create`, `kanban_link`, `kanban_unblock`, `kanban_comment` on foreign tasks) share the same toolset; the convention (enforced by the `kanban-orchestrator` skill) is that worker profiles don't fan out or route unrelated work, and orchestrator profiles don't execute implementation work. Dispatcher-spawned workers stay task-scoped for destructive lifecycle operations and cannot mutate unrelated tasks.

**Why tools instead of shelling to `hermes kanban`:** (1) **backend portability** — workers on a remote backend (Docker/Modal/SSH) can't run `hermes kanban` inside the container where `hermes` isn't installed and `kanban.db` isn't mounted, but the tools run in the agent's own Python process and always reach `~/.hermes/kanban.db`; (2) **no shell-quoting fragility** — structured tool args skip the `shlex`+`argparse` footgun of `--metadata '{...}'`; (3) **better errors** — tool results are structured JSON the model can reason about. There is also **zero schema footprint on normal sessions**: a regular `hermes chat` has no `kanban_*` tools unless the profile enables the toolset for orchestrator work.

**Recommended handoff evidence.** `kanban_complete(summary=…, metadata={…})` is intentionally flexible — `summary` is the human closeout, `metadata` is the machine-readable handoff downstream agents/reviewers/dashboards reuse without scraping prose. For engineering/review tasks, prefer keys like `changed_files`, `verification`, `dependencies`, `blocked_reason`, `retry_notes`, and `residual_risk` so the next reader can answer: what changed, how was it verified, what unblocks/retries it, and what risk is left open. Keep secrets, raw logs, tokens, OAuth material, and unrelated transcripts out of `metadata` — store pointers and summaries instead.

### The worker skill and protocol

Any profile that should work kanban tasks must load the `kanban-worker` skill, which teaches the lifecycle in tool calls: (1) `kanban_show()` on spawn; (2) `cd $HERMES_KANBAN_WORKSPACE` via the terminal tool; (3) `kanban_heartbeat(note=…)` every few minutes — **at least once an hour for work over 1 hour**, since the dispatcher reclaims tasks running past `kanban.dispatch_stale_timeout_seconds` (default 4 h) with no recent heartbeat; (4) `kanban_complete(...)` or `kanban_block(reason=…)`. That final terminal call is part of the protocol: if the worker process exits with status 0 while the task is still `running`, the dispatcher emits a `protocol_violation` event and auto-blocks instead of respawning — usually a sign the model wrote a plain-text answer and exited without the Kanban tool surface.

`kanban-worker` is a **bundled skill**, synced into every profile during install/update (no Skills Hub step). The dispatcher also auto-passes `--skills kanban-worker` when spawning every worker, so the pattern library is always available. Verify or restore it per profile:

```bash
hermes -p <your-worker-profile> skills list | grep kanban-worker
hermes -p <your-worker-profile> skills reset kanban-worker --restore
```

### Pinning extra skills to a task

When one task needs specialist context the assignee doesn't carry by default (a `translation` job, a `security-pr-audit` review), attach skills to the task directly rather than editing the profile. From an orchestrator agent use the `kanban_create` tool's `skills` array (`skills=["security-pr-audit", "github-code-review"]`); from a human repeat `--skill` (`--skill translation`); from the dashboard type the skills comma-separated in the inline-create form. These are **additive** to the built-in `kanban-worker` — the dispatcher emits one `--skills <name>` flag for each — and the names must match skills already installed on the assignee's profile (there is no runtime install).

### Goal-mode cards (`--goal`)

By default each worker gets **one shot** at its card. Pass `--goal` (CLI) or `goal_mode=True` (tool/dashboard) to run the worker in a **goal loop** — the same Ralph-style engine behind the `/goal` slash command: after every turn an auxiliary judge checks the worker's output against the card's title + body (the acceptance criteria), and while the work isn't done and the turn budget remains, the worker keeps going in the same session until the judge agrees, the worker terminates the task, or the budget runs out (which **blocks** the card for human review rather than exiting silently).

```bash
hermes kanban create "Translate the docs site to French" \
    --body "Acceptance: every page translated, no English left, links intact." \
    --assignee linguist \
    --goal \
    --goal-max-turns 15      # optional; default 20
```

Use goal-mode for open-ended, multi-step, or "keep going until X is true" cards; skip it for cheap one-shot work since the per-turn judge overhead isn't worth it and the dispatcher's retry/circuit-breaker already handles transient failures. The judge is only as good as the goal text, so write the body as **explicit acceptance criteria**.

### The orchestrator skill

A **well-behaved orchestrator does not do the work itself.** It decomposes the user's goal into tasks, links them, assigns each to one of your set-up profiles, and steps back. The `kanban-orchestrator` skill encodes this as tool-call patterns — anti-temptation rules, a Step-0 profile-discovery prompt (the dispatcher silently fails on unknown assignee names, so every card must ground in profiles that actually exist), and a decomposition playbook keyed on `kanban_create` / `kanban_link` / `kanban_comment`. A canonical orchestrator turn (two parallel researchers handing to a writer):

```
# Goal from user: "draft a launch post on the ICP funding landscape"
kanban_create(title="research ICP funding, NA angle",  assignee="researcher-a", body="…")  # → t_r1
kanban_create(title="research ICP funding, EU angle",  assignee="researcher-b", body="…")  # → t_r2
kanban_create(
    title="synthesize ICP funding research into launch post draft",
    assignee="writer",
    parents=["t_r1", "t_r2"],        # promoted to 'ready' when both researchers complete
    body="one-pager, neutral tone, cite sources inline",
)                                     # → t_w1
kanban_link(parent_id="t_r1", child_id="t_followup")   # add deps discovered later
kanban_complete(summary="decomposed into 2 parallel research tasks → 1 synthesis task")
```

`kanban-orchestrator` is also bundled and synced per profile (verify with `hermes -p orchestrator skills list | grep kanban-orchestrator`; restore with `skills reset kanban-orchestrator --restore`). For best results pair it with a profile whose toolsets are restricted to board operations (`kanban`, `gateway`, `memory`) so the orchestrator literally cannot execute implementation tasks even if it tries.

## Multi-tenant usage

When one specialist fleet serves multiple businesses, tag each task with a tenant. The board, dispatcher, and profile definitions are all shared; only the data is scoped — workers receive `$HERMES_TENANT` and namespace their memory writes by prefix. Tenants are a soft filter (boards are the hard isolation boundary).

```bash
hermes kanban create "monthly report" \
    --assignee researcher \
    --tenant business-a \
    --workspace dir:~/tenants/business-a/data/
```

## Collaboration patterns

The board supports nine canonical patterns without any new primitives — they compose from tasks, links, assignees, comments, tenants, and goal-mode:

| Pattern | Shape | Example |
|---|---|---|
| **P1 Fan-out** | N siblings, same role | "research 5 angles in parallel" |
| **P2 Pipeline** | role chain: scout → editor → writer | daily brief assembly |
| **P3 Voting / quorum** | N siblings + 1 aggregator | 3 researchers → 1 reviewer picks |
| **P4 Long-running journal** | same profile + shared dir + cron | Obsidian vault |
| **P5 Human-in-the-loop** | worker blocks → user comments → unblock | ambiguous decisions |
| **P6 `@mention`** | inline routing from prose | `@reviewer look at this` |
| **P7 Thread-scoped workspace** | `/kanban here` in a thread | per-project gateway threads |
| **P8 Fleet farming** | one profile, N subjects | 50 social accounts |
| **P9 Triage specifier** | rough idea → `triage` → `hermes kanban specify` expands body → `todo` | "turn this one-liner into a spec'd task" |

For worked examples of each, see `docs/hermes-kanban-v1-spec.pdf` in the repository.

**Source**: `inbox/hermes_agent_docs/user-guide/features/kanban.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
**Last Updated**: 2026-06-19
**Status**: Active
