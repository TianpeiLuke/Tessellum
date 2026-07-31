---
tags:
  - resource
  - documentation
  - openclaw
  - top_level
  - codex_harness
keywords:
  - codex context engine harness implementation
  - context-engine-projection.ts
  - bootstrapHarnessContextEngine assembleHarnessContextEngine
  - finalizeHarnessContextEngineTurn
  - codex ownsCompaction thread/compact/start
  - projectContextEngineAssemblyForCodex
  - codex harness test plan observability
  - dynamic tool fingerprint context engine
topics:
  - OpenClaw
  - Codex Harness Context Engine Port
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plan/codex-context-engine-harness
access_control_group: ["general"]
---

# OpenClaw — Codex Context-Engine Harness: Implementation Procedure

## Overview

This note is the **build runbook** half of OpenClaw's `plan/codex-context-engine-harness` Draft implementation spec: the ordered 10-step procedure for making the bundled Codex app-server harness honor the same context-engine lifecycle (bootstrap / assemble / afterTurn / ingest / maintain / compact) that built-in OpenClaw turns already run, plus the **Test plan**, the **Observability** fields, and the **Migration / compatibility** rules. The rationale, goal, non-goals, current architecture/gap, and acceptance criteria are owned by the sibling design note ([oc_plan_codex_context_engine_harness_design](oc_plan_codex_context_engine_harness_design.md)); this note covers only the source page's `## Implementation plan` (steps 1-10, incl. the two compaction-policy H4s), `## Test plan`, `## Observability`, and `## Migration / compatibility` sections.

## Implementation Steps (1-10)

### 1. Export or relocate reusable context-engine attempt helpers

The reusable lifecycle helpers today live under the embedded agent runner: `src/agents/embedded-agent-runner/run/attempt.context-engine-helpers.ts`, `attempt.prompt-helpers.ts`, and `context-engine-maintenance.ts`. Codex should import **harness-neutral** helpers rather than reaching into runner internals. Create a harness-neutral module, e.g. `src/agents/harness/context-engine-lifecycle.ts`, and move or re-export `runAttemptContextEngineBootstrap`, `assembleAttemptContextEngine`, `finalizeAttemptContextEngineTurn`, `buildAfterTurnRuntimeContext`, `buildAfterTurnRuntimeContextFromUsage`, and a small wrapper around `runContextEngineMaintenance`. Update built-in harness call sites in the same PR. Neutral names should not mention the built-in harness; suggested: `bootstrapHarnessContextEngine`, `assembleHarnessContextEngine`, `finalizeHarnessContextEngineTurn`, `buildHarnessContextEngineRuntimeContext`, `runHarnessContextEngineMaintenance`.

### 2. Add a Codex context projection helper

Add a new module `extensions/codex/src/app-server/context-engine-projection.ts`. Responsibilities: accept the assembled `AgentMessage[]`, original mirrored history, and current prompt; determine which context belongs in developer instructions vs current user input; preserve the current user prompt as the final actionable request; render prior messages in a stable, explicit format; and avoid volatile metadata. The proposed API is:

```ts
export type CodexContextProjection = {
  developerInstructionAddition?: string;
  promptText: string;
  assembledMessages: AgentMessage[];
  prePromptMessageCount: number;
};

export function projectContextEngineAssemblyForCodex(params: {
  assembledMessages: AgentMessage[];
  originalHistoryMessages: AgentMessage[];
  prompt: string;
  systemPromptAddition?: string;
}): CodexContextProjection;
```

The recommended first projection puts `systemPromptAddition` into developer instructions, puts the assembled transcript context before the current prompt in `promptText`, labels it clearly as OpenClaw assembled context, keeps the current prompt last, and excludes a duplicate current user prompt if it already appears at the tail. The example prompt shape is `OpenClaw assembled context for this turn:` followed by a `<conversation_context>` block of `[user]`/`[assistant]` turns and a trailing `Current user request:` section. This preserves context-engine semantics while staying implementable inside OpenClaw. Future improvement: if the Codex app-server exposes a protocol for replacing or supplementing thread history, swap this projection layer to use that API.

### 3. Wire bootstrap before Codex thread startup

In `extensions/codex/src/app-server/run-attempt.ts`: read mirrored session history as today; determine whether the session file existed before this run (prefer a helper that checks `fs.stat(params.sessionFile)` before mirroring writes); open a `SessionManager` (or a narrow session-manager adapter if the helper requires it); and call the neutral bootstrap helper when `params.contextEngine` exists. The pseudo-flow is:

```ts
const hadSessionFile = await fileExists(params.sessionFile);
const sessionManager = SessionManager.open(params.sessionFile);
const historyMessages = sessionManager.buildSessionContext().messages;

await bootstrapHarnessContextEngine({
  hadSessionFile,
  contextEngine: params.contextEngine,
  sessionId: params.sessionId,
  sessionKey: sandboxSessionKey,
  sessionFile: params.sessionFile,
  sessionManager,
  runtimeContext: buildHarnessContextEngineRuntimeContext(...),
  runMaintenance: runHarnessContextEngineMaintenance,
  warn,
});
```

