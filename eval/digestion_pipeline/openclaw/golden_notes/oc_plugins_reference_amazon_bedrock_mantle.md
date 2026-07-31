---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - amazon bedrock mantle plugin
  - openclaw provider plugin
  - openai-compatible model routing
  - amazon-bedrock-mantle-provider
  - providers amazon-bedrock-mantle
  - bedrock mantle distribution
  - clawhub npm install route
  - plugin surface providers
topics:
  - OpenClaw
  - Plugins Reference Catalog
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/amazon-bedrock-mantle
access_control_group: ["general"]
---

# OpenClaw — Amazon Bedrock Mantle Plugin (Reference Catalog Entry)

## Overview

This note is the generated plugin-reference catalog entry for the OpenClaw **Amazon Bedrock Mantle** provider plugin, mirroring the `plugins/reference/amazon-bedrock-mantle` source page. The page describes the plugin as "OpenClaw Amazon Bedrock Mantle provider plugin for OpenAI-compatible model routing" — that is, it registers a model provider that fronts Amazon Bedrock behind an OpenAI-compatible routing surface. As an auto-generated reference stub (emitted from `extensions/*/package.json` + `openclaw.plugin.json`), it carries three load-bearing facts only: the **Distribution** block (npm package id + install route), the **Surface** block (the provider it exposes), and a **Related docs** pointer to the fuller provider documentation. This note faithfully reproduces those facts; it does not invent setup steps, config keys, model lists, or behavior the page does not state, and it links the substantive provider/runtime homes through `## Related Notes`.

## Distribution

The plugin is distributed as the npm package **`@openclaw/amazon-bedrock-mantle-provider`**. Its install route is **npm; ClawHub** — meaning the plugin is not bundled "included in OpenClaw" but is installed externally, either from the npm registry or via the ClawHub plugin channel. (Contrast with sibling reference entries such as `anthropic`/`admin-http-rpc`, whose install route is "included in OpenClaw".)

## Surface

The plugin's exposed Surface is a single provider:

> providers: amazon-bedrock-mantle

That is, installing this plugin registers the `amazon-bedrock-mantle` model provider into the OpenClaw runtime. The source page lists no additional `contracts:` or `skills:` on this plugin's Surface (unlike the sibling `amazon-bedrock` entry, which also exposes `contracts: memoryEmbeddingProviders`). The provider id `amazon-bedrock-mantle` is the configuration identifier under which OpenAI-compatible routing to Bedrock is selected; the routing/translation behavior itself is documented in the fuller provider doc, not on this generated stub.

**Source**: OpenClaw documentation — `plugins/reference/amazon-bedrock-mantle` (mirror `inbox/openclaw_docs/plugins/reference/amazon-bedrock-mantle.md`)
**Last Updated**: 2026-06-22
**Status**: Active
