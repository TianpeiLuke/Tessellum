---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - feishu
keywords:
  - openclaw feishu plugin
  - feishu lark channel
  - "@openclaw/feishu"
  - feishu channels contract
  - feishu tools skills surface
  - community plugin m1heng
  - npm clawhub install
  - plugin manifest card
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/feishu
access_control_group: ["general"]
---

# OpenClaw — Feishu Plugin Reference (`@openclaw/feishu`)

## Overview

This note is the plugin-manifest reference card for the OpenClaw **Feishu plugin** (`@openclaw/feishu`), a community-maintained extension (by `@m1heng`) that adds Feishu/Lark chats and workplace tooling to an OpenClaw gateway. It mirrors the `plugins/reference/feishu` source page: the one-line summary, the install-trigger `read_when`, the **Distribution** block (npm package identity + install route), and the **Surface** block (the typed contracts the plugin contributes — a `feishu` channel plus `tools` and `skills`). As a `model` (reference/record schema) note it captures the plugin's identity triple — package name, install route, and verbatim Surface declaration — and links out (rather than duplicating) to the matching `/channels/feishu` user page and the channel/skill concepts the contributions satisfy.

## Distribution

- Package: `@openclaw/feishu`
- Install route: npm; ClawHub

The plugin is **community-maintained** (by `@m1heng`), not bundled inside the OpenClaw monorepo. It is installed on demand through either the npm registry or ClawHub (the OpenClaw plugin marketplace), in contrast to bundled "included in OpenClaw" plugins that ship with the gateway. Its `read_when` trigger on the source page is: "You are installing, configuring, or auditing the feishu plugin."

## Surface

The plugin's Surface declaration, reproduced verbatim from the source page, is:

```
channels: feishu; contracts: tools; skills
```

This resolves to three contributed contracts:

- **`channels: feishu`** — registers a `feishu` channel, the chat-platform adapter that bridges Feishu/Lark conversations into the OpenClaw channel kernel so an agent can be reached over Feishu/Lark chats.
- **`contracts: tools`** — contributes agent-callable `tools` (function-calling tools) for the workplace-tooling capability described in the summary.
- **`skills`** — contributes `skills` (packaged agent capabilities) supporting the Feishu/Lark workplace-tools experience.

Per the summary, the plugin's purpose is "Feishu/Lark channel plugin for chats and workplace tools" — the `feishu` channel covers the chats side and the `tools` + `skills` contracts cover the workplace-tools side. No configuration keys, environment variables, or default values are listed on the source page (*not specified in source*); those belong to the linked `/channels/feishu` user page.

**Source**: OpenClaw documentation — `plugins/reference/feishu` (mirror `inbox/openclaw_docs/plugins/reference/feishu.md`)
**Last Updated**: 2026-06-22
**Status**: Active
