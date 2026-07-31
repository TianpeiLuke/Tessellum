---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - chutes
keywords:
  - openclaw chutes provider
  - chutes oauth onboarding
  - chutes api key onboarding
  - chutes default model glm-4.7-tee
  - chutes static catalog discovery
  - chutes default aliases
  - openai-compatible provider openclaw
  - chutes-provider plugin install
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/chutes
access_control_group: ["general"]
---

# OpenClaw — Configuring the Chutes Provider

## Overview

This note is the setup procedure for the OpenClaw `chutes` provider, mirroring the `providers/chutes` source page. Chutes exposes open-source model catalogs through an OpenAI-compatible API, and OpenClaw supports both browser OAuth and direct API-key auth for the `chutes` provider. The procedure covers installing the official plugin, the two onboarding paths (OAuth vs API key), the live-discovery-with-static-fallback model behavior, the three convenience aliases, the built-in starter catalog, and the config block — every claim is grounded in the source page's tables, code blocks, and accordions.

The provider properties (verbatim from the source page) are: provider id `chutes`; API is OpenAI-compatible; base URL `https://llm.chutes.ai/v1`; auth is OAuth or API key. Both onboarding paths register the Chutes static catalog and set the default model to `chutes/zai-org/GLM-4.7-TEE`.

## Install plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/chutes-provider
openclaw gateway restart
```

## Getting started

Pick one of two onboarding paths. Both register the Chutes static catalog and set the default model to `chutes/zai-org/GLM-4.7-TEE`, and both use the same `chutes` provider id. The runtime environment variables are `CHUTES_API_KEY` and `CHUTES_OAUTH_TOKEN`.

### OAuth path

Run the OAuth onboarding flow:

```bash
openclaw onboard --auth-choice chutes
```

OpenClaw launches the browser flow locally, or shows a URL plus redirect-paste flow on remote/headless hosts. OAuth tokens auto-refresh through OpenClaw auth profiles. After onboarding, the default model is set to `chutes/zai-org/GLM-4.7-TEE` and the Chutes static catalog is registered.

### API key path

First create a key at [chutes.ai/settings/api-keys](https://chutes.ai/settings/api-keys), then run the API-key onboarding flow:

```bash
openclaw onboard --auth-choice chutes-api-key
```

After onboarding, the default model is set to `chutes/zai-org/GLM-4.7-TEE` and the Chutes static catalog is registered.

## Discovery behavior

When Chutes auth is available, OpenClaw queries the Chutes catalog with that credential and uses the discovered models. If discovery fails, OpenClaw falls back to a static catalog so onboarding and startup still work.

## Default aliases

OpenClaw registers three convenience aliases for the Chutes static catalog:

| Alias           | Target model                                          |
| --------------- | ----------------------------------------------------- |
| `chutes-fast`   | `chutes/zai-org/GLM-4.7-FP8`                          |
| `chutes-pro`    | `chutes/deepseek-ai/DeepSeek-V3.2-TEE`                |
| `chutes-vision` | `chutes/chutesai/Mistral-Small-3.2-24B-Instruct-2506` |

## Built-in starter catalog

The static fallback catalog includes these current Chutes refs: `chutes/zai-org/GLM-4.7-TEE`, `chutes/zai-org/GLM-5-TEE`, `chutes/deepseek-ai/DeepSeek-V3.2-TEE`, `chutes/deepseek-ai/DeepSeek-R1-0528-TEE`, `chutes/moonshotai/Kimi-K2.5-TEE`, `chutes/chutesai/Mistral-Small-3.2-24B-Instruct-2506`, `chutes/Qwen/Qwen3-Coder-Next-TEE`, and `chutes/openai/gpt-oss-120b-TEE`.

## Config example

A config block setting the primary model and per-model aliases:

```json5
{
  agents: {
    defaults: {
      model: { primary: "chutes/zai-org/GLM-4.7-TEE" },
      models: {
        "chutes/zai-org/GLM-4.7-TEE": { alias: "Chutes GLM 4.7" },
        "chutes/deepseek-ai/DeepSeek-V3.2-TEE": { alias: "Chutes DeepSeek V3.2" },
      },
    },
  },
}
```

The OAuth flow can be customized with optional environment variables: `CHUTES_CLIENT_ID` (custom OAuth client ID), `CHUTES_CLIENT_SECRET` (custom OAuth client secret), `CHUTES_OAUTH_REDIRECT_URI` (custom redirect URI), and `CHUTES_OAUTH_SCOPES` (custom OAuth scopes); see the Chutes OAuth docs for redirect-app requirements. Source notes: API-key and OAuth discovery both use the same `chutes` provider id; Chutes models are registered as `chutes/<model-id>`; and if discovery fails at startup, the static catalog is used automatically.

**Source**: OpenClaw documentation — `providers/chutes` (mirror `inbox/openclaw_docs/providers/chutes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
