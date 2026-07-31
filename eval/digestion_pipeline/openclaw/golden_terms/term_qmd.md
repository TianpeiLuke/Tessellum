---
tags:
  - resource
  - terminology
  - openclaw
  - qmd
  - memory-query
  - query-cli
  - subprocess-bridge
keywords:
  - QMD
  - qmd query
  - qmd binary
  - memory-search subprocess
  - per-collection scope
  - parseQmdQueryJson
topics:
  - Query languages
  - Memory search
  - OpenClaw memory architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://docs.openclaw.ai/concepts/memory-qmd
access_control_group: ["general"]
---

# QMD — Query Memory Driver

## Definition

**QMD** is OpenClaw's memory-search subsystem implemented as an external **CLI binary** that the host process spawns on demand to answer "what does this agent remember about X?" The OpenClaw repo references it inconsistently — `qmd-scope.ts` glosses it as *queryable memory dictionary* and the plan tracker as *Query Markdown DSL* — but in practice QMD is a typed query CLI (`qmd query --json`) that combines BM25 full-text search, vector semantic search, and an LLM-rerank stage over a local SQLite-FTS5 index built from the agent's memory files. The OpenClaw memory host treats this binary as a fallible dependency: it resolves a platform-correct spawn invocation, runs a bounded availability probe, captures bounded stdout/stderr, parses the JSON result envelope, and gates per-collection access through a session-scope matcher.

QMD is **not** Quarto Markdown (the `.qmd` document format from Posit). The names collide because both involve markdown; the concepts are unrelated. OpenClaw's QMD is an internal subprocess search binary (the upstream open-source implementation is `tobi/qmd` — a local-first BM25 + vector + rerank engine), not a document-authoring format. Any reference to "QMD" inside the OpenClaw codebase means the search binary.

## Context

QMD sits between the OpenClaw agent runtime and the per-agent memory store (markdown files and a derived SQLite-FTS5 index under `~/.openclaw/agents/<agentId>/qmd/`). When an ACP-spawned agent asks "search my memory for X," the request flows: agent → memory-host-sdk → `runCliCommand("qmd query --json ...")` → JSON parse → typed `QmdQueryResult[]` → ranked context for the next LLM turn. OpenClaw externalized this to a CLI binary (rather than linking the search engine in-process) so the engine can ship its own native dependencies (node-llama-cpp embeddings, SQLite-with-extensions), be replaced wholesale (`memory.qmd.searchMode` is configurable), and benefit from OS-level isolation — a crashing or hung QMD process never takes down the host. The trade-off is every search costs one fork/exec plus an availability probe; the host caches the probe result and re-uses one QMD invocation per turn.

Per-collection scope rules (`qmd-scope.ts`) gate which memory dictionaries a session may search, keyed off the session envelope (`agent:<id>:<channel>:<chatType>:<rest>`). A rule list is a first-match-wins conjunction over `channel`, `chatType`, `keyPrefix`, and `rawKeyPrefix` matchers; empty rules fall through to `scope.default ?? "allow"`. The `subagent:` sentinel returns `undefined`, so subagent-spawned sessions inherit only the default scope — a deliberate sandbox.

## Key Characteristics

- **Bundled external binary**: `qmd` is shipped separately (e.g., `bun install -g tobi/qmd`) and must be on `PATH`; OpenClaw does not vendor the engine, only the adapter.
- **Cross-platform spawn shim**: Windows requires `cmd.exe /c` indirection for npm-installed `.cmd` shims; `resolveCliSpawnInvocation` isolates the platform branch so business logic doesn't sniff `process.platform`.
- **Spawn-event availability probe**: the host answers "is QMD launchable?" by listening for the `spawn` event (not `close`/exit-code), then killing the child; pairs with a 2-second timeout for unresponsive filesystems.
- **Bounded stdout/stderr capture**: `runCliCommand` keeps a sliding-window tail of `maxOutputChars`, sets a `truncated` flag, and refuses to OOM on a runaway child.
- **SIGKILL escalation on timeout**: graceful `SIGTERM` is skipped — buggy or hung children get `SIGKILL` immediately so the host's deadline is the wall-clock truth.
- **JSON result envelope**: `QmdQueryResult { docid, score, collection, file, snippet, body, startLine, endLine }`, parsed by `parseQmdQueryJson(stdout, stderr)` with per-field type guards.
- **No-results sentinel**: an empty result is a sentinel line on stdout *or* stderr (with or without `[ts] level:` prefix), distinct from a malformed response — the former returns `[]`, the latter throws with stderr summary.
- **Direct-then-noisy JSON recovery**: parser first tries `JSON.parse(stdout.trim())`; if that fails, falls back to a depth-counting scan that extracts the first balanced `[...]` array surrounded by log noise.
- **Per-collection scope gate**: `isQmdScopeAllowed(rules, parsedKey)` enforces conjunctive matchers (channel, chatType, key-prefix) before the query reaches the binary; subagents fall through to the safe default.
- **Hybrid search internals**: under the hood the binary runs BM25 (SQLite FTS5) and vector retrieval in parallel, fuses via Reciprocal Rank Fusion, and applies LLM rerank — the host only sees the JSON envelope, not the internal stages.

## Related Terms

- **Dreaming (memory consolidation)** *(planned: term_memory_dreaming.md)*: background memory consolidation cycles whose outputs feed the QMD index.
- **Model Failover** *(planned: term_model_failover.md)*: 3-way failover ladder; the rerank LLM call inside QMD uses this for transient errors.

## Related Code Snippets

- **[OpenClaw Memory Host — qmd-process.ts](../code_snippets/snippet_openclaw_memory_host_qmd_process.md)**: subprocess spawn, Windows shim, spawn-event availability probe, bounded output capture, SIGKILL timeout escalation.
- **[OpenClaw Memory Host — qmd-query-parser.ts](../code_snippets/snippet_openclaw_memory_host_qmd_query_parser.md)**: `parseQmdQueryJson`, no-results sentinel detection, direct-then-noisy JSON recovery, per-field type guards.
- **[OpenClaw Memory Host — qmd-scope.ts](../code_snippets/snippet_openclaw_memory_host_qmd_scope.md)**: `isQmdScopeAllowed` first-match-wins channel/chat-type rule matcher and the `subagent:` sentinel default-scope fallback.

## Related Analysis (FZ 15)


## References

- [QMD Memory Engine — OpenClaw Docs](https://docs.openclaw.ai/concepts/memory-qmd) — official documentation for the QMD memory backend, search modes, and configuration.
- [tobi/qmd — Local CLI Search Engine](https://github.com/tobi/qmd) — upstream open-source binary OpenClaw integrates with; BM25 + vector + LLM-rerank over a local SQLite FTS5 index.
- [openclaw/openclaw — qmd-process.ts](https://github.com/openclaw/openclaw/blob/main/packages/memory-host-sdk/src/host/qmd-process.ts) — OpenClaw's subprocess adapter for the QMD binary.
- [Datalog — Wikipedia](https://en.wikipedia.org/wiki/Datalog) — analogous embedded declarative query DSL; like QMD's CLI, Datalog implementations are commonly embedded into larger systems with a typed result envelope.
- [jq (programming language) — Wikipedia](https://en.wikipedia.org/wiki/Jq_(programming_language)) — analogous CLI-as-DSL pattern; jq is a functional DSL invoked as a subprocess with JSON I/O, the same integration shape QMD exposes via `qmd query --json`.
- [Domain-specific language — Wikipedia](https://en.wikipedia.org/wiki/Domain-specific_language) — context for the embedded-query-DSL pattern QMD belongs to.
