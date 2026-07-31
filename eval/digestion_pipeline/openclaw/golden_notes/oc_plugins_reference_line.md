---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw line plugin
  - line bot api channel
  - "@openclaw/line"
  - channels line surface
  - line chat channel plugin
  - npm clawhub install route
  - openclaw plugin reference
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/line
access_control_group: ["general"]
---

# OpenClaw — LINE Plugin Reference Card

## Overview

This note captures the OpenClaw **LINE plugin** reference card from the `plugins/reference/line` source page: a catalog stub describing one shippable OpenClaw plugin that adds a LINE chat channel for LINE Bot API chats. It records the three load-bearing catalog facts — the npm **package name** (`@openclaw/line`), the **install route** (npm; ClawHub), and the exact **surface** the plugin contributes (`channels: line`) — plus the pointer to the deeper channel page. This is the thin catalog layer above the richer `/channels/line` page (owned by the channels sub-plan) and the code-side `repo_openclaw_channels*` notes; the procedure here is how to identify, install, and audit the LINE channel plugin, not how to configure the channel itself.

## Distribution

The plugin ships as the npm package **`@openclaw/line`**. Its install route is **npm; ClawHub** — i.e. it is not bundled with OpenClaw and is installed from the npm registry or via ClawHub, OpenClaw's plugin distribution surface. To identify or audit an installed instance, look for the `@openclaw/line` package in the plugin install material; to add it, install the package through the npm or ClawHub install path rather than relying on a bundled copy.

## Surface

The plugin contributes a single channel surface: **`channels: line`**. Enabling the plugin docks the LINE platform into the OpenClaw messaging gateway as the `line` channel, through which OpenClaw sends and receives messages over the LINE Bot API. The card declares only this surface key — it adds no model `provider` and no `speechProviders` contract.

**Source**: OpenClaw documentation — `plugins/reference/line` (mirror `inbox/openclaw_docs/plugins/reference/line.md`)
**Last Updated**: 2026-06-22
**Status**: Active
