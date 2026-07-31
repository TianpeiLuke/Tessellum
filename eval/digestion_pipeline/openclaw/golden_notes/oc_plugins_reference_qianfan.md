---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw qianfan plugin
  - qianfan provider plugin
  - openclaw qianfan-provider
  - qianfan model provider
  - providers qianfan surface
  - baidu qianfan openclaw
  - clawhub qianfan-provider
  - openclaw provider plugin npm
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/qianfan
access_control_group: ["general"]
---

# OpenClaw — Qianfan Plugin (Reference Card)

## Overview

This note models the OpenClaw **Qianfan plugin** registry card, mirroring the `plugins/reference/qianfan` source page. A `plugins/reference/*` page is a machine-generated catalog card: it is a static descriptor of one registry entity, naming the npm package, the install route(s), and the contract **surface** the plugin contributes to the gateway — not a setup how-to. The Qianfan card describes the plugin that "Adds Qianfan model provider support to OpenClaw": it ships as the package `@openclaw/qianfan-provider`, installs via npm or ClawHub, and registers a model-provider surface (`providers: qianfan`). The deep configuration and setup for the provider itself live in a separate `/providers/qianfan` page (a different sub-plan), which this card link-outs to rather than duplicating.

## Distribution

The card declares how the plugin is packaged and obtained. The npm package id is `@openclaw/qianfan-provider`, and the install route is **npm; ClawHub: `clawhub:@openclaw/qianfan-provider`** — i.e. the plugin is fetched as a published npm package, or installed from ClawHub via the `clawhub:@openclaw/qianfan-provider` identifier. This is the standard "installable" distribution mode for an external provider plugin (in contrast to bundled "included in OpenClaw" plugins, or source-checkout-only plugins, that other reference cards in this slice describe).

## Surface

The **Surface** field names the contract the plugin registers into the gateway when it loads. The Qianfan card registers a single surface:

```
providers: qianfan
```

That is, the plugin contributes one entry, `qianfan`, to OpenClaw's `providers:` (model-provider) surface. Once loaded, a `providers: qianfan` entry participates in model resolution and routing, and its model variants are added to the model catalog. Qianfan is Baidu's managed model platform, so this plugin is the wiring that fronts that external GenAI service as a selectable OpenClaw model provider. The card states only the surface name; the credentials, endpoints, and per-model configuration are owned by the deep provider doc below.

**Source**: OpenClaw documentation — `plugins/reference/qianfan` (mirror `inbox/openclaw_docs/plugins/reference/qianfan.md`)
**Last Updated**: 2026-06-22
**Status**: Active
