---
tags:
  - resource
  - terminology
  - openclaw
  - agent_framework
  - context_engine
  - context-management
  - acp-runtime-adapter
keywords:
  - Context Engine
  - context-engine registry
  - bootstrap maintain ingest afterTurn assemble compact
  - ACP runtime adapter
  - legacy compat shim
  - owner-scoped factory
  - LegacyContextEngine
  - delegateCompactionToRuntime
topics:
  - Context management
  - LLM agent runtime
  - OpenClaw architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://github.com/openclaw/openclaw/tree/main/src/context-engine
access_control_group: ["general"]
---

# Context Engine

## Definition

A **Context Engine** is a pluggable runtime component that owns the per-session lifecycle of an LLM agent's context window — deciding what to ingest into working state, how to assemble that state into the next prompt, and when to compact it back down so the conversation can keep running past the model's token budget. In OpenClaw the contract lives at `src/context-engine/types.ts` as the `ContextEngine` interface plus six lifecycle methods (`bootstrap`, `maintain`, `ingest`/`ingestBatch`, `afterTurn`, `assemble`, `compact`) and a `ContextEngineInfo` capability descriptor; concrete engines (the built-in `LegacyContextEngine` in `legacy.ts`, plus plugin-supplied engines) implement this interface and are registered into a process-global, owner-scoped factory map in `registry.ts`.

The component exists because **context is a finite, attention-budgeted resource with diminishing marginal returns** — Anthropic's "Effective context engineering for AI agents" frames this as treating the window as a budget, and shows that beyond a threshold the model's recall degrades (the *context rot* effect). LangChain's framing of agent context engineering as four operations — **write, select, compress, isolate** — maps directly onto the OpenClaw lifecycle: `ingest` and `afterTurn` are write/select operations on session state, `assemble` is the select-and-order step that produces the next prompt, and `compact` is the compress operation that delegates (via lazy import of `compact.runtime`) to OpenClaw's compaction subsystem. A Context Engine is therefore the **runtime-side counterpart to the design discipline of [context engineering](term_context_engineering.md)**: the discipline says *what* the right configuration of context is; the engine is the per-session machine that *enforces* it.

## Context

Context Engines appear in every agent framework that needs to run conversations longer than a single model call. Anthropic ships server-side compaction and tool-result clearing on the Claude Developer Platform as a managed Context Engine equivalent; Claude Sonnet 4.5+ and Haiku 4.5 add "context awareness" so the model can track its own token budget mid-conversation. LangChain/LangGraph implement Context Engines as checkpointers (short-term/thread-scoped) plus long-term memory stores, exposing the four-pillar API to agent authors. In OpenClaw, the Context Engine is the **ACP runtime adapter's main pluggable surface**: an [ACP](term_acp_agent_client_protocol.md) host (gateway, IDE plugin, voice runtime) registers exactly one engine per agent slot via `registerContextEngineForOwner`, and every turn of the agent loop flows through that engine's `assemble` → model call → `afterTurn` → optional `compact` cycle.

The OpenClaw implementation is deliberately a **compat shim** for legacy ACP runtimes. The `LegacyContextEngine` keeps the original sanitize/validate/limit pipeline (in `attempt.ts`) authoritative — its `ingest` and `afterTurn` are no-ops, `assemble` is pass-through, and only `compact` does real work by delegating to `compactEmbeddedPiSessionDirect`. The registry's Proxy wrapper intercepts the seven session-coupled methods to accept the legacy `sessionKey` (and `prompt`) parameters that newer engines no longer require, so older runtimes can register against the new interface without modification. This separation — generic interface in `types.ts`, legacy pass-through in `legacy.ts`, owner-scoped registration in `registry.ts`, lazy runtime bridge in `delegate.ts` — lets OpenClaw migrate to richer Context Engines (compaction-aware, memory-aware, sub-agent-aware) without breaking the existing fleet.

## Key Characteristics

