---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw qqbot plugin
  - qq bot channel plugin
  - "@openclaw/qqbot"
  - channels qqbot surface
  - group and direct-message workflows
  - npm clawhub install route
  - contracts tools skills
  - plugin reference card
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/qqbot
access_control_group: ["general"]
---

# OpenClaw — QQ Bot Plugin (`@openclaw/qqbot`) Reference Card

## Overview

This note models the OpenClaw `plugins/reference/qqbot` registry card: the machine-generated catalog entry for the **QQ Bot channel plugin**, which adds a QQ chat channel "for group and direct-message workflows." As a `model` descriptor it captures the three load-bearing facts of the card — what the package is (`@openclaw/qqbot`), where it is distributed from (npm; ClawHub), and what contract surface it registers (`channels: qqbot; contracts: tools; skills`) — plus the deep-config doc the card points at (`/channels/qqbot`). It mirrors the `plugins/reference/qqbot` source page exactly; the substantive channel setup lives in the linked channel doc and is referenced, not duplicated.

## Distribution

The plugin's distribution metadata, copied verbatim from the source card:

- **Package**: `@openclaw/qqbot`
- **Install route**: npm; ClawHub

The two listed install routes mean the plugin is published as a standard npm package (`@openclaw/qqbot`) and is also discoverable/installable through ClawHub (the OpenClaw plugin registry). This contrasts with bundled/"included in OpenClaw" plugins (which require no separate install) and with source-checkout-only plugins (which are not published): `@openclaw/qqbot` is a separately-installed, npm-distributed extension.

## Surface

The contract surface the plugin registers, verbatim from the source card:

```
channels: qqbot; contracts: tools; skills
```

This surface declares three contributions:

- **`channels: qqbot`** — the plugin registers a channel adapter named `qqbot`, i.e. it adds QQ as a messaging channel the gateway can dock and route inbound/outbound messages over. This is the primary surface and the reason the card is classified as a channel plugin (serving the "group and direct-message workflows" stated in the summary).
- **`contracts: tools`** — the plugin also contributes a `tools` contract, i.e. it can expose agent-callable tools alongside the channel adapter (for QQ-specific actions the agent can invoke).
- **`skills`** — the plugin additionally ships `skills` (packaged agent capabilities/instructions) as part of its surface.

The card does not enumerate individual channel configuration keys, tool names, or skill identifiers — those are the responsibility of the deep channel-config doc (`/channels/qqbot`), referenced below. Anything beyond these three surface declarations is *Not specified in source*.

**Source**: OpenClaw documentation — `plugins/reference/qqbot` (mirror `inbox/openclaw_docs/plugins/reference/qqbot.md`)
**Last Updated**: 2026-06-22
**Status**: Active
