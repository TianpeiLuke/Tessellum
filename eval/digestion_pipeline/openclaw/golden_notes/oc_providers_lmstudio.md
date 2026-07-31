---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - lmstudio
keywords:
  - openclaw lm studio provider
  - local open-weight model inference
  - lmstudio onboard auth-choice
  - models.providers.lmstudio config
  - llama.cpp gguf mlx
  - lm_api_token 401 troubleshooting
  - jit model loading preload
  - lan tailnet allowprivatenetwork
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/lmstudio
access_control_group: ["general"]
---

# OpenClaw — Run Local Open-Weight Models via LM Studio

## Overview

This note is the step-by-step procedure for running OpenClaw against local open-weight models served by **LM Studio** — the desktop GUI app or its headless daemon `llmster`, which runs llama.cpp (GGUF) or MLX (Apple Silicon) models on your own hardware. It mirrors the `providers/lmstudio` source page: installing and starting the local server, interactive and non-interactive onboarding, the `author/model-name` → `lmstudio/...` model-ref convention, the `models.providers.lmstudio` config block, OpenClaw's streaming-usage and reasoning-effort compatibility normalization, JIT/preload model lifecycle, LAN/tailnet host trust, and the not-detected / HTTP 401 troubleshooting paths.

## Quick Start

LM Studio is a friendly yet powerful app for running open-weight models on your own hardware; it runs llama.cpp (GGUF) or MLX models (Apple Silicon) and comes as a GUI package or the headless daemon `llmster`. Follow the source page's five-step quick start.

**1. Install LM Studio (desktop) or `llmster` (headless), then start the local server:**

```bash
curl -fsSL https://lmstudio.ai/install.sh | bash
```

**2. Start the server.** Make sure you either start the desktop app or run the daemon. The source shows the daemon command `lms daemon up` and the server-start command `lms server start --port 1234`. If you are using the app, make sure you have **JIT enabled** for a smooth experience (see the LM Studio JIT and TTL guide).

**3. Set `LM_API_TOKEN` if LM Studio authentication is enabled:**

```bash
export LM_API_TOKEN="your-lm-studio-api-token"
```

If LM Studio authentication is disabled, you can leave the API key blank during interactive OpenClaw setup.

**4. Run onboarding and choose `LM Studio`:** `openclaw onboard`.

**5. In onboarding, use the `Default model` prompt to pick your LM Studio model.** You can set or change it later with `openclaw models set lmstudio/qwen/qwen3.5-9b`.

LM Studio model keys follow an `author/model-name` format (e.g. `qwen/qwen3.5-9b`). OpenClaw model refs prepend the provider name: `lmstudio/qwen/qwen3.5-9b`. You can find the exact key for a model by running `curl http://localhost:1234/api/v1/models` and looking at the `key` field.

## Non-Interactive Onboarding

Use non-interactive onboarding when you want to script setup (CI, provisioning, remote bootstrap). The minimal form passes `--non-interactive`, `--accept-risk`, and `--auth-choice lmstudio`; you can additionally specify the base URL, model, and optional API key:

```bash
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --auth-choice lmstudio \
  --custom-base-url http://localhost:1234/v1 \
  --lmstudio-api-key "$LM_API_TOKEN" \
  --custom-model-id qwen/qwen3.5-9b
```

`--custom-model-id` takes the model key as returned by LM Studio (e.g. `qwen/qwen3.5-9b`), **without** the `lmstudio/` provider prefix. For authenticated LM Studio servers, pass `--lmstudio-api-key` or set `LM_API_TOKEN`; for unauthenticated servers, omit the key and OpenClaw stores a local non-secret marker. `--custom-api-key` remains supported for compatibility, but `--lmstudio-api-key` is preferred for LM Studio. This writes `models.providers.lmstudio` and sets the default model to `lmstudio/<custom-model-id>`; when you provide an API key, setup also writes the `lmstudio:default` auth profile.

