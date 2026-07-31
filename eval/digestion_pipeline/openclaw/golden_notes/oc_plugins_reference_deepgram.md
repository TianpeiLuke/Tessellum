---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - speech
keywords:
  - openclaw deepgram plugin
  - deepgram provider
  - mediaunderstandingproviders contract
  - realtimetranscriptionproviders contract
  - openclaw speech to text
  - realtime transcription provider
  - openclaw deepgram-provider package
  - included in openclaw plugin
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/deepgram
access_control_group: ["general"]
---

# OpenClaw — Deepgram Plugin Reference Card

## Overview

This note is the reference-card descriptor for the OpenClaw **Deepgram plugin**, mirroring the `plugins/reference/deepgram` source page. The plugin's one-line summary is: "Adds media understanding provider support. Adds realtime transcription provider support." Unlike most cards in this reference series, Deepgram is a **pure-contract** plugin — it registers no `providers:` id; instead it contributes two capability contracts to the OpenClaw runtime surface (`mediaUnderstandingProviders` and `realtimeTranscriptionProviders`). This card captures its two load-bearing facts from the source page: the Distribution (package id and install route) and the Surface (the contracts it contributes); the linked provider-configuration page `/providers/deepgram` is owned by another sub-plan and is cited as an external pointer in the References footer, not duplicated here.

## Distribution

The Deepgram plugin is packaged and installed as follows (verbatim from the source page's `## Distribution` section):

- Package: `@openclaw/deepgram-provider`
- Install route: included in OpenClaw

"Included in OpenClaw" means the plugin is bundled with the gateway distribution — no separate npm or ClawHub install step is required to make its contracts available. *(No npm or `clawhub:` install route is listed on the source page for this plugin.)*

## Surface

The plugin's runtime *surface* — what it contributes when loaded — is declared on the source page's `## Surface` section verbatim as:

```
contracts: mediaUnderstandingProviders, realtimeTranscriptionProviders
```

There is **no** `providers:` line on this card: Deepgram does not register a named model provider id. It contributes only two capability contracts:

- `mediaUnderstandingProviders` — corresponds to the summary's "Adds media understanding provider support." This is the contract for understanding non-text media.
- `realtimeTranscriptionProviders` — corresponds to the summary's "Adds realtime transcription provider support." This is the streaming live speech-to-text (STT) contract, the headline Deepgram capability.

No models, defaults, env vars, or configuration keys are listed on this source page (a reference stub); the upstream provider-configuration page `/providers/deepgram` (linked under `## Related docs`, owned by another sub-plan) carries that detail.

**Source**: OpenClaw documentation — `plugins/reference/deepgram` (mirror `inbox/openclaw_docs/plugins/reference/deepgram.md`)
**Last Updated**: 2026-06-22
**Status**: Active
