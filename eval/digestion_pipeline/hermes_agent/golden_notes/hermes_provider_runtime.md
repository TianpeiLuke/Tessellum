---
tags:
  - resource
  - documentation
  - hermes_agent
  - provider_runtime
  - model_routing
keywords:
  - provider runtime resolution
  - resolution precedence
  - provider profile registry
  - api_mode base_url credentials
  - native anthropic codex responses
  - auxiliary model routing
  - fallback provider chain
topics:
  - Hermes Agent
  - Provider Runtime
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/provider-runtime
access_control_group: ["general"]
---

# Hermes Agent — Provider Runtime Resolution

## Overview

The Provider Runtime is the **single shared resolver** Hermes uses to turn a desired *(provider, model)* into a concrete callable client — resolving the API mode, credentials, and base URL — across every execution surface: `hermes chat` (CLI), the messaging gateway, cron jobs running in fresh sessions, ACP editor sessions, and auxiliary model tasks. Rather than duplicate auth and endpoint logic in each surface, all of them route through the same path so a model/provider choice resolves identically everywhere. The primary implementation spans `hermes_cli/runtime_provider.py` (credential resolution, `_resolve_custom_runtime()`), `hermes_cli/auth.py` (`resolve_provider()`), `hermes_cli/model_switch.py` (the shared `/model` switch pipeline used by CLI and gateway), `agent/auxiliary_client.py` (auxiliary routing), and the `providers/` package — the `ProviderProfile` ABC plus registry entry points (`register_provider`, `get_provider_profile`, `list_providers`). Per-provider definitions live as **bundled plugins** under `plugins/model-providers/<name>/`. This is the runtime *behavior* layer; the user-facing provider catalog, the routing/fallback feature guide, and the how-to of *adding* a provider live in their own docs (link-outs below).

## Resolution precedence

At a high level, provider resolution applies four ordered sources, highest precedence first:

1. **Explicit CLI/runtime request** — what the user or surface asked for at invocation time.
2. **`config.yaml` model/provider config** — the saved model/provider choice.
3. **Environment variables** — exported provider keys/base URLs.
4. **Provider-specific defaults or auto resolution** — the bundled profile's defaults.

That ordering matters because Hermes treats the **saved model/provider choice as the source of truth** for normal runs. This prevents a stale shell export from silently overriding the endpoint a user last selected in `hermes model`.

## Providers

Provider definitions are not hard-coded branches in the resolver — each lives as a bundled plugin under `plugins/model-providers/<name>/` that declares its `api_mode`, `base_url`, `env_vars`, and `fallback_models` and **registers itself into the registry on first access**. A user plugin at `$HERMES_HOME/plugins/model-providers/<name>/` overrides a bundled plugin of the same name. `get_provider_profile()` returns the `ProviderProfile` for a provider id; `runtime_provider.py` calls it at resolution time to obtain the canonical `base_url`, `env_vars` priority list, `api_mode`, and `fallback_models` without duplicating that data. Adding a new plugin that calls `register_provider()` is enough for the resolver to pick it up — **no branch is needed in the resolver itself**.

Current provider families (see `plugins/model-providers/` for the complete bundled set) include: OpenRouter; Nous Portal; OpenAI Codex; Copilot / Copilot ACP; Anthropic (native); Google / Gemini (`gemini`, `google-gemini-cli`); Alibaba / DashScope (`alibaba`, `alibaba-coding-plan`); DeepSeek; Z.AI; Kimi / Moonshot (`kimi-coding`, `kimi-coding-cn`); MiniMax (`minimax`, `minimax-cn`, `minimax-oauth`); Kilo Code; Hugging Face; OpenCode Zen / OpenCode Go; AWS Bedrock; Azure Foundry; NVIDIA NIM; xAI (Grok); Arcee; GMI Cloud; StepFun; Qwen OAuth; Xiaomi; Ollama Cloud; LM Studio; Tencent TokenHub; `custom` (a first-class provider for any OpenAI-compatible endpoint); and **named custom providers** (the `custom_providers` list in `config.yaml`).

## Output of runtime resolution

A single resolution call returns the data every surface needs to make a request:

- `provider`
- `api_mode`
- `base_url`
- `api_key`
- `source` (which precedence level supplied the credential)
- provider-specific metadata such as expiry/refresh info

## Why this matters

This resolver is the main reason Hermes can **share auth/runtime logic** between `hermes chat`, gateway message handling, cron jobs running in fresh sessions, ACP editor sessions, and auxiliary model tasks. One code path means the same model/provider choice behaves identically regardless of which surface invoked it.

## OpenRouter and custom OpenAI-compatible base URLs

