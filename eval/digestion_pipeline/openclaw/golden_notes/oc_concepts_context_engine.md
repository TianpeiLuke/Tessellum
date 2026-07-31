---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - context_engine
keywords:
  - openclaw context engine
  - contextengine interface
  - registercontextengine
  - plugins slots contextengine
  - ownscompaction
  - assembleresult promptauthority
  - legacy context engine
  - context engine failure isolation
topics:
  - OpenClaw
  - Context Engine
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/concepts/context-engine
access_control_group: ["general"]
---

# OpenClaw — The Pluggable Context Engine

## Overview

This note models OpenClaw's **context engine**: the pluggable subsystem that controls how OpenClaw builds model context for each run — which messages to include, how to summarize older history, and how to manage context across subagent boundaries. It mirrors the `concepts/context-engine` source page: the four-point lifecycle (ingest / assemble / compact / after-turn), the optional subagent hooks, the built-in `legacy` engine, plugin-engine registration, the `ContextEngine` interface (`AssembleResult`, `promptAuthority`), `runtimeSettings`, host requirements, failure isolation, `ownsCompaction` semantics, the selection slot, and the relationship to compaction and memory.

OpenClaw ships with the `legacy` engine and uses it by default — most users never need to change this. Installing and selecting a plugin engine is reserved for when you want different assembly, compaction, or cross-session recall behavior.

## Quick start

`openclaw doctor` reports the active engine, or inspect config with `cat ~/.openclaw/openclaw.json | jq '.plugins.slots.contextEngine'`. Context engine plugins install like any other OpenClaw plugin — `openclaw plugins install @martian-engineering/lossless-claw` (from npm) or `openclaw plugins install -l ./my-context-engine` (from a local path). Enable and select the engine in `openclaw.json`, then restart the gateway:

```json5
// openclaw.json
{
  plugins: {
    slots: {
      contextEngine: "lossless-claw", // must match the plugin's registered engine id
    },
    entries: {
      "lossless-claw": {
        enabled: true,
        // Plugin-specific config goes here (see the plugin's docs)
      },
    },
  },
}
```

To switch back, set `contextEngine` to `"legacy"` (or remove the key entirely — `"legacy"` is the default).

## How it works — the four lifecycle points

Every time OpenClaw runs a model prompt, the context engine participates at four lifecycle points. **1. Ingest** — when a new message is added to the session; the engine can store or index it in its own data store. **2. Assemble** — before each model run; the engine returns an ordered set of messages (and an optional `systemPromptAddition`) that fit within the token budget. **3. Compact** — when the context window is full or the user runs `/compact`; the engine summarizes older history to free space. **4. After turn** — after a run completes; the engine can persist state, trigger background compaction, or update indexes.

For the bundled non-ACP Codex harness, OpenClaw applies the same lifecycle by projecting assembled context into Codex developer instructions and the current turn prompt; Codex still owns its native thread history and compactor.

### Subagent lifecycle (optional)

OpenClaw calls two optional subagent lifecycle hooks. `prepareSubagentSpawn` prepares shared context state before a child run starts: it receives parent/child session keys, `contextMode` (`isolated` or `fork`), available transcript ids/files, and optional TTL; a returned rollback handle is called when spawn fails after preparation succeeds. Native subagent spawns that request `lightContext` and resolve to `contextMode="isolated"` intentionally skip this hook so the child starts from the lightweight bootstrap context without engine-managed pre-spawn state. `onSubagentEnded` cleans up when a subagent session completes or is swept.

### System prompt addition

The `assemble` method can return a `systemPromptAddition` string, which OpenClaw prepends to the system prompt for the run. This lets engines inject dynamic recall guidance, retrieval instructions, or context-aware hints without static workspace files.

## The legacy engine

