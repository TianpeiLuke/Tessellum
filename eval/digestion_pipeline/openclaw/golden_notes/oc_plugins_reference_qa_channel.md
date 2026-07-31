---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - qa_channel
keywords:
  - openclaw qa-channel plugin
  - qa channel surface
  - "@openclaw/qa-channel"
  - channels contract
  - source checkout only plugin
  - send receive openclaw messages
  - channel test scenarios
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/qa-channel
access_control_group: ["general"]
---

# OpenClaw — QA Channel Plugin Reference

## Overview

This note models the **QA Channel plugin** as cataloged on the OpenClaw `plugins/reference/qa-channel` reference page (mirror `inbox/openclaw_docs/plugins/reference/qa-channel.md`). It is a terse plugin-reference card describing one bundled-tree plugin: its npm package, install route, the channel surface it contributes, and a link-out to the fuller channel documentation. The QA Channel plugin "adds the QA Channel surface for sending and receiving OpenClaw messages" — a `qa-channel` channel surface intended for sending/receiving OpenClaw messages in test/QA scenarios. As a plugin/contract descriptor (package → contributed `channels` contract), it is captured as a `model` note; this card records the descriptor and links the canonical `channels/qa-channel` page rather than re-digesting it.

## Distribution

The QA Channel plugin is distributed as a single npm-scoped package with a restricted install route:

- **Package:** `@openclaw/qa-channel`
- **Install route:** source checkout only

The "source checkout only" install route means the plugin is not published for the standard install paths (it is obtained by checking out the OpenClaw source tree), distinguishing it from the npm/ClawHub-installable provider plugins in the same reference cluster. *(The page states only the package name and the source-checkout install route; it does not specify a ClawHub listing or version constraints — Not specified in source.)*

## Surface

The plugin contributes a single contract surface to OpenClaw:

- `channels: qa-channel`

That is, the plugin registers a **channel** named `qa-channel` against OpenClaw's `channels` contract. A channel surface is the integration point through which OpenClaw sends and receives messages; the `qa-channel` surface exposes exactly the send/receive message path used in test and QA scenarios per the card's one-line summary. The page declares no providers, tools, or other contracts for this plugin — its only surface is the one `qa-channel` channel.

**Source**: OpenClaw documentation — `plugins/reference/qa-channel` (mirror `inbox/openclaw_docs/plugins/reference/qa-channel.md`)
**Last Updated**: 2026-06-22
**Status**: Active
