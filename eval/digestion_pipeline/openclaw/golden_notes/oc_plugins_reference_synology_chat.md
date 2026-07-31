---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw synology chat plugin
  - synology-chat channel
  - "@openclaw/synology-chat"
  - synology chat channel surface
  - synology chat npm clawhub
  - synology chat direct messages
  - openclaw channel plugin install
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/synology-chat
access_control_group: ["general"]
---

# OpenClaw — Synology Chat Channel Plugin Reference

## Overview

This note is the install/configure/audit reference card for the OpenClaw **Synology Chat plugin** — the `@openclaw/synology-chat` package that adds the `channels: synology-chat` surface, letting OpenClaw send and receive messages over Synology Chat channels and direct messages. It mirrors the `plugins/reference/synology-chat` source page: the one-line summary, the **Distribution** (package name + install route), the **Surface** the plugin contributes, and the **Related docs** pointer to the conceptual Synology Chat channel guide. This is a thin plumbing/install reference; the deep channel-setup knowledge lives in the planned `/channels/synology-chat` guide it links out to, not here.

## Distribution

The plugin is published as the npm package **`@openclaw/synology-chat`**. Its install route is **npm; ClawHub** — it can be installed either from npm or from ClawHub (the OpenClaw plugin registry). The source page does not state any further install flags, version pins, or configuration keys beyond the package name and route.

## Surface

The plugin contributes a single channel surface: **`channels: synology-chat`**. This registers Synology Chat as a messaging channel on the OpenClaw gateway, enabling OpenClaw to operate as a Synology Chat bot across both Synology Chat channels and direct messages (per the summary). No other surfaces (providers/tools), config blocks, or environment variables are listed on the source card.

**Source**: OpenClaw documentation — `plugins/reference/synology-chat` (mirror `inbox/openclaw_docs/plugins/reference/synology-chat.md`)
**Last Updated**: 2026-06-22
**Status**: Active
