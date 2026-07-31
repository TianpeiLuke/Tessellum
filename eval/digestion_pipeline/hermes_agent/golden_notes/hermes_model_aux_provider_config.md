---
tags:
  - resource
  - documentation
  - hermes_agent
  - configuration
  - model_providers
keywords:
  - auxiliary models config
  - provider timeouts
  - credential pool strategies
  - prompt caching
  - reasoning effort
  - tool-use enforcement
topics:
  - Hermes Agent
  - Model & Provider Configuration
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/configuration
access_control_group: ["general"]
---

# Hermes Agent — Model, Auxiliary & Provider Configuration

## Overview

This is the model-and-provider tuning surface of `~/.hermes/config.yaml`: how Hermes Agent times out provider calls, rotates a pool of credentials, caches prompts, routes its 11 **auxiliary** model slots, sets reasoning effort, and enforces tool use. The defining concept is the **universal config pattern** — every model slot (auxiliary tasks, compression, fallback) takes the same three knobs `provider` / `model` / `base_url` — so once you learn one slot you can configure them all. These settings are largely opt-in: leaving them unset keeps sensible legacy defaults, and `auxiliary.*.provider: "auto"` simply reuses your main chat model. This note documents the config blocks; the *concepts* each block configures (credential pools, fallback/provider routing, the provider catalog, OAuth provider guides) are owned by other docs and linked, not duplicated.

## Provider Timeouts

Set `providers.<id>.request_timeout_seconds` for a provider-wide request timeout, plus `providers.<id>.models.<model>.timeout_seconds` for a model-specific override. It applies to the primary turn client on every transport (OpenAI-wire, native Anthropic, Anthropic-compatible), the fallback chain, rebuilds after credential rotation, and (for OpenAI-wire) the per-request timeout kwarg — so the configured value wins over the legacy `HERMES_API_TIMEOUT` env var.

Set `providers.<id>.stale_timeout_seconds` for the non-streaming stale-call detector, plus `providers.<id>.models.<model>.stale_timeout_seconds` for a model-specific override. This wins over the legacy `HERMES_API_CALL_STALE_TIMEOUT` env var.

Leaving these unset keeps the legacy defaults (`HERMES_API_TIMEOUT=1800`s, `HERMES_API_CALL_STALE_TIMEOUT=300`s, native Anthropic 900s). Not currently wired for AWS Bedrock (both `bedrock_converse` and AnthropicBedrock SDK paths use boto3 with its own timeout configuration).

## Credential Pool Strategies

When you have multiple API keys or OAuth tokens for the same provider, configure the rotation strategy:

```yaml
credential_pool_strategies:
  openrouter: round_robin    # cycle through keys evenly
  anthropic: least_used      # always pick the least-used key
```

Options: `fill_first` (default), `round_robin`, `least_used`, `random`. The credential-pool concept itself (seeding from multiple keys, full rotation semantics) is documented under Credential Pools (link-out, SP09).

## Prompt caching

Hermes turns on cross-session prompt caching automatically when the active provider supports it — no user config needed. For Claude on **native Anthropic**, **OpenRouter**, and **Nous Portal**, Hermes attaches `cache_control` breakpoints with the 1-hour TTL (`ttl: "1h"`) on the system prompt and skill blocks. The first send within a fresh hour pays full input rates; subsequent sends across any session within the same hour pull from the cache at the discounted cached-read rate. The system prompt, loaded skill content, and the early portion of any long-context include get reused across `hermes` sessions and across forked subagents for the first hour.

The Qwen Cloud (Alibaba DashScope) upstream caps cache TTL at 5 minutes, so Hermes uses the 5-minute breakpoint TTL there instead. Other Claude-via-third-party paths (AWS Bedrock, Azure Foundry) fall back to the provider's own caching defaults. xAI Grok uses a separate session-pinned conversation-id mechanism. **No knob exists to disable this** — caching is always-on and saves money even on single-turn conversations because the system prompt alone is a meaningful fraction of the input token count.

## Auxiliary Models

Hermes uses "auxiliary" models for side tasks like image analysis, web-page summarization, browser screenshot analysis, session-title generation, and context compression. By default (`auxiliary.*.provider: "auto"`), Hermes routes every auxiliary task to your **main chat model** — the same provider/model you picked in `hermes model`. You don't need to configure anything to get started, but on expensive reasoning models (Opus, MiniMax M2.7, etc.) auxiliary tasks add meaningful cost. For cheap-and-fast side tasks regardless of your main model, set `auxiliary.<task>.provider` and `auxiliary.<task>.model` explicitly (for example, Gemini Flash on OpenRouter for vision and web extraction). `auto` now uses the main model for everyone, and per-task overrides in `config.yaml` still win.

### Configuring auxiliary models interactively

Instead of hand-editing YAML, run `hermes model` and pick **"Configure auxiliary models"** from the menu for an interactive per-task picker:

```
$ hermes model
→ Configure auxiliary models

[ ] vision               currently: auto / main model
[ ] web_extract          currently: auto / main model
[ ] title_generation     currently: openrouter / google/gemini-3-flash-preview
[ ] tts_audio_tags       currently: auto / main model
[ ] compression          currently: auto / main model
[ ] approval             currently: auto / main model
[ ] triage_specifier     currently: auto / main model
[ ] kanban_decomposer    currently: auto / main model
[ ] profile_describer    currently: auto / main model
```

Select a task, pick a provider (OAuth flows open a browser; API-key providers prompt), pick a model. The change persists to `auxiliary.<task>.*` in `config.yaml` — the same machinery as the main-model picker, no extra syntax to learn.

### The universal config pattern

Every model slot in Hermes — auxiliary tasks, compression, fallback — uses the same three knobs:

| Key | What it does | Default |
|-----|-------------|---------|
| `provider` | Which provider to use for auth and routing | `"auto"` |
| `model` | Which model to request | provider's default |
| `base_url` | Custom OpenAI-compatible endpoint (overrides provider) | not set |

When `base_url` is set, Hermes ignores the provider and calls that endpoint directly (using `api_key` or `OPENAI_API_KEY` for auth). When only `provider` is set, Hermes uses that provider's built-in auth and base URL.

Available providers for auxiliary tasks: `auto`, `main`, plus any provider in the provider registry — `openrouter`, `nous`, `openai-codex`, `copilot`, `anthropic`, `gemini`, `qwen-oauth`, `zai`, `minimax`, `minimax-oauth`, `deepseek`, `nvidia`, `xai`, `xai-oauth`, `bedrock`, `azure-foundry`, and others — or any named custom provider from your `custom_providers` list (e.g. `provider: "beans"`). The full main-model provider catalog is owned by AI Providers (link-out, SP14); the MiniMax/xAI OAuth flows have dedicated guides (link-out, SP15).

> **`"main"` is for auxiliary tasks only.** The `"main"` provider option means "use whatever provider my main agent uses" — it's only valid inside `auxiliary:`, `compression:`, and primary fallback entries (`fallback_providers:` or legacy `fallback_model:`). It is **not** a valid value for your top-level `model.provider` setting; use `provider: custom` there.

### Full auxiliary config reference

```yaml
auxiliary:
  # Image analysis (vision_analyze tool + browser screenshots)
  vision:
    provider: "auto"           # "auto", "openrouter", "nous", "codex", "main", etc.
    model: ""                  # e.g. "openai/gpt-4o", "google/gemini-2.5-flash"
    base_url: ""               # Custom OpenAI-compatible endpoint (overrides provider)
    api_key: ""                # API key for base_url (falls back to OPENAI_API_KEY)
    timeout: 120               # seconds — LLM API call timeout; vision payloads need generous timeout
    download_timeout: 30       # seconds — image HTTP download; increase for slow connections

  # Web page summarization + browser page text extraction
  web_extract:
    provider: "auto"
    model: ""                  # e.g. "google/gemini-2.5-flash"
    base_url: ""
    api_key: ""
    timeout: 360               # seconds (6min) — per-attempt LLM summarization

  # Dangerous command approval classifier
  approval:
    provider: "auto"
    model: ""
    timeout: 30                # seconds

  # Context compression timeout (separate from compression.* config)
  compression:
    timeout: 120               # seconds — compression summarizes long conversations, needs more time

  # Auto-generated session titles. Empty language follows the conversation.
  title_generation:
    provider: "auto"
    model: ""
    timeout: 30
    language: ""

  # MCP tool dispatch
  mcp:
    provider: "auto"
    model: ""
    timeout: 30
```

Each auxiliary task has a configurable `timeout` (in seconds). Defaults: vision 120s, web_extract 360s, approval 30s, compression 120s. Increase these if you use slow local models. Vision also has a separate `download_timeout` (default 30s) for the HTTP image download. The full reference adds `tts_audio_tags`, `skills_hub`, and `triage_specifier` slots — each following the same pattern. Context compression has its own `compression:` block for thresholds and an `auxiliary.compression:` block for model/provider settings (link-out: Context Compression); the primary fallback chain uses a top-level `fallback_providers:` list (link-out, SP09). All three follow the same provider/model/base_url pattern.

### OpenRouter routing & Pareto Code for auxiliary tasks

When an auxiliary task resolves to OpenRouter (explicitly or via `provider: "main"` while your main agent is on OpenRouter), the main agent's `provider_routing` and `openrouter.min_coding_score` settings **do not propagate** — by design, each auxiliary task is independent. To set OpenRouter provider preferences or use the Pareto Code router for a specific aux task, set them per-task via `extra_body`:

```yaml
auxiliary:
  compression:
    provider: openrouter
    model: openrouter/pareto-code         # use the Pareto Code router for this task
    extra_body:
      provider:                            # OpenRouter provider routing prefs
        order: [anthropic, google]         # try these providers in order
        sort: throughput                   # or "price" | "latency"
      plugins:                             # OpenRouter Pareto Code router knob
        - id: pareto-router
          min_coding_score: 0.5            # 0.0–1.0; higher = stronger coders
```

