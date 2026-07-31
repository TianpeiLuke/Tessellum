---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw tavily plugin
  - tavily web search plugin
  - "@openclaw/tavily-plugin"
  - websearchproviders contract
  - tools contract plugin
  - web search provider support
  - included in openclaw plugin
  - tavily reference card
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/tavily
access_control_group: ["general"]
---

# OpenClaw — Tavily Plugin Reference Card

## Overview

This note captures the OpenClaw **Tavily plugin** reference card from the `plugins/reference/tavily` source page — one card in the uniform ClawHub plugin catalog. The card states the plugin's one-line purpose ("Adds agent-callable tools. Adds web search provider support."), its **Distribution** (npm package id + install route), and its **Surface** (the OpenClaw SDK contracts and skills the plugin contributes). It is an inventory card, not a how-to: the deep Tavily integration behavior is documented on the linked feature page `/tools/tavily`, which is owned by a separate (Tools) sub-plan and is linked here rather than re-described.

The Tavily plugin's entire informational payload is three load-bearing facts: it ships as `@openclaw/tavily-plugin`, it is **included in OpenClaw** (no separate install), and it registers the `tools` and `webSearchProviders` contracts plus skills. Those three facts and the deep-page pointer are reproduced verbatim below.

## Distribution

The card's `## Distribution` facet declares how the plugin is packaged and installed:

- **Package:** `@openclaw/tavily-plugin`
- **Install route:** included in OpenClaw

"Included in OpenClaw" means the plugin ships bundled with the gateway distribution and requires no separate npm/ClawHub install step — unlike plugins whose install route is npm or ClawHub. The package id is the manifest identity the plugin loads under.

## Surface

The card's `## Surface` facet declares which OpenClaw SDK extension points the plugin registers against:

- `contracts: tools, webSearchProviders; skills`

In OpenClaw SDK terms, the plugin contributes against two contracts plus skills: the **`tools`** contract (registering an agent-callable Tavily search tool so the agent can invoke it as a function call) and the **`webSearchProviders`** contract (registering Tavily as a web-search provider backend), and additionally contributes **skills**. The card matches its own summary line — "Adds agent-callable tools" maps to the `tools` contract, and "Adds web search provider support" maps to the `webSearchProviders` contract.

**Source**: OpenClaw documentation — `plugins/reference/tavily` (mirror `inbox/openclaw_docs/plugins/reference/tavily.md`)
**Last Updated**: 2026-06-22
**Status**: Active
