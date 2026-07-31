---
tags:
  - resource
  - documentation
  - hermes_agent
  - provider_resilience
  - llm_infrastructure
keywords:
  - hermes fallback providers
  - primary model fallback
  - auxiliary task fallback
  - capacity-error fallback ladder
  - cross-provider failover
  - context compression fallback
topics:
  - Hermes Agent
  - Provider Resilience
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers
access_control_group: ["general"]
---

# Hermes Agent — Fallback Providers

## Overview

Fallback Providers is the **cross-provider resilience model** in Hermes Agent: when a model request fails, Hermes switches to a *different* provider:model pair instead of erroring out. It is the second of three resilience layers — [credential pools](hermes_credential_pools.md) rotate keys for the *same* provider first, primary model fallback switches to a different provider:model mid-session, and auxiliary task fallback gives side tasks (vision, compression, web extraction) their own independent provider chains. This note is the data model of that failover stack: which errors trigger each layer, the supported-provider matrix, the per-task chains, the capacity-error fallback ladder, compression degrade-to-no-summary, and delegation/cron chain inheritance.

## Three Layers of Resilience

Hermes Agent has three layers that keep sessions running when providers hit issues:

1. **Credential pools** — rotate across multiple API keys for the *same* provider (tried first).
2. **Primary model fallback** — automatically switches to a *different* provider:model when the main model fails.
3. **Auxiliary task fallback** — independent provider resolution for side tasks like vision, compression, and web extraction.

Credential pools handle same-provider rotation (e.g., multiple OpenRouter keys); this page covers cross-provider fallback. Both are optional and independent.

## Primary Model Fallback

When the main LLM provider hits errors — rate limits, server overload, auth failures, connection drops — Hermes can automatically switch to a backup provider:model pair mid-session **without losing the conversation**.

### Configuration

The easiest path is the interactive manager `hermes fallback`, which reuses the provider picker from `hermes model` (same provider list, credential prompts, validation). Subcommands `add`, `list` (alias `ls`), `remove` (alias `rm`), and `clear` manage the chain; changes persist under the top-level `fallback_providers:` list in `config.yaml`. To edit YAML directly, add that list to `~/.hermes/config.yaml`:

```yaml
fallback_providers:
  - provider: openrouter
    model: anthropic/claude-sonnet-4
```

Each entry requires both `provider` and `model`; entries missing either are ignored. `fallback_providers` (plural, list) is the current shape and supports multiple fallbacks tried in order. `fallback_model` (singular) is the legacy single-fallback key — still honored for back-compat, but `hermes fallback` writes `fallback_providers` and migrates legacy config on write; when both are set, `fallback_providers` takes priority. (The `fallback_providers:` / `auxiliary.*` config-key catalog is owned by SP02 — see [hermes_config_files_precedence](hermes_config_files_precedence.md).)

### Supported Providers

A `fallback_providers` entry can target any of ~40 supported providers; each source-matrix row gives a `provider` value plus its credential requirement. The full per-provider catalog and auth details are owned by SP14/SP15 (see [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md)) and are link-routed, not re-mirrored. Representative values: `openrouter`, `nous` (Nous Portal), `openai-codex`, `copilot`/`copilot-acp`, `anthropic`, `zai` (GLM), `kimi-coding`, `minimax`/`minimax-cn`/`minimax-oauth`, `deepseek`, `nvidia`, `gmi`, `stepfun`, `ollama-cloud`, `google-gemini-cli`/`gemini`, `xai` (alias `grok`)/`xai-oauth`, `bedrock`, `qwen-oauth`, `opencode-zen`/`opencode-go`, `kilocode`, `xiaomi`, `arcee`, `alibaba`/`alibaba-coding-plan`, `kimi-coding-cn`, `tencent-tokenhub`, `azure-foundry`, `lmstudio` (local), `huggingface`, and `custom` (`base_url` + `key_env`). Each entry requires both `provider` and `model`.

### Custom Endpoint Fallback

For a custom OpenAI-compatible endpoint, add `base_url` and optionally `key_env`:

```yaml
fallback_providers:
  - provider: custom
    model: my-local-model
    base_url: http://localhost:8000/v1
    key_env: MY_LOCAL_KEY            # env var name containing the API key
```

### When Fallback Triggers

The fallback activates automatically when the primary model fails with:

- **Rate limits** (HTTP 429) — after exhausting retry attempts.
- **Server errors** (HTTP 500, 502, 503) — after exhausting retry attempts.
- **Auth failures** (HTTP 401, 403) — immediately (no point retrying).
- **Not found** (HTTP 404) — immediately.
- **Invalid responses** — when the API returns malformed or empty responses repeatedly.

