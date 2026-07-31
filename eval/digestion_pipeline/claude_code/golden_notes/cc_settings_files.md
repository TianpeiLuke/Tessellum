---
tags:
  - resource
  - documentation
  - claude_code
  - settings
  - configuration
keywords:
  - settings.json
  - settings files
  - user project local settings
  - $schema autocomplete
  - when edits take effect
  - hot reload settings
  - ~/.claude.json
  - timestamped backups
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

# Claude Code — Settings Files

## Overview

The `settings.json` file is the official mechanism for configuring Claude Code through hierarchical settings. A user file (`~/.claude/settings.json`) applies to all projects; a project repository carries a shared, source-controlled `.claude/settings.json` and an untracked `.claude/settings.local.json` for personal preferences and experimentation. All files share the same JSON format, support a `$schema` line for editor autocomplete and validation, and are watched at runtime so most edits apply to the running session without a restart.

This note covers the settings-file mechanism itself: where the files live, the `$schema` autocomplete hook, when edits take effect (hot-reload vs read-once keys), the separate `~/.claude.json` "other configuration" store, and Claude Code's automatic timestamped backups. The scope/precedence ladder across these files lives in [cc_settings_scopes_and_precedence.md](cc_settings_scopes_and_precedence.md); the field-by-field key reference lives in [cc_settings_reference.md](cc_settings_reference.md); the managed (organization-deployed) delivery mechanisms and tolerant parsing of invalid entries live in [cc_managed_settings.md](cc_managed_settings.md).

## Settings file locations

The `settings.json` file configures Claude Code through hierarchical settings:

- **User settings** are defined in `~/.claude/settings.json` and apply to all projects.
- **Project settings** are saved in your project directory:
  - `.claude/settings.json` for settings that are checked into source control and shared with your team
  - `.claude/settings.local.json` for settings that are not checked in, useful for personal preferences and experimentation. When Claude Code creates `.claude/settings.local.json`, it configures git to ignore the file. If you create the file yourself, add it to your gitignore manually.
- **Managed settings**: For organizations that need centralized control, Claude Code supports multiple delivery mechanisms for managed settings. All use the same JSON format and cannot be overridden by user or project settings. (See [cc_managed_settings.md](cc_managed_settings.md) for the delivery mechanisms and invalid-entry handling.)

Each settings file uses the same JSON structure — for example, a user file with permission rules, environment variables, and company announcements:

```JSON Example settings.json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

## The `$schema` line

The `$schema` line in the example above points to the official JSON schema (`https://json.schemastore.org/claude-code-settings.json`) for Claude Code settings. Adding it to your `settings.json` enables autocomplete and inline validation in VS Code, Cursor, and any other editor that supports JSON schema validation.

The published schema is updated periodically and may not include settings added in the most recent CLI releases, so a validation warning on a recently documented field does not necessarily mean your configuration is invalid.

## When edits take effect

Claude Code watches your settings files and reloads them when they change, so edits to most keys apply to the running session without a restart. This includes `permissions`, `hooks`, and credential helpers like `apiKeyHelper`. The reload covers user, project, local, and managed settings, and the [`ConfigChange` hook](https://code.claude.com/docs/en/hooks) fires for each detected change.

A few keys are read once at session start and apply on the next restart instead:

- `model`: use [`/model`](https://code.claude.com/docs/en/model-config) to switch mid-session
- [`outputStyle`](https://code.claude.com/docs/en/output-styles): part of the system prompt, which is rebuilt on `/clear` or restart

## Other configuration: `~/.claude.json`

Other configuration is stored in `~/.claude.json`. This file contains your OAuth session, [MCP server](https://code.claude.com/docs/en/mcp) configurations for user and local scopes, per-project state (allowed tools, trust settings), and various caches. Project-scoped MCP servers are stored separately in `.mcp.json`.

## Timestamped backups

Claude Code automatically creates timestamped backups of configuration files and retains the five most recent backups to prevent data loss.

**Source**: https://code.claude.com/docs/en/settings
**Last Updated**: 2026-06-13
**Status**: Active
