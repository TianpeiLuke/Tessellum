---
tags:
  - resource
  - terminology
  - openclaw
  - agent_framework
  - compaction
  - context-management
  - llm-summarization
keywords:
  - Compaction
  - context compaction
  - adaptive chunked compaction
  - identifier preservation
  - handoff instructions
  - SAFETY_MARGIN
  - BASE_CHUNK_RATIO
  - MIN_CHUNK_RATIO
  - chunkMessagesByMaxTokens
  - computeAdaptiveChunkRatio
  - MERGE_SUMMARIES_INSTRUCTIONS
  - HANDOFF_INSTRUCTIONS
  - summarizeChunks
  - summarizeForHandoff
  - resolveIdentifierPreservationInstructions
  - buildCompactionSummarizationInstructions
  - isOversizedForSummary
topics:
  - Context management
  - LLM agent runtime
  - OpenClaw architecture
  - Conversation summarization
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://github.com/openclaw/openclaw/blob/main/src/agents/compaction.ts
access_control_group: ["general"]
---

# Compaction

## Definition

**Compaction** is the runtime mechanism by which an LLM agent stays inside its finite context window over long, multi-turn sessions: the message history is replaced with an LLM-generated summary that preserves task state, active tool executions, decisions, and trailing user intent. In OpenClaw this contract lives in `src/agents/compaction.ts` (633 LOC) and is split into a **chunk-planning half** (adaptive chunk sizing under a safety margin) and a **prompt-policy half** (identifier preservation rules and handoff briefings). The same primitive is shipped under different names across the industry — Anthropic's Claude API exposes it as a server-side `context_management.compaction` strategy and as the Claude Code `/compact` slash command; Microsoft's Agent Framework calls it `ChatHistoryCompaction`; LangChain ships it as `ConversationSummaryMemory`/`ConversationSummaryBufferMemory`. All four implementations follow the same shape: detect that the budget is nearly exhausted, summarize the older portion of the trajectory, splice the summary into the front of the working transcript, and continue.

Compaction is distinct from both raw-context retention (cheap but bounded) and from RAG (retrieve-from-corpus, not summarize-the-trajectory): it is a **reversible compression of the in-session trajectory** that strips redundant scaffolding (verbatim tool-call payloads, duplicated read-file outputs, exploratory wrong paths) while keeping the load-bearing state the agent needs to continue. The arXiv ACON paper formalises this as "optimizing context compression for long-horizon LLM agents" and shows that without compaction, agent performance degrades as the conversation length approaches the context window — the "context rot" effect that Anthropic's compaction docs explicitly cite as the motivation for the feature.

## Context

OpenClaw's compactor is the concrete implementation behind the `compact` lifecycle method of every [Context Engine](term_context_engine.md) — when the engine's runtime context reports that `currentTokenCount` is approaching `tokenBudget`, the engine routes to `summarizeChunks` (the generic entry) or to one of its specialized wrappers (`summarizeWithFallback`, `summarizeForHandoff`). Compaction is invoked from three architectural positions: (a) **proactive** — Anthropic's cookbook recommends pausing at 60% context and running `/compact` with preservation notes; (b) **reactive** — Claude Code's auto-compact triggers at ~95% capacity; (c) **failover** — when a model hits its quota mid-session, `summarizeForHandoff` produces a leader-hierarchy briefing for the successor model so [Model Failover](term_model_failover.md) does not lose the agent's state.

The OpenClaw implementation is notable for applying the safety buffer at **three independent decision points** — the chunk planner divides `maxTokens` by `SAFETY_MARGIN`, the adaptive ratio classifier multiplies average message size by `SAFETY_MARGIN`, and the oversize predicate multiplies single-message size by `SAFETY_MARGIN` — so any one of them blocking is enough to keep the LLM call within budget despite the well-known underestimation of `estimateTokens()` (the `chars/4` heuristic that misses multi-byte chars, special tokens, JSON wrappers, and tool-call serialisations). The policy half is equally explicit: a strict-by-default identifier-preservation rule lists the identifier classes (UUIDs, hashes, IDs, hostnames, IPs, ports, URLs, file names) the LLM must echo verbatim, with `"off"` and `"custom"` policy arms for callers who need different contracts.

