---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - tool_search
keywords:
  - openclaw tool search
  - tool_search_code bridge
  - openclaw.tools search describe call
  - compact tool catalog
  - tools.toolSearch config
  - code tools directory modes
  - isolated node subprocess runtime
  - fail closed tool policy
topics:
  - OpenClaw
  - Tool Search
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/tools/tool-search
access_control_group: ["general"]
---

# OpenClaw — Tool Search Runtime

## Overview

This note explains the **Tool Search** concept: an experimental OpenClaw agent runtime feature that lets an agent discover and call a large tool catalog through one compact `search` / `describe` / `call` surface instead of putting every tool schema in the prompt. It is useful when a run has many available tools but the model is likely to need only a few. It covers how a turn builds the effective catalog, the three model-facing modes (`code` / `tools` / `directory`), why the feature exists, the `openclaw.tools.*` API, the isolated-runtime boundary, configuration, prompt/telemetry signals, the E2E validation harness, and fail-closed behavior — mirroring the `tools/tool-search` source page. Tool Search is the OpenClaw feature; it is explicitly **not** the Codex-native tool search or dynamic-tools surface, which are stable Codex harness surfaces that do not depend on `tools.toolSearch`.

## What Tool Search Is

When enabled for OpenClaw runs, the model receives one `tool_search_code` tool by default. That tool runs a short JavaScript body in an isolated Node subprocess with an `openclaw.tools` bridge:

```js
const hits = await openclaw.tools.search("create a GitHub issue");
const tool = await openclaw.tools.describe(hits[0].id);
return await openclaw.tools.call(tool.id, {
  title: "Crash on startup",
  body: "Steps to reproduce...",
});
```

The catalog can include OpenClaw tools, plugin tools, MCP tools, and client-provided tools. The model does not see every full schema up front; instead it searches compact descriptors, describes one selected tool when it needs the exact schema, and calls that tool through OpenClaw. Codex harness runs do not receive these experimental OpenClaw Tool Search controls — OpenClaw passes product capabilities to Codex as dynamic tools, and Codex owns the stable native code mode, native tool search, deferred dynamic tools, and nested tool calls.

## How a Turn Runs

At planning time the OpenClaw embedded runner builds the effective catalog for the run in six steps:

1. Resolve the active tool policy for the agent, profile, sandbox, and session.
2. List eligible OpenClaw and plugin tools.
3. List eligible MCP tools through the session MCP runtime.
4. Add eligible client tools supplied for the current run.
5. Index compact descriptors for search.
6. Expose the OpenClaw code bridge, the structured fallback tools, or the compact directory surface to the model.

At execution time every real tool call returns to OpenClaw. The isolated Node runtime does not hold plugin implementations, MCP client objects, or secrets; `openclaw.tools.call(...)` crosses the bridge back into the Gateway, where the normal policy, approval, hook, logging, and result handling still apply.

## Modes

`tools.toolSearch` has three model-facing modes:

- `code`: exposes `tool_search_code`, the default compact JavaScript bridge.
- `tools`: exposes `tool_search`, `tool_describe`, and `tool_call` as plain structured tools for providers that should not receive code.
- `directory`: exposes `tool_search`, `tool_describe`, and `tool_call` plus a bounded prompt directory of available tool names and descriptions for providers that should see tool names without every full schema. OpenClaw can also expose a small bounded set of likely or required tool schemas directly for the current turn.

All modes use the same policy-filtered catalog and normal OpenClaw execution path. If the current runtime cannot launch the isolated Node code-mode child process, the default `code` mode falls back to `tools` before catalog compaction. In `directory` mode, client-provided tools stay directly visible for the current run while OpenClaw tools, plugin tools, and MCP tools can be compacted behind the directory catalog; a direct call to an exact hidden directory name is hydrated from that same authorized catalog before execution. All modes are experimental — prefer direct tool exposure for small OpenClaw tool catalogs, and prefer the Codex-native stable surfaces for Codex harness runs. There is no separate source-selection config: when Tool Search is enabled, the catalog includes eligible OpenClaw, MCP, and client tools after normal policy filtering.

## Why This Exists

Large catalogs are useful but expensive: sending every tool schema to the model makes the request larger, slows planning, and increases accidental tool selection. Tool Search changes the shape of what the model sees:

- direct tools: the model sees every selected schema before the first token.
- Tool Search code mode: the model sees one compact code tool and a short API contract.
- Tool Search tools mode: the model sees three compact structured fallback tools.
- Tool Search directory mode: the model sees a bounded directory plus search/describe/call controls and a small bounded set of likely or required schemas.
- during the turn: the model can load remaining schemas as needed.

