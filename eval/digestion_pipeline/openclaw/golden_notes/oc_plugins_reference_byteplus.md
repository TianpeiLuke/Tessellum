---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw byteplus plugin
  - byteplus model provider
  - byteplus-plan provider
  - "@openclaw/byteplus-provider"
  - videogenerationproviders contract
  - byteplus video generation
  - openclaw provider plugin
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/byteplus
access_control_group: ["general"]
---

# OpenClaw — BytePlus Provider Plugin

## Overview

This note is the plugin-reference card for the OpenClaw **BytePlus plugin**, which "Adds BytePlus, BytePlus Plan model provider support to OpenClaw." It mirrors the `plugins/reference/byteplus` source page: the plugin's distribution (package `@openclaw/byteplus-provider`, included in OpenClaw) and the runtime surface it registers. Unlike the single-provider cards in this alphabetical slice, BytePlus registers **two** model-provider names (`byteplus`, `byteplus-plan`) plus a `contracts: videoGenerationProviders` capability — so it spans both LLM model serving and video generation. The source page has only `## Distribution` and `## Surface` (no `Related docs` section); this card captures those identity and install/surface facts only.

## Distribution

The BytePlus plugin is distributed as the package `@openclaw/byteplus-provider`. Its documented install route is **included in OpenClaw** — the plugin ships with OpenClaw rather than requiring a separate npm or ClawHub install step.

## Surface

The plugin registers the runtime surface `providers: byteplus, byteplus-plan; contracts: videoGenerationProviders`. It adds two model-provider names — `byteplus` and `byteplus-plan` — and one capability contract, `videoGenerationProviders`. Once registered, `byteplus` and `byteplus-plan` become selectable/routable model-provider names in OpenClaw's runtime (BytePlus / BytePlus Plan), and the `videoGenerationProviders` contract lets the plugin back the agent's video-generation capability. No other surface is declared by this plugin on the source page.

**Source**: OpenClaw documentation — `plugins/reference/byteplus` (mirror `inbox/openclaw_docs/plugins/reference/byteplus.md`)
**Last Updated**: 2026-06-22
**Status**: Active
