---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - models
keywords:
  - openclaw model selection
  - model aliases shortcuts
  - /model command switching
  - model failover all models failed
  - agents.defaults.model.fallbacks
  - auth profiles auth-profiles.json
  - openclaw models auth order
  - provider model collision
topics:
  - OpenClaw
  - Models FAQ
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/faq-models
access_control_group: ["general"]
---

# OpenClaw — Models FAQ (Selection, Aliases, Failover, Auth Profiles)

## Overview

This is the procedural Models FAQ for OpenClaw: setting defaults, selecting/switching models, defining aliases, adding provider models, understanding failover and "All models failed", and managing auth profiles. It mirrors all three content H2s of the `help/faq-models` source page, preserving the exact config keys, CLI commands, and error strings.

## Defaults, Selection, and Switching

OpenClaw's default model is whatever you set as `agents.defaults.model.primary`. Models are referenced as `provider/model` (example: `openai/gpt-5.5` or `anthropic/claude-sonnet-4-6`). If you omit the provider, OpenClaw first tries an alias, then a unique configured-provider match for that exact model id, and only then falls back to the configured default provider as a deprecated compatibility path; if that provider no longer exposes the configured default model, it falls back to the first configured provider/model instead of a stale removed-provider default. You should still **explicitly** set `provider/model`.

The recommended default is the strongest latest-generation model in your provider stack; tool-enabled or untrusted-input agents should prioritize strength over cost, and routine chat can use cheaper models routed by agent role. Weaker/over-quantized models are more vulnerable to prompt injection. You can route models per agent and use sub-agents to parallelize long tasks (each consumes tokens). OpenClaw, Flawd, and Krill deployments have no fixed provider recommendation — check each gateway with `openclaw models status`.

To switch models without wiping config, use model commands or edit only the model fields. Safe options: `/model` in chat (per-session); `openclaw models set ...` (model config only); `openclaw configure --section model` (interactive); or edit `agents.defaults.model` in `~/.openclaw/openclaw.json`. Avoid `config.apply` with a partial object unless you intend to replace the whole config; for RPC edits, inspect with `config.schema.lookup` first (it returns the normalized path, shallow schema docs/constraints, and immediate child summaries) and prefer `config.patch` for partial updates. If you overwrote config, restore from backup or re-run `openclaw doctor`.

### Switching on the fly with `/model`

Use `/model` as a standalone message. Built-in aliases: `/model sonnet`, `/model opus`, `/model gpt`, `/model gpt-mini`, `/model gemini`, `/model gemini-flash`, `/model gemini-flash-lite`. List models with `/model`, `/model list`, or `/model status`; `/model` and `/model list` show a compact numbered picker so you can select by number (e.g. `/model 3`). Force a specific auth profile per session with the `@profile` suffix, e.g. `/model opus@anthropic:default` or `/model opus@anthropic:work`. To unpin a profile set with `@profile`, re-run `/model` **without** the suffix (e.g. `/model anthropic/claude-opus-4-6`); to return to the default, pick it from `/model`. `/model status` shows the active agent, which `auth-profiles.json` is in use, which profile will be tried next, and (when available) the provider endpoint (`baseUrl`) and API mode (`api`).

### Same model id across two providers

`/model provider/model` selects that exact provider route for the session. For example, `qianfan/deepseek-v4-flash` and `deepseek/deepseek-v4-flash` are different model refs even though both contain `deepseek-v4-flash`, and OpenClaw should not silently switch between them just because the bare id matches. A user-selected `/model` ref is also strict for fallback: if that provider/model is unavailable, the reply fails visibly instead of answering from `agents.defaults.model.fallbacks`. Configured fallback chains still apply to configured defaults, cron job primaries, and auto-selected fallback state; a run from a non-session override that may use fallback tries the requested provider/model first, then configured fallbacks, then the configured primary (so duplicate bare ids do not jump straight back to the default provider).

### Self-hosted models and routing combos

For self-hosted models (llama.cpp, vLLM, Ollama), Ollama is the easiest path: install Ollama, pull a model such as `ollama pull gemma4`, optionally `ollama signin` for cloud models, then run `openclaw onboard`, choose `Ollama`, and pick `Local` or `Cloud + Local`. For manual switching use `openclaw models list` and `openclaw models set ollama/<model>`; cloud models such as `kimi-k2.5:cloud` need no local pull. To run GPT 5.5 for daily tasks and Codex 5.5 for coding, treat model and runtime choice separately — set `agents.defaults.model.primary` to `openai/gpt-5.5` for the native Codex agent and sign in with `openclaw models auth login --provider openai` for ChatGPT/Codex subscription auth; configure `OPENAI_API_KEY` for direct OpenAI API surfaces (images, embeddings, speech, realtime); use `/model openai/gpt-5.5` with an ordered `openai` API-key profile for agent API-key auth; or route coding to a Codex sub-agent. Fast mode for GPT 5.5 is set per session with `/fast on` (while using `openai/gpt-5.5`) or per model default via `agents.defaults.models["openai/gpt-5.5"].params.fastMode` set to `true` (for OpenAI it maps to `service_tier = "priority"` on supported native Responses requests; session `/fast` beats config defaults).

