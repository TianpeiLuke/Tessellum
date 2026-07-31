---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - web_search
keywords:
  - openclaw brave plugin
  - brave search provider
  - websearchproviders contract
  - "@openclaw/brave-plugin"
  - clawhub npm install plugin
  - agent web search plugin
  - plugin surface contract
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/brave
access_control_group: ["general"]
---

# OpenClaw — Brave Search Provider Plugin

## Overview

This note captures the OpenClaw **Brave plugin** reference card from the `plugins/reference/brave` source page: a plugin that contributes a Brave Search web-search backend so an OpenClaw agent can search the web. It records the plugin's identity tuple — purpose, distribution (package name + install route), and the runtime surface it registers — plus the pointer to the corresponding tool doc. It is a stub "plugin reference card" (one `concept` note); the underlying web-search tool itself is documented separately in the `/tools/brave-search` tool doc, which this card links out to rather than duplicating.

## Distribution

The plugin's identity and how to obtain it, copied verbatim from the source page:

- **Package**: `@openclaw/brave-plugin`
- **Install route**: npm; ClawHub

The page's own one-line summary describes it as the "OpenClaw Brave Search provider plugin for web search." The two install routes are npm (the Node package registry) and ClawHub (OpenClaw's plugin registry). The page does not specify an environment variable, API-key name, default region, or version for the Brave plugin — none of those are stated in source.

## Surface

The runtime surface the plugin registers, verbatim from source:

```
contracts: webSearchProviders
```

The plugin registers a `contracts:` capability named `webSearchProviders` — it does not register a model `providers:` name and is not a plain `plugin` surface. In OpenClaw's plugin-surface taxonomy, a `contracts:` plugin contributes a named capability (here, a web-search backend) that the agent can invoke as a tool. By backing the `webSearchProviders` contract, the Brave plugin supplies Brave Search as one selectable web-search backend for agent web search.

**Source**: OpenClaw documentation — `plugins/reference/brave` (mirror `inbox/openclaw_docs/plugins/reference/brave.md`)
**Last Updated**: 2026-06-22
**Status**: Active
