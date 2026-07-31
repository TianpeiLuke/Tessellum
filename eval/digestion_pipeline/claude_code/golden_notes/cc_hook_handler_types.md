---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - configuration
keywords:
  - hook handler types
  - command hook
  - http hook
  - mcp tool hook
  - exec form shell form
  - path placeholders
  - claude_project_dir
  - hooks in skills and agents
  - hooks menu
  - disableallhooks
topics:
  - Claude Code
  - Hooks
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/hooks
access_control_group: ["general"]
---

# Claude Code Hooks — Handler Types and Locations

## Overview

A **hook handler** is the unit inside a matcher group's inner `hooks` array that actually runs when the matcher matches. Claude Code supports **five handler types**, selected by the required `type` field: `command` (a shell command), `http` (an HTTP POST endpoint), `mcp_tool` (a tool call on a connected MCP server), `prompt` (a single-turn LLM evaluation), and `agent` (an experimental tool-using subagent verifier). This note documents the type-specific fields for `command`, `http`, and `mcp_tool`, plus where you can define hooks (settings, plugins, skill/agent frontmatter), how path placeholders resolve script locations, the read-only `/hooks` inspection menu, and how to disable or remove hooks. The `if`/`timeout`/`statusMessage`/`once` **common fields** shared by all types, plus matcher patterns, are covered in the [matchers and common fields section](https://code.claude.com/docs/en/hooks); the `prompt` and `agent` LLM-judge types in [`cc_prompt_and_agent_hooks`](cc_prompt_and_agent_hooks.md).

## The five handler types

Each object in the inner `hooks` array is one handler. The `type` field picks the mechanism:

- **`command`** — runs a shell command. The script receives the event's JSON input on stdin and communicates results back through exit codes and stdout.
- **`http`** — sends the event's JSON input as an HTTP POST to a URL. The endpoint communicates results back through the response body using the same JSON output format as command hooks.
- **`mcp_tool`** — calls a tool on an already-connected MCP server. The tool's text output is treated like command-hook stdout.
- **`prompt`** — sends a prompt to a Claude model for single-turn evaluation; the model returns a yes/no decision as JSON (see sibling note).
- **`agent`** — spawns a subagent that can use tools like Read, Grep, and Glob to verify conditions before returning a decision. Agent hooks are experimental and may change.

All matching hooks run in parallel, and identical handlers are deduplicated automatically: command hooks by command string and `args`, HTTP hooks by URL. Handlers run in the current directory with Claude Code's environment; `$CLAUDE_CODE_REMOTE` is set to `"true"` in remote web environments and unset in the local CLI.

## Command hook fields

In addition to the common fields, command hooks accept `command` (required shell command), `args` (argument list — when present, `command` is resolved as an executable and spawned directly with no shell), `async` / `asyncRewake` (background execution — see [`cc_async_hooks`](cc_async_hooks.md)), and `shell` (`"bash"` default or `"powershell"`; ignored when `args` is set).

### Exec form and shell form

A command hook runs as **exec form** when `args` is set, and **shell form** when `args` is omitted. Set `args` whenever the hook references a path placeholder, since each element is passed as one argument with no quoting. Omit `args` when you need shell features like pipes or `&&`.

