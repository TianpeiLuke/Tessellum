---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - kilocode
keywords:
  - kilocode provider
  - kilo gateway openclaw
  - kilocode/kilo/auto
  - KILOCODE_API_KEY
  - openclaw unified api provider
  - openrouter-compatible proxy transport
  - dynamic model discovery static fallback
  - proxy reasoning caveat
topics:
  - OpenClaw
  - Provider configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/kilocode
access_control_group: ["general"]
---

# OpenClaw — Configuring the Kilo Gateway (`kilocode`) Provider

## Overview

This note is the configuration procedure for the OpenClaw **Kilo Gateway** provider (`kilocode`), mirroring the `providers/kilocode` source page. Kilo Gateway provides a **unified API** that routes requests to many models behind a single endpoint and API key; it is OpenAI-compatible, so most OpenAI SDKs work by switching the base URL. The note covers the provider property table (id / auth / API / base URL), installing the `@openclaw/kilocode-provider` plugin, the `KILOCODE_API_KEY` onboarding flow, the `kilocode/kilo/auto` smart-routing default model, dynamic model discovery merged ahead of a static fallback catalog, the JSON5 config example, and the advanced transport, stream-wrapper/reasoning, and troubleshooting accordions.

## Provider Properties

The source page documents Kilo Gateway with the following fixed properties:

| Property | Value |
| -------- | ---------------------------------- |
| Provider | `kilocode` |
| Auth     | `KILOCODE_API_KEY` |
| API      | OpenAI-compatible |
| Base URL | `https://api.kilo.ai/api/gateway/` |

The unified API routes requests to many models behind this single endpoint and API key, and because the API is OpenAI-compatible most OpenAI SDKs work simply by switching the base URL to `https://api.kilo.ai/api/gateway/`.

## Install Plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/kilocode-provider
openclaw gateway restart
```

## Getting Started

The source page walks through three onboarding steps. First, **create an account**: go to [app.kilo.ai](https://app.kilo.ai), sign in or create an account, then navigate to API Keys and generate a new key. Second, **run onboarding** with the Kilo auth choice, or set the environment variable directly:

```bash
openclaw onboard --auth-choice kilocode-api-key
# Or set the environment variable directly:
export KILOCODE_API_KEY="<your-kilocode-api-key>" # pragma: allowlist secret
```

Third, **verify the model is available** with `openclaw models list --provider kilocode`.

## Default Model

The default model is `kilocode/kilo/auto`, a provider-owned smart-routing model managed by Kilo Gateway. Per the source `Note` callout, OpenClaw treats `kilocode/kilo/auto` as the stable default ref but does **not** publish a source-backed task-to-upstream-model mapping for that route — the exact upstream routing behind `kilocode/kilo/auto` is owned by Kilo Gateway, not hard-coded in OpenClaw.

## Built-in Catalog (Dynamic Discovery + Static Fallback)

OpenClaw dynamically discovers available models from the Kilo Gateway at startup. Use `/models kilocode` to see the full list of models available with your account. Any model available on the gateway can be used with the `kilocode/` prefix:

| Model ref | Notes |
| ---------------------------------------- | ---------------------------------- |
| `kilocode/kilo/auto` | Default — smart routing |
| `kilocode/anthropic/claude-sonnet-4` | Anthropic via Kilo |
| `kilocode/openai/gpt-5.5` | OpenAI via Kilo |
| `kilocode/google/gemini-3.1-pro-preview` | Google via Kilo |
| ...and many more | Use `/models kilocode` to list all |

At startup, OpenClaw queries `GET https://api.kilo.ai/api/gateway/models` and merges discovered models ahead of the static fallback catalog. The static fallback always includes `kilocode/kilo/auto` (`Kilo Auto`) with `input: ["text", "image"]`, `reasoning: true`, `contextWindow: 1000000`, and `maxTokens: 128000`.

## Config Example

A minimal JSON5 configuration sets the API key in `env` and pins the default model to the smart-routing ref:

```json5
{
  env: { KILOCODE_API_KEY: "<your-kilocode-api-key>" }, // pragma: allowlist secret
  agents: {
    defaults: {
      model: { primary: "kilocode/kilo/auto" },
    },
  },
}
```

## Advanced — Transport, Stream Wrapper, and Troubleshooting

**Transport and compatibility.** Kilo Gateway is documented in source as OpenRouter-compatible, so it stays on the proxy-style OpenAI-compatible path rather than native OpenAI request shaping. Gemini-backed Kilo refs stay on the proxy-Gemini path, so OpenClaw keeps Gemini thought-signature sanitation there without enabling native Gemini replay validation or bootstrap rewrites. Kilo Gateway uses a Bearer token with your API key under the hood.

**Stream wrapper and reasoning.** Kilo's shared stream wrapper adds the provider app header and normalizes proxy reasoning payloads for supported concrete model refs. Per the source `Warning`, `kilocode/kilo/auto` and other proxy-reasoning-unsupported hints **skip reasoning injection**; if you need reasoning support, use a concrete model ref such as `kilocode/anthropic/claude-sonnet-4`.

**Troubleshooting.** If model discovery fails at startup, OpenClaw falls back to the static catalog containing `kilocode/kilo/auto`. Confirm your API key is valid and that your Kilo account has the desired models enabled. When the Gateway runs as a daemon, ensure `KILOCODE_API_KEY` is available to that process (for example in `~/.openclaw/.env` or via `env.shellEnv`).

**Source**: OpenClaw documentation — `providers/kilocode` (mirror `inbox/openclaw_docs/providers/kilocode.md`)
**Last Updated**: 2026-06-22
**Status**: Active