The built-in `legacy` engine preserves OpenClaw's original behavior: **Ingest** is a no-op (the session manager persists messages directly); **Assemble** is pass-through (the runtime's existing sanitize → validate → limit pipeline handles assembly); **Compact** delegates to built-in summarization, creating a single summary of older messages and keeping recent ones intact; **After turn** is a no-op. The legacy engine registers no tools and provides no `systemPromptAddition`. When no `plugins.slots.contextEngine` is set (or it's `"legacy"`), this engine is used automatically.

## Plugin engines

A plugin registers a context engine via the plugin API. The factory passed to `api.registerContextEngine(id, factory)` returns an object with `info` plus the lifecycle methods:

```ts
import { buildMemorySystemPromptAddition } from "openclaw/plugin-sdk/core";

export default function register(api) {
  api.registerContextEngine("my-engine", (ctx) => ({
    info: {
      id: "my-engine",
      name: "My Context Engine",
      ownsCompaction: true,
    },

    async ingest({ sessionId, message, isHeartbeat }) {
      // Store the message in your data store
      return { ingested: true };
    },

    async assemble({ sessionId, messages, tokenBudget, availableTools, citationsMode }) {
      // Return messages that fit the budget
      return {
        messages: buildContext(messages, tokenBudget),
        estimatedTokens: countTokens(messages),
        systemPromptAddition: buildMemorySystemPromptAddition({
          availableTools: availableTools ?? new Set(),
          citationsMode,
        }),
      };
    },

    async compact({ sessionId, force }) {
      // Summarize older context
      return { ok: true, compacted: true };
    },
  }));
}
```

The factory `ctx` includes optional `config`, `agentDir`, and `workspaceDir` values so plugins can initialize per-agent or per-workspace state before the first lifecycle hook runs. The engine is enabled by setting `contextEngine: "my-engine"` under `plugins.slots` and `enabled: true` under the matching `plugins.entries` key.

### The ContextEngine interface

The interface defines four **required members**: `info` (property) carries the engine id, name, version, and whether it owns compaction; `ingest(params)` (method) stores a single message; `assemble(params)` (method) builds context for a model run (returning an `AssembleResult`); `compact(params)` (method) summarizes/reduces context.

`assemble` returns an `AssembleResult` with these fields: `messages` (`Message[]`, required) — the ordered messages to send to the model; `estimatedTokens` (`number`, required) — the engine's estimate of total tokens, used for compaction threshold decisions and diagnostic reporting; `systemPromptAddition` (`string`) — prepended to the system prompt; and `promptAuthority` (`"assembled" | "preassembly_may_overflow"`) — controls which token estimate the runner uses for preemptive overflow prechecks. `promptAuthority` defaults to `"assembled"` (only the assembled prompt's estimate is checked — appropriate for engines returning a windowed, self-contained context); set it to `"preassembly_may_overflow"` only when your assembled view can hide overflow risk in the underlying transcript, in which case the runner takes the maximum of the assembled estimate and the pre-assembly (unwindowed) session-history estimate when deciding whether to preemptively compact. Either way, the messages you return are still what the model sees, so `promptAuthority` only affects the precheck. `compact` returns a `CompactResult`; when compaction rotates the active transcript, `result.sessionId` and `result.sessionFile` identify the successor session the next retry or turn must use.

The interface also defines six **optional members**: `bootstrap(params)` initializes engine state once when the engine first sees a session (e.g., import history); `ingestBatch(params)` ingests a completed turn as a batch after a run completes; `afterTurn(params)` does post-run work (persist state, trigger background compaction); `prepareSubagentSpawn(params)` sets up shared state for a child session before it starts; `onSubagentEnded(params)` cleans up after a subagent ends; and `dispose()` releases resources during gateway shutdown or plugin reload — not per-session.

### Runtime settings

Lifecycle hooks that run inside OpenClaw receive an optional `runtimeSettings` object — a versioned, read-only internal producer/consumer API surface OpenClaw produces for the selected engine and the engine consumes inside lifecycle hooks; it is not rendered to users and does not create a dedicated reporting surface. Its fields are `schemaVersion` (currently `1`), `runtime` (OpenClaw host, runtime mode `normal`/`fallback`/`degraded`, and optional harness/runtime ids), `contextEngineSelection` (selected engine id and selection source), `executionHost` (host id and label for the surface invoking the hook), `model` (requested model, resolved model, provider, and optional model family), `limits` (prompt token budget and max output tokens when known), and `diagnostics` (closed fallback and degraded reason codes when known). Fields that can be unknown are `null`; discriminator fields such as runtime mode and selection source remain non-nullable. Older engines remain compatible: if a strict legacy engine rejects `runtimeSettings` as an unknown property, OpenClaw retries the lifecycle call without it instead of quarantining the engine.

### Host requirements

Context engines can declare host capability requirements on `info.hostRequirements`. OpenClaw checks these before starting the operation and fails closed with a descriptive error when the runtime cannot satisfy them. For agent runs, declare `assemble-before-prompt` when the engine must control the actual model prompt through `assemble()`:

