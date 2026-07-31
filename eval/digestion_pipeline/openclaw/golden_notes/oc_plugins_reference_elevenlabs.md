---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - speech
keywords:
  - openclaw elevenlabs plugin
  - elevenlabs-speech package
  - speechProviders contract
  - realtimeTranscriptionProviders
  - mediaUnderstandingProviders
  - text-to-speech provider
  - realtime transcription provider
  - bundled openclaw plugin
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/elevenlabs
access_control_group: ["general"]
---

# OpenClaw — Elevenlabs Plugin Reference Card

## Overview

This note is the plugin-manifest reference card for the OpenClaw **`@openclaw/elevenlabs-speech`** plugin, mirroring the `plugins/reference/elevenlabs` source page. As a reference/record schema (model BB), it captures the plugin's identity triple — its npm package name, its install route, and the exact typed contracts it registers on the OpenClaw extension surface. The plugin adds media understanding, realtime transcription, and text-to-speech provider support, registering the `mediaUnderstandingProviders`, `realtimeTranscriptionProviders`, and `speechProviders` contracts. You read this page when you are installing, configuring, or auditing the elevenlabs plugin; the consumer-facing capability docs live on the linked `/providers/elevenlabs` user page rather than here.

## Distribution

The plugin's package and install route, copied verbatim from the source card:

- Package: `@openclaw/elevenlabs-speech`
- Install route: included in OpenClaw

"Included in OpenClaw" means the plugin is **bundled** with the OpenClaw monorepo rather than installed separately from npm or ClawHub — it ships and loads with the gateway, with no per-plugin install step required.

## Surface

The Surface block declares the typed OpenClaw extension contracts this plugin contributes, reproduced verbatim:

```
contracts: mediaUnderstandingProviders, realtimeTranscriptionProviders, speechProviders
```

These three contracts map to the plugin's one-line summary — "Adds media understanding provider support. Adds realtime transcription provider support. Adds text-to-speech provider support." — as follows:

- **`mediaUnderstandingProviders`** — media understanding provider support (analyzing/understanding audio and other media inputs).
- **`realtimeTranscriptionProviders`** — realtime transcription provider support (the low-latency streaming speech-to-text side of the plugin).
- **`speechProviders`** — text-to-speech provider support (synthesizing ElevenLabs voice audio from text).

The card declares no providers, channels, or skills contracts and no configuration keys beyond these three provider contracts; nothing further is specified in source.

**Source**: OpenClaw documentation — `plugins/reference/elevenlabs` (mirror `inbox/openclaw_docs/plugins/reference/elevenlabs.md`)
**Last Updated**: 2026-06-22
**Status**: Active
