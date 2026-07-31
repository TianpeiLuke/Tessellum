---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - directory_structure
keywords:
  - plugin directory structure
  - claude-plugin manifest directory
  - plugin root layout
  - default component locations
  - file locations reference
  - single skill at root
  - standard plugin layout
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

# Claude Code — Plugin Directory Structure

## Overview

A Claude Code plugin is an on-disk directory whose components live in well-known locations that the loader scans automatically. The single firm rule: only `plugin.json` belongs inside `.claude-plugin/` — every other component directory (`skills/`, `commands/`, `agents/`, `hooks/`, `monitors/`, etc.) must sit at the **plugin root**, not nested inside `.claude-plugin/`. Because each component type has a default location, the manifest itself is optional when components use those defaults; the manifest is only needed for metadata or custom component paths (see [Plugin Manifest Schema](cc_plugin_manifest_schema.md)).

This note documents the standard plugin layout and the per-component default-location reference. What each component type *does* is covered in [Plugin Components](cc_plugin_components.md).

## Standard plugin layout

A complete plugin follows this structure (the `.claude-plugin/` metadata directory is optional; all other directories are at the plugin root):

```text
enterprise-plugin/
├── .claude-plugin/           # Metadata directory (optional)
│   └── plugin.json             # plugin manifest
├── skills/                   # Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── commands/                 # Skills as flat .md files
├── agents/                   # Subagent definitions
├── output-styles/            # Output style definitions
├── themes/                   # Color theme definitions
├── monitors/                 # Background monitor configurations
├── hooks/                    # Hook configurations
│   └── hooks.json           # Main hook config
├── bin/                      # Plugin executables added to PATH
├── settings.json            # Default settings for the plugin
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
├── scripts/                 # Hook and utility scripts
├── LICENSE                  # License file
└── CHANGELOG.md             # Version history
```

The `.claude-plugin/` directory contains the `plugin.json` file. All other directories (`commands/`, `agents/`, `skills/`, `output-styles/`, `themes/`, `monitors/`, `hooks/`) must be at the plugin root, not inside `.claude-plugin/`. (When components are misplaced inside `.claude-plugin/`, the plugin loads but its skills/agents/hooks go missing — see [Plugin Caching and Troubleshooting](cc_plugin_caching_and_troubleshooting.md).)

A `CLAUDE.md` file at the plugin root is **not** loaded as project context. Plugins contribute context through skills, agents, and hooks rather than CLAUDE.md. To ship instructions that load into Claude's context, put them in a skill.

## Single-skill-at-root layout

A plugin that ships exactly one skill can place `SKILL.md` directly at the plugin root instead of creating a `skills/` directory. Claude Code loads it as a single skill and uses the frontmatter `name` field for the invocation name. Use the `skills/` layout for plugins that may grow to more than one skill.

## File locations reference

Each component type has a default location relative to the plugin root:

| Component | Default Location | Purpose |
| :--- | :--- | :--- |
| Manifest | `.claude-plugin/plugin.json` | Plugin metadata and configuration (optional) |
| Skills | `skills/` | Skills with `<name>/SKILL.md` structure |
| Commands | `commands/` | Skills as flat Markdown files. Use `skills/` for new plugins |
| Agents | `agents/` | Subagent Markdown files |
| Output styles | `output-styles/` | Output style definitions |
| Themes | `themes/` | Color theme definitions |
| Hooks | `hooks/hooks.json` | Hook configuration |
| MCP servers | `.mcp.json` | MCP server definitions |
| LSP servers | `.lsp.json` | Language server configurations |
| Monitors | `monitors/monitors.json` | Background monitor configurations |
| Executables | `bin/` | Executables added to the Bash tool's `PATH`; invokable as bare commands in any Bash tool call while the plugin is enabled |
| Settings | `settings.json` | Default configuration applied when the plugin is enabled. Only the `agent` and `subagentStatusLine` keys are currently supported |

The lighter "structure overview" in the plugins guide presents the same set of root directories (plus the rule that `bin/` adds executables to the Bash tool's `PATH`). For plugins with many components, organize the directory structure by functionality; the manifest's component-path fields can override or extend these defaults (see [Plugin Manifest Schema](cc_plugin_manifest_schema.md)). To scaffold this layout, use `claude plugin init` (see [Plugin CLI Commands](cc_plugin_cli_commands.md)).

**Source**: https://code.claude.com/docs/en/plugins-reference
**Last Updated**: 2026-06-13
**Status**: Active
