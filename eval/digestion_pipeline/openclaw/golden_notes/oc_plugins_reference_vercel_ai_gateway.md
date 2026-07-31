---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - vercel ai gateway plugin
  - openclaw vercel-ai-gateway-provider
  - providers vercel-ai-gateway surface
  - llm aggregator gateway provider
  - bundled openclaw provider plugin
  - openclaw model provider plugin
  - vercel ai gateway model provider
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/vercel-ai-gateway
access_control_group: ["general"]
---

# OpenClaw — Vercel AI Gateway Provider Plugin (`@openclaw/vercel-ai-gateway-provider`)

## Overview

This note is the plugin-descriptor card for the OpenClaw **Vercel AI Gateway plugin**, which "Adds Vercel AI Gateway model provider support to OpenClaw." It mirrors the `plugins/reference/vercel-ai-gateway` source page — a compact descriptor with three sections (Distribution, Surface, Related docs). The card states three load-bearing facts: the npm package name, the install route, and the contract surface the plugin registers (`providers: vercel-ai-gateway`). It does NOT redefine the deeper Vercel AI Gateway provider configuration — that is owned by the provider doc this card points to. The Vercel AI Gateway is an LLM-aggregator/gateway service, so registering it contributes one aggregator-gateway provider entry to OpenClaw's model provider surface.

## Distribution

- **Package:** `@openclaw/vercel-ai-gateway-provider`
- **Install route:** included in OpenClaw

The plugin ships bundled with OpenClaw ("included in OpenClaw"), so no separate npm or ClawHub install step is required to make the Vercel AI Gateway provider available.

## Surface

The plugin registers the following contract surface (verbatim from source):

```
providers: vercel-ai-gateway
```

The `providers:` surface means the plugin adds an entry to OpenClaw's model-provider registry under the id `vercel-ai-gateway`. Because Vercel AI Gateway is itself an aggregator/gateway that fronts multiple upstream model providers, this single registered provider exposes the gateway's aggregated models to OpenClaw's model routing and catalog. The source does not specify per-model ids, auth env vars, or configuration keys for this provider — those are documented by the deeper provider config doc (see Related docs).

**Source**: OpenClaw documentation — `plugins/reference/vercel-ai-gateway` (mirror `inbox/openclaw_docs/plugins/reference/vercel-ai-gateway.md`)
**Last Updated**: 2026-06-22
**Status**: Active
