---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - model_quickstart
keywords:
  - openclaw model provider quickstart
  - provider/model default model
  - openclaw onboard authenticate provider
  - agents.defaults.model.primary
  - supported providers starter set
  - anthropic-vertex copilot-proxy google-gemini-cli
  - openclaw models auth login
  - llm provider catalog index
topics:
  - OpenClaw
  - Model Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/models
access_control_group: ["general"]
---

# OpenClaw — Model Provider Quickstart and Index

## Overview

This note is the model-provider quickstart and index for OpenClaw, mirroring the `providers/models` source page. It documents the two-step "authenticate, then set `provider/model`" flow every provider shares, the starter-set catalog of supported LLM providers (each linking to its own per-provider setup page), and the additional provider variants (`anthropic-vertex`, `copilot-proxy`, `google-gemini-cli`) that onboard differently from the starter set. OpenClaw can use many LLM providers; you pick one, authenticate, then set the default model as `provider/model`. This page is an index — the per-provider config blocks (baseUrl / apiKey / api / models) live in the individual provider notes it links out to.

## Quick start (two steps)

Configuring a model provider is two steps:

1. **Authenticate with the provider** — usually via `openclaw onboard`.
2. **Set the default model** — express it as `provider/model` under `agents.defaults.model.primary`:

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

The model reference is always `provider/model` (here provider `anthropic`, model `claude-opus-4-6`). After authenticating once and setting this default, OpenClaw routes agent runs to that provider/model pair. Per-provider authentication details, base URLs, and the model catalog for each vendor live on the individual provider pages linked below.

## Supported providers (starter set)

The starter set of supported providers on this page (each entry links to its per-provider page, except BytePlus which links into the model-providers concept page):

- Alibaba Model Studio — `/providers/alibaba`
- Amazon Bedrock — `/providers/bedrock`
- Anthropic (API + Claude CLI) — `/providers/anthropic`
- BytePlus (International) — `/concepts/model-providers#byteplus-international`
- Chutes — `/providers/chutes`
- Cohere — `/providers/cohere`
- ComfyUI — `/providers/comfy`
- Cloudflare AI Gateway — `/providers/cloudflare-ai-gateway`
- DeepInfra — `/providers/deepinfra`
- fal — `/providers/fal`
- Fireworks — `/providers/fireworks`
- MiniMax — `/providers/minimax`
- Mistral — `/providers/mistral`
- Moonshot AI (Kimi + Kimi Coding) — `/providers/moonshot`
- OpenAI (API + Codex) — `/providers/openai`
- OpenCode (Zen + Go) — `/providers/opencode`
- OpenRouter — `/providers/openrouter`
- Qianfan — `/providers/qianfan`
- Qwen — `/providers/qwen`
- Runway — `/providers/runway`
- StepFun — `/providers/stepfun`
- Synthetic — `/providers/synthetic`
- Vercel AI Gateway — `/providers/vercel-ai-gateway`
- Venice (Venice AI) — `/providers/venice`
- xAI — `/providers/xai`
- Z.AI (GLM) — `/providers/zai`

For the full provider catalog (xAI, Groq, Mistral, etc.) and advanced configuration, the page points to [Model providers](https://docs.openclaw.ai/concepts/model-providers). The starter set above is a curated subset; the concept page enumerates the complete catalog and provider-rule semantics.

## Additional provider variants

Beyond the starter set, the page documents three additional provider variants that onboard or install differently:

- **`anthropic-vertex`** — install `@openclaw/anthropic-vertex-provider` for implicit Anthropic-on-Google-Vertex support when Vertex credentials are available; **no separate onboarding auth choice** (it activates implicitly given Vertex credentials).
- **`copilot-proxy`** — a local VS Code Copilot Proxy bridge; onboard with `openclaw onboard --auth-choice copilot-proxy`.
- **`google-gemini-cli`** — an unofficial Gemini CLI OAuth flow. It requires a local `gemini` install (`brew install gemini-cli` or `npm install -g @google/gemini-cli`), defaults to model `google-gemini-cli/gemini-3-flash-preview`, and onboards with either `openclaw onboard --auth-choice google-gemini-cli` or `openclaw models auth login --provider google-gemini-cli --set-default`.

The page's Related section also links [Model selection](https://docs.openclaw.ai/concepts/model-providers), [Model failover](https://docs.openclaw.ai/concepts/model-failover), and the [Models CLI](https://docs.openclaw.ai/cli/models) for choosing, failing over between, and managing models from the command line.

**Source**: OpenClaw documentation — `providers/models` (mirror `inbox/openclaw_docs/providers/models.md`)
**Last Updated**: 2026-06-22
**Status**: Active
