---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw searxng plugin
  - searxng-plugin package
  - web search provider
  - websearchproviders contract
  - bundled openclaw plugin
  - self-hosted metasearch
  - plugin registry card
  - contracts websearchproviders surface
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/searxng
access_control_group: ["general"]
---

# OpenClaw — SearXNG Plugin (Reference Card)

## Overview

This note models the OpenClaw **SearXNG plugin** registry card from the `plugins/reference/searxng` source page: a static descriptor of one bundled extension — its summary, its npm package id and install route (Distribution), and the contract surface it contributes to the gateway (Surface). The plugin **adds web search provider support**, registering a `contracts: webSearchProviders` surface so that an agent's web-search tool can be backed by a SearXNG (self-hosted metasearch) instance. The source page is a one-screen, machine-generated catalog card with two H2 sections (`## Distribution`, `## Surface`) and no `## Related docs` link-out; the deep configuration/setup for the web-search tool itself lives in other OpenClaw docs (the tools sub-plan), which this card links toward rather than duplicating.

## Distribution

The plugin is published as the npm package **`@openclaw/searxng-plugin`**. Its install route is **included in OpenClaw** — that is, the plugin is bundled with the gateway distribution rather than fetched separately via npm, ClawHub, or a source checkout. Because it ships with OpenClaw, no add-on install step is required to make the surface available; the gateway's plugin runtime loads the bundled plugin at startup. The package id is the verbatim identifier from the source card and is the handle by which the plugin is referenced in the registry.

## Surface

The plugin registers a single contract surface: **`contracts: webSearchProviders`**. A `webSearchProviders` contract entry contributes a web-search backend that the agent's search tooling can dispatch to — here, a SearXNG metasearch endpoint that aggregates results from multiple upstream search engines. This is a `contracts:` surface (not a `providers:` model-provider surface, nor a `channels:` chat-channel surface): the plugin does not add a model or a messaging channel, it registers an implementation behind the gateway's web-search capability so that "search the web" turns resolve through SearXNG. The source card names only this one surface; no provider variants, channels, tools, or skills are declared on this page.

**Source**: OpenClaw documentation — `plugins/reference/searxng` (mirror `inbox/openclaw_docs/plugins/reference/searxng.md`)
**Last Updated**: 2026-06-22
**Status**: Active
