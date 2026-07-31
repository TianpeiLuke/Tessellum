---
tags:
  - resource
  - terminology
  - openclaw
  - agent_framework
  - subagent
  - multi-agent
  - spawn-orchestration
keywords:
  - subagent
  - subagent spawn
  - fork-or-isolate
  - agent orchestration
  - parent-child agent
  - spawn depth
  - children cap
  - ACP runtime
topics:
  - Multi-agent systems
  - Agent orchestration
  - OpenClaw architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://code.claude.com/docs/en/sub-agents
access_control_group: ["general"]
---

# Subagent

## Definition

A **subagent** is a delegated child agent spawned by a parent ("orchestrator") agent to handle a bounded sub-task within a larger multi-agent workflow, while remaining under the parent's control plane for lifecycle, policy, and result aggregation. Across modern agent frameworks the term contrasts with two adjacent patterns: a plain **agent** (top-level, no parent), and an **agent-as-a-tool** (a self-contained expert exposed as a transactional tool call). Subagents instead occupy a middle tier — they share context with the parent (full or summarized), participate in the parent's session lineage, and report terminal outcomes back through a lifecycle event stream rather than a single return value (Anthropic Claude Code; LangChain/LangGraph; OpenAI Codex).

The defining design choice is **fork-or-isolate**: a subagent is spawned either with an inherited copy of the parent's transcript (a "fork", so the child sees parent history) or with a clean context window (an "isolated" run, so noisy parent context does not leak in). In OpenClaw, this trichotomy is encoded as a `PreparedSpawnContext` discriminated union with arms `ok+isolated`, `ok+fork`, and `error`; spawn requests pass through a chain of policy gates (depth/children caps, ACP-runtime availability, target/agent allowlist, attachment-path sanitization, thread-binding capability) before a child `SessionEntry` is persisted and an admin-scope gateway call dispatches the child run. The same record carries `spawnDepth`, `spawnedWorkspaceDir`, and `subagentRole` so downstream cap-enforcement (`callerDepth >= maxSpawnDepth`, `activeChildren >= maxChildren`) and orphan-recovery (the registry's periodic sweeper) can reason about the lineage.

## Context

Subagents appear in three industry-prominent settings:

- **Anthropic Claude Code** ships a first-class `/fork` subagent that inherits the parent's full conversation, shares the prompt cache prefix (cutting token cost for children 2..N by up to ~90%), and can run with `isolation: "worktree"` so file edits land in a separate git worktree. A fork cannot spawn further forks (depth = 1 cap).
- **OpenAI Codex** runs subagent workflows that spawn specialized agents in parallel and collect results in one response — used for codebase exploration and multi-step feature plans.
- **LangGraph / LangChain** treats subagents as stateless tools owned by a supervisor; each invocation gets a clean context window, enforcing context isolation by construction.

In **OpenClaw** specifically, the subagent surface lives in `src/agents/subagent-spawn.ts` (1336 LOC, three-way split) and `src/agents/subagent-registry.ts` (also three-way split). `subagent-spawn.ts` orchestrates the spawn pipeline — workspace-inheritance resolution, ACP-runtime availability gate, attachment materialization with prompt-injection-hardened path sanitization, thread-binding hook, admin-scope gateway dispatch — while `subagent-registry.ts` is the in-process system-of-record for every running subagent: it owns the lifecycle CRUD (`running` → `done`/`timeout`/`failed`/`killed`), the announce-loop guard with grace-window deferred timers, persistence-resume across restarts, and the periodic sweeper that reconciles orphans.

## Key Characteristics