The shape mirrors what OpenRouter accepts in the chat completions request body — Hermes forwards the entire `extra_body` verbatim, so any other OpenRouter request-body field works the same way.

### Provider options, common setups & legacy env

The `provider` value selects the auxiliary route: `"auto"` (best available; Vision tries OpenRouter → Nous → Codex), `"openrouter"` (requires `OPENROUTER_API_KEY`), `"nous"` (requires `hermes auth`), `"codex"` (ChatGPT OAuth, supports vision via gpt-5.3-codex), `"minimax-oauth"`/`"xai-oauth"` (browser OAuth, no API key), and `"main"` (your active custom/main endpoint — auxiliary tasks only). Direct API-key providers from the main catalog also work (e.g. `gmi` once `GMI_API_KEY` is set; use the exact model ID from its `/v1/models`).

The most explicit way to route a task is a direct endpoint, since `base_url` takes precedence over `provider` — e.g. setting `auxiliary.vision.base_url: "http://localhost:1234/v1"` with `api_key: "local-key"` and `model: "qwen2.5-vl"` calls that endpoint directly regardless of provider. To change just the vision model: `auxiliary.vision.model: "openai/gpt-4o"` (or env var `AUXILIARY_VISION_MODEL=openai/gpt-4o`). **Vision requires a multimodal model** — if you set `provider: "main"`, ensure your endpoint supports vision or image analysis will fail. Codex OAuth as your main provider gets vision automatically. Auxiliary vision/web-extract slots can also be set via legacy env vars (`AUXILIARY_VISION_PROVIDER`/`_MODEL`/`_BASE_URL`/`_API_KEY`, and the `AUXILIARY_WEB_EXTRACT_*` equivalents), but `config.yaml` is preferred — it's easier to manage and supports `base_url` and `api_key`. Compression and fallback model settings are config.yaml-only. Run `hermes config` to see current auxiliary settings (overrides show only when they differ from defaults).

## Reasoning Effort

Control how much "thinking" the model does before responding:

```yaml
agent:
  reasoning_effort: ""   # empty = medium (default). Options: none, minimal, low, medium, high, xhigh (max)
```

When unset (default), reasoning effort defaults to "medium" — a balanced level for most tasks. Setting a value overrides it: higher effort gives better results on complex tasks at the cost of more tokens and latency.

For adaptive-thinking models (Claude 4.6+, Fable/Mythos-class) over OpenRouter, those models don't accept the usual `reasoning.effort` field — OpenRouter ignores it. Hermes transparently routes your `reasoning_effort` to OpenRouter's `verbosity` parameter instead (which maps to Anthropic's `output_config.effort`), so the same `low`/`medium`/`high`/`xhigh` knob keeps working. `none` (or unset) leaves the model on its adaptive default. (`max` is accepted on the wire but is not a selectable value; `xhigh` is the configurable ceiling.) The native Anthropic provider already controls effort directly and is unaffected. At runtime, the `/reasoning` command shows or changes the level (`/reasoning high`, `/reasoning none`, `/reasoning show`, `/reasoning hide`).

## Tool-Use Enforcement

Some models occasionally describe intended actions as text instead of making tool calls ("I would run the tests..." instead of actually calling the terminal). Tool-use enforcement injects system-prompt guidance that steers the model back to actually calling tools.

```yaml
agent:
  tool_use_enforcement: "auto"   # "auto" | true | false | ["model-substring", ...]
```

| Value | Behavior |
|-------|----------|
| `"auto"` (default) | Enabled for models matching: `gpt`, `codex`, `gemini`, `gemma`, `grok`. Disabled for all others (Claude, DeepSeek, Qwen, etc.). |
| `true` | Always enabled, regardless of model. |
| `false` | Always disabled, regardless of model. |
| `["gpt", "codex", "qwen", "llama"]` | Enabled only when the model name contains one of the listed substrings (case-insensitive). |

When enabled, three layers of guidance may be added to the system prompt: (1) **general tool-use enforcement** for all matched models — make tool calls immediately, keep working until the task is complete, never end a turn with a promise of future action; (2) **OpenAI execution discipline** for GPT/Codex models only — addressing abandoning work on partial results, skipping prerequisite lookups, hallucinating instead of using tools, and declaring "done" without verification; (3) **Google operational guidance** for Gemini/Gemma models only — conciseness, absolute paths, parallel tool calls, verify-before-edit. These are transparent to the user and only affect the system prompt; models that already use tools reliably (Claude) are excluded by `"auto"`. If your model isn't in the auto list and frequently describes intentions, set `tool_use_enforcement: true` or add its substring to the list.

**Source**: `inbox/hermes_agent_docs/user-guide/configuration.md` · https://hermes-agent.nousresearch.com/docs/user-guide/configuration
**Last Updated**: 2026-06-19
**Status**: Active
