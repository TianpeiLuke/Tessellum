---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - hooks
keywords:
  - configure hooks
  - options.hooks
  - hookmatcher
  - matcher pattern
  - callback functions
  - hookspecificoutput
  - permissiondecision
  - updatedinput
  - asynchronous output
  - mcp tool naming
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/hooks
access_control_group: ["general"]
---

# Claude Code Agent SDK — Configuring Hooks

## Overview

This note covers how to register hooks in the Claude Code Agent SDK and what each callback receives and returns. A hook is wired in through the `hooks` field of your agent options, keyed by event name, with each value being an array of **matchers** that pair an optional filter pattern with one or more callback functions. When the event fires, each callback gets a typed input object, runs whatever logic you need, and returns an output object that decides the operation's fate. This is the registration-and-contract layer of SDK hooks; the event model and the full event table are covered in [SDK Hooks Overview](cc_sdk_hooks_overview.md), and concrete recipes in [SDK Hooks Examples](cc_sdk_hooks_examples.md).

## Configure hooks

To configure a hook, pass it in the `hooks` field of your agent options (`ClaudeAgentOptions` in Python, the `options` object in TypeScript):

```python Python
options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="Bash", hooks=[my_callback])]}
)

async with ClaudeSDKClient(options=options) as client:
    await client.query("Your prompt")
    async for message in client.receive_response():
        print(message)
```

The `hooks` option is a dictionary (Python) or object (TypeScript) where:

- **Keys** are hook event names (e.g., `'PreToolUse'`, `'PostToolUse'`, `'Stop'`).
- **Values** are arrays of matchers, each containing an optional filter pattern and your callback functions.

The TypeScript equivalent uses the same shape passed to `query({ ..., options: { hooks: {...} } })` (see the TypeScript SDK reference).

## Matchers

Matchers filter when your callbacks fire. The `matcher` field matches against a different value depending on the hook event type — tool-based hooks match against the **tool name**, while `Notification` hooks match against the notification type. Matchers follow the same rules as matchers in settings files:

- A matcher containing only letters, digits, `_`, and `|` is compared as an **exact string**, with `|` separating alternatives, so `Write|Edit` matches exactly those two tools.
- A matcher of `*`, an empty string, or omitting the matcher entirely matches **every occurrence** of the event.
- A matcher containing any other character is evaluated as a **regular expression**, so `^mcp__` matches every MCP tool.
- A matcher like `mcp__memory` contains only letters and underscores, so it is compared as an exact string and matches no tool; use `mcp__memory__.*` to match every tool from that server.

The matcher object accepts three options:

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `matcher` | `string` | `undefined` | Pattern matched against the event's filter field. For tool hooks, this is the tool name. Built-in tools include `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebFetch`, `Agent`, and others. MCP tools use the pattern `mcp__<server>__<action>`. |
| `hooks` | `HookCallback[]` | — | Required. Array of callback functions to execute when the pattern matches. |
| `timeout` | `number` | `60` | Timeout in seconds. |

Target specific tools whenever possible — a matcher with `'Bash'` only runs for Bash commands, while omitting the pattern runs your callbacks for every occurrence of the event. For tool-based hooks, matchers only filter by **tool name**, not by file paths or other arguments; to filter by file path, check `tool_input.file_path` inside your callback. MCP tools always start with `mcp__` followed by the server name and action (`mcp__<server>__<action>`), where the server name comes from the key used in the `mcpServers` configuration.

## Callback functions

### Inputs

Every hook callback receives three arguments:

- **Input data** — a typed object containing event details. Each hook type has its own input shape (for example, `PreToolUseHookInput` includes `tool_name` and `tool_input`, while `NotificationHookInput` includes `message`). All hook inputs share `session_id`, `cwd`, and `hook_event_name`. `agent_id` and `agent_type` are populated when the hook fires inside a subagent (in TypeScript on the base input for all hook types; in Python only on `PreToolUse`, `PostToolUse`, and `PostToolUseFailure`).
- **Tool use ID** (`str | None` / `string | undefined`) — correlates `PreToolUse` and `PostToolUse` events for the same tool call.
- **Context** — in TypeScript, contains a `signal` property (`AbortSignal`) for cancellation; in Python this argument is reserved for future use.

### Outputs

The callback returns an object with two categories of fields:

- **Top-level fields** work the same on every event: `systemMessage` shows a message to the user, and `continue` (`continue_` in Python) determines whether the agent keeps running after this hook.
- **`hookSpecificOutput`** controls the current operation; the fields inside depend on the hook event type. For `PreToolUse` hooks, this is where you set `permissionDecision` (`"allow"`, `"deny"`, `"ask"`, or `"defer"`), `permissionDecisionReason`, and `updatedInput`. Returning `"defer"` ends the query so you can resume it later. For `PostToolUse` hooks, set `additionalContext` to append information to the tool result; to replace the tool's output before Claude sees it, set `updatedToolOutput` (works for any tool in both SDKs). The older `updatedMCPToolOutput` field replaces MCP tool output only and is deprecated.

Return `{}` to allow the operation without changes. When multiple hooks or permission rules apply, **deny** takes priority over **defer**, which takes priority over **ask**, which takes priority over **allow** — if any hook returns `deny`, the operation is blocked regardless of other hooks.

### Asynchronous output

By default the agent waits for your hook to return before proceeding. If your hook performs a side effect (logging, sending a webhook) and doesn't need to influence the agent's behavior, return an async output to tell the agent to continue immediately:

```python Python
async def async_hook(input_data, tool_use_id, context):
    # Start a background task, then return immediately
    asyncio.create_task(send_to_logging_service(input_data))
    return {"async_": True, "asyncTimeout": 30000}
```

| Field | Type | Description |
| --- | --- | --- |
| `async` | `true` | Signals async mode. The agent proceeds without waiting. In Python, use `async_` to avoid the reserved keyword. |
| `asyncTimeout` | `number` | Optional timeout in milliseconds for the background operation. |

Async outputs cannot block, modify, or inject context into the operation since the agent has already moved on — use them only for side effects like logging, metrics, or notifications.

**Source**: https://code.claude.com/docs/en/agent-sdk/hooks
**Last Updated**: 2026-06-13
**Status**: Active
