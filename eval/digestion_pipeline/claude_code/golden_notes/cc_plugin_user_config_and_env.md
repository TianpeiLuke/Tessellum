---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - configuration
keywords:
  - userConfig
  - user configuration prompts
  - sensitive config secure storage
  - channels mcp injection
  - CLAUDE_PLUGIN_ROOT
  - CLAUDE_PLUGIN_DATA
  - CLAUDE_PROJECT_DIR
  - persistent data directory
  - variable substitution
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

# Claude Code — Plugin User Configuration and Environment Variables

## Overview

Beyond declaring components, a plugin's `.claude-plugin/plugin.json` can drive **runtime configuration** through three related manifest features: `userConfig` declares values Claude Code prompts the user for at enable time (instead of making them hand-edit `settings.json`), `channels` declares MCP-backed message channels that inject content into the conversation, and a set of **substitution variables** lets the plugin reference paths and config values inline. This note covers those configuration surfaces plus the three environment variables Claude Code provides (`${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_PROJECT_DIR}`) and the persistent-data-directory pattern for state that must survive plugin updates.

The schema fields and component types these settings attach to are covered in [Plugin manifest schema](cc_plugin_manifest_schema.md) and [Plugin components](cc_plugin_components.md).

## User configuration (`userConfig`)

The `userConfig` field declares values Claude Code prompts the user for when the plugin is enabled. Use this instead of requiring users to hand-edit `settings.json`. Keys must be valid identifiers.

```json
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "Your team's API endpoint"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "API authentication token",
      "sensitive": true
    }
  }
}
```

Each option supports these fields:

| Field | Required | Description |
| :--- | :--- | :--- |
| `type` | Yes | One of `string`, `number`, `boolean`, `directory`, or `file` |
| `title` | Yes | Label shown in the configuration dialog |
| `description` | Yes | Help text shown beneath the field |
| `sensitive` | No | If `true`, masks input and stores the value in secure storage instead of `settings.json` |
| `required` | No | If `true`, validation fails when the field is empty |
| `default` | No | Value used when the user provides nothing |
| `multiple` | No | For `string` type, allow an array of strings |
| `min` / `max` | No | Bounds for `number` type |

**Where values are usable.** Each value is available for substitution as `${user_config.KEY}` in MCP and LSP server configs, hook commands, and monitor commands. Non-sensitive values can also be substituted in skill and agent content. All values are exported to plugin subprocesses as `CLAUDE_PLUGIN_OPTION_<KEY>` environment variables.

**Where values are stored.** Non-sensitive values are stored in `settings.json` under `pluginConfigs[<plugin-id>].options`. Sensitive values go to the system keychain (or `~/.claude/.credentials.json` where the keychain is unavailable). Keychain storage is shared with OAuth tokens and has an approximately 2 KB total limit, so keep sensitive values small.

## Channels

The `channels` field lets a plugin declare one or more message channels that inject content into the conversation. Each channel binds to an MCP server that the plugin provides.

```json
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        },
        "owner_id": {
          "type": "string",
          "title": "Owner ID",
          "description": "Your Telegram user ID"
        }
      }
    }
  ]
}
```

The `server` field is required and must match a key in the plugin's `mcpServers`. The optional per-channel `userConfig` uses the same schema as the top-level field, letting the plugin prompt for bot tokens or owner IDs when the plugin is enabled.

## Environment variables

Claude Code provides three variables for referencing paths. All are substituted inline anywhere they appear in skill content, agent content, hook commands, monitor commands, and MCP or LSP server configs. All are also exported as environment variables to hook processes and MCP or LSP server subprocesses.

- **`${CLAUDE_PLUGIN_ROOT}`** — the absolute path to your plugin's installation directory. Use this to reference scripts, binaries, and config files bundled with the plugin. In hook commands, use exec form with `args` so the path is passed as one argument with no quoting; in shell-form hooks and monitor commands, wrap it in double quotes, as in `"${CLAUDE_PLUGIN_ROOT}"`. **This path changes when the plugin updates.** The previous version's directory remains on disk for about seven days after an update before cleanup, but treat it as ephemeral and do not write state here.
- **`${CLAUDE_PLUGIN_DATA}`** — a persistent directory for plugin state that survives updates. Use this for installed dependencies such as `node_modules` or Python virtual environments, generated code, caches, and any other files that should persist across plugin versions. The directory is created automatically the first time this variable is referenced.
- **`${CLAUDE_PROJECT_DIR}`** — the project root. This is the same directory hooks receive in their `CLAUDE_PROJECT_DIR` variable. Use this to reference project-local scripts or config files. Wrap in quotes to handle paths with spaces. MCP servers can also call the MCP `roots/list` request, which returns the directory Claude Code was launched from.

When a plugin updates mid-session, hook commands, monitors, MCP servers, and LSP servers keep using the previous version's path. Run `/reload-plugins` to switch hooks, MCP servers, and LSP servers to the new path; monitors require a session restart.

## Persistent data directory

The `${CLAUDE_PLUGIN_DATA}` directory resolves to `~/.claude/plugins/data/{id}/`, where `{id}` is the plugin identifier with characters outside `a-z`, `A-Z`, `0-9`, `_`, and `-` replaced by `-`. For a plugin installed as `formatter@my-marketplace`, the directory is `~/.claude/plugins/data/formatter-my-marketplace/`.

A common use is installing language dependencies once and reusing them across sessions and plugin updates. Because the data directory outlives any single plugin version, a check for directory existence alone cannot detect when an update changes the plugin's dependency manifest. The recommended pattern compares the bundled manifest against a copy in the data directory and reinstalls when they differ. This `SessionStart` hook installs `node_modules` on the first run and again whenever a plugin update includes a changed `package.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

The `diff` exits nonzero when the stored copy is missing or differs from the bundled one, covering both first run and dependency-changing updates. If `npm install` fails, the trailing `rm` removes the copied manifest so the next session retries. Scripts bundled in `${CLAUDE_PLUGIN_ROOT}` can then run against the persisted `node_modules` (for example, an MCP server launched with `NODE_PATH` set to `${CLAUDE_PLUGIN_DATA}/node_modules`).

The data directory is deleted automatically when you uninstall the plugin from the last scope where it is installed. The `/plugin` interface shows the directory size and prompts before deleting; the CLI deletes by default, and you pass `--keep-data` to preserve it.

**Source**: https://code.claude.com/docs/en/plugins-reference
**Last Updated**: 2026-06-13
**Status**: Active
