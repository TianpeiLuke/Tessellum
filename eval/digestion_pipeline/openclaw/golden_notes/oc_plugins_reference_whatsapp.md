---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw whatsapp plugin
  - whatsapp channel plugin
  - "@openclaw/whatsapp"
  - clawhub whatsapp install
  - whatsapp web chats
  - channels whatsapp surface
  - openclaw channel plugin reference
topics:
  - OpenClaw
  - Plugin Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/whatsapp
access_control_group: ["general"]
---

# OpenClaw — WhatsApp Channel Plugin Reference

## Overview

This note is the reference data sheet for the OpenClaw **WhatsApp channel plugin** — the bundled plugin that adds WhatsApp as a messaging channel so OpenClaw agents can converse over WhatsApp Web chats. It mirrors the `plugins/reference/whatsapp` source page, whose `summary` is "OpenClaw WhatsApp channel plugin for WhatsApp Web chats" and whose `read_when` cue is for when you are installing, configuring, or auditing the `whatsapp` plugin. The page is a one-screen plugin reference with three sections — Distribution (the npm package and install routes), Surface (the channel the plugin registers), and a Related docs pointer to the full `/channels/whatsapp` channel doc — and this note captures each verbatim while linking, not duplicating, the deeper channel and SDK material.

## Distribution

The plugin's package and install routes, copied verbatim from the source page:

- **Package**: `@openclaw/whatsapp`
- **Install route**: ClawHub: `clawhub:@openclaw/whatsapp`; npm

WhatsApp is one of the few plugin-reference entries that exposes **two distribution routes** rather than the usual bundled-only path: it can be installed from ClawHub via the `clawhub:@openclaw/whatsapp` reference, or from the npm registry as the `@openclaw/whatsapp` package. The source page does not specify a version, a bundled flag, or any further install flags for this plugin, so none are asserted here (*not specified in source*).

## Surface

The Surface block declares what the plugin registers into the OpenClaw runtime, copied verbatim from the source page:

- **channels**: `whatsapp`

The plugin's sole registered surface is the `channels` contract, and it contributes a single channel id, `whatsapp`. Registering a `channels` entry is how a plugin docks a new messaging platform into OpenClaw's channel layer; once registered, the `whatsapp` channel routes inbound WhatsApp Web messages into agent sessions and sends agent replies back out over the same channel. The source page does not enumerate any other contracts (no providers, no tools, no extractors) for this plugin — its surface is exactly the one `channels: whatsapp` entry.

**Source**: OpenClaw documentation — `plugins/reference/whatsapp` (mirror `inbox/openclaw_docs/plugins/reference/whatsapp.md`)
**Last Updated**: 2026-06-22
**Status**: Active
