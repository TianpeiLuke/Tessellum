---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - tools
keywords:
  - openclaw file-transfer plugin
  - file-transfer package
  - tools contract
  - node.invoke base64 transfer
  - paired node file ops
  - fetch list write files
  - bypass bash stdout truncation
  - bundled openclaw plugin
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/file-transfer
access_control_group: ["general"]
---

# OpenClaw — File Transfer Plugin Reference Card

## Overview

This note is the plugin-manifest reference card for the OpenClaw **`@openclaw/file-transfer`** plugin, mirroring the `plugins/reference/file-transfer` source page. As a reference/record schema (model BB), it captures the plugin's identity triple — its npm package name, its install route, and the exact typed contract it registers on the OpenClaw extension surface. The plugin lets an agent fetch, list, and write files on paired nodes via dedicated node commands; it bypasses bash stdout truncation by sending binaries base64-encoded over `node.invoke` for payloads up to 16 MB. You read this page when you are installing, configuring, or auditing the file-transfer plugin. Unlike most plugin cards in this series, the source page declares no `## Related docs` section, so this note carries only the Distribution and Surface blocks from the mirror.

## Distribution

The plugin's package and install route, copied verbatim from the source card:

- Package: `@openclaw/file-transfer`
- Install route: included in OpenClaw

"Included in OpenClaw" means the plugin is **bundled** with the OpenClaw monorepo rather than installed separately from npm or ClawHub — it ships and loads with the gateway, with no per-plugin install step required.

## Surface

The Surface block declares the typed OpenClaw extension contract this plugin contributes, reproduced verbatim:

```
contracts: tools
```

The single `tools` contract maps to the plugin's one-line summary — "Fetch, list, and write files on paired nodes via dedicated node commands. Bypasses bash stdout truncation by using base64 over `node.invoke` for binaries up to 16 MB." The plugin registers fetch, list, and write file operations as agent-callable tools; each runs as a dedicated node command targeting a paired node. Binary content moves base64-encoded over the `node.invoke` transport, which sidesteps the truncation that bash stdout would impose, with a stated ceiling of 16 MB per binary. The card declares no providers, channels, or skills contracts and no configuration keys beyond this `tools` contract; nothing further is specified in source.

**Source**: OpenClaw documentation — `plugins/reference/file-transfer` (mirror `inbox/openclaw_docs/plugins/reference/file-transfer.md`)
**Last Updated**: 2026-06-22
**Status**: Active
