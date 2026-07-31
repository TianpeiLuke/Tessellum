---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - python
keywords:
  - claudesdkclient
  - stateful session client
  - continuous conversation
  - interrupt
  - set_permission_mode
  - set_model
  - rewind_files
  - mcp control methods
  - async context manager
  - progress monitoring
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

# Claude Code Python SDK — `ClaudeSDKClient`

## Overview

`ClaudeSDKClient` is the stateful Python entry point into the `claude-agent-sdk`. Unlike `query()` (a fresh one-off agent each call), the client **maintains a conversation session across multiple exchanges** — the session retains previous messages, so follow-up `query()` calls build on prior context. It is the Python equivalent of how the TypeScript SDK's `query()` works internally: it creates a client object that can continue conversations, with explicit lifecycle control, interrupt support, and runtime model/permission/MCP changes.

This note documents the class's methods, async-context-manager usage, the interrupt buffer-drain caveat, and the advanced continuous-conversation / progress-monitoring patterns. Conceptual SDK material is owned elsewhere: session behavior at [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions), file checkpointing at [File checkpointing](https://code.claude.com/docs/en/agent-sdk/file-checkpointing), and the options surface in [`cc_sdk_python_options_and_config_types`](cc_sdk_python_options_and_config_types.md).

## Key Features

- **Session continuity** — maintains conversation context across multiple `query()` calls; the session retains previous messages.
- **Interrupt support** — can stop execution mid-task.
- **Explicit lifecycle** — you control when the session starts and ends.
- **Response-driven flow** — can react to responses and send follow-ups.
- **Custom tools and hooks** — supports custom tools (created with the `@tool` decorator) and hooks.

## Class definition and methods

```python
class ClaudeSDKClient:
    def __init__(self, options: ClaudeAgentOptions | None = None, transport: Transport | None = None)
    async def connect(self, prompt: str | AsyncIterable[dict] | None = None) -> None
    async def query(self, prompt: str | AsyncIterable[dict], session_id: str = "default") -> None
    async def receive_messages(self) -> AsyncIterator[Message]
    async def receive_response(self) -> AsyncIterator[Message]
    async def interrupt(self) -> None
    async def set_permission_mode(self, mode: str) -> None
    async def set_model(self, model: str | None = None) -> None
    async def rewind_files(self, user_message_id: str) -> None
    async def get_mcp_status(self) -> McpStatusResponse
    async def reconnect_mcp_server(self, server_name: str) -> None
    async def toggle_mcp_server(self, server_name: str, enabled: bool) -> None
    async def stop_task(self, task_id: str) -> None
    async def get_server_info(self) -> dict[str, Any] | None
    async def disconnect(self) -> None
```

| Method | Description |
| :--- | :--- |
| `__init__(options)` | Initialize the client with optional configuration |
| `connect(prompt)` | Connect to Claude with an optional initial prompt or message stream |
| `query(prompt, session_id)` | Send a new request in streaming mode |
| `receive_messages()` | Receive all messages from Claude as an async iterator |
| `receive_response()` | Receive messages until and including a `ResultMessage` |
| `interrupt()` | Send interrupt signal (only works in streaming mode) |
| `set_permission_mode(mode)` | Change the permission mode for the current session |
| `set_model(model)` | Change the model for the current session. Pass `None` to reset to default |
| `rewind_files(user_message_id)` | Restore files to their state at the specified user message. Requires `enable_file_checkpointing=True` |
| `get_mcp_status()` | Get the status of all configured MCP servers. Returns `McpStatusResponse` |
| `reconnect_mcp_server(server_name)` | Retry connecting to an MCP server that failed or was disconnected |
| `toggle_mcp_server(server_name, enabled)` | Enable or disable an MCP server mid-session. Disabling removes its tools |
| `stop_task(task_id)` | Stop a running background task. A `TaskNotificationMessage` with status `"stopped"` follows in the message stream |
| `get_server_info()` | Get server information including session ID and capabilities |
| `disconnect()` | Disconnect from Claude |

## Context manager support

The client can be used as an async context manager for automatic connection management:

```python
async with ClaudeSDKClient() as client:
    await client.query("Hello Claude")
    async for message in client.receive_response():
        print(message)
```

> **Important:** When iterating over messages, avoid using `break` to exit early as this can cause asyncio cleanup issues. Instead, let the iteration complete naturally or use flags to track when you've found what you need.

