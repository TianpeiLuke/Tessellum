---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - plugin_reference
keywords:
  - openclaw exa plugin
  - exa web search provider
  - websearchproviders contract
  - clawhub exa plugin install
  - npm openclaw exa-plugin
  - exa-search tool
  - plugin manifest surface
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/exa
access_control_group: ["general"]
---

# OpenClaw — Exa Plugin (Reference Card)

## Overview

This note models the `@openclaw/exa-plugin` reference card from the OpenClaw `plugins/reference/exa` page: a plugin-manifest descriptor whose load-bearing content is its identity triple — the npm package name, the install route, and the exact `Surface` contract the plugin registers. The Exa plugin "Adds web search provider support" and is triggered for `read_when` you are installing, configuring, or auditing the exa plugin. It contributes the single `webSearchProviders` contract (the Exa web-search provider) and pairs with the consumer-facing `/tools/exa-search` tool page. Everything else on the source page is a one-line gloss; this card captures the package + Surface schema faithfully and links the concept/provider/tool notes rather than inlining them.

## Distribution

- **Package**: `@openclaw/exa-plugin`
- **Install route**: npm; ClawHub: `clawhub:@openclaw/exa-plugin`

The plugin is distributed over npm and installable via ClawHub using the token `clawhub:@openclaw/exa-plugin` — it is an installed (not bundled-in-OpenClaw) plugin, contrasting with the providers bundled directly in the OpenClaw monorepo.

## Surface

The plugin declares exactly one contract:

```
contracts: webSearchProviders
```

`webSearchProviders` is the typed contract through which the Exa web-search provider is registered with OpenClaw, exposing Exa-backed web search to the agent. No additional providers, channels, or skills are declared on this card.

**Source**: OpenClaw documentation — `plugins/reference/exa` (mirror `inbox/openclaw_docs/plugins/reference/exa.md`)
**Last Updated**: 2026-06-22
**Status**: Active
