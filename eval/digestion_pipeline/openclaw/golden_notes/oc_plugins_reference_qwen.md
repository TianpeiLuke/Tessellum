---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw qwen plugin
  - qwen-provider plugin
  - qwen provider variants
  - dashscope model studio provider
  - qwen-oauth qwen-portal qwen-cli
  - mediaunderstandingproviders videogenerationproviders
  - clawhub qwen-provider install
  - alibaba qwen model provider
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/qwen
access_control_group: ["general"]
---

# OpenClaw — Qwen Plugin (`@openclaw/qwen-provider`) Reference Card

## Overview

This note models the OpenClaw **Qwen plugin** registry card from the `plugins/reference/qwen` source page: a static descriptor of one registry entity — its npm/ClawHub package id, its install route, and the contract **surface** it registers into the gateway. Per the source summary, the plugin "Adds Qwen, Qwen Cloud, Model Studio, DashScope, Qwen Oauth, Qwen Portal, Qwen CLI model provider support to OpenClaw." It is the densest card in the `q-r-s` reference slice because it registers **seven model `providers:` variants** plus **two media `contracts:`** (`mediaUnderstandingProviders`, `videoGenerationProviders`) from a single package. This card is the "what package / where from / what it exposes" index entry; the deep setup lives in the linked `/providers/qwen` and `/providers/qwen-oauth` docs (owned by other sub-plans), referenced — not duplicated — below.

## Distribution

The plugin's distribution facts (verbatim from the source `## Distribution` section):

- **Package**: `@openclaw/qwen-provider`
- **Install route**: npm; ClawHub: `clawhub:@openclaw/qwen-provider`

The npm route installs `@openclaw/qwen-provider` as a scoped Node package, and the ClawHub route resolves the same package through the ClawHub registry via the `clawhub:@openclaw/qwen-provider` identifier. Unlike the bundled cards in this slice (Runway, SearXNG, Senseaudio, which are "included in OpenClaw"), the Qwen plugin is **separately installed** — it is not shipped pre-bundled with the gateway and must be added through one of these two declared routes.

## Surface

The contract surface registered by the plugin (verbatim from the source `## Surface` section):

```
providers: qwen, qwencloud, modelstudio, dashscope, qwen-oauth, qwen-portal, qwen-cli; contracts: mediaUnderstandingProviders, videoGenerationProviders
```

The surface declares two kinds of registration. The **`providers:`** field registers seven distinct model-provider variants the gateway can route inference to: `qwen`, `qwencloud`, `modelstudio`, `dashscope`, `qwen-oauth`, `qwen-portal`, and `qwen-cli` — these front the Alibaba Qwen model family across its API endpoints and authentication modes (the `qwen-oauth` variant authenticates via OAuth, documented in the `/providers/qwen-oauth` link-out; DashScope and Model Studio are Alibaba's hosted endpoints for the same family). The **`contracts:`** field registers two media-capability contracts: `mediaUnderstandingProviders` (a multimodal media-understanding surface) and `videoGenerationProviders` (a video-generation surface). A single plugin package therefore contributes both LLM-provider entries and multimodal media contracts to the gateway's model/contract registries. *(The source card lists only the provider/contract names; per-variant config, endpoints, defaults, and credential keys are "Not specified in source" on this index card and live in the `/providers/qwen` and `/providers/qwen-oauth` deep-config docs.)*

**Source**: OpenClaw documentation — `plugins/reference/qwen` (mirror `inbox/openclaw_docs/plugins/reference/qwen.md`)
**Last Updated**: 2026-06-22
**Status**: Active
