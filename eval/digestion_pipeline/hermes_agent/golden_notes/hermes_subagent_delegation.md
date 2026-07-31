---
tags:
  - resource
  - documentation
  - hermes_agent
  - multi_agent
  - automation
keywords:
  - delegate_task
  - subagent delegation
  - parallel batch
  - orchestrator role
  - max_spawn_depth
  - child timeout
  - nested orchestration
topics:
  - Hermes Agent
  - Multi-Agent Delegation
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation
access_control_group: ["general"]
---

# Hermes Agent — Subagent Delegation

## Overview

Subagent delegation is the `delegate_task` tool that spawns **child `AIAgent` instances with isolated context, restricted toolsets, and their own terminal sessions**. Each child starts a completely fresh conversation, works independently to completion, and returns only its final summary to the parent — so the parent stays focused while heavy or parallelizable subtasks run off to the side. It is the in-turn fan-out mechanism in Hermes' automation surface: a single `delegate_task(goal=..., context=..., toolsets=[...])` call dispatches one child; a `tasks=[...]` array dispatches a parallel batch (up to 3 concurrent by default via a `ThreadPoolExecutor`). Delegation is synchronous and non-durable — it blocks the parent's current turn and discards in-progress work if the parent is interrupted — so for work that must outlive the turn you reach for `cronjob` or background `terminal` instead. The agent invokes delegation automatically when task complexity warrants it; you rarely ask for it explicitly.

## Single Task

```python
delegate_task(
    goal="Debug why tests fail",
    context="Error: assertion in test_foo.py line 42",
    toolsets=["terminal", "file"]
)
```

A single-task call runs directly without thread-pool overhead.

## Parallel Batch

Provide a `tasks` array to run subagents in parallel — up to 3 concurrent by default (configurable, no hard ceiling):

```python
delegate_task(tasks=[
    {"goal": "Research topic A", "toolsets": ["web"]},
    {"goal": "Research topic B", "toolsets": ["web"]},
    {"goal": "Fix the build", "toolsets": ["terminal", "file"]}
])
```

## How Subagent Context Works

**Critical — subagents know nothing.** Subagents start with a completely fresh conversation. They have zero knowledge of the parent's conversation history, prior tool calls, or anything discussed before delegation. The subagent's only context comes from the `goal` and `context` fields the parent populates when it calls `delegate_task`. The parent must therefore pass **everything** the subagent needs in the call:

```python
# BAD - subagent has no idea what "the error" is
delegate_task(goal="Fix the error")

# GOOD - subagent has all context it needs
delegate_task(
    goal="Fix the TypeError in api/handlers.py",
    context="""The file api/handlers.py has a TypeError on line 47:
    'NoneType' object has no attribute 'get'.
    The function process_request() receives a dict from parse_body(),
    but parse_body() returns None when Content-Type is missing.
    The project is at /home/user/myproject and uses Python 3.11."""
)
```

The subagent receives a focused system prompt built from the goal and context, instructing it to complete the task and provide a structured summary of what it did, what it found, any files modified, and any issues encountered.

## Practical Examples

