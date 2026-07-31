---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - prompt_caching
keywords:
  - openclaw prompt caching
  - cacheRetention none short long
  - contextPruning cache-ttl pruning
  - heartbeat keep-warm cache
  - system-prompt cache boundary
  - cacheRead cacheWrite normalization
  - per-provider cache behavior anthropic openai bedrock
  - cacheTrace diagnostics env toggles
  - cache regression live tests
topics:
  - OpenClaw
  - Prompt Caching
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/prompt-caching
access_control_group: ["general"]
---

# OpenClaw — Tuning Prompt Caching

## Overview

This note is the procedure reference for tuning OpenClaw **prompt caching** — the provider-side reuse of unchanged prompt prefixes (system/developer instructions and other stable context) across turns instead of re-processing them every time, which OpenClaw normalizes into `cacheRead` / `cacheWrite` counters where the upstream API exposes them. It mirrors the `reference/prompt-caching` source page end to end: the primary knobs (`cacheRetention`, `contextPruning.mode: "cache-ttl"`, heartbeat keep-warm), per-provider cache behavior (Anthropic, OpenAI, Anthropic Vertex, Amazon Bedrock, OpenRouter, other, Google Gemini, Gemini CLI), the system-prompt cache boundary, cache-stability guards, the mixed-traffic and cost-first tuning patterns, cache diagnostics, the live regression tests, and quick troubleshooting. The rationale is lower token cost, faster responses, and more predictable long-running sessions; without caching, repeated prompts pay the full cost every turn even when most input did not change.

## Primary knobs

### `cacheRetention` (global default, model, and per-agent)

`cacheRetention` accepts `none | short | long` at three scopes: the global default under `agents.defaults.params`, a per-model override under `agents.defaults.models["provider/model"].params`, and a per-agent override under a matching `agents.list[].params` entry. The config merge order is: (1) `agents.defaults.params` (global default — applies to all models), (2) `agents.defaults.models["provider/model"].params` (per-model override), (3) `agents.list[].params` (matching agent id; overrides by key). The canonical global block is:

```yaml
agents:
  defaults:
    params:
      cacheRetention: "long" # none | short | long
```

The per-model override is keyed by the exact `provider/model` ref (e.g. `agents.defaults.models["anthropic/claude-opus-4-6"].params.cacheRetention: "short"`); a per-agent override targets one agent by id (e.g. `cacheRetention: "none"` on an `alerts` agent).

### `contextPruning.mode: "cache-ttl"`

This mode prunes old tool-result context after cache TTL windows so post-idle requests do not re-cache oversized history. Configure it under `agents.defaults.contextPruning` with a `ttl` such as `"1h"`:

```yaml
agents:
  defaults:
    contextPruning:
      mode: "cache-ttl"
      ttl: "1h"
```

Full behavior is documented in the Session Pruning concept page (linked under References).

### Heartbeat keep-warm

Heartbeat can keep cache windows warm and reduce repeated cache writes after idle gaps; set it under `agents.defaults.heartbeat.every` (such as `"55m"`). Per-agent heartbeat is supported at `agents.list[].heartbeat`.

## Provider behavior

Cache behavior differs per provider.

