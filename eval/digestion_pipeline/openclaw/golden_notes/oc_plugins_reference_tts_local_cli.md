---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw tts-local-cli plugin
  - text-to-speech provider plugin
  - speechProviders contract
  - local text-to-speech
  - "@openclaw/tts-local-cli"
  - included in openclaw
  - openclaw speech provider
  - plugin reference card
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/tts-local-cli
access_control_group: ["general"]
---

# OpenClaw — TTS Local CLI Plugin Reference Card

## Overview

This note captures the OpenClaw **TTS Local CLI** plugin-reference card from the `plugins/reference/tts-local-cli` source page. It is one of the uniform ClawHub plugin-catalog cards, summarized in source as "Adds text-to-speech provider support." The card carries two load-bearing facets: **Distribution** (the npm package id and install route) and **Surface** (the OpenClaw SDK contract the plugin contributes). The plugin ships as `@openclaw/tts-local-cli`, is **included in OpenClaw** (no separate install), and contributes the `speechProviders` contract, registering a local command-line text-to-speech backend so the agent can emit synthesized speech. Unlike most reference cards in this batch, this card has only two H2 sections — it omits the `## Related docs` pointer — so the deep feature page is not named on the card itself; the depth of the TTS feature is deferred to the Tools/voice section (planned `oc_tools_tts`, sub-plan to08), which is linked, not recreated here.

## Distribution

The source card's `## Distribution` facet declares two values verbatim:

- **Package:** `@openclaw/tts-local-cli`
- **Install route:** included in OpenClaw

Because the install route is "included in OpenClaw", the plugin is bundled with the gateway distribution and does not require a separate npm or ClawHub install step (in contrast to npm/ClawHub-distributed plugins in the same batch). No version, configuration keys, or environment variables are listed on the source card — those are not specified in source and are deferred to the deep feature page.

## Surface

The source card's `## Surface` facet declares exactly one contributed contract, verbatim:

- **contracts:** `speechProviders`

The `speechProviders` contract is the OpenClaw SDK speech-output extension point: a plugin that implements it registers a pluggable text-to-speech backend that the agent harness can route response text through to produce audio. This plugin's specific backend is a **local CLI** speech provider — synthesis runs through a local command-line tool rather than a hosted/cloud speech API — which is the meaning of "local" in the plugin name and of "Adds text-to-speech provider support." in the summary. The card declares no `channels`, `providers` (model providers), `tools`, or `skills` surfaces — only `speechProviders`.

**Source**: OpenClaw documentation — `plugins/reference/tts-local-cli` (mirror `inbox/openclaw_docs/plugins/reference/tts-local-cli.md`)
**Last Updated**: 2026-06-22
**Status**: Active
