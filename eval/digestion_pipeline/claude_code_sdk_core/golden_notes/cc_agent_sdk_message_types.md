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

## Related Notes

### Related Notes (Claude Code Series)

- [Agent Loop](cc_agent_sdk_agent_loop.md) — the turns-and-messages cycle that emits this message stream; this note details the message-type stage of that loop.
- [Tool Execution](cc_agent_sdk_tool_execution.md) — the tool-call/tool-result step whose requests ride on `AssistantMessage` and whose results ride on `UserMessage`.
- [Result and Hooks](cc_agent_sdk_result_and_hooks.md) — the `ResultMessage` subtypes, `stop_reason`, and cost/usage fields used to handle loop termination.
- [Python SDK — Message, Content Block, and Error Types](cc_sdk_python_message_and_error_types.md) — the Python-side reference for the same `UserMessage`/`AssistantMessage`/`SystemMessage`/`ResultMessage`/`StreamEvent` union plus the content blocks inside them; expands the `isinstance` handling this note introduces.
- [TypeScript SDK — Message and Hook Types](cc_sdk_typescript_message_and_hook_types.md) — the TypeScript-side reference for the `SDKMessage` discriminated union pattern-matched by `type`/`subtype`; expands the `message.type === "..."` idiom this note contrasts with Python.
- [Partial-Message Output Streaming](cc_sdk_streaming_output.md) — documents the `StreamEvent`/`SDKPartialAssistantMessage` type and the `include_partial_messages` flag that this note lists as the trigger for real-time deltas.
- [Stream Text and Tool Calls](cc_sdk_stream_text_and_tool_calls.md) — the concrete consume-the-stream recipes (printing text deltas, surfacing tool calls) built on the message types catalogued here.
- [Controlling How the Loop Runs](cc_agent_sdk_loop_controls.md) — the turn/cost/effort/permission knobs whose limit outcomes surface in the `ResultMessage` `subtype` field this note tells you to check.

### Related Notes (Out-of-Series)

- [Claude Code](../../term_dictionary/term_claude_code.md) — the five message types are the Agent SDK's (Claude Code's library form) public streaming surface; the product term anchors the API this note documents.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — `SystemMessage`/`AssistantMessage`/`UserMessage`/`StreamEvent`/`ResultMessage` are the harness's emitted lifecycle events; the harness term frames what produces this message stream.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — `AssistantMessage` carries tool-call blocks and `UserMessage` carries tool results — the function-calling request/response pair surfaced as message types.
- [Structured Output](../../term_dictionary/term_structured_output.md) — `ResultMessage` exposes a typed `subtype`/`result`/`usage` schema and an `error_max_structured_output_retries` subtype; the note's typed-result handling is the structured-output contract this term defines.
- [ReAct](../../term_dictionary/term_react.md) — the message sequence (`AssistantMessage` action → `UserMessage` observation → next `AssistantMessage`) is the observable trace of the reason-act-observe cycle this term names.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — `AssistantMessage` tool-call blocks reference tool names/inputs defined by tool descriptors; the term grounds the tool-definition side of the messages this note parses.
- [Observability (Agent Systems)](../../term_dictionary/term_observability_agent_systems.md) — `ResultMessage`'s token usage / cost fields and the `AssistantMessage`→`UserMessage` trajectory are exactly the per-turn telemetry and trajectory tracing this observability concept consumes.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — a contrasting agent-API surface whose client-managed tool-call loop (model requests → client executes → client returns result) and typed streaming event payloads parallel the `AssistantMessage`/`UserMessage`/`StreamEvent` shapes this note defines.
- [AgentCore Runtime — Response Streaming](../aws_bedrock_agentcore/bedrock_agentcore_streaming_response.md) — an analogous "iterate a stream of yielded events" pattern in a different runtime (`agent.stream_async()` via async generator), comparable to consuming this SDK's async message stream to completion.
- [Band human event payload data model](../band/band_websocket_human_events.md) — the human-channel envelope/payload data model whose client destructures and switches on `event`/`message_type`; relevance: a directly analogous typed-message contract to this note's five-type stream where a client branches on a `type` field, so a reader comparing typed message-stream data models would want Band's human payload model as a parallel external precedent.
- *(No tool note is closely relevant: the operational ticket-agent tools surfaced by search are production-ops bots, not consumers of the Agent SDK message stream.)*
- *(No project note is closely relevant: the callout-agent project hits are domain-specific experiment-result reports, unrelated to SDK message-type handling.)*

**Source**: https://code.claude.com/docs/en/agent-sdk/agent-loop
**Last Updated**: 2026-06-13
**Status**: Active
