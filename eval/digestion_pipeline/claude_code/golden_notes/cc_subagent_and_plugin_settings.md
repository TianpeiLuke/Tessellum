---
tags:
  - resource
  - documentation
  - claude_code
  - settings
  - plugins
keywords:
  - subagent configuration
  - subagent file locations
  - plugin configuration
  - enabledPlugins
  - extraKnownMarketplaces
  - marketplace source types
  - plugin scope precedence
  - managing plugins
topics:
  - Claude Code
  - Settings
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/settings
access_control_group: ["general"]
---

# Claude Code — Subagent and Plugin Settings

## Overview

Claude Code is extended by two scoped customization surfaces configured through `settings.json` and the agents directory: **subagents** (custom AI assistants stored as Markdown files) and **plugins** (skills, agents, hooks, and MCP servers distributed through marketplaces). Both follow the scope system — user-scope files apply across all your projects, project-scope files are shared with your team — so where a subagent or plugin lives determines who can use it.

This note covers where subagent files live, how the `enabledPlugins` map enables/disables plugins and how its scopes resolve, how `extraKnownMarketplaces` registers additional marketplace sources for a repository (and the five source types), and the `/plugin` command for interactive management. The managed-only strict policy keys (`strictKnownMarketplaces`, `strictPluginOnlyCustomization`) are a separate enterprise governance layer covered in [Managed Plugin Policy Settings](cc_managed_plugin_policy_settings.md).

## Subagent configuration

Claude Code supports custom AI subagents that can be configured at both user and project levels. These subagents are stored as Markdown files with YAML frontmatter:

- **User subagents**: `~/.claude/agents/` — Available across all your projects
- **Project subagents**: `.claude/agents/` — Specific to your project and can be shared with your team

Subagent files define specialized AI assistants with custom prompts and tool permissions. Full authoring and usage detail is in the [subagents documentation](https://code.claude.com/docs/en/sub-agents).

## Plugin configuration

Claude Code supports a plugin system that lets you extend functionality with skills, agents, hooks, and MCP servers. Plugins are distributed through marketplaces and can be configured at both user and repository levels.

### Plugin settings

Plugin-related settings in `settings.json` use two keys — `enabledPlugins` (which plugins are on) and `extraKnownMarketplaces` (where they come from):

```json
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    }
  }
}
```

### `enabledPlugins`

Controls which plugins are enabled. Format: `"plugin-name@marketplace-name": true/false`. A plugin with no entry at any scope falls back to its `defaultEnabled` value.

**Scopes**:

- **User settings** (`~/.claude/settings.json`): Personal plugin preferences
- **Project settings** (`.claude/settings.json`): Project-specific plugins shared with team
- **Local settings** (`.claude/settings.local.json`): Per-machine overrides, gitignored when Claude Code creates it
- **Managed settings** (`managed-settings.json`): Organization-wide policy overrides that block installation at all scopes and hide the plugin from the marketplace

Project settings take precedence over user settings, so setting a plugin to `false` in `~/.claude/settings.json` does not disable a plugin that the project's `.claude/settings.json` enables. To opt out of a project-enabled plugin on your machine, set it to `false` in `.claude/settings.local.json` instead. Plugins force-enabled by managed settings cannot be disabled this way, since managed settings override local settings.

### `extraKnownMarketplaces`

Defines additional marketplaces that should be made available for the repository. Typically used in repository-level settings to ensure team members have access to required plugin sources.

When a repository includes `extraKnownMarketplaces`:

1. Team members are prompted to install the marketplace when they trust the folder
2. Team members are then prompted to install plugins from that marketplace
3. Users can skip unwanted marketplaces or plugins (stored in user settings)
4. Installation respects trust boundaries and requires explicit consent

**Marketplace source types** — each entry's `source` object declares one of:

- `github`: GitHub repository (uses `repo`)
- `git`: Any git URL (uses `url`)
- `directory`: Local filesystem path (uses `path`, for development only)
- `hostPattern`: regex pattern to match marketplace hosts (uses `hostPattern`)
- `settings`: inline marketplace declared directly in `settings.json` without a separate hosted repository (uses `name` and `plugins`)

The `git` source type works with any git hosting service, including self-hosted GitLab and Bitbucket. Claude Code clones the repository with the same authentication that `git clone` would use on that machine: configured credential helpers, SSH keys, or a host-specific token environment variable. For `github` and `git` sources, set `"skipLfs": true` inside the `source` object (alongside `repo` or `url`) to skip Git LFS downloads when cloning or updating the marketplace repository (requires Claude Code v2.1.153 or later). Each marketplace entry also accepts an optional `autoUpdate` Boolean: set `"autoUpdate": true` alongside `source` to refresh that marketplace and update its installed plugins at startup. When omitted, official Anthropic marketplaces default to `true` and all other marketplaces default to `false`.

Use `source: 'settings'` to declare a small set of plugins inline without setting up a hosted marketplace repository. Plugins listed here must reference external sources such as GitHub or npm. You still need to enable each plugin separately in `enabledPlugins`:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
```

The managed-only `strictKnownMarketplaces` (marketplace allowlist) and `strictPluginOnlyCustomization` (surface lockdown) keys are an enterprise governance layer that user and project scope cannot override — see [Managed Plugin Policy Settings](cc_managed_plugin_policy_settings.md).

### Managing plugins

Use the `/plugin` command to manage plugins interactively:

- Browse available plugins from marketplaces
- Install/uninstall plugins
- Enable/disable plugins
- View plugin details (skills, agents, hooks provided)
- Add/remove marketplaces

More on the plugin system is in the [plugins documentation](https://code.claude.com/docs/en/plugins).

**Source**: https://code.claude.com/docs/en/settings
**Last Updated**: 2026-06-13
**Status**: Active
