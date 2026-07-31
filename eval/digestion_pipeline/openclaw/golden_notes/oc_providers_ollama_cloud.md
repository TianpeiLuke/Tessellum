---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - ollama
keywords:
  - ollama cloud provider
  - ollama-cloud provider id
  - OLLAMA_API_KEY cloud key
  - hosted ollama models openclaw
  - ollama native /api/chat
  - cloud-only model routing
  - ollama.com base url
  - ollama cloud catalog discovery
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/ollama-cloud
access_control_group: ["general"]
---

# OpenClaw — Configuring the Ollama Cloud Provider (`ollama-cloud`)

## Overview

This note is the procedure for wiring OpenClaw to **Ollama Cloud** — Ollama's hosted model API — through the dedicated `ollama-cloud` provider id, mirroring the `providers/ollama-cloud` source page. It covers creating and exporting the cloud API key, the fixed provider defaults (`https://ollama.com` base URL, native `/api/chat` style), choosing between the cloud-only `ollama-cloud` provider and the local/hybrid `ollama` provider, discovering hosted models from the live catalog, running the cloud live smoke test, and the three documented troubleshooting cases. Ollama Cloud lets OpenClaw call Ollama-hosted models directly, without installing a local Ollama server or signing a local Ollama app into cloud mode; OpenClaw registers it as a **separate provider id** so cloud-only credentials, live catalog discovery, and model selection are not mixed with a local `ollama` host. For local Ollama, hybrid cloud-plus-local routing, embeddings, and custom host details, use the [Ollama](oc_providers_ollama_setup.md) provider instead.

## Setup

Create an Ollama Cloud API key at `ollama.com/settings/keys`, then onboard the provider with the dedicated auth choice:

```bash
openclaw onboard --auth-choice ollama-cloud
```

Or set the key directly as an environment variable:

```bash
export OLLAMA_API_KEY="<your-ollama-cloud-api-key>" # pragma: allowlist secret
```

The `OLLAMA_API_KEY` here must be a **real cloud API key**. This differs from the local Ollama provider, where a local or private host can use the `ollama-local` marker instead of a real key (see the [Ollama setup](oc_providers_ollama_setup.md) provider).

## Defaults

The `ollama-cloud` provider ships with these fixed defaults (verbatim from source):

- **Provider:** `ollama-cloud`
- **Base URL:** `https://ollama.com`
- **Env var:** `OLLAMA_API_KEY`
- **API style:** Ollama native `/api/chat`
- **Example model:** `ollama-cloud/kimi-k2.6`

The native `/api/chat` style — not the OpenAI-compatible `/v1` route — is what distinguishes Ollama routes and preserves native tool calling. Model refs follow the `ollama-cloud/<model>` form, e.g. `ollama-cloud/kimi-k2.6`.

## When to Choose Ollama Cloud

Pick the `ollama-cloud` provider when:

- You want hosted Ollama models without running `ollama serve` locally.
- You want the same native Ollama chat API shape OpenClaw uses for local Ollama, but pointed at `https://ollama.com`.
- You want a simple cloud path for models that are already in Ollama's hosted catalog.
- You do not need local model pulls, local GPU control, or LAN-only inference.

Use the [Ollama](oc_providers_ollama_setup.md) provider instead when you want local-only or cloud-plus-local routing through a signed-in Ollama host. Use an OpenAI-compatible provider (e.g. [OpenRouter](oc_providers_openrouter.md)) instead when you need `/v1/chat/completions` semantics or provider-specific OpenAI-style features.

## Models

OpenClaw discovers Ollama Cloud models from the **live hosted catalog**. Commonly available hosted ids include:

- `ollama-cloud/gpt-oss:20b`
- `ollama-cloud/kimi-k2.6`
- `ollama-cloud/deepseek-v4-flash`
- `ollama-cloud/minimax-m2.7`
- `ollama-cloud/glm-5`

List the current catalog and select a model id from it:

```bash
openclaw models list --provider ollama-cloud
openclaw models set ollama-cloud/kimi-k2.6
```

Model ids are **cloud catalog ids, not local pull names**. If a model name works in a local Ollama host but is absent from the hosted catalog, use the `ollama` provider with that local host instead.

## Live Test

For Ollama Cloud API-key smoke tests, point the shared Ollama live test at the hosted endpoint and choose a model from your current catalog:

```bash
export OLLAMA_API_KEY="<your-ollama-cloud-api-key>" # pragma: allowlist secret

OPENCLAW_LIVE_TEST=1 \
OPENCLAW_LIVE_OLLAMA=1 \
OPENCLAW_LIVE_OLLAMA_BASE_URL=https://ollama.com \
OPENCLAW_LIVE_OLLAMA_MODEL=kimi-k2.6 \
OPENCLAW_LIVE_OLLAMA_WEB_SEARCH=1 \
pnpm test:live -- extensions/ollama/ollama.live.test.ts
```

The cloud smoke runs text, native stream, and web search. It **skips embeddings by default** for `https://ollama.com` because Ollama Cloud API keys may not authorize `/api/embed`.

## Troubleshooting

- **`Set OLLAMA_API_KEY` errors:** provide a real cloud API key. The local `ollama-local` marker is only for local or private Ollama hosts.
- **Unknown model errors:** run `openclaw models list --provider ollama-cloud` and copy the hosted model id exactly.
- **Tool-call or raw JSON issues on custom Ollama hosts:** check whether you are accidentally using an OpenAI-compatible `/v1` URL. Ollama routes should use the native base URL with no `/v1` suffix.

**Source**: OpenClaw documentation — `providers/ollama-cloud` (mirror `inbox/openclaw_docs/providers/ollama-cloud.md`)
**Last Updated**: 2026-06-22
**Status**: Active
