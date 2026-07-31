---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - hooks
keywords:
  - openclaw hooks cli
  - agent hooks lifecycle
  - hooks list info check
  - enable disable hook
  - hook packs install update
  - bundled hooks session-memory boot-md
  - hooks.internal.entries config
  - plugin-managed hooks
topics:
  - OpenClaw
  - CLI Hooks
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/hooks
access_control_group: ["general"]
---

# OpenClaw — `openclaw hooks` CLI (Agent Hook Lifecycle)

## Overview

This note is the procedure for `openclaw hooks`, OpenClaw's CLI for managing **agent hooks** — event-driven automations that fire on commands like `/new`, `/reset`, and gateway startup. It mirrors the `cli/hooks` source page: discovering and inspecting hooks (`list` / `info` / `check`), the workspace opt-in via `enable` / `disable`, installing and updating hook packs through the unified `openclaw plugins` installer, and the four bundled hooks (`session-memory`, `bootstrap-extra-files`, `command-logger`, `boot-md`). Running `openclaw hooks` with no subcommand is equivalent to `openclaw hooks list`. The deeper hook-event model lives in the automation hooks and plugin hooks references (linked below), not here.

## Discover and Inspect Hooks

Three read-only subcommands surface hook availability. `openclaw hooks list` lists all discovered hooks from **workspace, managed, extra, and bundled** directories; Gateway startup does not load internal hook handlers until at least one internal hook is configured. `openclaw hooks info <name>` shows detailed information for one hook, where `<name>` is a hook name or hook key (e.g., `session-memory`). `openclaw hooks check` shows a summary of eligibility status (how many hooks are ready vs. not ready). Each accepts `--json`; `list` additionally takes `--eligible` (show only eligible hooks whose requirements are met) and `-v, --verbose` (show detailed information including missing requirements for ineligible hooks).

```bash
openclaw hooks list             # discovered hooks (workspace/managed/extra/bundled)
openclaw hooks list --verbose   # show missing requirements for ineligible hooks
openclaw hooks list --json      # structured JSON for programmatic use
openclaw hooks info <name>      # details for one hook (--json supported)
openclaw hooks check            # ready vs. not-ready summary (--json supported)
```

`openclaw hooks info session-memory` reports the hook's `Source` (e.g., `openclaw-bundled`), its `HOOK.md` `Path`, the `Handler` script path, `Homepage`, the subscribed `Events` (e.g., `command:new, command:reset`), and `Requirements` (e.g., `Config: ✓ workspace.dir`). Per the Notes, `openclaw hooks list --json`, `info --json`, and `check --json` write structured JSON directly to stdout.

## Enable / Disable a Hook

`openclaw hooks enable <name>` enables a specific hook by adding it to your config (`~/.openclaw/openclaw.json` by default); `openclaw hooks disable <name>` disables it by updating the config. The argument `<name>` is the hook name (e.g., `session-memory` to enable, `command-logger` to disable).

```bash
openclaw hooks enable session-memory    # → ✓ Enabled hook: 💾 session-memory
openclaw hooks disable command-logger   # → ⏸ Disabled hook: 📝 command-logger
```

Enabling checks that the hook exists and is eligible, sets `hooks.internal.entries.<name>.enabled = true` in your config, and saves the config to disk. **Workspace hooks are disabled by default until enabled here or in config** — if the hook came from `<workspace>/hooks/`, this opt-in step is required before the Gateway will load it. After enabling or disabling, **restart the gateway so hooks reload** (menu bar app restart on macOS, or restart your gateway process in dev).

### Plugin-managed hooks

Hooks managed by plugins show `plugin:<id>` in `openclaw hooks list` and **cannot be enabled or disabled here** — enable or disable the owning plugin instead.

## Install Hook Packs

Hook packs install through the unified plugins installer. `openclaw hooks install` still works as a compatibility alias, but it prints a deprecation warning and forwards to `openclaw plugins install`.

```bash
openclaw plugins install <package>        # npm by default
openclaw plugins install npm:<package>    # npm only
openclaw plugins install <package> --pin  # pin version
openclaw plugins install <path>           # local path
```

Npm specs are **registry-only** (package name + optional **exact version** or **dist-tag**); Git/URL/file specs and semver ranges are rejected. Dependency installs run project-local with `--ignore-scripts` for safety, even when your shell has global npm install settings. Bare specs and `@latest` stay on the stable track; if npm resolves either to a prerelease, OpenClaw stops and asks you to opt in explicitly with a prerelease tag such as `@beta`/`@rc` or an exact prerelease version. Supported archives are `.zip`, `.tgz`, `.tar.gz`, `.tar`.

Installing copies the hook pack into `~/.openclaw/hooks/<id>`, enables the installed hooks in `hooks.internal.entries.*`, and records the install under `hooks.internal.installs`. Options: `-l, --link` links a local directory instead of copying (adds it to `hooks.internal.load.extraDirs`); `--pin` records npm installs as exact resolved `name@version` in `hooks.internal.installs`. Linked hook packs are treated as managed hooks from an operator-configured directory, not as workspace hooks.

```bash
openclaw plugins install ./my-hook-pack          # local directory
openclaw plugins install ./my-hook-pack.zip      # local archive
openclaw plugins install @openclaw/my-hook-pack  # npm package
openclaw plugins install -l ./my-hook-pack       # link without copying
```

## Update Hook Packs

`openclaw plugins update <id>` (or `--all`) updates tracked npm-based hook packs through the unified plugins updater. `openclaw hooks update` still works as a compatibility alias but prints a deprecation warning and forwards to `openclaw plugins update`. Options are `--all` (update all tracked hook packs) and `--dry-run` (show what would change without writing). When a stored integrity hash exists and the fetched artifact hash changes, OpenClaw prints a warning and asks for confirmation before proceeding; use global `--yes` to bypass prompts in CI/non-interactive runs.

## Bundled Hooks

OpenClaw ships four bundled hooks, each enabled by name via `openclaw hooks enable <name>`.

- **`session-memory`** — saves session context to memory when you issue `/new` or `/reset`. Output goes to `~/.openclaw/workspace/memory/YYYY-MM-DD-HHMM.md` by default; set `hooks.internal.entries.session-memory.llmSlug: true` for model-generated filename slugs.
- **`bootstrap-extra-files`** — injects additional bootstrap files (for example monorepo-local `AGENTS.md` / `TOOLS.md`) during `agent:bootstrap`.
- **`command-logger`** — logs all command events to a centralized audit file at `~/.openclaw/logs/commands.log`. View it with `tail -n 20 ~/.openclaw/logs/commands.log`, pretty-print with `cat ~/.openclaw/logs/commands.log | jq .`, or filter with `grep '"action":"new"' ~/.openclaw/logs/commands.log | jq .`.
- **`boot-md`** — runs `BOOT.md` when the gateway starts (after channels start); subscribed `Events`: `gateway:startup`.

**Source**: OpenClaw documentation — `cli/hooks` (mirror `inbox/openclaw_docs/cli/hooks.md`)
**Last Updated**: 2026-06-22
**Status**: Active
