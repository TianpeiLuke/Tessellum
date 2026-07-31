---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - code_mode
keywords:
  - openclaw code mode namespaces
  - guest runtime api all_tools
  - tools.search describe call
  - MCP namespace api virtual declarations
  - registerCodeModeNamespaceForPlugin
  - createCodeModeNamespaceTool
  - code-mode tool catalog id
  - tool search interaction supersession
  - nested tool execution bridge
  - scope serialization rules
topics:
  - OpenClaw
  - Code Mode
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/code-mode
access_control_group: ["general"]
---

# OpenClaw — Code Mode: Guest Runtime API, Internal Namespaces, and the Hidden Tool Catalog

## Overview

This note is the procedure for authoring and invoking tool access from inside OpenClaw **code-mode** guest programs — the `exec`/`wait` worker that the model drives once `tools.codeMode.enabled: true` is active. It mirrors the back half of the `reference/code-mode` source page: the guest global API (`ALL_TOOLS`, `tools.search`/`describe`/`call`, the generated `MCP.<server>` namespace, the read-only `API` virtual declaration surface), the loader-owned **internal-namespace registry** (register → scope → serialize → dispatch → cleanup, with the security test checklist), the hidden **tool catalog** id shape and control-tool exclusions, how code mode supersedes the standalone **Tool Search** model surface, **tool-name collision** handling, and how **nested tool calls** cross the host bridge while preserving policy. The user-facing contract (`exec`/`wait` schemas, enable config) lives in the sibling overview note; the runtime state machine, QuickJS-WASI worker, and security boundary live in the sibling runtime/security note.

## Guest runtime API

When code mode is active, the guest runtime exposes a small set of globals. `ALL_TOOLS` is **compact metadata** for the run-scoped catalog (it does not contain full schemas by default); full schema is loaded only on demand through `tools.describe(id)`.

```typescript
declare const ALL_TOOLS: ToolCatalogEntry[];
declare const tools: ToolCatalog;
declare const MCP: Record<string, unknown>;
declare const namespaces: Record<string, unknown>;

declare function text(value: unknown): void;
declare function json(value: unknown): void;
declare function yield_control(reason?: string): Promise<void>;
```

A `ToolCatalogEntry` carries `id`, `name`, optional `label`, `description`, `source` (`"openclaw" | "plugin" | "mcp" | "client"`), and optional `sourceName`. The on-demand `ToolCatalogEntryWithSchema` is the same entry plus `parameters: unknown`. The catalog helpers are `search(query, options?: { limit? })`, `describe(id)`, and `call(id, input?)`, plus an index signature `[safeToolName: string]: unknown` for convenience functions.

```typescript
type ToolCatalog = {
  search(query: string, options?: { limit?: number }): Promise<ToolCatalogEntry[]>;
  describe(id: string): Promise<ToolCatalogEntryWithSchema>;
  call(id: string, input?: unknown): Promise<unknown>;
  [safeToolName: string]: unknown;
};
```

Convenience tool functions (e.g. `tools.web_search(...)`) are installed **only for unambiguous safe names**. The documented usage path is search → describe → call: `tools.search("read local file")`, then `tools.describe(files[0].id)`, then `tools.call(fileRead.id, { path: "README.md" })`.

### Calling MCP tools through the `MCP` namespace

MCP catalog entries are **not** callable through `tools.call(...)` or convenience functions in code mode — they are exposed only through the generated `MCP` namespace. TypeScript-style declaration files are available through the read-only `API` virtual file surface, so agents inspect MCP signatures without adding MCP schemas to the prompt. Guest code calls `await API.list("mcp")` for file metadata and `await API.read("mcp/<server>.d.ts")` for a declaration, then calls `MCP.<server>.<tool>({ ...input })` with one object argument:

```typescript
const files = await API.list("mcp");
const githubApi = await API.read("mcp/github.d.ts");

const issue = await MCP.github.createIssue({
  owner: "openclaw",
  repo: "openclaw",
  title: "Investigate gateway logs",
});

const resource = await MCP.docs.resources.read({ uri: "memo://one" });
```

`API.read("mcp/<server>.d.ts")` returns compact declarations inferred from MCP tool metadata, including a per-server `$api(toolName?, options?: { schema? }): Promise<McpApiHeader>` helper that stays available as an inline fallback for a single-tool schema response. The declaration files are **virtual** (not written under the workspace or state directory): for each `exec` call OpenClaw builds the run-scoped catalog, keeps the visible MCP entries, renders `mcp/index.d.ts` plus one `mcp/<server>.d.ts` per visible server, and injects that small read-only table into the QuickJS worker. Guest code sees only the `API` object; **unknown paths and `.` / `..` segments are rejected**. The guest runtime must not expose host objects directly — inputs and outputs cross the bridge as JSON-compatible values with explicit size caps.

