---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - python_reference
keywords:
  - claude-agent-sdk message types
  - resultmessage usage
  - assistantmessage content blocks
  - tooluseblock toolresultblock
  - thinkingblock signature
  - cache_read_input_tokens
  - claudesdkerror exceptions
  - dataclass vs typeddict
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

# Claude Code Python SDK — Message, Content Block, and Error Types

## Overview

When you iterate the async stream returned by `query()` or `ClaudeSDKClient.receive_response()`, each item is a `Message`, and reading them by `isinstance` is how a Python host consumes a run's output. This note documents the three runtime output families of the `claude-agent-sdk`: the **message union** (`UserMessage`, `AssistantMessage`, `SystemMessage`, `ResultMessage`, `StreamEvent`, `RateLimitEvent`, plus the background-task messages), the **content blocks** carried inside assistant/user messages (`TextBlock`, `ThinkingBlock`, `ToolUseBlock`, `ToolResultBlock`), and the **five SDK exception classes** you catch around a query.

A runtime access caveat threads through all of these: classes decorated with `@dataclass` (such as `ResultMessage`, `AssistantMessage`, `TextBlock`) are object instances supporting attribute access (`msg.result`), while `TypedDict` classes (such as `TaskUsage`) are plain dicts requiring key access (`usage["total_tokens"]`). The configuration inputs these types pair with live in the sibling note [`cc_sdk_python_options_and_config_types`](cc_sdk_python_options_and_config_types.md).

## Message Types

### `Message` (the union)

`Message` is the union of every value the stream can yield:

```python
Message = (
    UserMessage
    | AssistantMessage
    | SystemMessage
    | ResultMessage
    | StreamEvent
    | RateLimitEvent
)
```

`UserMessage` (`@dataclass`) carries `content: str | list[ContentBlock]`, plus `uuid`, `parent_tool_use_id` (the tool-use ID if the message is a tool-result response), and `tool_use_result`. `AssistantMessage` (`@dataclass`) carries `content: list[ContentBlock]`, the `model: str` that generated it, optional `parent_tool_use_id`, an optional `error: AssistantMessageError`, per-message `usage` (same keys as `ResultMessage.usage`), and `message_id` (multiple messages from one turn share the same API message ID). `SystemMessage` (`@dataclass`) is a `subtype: str` plus a `data: dict[str, Any]` payload.

`AssistantMessageError` is a literal of the error types an assistant response can encounter:

| Value | |
| :-- | :-- |
| `authentication_failed` | `billing_error` |
| `rate_limit` | `invalid_request` |
| `server_error` | `max_output_tokens` |
| `unknown` | |

### `ResultMessage` — cost and usage

`ResultMessage` (`@dataclass`) is the final message of a turn and the single richest type in the SDK:

```python
@dataclass
class ResultMessage:
    subtype: str
    duration_ms: int
    duration_api_ms: int
    is_error: bool
    num_turns: int
    session_id: str
    stop_reason: str | None = None
    total_cost_usd: float | None = None
    usage: dict[str, Any] | None = None
    result: str | None = None
    structured_output: Any = None
    model_usage: dict[str, Any] | None = None
    permission_denials: list[Any] | None = None
    deferred_tool_use: DeferredToolUse | None = None
    errors: list[str] | None = None
    api_error_status: int | None = None
    uuid: str | None = None
```

`subtype` determines which other fields are populated: one of `"success"`, `"error_during_execution"`, `"error_max_turns"`, `"error_max_budget_usd"`, or `"error_max_structured_output_retries"`. The Python dataclass flattens all variants into one shape, so fields that don't apply to the returned subtype are `None`. Diagnostic fields: `is_error` is `True` whenever the conversation ended in error (always on `error_*`; on `"success"` it is `True` when the final model request failed); `api_error_status` is the HTTP status of the terminating API error (populated only on `"success"`); `result` is the final assistant text on `"success"` (or `None` on `error_*`); `errors` holds loop-level error strings (the max-turns message, etc.) only on `error_*`.

The `usage` dict (snake_case, aggregate) and `model_usage` dict (per-model, camelCase — passed through unmodified from the CLI to match the TypeScript `ModelUsage` type) report token consumption:

| `usage` key | Type | Description |
| :-- | :-- | :-- |
| `input_tokens` | `int` | Total input tokens consumed |
| `output_tokens` | `int` | Total output tokens generated |
| `cache_creation_input_tokens` | `int` | Tokens used to create new cache entries |
| `cache_read_input_tokens` | `int` | Tokens read from existing cache entries |

`model_usage` maps a model name to a per-model dict with `inputTokens`, `outputTokens`, `cacheReadInputTokens`, `cacheCreationInputTokens`, `webSearchRequests`, `costUSD` (estimated cost, computed client-side — see cost-tracking caveats), `contextWindow`, and `maxOutputTokens`.

