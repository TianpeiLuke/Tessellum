---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - browser
keywords:
  - openclaw browser plugin
  - "@openclaw/browser-plugin"
  - agent-callable tools
  - browser plugin surface
  - contracts tools skills
  - included in openclaw
  - browser automation plugin
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/browser
access_control_group: ["general"]
---

# OpenClaw — Browser Plugin Reference

## Overview

This note is the reference card for OpenClaw's **Browser plugin** (`@openclaw/browser-plugin`), mirroring the `plugins/reference/browser` source page. The plugin "Adds agent-callable tools" — it contributes both a `tools` contract surface and `skills` to the OpenClaw runtime so an agent can drive a browser. It is one of three sub-domains in this campaign slice that register a `contracts:` capability surface (alongside `azure-speech` and `brave`), rather than a model provider name. This card captures the plugin's identity tuple — package name, install route, and registered surface — plus the pointer to its companion tool doc; the per-tool browser-control detail lives in the `/tools/browser` doc, not here.

## Distribution

- **Package**: `@openclaw/browser-plugin`
- **Install route**: included in OpenClaw

Because the plugin is **included in OpenClaw**, it ships with the gateway distribution rather than being fetched separately from npm or ClawHub; no separate install command is documented on the source page.

## Surface

The plugin registers the following surface (verbatim from source): `contracts: tools; skills`. This means the Browser plugin contributes into the `tools` contract — making browser-control functions agent-callable (the page's one-line summary, "Adds agent-callable tools") — and also contributes `skills`, packaged agent capabilities for browser workflows. Unlike a model-provider plugin (which registers a `providers:` name) or a single-contract plugin, the Browser plugin spans two contributions on its surface: an agent-tool capability and skills.

**Source**: OpenClaw documentation — `plugins/reference/browser` (mirror `inbox/openclaw_docs/plugins/reference/browser.md`)
**Last Updated**: 2026-06-22
**Status**: Active
