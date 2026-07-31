---
tags:
  - resource
  - documentation
  - hermes_agent
  - context_compression
  - prompt_caching
keywords:
  - dual compression system
  - gateway session hygiene 85 percent
  - agent contextcompressor 50 percent
  - pluggable context engine abc
  - 4-phase compression algorithm
  - codex gpt-5.5 autoraise 272k
  - anthropic prompt caching system_and_3
topics:
  - Hermes Agent
  - Context Compression
  - Prompt Caching
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching
access_control_group: ["general"]
---

# Hermes Agent — Context Compression and Caching

## Overview

Context Compression and Caching is the Hermes Agent subsystem that keeps long conversations inside the model's context window without losing the thread of work. It is **two cooperating mechanisms**. First, a *dual compression system*: two independent compression layers — a **gateway session-hygiene safety net** that fires at 85% of context before the agent even sees a message, and the **agent's `ContextCompressor`** that fires at 50% of context (configurable) inside the tool loop with accurate API-reported token counts. Second, **Anthropic prompt caching**, which caches the conversation prefix to cut input-token cost by ~75% on multi-turn chats. Compression is built on a pluggable `ContextEngine` ABC (`agent/context_engine.py`), whose default implementation is `ContextCompressor` (`agent/context_compressor.py`) but which plugins can swap out (e.g. Lossless Context Management). This note documents the *behavior* of that subsystem; the user-facing config knobs live in the runtime-settings docs and the engine-plugin authoring path lives in the developer-extending docs (see Related Notes). This page owns the Hermes-specific term [term_context_compression](../../term_dictionary/term_context_compression.md). Source files: `agent/context_engine.py`, `agent/context_compressor.py`, `agent/prompt_caching.py`, `gateway/run.py` (session hygiene), `run_agent.py` (`_compress_context`).

## Pluggable Context Engine

Context management is built on the `ContextEngine` ABC (`agent/context_engine.py`). The built-in `ContextCompressor` is the default implementation, but plugins can replace it with alternative engines (e.g. Lossless Context Management). The engine is responsible for: deciding when compaction should fire (`should_compress()`), performing compaction (`compress()`), optionally exposing tools the agent can call (e.g. `lcm_grep`), and tracking token usage from API responses.

Selection is config-driven via `context.engine` in `config.yaml`:

```yaml
context:
  engine: "compressor"    # default — built-in lossy summarization
  engine: "lcm"           # example — plugin providing lossless context
```

The resolution order is: (1) check the `plugins/context_engine/<name>/` directory, (2) check the general plugin system (`register_context_engine()`), (3) fall back to the built-in `ContextCompressor`. Plugin engines are **never auto-activated** — the user must explicitly set `context.engine` to the plugin's name; the default `"compressor"` always uses the built-in. Configure via `hermes plugins` → Provider Plugins → Context Engine, or edit `config.yaml` directly.

## Dual Compression System

Hermes has two separate compression layers that operate independently. An incoming message first passes through **Gateway Session Hygiene** (pre-agent, rough estimate), which fires at 85% of context as a safety net for large sessions; then the **Agent `ContextCompressor`** (in-loop, real tokens) fires at 50% of context (default) for normal context management.

### 1. Gateway Session Hygiene (85% threshold)

Located in `gateway/run.py` (search for `Session hygiene: auto-compress`). This is a **safety net** that runs before the agent processes a message. It prevents API failures when sessions grow too large between turns (e.g. overnight accumulation in Telegram/Discord).

- **Threshold**: fixed at 85% of model context length.
- **Token source**: prefers actual API-reported tokens from the last turn; falls back to a rough character-based estimate (`estimate_messages_tokens_rough`).
- **Fires**: only when `len(history) >= 4` and compression is enabled.
- **Purpose**: catch sessions that escaped the agent's own compressor.

The gateway hygiene threshold is intentionally higher than the agent's compressor — setting it at 50% (same as the agent) caused premature compression on every turn in long gateway sessions.

### 2. Agent ContextCompressor (50% threshold, configurable)

Located in `agent/context_compressor.py`, this is the **primary compression system**. It runs inside the agent's tool loop with access to accurate, API-reported token counts, making it the normal path for context management.

## Configuration

