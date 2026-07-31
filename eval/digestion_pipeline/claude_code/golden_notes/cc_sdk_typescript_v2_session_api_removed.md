---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - deprecation
keywords:
  - v2 session api removed
  - unstable_v2_createsession
  - unstable_v2_resumesession
  - unstable_v2_prompt
  - sdksession interface
  - send stream split
  - version pin 0.2
  - migrate to query
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/typescript-v2-preview
access_control_group: ["general"]
---

# TypeScript SDK — V2 Session API (Removed)

## Overview

The **V2 session API** was an experimental TypeScript Agent SDK interface that removed the need for async generators and yield coordination: instead of managing generator state across turns, each turn was a separate `send()`/`stream()` cycle exposed through three functions — `unstable_v2_createSession()` / `unstable_v2_resumeSession()` to start or continue a conversation, `session.send()` to send a message, and `session.stream()` to get the response. It is **no longer supported** — TypeScript Agent SDK **0.3.142** removes `unstable_v2_createSession`, `unstable_v2_resumeSession`, `unstable_v2_prompt`, and the `SDKSession` and `SDKSessionOptions` types.

This note documents the removed surface and the supported migration path so that code still pinned to Agent SDK 0.2.x can be understood and moved forward. The replacement is the V1 [`query()` API](cc_sdk_typescript_query_function.md) plus its session options.

## Installation (version-pin boundary)

Agent SDK **0.2.x is the last version that includes the V2 interface**. The package version jumped from 0.2.x directly to 0.3.142, so the removal version and the install pin describe the same boundary. To install the last V2-compatible release, pin the major and minor version:

```bash
npm install @anthropic-ai/claude-agent-sdk@0.2
```

The SDK bundles a native Claude Code binary for your platform as an optional dependency, so you do not need to install Claude Code separately.

## API reference (removed)

| Function / type | Purpose | Signature (summary) |
|---|---|---|
| `unstable_v2_createSession(options)` | Create a new session for multi-turn conversations | returns `SDKSession` |
| `unstable_v2_resumeSession(sessionId, options)` | Resume an existing session by ID | returns `SDKSession` |
| `unstable_v2_prompt(prompt, options)` | One-shot convenience for single-turn queries | returns `Promise<SDKResultMessage>` |
| `SDKSessionOptions` | Options type accepted by the session functions | removed |

`options` for all three carried at least `model: string` plus additional supported options. The `SDKSession` interface was the live session handle:

```typescript
interface SDKSession {
  readonly sessionId: string;
  send(message: string | SDKUserMessage): Promise<void>;
  stream(): AsyncGenerator<SDKMessage, void>;
  close(): void;
}
```

## Usage pattern (the send/stream split)

V2 separated dispatching a message (`send()`) from streaming back the response (`stream()`), which made it easier to add logic between turns. Sessions persisted context across exchanges; calling `send()` again on the same session continued the conversation. Sessions closed manually via `session.close()` or automatically with [`await using`](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-2.html#using-declarations-and-explicit-resource-management) (TypeScript 5.2+ explicit resource management):

```typescript
import { unstable_v2_createSession } from "@anthropic-ai/claude-agent-sdk";

await using session = unstable_v2_createSession({
  model: "claude-opus-4-7"
});

await session.send("Hello!");
for await (const msg of session.stream()) {
  if (msg.type === "assistant") {
    const text = msg.message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("");
    console.log(text);
  }
}
```

Session resume stored a `session_id` taken from any received message, closed the session, then later passed that ID to `unstable_v2_resumeSession()`.

## Feature availability

The V2 session API did **not** support every V1 feature. The following required the V1 SDK: **session forking** (the `forkSession` option) and **some advanced streaming input patterns**.

## Migration path

Use the [`query()` API](cc_sdk_typescript_query_function.md) and the session options it accepts:

- For multi-turn conversations, pass an `AsyncIterable<SDKUserMessage>` as the `prompt` (an input generator) rather than a session object — input and output both flow through the single `query()` async generator.
- To continue a saved session, set `options.resume` to the stored session ID instead of calling `unstable_v2_resumeSession()`.

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

const resumedQuery = query({
  prompt: "What number did I ask you to remember?",
  options: {
    model: "claude-opus-4-7",
    resume: sessionId
  }
});
```

**Source**: https://code.claude.com/docs/en/agent-sdk/typescript-v2-preview
**Last Updated**: 2026-06-13
**Status**: Active
