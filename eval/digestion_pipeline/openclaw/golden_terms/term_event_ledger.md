---
tags:
  - resource
  - terminology
  - event-ledger
  - event-sourcing
  - append-only-log
  - durability
  - openclaw
  - acp
keywords:
  - Event Ledger
  - ACP event ledger
  - per-session event log
  - append-only log
  - event sourcing
  - session replay
  - file-lock retry
  - atomic write
  - structured clone
  - normalize-on-read
topics:
  - OpenClaw ACP runtime
  - Session replay and crash recovery
  - Event-sourcing patterns
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: null
access_control_group: ["general"]
---

# Event Ledger

## Definition

An **Event Ledger** is a per-session, append-only log of agent-client-protocol ([ACP](term_acp_agent_client_protocol.md)) `SessionUpdate` events with a versioned JSON envelope, per-session monotonic `seq` counter, three-stage trim policy, and a retrying file-lock + atomic-write durability frame — OpenClaw's substrate for crash-safe session replay. The on-disk shape is `{version: 1, sessions: {sessionId -> LedgerSession}}`, where each `LedgerSession` carries a monotonic `nextSeq`, an ordered `events` array of `AcpEventLedgerEntry` records, and a `complete` boolean that becomes `false` whenever trim policy truncates the head of the session — the load-bearing signal that lets a replay consumer detect a non-prefix-from-seq-1 transcript and refuse to serve it as canonical.

