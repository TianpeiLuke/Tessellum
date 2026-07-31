---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - litellm
keywords:
  - openclaw litellm provider
  - litellm proxy openclaw
  - litellm-api-key onboarding
  - models.providers.litellm config
  - litellm virtual keys spend limits
  - litellm model routing model_list
  - openai-completions api gateway
  - litellm cost tracking spend logs
  - allowprivatenetwork lan proxy
topics:
  - OpenClaw
  - Model Providers
  - LiteLLM
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/litellm
access_control_group: ["general"]
---

# OpenClaw — Routing Through a LiteLLM Proxy

## Overview

This note is the procedure for routing OpenClaw through a [LiteLLM](https://litellm.ai) proxy — an open-source LLM gateway exposing a unified API over 100+ model providers — to get centralized cost tracking, request/response logging, virtual keys with spend limits, model routing across backends (Claude, GPT-4, Gemini, Bedrock) without OpenClaw config changes, and automatic failover. It mirrors the `providers/litellm` source page: the two Quick start paths (onboarding vs manual), the `models.providers.litellm` configuration (env var + config file), and the Advanced configuration block (image generation, virtual keys, model routing, viewing usage, and the OpenAI-compat proxy-behavior caveats).

## Quick start

Two setup paths are offered. **Onboarding (recommended)** is the fastest path to a working LiteLLM setup; **Manual setup** gives full control over installation and config.

### Onboarding (recommended)

Run onboarding with the `litellm-api-key` auth choice. For non-interactive setup against a remote proxy, pass the proxy URL explicitly via `--custom-base-url` (and `--litellm-api-key`):

```bash
openclaw onboard --auth-choice litellm-api-key

# Non-interactive (remote proxy):
openclaw onboard --non-interactive --auth-choice litellm-api-key --litellm-api-key "$LITELLM_API_KEY" --custom-base-url "https://litellm.example/v1"
```

### Manual setup

First start the LiteLLM Proxy (the `[proxy]` extra installs the proxy server), then export the LiteLLM key and run OpenClaw — OpenClaw then routes through LiteLLM:

```bash
pip install 'litellm[proxy]'
litellm --model claude-opus-4-6

export LITELLM_API_KEY="your-litellm-key"
openclaw
```

## Configuration

### Environment variables

The proxy key is supplied via the `LITELLM_API_KEY` environment variable, e.g. `export LITELLM_API_KEY="sk-litellm-key"`.

### Config file

Define the provider under `models.providers.litellm` with `baseUrl`, `apiKey` (interpolating `${LITELLM_API_KEY}`), `api: "openai-completions"`, and a `models[]` catalog; set the agent's primary model to a `litellm/<id>` ref under `agents.defaults.model`:

```json5
{
  models: {
    providers: {
      litellm: {
        baseUrl: "http://localhost:4000",
        apiKey: "${LITELLM_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "claude-opus-4-6",
            name: "Claude Opus 4.6",
            reasoning: true,
            input: ["text", "image"],
            contextWindow: 200000,
            maxTokens: 64000,
          },
          {
            id: "gpt-4o",
            name: "GPT-4o",
            reasoning: false,
            input: ["text", "image"],
            contextWindow: 128000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "litellm/claude-opus-4-6" },
    },
  },
}
```

## Advanced configuration

### Image generation

LiteLLM can also back the `image_generate` tool through OpenAI-compatible `/images/generations` and `/images/edits` routes. Configure a LiteLLM image model under `agents.defaults.imageGenerationModel` (here `litellm/gpt-image-2` with a `timeoutMs` of `180_000`):

```json5
{
  models: {
    providers: {
      litellm: {
        baseUrl: "http://localhost:4000",
        apiKey: "${LITELLM_API_KEY}",
      },
    },
  },
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "litellm/gpt-image-2",
        timeoutMs: 180_000,
      },
    },
  },
}
```

Loopback LiteLLM URLs such as `http://localhost:4000` work without a global private-network override. For a LAN-hosted proxy, set `models.providers.litellm.request.allowPrivateNetwork: true` because the API key will be sent to the configured proxy host.

### Virtual keys

Create a dedicated key for OpenClaw with spend limits, then use the generated key as `LITELLM_API_KEY`:

```bash
curl -X POST "http://localhost:4000/key/generate" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "key_alias": "openclaw",
    "max_budget": 50.00,
    "budget_duration": "monthly"
  }'
```

### Model routing

LiteLLM can route model requests to different backends. Configure the route map in your LiteLLM `config.yaml` — OpenClaw keeps requesting `claude-opus-4-6` while LiteLLM handles the routing to the backend `litellm_params`:

```yaml
model_list:
  - model_name: claude-opus-4-6
    litellm_params:
      model: claude-opus-4-6
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: gpt-4o
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY
```

### Viewing usage

Check LiteLLM's dashboard or API for spend. Per the source, query the `GET http://localhost:4000/key/info` endpoint with `Authorization: Bearer sk-litellm-key` (the per-key value) for key info, and the `GET http://localhost:4000/spend/logs` endpoint with `Authorization: Bearer $LITELLM_MASTER_KEY` for spend logs.

### Proxy behavior notes

Because requests pass through LiteLLM's proxy-style OpenAI-compatible `/v1` endpoint rather than a native provider SDK, several OpenAI-only behaviors do not apply, per the source page:

- LiteLLM runs on `http://localhost:4000` by default.
- OpenClaw connects through LiteLLM's proxy-style OpenAI-compatible `/v1` endpoint.
- Native OpenAI-only request shaping does not apply through LiteLLM: no `service_tier`, no Responses `store`, no prompt-cache hints, and no OpenAI reasoning-compat payload shaping.
- Hidden OpenClaw attribution headers (`originator`, `version`, `User-Agent`) are not injected on custom LiteLLM base URLs.

For general provider configuration and failover behavior, see the Model Providers concept page (`/concepts/model-providers`).

**Source**: OpenClaw documentation — `providers/litellm` (mirror `inbox/openclaw_docs/providers/litellm.md`)
**Last Updated**: 2026-06-22
**Status**: Active
