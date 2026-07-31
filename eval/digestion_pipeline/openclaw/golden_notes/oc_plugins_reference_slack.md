---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw slack plugin
  - "@openclaw/slack package"
  - slack channel surface
  - channels slack
  - slack channels dms commands app events
  - install npm clawhub
  - slack plugin reference card
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/slack
access_control_group: ["general"]
---

# OpenClaw — Slack Plugin (Reference)

## Overview

This note is the install/configure/audit reference card for the OpenClaw **Slack channel plugin**, mirroring the `plugins/reference/slack` source page. The plugin is the **OpenClaw Slack channel plugin for channels, DMs, commands, and app events**. It ships as the npm package `@openclaw/slack` and installs via **npm** or **ClawHub**. The plugin contributes the `channels: slack` surface — a messaging-channel capability that lets OpenClaw operate inside Slack channels, direct messages, slash commands, and Slack app events. The deep conceptual setup (tokens, Socket Mode vs webhooks, app installation, routing) lives in the `/channels/slack` channel guide, which this card points to under Related docs; it is linked, not reproduced here.

## Distribution

- **Package:** `@openclaw/slack`
- **Install route:** npm; ClawHub

The plugin is distributed as the scoped npm package `@openclaw/slack` and can be installed either from npm directly or from ClawHub (the OpenClaw plugin registry). The source page lists no further install commands, version pins, or configuration keys for this card.

## Surface

```
channels: slack
```

The plugin adds a single capability — the `channels: slack` surface. Registering this surface makes Slack a messaging channel for OpenClaw, covering the Slack channels, DMs, commands, and app events called out in the page summary. The source page does not enumerate per-feature config beyond this surface declaration.

**Source**: OpenClaw documentation — `plugins/reference/slack` (mirror `inbox/openclaw_docs/plugins/reference/slack.md`)
**Last Updated**: 2026-06-22
**Status**: Active
