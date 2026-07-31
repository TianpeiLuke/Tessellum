---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - marketplaces
keywords:
  - plugin marketplace
  - add marketplace
  - install plugin
  - claude-plugins-official
  - claude-community
  - installation scope
  - extraknownmarketplaces
  - team marketplace
  - reload-plugins
  - plugin security
topics:
  - Claude Code
  - Plugins
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/discover-plugins
access_control_group: ["general"]
---

# Claude Code — Discover, Add Marketplaces, and Install Plugins

## Overview

Plugins extend Claude Code with skills, agents, hooks, and MCP servers, and **plugin marketplaces** are catalogs that let you discover and install these extensions without building them yourself. Using a marketplace is always a **two-step process**: first **add the marketplace** (registers the catalog so you can browse — no plugins installed yet), then **install individual plugins** from it. Think of it like an app store: adding the store gives you access to browse, but you still choose which apps to download.

This note is the procedure for the full flow — adding marketplaces from GitHub / Git / local / remote sources, installing plugins with `/plugin install name@marketplace`, choosing an installation scope, managing installed plugins and marketplaces, configuring auto-updates and team marketplaces, and the trust/security warning. Plugin **marketplace creation** and the `marketplace.json` schema are owned separately — see [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces).

## The marketplaces

### Official Anthropic marketplace

