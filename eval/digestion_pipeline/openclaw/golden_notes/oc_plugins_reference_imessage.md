---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw imessage plugin
  - imessage channel surface
  - "@openclaw/imessage"
  - channels imessage
  - bundled openclaw plugin
  - imessage chat channel
  - send receive openclaw messages
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/imessage
access_control_group: ["general"]
---

# OpenClaw — iMessage Plugin (`@openclaw/imessage`)

## Overview

This note is the catalog reference card for the OpenClaw **iMessage plugin**, mirroring the `plugins/reference/imessage` source page. The plugin "Adds the iMessage channel surface for sending and receiving OpenClaw messages." As a procedure note it captures the three load-bearing catalog facts you use to identify, install, or audit this plugin: its npm **package name** (`@openclaw/imessage`), its **install route** (included in OpenClaw — i.e. bundled), and the exact **surface** it contributes (`channels: imessage`). It is the thin catalog layer above the deeper iMessage channel setup page; the full channel configuration lives on the linked `/channels/imessage` page, not here.

## Distribution

- Package: `@openclaw/imessage`
- Install route: included in OpenClaw

The plugin ships **bundled** with OpenClaw, so the "included in OpenClaw" route means no separate npm or ClawHub install step is required — the package is present once OpenClaw is installed. To identify or audit it, look for the `@openclaw/imessage` package name in the OpenClaw plugin inventory.

## Surface

The plugin contributes one surface:

```
channels: imessage
```

This declares a chat **channel** named `imessage`. Enabling the plugin makes the iMessage channel available to the OpenClaw gateway for sending and receiving OpenClaw messages over iMessage. The deeper per-channel configuration (how to connect, authenticate, and route messages) is documented on the related channel page below — the surface key here is only the identity of what the plugin registers.

**Source**: OpenClaw documentation — `plugins/reference/imessage` (mirror `inbox/openclaw_docs/plugins/reference/imessage.md`)
**Last Updated**: 2026-06-22
**Status**: Active
