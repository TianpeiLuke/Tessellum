---
tags:
  - resource
  - documentation
  - claude_code
  - cli
  - flags
keywords:
  - claude code cli flags
  - runtime flags
  - permission-mode flag
  - model flag
  - mcp-config flag
  - print mode flags
  - dangerously-skip-permissions
  - per-session override
topics:
  - Claude Code
  - CLI
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/cli-reference
access_control_group: ["general"]
---

# Claude Code — CLI Flags

## Overview

CLI flags customize the behavior of the `claude` command for a single invocation. They are passed alongside a command (e.g. `claude --model claude-sonnet-4-6 "query"`) and, where they overlap with a persistent setting, **override that setting for the current session only** without changing the file-based value. The flag list is large (~45 flags); this note groups them by function. One caution from the docs: `claude --help` does **not** list every flag, so a flag's absence from `--help` does not mean it is unavailable.

This note covers the general runtime flags. The four system-prompt customization flags (`--system-prompt`, `--system-prompt-file`, `--append-system-prompt`, `--append-system-prompt-file`) get their own decision-rule note, `cc_cli_system_prompt_flags`. Permission-rule pattern syntax, the settings keys these flags override, and environment variables are each owned by other reference notes and are linked rather than re-defined here.

## Session and resume flags

These control how a session is started, named, persisted, or resumed:

- `--continue`, `-c` — Load the most recent conversation in the current directory. Includes sessions that added this directory with `/add-dir`.
- `--resume`, `-r` — Resume a specific session by ID or name, or show an interactive picker. The picker and name search include sessions that added this directory with `/add-dir`; passing a session ID searches only the current project directory and its git worktrees. As of v2.1.144, background sessions appear in the picker marked with `bg`.
- `--fork-session` — When resuming, create a new session ID instead of reusing the original (use with `--resume` or `--continue`).
- `--from-pr` — Resume sessions linked to a specific pull request. Accepts a PR number, or a GitHub / GitHub Enterprise / GitLab merge request / Bitbucket pull request URL. Sessions are linked automatically when Claude creates the pull request.
- `--session-id` — Use a specific session ID for the conversation (must be a valid UUID).
- `--name`, `-n` — Set a display name for the session, shown in `/resume` and the terminal title. Resume a named session with `claude --resume <name>`. `/rename` changes the name mid-session.
- `--no-session-persistence` — Disable session persistence so sessions are not saved to disk and cannot be resumed (print mode only). `CLAUDE_CODE_SKIP_PROMPT_HISTORY` does the same in any mode.

## Model and effort flags

- `--model` — Set the model for the current session with an alias (`sonnet`, `opus`, `haiku`, or `fable`) or a model's full name. Overrides the `model` setting and `ANTHROPIC_MODEL`.
- `--advisor <model>` — Enable the server-side advisor tool for this session with a model alias (`opus`, `sonnet`, or `fable` in v2.1.170+) or a full model ID. Takes precedence over the `advisorModel` setting. Requires Claude Code v2.1.98+.
- `--effort` — Set the effort level for the current session. Options: `low`, `medium`, `high`, `xhigh`, `max`; available levels depend on the model. Overrides the `effortLevel` setting and does not persist.
- `--fallback-model` — Enable automatic fallback to the specified model(s) when the primary is overloaded or unavailable. Accepts a comma-separated list tried in order. Overrides the persistent `fallbackModel` setting.

## Permissions and tools flags

These shape the trust ladder and which tools are usable for the session:

