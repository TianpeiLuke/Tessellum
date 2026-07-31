---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw discord plugin
  - "@openclaw/discord"
  - discord channel plugin
  - channels discord contract
  - transcriptsourceproviders contract
  - clawhub install discord
  - discord dms commands app events
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/discord
access_control_group: ["general"]
---

# OpenClaw — Discord Channel Plugin Reference

## Overview

This note is the reference card for the `@openclaw/discord` channel plugin, mirroring the `plugins/reference/discord` source page. The plugin connects OpenClaw to Discord channels, DMs, commands, and app events. It documents the plugin's distribution (npm package name and install routes) and its declared surface (the channel and contract IDs it provides), and points to the full Discord channel feature doc rather than reproducing it. As one card in the `plugins/reference/` catalog, it is the identity layer that the richer `channels/discord` doc and the channels code repos reference.

## Distribution

- Package: `@openclaw/discord`
- Install route: npm; ClawHub

The plugin is distributed as the npm package `@openclaw/discord` and is installable via npm or through ClawHub (OpenClaw's plugin registry/install route). The source page does not list a default-bundled status for this plugin, so it is treated as a separately installable extension rather than one "included in OpenClaw".

## Surface

The plugin's declared surface is `channels: discord; contracts: transcriptSourceProviders`. It registers a `discord` channel (the channel adapter that bridges OpenClaw to the Discord platform — channels, DMs, commands, and app events as summarized on the source page) and implements the `transcriptSourceProviders` contract (a provider that supplies transcript/message-source content from the connected Discord channels). These two surface entries are the load-bearing facts of the card: a channel registration plus a contract implementation.

**Source**: OpenClaw documentation — `plugins/reference/discord` (mirror `inbox/openclaw_docs/plugins/reference/discord.md`)
**Last Updated**: 2026-06-22
**Status**: Active