### Aliases, allowlists, and adding providers

OpenClaw ships built-in shorthands, applied **only** when the model exists in `agents.defaults.models`: `opus` → `anthropic/claude-opus-4-8`; `sonnet` → `anthropic/claude-sonnet-4-6`; `gpt` → `openai/gpt-5.4`; `gpt-mini` → `openai/gpt-5.4-mini`; `gpt-nano` → `openai/gpt-5.4-nano`; `gemini` → `google/gemini-3.1-pro-preview`; `gemini-flash` → `google/gemini-3-flash-preview`; `gemini-flash-lite` → `google/gemini-3.1-flash-lite`. If you set your own alias with the same name, your value wins. Custom aliases come from `agents.defaults.models.<modelId>.alias`, e.g.:

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-6" },
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
        "anthropic/claude-sonnet-4-6": { alias: "sonnet" },
      },
    },
  },
}
```

To add models from other providers, configure the provider/model plus its API key. OpenRouter (pay-per-token) and Z.AI (GLM models):

```json5
{
  agents: {
    defaults: {
      model: { primary: "openrouter/anthropic/claude-sonnet-4-6" },
      models: { "openrouter/anthropic/claude-sonnet-4-6": {} },
    },
  },
  env: { OPENROUTER_API_KEY: "sk-or-..." },
}
```

If you reference a provider/model but the provider key is missing, you get a runtime auth error (e.g. `No API key found for provider "zai"`). If `agents.defaults.models` is set, it becomes the **allowlist** for `/model` and session overrides; choosing a model not in the list returns `Model "provider/model" is not allowed. Use /models to list providers, or /models <provider> to list models.` (with an `openclaw config set agents.defaults.models '{"provider/model":{}}' --strict-json --merge` hint) **instead of** a normal reply. Fix by adding the exact model, adding a provider wildcard such as `"provider/*": {}` for dynamic catalogs, removing the allowlist, or picking from `/model list`; if `--runtime codex` was included, update the allowlist first then retry the same command. An `Unknown model: minimax/MiniMax-M3` error means the provider isn't configured (no provider config or auth profile found) — upgrade and restart the gateway, ensure the provider is configured or auth exists in env/auth profiles (`MINIMAX_API_KEY` for `minimax`, `MINIMAX_OAUTH_TOKEN` or stored OAuth for `minimax-portal`), use the exact case-sensitive model id, then `openclaw models list`. Auth is **per-agent**, stored in `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`; a `No API key found` error after adding a new agent usually means its auth store is empty — run `openclaw agents add <id>` and configure auth, or copy only portable static `api_key`/`token` profiles into the new store (sign in fresh for OAuth, or let OpenClaw read through to the default/main agent without cloning refresh tokens). Do **not** reuse `agentDir` across agents (it causes auth/session collisions).

## Model Failover and "All Models Failed"

Failover happens in two stages: (1) **auth profile rotation** within the same provider, then (2) **model fallback** to the next model in `agents.defaults.model.fallbacks`. Cooldowns apply to failing profiles (exponential backoff) so OpenClaw keeps responding even when a provider is rate-limited or temporarily failing. The rate-limit bucket includes more than plain `429`: OpenClaw also treats `Too many concurrent requests`, `ThrottlingException`, `concurrency limit reached`, `workers_ai ... quota limit exceeded`, `resource exhausted`, and periodic usage-window limits (`weekly/monthly limit reached`) as failover-worthy. Some billing-looking responses are not `402`, and some HTTP `402` responses also stay transient; explicit billing text on `401`/`403` can stay in the billing lane, but provider-specific text matchers stay scoped to their owning provider (e.g. OpenRouter `Key limit exceeded`). A `402` that looks like a retryable usage-window or org/workspace spend limit (`daily limit reached, resets tomorrow`, `organization spending limit exceeded`) is treated as `rate_limit`, not a long billing disable.

Context-overflow errors are different — signatures such as `request_too_large`, `input exceeds the maximum number of tokens`, `input token count exceeds the maximum number of input tokens`, `input is too long for the model`, or `ollama error: context length exceeded` stay on the compaction/retry path instead of advancing model fallback. Generic server-error text is intentionally narrow: OpenClaw treats provider-scoped transient shapes — Anthropic bare `An unknown error occurred`, OpenRouter bare `Provider returned error`, stop-reason errors like `Unhandled stop reason: error`, JSON `api_error` payloads with transient text (`internal server error`, `unknown error, 520`, `upstream error`, `backend error`), and provider-busy errors such as `ModelNotReadyException` — as failover-worthy when the provider context matches, while generic text like `LLM request failed with an unknown error.` stays conservative and does not trigger fallback. If your config lists Google Gemini as a fallback (or you switched to a Gemini shorthand) without Google credentials, you'll see `No API key found for provider "google"` — either provide Google auth or remove Google models from `agents.defaults.model.fallbacks` / aliases. For `LLM request rejected: thinking signature required (Google Antigravity)`, the session history holds thinking blocks without signatures (often from an aborted stream); OpenClaw now strips unsigned thinking blocks for Google Antigravity Claude, but if it persists, start a **new session** or set `/thinking off` for that agent.

For `No credentials found for profile anthropic:default`, the system tried profile ID `anthropic:default` but found no credentials in the expected store. Checklist: confirm where profiles live (current `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`; legacy `~/.openclaw/agent/*`, migrated by `openclaw doctor`); confirm the env var is loaded by the Gateway (a shell-set `ANTHROPIC_API_KEY` may not be inherited under systemd/launchd — put it in `~/.openclaw/.env` or enable `env.shellEnv`); edit the correct agent (multi-agent setups have multiple `auth-profiles.json`); and sanity-check with `openclaw models status`. For the bare `No credentials found for profile anthropic`, the run is pinned to an Anthropic profile the Gateway can't find — use Claude CLI via `openclaw models auth login --provider anthropic --method cli --set-default` on the gateway host, or put `ANTHROPIC_API_KEY` in `~/.openclaw/.env` on the gateway host and clear a forced order with `openclaw models auth order clear --provider anthropic`; in remote mode, profiles live on the gateway machine, not your laptop.

## Auth Profiles: What They Are and How to Manage Them

An auth profile is a named credential record (OAuth or API key) tied to a provider; profiles live in `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`. Inspect saved profiles without dumping secrets via `openclaw models auth list` (optionally `--provider <id>` or `--json`). Typical IDs are provider-prefixed: `anthropic:default` (common when no email identity exists), `anthropic:<email>` for OAuth identities, and custom IDs you choose (e.g. `anthropic:work`).

You can control which profile is tried first. Config supports optional per-profile metadata and an ordering per provider (`auth.order.<provider>`); this stores no secrets — it maps IDs to provider/mode and sets rotation order. OpenClaw may temporarily skip a profile in a short **cooldown** (rate limits/timeouts/auth failures) or a longer **disabled** state (billing/insufficient credits); inspect with `openclaw models status --json` and check `auth.unusableProfiles` (tuning: `auth.cooldowns.billingBackoffHours*`). Rate-limit cooldowns can be model-scoped — a profile cooling down for one model can still serve a sibling model on the same provider, while billing/disabled windows block the whole profile. A **per-agent** order override (stored in that agent's `auth-state.json`) is set via the CLI:

```bash
# Defaults to the configured default agent (omit --agent)
openclaw models auth order get --provider anthropic

# Lock rotation to a single profile (only try this one)
openclaw models auth order set --provider anthropic anthropic:default

# Or set an explicit order (fallback within provider)
openclaw models auth order set --provider anthropic anthropic:work anthropic:default

# Clear override (fall back to config auth.order / round-robin)
openclaw models auth order clear --provider anthropic
```

To target a specific agent, add `--agent`, e.g. `openclaw models auth order set --provider anthropic --agent main anthropic:default`. To verify what will be tried, run `openclaw models status --probe`; if a stored profile is omitted from the explicit order, probe reports `excluded_by_auth_order` for it instead of trying it silently. On **OAuth vs API key**: OAuth / CLI login often leverages subscription access where the provider supports it — for Anthropic, OpenClaw's Claude CLI backend uses Claude Code `claude -p`, which Anthropic currently treats as Agent SDK/programmatic usage with a separate monthly Agent SDK credit starting June 15, 2026 — while API keys use pay-per-token billing. The wizard explicitly supports Anthropic Claude CLI, OpenAI Codex OAuth, and API keys.

**Source**: OpenClaw documentation — `help/faq-models` (mirror `inbox/openclaw_docs/help/faq-models.md`)
**Last Updated**: 2026-06-22
**Status**: Active
