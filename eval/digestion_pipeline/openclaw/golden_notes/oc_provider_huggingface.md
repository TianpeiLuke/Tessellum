---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - huggingface
keywords:
  - openclaw huggingface provider
  - hugging face inference providers router
  - hf_token huggingface_hub_token
  - huggingface model ids hub-style
  - fastest cheapest policy suffixes
  - model discovery v1 models
  - deepseek-r1 default model
  - fallback alias config
topics:
  - OpenClaw
  - Hugging Face Inference Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/huggingface
access_control_group: ["general"]
---

# OpenClaw — Configuring the Hugging Face Inference Provider

## Overview

This note is the configuration procedure for the OpenClaw **Hugging Face (inference)** provider, mirroring the `providers/huggingface` source page. Hugging Face Inference Providers offer OpenAI-compatible chat completions through a single router API, giving access to many models (DeepSeek, Llama, and more) with one token. It covers the provider's identity card (`provider: huggingface`, fine-grained `HUGGINGFACE_HUB_TOKEN`/`HF_TOKEN` auth, the OpenAI-compatible `https://router.huggingface.co/v1` API, single-token billing), the interactive and non-interactive onboarding steps, the Hub-style `huggingface/<org>/<model>` model-ref form with `:fastest`/`:cheapest` policy suffixes, and the advanced configuration: dynamic model discovery via GET `/v1/models`, name/alias hydration, the env-var precedence rule, and the fallback/alias config examples. OpenClaw uses only the OpenAI-compatible endpoint (chat completions only); for text-to-image, embeddings, or speech the source directs you to the HF inference clients directly.

## Provider identity

The page's front matter defines the provider card you configure against:

- **Provider:** `huggingface`
- **Auth:** `HUGGINGFACE_HUB_TOKEN` or `HF_TOKEN` (a fine-grained token with the **Make calls to Inference Providers** permission).
- **API:** OpenAI-compatible (`https://router.huggingface.co/v1`).
- **Billing:** A single HF token; pricing follows provider rates with a free tier.

A single HF token routes to many upstream inference providers behind one router API, so model access and billing are unified under that one credential.

## Getting started

The interactive setup is a four-step flow:

1. **Create a fine-grained token** at Hugging Face Settings → Tokens and create a new fine-grained token. The token **must** have the **Make calls to Inference Providers** permission enabled, or API requests will be rejected.
2. **Run onboarding** — choose **Hugging Face** in the provider dropdown, then enter your API key when prompted, or run it directly:

```bash
openclaw onboard --auth-choice huggingface-api-key
```

3. **Select a default model** — in the **Default Hugging Face model** dropdown, pick the model you want. The list is loaded from the Inference API when you have a valid token; otherwise a built-in list is shown. Your choice is saved as the default model. You can also set or change the default model later in config:

```json5
{
  agents: {
    defaults: {
      model: { primary: "huggingface/deepseek-ai/DeepSeek-R1" },
    },
  },
}
```

4. **Verify the model is available** — list the provider's resolved models:

```bash
openclaw models list --provider huggingface
```

### Non-interactive setup

For scripted/headless installs, run onboarding non-interactively. This sets `huggingface/deepseek-ai/DeepSeek-R1` as the default model:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice huggingface-api-key \
  --huggingface-api-key "$HF_TOKEN"
```

## Model IDs

Model refs use the form `huggingface/<org>/<model>` (Hub-style IDs). The list below is from **GET** `https://router.huggingface.co/v1/models`; your catalog may include more.

| Model | Ref (prefix with `huggingface/`) |
| --- | --- |
| DeepSeek R1 | `deepseek-ai/DeepSeek-R1` |
| DeepSeek V3.2 | `deepseek-ai/DeepSeek-V3.2` |
| Qwen3 8B | `Qwen/Qwen3-8B` |
| Qwen2.5 7B Instruct | `Qwen/Qwen2.5-7B-Instruct` |
| Qwen3 32B | `Qwen/Qwen3-32B` |
| Llama 3.3 70B Instruct | `meta-llama/Llama-3.3-70B-Instruct` |
| Llama 3.1 8B Instruct | `meta-llama/Llama-3.1-8B-Instruct` |
| GPT-OSS 120B | `openai/gpt-oss-120b` |
| GLM 4.7 | `zai-org/GLM-4.7` |
| Kimi K2.5 | `moonshotai/Kimi-K2.5` |

