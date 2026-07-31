---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - gradium plugin
  - openclaw gradium speech
  - text-to-speech provider plugin
  - speechProviders contract
  - "@openclaw/gradium-speech"
  - clawhub gradium speech
  - openclaw tts provider install
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/gradium
access_control_group: ["general"]
---

# OpenClaw — Gradium Speech Provider Plugin (install & capability surface)

## Overview

This note is the plugin-inventory card for the OpenClaw **Gradium** plugin, mirroring the `plugins/reference/gradium` source page. It is a procedure note: how to install/enable the plugin and what capability surface it registers. Gradium "Adds text-to-speech provider support" — it is the one `g*` reference card whose capability class is text-to-speech (TTS) rather than a model/inference provider, a chat channel, or a meeting tool. The card states only three things: the npm package name, the install route (npm or ClawHub — Gradium is NOT built into OpenClaw), and the single capability contract it registers (`speechProviders`). Provider-level configuration (auth, voice selection, audio format) lives on the `/providers/gradium` deep-dive page, which is out of this card's scope and is linked, not duplicated.

## Distribution

Gradium ships as a standalone package and is not included in OpenClaw, so it must be installed explicitly. The source lists:

- **Package:** `@openclaw/gradium-speech`
- **Install route:** npm; ClawHub: `clawhub:@openclaw/gradium-speech`

The package is installable two equivalent ways: from npm by its package name `@openclaw/gradium-speech`, or from ClawHub using the identifier `clawhub:@openclaw/gradium-speech`. The source does not specify version pins, an exact install command, post-install configuration, or any defaults — those are *not specified in source* on this card. (For contrast, the built-in `g*` model-provider plugins such as GitHub Copilot and Google ship inside OpenClaw and need no install step; Gradium, like GMI Cloud and Groq, is an external add-on.)

## Surface

Once installed and enabled, the Gradium plugin registers exactly one capability contract:

- **`contracts: speechProviders`**

The `speechProviders` contract is OpenClaw's text-to-speech provider surface — registering it makes Gradium's TTS available to the host's speech pipeline (e.g., voice-mode replies that synthesize audio from text). The card declares no `providers:` ids and no `channels:` surface; its only registered surface is the `speechProviders` contract. The set of voices, models, audio formats, or provider ids exposed under that contract is *not specified in source* on this card — that detail belongs to the `/providers/gradium` deep-dive.

**Source**: OpenClaw documentation — `plugins/reference/gradium` (mirror `inbox/openclaw_docs/plugins/reference/gradium.md`)
**Last Updated**: 2026-06-22
**Status**: Active
