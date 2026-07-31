---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - arcee
keywords:
  - openclaw arcee provider
  - arcee trinity models
  - arceeai api key
  - openrouter api key arcee
  - openclaw plugins install arcee-provider
  - arcee onboarding auth-choice
  - trinity mixture of experts moe
  - openai-compatible provider setup
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/arcee
access_control_group: ["general"]
---

# OpenClaw — Arcee AI Provider Setup

## Overview

This note is the setup procedure for the **Arcee AI** provider in OpenClaw, mirroring the `providers/arcee` source page. Arcee AI provides access to the **Trinity** family of mixture-of-experts (MoE) models through an OpenAI-compatible API, and all Trinity models are Apache 2.0 licensed. Arcee models can be reached two ways: **directly** via the Arcee platform, or **via OpenRouter** — and the procedure here walks the plugin install, the two auth/onboarding routes (interactive and non-interactive), the static built-in Trinity catalog, and the supported-features matrix exactly as the source documents them.

The provider's at-a-glance properties (from the page's header table): provider id `arcee`; auth via `ARCEEAI_API_KEY` (direct) or `OPENROUTER_API_KEY` (via OpenRouter); API is OpenAI-compatible; base URL `https://api.arcee.ai/api/v1` (direct) or `https://openrouter.ai/api/v1` (OpenRouter).

## Install plugin

Arcee is an official OpenClaw provider plugin. Install it, then restart the Gateway so the provider registers:

```bash
openclaw plugins install @openclaw/arcee-provider
openclaw gateway restart
```

## Getting started

There are two auth routes — **Direct (Arcee platform)** and **Via OpenRouter** — each a three-step flow (get key → run onboarding → set a default model).

**Direct (Arcee platform).** Create an API key at the Arcee AI chat console (`https://chat.arcee.ai/`), then run onboarding with the Arcee direct auth choice:

```bash
openclaw onboard --auth-choice arceeai-api-key
```

**Via OpenRouter.** Create an API key at OpenRouter (`https://openrouter.ai/keys`), then run onboarding with the OpenRouter auth choice:

```bash
openclaw onboard --auth-choice arceeai-openrouter
```

**Set a default model** (identical for both routes — the same model refs work for direct and OpenRouter setups, for example `arcee/trinity-large-thinking`):

```json5
{
  agents: {
    defaults: {
      model: { primary: "arcee/trinity-large-thinking" },
    },
  },
}
```

## Non-interactive setup

For scripted/headless onboarding, the page provides a non-interactive flow per auth route. Direct (Arcee platform) — passes the Arcee key explicitly via `--arceeai-api-key`; OpenRouter — passes the OpenRouter key via `--openrouter-api-key`:

```bash
# Direct (Arcee platform)
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice arceeai-api-key \
  --arceeai-api-key "$ARCEEAI_API_KEY"

# Via OpenRouter
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice arceeai-openrouter \
  --openrouter-api-key "$OPENROUTER_API_KEY"
```

## Built-in catalog

OpenClaw currently ships this Arcee static catalog (reproduced verbatim from the source page):

| Model ref                      | Name                   | Input | Context | Cost (in/out per 1M) | Notes                                     |
| ------------------------------ | ---------------------- | ----- | ------- | -------------------- | ----------------------------------------- |
| `arcee/trinity-large-thinking` | Trinity Large Thinking | text  | 256K    | $0.25 / $0.90        | Default model; reasoning enabled          |
| `arcee/trinity-large-preview`  | Trinity Large Preview  | text  | 128K    | $0.25 / $1.00        | General-purpose; 400B params, 13B active  |
| `arcee/trinity-mini`           | Trinity Mini 26B       | text  | 128K    | $0.045 / $0.15       | Fast and cost-efficient; function calling |

The onboarding preset sets `arcee/trinity-large-thinking` as the default model.

## Supported features

| Feature                                       | Supported                                    |
| --------------------------------------------- | -------------------------------------------- |
| Streaming                                     | Yes                                          |
| Tool use / function calling                   | Yes (Trinity Mini, Trinity Large Preview)    |
| Structured output (JSON mode and JSON schema) | Yes                                          |
| Extended thinking                             | Yes (Trinity Large Thinking; tools disabled) |

**Environment note.** If the Gateway runs as a daemon (launchd/systemd), make sure `ARCEEAI_API_KEY` (or `OPENROUTER_API_KEY`) is available to that process — for example in `~/.openclaw/.env` or via `env.shellEnv`.

**OpenRouter routing.** When using Arcee models via OpenRouter, the same `arcee/*` model refs apply. OpenClaw handles routing transparently based on your auth choice; see the OpenRouter provider docs for OpenRouter-specific configuration details.

**Source**: OpenClaw documentation — `providers/arcee` (mirror `inbox/openclaw_docs/providers/arcee.md`)
**Last Updated**: 2026-06-22
**Status**: Active
