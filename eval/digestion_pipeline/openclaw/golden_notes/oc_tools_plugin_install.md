---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - plugins
keywords:
  - openclaw plugins install
  - openclaw plugins search clawhub
  - plugin install source clawhub npm git local
  - bare package spec resolution
  - native openclaw plugin vs compatible bundle
  - openclaw.plugin.json runtime module
  - gateway restart plugin reload
  - plugins inspect runtime json
  - npm compat pluginApi minHostVersion
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/plugin
access_control_group: ["general"]
---

# OpenClaw — Installing Plugins (Requirements, Quick Start, Install Sources, Formats)

## Overview

This note is the install half of the OpenClaw `tools/plugin` page: how to get a plugin running end to end. It covers what plugins extend, the prerequisites before installing, the five-step quick-start flow (find on ClawHub → install from a source → configure/enable → let the Gateway reload → verify runtime registration), how to choose an install source (`clawhub`/`npm`/`git`/local/marketplace) plus bare-spec resolution and npm compatibility scanning, and the two recognized plugin formats (native OpenClaw plugin vs compatible bundle). The configuration, operator install policy, plugin hooks, live-Gateway verification, and troubleshooting surfaces are documented separately in the config sibling.

Plugins extend OpenClaw with channels, model providers, agent harnesses, tools, skills, speech, realtime transcription, voice, media understanding, generation, web fetch, web search, and other runtime capabilities. For command-only examples, OpenClaw points to its `Manage plugins` page; for the full generated inventory of bundled, official external, and source-only plugins, it points to its `Plugin inventory` page.

## Requirements

Before installing a plugin, make sure you have:

- an OpenClaw checkout or installation with the `openclaw` CLI available;
- network access to the selected source, such as ClawHub, npm, or a git host;
- any plugin-specific credentials, config keys, or operating-system tools named by that plugin's setup docs;
- permission for the Gateway that serves your channels to reload or restart.

## Quick Start

The quick-start flow is a five-step sequence: find → install → configure/enable → let the Gateway reload → verify runtime registration.

### Step 1 — Find the plugin

Search ClawHub for public plugin packages:

```bash
openclaw plugins search "calendar"
```

ClawHub is the primary discovery surface for community plugins. During the launch cutover, ordinary bare package specs still install from npm unless they match an official plugin id. Raw `@openclaw/*` package specs that match bundled plugins use the bundled copy from the current OpenClaw build. Use an explicit prefix when you need one source.

### Step 2 — Install the plugin

Install from any of the supported sources:

```bash
# From ClawHub.
openclaw plugins install clawhub:<package>

# From npm.
openclaw plugins install npm:<package>

# From git.
openclaw plugins install git:github.com/<owner>/<repo>@<ref>

# From a local development checkout.
openclaw plugins install ./my-plugin
openclaw plugins install --link ./my-plugin
```

Treat plugin installs like running code. Prefer pinned versions when you need reproducible production installs.

### Step 3 — Configure and enable it

Configure plugin-specific settings under `plugins.entries.<id>.config`. Enable the plugin when it is not already enabled:

```bash
openclaw plugins enable <plugin-id>
```

If your config uses a restrictive `plugins.allow` list, the installed plugin id must be present there before the plugin can load. `openclaw plugins install` adds the installed id to an existing `plugins.allow` list and removes the same id from `plugins.deny` so the explicit install can load after restart.

### Step 4 — Let the Gateway reload

Installing, updating, or uninstalling plugin code requires a Gateway restart. When a managed Gateway is already running with config reload enabled, OpenClaw detects the changed plugin install record and restarts the Gateway automatically. If the Gateway is not managed or reload is disabled, restart it yourself:

```bash
openclaw gateway restart
```

Enable and disable operations update config and refresh the cold registry. A runtime inspect is still the clearest verification path for live runtime surfaces.

### Step 5 — Verify runtime registration

```bash
openclaw plugins inspect <plugin-id> --runtime --json
```

Use `--runtime` when you need to prove registered tools, hooks, services, Gateway methods, or plugin-owned CLI commands. Plain `inspect` is a cold manifest and registry check.

## Choose an Install Source

Pick a source by intent. The five install sources and when to use each:

| Source | Use when | Example |
| --- | --- | --- |
| ClawHub | You want OpenClaw-native discovery, scans, version metadata, and install hints | `openclaw plugins install clawhub:<package>` |
| npm | You need direct npm registry or dist-tag workflows | `openclaw plugins install npm:<package>` |
| git | You need a branch, tag, or commit from a repository | `openclaw plugins install git:github.com/<owner>/<repo>@<ref>` |
| local path | You are developing or testing a plugin on the same machine | `openclaw plugins install --link ./my-plugin` |
| marketplace | You are installing a Claude-compatible marketplace plugin | `openclaw plugins install <plugin> --marketplace <source>` |

### Bare-spec resolution rules

Bare package specs have special compatibility behavior. If the bare name matches a bundled plugin id, OpenClaw uses that bundled source. If it matches an official external plugin id, OpenClaw uses the official package catalog. Other ordinary bare package specs install through npm during the launch cutover. Raw `@openclaw/*` package specs that match bundled plugins also resolve to the bundled copy before npm fallback. Use `npm:@openclaw/<plugin>@<version>` when you deliberately want the external npm package instead of the image-owned bundled copy. Use `clawhub:`, `npm:`, `git:`, or `npm-pack:` when you need deterministic source selection. (OpenClaw points to `openclaw plugins`'s install section for the full command contract.)

### npm compatibility scanning

For npm installs, unpinned package specs and `@latest` choose the newest stable package that advertises compatibility with this OpenClaw build. If npm's current latest release declares a newer `openclaw.compat.pluginApi` or `openclaw.install.minHostVersion`, OpenClaw scans older stable package versions and installs the newest one that fits. Exact versions and explicit channel tags such as `@beta` stay pinned to the selected package and fail when incompatible.

## Understand Plugin Formats

OpenClaw recognizes two plugin formats:

| Format | How it loads | Use when |
| --- | --- | --- |
| Native OpenClaw plugin | `openclaw.plugin.json` plus a runtime module loaded in process | You are installing or building OpenClaw-specific runtime capabilities |
| Compatible bundle | Codex, Claude, or Cursor plugin layout mapped into OpenClaw plugin inventory | You are reusing compatible skills, commands, hooks, or bundle metadata |

Both formats appear in `openclaw plugins list`, `openclaw plugins inspect`, `openclaw plugins enable`, and `openclaw plugins disable`. (OpenClaw points to its `Plugin bundles` page for the bundle compatibility boundary and to `Building plugins` for native plugin authoring.)

**Source**: OpenClaw documentation — `tools/plugin` (mirror `inbox/openclaw_docs/tools/plugin.md`)
**Last Updated**: 2026-06-22
**Status**: Active