```ts
info: {
  id: "my-context-engine",
  name: "My Context Engine",
  hostRequirements: {
    "agent-run": {
      requiredCapabilities: ["assemble-before-prompt"],
      unsupportedMessage:
        "Use the native Codex or OpenClaw embedded runtime, or select the legacy context engine.",
    },
  },
}
```

Native Codex and OpenClaw embedded agent runs satisfy `assemble-before-prompt`; generic CLI backends do not, so engines requiring it are rejected before the CLI process starts.

### Failure isolation

OpenClaw isolates the selected plugin engine from the core reply path. If a non-legacy engine is missing, fails contract validation, throws during factory creation, or throws from a lifecycle method, OpenClaw quarantines that engine for the current Gateway process and downgrades context-engine work to the built-in `legacy` engine. The error is logged with the failed operation so the operator can repair, update, or disable the plugin without the agent going silent. Host requirement failures differ: when an engine declares a runtime lacks a required capability, OpenClaw fails closed before starting the run — protecting engines that would corrupt state in an unsupported host.

### ownsCompaction

`ownsCompaction` controls whether OpenClaw runtime's built-in in-attempt auto-compaction stays enabled for the run. With **`ownsCompaction: true`**, the engine owns compaction: OpenClaw disables its built-in auto-compaction for that run, and the engine's `compact()` is responsible for `/compact`, overflow recovery compaction, and any proactive compaction in `afterTurn()` — though OpenClaw may still run the pre-prompt overflow safeguard, and when it predicts the full transcript will overflow, the recovery path calls the active engine's `compact()` before submitting another prompt. With **`ownsCompaction: false` or unset**, OpenClaw's built-in auto-compaction may still run during prompt execution, but the active engine's `compact()` is still called for `/compact` and overflow recovery. Critically, `ownsCompaction: false` does **not** mean OpenClaw automatically falls back to the legacy engine's compaction path.

That gives two valid plugin patterns: **owning mode** implements your own compaction algorithm and sets `ownsCompaction: true`; **delegating mode** sets `ownsCompaction: false` and has `compact()` call `delegateCompactionToRuntime(...)` from `openclaw/plugin-sdk/core` to use OpenClaw's built-in compaction. A no-op `compact()` is unsafe for an active non-owning engine because it disables the normal `/compact` and overflow-recovery path for that slot.

## Configuration reference

The active context engine is selected via the `plugins.slots.contextEngine` key, which defaults to `"legacy"`; set it to a plugin id to use a plugin engine:

```json5
{
  plugins: {
    slots: {
      // Select the active context engine. Default: "legacy".
      // Set to a plugin id to use a plugin engine.
      contextEngine: "legacy",
    },
  },
}
```

The slot is exclusive at run time — only one registered engine is resolved for a given run or compaction operation. Other enabled `kind: "context-engine"` plugins can still load and run their registration code; the slot only selects which registered engine id OpenClaw resolves when it needs a context engine. When you uninstall the plugin currently selected as `plugins.slots.contextEngine`, OpenClaw resets the slot back to the default (`legacy`) — the same reset applies to `plugins.slots.memory`, with no manual config edit required.

## Relationship to compaction and memory

**Compaction** is one responsibility of the context engine: the legacy engine delegates to OpenClaw's built-in summarization, while plugin engines can implement any strategy (DAG summaries, vector retrieval, etc.). **Memory plugins** (`plugins.slots.memory`) are separate — they provide search/retrieval while context engines control what the model sees, and they can work together (an engine might use memory plugin data during assembly). Engines wanting the active memory prompt path should prefer `buildMemorySystemPromptAddition(...)` from `openclaw/plugin-sdk/core`, which converts active memory prompt sections into a ready-to-prepend `systemPromptAddition`; for lower-level control, pull raw lines from `openclaw/plugin-sdk/memory-host-core` via `buildActiveMemoryPromptSection(...)`. **Session pruning** — trimming old tool results in-memory — still runs regardless of which engine is active.

## Tips

Use `openclaw doctor` to verify your engine is loading correctly. When switching engines, existing sessions continue with their current history while the new engine takes over for future runs. Engine errors are logged and the plugin engine is quarantined for the current Gateway process, with `legacy` taking over user turns so replies continue — repair, update, disable, or uninstall the broken plugin. For development, `openclaw plugins install -l ./my-engine` links a local plugin directory without copying.

**Source**: OpenClaw documentation — `concepts/context-engine` (mirror `inbox/openclaw_docs/concepts/context-engine.md`)
**Last Updated**: 2026-06-22
**Status**: Active
