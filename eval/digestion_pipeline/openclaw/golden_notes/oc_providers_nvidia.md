---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - nvidia
keywords:
  - openclaw nvidia provider
  - nvidia_api_key onboarding
  - nemotron 3 ultra default
  - openai-compatible nvidia base url
  - featured-models.json catalog
  - bundled fallback catalog
  - enable_thinking reasoning_budget
  - slow custom provider timeout
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/nvidia
access_control_group: ["general"]
---

# OpenClaw — Configuring the NVIDIA Free OpenAI-Compatible Provider

## Overview

This note is the operational procedure for connecting OpenClaw to NVIDIA's free OpenAI-compatible API, mirroring the `providers/nvidia` source page in full: getting started (API-key + onboarding + model-set), the JSON5 config example, the live featured-model catalog, the Nemotron 3 Ultra default, the bundled fallback catalog, and advanced configuration (auto-enable, catalog/pricing, OpenAI-compatible endpoint, Ultra reasoning params, slow custom-provider timeouts). NVIDIA exposes an OpenAI-compatible API at `https://integrate.api.nvidia.com/v1` serving open models for free, authenticated with an API key from build.nvidia.com; OpenClaw defaults the NVIDIA provider to Nemotron 3 Ultra (NVIDIA's 550B total / 55B active reasoning model for long-context agentic work).

## Getting Started

Three steps onboard the NVIDIA provider:

1. **Get your API key** — create an API key at `build.nvidia.com/settings/api-keys`.
2. **Export the key and run onboarding** — set the environment variable and onboard with the NVIDIA auth choice:

```bash
export NVIDIA_API_KEY="nvapi-..."
openclaw onboard --auth-choice nvidia-api-key
```