When triggered, Hermes (1) resolves credentials for the fallback provider, (2) builds a new API client, (3) swaps the model, provider, and client in-place, and (4) resets the retry counter and continues. The switch is seamless — conversation history, tool calls, and context are preserved; the agent continues from exactly where it left off, just using a different model.

**Per-turn, not per-session:** Fallback is turn-scoped. Each new user message starts with the primary model restored. If the primary fails mid-turn, fallback activates for that turn only. On the next message, Hermes tries the primary again. Within a single turn, fallback activates **at most once** — if the fallback also fails, normal error handling takes over (retries, then error message). This prevents cascading failover loops within a turn while giving the primary a fresh chance every turn.

### Examples and Where It Works

The page shows several config shapes (all the `fallback_providers:` list shape above): OpenRouter as fallback for Anthropic native, Nous Portal as fallback for OpenRouter, a local model as fallback for cloud (`provider: custom` + `base_url` + `key_env`), and Codex OAuth as fallback. Fallback is supported across CLI sessions, the messaging gateway (Telegram, Discord, etc.), subagent delegation (subagents inherit the parent chain), cron jobs (cron agents inherit configured fallback providers), and auxiliary tasks on `provider: auto` (try per-task fallback, then the main chain, before built-in aux discovery).

There are **no environment variables** for the primary fallback chain — configure it exclusively through `config.yaml` or `hermes fallback`. This is intentional: fallback configuration is a deliberate choice, not something a stale shell export should override.

## Auxiliary Task Fallback

Hermes uses separate lightweight models for side tasks. Each task has its own provider-resolution chain that acts as a built-in fallback.

### Tasks with Independent Provider Resolution

| Task | What It Does | Config Key |
|------|-------------|-----------|
| Vision | Image analysis, browser screenshots | `auxiliary.vision` |
| Web Extract | Web page summarization | `auxiliary.web_extract` |
| Compression | Context compression summaries | `auxiliary.compression` |
| Skills Hub | Skill search and discovery | `auxiliary.skills_hub` |
| MCP | MCP helper operations | `auxiliary.mcp` |
| Approval | Smart command-approval classification | `auxiliary.approval` |
| Title Generation | Session title summaries | `auxiliary.title_generation` |
| Triage Specifier | `hermes kanban specify` / dashboard button — fleshes a one-liner triage task into a real spec | `auxiliary.triage_specifier` |

### Auto-Detection Chain

When a task's provider is set to `"auto"` (the default), Hermes first tries the main provider + main model for that auxiliary task. If that route is unavailable or later fails with a capacity-style error, Hermes honors user-configured fallback policy before using the built-in discovery chain:

```text
Main provider + main model → auxiliary.<task>.fallback_chain →
fallback_providers / fallback_model → built-in auxiliary discovery chain
```

The task-specific chain is most precise and wins when present; the top-level `fallback_providers` chain is the same policy the main agent uses, so its rules apply to `auto` aux tasks too. The **built-in text discovery chain** (compression, web extract, title generation, etc.) is `OpenRouter → Nous Portal → Custom endpoint → Codex OAuth → API-key providers (z.ai, Kimi, MiniMax, Xiaomi MiMo, Hugging Face, Anthropic) → give up`. The **built-in vision discovery chain** is `Main provider (if vision-capable) → OpenRouter → Nous Portal → Codex OAuth → Anthropic → Custom endpoint → give up`. These built-in chains are a convenience fallback for users with no task-specific or main fallback policy declared.

### Configuring Auxiliary Providers

Each task is configured independently in `config.yaml`, following the same `provider` / `model` / `base_url` pattern; each can also declare its own `fallback_chain` (if omitted, `provider: auto` uses the top-level `fallback_providers` chain before the built-in discovery chain):

```yaml
auxiliary:
  vision:
    provider: "auto"              # auto | openrouter | nous | codex | main | anthropic
    model: ""                     # e.g. "openai/gpt-4o"
    base_url: ""                  # direct endpoint (takes precedence over provider)
    api_key: ""                   # API key for base_url
  compression:
    provider: "auto"
    model: ""
    fallback_chain:              # optional, task-specific fallback policy
      - provider: openrouter
        model: inclusionai/ring-2.6-1t:free
```

### Provider Options and Direct Endpoint Override