- **Anthropic (direct API).** `cacheRetention` is supported. With Anthropic API-key auth profiles, OpenClaw seeds `cacheRetention: "short"` for Anthropic model refs when unset. Anthropic native Messages responses expose both `cache_read_input_tokens` and `cache_creation_input_tokens`, so OpenClaw shows both `cacheRead` and `cacheWrite`. For native Anthropic requests, `cacheRetention: "short"` maps to the default 5-minute ephemeral cache, and `cacheRetention: "long"` upgrades to the 1-hour TTL only on direct `api.anthropic.com` hosts.
- **OpenAI (direct API).** Prompt caching is automatic on supported recent models, so OpenClaw does not inject block-level cache markers. OpenClaw uses `prompt_cache_key` to keep cache routing stable across turns; direct OpenAI hosts use `prompt_cache_retention: "24h"` when `cacheRetention: "long"` is selected. OpenAI-compatible Completions providers receive `prompt_cache_key` only when their model config sets `compat.supportsPromptCacheKey: true`; long-retention forwarding is separate, so `cacheRetention: "long"` sends `prompt_cache_retention: "24h"` only when that compat entry also supports long retention (a provider such as Mistral can set `compat.supportsLongCacheRetention: false` to suppress the long-retention field). `cacheRetention: "none"` suppresses both fields. OpenAI exposes cached prompt tokens via `usage.prompt_tokens_details.cached_tokens` (or `input_tokens_details.cached_tokens` on Responses API events), which OpenClaw maps to `cacheRead`; OpenAI exposes no separate cache-write counter, so `cacheWrite` stays `0` even while warming a cache. OpenAI returns useful tracing/rate-limit headers (`x-request-id`, `openai-processing-ms`, `x-ratelimit-*`), but cache-hit accounting should come from the usage payload, not headers. In practice OpenAI behaves like an initial-prefix cache rather than Anthropic-style moving full-history reuse: stable long-prefix turns can land near a `4864` cached-token plateau in current live probes, while tool-heavy or MCP-style transcripts often plateau near `4608` cached tokens even on exact repeats.
- **Anthropic Vertex.** Anthropic models on Vertex AI (`anthropic-vertex/*`) support `cacheRetention` the same way as direct Anthropic; `cacheRetention: "long"` maps to the real 1-hour prompt-cache TTL on Vertex AI endpoints; default retention matches direct Anthropic; Vertex requests are routed through boundary-aware cache shaping so reuse stays aligned with what providers actually receive.
- **Amazon Bedrock.** Anthropic Claude model refs (`amazon-bedrock/*anthropic.claude*`) support explicit `cacheRetention` pass-through; non-Anthropic Bedrock models are forced to `cacheRetention: "none"` at runtime.
- **OpenRouter models.** For `openrouter/anthropic/*` model refs, OpenClaw injects Anthropic `cache_control` on system/developer prompt blocks only when the request still targets a verified OpenRouter route (`openrouter` on its default endpoint, or any provider/base URL that resolves to `openrouter.ai`). For `openrouter/deepseek/*`, `openrouter/moonshot*/*`, and `openrouter/zai/*` refs, `contextPruning.mode: "cache-ttl"` is allowed because OpenRouter handles provider-side caching automatically and OpenClaw does not inject `cache_control` markers there. DeepSeek cache construction is best-effort and can take a few seconds — an immediate follow-up may still show `cached_tokens: 0`, so verify with a repeated same-prefix request after a short delay and use `usage.prompt_tokens_details.cached_tokens` as the cache-hit signal. If you repoint the model at an arbitrary OpenAI-compatible proxy URL, OpenClaw stops injecting those OpenRouter-specific Anthropic cache markers.
- **Other providers.** If the provider does not support this cache mode, `cacheRetention` has no effect.
- **Google Gemini direct API.** Direct Gemini transport (`api: "google-generative-ai"`) reports cache hits through upstream `cachedContentTokenCount`, which OpenClaw maps to `cacheRead`. When `cacheRetention` is set on a direct Gemini model, OpenClaw automatically creates, reuses, and refreshes `cachedContents` resources for system prompts on Google AI Studio runs (no manual pre-creation needed); you can still pass a pre-existing handle as `params.cachedContent` (or legacy `params.cached_content`). This is separate from prompt-prefix caching — OpenClaw manages a provider-native `cachedContents` resource rather than injecting cache markers.
- **Gemini CLI usage.** Gemini CLI `stream-json` output can surface cache hits through `stats.cached`, which OpenClaw maps to `cacheRead` (legacy `--output-format json` overrides use the same normalization). If the CLI omits a direct `stats.input` value, OpenClaw derives input tokens from `stats.input_tokens - stats.cached`. This is usage normalization only, not Anthropic/OpenAI-style prompt-cache markers.

## System-prompt cache boundary

OpenClaw splits the system prompt into a **stable prefix** and a **volatile suffix** separated by an internal cache-prefix boundary. Content above the boundary (tool definitions, skills metadata, workspace files, and other relatively static context) is ordered so it stays byte-identical across turns, while content below the boundary (for example `HEARTBEAT.md`, runtime timestamps, and other per-turn metadata) may change without invalidating the cached prefix. Key design choices: stable workspace project-context files are ordered before `HEARTBEAT.md` so heartbeat churn does not bust the prefix; the boundary is applied across Anthropic-family, OpenAI-family, Google, and CLI transport shaping (and Codex Responses + Anthropic Vertex requests are routed through this boundary-aware shaping) so all providers get the same prefix stability aligned with what they actually receive; and system-prompt fingerprints are normalized (whitespace, line endings, hook-added context, runtime capability ordering) so semantically unchanged prompts share KV/cache across turns. If you see unexpected `cacheWrite` spikes after a config or workspace change, check whether the change lands above or below the cache boundary — moving volatile content below it (or stabilizing it) often resolves the issue.

## OpenClaw cache-stability guards

OpenClaw keeps several cache-sensitive payload shapes deterministic before the request reaches the provider. Bundle MCP tool catalogs are sorted deterministically before tool registration, so `listTools()` order changes do not churn the tools block and bust prompt-cache prefixes. Legacy sessions with persisted image blocks keep the **3 most recent completed turns** intact; older already-processed image blocks may be replaced with a marker so image-heavy follow-ups do not re-send large stale payloads.

## Tuning patterns

### Mixed traffic (recommended default)

Keep a long-lived baseline on the main agent and disable caching on bursty notifiers — set the primary model's `cacheRetention: "long"`, give the default `research` agent a `55m` heartbeat, and force `cacheRetention: "none"` on `alerts`:

```yaml
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-6"
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "long"
  list:
    - id: "research"
      default: true
      heartbeat:
        every: "55m"
    - id: "alerts"
      params:
        cacheRetention: "none"
```

### Cost-first baseline

