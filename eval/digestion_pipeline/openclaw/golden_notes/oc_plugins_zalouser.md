---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw zalouser plugin
  - zalo personal channel
  - zca-js personal account automation
  - channels.zalouser config
  - openclaw plugins install zalouser
  - channels login zalouser qr
  - dmpolicy pairing
  - zalouser agent tool actions
topics:
  - OpenClaw
  - Zalo Personal Plugin
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/zalouser
access_control_group: ["general"]
---

# OpenClaw — Zalo Personal (`zalouser`) Channel Plugin

## Overview

This note is the operator procedure for the bundled OpenClaw **Zalo Personal** channel plugin, whose channel id is `zalouser`. It mirrors the `plugins/zalouser` source page: the naming and account-suspension risk warning, the Gateway-process placement, the two install paths (npm and local-folder dev), the `channels.zalouser` configuration, the channel CLI commands (QR login/logout/status/message-send/directory-peers), and the `zalouser` agent tool actions. The plugin provides Zalo Personal support for OpenClaw by using native `zca-js` to automate a normal Zalo user account.

## Naming

The channel id is `zalouser` to make it explicit that this **automates a personal Zalo user account** (unofficial). The source notes that `zalo` is kept reserved for a potential future official Zalo API integration, so the `user` suffix disambiguates the unofficial personal-account path from any future official integration.

> **Warning (from source):** Unofficial automation may lead to account suspension or ban. Use at your own risk.

## Where it runs

The plugin runs **inside the Gateway process**. If you use a remote Gateway, install and configure it on the **machine running the Gateway**, then restart the Gateway. No external `zca`/`openzca` CLI binary is required.

## Install

The source documents two install options. After either option, restart the Gateway afterwards.

### Option A: install from npm

Install the bundled package by name:

```bash
openclaw plugins install @openclaw/zalouser
```

Per the source, use the bare package to follow the current official release tag, and pin an exact version only when you need a reproducible install. Restart the Gateway afterwards.

### Option B: install from a local folder (dev)

For local development, install from a local folder and install its dependencies with `pnpm`:

```bash
PLUGIN_SRC=./path/to/local/zalouser-plugin
openclaw plugins install "$PLUGIN_SRC"
cd "$PLUGIN_SRC" && pnpm install
```

Restart the Gateway afterwards.

## Config

Channel config lives under `channels.zalouser` (the source explicitly notes this is **not** `plugins.entries.*`):

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

The two documented config keys are `enabled` (set `true` to turn the channel on) and `dmPolicy` (set to `"pairing"` in the example). No other config keys are documented for this channel — *(inferred — only `enabled` and `dmPolicy` appear in the source example; defaults for other fields are not specified in source)*.

## CLI

The channel exposes the following CLI commands (verbatim from source):

```bash
openclaw channels login --channel zalouser
openclaw channels logout --channel zalouser
openclaw channels status --probe
openclaw message send --channel zalouser --target <threadId> --message "Hello from OpenClaw"
openclaw directory peers list --channel zalouser --query "name"
```

`channels login --channel zalouser` performs the login of the personal account; `channels logout --channel zalouser` ends that session; `channels status --probe` probes channel status; `message send` posts a message to a target thread (`--target <threadId>`) with `--message`; and `directory peers list` lists channel peers filtered by `--query`. Note that `channels status --probe` is written in the source without an explicit `--channel zalouser` flag.

## Agent tool

The plugin registers an agent tool with the name `zalouser`. Its documented actions are: `send`, `image`, `link`, `friends`, `groups`, `me`, `status`. The source also states that channel message actions support `react` for message reactions.

**Source**: OpenClaw documentation — `plugins/zalouser` (mirror `inbox/openclaw_docs/plugins/zalouser.md`)
**Last Updated**: 2026-06-22
**Status**: Active
