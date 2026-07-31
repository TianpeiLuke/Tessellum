---
tags:
  - resource
  - documentation
  - hermes_agent
  - inference_providers
  - google_gemini
keywords:
  - google gemini native provider
  - generateContent api translation
  - GOOGLE_API_KEY GEMINI_API_KEY
  - google-gemini-cli oauth provider
  - gemini model aliases gemma
  - hermes doctor gquota diagnostics
topics:
  - Hermes Agent
  - Inference Providers
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/google-gemini
access_control_group: ["general"]
---

# Hermes Agent — Google Gemini Provider Setup

## Overview

This note is the **Google Gemini provider setup task script** for Hermes Agent — connecting Hermes to Google's **AI Studio / Gemini API as a native provider**, not the OpenAI-compatible endpoint. Hermes translates its internal OpenAI-shaped message and tool loop into Gemini's native `generateContent` API while preserving tool calling, streaming, multimodal inputs, and Gemini-specific response metadata. Two distinct providers exist: the API-key provider (`gemini`, the lowest-risk official API path) and a separate `google-gemini-cli` OAuth provider that uses the same Cloud Code Assist backend as Google's Gemini CLI. This guide is the step-by-step procedure — API-key vs OAuth setup, the native-endpoint translation, model aliases + Gemma access, mid-session `/model` switching, `hermes doctor` diagnostics, gateway use, and the common 404/429/schema troubleshooting. The provider's place in the broader catalog is owned by [Cloud & First-Class Inference Providers](hermes_inference_providers_cloud.md); the `config.yaml` model/provider surface is owned by the configuring-models doc.

## Prerequisites

- **Google AI Studio API key** — create one at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
- **Billing-enabled Google Cloud project** — recommended for agent use. Gemini's free tier is too small for long-running agent sessions because Hermes may make several model calls per user turn.
- **Hermes installed** — no extra Python package is required for the native Gemini provider.

Set `GOOGLE_API_KEY` or `GEMINI_API_KEY`; Hermes checks both names for the `gemini` provider.

## Quick Start

```bash
# Add your Gemini API key
echo "GOOGLE_API_KEY=..." >> ~/.hermes/.env

# Select Gemini as your provider
hermes model
# → Choose "More providers..." → "Google AI Studio"
# → Hermes checks your key tier and shows Gemini models
# → Select a model

# Start chatting
hermes chat
```

## Configuration

After running `hermes model`, your `~/.hermes/config.yaml` will contain the native Gemini API base URL, and `~/.hermes/.env` will hold `GOOGLE_API_KEY=...`:

```yaml
model:
  default: gemini-3-flash-preview
  provider: gemini
  base_url: https://generativelanguage.googleapis.com/v1beta
```

### Native Gemini API

The recommended endpoint is `https://generativelanguage.googleapis.com/v1beta`. Hermes detects this endpoint and creates its native Gemini adapter. Internally, Hermes still keeps the agent loop in OpenAI-shaped messages, then translates each request to Gemini's native schema:

- `messages[]` → Gemini `contents[]`
- system prompts → Gemini `systemInstruction`
- tool schemas → Gemini `functionDeclarations`
- tool results → Gemini `functionResponse` parts
- streaming responses → OpenAI-shaped stream chunks for the Hermes loop

For **Gemini 3** tool use, Hermes preserves the `thoughtSignature` values attached to function-call parts and replays them on the next tool turn (the validation-critical path for multi-step agent workflows). Gemini 3 may also attach thought signatures to other response parts; the native adapter is optimized for agent tool loops today and does not yet replay every non-tool-call signature with full part-level fidelity.

### Prefer the Native Endpoint

Google also exposes an OpenAI-compatible endpoint (`.../v1beta/openai/`). For Hermes agent sessions, prefer the native Gemini endpoint so Hermes can map multi-turn tool use, tool-call results, streaming, multimodal inputs, and Gemini response metadata directly onto `generateContent`. The OpenAI-compatible endpoint remains useful when you specifically need OpenAI API compatibility. If you previously set `GEMINI_BASE_URL` to the `/openai` URL, remove it or change it back to the native `v1beta` URL.

### OAuth Provider

Hermes also has a `google-gemini-cli` provider, selected via `hermes model` → "Google Gemini (OAuth)". This uses browser PKCE login and the Cloud Code Assist backend, useful for users who want Gemini CLI-style OAuth. Hermes shows an explicit warning because Google may treat use of the Gemini CLI OAuth client from third-party software as a policy violation. For production or lowest-risk usage, prefer the API-key provider (`gemini` with `GOOGLE_API_KEY`).

## Available Models

