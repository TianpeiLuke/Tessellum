---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - diffs
keywords:
  - openclaw diffs plugin
  - read-only diff viewer
  - file renderer for agents
  - "@openclaw/diffs package"
  - npm clawhub install route
  - tools contract
  - skills surface
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/diffs
access_control_group: ["general"]
---

# OpenClaw — Diffs Plugin (`@openclaw/diffs`)

## Overview

This note is the plugin-reference card for the OpenClaw **Diffs plugin**, mirroring the `plugins/reference/diffs` source page. The diffs plugin is OpenClaw's **read-only diff viewer plugin and file renderer for agents** — a packaged capability an agent can use to render file contents and diffs without mutating them. The card documents the plugin's two load-bearing facts: its **distribution** (the npm package name and install route) and its **surface** (the plugin contracts it provides). The full feature documentation for the tool itself lives in the `tools/diffs` doc (sub-plan to02), which this reference card points at rather than reproduces.

## Distribution

- **Package**: `@openclaw/diffs`
- **Install route**: npm; ClawHub

The plugin is distributed as the npm package `@openclaw/diffs` and is installable via npm or through ClawHub (OpenClaw's plugin registry/install route). It is not bundled/"included in OpenClaw" — it is an installable extension.

## Surface

The diffs plugin declares the following contract surface: `contracts: tools; skills`. That is, the plugin contributes both a `tools` contract (registering the read-only diff-viewer/file-renderer as an agent-callable tool) and `skills` (the packaged diff-viewer capability the agent can use). This dual `tools` + `skills` surface is what an operator audits or relies on when installing the plugin.

**Source**: OpenClaw documentation — `plugins/reference/diffs` (mirror `inbox/openclaw_docs/plugins/reference/diffs.md`)
**Last Updated**: 2026-06-22
**Status**: Active
