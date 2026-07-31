---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - input_modes
keywords:
  - streaming input mode
  - single message input
  - claude agent sdk input
  - claudesdkclient
  - one-shot query
  - session resuming
  - long lived process
  - mode decision guide
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode
access_control_group: ["general"]
---

# Claude Agent SDK — Streaming vs Single Message Input Modes

## Overview

The Claude Agent SDK supports **two distinct input modes** for interacting with agents, and choosing between them is the central design decision this note frames. **Streaming Input Mode** (the default and recommended mode) runs the agent as a persistent, interactive session; **Single Message Input** issues one-shot queries that rely on session state and resuming. The two modes trade interactivity and capability against operational simplicity, so the right choice depends on whether the application needs a long-lived interactive agent or stateless one-shot responses.

This note is the decision guide — the *why* and *when* of each mode (overview, how streaming works, benefits, when to use single-message, limitations). The concrete code for each mode lives in the companion procedure note [Streaming Input Example](cc_sdk_streaming_input_example.md).

## Streaming Input Mode (Recommended)

Streaming input mode is the **preferred** way to use the Claude Agent SDK. It provides full access to the agent's capabilities and enables rich, interactive experiences. It allows the agent to operate as a **long lived process** that takes in user input, handles interruptions, surfaces permission requests, and handles session management.

### How It Works

The application initializes the agent with an `AsyncGenerator` and then yields messages into the live session. The agent executes tools (reading, writing, and editing files against the environment/file system), streams partial responses back to the application as they are generated, and completes each message. The application can yield follow-up messages (including images), queue additional messages, and interrupt or cancel mid-flight. Throughout, the **session stays alive** and persistent file-system state is maintained across messages. (The source documents this flow with a `sequenceDiagram` between the application, the Claude agent, tools/hooks, and the environment/file system.)

### Benefits

The source lists five benefits of streaming input mode:

- **Image Uploads** — attach images directly to messages for visual analysis and understanding.
- **Queued Messages** — send multiple messages that process sequentially, with the ability to interrupt.
- **Tool Integration** — full access to all tools and custom MCP servers during the session.
- **Real-time Feedback** — see responses as they're generated, not just final results.
- **Context Persistence** — maintain conversation context across multiple turns naturally.

## Single Message Input

Single message input is **simpler but more limited**.

### When to Use Single Message Input

Use single message input when:

- You need a one-shot response.
- You do not need image attachments or mid-session control methods.
- You need to operate in a **stateless environment, such as a lambda function**.

Single-message mode uses the `query()` function and resumes prior context via session management — the source's TypeScript example sets `continue: true` and the Python example sets `continue_conversation=True` to continue a conversation across separate one-shot calls. (See the companion procedure note for the code.)

### Limitations

Single message input mode does **not** support:

- Direct image attachments in messages
- Dynamic message queueing
- Real-time interruption
- Natural multi-turn conversations

If a query ends with an error result, such as `error_max_turns`, a single message `query()` call raises an error that includes the failure text after yielding the final result message, so the source advises wrapping the loop in a `try` block if your code needs to continue. (The result subtypes are documented in the agent-loop page — see https://code.claude.com/docs/en/agent-sdk/agent-loop.)

## Choosing a Mode

Pick **streaming input mode** (the default) for interactive, multi-turn experiences: image analysis, queued messages with interruption, full tool/MCP access, and real-time feedback in a long-lived session. Pick **single message input** for one-shot responses in stateless environments (e.g. a lambda function) where image attachments, mid-session control, and natural multi-turn conversation are not needed, resuming context with `continue`/`continue_conversation` when a follow-up is required.

**Source**: https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode
**Last Updated**: 2026-06-13
**Status**: Active
