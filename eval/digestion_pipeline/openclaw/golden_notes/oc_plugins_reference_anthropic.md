---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw anthropic plugin
  - "@openclaw/anthropic-provider"
  - anthropic model provider
  - providers anthropic
  - mediaunderstandingproviders contract
  - included in openclaw
  - plugin reference catalog
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/anthropic
access_control_group: ["general"]
---

# OpenClaw — Anthropic Plugin Reference (`@openclaw/anthropic-provider`)

## Overview

This note is the OpenClaw plugin-reference catalog entry for the **Anthropic plugin**, mirroring the auto-generated stub page `plugins/reference/anthropic`. The page's one-line summary is that the plugin "Adds Anthropic model provider support to OpenClaw." Like every other entry in the generated plugin reference, it carries three fixed sections — `## Distribution` (npm package id + install route), `## Surface` (the providers/contracts the plugin registers), and `## Related docs` (a pointer to the fuller provider documentation). This descriptor records the plugin's identity and registered surface only; it does not document setup steps, configuration keys, model lists, or runtime behavior (those live in the linked provider doc).

## Distribution

- Package: `@openclaw/anthropic-provider`
- Install route: included in OpenClaw

The plugin ships **included in OpenClaw** — it is bundled with the gateway rather than installed separately from npm / ClawHub.

## Surface

The plugin's registered surface, copied verbatim from the source page, is:

`providers: anthropic; contracts: mediaUnderstandingProviders`

That is, the plugin registers one provider id — `anthropic` (the Anthropic model provider) — and implements one contract — `mediaUnderstandingProviders` (the media-understanding contract that lets the Anthropic models consume/understand media inputs). The source stub does not enumerate which Claude models, endpoints, or features the provider exposes beyond this provider/contract surface.

**Source**: OpenClaw documentation — `plugins/reference/anthropic` (mirror `inbox/openclaw_docs/plugins/reference/anthropic.md`)
**Last Updated**: 2026-06-22
**Status**: Active
