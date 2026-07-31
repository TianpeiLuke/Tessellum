---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw arcee plugin
  - arcee model provider
  - "@openclaw/arcee-provider"
  - clawhub arcee provider
  - providers arcee surface
  - arcee provider plugin install
  - openclaw llm provider plugin
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/arcee
access_control_group: ["general"]
---

# OpenClaw — Arcee Provider Plugin

## Overview

This note is the plugin-reference card for the OpenClaw **Arcee plugin**, which "Adds Arcee model provider support to OpenClaw." It mirrors the `plugins/reference/arcee` source page: the plugin's distribution (npm / ClawHub package `@openclaw/arcee-provider`), the runtime surface it registers (`providers: arcee`), and the pointer to the corresponding provider configuration doc. Arcee is one of the LLM model-provider plugins in OpenClaw's ClawHub/built-in plugin catalog; this card captures its identity and install/surface facts only — the provider's auth and model-selection setup lives in the separate `/providers/arcee` doc.

## Distribution

The Arcee plugin is distributed as the package `@openclaw/arcee-provider`. It has two documented install routes: **npm**, and **ClawHub** via the install reference `clawhub:@openclaw/arcee-provider`.

## Surface

The plugin registers the runtime surface `providers: arcee` — it adds a single model provider named `arcee` to OpenClaw. Once registered, `arcee` becomes a selectable/routable model-provider name in OpenClaw's runtime. No other surface (no `contracts:` capability and no additional provider names) is declared by this plugin on the source page.

**Source**: OpenClaw documentation — `plugins/reference/arcee` (mirror `inbox/openclaw_docs/plugins/reference/arcee.md`)
**Last Updated**: 2026-06-22
**Status**: Active
