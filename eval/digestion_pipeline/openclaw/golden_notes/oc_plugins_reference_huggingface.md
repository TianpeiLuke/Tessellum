---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw huggingface plugin
  - huggingface model provider
  - openclaw huggingface-provider npm package
  - providers huggingface surface
  - bundled openclaw plugin
  - install route included in openclaw
  - hugging face provider plugin
  - openclaw provider plugin card
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/huggingface
access_control_group: ["general"]
---

# OpenClaw — Hugging Face Plugin Reference Card

## Overview

This note is the catalog reference card for the OpenClaw **Hugging Face plugin**, mirroring the `plugins/reference/huggingface` source page. The card documents one shippable OpenClaw plugin: the npm package `@openclaw/huggingface-provider`, which "Adds Hugging Face model provider support to OpenClaw." As a procedure, it tells you how to identify and audit this plugin — its distribution (package name + install route), the surface it contributes (`providers: huggingface`), and where the deeper provider configuration lives. The source page exposes exactly three H2 sections (`## Distribution`, `## Surface`, `## Related docs`) plus an H1 summary line; all of them map into this single note. This card is the thin catalog layer above the much richer `/providers/huggingface` provider page (owned by a separate sub-plan) — it links out to that deeper page rather than re-explaining provider auth or model configuration here.

## Distribution

- **Package**: `@openclaw/huggingface-provider`
- **Install route**: included in OpenClaw

The plugin is **bundled** — it ships with OpenClaw and does not require a separate `npm` or ClawHub install step. To identify or audit it, look for the `@openclaw/huggingface-provider` package as part of the OpenClaw distribution; because it is included rather than externally installed, no add-on install command is given on the source card. Verbatim, the source page states only `Package: @openclaw/huggingface-provider` and `Install route: included in OpenClaw`; any additional install/enable steps are *(not specified in source)* and belong to the deeper `/providers/huggingface` page.

## Surface

The plugin contributes one surface to OpenClaw:

```
providers: huggingface
```

This means enabling the plugin registers a model **provider** keyed `huggingface`. Once active, Hugging Face becomes a selectable, routable model provider inside OpenClaw's agent loop — the provider key `huggingface` is the exact identifier used to reference it in provider configuration and routing. The source card declares only this single `providers: huggingface` surface (it is a model-provider plugin, not a channel or speech-provider plugin); no channel (`channels:`) or speech (`contracts: speechProviders`) surface is declared.

**Source**: OpenClaw documentation — `plugins/reference/huggingface` (mirror `inbox/openclaw_docs/plugins/reference/huggingface.md`)
**Last Updated**: 2026-06-22
**Status**: Active
