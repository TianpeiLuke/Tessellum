---
tags:
  - resource
  - documentation
  - hermes_agent
  - inference_provider
  - developer_guide
keywords:
  - adding inference provider
  - PROVIDER_REGISTRY auth metadata
  - api_mode chat_completions
  - resolve_runtime_provider
  - provider model alias
  - native provider adapter
  - fast path provider plugin
  - provider wiring pitfalls
topics:
  - Hermes Agent
  - Developer Guide
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-providers
access_control_group: ["general"]
---

# Hermes Agent — Adding an Inference Provider

## Overview

This is the developer procedure for wiring a new **built-in inference provider** into Hermes Agent — making a model service a first-class option across the auth → runtime → CLI → auxiliary layers. Hermes can *already* talk to any OpenAI-compatible endpoint through the custom-provider path, so the page opens with a deliberate gate: **do not add a built-in provider unless you want first-class UX** — provider-specific auth or token refresh, a curated model catalog, setup / `hermes model` menu entries, `provider:model` aliases, or a non-OpenAI API shape that needs an adapter. If the service is "just another OpenAI-compatible base URL and API key", a named custom provider may be enough.

A built-in provider has to line up across several layers, and the procedure is mostly about not missing one. The load-bearing abstraction is `api_mode`: most providers use `chat_completions`, Codex uses `codex_responses`, and Anthropic uses `anthropic_messages`; a brand-new non-OpenAI protocol means adding a new adapter and a new `api_mode` branch. The page offers two implementation paths (OpenAI-compatible vs native), a **fast path** (a drop-in provider plugin that auto-wires everything) for simple API-key providers, and a **full path** (a 10-step checklist) for OAuth/complex/native providers. It closes with two checklists, seven common pitfalls, and a symbol list for finding every place a provider touches.

## The mental model

A built-in provider lines up across a few layers:

1. `hermes_cli/auth.py` decides how credentials are found.
2. `hermes_cli/runtime_provider.py` turns that into runtime data — `provider`, `api_mode`, `base_url`, `api_key`, `source`.
3. `run_agent.py` uses `api_mode` to decide how requests are built and sent.
4. `hermes_cli/models.py` and `hermes_cli/main.py` make the provider show up in the CLI. (`hermes_cli/setup.py` delegates to `main.py` automatically — no changes needed there.)
5. `agent/auxiliary_client.py` and `agent/model_metadata.py` keep side tasks and token budgeting working.

The important abstraction is `api_mode`: most providers use `chat_completions`; Codex uses `codex_responses`; Anthropic uses `anthropic_messages`; a new non-OpenAI protocol usually means a new adapter and a new `api_mode` branch.

## Choose the implementation path first

**Path A — OpenAI-compatible provider.** Use when the provider accepts standard chat-completions requests. Typical work: add auth metadata, model catalog / aliases, runtime resolution, CLI menu wiring, aux-model defaults, tests, and user docs. You usually do not need a new adapter or a new `api_mode`.

**Path B — Native provider.** Use when the provider does not behave like OpenAI chat completions (in-tree examples: `codex_responses`, `anthropic_messages`). This path includes everything from Path A **plus** a provider adapter in `agent/`, `run_agent.py` branches (request building, dispatch, usage extraction, interrupt handling, response normalization), and adapter tests.

### File checklist

Required for every built-in provider: `hermes_cli/auth.py`, `hermes_cli/models.py`, `hermes_cli/runtime_provider.py`, `hermes_cli/main.py`, `agent/auxiliary_client.py`, `agent/model_metadata.py`, tests, and user docs under `website/docs/`. `hermes_cli/setup.py` does **not** need changes — the wizard delegates provider/model selection to `select_provider_and_model()` in `main.py`, so any provider added there is automatically available in `hermes setup`. Native / non-OpenAI providers additionally touch `agent/<provider>_adapter.py`, `run_agent.py`, and `pyproject.toml` (if a provider SDK is required).

## Fast path: Simple API-key providers

If the provider is just an OpenAI-compatible endpoint that authenticates with a single API key, you do **not** touch `auth.py`, `runtime_provider.py`, `main.py`, or any other full-checklist file. All you need is a plugin directory under `plugins/model-providers/<your-provider>/` containing `__init__.py` (calls `register_provider(profile)` at module-level) and `plugin.yaml` (manifest: name, `kind: model-provider`, version, description). Provider plugins auto-load the first time anything calls `get_provider_profile()` or `list_providers()` — both bundled plugins (this repo) and user plugins at `$HERMES_HOME/plugins/model-providers/` get picked up.

