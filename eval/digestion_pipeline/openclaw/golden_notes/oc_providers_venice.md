---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - venice
keywords:
  - openclaw venice provider
  - venice ai privacy modes
  - private vs anonymized inference
  - venice_api_key vapi_
  - venice onboard auth-choice
  - venice model catalog 41
  - deepseek v4 reasoning_content replay
  - venice openai-completions config
  - venice model discovery manifest
topics:
  - OpenClaw
  - Providers
  - Venice AI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/venice
access_control_group: ["general"]
---

# OpenClaw — Connecting the Venice AI Privacy Provider

## Overview

This note is the procedure for connecting OpenClaw to **Venice AI**, a privacy-focused inference provider that serves uncensored open-source models privately and proxies major proprietary models (Claude, GPT, Gemini, Grok) anonymized. It mirrors the `providers/venice` source page: the load-bearing **private-vs-anonymized privacy distinction**, `VENICE_API_KEY` (`vapi_` format) onboarding via `--auth-choice venice-api-key`, recommended-model selection, the DeepSeek V4 `reasoning_content` replay fix, manifest-backed model discovery, streaming/tool support, credit-based pricing, usage examples, troubleshooting, and the OpenAI-compatible `openai-completions` config block. All inference is private by default (no training on your data, no logging); the 41-model catalog is summarized to representative rows rather than reproduced in full.

## Why Venice in OpenClaw

Venice provides **privacy-focused AI inference** with support for uncensored models and access to major proprietary models through their anonymized proxy. The source lists four reasons to use it in OpenClaw: **private inference** for open-source models (no logging); **uncensored models** when you need them; **anonymized access** to proprietary models (Opus/GPT/Gemini) when quality matters; and OpenAI-compatible `/v1` endpoints.

## Privacy modes (load-bearing)

Venice offers two privacy levels, and understanding them is key to choosing a model. **Private** models are fully private — prompts/responses are never stored or logged and are ephemeral (Llama, Qwen, DeepSeek, Kimi, MiniMax, Venice Uncensored, etc.). **Anonymized** models are proxied through Venice with metadata stripped; the underlying provider (OpenAI, Anthropic, Google, xAI) sees anonymized requests (Claude, GPT, Gemini, Grok). The source carries an explicit **Warning**: anonymized models are NOT fully private — Venice strips metadata before forwarding, but the underlying provider still processes the request, so choose **Private** models when full privacy is required.

## Features

