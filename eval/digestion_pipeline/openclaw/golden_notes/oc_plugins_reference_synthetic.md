---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw synthetic plugin
  - synthetic model provider
  - "@openclaw/synthetic-provider"
  - providers synthetic surface
  - included in openclaw
  - provider plugin install
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/synthetic
access_control_group: ["general"]
---

# OpenClaw — Synthetic Provider Plugin (Reference)

## Overview

This note is the install/configure/audit reference card for the OpenClaw **Synthetic plugin**, which "Adds Synthetic model provider support to OpenClaw." It mirrors the `plugins/reference/synthetic` source page: the plugin ships as the npm package `@openclaw/synthetic-provider`, is **included in OpenClaw** (no separate install required), and contributes a single model-provider surface — `providers: synthetic`. The page's `## Related docs` pointer links the deep conceptual provider guide at `/providers/synthetic`; that setup detail (auth, model IDs, options) lives in the planned provider guide note, not here.

## Distribution

- **Package:** `@openclaw/synthetic-provider`
- **Install route:** included in OpenClaw

Because the plugin is bundled with OpenClaw, no separate `npm install` or ClawHub fetch is required to make the Synthetic provider available — it loads with the gateway runtime. *(The source card states only the package name and the "included in OpenClaw" route; no env vars, version constraints, or additional install steps are specified in source.)*

## Surface

The plugin contributes one **model-provider surface**:

```
providers: synthetic
```

Registering this surface makes Synthetic-served models selectable in OpenClaw's model catalog under the `synthetic` provider ID. This is a `providers:` surface (an LLM/inference backend), as opposed to a `channels:` (messaging) surface.

**Source**: OpenClaw documentation — `plugins/reference/synthetic` (mirror `inbox/openclaw_docs/plugins/reference/synthetic.md`)
**Last Updated**: 2026-06-22
**Status**: Active
