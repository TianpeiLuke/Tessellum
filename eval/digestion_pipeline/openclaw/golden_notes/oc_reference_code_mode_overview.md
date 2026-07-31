---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - code_mode
keywords:
  - openclaw code mode
  - exec wait tool surface
  - tools.codemode.enabled
  - quickjs-wasi guest runtime
  - codemoderesult union
  - hidden tool catalog
  - code mode vs codex code mode
  - codemode activation order
topics:
  - OpenClaw
  - Code Mode
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/reference/code-mode
access_control_group: ["general"]
---

# OpenClaw — Code Mode Overview and `exec`/`wait` Contract

## Overview

This note covers the user-facing **contract** of OpenClaw **code mode** (an experimental, off-by-default agent-runtime feature): what it is, why it helps large tool catalogs, how to enable it (`tools.codeMode.enabled: true`), the configuration fields with defaults and runtime clamps, the activation order that swaps the model-visible tool list for just `exec` and `wait`, the `exec`/`wait` input contracts and the `CodeModeResult` union, and the `text`/`json` output API. It mirrors the `reference/code-mode` source page from its intro through *Output API*. The guest-runtime namespace/catalog authoring side is [oc_reference_code_mode_namespaces](oc_reference_code_mode_namespaces.md); the runtime/security/schema model is [oc_reference_code_mode_runtime_security](oc_reference_code_mode_runtime_security.md).

## What Code Mode Is

Code mode is an experimental OpenClaw agent-runtime feature, off by default. When enabled, OpenClaw changes what the model sees for one run: instead of exposing every enabled tool schema directly, the model-visible tool list is exactly `exec` and `wait`, and the model writes a small JavaScript or TypeScript program rather than choosing from a long list of tools.

When code mode is active: the model-visible tool list is exactly `exec` and `wait`; `exec` evaluates model-generated JavaScript or TypeScript in a constrained QuickJS-WASI worker; normal OpenClaw tools are hidden from the model prompt and exposed inside the guest program through `ALL_TOOLS` and `tools`; guest code can search the hidden catalog, describe a tool, and call a tool through the same OpenClaw execution path used by normal turns; MCP tools are grouped under the `MCP` namespace (in code mode the only supported way to call MCP tools); and `wait` resumes a suspended run when nested tool calls are still pending. The key distinction: code mode changes only the model-facing orchestration surface — not OpenClaw/plugin/MCP tools, auth, approval policy, channel behavior, or model selection.

### Code Mode vs Codex Code Mode

OpenClaw code mode is **not** Codex Code mode — they share a name but use different runtimes and expose different `exec` contracts:

- **Codex Code Mode** is enabled for Codex app-server threads unless restricted tool policy disables native code mode; it runs in the Codex coding harness, where the model writes shell commands through an `exec.command` contract.
- **OpenClaw code mode** is disabled unless `tools.codeMode.enabled: true` is configured; it runs in the OpenClaw generic agent runtime, where the model writes JavaScript or TypeScript programs through an `exec.code` contract.

Codex Code Mode and Codex-native dynamic tool search are stable Codex harness surfaces; OpenClaw code mode is an OpenClaw-owned experimental tool-surface adapter for generic OpenClaw runs, using `quickjs-wasi`, a hidden OpenClaw tool catalog, and the normal OpenClaw tool executor.

## Why Code Mode Is Good

Code mode makes large tool catalogs easier for models to use: **smaller prompt surface** (providers receive two control tools instead of dozens or hundreds of full tool schemas); **better orchestration** (loops, joins, small transforms, conditional logic, and parallel nested tool calls inside one code cell); **provider neutral** (works for OpenClaw, plugin, MCP, and client tools without depending on provider-native code execution); **existing policy stays in force** (nested calls still go through OpenClaw policy, approvals, hooks, session context, and audit paths); and **clear failure mode** (when explicitly enabled and the runtime is unavailable, OpenClaw fails closed instead of falling back to broad direct tool exposure). It is especially useful for agents with a large tool catalog or workflows where the model repeatedly searches, combines, and calls tools before answering.

## How to Enable It

Add `tools.codeMode.enabled: true` to the agent or runtime config; the boolean shorthand `tools: { codeMode: true }` is also accepted.

```json5
{
  tools: {
    codeMode: {
      enabled: true,
    },
  },
}
```

Code mode remains off when `tools.codeMode` is omitted, `false`, or an object without `enabled: true`. With sandboxed agents that have configured MCP servers, also ensure the sandbox tool policy allows the bundled MCP plugin, e.g. `tools.sandbox.tools.alsoAllow: ["bundle-mcp"]`. Use explicit limits for tighter bounds:

