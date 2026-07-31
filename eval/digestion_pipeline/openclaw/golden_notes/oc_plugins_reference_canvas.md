---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - canvas
keywords:
  - openclaw canvas plugin
  - canvas control surface
  - a2ui rendering surface
  - paired nodes canvas
  - openclaw canvas-plugin package
  - included in openclaw
  - canvas tools contract surface
  - experimental canvas plugin
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/canvas
access_control_group: ["general"]
---

# OpenClaw — Canvas Plugin Reference

## Overview

This note is the operator reference card for the OpenClaw **Canvas plugin**, mirroring the `plugins/reference/canvas` source page. The card summarizes the plugin as **"Experimental Canvas control and A2UI rendering surfaces for paired nodes,"** then records the two facts an operator needs to install and audit it: its **Distribution** (the npm package and install route) and the contract **Surface** it registers. Use this card to discover that the canvas capability exists, confirm the package name, and learn that it ships bundled with OpenClaw rather than being separately installed.

## Distribution

The plugin is packaged as **`@openclaw/canvas-plugin`** and its install route is **included in OpenClaw** — that is, it ships bundled with the gateway rather than being installed separately via npm or a ClawHub slug. No additional `npm install` or `clawhub:` step is documented on this card; the plugin is present once OpenClaw is installed and is enabled through the gateway's plugin configuration.

## Surface

The plugin registers the **`contracts: tools`** surface — it contributes to the `tools` contract surface of the OpenClaw plugin/contract registry. Per the card's summary, the capability it surfaces is **experimental Canvas control and A2UI rendering surfaces for paired nodes**, so the registered `tools` surface is how the agent drives those paired-node canvas/A2UI render and control operations. The card does not enumerate individual tool names, default flags, or configuration keys (none are specified in source); deeper canvas-surface architecture lives in the linked canvas refactor design page.

**Source**: OpenClaw documentation — `plugins/reference/canvas` (mirror `inbox/openclaw_docs/plugins/reference/canvas.md`)
**Last Updated**: 2026-06-22
**Status**: Active
