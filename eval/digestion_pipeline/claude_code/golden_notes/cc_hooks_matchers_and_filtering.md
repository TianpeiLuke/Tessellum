---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - matchers
keywords:
  - hook matcher
  - filter hooks by tool name
  - if field
  - permission rule syntax
  - mcp tool matcher
  - edit write matcher
  - per-event matcher field
  - matcher fails open
topics:
  - Claude Code
  - Hooks
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/hooks-guide
access_control_group: ["general"]
---

# Claude Code Hooks — Matchers and Filtering

## Overview

A Claude Code hook fires on **every** occurrence of its event unless you narrow it down. Two settings-file constructs do that narrowing: the **`matcher`** (group-level, by tool name or other event-specific field) and the **`if`** field (handler-level, by tool name *and* arguments using permission-rule syntax). The matcher filters at the hook-group level and supports plain names plus pipe alternation and regex; the `if` field goes further by inspecting tool arguments and subcommands so the hook process only spawns when the call actually matches.

This note covers matcher semantics, which field each event matches on, worked matcher examples (Bash logging, MCP tools, `SessionEnd` cleanup), and the `if` field's permission-rule syntax, subcommand/`$()` checking, and fail-open behavior. Full matcher-pattern and configuration schema details live in the [Hooks reference](https://code.claude.com/docs/en/hooks) (B07A), which this guide links out to rather than duplicates.

## Filter hooks with matchers

Without a matcher, a hook fires on every occurrence of its event. Matchers let you narrow that down. For example, to run a formatter only after file edits (not after every tool call), add a matcher to your `PostToolUse` hook:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write ..." }
        ]
      }
    ]
  }
}
```

The `"Edit|Write"` matcher fires only when Claude uses the `Edit` or `Write` tool, not when it uses `Bash`, `Read`, or any other tool. See [Matcher patterns](https://code.claude.com/docs/en/hooks) in the reference for how plain names and regular expressions are evaluated.

Claude can also create or modify files by running shell commands through the `Bash` tool. If your hook must see every file change (for example, for compliance scanning or audit logging), add a `Stop` hook that scans the working tree once per turn. For per-call coverage instead, also match `Bash` and have your script list modified and untracked files with `git status --porcelain`.

### Per-event matcher field

Each event type matches on a specific field. An empty matcher (or no matcher at all) fires on all occurrences; matchers are case-sensitive.

| Event | What the matcher filters | Example matcher values |
| :--- | :--- | :--- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` | tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| `SessionStart` | how the session started | `startup`, `resume`, `clear`, `compact` |
| `Setup` | which CLI flag triggered setup | `init`, `maintenance` |
| `SessionEnd` | why the session ended | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` |
| `Notification` | notification type | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response` |
| `SubagentStart` | agent type | `general-purpose`, `Explore`, `Plan`, or custom agent names |
| `PreCompact`, `PostCompact` | what triggered compaction | `manual`, `auto` |
| `SubagentStop` | agent type | same values as `SubagentStart` |
| `ConfigChange` | configuration source | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `StopFailure` | error type | `rate_limit`, `overloaded`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded` | load reason | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact` |
| `Elicitation`, `ElicitationResult` | MCP server name | your configured MCP server names |
| `FileChanged` | literal filenames to watch | `.envrc\|.env` |
| `UserPromptExpansion` | command name | your skill or command names |
| `UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `CwdChanged`, `MessageDisplay` | no matcher support | always fires on every occurrence |

### Matcher examples

A few examples showing matchers on different event types.

**Log every Bash command** — match only `Bash` tool calls and log each command to a file. The `PostToolUse` event fires after the command completes, so `tool_input.command` contains what ran. The hook receives the event data as JSON on stdin, and `jq -r '.tool_input.command'` extracts just the command string, which `>>` appends to the log file:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
          }
        ]
      }
    ]
  }
}
```

**Match MCP tools** — MCP tools use a different naming convention than built-in tools: `mcp__<server>__<tool>`, where `<server>` is the MCP server name and `<tool>` is the tool it provides. For example, `mcp__github__search_repositories` or `mcp__filesystem__read_file`. Use a regex matcher to target all tools from a specific server, or match across servers with a pattern like `mcp__.*__write.*`. The command below extracts the tool name from the hook's JSON input with `jq` and writes it to stderr; writing to stderr keeps stdout clean for JSON output and sends the message to the debug log:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__github__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"GitHub tool called: $(jq -r '.tool_name')\" >&2"
          }
        ]
      }
    ]
  }
}
```

**Clean up on session end** — the `SessionEnd` event supports matchers on the reason the session ended. This hook only fires on `clear` (when you run `/clear`), not on normal exits:

```json theme={null}
{
  "hooks": {
    "SessionEnd": [
      {
        "matcher": "clear",
        "hooks": [
          {
            "type": "command",
            "command": "rm -f /tmp/claude-scratch-*.txt"
          }
        ]
      }
    ]
  }
}
```

For full matcher syntax, see the [Hooks reference](https://code.claude.com/docs/en/hooks).

## Filter by tool name and arguments with the `if` field

The `if` field requires Claude Code v2.1.85 or later. Earlier versions ignore it and run the hook on every matched call.

The `if` field uses [permission rule syntax](https://code.claude.com/docs/en/permissions) to filter hooks by tool name and arguments together, so the hook process only spawns when the tool call matches. This goes beyond `matcher`, which filters at the group level by tool name only.

For example, to run a hook only when Claude uses `git` commands rather than all Bash commands:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(git *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-git-policy.sh"
          }
        ]
      }
    ]
  }
}
```

Whether your hook command runs depends on the shape of your `if` pattern and the Bash command Claude is invoking. Subcommands are checked individually, and commands inside `$()` and backticks are checked too:

| `if` pattern | Bash command | Hook runs? | Why |
| :--- | :--- | :--- | :--- |
| `Bash(git *)` | `git push` | yes | command name matches |
| `Bash(git *)` | `npm test && git push` | yes | each subcommand is checked; `git push` matches |
| `Bash(git *)` | `echo $(git log)` | yes | commands inside `$()` and backticks are checked; `git log` matches |
| `Bash(git *)` | `echo $(date)` | no | no subcommand matches `git *` |
| `Bash(git push *)` | `echo $(date)` | yes | patterns that specify more than the command name run the hook anyway on `$()`, backticks, or `$VAR` |

The filter also **fails open**, running your hook regardless of pattern, when the Bash command cannot be parsed. Because the filter is best-effort, use the [permission system](https://code.claude.com/docs/en/permissions) rather than a hook to enforce a hard allow or deny.

The `if` field accepts the same patterns as permission rules: `"Bash(git *)"`, `"Edit(*.ts)"`, and so on. To match multiple tool names, use separate handlers each with its own `if` value, or match at the `matcher` level where pipe alternation is supported.

`if` only works on tool events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, and `PermissionDenied`. Adding it to any other event prevents the hook from running.

**Source**: https://code.claude.com/docs/en/hooks-guide
**Last Updated**: 2026-06-13
**Status**: Active
