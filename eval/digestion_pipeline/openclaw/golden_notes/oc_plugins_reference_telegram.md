---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - telegram
keywords:
  - openclaw telegram plugin
  - telegram channel surface
  - "@openclaw/telegram"
  - included in openclaw
  - channels telegram contract
  - plugin reference card
  - telegram send receive messages
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/telegram
access_control_group: ["general"]
---

# OpenClaw — Telegram Plugin Reference Card

## Overview

This note captures the OpenClaw **Telegram plugin** reference card from the `plugins/reference/telegram` source page. The Telegram plugin adds the Telegram channel surface for sending and receiving OpenClaw messages. As a plugin-catalog card it carries three load-bearing facts — its npm package id, its install route, and the OpenClaw SDK **Surface** it contributes — and otherwise defers all depth to the deep channel feature page at `/channels/telegram`. The body below mirrors the source card's three H2 facets (Distribution, Surface, Related docs) verbatim; the deep channel behavior, configuration, and message-handling semantics belong to the Channels sub-plan, not here.

## Distribution

- Package: `@openclaw/telegram`
- Install route: included in OpenClaw

The plugin ships bundled with OpenClaw (no separate npm or ClawHub install step is listed on the card), so the Telegram channel is available once OpenClaw itself is installed and the channel is configured.

## Surface

The plugin contributes a single OpenClaw SDK surface:

- `channels: telegram`

That is, it registers the `telegram` channel adapter into OpenClaw's channels subsystem, enabling the gateway to send and receive messages over Telegram. No other contracts (no `tools`, `providers`, or `skills`) are declared on this reference card.

**Source**: OpenClaw documentation — `plugins/reference/telegram` (mirror `inbox/openclaw_docs/plugins/reference/telegram.md`)
**Last Updated**: 2026-06-22
**Status**: Active
