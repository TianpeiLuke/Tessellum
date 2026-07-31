---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - web_search
keywords:
  - openclaw perplexity plugin
  - perplexity-plugin
  - websearchproviders contract
  - web search provider
  - clawhub perplexity
  - perplexity-search tool
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/perplexity
access_control_group: ["general"]
---

# OpenClaw — Perplexity Plugin (Web Search Provider)

## Overview

This note models the **Perplexity plugin** reference card from the OpenClaw `plugins/reference/perplexity` page. The card's one-line summary is "Adds web search provider support." The plugin is distributed as the npm package `@openclaw/perplexity-plugin` and registers a single `webSearchProviders` contract, so OpenClaw agents can run Perplexity web search. It mirrors the source page's three sections — **Distribution** (package + install route), **Surface** (contributed contract), and **Related docs** (a link-out to the fuller `tools/perplexity-search` page) — and does not re-digest that linked tool page.

## Distribution

The plugin ships as a standalone npm package, not bundled with the OpenClaw core. The source page records two install routes for it:

- **Package**: `@openclaw/perplexity-plugin`
- **Install route**: npm; ClawHub: `clawhub:@openclaw/perplexity-plugin`

That is, the plugin can be installed from npm directly, or referenced through ClawHub using the `clawhub:@openclaw/perplexity-plugin` identifier. (No version, default config keys, or environment variables are specified in source.)

## Surface

The plugin contributes exactly one OpenClaw plugin surface — a provider contract:

- **contracts**: `webSearchProviders`

By registering the `webSearchProviders` contract, the plugin makes Perplexity available to agents as a web-search provider: agents can invoke it (via a tool/function call) to retrieve web results and answers and feed that retrieved context back into their generations. The source card declares only this single contract on its **Surface** section and lists no additional channels, tools, or model-provider contracts.

**Source**: OpenClaw documentation — `plugins/reference/perplexity` (mirror `inbox/openclaw_docs/plugins/reference/perplexity.md`)
**Last Updated**: 2026-06-22
**Status**: Active
