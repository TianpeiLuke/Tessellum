---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw comfy plugin
  - comfyui model provider
  - "@openclaw/comfy-provider"
  - comfy provider id
  - imagegenerationproviders contract
  - musicgenerationproviders contract
  - videogenerationproviders contract
  - bundled provider plugin
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/comfy
access_control_group: ["general"]
---

# OpenClaw — ComfyUI Provider Plugin Reference

## Overview

This note is the reference card for the OpenClaw **ComfyUI plugin**, mirroring the `plugins/reference/comfy` source page. The plugin "Adds ComfyUI model provider support to OpenClaw" — it packages the ComfyUI generation backend as an OpenClaw model provider. The card documents the plugin's two fixed schema facts: its **Distribution** (package id `@openclaw/comfy-provider`, install route "included in OpenClaw") and its **Surface** (the runtime contributions it registers — the `comfy` provider id plus three media-generation capability contracts). The detailed provider *configuration* lives on the separate `/providers/comfy` page (owned by another sub-plan) and is linked, not reproduced here.

## Distribution

The `plugins/reference/comfy` page declares the plugin's distribution as two fields, reproduced verbatim:

- **Package**: `@openclaw/comfy-provider`
- **Install route**: included in OpenClaw

"Included in OpenClaw" means the plugin is **bundled** with the OpenClaw distribution rather than installed separately from npm or ClawHub — no extra install step is required to make the `comfy` provider available. The source page lists no npm or ClawHub (`clawhub:@openclaw/<pkg>`) install route for this plugin (those alternate routes appear on other cards in the series, e.g. cohere/deepinfra/deepseek, but not on comfy).

## Surface

The **Surface** line is the load-bearing fact of this card — it names the runtime surface the plugin contributes. The source declares it verbatim as:

```
providers: comfy; contracts: imageGenerationProviders, musicGenerationProviders, videoGenerationProviders
```

This decomposes into two kinds of registration:

- **Provider id** — `providers: comfy`: the plugin registers a single model provider under the id `comfy`. Once registered, ComfyUI's generation models enter OpenClaw's model catalog under this provider id.
- **Capability contracts** — `contracts:` lists three media-generation provider contracts the plugin satisfies:
  - `imageGenerationProviders` — image-generation capability (ComfyUI's canonical diffusion image pipelines).
  - `musicGenerationProviders` — music/audio-generation capability.
  - `videoGenerationProviders` — video-generation capability.

These contract names are OpenClaw SDK capability-contract vocabulary (the same family includes `mediaUnderstandingProviders`, `memoryEmbeddingProviders`, `speechProviders`, and `realtimeTranscriptionProviders` declared by sibling plugins). ComfyUI is a node-graph engine for diffusion-based generation, so it fronts image, music, and video generation through these three contracts rather than registering a chat/embedding model provider. No other surfaces, flags, defaults, or model ids are specified on this source page.

## Provider Configuration Pointer

The source page's `Related docs` section points to the provider configuration page, preserved as an external pointer in the References section below (the `/providers/comfy` page is owned by another sub-plan and is not duplicated here): the link `comfy` → `/providers/comfy` (`https://docs.openclaw.ai/providers/comfy`).

**Source**: OpenClaw documentation — `plugins/reference/comfy` (mirror `inbox/openclaw_docs/plugins/reference/comfy.md`)
**Last Updated**: 2026-06-22
**Status**: Active
