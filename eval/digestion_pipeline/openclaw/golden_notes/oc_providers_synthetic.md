---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - synthetic
keywords:
  - openclaw synthetic provider
  - synthetic api key
  - anthropic messages compatible proxy
  - hf prefixed open weight models
  - synthetic base url override
  - openclaw onboard auth-choice synthetic-api-key
  - model allowlist agents defaults models
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/synthetic
access_control_group: ["general"]
---

# OpenClaw — Connecting the Synthetic Provider (Anthropic-Messages Proxy for Open-Weight Models)

## Overview

This note is the procedure for connecting OpenClaw to [Synthetic](https://synthetic.new), an Anthropic-compatible proxy that fronts open-weight HuggingFace models. It mirrors the `providers/synthetic` source page: OpenClaw registers Synthetic as the `synthetic` provider and talks to it over the **Anthropic Messages API** at base URL `https://api.synthetic.new/anthropic`. The note covers the provider property table, onboarding with `SYNTHETIC_API_KEY` and `--auth-choice synthetic-api-key`, the verbatim `models.providers.synthetic` config block, the 21-model `hf:`-prefixed built-in catalog, the model allowlist, and the base-URL override (including OpenClaw's automatic `/v1` append). Shared model-selection rules and the full config schema are link-outs (`concepts/model-providers`, `gateway/configuration-reference`), not redigested here.

## Provider Properties

Synthetic exposes Anthropic-compatible endpoints, and OpenClaw uses the Anthropic Messages API to reach it. The provider's identifying properties (from the source property table) are:

| Property | Value |
| -------- | ------------------------------------- |
| Provider | `synthetic` |
| Auth | `SYNTHETIC_API_KEY` |
| API | Anthropic Messages |
| Base URL | `https://api.synthetic.new/anthropic` |

## Getting Started

Onboarding is a three-step wizard flow. First, obtain a `SYNTHETIC_API_KEY` from your Synthetic account, or let the onboarding wizard prompt you for one. Second, run onboarding with the Synthetic auth choice:

```bash
openclaw onboard --auth-choice synthetic-api-key
```

Third, verify the default model. After onboarding the default model is set to:

```
synthetic/hf:MiniMaxAI/MiniMax-M2.5
```

A base-URL caveat applies throughout: OpenClaw's Anthropic client appends `/v1` to the base URL automatically, so you use `https://api.synthetic.new/anthropic` (NOT `/anthropic/v1`). If Synthetic changes its base URL, override `models.providers.synthetic.baseUrl` (see Base URL Override below).

## Config Example

A full configuration block sets the API key in `env`, selects a default primary model with an alias under `agents.defaults`, and defines the `synthetic` provider under `models.providers` with `models.mode: "merge"`. The provider block specifies `baseUrl`, `apiKey` (interpolated from the env var), `api: "anthropic-messages"`, and a per-model definition with `id`, `name`, `reasoning`, `input`, `cost`, `contextWindow`, and `maxTokens`. The source's example (reproduced verbatim) is:

```json5
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.5" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.5": { alias: "MiniMax M2.5" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.5",
            name: "MiniMax M2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

## Built-in Catalog

All Synthetic models use cost `0` (input/output/cache). Model refs use the form `synthetic/<modelId>`, and every catalog model ID carries the `hf:` HuggingFace prefix. Use `openclaw models list --provider synthetic` to see all models available on your account. The 21 built-in models (reproduced verbatim from the source catalog) are:

| Model ID | Context window | Max tokens | Reasoning | Input |
| ------------------------------------------------------ | -------------- | ---------- | --------- | ------------ |
| `hf:MiniMaxAI/MiniMax-M2.5` | 192,000 | 65,536 | no | text |
| `hf:moonshotai/Kimi-K2-Thinking` | 256,000 | 8,192 | yes | text |
| `hf:zai-org/GLM-4.7` | 198,000 | 128,000 | no | text |
| `hf:deepseek-ai/DeepSeek-R1-0528` | 128,000 | 8,192 | no | text |
| `hf:deepseek-ai/DeepSeek-V3-0324` | 128,000 | 8,192 | no | text |
| `hf:deepseek-ai/DeepSeek-V3.1` | 128,000 | 8,192 | no | text |
| `hf:deepseek-ai/DeepSeek-V3.1-Terminus` | 128,000 | 8,192 | no | text |
| `hf:deepseek-ai/DeepSeek-V3.2` | 159,000 | 8,192 | no | text |
| `hf:meta-llama/Llama-3.3-70B-Instruct` | 128,000 | 8,192 | no | text |
| `hf:meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | 524,000 | 8,192 | no | text |
| `hf:moonshotai/Kimi-K2-Instruct-0905` | 256,000 | 8,192 | no | text |
| `hf:moonshotai/Kimi-K2.5` | 256,000 | 8,192 | yes | text + image |
| `hf:openai/gpt-oss-120b` | 128,000 | 8,192 | no | text |
| `hf:Qwen/Qwen3-235B-A22B-Instruct-2507` | 256,000 | 8,192 | no | text |
| `hf:Qwen/Qwen3-Coder-480B-A35B-Instruct` | 256,000 | 8,192 | no | text |
| `hf:Qwen/Qwen3-VL-235B-A22B-Instruct` | 250,000 | 8,192 | no | text + image |
| `hf:zai-org/GLM-4.5` | 128,000 | 128,000 | no | text |
| `hf:zai-org/GLM-4.6` | 198,000 | 128,000 | no | text |
| `hf:zai-org/GLM-5` | 256,000 | 128,000 | yes | text + image |
| `hf:deepseek-ai/DeepSeek-V3` | 128,000 | 8,192 | no | text |
| `hf:Qwen/Qwen3-235B-A22B-Thinking-2507` | 256,000 | 8,192 | yes | text |

Reasoning is enabled on `Kimi-K2-Thinking`, `Kimi-K2.5`, `GLM-5`, and `Qwen3-235B-A22B-Thinking-2507`; vision (`text + image` input) is supported by `Kimi-K2.5`, `Qwen3-VL-235B-A22B-Instruct`, and `GLM-5`. The largest context window is `Llama-4-Maverick-17B-128E-Instruct-FP8` at 524,000 tokens.

### Model Allowlist

If you enable a model allowlist (`agents.defaults.models`), add every Synthetic model you plan to use. Models not in the allowlist will be hidden from the agent.

### Base URL Override

If Synthetic changes its API endpoint, override the base URL in your config:

```json5
{
  models: {
    providers: {
      synthetic: {
        baseUrl: "https://new-api.synthetic.new/anthropic",
      },
    },
  },
}
```

Remember that OpenClaw appends `/v1` automatically, so the override URL should end at `/anthropic` and not include `/v1`.

**Source**: OpenClaw documentation — `providers/synthetic` (mirror `inbox/openclaw_docs/providers/synthetic.md`)
**Last Updated**: 2026-06-22
**Status**: Active
