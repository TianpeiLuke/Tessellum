---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw twitch plugin
  - "@openclaw/twitch"
  - twitch channel plugin
  - chat and moderation workflows
  - channels twitch surface
  - npm clawhub install route
  - plugin descriptor card
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/twitch
access_control_group: ["general"]
---

# OpenClaw — Twitch Plugin (`@openclaw/twitch`)

## Overview

This note describes the `@openclaw/twitch` plugin descriptor as documented on the `plugins/reference/twitch` source page. The page is a uniform plugin-reference card stating the plugin's identity: OpenClaw's Twitch channel plugin for chat and moderation workflows, the npm + ClawHub install route, and the contract surface it registers (`channels: twitch`), with a pointer to the deeper Twitch channel doc. The card states the package + surface only; the deeper channel behavior is documented by the Twitch channel doc this card links rather than redefines.

## Distribution

The page documents the plugin's packaging and how to obtain it:

- **Package:** `@openclaw/twitch`
- **Install route:** npm; ClawHub

This is an npm-distributed plugin also published to ClawHub (OpenClaw's plugin marketplace) — it is not bundled "included in OpenClaw", so it is installed/added rather than shipping in the core distribution.

## Surface

The plugin registers the following contract surface:

```
channels: twitch
```

The `channels: twitch` line is the load-bearing fact of the card: it states that the plugin adds a Twitch channel capability under the `channels` contract. Registering this surface makes Twitch available as a messaging channel for the gateway, supporting the chat and moderation workflows described in the page header. The card scopes its claim to the surface identity; the channel's runtime behavior is the subject of the deeper Twitch channel doc below.

**Source**: OpenClaw documentation — `plugins/reference/twitch` (mirror `inbox/openclaw_docs/plugins/reference/twitch.md`)
**Last Updated**: 2026-06-22
**Status**: Active