When the plugin calls `register_provider()`, these wire up automatically: a `PROVIDER_REGISTRY` entry in `auth.py` (credential/env-var resolution); `api_mode` set to `chat_completions`; `base_url` from config or the declared env var; `env_vars` checked in priority order for the API key; the `fallback_models` list; the `--provider` CLI flag and `hermes model` menu entry; `hermes setup` delegation; `provider:model` alias syntax; the runtime resolver returning the correct `base_url`/`api_key`; and clean fallback-model activation into the provider. User plugins at `$HERMES_HOME/plugins/model-providers/<name>/` override bundled plugins of the same name (last-writer-wins in `register_provider()`), so third parties can replace any built-in profile without editing the repo. See `plugins/model-providers/nvidia/` or `plugins/model-providers/gmi/` as a template, and the Model Provider Plugin guide for field reference and end-to-end examples.

## Full path: Steps 1–10

Use the full checklist when the provider needs OAuth / token refresh (Nous Portal, Codex, Google Gemini, Qwen Portal, Copilot), a non-OpenAI API shape (Anthropic Messages, Codex Responses), custom endpoint detection / multi-region probing (z.ai, Kimi), a curated static catalog or live `/models` fetch, or bespoke `hermes model` auth flows.

**Step 1 — Pick one canonical provider id.** Choose a single id (e.g. `openai-codex`, `kimi-coding`, `minimax-cn`) and use it *everywhere*: `PROVIDER_REGISTRY` (`auth.py`), `_PROVIDER_LABELS` (`models.py`), `_PROVIDER_ALIASES` (both `auth.py` and `models.py`), CLI `--provider` choices (`main.py`), setup/model branches, aux-model defaults, and tests. If the id differs between files the provider feels half-wired — auth may work while `/model`, setup, or runtime resolution silently misses it.

**Step 2 — Add auth metadata in `hermes_cli/auth.py`.** For API-key providers add a `ProviderConfig` to `PROVIDER_REGISTRY` (`id`, `name`, `auth_type="api_key"`, `inference_base_url`, `api_key_env_vars`, optional `base_url_env_var`) and aliases to `_PROVIDER_ALIASES`. Templates: simple API-key path (Z.AI, MiniMax), API-key with endpoint detection (Kimi, Z.AI), native token resolution (Anthropic), OAuth / auth-store path (Nous, OpenAI Codex). Decide which env vars to check and in what priority, whether base-URL overrides / endpoint probing / token refresh are needed, and what the auth error says when credentials are missing. For anything beyond "look up an API key", add a dedicated credential resolver rather than shoving logic into unrelated branches.

**Step 3 — Add model catalog and aliases in `hermes_cli/models.py`.** Update `_PROVIDER_MODELS`, `_PROVIDER_LABELS`, `_PROVIDER_ALIASES`, provider display order in `list_available_providers()`, and `provider_model_ids()` if a live `/models` fetch is supported (prefer the live list, keep `_PROVIDER_MODELS` as the static fallback). This file is what makes `provider:model` inputs work:

```text
anthropic:claude-sonnet-4-6
kimi:model-name
```

If aliases are missing here, the provider may authenticate correctly but still fail in `/model` parsing.

**Step 4 — Resolve runtime data in `hermes_cli/runtime_provider.py`.** `resolve_runtime_provider()` is the shared path used by CLI, gateway, cron, ACP, and helper clients. Add a branch returning at least:

```python
{
    "provider": "your-provider",
    "api_mode": "chat_completions",  # or your native mode
    "base_url": "https://...",
    "api_key": "...",
    "source": "env|portal|auth-store|explicit",
    "requested_provider": requested_provider,
}
```

For OpenAI-compatible providers `api_mode` should usually stay `chat_completions`. Be careful with API-key precedence — Hermes already avoids leaking an OpenRouter key to unrelated endpoints; a new provider should be equally explicit about which key goes to which base URL.

**Step 5 — Wire the CLI in `hermes_cli/main.py`.** A provider is not discoverable until it shows up in the interactive `hermes model` flow. Update the `provider_labels` dict, the `providers` list in `select_provider_and_model()`, the provider dispatch (`if selected_provider == ...`), the `--provider` argument choices, login/logout choices if applicable, and add a `_model_flow_<provider>()` function (or reuse `_model_flow_api_key_provider()` if it fits). `setup.py` inherits this automatically.

