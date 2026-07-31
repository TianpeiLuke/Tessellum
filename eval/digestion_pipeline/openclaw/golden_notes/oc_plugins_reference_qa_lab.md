---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw qa-lab plugin
  - qa lab debugger ui
  - scenario runner
  - websearchproviders contract
  - source checkout only plugin
  - openclaw qa-lab package
  - private debugger ui
  - qa-lab scenario testing
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/qa-lab
access_control_group: ["general"]
---

# OpenClaw — QA Lab Plugin (`@openclaw/qa-lab`)

## Overview

This note is the plugin-reference card for the OpenClaw **QA Lab** plugin, mirroring the `plugins/reference/qa-lab` source page. QA Lab is described in the source as an "OpenClaw QA lab plugin with private debugger UI and scenario runner" — a development/test surface that pairs an interactive debugger UI with a scenario runner for exercising OpenClaw agents end-to-end. It models the plugin as a distribution + surface descriptor: the npm package and install route under `## Distribution`, and the single contract it contributes (`webSearchProviders`) under `## Surface`. This page has no `## Related docs` pointer; the fuller cross-links are to the QA-tooling and web/control-UI pages noted below.

## Distribution

- **Package:** `@openclaw/qa-lab`
- **Install route:** source checkout only

The "source checkout only" route means the plugin is not published to the public npm registry or ClawHub for direct install — it is obtained by checking out the OpenClaw source tree, where it lives as a development/test plugin. This matches its role as private internal debugging tooling rather than an end-user-installable provider.

## Surface

- **contracts:** `webSearchProviders`

The QA Lab plugin's only declared contract surface is `webSearchProviders` — the same web-search provider contract registered by the Perplexity plugin. QA Lab declares this contract so its scenarios can drive the web-search code path during agent debugging and scenario runs, rather than to ship a production search backend. The plugin's substantive value is the debugger UI and scenario runner described in the summary; the `webSearchProviders` declaration is the machine-readable contract the plugin contributes to OpenClaw's plugin system.

**Source**: OpenClaw documentation — `plugins/reference/qa-lab` (mirror `inbox/openclaw_docs/plugins/reference/qa-lab.md`)
**Last Updated**: 2026-06-22
**Status**: Active
