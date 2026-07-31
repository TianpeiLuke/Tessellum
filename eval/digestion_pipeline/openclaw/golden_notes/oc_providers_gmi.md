---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - gmi
keywords:
  - openclaw gmi cloud provider
  - gmi-provider plugin install
  - gmi multi-vendor route catalog
  - GMI_API_KEY auth
  - openai-compatible aggregator
  - gmi fallback provider
  - models list --provider gmi
topics:
  - OpenClaw
  - GMI Cloud Provider
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/gmi
access_control_group: ["general"]
---

# OpenClaw — Configure the GMI Cloud Provider

## Overview

This note is the setup procedure for wiring **GMI Cloud** into OpenClaw as a hosted, multi-vendor, OpenAI-compatible model provider, mirroring the `providers/gmi` source page. GMI Cloud is a hosted inference platform for frontier and open-weight models behind an OpenAI-compatible API; in OpenClaw it is an **official external provider plugin**, so you install it once, select it with the provider id `gmi`, store credentials through normal model auth, and use model refs like `gmi/google/gemini-3.1-flash-lite`. The note covers installing `@openclaw/gmi-provider`, the `GMI_API_KEY` / `onboard --auth-choice gmi-api-key` auth path, the provider defaults (id, aliases, base URL, default model), when to choose GMI as a fallback aggregator versus a direct vendor or local provider, the seeded multi-vendor route catalog, and the documented troubleshooting cases.

GMI ownership boundary (verbatim from source): this provider uses OpenAI-compatible chat semantics; **OpenClaw owns** the provider id, auth profile, aliases, model catalog seed, and base URL, while **GMI owns** the live model availability, billing, rate limits, and any provider-side routing policy.

## Setup

Install the plugin, restart the gateway, then create an API key in GMI Cloud:

```bash
openclaw plugins install @openclaw/gmi-provider
openclaw gateway restart
```

Then run onboarding to store the key in the provider auth profile:

```bash
openclaw onboard --auth-choice gmi-api-key
```

Or set the key as an environment variable for the process running OpenClaw:

```bash
export GMI_API_KEY="<your-gmi-api-key>" # pragma: allowlist secret
```

## Defaults

The plugin registers the following defaults (copied verbatim from the source page):

- **Provider:** `gmi`
- **Aliases:** `gmi-cloud`, `gmicloud`
- **Base URL:** `https://api.gmi-serving.com/v1`
- **Env var:** `GMI_API_KEY`
- **Default model:** `gmi/google/gemini-3.1-flash-lite`

## When to choose GMI

Per the source, choose GMI when:

- You want a hosted OpenAI-compatible endpoint rather than a local model server.
- You want to try several commercial and open-weight model families through one provider account.
- You want a fallback provider with different upstream routing from OpenRouter, DeepInfra, Together, or the direct vendor APIs.
- You need GMI-specific model ids, pricing, or account controls.

GMI is positioned as a secondary provider for model fallback, for comparing hosted routes across vendors, or for when GMI has a model available before your primary provider does — it exposes Google, Anthropic, OpenAI, DeepSeek, Moonshot, and Z.AI routes through its catalog under one API key. Choose the **direct vendor provider** instead when you need vendor-native features that GMI does not expose through its OpenAI-compatible route. Choose a **local provider** such as Ollama, LM Studio, vLLM, or SGLang when data locality or local GPU control matters more than hosted convenience.

## Models

The plugin catalog seeds commonly available GMI Cloud route ids, including:

- `gmi/zai-org/GLM-5.1-FP8`
- `gmi/deepseek-ai/DeepSeek-V3.2`
- `gmi/moonshotai/Kimi-K2.5`
- `gmi/google/gemini-3.1-flash-lite`
- `gmi/anthropic/claude-sonnet-4.6`
- `gmi/openai/gpt-5.4`

The catalog is a **seed, not a promise** that every account can call every model at all times. Use OpenClaw's model listing command to see what the configured provider actually reports in your environment:

```bash
openclaw models list --provider gmi
```

## Troubleshooting

The source page documents three failure cases:

- **`401` or `403`:** check that `GMI_API_KEY` is set for the process running OpenClaw, or re-run onboarding to store the key in the provider auth profile.
- **Unknown model errors:** confirm the model exists in your GMI account and use the full `gmi/<route-id>` ref shown by `openclaw models list --provider gmi`.
- **Intermittent provider errors:** try a different GMI route or configure GMI as a fallback rather than the only primary model provider.

**Source**: OpenClaw documentation — `providers/gmi` (mirror `inbox/openclaw_docs/providers/gmi.md`)
**Last Updated**: 2026-06-22
**Status**: Active