Set baseline `cacheRetention: "short"`, enable `contextPruning.mode: "cache-ttl"`, and keep heartbeat below your TTL only for agents that benefit from warm caches.

## Cache diagnostics

OpenClaw exposes dedicated cache-trace diagnostics for embedded agent runs. For normal user-facing diagnostics, `/status` and other usage summaries can fall back to the latest transcript usage entry for `cacheRead` / `cacheWrite` when the live session entry lacks those counters (existing nonzero live values still take precedence over transcript fallback values).

### `diagnostics.cacheTrace` config

Configure persistent cache tracing under `diagnostics.cacheTrace`:

```yaml
diagnostics:
  cacheTrace:
    enabled: true
    filePath: "~/.openclaw/logs/cache-trace.jsonl" # optional
    includeMessages: false # default true
    includePrompt: false # default true
    includeSystem: false # default true
```

Documented defaults: `filePath` → `$OPENCLAW_STATE_DIR/logs/cache-trace.jsonl`; `includeMessages`, `includePrompt`, and `includeSystem` all default to `true`.

### Env toggles (one-off debugging)

For one-off debugging the same trace is driven by env vars: `OPENCLAW_CACHE_TRACE=1` enables tracing; `OPENCLAW_CACHE_TRACE_FILE=/path/to/cache-trace.jsonl` overrides the output path; and `OPENCLAW_CACHE_TRACE_MESSAGES=0|1`, `OPENCLAW_CACHE_TRACE_PROMPT=0|1`, and `OPENCLAW_CACHE_TRACE_SYSTEM=0|1` toggle message-payload, prompt-text, and system-prompt capture respectively.

### What to inspect

Cache trace events are JSONL and include staged snapshots like `session:loaded`, `prompt:before`, `stream:context`, and `session:after`. Per-turn cache token impact is visible in normal usage surfaces via `cacheRead` and `cacheWrite` (e.g. `/usage full` and session usage summaries). For Anthropic, expect both `cacheRead` and `cacheWrite` when caching is active; for OpenAI, expect `cacheRead` on hits and `cacheWrite` to stay `0` (no separate cache-write field). If you need request tracing, log request IDs and rate-limit headers separately — the cache-trace output focuses on prompt/session shape and normalized token usage, not raw provider response headers.

## Live regression tests

OpenClaw keeps one combined live cache regression gate for repeated prefixes, tool turns, image turns, MCP-style transcripts, and an Anthropic no-cache control. The test files are `src/agents/live-cache-regression.live.test.ts` and `src/agents/live-cache-regression-baseline.ts`. Run the narrow gate with:

```sh
OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_CACHE_TEST=1 pnpm test:live:cache
```

The baseline file stores the most recent observed live numbers plus the provider-specific regression floors used by the test; the runner uses fresh per-run session IDs and prompt namespaces so previous cache state does not pollute the current sample. These tests intentionally do not use identical success criteria across providers.

### Anthropic live expectations

Expect explicit warmup writes via `cacheWrite`, near-full history reuse on repeated turns (Anthropic cache control advances the cache breakpoint through the conversation), and current live assertions still using high hit-rate thresholds for the stable, tool, and image paths.

### OpenAI live expectations

Expect `cacheRead` only — `cacheWrite` remains `0` — and treat repeated-turn reuse as a provider-specific plateau, not Anthropic-style moving full-history reuse. Current live assertions use conservative floor checks derived from observed live behavior on `gpt-5.4-mini`: stable prefix `cacheRead >= 4608` (hit rate `>= 0.90`); tool transcript `cacheRead >= 4096` (`>= 0.85`); image transcript `cacheRead >= 3840` (`>= 0.82`); MCP-style transcript `cacheRead >= 4096` (`>= 0.85`). Fresh combined live verification on 2026-04-04 landed at: stable prefix `cacheRead=4864` (`0.966`); tool `cacheRead=4608` (`0.896`); image `cacheRead=4864` (`0.954`); MCP-style `cacheRead=4608` (`0.891`); recent local wall-clock for the combined gate was about `88s`. The assertions differ because Anthropic exposes explicit cache breakpoints and moving conversation-history reuse while OpenAI is still exact-prefix sensitive (its effective reusable prefix can plateau earlier than the full prompt), so a single cross-provider percentage threshold would create false regressions.

## Quick troubleshooting

- High `cacheWrite` on most turns: check for volatile system-prompt inputs and verify the model/provider supports your cache settings.
- High `cacheWrite` on Anthropic: often the cache breakpoint is landing on content that changes every request.
- Low OpenAI `cacheRead`: verify the stable prefix is at the front, the repeated prefix is at least 1024 tokens, and the same `prompt_cache_key` is reused for turns that should share a cache.
- No effect from `cacheRetention`: confirm the model key matches `agents.defaults.models["provider/model"]`.
- Bedrock Nova/Mistral requests with cache settings: expected runtime force to `none`.

**Source**: OpenClaw documentation — `reference/prompt-caching` (mirror `inbox/openclaw_docs/reference/prompt-caching.md`)
**Last Updated**: 2026-06-22
**Status**: Active
