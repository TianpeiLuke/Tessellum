---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - gateway
keywords:
  - vercel ai gateway openclaw
  - vercel-ai-gateway provider
  - ai_gateway_api_key
  - ai-gateway-api-key auth-choice
  - anthropic messages compatible gateway
  - v1 models auto-discovery
  - model id shorthand normalization
  - provider routing model ref prefix
  - prefix-aware thinking levels
topics:
  - OpenClaw
  - Providers
  - Vercel AI Gateway
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/vercel-ai-gateway
access_control_group: ["general"]
---

# OpenClaw — Connecting the Vercel AI Gateway Provider

## Overview

This note is the procedure for connecting OpenClaw to the [Vercel AI Gateway](https://vercel.com/ai-gateway), a unified API that fronts hundreds of upstream models through a single endpoint. It mirrors the `providers/vercel-ai-gateway` source page: the provider property table, the three-step `Getting started` onboarding, the non-interactive (CI) onboarding command, the model-ID shorthand normalization table, and the three `Advanced configuration` accordions (daemon env-var availability, per-upstream provider routing by model-ref prefix, and prefix-aware thinking levels). The gateway's distinguishing trait is that a single `AI_GATEWAY_API_KEY` authenticates against every upstream provider, while OpenClaw routes each request to the correct upstream by the model-ref prefix.

## Provider Properties

The provider is identified and configured by the following fixed values, reproduced verbatim from the source property table:

| Property | Value |
| --- | --- |
| Provider | `vercel-ai-gateway` |
| Auth | `AI_GATEWAY_API_KEY` |
| API | Anthropic Messages compatible |
| Model catalog | Auto-discovered via `/v1/models` |

OpenClaw auto-discovers the Gateway `/v1/models` catalog, so `/models vercel-ai-gateway` includes current model refs such as `vercel-ai-gateway/openai/gpt-5.5` and `vercel-ai-gateway/moonshotai/kimi-k2.6`. The catalog is not enumerated in the source page; it is populated dynamically from the gateway's `/v1/models` endpoint at runtime.

## Getting Started

The source page presents onboarding as three steps:

1. **Set the API key.** Run onboarding and choose the AI Gateway auth option:

```bash
openclaw onboard --auth-choice ai-gateway-api-key
```

2. **Set a default model.** Add the model to your OpenClaw config:

```json5
{
  agents: {
    defaults: {
      model: { primary: "vercel-ai-gateway/anthropic/claude-opus-4.6" },
    },
  },
}
```

3. **Verify the model is available.** List the provider's models:

```bash
openclaw models list --provider vercel-ai-gateway
```

The auth choice for this provider is `ai-gateway-api-key` (note the hyphenated `ai-gateway` prefix), distinct from the provider id `vercel-ai-gateway` and from the env var `AI_GATEWAY_API_KEY`.

## Non-Interactive Example

For scripted or CI setups, pass all values on the command line:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY"
```

The non-interactive form combines `--non-interactive`, `--mode local`, the same `--auth-choice ai-gateway-api-key` selector used interactively, and a dedicated `--ai-gateway-api-key` flag that receives the key value (here read from the `$AI_GATEWAY_API_KEY` shell variable).

## Model ID Shorthand

OpenClaw accepts Vercel Claude shorthand model refs and normalizes them to a canonical form at runtime. The source documents two shorthand inputs and their normalized results:

| Shorthand input | Normalized model ref |
| --- | --- |
| `vercel-ai-gateway/claude-opus-4.6` | `vercel-ai-gateway/anthropic/claude-opus-4.6` |
| `vercel-ai-gateway/opus-4.6` | `vercel-ai-gateway/anthropic/claude-opus-4-6` |

The first shorthand omits the `anthropic/` upstream namespace, which normalization inserts; the second additionally rewrites the dotted version `opus-4.6` to the canonical dashed `claude-opus-4-6` form. Per the source, you can use either the shorthand or the fully qualified model ref in your configuration — OpenClaw resolves the canonical form automatically.

## Advanced Configuration

The source page's `Advanced configuration` block contains three accordions, all of which are this note's scope.

**Environment variable for daemon processes.** If the OpenClaw Gateway runs as a daemon (launchd/systemd), make sure `AI_GATEWAY_API_KEY` is available to that process. A key exported only in an interactive shell will not be visible to a launchd/systemd daemon unless that environment is explicitly imported. Set the key in `~/.openclaw/.env` or via `env.shellEnv` to ensure the gateway process can read it. (This daemon-env-availability note recurs across several provider pages; see the cross-referenced sibling provider notes and `cc_configure_your_environment`.)

**Provider routing.** Vercel AI Gateway routes requests to the upstream provider based on the model-ref prefix. For example, `vercel-ai-gateway/anthropic/claude-opus-4.6` routes through Anthropic, while `vercel-ai-gateway/openai/gpt-5.5` routes through OpenAI and `vercel-ai-gateway/moonshotai/kimi-k2.6` routes through MoonshotAI. Your single `AI_GATEWAY_API_KEY` handles authentication for all upstream providers — there is no per-upstream key to manage.

**Thinking levels.** `/think` options follow trusted upstream model prefixes when OpenClaw knows the upstream provider contract. `vercel-ai-gateway/anthropic/...` uses the Claude thinking profile, including adaptive defaults for Claude 4.6 models. `vercel-ai-gateway/openai/gpt-5.4`, `gpt-5.5`, and Codex-style refs expose `/think xhigh` just like the direct OpenAI/OpenAI Codex providers. Other namespaced refs keep the normal reasoning levels unless their catalog metadata declares more.

**Source**: OpenClaw documentation — `providers/vercel-ai-gateway` (mirror `inbox/openclaw_docs/providers/vercel-ai-gateway.md`)
**Last Updated**: 2026-06-22
**Status**: Active
