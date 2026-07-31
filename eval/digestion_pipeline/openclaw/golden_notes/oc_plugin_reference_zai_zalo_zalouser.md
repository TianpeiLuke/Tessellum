---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw zai plugin
  - openclaw zalo plugin
  - openclaw zalouser plugin
  - openclaw zai-provider package
  - zalo channel plugin clawhub
  - zalouser zca-js personal account
  - plugin manifest distribution surface
  - mediaunderstandingproviders contract
topics:
  - OpenClaw
  - Plugin Reference Manifests
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/zai
access_control_group: ["general"]
---

# OpenClaw — Plugin Manifest Reference: Z.AI, Zalo, Zalo Personal

## Overview

This note models the **plugin-manifest reference** for three OpenClaw plugins — **Z.AI** (a model provider), **Zalo** (a bot/webhook chat channel), and **Zalo Personal** (a personal-account chat channel) — consolidating the three micro-stub reference pages `plugins/reference/zai`, `plugins/reference/zalo`, and `plugins/reference/zalouser`. Each source page is a manifest stub carrying exactly three sections — **Distribution** (npm package + install route), **Surface** (the declared providers / channels / contracts), and **Related docs** (pointers into the substantive provider/channel docs) — so this note renders all three as one lossless package→install-route→surface→target reference table plus per-plugin notes. It documents what each plugin ships, how it is installed, what runtime surface it registers, and where to find its full configuration; the substantive provider/channel behaviour itself lives in the linked `/providers/zai` and `/channels/zalo` / `/channels/zalouser` docs and is not duplicated here.

## Manifest Summary Table

The three pages are reference manifests only (Distribution / Surface / Related docs). The full manifest is:

| Plugin | Package | Install route | Surface (providers / channels) | Contracts | Related docs |
|---|---|---|---|---|---|
| Z.AI plugin | `@openclaw/zai-provider` | included in OpenClaw | `providers: zai` | `mediaUnderstandingProviders` | `/providers/zai` |
| Zalo plugin | `@openclaw/zalo` | npm; ClawHub | `channels: zalo` | *(none declared)* | `/channels/zalo` |
| Zalo Personal plugin | `@openclaw/zalouser` | npm; ClawHub | `channels: zalouser` | `tools` | `/channels/zalouser`, `/plugins/zalouser` |

## Z.AI Plugin

The **Z.AI plugin** "Adds Z.AI model provider support to OpenClaw." Its **Distribution** is package `@openclaw/zai-provider`, with install route "included in OpenClaw" (it ships with the gateway rather than being installed separately). Its **Surface** declares `providers: zai` and `contracts: mediaUnderstandingProviders` — i.e. it registers the `zai` model provider and implements the `mediaUnderstandingProviders` contract. Its **Related docs** point to `/providers/zai` for the substantive provider configuration. This is the only one of the three plugins shipped bundled (the other two are external installs).

## Zalo Plugin

The **Zalo plugin** is the "OpenClaw Zalo channel plugin for bot and webhook chats." Its **Distribution** is package `@openclaw/zalo`, with install route "npm; ClawHub" (installable from the npm registry or via ClawHub). Its **Surface** declares `channels: zalo` and declares no `contracts`. Its **Related docs** point to `/channels/zalo` for the substantive channel configuration. This is the bot/webhook-style Zalo channel (as distinct from the personal-account variant below).

## Zalo Personal Plugin

The **Zalo Personal plugin** is the "OpenClaw Zalo Personal Account plugin via native zca-js integration" — it connects a personal Zalo account using the native `zca-js` library rather than the official bot/webhook API. Its **Distribution** is package `@openclaw/zalouser`, with install route "npm; ClawHub". Its **Surface** declares `channels: zalouser` and `contracts: tools` (it registers the `zalouser` channel and contributes a `tools` contract). Its **Related docs** point to both `/channels/zalouser` and `/plugins/zalouser` for the substantive channel and plugin documentation.

**Source**: OpenClaw documentation — `plugins/reference/zai`, `plugins/reference/zalo`, `plugins/reference/zalouser` (mirrors `inbox/openclaw_docs/plugins/reference/{zai,zalo,zalouser}.md`)
**Last Updated**: 2026-06-22
**Status**: Active