All compression settings are read from `config.yaml` under the `compression` key; the summarization model/provider is configured under `auxiliary.compression`:

```yaml
compression:
  enabled: true              # Enable/disable compression (default: true)
  threshold: 0.50            # Fraction of context window (default: 0.50 = 50%)
  target_ratio: 0.20         # How much of threshold to keep as tail (default: 0.20)
  protect_last_n: 20         # Minimum protected tail messages (default: 20)
  codex_gpt55_autoraise: true  # gpt-5.5 on Codex OAuth: raise trigger to 85% (default: true)

auxiliary:
  compression:
    model: null              # Override model for summaries (default: auto-detect)
    provider: auto           # "auto", "openrouter", "nous", "main", etc.
    base_url: null           # Custom OpenAI-compatible endpoint
```

### Parameter Details

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `threshold` | `0.50` | 0.0-1.0 | Compression triggers when prompt tokens ≥ `threshold × context_length` |
| `target_ratio` | `0.20` | 0.10-0.80 | Controls tail protection budget: `threshold_tokens × target_ratio` |
| `protect_last_n` | `20` | ≥1 | Minimum number of recent messages always preserved |
| `protect_first_n` | `3` | (hardcoded) | System prompt + first exchange always preserved |
| `codex_gpt55_autoraise` | `true` | bool | Raise trigger to 85% for gpt-5.5 on the ChatGPT Codex OAuth route. Set `false` to keep the global `threshold` |

### Codex gpt-5.5 threshold autoraise

