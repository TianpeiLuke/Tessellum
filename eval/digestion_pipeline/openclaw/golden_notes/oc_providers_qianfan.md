---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - qianfan
keywords:
  - openclaw qianfan provider
  - baidu qianfan maas
  - qianfan-provider plugin
  - QIANFAN_API_KEY bce-v3 altak
  - qianfan deepseek-v3.2 default
  - ernie-5.0-thinking-preview
  - openai-compatible transport
  - models.providers.qianfan config
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/qianfan
access_control_group: ["general"]
---

# OpenClaw — Configuring the Qianfan (Baidu MaaS) Provider

## Overview

This note is the setup procedure for wiring **Baidu Qianfan** as an OpenClaw model provider, mirroring the `providers/qianfan` source page. Qianfan is Baidu's MaaS platform that exposes a **unified API** routing requests to many models behind a single endpoint and API key; it is OpenAI-compatible, so most OpenAI SDKs work by switching the base URL. The procedure covers installing the `@openclaw/qianfan-provider` plugin, creating a Baidu Cloud account and `QIANFAN_API_KEY` (`bce-v3/ALTAK-...`), onboarding and verifying, the built-in catalog (`qianfan/deepseek-v3.2` default, `qianfan/ernie-5.0-thinking-preview`), a full `models.providers.qianfan` config override example, and the transport / catalog-override / troubleshooting caveats from the page's accordions.

## Provider Reference

The page header table fixes the provider identity and transport (all verbatim from source):

| Property | Value |
| -------- | --------------------------------- |
| Provider | `qianfan` |
| Auth | `QIANFAN_API_KEY` |
| API | OpenAI-compatible |
| Base URL | `https://qianfan.baidubce.com/v2` |

Qianfan's unified API routes requests to many models behind one endpoint and one API key, and because the transport is OpenAI-compatible, most OpenAI SDKs work simply by switching the base URL to `https://qianfan.baidubce.com/v2`.

## Install plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/qianfan-provider
openclaw gateway restart
```

## Getting started

The page walks four `<Steps>` to go from a Baidu account to a verified provider:

1. **Create a Baidu Cloud account** — Sign up or log in at the [Qianfan Console](https://console.bce.baidu.com/qianfan/ais/console/apiKey) and ensure you have Qianfan API access enabled.
2. **Generate an API key** — Create a new application or select an existing one, then generate an API key. The key format is `bce-v3/ALTAK-...`.
3. **Run onboarding** — `openclaw onboard --auth-choice qianfan-api-key`.
4. **Verify the model is available** — `openclaw models list --provider qianfan`.

```bash
openclaw onboard --auth-choice qianfan-api-key
openclaw models list --provider qianfan
```

## Built-in catalog

The provider ships a static catalog of two model refs (both use the `qianfan/` prefix and are reasoning-enabled):

| Model ref | Input | Context | Max output | Reasoning | Notes |
| ------------------------------------ | ----------- | ------- | ---------- | --------- | ------------- |
| `qianfan/deepseek-v3.2` | text | 98,304 | 32,768 | Yes | Default model |
| `qianfan/ernie-5.0-thinking-preview` | text, image | 119,000 | 64,000 | Yes | Multimodal |

The default model ref is `qianfan/deepseek-v3.2`. Per the page's `<Tip>`, you only need to override `models.providers.qianfan` when you need a custom base URL or model metadata.

## Config example

A full `models.providers.qianfan` override (sets the primary model, an alias, and explicit per-model metadata). Note the transport is declared as `api: "openai-completions"` (verbatim from source):

```json5
{
  env: { QIANFAN_API_KEY: "bce-v3/ALTAK-..." },
  agents: {
    defaults: {
      model: { primary: "qianfan/deepseek-v3.2" },
      models: {
        "qianfan/deepseek-v3.2": { alias: "QIANFAN" },
      },
    },
  },
  models: {
    providers: {
      qianfan: {
        baseUrl: "https://qianfan.baidubce.com/v2",
        api: "openai-completions",
        models: [
          {
            id: "deepseek-v3.2",
            name: "DEEPSEEK V3.2",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 98304,
            maxTokens: 32768,
          },
          {
            id: "ernie-5.0-thinking-preview",
            name: "ERNIE-5.0-Thinking-Preview",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 119000,
            maxTokens: 64000,
          },
        ],
      },
    },
  },
}
```

## Transport, catalog overrides, and troubleshooting

The page's `<AccordionGroup>` captures three operational caveats:

- **Transport and compatibility** — Qianfan runs through the OpenAI-compatible transport path, NOT native OpenAI request shaping. Standard OpenAI SDK features work, but provider-specific parameters may not be forwarded.
- **Catalog and overrides** — The static catalog currently includes `deepseek-v3.2` and `ernie-5.0-thinking-preview`. Add or override `models.providers.qianfan` only when you need a custom base URL or model metadata. Model refs use the `qianfan/` prefix (for example `qianfan/deepseek-v3.2`).
- **Troubleshooting** — Ensure your API key starts with `bce-v3/ALTAK-` and has Qianfan API access enabled in the Baidu Cloud console; if models are not listed, confirm your account has the Qianfan service activated; the default base URL is `https://qianfan.baidubce.com/v2` and should only be changed if you use a custom endpoint or proxy.

**Source**: OpenClaw documentation — `providers/qianfan` (mirror `inbox/openclaw_docs/providers/qianfan.md`)
**Last Updated**: 2026-06-22
**Status**: Active
