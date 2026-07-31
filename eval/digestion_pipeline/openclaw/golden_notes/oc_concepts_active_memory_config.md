---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - active_memory
keywords:
  - openclaw active memory config
  - openclaw.json plugins.entries.active-memory
  - active memory queryMode promptStyle
  - active memory toolsAllow memory_search memory_recall
  - cerebras gpt-oss-120b recall model
  - active-memory session toggle
  - modelFallback gemini-3-flash
  - setupGraceTimeoutMs cold-start grace
  - persistTranscripts transcriptDir
topics:
  - OpenClaw
  - Active Memory
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/active-memory
access_control_group: ["general"]
---

# OpenClaw — Configuring and Tuning Active Memory

## Overview

This note is the operator procedure for enabling and tuning OpenClaw **active memory** — the optional plugin-owned blocking memory sub-agent that surfaces relevant memory before the main reply. All configuration lives under `plugins.entries.active-memory` in `openclaw.json`. It covers the quick start, fast recall models (Cerebras), the `/active-memory` session toggle, session scoping, query-mode/prompt-style tuning, the model-fallback chain, memory-tool wiring (memory-core / LanceDB / Lossless Claw), advanced escape hatches, transcript persistence, the field tables, recommended setup with cold-start grace, and debugging — mirroring the procedure-side sections of `concepts/active-memory`. The conceptual "what/why/when it runs" half is in [oc_concepts_active_memory_overview](oc_concepts_active_memory_overview.md).

## Quick start

A safe-default `openclaw.json` setup — plugin on, scoped to the `main` agent, direct-message sessions only, inherits the session model:

```json5
{
  plugins: {
    entries: {
      "active-memory": {
        enabled: true,
        config: {
          enabled: true,
          agents: ["main"],
          allowedChatTypes: ["direct"],
          modelFallback: "google/gemini-3-flash",
          queryMode: "recent",
          promptStyle: "balanced",
          timeoutMs: 15000,
          maxSummaryChars: 220,
          persistTranscripts: false,
          logging: true,
        },
      },
    },
  },
}
```

Restart with `openclaw gateway`. `enabled: true` turns the plugin on; `config.agents: ["main"]` opts only the `main` agent in; `config.allowedChatTypes: ["direct"]` scopes it to direct sessions; `config.model` (unset) inherits the session model and `config.modelFallback` is used only when no explicit/inherited model resolves. Active memory still runs only for eligible interactive persistent chat sessions; inspect it live with `/verbose on` and `/trace on` (full field semantics in the field reference below).

## Speed recommendations (dedicated recall models)

Leaving `config.model` unset reuses your normal reply model — the safest default since it follows your existing provider, auth, and model preferences. To make recall feel faster, use a dedicated inference model: latency matters more here than on the main path, and the tool surface is narrow. Good fast-model options: `cerebras/gpt-oss-120b` for low-latency recall, or `google/gemini-3-flash` as a low-latency fallback.

### Cerebras setup

Add a Cerebras provider and point active memory at it:

```json5
{
  models: {
    providers: {
      cerebras: {
        baseUrl: "https://api.cerebras.ai/v1",
        apiKey: "${CEREBRAS_API_KEY}",
        api: "openai-completions",
        models: [{ id: "gpt-oss-120b", name: "GPT OSS 120B (Cerebras)" }],
      },
    },
  },
  plugins: {
    entries: {
      "active-memory": {
        enabled: true,
        config: { model: "cerebras/gpt-oss-120b" },
      },
    },
  },
}
```

Ensure the Cerebras API key has `chat/completions` access for the chosen model — `/v1/models` visibility alone does not guarantee it.

## Session toggle (`/active-memory`)