- **Six-method lifecycle**: `bootstrap` (per-session init, optional history import), `maintain` (turn-triggered foreground/background maintenance), `ingest`/`ingestBatch` (capture new messages into engine state), `afterTurn` (post-turn bookkeeping), `assemble` (return ordered messages + token estimate + optional system-prompt addition for the next model call), `compact` (summarize and rotate the transcript when budget is exhausted).
- **`ContextEngineInfo` capability descriptor**: each engine declares `id`, `name`, `version`, `ownsCompaction` (so the runtime knows whether to schedule its own compaction pass), and `turnMaintenanceMode` (`foreground` vs `background`).
- **Owner-scoped factory registration**: `registerContextEngineForOwner(id, factory, owner)` returns a `{ ok: true } | { ok: false; existingOwner }` discriminated result so callers branch on conflict; the engines map is a `Symbol.for("openclaw.contextEngine.sessionKeyCompat")`-keyed process-global so duplicated dist chunks share it.
- **Session-key compat Proxy**: at resolution, every engine is wrapped in a Proxy that intercepts the seven session-coupled methods and strips the legacy `sessionKey` / `prompt` parameters when the underlying schema rejects them — keeps old ACP hosts working unchanged.
- **`LegacyContextEngine` as baseline**: ships with `id: "legacy"`; `ingest` and `afterTurn` are no-ops, `assemble` is pass-through (relies on `attempt.ts`), `compact` delegates to `delegateCompactionToRuntime` which lazy-imports `compact.runtime` across the bundler chunk boundary.
- **Runtime context per call**: `ContextEngineRuntimeContext` carries `tokenBudget`, `currentTokenCount`, `promptCache` telemetry (retention, last-call usage, cache-break observations), an `rewriteTranscriptEntries` callback, and an optional `llm.complete` capability — engines that need model inference (e.g. for summarization) get a runtime-provided completion path.
- **Mirrors the four-pillar discipline**: write (`ingest`/`afterTurn`) → select+compress (`assemble`) → compress further (`compact`) → isolate (sub-agent spawn hooks via `SubagentSpawnPreparation`). This is the LangChain agent-context taxonomy made executable.
- **Per-agent pluggability**: an OpenClaw agent config selects which Context Engine implementation to bind for its slot; the same agent class can run with the legacy engine in production and a richer memory-aware engine in development without code changes.

## Related Terms


## Related Code Snippets

- [OpenClaw Context Engine Registry — Owner-Scoped Factories](../code_snippets/snippet_openclaw_context_engine_registry_factories.md): The factory registration map, `Symbol.for` global singleton, and `WeakMap` owner tagging that make engines pluggable per agent slot.
- [OpenClaw Context Engine Registry — Session-Key Compat](../code_snippets/snippet_openclaw_context_engine_registry_compat.md): The Proxy wrapper that intercepts the seven session-coupled methods to strip legacy `sessionKey`/`prompt` parameters from ACP host calls.
- [OpenClaw Context Engine Delegate](../code_snippets/snippet_openclaw_context_engine_delegate.md): The `delegateCompactionToRuntime` lazy-import bridge that lets `LegacyContextEngine.compact` reach `compactEmbeddedPiSessionDirect` across the bundler chunk boundary.

## References

- [Anthropic Engineering. "Effective context engineering for AI agents."](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Class 2 industry doc: defines the attention-budget framing, context-rot benchmark, and the write/select/compress/isolate decomposition that the OpenClaw lifecycle mirrors.
- [Claude API Docs. "Context windows."](https://docs.anthropic.com/en/docs/build-with-claude/context-windows) — Class 1 authoritative spec: the per-model token budgets and server-side compaction/tool-result-clearing primitives that any Context Engine implementation must respect.
- [LangChain Docs. "Context engineering in agents."](https://docs.langchain.com/oss/python/langchain/context-engineering) — Class 2 framework doc: the canonical four-strategy (write/select/compress/isolate) framing that maps onto the OpenClaw six-method lifecycle.
- [LangChain Blog. "Context Engineering for Agents."](https://www.langchain.com/blog/context-engineering-for-agents) — Class 2 industry blog: short-term (thread-scoped) vs long-term memory split, and the LangGraph checkpointer pattern that is the closest peer to a Context Engine.
- [OpenClaw Source — `src/context-engine/`](https://github.com/openclaw/openclaw/tree/main/src/context-engine) — Primary implementation source: `types.ts` (interface + `ContextEngineInfo`), `legacy.ts` (`LegacyContextEngine`), `registry.ts` (owner-scoped factories + Proxy), `delegate.ts` (lazy runtime bridge).
