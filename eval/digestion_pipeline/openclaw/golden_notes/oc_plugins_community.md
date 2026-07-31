---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - clawhub
keywords:
  - openclaw community plugins
  - clawhub plugin discovery
  - openclaw plugins search
  - openclaw plugins install
  - clawhub package publish
  - community plugin publish workflow
  - clawhub source prefix
  - plugin publish checklist
topics:
  - OpenClaw
  - Community Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/community
access_control_group: ["general"]
---

# OpenClaw — Finding and Publishing Community Plugins

## Overview

This procedure covers how to **discover and publish community-maintained OpenClaw plugins** through ClawHub, mirroring the `plugins/community` source page. Community plugins are third-party packages that extend OpenClaw with channels, tools, providers, hooks, or other capabilities, and **ClawHub is the primary discovery surface for public community plugins**. The page documents two task flows: finding (and installing) a plugin from the CLI using explicit source prefixes, and the publish workflow for sharing your own plugin — including the pre-publish checklist and what ClawHub validates before creating a release. The docs intentionally do **not** maintain a static third-party plugin catalog; ClawHub owns the live package listing, release history, scan status, and install hints.

## Find plugins

Search ClawHub from the CLI:

```bash
openclaw plugins search "calendar"
```

Install a ClawHub plugin with an **explicit source prefix**:

```bash
openclaw plugins install clawhub:<package-name>
```

**npm** remains a supported direct-install path during the launch cutover:

```bash
openclaw plugins install npm:<package-name>
```

For common install, update, inspect, and uninstall examples, the source page points to the **Manage plugins** page (`/plugins/manage-plugins`). For the full command reference and source-selection rules, it points to the **`openclaw plugins`** CLI reference (`/cli/plugins`).

## Publish plugins

Publish public community plugins on ClawHub when you want OpenClaw users to discover and install them. **ClawHub owns the live package listing, release history, scan status, and install hints; the docs do not maintain a static third-party plugin catalog.** Publishing uses the `clawhub package publish` command, run first as a dry run and then for real:

```bash
clawhub package publish your-org/your-plugin --dry-run
clawhub package publish your-org/your-plugin
```

Before publishing, make sure the plugin has **package metadata, a plugin manifest, setup docs, and a clear maintenance owner.** ClawHub **validates owner scope, package name, version, file limits, and source metadata** before it creates a release, then keeps new releases **hidden from normal install and download surfaces until review and verification finish.**

### Pre-publish checklist

The source page provides this checklist to satisfy before you publish:

| Requirement          | Why                                                 |
| -------------------- | --------------------------------------------------- |
| Published on ClawHub | Users need `openclaw plugins install` hints to work |
| Public GitHub repo   | Source review, issue tracking, transparency         |
| Setup and usage docs | Users need to know how to configure it              |
| Active maintenance   | Recent updates or responsive issue handling         |

### Full publishing contract

The source page directs you to three pages for the full publishing contract: **ClawHub publishing** (`/clawhub/publishing`) explains owners, scopes, releases, review, package validation, and package transfer; **Building plugins** (`/plugins/building-plugins`) shows the plugin package shape and first publish workflow; and **Plugin manifest** (`/plugins/manifest`) defines native plugin manifest fields.

**Source**: OpenClaw documentation — `plugins/community` (mirror `inbox/openclaw_docs/plugins/community.md`)
**Last Updated**: 2026-06-22
**Status**: Active
