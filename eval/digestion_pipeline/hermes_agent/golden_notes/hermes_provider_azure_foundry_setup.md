---
tags:
  - resource
  - documentation
  - hermes_agent
  - provider_setup
  - azure_foundry
keywords:
  - azure-foundry provider
  - Microsoft Foundry
  - Azure OpenAI
  - OpenAI-style vs Anthropic-style transport
  - api_mode auto-detection
  - codex_responses auto-route
topics:
  - Hermes Agent
  - Provider Setup
  - Microsoft Foundry
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/azure-foundry
access_control_group: ["general"]
---

# Hermes Provider Setup — Microsoft Foundry (Azure)

## Overview

This is the setup procedure for Hermes Agent's `azure-foundry` provider, which connects Hermes to **Microsoft Foundry** (formerly Azure AI Foundry) and **Azure OpenAI**. The defining complication it solves is that a single Foundry resource can host models behind **two different wire formats**, and the right transport depends on the deployed model family:

- **OpenAI-style** — `POST /v1/chat/completions` on endpoints like `https://<resource>.openai.azure.com/openai/v1`. Used for GPT-4.x, GPT-5.x, Llama, Mistral, and most open-weight models.
- **Anthropic-style** — `POST /v1/messages` on endpoints like `https://<resource>.services.ai.azure.com/anthropic`. Used when Microsoft Foundry serves Claude models via the Anthropic Messages API format.

The `hermes model` wizard probes your endpoint and **auto-detects** which transport it uses, which deployments are available, and each model's context length, so you usually do not have to know the wire format in advance. This note covers the procedural surface: the wizard's probe chain, the `config.yaml` that gets written, the two wire-format routing rules, the `provider: anthropic` + Azure base-URL alternative, model discovery, and troubleshooting. The **keyless Microsoft Entra ID auth model** (RBAC, `DefaultAzureCredential` resolution order, deployment patterns, and the `AZURE_*` env-var table) is documented in its own note — see [hermes_provider_azure_foundry_entra_id](hermes_provider_azure_foundry_entra_id.md).

## Prerequisites

- A Microsoft Foundry or Azure OpenAI resource with at least one deployment.
- The deployment's endpoint URL.
- **Either** an API key (Azure Portal → "Keys and Endpoint") **or** the **Azure AI User** RBAC role on the Foundry resource if you plan to use Microsoft Entra ID (the keyless path Microsoft recommends; covered in the Entra-ID note). Some tenants may show the role as **Foundry User** during Microsoft's rename rollout.

## Quick Start

```bash
hermes model
# → Select "Azure Foundry"
# → Enter your endpoint URL
# → Choose Authentication:
#     1. API key
#     2. Microsoft Entra ID  (managed identity / workload identity / az login)
# → (Entra) Hermes probes DefaultAzureCredential; on success it never asks for a key
# → (API key) Enter your API key
# Hermes probes the endpoint and auto-detects transport + models
# → Pick a model from the list (or type a deployment name manually)
```

The wizard runs a four-step probe to pick the transport (`api_mode`) and prefill the model picker:

1. **Sniff the URL path** — URLs ending in `/anthropic` are recognised as Microsoft Foundry Claude routes.
2. **Probe `GET <base>/models`** — if the endpoint returns an OpenAI-shaped model list, Hermes switches to `chat_completions` and prefills the picker with the returned deployment IDs.
3. **Probe Anthropic Messages shape** — fallback for endpoints that do not expose `/models` but do accept the Anthropic Messages format.
4. **Fall back to manual entry** — private/gated endpoints that reject every probe still work; you pick the API mode and type a deployment name by hand.

Context length for the chosen model is resolved via Hermes' standard metadata chain (`models.dev`, provider metadata, and hardcoded family fallbacks) and stored in `config.yaml` so the model can size its own context window correctly.

## Configuration (written to `config.yaml`)

After running the wizard you'll see something like this written to `config.yaml`, with the API key set as `AZURE_FOUNDRY_API_KEY=<your-azure-key>` in `~/.hermes/.env`:

```yaml
model:
  provider: azure-foundry
  base_url: https://my-resource.openai.azure.com/openai/v1
  api_mode: chat_completions         # or "anthropic_messages"
  default: gpt-5.4-mini              # your deployment / model name
  context_length: 400000             # auto-detected
```

The `api_mode` is the transport selector the probe chain resolves; `base_url` and `default` are the endpoint and deployment name; `context_length` is auto-detected. For the keyless `auth_mode: entra_id` variant of this block (and the `AZURE_*` env vars `azure-identity` reads), see [hermes_provider_azure_foundry_entra_id](hermes_provider_azure_foundry_entra_id.md). The full `config.yaml` model/provider reference lives in the configuration docs.

## OpenAI-style endpoints (GPT, Llama, etc.)

Azure OpenAI's v1 GA endpoint accepts the standard `openai` Python client with minimal changes:

```yaml
model:
  provider: azure-foundry
  base_url: https://my-resource.openai.azure.com/openai/v1
  api_mode: chat_completions
  default: gpt-5.4
```

Three behaviours matter on this path:

