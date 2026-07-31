---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - novita
keywords:
  - openclaw novita provider
  - novita openai-compatible api
  - novita api key setup
  - novita deepseek default model
  - novita route catalog
  - novita 401 403 troubleshooting
  - hosted model aggregator openclaw
topics:
  - OpenClaw
  - Model Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/novita
access_control_group: ["general"]
---

# OpenClaw — Configure the NovitaAI Hosted Provider

## Overview

This note is the setup/configuration procedure for running OpenClaw against **NovitaAI**, a hosted AI infrastructure provider that exposes an OpenAI-compatible model API. It mirrors the `providers/novita` source page: API-key setup (onboarding flag or env var), the provider defaults (id, aliases, base URL, env var, default model), the "when to choose Novita" guidance, the seeded multi-vendor route catalog, and the 401/403 + unknown-model troubleshooting steps. In OpenClaw, Novita is a bundled model provider, so the provider id is `novita`, credentials go through the normal model auth flow, and model refs look like `novita/deepseek/deepseek-v3-0324`. OpenClaw handles provider registration, auth, aliases, model ref normalization, and base URL selection; Novita controls live model availability, account permissions, pricing, and rate limits.

## Setup

Create an API key at [novita.ai/settings/key-management](https://novita.ai/settings/key-management), then onboard the provider with the dedicated auth choice:

```bash
openclaw onboard --auth-choice novita-api-key
```

Alternatively, set the API key directly as an environment variable instead of onboarding:

```bash
export NOVITA_API_KEY="<your-novita-api-key>"
```

## Defaults

The bundled provider ships these defaults (verbatim from source):

- Provider: `novita`
- Aliases: `novita-ai`, `novitaai`
- Base URL: `https://api.novita.ai/openai/v1`
- Env var: `NOVITA_API_KEY`
- Default model: `novita/deepseek/deepseek-v3-0324`

## When to choose Novita

The source positions Novita as a hosted aggregation path. Choose Novita when:

- You want hosted open-weight model access with an OpenAI-compatible API.
- You want DeepSeek, Kimi, MiniMax, GLM, or Qwen-family routes through a single provider account.
- You want another hosted fallback path beside OpenRouter, GMI, DeepInfra, or direct vendor APIs.
- You prefer provider-side model hosting over maintaining vLLM, SGLang, LM Studio, or Ollama infrastructure.

Conversely, choose a direct vendor provider when you need vendor-native request parameters or support contracts, and choose a local provider when the model must run on your own hardware or behind your own network boundary.

## Models

The bundled catalog seeds commonly available NovitaAI route ids, including:

- `novita/moonshotai/kimi-k2.5`
- `novita/minimax/minimax-m2.7`
- `novita/zai-org/glm-5`
- `novita/deepseek/deepseek-v3-0324`
- `novita/deepseek/deepseek-r1-0528`
- `novita/qwen/qwen3-235b-a22b-fp8`

The catalog is a starting point for OpenClaw model selection; your account, region, or Novita's current catalog may add, remove, or restrict routes. Check the provider from the CLI before setting a long-lived default:

```bash
openclaw models list --provider novita
```

## Troubleshooting

The source documents three failure modes:

- **`401` or `403`** — verify the key in Novita's key management page and re-run `openclaw onboard --auth-choice novita-api-key` if the stored profile is stale.
- **Unknown model errors** — use the exact `novita/<route-id>` returned by `openclaw models list --provider novita`.
- **Slow or failed routes** — try another Novita model route, or set Novita as a fallback provider for workloads that can tolerate provider-specific variance.

**Source**: OpenClaw documentation — `providers/novita` (mirror `inbox/openclaw_docs/providers/novita.md`)
**Last Updated**: 2026-06-22
**Status**: Active
