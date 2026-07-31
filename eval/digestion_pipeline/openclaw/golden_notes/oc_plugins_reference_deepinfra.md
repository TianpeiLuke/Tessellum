---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw deepinfra plugin
  - deepinfra-provider package
  - deepinfra model provider
  - imageGenerationProviders contract
  - mediaUnderstandingProviders contract
  - memoryEmbeddingProviders contract
  - speechProviders videoGenerationProviders
  - clawhub deepinfra install route
topics:
  - OpenClaw
  - Plugin Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/deepinfra
access_control_group: ["general"]
---

# OpenClaw — DeepInfra Provider Plugin Reference

## Overview

This note is a reference card for the OpenClaw **DeepInfra plugin**, the packaged extension that "Adds DeepInfra model provider support to OpenClaw" — mirroring the `plugins/reference/deepinfra` source page. It documents the plugin's fixed descriptor schema: its **Distribution** (npm package id and install routes) and its **Surface** (the provider id and capability contracts it registers into the OpenClaw runtime). DeepInfra has the broadest surface of the pl08 (`cohere → deepseek`) reference cards: one provider id plus five capability contracts spanning image generation, media understanding, memory embeddings, speech, and video generation. The upstream provider-configuration page (`/providers/deepinfra`) is owned by another sub-plan and is cited as an external pointer, not duplicated here.

## Distribution

The plugin is published as the npm package **`@openclaw/deepinfra-provider`**. The source page lists two install routes:

- **Package:** `@openclaw/deepinfra-provider`
- **Install route:** npm; ClawHub: `clawhub:@openclaw/deepinfra-provider`

That is, the plugin is installable from the public npm registry and is also catalogued on ClawHub under the `clawhub:@openclaw/deepinfra-provider` identifier. Unlike the bundled cards in this series (e.g. `comfy`, `copilot-proxy`, `deepgram`), the source page does NOT mark DeepInfra as included-in-OpenClaw — its distribution is npm + ClawHub only. No version pin, configuration key, or credential env var is stated on this reference page; provider configuration is deferred to the `/providers/deepinfra` page.

## Surface

The **Surface** line declares exactly what this plugin contributes to the OpenClaw runtime when loaded, reproduced verbatim from source:

> providers: deepinfra; contracts: imageGenerationProviders, mediaUnderstandingProviders, memoryEmbeddingProviders, speechProviders, videoGenerationProviders

This decomposes into:

- **Provider id (`providers: deepinfra`)** — registers a model inference provider under the id `deepinfra`, so DeepInfra-hosted models become selectable as the `deepinfra` provider in OpenClaw's model catalog. DeepInfra is an OpenAI-compatible inference host serving many open models, so this provider exposes those models to OpenClaw agents.
- **Five capability contracts** — beyond plain chat/LLM inference, the plugin implements five OpenClaw SDK capability contracts: **`imageGenerationProviders`** (image synthesis), **`mediaUnderstandingProviders`** (understanding non-text media inputs), **`memoryEmbeddingProviders`** (dense embedding generation for memory/retrieval), **`speechProviders`** (speech — TTS/STT), and **`videoGenerationProviders`** (video synthesis). Each contract name is an OpenClaw SDK vocabulary identifier (owned by the SDK sub-plans), copied here exactly as the source declares it; this card does not redefine the contracts, only records which ones DeepInfra registers.

This five-contract breadth makes DeepInfra a multi-capability provider: a single registration adds inference, image/video generation, media understanding, embeddings, and speech surfaces at once, which is why it overlaps with the sibling cards `oc_plugins_reference_cohere.md` (shared embedding capability) and `oc_plugins_reference_deepgram.md` (shared `mediaUnderstandingProviders` contract).

**Source**: OpenClaw documentation — `plugins/reference/deepinfra` (mirror `inbox/openclaw_docs/plugins/reference/deepinfra.md`)
**Last Updated**: 2026-06-22
**Status**: Active
