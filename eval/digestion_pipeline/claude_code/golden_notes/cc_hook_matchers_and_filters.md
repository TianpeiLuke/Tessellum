---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - matchers
keywords:
  - hook matcher patterns
  - matcher evaluation
  - per-event matcher field
  - match mcp tools
  - if field permission rule
  - bash subcommand matching
  - common hook handler fields
  - timeout statusmessage once
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

# Claude Code — Hook Matchers and Filters

## Overview

A Claude Code hook fires on **every** occurrence of its event unless you narrow it. Two filtering layers do that narrowing: the group-level **`matcher`** (which event-specific field, such as a tool name, the hook group reacts to) and the handler-level **`if`** field (which inspects tool name *and* arguments together using permission-rule syntax so the hook process only spawns when the call actually matches). This note is the reference procedure for both: how a matcher value is evaluated (match-all / exact / `|`-list / regex), which field each event matches against, how to match MCP server tools, the `if` filter and its Bash-subcommand matching behavior, and the common handler fields (`if`, `timeout`, `statusMessage`, `once`) shared by all five handler types.

The matcher runs against a field from the [JSON input](https://code.claude.com/docs/en/hooks) Claude Code sends to your hook (on stdin for command hooks, the POST body for HTTP hooks); for tool events that field is `tool_name`. The five handler types themselves are documented in [Hook Handler Types](cc_hook_handler_types.md), and the event catalog that lists every matcher field is in [Hook Events Catalog](cc_hook_events_catalog.md).

## Matcher patterns

The `matcher` field filters when hooks fire. How a matcher is evaluated depends on the characters it contains:

| Matcher value | Evaluated as | Example |
| :-- | :-- | :-- |
| `"*"`, `""`, or omitted | Match all | fires on every occurrence of the event |
| Only letters, digits, `_`, and `\|` | Exact string, or `\|`-separated list of exact strings | `Bash` matches only the Bash tool; `Edit\|Write` matches either tool exactly |
| Contains any other character | JavaScript regular expression | `^Notebook` matches any tool starting with Notebook; `mcp__memory__.*` matches every tool from the `memory` server |

The `FileChanged` event does not follow these rules when building its watch list; see the [FileChanged](https://code.claude.com/docs/en/hooks) section of the reference.

### What each event's matcher filters

Each event type matches on a different field. The full mapping (verbatim from the source per-event matcher table):

| Event | What the matcher filters | Example matcher values |
| :-- | :-- | :-- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` | tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| `SessionStart` | how the session started | `startup`, `resume`, `clear`, `compact` |
| `Setup` | which CLI flag triggered setup | `init`, `maintenance` |
| `SessionEnd` | why the session ended | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` |
| `Notification` | notification type | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response` |
| `SubagentStart` | agent type | `general-purpose`, `Explore`, `Plan`, or custom agent names |
| `PreCompact`, `PostCompact` | what triggered compaction | `manual`, `auto` |
| `SubagentStop` | agent type | same values as `SubagentStart` |
| `ConfigChange` | configuration source | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `CwdChanged` | no matcher support | always fires on every directory change |
| `FileChanged` | literal filenames to watch | `.envrc\|.env` |
| `StopFailure` | error type | `rate_limit`, `overloaded`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded` | load reason | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact` |
| `UserPromptExpansion` | command name | your skill or command names |
| `Elicitation`, `ElicitationResult` | MCP server name | your configured MCP server names |
| `UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `MessageDisplay` | no matcher support | always fires on every occurrence |

`UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, and `CwdChanged` don't support matchers and always fire on every occurrence. If you add a `matcher` field to these events, it is silently ignored.

This example runs a linting script only when Claude writes or edits a file, using the `|`-list matcher:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

### Match MCP tools

[MCP](https://code.claude.com/docs/en/mcp) server tools appear as regular tools in tool events (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`), so you can match them the same way you match any other tool name. MCP tools follow the naming pattern `mcp__<server>__<tool>`, for example:

- `mcp__memory__create_entities`: Memory server's create entities tool
- `mcp__filesystem__read_file`: Filesystem server's read file tool
- `mcp__github__search_repositories`: GitHub server's search tool

To match every tool from a server, append `.*` to the server prefix. The `.*` is **required**: a matcher like `mcp__memory` contains only letters and underscores, so it is compared as an exact string and matches no tool.

- `mcp__memory__.*` matches all tools from the `memory` server.
- `mcp__.*__write.*` matches any tool whose name starts with `write` from any server.

This example logs all memory server operations and validates write operations from any MCP server:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

## Common hook handler fields

Each object in the inner `hooks` array is a hook handler. These fields apply to **all** five handler types (command / HTTP / MCP-tool / prompt / agent); type-specific fields are documented in [Hook Handler Types](cc_hook_handler_types.md):

| Field | Required | Description |
| :-- | :-- | :-- |
| `type` | yes | `"command"`, `"http"`, `"mcp_tool"`, `"prompt"`, or `"agent"` |
| `if` | no | Permission rule syntax to filter when this hook runs, such as `"Bash(git *)"` or `"Edit(*.ts)"`. The hook command only runs if the tool call matches the pattern. Only evaluated on tool events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, and `PermissionDenied`. On other events, a hook with `if` set never runs. Uses the same syntax as [permission rules](https://code.claude.com/docs/en/permissions) |
| `timeout` | no | Seconds before canceling. Defaults: 600 for `command`, `http`, and `mcp_tool`; 30 for `prompt`; 60 for `agent`. `UserPromptSubmit` lowers the `command`/`http`/`mcp_tool` default to 30, and `MessageDisplay` lowers it to 10 |
| `statusMessage` | no | Custom spinner message displayed while the hook runs |
| `once` | no | If `true`, runs once per session then is removed. Only honored for hooks declared in [skill frontmatter](cc_hook_handler_types.md); ignored in settings files and agent frontmatter |

### The `if` field

For tool events, you can filter more narrowly than the matcher by setting the `if` field on individual hook handlers. `if` uses [permission rule syntax](https://code.claude.com/docs/en/permissions) to match against the tool name and arguments together, so `"Bash(git *)"` runs when any subcommand of the Bash input matches `git *` and `"Edit(*.ts)"` runs only for TypeScript files.

The `if` field holds exactly **one** permission rule. There is no `&&`, `||`, or list syntax for combining rules; to apply multiple conditions, define a separate hook handler for each.

#### Bash `if` matching

For Bash patterns, whether your hook command runs depends on the shape of the pattern and the Bash command Claude is invoking. Leading `VAR=value` assignments are stripped before matching:

| `if` pattern | Bash command | Hook runs? | Why |
| :-- | :-- | :-- | :-- |
| `Bash(git *)` | `FOO=bar git push` | yes | leading assignments are stripped; `git push` matches |
| `Bash(git *)` | `npm test && git push` | yes | each subcommand is checked; `git push` matches |
| `Bash(rm *)` | `echo $(rm -rf /)` | yes | commands inside `$()` and backticks are checked; `rm -rf /` matches |
| `Bash(rm *)` | `echo $(date)` | no | no subcommand matches `rm *` |
| `Bash(git push *)` | `echo $(date)` | yes | patterns that specify more than the command name run the hook anyway on `$()`, backticks, or `$VAR` |

The filter also **fails open**, running your hook regardless of pattern, when the Bash command cannot be parsed. Because the `if` filter is best-effort, use the [permission system](https://code.claude.com/docs/en/permissions) rather than a hook to enforce a hard allow or deny.

**Source**: https://code.claude.com/docs/en/hooks
**Last Updated**: 2026-06-13
**Status**: Active