The `hermes model` picker shows Gemini models maintained in Hermes' provider registry. Common choices: `gemini-3.1-pro-preview` (most capable preview when available), `gemini-3-pro-preview` (strong reasoning/coding), `gemini-3-flash-preview` (recommended default balance), and `gemini-3.1-flash-lite-preview` (fastest / lowest cost when available). Model availability changes over time — if a model disappears or is not enabled for your key, run `hermes model` again. Use Gemini's native model IDs (e.g. `gemini-3-flash-preview`), not OpenRouter-style IDs (`google/gemini-3-flash-preview`), when `provider: gemini`.

### Latest Aliases

Google publishes moving aliases for the Pro and Flash families: `gemini-pro-latest` (tracks the latest Gemini Pro) and `gemini-flash-latest` (tracks the latest Gemini Flash). They are useful when you want Google to advance the model automatically without changing your Hermes config:

```yaml
model:
  default: gemini-pro-latest
  provider: gemini
  base_url: https://generativelanguage.googleapis.com/v1beta
```

If you need strict reproducibility, prefer explicit model IDs such as `gemini-3.1-pro-preview` or `gemini-3-flash-preview`.

### Gemma via the Gemini API

Google also exposes Gemma models through the Gemini API. Hermes recognizes these as Google models but hides very low-throughput Gemma entries from the default picker so new users do not accidentally select an evaluation-tier model for a long-running session. Useful evaluation IDs include `gemma-4-31b-it` (larger Gemma model, compatibility/quality evaluation) and `gemma-4-26b-a4b-it` (smaller active-parameter variant when available). Gemma API pricing is free-tier-only with low usage caps, so sustained agent use should move to a paid Gemini model, a self-hosted deployment, or another provider. To use a Gemma model hidden from the picker, set it directly in `config.yaml` with `default: gemma-4-31b-it` and `provider: gemini`.

## Switching Models Mid-Session

Use the `/model` command during a conversation:

```text
/model gemini-3-flash-preview
/model gemini-flash-latest
/model gemini-3-pro-preview
/model gemini-pro-latest
/model gemma-4-31b-it
/model gemini-3.1-flash-lite-preview
```

If you have not configured Gemini yet, exit the session and run `hermes model` first. `/model` switches among already-configured providers and models; it does not collect new API keys.

## Diagnostics

```bash
hermes doctor
```

The doctor checks whether `GOOGLE_API_KEY` or `GEMINI_API_KEY` is available, whether Gemini OAuth credentials exist for `google-gemini-cli`, and whether configured provider credentials can be resolved. For OAuth quota usage, run `/gquota` inside a Hermes session — it applies to the `google-gemini-cli` OAuth provider, not the AI Studio API-key provider.

## Gateway (Messaging Platforms)

Gemini works with all Hermes gateway platforms (Telegram, Discord, Slack, WhatsApp, LINE, Feishu, etc.). Configure Gemini as your provider, then start the gateway normally with `hermes gateway setup` followed by `hermes gateway start`. The gateway reads `config.yaml` and uses the same Gemini provider configuration.

## Troubleshooting

- **"Gemini native client requires an API key"** — Hermes could not find a usable key. Add `GOOGLE_API_KEY=...` or `GEMINI_API_KEY=...` to `~/.hermes/.env`, then run `hermes model` again.
- **"This Google API key is on the free tier"** — Hermes probes keys during setup; free-tier quotas can be exhausted after a handful of agent turns (tool use, retries, compression, auxiliary tasks each cost calls). Enable billing on the Google Cloud project attached to the key, regenerate if needed, then run `hermes model`.
- **"404 model not found"** — the selected model is not available for your account, region, or key. Run `hermes model` again and pick another Gemini model from the current list.
- **Gemma model is not shown in `hermes model`** — Hermes hides low-throughput Gemma models by default; to evaluate one, set the model ID directly in `~/.hermes/config.yaml`.
- **"429 quota exceeded" on Gemma** — Gemma's Gemini-API free-tier caps are low; use for compatibility testing, then switch to a paid Gemini model or another provider for sustained sessions.
- **OpenAI-compatible endpoint is configured** — check `~/.hermes/.env` for a `GEMINI_BASE_URL` ending in `/openai/`; change it to the native `v1beta` endpoint or remove the override.
- **OAuth login warning** — the `google-gemini-cli` provider uses a Gemini CLI / Cloud Code Assist OAuth flow distinct from the official AI Studio API-key path; use `provider: gemini` with `GOOGLE_API_KEY` for the official integration.
- **Tool calling fails with schema errors** — upgrade Hermes and rerun `hermes model`; the native Gemini adapter sanitizes tool schemas for Gemini's stricter function-declaration format, which older builds or custom endpoints may not.

**Source**: `inbox/hermes_agent_docs/guides/google-gemini.md` · https://hermes-agent.nousresearch.com/docs/guides/google-gemini
**Last Updated**: 2026-06-19
**Status**: Active