## Continuing a conversation

Each `query()` call sends a new turn; because the client reuses the same session, follow-up turns retain the previous context (e.g. ask "What's the capital of France?", then "What's the population of that city?" — Claude remembers "that city"):

```python
async with ClaudeSDKClient() as client:
    # First question
    await client.query("What's the capital of France?")
    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")

    # Follow-up - the session retains the previous context
    await client.query("What's the population of that city?")
    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
```

The client also accepts an async generator as the `query()` prompt for **streaming input** (yield `{"type": "user", "message": {"role": "user", "content": ...}}` dicts), and supports **custom tools** built with `@tool` + `create_sdk_mcp_server()` passed via `ClaudeAgentOptions(mcp_servers=...)` — see [`cc_sdk_python_options_and_config_types`](cc_sdk_python_options_and_config_types.md) and the [custom tools guide](https://code.claude.com/docs/en/agent-sdk/custom-tools).

## Interrupts and the buffer-drain caveat

`interrupt()` (streaming mode only) stops a long-running task mid-execution:

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("Count from 1 to 100 slowly, using the bash sleep command")
    await asyncio.sleep(2)
    await client.interrupt()

    # Drain the interrupted task's messages (including its ResultMessage)
    async for message in client.receive_response():
        if isinstance(message, ResultMessage):
            print(f"Interrupted task finished with subtype={message.subtype!r}")
            # subtype is "error_during_execution" for interrupted tasks
```

> **Buffer behavior after interrupt:** `interrupt()` sends a stop signal but does not clear the message buffer. Messages already produced by the interrupted task, including its `ResultMessage` (with `subtype="error_during_execution"`), remain in the stream. You must drain them with `receive_response()` before reading the response to a new query. If you send a new query immediately after `interrupt()` and call `receive_response()` only once, you'll receive the interrupted task's messages, not the new query's response.

## Advanced features

**Continuous conversation interface** — wrap the client in a long-lived loop (e.g. a `ConversationSession` class that calls `connect()` once, reads user input in a `while` loop, dispatches `exit`/`interrupt`/`new` commands, and streams each turn's response). A `new` command calls `disconnect()` then `connect()` to start a fresh session with previous context cleared. Pair with `set_permission_mode()` to escalate trust (e.g. `"default"` → `"acceptEdits"`) mid-run and `set_model()` to switch models per turn.

**Hooks for behavior modification** — pass `hooks={...}` on `ClaudeAgentOptions` to register `PreToolUse`/`PostToolUse`/`UserPromptSubmit` callbacks that log, block (return a `permissionDecision: "deny"` payload), or inject `additionalContext`. See [`cc_sdk_python_hook_types`](cc_sdk_python_hook_types.md) for the type contract and [Hooks](https://code.claude.com/docs/en/agent-sdk/hooks) for usage.

**Advanced permission control** — supply a `can_use_tool` callback that returns `PermissionResultAllow`/`PermissionResultDeny` to redirect or block specific tool calls at runtime:

```python
async def custom_permission_handler(tool_name, input_data, context: ToolPermissionContext):
    if tool_name == "Write" and input_data.get("file_path", "").startswith("/system/"):
        return PermissionResultDeny(message="System directory write not allowed", interrupt=True)
    if tool_name in ["Write", "Edit"] and "config" in input_data.get("file_path", ""):
        safe_path = f"./sandbox/{input_data['file_path']}"
        return PermissionResultAllow(updated_input={**input_data, "file_path": safe_path})
    return PermissionResultAllow(updated_input=input_data)
```

**Real-time progress monitoring** — inspect each streamed `AssistantMessage`'s content blocks to report tool activity as it happens:

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("Create 5 Python files with different sorting algorithms")
    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    if block.name == "Write":
                        print(f"Creating: {block.input.get('file_path', '')}")
                elif isinstance(block, ToolResultBlock):
                    print("Completed tool execution")
                elif isinstance(block, TextBlock):
                    print(f"Claude says: {block.text[:100]}...")
```

The message and content-block types iterated above are defined in [`cc_sdk_python_message_and_error_types`](cc_sdk_python_message_and_error_types.md).

**Source**: https://code.claude.com/docs/en/agent-sdk/python
**Last Updated**: 2026-06-13
**Status**: Active