Use the same `sessionKey` convention as the Codex tool bridge and transcript mirror. Today Codex computes `sandboxSessionKey` from `params.sessionKey` or `params.sessionId`; use that consistently unless there is a reason to preserve raw `params.sessionKey`.

### 4. Wire assemble before `thread/start` / `thread/resume` and `turn/start`

In `runCodexAppServerAttempt`: (1) build dynamic tools FIRST so the context engine sees the actual available tool names; (2) read mirrored session history; (3) run context-engine `assemble(...)` when `params.contextEngine` exists; (4) project the assembled result into a developer-instruction addition and prompt text for `turn/start`. The existing hook call `resolveAgentHarnessBeforePromptBuildResult({ prompt, developerInstructions, messages, ctx })` should become context-aware: compute base developer instructions with `buildDeveloperInstructions(params)`, apply context-engine assembly/projection, then run `before_prompt_build` with the projected prompt/developer instructions, so generic prompt hooks see the same prompt Codex will receive. The invariant is that both context engine and hooks get a deterministic, documented order. The recommended first-implementation order is: `buildDeveloperInstructions(params)` → context-engine `assemble()` → append/prepend `systemPromptAddition` to developer instructions → project assembled messages into prompt text → `resolveAgentHarnessBeforePromptBuildResult(...)` → pass final developer instructions to `startOrResumeThread(...)` → pass final prompt text to `buildTurnStartParams(...)`. Encode this order in tests so future changes do not reorder it by accident.

### 5. Preserve prompt-cache stable formatting

The projection helper must produce **byte-stable** output for identical inputs: stable message order, stable role labels, no generated timestamps, no object key order leakage, no random delimiters, and no per-run ids. Use fixed delimiters and explicit sections.

### 6. Wire post-turn after transcript mirroring

Codex's `CodexAppServerEventProjector` builds a local `messagesSnapshot` for the current turn, and `mirrorTranscriptBestEffort(...)` writes that snapshot into the OpenClaw transcript mirror. After mirroring succeeds or fails, call the context-engine finalizer with the best available message snapshot: prefer the full mirrored session context after the write (because `afterTurn` expects the session snapshot, not only the current turn), and fall back to `historyMessages + result.messagesSnapshot` if the session file cannot be reopened. The pseudo-flow is:

```ts
const prePromptMessageCount = historyMessages.length;
await mirrorTranscriptBestEffort(...);
const finalMessages = readMirroredSessionHistoryMessages(params.sessionFile)
  ?? [...historyMessages, ...result.messagesSnapshot];

await finalizeHarnessContextEngineTurn({
  contextEngine: params.contextEngine,
  promptError: Boolean(finalPromptError),
  aborted: finalAborted,
  yieldAborted,
  sessionIdUsed: params.sessionId,
  sessionKey: sandboxSessionKey,
  sessionFile: params.sessionFile,
  messagesSnapshot: finalMessages,
  prePromptMessageCount,
  tokenBudget: params.contextTokenBudget,
  runtimeContext: buildHarnessContextEngineRuntimeContextFromUsage({
    attempt: params,
    workspaceDir: effectiveWorkspace,
    agentDir,
    tokenBudget: params.contextTokenBudget,
    lastCallUsage: result.attemptUsage,
    promptCache: result.promptCache,
  }),
  runMaintenance: runHarnessContextEngineMaintenance,
  sessionManager,
  warn,
});
```

If mirroring fails, still call `afterTurn` with the fallback snapshot, but log that the context engine is ingesting from fallback turn data.

### 7. Normalize usage and prompt-cache runtime context

Codex results include normalized usage from app-server token notifications when available; pass that usage into the context-engine runtime context. If the Codex app-server eventually exposes cache read/write details, map them into `ContextEnginePromptCacheInfo`. Until then, **omit `promptCache` rather than inventing zeros**.

### 8. Compaction policy

There are two compaction systems: (1) OpenClaw context-engine `compact()` and (2) Codex app-server native `thread/compact/start`. Do not silently conflate them.

#### `/compact` and explicit OpenClaw compaction

When the selected context engine has `info.ownsCompaction === true`, explicit OpenClaw compaction should prefer the context engine's `compact()` result for the OpenClaw transcript mirror and plugin state. When the selected Codex harness has a native thread binding, OpenClaw may additionally request Codex native compaction to keep the app-server thread healthy, but this must be reported as a separate backend action in details. Recommended behavior — if `contextEngine.info.ownsCompaction === true`: call context-engine `compact()` first, then best-effort call Codex native compaction when a thread binding exists, return the context-engine result as the primary result, and include Codex native compaction status in `details.codexNativeCompaction`; if the active context engine does not own compaction, preserve current Codex native compaction behavior. This likely requires changing `extensions/codex/src/app-server/compact.ts` or wrapping it from the generic compaction path, depending on where `maybeCompactAgentHarnessSession(...)` is invoked.

