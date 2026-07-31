---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw sms plugin
  - "@openclaw/sms"
  - twilio sms channel
  - channels sms surface
  - included in openclaw
  - sms channel plugin
  - text message channel
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/sms
access_control_group: ["general"]
---

# OpenClaw — SMS Plugin Reference (`@openclaw/sms`)

## Overview

This is the install/configure/audit reference card for the OpenClaw **SMS plugin**, mirroring the `plugins/reference/sms` source page. The plugin is the Twilio SMS channel plugin for OpenClaw text messages: it adds a `channels: sms` surface so OpenClaw can send and receive text messages over a Twilio-backed SMS number. It ships as the npm package `@openclaw/sms` and is included in OpenClaw (no separate install needed). The source page lists exactly three operational facts — Distribution (package + install route), Surface (the channel it contributes), and a Related docs pointer to the conceptual `/channels/sms` setup guide — and this note reproduces those facts faithfully. The deep channel setup (Twilio credentials, inbound webhook wiring, behavior config) is NOT reproduced here; it lives in the conceptual SMS channel guide this card links out to.

## Distribution

- Package: `@openclaw/sms`
- Install route: **included in OpenClaw** — the plugin ships with OpenClaw, so it is loaded at the gateway without a separate npm or ClawHub install step. ("Twilio" names the SMS-delivery backend the channel rides on; it is described inline here because the source page states only the plugin's package and install route, not Twilio account configuration — that is owned by the conceptual `/channels/sms` guide.)

## Surface

The plugin contributes a single channel surface:

`channels: sms`

This registers a Twilio-backed SMS channel so OpenClaw can answer and originate text messages addressed to a phone number, behaving as an SMS bot. Inbound texts arrive as a Twilio webhook to the gateway and are dispatched into the agent loop; outbound replies are sent back over the same SMS surface. The source page documents no other surfaces, env vars, or configuration keys.

**Source**: OpenClaw documentation — `plugins/reference/sms` (mirror `inbox/openclaw_docs/plugins/reference/sms.md`)
**Last Updated**: 2026-06-22
**Status**: Active
