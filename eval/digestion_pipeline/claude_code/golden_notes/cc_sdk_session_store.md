---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - session_storage
keywords:
  - sessionstore interface
  - mirror adapter
  - dual-write architecture
  - append and load
  - sessionkey
  - mirror_error
  - post-compaction chain
  - subagent subpath
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/session-storage
access_control_group: ["general"]
---

# Claude Code Agent SDK — The SessionStore Interface

## Overview

By default the Agent SDK writes session transcripts to JSONL files under `~/.claude/projects/` on the local filesystem. A **`SessionStore`** adapter lets you *mirror* those transcripts to your own backend — S3, Redis, or a database — so a session created on one host can be resumed on another. Common reasons to use one: **multi-host deployments** (serverless functions, autoscaled workers, and CI runners do not share a filesystem, so a shared store lets any replica resume any session), **durability** (local containers are ephemeral; an S3- or database-backed store survives restarts and redeploys), and **compliance and audit** (keep transcripts in storage you already govern, with your own retention rules, encryption, and access controls).

This note documents the *contract and behavior* of a `SessionStore` — its required and optional methods, the `SessionKey` addressing model, the dual-write semantics, and the SDK functions that accept one. For the build-an-adapter procedure (quick start, writing your own adapter, the reference S3/Redis/Postgres implementations, and the conformance suite), see the sibling note [Build a SessionStore Adapter](cc_sdk_session_store_setup.md).

## The `SessionStore` interface

A `SessionStore` is an object with two **required** methods, `append` and `load`, and three **optional** methods. The SDK calls `append` to write transcript entries during a query and `load` to read them back for resume.

```typescript TypeScript theme={null}
// Exported from @anthropic-ai/claude-agent-sdk as
// SessionStore, SessionKey, SessionStoreEntry.

type SessionKey = {
  projectKey: string;
  sessionId: string;
  subpath?: string;
};

type SessionStore = {
  // Required
  append(key: SessionKey, entries: SessionStoreEntry[]): Promise<void>;
  load(key: SessionKey): Promise<SessionStoreEntry[] | null>;

  // Optional
  listSessions?(
    projectKey: string,
  ): Promise<Array<{ sessionId: string; mtime: number }>>;
  delete?(key: SessionKey): Promise<void>;
  listSubkeys?(key: {
    projectKey: string;
    sessionId: string;
  }): Promise<string[]>;
};
```

```python Python theme={null}
# Exported from claude_agent_sdk as
# SessionStore, SessionKey, SessionStoreEntry.

class SessionKey(TypedDict):
    project_key: str
    session_id: str
    subpath: NotRequired[str]

class SessionStore(Protocol):
    # Required
    async def append(
        self, key: SessionKey, entries: list[SessionStoreEntry]
    ) -> None: ...
    async def load(self, key: SessionKey) -> list[SessionStoreEntry] | None: ...

    # Optional — omit or raise NotImplementedError
    async def list_sessions(
        self, project_key: str
    ) -> list[SessionStoreListEntry]: ...
    async def delete(self, key: SessionKey) -> None: ...
    async def list_subkeys(self, key: SessionListSubkeysKey) -> list[str]: ...
```

`SessionKey` addresses **one transcript**. `projectKey` is a stable, filesystem-safe encoding of the working directory; `sessionId` is the session UUID; and `subpath` is set when the entry belongs to a subagent transcript or sidecar file rather than the main conversation. Treat `subpath` as an opaque key suffix — it follows the on-disk layout, for example `subagents/agent-<id>`. When `subpath` is undefined the key refers to the main transcript.

The five methods and when the SDK calls each:

| Method | Required | Called when |
| :--- | :--- | :--- |
| `append` | Yes | After each batch of transcript entries is written locally. Entries are JSON-safe objects, one per line in the local JSONL. |
| `load` | Yes | Once before the subprocess spawns, when `resume` is set. Return `null` if the session is unknown. |
| `listSessions` | No | By `listSessions({ sessionStore })` and by `query()`/`startup()` with `continue: true`. If undefined, those calls throw. |
| `delete` | No | By `deleteSession({ sessionStore })`. Deleting the main key (no `subpath`) must cascade to all subkeys for that session. If undefined, deletion is a no-op, which suits append-only backends. |
| `listSubkeys` | No | During resume, to discover subagent transcripts. If undefined, only the main transcript is restored. |

## Behavior notes

### Dual-write architecture

The store is a **mirror, not a replacement**. The Claude Code subprocess always writes to local disk first; the SDK then forwards each batch to `append()`. If you want the local copy to be ephemeral, point `CLAUDE_CONFIG_DIR` at a temp directory in `options.env`. Because the mirror depends on local writes, `sessionStore` **cannot be combined with `persistSession: false`** — the SDK throws if you set both. It also throws if combined with `enableFileCheckpointing`, since file-history backup blobs are written directly to local disk and are not mirrored to the store.

### Mirror writes are best-effort

If `append()` rejects or times out, the error is logged, a `{ type: "system", subtype: "mirror_error" }` message is emitted into the iterator, and the query continues. The local transcript is already durable on disk, so a store outage does not interrupt the agent or lose data locally. Batches that fail are **not retried**, so monitor for `mirror_error` if you need to detect store data loss.

### `getSessionMessages` returns the post-compaction chain

`getSessionMessages({ sessionStore })` returns the linked message chain the agent would see on resume. After auto-compaction, earlier turns are replaced by a summary, so a session whose store holds 503 raw entries may return 18 messages from `getSessionMessages`. For the full raw history, including pre-compaction turns and metadata entries, call `store.load(key)` directly.

### `forkSession` is not a byte copy

`forkSession({ sessionStore })` reads the source entries, rewrites every `sessionId` field and remaps message UUIDs, then appends the transformed entries under a new key. An adapter-level copy or `CopyObject` shortcut would produce a transcript that still references the old session ID, so the SDK does not use one.

### Subagent transcripts

Subagent transcripts are mirrored under `subpath: "subagents/agent-<id>"`. `listSubagents({ sessionStore })` requires the adapter to implement `listSubkeys`; `getSubagentMessages({ sessionStore })` uses it when available but falls back to the direct subpath when it is undefined. Resume also calls `listSubkeys` to restore subagent files — without it, only the main transcript is materialized.

### Retention

The SDK **never deletes from your store on its own**. Retention is the adapter's responsibility: implement TTLs, S3 lifecycle policies, or scheduled cleanup according to your compliance requirements. Local transcripts under `CLAUDE_CONFIG_DIR` are swept independently by the `cleanupPeriodDays` setting (see [SDK environment variables / settings](https://code.claude.com/docs/en/settings)).

## Supported on

The following SDK functions accept a `sessionStore` option and operate against the store instead of the local filesystem when it is provided: `query()`, `startup()`, `listSessions()`, `getSessionInfo()`, `getSessionMessages()`, `renameSession()`, `tagSession()`, `deleteSession()`, `forkSession()`, `listSubagents()`, and `getSubagentMessages()`. (See the [TypeScript `Options` reference](https://code.claude.com/docs/en/agent-sdk/typescript) for the full option set.)

**Source**: https://code.claude.com/docs/en/agent-sdk/session-storage
**Last Updated**: 2026-06-13
**Status**: Active