**Step 6 — Keep auxiliary calls working.** In `agent/auxiliary_client.py`, add a cheap/fast aux model to `_API_KEY_PROVIDER_AUX_MODELS` for direct API-key providers (aux tasks include vision summarization, web-extraction summaries, context-compression summaries, session-search summaries, memory flushes). In `agent/model_metadata.py`, add context lengths for the provider's models so token budgeting, compression thresholds, and limits stay sane. Without an aux default, side tasks may fall back badly or burn an expensive main model.

**Step 7 — If native, add an adapter and `run_agent.py` support.** Isolate provider-specific logic in `agent/<provider>_adapter.py` (build the SDK/HTTP client, resolve tokens, convert OpenAI-style messages to the provider's request format, convert tool schemas if needed, normalize responses, extract usage/finish-reason). Keep `run_agent.py` on orchestration — it calls adapter helpers, not inline payload building. Then search `run_agent.py` for `api_mode` and audit **every** switch point: `__init__` chooses the new mode, client construction works, `_build_api_kwargs()` formats requests, `_interruptible_api_call()` dispatches to the right client call, interrupt / rebuild paths work, response validation accepts the shape, finish-reason and token-usage extraction are correct, fallback-model activation switches in cleanly, and summary/memory-flush paths still work. Also search for `self.client.` — any path assuming the standard OpenAI client can break when a native provider uses a different client object or `self.client = None`. Watch prompt caching and provider-specific request fields (Anthropic's native prompt-caching path, OpenRouter's provider-routing fields): only send fields the provider understands.

**Steps 8–10 — Tests, live verification, docs.** Touch the provider-wiring tests (`tests/hermes_cli/test_runtime_provider_resolution.py`, `tests/cli/test_cli_provider_resolution.py`, `tests/hermes_cli/test_model_switch_*.py`, `tests/hermes_cli/test_setup_model_provider.py`, `tests/run_agent/test_provider_parity.py`, `tests/run_agent/test_run_agent.py`, and `tests/test_<provider>_adapter.py` for native), covering auth resolution, CLI/provider selection, runtime resolution, the agent execution path, `provider:model` parsing, and adapter message conversion. Run with xdist disabled, then smoke-test a real call:

```bash
source venv/bin/activate
python -m hermes_cli.main chat -q "Say hello" --provider your-provider --model your-model
```

Also test interactive `hermes model` / `hermes setup` if menus changed, and verify at least one tool call for native providers. Finally, if the provider ships first-class, update user docs (`website/docs/getting-started/quickstart.md`, `user-guide/configuration.md`, `reference/environment-variables.md`) — a perfectly wired provider is useless if users cannot discover the required env vars or setup flow.

## Checklists, pitfalls, and search targets

The **OpenAI-compatible checklist** is the Steps-1–6 + tests + user-docs list. The **native checklist** is "everything in the OpenAI-compatible checklist" plus the adapter, the new `api_mode` in `run_agent.py`, working interrupt/rebuild, usage/finish-reason extraction, fallback path, adapter tests, and a passing live smoke test.

The **seven common pitfalls**: (1) adding to auth but not model parsing (credentials resolve while `/model` and `provider:model` fail); (2) forgetting `config["model"]` can be a string *or* a dict; (3) assuming a built-in provider is required when a custom OpenAI-compatible provider would do with less maintenance; (4) forgetting auxiliary paths (main chat works while summarization/memory/vision break); (5) native-provider branches hiding in `run_agent.py` (search `api_mode` and `self.client.`); (6) sending OpenRouter-only knobs to other providers; (7) updating `hermes model` but not `hermes setup`.

When hunting for everywhere a provider touches, search these symbols: `PROVIDER_REGISTRY`, `_PROVIDER_ALIASES`, `_PROVIDER_MODELS`, `resolve_runtime_provider`, `_model_flow_`, `select_provider_and_model`, `api_mode`, `_API_KEY_PROVIDER_AUX_MODELS`, and `self.client.`.

**Source**: `inbox/hermes_agent_docs/developer-guide/adding-providers.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/adding-providers
**Last Updated**: 2026-06-19
**Status**: Active
