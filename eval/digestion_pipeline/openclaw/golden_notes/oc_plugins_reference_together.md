---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw together plugin
  - together model provider
  - "@openclaw/together-provider"
  - together provider plugin reference
  - videogenerationproviders contract
  - together video generation
  - included in openclaw provider
  - clawhub plugin reference card
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/together
access_control_group: ["general"]
---

# OpenClaw — Together Provider Plugin (Reference Card)

## Overview

This note is the OpenClaw **Together plugin** reference card, mirroring the ClawHub plugin-catalog page `plugins/reference/together`. The page is one uniform reference card with three facets: a one-line summary, `## Distribution` (npm package id + install route), and `## Surface` (the OpenClaw SDK contracts the plugin contributes), plus a `## Related docs` pointer to the deep provider feature page. The card states that the plugin **adds Together model provider support to OpenClaw** — it registers the `together` model provider and additionally contributes the `videoGenerationProviders` contract. The card is intentionally terse: deep configuration and model behavior live on the linked `/providers/together` provider feature page (owned by a separate Providers sub-plan), and this note does not re-derive that depth — it captures the three load-bearing inventory facts (package, install route, surface) and wires the card into the vault.

## Distribution

- **Package:** `@openclaw/together-provider`
- **Install route:** included in OpenClaw

The plugin ships bundled with OpenClaw (no separate npm/ClawHub install step), so the `together` provider is available once OpenClaw is installed; only provider configuration (e.g. credentials, model selection) is required to activate it.

## Surface

The card's Surface facet declares verbatim: `providers: together; contracts: videoGenerationProviders`.

- **providers: together** — the plugin registers the `together` model provider, adding Together AI's open-weight model backend to the OpenClaw model catalog as a routable provider.
- **contracts: videoGenerationProviders** — beyond the model-provider surface, the plugin also contributes the `videoGenerationProviders` SDK contract, exposing Together's video-generation capability to the OpenClaw video-generation feature.

This dual surface (a model provider plus a media-generation contract) is what distinguishes the Together card from a plain model-provider reference card such as Tencent, which contributes only a `providers` surface.

**Source**: OpenClaw documentation — `plugins/reference/together` (mirror `inbox/openclaw_docs/plugins/reference/together.md`)
**Last Updated**: 2026-06-22
**Status**: Active
