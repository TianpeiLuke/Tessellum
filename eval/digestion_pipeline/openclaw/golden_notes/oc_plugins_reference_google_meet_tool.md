---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw google meet plugin
  - "@openclaw/google-meet"
  - google meet participant plugin
  - contracts tools plugin
  - chrome twilio transport
  - meeting participant tool
  - join call agent
  - npm clawhub install plugin
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/google-meet
access_control_group: ["general"]
---

# OpenClaw — Google Meet Participant Plugin (`@openclaw/google-meet`)

## Overview

This note is the install/enable procedure card for the OpenClaw **Google Meet** participant plugin, sourced from the `plugins/reference/google-meet` inventory page. The source describes it verbatim as the "OpenClaw Google Meet participant plugin for joining calls through Chrome or Twilio transports." It is a meeting-participant *tool* plugin: installing and enabling the `@openclaw/google-meet` package registers the `tools` contract so the agent can join and participate in Google Meet calls. This card captures the durable inventory mapping — npm-package → install route → registered capability surface → deep-dive pointer — and does NOT duplicate the configuration detail of the `/plugins/google-meet` deep-dive (owned by sub-plan pl03).

## Distribution (install route)

To make the Google Meet participant available to the agent, install the plugin package and let OpenClaw resolve its registered surface:

- **Package**: `@openclaw/google-meet`
- **Install route**: npm; ClawHub

Unlike the built-in `g*` model providers (GitHub Copilot, Google), the Google Meet plugin is *not* included in OpenClaw by default — it is distributed externally and installed on demand. The two routes are equivalent ways to obtain the same package: install from the public npm registry, or install through ClawHub (the OpenClaw plugin distribution channel). Specific install flags, ClawHub coordinate syntax, and version pinning are not specified on this inventory card — those belong to the install procedure and the `/plugins/google-meet` deep-dive.

## Surface (registered capability)

The plugin registers exactly one capability contract:

- **contracts**: `tools`

Registering the `tools` contract means the plugin contributes one or more agent-callable tools (here, the meeting-participant tool) into OpenClaw's tool surface; the agent invokes them through function calling. This is distinct from the `g*` model-provider cards (which register a `providers:` surface) and from the Google Chat card (which registers a `channels:` surface). The two transports named in the source summary — **Chrome** and **Twilio** — are the mechanisms by which the registered tool joins a call: Chrome drives a browser session to join the Meet UI, while Twilio joins via a voice-call/telephony path. The card does not specify per-transport configuration, credentials, or selection logic; those details live in the deep-dive page below.

**Source**: OpenClaw documentation — `plugins/reference/google-meet` (mirror `inbox/openclaw_docs/plugins/reference/google-meet.md`)
**Last Updated**: 2026-06-22
**Status**: Active
