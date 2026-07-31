---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - signal
keywords:
  - openclaw signal plugin
  - "@openclaw/signal package"
  - signal channel surface
  - channels signal
  - included in openclaw
  - signal messaging plugin
  - install configure audit signal
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/signal
access_control_group: ["general"]
---

# OpenClaw — Signal Plugin Reference

## Overview

This note is the install/configure/audit reference card for the OpenClaw **Signal plugin**, mirroring the `plugins/reference/signal` source page. Its one-line summary is that it "Adds the Signal channel surface for sending and receiving OpenClaw messages," and its stated `read_when` audience is "You are installing, configuring, or auditing the signal plugin." The page is a thin three-section reference card — **Distribution** (the npm package and install route), **Surface** (the capability the plugin contributes), and **Related docs** (the pointer to the conceptual channel guide). The deep Signal channel setup is owned by the `/channels/signal` guide and is linked, not reproduced here.

## Distribution

- **Package:** `@openclaw/signal`
- **Install route:** included in OpenClaw

The Signal plugin ships as the npm-scoped package `@openclaw/signal` and is **included in OpenClaw** — it is a built-in/bundled plugin loaded at gateway start rather than one installed separately via npm or ClawHub. No additional install command, version, or configuration key is given on the source card.

## Surface

```
channels: signal
```

The plugin contributes a single capability surface: a **`channels:` surface** named `signal`. This makes it a channel adapter — it registers the `signal` channel with OpenClaw so the agent can send and receive messages over Signal. The card does not enumerate channel configuration fields, credentials, or runtime options; those belong to the conceptual channel guide.

**Source**: OpenClaw documentation — `plugins/reference/signal` (mirror `inbox/openclaw_docs/plugins/reference/signal.md`)
**Last Updated**: 2026-06-22
**Status**: Active
