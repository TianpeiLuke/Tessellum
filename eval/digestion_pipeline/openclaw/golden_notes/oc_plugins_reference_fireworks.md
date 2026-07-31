---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw fireworks plugin
  - fireworks-provider plugin
  - fireworks model provider
  - fireworks ai inference
  - bundled openclaw plugin
  - model provider plugin
  - plugin surface providers
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/fireworks
access_control_group: ["general"]
---

# OpenClaw — Fireworks Plugin Reference Card

## Overview

This note models the OpenClaw **Fireworks plugin** as a plugin-manifest reference card, mirroring the `plugins/reference/fireworks` source page. The plugin's summary is "Adds Fireworks model provider support to OpenClaw." Its `read_when` trigger is: "You are installing, configuring, or auditing the fireworks plugin." The card carries the plugin's identity triple — its npm package name, its install route, and its Surface declaration (the provider it registers) — together with a `Related docs` pointer to the matching `/providers/fireworks` user page. This is a leaf reference record (model BB), not a how-to procedure; depth on model-provider configuration, model identifiers, and the provider runtime lives in the linked term, provider, and code notes rather than inline.

## Distribution

The Fireworks plugin's package identity and install route, reproduced verbatim from the source page:

- Package: `@openclaw/fireworks-provider`
- Install route: included in OpenClaw

"Included in OpenClaw" means the plugin is **bundled** in the OpenClaw monorepo — it ships with the gateway and does not require a separate npm or ClawHub install step (unlike installed plugins distributed as `clawhub:` / npm packages).

## Surface

The Surface declaration is the load-bearing, machine-meaningful content of the card — the typed provider the plugin registers with the OpenClaw extension framework. Reproduced verbatim from the source page:

> providers: fireworks

So the Fireworks plugin registers the **`fireworks` provider**, adding Fireworks AI model-provider support to OpenClaw. Through this provider, Fireworks AI's hosted models become selectable in the OpenClaw model catalog. The page declares no contracts beyond the `fireworks` provider, and no further configuration keys, environment variables, or model identifiers — those are owned by the `/providers/fireworks` user page, which this card links to as its `Related docs` target.

**Source**: OpenClaw documentation — `plugins/reference/fireworks` (mirror `inbox/openclaw_docs/plugins/reference/fireworks.md`)
**Last Updated**: 2026-06-22
**Status**: Active
