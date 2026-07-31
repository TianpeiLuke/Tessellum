---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw tencent plugin
  - tencent tokenhub provider
  - openclaw/tencent-provider
  - tencent-tokenhub model provider
  - openclaw model provider plugin
  - included in openclaw
  - providers contract surface
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/tencent
access_control_group: ["general"]
---

# OpenClaw — Tencent Plugin Reference Card

## Overview

This note captures the OpenClaw **Tencent plugin** reference card from the ClawHub plugin catalog (`plugins/reference/tencent`). The card states one capability — it "Adds Tencent TokenHub model provider support to OpenClaw" — and exposes three fixed facets: **Distribution** (the npm package id and install route), **Surface** (the OpenClaw SDK contracts the plugin contributes), and **Related docs** (a pointer to the deep provider feature page). It is an inventory card, not a configuration guide: the plugin ships in OpenClaw as `@openclaw/tencent-provider` and registers the `tencent-tokenhub` model provider. The provider's actual configuration, credentials, and model catalog are documented on the deep page at `/providers/tencent`, which is owned by a separate Providers sub-plan and linked, not reproduced here.

## Distribution

- **Package:** `@openclaw/tencent-provider`
- **Install route:** included in OpenClaw

The plugin is bundled with OpenClaw rather than installed separately from npm or ClawHub, so no extra install step is required to make the Tencent TokenHub provider available — it is present in the gateway by default and activated through provider configuration.

## Surface

The card declares the OpenClaw SDK surface the plugin contributes:

- **providers:** `tencent-tokenhub`

This is a single `providers` contract registration: the plugin adds the `tencent-tokenhub` model provider to OpenClaw's provider/model catalog, making Tencent TokenHub models selectable as agent backends. No other contracts (channels, tools, skills, web-search, video, speech) are declared on this card.

**Source**: OpenClaw documentation — `plugins/reference/tencent` (mirror `inbox/openclaw_docs/plugins/reference/tencent.md`)
**Last Updated**: 2026-06-22
**Status**: Active
