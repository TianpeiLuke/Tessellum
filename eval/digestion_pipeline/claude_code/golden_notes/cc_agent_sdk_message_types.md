---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - message_types
keywords:
  - agent sdk message types
  - systemmessage assistantmessage usermessage
  - streamevent resultmessage
  - message stream lifecycle
  - handle messages
  - isinstance vs type field
  - subtype init compact_boundary
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/agent-loop
access_control_group: ["general"]
---

# Agent SDK — Message Types

## Overview

As the Agent SDK loop runs, it yields a **stream of messages**, each carrying a type that tells you what stage of the loop it came from. There are **five core message types** — `SystemMessage`, `AssistantMessage`, `UserMessage`, `StreamEvent`, and `ResultMessage` — and together they cover the full agent-loop lifecycle in both the Python and TypeScript SDKs. Iterating that stream is how your application observes session startup, each Claude turn, each tool result, optional real-time deltas, and the final termination.

Which messages you actually handle depends on what you are building, and *how* you check a message's type depends on the SDK: Python uses `isinstance()` against imported classes, while TypeScript checks a `type` string field. This note documents the five types, the SDK-specific handling idioms, and which messages to handle per use case. It dissects the "Message types" stage of the broader [agent loop](cc_agent_sdk_agent_loop.md).

## The Five Core Message Types

As the loop runs, the SDK yields a stream of messages; each message carries a type that tells you what stage of the loop it came from. The five core types are:

- **`SystemMessage`** — session lifecycle events. The `subtype` field distinguishes them: `"init"` is the first message (session metadata), and `"compact_boundary"` fires after compaction. In TypeScript, the compact boundary is its own `SDKCompactBoundaryMessage` type rather than a subtype of `SDKSystemMessage`.
- **`AssistantMessage`** — emitted after each Claude response, including the final text-only one. Contains text content blocks and tool call blocks from that turn.
- **`UserMessage`** — emitted after each tool execution with the tool result content sent back to Claude. Also emitted for any user inputs you stream mid-loop.
- **`StreamEvent`** — only emitted when partial messages are enabled. Contains raw API streaming events (text deltas, tool input chunks). See [Stream responses](https://code.claude.com/docs/en/agent-sdk/streaming-output).
- **`ResultMessage`** — marks the end of the agent loop. Contains the final text result, token usage, cost, and session ID. Check the `subtype` field to determine whether the task succeeded or hit a limit. A small number of trailing system events, such as `prompt_suggestion`, can arrive after it, so iterate the stream to completion rather than breaking on the result. See [Handle the result](cc_agent_sdk_result_and_hooks.md).

These five types cover the full agent-loop lifecycle in both SDKs. The TypeScript SDK also yields **additional observability events** (hook events, tool progress, rate limits, task notifications) that provide extra detail but are not required to drive the loop. See the [Python message types reference](https://code.claude.com/docs/en/agent-sdk/python#message-types) and [TypeScript message types reference](https://code.claude.com/docs/en/agent-sdk/typescript#message-types) for the complete lists.

### Where each type comes from in the loop

The message types map directly onto loop stages: the SDK yields a `SystemMessage` with subtype `"init"` first; each `AssistantMessage` follows a Claude response (text and/or tool-call blocks); each `UserMessage` carries the tool result content back to Claude after the SDK executes the requested tools; a final text-only `AssistantMessage` precedes the terminating `ResultMessage`. (`AssistantMessage` carries the tool-call requests and `UserMessage` carries the tool results — the request/response pair of tool execution; see [tool execution](cc_agent_sdk_tool_execution.md).)

## Handle Messages

Which messages you handle depends on what you are building:

- **Final results only:** handle `ResultMessage` to get the output, cost, and whether the task succeeded or hit a limit.
- **Progress updates:** handle `AssistantMessage` to see what Claude is doing each turn, including which tools it called.
- **Live streaming:** enable partial messages (`include_partial_messages` in Python, `includePartialMessages` in TypeScript) to get `StreamEvent` messages in real time. See [Stream responses in real-time](https://code.claude.com/docs/en/agent-sdk/streaming-output).

How you check message types depends on the SDK:

- **Python:** check message types with `isinstance()` against classes imported from `claude_agent_sdk` (for example, `isinstance(message, ResultMessage)`).
- **TypeScript:** check the `type` string field (for example, `message.type === "result"`). `AssistantMessage` and `UserMessage` wrap the raw API message in a `.message` field, so content blocks are at `message.message.content`, not `message.content`.

### Example: check message types and handle results

The same iteration in Python (`isinstance` against imported classes) — the TypeScript equivalent uses `message.type === "assistant"` / `"result"` and reads content blocks from `message.message.content`:

```python Python
from claude_agent_sdk import query, AssistantMessage, ResultMessage

async for message in query(prompt="Summarize this project"):
    if isinstance(message, AssistantMessage):
        print(f"Turn completed: {len(message.content)} content blocks")
    if isinstance(message, ResultMessage):
        if message.subtype == "success":
            print(message.result)
        else:
            print(f"Stopped: {message.subtype}")
```

**Source**: https://code.claude.com/docs/en/agent-sdk/agent-loop
**Last Updated**: 2026-06-13
**Status**: Active