## Internal namespaces

Internal namespaces give code mode a concise domain API (e.g. `Issues`, `Fictions`, `Calendar`) without adding model-visible tools; the model still sees only `exec` and `wait`. **Namespaces are internal for now — there is no public plugin SDK namespace API**: external plugin namespaces need a loader-owned contract so plugin identity, installed manifests, auth state, and cached catalog descriptors cannot drift from the plugin tools that back the namespace. Core code mode owns only the sandbox, serialization, catalog gating, and bridge dispatch. Guest code uses either the direct global or the `namespaces` map:

```javascript
const open = await Issues.list({ state: "open" });
const alsoOpen = await namespaces.Issues.list({ state: "open" });
return { count: open.length, alsoCount: alsoOpen.length };
```

### Registry lifecycle

The namespace registry is **process-local and keyed by namespace id**. A typical run follows this path:

1. A trusted loader calls `registerCodeModeNamespaceForPlugin(pluginId, registration)`.
2. Code mode creates the hidden `ToolSearchRuntime` for the run and reads its run-scoped catalog.
3. `createCodeModeNamespaceRuntime(ctx, catalog)` keeps only registrations whose `requiredToolNames` are all visible and owned by the same `pluginId`.
4. Each visible namespace calls `createScope(ctx)` for the current run. The scope receives run context such as `agentId`, `sessionKey`, `sessionId`, `runId`, config, and abort state.
5. Scope data is serialized into a plain descriptor and injected into QuickJS as direct globals and `namespaces.<globalName>`.
6. Guest calls suspend through the worker bridge, resolve the namespace path on the host, map the call to a declared plugin-owned catalog tool, and execute that tool through `ToolSearchRuntime.call`.
7. OpenClaw auto-drains ready namespace bridge calls inside the active `exec`/`wait` tool call. If namespace work is still pending at the timeout or the guest yields explicitly, `wait` resumes the same namespace runtime later.
8. Plugin rollback or uninstall calls `clearCodeModeNamespacesForPlugin(pluginId)` so stale globals do not survive a failed plugin load.

The important invariant: **namespace calls are catalog tool calls.** They use the same policy hooks, approvals, abort handling, telemetry, transcript projection, and suspend/resume behavior as `tools.call(...)`.

### Registration shape

Register namespaces from the integration that owns the backing tools; keep the scope small and only expose domain verbs that map to declared catalog tools. `createCodeModeNamespaceTool(toolName, inputMapper)` marks a scope member as a callable namespace function — the optional `inputMapper` receives the guest arguments and returns the input object for the backing catalog tool; without a mapper the first guest argument is used, or `{}` when omitted.

```typescript
import {
  createCodeModeNamespaceTool,
  registerCodeModeNamespaceForPlugin,
} from "../agents/code-mode-namespaces.js";

const pluginId = "github";

registerCodeModeNamespaceForPlugin(pluginId, {
  id: "github-issues",
  globalName: "Issues",
  description: "GitHub issue helpers for the current repository.",
  requiredToolNames: ["github_list_issues", "github_update_issue"],
  prompt: "Use Issues.list(params) and Issues.update(number, patch).",
  createScope: (ctx) => ({
    repository: ctx.config,
    list: createCodeModeNamespaceTool("github_list_issues", ([params]) => params ?? {}),
    update: createCodeModeNamespaceTool("github_update_issue", ([number, patch]) => ({
      number,
      patch,
    })),
  }),
});
```

Raw host functions are **rejected before guest code runs** — returning `list: async () => githubClient.listIssues()` from `createScope` bypasses the catalog tool lifecycle and is rejected. Use `createCodeModeNamespaceTool(...)` markers instead.

### Ownership and visibility

Namespace ownership is bound to the registration caller's `pluginId`; `requiredToolNames` is both a visibility gate and an ownership check:

- every required tool must exist in the run catalog;
- every required tool must have `sourceName === pluginId`;
- the namespace is hidden when any required tool is absent or owned by another plugin;
- each callable path may target only a tool named in `requiredToolNames`.

This prevents another plugin from exposing a namespace by registering a same-named tool, and keeps namespaces aligned with ordinary agent policy: if the run cannot see the backing tools, it cannot see the namespace. A domain namespace (e.g. GitHub) should live behind the extension that owns its auth, clients, rate limits, write approvals, and tests; core code mode should not embed provider-specific APIs, token handling, or provider policy.

### Scope serialization rules