Interactive setup can prompt for an optional **preferred load context length** and applies it across the discovered LM Studio models it saves into config. The LM Studio plugin config trusts the configured LM Studio endpoint for model requests, including loopback, LAN, and tailnet hosts; metadata/link-local origins still require explicit opt-in. You can opt out by setting `models.providers.lmstudio.request.allowPrivateNetwork: false`.

## Configuration

### Streaming usage compatibility

LM Studio is streaming-usage compatible. When it does not emit an OpenAI-shaped `usage` object, OpenClaw recovers token counts from llama.cpp-style `timings.prompt_n` / `timings.predicted_n` metadata instead. The same streaming-usage behavior applies to these other OpenAI-compatible local backends: **vLLM**, **SGLang**, **llama.cpp**, **LocalAI**, **Jan**, **TabbyAPI**, and **text-generation-webui**.

### Thinking compatibility

When LM Studio's `/api/v1/models` discovery reports model-specific reasoning options, OpenClaw exposes the matching OpenAI-compatible `reasoning_effort` values in model compat metadata. Current LM Studio builds can advertise binary UI options such as `allowed_options: ["off", "on"]` while rejecting those values on `/v1/chat/completions`; OpenClaw normalizes that binary discovery shape to `none`, `minimal`, `low`, `medium`, `high`, and `xhigh` before sending requests. Older saved LM Studio config that contains `off`/`on` reasoning maps is normalized the same way when the catalog is loaded.

### Explicit configuration

The canonical explicit provider block uses `api: "openai-completions"`, a `${LM_API_TOKEN}` apiKey, and a per-model entry carrying `reasoning`, `input`, a zero `cost` block, `contextWindow`, and `maxTokens`:

```json5
{
  models: {
    providers: {
      lmstudio: {
        baseUrl: "http://localhost:1234/v1",
        apiKey: "${LM_API_TOKEN}",
        api: "openai-completions",
        models: [
          {
            id: "qwen/qwen3-coder-next",
            name: "Qwen 3 Coder Next",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Troubleshooting

### LM Studio not detected

Make sure LM Studio is running. If authentication is enabled, also set `LM_API_TOKEN`. The source shows starting it headless via `lms server start --port 1234` (or via the desktop app), then verifying the API is accessible:

```bash
curl http://localhost:1234/api/v1/models
```

### Authentication errors (HTTP 401)

If setup reports HTTP 401, verify your API key: check that `LM_API_TOKEN` matches the key configured in LM Studio; for LM Studio auth setup details, see LM Studio Authentication; and if your server does not require authentication, leave the key blank during setup.

### Just-in-time model loading

LM Studio supports just-in-time (JIT) model loading, where models are loaded on first request. OpenClaw preloads models through LM Studio's native load endpoint by default, which helps when JIT is disabled. To let LM Studio's JIT, idle TTL, and auto-evict behavior own model lifecycle, disable OpenClaw's preload step with `params: { preload: false }` (paired with `baseUrl`, `api: "openai-completions"`, and a `models` entry such as `{ id: "qwen/qwen3.5-9b" }`).

### LAN or tailnet LM Studio host

Use the LM Studio host's reachable address, keep `/v1`, and make sure LM Studio is bound beyond loopback on that machine:

```json5
{
  models: {
    providers: {
      lmstudio: {
        baseUrl: "http://gpu-box.local:1234/v1",
        apiKey: "lmstudio",
        api: "openai-completions",
        models: [{ id: "qwen/qwen3.5-9b" }],
      },
    },
  },
}
```

`lmstudio` automatically trusts its configured local/private endpoint for guarded model requests. Custom/local OpenAI-compatible provider entries also trust their exact configured `baseUrl` origin, except metadata/link-local origins; requests to different private ports or destinations still require `models.providers.<id>.request.allowPrivateNetwork: true`. Set `models.providers.<id>.request.allowPrivateNetwork: false` to opt out of exact-origin trust.

**Source**: OpenClaw documentation — `providers/lmstudio` (mirror `inbox/openclaw_docs/providers/lmstudio.md`)
**Last Updated**: 2026-06-22
**Status**: Active