- **GPT-5.x, codex, and o-series auto-route to the Responses API.** Microsoft Foundry deploys GPT-5 / codex / o1 / o3 / o4 models as Responses-API-only — calling `/chat/completions` against them returns `400 "The requested operation is unsupported."`. Hermes detects these model families by name and upgrades `api_mode` to `codex_responses` transparently, even when `config.yaml` still reads `api_mode: chat_completions`. GPT-4, GPT-4o, Llama, Mistral, and other deployments stay on `/chat/completions`.
- **`max_completion_tokens` is used automatically.** Azure OpenAI (like direct OpenAI) requires `max_completion_tokens` for gpt-4o, o-series, and gpt-5.x models. Hermes sends the right parameter based on the endpoint.
- **Pre-v1 endpoints that require `api-version`.** For a legacy base URL like `https://<resource>.openai.azure.com/openai?api-version=2025-04-01-preview`, Hermes extracts the query string and forwards it via `default_query` on every request (the OpenAI SDK otherwise drops it when joining paths).

## Anthropic-style endpoints (Claude via Microsoft Foundry)

For Claude deployments, use the Anthropic-style route:

```yaml
model:
  provider: azure-foundry
  base_url: https://my-resource.services.ai.azure.com/anthropic
  api_mode: anthropic_messages
  default: claude-sonnet-4-6
```

Important behaviour:

- **`/v1` is stripped from the base URL.** The Anthropic SDK appends `/v1/messages` to every request URL — Hermes removes any trailing `/v1` before handing the URL to the SDK to avoid double-`/v1` paths.
- **`api-version` is sent via `default_query`, not appended to the URL.** Azure Anthropic requires an `api-version` query string. Baking it into the base URL produces malformed paths like `/anthropic?api-version=.../v1/messages` and returns 404. Hermes passes `api-version=2025-04-15` via the Anthropic SDK's `default_query` instead.
- **Bearer auth is used instead of `x-api-key`.** Azure's Anthropic-compatible route requires `Authorization: Bearer <key>` rather than Anthropic's native `x-api-key` header. Hermes detects `azure.com` in the base URL and routes the API key through the SDK's `auth_token` field so the right header reaches the upstream.
- **1M context window beta header is kept.** Azure still gates the 1M-token Claude context (Opus 4.6/4.7, Sonnet 4.6) behind the `anthropic-beta: context-1m-2025-08-07` header. Hermes keeps that beta header on Azure paths (it's stripped from native Anthropic OAuth requests because some subscriptions reject it, but Azure requires it).
- **OAuth token refresh is disabled.** Azure deployments use static API keys. The `~/.claude/.credentials.json` OAuth token refresh loop that applies to Anthropic Console is explicitly skipped for Azure endpoints to prevent the Claude Code OAuth token from overwriting your Azure key mid-session.

## Alternative: `provider: anthropic` + Azure base URL

If you already have `provider: anthropic` configured and just want to point it at Microsoft Foundry for Claude, you can skip the `azure-foundry` provider entirely:

```yaml
model:
  provider: anthropic
  base_url: https://my-resource.services.ai.azure.com/anthropic
  key_env: AZURE_ANTHROPIC_KEY
  default: claude-sonnet-4-6
```

With `AZURE_ANTHROPIC_KEY` set in `~/.hermes/.env`. Hermes detects `azure.com` in the base URL and short-circuits around the Claude Code OAuth token chain so the Azure key is used directly with `x-api-key` auth. `key_env` is the canonical snake_case field name; `api_key_env` (and the camelCase `keyEnv` / `apiKeyEnv`) are accepted as aliases. If both `key_env` and `AZURE_ANTHROPIC_KEY`/`ANTHROPIC_API_KEY` are set, the `key_env`-named env var wins.

## Model discovery

Azure does **not** expose a pure-API-key endpoint to list your *deployed* model deployments. Deployment enumeration requires Azure Resource Manager authentication (`az cognitiveservices account deployment list`) with an Azure AD principal, not the inference API key. What Hermes can do:

- Azure OpenAI v1 endpoints (`<resource>.openai.azure.com/openai/v1`) expose `GET /models` with the resource's **available** model catalog. Hermes uses this list to prefill the model picker.
- Microsoft Foundry `/anthropic` routes: detected via URL path, model name entered manually.
- Private / firewalled endpoints: manual entry with a friendly "couldn't probe" message.

You can always type a deployment name directly — Hermes does not validate against the returned list.

## Troubleshooting

- **401 Unauthorized on gpt-5.x deployments.** Azure serves gpt-5.x on `/chat/completions`, not `/responses`. Hermes handles this automatically when the URL contains `openai.azure.com`, but if you see a 401 with an `Invalid API key` body, check that `api_mode` in your `config.yaml` is `chat_completions`.
- **404 on `/v1/messages?api-version=.../v1/messages`.** This is the malformed-URL bug from pre-fix Azure Anthropic setups. Upgrade Hermes — the `api-version` parameter is now passed via `default_query` rather than baked into the base URL, so the SDK can't corrupt it during URL joining.
- **Wizard says "Auto-detection incomplete."** The endpoint rejected both the `/models` probe and the Anthropic Messages probe. This is normal for private endpoints behind a firewall or with an IP allow-list. Fall back to manual API mode selection and type your deployment name — everything still works, Hermes just can't prefill the picker.
- **Wrong transport picked.** Run `hermes model` again and the wizard will re-probe. If the probe still picks the wrong mode, you can edit `config.yaml` directly:

```yaml
model:
  provider: azure-foundry
  api_mode: anthropic_messages   # or chat_completions
```

(Entra-ID-specific troubleshooting — credential-chain exhaustion, preflight hangs, and 401s after switching to `auth_mode: entra_id` — is in the [Entra-ID note](hermes_provider_azure_foundry_entra_id.md).)

**Source**: `inbox/hermes_agent_docs/guides/azure-foundry.md`
**Last Updated**: 2026-06-19
**Status**: Active
