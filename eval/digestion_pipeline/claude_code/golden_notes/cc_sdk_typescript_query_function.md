---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - typescript
keywords:
  - query function
  - typescript agent sdk
  - async generator
  - sdkusermessage stream
  - startup pre-warm
  - warmquery handle
  - await using cleanup
  - query entry point
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/typescript
access_control_group: ["general"]
---

# Claude Agent SDK (TypeScript) — The `query()` Entry Point

## Overview

`query()` is the primary function for interacting with Claude Code from the TypeScript Agent SDK. You pass it a `prompt` plus an optional `Options` object, and it returns a `Query` object — an async generator that streams `SDKMessage` values as they arrive. Iterating the generator with `for await` is how a host application drives one agent run and observes every step the agent takes (the underlying gather-context / take-action / verify loop is documented at [how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)).

This note documents the `query()` signature and its two input/return shapes, plus the related latency-optimization pair `startup()` and the `WarmQuery` handle, which pay the subprocess spawn + initialize cost upfront so the first prompt resolves without that inline delay. The `Options` config object is documented in [cc_sdk_typescript_options.md](cc_sdk_typescript_options.md); the runtime-control methods on the returned `Query` object are in [cc_sdk_typescript_query_object.md](cc_sdk_typescript_query_object.md).

## `query()`

The primary function for interacting with Claude Code. Creates an async generator that streams messages as they arrive.

```typescript
function query({
  prompt,
  options
}: {
  prompt: string | AsyncIterable<SDKUserMessage>;
  options?: Options;
}): Query;
```

### Parameters

| Parameter | Type | Description |
| :-------- | :--- | :---------- |
| `prompt` | `string \| AsyncIterable<SDKUserMessage>` | The input prompt as a string or async iterable for streaming mode |
| `options` | `Options` | Optional configuration object (see Options type below) |

The `prompt` accepts two forms. A plain `string` is a single one-shot prompt. An `AsyncIterable<SDKUserMessage>` is **streaming input mode**: you feed user messages over time, which is what enables multi-turn conversations and the runtime-control methods that are streaming-input-only (`interrupt()`, `setPermissionMode()`, etc., per [cc_sdk_typescript_query_object.md](cc_sdk_typescript_query_object.md)).

### Returns

Returns a `Query` object that extends `AsyncGenerator<SDKMessage, void>` with additional methods. Consuming the stream is a `for await` loop; the `SDKMessage` discriminated union it yields is catalogued in [cc_sdk_typescript_message_and_hook_types.md](cc_sdk_typescript_message_and_hook_types.md).

## `startup()`

Pre-warms the CLI subprocess by spawning it and completing the initialize handshake **before a prompt is available**. The returned `WarmQuery` handle accepts a prompt later and writes it to an already-ready process, so the first `query()` call resolves without paying subprocess spawn and initialization cost inline.

```typescript
function startup(params?: {
  options?: Options;
  initializeTimeoutMs?: number;
}): Promise<WarmQuery>;
```

### Parameters

| Parameter | Type | Description |
| :-------- | :--- | :---------- |
| `options` | `Options` | Optional configuration object. Same as the `options` parameter to `query()` |
| `initializeTimeoutMs` | `number` | Maximum time in milliseconds to wait for subprocess initialization. Defaults to `60000`. If initialization does not complete in time, the promise rejects with a timeout error |

### Returns

Returns a `Promise<WarmQuery>` that resolves once the subprocess has spawned and completed its initialize handshake.

### Example

Call `startup()` early, for example on application boot, then call `.query()` on the returned handle once a prompt is ready. This moves subprocess spawn and initialization out of the critical path.

```typescript
import { startup } from "@anthropic-ai/claude-agent-sdk";

// Pay startup cost upfront
const warm = await startup({ options: { maxTurns: 3 } });

// Later, when a prompt is ready, this is immediate
for await (const message of warm.query("What files are here?")) {
  console.log(message);
}
```

## `WarmQuery`

Handle returned by `startup()`. The subprocess is already spawned and initialized, so calling `query()` on this handle writes the prompt directly to a ready process with no startup latency.

```typescript
interface WarmQuery extends AsyncDisposable {
  query(prompt: string | AsyncIterable<SDKUserMessage>): Query;
  close(): void;
}
```

### Methods

| Method | Description |
| :----- | :---------- |
| `query(prompt)` | Send a prompt to the pre-warmed subprocess and return a `Query`. Can only be called once per `WarmQuery` |
| `close()` | Close the subprocess without sending a prompt. Use this to discard a warm query that is no longer needed |

`WarmQuery` implements `AsyncDisposable`, so it can be used with `await using` for automatic cleanup. The same `prompt: string | AsyncIterable<SDKUserMessage>` accepted by `query()` is accepted by `WarmQuery.query()`; either form returns the same streaming `Query` object documented in [cc_sdk_typescript_query_object.md](cc_sdk_typescript_query_object.md).

**Source**: https://code.claude.com/docs/en/agent-sdk/typescript
**Last Updated**: 2026-06-13
**Status**: Active
