---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw matrix plugin
  - openclaw mattermost plugin
  - channels matrix
  - channels mattermost
  - clawhub openclaw matrix package
  - openclaw mattermost package
  - chat channel plugin install
  - matrix rooms direct messages
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/matrix
access_control_group: ["general"]
---

# OpenClaw — Matrix & Mattermost Channel Plugins

## Overview

This note is the install/enable procedure card for the two `m*` chat-channel plugins in the OpenClaw plugin reference: **Matrix** (`@openclaw/matrix`) and **Mattermost** (`@openclaw/mattermost`). Both register the `channels:` capability surface — the surface that bridges an external chat platform's rooms and messages into the OpenClaw agent gateway. It mirrors the `plugins/reference/matrix` and `plugins/reference/mattermost` inventory cards, consolidating their `## Distribution`, `## Surface`, and `## Related docs` sections per plugin: the npm package name, the install route (ClawHub/npm vs included-in-OpenClaw), the `channels:` id each registers, and a pointer to the channel deep-dive. These are inventory cards — the operational connection/config detail (auth, room mapping, encryption) lives in the `channels/matrix` and `channels/mattermost` deep-dive pages, not here.

## Matrix Plugin

The Matrix plugin is the "OpenClaw Matrix channel plugin for rooms and direct messages."

- **Package**: `@openclaw/matrix`
- **Install route**: ClawHub: `clawhub:@openclaw/matrix`; npm
- **Surface**: `channels: matrix`

Matrix is **not** included in OpenClaw by default — it is installed from ClawHub via the `clawhub:@openclaw/matrix` identifier, or alternatively from npm. Once installed and enabled, the plugin registers the `matrix` entry under the `channels:` surface, attaching OpenClaw to Matrix rooms and direct messages so messages on those Matrix conversations are routed through the agent gateway. The `## Related docs` pointer on the card is the `/channels/matrix` deep-dive page (owned by sub-plan `ch03`), which carries the platform-specific connection, room, and DM configuration.

## Mattermost Plugin

The Mattermost plugin "Adds the Mattermost channel surface for sending and receiving OpenClaw messages."

- **Package**: `@openclaw/mattermost`
- **Install route**: included in OpenClaw
- **Surface**: `channels: mattermost`

Mattermost is **included in OpenClaw**, so no separate ClawHub or npm install step is needed — the package ships with OpenClaw and is enabled through the channel configuration. Enabling it registers the `mattermost` entry under the `channels:` surface, adding a send/receive bridge for OpenClaw messages on a Mattermost workspace. The `## Related docs` pointer on the card is the `/channels/mattermost` deep-dive page (owned by sub-plan `ch03`) for the workspace connection and channel binding detail.

## Capability Surface and Install-Route Contrast

Both plugins register the same capability *kind* — the `channels:` surface — which is how OpenClaw onboards an external chat platform as a messaging channel. The durable distinction between the two cards is the **install route**: Mattermost is bundled (`included in OpenClaw`), while Matrix is an external plugin pulled from ClawHub (`clawhub:@openclaw/matrix`) or npm. The capability-surface mapping is the load-bearing content of each card — `@openclaw/matrix → channels: matrix` and `@openclaw/mattermost → channels: mattermost` — with the deep operational configuration deferred to the `channels/*` deep-dives, not duplicated in these inventory entries.

**Source**: OpenClaw documentation — `plugins/reference/matrix` + `plugins/reference/mattermost` (mirror `inbox/openclaw_docs/plugins/reference/matrix.md`, `mattermost.md`)
**Last Updated**: 2026-06-22
**Status**: Active
