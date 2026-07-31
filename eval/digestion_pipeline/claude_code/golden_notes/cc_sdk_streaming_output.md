---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - streaming
keywords:
  - partial message streaming
  - include_partial_messages
  - streamevent
  - sdkpartialassistantmessage
  - content_block_delta
  - text_delta
  - input_json_delta
  - message flow ordering
  - raw claude api events
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/streaming-output
access_control_group: ["general"]
---

# Agent SDK — Partial-Message Output Streaming

## Overview

By default, the Agent SDK yields complete `AssistantMessage` objects only after Claude finishes generating each response. To receive incremental updates as text and tool calls are generated, you enable **partial message streaming** by setting `include_partial_messages` (Python) or `includePartialMessages` (TypeScript) to `true` in your options. With this enabled, the SDK yields `StreamEvent` messages that wrap raw Claude API streaming events as they arrive, in addition to the usual `AssistantMessage` and `ResultMessage`.

This note describes the streaming-output data model: the option that turns it on, the `StreamEvent`/`SDKPartialAssistantMessage` type that carries raw API events, the event-type vocabulary, the ordering of messages in a turn, and the boundary where structured output sits outside the stream. (This page covers *output* streaming — receiving tokens in real time. For *input* modes (how you send messages) see [Interactive vs one-shot queries](cc_sdk_input_modes.md). The three concrete consume-the-stream recipes live in [Stream text and tool calls](cc_sdk_stream_text_and_tool_calls.md).)

## Enable streaming output

Set `include_partial_messages` (Python) / `includePartialMessages` (TypeScript) to `true` in your options. This causes the SDK to yield `StreamEvent` messages containing raw API events as they arrive, alongside the usual `AssistantMessage` and `ResultMessage`. Your code then needs to:

1. Check each message's type to distinguish `StreamEvent` from other message types.
2. For `StreamEvent`, extract the `event` field and check its `type`.
3. Look for `content_block_delta` events where `delta.type` is `text_delta`, which contain the actual text chunks.

These are nested type checks: first for `StreamEvent`, then for `content_block_delta`, then for `text_delta`.

## StreamEvent reference

When partial messages are enabled, you receive raw Claude API streaming events wrapped in an object. The wrapper type has a different name in each SDK:

* **Python**: `StreamEvent` (import from `claude_agent_sdk.types`)
* **TypeScript**: `SDKPartialAssistantMessage` with `type: 'stream_event'`

Both contain raw Claude API events, **not** accumulated text — you must extract and accumulate text deltas yourself. The field schema of each type:

```python Python
@dataclass
class StreamEvent:
    uuid: str  # Unique identifier for this event
    session_id: str  # Session identifier
    event: dict[str, Any]  # The raw Claude API stream event
    parent_tool_use_id: str | None  # Parent tool ID if from a subagent
```

```typescript TypeScript
type SDKPartialAssistantMessage = {
  type: "stream_event";
  event: BetaRawMessageStreamEvent; // From Anthropic SDK
  parent_tool_use_id: string | null;
  uuid: UUID;
  session_id: string;
  ttft_ms?: number; // Time to first token in ms, present only on message_start events
};
```

The `event` field contains the raw streaming event from the [Claude API](https://platform.claude.com/docs/en/build-with-claude/streaming#event-types). Common event types:

| Event Type | Description |
| :--- | :--- |
| `message_start` | Start of a new message |
| `content_block_start` | Start of a new content block (text or tool use) |
| `content_block_delta` | Incremental update to content |
| `content_block_stop` | End of a content block |
| `message_delta` | Message-level updates (stop reason, usage) |
| `message_stop` | End of the message |

## Message flow

With partial messages enabled, you receive messages in this order:

```text
StreamEvent (message_start)
StreamEvent (content_block_start) - text block
StreamEvent (content_block_delta) - text chunks...
StreamEvent (content_block_stop)
StreamEvent (content_block_start) - tool_use block
StreamEvent (content_block_delta) - tool input chunks...
StreamEvent (content_block_stop)
StreamEvent (message_delta)
StreamEvent (message_stop)
AssistantMessage - complete message with all content
... tool executes ...
... more streaming events for next turn ...
ResultMessage - final result
```

Without partial messages enabled, you receive all message types **except** `StreamEvent`. Common types then include `SystemMessage` (session initialization), `AssistantMessage` (complete responses), `ResultMessage` (final result), and a compact boundary message indicating when conversation history was compacted (`SDKCompactBoundaryMessage` in TypeScript; `SystemMessage` with subtype `"compact_boundary"` in Python).

## Known limitations

* **Structured output**: the JSON result appears only in the final `ResultMessage.structured_output`, **not** as streaming deltas. See [Structured outputs](cc_sdk_structured_outputs.md) for details — this is the explicit boundary between the partial-message stream and the typed structured-output result.

**Source**: https://code.claude.com/docs/en/agent-sdk/streaming-output
**Last Updated**: 2026-06-13
**Status**: Active
