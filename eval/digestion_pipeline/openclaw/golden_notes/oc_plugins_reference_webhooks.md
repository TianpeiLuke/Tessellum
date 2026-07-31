---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - webhooks
keywords:
  - openclaw webhooks plugin
  - "@openclaw/webhooks"
  - authenticated inbound webhooks
  - bind external automation taskflows
  - webhooks plugin surface
  - bundled openclaw plugin
  - plugin distribution install route
  - webhooks related docs plugins
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/webhooks
access_control_group: ["general"]
---

# OpenClaw — Webhooks Plugin Reference

## Overview

This note is the reference data sheet for the OpenClaw **Webhooks plugin**, mirroring the `plugins/reference/webhooks` source page. The plugin provides **authenticated inbound webhooks that bind external automation to OpenClaw TaskFlows** — i.e. external systems call an authenticated inbound HTTP endpoint and that call drives an OpenClaw TaskFlow. Per the source frontmatter, you read this page when you are **installing, configuring, or auditing the webhooks plugin**. The page captures three load-bearing facts: the plugin's **Distribution** (npm package id + install route), its **Surface** (what it registers — here, `plugin`), and a **Related docs** pointer to the full `/plugins/webhooks` how-to. This reference does not duplicate the full webhooks how-to (the TaskFlow binding, endpoint setup, and authentication details live in the `/plugins/webhooks` doc); it documents only what the plugin *is* and how it is distributed.

## Distribution

The source page lists the Distribution facts verbatim:

- **Package**: `@openclaw/webhooks`
- **Install route**: included in OpenClaw

The plugin is therefore a **bundled** plugin — its npm package id is `@openclaw/webhooks`, and its install route is "included in OpenClaw" (it ships with OpenClaw rather than requiring a separate ClawHub or npm install step).

## Surface

The source page declares the plugin's Surface as a single entry:

- `plugin`

That is, the Webhooks plugin registers as a **plugin** surface in the OpenClaw runtime. The page does not enumerate a more specific provider/channel/contract for this surface beyond `plugin` (*not specified in source* — the inbound-HTTP endpoint wiring and TaskFlow binding are documented in the linked `/plugins/webhooks` how-to, not on this reference data sheet).

**Source**: OpenClaw documentation — `plugins/reference/webhooks` (mirror `inbox/openclaw_docs/plugins/reference/webhooks.md`)
**Last Updated**: 2026-06-22
**Status**: Active
