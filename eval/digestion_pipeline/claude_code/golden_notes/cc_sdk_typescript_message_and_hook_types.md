---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - typescript
keywords:
  - sdkmessage discriminated union
  - message types catalog
  - hook types
  - hookevent hookcallback
  - streaming event messages
  - task progress message
  - compact boundary message
  - permission denied message
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: model
source_url: https://code.claude.com/docs/en/agent-sdk/typescript
access_control_group: ["general"]
---

# SDK TypeScript — Message and Hook Types

## Overview

The TypeScript Agent SDK streams its work as a sequence of typed **message** objects and fires user code on typed **hook** events. This note is a navigable catalog of those two type families: the `SDKMessage` discriminated union (the values `query()` yields, which a consumer pattern-matches on by `type`/`subtype`), the streaming/event message variants that carry lifecycle and progress signals, and the hook types (`HookEvent`, `HookCallback`, `HookCallbackMatcher`, `HookInput`/`BaseHookInput`, `HookJSONOutput`) that define the callback contract.

Because the source page is a large reference (176 code fences), this note gives a one-line gloss per type plus the key shape, and points back to the live `source_url` for the exhaustive per-type field tables. The **hooks concept** (how to write and wire hooks) and the **permission concept** live in their own docs — see the [Hooks guide](https://code.claude.com/docs/en/agent-sdk/hooks); this note documents only the TypeScript type shapes.

## Message Types — the `SDKMessage` union

`SDKMessage` is the discriminated union of every message the query yields. A consumer narrows on the `type` field (and, for `"system"` messages, the `subtype`). The full union:

```typescript
type SDKMessage =
  | SDKAssistantMessage
  | SDKUserMessage
  | SDKUserMessageReplay
  | SDKResultMessage
  | SDKSystemMessage
  | SDKPartialAssistantMessage
  | SDKCompactBoundaryMessage
  | SDKStatusMessage
  | SDKLocalCommandOutputMessage
  | SDKHookStartedMessage
  | SDKHookProgressMessage
  | SDKHookResponseMessage
  | SDKPluginInstallMessage
  | SDKToolProgressMessage
  | SDKAuthStatusMessage
  | SDKTaskNotificationMessage
  | SDKTaskStartedMessage
  | SDKTaskProgressMessage
  | SDKTaskUpdatedMessage
  | SDKSessionStateChangedMessage
  | SDKCommandsChangedMessage
  | SDKNotificationMessage
  | SDKFilesPersistedEvent
  | SDKToolUseSummaryMessage
  | SDKMemoryRecallMessage
  | SDKRateLimitEvent
  | SDKElicitationCompleteMessage
  | SDKPermissionDeniedMessage
  | SDKPromptSuggestionMessage
  | SDKAPIRetryMessage
  | SDKMirrorErrorMessage;
```

### Core conversation variants

| Type | `type` / `subtype` | What it carries |
| :--- | :--- | :--- |
| `SDKAssistantMessage` | `"assistant"` | A `BetaMessage` from the Anthropic SDK (`content`, `model`, `stop_reason`, `usage`); optional `error` (`SDKAssistantMessageError`, e.g. `'rate_limit'`, `'overloaded'`, `'model_not_found'`). |
| `SDKUserMessage` | `"user"` | A `MessageParam`; set `shouldQuery: false` to append context without triggering an assistant turn; `origin` records provenance. |
| `SDKUserMessageReplay` | `"user"` | Replayed user message with required `uuid` and `isReplay: true`. |
| `SDKResultMessage` | `"result"` (`subtype` `"success"` or an `error_*`) | Final result: `duration_ms`, `num_turns`, `total_cost_usd`, `usage`, `modelUsage`, `permission_denials`, `structured_output?`, `terminal_reason?`. Success arm adds `result`, `ttft_ms`, `ttft_stream_ms`. |
| `SDKSystemMessage` | `"system"` / `"init"` | Session init snapshot: `tools`, `mcp_servers`, `model`, `permissionMode`, `slash_commands`, `skills`, `plugins`. |
| `SDKPartialAssistantMessage` | `"stream_event"` | A `BetaRawMessageStreamEvent` (only when `includePartialMessages` is true). |
| `SDKCompactBoundaryMessage` | `"system"` / `"compact_boundary"` | Marks an auto/manual context-compaction boundary; `compact_metadata` has `trigger` and `pre_tokens`. |
| `SDKPluginInstallMessage` | `"system"` / `"plugin_install"` | Marketplace plugin install progress (`status`: `started`/`installed`/`failed`/`completed`). |
| `SDKPermissionDeniedMessage` | `"system"` / `"permission_denied"` | A tool call auto-denied without an interactive prompt; `tool_name`, `tool_use_id`, `decision_reason_type`/`decision_reason`. |

Two helper shapes accompany these: `SDKPermissionDenial` (`tool_name`/`tool_use_id`/`tool_input`, used inside `permission_denials`), and `SDKMessageOrigin` — the provenance tag on a user message, forwarded onto the matching result: `{ kind: "human" }`, `"channel"`, `"peer"`, `"task-notification"`, `"coordinator"`, or `"auto-continuation"`. Check `origin` to tell a reply to your prompt from a synthetic background-task follow-up.

### Streaming / event message variants ("Other Types")

These `"system"`- and event-typed variants are progress and lifecycle signals the host reacts to:

| Type | `subtype` / `type` | Signal |
| :--- | :--- | :--- |
| `SDKStatusMessage` | `"status"` | Transient status, e.g. `status: "compacting"`. |
| `SDKTaskNotificationMessage` | `"task_notification"` | A background task `completed`/`failed`/`stopped`; `output_file`, `summary`, optional `usage`. |
| `SDKTaskStartedMessage` | `"task_started"` | Background task begins; `task_type` is `"local_bash"`, `"local_agent"`, or `"remote_agent"`. |
| `SDKTaskProgressMessage` | `"task_progress"` | Periodic subagent/task progress; `usage`, `last_tool_name`, `summary?` (when `agentProgressSummaries` on). |
| `SDKTaskUpdatedMessage` | `"task_updated"` | Task state change; merge `patch` (`status`, `end_time`, `error`, …) by `task_id`. |
| `SDKToolProgressMessage` | `type: "tool_progress"` | Periodic in-flight tool progress; `elapsed_time_seconds`. |
| `SDKToolUseSummaryMessage` | `type: "tool_use_summary"` | A summary spanning `preceding_tool_use_ids`. |
| `SDKHookStartedMessage` / `SDKHookProgressMessage` / `SDKHookResponseMessage` | `"hook_started"`/`"hook_progress"`/`"hook_response"` | Hook lifecycle (emitted when `includeHookEvents` is set): `hook_id`/`hook_name`/`hook_event`, plus `stdout`/`stderr`/`output`, and `outcome` + `exit_code?` on response. |
| `SDKAuthStatusMessage` | `type: "auth_status"` | Authentication-flow progress (`isAuthenticating`, `output`). |
| `SDKFilesPersistedEvent` | `"files_persisted"` | File checkpoints written to disk (`files`, `failed`). |
| `SDKRateLimitEvent` | `type: "rate_limit_event"` | Rate-limit signal; `rate_limit_info.status` is `allowed`/`allowed_warning`/`rejected`. |
| `SDKLocalCommandOutputMessage` | `"local_command_output"` | Output of a local slash command (e.g. `/usage`). |
| `SDKCommandsChangedMessage` | `"commands_changed"` | Full updated command list mid-session (replace your cache; `supportedCommands()` only returns the init snapshot). |
| `SDKPromptSuggestionMessage` | `type: "prompt_suggestion"` | Predicted next user prompt (when `promptSuggestions` on). |

`AbortError` is a custom `Error` subclass thrown for abort operations. The remaining union members (`SDKSessionStateChangedMessage`, `SDKNotificationMessage`, `SDKMemoryRecallMessage`, `SDKElicitationCompleteMessage`, `SDKAPIRetryMessage`, `SDKMirrorErrorMessage`) are additional event types — see `source_url` for their full field tables.

## Hook Types

The SDK fires user-supplied callbacks on lifecycle events. For the conceptual guide (patterns, examples), see the [Hooks guide](https://code.claude.com/docs/en/agent-sdk/hooks); the type contract is:

- **`HookEvent`** — the event-name union the `hooks` option keys on: `"PreToolUse"`, `"PostToolUse"`, `"PostToolUseFailure"`, `"PostToolBatch"`, `"Notification"`, `"UserPromptSubmit"`, `"SessionStart"`, `"SessionEnd"`, `"Stop"`, `"SubagentStart"`, `"SubagentStop"`, `"PreCompact"`, `"PermissionRequest"`, `"Setup"`, `"TeammateIdle"`, `"TaskCompleted"`, `"ConfigChange"`, `"WorktreeCreate"`, `"WorktreeRemove"`, `"MessageDisplay"`.
- **`HookCallback`** — `(input: HookInput, toolUseID: string | undefined, options: { signal: AbortSignal }) => Promise<HookJSONOutput>`.
- **`HookCallbackMatcher`** — config object: optional `matcher?: string`, `hooks: HookCallback[]`, `timeout?` (seconds for all hooks in the matcher).
- **`HookInput`** — the union of all per-event input types (one variant per `HookEvent`, e.g. `PreToolUseHookInput`, `PostToolUseHookInput`, `SessionStartHookInput`, `PreCompactHookInput`, …).
- **`BaseHookInput`** — the base every input extends: `session_id`, `transcript_path`, `cwd`, optional `permission_mode`, `effort`, `agent_id`, `agent_type`.

Each input variant intersects `BaseHookInput` with a `hook_event_name` discriminator plus event-specific fields, for example:

```typescript
type PreToolUseHookInput = BaseHookInput & {
  hook_event_name: "PreToolUse";
  tool_name: string;
  tool_input: unknown;
  tool_use_id: string;
};
```

`PostToolUseHookInput` adds `tool_response`/`duration_ms?`; `PostToolBatchHookInput` carries `tool_calls: PostToolBatchToolCall[]`; `SessionStartHookInput` has `source` (`"startup"`/`"resume"`/`"clear"`/`"compact"`); `PreCompactHookInput` has `trigger` + `custom_instructions`; `StopHookInput`/`SubagentStopHookInput` add `background_tasks`/`session_crons` summaries. See `source_url` for every variant's fields.

### `HookJSONOutput`

A hook returns `AsyncHookJSONOutput | SyncHookJSONOutput`. `AsyncHookJSONOutput` is `{ async: true; asyncTimeout? }`. `SyncHookJSONOutput` carries control fields (`continue?`, `suppressOutput?`, `stopReason?`, `decision?: "approve" | "block"`, `systemMessage?`, `reason?`) plus a discriminated `hookSpecificOutput` keyed by `hookEventName` — e.g. a `"PreToolUse"` entry can set `permissionDecision?: "allow" | "deny" | "ask" | "defer"`, `updatedInput?`, and `additionalContext?`; a `"PermissionRequest"` entry returns an allow/deny `decision`. (A `PreToolUse` `"defer"` surfaces as `terminal_reason: "tool_deferred"` + `deferred_tool_use` on the result.)

**Source**: https://code.claude.com/docs/en/agent-sdk/typescript
**Last Updated**: 2026-06-13
**Status**: Active
