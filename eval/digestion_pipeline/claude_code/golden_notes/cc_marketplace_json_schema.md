---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - marketplace
keywords:
  - marketplace.json schema
  - plugin marketplace catalog
  - plugin entries
  - reserved marketplace names
  - metadata.pluginRoot
  - allowCrossMarketplaceDependenciesOn
  - strict mode
  - component configuration fields
topics:
  - Claude Code
  - Plugins
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/plugin-marketplaces
access_control_group: ["general"]
---

# Claude Code — marketplace.json Schema

## Overview

A **`marketplace.json`** file is the catalog that defines a Claude Code plugin marketplace: its `name`, `owner` information, and a `plugins` array listing each plugin and where to fetch it. The file lives at `.claude-plugin/marketplace.json` in the repository root, and Claude Code reads and validates it when a user adds the marketplace.

This note is the field reference for that file — the marketplace-level required, owner, and optional fields (including `metadata.pluginRoot` and `allowCrossMarketplaceDependenciesOn`), and the per-plugin entry fields (required `name`/`source`, standard metadata, component-configuration fields, and `strict` mode). Each plugin entry's `source` field — the relative/`github`/`url`/`git-subdir`/`npm` source types — is covered in [Plugin sources](cc_plugin_sources.md), and the dependency-version `dependencies` array is covered in [Plugin dependencies](cc_plugin_dependencies.md).

## Create the marketplace file

Create `.claude-plugin/marketplace.json` in your repository root. This file defines your marketplace's name, owner information, and a list of plugins with their sources. Each plugin entry needs at minimum a `name` and `source` (where to fetch it from).

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation tools"
    }
  ]
}
```

## Marketplace schema

### Required fields

- **`name`** (string) — Marketplace identifier (kebab-case, no spaces). Public-facing: users see it when installing plugins (e.g. `/plugin install my-tool@your-marketplace`). Each user can register only one marketplace per name — adding a second marketplace with the same name **replaces** the first. To publish multiple plugins under one marketplace name, list them all in a single `marketplace.json`.
- **`owner`** (object) — Marketplace maintainer information (see Owner fields below).
- **`plugins`** (array) — List of available plugins.

> **Reserved names**: A set of marketplace names is reserved for official Anthropic use and cannot be used by third-party marketplaces (e.g. `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `agent-skills`, plus others). Names that **impersonate** official marketplaces, such as `official-claude-plugins` or `anthropic-tools-v2`, are also blocked.

### Owner fields

| Field   | Type   | Required | Description                      |
| :------ | :----- | :------- | :------------------------------- |
| `name`  | string | Yes      | Name of the maintainer or team   |
| `email` | string | No       | Contact email for the maintainer |

### Optional fields

| Field                                 | Type   | Description                                                                                                                                            |
| :------------------------------------ | :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$schema`                             | string | JSON Schema URL for editor autocomplete and validation. Claude Code ignores this field at load time.                                                  |
| `description`                         | string | Brief marketplace description                                                                                                                          |
| `version`                             | string | Marketplace manifest version                                                                                                                          |
| `metadata.pluginRoot`                 | string | Base directory prepended to relative plugin source paths (e.g. `"./plugins"` lets you write `"source": "formatter"` instead of `"source": "./plugins/formatter"`) |
| `allowCrossMarketplaceDependenciesOn` | array  | Other marketplaces that plugins in this marketplace may depend on. Dependencies from a marketplace not listed here are blocked at install.             |

`description` and `version` are also accepted under `metadata` for backward compatibility. The `allowCrossMarketplaceDependenciesOn` allowlist gates cross-marketplace dependency resolution — see [Plugin dependencies](cc_plugin_dependencies.md).

## Plugin entries

Each entry in the `plugins` array describes a plugin and where to find it. You can include any field from the plugin manifest schema (like `description`, `version`, `author`, `commands`, `hooks`, etc. — see the [plugin.json manifest schema](https://code.claude.com/docs/en/plugins-reference)), plus these marketplace-specific fields: `source`, `category`, `tags`, and `strict`.

### Required fields

- **`name`** (string) — Plugin identifier (kebab-case, no spaces). Public-facing: users see it when installing (e.g. `/plugin install my-plugin@marketplace`).
- **`source`** (string | object) — Where to fetch the plugin from. See [Plugin sources](cc_plugin_sources.md).

### Optional plugin fields

**Standard metadata fields:**

- **`displayName`** (string) — Human-readable name shown in UI surfaces. Falls back to `name` when omitted; may contain spaces and any casing; not used for namespacing or lookup. Requires Claude Code v2.1.143 or later.
- **`description`** (string) — Brief plugin description.
- **`version`** (string) — Plugin version. If set (here or in `plugin.json`), the plugin is pinned to this string and users only receive updates when it changes. Omit to fall back to the git commit SHA.
- **`author`** (object) — Plugin author information (`name` required, `email` optional).
- **`homepage`** (string) — Plugin homepage or documentation URL.
- **`repository`** (string) — Source code repository URL.
- **`license`** (string) — SPDX license identifier (e.g. `MIT`, `Apache-2.0`).
- **`keywords`** (array) — Tags for plugin discovery and categorization.
- **`category`** (string) — Plugin category for organization.
- **`tags`** (array) — Tags for searchability.
- **`strict`** (boolean) — Controls whether `plugin.json` is the authority for component definitions (default: `true`). See Strict mode below.
- **`defaultEnabled`** (boolean) — Whether the plugin is enabled after install (default: `true`). Set to `false` to install the plugin disabled until the user opts in. Takes precedence over the same field in the plugin's `plugin.json`. See [Default enablement](https://code.claude.com/docs/en/plugins-reference). Requires Claude Code v2.1.154 or later.

**Component configuration fields:**

| Field        | Type           | Description                                                    |
| :----------- | :------------- | :------------------------------------------------------------- |
| `skills`     | string\|array  | Custom paths to skill directories containing `<name>/SKILL.md` |
| `commands`   | string\|array  | Custom paths to flat `.md` skill files or directories          |
| `agents`     | string\|array  | Custom paths to agent files                                    |
| `hooks`      | string\|object | Custom hooks configuration or path to hooks file               |
| `mcpServers` | string\|object | MCP server configurations or path to MCP config                |
| `lspServers` | string\|object | LSP server configurations or path to LSP config                |

## Strict mode

The `strict` field controls whether `plugin.json` is the authority for component definitions (skills, agents, hooks, MCP servers, output styles):

| Value            | Behavior                                                                                                                                                         |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `true` (default) | `plugin.json` is the authority. The marketplace entry can supplement it with additional components, and both sources are merged.                                 |
| `false`          | The marketplace entry is the entire definition. If the plugin also has a `plugin.json` that declares components, that's a conflict and the plugin fails to load. |

Use `strict: true` when the plugin manages its own components and the marketplace entry only adds extras on top (the default, fits most plugins). Use `strict: false` when the marketplace operator wants full control: the plugin repo provides raw files, and the marketplace entry defines which files are exposed as skills, agents, hooks, etc. — useful when a marketplace curates a plugin's components differently than the plugin author intended.

**Source**: https://code.claude.com/docs/en/plugin-marketplaces
**Last Updated**: 2026-06-13
**Status**: Active