3. **Set an NVIDIA model** — select the default Ultra model ref (the leading `nvidia/` is the provider id, the rest is NVIDIA's own model id):

```bash
openclaw models set nvidia/nvidia/nemotron-3-ultra-550b-a55b
```

The source warns: if you pass `--nvidia-api-key` instead of the env var, the value lands in shell history and `ps` output — prefer the `NVIDIA_API_KEY` environment variable when possible. For non-interactive setup you can pass the key directly:

```bash
openclaw onboard --auth-choice nvidia-api-key --nvidia-api-key "nvapi-..."
```

## Config Example

The minimal explicit config sets the env key, registers the `nvidia` provider against the OpenAI-compatible base URL with `api: "openai-completions"`, and pins the default agent model to the Ultra ref:

```json5
{
  env: { NVIDIA_API_KEY: "nvapi-..." },
  models: {
    providers: {
      nvidia: {
        baseUrl: "https://integrate.api.nvidia.com/v1",
        api: "openai-completions",
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "nvidia/nvidia/nemotron-3-ultra-550b-a55b" },
    },
  },
}
```

## Featured Catalog

When an NVIDIA API key is configured, OpenClaw setup and model-selection paths try NVIDIA's public featured-model catalog from `https://assets.ngc.nvidia.com/products/api-catalog/featured-models.json` and cache the ranked result for 24 hours. New featured models from build.nvidia.com therefore appear in setup and model-selection surfaces without waiting for an OpenClaw release. When the live feed is available, the first returned model is the default option shown during NVIDIA setup. The fetch uses a fixed HTTPS host policy for `assets.ngc.nvidia.com`. If no NVIDIA API key is configured, or if that public catalog is unavailable or malformed, OpenClaw falls back to the bundled catalog and bundled default described below.

## Nemotron 3 Ultra (Default Model)

Nemotron 3 Ultra is the default NVIDIA model in OpenClaw. NVIDIA's build page for `nvidia/nemotron-3-ultra-550b-a55b` lists it as an available free endpoint with a 1M-token context specification. The bundled catalog records a 16,384-token max output to match NVIDIA's current OpenAI-compatible sample request for the hosted endpoint. Use Ultra for the highest-capability NVIDIA default; keep Super selected when you want the smaller Nemotron 3 option, or choose one of the third-party models hosted in NVIDIA's catalog when their context, latency, or behavior fits better. The bundled Ultra row sends `chat_template_kwargs.enable_thinking: false` and `force_nonempty_content: true` by default so normal chat output stays in the visible answer instead of exposing reasoning text.

## Bundled Fallback Catalog

The bundled fallback catalog is the static model list OpenClaw uses when no key is set or the live featured feed is unavailable/malformed (it also retains deprecated shipped refs for upgrade compatibility):

| Model ref | Name | Context | Max output | Notes |
| --- | --- | --- | --- | --- |
| `nvidia/nvidia/nemotron-3-ultra-550b-a55b` | NVIDIA Nemotron 3 Ultra 550B | 1,000,000 | 16,384 | Default |
| `nvidia/nvidia/nemotron-3-super-120b-a12b` | NVIDIA Nemotron 3 Super 120B | 262,144 | 8,192 | Featured fallback |
| `nvidia/moonshotai/kimi-k2.5` | Kimi K2.5 | 262,144 | 8,192 | Featured fallback |
| `nvidia/minimaxai/minimax-m2.7` | Minimax M2.7 | 196,608 | 8,192 | Featured fallback |
| `nvidia/z-ai/glm-5.1` | GLM 5.1 | 202,752 | 8,192 | Featured fallback |
| `nvidia/minimaxai/minimax-m2.5` | MiniMax M2.5 | 196,608 | 8,192 | Deprecated, upgrade compatibility |
| `nvidia/z-ai/glm5` | GLM-5 | 202,752 | 8,192 | Deprecated, upgrade compatibility |

## Advanced Configuration

**Auto-enable behavior** — the provider auto-enables when the `NVIDIA_API_KEY` environment variable is set; no explicit provider config is required beyond the key.

**Catalog and pricing** — OpenClaw prefers NVIDIA's public featured-model catalog when NVIDIA auth is configured and caches it for 24 hours. The bundled fallback catalog is static and keeps deprecated shipped refs for upgrade compatibility. Costs default to `0` in source since NVIDIA currently offers free API access for the listed models.

**OpenAI-compatible endpoint** — NVIDIA uses the standard `/v1` completions endpoint. Any OpenAI-compatible tooling should work out of the box with the NVIDIA base URL.

**Nemotron 3 Ultra reasoning params** — NVIDIA's Ultra sample request uses `chat_template_kwargs.enable_thinking` and `reasoning_budget` for reasoning output. OpenClaw's bundled Ultra row disables template thinking by default for normal chat use. To opt into NVIDIA reasoning output or force other NVIDIA-specific request fields, set per-model params and keep provider-specific overrides scoped to the NVIDIA model:

```json5
{
  agents: {
    defaults: {
      models: {
        "nvidia/nvidia/nemotron-3-ultra-550b-a55b": {
          params: {
            chat_template_kwargs: { enable_thinking: true },
            extra_body: { reasoning_budget: 16384 },
          },
        },
      },
    },
  },
}
```

`params.extra_body` is the final OpenAI-compatible request-body override, so use it only for fields NVIDIA documents for the selected endpoint.

**Slow custom provider responses** — some NVIDIA-hosted custom models can take longer than the default model idle watchdog before they emit a first response chunk. For custom NVIDIA provider entries, raise the provider `timeoutSeconds` instead of raising the whole agent runtime timeout:

```json5
{
  models: {
    providers: {
      "custom-integrate-api-nvidia-com": {
        baseUrl: "https://integrate.api.nvidia.com/v1",
        api: "openai-completions",
        apiKey: "NVIDIA_API_KEY",
        timeoutSeconds: 300,
      },
    },
  },
  agents: {
    defaults: {
      models: {
        "custom-integrate-api-nvidia-com/meta/llama-3.1-70b-instruct": {
          params: { thinking: "off" },
        },
      },
    },
  },
}
```

NVIDIA models are currently free to use; check `build.nvidia.com` for the latest availability and rate-limit details.

**Source**: OpenClaw documentation — `providers/nvidia` (mirror `inbox/openclaw_docs/providers/nvidia.md`)
**Last Updated**: 2026-06-22
**Status**: Active