The page enumerates: **Privacy-focused** (choose between "private" fully-private and "anonymized" proxied modes); **Uncensored models** (access to models without content restrictions); **Major model access** (use Claude, GPT, Gemini, and Grok via Venice's anonymized proxy); **OpenAI-compatible API** (standard `/v1` endpoints); **Streaming** (supported on all models); **Function calling** (supported on select models — check model capabilities); **Vision** (supported on models with vision capability); and **No hard rate limits** (fair-use throttling may apply for extreme usage).

## Getting started

The source documents a three-step onboarding flow.

**Step 1 — Get your API key.** Sign up at venice.ai, go to **Settings > API Keys > Create new key**, and copy the API key (format: `vapi_xxxxxxxxxxxx`).

**Step 2 — Configure OpenClaw.** Pick one of three setup methods. Interactive (recommended) runs the onboarding wizard, which prompts for your API key (or uses an existing `VENICE_API_KEY`), shows all available Venice models, lets you pick a default model, and configures the provider automatically. The environment-variable method just exports the key. The non-interactive method passes the key on the command line:

```bash
# Interactive (recommended)
openclaw onboard --auth-choice venice-api-key

# Environment variable
export VENICE_API_KEY="vapi_xxxxxxxxxxxx"

# Non-interactive
openclaw onboard --non-interactive \
  --auth-choice venice-api-key \
  --venice-api-key "vapi_xxxxxxxxxxxx"
```

**Step 3 — Verify setup.** Run a quick agent turn against the default model: `openclaw agent --model venice/kimi-k2-5 --message "Hello, are you working?"`.

## Model selection

After setup OpenClaw shows all available Venice models. The source's defaults are: **default model** `venice/kimi-k2-5` (strong private reasoning plus vision); **high-capability option** `venice/claude-opus-4-6` (the strongest anonymized Venice path); choose **"private"** models for fully private inference and **"anonymized"** models to access Claude, GPT, Gemini via Venice's proxy. Change the default anytime with `openclaw models set venice/kimi-k2-5` or `openclaw models set venice/claude-opus-4-6`, and list everything with `openclaw models list --all --provider venice`. You can also run `openclaw configure`, select **Model/auth**, and choose **Venice AI**.

The page's use-case picker (verbatim recommendations): General chat (default) → `kimi-k2-5` (strong private reasoning plus vision); Best overall quality → `claude-opus-4-6` (strongest anonymized Venice option); Privacy + coding → `qwen3-coder-480b-a35b-instruct` (private coding model with large context); Private vision → `kimi-k2-5` (vision support without leaving private mode); Fast + cheap → `qwen3-4b` (lightweight reasoning model); Complex private tasks → `deepseek-v3.2` (strong reasoning, but no Venice tool support); Uncensored → `venice-uncensored` (no content restrictions).

## DeepSeek V4 replay behavior

If Venice exposes DeepSeek V4 models such as `venice/deepseek-v4-pro` or `venice/deepseek-v4-flash`, OpenClaw fills the required DeepSeek V4 `reasoning_content` replay placeholder on assistant messages when the proxy omits it. Venice rejects DeepSeek's native top-level `thinking` control, so OpenClaw keeps that provider-specific replay fix separate from the native DeepSeek provider's thinking controls.

## Built-in catalog (41 total: 26 private + 12 anonymized)

The page ships a built-in catalog of **41 models** split into **Private models (26)** — fully private, no logging — and **Anonymized models (12)** — via Venice proxy. The catalog is summarized here to representative rows (model ID · context · features); run `openclaw models list --all --provider venice` for the full, dynamically-updated list.

Representative **private** rows: `kimi-k2-5` (Kimi K2.5, 256k, Default/reasoning/vision); `qwen3-coder-480b-a35b-instruct` (Qwen3 Coder 480B, 256k, Coding); `qwen3-vl-235b-a22b` (Qwen3 VL 235B, 256k, Vision); `qwen3-4b` (Venice Small, 32k, Fast/reasoning); `deepseek-v3.2` (DeepSeek V3.2, 160k, Reasoning, tools disabled); `venice-uncensored` (Venice Uncensored / Dolphin-Mistral, 32k, Uncensored, tools disabled); `hermes-3-llama-3.1-405b` (128k, General, tools disabled); plus Llama 3.3 70B / 3.2 3B, the Qwen3 235B thinking/instruct/next-80b/3.5-35b family, `mistral-31-24b`, `google-gemma-3-27b-it`, `openai-gpt-oss-120b`, `nvidia-nemotron-3-nano-30b-a3b`, GLM 4.6/4.7/4.7-flash/5 (`zai-org-glm-*`, plus `olafangensan-glm-4.7-flash-heretic`), and MiniMax M2.1/M2.5.

Representative **anonymized** rows (all "via Venice"): `claude-opus-4-6` (Claude Opus 4.6, 1M, Reasoning/vision); `claude-sonnet-4-6` (1M, Reasoning/vision); `openai-gpt-54` (GPT-5.4, 1M, Reasoning/vision); `openai-gpt-53-codex` (GPT-5.3 Codex, 400k, Reasoning/vision/coding); `openai-gpt-52` / `openai-gpt-52-codex` (256k); `openai-gpt-4o-2024-11-20` / `openai-gpt-4o-mini-2024-07-18` (128k, Vision); `gemini-3-1-pro-preview` (1M), `gemini-3-pro-preview` (198k), `gemini-3-flash-preview` (256k); and `grok-41-fast` (Grok 4.1 Fast, 1M, Reasoning/vision). Anonymized Claude/GPT/Gemini/Grok models expose up to **1M context**.

## Model discovery

OpenClaw ships a **manifest-backed Venice seed catalog** for read-only model listing. Runtime refresh can still discover models from the Venice API, and falls back to the manifest catalog if the API is unreachable. The `/models` endpoint is public (no auth needed for listing), but inference requires a valid API key.

## Streaming and tool support

Per the source's support matrix: **Streaming** is supported on all models; **Function calling** on most models (check `supportsFunctionCalling` in the API); **Vision/Images** on models marked with the "Vision" feature; and **JSON mode** is supported via `response_format`.

## Pricing — Venice (anonymized) vs direct API

Venice uses a **credit-based system**; check venice.ai/pricing for current rates. Private models are generally lower cost; anonymized models are similar to direct API pricing plus a small Venice fee. The page contrasts Venice (anonymized) against the direct API: **Privacy** — metadata stripped/anonymized vs your account linked; **Latency** — +10-50ms (proxy) vs direct; **Features** — most features supported vs full features; **Billing** — Venice credits vs provider billing.

## Usage examples

The source provides representative agent invocations across the private/anonymized split and capabilities:

```bash
# Use the default private model
openclaw agent --model venice/kimi-k2-5 --message "Quick health check"

# Use Claude Opus via Venice (anonymized)
openclaw agent --model venice/claude-opus-4-6 --message "Summarize this task"

# Use uncensored model
openclaw agent --model venice/venice-uncensored --message "Draft options"

# Use vision model with image
openclaw agent --model venice/qwen3-vl-235b-a22b --message "Review attached image"

# Use coding model
openclaw agent --model venice/qwen3-coder-480b-a35b-instruct --message "Refactor this function"
```

## Troubleshooting

**API key not recognized** — check the key is exported and visible to the catalog with `echo $VENICE_API_KEY` and `openclaw models list | grep venice`; ensure the key starts with `vapi_`. **Model not available** — the Venice model catalog updates dynamically; run `openclaw models list` to see currently available models (some models may be temporarily offline). **Connection issues** — the Venice API is at `https://api.venice.ai/api/v1`; ensure your network allows HTTPS connections. For more help the page points to its Troubleshooting and FAQ guides.

## Advanced configuration

The config-file example uses `models.mode: "merge"` so Venice models add to (rather than replace) the existing catalog, and an `openai-completions` API surface pointing at the Venice `/v1` base URL with the key resolved from `${VENICE_API_KEY}`:

```json5
{
  env: { VENICE_API_KEY: "vapi_..." },
  agents: { defaults: { model: { primary: "venice/kimi-k2-5" } } },
  models: {
    mode: "merge",
    providers: {
      venice: {
        baseUrl: "https://api.venice.ai/api/v1",
        apiKey: "${VENICE_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "kimi-k2-5",
            name: "Kimi K2.5",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

**Source**: OpenClaw documentation — `providers/venice` (mirror `inbox/openclaw_docs/providers/venice.md`)
**Last Updated**: 2026-06-22
**Status**: Active