## Key Characteristics

- **Three policy constants under one safety multiplier** — `BASE_CHUNK_RATIO=0.4` (default chunk fraction of context window), `MIN_CHUNK_RATIO=0.15` (floor below which the adaptive classifier must not shrink), and `SAFETY_MARGIN=1.2` (20% buffer compensating for `estimateTokens` underestimation, applied at three independent decision points so the buffer is uniform across the file).
- **Token-budget chunk planner** — `chunkMessagesByMaxTokens` pre-divides the caller's `maxTokens` by `SAFETY_MARGIN` into an `effectiveMax` and packs messages with a flush-before-append guard plus a flush-after-append oversize-spill guard; `Math.max(1, ...)` clamps the effective budget so a degenerate `maxTokens=0` still progresses.
- **Adaptive chunk-ratio classifier** — `computeAdaptiveChunkRatio(messages, contextWindow)` multiplies the average message size by `SAFETY_MARGIN` first, then if `avgRatio > 0.1` reduces from `BASE_CHUNK_RATIO` toward `MIN_CHUNK_RATIO` by `Math.min(avgRatio * 2, BASE - MIN)`; empty input returns `BASE_CHUNK_RATIO` (no-evidence default is standard, not minimum).
- **Single-message oversize trigger** — `isOversizedForSummary(msg, ctx)` is a pure predicate `tokens * SAFETY_MARGIN > ctx * 0.5`; the half-window cutoff is a hard policy floor since below it the prompt + summary cannot both fit.
- **Merge-summaries prompt template** — `MERGE_SUMMARIES_INSTRUCTIONS` is a module-scope `string[].join("\n")` with `MUST PRESERVE` (active tasks, batch-operation progress, last user request, decisions, TODOs, follow-ups) and `PRIORITIZE recent context over older history` — the only place this contract is encoded, so the constant *is* the spec.
- **Identifier-preservation policy** — `resolveIdentifierPreservationInstructions` resolves a tri-state enum (`"strict" | "off" | "custom"`) into the rule string; `"off"` returns `undefined` (no rule), `"custom"` falls back to strict when the caller's text is empty/whitespace, default is `"strict"` (safe-by-default via `?? "strict"`).
- **Two-source instruction assembler** — `buildCompactionSummarizationInstructions` composes the per-call prompt from the resolved identifier rule plus the caller's `customInstructions` with a 2×2 truth table (both-empty → `undefined`; only custom → `Additional focus:\n…`; only identifier → identifier alone; both → identifier `\n\nAdditional focus:\n` custom); the `Additional focus:` label is load-bearing — it tells the LLM the second block is a *supplement*, not a replacement.
- **Handoff briefing template** — `HANDOFF_INSTRUCTIONS` is a module-scope `string[].join("\n")` encoding a `LEADER HIERARCHY REINFORCEMENT` directive (new model is `LEADER (Orchestrator)`, active autonomous units are `SUBORDINATES — supervise, do not perform`) plus a `MUST CAPTURE` checklist (goal, tool-execution status, files, next steps); used when the previous model hits a quota wall and a successor needs a smooth context transfer.
- **Specialized handoff entry** — `summarizeForHandoff` thin-wraps `summarizeWithFallback` with three contributions: prepend `HANDOFF_INSTRUCTIONS` (or merge with caller's custom), `Math.min(params.maxChunkTokens, 4000)` hard cap so the briefing fits in a successor's context, and `reserveTokens = SUMMARIZATION_OVERHEAD_TOKENS` (≈4096) headroom for the prompt itself.
- **Generic compaction entry** — `summarizeChunks` is the canonical pipeline: empty-input early return that yields `previousSummary` (preserves prior state), security strip of `toolResult.details` + runtime-context messages *before* chunking, chunk-plan via `chunkMessagesByMaxTokens`, per-call instruction assembly, per-chunk LLM call wrapped in `retryAsync` with `attempts: 3, minDelayMs: 500, maxDelayMs: 5000, jitter: 0.2, shouldRetry: !abort && !timeout`, exit with `summary ?? DEFAULT_SUMMARY_FALLBACK` so even a no-chunks path returns a defined string.
- **Carry-forward summary** — within `summarizeChunks` the previous chunk's summary becomes the next chunk's `previousSummary` so the per-chunk LLM call sees accumulating context rather than a fresh start.
- **Three invocation modes** — proactive (Anthropic recommends `/compact` at 60% capacity with preservation notes), reactive (Claude Code auto-compact at ~95%), failover (quota-wall handoff via `summarizeForHandoff`).

## Related Terms


## Related Code Snippets

- [OpenClaw Agents — compaction.ts (Part 1 of 2) — Chunk Ratio + Safety Margin + Merge-Summaries Instructions](../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md): The chunk-planning half — `BASE_CHUNK_RATIO`/`MIN_CHUNK_RATIO`/`SAFETY_MARGIN` constants, `chunkMessagesByMaxTokens` planner, `computeAdaptiveChunkRatio` classifier, `MERGE_SUMMARIES_INSTRUCTIONS` template, `isOversizedForSummary` trigger.
- [OpenClaw Agents — compaction.ts (Part 2 of 2) — Identifier Preservation + Leader-Handoff Briefing](../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md): The prompt-policy half — `resolveIdentifierPreservationInstructions` tri-state policy, `buildCompactionSummarizationInstructions` 2×2 assembler, `HANDOFF_INSTRUCTIONS` template, `summarizeForHandoff` wrapper, `summarizeChunks` entry/exit.

## References

- [Compaction — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/compaction) — Class 2 authoritative spec: Anthropic's server-side `context_management.compaction` strategy that replaces older turns with an LLM-generated summary; the canonical industry reference for the pattern.
- [Context engineering: memory, compaction, and tool clearing — Claude Cookbook](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools) — Class 2 industry doc: the proactive (60%) vs reactive (95%) compaction-invocation guidance and preservation-instruction contract that OpenClaw's `customInstructions` field implements.
- [ConversationSummaryMemory — LangChain API Reference](https://python.langchain.com/api_reference/langchain/memory/langchain.memory.summary.ConversationSummaryMemory.html) — Class 2 framework doc: the LangChain equivalent that continually summarizes the conversation history; `ConversationSummaryBufferMemory` is the closest peer to OpenClaw's adaptive chunked variant since it summarizes earliest interactions while preserving the most recent `max_token_limit` tokens.
- [Compaction — Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/agents/conversations/compaction) — Class 2 framework doc: Microsoft's `ChatHistoryCompaction` reducer; another industry instance of the same pattern, demonstrating that compaction is now a cross-framework primitive.
- [ACON: Optimizing Context Compression for Long-horizon LLM Agents (arXiv:2510.00615)](https://arxiv.org/abs/2510.00615) — Class 3 academic reference: formalises context compression for agent trajectories and quantifies how performance degrades without it.
- [Automatic summarization — Wikipedia](https://en.wikipedia.org/wiki/Automatic_summarization) — Class 1 reference on the broader NLP discipline (extractive vs abstractive summarization) that LLM-based conversation compaction is an instance of.
- [Context Engineering for Agents — LangChain Blog](https://www.langchain.com/blog/context-engineering-for-agents) — Class 2 industry blog: situates compaction inside the four-pillar write/select/compress/isolate taxonomy and contrasts it with RAG and isolation.
- [OpenClaw `src/agents/compaction.ts` source](https://github.com/openclaw/openclaw/blob/main/src/agents/compaction.ts) — Primary upstream source for the 633-LOC compactor.