```json5
{
  tools: {
    codeMode: {
      enabled: true,
      timeoutMs: 10000,
      memoryLimitBytes: 67108864,
      maxOutputBytes: 65536,
      maxSnapshotBytes: 10485760,
      maxPendingToolCalls: 16,
      snapshotTtlSeconds: 900,
      searchDefaultLimit: 8,
      maxSearchLimit: 50,
    },
  },
}
```

To confirm the model payload shape while debugging, run the Gateway with targeted logging: `OPENCLAW_DEBUG_CODE_MODE=1 OPENCLAW_DEBUG_MODEL_TRANSPORT=1 OPENCLAW_DEBUG_MODEL_PAYLOAD=tools openclaw gateway`. With code mode active, the logged model-facing tool names should be `exec` and `wait`; for the redacted provider payload, use `OPENCLAW_DEBUG_MODEL_PAYLOAD=full-redacted` briefly.

## Scope and Terms

The *Technical tour* notes the rest of the source page describes the runtime contract and implementation details, for maintainers, plugin authors debugging tool exposure, and operators validating high-risk deployments. **Runtime status**: runtime [`quickjs-wasi`](https://github.com/vercel-labs/quickjs-wasi); default state disabled; stability experimental (Codex Code mode is a separate stable Codex harness surface); target surface generic OpenClaw agent runs; security posture treats model code as hostile; the user-facing promise is that enabling code mode never silently falls back to broad direct tool exposure.

**Scope** — code mode owns the model-facing orchestration shape for a prepared run; it does not own model selection, channel behavior, auth, tool policy, or tool implementations. *In scope*: the `exec`/`wait` tool definitions, hidden tool catalog construction, JavaScript/TypeScript guest execution, the QuickJS-WASI worker runtime, host callbacks for catalog search/describe/call, resumable state for suspended programs, output/timeout/memory/pending-call/snapshot limits, and telemetry plus trajectory projection for nested calls. *Out of scope*: provider-native remote code execution, shell execution semantics, changing existing tool authorization, persistent user-authored scripts, package-manager/file/network/module access in guest code, and direct reuse of Codex Code mode internals (provider-owned tools such as remote Python sandboxes stay separate).

**Terms** (verbatim): **Code mode** hides normal model tools and exposes only `exec`/`wait`. **Guest runtime** is the QuickJS-WASI JavaScript VM that evaluates model code. **Host bridge** is the narrow JSON-compatible callback surface from guest code back into OpenClaw. **Catalog** is the run-scoped list of effective tools after normal tool policy, plugin, MCP, and client-tool resolution. **Nested tool call** is a tool call made from guest code through the host bridge. **Snapshot** is serialized QuickJS-WASI VM state saved so `wait` can continue a suspended run.

## Configuration Fields

`tools.codeMode.enabled` is the activation gate; setting other code-mode fields does not enable the feature. Supported fields (default · runtime clamp):

- `enabled`: boolean — `false` (enables code mode only when `true`).
- `runtime`: `"quickjs-wasi"` — only supported runtime.
- `mode`: `"only"` — exposes `exec`/`wait`, hides normal model tools.
- `languages`: array of `"javascript"`/`"typescript"` — default includes both.
- `timeoutMs`: wall-clock cap for one `exec`/`wait` — `10000` · `100`–`60000`.
- `memoryLimitBytes`: QuickJS heap cap — `67108864` · `1048576`–`1073741824`.
- `maxOutputBytes`: cap for returned text, JSON, and logs — `65536` · `1024`–`10485760`.
- `maxSnapshotBytes`: cap for serialized VM snapshots — `10485760` · `1024`–`268435456`.
- `maxPendingToolCalls`: cap for concurrent nested tool calls — `16` · `1`–`128`.
- `snapshotTtlSeconds`: how long a suspended VM can resume — `900` · `1`–`86400`.
- `searchDefaultLimit`: default hidden-catalog search result count — `8` (clamped to `maxSearchLimit`).
- `maxSearchLimit`: maximum hidden-catalog search result count — `50` · `1`–`50`.

If code mode is enabled but QuickJS-WASI cannot load, OpenClaw fails closed for that run; it does not silently expose normal tools as fallback.

## Activation Order

Code mode is evaluated after the effective tool policy is known and before the final model request is assembled. The activation order:

1. Resolve the agent, model, provider, sandbox, channel, sender, and run policy.
2. Build the effective OpenClaw tool list.
3. Add eligible plugin, MCP, and client tools.
4. Apply allow and deny policy.
5. If `tools.codeMode.enabled` is false, continue with normal tool exposure.
6. If enabled and tools are active for the run, register the effective tools in the code-mode catalog.
7. Remove all normal tools from the model-visible tool list.
8. Add code-mode `exec` and `wait`.

Runs that intentionally have no tools — raw model calls, `disableTools`, or an empty allowlist — do not activate the code-mode surface even if `tools.codeMode.enabled: true`. The catalog is run-scoped: it must not leak tools from another agent, session, sender, or run.

## Model-Visible Tools

When code mode is active, the model sees exactly two top-level tools, `exec` and `wait`; all other enabled tools are hidden from the model-facing list and registered in the code-mode catalog. The model uses `exec` for tool orchestration, data joining, loops, parallel nested calls, and structured transformations, and `wait` only when `exec` returns a resumable `waiting` result.

### `exec`

`exec` starts a code-mode cell and returns one result; the input code is model generated and treated as hostile.

```typescript
type CodeModeExecInput = {
  code?: string;
  command?: string;
  language?: "javascript" | "typescript";
};
```

Input rules: one of `code` or `command` must be non-empty; `code` is the documented model-facing field; `command` is an exec-compatible alias for hook policies and trusted rewrites (when both are present the values must match); outer code-mode `exec` hook events include `toolKind: "code_mode_exec"` plus `toolInputKind: "javascript" | "typescript"` when the input language is known, letting policies distinguish code-mode cells from shell-style `exec` calls that share the tool name; `language` defaults to `"javascript"`, and `"typescript"` is transpiled before evaluation; `exec` rejects `import`, `require`, dynamic import, and module-loader patterns in v1, and never exposes the normal shell `exec` recursively.

The result is the `CodeModeResult` union:

```typescript
type CodeModeResult = CodeModeCompletedResult | CodeModeWaitingResult | CodeModeFailedResult;

type CodeModeCompletedResult = {
  status: "completed";
  value: unknown;
  output?: CodeModeOutput[];
  telemetry: CodeModeTelemetry;
};

type CodeModeWaitingResult = {
  status: "waiting";
  runId: string;
  reason: "pending_tools" | "yield";
  pendingToolCalls?: CodeModePendingToolCall[];
  output?: CodeModeOutput[];
  telemetry: CodeModeTelemetry;
};

type CodeModeFailedResult = {
  status: "failed";
  error: string;
  code?: CodeModeErrorCode;
  output?: CodeModeOutput[];
  telemetry: CodeModeTelemetry;
};
```

`exec` returns `waiting` when the QuickJS VM suspends with resumable state that still needs a model-visible continuation; the result includes a `runId` for `wait`. Namespace bridge calls (including MCP namespace calls) are auto-drained inside the same `exec`/`wait` call while ready, so a compact code block can inspect `$api()` and call an MCP tool without one model tool call per namespace await. `exec` returns `completed` only when the guest VM has no pending work and the final value is JSON-compatible after the output adapter runs.

### `wait`

`wait` continues a suspended code-mode VM. Its input is `type CodeModeWaitInput = { runId: string }`; its output is the same `CodeModeResult` union returned by `exec`. `wait` exists because nested tools can be slow, interactive, approval gated, or stream partial updates, so the model need not keep one long `exec` call open while the host waits. The QuickJS-WASI snapshot/restore resume mechanism (v1): `exec` evaluates code until completion/failure/suspension; on suspension OpenClaw snapshots the VM and records pending host work; when that work settles, `wait` restores the snapshot, re-registers host callbacks by stable names, delivers nested tool results into the restored VM, drains QuickJS pending jobs, and returns `completed`, `failed`, or another `waiting` result. Snapshots are runtime state, not user artifacts — size-limited, expired, and scoped to the run/session that created them. `wait` fails when `runId` is unknown, the snapshot expired, the parent run/session was aborted, the caller is out of run/session scope, QuickJS-WASI restore fails, or restoring would exceed configured limits.

## Output API

`text(value)` appends human-readable output to the `output` array; `json(value)` appends a structured output item after JSON-compatible serialization; the guest code's final returned value becomes `value` in a `completed` result. An output item is `type CodeModeOutput = { type: "text"; text: string } | { type: "json"; value: unknown }`. Output rules: order matches guest calls; output is capped by `maxOutputBytes`; non-serializable values become plain strings or errors; binary values are unsupported in v1; images/files travel through ordinary OpenClaw tools, not the code-mode bridge.

**Source**: OpenClaw documentation — `reference/code-mode` (mirror `inbox/openclaw_docs/reference/code-mode.md`)
**Last Updated**: 2026-06-22
**Status**: Active
