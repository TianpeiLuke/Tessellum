---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw inworld plugin
  - inworld streaming text-to-speech
  - "@openclaw/inworld-speech"
  - speechProviders contract
  - inworld tts mp3 ogg_opus pcm
  - clawhub inworld speech install
  - openclaw speech provider plugin
  - pcm telephony tts
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/inworld
access_control_group: ["general"]
---

# OpenClaw — Inworld Speech Plugin (`@openclaw/inworld-speech`)

## Overview

This note is the procedure card for identifying, installing, and auditing the OpenClaw **Inworld** plugin, mirroring the `plugins/reference/inworld` reference page. The plugin provides **Inworld streaming text-to-speech (MP3, OGG_OPUS, PCM telephony)** and is the thin catalog entry above the deeper `/providers/inworld` page. It records the three load-bearing facts of the card — the npm **package name**, the **install route**, and the exact **surface** the plugin contributes — so the plugin can be looked up and verified without re-reading the deeper provider docs. Unlike the bundled channel/provider cards in this series, Inworld is NOT bundled in OpenClaw; it installs from npm or ClawHub.

## Distribution

- **Package:** `@openclaw/inworld-speech`
- **Install route:** `npm`; ClawHub: `clawhub:@openclaw/inworld-speech`

The plugin is distributed as the npm package `@openclaw/inworld-speech`. It is not included in a default OpenClaw install (no "included in OpenClaw" route on this card); to add it you install it from npm, or from ClawHub via the identifier `clawhub:@openclaw/inworld-speech`. To audit an install, confirm this package name and ClawHub identifier match what is declared in the OpenClaw plugin set.

## Surface

`contracts: speechProviders`

The plugin contributes a **speech-provider** surface via the `speechProviders` contract (the `contracts:` surface key, not a `providers:` model surface nor a `channels:` chat surface). Concretely it registers an Inworld streaming text-to-speech engine that emits audio in **MP3**, **OGG_OPUS**, and **PCM telephony** formats, making Inworld a selectable TTS backend within OpenClaw's voice/speech stack. The deeper configuration of that speech-provider surface (auth, voices, format selection) lives on the `/providers/inworld` page linked below — this card only declares which contract the plugin satisfies.

**Source**: OpenClaw documentation — `plugins/reference/inworld` (mirror `inbox/openclaw_docs/plugins/reference/inworld.md`)
**Last Updated**: 2026-06-22
**Status**: Active
