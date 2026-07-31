---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - session_storage
keywords:
  - session store adapter
  - inmemorysessionstore quick start
  - append and load
  - sessionstoreentry
  - reference adapters s3 redis postgres
  - run_session_store_conformance
  - deep-equal load
  - external session storage
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/session-storage
access_control_group: ["general"]
---

# Build and Use a Session Store Adapter

## Overview

This note is the build-and-use procedure for a Claude Code SDK `SessionStore` — the adapter that mirrors session transcripts to an external backend (S3, Redis, a database) so a session created on one host can resume on another. The interface, dual-write semantics, and behavior contract are covered in the sibling concept note [cc_sdk_session_store](cc_sdk_session_store.md); here the focus is the hands-on steps: attach the shipped in-memory store for a quick start, implement your own `append`/`load`, copy a reference adapter, and run the conformance suite to validate it.

The procedure has four steps in escalating effort: (1) prove the wiring with `InMemorySessionStore`, (2) write your own adapter against your backend, (3) copy a runnable S3/Redis/Postgres reference implementation instead of writing from scratch, and (4) validate any adapter against the shipped conformance suite.

## Step 1 — Quick start with `InMemorySessionStore`

The SDK ships an `InMemorySessionStore` for development and testing. Run a query with the store attached, capture the session ID from the result message, then resume from the store in a second `query()` call. The second call passes the same store instance plus `resume`, so the SDK loads the transcript from the store instead of the local filesystem.

```python Python theme={null}
import asyncio
from claude_agent_sdk import (
    ClaudeAgentOptions,
    InMemorySessionStore,
    ResultMessage,
    query,
)

store = InMemorySessionStore()


async def main():
    session_id = None
    async for message in query(
        prompt="List the Python files under src/",
        options=ClaudeAgentOptions(session_store=store),
    ):
        if isinstance(message, ResultMessage):
            session_id = message.session_id

    # Resume from the store. The agent has full context from the first call.
    async for message in query(
        prompt="Summarize what those files do",
        options=ClaudeAgentOptions(session_store=store, resume=session_id),
    ):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

The TypeScript form is identical in shape: import `query` and `InMemorySessionStore` from `@anthropic-ai/claude-agent-sdk`, pass `options: { sessionStore: store }` on the first `query()`, read `message.session_id` from the `result` message, then pass `options: { sessionStore: store, resume: sessionId }` on the second. The second query prints a summary of the files from the first query, which shows the agent resumed with full context from the store.

## Step 2 — Write your own adapter

Implement `append` and `load` against your backend. Add `listSessions`, `delete`, and `listSubkeys` if you want `listSessions()`, `deleteSession()`, and subagent resume to work against the store.

Entries passed to `append` are typed as `SessionStoreEntry` (a `{ type: string; ... }` object). Treat them as **opaque JSON-safe values**: persist them in order and return them from `load` in the same order. `load` must return entries that are **deep-equal** to what was appended — byte-equal serialization is not required, so backends like Postgres `jsonb` that reorder object keys are fine.

## Step 3 — Copy a reference implementation

The TypeScript SDK repository includes runnable reference adapters for S3, Redis, and Postgres under [`examples/session-stores/`](https://github.com/anthropics/claude-agent-sdk-typescript/tree/main/examples/session-stores). They are **not published to npm**; copy the `src/` file you need into your project and install the corresponding backend client.

| Adapter | Backend client | Storage model |
| :--- | :--- | :--- |
| `S3SessionStore` | `@aws-sdk/client-s3` | One JSONL part file per `append()`; `load()` lists, sorts, and concatenates. |
| `RedisSessionStore` | `ioredis` | `RPUSH`/`LRANGE` list per transcript, plus a sorted-set session index. |
| `PostgresSessionStore` | `pg` | One row per entry in a `jsonb` table, ordered by `BIGSERIAL`. |

Each adapter takes a **pre-configured client instance**, so you control credentials, TLS, region, and pooling. For example, with S3:

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";
import { S3Client } from "@aws-sdk/client-s3";
import { S3SessionStore } from "./S3SessionStore"; // copied from examples/session-stores/s3

const store = new S3SessionStore({
  bucket: "my-claude-sessions",
  prefix: "transcripts",
  client: new S3Client({ region: "us-east-1" }),
});

for await (const message of query({
  prompt: "Hello!",
  options: { sessionStore: store },
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}

// Later, possibly on a different host:
for await (const message of query({
  prompt: "Continue where we left off",
  options: { sessionStore: store, resume: "previous-session-id" },
})) {
  // ...
}
```

## Step 4 — Validate your adapter (conformance)

Both SDKs ship a **conformance suite** that asserts the behavioral contract `append`, `load`, and the optional methods must satisfy. Tests for optional methods skip automatically when those methods are not implemented.

In TypeScript, copy [`shared/conformance.ts`](https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/examples/session-stores/shared/conformance.ts) from the example directory into your test suite. In Python, the suite ships in the package:

```python Python theme={null}
import pytest
from claude_agent_sdk.testing import run_session_store_conformance


@pytest.mark.asyncio
async def test_my_store_conformance():
    await run_session_store_conformance(MyRedisStore)
```

**Source**: https://code.claude.com/docs/en/agent-sdk/session-storage
**Last Updated**: 2026-06-13
**Status**: Active
