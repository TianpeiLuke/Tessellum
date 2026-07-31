---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw openrouter plugin
  - openrouter model provider
  - "@openclaw/openrouter-provider"
  - openrouter aggregator key
  - providers openrouter contract
  - imagegenerationproviders contract
  - bundled provider plugin
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/openrouter
access_control_group: ["general"]
---

# OpenClaw — OpenRouter Provider Plugin

## Overview

This note models the OpenClaw **OpenRouter plugin** as a plugin/contract descriptor, mirroring the `plugins/reference/openrouter` reference card. Per the source page, the plugin "Adds OpenRouter model provider support to OpenClaw." It is a bundled provider plugin distributed as the `@openclaw/openrouter-provider` package whose surface registers the `openrouter` model provider plus five media provider contracts through a single aggregator key. The card has three sections — **Distribution** (package + install route), **Surface** (the providers/contracts it contributes), and **Related docs** (a link-out to the fuller `providers/openrouter` page) — all of which this note captures.

## Distribution

The plugin is published as the package **`@openclaw/openrouter-provider`**. Its install route is **"included in OpenClaw"** — i.e., the plugin is bundled with the OpenClaw distribution rather than requiring a separate npm or ClawHub install. No additional install command, version pin, or configuration key is given on the source card.

## Surface

The Surface section declares what the plugin contributes to OpenClaw, copied verbatim from the source: **`providers: openrouter`**; **`contracts: imageGenerationProviders, mediaUnderstandingProviders, musicGenerationProviders, speechProviders, videoGenerationProviders`**. In other words, the plugin registers a single model provider named `openrouter` and, alongside it, the following five media-provider contracts: `imageGenerationProviders` (image generation), `mediaUnderstandingProviders` (media understanding), `musicGenerationProviders` (music generation), `speechProviders` (speech), and `videoGenerationProviders` (video generation). The functional effect — that this represents OpenRouter's aggregator-key model fronting many upstream model/media capabilities through one provider entry — is *(inferred — the card states only the provider name and the five contract names; it does not describe the aggregation mechanism itself)*.

**Source**: OpenClaw documentation — `plugins/reference/openrouter` (mirror `inbox/openclaw_docs/plugins/reference/openrouter.md`)
**Last Updated**: 2026-06-22
**Status**: Active
