---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw fal plugin
  - fal-provider plugin
  - fal model provider
  - imageGenerationProviders contract
  - musicGenerationProviders contract
  - videoGenerationProviders contract
  - fal media generation
  - bundled openclaw plugin
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/fal
access_control_group: ["general"]
---

# OpenClaw — fal Plugin Reference Card

## Overview

This note models the OpenClaw **fal plugin** as a plugin-manifest reference card, mirroring the `plugins/reference/fal` source page. The plugin's summary is "Adds fal model provider support to OpenClaw." Its `read_when` trigger is: "You are installing, configuring, or auditing the fal plugin." The card carries the plugin's identity triple — its npm package name, its install route, and its Surface declaration (the provider it registers plus the typed media-generation contracts it contributes) — together with a `Related docs` pointer to the matching `/providers/fal` user page. This is a leaf reference record (model BB), not a how-to procedure; depth on the underlying media-generation concepts and the provider runtime lives in the linked term, provider, and code notes rather than inline.

## Distribution

The fal plugin's package identity and install route, reproduced verbatim from the source page:

- Package: `@openclaw/fal-provider`
- Install route: included in OpenClaw

"Included in OpenClaw" means the plugin is **bundled** in the OpenClaw monorepo — it ships with the gateway and does not require a separate npm or ClawHub install step (unlike installed plugins distributed as `clawhub:` / npm packages).

## Surface

The Surface declaration is the load-bearing, machine-meaningful content of the card — the typed provider and contracts the plugin registers with the OpenClaw extension framework. Reproduced verbatim from the source page:

> providers: fal; contracts: imageGenerationProviders, musicGenerationProviders, videoGenerationProviders

So the fal plugin registers the **`fal` provider** and contributes three media-generation contracts: `imageGenerationProviders` (image generation), `musicGenerationProviders` (music/audio generation), and `videoGenerationProviders` (video generation). Through these contracts, fal's hosted media-generation models become selectable in the OpenClaw model catalog. The page declares no further configuration keys, environment variables, or model identifiers — those are owned by the `/providers/fal` user page, which this card links to as its `Related docs` target.

**Source**: OpenClaw documentation — `plugins/reference/fal` (mirror `inbox/openclaw_docs/plugins/reference/fal.md`)
**Last Updated**: 2026-06-22
**Status**: Active