The `provider` values valid for `auxiliary:`, `compression:`, and `fallback_providers:` entries: `"auto"` (try providers in order until one works — default), `"openrouter"`, `"nous"`, `"codex"` (Codex OAuth), `"main"` (whatever the main agent uses — aux tasks only), `"anthropic"`. `"main"` is **not** valid for the top-level `model.provider`. For any aux task, setting `base_url` bypasses provider resolution and sends requests directly to that endpoint (precedence over `provider`); Hermes uses the configured `api_key`, falling back to `OPENAI_API_KEY` if unset — it does **not** reuse `OPENROUTER_API_KEY` for custom endpoints.

## Auxiliary Capacity-Error Fallback

When an explicit auxiliary provider is set (e.g. `auxiliary.vision.provider: glm`), Hermes treats that as the preferred choice — but if the provider literally cannot serve the request because of a **capacity error** (HTTP 402 payment required, HTTP 429 daily-quota exhaustion, connection failure), Hermes falls back through a layered ladder instead of failing silently:

1. **Primary aux provider** — the configured one (tried first, always).
2. **`auxiliary.<task>.fallback_chain`** — the per-task override list, if written.
3. **Main agent provider + model** — last-resort safety net (always tried, even with no chain).
4. **Warn + re-raise** — if every layer fails, Hermes logs `Auxiliary <task>: ... all fallbacks exhausted` at WARNING and re-raises the original error.

Transient HTTP 429 rate limits (`Retry-After: ...`) are treated as request constraints, not capacity problems — they respect the explicit provider choice and do **not** trigger the ladder. Only daily/monthly quota exhaustion, payment errors, and connection failures bypass the explicit-provider gate. For `provider: auto` users, the existing auto-detection chain runs in place of steps 2–3; its first step is already the main agent model, so `auto` users get the same outcome with zero config. A per-task `fallback_chain` is optional (the main-agent safety net runs regardless) — use it only to set a non-default order; each entry needs at least `provider`, with `model`/`base_url`/`api_key` optional.

**Provider quota errors that trigger fallback** — Hermes recognizes these as capacity-equivalent to 402 credit exhaustion (not transient rate limits): Bedrock / LiteLLM (`Too many tokens per day`, `daily limit`, `tokens per day`); Vertex AI / GCP (`quota exceeded`, `resource exhausted`, `RESOURCE_EXHAUSTED`); Generic (`daily quota`, `quota_exceeded`). If a provider returns a different daily-quota phrase and Hermes doesn't trigger fallback, that is a bug — open an issue with the exact error string.

## Context Compression Fallback

Context compression uses the `auxiliary.compression` config block to control which model/provider handles summarization (`provider`: `auto | openrouter | nous | main`; `model`: e.g. `google/gemini-3-flash-preview`). Older configs with `compression.summary_model` / `summary_provider` / `summary_base_url` are automatically migrated to `auxiliary.compression.*` on first load (config version 17). If no provider is available, Hermes **drops middle conversation turns without generating a summary** rather than failing the session.

## Delegation & Cron Provider Inheritance

Subagents spawned by `delegate_task` inherit the parent agent's primary fallback chain; they can still be routed to a different primary provider:model via a `delegation:` block (`provider` / `model` / optional `base_url` / `api_key`). Delegation itself is provider-override only — no automatic fallback (SP06 owns delegation — see [hermes_cron_scheduled_tasks](hermes_cron_scheduling.md)). Cron jobs inherit the configured `fallback_providers` chain (or legacy `fallback_model`) when creating an agent; to use a different primary provider, pass `provider`/`model` overrides on the cron job itself:

```python
cronjob(
    action="create",
    schedule="every 2h",
    prompt="Check server status",
    provider="openrouter",
    model="google/gemini-3-flash-preview"
)
```

## Summary

| Feature | Fallback Mechanism | Config Location |
|---------|-------------------|----------------|
| Main agent model | Per-turn failover on errors (primary restored each turn) | `fallback_providers:` (top-level list) |
| Aux tasks — auto users | Full auto-detection chain (main model first, then provider chain) on capacity errors | `auxiliary.<task>.provider: auto` |
| Aux tasks — explicit provider | `fallback_chain` (if set) → main model → warn + raise, on capacity errors only | `auxiliary.<task>.fallback_chain` |
| Vision / Web extraction | Layered + internal OpenRouter retry | `auxiliary.vision` / `.web_extract` |
| Context compression | Layered; degrades to no-summary if all layers unavailable | `auxiliary.compression` |
| Skills hub / MCP / Approval / Title / Triage | Layered (see above) | `auxiliary.<task>` |
| Delegation / Cron jobs | Provider override only (no automatic fallback) | `delegation.*` / per-job `provider`+`model` |

**Source**: `inbox/hermes_agent_docs/user-guide/features/fallback-providers.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers
**Last Updated**: 2026-06-19
**Status**: Active
