---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - python
keywords:
  - claude-agent-sdk
  - query function
  - claudesdkclient
  - async iterator
  - one-off task
  - continuous conversation
  - permission_mode
  - streaming input
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

# Claude Agent SDK (Python) — Entry Points: query() and ClaudeSDKClient

## Overview

The Python Agent SDK (`claude-agent-sdk`) gives a program two ways to drive Claude Code: the `query()` function for one-off, stateless interactions, and the `ClaudeSDKClient` class for stateful, continuous conversations. This note covers installation, the decision between the two entry points, the full `query()` signature, and the basic usage patterns (file operations, error handling, streaming). The `ClaudeSDKClient` class itself is documented in [cc_sdk_python_client](cc_sdk_python_client.md); the `ClaudeAgentOptions` configuration object passed to both is documented in [cc_sdk_python_options_and_config_types](cc_sdk_python_options_and_config_types.md). The conceptual agent-loop behavior these entry points run is owned by the [agent-loop guide](https://code.claude.com/docs/en/agent-sdk/agent-loop).

## Installation

```bash
pip install claude-agent-sdk
```

## Choosing between query() and ClaudeSDKClient

The SDK provides two ways to interact with Claude Code. The choice is primarily about whether you need conversation memory and explicit lifecycle control.

| Feature | `query()` | `ClaudeSDKClient` |
| :--- | :--- | :--- |
| **Session** | Creates a new session by default | Reuses same session |
| **Conversation** | Single exchange | Multiple exchanges in same context |
| **Connection** | Managed automatically | Manual control |
| **Streaming Input** | Supported | Supported |
| **Interrupts** | Not supported | Supported |
| **Hooks** | Supported | Supported |
| **Custom Tools** | Supported | Supported |
| **Continue Chat** | Manual via `continue_conversation` or `resume` | Automatic |
| **Use Case** | One-off tasks | Continuous conversations |

**Use `query()`** for: one-off questions where you don't need conversation history; independent tasks that don't require context from previous exchanges; simple automation scripts; and when you want a fresh start each time.

**Use `ClaudeSDKClient`** for: continuing conversations where Claude must remember context; follow-up questions building on previous responses; interactive applications (chat interfaces, REPLs); response-driven logic where the next action depends on Claude's response; and explicit session-lifecycle management.

## Functions: query()

`query()` creates a new session for each interaction by default and returns an async iterator that yields messages as they arrive. Each call starts fresh with no memory of previous interactions unless you pass `continue_conversation=True` or `resume` in `ClaudeAgentOptions`.

```python
async def query(
    *,
    prompt: str | AsyncIterable[dict[str, Any]],
    options: ClaudeAgentOptions | None = None,
    transport: Transport | None = None
) -> AsyncIterator[Message]
```

**Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `prompt` | `str \| AsyncIterable[dict]` | The input prompt as a string or async iterable for streaming mode |
| `options` | `ClaudeAgentOptions \| None` | Optional configuration object (defaults to `ClaudeAgentOptions()` if None) |
| `transport` | `Transport \| None` | Optional custom transport for communicating with the CLI process |

**Returns** an `AsyncIterator[Message]` that yields messages from the conversation. (Message types are documented in [cc_sdk_python_message_and_error_types](cc_sdk_python_message_and_error_types.md).)

### Example — with options

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are an expert Python developer",
        permission_mode="acceptEdits",
        cwd="/home/user/project",
    )

    async for message in query(prompt="Create a Python web server", options=options):
        print(message)


asyncio.run(main())
```

## Example Usage

### Basic file operations (using query)

Iterate the async iterator and dispatch on message type — here filtering for `AssistantMessage` content blocks that are `ToolUseBlock` to log each tool the agent invokes.

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ToolUseBlock
import asyncio


async def create_project():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode="acceptEdits",
        cwd="/home/user/project",
    )

    async for message in query(
        prompt="Create a Python project structure with setup.py", options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    print(f"Using tool: {block.name}")


asyncio.run(create_project())
```

### Error handling

`query()` can raise the SDK's exception classes (see [cc_sdk_python_message_and_error_types](cc_sdk_python_message_and_error_types.md)); wrap iteration in `try`/`except` to handle a missing CLI, a process failure, or a JSON decode error.

```python
from claude_agent_sdk import query, CLINotFoundError, ProcessError, CLIJSONDecodeError

try:
    async for message in query(prompt="Hello"):
        print(message)
except CLINotFoundError:
    print(
        "Claude Code CLI not found. Try reinstalling: pip install --force-reinstall claude-agent-sdk"
    )
except ProcessError as e:
    print(f"Process failed with exit code: {e.exit_code}")
except CLIJSONDecodeError as e:
    print(f"Failed to parse response: {e}")
```

### Streaming mode

Both entry points accept an `AsyncIterable[dict]` for `prompt` to stream input. The source's streaming example uses `ClaudeSDKClient` (sending an initial query, draining `receive_response()`, then sending a follow-up in the same session) — see [cc_sdk_python_client](cc_sdk_python_client.md) for that pattern. For partial output streaming, set `include_partial_messages=True` in options to receive `StreamEvent` messages. Streaming semantics are owned by the [streaming-input guide](https://code.claude.com/docs/en/agent-sdk/streaming-input).

**Source**: https://code.claude.com/docs/en/agent-sdk/python
**Last Updated**: 2026-06-13
**Status**: Active
