---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - cloudflare ai gateway plugin
  - cloudflare-ai-gateway provider
  - openclaw model provider plugin
  - "@openclaw/cloudflare-ai-gateway-provider"
  - clawhub provider install
  - ai gateway model routing
  - npm plugin install route
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/cloudflare-ai-gateway
access_control_group: ["general"]
---

# OpenClaw — Cloudflare AI Gateway Plugin Reference

## Overview

This note is the procedure-level reference card for the OpenClaw **Cloudflare AI Gateway plugin**, which "Adds Cloudflare AI Gateway model provider support to OpenClaw." It mirrors the `plugins/reference/cloudflare-ai-gateway` stub page: how to obtain and install the plugin (its npm/ClawHub **Distribution** package), which contract **Surface** it registers (`providers: cloudflare-ai-gateway`), and the **Related docs** pointer to the deeper provider-configuration page. Use this card to discover or audit which plugin owns the `cloudflare-ai-gateway` model-provider capability; the upstream gateway's full configuration (base URL, auth, routed upstream models) lives on the linked provider page, not here.

## Distribution

The plugin is published as the npm package **`@openclaw/cloudflare-ai-gateway-provider`**. There are two install routes per the source card:

- **npm** — install the `@openclaw/cloudflare-ai-gateway-provider` package directly.
- **ClawHub** — install via the ClawHub slug `clawhub:@openclaw/cloudflare-ai-gateway-provider`.

The source does not state any further install flags, version pins, or configuration steps; those (provider base URL, credentials, model routing) are on the deeper provider page, not this reference card.

## Surface

The plugin registers a single contract surface: **`providers: cloudflare-ai-gateway`**. That is, it adds the `cloudflare-ai-gateway` model provider to OpenClaw's provider/model layer. Cloudflare AI Gateway itself is an AI gateway that fronts upstream model APIs, so once this provider is registered, OpenClaw can route model calls through it and surface the gateway-routed models into its model catalog. No channel, tool, or other contract surface is declared by this plugin in the source card.

**Source**: OpenClaw documentation — `plugins/reference/cloudflare-ai-gateway` (mirror `inbox/openclaw_docs/plugins/reference/cloudflare-ai-gateway.md`)
**Last Updated**: 2026-06-22
**Status**: Active
