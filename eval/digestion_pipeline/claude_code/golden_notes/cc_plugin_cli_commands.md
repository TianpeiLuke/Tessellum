---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - cli
keywords:
  - claude plugin cli
  - plugin install scope
  - plugin init scaffold
  - skills-directory plugin
  - plugin enable disable
  - plugin details token cost
  - plugin uninstall keep-data
topics:
  - Claude Code
  - Plugins
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/plugins-reference
access_control_group: ["general"]
---

# Claude Code — Plugin CLI Commands & Install Scopes

## Overview

Claude Code exposes a `claude plugin` command family (and matching `/plugin` interactive forms) for non-interactive plugin management, useful for scripting and automation. The commands scaffold (`init`), install/remove (`install`, `uninstall`, `prune`), toggle (`enable`, `disable`), update, and inspect (`list`, `details`, `tag`) plugins. Most of these take a `--scope` flag — `user`, `project`, or `local` (with `managed` read-only) — that decides which settings file the plugin is written to and therefore who can use it.

A separate, install-free path is the **skills-directory plugin**: any folder under a skills directory that contains a `.claude-plugin/plugin.json` manifest is loaded as `<name>@skills-dir` on the next session, with no marketplace and no install step. Where it loads from (personal vs project) determines its trust gating. This note is the CLI/scope/skills-directory reference; dependency-related semantics of `prune` and `tag` are covered under [plugin dependencies](https://code.claude.com/docs/en/plugin-dependencies).

## Plugin installation scopes

When you install a plugin, you choose a **scope** that determines where the plugin is available and who else can use it:

| Scope     | Settings file                 | Use case                                                 |
| :-------- | :---------------------------- | :------------------------------------------------------- |
| `user`    | `~/.claude/settings.json`     | Personal plugins available across all projects (default) |
| `project` | `.claude/settings.json`       | Team plugins shared via version control                  |
| `local`   | `.claude/settings.local.json` | Project-specific plugins, gitignored                     |
| `managed` | Managed settings              | Managed plugins (read-only, update only)                 |

Plugins use the same scope system as other Claude Code configurations. `--scope project` writes to `enabledPlugins` in `.claude/settings.json`, making the plugin available to everyone who clones the project repository. For the full scope explanation, see [Configuration scopes](https://code.claude.com/docs/en/settings#configuration-scopes).

## Skills-directory plugins

Any folder under a skills directory that contains a `.claude-plugin/plugin.json` manifest is loaded as a plugin named `<name>@skills-dir` on the next session, with no marketplace and no install step. Scaffold one with `plugin init`. Unlike a marketplace install, the plugin is discovered in place rather than copied into the plugin cache. A skills directory tree supports three distinct things:

| What you have                                 | What it is                                                                          |
| :-------------------------------------------- | :---------------------------------------------------------------------------------- |
| `<skills-dir>/foo/SKILL.md` with no manifest  | A plain skill named `foo`                                                            |
| `<skills-dir>/foo/.claude-plugin/plugin.json` | A plugin `foo@skills-dir`, which can bundle its own skills, agents, hooks, and more |
| `<plugin>/skills/bar/SKILL.md`                | A skill `bar` packaged inside a plugin                                              |

**Choose where the plugin loads from.** `~/.claude/skills/` is personal scope and loads in every project, since the location is yours alone. `<cwd>/.claude/skills/` is project scope and loads only after you accept the workspace trust dialog for that folder. A project-scope plugin is checked into the repository and reaches every collaborator who clones it; because that content comes from the repo rather than from you, it loads only after the same trust gate that governs `.claude/settings.json`, and components that run code are restricted further: MCP servers it declares go through the same per-server approval as a project `.mcp.json`, LSP servers start only after you trust the workspace, and background monitors do not load. Personal-scope plugins have none of these restrictions. Note that project-scope `@skills-dir` plugins load only from the `.claude/skills/` of the directory where you start Claude Code — they do not walk up to the repository root, so launch from the repo root or run `/reload-plugins` after changing directories.

**Edit, reload, and disable.** Changes to a skill's `SKILL.md` take effect immediately in the current session; changes to other components (`hooks/`, `.mcp.json`, `agents/`, `output-styles/`) require `/reload-plugins` or a restart. To stop loading a skills-directory plugin, delete its folder or disable it by name — there is no `uninstall` step because nothing was installed from a marketplace:

```bash
claude plugin disable my-tool@skills-dir
```

## CLI commands reference

### plugin init

Scaffold a new plugin at `~/.claude/skills/<name>/`. On the next session it loads automatically as `<name>@skills-dir` and appears in `/plugin` and `claude plugin list` with no install step. The `<name>` becomes the skill namespace and directory name, so it cannot contain spaces or path separators. Options include `--description <text>`, `--author <name>` (default `git config user.name`), `--author-email <email>`, `-f, --force` (overwrite an existing `.claude-plugin/`), and `--with <components...>`. Each `--with` value adds a starter file for that component, ready to edit — valid values are `skills`, `agents`, `hooks`, `mcp`, `lsp`, `output-style`, and `channel`. Alias: `new`. The scaffolded plugin uses the `@skills-dir` source; admins can block this source via `strictKnownMarketplaces` or `blockedMarketplaces` in managed settings, in which case `plugin init` fails before writing.

```bash
# Scaffold a minimal plugin
claude plugin init my-helper

# Scaffold with skill and hook folders
claude plugin init my-helper --with skills hooks
```

### plugin install / uninstall

`claude plugin install <plugin> [options]` installs a plugin from available marketplaces; `<plugin>` is a plugin name or `plugin-name@marketplace-name`. The `-s, --scope <scope>` option (`user`, `project`, or `local`; default `user`) determines which settings file the installed plugin is added to.

```bash
claude plugin install formatter@my-marketplace --scope project
```

`claude plugin uninstall <plugin>` removes an installed plugin (aliases `remove`, `rm`). Options: `--scope`, `--keep-data` (preserve the persistent data directory), `--prune` (also remove auto-installed dependencies no other plugin requires), and `-y, --yes` (skip the `--prune` confirmation; required when stdin/stdout is not a TTY). By default, uninstalling from the last remaining scope also deletes the plugin's `${CLAUDE_PLUGIN_DATA}` directory; use `--keep-data` to preserve it, for example when reinstalling after testing a new version.

### plugin enable / disable

`claude plugin enable <plugin>` enables a disabled plugin; if the plugin declares dependencies, Claude Code enables them transitively at the same scope and fails when a dependency is not installed. `claude plugin disable <plugin>` disables a plugin without uninstalling it, and fails when another enabled plugin depends on the target (the error message includes a chained command that disables every dependent first). Both take `-s, --scope <scope>` (`user`, `project`, or `local`; default `user`). Dependency semantics are detailed under [plugin dependencies](https://code.claude.com/docs/en/plugin-dependencies).

### plugin update / prune

`claude plugin update <plugin>` updates a plugin to the latest version; its `--scope` accepts `user`, `project`, `local`, or `managed`. `claude plugin prune` (alias `autoremove`) removes auto-installed dependencies that are no longer required by any installed plugin — plugins you installed directly are never touched. It supports `--scope`, `--dry-run` (list what would be removed), and `-y, --yes`. To remove a plugin and clean up its dependencies in one step, run `claude plugin uninstall <plugin> --prune`. (`plugin prune` requires Claude Code v2.1.121 or later; its dependency logic is owned by [plugin dependencies](https://code.claude.com/docs/en/plugin-dependencies).)

### plugin list / details

`claude plugin list` lists installed plugins with version, source marketplace, and enable status; `--json` outputs JSON and `--available` (requires `--json`) includes available plugins from marketplaces. The interactive `/plugin list` (shorthand `ls`) prints the same listing inline and accepts `--enabled` / `--disabled` to filter by state.

`claude plugin details <name>` shows a plugin's component inventory and projected token cost. Components are grouped as Skills (both `skills/` and `commands/` entries), Agents, Hooks, MCP servers, and LSP servers. Each component reports two cost figures — **Always-on** (tokens added to every session by listing text such as skill/agent descriptions and command names, regardless of whether a component fires) and **On-invoke** (tokens a component costs when it fires, shown per component). The always-on total is computed via the `count_tokens` API for your active model, with per-component numbers proportionally scaled; if the API is unreachable, the command falls back to a character-based estimate.

```
dependency-guard 1.2.0
  Dependency analysis for Claude Code sessions
  Source: dependency-guard@example-marketplace

Component inventory
  Skills (2)  scan-dependencies, review-changes
  Agents (0)
  Hooks (1)  (harness-only — no model context cost)
  MCP servers (0)
  LSP servers (0)

Projected token cost
  Always-on:   ~180 tok   added to every session
```

### plugin tag

`claude plugin tag` creates a release git tag for the plugin in the current directory; run it from inside the plugin's folder. Options: `--push` (push the tag to the remote after creating it), `--dry-run`, and `-f, --force` (tag even if the working tree is dirty or the tag already exists). Tagging is used for dependency version resolution — see [plugin dependencies](https://code.claude.com/docs/en/plugin-dependencies#tag-plugin-releases-for-version-resolution).

**Source**: https://code.claude.com/docs/en/plugins-reference
**Last Updated**: 2026-06-13
**Status**: Active
