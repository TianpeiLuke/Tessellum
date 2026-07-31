---
tags:
  - resource
  - terminology
  - agentic_ai
  - llm
keywords:
  - delegate_task
  - Subagent Delegation
  - delegate task
  - subagent spawn tool
  - orchestrator-worker delegation
topics:
  - agentic AI
  - multi-agent systems
  - LLM tooling
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# delegate_task - Subagent Delegation Tool

## Definition

**`delegate_task`** is the Hermes Agent tool that spawns one or more isolated child `AIAgent`
instances ("subagents") to carry out a delegated workstream, then returns only each child's final summary to the parent's context. Each subagent starts from a **completely fresh conversation** — it has zero knowledge of the parent's history, prior tool calls, or anything discussed before the call — so the parent must pass everything the child needs through the tool's `goal` and `context` fields. A subagent receives a focused system prompt built from those fields, runs its own reasoning loop with a restricted toolset and its own terminal session, and reports back a structured summary of what it did, what it found, files modified, and issues encountered.

The tool exists to solve two problems at once: **context-window economy** (a large or noisy subtask is explored in the child's window and only its condensed result re-enters the parent, keeping parent token usage efficient) and **parallel breadth** (independent subtasks fan out concurrently rather than running serially in one long conversation). It is the LLM-agent realization of the classic orchestrator-worker pattern from multi-agent systems, where a lead agent coordinates while specialized workers operate in parallel on separate aspects of a problem.

## Context

`delegate_task` lives in the Hermes Agent **tool layer** (`repo_hermes_agent_tools`) and is executed by the agent core's orchestrator (`repo_hermes_agent_agent_core`), which builds each child's system prompt, runs the isolated conversation, and aggregates results. It is documented in the Hermes `hermes_subagent_delegation` user guide and is one of several automation/multi-agent execution surfaces alongside the durable `term_cron` scheduler, the standing-objective `term_persistent_goal` loop, and the mechanical `term_code_execution_tool` sandbox. Delegation is the **synchronous, reasoning-heavy** member of that family: it runs inside the parent's current turn and blocks until every child finishes or is cancelled, so for work that must outlive the turn the docs steer users to `cronjob` or background terminal jobs instead.

The same orchestrator-worker shape appears across the agent ecosystem — Anthropic's multi-agent research system spins up 3-5 subagents in parallel each with its own context window, and the broader `term_multi_agent_systems` / `term_agent_orchestration` literature formalizes task allocation via schemes such as the Contract Net Protocol. In Hermes, delegation also underpins offline scale: the batch trajectory runner reuses the same isolated-session machinery to generate `term_agent_trajectory` data.

## Key Characteristics

- **Fresh-context isolation**: each child gets a brand-new conversation; the only information it has is the `goal` + `context` the parent supplies. Vague delegation (e.g. "fix the error") fails because the child cannot see what "the error" refers to.
- **Single vs parallel batch**: a single `goal` runs directly; a `tasks=[...]` array runs subagents in parallel via a `ThreadPoolExecutor`. Default concurrency is **3** children per batch (`delegation.max_concurrent_children`, floor 1, no hard ceiling). Over-limit batches return a tool error rather than being silently truncated.
- **Result ordering & summary-only return**: results are sorted by task index to match input order regardless of completion order, and only each child's final structured summary re-enters the parent — intermediate tool calls never pollute the parent context.
- **Restricted toolsets**: the `toolsets` parameter scopes child tool access (e.g. `["terminal","file"]` for code work, `["web"]` for research). Leaf subagents are categorically blocked from `delegation`, `clarify`, `memory`, `code_execution`, and `send_message`.
- **Leaf vs orchestrator depth**: delegation is **flat** by default (`role="leaf"`, parent depth 0 → children depth 1, no further recursion). A `role="orchestrator"` child retains the `delegation` toolset, gated by `delegation.max_spawn_depth` (default 1 = flat). A global `orchestrator_enabled: false` kill switch forces every child to leaf. Cost compounds multiplicatively with depth × width (e.g. depth 3 × width 3 → up to 27 concurrent leaves).
- **Iteration & timeout budgets**: each child has a `max_iterations` tool-call cap (default 50). There is **no wall-clock timeout** by default; a positive `child_timeout_seconds` opts into a hard cap (floor 30s). A heartbeat-staleness monitor still detects genuinely wedged children.
- **Synchronous, non-durable lifetime**: runs inside the parent turn and blocks it. Interrupting the parent cancels all active children (and grandchildren), which return `status="interrupted"` with their in-progress work discarded. Children inherit the parent's API key, provider config, and credential pool, enabling `term_failover`-style key rotation on rate limits.
- **Delegation vs execute_code**: use `delegate_task` when the subtask needs full LLM reasoning, judgment, or multi-step problem solving; use `term_code_execution_tool` for mechanical, scripted, no-reasoning pipelines (lower token cost, only stdout returned).

## Related Terms


## References
- [Hermes Agent — Subagent Delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation)
- [How we built our multi-agent research system (Anthropic Engineering)](https://www.anthropic.com/engineering/built-multi-agent-research-system)
- [Multi-agent system (Wikipedia)](https://en.wikipedia.org/wiki/Multi-agent_system)
- [Contract Net Protocol (Wikipedia)](https://en.wikipedia.org/wiki/Contract_Net_Protocol)