In **exec form**, Claude Code resolves `command` as an executable on `PATH` and spawns it directly with `args` as the argument vector — no shell, so each element is one argument exactly as written and special characters (apostrophes, `$`, backticks) pass through verbatim. In **shell form**, the `command` string is passed to a shell (`sh -c` on macOS/Linux, Git Bash on Windows, or PowerShell when Git Bash isn't installed); the shell tokenizes, expands variables, and interprets pipes, `&&`, redirects, and globs. On Windows, exec form requires `command` to resolve to a real executable (e.g. `.exe`); `.cmd`/`.bat` shims must be run via shell form or by invoking the underlying script with `node`.

```json
{
  "type": "command",
  "command": "node",
  "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/format.js", "--fix"]
}
```

The equivalent shell form needs quoting to handle paths with spaces or special characters:

```json
{
  "type": "command",
  "command": "node \"${CLAUDE_PLUGIN_ROOT}\"/scripts/format.js --fix"
}
```

## HTTP hook fields

HTTP hooks add `url` (required POST target), `headers` (key-value pairs supporting `$VAR_NAME`/`${VAR_NAME}` interpolation), and `allowedEnvVars` (the list of env var names that may be interpolated into headers — required for any interpolation; unlisted references become empty strings). Claude Code sends the JSON input as the POST body with `Content-Type: application/json`, and the response body uses the same JSON output format as command hooks. Error handling differs: non-2xx responses, connection failures, and timeouts all produce **non-blocking** errors that allow execution to continue. To block a tool call or deny a permission, an HTTP hook must return a 2xx response with a JSON body containing `decision: "block"` or a `hookSpecificOutput` with `permissionDecision: "deny"`.

```json
{
  "type": "http",
  "url": "http://localhost:8080/hooks/pre-tool-use",
  "timeout": 30,
  "headers": { "Authorization": "Bearer $MY_TOKEN" },
  "allowedEnvVars": ["MY_TOKEN"]
}
```

## MCP tool hook fields

MCP tool hooks add `server` (required — name of a configured MCP server that must already be connected; the hook never triggers an OAuth or connection flow), `tool` (required tool name on that server), and `input` (arguments passed to the tool; string values support `${path}` substitution from the hook's JSON input, such as `"${tool_input.file_path}"`). The tool's text content is treated like command-hook stdout — parsed as a decision if valid JSON output, otherwise shown as plain text. If the server is not connected or the tool returns `isError: true`, the hook produces a non-blocking error. MCP tool hooks are available on every event once servers are connected; `SessionStart` and `Setup` typically fire before servers finish connecting, so hooks there should expect a "not connected" error on first run. (MCP matcher naming → the ["Match MCP tools" section](https://code.claude.com/docs/en/hooks).)

```json
{
  "type": "mcp_tool",
  "server": "my_server",
  "tool": "security_scan",
  "input": { "file_path": "${tool_input.file_path}" }
}
```

## Reference scripts by path

Three placeholders reference hook scripts relative to a root regardless of the working directory when the hook runs: `${CLAUDE_PROJECT_DIR}` (the project root — also set in the environment of stdio MCP servers and plugin LSP servers), `${CLAUDE_PLUGIN_ROOT}` (the plugin's installation directory, which changes on each plugin update), and `${CLAUDE_PLUGIN_DATA}` (the plugin's persistent data directory). Both exec and shell form export these as the environment variables `CLAUDE_PROJECT_DIR`, `CLAUDE_PLUGIN_ROOT`, and `CLAUDE_PLUGIN_DATA` on the spawned process. Prefer exec form for any path placeholder; in shell form, wrap each placeholder in double quotes. Plugin hooks additionally substitute `${user_config.*}` values.

## Hooks in skills and agents

Beyond settings files and plugins, hooks can be defined directly in [skill](https://code.claude.com/docs/en/skills) and [subagent](https://code.claude.com/docs/en/sub-agents) frontmatter. These hooks use the same configuration format but are **scoped to the component's lifetime** and cleaned up when it finishes — they only run while that component is active. All hook events are supported. For subagents, `Stop` hooks are automatically converted to `SubagentStop`, since that is the event that fires when a subagent completes. (The `once` common field is only honored for hooks declared in skill frontmatter.)

```yaml
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

## The `/hooks` menu, and disabling hooks

Type `/hooks` in Claude Code to open a **read-only** browser of configured hooks. It shows every event with a count, lets you drill into matchers and a hook handler's full details, and labels each with a `[type]` prefix and a source: `User` (`~/.claude/settings.json`), `Project` (`.claude/settings.json`), `Local` (`.claude/settings.local.json`), `Plugin`, `Session` (registered in memory), or `Built-in`. The menu cannot edit hooks — to add, modify, or remove one, edit the settings JSON directly.

To remove a hook, delete its entry from the settings JSON. To temporarily disable all hooks without removing them, set `"disableAllHooks": true` in a settings file; there is no way to disable an individual hook while keeping it configured. `disableAllHooks` respects the managed settings hierarchy — only `disableAllHooks` at the managed settings level can disable managed-policy hooks. Direct edits in settings files are normally picked up automatically by the file watcher. Settings-file resolution and the `allowManagedHooksOnly` precedence are documented in [settings](https://code.claude.com/docs/en/settings).

**Source**: https://code.claude.com/docs/en/hooks
**Last Updated**: 2026-06-13
**Status**: Active
