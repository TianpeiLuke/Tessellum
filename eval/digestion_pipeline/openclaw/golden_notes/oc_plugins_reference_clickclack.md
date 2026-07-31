---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw clickclack plugin
  - clickclack channel surface
  - "@openclaw/clickclack"
  - channels clickclack
  - included in openclaw plugin
  - chat channel plugin reference
  - openclaw send receive messages
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/clickclack
access_control_group: ["general"]
---

# OpenClaw — Clickclack Plugin Reference

## Overview

This note is the OpenClaw plugin-reference card for **clickclack**, mirroring the `plugins/reference/clickclack` source page. The card states what an operator needs to install, configure, or audit the plugin: its one-line summary ("Adds the Clickclack channel surface for sending and receiving OpenClaw messages"), its **Distribution** (npm package `@openclaw/clickclack`, install route "included in OpenClaw"), the contract **Surface** it registers (`channels: clickclack`), and a **Related docs** pointer to the deeper `/channels/clickclack` channel-configuration page. The substance — the channel's full configuration, message send/receive semantics, and routing — lives on that deeper channel page and is reached through `## Related Notes`, not duplicated here.

## Summary

Clickclack adds the **Clickclack channel surface** for **sending and receiving OpenClaw messages** — that is, it docks a chat channel into the OpenClaw gateway so messages can flow in and out through it. It is a channel-type plugin (not a model provider or harness): it implements the channel contract surface rather than registering a model provider or supervising a runtime.

## Distribution

- **Package:** `@openclaw/clickclack`
- **Install route:** included in OpenClaw

Because the plugin is "included in OpenClaw," it ships bundled with the gateway and does not require a separate npm install or a ClawHub (`clawhub:`) install slug — unlike the provider plugins (e.g. cerebras, chutes) whose cards list an explicit npm + ClawHub install route. The package identifier above is reproduced verbatim from the source card.

## Surface

The plugin registers the contract surface:

```
channels: clickclack
```

This declares a single **`channels`** contract surface named `clickclack` — i.e. the plugin contributes a chat-channel adapter under that channel id. No other surfaces (no `providers`, no `tools`/`contracts`) are declared by this card.

**Source**: OpenClaw documentation — `plugins/reference/clickclack` (mirror `inbox/openclaw_docs/plugins/reference/clickclack.md`)
**Last Updated**: 2026-06-22
**Status**: Active