The ChatGPT Codex OAuth backend hard-caps gpt-5.5 at a **272K** context window (the same slug exposes 1.05M on OpenAI's direct API and OpenRouter, and 400K on GitHub Copilot). At the default 50% trigger, compaction would fire at ~136K — half the window the model can actually use. When the active route is Codex OAuth (`provider: openai-codex`) and the model is gpt-5.5, Hermes raises the trigger to **85%** (~231K) and prints a one-time notice with the opt-out command. Only this exact route is affected; gpt-5.5 on any other provider keeps the global `threshold`. To opt back down: `hermes config set compression.codex_gpt55_autoraise false`.

### Computed Values (for a 200K context model at defaults)

The threshold is derived from the **main** model's context window, never the auxiliary/summary model's: `threshold_tokens = threshold × context_length`. For a 200K model at defaults: `threshold_tokens = 200,000 × 0.50 = 100,000`; `tail_token_budget = 100,000 × 0.20 = 20,000`; `max_summary_tokens = min(200,000 × 0.05, 12,000) = 10,000`. On a 262,144-token model at the default `0.50` the threshold is `131,072` — its closeness to a common "128K context" is a coincidence of the percentage, not the auxiliary window. The auxiliary model's context window is a separate concern (it governs whether a summary can be *produced*, not *when* compression fires).

## Compression Algorithm

The `ContextCompressor.compress()` method follows a 4-phase algorithm.

**Phase 1 — Prune Old Tool Results (cheap, no LLM call).** Old tool results (>200 chars) outside the protected tail are replaced with `[Old tool output cleared to save context space]`. This cheap pre-pass saves significant tokens from verbose tool outputs (file contents, terminal output, search results).

**Phase 2 — Determine Boundaries.** The message list is split into a protected head, a summarized middle, and a protected tail:

```
┌─────────────────────────────────────────────────────────────┐
│  [0..2]   ← protect_first_n (system + first exchange)        │
│  [3..N]   ← middle turns → SUMMARIZED                        │
│  [N..end] ← tail (by token budget OR protect_last_n)         │
└─────────────────────────────────────────────────────────────┘
```

Tail protection is **token-budget based**: it walks backward from the end, accumulating tokens until the budget is exhausted, then falls back to the fixed `protect_last_n` count if the budget would protect fewer messages. Boundaries are aligned to avoid splitting tool_call/tool_result groups — `_align_boundary_backward()` walks past consecutive tool results to find the parent assistant message, keeping groups intact.

**Phase 3 — Generate Structured Summary.** The middle turns are summarized using the auxiliary LLM in a single `call_llm(task="compression")` call against a structured template with fixed sections: *Goal*, *Constraints & Preferences*, *Progress* (split into *Done* / *In Progress* / *Blocked*), *Key Decisions*, *Relevant Files*, *Next Steps*, and *Critical Context*. Summary budget scales with content compressed: `content_tokens × 0.20` (the `_SUMMARY_RATIO` constant), with a minimum of 2,000 tokens and a maximum of `min(context_length × 0.05, 12,000)`. A critical failure mode: the summary model must have a context window **at least as large** as the main model's — if smaller, the API returns a context-length error, `_generate_summary()` catches it, logs a warning, and returns `None`, after which the compressor drops the middle turns **without a summary**, silently losing context. This is the most common cause of degraded compaction quality.

**Phase 4 — Assemble Compressed Messages.** The compressed list is: (1) head messages (with a note appended to the system prompt on first compression), (2) the summary message (role chosen to avoid consecutive same-role violations), (3) tail messages (unmodified). Orphaned pairs are cleaned by `_sanitize_tool_pairs()`: tool results referencing removed calls are removed; tool calls whose results were removed get a stub result injected.

**Iterative Re-compression.** On subsequent compressions the previous summary (stored in the `_previous_summary` field) is passed to the LLM with instructions to **update** it rather than re-summarize from scratch — items move from "In Progress" to "Done", new progress is added, and obsolete information is removed.

The Before/After example in the source illustrates this: a 45-message ~95K-token conversation (30+ turns of file editing, testing, debugging) compacts to 25 messages ~45K tokens, where the middle turns collapse into a single `[CONTEXT COMPACTION]` assistant message carrying the structured-summary template (Goal, Progress, Relevant Files, Next Steps) while the protected head and recent tail survive verbatim.

## Prompt Caching (Anthropic)

Source: `agent/prompt_caching.py`. Prompt caching reduces input-token cost by ~75% on multi-turn conversations by caching the conversation prefix using Anthropic's `cache_control` breakpoints.

### Strategy: system_and_3

Anthropic allows a maximum of 4 `cache_control` breakpoints per request. Hermes uses "system_and_3":

```
Breakpoint 1: System prompt                     (stable across all turns)
Breakpoint 2: 3rd-to-last non-system message  ─┐
Breakpoint 3: 2nd-to-last non-system message   ├─ Rolling window
Breakpoint 4: Last non-system message          ─┘
```

`apply_anthropic_cache_control()` deep-copies the messages and injects markers; the default TTL is `5m`, with `1h` available for long sessions:

```python
marker = {"type": "ephemeral"}              # default 5m TTL
marker = {"type": "ephemeral", "ttl": "1h"} # 1-hour TTL
```

The marker placement depends on content type: string content is converted to `[{"type": "text", "text": ..., "cache_control": ...}]`; list content gets the marker on its last element; `None`/empty and tool messages get it as `msg["cache_control"]` (tool messages: native Anthropic only).

### Cache-Aware Design Patterns

1. **Stable system prompt** — it is breakpoint 1, cached across all turns; avoid mutating it mid-conversation (compression appends its note only on the first compaction).
2. **Message ordering matters** — cache hits require prefix matching, so adding/removing middle messages invalidates everything after.
3. **Compression interaction** — after compression the cache is invalidated for the compressed region but the system-prompt cache survives; the rolling 3-message window re-establishes caching within 1-2 turns.
4. **TTL selection** — default `5m`; use `1h` for long-running sessions with breaks between turns.

### Enabling Prompt Caching

Caching is automatic when the model is an Anthropic Claude model (detected by name) and the provider supports `cache_control` (native Anthropic API or OpenRouter). TTL is configurable (`"5m"` or `"1h"`):

```yaml
prompt_caching:
  cache_ttl: "5m"
```

The CLI shows status at startup, e.g. `💾 Prompt caching: ENABLED (Claude via OpenRouter, 5m TTL)`.

## Context Pressure Warnings

Intermediate context-pressure warnings have been removed (see the iteration-budget block in `run_agent.py`: "No intermediate pressure warnings — they caused models to 'give up' prematurely on complex tasks"). Compression fires when prompt tokens reach the configured `compression.threshold` (default 50%) with no prior warning step; gateway session hygiene fires as the secondary safety net at 85% of the model's context window.

**Source**: `inbox/hermes_agent_docs/developer-guide/context-compression-and-caching.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching
**Last Updated**: 2026-06-19
**Status**: Active
