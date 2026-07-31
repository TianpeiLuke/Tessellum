---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - cli
keywords:
  - openclaw plugins list
  - openclaw plugins install
  - openclaw plugins update uninstall
  - clawhub npm git local install source
  - plugins inspect runtime registrations
  - managed gateway auto-restart
  - clawhub package publish
  - openclaw plugin manifest extensions
topics:
  - OpenClaw
  - Plugin Management
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/manage-plugins
access_control_group: ["general"]
---

# OpenClaw — Manage Plugins (CLI Quick Reference)

## Overview

This note is the everyday `openclaw plugins` command quick-reference: how to list/search, install, restart-and-inspect, update, and uninstall plugins, how to pick an install source (ClawHub / npm / git / local path / npm pack / marketplace), and the pointer to publishing. It mirrors the `plugins/manage-plugins` source page, which is the curated common-command surface; the exhaustive command contract, flags, source-selection rules, and edge cases live in [`openclaw plugins`](https://docs.openclaw.ai/cli/plugins). The page frames most install workflows as four steps: (1) find a package, (2) install it from ClawHub, npm, git, or a local path, (3) let the managed Gateway auto-restart (or restart it manually when unmanaged), and (4) verify the plugin's runtime registrations.

## List and search plugins

`openclaw plugins list` is a cold inventory check: it shows what OpenClaw can discover from config, manifests, and the plugin registry, but it does NOT prove that an already-running Gateway imported the plugin runtime. The common list/search variants are:

```bash
openclaw plugins list
openclaw plugins list --enabled
openclaw plugins list --verbose
openclaw plugins list --json
openclaw plugins search "calendar"
```

Use `--json` for scripts — for example, `openclaw plugins list --json | jq '.plugins[] | {id, enabled, format, source, dependencyStatus}'`. The JSON output includes registry diagnostics and each plugin's static `dependencyStatus` when the plugin package declares `dependencies` or `optionalDependencies`. `openclaw plugins search` queries ClawHub for installable plugin packages and prints install hints such as `openclaw plugins install clawhub:<package>`.

## Install plugins

Install accepts a source-prefixed spec (`clawhub:`, `npm:`, `git:`, `npm-pack:`) or a bare/local path. Bare package specs install from npm during the launch cutover; use an explicit prefix when you need deterministic source selection. If the bare name matches an official plugin id, OpenClaw can install the catalog entry directly:

```bash
# Search ClawHub for plugin packages.
openclaw plugins search "calendar"

# Install from ClawHub.
openclaw plugins install clawhub:<package>
openclaw plugins install clawhub:<package>@1.2.3
openclaw plugins install clawhub:<package>@beta

# Install from npm.
openclaw plugins install npm:<package>
openclaw plugins install npm:@scope/openclaw-plugin@1.2.3
openclaw plugins install npm:@openclaw/codex

# Install from a local npm pack artifact.
openclaw plugins install npm-pack:<path.tgz>

# Install from git or a local development checkout.
openclaw plugins install git:github.com/acme/openclaw-plugin@v1.0.0
openclaw plugins install ./my-plugin
openclaw plugins install --link ./my-plugin
```

Use `--force` ONLY when you intentionally want to overwrite an existing install target. For routine upgrades of tracked npm, ClawHub, or hook-pack installs, use `openclaw plugins update` instead.

## Restart and inspect

After installing, updating, or uninstalling plugin code, a running managed Gateway with config reload enabled restarts automatically. If the Gateway is not managed or reload is disabled, restart it yourself before checking live runtime surfaces:

```bash
openclaw gateway restart
openclaw plugins inspect <plugin-id> --runtime --json
```

Use `inspect --runtime` when you need PROOF that the plugin registered runtime surfaces such as tools, hooks, services, Gateway methods, HTTP routes, or plugin-owned CLI commands. Plain `inspect` and `list` are cold manifest, config, and registry checks (they do not confirm live runtime import).

## Update plugins

When you pass a plugin id, OpenClaw reuses the tracked install spec; stored dist-tags such as `@beta` and exact pinned versions continue to be used on later `update <plugin-id>` runs:

```bash
openclaw plugins update <plugin-id>
openclaw plugins update <npm-package-or-spec>
openclaw plugins update --all
openclaw plugins update <plugin-id> --dry-run
```

For npm installs, you can pass an explicit package spec to switch the tracked record. `openclaw plugins update @scope/openclaw-plugin@beta` repins to the `@beta` line, while `openclaw plugins update @scope/openclaw-plugin` (no tag) moves a plugin back to the registry's default release line when it was previously pinned to an exact version or tag. When `openclaw update` runs on the beta channel, plugin records can prefer matching `@beta` releases; for the exact fallback and pinning rules see [`openclaw plugins`](https://docs.openclaw.ai/cli/plugins#update).

## Uninstall plugins

Uninstall removes the plugin's config entry, persisted plugin index record, allow/deny list entries, and linked load paths when applicable. Managed install directories are removed unless you pass `--keep-files`. A running managed Gateway restarts automatically when the uninstall changes plugin source:

```bash
openclaw plugins uninstall <plugin-id> --dry-run
openclaw plugins uninstall <plugin-id>
openclaw plugins uninstall <plugin-id> --keep-files
```

In Nix mode (`OPENCLAW_NIX_MODE=1`), plugin install, update, uninstall, enable, and disable commands are DISABLED — manage those choices in the Nix source for the install instead.

## Choose a source

The install source determines discovery, versioning, and how the spec is tracked. Pick per the source table:

| Source      | Use when                                                                    | Example                                                        |
| ----------- | --------------------------------------------------------------------------- | -------------------------------------------------------------- |
| ClawHub     | You want OpenClaw-native discovery, scan summaries, versions, and hints     | `openclaw plugins install clawhub:<package>`                   |
| npmjs.com   | You already ship JavaScript packages or need npm dist-tags/private registry | `openclaw plugins install npm:@acme/openclaw-plugin`           |
| git         | You want a branch, tag, or commit from a repository                         | `openclaw plugins install git:github.com/<owner>/<repo>@<ref>` |
| local path  | You are developing or testing a plugin on the same machine                  | `openclaw plugins install --link ./my-plugin`                  |
| npm pack    | You are proving a local package artifact through npm install semantics      | `openclaw plugins install npm-pack:<path.tgz>`                 |
| marketplace | You are installing a Claude-compatible marketplace plugin                   | `openclaw plugins install <plugin> --marketplace <source>`     |

Managed local path installs must be plugin directories or archives. Put standalone plugin files in `plugins.load.paths` instead of installing them with `plugins install`.

## Publish plugins

ClawHub is the primary public discovery surface for OpenClaw plugins — publish there when you want users to find plugin metadata, version history, registry scan results, and install hints before they install (via `npm i -g clawhub`, `clawhub login`, then `clawhub package publish your-org/your-plugin` with optional `--dry-run` or an `@v1.0.0` version). Native npm plugins must include a plugin manifest and package metadata before publishing — the `package.json` declares `"type": "module"` and an `openclaw.extensions` entrypoint array:

```json package.json
{
  "name": "@acme/openclaw-plugin",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./dist/index.js"]
  }
}
```

After publishing with `npm publish --access public`, the package installs via `openclaw plugins install npm:@acme/openclaw-plugin` (optionally with `@beta` or `@1.0.0`). For the full publishing contract, use the dedicated pages rather than treating this quick-reference as authoritative: [ClawHub publishing](https://docs.openclaw.ai/clawhub/publishing) (owners, scopes, releases, review, package validation, package transfer), [Building plugins](https://docs.openclaw.ai/plugins/building-plugins) (plugin package shape + first publish workflow), and [Plugin manifest](https://docs.openclaw.ai/plugins/manifest) (native plugin manifest fields). If the same package is available on both ClawHub and npm, use the explicit `clawhub:` or `npm:` prefix when you need to force one source.

**Source**: OpenClaw documentation — `plugins/manage-plugins` (mirror `inbox/openclaw_docs/plugins/manage-plugins.md`)
**Last Updated**: 2026-06-22
**Status**: Active
