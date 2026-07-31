---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw xai plugin
  - xai model provider plugin
  - "@openclaw/xai-plugin"
  - grok provider openclaw
  - xai provider contracts
  - websearchproviders xai
  - realtimetranscriptionproviders
  - bundled provider plugin
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/xai
access_control_group: ["general"]
---

# OpenClaw — xAI Provider Plugin (`@openclaw/xai-plugin`)

## Overview

This note is the reference data sheet for the OpenClaw **xAI plugin**, which "Adds xAI model provider support to OpenClaw" — bringing the xAI (Grok) model family into OpenClaw's model/provider layer. It mirrors the `plugins/reference/xai` source page, which is a one-screen plugin reference (`read_when`: you are installing, configuring, or auditing the `xai` plugin). The plugin is a bundled (in-tree) **provider plugin** registering the single provider id `xai` and exposing the broadest contract surface of any plugin in this reference series — seven contracts spanning image generation, media understanding, realtime transcription, speech, tools, video generation, and web search. The full provider configuration (auth, models, options) lives in the separate `/providers/xai` doc that this reference links out to; this note captures only the plugin's distribution and registered surface.

## Distribution

- Package: `@openclaw/xai-plugin`
- Install route: included in OpenClaw

The plugin is **bundled** — its install route is "included in OpenClaw" (no separate ClawHub or npm install step is required; it ships in-tree).

## Surface

The plugin registers the provider id and contracts verbatim as:

> providers: xai; contracts: imageGenerationProviders, mediaUnderstandingProviders, realtimeTranscriptionProviders, speechProviders, tools, videoGenerationProviders, webSearchProviders

That is, it adds one **provider** (`xai`) and binds into seven OpenClaw plugin **contracts**: `imageGenerationProviders`, `mediaUnderstandingProviders`, `realtimeTranscriptionProviders`, `speechProviders`, `tools`, `videoGenerationProviders`, and `webSearchProviders`. This seven-contract surface makes xAI a multimodal provider (image + media understanding + speech + transcription + video + web search) that also contributes agent-callable `tools`. The contract identifiers are OpenClaw plugin-surface keys, not separately documented here; what a consumer subscribes to is the registered set above.

**Source**: OpenClaw documentation — `plugins/reference/xai` (mirror `inbox/openclaw_docs/plugins/reference/xai.md`)
**Last Updated**: 2026-06-22
**Status**: Active
