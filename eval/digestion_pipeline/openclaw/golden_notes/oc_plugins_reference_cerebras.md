---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - cerebras plugin
  - openclaw cerebras provider
  - "@openclaw/cerebras-provider"
  - cerebras model provider
  - clawhub cerebras install
  - providers cerebras surface
  - openclaw provider plugin
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/cerebras
access_control_group: ["general"]
---

# OpenClaw — Cerebras Plugin Reference

## Overview

This note is the OpenClaw plugin-reference card for the **Cerebras plugin**, mirroring the `plugins/reference/cerebras` source page. The card states one capability — it "Adds Cerebras model provider support to OpenClaw." — and then gives the operator the three facts needed to install and audit the plugin: its **Distribution** (npm/ClawHub package), the contract **Surface** it implements (`providers: cerebras`), and a **Related docs** pointer to the deeper Cerebras provider configuration page. This is a deliberately thin reference card; the full provider configuration (credentials, base URL, model catalog) lives on the linked `/providers/cerebras` page reached via `## Related Notes`, not here.

## Distribution

The plugin ships as a single npm package and is installed (not bundled) — it is a provider plugin you add when you want Cerebras model support, unlike "included in OpenClaw" plugins. The card lists, verbatim:

- **Package**: `@openclaw/cerebras-provider`
- **Install route**: npm; ClawHub: `clawhub:@openclaw/cerebras-provider`

There are two equivalent install routes for the same package: the standard npm registry, or ClawHub via the slug `clawhub:@openclaw/cerebras-provider`. The source page does not specify any version pin, additional dependencies, or configuration flags for installation, so none are stated here *(inferred — none given in source; configure the provider itself on the linked provider page)*.

## Surface

The plugin registers exactly one contract surface, stated verbatim on the card as:

```
providers: cerebras
```

That is, it adds a model **provider** named `cerebras` to OpenClaw. Once the plugin is loaded, `cerebras` becomes a registered, routable model provider — its models can be discovered into the model catalog and selected like any other provider. The card declares only the `providers` surface (no `channels`, `contracts`, or other surfaces), so the Cerebras plugin's sole role is to register the `cerebras` provider.

**Source**: OpenClaw documentation — `plugins/reference/cerebras` (mirror `inbox/openclaw_docs/plugins/reference/cerebras.md`)
**Last Updated**: 2026-06-22
**Status**: Active
