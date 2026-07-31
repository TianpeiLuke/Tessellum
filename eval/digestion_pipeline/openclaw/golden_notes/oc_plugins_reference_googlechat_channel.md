---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw googlechat plugin
  - google chat channel plugin
  - "@openclaw/googlechat"
  - channels googlechat surface
  - install googlechat npm clawhub
  - google chat spaces direct messages
  - channel plugin install card
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/googlechat
access_control_group: ["general"]
---

# OpenClaw — Google Chat Channel Plugin (`@openclaw/googlechat`)

## Overview

This note is the plugin-inventory procedure for the OpenClaw **Google Chat channel plugin** — the `@openclaw/googlechat` package that wires the OpenClaw agent into Google Chat **spaces and direct messages**, registering the `channels: googlechat` surface. It mirrors the `plugins/reference/googlechat` reference card and covers exactly what an operator needs from that card: the npm package name, the install route, the capability surface the plugin registers, and the pointer to the channel deep-dive. The card is a thin "what package provides what capability" entry; the substantive channel configuration (auth, ingress, message routing) lives on the `/channels/googlechat` deep-dive page (owned elsewhere) and is linked, not duplicated, here.

## Distribution

The plugin ships as the npm package **`@openclaw/googlechat`**. Per the source card, the install route is **npm; ClawHub** — i.e. it is not bundled into OpenClaw and is installed on demand from either the npm registry or ClawHub. To enable it, install the `@openclaw/googlechat` package through the plugin install path (npm install or the ClawHub install route) so the OpenClaw extension framework loads it and exposes its registered surface. Specific configuration keys, credentials, and ingress setup are **not specified in this source card** — they are documented on the `/channels/googlechat` deep-dive.

## Surface

Once installed, the plugin registers the channel surface **`channels: googlechat`** with the host gateway. That surface makes the OpenClaw agent reachable in Google Chat as a conversational participant across the two contexts the card names — **spaces** (multi-party rooms) and **direct messages** (one-to-one conversations). Registering `channels: googlechat` is the channel-plugin analog of a provider plugin registering `providers:` ids or a tool plugin registering a `contracts: tools` surface — the same plugin-registration mechanism, declaring a `channels:` surface rather than a model or tool surface. No additional contracts are declared on this card.

**Source**: OpenClaw documentation — `plugins/reference/googlechat` (mirror `inbox/openclaw_docs/plugins/reference/googlechat.md`)
**Last Updated**: 2026-06-22
**Status**: Active
