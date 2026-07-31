---
tags:
  - resource
  - terminology
  - hermes_agent
  - context-management
  - llm-summarization
  - agent_runtime
keywords:
  - Context Compression
  - dual-threshold compression
  - two-layer compaction
  - gateway session hygiene
  - ContextCompressor
  - 85 percent threshold
  - 50 percent threshold
  - codex gpt-5.5 autoraise
  - four-phase compression algorithm
  - iterative re-compression
  - structured summary template
topics:
  - Context management
  - LLM agent runtime
  - Hermes Agent architecture
  - Conversation summarization
language: markdown
date of note: 2026-06-20
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Context Compression

## Definition

**Context compression** is Hermes Agent's mechanism for keeping a long, multi-turn conversation inside the main model's finite context window by replacing older message history with an LLM-generated structured summary. What distinguishes Hermes' design from generic [compaction](term_compaction.md) is that it is **dual-threshold and two-layer**: two independent compression stages fire at different fill levels and from different positions in the request path. The *primary* layer is the in-loop agent `ContextCompressor`, which fires at 50% of the context window using accurate, API-reported token counts; the *secondary* layer is a gateway "session hygiene" safety net that fires at 85% using a rough character-based estimate, catching sessions that grew between turns (e.g. overnight accumulation in a Telegram/Discord channel) before the agent ever processes them.

Context compression solves the problem that an agent's transcript grows monotonically — verbatim tool outputs, file reads, exploratory dead-ends — until it exceeds the model budget and the API rejects the request, or the model's recall degrades (the "context rot" effect). Compression is a reversible, in-session compaction of the trajectory that strips redundant scaffolding while preserving the load-bearing state (goal, decisions, progress, relevant files, next steps) the agent needs to continue. It is the default implementation of Hermes' pluggable [Context Engine](term_context_engine.md) ABC — selectable via `context.engine` in `config.yaml`, replaceable by a plugin engine such as Lossless Context Management.

## Context

Context compression lives in the Hermes Agent runtime and spans two architectural positions. The gateway hygiene pass is in `gateway/run.py` (search `Session hygiene: auto-compress`) and runs *before* the agent loop, only when `len(history) >= 4` and compression is enabled. The primary compressor is `agent/context_compressor.py`, invoked from inside the agent tool loop (`run_agent.py`, search `_compress_context`) where real API token counts are available. The summarization itself is delegated to an **auxiliary** LLM (`auxiliary.compression.model`/`provider`), which may differ from the main agent model. The whole subsystem is the default behind the `ContextEngine` ABC in `agent/context_engine.py`, paired with a separate Anthropic [prompt caching](term_prompt_caching.md) layer (`agent/prompt_caching.py`) that reduces input-token cost on the *uncompressed* prefix. The gateway threshold is deliberately higher than the agent's — setting it to 50% (same as the agent) caused premature compression on every turn in long gateway sessions.

## Key Characteristics

- **Dual-threshold, two-layer design.** Agent `ContextCompressor` at 50% (configurable, primary, real tokens) + gateway session hygiene at a fixed 85% (safety net, rough estimate). The two layers operate independently so a session that escapes the in-loop compressor is still caught before an API failure.
- **Threshold is a fraction of the MAIN model's window.** The trigger is $\text{threshold\_tokens} = \text{threshold} \times \text{context\_length}$ where `context_length` is the main agent model's window, never the auxiliary/summary model's. For a 200K model at the default `0.50`, the trigger is 100,000 tokens.
- **Codex gpt-5.5 autoraise.** The ChatGPT Codex OAuth backend hard-caps gpt-5.5 at a 272K window; at the default 50% trigger compaction would fire at ~136K — half the usable window. When the active route is `provider: openai-codex` *and* the model is gpt-5.5, Hermes raises the trigger to 85% (~231K). Only this exact route is affected; `compression.codex_gpt55_autoraise: false` opts back to the global threshold.
- **Four-phase compress algorithm.** `ContextCompressor.compress()`: (1) **prune** old tool results >200 chars outside the protected tail to a placeholder (cheap, no LLM); (2) **determine boundaries** — `protect_first_n` (system + first exchange, hardcoded 3), middle turns to summarize, token-budget-based tail with `protect_last_n` fallback, aligned via `_align_boundary_backward()` so tool_call/tool_result groups stay intact; (3) **generate structured summary** of the middle via one `call_llm(task="compression")` against the auxiliary model; (4) **assemble** head + summary message + unmodified tail, then `_sanitize_tool_pairs()` cleans orphaned tool calls/results.
- **Structured-summary template.** The middle turns are summarized into a fixed template — Goal, Constraints & Preferences, Progress (Done / In Progress / Blocked), Key Decisions, Relevant Files, Next Steps, Critical Context — so the summary is parseable and the agent can resume reliably.
- **Token budgets.** Tail budget is $\text{threshold\_tokens} \times \text{target\_ratio}$ (default `0.20` → 20,000 for a 200K model). Summary budget scales with compressed content: $\text{content\_tokens} \times 0.20$, floored at 2,000 and capped at $\min(\text{context\_length} \times 0.05,\ 12{,}000)$.
- **Iterative re-compression.** On subsequent compactions the previous summary (`_previous_summary`) is passed back to the LLM with instructions to *update* it — items move from "In Progress" to "Done", new progress is added, obsolete items dropped — rather than re-summarizing from scratch, preserving information across multiple compactions.
- **Silent-degradation failure mode.** The summary model must have a window at least as large as the main model's, since the entire middle is sent in one call. If it is smaller, `_generate_summary()` catches the context-length error, logs a warning, returns `None`, and the compressor drops the middle turns *without* a summary — the most common cause of degraded compaction quality.
- **No intermediate pressure warnings.** Earlier "context pressure" warnings were removed because they caused models to give up prematurely on complex tasks; compression simply fires at the threshold with no prior warning step.

## Related Terms


## References

- [Effective context engineering for AI agents — Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Industry doc: the attention-budget framing and context-rot benchmark motivating compression.
- [Compaction — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/compaction) — Authoritative spec for the server-side `context_management.compaction` strategy that Hermes' agent-side compressor parallels.
- [ConversationSummaryBufferMemory — LangChain API Reference](https://python.langchain.com/api_reference/langchain/memory/langchain.memory.summary_buffer.ConversationSummaryBufferMemory.html) — Framework peer: summarizes earliest interactions while preserving the most-recent token budget, the closest external analogue to Hermes' tail-protected summarization.
