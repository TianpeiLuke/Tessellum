---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - chutes plugin
  - openclaw chutes provider
  - "@openclaw/chutes-provider"
  - chutes model provider
  - clawhub chutes provider
  - install chutes plugin
  - providers chutes surface
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/chutes
access_control_group: ["general"]
---

# OpenClaw — Chutes Plugin Reference

## Overview

This note is the plugin reference card for the OpenClaw **Chutes plugin**, which "Adds Chutes model provider support to OpenClaw." It is a procedure note for installing, configuring, or auditing the `chutes` plugin: it states the npm/ClawHub **Distribution** package, the contract **Surface** the plugin registers (`providers: chutes`), and the **Related docs** pointer to the deeper Chutes provider configuration page. It mirrors the `plugins/reference/chutes` source card 1:1; the full provider configuration (auth, base URL, model catalog) lives on the linked `/providers/chutes` page, not here.

## Distribution

- **Package**: `@openclaw/chutes-provider`
- **Install route**: npm; ClawHub: `clawhub:@openclaw/chutes-provider`

The plugin is distributed as the npm package `@openclaw/chutes-provider` and can be installed either from npm or from ClawHub via the `clawhub:@openclaw/chutes-provider` slug. The source card does not mark this plugin as "included in OpenClaw" (unlike bundled plugins such as canvas/clickclack/codex-supervisor), so it is installed on demand rather than shipped enabled by default.

## Surface

The plugin registers the contract surface:

```
providers: chutes
```

It implements the `providers` contract, adding `chutes` as a selectable OpenClaw model provider. Once installed, the `chutes` provider becomes available for model resolution and routing in the OpenClaw runtime; its models feed into the model catalog. No other surfaces (channels, tools, or other contracts) are declared by this card.

**Source**: OpenClaw documentation — `plugins/reference/chutes` (mirror `inbox/openclaw_docs/plugins/reference/chutes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