#### In-turn Codex native contextCompaction events

Codex may emit `contextCompaction` item events during a turn. Keep the current before/after compaction hook emission in `event-projector.ts`, but do not treat that as a completed context-engine compaction. For engines that own compaction, emit an explicit diagnostic when Codex performs native compaction anyway — the existing `compaction` stream is acceptable, with `details: { backend: "codex-app-server", ownsCompaction: true }`. This makes the split auditable.

### 9. Session reset and binding behavior

The existing Codex harness `reset(...)` clears the Codex app-server binding from the OpenClaw session file; preserve that behavior. Also ensure context-engine state cleanup continues to happen through existing OpenClaw session lifecycle paths. Do not add Codex-specific cleanup unless the context-engine lifecycle currently misses reset/delete events for all harnesses.

### 10. Error handling

Follow built-in OpenClaw semantics: bootstrap failures warn and continue; assemble failures warn and fall back to unassembled pipeline messages/prompt; afterTurn/ingest failures warn and mark post-turn finalization unsuccessful; maintenance runs only after successful, non-aborted, non-yield turns; and compaction errors should not be retried as fresh prompts. Codex-specific additions: if context projection fails, warn and fall back to the original prompt; if the transcript mirror fails, still attempt context-engine finalization with fallback messages; and if Codex native compaction fails after context-engine compaction succeeds, do not fail the whole OpenClaw compaction when the context engine is primary.

## Test Plan

### Unit tests

Add tests under `extensions/codex/src/app-server`. (1) `run-attempt.context-engine.test.ts` — Codex calls `bootstrap` when a session file exists; calls `assemble` with mirrored messages, token budget, tool names, citations mode, model id, and prompt; `systemPromptAddition` is in developer instructions; assembled messages are projected into the prompt before the current request; Codex calls `afterTurn` after mirroring; without `afterTurn`, Codex calls `ingestBatch` or per-message `ingest`; turn maintenance runs after successful turns; and does not run on prompt error, abort, or yield abort. (2) `context-engine-projection.test.ts` — stable output for identical inputs, no duplicate current prompt when assembled history includes it, handles empty history, preserves role order, and includes the system prompt addition only in developer instructions. (3) `compact.context-engine.test.ts` — owning context engine primary result wins, Codex native compaction status appears in details when also attempted, Codex native failure does not fail owning context-engine compaction, and a non-owning context engine preserves current native compaction behavior.

### Existing tests to update

Update `extensions/codex/src/app-server/run-attempt.test.ts` if present (otherwise the nearest Codex app-server run tests); update `extensions/codex/src/app-server/event-projector.test.ts` only if compaction event details change; `src/agents/harness/selection.test.ts` should not need changes unless config behavior changes and should remain stable; and built-in harness context-engine tests should continue to pass unchanged.

### Integration / live tests

Add or extend live Codex harness smoke tests: configure `plugins.slots.contextEngine` to a test engine, configure `agents.defaults.model` to a `codex/*` model, and configure provider/model `agentRuntime.id = "codex"`; then assert the test engine observed `bootstrap`, `assemble`, `afterTurn` or `ingest`, and `maintenance`. Avoid requiring lossless-claw in OpenClaw core tests — use a small in-repo fake context-engine plugin.

## Observability

Add debug logs around the Codex context-engine lifecycle calls: `codex context engine bootstrap started/completed/failed`, `codex context engine assemble applied`, `codex context engine finalize completed/failed`, `codex context engine maintenance skipped` (with reason), and `codex native compaction completed alongside context-engine compaction`. Avoid logging full prompts or transcript contents. Add structured fields where useful: `sessionId`; `sessionKey` (redacted or omitted per existing logging practice); `engineId`; `threadId`; `turnId`; `assembledMessageCount`; `estimatedTokens`; and `hasSystemPromptAddition`.

## Migration / Compatibility

This should be backward-compatible. If no context engine is configured, legacy context-engine behavior should equal today's Codex harness behavior. If `assemble` fails, Codex should continue with the original prompt path. Existing Codex thread bindings should remain valid. **Dynamic tool fingerprinting should not include context-engine output** — otherwise every context change could force a new Codex thread; only the tool catalog should affect the dynamic tool fingerprint.

**Source**: OpenClaw documentation — `plan/codex-context-engine-harness` (mirror `inbox/openclaw_docs/plan/codex-context-engine-harness.md`), Implementation plan / Test plan / Observability / Migration sections
**Last Updated**: 2026-06-22
**Status**: Active