You can append `:fastest` or `:cheapest` to any model id. You set your default provider order in the Inference Provider settings on Hugging Face; the page points to the Inference Providers docs and **GET** `https://router.huggingface.co/v1/models` for the full list.

## Advanced configuration

### Model discovery and onboarding dropdown

OpenClaw discovers models by calling the Inference endpoint directly with `GET https://router.huggingface.co/v1/models`. Optionally send `Authorization: Bearer $HUGGINGFACE_HUB_TOKEN` or `$HF_TOKEN` for the full list — some endpoints return a subset without auth. The response is OpenAI-style `{ "object": "list", "data": [ { "id": "Qwen/Qwen3-8B", "owned_by": "Qwen", ... }, ... ] }`. When you configure a Hugging Face API key (via onboarding, `HUGGINGFACE_HUB_TOKEN`, or `HF_TOKEN`), OpenClaw uses this GET to discover available chat-completion models. During interactive setup, after you enter your token you see a **Default Hugging Face model** dropdown populated from that list (or the built-in catalog if the request fails). At runtime (e.g. Gateway startup), when a key is present, OpenClaw again calls **GET** `https://router.huggingface.co/v1/models` to refresh the catalog. The list is merged with a built-in catalog (for metadata like context window and cost). If the request fails or no key is set, only the built-in catalog is used.

### Model names, aliases, and policy suffixes

The display name is **hydrated from GET /v1/models** when the API returns `name`, `title`, or `display_name`; otherwise it is derived from the model id (e.g. `deepseek-ai/DeepSeek-R1` becomes "DeepSeek R1"). You can override the display name per model in config so it appears the way you want in the CLI and UI:

```json5
{
  agents: {
    defaults: {
      models: {
        "huggingface/deepseek-ai/DeepSeek-R1": { alias: "DeepSeek R1 (fast)" },
        "huggingface/deepseek-ai/DeepSeek-R1:cheapest": { alias: "DeepSeek R1 (cheap)" },
      },
    },
  },
}
```

OpenClaw's bundled Hugging Face docs and helpers currently treat two suffixes as the built-in **policy variants**: **`:fastest`** (highest throughput) and **`:cheapest`** (lowest cost per output token). You can add these as separate entries in `models.providers.huggingface.models` or set `model.primary` with the suffix; you can also set your default provider order in the Inference Provider settings (no suffix = use that order). On **config merge**, existing entries in `models.providers.huggingface.models` (e.g. in `models.json`) are kept, so any custom `name`, `alias`, or model options you set there are preserved.

### Environment and daemon setup

If the Gateway runs as a daemon (launchd/systemd), make sure `HUGGINGFACE_HUB_TOKEN` or `HF_TOKEN` is available to that process (for example, in `~/.openclaw/.env` or via `env.shellEnv`). OpenClaw accepts both `HUGGINGFACE_HUB_TOKEN` and `HF_TOKEN` as env var aliases — either one works, and **if both are set, `HUGGINGFACE_HUB_TOKEN` takes precedence**.

### Fallback and alias config examples

The page provides several `agents.defaults.model` examples combining a `primary`, a `fallbacks` ladder, and per-model `alias` overrides (and policy suffixes). A representative example pins DeepSeek R1 as primary with a Qwen fallback and aliases for both:

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "huggingface/deepseek-ai/DeepSeek-R1",
        fallbacks: ["huggingface/Qwen/Qwen3-8B"],
      },
      models: {
        "huggingface/deepseek-ai/DeepSeek-R1": { alias: "DeepSeek R1" },
        "huggingface/Qwen/Qwen3-8B": { alias: "Qwen3 8B" },
      },
    },
  },
}
```

The source also documents the same shape for: a Qwen primary with `:cheapest`/`:fastest` variant aliases; a DeepSeek V3.2 primary with Llama 3.3 70B and GPT-OSS 120B fallbacks; and a multi-model Qwen + DeepSeek + Llama set using `:cheapest`/`:fastest` policy suffixes — all variations of the same `model.primary` + `fallbacks` + `models` alias-map task.

**Source**: OpenClaw documentation — `providers/huggingface` (mirror `inbox/openclaw_docs/providers/huggingface.md`)
**Last Updated**: 2026-06-22
**Status**: Active