- `--permission-mode` — Begin in a specified permission mode. Accepts `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, or `bypassPermissions`. Overrides `defaultMode` from settings files.
- `--dangerously-skip-permissions` — Skip permission prompts. Equivalent to `--permission-mode bypassPermissions`.
- `--allow-dangerously-skip-permissions` — Add `bypassPermissions` to the `Shift+Tab` mode cycle without starting in it, so you can begin in another mode (like `plan`) and switch later.
- `--allowedTools`, `--allowed-tools` — Tools that execute without prompting for permission. To restrict which tools are *available*, use `--tools` instead.
- `--disallowedTools`, `--disallowed-tools` — Deny rules. A bare tool name removes the matching tools from the model's context (`"Edit"` removes Edit, `"*"` removes every tool, `"mcp__*"` removes every MCP tool). A scoped rule such as `Bash(rm *)` leaves the tool available and denies only matching calls.
- `--tools` — Restrict which built-in tools Claude can use. Use `""` to disable all, `"default"` for all, or tool names like `"Bash,Edit,Read"`. MCP tools are not affected.
- `--permission-prompt-tool` — Specify an MCP tool to handle permission prompts in non-interactive mode.

## MCP and plugin flags

- `--mcp-config` — Load MCP servers from JSON files or strings (space-separated).
- `--strict-mcp-config` — Only use MCP servers from `--mcp-config`, ignoring all other MCP configurations.
- `--plugin-dir` — Load a plugin from a directory or `.zip` archive for this session only. Each flag takes one path; repeat for multiple plugins.
- `--plugin-url` — Fetch a plugin `.zip` archive from a URL for this session only. Repeat the flag or pass space-separated URLs in one quoted value.
- `--channels` — (Research preview) MCP servers whose channel notifications Claude should listen for this session. Space-separated `plugin:<name>@<marketplace>` entries. Requires Claude.ai authentication.
- `--dangerously-load-development-channels` — Enable channels not on the approved allowlist, for local development. Accepts `plugin:<name>@<marketplace>` and `server:<name>` entries. Prompts for confirmation.
- `--disable-slash-commands` — Disable all skills and commands for this session.

## Print-mode and output flags

These apply to non-interactive (`-p` / print) runs and scripting:

- `--print`, `-p` — Print response without interactive mode.
- `--output-format` — Output format for print mode: `text`, `json`, or `stream-json`.
- `--input-format` — Input format for print mode: `text` or `stream-json`.
- `--json-schema` — Get validated JSON output matching a JSON Schema after the agent completes its workflow (print mode only).
- `--include-hook-events` — Include all hook lifecycle events in the output stream. Requires `--output-format stream-json`.
- `--include-partial-messages` — Include partial streaming events in output. Requires `--print` and `--output-format stream-json`.
- `--replay-user-messages` — Re-emit user messages from stdin back on stdout for acknowledgment. Requires `--input-format stream-json` and `--output-format stream-json`.
- `--prompt-suggestions` — Emit a `prompt_suggestion` message after each turn with a predicted next prompt. Requires `--print`, `--output-format stream-json`, and `--verbose`.
- `--max-budget-usd` — Maximum dollar amount to spend on API calls before stopping (print mode only).
- `--max-turns` — Limit the number of agentic turns (print mode only). Exits with an error when the limit is reached; no limit by default.
- `--init` — Run Setup hooks with the `init` matcher before the session (print mode only).
- `--init-only` — Run Setup and `SessionStart` hooks, then exit without starting a conversation.
- `--maintenance` — Run Setup hooks with the `maintenance` matcher before the session (print mode only).

## Surface and integration flags

These connect a session to an editor, browser, worktree, or remote surface:

- `--add-dir` — Add additional working directories for Claude to read and edit files. Grants file access; most `.claude/` configuration is not discovered from these directories. To persist, set `permissions.additionalDirectories`.
- `--ide` — Automatically connect to IDE on startup if exactly one valid IDE is available.
- `--chrome` / `--no-chrome` — Enable / disable Chrome browser integration for web automation and testing.
- `--worktree`, `-w` — Start Claude in an isolated git worktree at `<repo>/.claude/worktrees/<name>` (auto-generated name if none given). Pass `#<number>` or a GitHub pull request URL to fetch that PR and branch the worktree from it.
- `--tmux` — Create a tmux session for the worktree. Requires `--worktree`. Uses iTerm2 native panes when available; `--tmux=classic` forces traditional tmux.
- `--remote` — Create a new web session on claude.ai with the provided task description.
- `--remote-control`, `--rc` — Start an interactive session with Remote Control enabled, so it can also be controlled from claude.ai or the Claude app. Optionally pass a session name.
- `--remote-control-session-name-prefix <prefix>` — Prefix for auto-generated Remote Control session names. Defaults to the machine's hostname. `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` has the same effect.
- `--teleport` — Resume a web session in your local terminal.
- `--teammate-mode` — Set how agent team teammates display: `auto` (default), `in-process`, or `tmux`. Overrides the `teammateMode` setting.
- `--agent` — Specify an agent for the current session (overrides the `agent` setting).
- `--agents` — Define custom subagents dynamically via JSON, using the same field names as subagent frontmatter plus a `prompt` field for the agent's instructions.
- `--bg` — Start the session as a background agent and return immediately. Prints the session ID and management commands. Combine with `--exec` to run a shell command as a background job, or `--agent` to run a specific subagent.
- `--exec` — Run a shell command as a PTY-backed background job instead of starting a Claude session. Use with `--bg`.

## Context, debug, and safe-mode flags

- `--exclude-dynamic-system-prompt-sections` — Move per-machine sections (working directory, environment info, memory paths, git-repo flag) from the system prompt into the first user message. Improves prompt-cache reuse across users and machines running the same task. Only applies with the default system prompt; ignored when `--system-prompt`/`--system-prompt-file` is set. Use with `-p` for scripted, multi-user workloads.
- `--bare` — Minimal mode: skip auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md so scripted calls start faster. Claude has access to Bash, file read, and file edit tools. Sets `CLAUDE_CODE_SIMPLE`.
- `--safe-mode` (v2.1.169+) — Start with all customizations disabled to troubleshoot a broken configuration: CLAUDE.md, skills, plugins, hooks, MCP servers, custom commands and agents, output styles, workflows, custom themes/keybindings, status line and file-suggestion commands, LSP servers, and auto-memory do not load. Authentication, model selection, built-in tools, and permissions work normally, which differs from `--bare`. Managed-settings policy still applies. Sets `CLAUDE_CODE_SAFE_MODE`.
- `--settings` — Path to a settings JSON file or inline JSON string. Values set here override the same keys in your `settings.json` for this session; omitted keys keep their file values.
- `--setting-sources` — Comma-separated list of setting sources to load (`user`, `project`, `local`).
- `--betas` — Beta headers to include in API requests (API key users only).
- `--debug` — Enable debug mode with optional category filtering (for example, `"api,hooks"` or `"!statsig,!file"`).
- `--debug-file <path>` — Write debug logs to a specific file path. Implicitly enables debug mode. Takes precedence over `CLAUDE_CODE_DEBUG_LOGS_DIR`.
- `--verbose` — Enable verbose logging; shows full turn-by-turn output. Overrides the `viewMode` setting.
- `--version`, `-v` — Output the version number.

> Note on a removed flag: `--enable-auto-mode` was removed in v2.1.111. Auto mode is now in the `Shift+Tab` cycle by default; use `--permission-mode auto` to start in it.

The full per-flag table (with version annotations and examples) lives in the [CLI reference source page](https://code.claude.com/docs/en/cli-reference); the companion `cc_cli_commands` note documents the `claude` subcommand catalog, and `cc_cli_system_prompt_flags` covers the four system-prompt flags excluded here.

**Source**: https://code.claude.com/docs/en/cli-reference
**Last Updated**: 2026-06-13
**Status**: Active