Direct tool exposure is still the right default for small catalogs. Tool Search is best when one run can see many tools, especially from MCP servers or client-provided app tools.

## API

The code bridge exposes three operations. `openclaw.tools.search(query, options?)` searches the effective catalog for the current run, returning compact results safe to put back into prompt context; `openclaw.tools.describe(id)` loads full metadata for one search result, including the exact input schema; and `openclaw.tools.call(id, args)` calls a selected tool through OpenClaw:

```js
const hits = await openclaw.tools.search("calendar event", { limit: 5 });
const calendarCreate = await openclaw.tools.describe("mcp:calendar:create_event");
await openclaw.tools.call(calendarCreate.id, {
  summary: "Planning",
  start: "2026-05-09T14:00:00Z",
});
```

The structured fallback mode exposes the same operations as tools — `tool_search`, `tool_describe`, and `tool_call`. Directory mode exposes the same three tools (`tool_search`, `tool_describe`, `tool_call`), keeps client-provided tools directly visible, and may expose a small bounded set of likely or required catalog tool schemas directly for the current turn. If the bounded directory omits entries, use `tool_search` to find them; if the model requests an exact hidden directory tool name directly, OpenClaw hydrates it from the authorized catalog before normal execution. Directory-mode client tool names must not collide with OpenClaw, plugin, or MCP tool names because exact deferred dispatch uses those names.

## Runtime Boundary

The code bridge runs in a short-lived Node subprocess. The subprocess starts with Node permission mode enabled, an empty environment, no filesystem or network grants, and no child-process or worker grants. OpenClaw enforces a parent-process wall-clock timeout and kills the subprocess on timeout, including after async continuations. The runtime exposes only:

- `console.log`, `console.warn`, and `console.error`
- `openclaw.tools.search`
- `openclaw.tools.describe`
- `openclaw.tools.call`

Normal OpenClaw behavior still applies to final calls: tool allow and deny policies; per-agent and per-sandbox tool restrictions; channel/runtime tool policy; approval hooks; plugin `before_tool_call` hooks; and session identity, logs, and telemetry.

## Config

Enable Tool Search for OpenClaw runs with the default code bridge:

```bash
openclaw config set tools.toolSearch true
```

The equivalent JSON is `{ tools: { toolSearch: true } }`. To use the structured fallback tools instead, set `mode: "tools"`; to use the compact directory surface instead, set `mode: "directory"`. The code-mode timeout and search result limits are tunable, and Tool Search can be disabled with `toolSearch: false`:

```json5
{
  tools: {
    toolSearch: {
      mode: "code",
      codeTimeoutMs: 10000,
      searchDefaultLimit: 8,
      maxSearchLimit: 20,
    },
  },
}
```

## Prompt and Telemetry

Tool Search records enough telemetry to compare it with direct tool exposure: total serialized tool and prompt bytes sent to the harness; catalog size and source breakdown; search, describe, and call counts; final tool calls executed through OpenClaw; and selected tool ids and sources. Session logs should make it possible to answer how many tool schemas the model saw up front, how many search and describe operations it performed, which final tool was called, and whether the result came from OpenClaw, MCP, or a client tool.

## E2E Validation

The gateway E2E runner proves both paths with the OpenClaw runtime:

```bash
node --import tsx scripts/tool-search-gateway-e2e.ts
```

It creates a temporary fake plugin with a large tool catalog, starts the mock OpenAI provider, starts a Gateway once in direct mode and once with Tool Search enabled, then compares provider request payloads and session logs. The regression proves: (1) direct mode can call the fake plugin tool; (2) Tool Search can call the same fake plugin tool; (3) direct mode exposes the fake plugin tool schemas directly to the provider; (4) Tool Search exposes only the compact bridge; (5) the Tool Search request payload is smaller for the large fake catalog; and (6) session logs show the expected tool-call counts and bridged call telemetry.

## Failure Behavior

Tool Search should fail closed: if a tool is not in the effective policy, search should not return it; if a selected tool becomes unavailable, `tool_call` should fail; if policy or approval blocks execution, the call result should report that block instead of bypassing it; and if the code bridge cannot create an isolated runtime, use `mode: "tools"` or disable Tool Search for that deployment.

**Source**: OpenClaw documentation — `tools/tool-search` (mirror `inbox/openclaw_docs/tools/tool-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
