---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - manifest
keywords:
  - plugin manifest
  - plugin.json schema
  - required name field
  - metadata fields
  - default enablement
  - component path fields
  - replace vs extend
  - unrecognized fields
  - strict validation
  - experimental components
topics:
  - Claude Code
  - Plugins
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/plugins-reference
access_control_group: ["general"]
---

# Claude Code — Plugin Manifest Schema (`plugin.json`)

## Overview

The `.claude-plugin/plugin.json` file defines a plugin's metadata and configuration. It is **optional**: if omitted, Claude Code auto-discovers components in their default locations (see [Plugin directory structure](cc_plugin_directory_structure.md)) and derives the plugin name from the directory name. A manifest is needed only when you want to supply metadata or point at custom component paths. This note is the field-by-field reference for that schema — required and metadata fields, default enablement, the component-path fields and their replace-vs-extend behavior, unrecognized-field tolerance, and experimental components.

Two related parts of the schema are documented separately: the `userConfig`, `channels`, and environment-variable substitution fields are covered in [User configuration and environment variables](cc_plugin_user_config_and_env.md), and the `dependencies` field plus version resolution are owned by the [plugin dependencies reference](https://code.claude.com/docs/en/plugin-dependencies).

## Complete schema

The manifest is a single JSON object. A complete example with every recognized top-level key:

```json
{
  "name": "plugin-name",
  "displayName": "Plugin Name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/reviewer.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "experimental": {
    "themes": "./themes/",
    "monitors": "./monitors.json"
  },
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

## Required fields

If you include a manifest, `name` is the **only** required field.

| Field  | Type   | Description                               | Example              |
| :----- | :----- | :---------------------------------------- | :------------------- |
| `name` | string | Unique identifier (kebab-case, no spaces) | `"deployment-tools"` |

The `name` is used for **namespacing** components. For example, the agent `agent-creator` belonging to the plugin named `plugin-dev` appears in the UI as `plugin-dev:agent-creator`.

## Unrecognized fields

Claude Code **ignores top-level fields it does not recognize**, so the plugin still loads. This makes it practical to maintain one manifest that doubles as a VS Code or Cursor extension manifest, an npm `package.json`, or an MCPB/DXT bundle manifest.

`claude plugin validate` reports unrecognized fields as **warnings, not errors**. If a field is one or two characters off from a recognized one, the warning suggests the likely intended name. A plugin with only unrecognized-field warnings still passes validation and loads at runtime.

Fields with the **wrong type still fail**: a `keywords` value that is a string instead of an array is a load error, and validation reports it as one. Pass `--strict` to treat warnings as errors — useful in CI to catch a misspelled field name or a leftover field from another tool's manifest before publishing, even though the plugin would load at runtime:

```bash
claude plugin validate ./my-plugin --strict
```

## Metadata fields

| Field            | Type    | Description                                                                                                                                                                                                                                          |
| :--------------- | :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$schema`        | string  | JSON Schema URL for editor autocomplete and validation. Ignored at load time.                                                                                                                                                                       |
| `displayName`    | string  | Human-readable name shown in the `/plugin` picker and other UI surfaces. Falls back to `name` when omitted; may contain spaces and any casing; not used for namespacing or lookup. Requires Claude Code v2.1.143 or later.                          |
| `version`        | string  | Optional semantic version. Setting it pins the plugin to that string, so users receive updates only when you bump it. If omitted, Claude Code falls back to the git commit SHA, treating every commit as a new version. `plugin.json` wins over the marketplace entry. |
| `description`    | string  | Brief explanation of plugin purpose.                                                                                                                                                                                                                |
| `author`         | object  | Author information (e.g. `{"name": "Dev Team", "email": "dev@company.com"}`).                                                                                                                                                                        |
| `homepage`       | string  | Documentation URL.                                                                                                                                                                                                                                   |
| `repository`     | string  | Source code URL.                                                                                                                                                                                                                                     |
| `license`        | string  | License identifier (e.g. `"MIT"`, `"Apache-2.0"`).                                                                                                                                                                                                   |
| `keywords`       | array   | Discovery tags (e.g. `["deployment", "ci-cd"]`).                                                                                                                                                                                                     |
| `defaultEnabled` | boolean | Whether the plugin starts enabled when the user has not set a state. Defaults to `true`. Requires Claude Code v2.1.154 or later.                                                                                                                     |

## Default enablement

Set `defaultEnabled: false` to ship a plugin that **installs disabled**; the user turns it on with `claude plugin enable <plugin>` or the `/plugin` interface. This is for plugins that add cost or scope a user should opt into, such as one that connects to an external service. Requires Claude Code v2.1.154 or later — earlier versions ignore the field and enable the plugin on install.

`defaultEnabled` is the fallback used only when nothing else has decided the plugin's state. Two things take precedence over it:

- **The user's setting** — an entry for the plugin in `enabledPlugins` at any settings scope. Once written, it persists across plugin updates and reinstalls, so changing `defaultEnabled` in a later release does not flip an existing user.
- **A dependency requirement** — when a plugin is required by another active plugin, Claude Code writes `true` for it at install or enable time, giving it an explicit setting so its own default no longer applies.

The same field can also appear in a plugin's marketplace entry, where it takes precedence over the value in `plugin.json`.

## Component path fields

These fields point the loader at custom component locations. Most accept a `string`, an `array`, or (for hooks/MCP/LSP) an inline `object`.

| Field                   | Type                  | Description                                                                                       |
| :---------------------- | :-------------------- | :------------------------------------------------------------------------------------------------ |
| `skills`                | string\|array         | Custom skill directories containing `<name>/SKILL.md` (in addition to default `skills/`)          |
| `commands`              | string\|array         | Custom flat `.md` skill files or directories (replaces default `commands/`)                       |
| `agents`                | string\|array         | Custom agent files (replaces default `agents/`)                                                   |
| `hooks`                 | string\|array\|object | Hook config paths or inline config                                                                |
| `mcpServers`            | string\|array\|object | MCP config paths or inline config                                                                 |
| `outputStyles`          | string\|array         | Custom output style files/directories (replaces default `output-styles/`)                         |
| `lspServers`            | string\|array\|object | Language Server Protocol configs for code intelligence                                            |
| `experimental.themes`   | string\|array         | Color theme files/directories (replaces default `themes/`)                                        |
| `experimental.monitors` | string\|array         | Background monitor configurations that start when the plugin is active                            |
| `userConfig`            | object                | User-configurable values prompted at enable time (see [User configuration and environment variables](cc_plugin_user_config_and_env.md)) |
| `channels`              | array                 | Channel declarations for message injection (see [User configuration and environment variables](cc_plugin_user_config_and_env.md))       |
| `dependencies`          | array                 | Other plugins this plugin requires (see [plugin dependencies](https://code.claude.com/docs/en/plugin-dependencies))                      |

## Path behavior rules (replace vs extend)

Whether a custom path **replaces** or **extends** the default directory depends on the field:

- **Replaces the default**: `commands`, `agents`, `outputStyles`, `experimental.themes`, `experimental.monitors`. When the manifest specifies `commands`, the default `commands/` directory is not scanned. To keep the default and add more, list it explicitly: `"commands": ["./commands/", "./extras/"]`.
- **Adds to the default**: `skills`. The default `skills/` directory is always scanned, and directories listed in `skills` are loaded alongside it.
- **Own merge rules**: `hooks`, `mcpServers`, and `lspServers` each combine multiple sources per their own section's rules.

When a plugin has both a default folder and the matching manifest key, Claude Code v2.1.140 and later flags the **ignored folder** in `/doctor`, `claude plugin list`, and the `/plugin` detail view; the plugin still loads using the manifest paths. No warning is shown when the manifest key points into the default folder (e.g. `"commands": ["./commands/deploy.md"]`), because the folder is addressed explicitly.

For all path fields:

- All paths must be **relative to the plugin root and start with `./`**.
- Components from custom paths use the same naming and namespacing rules.
- Multiple paths can be specified as arrays.
- When a skill path points to a directory containing a `SKILL.md` directly (e.g. `"skills": ["./"]` pointing at the plugin root), the frontmatter `name` field in `SKILL.md` determines the skill's invocation name, giving a stable name regardless of the install directory; if `name` is unset, the directory basename is the fallback.

A plugin that has a `SKILL.md` at its root, no `skills/` subdirectory, and no `skills` manifest field is automatically loaded as a **single-skill plugin** in Claude Code v2.1.142 and later — you do not need `"skills": ["./"]` for this layout. A sample of explicit array paths:

```json
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

## Experimental components

Components under the `experimental` key — `themes` and `monitors` — have a manifest schema that **may change between releases** while they stabilize. Where you declare them is a separate migration concern: the top level still works, `claude plugin validate` warns, and a future release will require `experimental.*`.

**Source**: https://code.claude.com/docs/en/plugins-reference
**Last Updated**: 2026-06-13
**Status**: Active
