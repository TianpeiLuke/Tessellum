---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - python_sdk
keywords:
  - claude agent sdk hooks
  - hookevent
  - hookcallback
  - hookmatcher
  - hookinput
  - hookjsonoutput
  - pretooluse hook
  - permissionrequest hook
  - hook registration
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/python
access_control_group: ["general"]
---

# Claude Agent SDK (Python) — Hook Types

## Overview

The Python `claude-agent-sdk` lets a host program register **hooks** — callbacks that fire on Claude Code lifecycle events to inspect, block, or augment the agent's behavior. This note documents the Python type contract for that: the `HookEvent` literal of supported event names, the `HookCallback` callable signature, the `HookContext` and `HookMatcher` configuration shapes, the discriminated-union `HookInput` family (one strongly-typed `*HookInput` per event), the `HookJSONOutput` decision/control schema a callback returns, and the registration example. Hooks are wired into a run through the `hooks` field of `ClaudeAgentOptions` (see [`cc_sdk_python_options_and_config_types`](cc_sdk_python_options_and_config_types.md)).

This is a type reference only — for the comprehensive guide on using hooks with examples and common patterns, the source points to the [Hooks guide](https://code.claude.com/docs/en/agent-sdk/hooks).

## `HookEvent`

Supported hook event types — a `Literal` of the ten event names that can trigger a hook:

```python
HookEvent = Literal[
    "PreToolUse",  # Called before tool execution
    "PostToolUse",  # Called after tool execution
    "PostToolUseFailure",  # Called when a tool execution fails
    "UserPromptSubmit",  # Called when user submits a prompt
    "Stop",  # Called when stopping execution
    "SubagentStop",  # Called when a subagent stops
    "PreCompact",  # Called before message compaction
    "Notification",  # Called for notification events
    "SubagentStart",  # Called when a subagent starts
    "PermissionRequest",  # Called when a permission decision is needed
]
```

The source notes that the TypeScript SDK supports additional hook events not yet available in Python: `SessionStart`, `SessionEnd`, `Setup`, `TeammateIdle`, `TaskCompleted`, `ConfigChange`, `WorktreeCreate`, `WorktreeRemove`, `PostToolBatch`, and `MessageDisplay`.

## `HookCallback`

Type definition for hook callback functions:

```python
HookCallback = Callable[[HookInput, str | None, HookContext], Awaitable[HookJSONOutput]]
```

Parameters:

- `input`: Strongly-typed hook input with discriminated unions based on `hook_event_name` (see `HookInput`).
- `tool_use_id`: Optional tool use identifier (for tool-related hooks).
- `context`: Hook context with additional information.

It returns a `HookJSONOutput` that may contain: `decision` (`"block"` to block the action), `systemMessage` (warning message shown to the user), and `hookSpecificOutput` (hook-specific output data).

## `HookContext` and `HookMatcher`

`HookContext` is the context information passed to each callback; `HookMatcher` is the configuration object that binds callbacks to events/tools (one or more `HookMatcher` lists per event in the `hooks` dict):

```python
class HookContext(TypedDict):
    signal: Any | None  # Future: abort signal support


@dataclass
class HookMatcher:
    matcher: str | None = (
        None  # Tool name or pattern to match (e.g., "Bash", "Write|Edit")
    )
    hooks: list[HookCallback] = field(
        default_factory=list
    )  # List of callbacks to execute
    timeout: float | None = (
        None  # Timeout in seconds for all hooks in this matcher (default: 60)
    )
```

## `HookInput` (per-event input types)

`HookInput` is a union whose actual type depends on the `hook_event_name` field: `PreToolUseHookInput | PostToolUseHookInput | PostToolUseFailureHookInput | UserPromptSubmitHookInput | StopHookInput | SubagentStopHookInput | PreCompactHookInput | NotificationHookInput | SubagentStartHookInput | PermissionRequestHookInput`.

All variants subclass `BaseHookInput`, which carries the fields present in every hook input: `session_id: str` (current session identifier), `transcript_path: str` (path to the session transcript file), `cwd: str` (current working directory), and `permission_mode: NotRequired[str]` (current permission mode).

Each variant then adds its `hook_event_name` discriminant plus event-specific fields (per-event fields beyond `BaseHookInput`):

| `*HookInput` | `hook_event_name` | Added fields (beyond `BaseHookInput`) |
| :--- | :--- | :--- |
| `PreToolUseHookInput` | `"PreToolUse"` | `tool_name: str`; `tool_input: dict[str, Any]`; `tool_use_id: str`; `agent_id` (optional); `agent_type` (optional) |
| `PostToolUseHookInput` | `"PostToolUse"` | `tool_name: str`; `tool_input: dict[str, Any]`; `tool_response: Any`; `tool_use_id: str`; `agent_id` (optional); `agent_type` (optional) |
| `PostToolUseFailureHookInput` | `"PostToolUseFailure"` | `tool_name: str`; `tool_input: dict[str, Any]`; `tool_use_id: str`; `error: str`; `is_interrupt` (optional, whether the failure was caused by an interrupt); `agent_id` (optional); `agent_type` (optional) |
| `UserPromptSubmitHookInput` | `"UserPromptSubmit"` | `prompt: str` (the user's submitted prompt) |
| `StopHookInput` | `"Stop"` | `stop_hook_active: bool` |
| `SubagentStopHookInput` | `"SubagentStop"` | `stop_hook_active: bool`; `agent_id: str`; `agent_transcript_path: str`; `agent_type: str` |
| `PreCompactHookInput` | `"PreCompact"` | `trigger: Literal["manual", "auto"]`; `custom_instructions: str \| None` |
| `NotificationHookInput` | `"Notification"` | `message: str`; `title` (optional); `notification_type: str` |
| `SubagentStartHookInput` | `"SubagentStart"` | `agent_id: str`; `agent_type: str` |
| `PermissionRequestHookInput` | `"PermissionRequest"` | `tool_name: str`; `tool_input: dict[str, Any]`; `permission_suggestions: NotRequired[list[Any]]` (suggested permission updates from the CLI) |

The `agent_id` / `agent_type` optional fields on the tool hooks are present when the hook fires inside a subagent.

## `HookJSONOutput`

The value a callback returns: `HookJSONOutput = AsyncHookJSONOutput | SyncHookJSONOutput`.

`SyncHookJSONOutput` carries control fields, decision fields, and hook-specific output:

```python
class SyncHookJSONOutput(TypedDict):
    # Control fields
    continue_: NotRequired[bool]  # Whether to proceed (default: True)
    suppressOutput: NotRequired[bool]  # Hide stdout from transcript
    stopReason: NotRequired[str]  # Message when continue is False

    # Decision fields
    decision: NotRequired[Literal["block"]]
    systemMessage: NotRequired[str]  # Warning message for user
    reason: NotRequired[str]  # Feedback for Claude

    # Hook-specific output
    hookSpecificOutput: NotRequired[HookSpecificOutput]
```

Use `continue_` (with the trailing underscore) in Python code; it is automatically converted to `continue` when sent to the CLI.

`HookSpecificOutput` is a discriminated union of per-event output `TypedDict`s keyed by `hookEventName`; the shape depends on the event. For example, the `PreToolUse` variant carries the permission decision:

```python
class PreToolUseHookSpecificOutput(TypedDict):
    hookEventName: Literal["PreToolUse"]
    permissionDecision: NotRequired[Literal["allow", "deny", "ask", "defer"]]
    permissionDecisionReason: NotRequired[str]
    updatedInput: NotRequired[dict[str, Any]]
    additionalContext: NotRequired[str]
```

The other variants are: `PostToolUseHookSpecificOutput` (`additionalContext`, `updatedToolOutput`, and deprecated `updatedMCPToolOutput`), `PostToolUseFailureHookSpecificOutput` (`additionalContext`), `UserPromptSubmitHookSpecificOutput` (`additionalContext`), `NotificationHookSpecificOutput` (`additionalContext`), `SubagentStartHookSpecificOutput` (`additionalContext`), and `PermissionRequestHookSpecificOutput` (`decision: dict[str, Any]`). For full details on available fields per hook event, the source links to [Control execution with hooks](https://code.claude.com/docs/en/agent-sdk/hooks#outputs).

`AsyncHookJSONOutput` is the alternative return shape that defers hook execution — a `TypedDict` with `async_: Literal[True]` (set to `True` to defer) and `asyncTimeout: NotRequired[int]` (timeout in milliseconds). Use `async_` (with underscore) in Python code; it is automatically converted to `async` when sent to the CLI.

## Hook Usage Example

This example registers two hooks: one that blocks dangerous bash commands like `rm -rf /`, and another that logs all tool usage for auditing. The security hook only runs on Bash commands (via the `matcher`), while the logging hook runs on all tools.

```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher, HookContext
from typing import Any


async def validate_bash_command(
    input_data: dict[str, Any], tool_use_id: str | None, context: HookContext
) -> dict[str, Any]:
    """Validate and potentially block dangerous bash commands."""
    if input_data["tool_name"] == "Bash":
        command = input_data["tool_input"].get("command", "")
        if "rm -rf /" in command:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Dangerous command blocked",
                }
            }
    return {}


async def log_tool_use(
    input_data: dict[str, Any], tool_use_id: str | None, context: HookContext
) -> dict[str, Any]:
    """Log all tool usage for auditing."""
    print(f"Tool used: {input_data.get('tool_name')}")
    return {}


options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(
                matcher="Bash", hooks=[validate_bash_command], timeout=120
            ),  # 2 min for validation
            HookMatcher(
                hooks=[log_tool_use]
            ),  # Applies to all tools (default 60s timeout)
        ],
        "PostToolUse": [HookMatcher(hooks=[log_tool_use])],
    }
)

async for message in query(prompt="Analyze this codebase", options=options):
    print(message)
```

**Source**: https://code.claude.com/docs/en/agent-sdk/python
**Last Updated**: 2026-06-13
**Status**: Active
