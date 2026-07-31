---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw irc plugin
  - "@openclaw/irc"
  - channels irc surface
  - irc chat channel
  - bundled openclaw plugin
  - irc plugin distribution
  - irc plugin install route
  - openclaw plugin reference card
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/irc
access_control_group: ["general"]
---

# OpenClaw — IRC Plugin Reference Card

## Overview

This note is the catalog reference card for the OpenClaw **IRC plugin**, mirroring the `plugins/reference/irc` source page. The card summarizes one shippable OpenClaw plugin along three load-bearing axes — its **Distribution** (the npm package name and how it is installed), the **Surface** it contributes to the gateway (the `channels: irc` chat channel), and a **Related docs** pointer to the deeper channel page. Per the source summary, the plugin "Adds the IRC channel surface for sending and receiving OpenClaw messages." This is the thin catalog layer above the richer `/channels/irc` page; it tells you how to identify and audit the plugin and where to go for full channel configuration, but it does not itself document IRC connection setup, auth, or message routing.

## Distribution

- **Package:** `@openclaw/irc`
- **Install route:** included in OpenClaw

The IRC plugin ships **bundled** with OpenClaw — its install route is "included in OpenClaw," meaning it does not require a separate `npm` install or a ClawHub fetch to be present in a standard OpenClaw deployment. To identify or audit the plugin you look for the `@openclaw/irc` package name. *(No version number, configuration key, or enablement flag is given on the source card; the source specifies only the package name and the bundled install route.)*

## Surface

```
channels: irc
```

The plugin contributes the **`channels: irc`** surface. In OpenClaw's plugin model a chat-channel plugin declares a `channels:` surface key; here that key is `irc`, registering IRC as one of the chat platforms the gateway can send to and receive from. This is the single surface this card declares — a channel surface, not a model `provider` or a `speechProviders` contract.

**Source**: OpenClaw documentation — `plugins/reference/irc` (mirror `inbox/openclaw_docs/plugins/reference/irc.md`)
**Last Updated**: 2026-06-22
**Status**: Active
