---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw copilot plugin
  - github copilot agent runtime
  - "@openclaw/copilot"
  - clawhub:@openclaw/copilot
  - plugin surface
  - agent runtime plugin
  - npm install route
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/copilot
access_control_group: ["general"]
---

# OpenClaw — Copilot Plugin Reference Card

## Overview

This note is the reference-card descriptor for the OpenClaw **Copilot plugin**, mirroring the `plugins/reference/copilot` source page. It captures the plugin's fixed registry schema: its package id and install routes (Distribution) and the runtime *surface* it contributes (Surface). Per the source, the Copilot plugin "Registers the GitHub Copilot agent runtime" — making it the only **agent-runtime** plugin in the pl08 reference cluster (its siblings register model providers). The page directs operators to read it when "installing, configuring, or auditing the copilot plugin." Its upstream configuration page (`/plugins/copilot`) is owned by another sub-plan and is cited in References, not duplicated here.

## Distribution

The Copilot plugin is distributed as a single ClawHub/npm package, not bundled into OpenClaw core (contrast its provider siblings, several of which are "included in OpenClaw"):

- **Package**: `@openclaw/copilot`
- **Install route**: npm; ClawHub: `clawhub:@openclaw/copilot`

This means an operator can install it either from the npm registry or via the ClawHub identifier `clawhub:@openclaw/copilot`. No version, default-enabled flag, or additional install detail is specified in the source.

## Surface

The plugin's declared surface is:

```
plugin
```

The bare `plugin` surface (no `providers:` id and no capability-contract list) is what distinguishes this card from the model-provider cards in the same cluster. Rather than registering a model provider id or a capability contract (e.g. `imageGenerationProviders`, `speechProviders`), the Copilot plugin **registers the GitHub Copilot agent runtime** — it contributes an agent runtime/harness, not an inference provider. The companion `copilot-proxy` plugin (a model provider exposing `providers: copilot-proxy`) is the provider-surface counterpart to this runtime-surface plugin. Beyond declaring the `plugin` surface and registering the Copilot agent runtime, the source page specifies no further capabilities, auth requirements, or configuration keys.

**Source**: OpenClaw documentation — `plugins/reference/copilot` (mirror `inbox/openclaw_docs/plugins/reference/copilot.md`)
**Last Updated**: 2026-06-22
**Status**: Active
