---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - components
keywords:
  - plugin components
  - plugin skills agents hooks
  - mcp servers
  - lsp servers
  - background monitors
  - plugin themes
  - default agent settings
  - plugin component locations
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

# Claude Code — Plugin Components

## Overview

A Claude Code plugin can contribute **seven component types**: skills, agents, hooks, MCP servers, LSP servers, monitors, and themes. Each type has a default location in the plugin root and a file format; Claude Code auto-discovers each when the plugin is installed. This note is the reference for *what each component type is and where it lives* — the deep authoring detail for each type is owned by its own page (skills → [Skills](https://code.claude.com/docs/en/skills), agents → [Subagents](https://code.claude.com/docs/en/sub-agents), hooks → [Hooks](https://code.claude.com/docs/en/hooks), MCP → [MCP](https://code.claude.com/docs/en/mcp)).

Two cross-cutting facts shape the whole set: most components are referenced by *variable substitutions* like `${CLAUDE_PLUGIN_ROOT}` (see [User Config and Environment Variables](cc_plugin_user_config_and_env.md)), and for security some component capabilities are restricted or run unsandboxed depending on plugin trust scope.

## Skills

Plugins add skills, creating `/name` shortcuts that you or Claude can invoke. **Location**: `skills/` or `commands/` directory in the plugin root, or a single `SKILL.md` at the plugin root. **Format**: skills are directories with `SKILL.md`; commands are simple markdown files. Skills and commands are automatically discovered when the plugin is installed, Claude can invoke them automatically based on task context, and skills can include supporting files alongside `SKILL.md`.

If a plugin has no `skills/` directory and no `skills` manifest field, a `SKILL.md` at the plugin root is loaded as a single skill. Set the frontmatter `name` field to control the invocation name; without it Claude Code falls back to the install directory name (a version string that changes on every update for marketplace installs). For more than one skill, use the `skills/` directory layout.

## Agents

Plugins can provide specialized subagents Claude invokes automatically when appropriate. **Location**: `agents/` directory in the plugin root. **Format**: markdown files describing agent capabilities, e.g.:

```markdown
---
name: agent-name
description: What this agent specializes in and when Claude should invoke it
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Detailed system prompt for the agent describing its role, expertise, and behavior.
```

Plugin agents support `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, and `isolation` frontmatter fields. The only valid `isolation` value is `"worktree"`. **For security reasons, `hooks`, `mcpServers`, and `permissionMode` are not supported for plugin-shipped agents.** Agents appear in the `/agents` interface, can be invoked automatically or manually, and work alongside built-in Claude agents.

## Hooks

Plugins provide event handlers that respond to Claude Code events automatically. **Location**: `hooks/hooks.json` in the plugin root, or inline in `plugin.json`. **Format**: JSON configuration with event matchers and actions:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

Plugin hooks respond to the **same lifecycle events as user-defined hooks** — roughly 30, including `SessionStart`, `Setup`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`/`PermissionDenied`, `PostToolUse`/`PostToolUseFailure`/`PostToolBatch`, `SubagentStart`/`SubagentStop`, `TaskCreated`/`TaskCompleted`, `Stop`/`StopFailure`, `PreCompact`/`PostCompact`, `Elicitation`/`ElicitationResult`, `FileChanged`, `CwdChanged`, `WorktreeCreate`/`WorktreeRemove`, and `SessionEnd`. **Hook types** are `command` (run a shell command/script), `http` (POST the event JSON to a URL), `mcp_tool` (call a tool on a configured MCP server), `prompt` (evaluate a prompt with an LLM using the `$ARGUMENTS` placeholder), and `agent` (run an agentic verifier with tools). Event semantics are detailed in [Hooks](https://code.claude.com/docs/en/hooks).

## MCP servers

Plugins can bundle Model Context Protocol (MCP) servers to connect Claude Code with external tools and services. **Location**: `.mcp.json` in the plugin root, or inline in `plugin.json`. **Format**: standard MCP server configuration:

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

Plugin MCP servers **start automatically when the plugin is enabled**, appear as standard MCP tools in Claude's toolkit, integrate seamlessly with existing tools, and can be configured independently of user MCP servers.

## LSP servers

Plugins can provide Language Server Protocol (LSP) servers to give Claude real-time **code intelligence**: instant diagnostics after each edit, code navigation (go to definition, find references, hover), and language awareness (type info, symbol docs). **Location**: `.lsp.json` in the plugin root, or inline as `lspServers` in `plugin.json`. **Format**: JSON mapping language-server names to configurations:

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Required fields are `command` (the LSP binary, must be in PATH) and `extensionToLanguage` (maps file extensions to language identifiers). Optional fields include `args`, `transport` (`stdio` default or `socket`), `env`, `initializationOptions`, `settings`, `workspaceFolder`, `startupTimeout`, `maxRestarts`, and `diagnostics` (default `true`). **You must install the language-server binary separately** — the plugin only configures how Claude Code connects to it; a missing binary produces `Executable not found in $PATH` in the `/plugin` Errors tab. Official LSP plugins exist for Python (`pyright-lsp`), TypeScript (`typescript-lsp`), and Rust (`rust-analyzer-lsp`); create a custom LSP plugin only for languages not already covered.

## Monitors

Plugins can declare background monitors that Claude Code starts automatically when the plugin is active (requires v2.1.105+). Each monitor runs a shell command for the session lifetime and delivers every stdout line to Claude as a notification, so Claude reacts to log entries or status changes without being asked to start the watch. Monitors use the same mechanism as the [Monitor tool](https://code.claude.com/docs/en/tools-reference#monitor-tool): they run only in interactive CLI sessions, **run unsandboxed at the same trust level as hooks**, and are skipped where the Monitor tool is unavailable. **Location**: `monitors/monitors.json` in the plugin root, or inline `experimental.monitors`. **Format**: a JSON array of entries:

```json
[
  {
    "name": "deploy-status",
    "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/poll-deploy.sh ${user_config.api_endpoint}",
    "description": "Deployment status changes"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "on-skill-invoke:debug"
  }
]
```

Required fields are `name`, `command`, and `description`; the optional `when` controls start timing (`"always"` is the default; `"on-skill-invoke:<skill-name>"` starts it the first time that skill is dispatched). Disabling a plugin mid-session does not stop already-running monitors — they stop when the session ends. Monitors are an **experimental component**.

## Themes

Plugins can ship color themes that appear in `/theme` alongside built-in presets. A theme is a JSON file in `themes/` with a `base` preset and a sparse `overrides` map of color tokens:

```json
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Selecting a plugin theme persists `custom:<plugin-name>:<slug>` in the user's config. Plugin themes are read-only; pressing `Ctrl+E` on one copies it into `~/.claude/themes/` so the user can edit the copy. Themes are an **experimental component**.

## Ship default settings (`settings.json`)

A plugin can include a `settings.json` at its root to apply default configuration when enabled. Currently only the `agent` and `subagentStatusLine` keys are supported. Setting `agent` activates one of the plugin's custom agents as the main thread — applying its system prompt, tool restrictions, and model — so a plugin can change how Claude Code behaves by default (e.g. `{"agent": "security-reviewer"}`). Settings from `settings.json` take priority over `settings` declared in `plugin.json`; unknown keys are silently ignored.

**Source**: https://code.claude.com/docs/en/plugins-reference
**Last Updated**: 2026-06-13
**Status**: Active
