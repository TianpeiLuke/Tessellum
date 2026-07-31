---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - provider_plugin
keywords:
  - openclaw venice plugin
  - venice model provider
  - "@openclaw/venice-provider"
  - providers venice surface
  - bundled provider plugin
  - venice llm provider
  - openclaw provider descriptor
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/venice
access_control_group: ["general"]
---

# OpenClaw — Venice Provider Plugin (`@openclaw/venice-provider`)

## Overview

This note is the plugin-descriptor card for the **Venice plugin**, which "Adds Venice model provider support to OpenClaw" per the `plugins/reference/venice` source page. It captures the load-bearing descriptor facts of one OpenClaw plugin: its npm package name, its install route, and the contract surface it registers. The Venice plugin is a **provider plugin** — it registers the `venice` LLM model provider so the OpenClaw model catalog and router can serve requests through Venice. This card states the package + surface only; the deeper Venice provider configuration (model list, auth, options) lives in the separate `providers/venice` doc, which this card links rather than redefines.

## Distribution

- **Package:** `@openclaw/venice-provider`
- **Install route:** included in OpenClaw

The plugin ships **bundled** ("included in OpenClaw") rather than installed separately from npm or ClawHub — it is part of the default OpenClaw distribution, so registering the Venice provider does not require a separate plugin install step.

## Surface

The plugin registers the following contract surface (copied verbatim from source):

```
providers: venice
```

The `providers: venice` line is the load-bearing descriptor fact: it declares that this plugin contributes the **`venice` LLM provider** to OpenClaw's provider registry. Once registered, the `venice` provider is selectable by the model router and its models are contributed to the model catalog. No additional config keys, env vars, or defaults are listed on this descriptor page — those are documented on the deeper Venice provider doc (see Related docs / References).

**Source**: OpenClaw documentation — `plugins/reference/venice` (mirror `inbox/openclaw_docs/plugins/reference/venice.md`)
**Last Updated**: 2026-06-22
**Status**: Active
