---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - speech
keywords:
  - openclaw azure-speech plugin
  - azure ai speech text-to-speech
  - speechProviders contract
  - native ogg opus voice notes
  - pcm telephony tts
  - mp3 voice output
  - included in openclaw plugin
  - openclaw azure-speech distribution
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/azure-speech
access_control_group: ["general"]
---

# OpenClaw — Azure Speech Plugin (`@openclaw/azure-speech`)

## Overview

This note is the plugin-reference card for OpenClaw's **Azure Speech plugin**, mirroring the `plugins/reference/azure-speech` source page. The plugin provides **Azure AI Speech text-to-speech (TTS)** and, per the page summary, supports three output forms: **MP3, native Ogg/Opus voice notes, and PCM telephony**. It captures the plugin's identity tuple — its distribution package and install route, the runtime surface it contributes (a `speechProviders` contract), and the pointer to the corresponding provider doc — without redefining the TTS provider concept itself, which lives in its own `/providers/azure-speech` doc.

## Distribution

The plugin's distribution package and install route, copied verbatim from the source page's `## Distribution` section:

- **Package**: `@openclaw/azure-speech`
- **Install route**: **included in OpenClaw**

Unlike provider plugins that ship as separate npm / ClawHub packages requiring an explicit install step, the azure-speech plugin is bundled with OpenClaw ("included in OpenClaw"), so it is available out of the box rather than fetched from an external registry. The page does not specify any additional install command, version, or configuration step beyond this — *(not specified in source)*.

## Surface

The runtime surface the plugin registers, copied verbatim from the source page's `## Surface` section:

```
contracts: speechProviders
```

The plugin contributes a **`speechProviders` contract** — it is a contract-surface plugin (it implements a capability contract) rather than a plain `plugin` or a named model `providers:` entry. Registering the `speechProviders` contract is what makes Azure AI Speech available as a text-to-speech backend that OpenClaw can route TTS requests to, producing the MP3 / native Ogg-Opus voice-note / PCM-telephony audio outputs named in the page summary. The source page does not enumerate individual voice names, configuration keys, environment variables, or API-key fields for this contract — *(not specified in source)*.

**Source**: OpenClaw documentation — `plugins/reference/azure-speech` (mirror `inbox/openclaw_docs/plugins/reference/azure-speech.md`)
**Last Updated**: 2026-06-22
**Status**: Active