The source gives three worked patterns: **Parallel Research** (a `tasks` batch of three `["web"]` research subagents collecting summaries simultaneously), **Code Review + Fix** (a single subagent given a project path, file list, and security focus areas with `toolsets=["terminal", "file"]`), and **Multi-File Refactoring** (a large refactor delegated to a fresh context so it does not flood the parent's window). Each demonstrates the same discipline: a precise `goal` plus a fully self-contained `context` block describing project path, files, framework, and the exact transformation/verification expected.

## Batch Mode Details

When you provide a `tasks` array, subagents run in **parallel** using a thread pool:

- **Maximum concurrency:** 3 tasks by default (configurable via `delegation.max_concurrent_children` or the `DELEGATION_MAX_CONCURRENT_CHILDREN` env var; floor of 1, no hard ceiling). Batches larger than the limit return a tool error rather than being silently truncated.
- **Thread pool:** Uses `ThreadPoolExecutor` with the configured concurrency limit as max workers.
- **Progress display:** In CLI mode, a tree-view shows tool calls from each subagent in real-time with per-task completion lines. In gateway mode, progress is batched and relayed to the parent's progress callback.
- **Result ordering:** Results are sorted by task index to match input order regardless of completion order.
- **Interrupt propagation:** Interrupting the parent (e.g., sending a new message) interrupts all active children.

Single-task delegation runs directly without thread-pool overhead.

## Model Override

Subagents can run on a different model via `config.yaml` — useful for delegating simple tasks to cheaper/faster models. Set `delegation.model` (e.g. `"google/gemini-flash-2.0"`) and optionally `delegation.provider` (e.g. `"openrouter"`) to route subagents to a cheaper model and/or a different provider; both keys appear in the consolidated §Configuration block below. If omitted, subagents use the same model as the parent.

## Toolset Selection Tips

The `toolsets` parameter controls what tools the subagent can access; choose based on the task. Common patterns: `["terminal", "file"]` for code work, debugging, file editing, and builds; `["web"]` for research, fact-checking, and documentation lookup; `["terminal", "file", "web"]` for full-stack tasks (the default); `["file"]` for read-only analysis and code review without execution; `["terminal"]` for system administration and process management.

Certain toolsets are **blocked for subagents regardless of what you specify**:

- `delegation` — blocked for leaf subagents (the default); retained for `role="orchestrator"` children, bounded by `max_spawn_depth`.
- `clarify` — subagents cannot interact with the user.
- `memory` — no writes to shared persistent memory.
- `code_execution` — children should reason step-by-step.
- `send_message` — no cross-platform side effects (e.g., sending Telegram messages).

## Max Iterations and Child Timeout

Each subagent has an iteration limit (default **50**) controlling how many tool-calling turns it can take; pass `max_iterations` to lower it for simple tasks. By default there is **no wall-clock timeout** on subagents — children fail only from API errors, tool errors, or hitting their iteration budget, never from a delegation-level stopwatch. (Earlier releases shipped a hard cap of 300s, later 600s, which kept killing legitimately busy children mid-task.) Genuinely stuck children are still caught: the heartbeat staleness monitor stops refreshing the parent's activity when a child makes no progress, letting the gateway inactivity timeout fire on a truly wedged worker.

A hard cap can be opted into per-install (useful for cost control on unattended cron-driven delegation):

```yaml
delegation:
  child_timeout_seconds: 0     # default: 0 = no timeout
  # child_timeout_seconds: 1800  # opt-in hard cap (floor 30s)
```

A positive value enforces a hard wall-clock limit on each child; `0` or a negative value disables it. With a hard cap configured, a subagent that times out having made **zero** API calls writes a structured diagnostic to `~/.hermes/logs/subagent-timeout-<session>-<timestamp>.log` (config snapshot, credential-resolution trace, and early error messages).

## Monitoring Running Subagents (`/agents`)

The TUI ships a `/agents` overlay (alias `/tasks`) that turns recursive `delegate_task` fan-out into a first-class audit surface: a live tree view of running and recently-finished subagents grouped by parent; per-branch cost, token, and file-touched rollups; kill and pause controls to cancel a specific subagent mid-flight without interrupting its siblings; and post-hoc review to step through each subagent's turn-by-turn history even after it returns to the parent. The classic CLI just prints `/agents` as a text summary — the TUI is where the overlay shines.

## Depth Limit and Nested Orchestration

By default, delegation is **flat**: a parent (depth 0) spawns children (depth 1), and those children cannot delegate further, preventing runaway recursive delegation. For multi-stage workflows, a parent can spawn **orchestrator** children that *can* delegate their own workers:

```python
delegate_task(
    goal="Survey three code review approaches and recommend one",
    role="orchestrator",  # Allows this child to spawn its own workers
    context="...",
)
```

- `role="leaf"` (default): child cannot delegate further — identical to flat-delegation behavior.
- `role="orchestrator"`: child retains the `delegation` toolset. Gated by `delegation.max_spawn_depth` (default **1** = flat, so `role="orchestrator"` is a no-op at defaults). Raise `max_spawn_depth` to 2 to allow orchestrator children to spawn leaf grandchildren; 3+ for deeper trees, with no upper ceiling — cost is the practical limit.
- `delegation.orchestrator_enabled: false`: global kill switch that forces every child to `leaf` regardless of the `role` parameter.

**Cost warning:** with `max_spawn_depth: 3` and `max_concurrent_children: 3`, the tree can reach 3×3×3 = 27 concurrent leaf agents — each extra level multiplies spend, so raise `max_spawn_depth` intentionally.

## Lifetime and Durability

`delegate_task` is **synchronous — not durable**. It runs inside the parent's current turn and blocks the parent until every child finishes (or is cancelled); it is not a background job queue. If the parent is interrupted (user sends a new message, `/stop`, `/new`), all active children are cancelled and return `status="interrupted"`, and their in-progress work is discarded. Children do not continue running after the parent turn ends. Cancelled children return a structured result (`status="interrupted"`, `exit_reason="interrupted"`), but because the parent was interrupted too, that result often never reaches a user-visible reply. For **durable long-running work** that must survive interrupts or outlive the current turn, use `cronjob` (action=`create`) — a separate agent run immune to parent-turn interrupts — or `terminal(background=True, notify_on_complete=True)` for long-running shell commands.

## Key Properties

- Each subagent gets its **own terminal session** (separate from the parent).
- **Nested delegation is opt-in** — only `role="orchestrator"` children can delegate further, and only when `max_spawn_depth` is raised from its default of 1 (flat). Disable globally with `orchestrator_enabled: false`.
- Leaf subagents **cannot** call `delegate_task`, `clarify`, `memory`, `send_message`, or `execute_code`. Orchestrator subagents retain `delegate_task` but still cannot use the other four.
- **Interrupt propagation** — interrupting the parent interrupts all active children (including grandchildren under orchestrators).
- Only the final summary enters the parent's context, keeping token usage efficient.
- Subagents inherit the parent's **API key, provider configuration, and credential pool** (enabling key rotation on rate limits).

## Delegation vs execute_code

Use `delegate_task` when the subtask requires **reasoning, judgment, or multi-step problem solving**: it runs a full LLM reasoning loop in a fresh isolated conversation with access to all non-blocked tools, runs up to 3 subagents concurrently by default, and costs more (full LLM loop). Use `execute_code` when you need **mechanical data processing or scripted workflows**: it is just Python code execution with no conversation, exposes 7 tools via RPC with no reasoning, runs a single script, and costs less (only stdout returned). Neither supports user interaction.

## Configuration

```yaml
# In ~/.hermes/config.yaml
delegation:
  max_iterations: 50                        # Max turns per child (default: 50)
  # max_concurrent_children: 3              # Parallel children per batch (default: 3)
  # max_spawn_depth: 1                      # Tree depth (floor 1, no ceiling, default 1 = flat)
  # orchestrator_enabled: true              # Disable to force all children to leaf role
  model: "google/gemini-3-flash-preview"    # Optional provider/model override
  provider: "openrouter"                    # Optional built-in provider
  api_mode: anthropic_messages              # optional; auto-detected from base_url
```

When `base_url` points at an Anthropic-compatible endpoint (e.g. a path ending in `/anthropic`, an Azure Foundry Claude route, or a MiniMax `/anthropic` proxy), `api_mode` is auto-detected as `anthropic_messages` so the subagent uses the right wire format. Set `api_mode` explicitly when the auto-detection guess is wrong (rare). The agent handles delegation automatically based on task complexity — you do not need to ask it to delegate explicitly.

**Source**: `inbox/hermes_agent_docs/user-guide/features/delegation.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation
**Last Updated**: 2026-06-19
**Status**: Active
