---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - code_mode
keywords:
  - openclaw code mode runtime
  - code mode state machine
  - quickjs-wasi worker
  - codemodeerrorcode union
  - code mode security boundary
  - code mode telemetry redaction
  - openclaw_debug_code_mode
  - code mode validation e2e
  - typescript source transform
topics:
  - OpenClaw
  - Code Mode
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/reference/code-mode
access_control_group: ["general"]
---

# OpenClaw — Code Mode Runtime State, QuickJS-WASI Sandbox, and Security Model

## Overview

This note models the OpenClaw **code mode** runtime and security boundary — the back half of the experimental `exec`/`wait` tool surface, where the model-generated program actually runs. It covers the per-run **state machine** (`running` / `waiting` / `completed` / `failed` / `expired` / `aborted`) and snapshot-storage bounds, the **QuickJS-WASI** worker responsibilities, the **TypeScript** source-transform-only path, the **defense-in-depth security boundary** ("model code is hostile"), the verbatim `CodeModeErrorCode` union, the **telemetry** counters + redaction constraint, the `OPENCLAW_DEBUG_*` **debugging** switches, the **implementation layout** units, and the **validation checklist** + **E2E test plan**. It mirrors the runtime/security half of the `reference/code-mode` source page (the `Runtime state` through `E2E test plan` sections). The model-facing contract (`exec`/`wait`, config limits) is in `oc_reference_code_mode_overview`; the guest API + namespace registry is in `oc_reference_code_mode_namespaces`.

## Runtime State

Each code-mode run has a state machine. State is scoped by agent run, session, and tool call id — a `wait` call from a different run or session fails. The six states are:

- `running`: VM is executing or nested calls are in flight.
- `waiting`: VM snapshot exists and can be resumed with `wait`.
- `completed`: final value returned; snapshot deleted.
- `failed`: error returned; snapshot deleted.
- `expired`: snapshot or pending state exceeded retention; cannot resume.
- `aborted`: parent run/session cancelled; snapshot deleted.

Snapshot storage is bounded along five dimensions: maximum snapshot bytes per run, maximum live snapshots per process, snapshot TTL, cleanup on run end, and cleanup on Gateway shutdown where persistence is not supported. Snapshots are runtime state, not user artifacts — they are size-limited, expired, and scoped to the run and session that created them. The actual byte/TTL/pending-call caps that bound these dimensions (`maxSnapshotBytes`, `snapshotTtlSeconds`, `maxPendingToolCalls`, etc.) are the `tools.codeMode.*` config fields documented in the overview note.

## QuickJS-WASI Runtime