### Streaming and rate-limit events

`StreamEvent` (`@dataclass`) is a partial-message update, received only when `include_partial_messages=True` in `ClaudeAgentOptions`; import via `from claude_agent_sdk.types import StreamEvent`. Its fields are `uuid`, `session_id`, `event: dict[str, Any]` (the raw Claude API stream event), and `parent_tool_use_id` (set when the event is from a subagent).

`RateLimitEvent` (`@dataclass`) is emitted when rate-limit status changes (for example `"allowed"` → `"allowed_warning"`); use it to warn users before a hard limit or to back off when status is `"rejected"`. It wraps a `rate_limit_info: RateLimitInfo` plus `uuid` and `session_id`. `RateLimitInfo` (`@dataclass`) carries `status` (`RateLimitStatus = Literal["allowed", "allowed_warning", "rejected"]`), `resets_at` (Unix timestamp), `rate_limit_type` (`Literal["five_hour", "seven_day", "seven_day_opus", "seven_day_sonnet", "overage"]`), `utilization` (0.0–1.0), the parallel `overage_*` fields for pay-as-you-go usage, and a `raw` dict with unmodeled fields.

### Background-task messages

Four `SystemMessage` subclasses report background work — a backgrounded Bash command, a `Monitor` watch, a subagent spawned via the Agent tool, or a remote agent (this naming is unrelated to the `Task`-to-`Agent` tool rename):

| Type | Key fields | When emitted |
| :-- | :-- | :-- |
| `TaskStartedMessage` | `task_id`, `description`, `tool_use_id`, `task_type` (`"local_bash"` / `"local_agent"` / `"remote_agent"`) | A background task starts |
| `TaskProgressMessage` | `task_id`, `description`, `usage: TaskUsage`, `last_tool_name` | Periodic progress updates |
| `TaskNotificationMessage` | `task_id`, `status` (`"completed"` / `"failed"` / `"stopped"`), `output_file`, `summary`, `usage: TaskUsage \| None` | A task completes, fails, or is stopped |
| `TaskUsage` (`TypedDict`) | `total_tokens`, `tool_uses`, `duration_ms` | Token/timing payload nested in the above |

## Content Block Types

`ContentBlock` is the union inside `AssistantMessage.content` (and `UserMessage.content` when it is a list):

```python
ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ToolResultBlock
```

All four are `@dataclass` (attribute access):

| Block | Fields | Carries |
| :-- | :-- | :-- |
| `TextBlock` | `text: str` | Plain assistant text |
| `ThinkingBlock` | `thinking: str`, `signature: str` | The model's extended reasoning (for thinking-capable models) |
| `ToolUseBlock` | `id: str`, `name: str`, `input: dict[str, Any]` | A tool-call request from the model |
| `ToolResultBlock` | `tool_use_id: str`, `content: str \| list[dict] \| None`, `is_error: bool \| None` | The result fed back for a tool call |

The `ToolUseBlock` → `ToolResultBlock` pair is the function-calling round-trip the agent loop runs; the per-tool input/output dict shapes referenced by these blocks are catalogued in [`cc_sdk_python_tool_io_and_sandbox`](cc_sdk_python_tool_io_and_sandbox.md).

## Error Types

The SDK raises five exception classes, all rooted at `ClaudeSDKError`:

```python
class ClaudeSDKError(Exception):
    """Base error for Claude SDK."""
```

- **`ClaudeSDKError`** — base class for all SDK errors; catch this to handle any SDK failure.
- **`CLIConnectionError(ClaudeSDKError)`** — raised when connection to Claude Code fails.
- **`CLINotFoundError(CLIConnectionError)`** — raised when the Claude Code CLI is not installed/found; `__init__(message="Claude Code not found", cli_path: str | None = None)`.
- **`ProcessError(ClaudeSDKError)`** — raised when the Claude Code process fails; carries `exit_code: int | None` and `stderr: str | None`.
- **`CLIJSONDecodeError(ClaudeSDKError)`** — raised when JSON parsing fails; carries `line` (the line that failed to parse) and `original_error` (the underlying JSON decode exception).

Note the hierarchy: `CLINotFoundError` subclasses `CLIConnectionError`, which subclasses `ClaudeSDKError`, so a broad `except ClaudeSDKError` catches all five. The entry-point note [`cc_sdk_python_entry_points`](cc_sdk_python_entry_points.md) shows the error-handling example that catches these around a `query()`.

**Source**: https://code.claude.com/docs/en/agent-sdk/python
**Last Updated**: 2026-06-13
**Status**: Active