Hermes contains logic to **avoid leaking the wrong API key to a custom endpoint** when multiple provider keys exist (e.g. `OPENROUTER_API_KEY` and `OPENAI_API_KEY`). Each provider's API key is **scoped to its own base URL**:

- `OPENROUTER_API_KEY` is only sent to `openrouter.ai` endpoints.
- `OPENAI_API_KEY` is used for custom endpoints and as a fallback.

Hermes also distinguishes a **real custom endpoint** selected by the user from the **OpenRouter fallback path** used when no custom endpoint is configured. That distinction is especially important for local model servers, non-OpenRouter OpenAI-compatible APIs, switching providers without re-running setup, and config-saved custom endpoints that should keep working even when `OPENAI_BASE_URL` is not exported in the current shell.

## Native Anthropic path

Anthropic is no longer "via OpenRouter" only. When provider resolution selects `anthropic`, Hermes uses `api_mode = anthropic_messages`, the native Anthropic Messages API, and `agent/anthropic_adapter.py` for translation. Credential resolution for native Anthropic **prefers refreshable Claude Code credentials over copied env tokens** when both are present. In practice:

- Claude Code credential files are the preferred source when they include refreshable auth.
- Manual `ANTHROPIC_TOKEN` / `CLAUDE_CODE_OAUTH_TOKEN` values still work as explicit overrides.
- Hermes preflights Anthropic credential refresh before native Messages API calls.
- Hermes still retries once on a 401 after rebuilding the Anthropic client, as a fallback path.

## OpenAI Codex path

Codex uses a **separate Responses API path**: `api_mode = codex_responses`, with dedicated credential resolution and auth-store support.

## Auxiliary model routing

Auxiliary tasks — vision, web-extraction summarization, context-compression summaries, skills-hub operations, MCP helper operations, and memory flushes — **can use their own provider/model routing** rather than the main conversational model. When an auxiliary task is configured with provider `main`, Hermes resolves it through the **same shared runtime path** as normal chat. In practice that means env-driven custom endpoints still work, custom endpoints saved via `hermes model` / `config.yaml` also work, and auxiliary routing can tell the difference between a real saved custom endpoint and the OpenRouter fallback.

## Fallback models

Hermes supports a configured **fallback provider chain** — a list of `(provider, model)` entries tried in order when the primary model encounters errors. The legacy single-pair `fallback_model` dict is still accepted for back-compat (and migrated on first write).

**How it works internally.** `AIAgent.__init__` stores the `fallback_model` dict and sets `_fallback_activated = False`. `_try_activate_fallback()` is called from **three trigger points** in the main retry loop in `run_agent.py`: after max retries on invalid API responses (None choices, missing content); on non-retryable client errors (HTTP 401, 403, 404); and after max retries on transient errors (HTTP 429, 500, 502, 503). The activation flow returns `False` immediately if already activated or not configured; otherwise it calls `resolve_provider_client()` from `auxiliary_client.py` to build a new client with proper auth, determines `api_mode` (`codex_responses` for openai-codex, `anthropic_messages` for anthropic, `chat_completions` for everything else), swaps in-place `self.model`/`self.provider`/`self.base_url`/`self.api_mode`/`self.client`/`self._client_kwargs`, builds a native Anthropic client for an anthropic fallback (instead of OpenAI-compatible), re-evaluates prompt caching (enabled for Claude models on OpenRouter), sets `_fallback_activated = True` to prevent firing again, resets the retry count to 0, and continues the loop. Config flow: the CLI reads `CLI_CONFIG["fallback_model"]` and passes it to `AIAgent(fallback_model=...)`; the gateway's `gateway/run.py._load_fallback_model()` reads `config.yaml`; both require non-empty `provider` and `model` keys or fallback is disabled.

**What does NOT support fallback.** **Subagent delegation** (`tools/delegate_tool.py`): subagents inherit the parent's provider but not the fallback config. **Auxiliary tasks**: they use their own independent provider auto-detection chain. Cron jobs **do** support fallback — `run_job()` reads `fallback_providers` (or legacy `fallback_model`) from `config.yaml` and passes it to `AIAgent(fallback_model=...)`, matching the gateway pattern.

**Test coverage.** Fallback behavior is exercised across several suites: `tests/run_agent/test_fallback_credential_isolation.py` (credential isolation between primary and fallback), `tests/hermes_cli/test_fallback_cmd.py` (the `/fallback` CLI command), and `tests/gateway/test_fallback_eviction.py` (gateway eviction of failed providers).

**Source**: https://hermes-agent.nousresearch.com/docs/developer-guide/provider-runtime
**Last Updated**: 2026-06-19
**Status**: Active