The official marketplace (`claude-plugins-official`) is **automatically available** when you start Claude Code. Run `/plugin` and go to the **Discover** tab to browse, or view the catalog at [claude.com/plugins](https://claude.com/plugins). Install with `/plugin install <name>@claude-plugins-official`:

```shell
/plugin install github@claude-plugins-official
```

If Claude Code reports the plugin is not found in any marketplace, the marketplace is missing or outdated: run `/plugin marketplace update claude-plugins-official` to refresh it, or `/plugin marketplace add anthropics/claude-plugins-official` if you never added it. The official marketplace is curated by Anthropic at its discretion; the in-app submission forms add to the community marketplace, not the official one. Its catalog spans **code intelligence** (LSP plugins — see [components](cc_plugin_components.md)), **external integrations** (pre-configured MCP servers: `github`, `gitlab`, `atlassian`, `linear`, `notion`, `figma`, `vercel`, `slack`, `sentry`, and more), **automatic security review** (`security-guidance`), **development workflows** (`commit-commands`, `pr-review-toolkit`, `agent-sdk-dev`, `plugin-dev`), and **output styles**.

### Community marketplace

The community marketplace ([`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community)) hosts third-party plugins that passed Anthropic's automated validation and safety screening; each plugin is pinned to a specific commit SHA. Unlike the official marketplace, you add it manually, then install with the `claude-community` name:

```shell
/plugin marketplace add anthropics/claude-plugins-community
/plugin install <plugin-name>@claude-community
```

### Try it: the demo marketplace

Anthropic also maintains a [demo marketplace](https://github.com/anthropics/claude-code/tree/main/plugins) (`claude-code-plugins`) with example plugins. Add it manually with `/plugin marketplace add anthropics/claude-code`, then run `/plugin` to open the tabbed plugin manager — **Discover**, **Installed**, **Marketplaces**, and **Errors** (cycle with **Tab** / **Shift+Tab**). When an administrator allowlists a marketplace via the `pluginSuggestionMarketplaces` managed setting, plugins relevant to your working directory are pinned at the top with a **suggested for this directory** label.

## Add marketplaces

Use `/plugin marketplace add` from four source types (shortcuts: `/plugin market`, and `rm` for `remove`):

- **GitHub repositories** — `owner/repo` format (the repo must contain `.claude-plugin/marketplace.json`): `/plugin marketplace add anthropics/claude-code`
- **Other Git hosts** — full URL, including GitLab, Bitbucket, self-hosted. Include the `.git` suffix so Claude Code clones the repo rather than treating the URL as a direct `marketplace.json` link. HTTPS: `/plugin marketplace add https://gitlab.com/company/plugins.git`; SSH: `git@gitlab.com:company/plugins.git`. Append `#<ref>` for a branch or tag (`...plugins.git#v1.0.0`).
- **Local paths** — a directory with `.claude-plugin/marketplace.json` (`/plugin marketplace add ./my-marketplace`) or a direct path to a `marketplace.json` file.
- **Remote URLs** — a hosted `marketplace.json` (`/plugin marketplace add https://example.com/marketplace.json`). URL-based marketplaces have limitations versus Git-based ones; "path not found" errors on install point to relative-path issues covered in the [marketplace troubleshooting](https://code.claude.com/docs/en/plugin-marketplaces#troubleshooting).

## Install plugins

Once a marketplace is added, install directly (defaults to **user scope**):

```shell
/plugin install plugin-name@marketplace-name
```

To choose a different installation scope, use the interactive UI: run `/plugin`, go to the **Discover** tab, and press **Enter** on a plugin. The detail pane shows what you're about to add before you commit — a **Context cost** token estimate (v2.1.143+), a **Last updated** date (v2.1.144+), and a **Will install** section listing the plugin's commands, agents, skills, hooks, and MCP/LSP servers (v2.1.145+). The scope choices:

- **User scope** (default): install for yourself across all projects.
- **Project scope**: install for all collaborators on this repository (adds to `.claude/settings.json`).
- **Local scope**: install for yourself in this repository only (not shared).

You may also see plugins with **managed** scope — installed by administrators via managed settings and not modifiable.

## Manage installed plugins and marketplaces

Run `/plugin` → **Installed** tab to view, enable, disable, or uninstall, grouped by scope and sorted problems-first (load errors / unresolved dependencies at top, favorites next, disabled folded at the bottom). Press `f` to favorite, type to filter, **Enter** to open a plugin's detail view (commands, skills, agents, hooks, MCP servers, LSP servers — also available via `claude plugin details`). Direct commands cover the same actions, with `--scope` to target a scope:

```shell
/plugin list
/plugin disable plugin-name@marketplace-name
/plugin enable plugin-name@marketplace-name
/plugin uninstall plugin-name@marketplace-name
```

**Apply changes without restarting**: after install/enable/disable during a session, run `/reload-plugins` to pick up all changes. It reloads plugins, skills, agents, hooks, and plugin MCP/LSP servers and shows counts. Reloading has a token cost on the next request; a plugin providing MCP servers whose tools aren't deferred by MCP tool search invalidates the prompt cache, so `/reload-plugins` shows a warning and skips the reload (pass `--force` to apply anyway).

**Manage marketplaces** via `/plugin` → **Marketplaces** tab, or CLI: `/plugin marketplace list`, `/plugin marketplace update <name>`, `/plugin marketplace remove <name>` (removing a marketplace uninstalls any plugins installed from it). **Auto-updates**: official Anthropic marketplaces have auto-update on by default; third-party and local-dev marketplaces have it off. Toggle per-marketplace in the UI. Set `DISABLE_AUTOUPDATER` to turn off all auto-updates, or pair it with `FORCE_AUTOUPDATE_PLUGINS=1` to keep plugin updates while managing Claude Code updates manually.

## Configure team marketplaces

Team admins enable automatic marketplace installation for a project by adding `extraKnownMarketplaces` to `.claude/settings.json`. When team members trust the repository folder, Claude Code prompts them to install the marketplaces and plugins:

```json
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Admins can also set `"autoUpdate": true` on each `extraKnownMarketplaces` entry to auto-update an org marketplace without each user toggling it. For full options including `enabledPlugins`, see [Plugin settings](https://code.claude.com/docs/en/settings#plugin-settings).

## Submit your plugin to the community marketplace

To distribute your own plugin, submit it for community-marketplace review via the in-app forms — claude.ai's `admin-settings/directory/submissions/plugins/new` (requires a Team/Enterprise org with directory-management access) or the Console form `platform.claude.com/plugins/submit` (for individual authors). Run `claude plugin validate` locally before submitting; the review pipeline runs the same check plus automated safety screening. Approved plugins are pinned to a specific commit SHA in the `anthropics/claude-plugins-community` catalog, with CI bumping the pin as you push new commits; the public catalog syncs nightly, so there is a delay between approval and your plugin appearing in `marketplace.json`. The official marketplace is curated separately — there is no application process and the form does not add plugins to it.

## Security

Plugins and marketplaces are **highly trusted components that can execute arbitrary code** on your machine with your user privileges. Only install plugins and add marketplaces from sources you trust; Anthropic does not control what MCP servers, files, or software a plugin includes and cannot verify it works as intended. Organizations can restrict which marketplaces users may add via [managed marketplace restrictions](https://code.claude.com/docs/en/plugin-marketplaces#managed-marketplace-restrictions). (For triaging marketplace/install failures, see [Plugin caching and troubleshooting](cc_plugin_caching_and_troubleshooting.md).)

**Source**: https://code.claude.com/docs/en/discover-plugins
**Last Updated**: 2026-06-13
**Status**: Active