`createScope(ctx)` may return a plain object containing JSON-compatible values, arrays, nested objects, and `createCodeModeNamespaceTool(...)` call markers — host objects never enter QuickJS directly. The serializer **rejects**: raw functions; circular object graphs; unsafe path segments (`__proto__`, `constructor`, `prototype`, empty keys, or keys containing the internal path separator); `globalName` values that are not JavaScript identifiers; and `globalName` collisions with built-in code-mode globals such as `tools`, `namespaces`, `text`, `json`, `yield_control`, or `__openclaw*`. Values that cannot be JSON-serialized are converted to JSON-safe fallback values before crossing the bridge; binary data, handles, sockets, clients, and class instances should stay behind ordinary catalog tools.

### Prompts and cleanup

The namespace `description` and optional `prompt` are appended to the model-visible `exec` schema **only when the namespace is visible** for that run; keep them about the namespace contract, not auth setup, implementation history, or unrelated plugin behavior. Cleanup is **plugin-owned**: namespaces are process-local registrations, so call `clearCodeModeNamespacesForPlugin(pluginId)` when the owning plugin is disabled, uninstalled, or rolled back rather than keeping per-namespace teardown handles. Tests can call `clearCodeModeNamespacesForTest()` to avoid leaking registrations across cases.

### Test checklist

Namespace changes should cover the security boundary and the guest behavior: namespace prompt text appears only when backing tools are visible; same-named tools from another `sourceName` do not expose the namespace; raw scope functions are rejected; forged namespace ids and forged paths are rejected; callable paths cannot target undeclared tools; nested objects and shared references serialize correctly; namespace calls execute through catalog tools and return JSON-safe details; failures can be caught by guest code; suspended namespace calls resume through `wait`; and plugin rollback clears the owning namespace registrations. Use the generic `tools.search` / `tools.call` catalog for arbitrary enabled OpenClaw/plugin/client tools, `MCP` for MCP tools, and other namespaces for plugin-owned documented domain APIs where concise code is more reliable than repeated schema lookups.

## Tool catalog

The hidden catalog includes tools **after effective policy filtering**, in this order: (1) OpenClaw core tools, (2) bundled plugin tools, (3) external plugin tools, (4) MCP tools, (5) client-provided tools for the current run. Catalog ids are stable within one run and deterministic across equivalent tool sets when possible. The recommended id shape is `<source>:<owner>:<tool-name>`, e.g. `openclaw:core:message`, `plugin:browser:browser_request`, `mcp:github:create_issue`, `client:app:select_file`.

The catalog **omits the code-mode control tools** to prevent recursion and keep the model-facing contract narrow: `exec`, `wait`, `tool_search_code`, `tool_search`, `tool_describe`, and `tool_call`. MCP entries stay in the run-scoped catalog so policy, approvals, hooks, telemetry, transcript projection, and exact tool ids remain shared with normal tool execution; the guest-facing `ALL_TOOLS`, `tools.search(...)`, `tools.describe(...)`, and `tools.call(...)` views omit MCP entries, while the generated `MCP.<server>.<tool>({ ...input })` namespace resolves back to the exact catalog id and dispatches through the same executor path.

## Tool Search interaction

Code mode **supersedes** the OpenClaw Tool Search model surface for runs where it is active. When `tools.codeMode.enabled` is true and code mode activates: OpenClaw does not expose `tool_search_code`, `tool_search`, `tool_describe`, or `tool_call` as model-visible tools; the same cataloging idea moves inside the guest runtime; the guest receives compact `ALL_TOOLS` metadata plus search/describe/call helpers for non-MCP tools; MCP calls use the generated `MCP` namespace and its `$api()` headers instead of `tools.call(...)`; and nested calls dispatch through the same OpenClaw executor path that Tool Search uses. The standalone Tool Search page describes the compact catalog bridge; code mode is the generic alternative for runs that can use `exec` and `wait`.

## Tool names and collisions

The model-visible `exec` tool is the code-mode tool. If the normal OpenClaw shell `exec` tool is enabled, it is hidden from the model and cataloged like any other tool. Inside the guest runtime: `tools.call("openclaw:core:exec", input)` can call the shell exec tool if policy allows it; `tools.exec(...)` is installed only if the shell exec catalog entry has an unambiguous safe name; and the code-mode `exec` tool is never recursively available through `tools`. If two tools normalize to the same safe convenience name, OpenClaw omits the convenience function and requires `tools.call(id, input)`.

## Nested tool execution

Every nested tool call crosses the host bridge and re-enters OpenClaw. Nested execution **preserves**: active agent id; session id and session key; sender and channel context; sandbox policy; approval policy; plugin `before_tool_call` hooks; abort signal; streaming updates where available; and trajectory and audit events. Nested calls project into the transcript as real tool calls (identifying the parent code-mode tool call and the nested tool id) so support bundles can show what happened. Parallel nested calls are allowed up to `maxPendingToolCalls`.

**Source**: OpenClaw documentation — `reference/code-mode` (mirror `inbox/openclaw_docs/reference/code-mode.md`)
**Last Updated**: 2026-06-22
**Status**: Active
