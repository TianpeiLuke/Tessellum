---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw acpx plugin
  - acp runtime backend
  - plugin-owned session transport
  - "@openclaw/acpx"
  - acpx surface skills
  - acpx npm clawhub install
  - acp agents setup
topics:
  - OpenClaw
  - Plugin Reference Catalog
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/acpx
access_control_group: ["general"]
---

# OpenClaw — ACPx Plugin (`@openclaw/acpx`) Reference

## Overview

This note is the generated plugin-reference descriptor for OpenClaw's **ACPx plugin**, mirroring the `plugins/reference/acpx` source page. The page is an auto-generated stub (one summary line plus three sections — `## Distribution`, `## Surface`, `## Related docs`) emitted from the plugin's `package.json` + `openclaw.plugin.json`. It records what the plugin *is* (the ACP runtime backend with plugin-owned session and transport management), how it is distributed (the `@openclaw/acpx` npm package, installed via npm or ClawHub), the contract surface it exposes (`skills`), and the related how-to it points at (ACP agents setup). The substantive runtime/protocol details live in the linked ACP and runtime docs and the `repo_openclaw*` code notes — this descriptor is the catalog entry that hangs off them.

## Distribution

The plugin's source-stated Distribution facts are reproduced verbatim:

- Package: `@openclaw/acpx`
- Install route: npm; ClawHub

So ACPx is not bundled "included in OpenClaw"; it is distributed as the `@openclaw/acpx` npm package and is also available through ClawHub (OpenClaw's plugin distribution channel). The source page states no version, no additional install commands, and no configuration keys — none are invented here.

## Surface

The source page's `## Surface` section lists exactly one surface entry:

skills

That is, ACPx registers a `skills` surface (it contributes skills to the host agent runtime). The page summary frames the plugin's role as the **OpenClaw ACP runtime backend with plugin-owned session and transport management** — i.e., ACPx is the plugin that backs OpenClaw's Agent Client Protocol (ACP) runtime, owning the session lifecycle and transport for ACP-speaking coding agents rather than delegating that ownership to the host. The page does not enumerate individual skill names, providers, or contract identifiers beyond `skills`, so none are listed here.

**Source**: OpenClaw documentation — `plugins/reference/acpx` (mirror `inbox/openclaw_docs/plugins/reference/acpx.md`)
**Last Updated**: 2026-06-22
**Status**: Active
