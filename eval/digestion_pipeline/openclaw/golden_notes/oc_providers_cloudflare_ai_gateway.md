---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - gateway
keywords:
  - cloudflare ai gateway openclaw
  - cloudflare-ai-gateway-provider
  - cloudflare ai gateway anthropic messages api
  - cf-aig-authorization header
  - cloudflare_ai_gateway_api_key
  - openclaw onboard cloudflare-ai-gateway-api-key
  - claude-sonnet-4-6 default model
  - daemon env var openclaw .env
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/cloudflare-ai-gateway
access_control_group: ["general"]
---

# OpenClaw — Routing Anthropic Through Cloudflare AI Gateway

## Overview

This note is the setup procedure for the OpenClaw `cloudflare-ai-gateway` provider, which routes the Anthropic Messages API through a Cloudflare AI Gateway endpoint so you can add analytics, caching, and controls in front of the provider. It mirrors the `providers/cloudflare-ai-gateway` source page: the provider property table (provider id, Base URL template, default model, API-key env var), the prefill-stripping behavior under extended thinking, installing `@openclaw/cloudflare-ai-gateway-provider`, the interactive and non-interactive onboarding flows, the `cf-aig-authorization` header for authenticated gateways, and the daemon environment-variable caveat. Provider/model resolution and failover are owned by `concepts/model-providers` and are linked, not redefined, here.

## Provider Properties

Cloudflare AI Gateway sits in front of provider APIs and lets you add analytics, caching, and controls; for Anthropic, OpenClaw uses the Anthropic Messages API through your Gateway endpoint. The provider exposes the following fixed properties (verbatim from source):

| Property | Value |
| --- | --- |
| Provider | `cloudflare-ai-gateway` |
| Base URL | `https://gateway.ai.cloudflare.com/v1/<account_id>/<gateway_id>/anthropic` |
| Default model | `cloudflare-ai-gateway/claude-sonnet-4-6` |
| API key | `CLOUDFLARE_AI_GATEWAY_API_KEY` (your provider API key for requests through the Gateway) |

For Anthropic models routed through Cloudflare AI Gateway, use your **Anthropic API key** as the provider key — the value stored in `CLOUDFLARE_AI_GATEWAY_API_KEY` is the upstream provider's key, not a separate Cloudflare key.

## Prefill Behavior With Extended Thinking

When thinking is enabled for Anthropic Messages models, OpenClaw strips trailing assistant prefill turns before sending the payload through Cloudflare AI Gateway. Anthropic rejects response prefilling with extended thinking, while ordinary non-thinking prefill remains available. No flags or config keys govern this — it is automatic payload normalization performed by OpenClaw for this provider path.

## Install Plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/cloudflare-ai-gateway-provider
openclaw gateway restart
```

## Getting Started

The interactive onboarding flow is three steps:

1. **Set the provider API key and Gateway details.** Run onboarding and choose the Cloudflare AI Gateway auth option; this prompts for your account ID, gateway ID, and API key:

   ```bash
   openclaw onboard --auth-choice cloudflare-ai-gateway-api-key
   ```

2. **Set a default model.** Add the model to your OpenClaw config:

   ```json5
   {
     agents: {
       defaults: {
         model: { primary: "cloudflare-ai-gateway/claude-sonnet-4-6" },
       },
     },
   }
   ```

3. **Verify the model is available.**

   ```bash
   openclaw models list --provider cloudflare-ai-gateway
   ```

## Non-Interactive Example

For scripted or CI setups, pass all values on the command line:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice cloudflare-ai-gateway-api-key \
  --cloudflare-ai-gateway-account-id "your-account-id" \
  --cloudflare-ai-gateway-gateway-id "your-gateway-id" \
  --cloudflare-ai-gateway-api-key "$CLOUDFLARE_AI_GATEWAY_API_KEY"
```

## Advanced Configuration

**Authenticated gateways.** If you enabled Gateway authentication in Cloudflare, add the `cf-aig-authorization` header. This is **in addition to** your provider API key:

```json5
{
  models: {
    providers: {
      "cloudflare-ai-gateway": {
        headers: {
          "cf-aig-authorization": "Bearer <cloudflare-ai-gateway-token>",
        },
      },
    },
  },
}
```

The `cf-aig-authorization` header authenticates with the Cloudflare Gateway itself, while the provider API key (for example, your Anthropic key) authenticates with the upstream provider — the two credentials cover two distinct auth boundaries.

**Environment note.** If the Gateway runs as a daemon (launchd/systemd), make sure `CLOUDFLARE_AI_GATEWAY_API_KEY` is available to that process. A key exported only in an interactive shell will not help a launchd/systemd daemon unless that environment is imported there as well; set the key in `~/.openclaw/.env` or via `env.shellEnv` to ensure the gateway process can read it.

**Source**: OpenClaw documentation — `providers/cloudflare-ai-gateway` (mirror `inbox/openclaw_docs/providers/cloudflare-ai-gateway.md`)
**Last Updated**: 2026-06-22
**Status**: Active