OpenClaw loads [`quickjs-wasi`](https://github.com/vercel-labs/quickjs-wasi) as a **direct dependency in the owning package**. The runtime does not rely on a transitive copy installed for proxy, PAC, or other unrelated dependencies. Its responsibilities are: compile or load the QuickJS-WASI WebAssembly module; create one isolated VM per code-mode run or resume; register host callbacks by stable names; set memory and interrupt limits; evaluate JavaScript; drain pending jobs; snapshot suspended VM state; restore snapshots for `wait`; and dispose VM handles and snapshots after terminal states. The runtime executes **outside OpenClaw's main event loop in a worker**, so a guest infinite loop must not block the Gateway process indefinitely.

## TypeScript

TypeScript support is a **source transform only**. The accepted input is one TypeScript code string; the output is a JavaScript string evaluated by QuickJS-WASI. There is **no typechecking, no module resolution**, and **no `import` or `require` in v1**; diagnostics are returned as `failed` results. The TypeScript compiler is loaded lazily only for TypeScript cells — plain JavaScript cells and disabled code mode do not load the compiler. The transform should preserve useful line numbers where feasible.

## Security Boundary

Model code is hostile. The runtime uses **defense in depth**, layering eleven distinct controls so the sandbox is never the only barrier:

- run QuickJS-WASI outside the main event loop
- load `quickjs-wasi` as a direct dependency, not through Codex or a transitive package
- no filesystem, network, subprocess, module import, environment variables, or host global objects in the guest
- use QuickJS memory and interrupt limits
- enforce parent-process wall-clock timeout
- enforce output, snapshot, log, and pending-call caps
- serialize host bridge values through a narrow JSON adapter
- convert host errors into plain guest errors, never host realm objects
- drop snapshots on timeout, abort, session end, or expiry
- reject recursive access to `exec`, `wait`, and Tool Search control tools
- prevent convenience-name collisions from shadowing catalog helpers

The sandbox is one security layer. Operators can still need OS-level hardening for high-risk deployments. This posture pairs with the user-facing promise that enabling code mode never silently falls back to broad direct tool exposure — when QuickJS-WASI cannot load, OpenClaw fails closed for that run.

## Error Codes

Errors are surfaced via the optional `code?: CodeModeErrorCode` field on a `CodeModeFailedResult`. The union enumerates every terminal failure category:

```typescript
type CodeModeErrorCode =
  | "runtime_unavailable"
  | "invalid_config"
  | "invalid_input"
  | "unsupported_language"
  | "typescript_transform_failed"
  | "module_access_denied"
  | "timeout"
  | "memory_limit_exceeded"
  | "output_limit_exceeded"
  | "snapshot_limit_exceeded"
  | "snapshot_expired"
  | "snapshot_restore_failed"
  | "too_many_pending_tool_calls"
  | "nested_tool_failed"
  | "aborted"
  | "internal_error";
```

Errors returned to the guest are **plain data**. Host `Error` instances, stack objects, prototypes, and host functions do not cross into QuickJS — consistent with the security boundary's "convert host errors into plain guest errors" rule.

## Telemetry

Code mode reports a fixed set of counters and lifecycle events: visible tool names sent to the model; hidden catalog size and source breakdown; `exec` and `wait` counts; nested search, describe, and call counts; nested tool ids called; timeout, memory, snapshot, and output cap failures; and snapshot lifecycle events. The hard constraint is redaction: telemetry **must not include secrets, raw environment values, or unredacted tool inputs** beyond existing OpenClaw trajectory policy.

## Debugging

When code mode behaves differently from a normal tool run, use targeted model transport logging:

```bash
OPENCLAW_DEBUG_CODE_MODE=1 \
OPENCLAW_DEBUG_MODEL_TRANSPORT=1 \
OPENCLAW_DEBUG_MODEL_PAYLOAD=tools \
OPENCLAW_DEBUG_SSE=events \
openclaw gateway
```

For payload-shape debugging, use `OPENCLAW_DEBUG_MODEL_PAYLOAD=full-redacted`. This logs a capped, redacted JSON snapshot of the model request; it should only be used while debugging because prompts and message text can still appear. For stream debugging, use `OPENCLAW_DEBUG_SSE=peek` to log the first five redacted SSE events. Code mode also **fails closed** if the final provider payload does not contain exactly `exec` and `wait` after the code-mode surface has activated.

## Implementation Layout

The runtime is built from these implementation units: the config contract (`tools.codeMode`); the catalog builder (effective tools to compact entries and id map); the model-surface adapter (replace visible tools with `exec` and `wait`); the QuickJS-WASI runtime adapter (load, eval, snapshot, restore, dispose); the worker supervisor (timeout, abort, crash isolation); the bridge adapter (JSON-safe host callbacks and result delivery); the TypeScript transform adapter; the snapshot store (TTL, size caps, run/session scoping); trajectory projection for nested tool calls; and telemetry counters and diagnostics. The implementation reuses catalog and executor concepts from Tool Search, but **does not use the `node:vm` child as the sandbox**.

## Validation Checklist

Code mode coverage should prove the runtime and security invariants hold:

- disabled config leaves existing tool exposure unchanged
- object config without `enabled: true` leaves code mode disabled
- enabled config exposes only `exec` and `wait` to the model when tools are active for the run
- raw no-tool runs, `disableTools`, and empty allowlists do not trigger code-mode payload enforcement
- all effective non-MCP tools appear in `ALL_TOOLS`; denied tools do not
- `tools.search`, `tools.describe`, and `tools.call` work for OpenClaw tools
- `API.list("mcp")` and `API.read("mcp/<server>.d.ts")` expose TypeScript-style MCP declarations without a bridge/tool call, and `$api()` remains an inline schema fallback
- MCP namespace calls work for visible MCP tools with one object input, while direct MCP catalog entries are absent from `tools.*`
- Tool Search control tools are hidden from both the model surface and the hidden catalog
- nested calls preserve approval and hook behavior
- shell `exec` is hidden from the model but callable by catalog id when allowed; recursive code-mode `exec`/`wait` are not callable from guest code
- TypeScript input is transformed and evaluated without loading TypeScript on disabled or JavaScript-only paths
- `import`, `require`, filesystem, network, and environment access fail
- infinite loops time out and cannot block the Gateway; memory cap failures terminate the guest VM
- output and snapshot caps are enforced for completed and suspended calls
- `wait` resumes a suspended snapshot and returns the final value; expired, aborted, wrong-session, and unknown `runId` values fail
- transcript replay and persistence preserve code-mode control calls; transcript and telemetry show nested tool calls clearly

## E2E Test Plan

Run these as integration or end-to-end tests when changing the runtime:

1. Start a Gateway with `tools.codeMode.enabled: false`.
2. Send an agent turn with a small direct tool set.
3. Assert the model-visible tools are unchanged.
4. Restart with `tools.codeMode.enabled: true`.
5. Send an agent turn with OpenClaw, plugin, MCP, and client test tools.
6. Assert the model-visible tool list is exactly `exec`, `wait`.
7. In `exec`, read `ALL_TOOLS` and assert the effective test tools are present.
8. In `exec`, call OpenClaw/plugin/client tools through `tools.search`, `tools.describe`, and `tools.call`.
9. In `exec`, call `API.list("mcp")` and `API.read("mcp/<server>.d.ts")` and assert the declaration files describe visible MCP tools.
10. In `exec`, call MCP tools through `MCP.<server>.<tool>({ ...input })` and assert direct MCP catalog entries are absent from `ALL_TOOLS` and `tools.*`.
11. Assert denied tools are absent and cannot be called by guessed id.
12. Start a nested tool call that resolves after `exec` returns `waiting`.
13. Call `wait` and assert the restored VM receives the tool result.
14. Assert the final answer contains output produced after restore.
15. Assert timeout, abort, and snapshot expiry clean up runtime state.
16. Export trajectory and assert nested calls are visible under the parent code-mode call.

Docs-only changes to this page should still run `pnpm check:docs`.

**Source**: OpenClaw documentation — `reference/code-mode` (mirror `inbox/openclaw_docs/reference/code-mode.md`)
**Last Updated**: 2026-06-22
**Status**: Active
