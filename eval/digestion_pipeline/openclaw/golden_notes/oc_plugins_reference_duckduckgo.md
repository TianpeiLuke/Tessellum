---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw duckduckgo plugin
  - duckduckgo web search provider
  - websearchproviders contract
  - openclaw-duckduckgo-plugin package
  - included in openclaw
  - web search provider plugin
  - clawhub plugin reference card
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/duckduckgo
access_control_group: ["general"]
---

# OpenClaw — DuckDuckGo Plugin (Web Search Provider)

## Overview

This note is the reference card for the OpenClaw **DuckDuckGo plugin**, mirroring the `plugins/reference/duckduckgo` source page. The plugin "adds web search provider support" — it registers DuckDuckGo as a selectable web-search provider for OpenClaw agents by implementing the `webSearchProviders` contract. It covers the plugin's identity (npm package name and install route) under `## Distribution`, the single contract it exposes under `## Surface`, and the pointer to the full DuckDuckGo search tool doc under `## Related docs`. The source page is a thin stub (one-line summary, no code fences); the load-bearing facts are the package name, the "included in OpenClaw" distribution, and the `webSearchProviders` contract surface — all reproduced verbatim below.

## Distribution

- **Package**: `@openclaw/duckduckgo-plugin`
- **Install route**: included in OpenClaw

The plugin ships as part of OpenClaw rather than requiring a separate npm/ClawHub install step, so it is available out of the box once the gateway is running.

## Surface

The plugin declares a single contract surface (verbatim from source):

```
contracts: webSearchProviders
```

By implementing the `webSearchProviders` contract, the plugin registers DuckDuckGo into OpenClaw's pluggable web-search-provider layer, making it one selectable provider that backs an agent's web-search tool call.

**Source**: OpenClaw documentation — `plugins/reference/duckduckgo` (mirror `inbox/openclaw_docs/plugins/reference/duckduckgo.md`)
**Last Updated**: 2026-06-22
**Status**: Active
