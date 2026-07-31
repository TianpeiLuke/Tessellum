---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw plugin reference
  - plugin reference index
  - plugins inventory gen
  - generated plugin pages
  - openclaw.plugin.json
  - extensions package.json
  - plugin inventory 128 pages
  - plugin catalog
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference
access_control_group: ["general"]
---

# OpenClaw — Plugin Reference (Generated Index)

## Overview

This note describes the OpenClaw **Plugin reference** index — the generated catalog page that anchors every per-plugin reference page in OpenClaw's documentation. It mirrors the `plugins/reference` source page, which states three load-bearing facts: the index (and the per-plugin pages it heads) is **generated from `extensions/*/package.json` and `openclaw.plugin.json`**, it is **regenerated with the `pnpm plugins:inventory:gen` command**, and the full set of reference pages is browsed through **Plugin inventory** (the `/plugins/plugin-inventory` page), which lists **128 generated plugin reference pages by distribution, package, and description**. The page itself carries a `read_when` hint: consult it when you need a reference page for a specific OpenClaw plugin, or when auditing plugin docs coverage.

## How the Plugin Reference Is Generated

The Plugin reference is not hand-authored. The source page states verbatim that "This page is generated from `extensions/*/package.json` and `openclaw.plugin.json`." Each OpenClaw plugin lives in the `extensions/*` tree, and its identity and surface are declared in two files: the standard npm `package.json` (giving the package name, e.g. `@openclaw/<name>`) and the OpenClaw-specific `openclaw.plugin.json` plugin manifest (declaring what the plugin registers). The generator reads those declarations across all extensions and emits one reference page per plugin, so the catalog stays in lockstep with the actual `extensions/*` source rather than drifting as a separately maintained doc.

The page is regenerated with a single command, reproduced here verbatim from the source:

```bash
pnpm plugins:inventory:gen
```

This `pnpm` script is what re-derives the index and the per-plugin pages from the current `package.json` + `openclaw.plugin.json` set. The source page does not specify any flags, options, or output paths for the command beyond this invocation; nothing further is stated, so none is added here.

## Browsing the Reference: Plugin Inventory

The index points readers at a separate browse view for the full catalog. The source states: "Use Plugin inventory to browse all 128 generated plugin reference pages by distribution, package, and description" — linking the `/plugins/plugin-inventory` page. So the Plugin reference index is the conceptual entry point, while **Plugin inventory** (`/plugins/plugin-inventory`) is the navigable listing of all **128** generated pages, filterable/organized along three axes the source names explicitly: **distribution** (how the plugin is shipped — e.g. included in OpenClaw vs. installed from npm/ClawHub), **package** (the npm package id), and **description** (the one-line plugin summary). The per-plugin reference stub pages this index heads (e.g. `acpx`, `admin-http-rpc`, `alibaba`, `amazon-bedrock`, `amazon-bedrock-mantle`, `anthropic`) each render a Distribution block, a Surface block, and a Related docs pointer — but those are described in their own sibling notes, not here.

**Source**: OpenClaw documentation — `plugins/reference` (mirror `inbox/openclaw_docs/plugins/reference.md`)
**Last Updated**: 2026-06-22
**Status**: Active
