---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw senseaudio plugin
  - senseaudio-provider
  - media understanding provider
  - mediaUnderstandingProviders contract
  - bundled provider plugin
  - included in openclaw
  - audio understanding provider
  - plugin registry card
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/senseaudio
access_control_group: ["general"]
---

# OpenClaw — Senseaudio Plugin (Reference Card)

## Overview

This note models the OpenClaw **Senseaudio plugin** registry card from the `plugins/reference/senseaudio` source page: the static descriptor of one bundled plugin — its npm package id, its install route, and the contract **surface** it registers. The card's one-line summary is "Adds media understanding provider support": the plugin contributes a media-understanding (audio) provider to OpenClaw's media stack. It is a machine-generated reference entry — the "what package / where from / what it exposes" card — NOT the deep provider config doc, which lives at `/providers/senseaudio` (linked, not duplicated). This note covers the two load-bearing fields the card carries (Distribution and Surface) plus the Related-docs link-out.

## Distribution

The package id and install route define how the plugin reaches a running gateway:

- **Package**: `@openclaw/senseaudio-provider`
- **Install route**: included in OpenClaw

"Included in OpenClaw" means the plugin is **bundled** — it ships inside the gateway distribution and loads from the built-in plugin set at startup rather than being fetched separately. This is the contrast to the npm / ClawHub install routes used by separately-distributed provider plugins (e.g. the `qianfan` and `qwen` cards in this same `q…r…s` reference slice) and to the source-checkout-only route of the `qa-matrix` card. Because it is bundled, no separate `npm install` or ClawHub fetch is required to make the `@openclaw/senseaudio-provider` package available; the operator only configures it (deep config at `/providers/senseaudio`).

## Surface

The **Surface** field names the contract the plugin registers into the gateway — its single load-bearing capability declaration:

```yaml
contracts: mediaUnderstandingProviders
```

The plugin registers a `contracts:` surface (not a `providers:` model-provider surface and not a `channels:` chat-channel surface) named `mediaUnderstandingProviders`. A `mediaUnderstandingProviders` contract supplies media-understanding capability over audio — i.e. consuming inbound audio and producing a text/structured understanding of it (audio transcription / speech understanding). Registering this contract makes the Senseaudio backend available to whatever runtime node or tool consumes the `mediaUnderstandingProviders` contract; the deep configuration of the provider itself (credentials, options) is documented separately at `/providers/senseaudio` and is out of scope for this registry card. The page declares no other surface — only the single `mediaUnderstandingProviders` contract.

**Source**: OpenClaw documentation — `plugins/reference/senseaudio` (mirror `inbox/openclaw_docs/plugins/reference/senseaudio.md`)
**Last Updated**: 2026-06-22
**Status**: Active
