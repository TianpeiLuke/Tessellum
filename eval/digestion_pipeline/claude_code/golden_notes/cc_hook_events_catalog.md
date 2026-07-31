---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - lifecycle
keywords:
  - hook events
  - event catalog
  - hook lifecycle
  - hook cadence
  - matcher field per event
  - handler type support
  - pretooluse posttooluse
  - sessionstart sessionend
topics:
  - Claude Code
  - Hooks
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/hooks
access_control_group: ["general"]
---

# Claude Code — Hook Events Catalog

## Overview

Claude Code's hook system fires at named **events** — points in a session's lifecycle where a matching hook handler can run. The source lifecycle table lists 30 such events. This note is the navigational index to all 30: when each one fires, its cadence (per-session / per-turn / per-tool-call), which input field its `matcher` filters on, and which of the five handler types (`command`, `http`, `mcp_tool`, `prompt`, `agent`) the event supports. Per-event input schemas and decision control are documented in the tool-loop and session-lifecycle notes; this catalog is the map that routes you to them.

When an event fires and a matcher matches, Claude Code passes JSON about the event to the handler (on stdin for command hooks, as the POST body for HTTP hooks) and the handler can inspect it, act, and optionally return a decision.

## The three cadences

Events fall into three cadences:

- **Once per session** — `SessionStart`, `SessionEnd`.
- **Once per turn** — `UserPromptSubmit`, `Stop`, `StopFailure`.
- **On every tool call inside the agentic loop** — `PreToolUse`, `PostToolUse` (and the rest of the tool-loop family).

Other events (such as `ConfigChange`, `CwdChanged`, `FileChanged`, `InstructionsLoaded`) fire as standalone async events when the underlying condition occurs.

## When each event fires

The full event set and trigger conditions (verbatim from the source lifecycle table):

| Event | When it fires |
| :-- | :-- |
| `SessionStart` | When a session begins or resumes |
| `Setup` | With `--init-only`, or with `--init`/`--maintenance` in `-p` mode. For one-time prep in CI or scripts |
| `UserPromptSubmit` | When you submit a prompt, before Claude processes it |
| `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion |
| `PreToolUse` | Before a tool call executes. Can block it |
| `PermissionRequest` | When a permission dialog appears |
| `PermissionDenied` | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to allow a retry |
| `PostToolUse` | After a tool call succeeds |
| `PostToolUseFailure` | After a tool call fails |
| `PostToolBatch` | After a full batch of parallel tool calls resolves, before the next model call |
| `Notification` | When Claude Code sends a notification |
| `MessageDisplay` | While assistant message text is displayed |
| `SubagentStart` | When a subagent is spawned |
| `SubagentStop` | When a subagent finishes |
| `TaskCreated` | When a task is being created via `TaskCreate` |
| `TaskCompleted` | When a task is being marked as completed |
| `Stop` | When Claude finishes responding |
| `StopFailure` | When the turn ends due to an API error. Output and exit code are ignored |
| `TeammateIdle` | When an agent team teammate is about to go idle |
| `InstructionsLoaded` | When a `CLAUDE.md` or `.claude/rules/*.md` file is loaded into context |
| `ConfigChange` | When a configuration file changes during a session |
| `CwdChanged` | When the working directory changes (e.g. a `cd` command) |
| `FileChanged` | When a watched file changes on disk. The `matcher` field specifies which filenames to watch |
| `WorktreeCreate` | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior |
| `WorktreeRemove` | When a worktree is being removed, at session exit or when a subagent finishes |
| `PreCompact` | Before context compaction |
| `PostCompact` | After context compaction completes |
| `Elicitation` | When an MCP server requests user input during a tool call |
| `ElicitationResult` | After a user responds to an MCP elicitation, before the response is sent back to the server |
| `SessionEnd` | When a session terminates |

## What each event's matcher filters

The `matcher` field narrows when a hook group fires, but the field it matches against differs by event:

- **Tool name** — `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` (e.g. `Bash`, `Edit|Write`, `mcp__.*`).
- **How the session started** — `SessionStart` (`startup`, `resume`, `clear`, `compact`).
- **Which CLI flag triggered setup** — `Setup` (`init`, `maintenance`).
- **Why the session ended** — `SessionEnd` (`clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`).
- **Notification type** — `Notification` (`permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response`).
- **Agent type** — `SubagentStart` and `SubagentStop` (`general-purpose`, `Explore`, `Plan`, or custom agent names).
- **What triggered compaction** — `PreCompact`, `PostCompact` (`manual`, `auto`).
- **Configuration source** — `ConfigChange` (`user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`).
- **Error type** — `StopFailure` (`rate_limit`, `overloaded`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, `unknown`).
- **Load reason** — `InstructionsLoaded` (`session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`).
- **Command name** — `UserPromptExpansion` (your skill or command names).
- **MCP server name** — `Elicitation`, `ElicitationResult` (your configured MCP server names).
- **Literal filenames to watch** — `FileChanged` (e.g. `.envrc|.env`; this event does not follow the normal matcher evaluation rules).
- **No matcher support (always fires)** — `CwdChanged`, plus `UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `MessageDisplay`. A `matcher` added to these is silently ignored.

The matcher runs against a field from the JSON input Claude Code sends on stdin; for tool events that field is `tool_name`. For tool events, you can filter more narrowly with the per-handler `if` field. See the [Matcher patterns](https://code.claude.com/docs/en/hooks) section of the hooks reference for matcher evaluation rules (exact / `|`-list / regex / match-all) and the `if` syntax.

## Which handler types each event supports

Not all events support every one of the five handler types:

- **All five types** (`command`, `http`, `mcp_tool`, `prompt`, `agent`): `PermissionDenied`, `PermissionRequest`, `PostToolBatch`, `PostToolUse`, `PostToolUseFailure`, `PreToolUse`, `Stop`, `SubagentStop`, `TaskCompleted`, `TaskCreated`, `TeammateIdle`, `UserPromptExpansion`, `UserPromptSubmit`.
- **`command`, `http`, `mcp_tool` only** (no `prompt`/`agent`): `ConfigChange`, `CwdChanged`, `Elicitation`, `ElicitationResult`, `FileChanged`, `InstructionsLoaded`, `Notification`, `PostCompact`, `PreCompact`, `SessionEnd`, `StopFailure`, `SubagentStart`, `WorktreeCreate`, `WorktreeRemove`.
- **`command` and `mcp_tool` only**: `SessionStart`, `Setup` (no `http`, `prompt`, or `agent`).

`MessageDisplay` runs while assistant text streams and is display-only. The five types themselves are documented in [Hook Handler Types](cc_hook_handler_types.md); the LLM-judge `prompt`/`agent` types in [Prompt and Agent Hooks](cc_prompt_and_agent_hooks.md).

## Where the per-event detail lives

This catalog indexes two detail notes:

- The six per-tool-call events (`PreToolUse`, `PermissionRequest`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `PermissionDenied`) — their input schemas and decision control are in [Hook Tool-Loop Events](cc_hook_tool_loop_events.md).
- The session-, turn-, and non-tool lifecycle events (everything else) — in the [Hook events](https://code.claude.com/docs/en/hooks) section of the hooks reference.

For the complete per-event input schema and decision-control fields, see the source page.

**Source**: https://code.claude.com/docs/en/hooks
**Last Updated**: 2026-06-13
**Status**: Active
