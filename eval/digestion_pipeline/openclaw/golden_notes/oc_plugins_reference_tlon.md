---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw tlon plugin
  - tlon urbit channel
  - "@openclaw/tlon"
  - tlon channel plugin
  - channels tlon skills surface
  - npm clawhub install route
  - openclaw plugin reference card
  - urbit chat channel
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/tlon
access_control_group: ["general"]
---

# OpenClaw — Tlon Plugin Reference Card

## Overview

This note captures the OpenClaw **Tlon plugin** reference card from the `plugins/reference/tlon` source page: a one-per-plugin catalog entry describing the OpenClaw Tlon/Urbit channel plugin for chat workflows. Like every plugin-reference card, it carries exactly three load-bearing facts — its **Distribution** (npm package id and install route), its **Surface** (the OpenClaw SDK contracts/channels/providers/skills the plugin contributes), and a **Related docs** pointer to the deep feature page. The card itself is intentionally terse; the full Tlon channel behavior lives at the deep `/channels/tlon` channel page (owned by the Channels sub-plan), which this reference card merely fronts.

## Distribution

- Package: `@openclaw/tlon`
- Install route: npm; ClawHub

Unlike the bundled plugins that ship inside OpenClaw, Tlon is **not included by default** — it is installed from npm or via ClawHub, the OpenClaw plugin marketplace. The package id `@openclaw/tlon` is the manifest's package identifier under the `@openclaw` scope.

## Surface

The card declares the surface as: `channels: tlon; skills`.

The Tlon plugin contributes a **`channels` SDK contract** — registering the `tlon` channel, which bridges the Tlon/Urbit chat platform to the agent harness so messages can be sent and received as a conversation channel — and additionally contributes **`skills`** (agent-callable skill contributions bundled with the plugin). The `channels: tlon` entry is the channel adapter the plugin registers; the `skills` entry indicates the plugin also ships one or more skills alongside the channel surface.

**Source**: OpenClaw documentation — `plugins/reference/tlon` (mirror `inbox/openclaw_docs/plugins/reference/tlon.md`)
**Last Updated**: 2026-06-22
**Status**: Active