The ledger is a concrete instance of the **event-sourcing pattern**: state is reconstructed by replaying an append-only sequence of events, not by reading a mutable snapshot ([Microsoft event-sourcing pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing); [AWS prescriptive guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html)). Compared to Kafka topics ([Confluent Kafka introduction](https://docs.confluent.io/kafka/introduction.html)) and EventStoreDB / Kurrent ([Kurrent EventStoreDB](https://www.kurrent.io/eventstoredb)), the ACP event ledger is a single-process, single-file log scoped to a desktop-agent runtime rather than a clustered distributed log — it borrows the same immutability + replay semantics, but trades cross-broker replication for atomic-rename durability and a file-lock retry policy. The durability frame (write-to-temp + rename under a retrying lock) is the userspace analog of database **write-ahead logging** ([Wikipedia WAL](https://en.wikipedia.org/wiki/Write-ahead_logging)) — both serialize mutations to disk before they become "real," and both rely on a normalize-on-read step to tolerate partial or future-version files.

## Context

In OpenClaw, the event ledger is owned by `src/acp/event-ledger.ts` and consumed by the ACP translator (`src/acp/translator/`). Three callers write to it: the prompt handler invokes `recordUserPrompt` when a user message arrives, the dispatch loop invokes `recordUpdate` for each emitted `SessionUpdate`, and the approval relay's exec-permission state machine invokes `recordUpdate` for `exec.approval` envelope events. Three call sites read it: ACP session-resume reads by `sessionId`, replay-by-key reads by the stable `sessionKey` (used when the agent process restarts and `sessionId` is regenerated), and the rate-limit path uses replay to reconstruct context after a transient failover.

Two factories ship the same `AcpEventLedger` interface: `createInMemoryAcpEventLedger` (volatile; used in tests and ephemeral runs) and `createFileAcpEventLedger` (durable; wraps every mutation in `withFileLock` + `writeTextAtomic`). Both share a single `createLedgerApi` factory — the variant difference is only the injected `mutate` / `read` strategies, so seq assignment, clone discipline, trim policy, and replay semantics are identical across the two. The file variant defaults to `mode: 0o600` (owner-only) on the ledger file and `0o700` on its parent directory because the events may carry user prompts, which are user-private data.

Outside OpenClaw, the closest direct analog is the ACP protocol's own session-replay semantics ([Agent Client Protocol docs](https://agentclientprotocol.com/)) — ACP defines that on session load, prior messages stream back, and the event ledger is OpenClaw's implementation of "where do those messages live between sessions."

## Key Characteristics

- **Version-tagged JSON envelope with normalize-on-read tolerance** — `LEDGER_VERSION = 1` is stamped on every persisted store; `normalizeStore` returns an empty store on any version mismatch, missing field, or shape error rather than throwing, so a downgrade reading a future-version file resets-and-resumes instead of crash-looping. Each entry validates every field type independently — one bad event drops that event, not the whole session; a session whose key disagrees with its `sessionId` field is dropped, not the whole store.
- **Per-session monotonic seq counter** — every event carries a `seq` assigned from the per-session `nextSeq` BEFORE the increment, so the first event in a session is always `seq=1` (not `seq=2`) and replays return events in append order. `nextSeq` is session-scoped — two concurrent sessions can carry seq=1 simultaneously; the combined replay key is `(sessionId, seq)`.
- **Three-stage trim policy** — `trimLedger` runs after every mutation and applies bounds in fixed order: (1) cap per-session events at `maxEventsPerSession=5000` by slicing the OLDEST off, (2) LRU-evict whole sessions when `maxSessions=200` is exceeded (sorting by `updatedAt`), (3) serialize-and-drop oldest events until under `maxSerializedBytes=16 MiB`, with a safety-valve second phase that drops whole sessions if the bytes cap is still breached.
- **Mark-incomplete on truncation** — any session whose events are truncated by stage 1 or stage 3 has `complete` flipped to `false`. Replay methods gate on `session.complete`, so a truncated session is invisible to canonical replay — the consumer sees `{complete: false, events: []}` and knows not to trust a stale prefix.
- **Retrying file-lock + atomic-write durability frame** — `withFileLock` uses 8 retries with exponential backoff (factor 2, 50ms-5000ms, randomized jitter, 15s stale-lock timeout); `writeTextAtomic` writes to a temp file then renames, with `mode: 0o600` and `dirMode: 0o700`. Reads also acquire the lock so a concurrent writer's pre-rename state is never exposed.
- **Structured-clone-on-write and structured-clone-on-read** — `appendUpdate` calls `structuredClone` on the incoming `update` so the caller's object cannot be mutated post-write to corrupt the stored event; `buildReplay` clones each event on the way out so the returned array cannot be mutated to corrupt the in-memory store. `structuredClone` is preferred over JSON round-trip because it preserves typed-array, `Date`, `Map`, and `Set` payloads.
- **Replay-on-reload semantics with three lookup modes** — `readReplay(sessionId, sessionKey)` requires both to match (strict resume), `readReplayBySessionId(sessionId)` is sessionId-only (after process restart with same id), `readReplayBySessionKey(sessionKey)` picks the MOST RECENT complete session sharing the key (after sessionId regeneration on agent reconnect). All three gate on `complete=true`.
- **Strategy injection for in-memory vs file variants** — one `createLedgerApi` factory backs both variants; the in-memory variant injects `mutate: fn => fn()` / `read: fn => fn()` no-ops, the file variant injects the lock-load-fn-write strategy. Same business logic, two durability frames.

## Related Terms


### Related Code Snippets

- **[OpenClaw ACP Event Ledger (#616)](../code_snippets/snippet_openclaw_acp_event_ledger.md)**: the 485-LOC source — lifts the five model patterns (version-tagged envelope, monotonic seq with clone discipline, three-stage trim, retrying file-lock + atomic write, strategy injection for in-memory/file variants).
## References

- [Write-ahead logging (Wikipedia)](https://en.wikipedia.org/wiki/Write-ahead_logging) — Class-1 source; the database technique the file ledger's durability frame instantiates in userspace (write-to-temp + rename under a lock is the userspace analog of log-before-data-page-flush).
- [Event Sourcing pattern (Microsoft Azure Architecture Center)](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) — Class-2 source; defines the append-only event store as the authoritative source of truth with state reconstructed by replay, exactly the contract the per-session ledger implements.
- [Event sourcing pattern (AWS Prescriptive Guidance)](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html) — Class-2 source; AWS framing of the same pattern with the immutability invariant and replay-derives-state principle.
- [Apache Kafka introduction (Confluent)](https://docs.confluent.io/kafka/introduction.html) — Class-2 source; the canonical clustered append-only log; contrasts with the ACP event ledger's single-file scope and atomic-rename durability vs Kafka's replicated-broker durability.
- [EventStoreDB / Kurrent](https://www.kurrent.io/eventstoredb) — Class-2 source; an event-native database where events are stored in an immutable append-only log in sequential order — the database-class analog of the ACP event ledger's per-session log.
- [Agent Client Protocol — Introduction](https://agentclientprotocol.com/) — Class-2 source; defines the ACP session-replay contract ("on load, all previous messages stream back") that this ledger implements on the OpenClaw side.
- [OpenClaw `src/acp/event-ledger.ts`](https://github.com/openclaw/openclaw/blob/main/src/acp/event-ledger.ts) — the upstream implementation this term documents.