- **Fork-or-isolate context mode** — caller-supplied `requestedContext` ∈ {`fork`, `isolated`} overrides per-channel policy; cross-agent spawns force `isolated`; a soft fork-failure falls back to `isolated` with a `forkFallbackNote` that surfaces in the accepted-note suffix.
- **Quota gates** — spawn-depth cap (`maxSpawnDepth`), per-agent active-children cap (`maxChildren`), and target-agent allowlist all fire before the gateway dispatch; the persisted `SessionEntry.spawnDepth` is what `callerDepth` reads downstream.
- **ACP-runtime availability gate** — when the target agent runs on an Agent-Client Protocol runtime, `isAcpRuntimeSpawnAvailable` must return true before attachment materialization runs.
- **Agent-policy enforcement chain** — DM-policy/allowlist → target policy → admin-scope routing for `sessions.patch`/`sessions.delete` while `agent` stays at write scope, preventing privilege-cascade close(1008) errors.
- **Persistence-resume** — the registry's run records survive process restart via swappable `persistSubagentRunsToDisk` / `restoreSubagentRunsFromDisk` deps; resumed runs respect their announce retry budget.
- **Announce-loop guard** — transient lifecycle errors and aborted-end events go through `schedulePendingLifecycleError` / `schedulePendingLifecycleTimeout` with grace windows so flapping does not flush a terminal outcome prematurely.
- **Orphan recovery** — the periodic sweeper reconciles `running` rows that have no live execution context against the session store, marking them terminal rather than letting them leak.
- **Lifecycle-hook narrowing** — on spawn failure, `subagent_ended` is only emitted when `hasHooks("subagent_ended")` is true AND `threadBindingReady`, and the downstream `sessions.delete` carries `emitLifecycleHooks = !endedHookEmitted` so the gateway never broadcasts a duplicate event.

## FAQ

- **[FAQ: How does Claude Code's ultracode automatic dynamic-workflow orchestration work?](../faqs/faq_how_ultracode_orchestration_works.md)** — how a dynamic workflow orchestrates subagents at scale (≤16 concurrent / 1,000 per run) with results held in script variables
- **[FAQ: How is Claude Code's dynamic workflow feature implemented?](../faqs/faq_how_dynamic_workflow_implemented.md)** — the implementation internals: the `Workflow` tool schema, the `agent()`/`parallel()`/`pipeline()`/`phase()` primitives that spawn subagents, resume caching, and the Agent-SDK layering (documented vs. inferred)

## How-To Guides

- **[How To: Write a Claude Code Dynamic-Workflow Orchestration Script](../how_to/howto_write_dynamic_workflow_script.md)** — how each `agent()` call spawns one subagent, and how `pipeline()`/`parallel()` orchestrate many of them from one script

## Related Terms


## Related Code Snippets

- [Subagent Spawn — Caps + Workspace (split 1/3)](../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md): depth/children cap foundations + `PreparedSpawnContext` fork-or-isolate union.
- [Subagent Spawn — ACP + Attachments (split 2/3)](../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md): ACP-runtime availability gate + prompt-injection-hardened attachment-path sanitizer.
- [Subagent Spawn — Target Policy (split 3/3)](../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md): cross-agent workspace override + admin-scope gateway dispatch + rollback pyramid.
- [Subagent Registry — Lifecycle (split 1/3)](../code_snippets/snippet_openclaw_agents_subagent_registry_lifecycle.md): the in-memory `subagentRuns` system-of-record and terminal-outcome mapper.
- [Subagent Registry — Announce + Orphan Recovery (split 2/3)](../code_snippets/snippet_openclaw_agents_subagent_registry_announce.md): grace-window deferred timers + periodic sweeper.
- [Subagent Registry — Run Manager + Persistence-Resume (split 3/3)](../code_snippets/snippet_openclaw_agents_subagent_registry_run_manager.md): agent-event lifecycle dispatcher + dual-key terminal completer.

## References

- [Multi-agent system — Wikipedia](https://en.wikipedia.org/wiki/Multi-agent_system)
- [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [Subagents — LangChain Docs](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents)
- [Subagents — OpenAI Codex Developers](https://developers.openai.com/codex/subagents)
- [OpenClaw `src/agents/subagent-spawn.ts`](https://github.com/openclaw/openclaw/blob/main/src/agents/subagent-spawn.ts)