Pause or resume active memory for the current session without editing config: `/active-memory status`, `/active-memory off`, `/active-memory on`. This is session-scoped — it does not change `plugins.entries.active-memory.enabled`, agent targeting, or other global config. To write config and pause/resume for all sessions, use the global form (`/active-memory status --global`, `... off --global`, `... on --global`), which writes `plugins.entries.active-memory.config.enabled` and leaves `plugins.entries.active-memory.enabled` on so the command stays available. To see it live, enable `/verbose on` (status line `Active Memory: status=ok elapsed=842ms query=recent summary=34 chars`) and `/trace on` (debug summary `Active Memory Debug: Lemon pepper wings with blue cheese.`). Those lines come from the same pass that feeds the hidden prompt prefix but are sent as a follow-up diagnostic after the reply, so clients like Telegram do not flash a separate pre-reply bubble.

## Scoping by session type and id

`config.allowedChatTypes` controls which conversation kinds may run active memory; the default `["direct"]` runs in direct sessions but not groups/channels unless opted in (e.g. `["direct", "group"]` or `["direct", "group", "channel"]`). For narrower rollout, use `config.allowedChatIds` (an allowlist of resolved conversation ids: when non-empty, active memory runs only when the session's id is in the list, narrowing every allowed type at once) and `config.deniedChatIds` (a denylist that always wins over both). The ids come from the persistent channel session key (e.g. Feishu `chat_id` / `open_id`, Telegram chat id, Slack channel id) and matching is case-insensitive; if `allowedChatIds` is non-empty and no conversation id resolves, the turn is skipped. Example:

```json5
allowedChatTypes: ["direct", "group"],
allowedChatIds: ["ou_operator_open_id", "oc_small_ops_group"],
deniedChatIds: ["oc_large_public_group"]
```

## Query-mode and prompt-style tuning

`config.queryMode` controls how much conversation the sub-agent sees; pick the smallest mode that still answers follow-ups, and grow timeouts with context size (`message` < `recent` < `full`). `message` sends only the latest user message (fastest, strongest preference-recall bias; `config.timeoutMs` ~`3000`–`5000` ms); `recent` sends the latest message plus a small recent tail (best speed/grounding balance; ~`15000` ms); `full` sends the whole conversation (strongest recall, higher latency; ~`15000` ms+).

`config.promptStyle` controls recall eagerness/strictness. Styles: `balanced` (default for `recent`); `strict` (least eager; least bleed); `contextual` (most continuity-friendly); `recall-heavy` (softer plausible matches); `precision-heavy` (prefers `NONE` unless obvious); `preference-only` (favorites, habits, routines, taste, recurring personal facts). When unset the default mapping is `message -> strict`, `recent -> balanced`, `full -> contextual`; an explicit override wins (e.g. `promptStyle: "preference-only"`).

## Model fallback policy

If `config.model` is unset, active memory resolves a model in this order: explicit plugin model -> current session model -> agent primary model -> optional configured fallback. `config.modelFallback` controls the fallback step (e.g. `modelFallback: "google/gemini-3-flash"`). If none resolve, active memory skips recall for that turn. `config.modelFallbackPolicy` is a deprecated compatibility field that no longer changes runtime behavior.

## Memory-tool wiring per memory plugin

By default the recall sub-agent calls `memory_search` and `memory_get` (the built-in `memory-core` contract); when `plugins.slots.memory` is `memory-lancedb` and `config.toolsAllow` is unset, it uses `memory_recall` instead. For another plugin, set `config.toolsAllow` to the tool names that plugin registers. If none of the configured tools are available, or the sub-agent fails, active memory skips recall and the main reply continues without memory context. For custom recall tools, non-empty model-visible output counts as recall evidence unless structured result fields report an empty result or failure. `toolsAllow` accepts only concrete memory tool names — wildcards, `group:*`, and core tools (`read`, `exec`, `message`, `web_search`) are ignored. `memory_recall` is no longer in the memory-core default allowlist; an explicit `toolsAllow` always overrides the default.

- **Built-in memory-core** — no explicit `toolsAllow`; uses `["memory_search", "memory_get"]`.
- **LanceDB memory** — `memory-lancedb` exposes `memory_recall`; selecting `plugins.slots.memory: "memory-lancedb"` is enough. Its `config.embedding` sets `provider` (e.g. `openai`) and `model` (e.g. `text-embedding-3-small`).
- **Lossless Claw** — a context-engine plugin with its own recall tools; install/configure it as a context engine first (see Context engine). Do not include `lcm_expand` in `toolsAllow` — it is a lower-level delegated expansion tool.

Lossless Claw wiring enables `lossless-claw` and points active memory at its `lcm_*` tools with a provider-specific prompt:

```json5
{
  plugins: {
    entries: {
      "lossless-claw": { enabled: true },
      "active-memory": {
        enabled: true,
        config: {
          agents: ["main"],
          toolsAllow: ["lcm_grep", "lcm_describe", "lcm_expand_query"],
          promptAppend: "Use lcm_grep first for compacted conversation recall. Use lcm_describe to inspect a specific summary. Use lcm_expand_query only when the latest user message needs exact details that may have been compacted away. Return NONE if the retrieved context is not clearly useful.",
        },
      },
    },
  },
}
```

## Advanced escape hatches

These options are intentionally not part of the recommended setup. `config.thinking` overrides the sub-agent thinking level (e.g. `thinking: "medium"`); keep the default `thinking: "off"` because active memory runs in the reply path and extra thinking directly increases user-visible latency. `config.promptAppend` adds operator instructions after the default prompt and before the conversation context (e.g. `promptAppend: "Prefer stable long-term preferences over one-off events."`); use it with a custom `toolsAllow` for provider-specific tool order. `config.promptOverride` replaces the default prompt (the conversation context is still appended), e.g. `promptOverride: "You are a memory search agent. Return NONE or one compact user fact."`; not recommended unless testing a different recall contract, since the default is tuned to return `NONE` or compact user-fact context.

## Transcript persistence

Blocking sub-agent runs create a real `session.jsonl` transcript; by default it is temporary — written to a temp directory, used only for the run, and deleted immediately after. To keep transcripts on disk for debugging, set `persistTranscripts: true` and an optional relative `transcriptDir` (e.g. `"active-memory"`). When enabled, transcripts go in a separate directory under the target agent's sessions folder, not the main conversation path; the default layout is conceptually `agents/<agent>/sessions/active-memory/<blocking-memory-sub-agent-session-id>.jsonl`. Use carefully — they accumulate quickly on busy sessions, `full` mode duplicates much context, and they contain hidden prompt context and recalled memories.

## Configuration field reference

All configuration lives under `plugins.entries.active-memory`:

| Key | Type | Meaning |
| --- | --- | --- |
| `enabled` | `boolean` | Enables the plugin |
| `config.agents` | `string[]` | Agent ids that may use active memory |
| `config.model` | `string` | Recall model ref; unset uses session model |
| `config.allowedChatTypes` | `("direct" \| "group" \| "channel")[]` | Session types that may run; default direct |
| `config.allowedChatIds` | `string[]` | Allowlist after `allowedChatTypes`; non-empty fails closed |
| `config.deniedChatIds` | `string[]` | Denylist over allowed types/ids |
| `config.queryMode` | `"message" \| "recent" \| "full"` | How much conversation the sub-agent sees |
| `config.promptStyle` | `"balanced" \| "strict" \| "contextual" \| "recall-heavy" \| "precision-heavy" \| "preference-only"` | Recall eagerness/strictness |
| `config.toolsAllow` | `string[]` | Tool names; default `["memory_search","memory_get"]`/`["memory_recall"]` (lancedb); wildcards/`group:*`/core ignored |
| `config.thinking` | `"off" \| "minimal" \| "low" \| "medium" \| "high" \| "xhigh" \| "adaptive" \| "max"` | Thinking override; default `off` |
| `config.promptOverride` | `string` | Full prompt replacement; not recommended |
| `config.promptAppend` | `string` | Extra instructions appended to the prompt |
| `config.timeoutMs` | `number` | Hard sub-agent timeout, cap 120000 ms |
| `config.setupGraceTimeoutMs` | `number` | Extra setup budget; default 0, cap 30000 ms |
| `config.maxSummaryChars` | `number` | Max chars in the summary |
| `config.logging` | `boolean` | Emits active memory logs |
| `config.persistTranscripts` | `boolean` | Keeps sub-agent transcripts on disk |
| `config.transcriptDir` | `string` | Relative transcript subdir under sessions |
| `config.recentUserTurns` | `number` | Prior user turns (`recent` mode) |
| `config.recentAssistantTurns` | `number` | Prior assistant turns (`recent` mode) |
| `config.recentUserChars` | `number` | Max chars per recent user turn |
| `config.recentAssistantChars` | `number` | Max chars per recent assistant turn |
| `config.cacheTtlMs` | `number` | Cache reuse for identical queries (1000-120000 ms; default 15000) |
| `config.circuitBreakerMaxTimeouts` | `number` | Skip recall after N timeouts/agent-model (1-20; default 3) |
| `config.circuitBreakerCooldownMs` | `number` | Cooldown after the breaker trips (5000-600000 ms; default 60000) |

## Recommended setup

Start with `recent`:

```json5
{
  plugins: {
    entries: {
      "active-memory": {
        enabled: true,
        config: {
          agents: ["main"],
          queryMode: "recent",
          promptStyle: "balanced",
          timeoutMs: 15000,
          maxSummaryChars: 220,
          logging: true,
        },
      },
    },
  },
}
```

While tuning, use `/verbose on` for the status line and `/trace on` for the debug summary (sent after the main reply). Move to `message` for lower latency, or `full` if extra context is worth the slower sub-agent.

### Cold-start grace

Before v2026.5.2 the plugin silently extended `timeoutMs` by an extra 30000 ms during cold-start so model warm-up, embedding-index load, and the first recall shared one budget. v2026.5.2 moved that behind an explicit `setupGraceTimeoutMs` config — `timeoutMs` is now the recall-work budget by default unless you opt in. The hook adds two bounded phases: up to 1500 ms preflight before recall and a fixed 1500 ms for abort settlement/transcript recovery after; neither extends model or tool execution. If you upgraded from v2026.4.x and tuned `timeoutMs` for the old implicit-grace world (the starter `timeoutMs: 15000` is one), set `setupGraceTimeoutMs: 30000` to restore the pre-v5.2 budgets. It covers both the outer prompt-build watchdog and the inner recall run; worst-case blocking time is `timeoutMs + setupGraceTimeoutMs + 3000` ms. Lower values (5000–15000 ms) work on resource-tight gateways, at the cost of a higher chance of the first post-restart recall returning empty.

## Debugging

If active memory is not showing up: (1) confirm `plugins.entries.active-memory.enabled`; (2) confirm the current agent id is in `config.agents`; (3) confirm you are testing an interactive persistent chat session; (4) set `config.logging: true` and watch gateway logs; (5) verify memory search with `openclaw memory status --deep`. If hits are noisy, tighten `maxSummaryChars`. If too slow, lower `queryMode` and `timeoutMs` and reduce recent turn counts and per-turn char caps.

Active memory rides on the memory plugin's recall pipeline, so most recall surprises are embedding-provider problems, not active-memory bugs. When `memorySearch.provider` is unset OpenClaw uses OpenAI embeddings; set it explicitly for local, Ollama, Gemini, Voyage, Mistral, DeepInfra, Bedrock, GitHub Copilot, or OpenAI-compatible embeddings. If the provider cannot run, `memory_search` may degrade to lexical-only retrieval, and runtime failures after a provider is selected do not fall back automatically — set `memorySearch.fallback` only for a deliberate single fallback. A `status=timeout` first recall after a restart (v2026.5.2+) means cold-start setup has not finished (see Cold-start grace). With `ollama`, confirm the embedding model is installed via `ollama list`.

**Source**: OpenClaw documentation — `concepts/active-memory` (mirror `inbox/openclaw_docs/concepts/active-memory.md`)
**Last Updated**: 2026-06-22
**Status**: Active
