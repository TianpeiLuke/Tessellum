---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - firecrawl
keywords:
  - openclaw firecrawl plugin
  - firecrawl-plugin
  - clawhub firecrawl
  - webfetchproviders contract
  - websearchproviders contract
  - firecrawl web crawl fetch search
  - npm install plugin
  - agent-callable tools
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/firecrawl
access_control_group: ["general"]
---

# OpenClaw — Firecrawl Plugin (Reference Card)

## Overview

This note models the OpenClaw **Firecrawl plugin** reference card from the `plugins/reference/firecrawl` source page: an npm/ClawHub-installed plugin that "Adds agent-callable tools. Adds web fetch provider support. Adds web search provider support." The page is a structured plugin-manifest descriptor — its load-bearing content is the plugin's identity triple: the package name, the install route, and the exact Surface declaration (the typed OpenClaw contracts it registers). The card is read when you are "installing, configuring, or auditing the firecrawl plugin," and it points to the consumer-facing `/tools/firecrawl` page for usage.

## Distribution

The plugin's package identity and how it reaches an OpenClaw deployment:

- **Package:** `@openclaw/firecrawl-plugin`
- **Install route:** npm; ClawHub: `clawhub:@openclaw/firecrawl-plugin`

Unlike bundled-in-OpenClaw plugins, Firecrawl is **installed** (not pre-shipped): it is fetched from npm or via the ClawHub registry token `clawhub:@openclaw/firecrawl-plugin`, then enabled in configuration before its Surface contracts take effect.

## Surface

The Surface declares the typed OpenClaw contracts this plugin contributes when loaded — verbatim from the source:

```
contracts: tools, webFetchProviders, webSearchProviders
```

The three registered contracts:

- **`tools`** — agent-callable tools: Firecrawl's crawl/fetch/search operations are exposed to the agent as typed, callable tools.
- **`webFetchProviders`** — web fetch provider support: registers Firecrawl as a provider that retrieves (fetches) the contents of a given web page/URL for the agent.
- **`webSearchProviders`** — web search provider support: registers Firecrawl as a web-search provider, supplying web-scale search results to the agent.

**Source**: OpenClaw documentation — `plugins/reference/firecrawl` (mirror `inbox/openclaw_docs/plugins/reference/firecrawl.md`)
**Last Updated**: 2026-06-22
**Status**: Active
