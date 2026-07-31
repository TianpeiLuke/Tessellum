---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - typescript
keywords:
  - tool function
  - createsdkmcpserver
  - in-process mcp server
  - zod schema
  - listsessions
  - getsessionmessages
  - renamesession
  - tagsession
  - resolvesettings
  - sdksessioninfo
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/typescript
access_control_group: ["general"]
---

# TypeScript SDK — Helper Functions (tool, MCP, sessions, settings)

## Overview

Beyond the `query()` entry point, the TypeScript Agent SDK exports a set of standalone helper functions for **authoring in-process tools**, **discovering and mutating past sessions**, and **inspecting resolved settings**. This note documents the TypeScript surface (signatures, parameters, return types) of `tool()`, `createSdkMcpServer()`, the session helpers (`listSessions()`, `getSessionMessages()`, `getSessionInfo()`, `renameSession()`, `tagSession()`), and the alpha `resolveSettings()` inspector.

The *concepts* behind these helpers live in other notes — custom tools and MCP in B20A, session storage in B19B — and are linked, not duplicated. This note covers only the shape of each exported function. For exhaustive field tables, see the live [source](https://code.claude.com/docs/en/agent-sdk/typescript).

## `tool()`

Creates a type-safe MCP tool definition for use with SDK MCP servers. The (name, description, input schema, handler, annotations) tuple is the tool descriptor the model uses to decide when and how to call the tool.

```typescript
function tool<Schema extends AnyZodRawShape>(
  name: string,
  description: string,
  inputSchema: Schema,
  handler: (args: InferShape<Schema>, extra: unknown) => Promise<CallToolResult>,
  extras?: { annotations?: ToolAnnotations }
): SdkMcpToolDefinition<Schema>;
```

Parameters: `name` (string), `description` (string), `inputSchema` (a Zod schema defining the tool's input parameters — supports both Zod 3 and Zod 4), `handler` (async function returning a `CallToolResult`), and an optional `extras.annotations` of type `ToolAnnotations`.

### `ToolAnnotations`

Re-exported from `@modelcontextprotocol/sdk/types.js`. All fields are optional hints; clients should not rely on them for security decisions. The fields are `title` (string), `readOnlyHint` (default `false` — tool does not modify its environment), `destructiveHint` (default `true` — tool may perform destructive updates, only meaningful when `readOnlyHint` is `false`), `idempotentHint` (default `false` — repeated calls with the same arguments have no additional effect), and `openWorldHint` (default `true` — tool interacts with external entities such as web search).

```typescript
import { tool } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const searchTool = tool(
  "search",
  "Search the web",
  { query: z.string() },
  async ({ query }) => {
    return { content: [{ type: "text", text: `Results for: ${query}` }] };
  },
  { annotations: { readOnlyHint: true, openWorldHint: true } }
);
```

## `createSdkMcpServer()`

Creates an MCP server instance that runs in the **same process** as your application, exposing the tools created with `tool()` to the agent without a separate subprocess. The signature is `createSdkMcpServer(options): McpSdkServerConfigWithInstance`, where `options.name` (string) names the MCP server, `options.version` is an optional version string, and `options.tools` is an array of tool definitions created with `tool()`. The returned `McpSdkServerConfigWithInstance` is the value you place in `Options.mcpServers`.

## Session discovery functions

These read past session transcripts and metadata from the persisted session store. (Session-storage concept → [B19B](https://code.claude.com/docs/en/agent-sdk/sessions).)

### `listSessions()`

Discovers and lists past sessions with light metadata: `listSessions(options?): Promise<SDKSessionInfo[]>`. Filter by project directory or list across all projects. Parameters: `options.dir` (directory to list sessions for; when omitted, returns sessions across all projects), `options.limit` (max number of sessions), and `options.includeWorktrees` (default `true` — when `dir` is inside a git repository, include sessions from all worktree paths). Results are sorted by `lastModified` descending, so the first item is the newest.

The return type `SDKSessionInfo` carries: `sessionId` (UUID), `summary` (display title: custom title, auto-generated summary, or first prompt), `lastModified` (ms since epoch), `fileSize` (bytes — only populated for local JSONL storage), `customTitle` (user-set, via `/rename`), `firstPrompt`, `gitBranch` (branch at the end of the session), `cwd`, `tag` (user-set, see `tagSession()`), and `createdAt`.

```typescript
import { listSessions } from "@anthropic-ai/claude-agent-sdk";

const sessions = await listSessions({ dir: "/path/to/project", limit: 10 });

for (const session of sessions) {
  console.log(`${session.summary} (${session.sessionId})`);
}
```

### `getSessionMessages()`

Reads user and assistant messages from a past session transcript: `getSessionMessages(sessionId, options?)` returns `Promise<SessionMessage[]>`. Parameters are `sessionId` (required UUID), `options.dir` (project directory; when omitted, searches all projects), `options.limit`, and `options.offset` (number of messages to skip from the start). Each returned `SessionMessage` has `type` (`"user" | "assistant"`), `uuid`, `session_id`, `message` (raw transcript payload, typed `unknown`), and `parent_tool_use_id` (for subagent messages, the `tool_use_id` of the spawning `Agent` tool call; `null` for main-session and older sessions).

### `getSessionInfo()`

Reads metadata for a single session by ID without scanning the full project directory: `getSessionInfo(sessionId, options?)` returns `Promise<SDKSessionInfo | undefined>`. Parameters are `sessionId` (required UUID) and `options.dir` (project directory; when omitted, searches all project directories). Returns the same `SDKSessionInfo` shape as `listSessions()`, or `undefined` if the session is not found.

## Session mutation functions

### `renameSession()`

Renames a session by appending a custom-title entry — `renameSession(sessionId, title, options?): Promise<void>`. Repeated calls are safe; the most recent title wins. Parameters: `sessionId` (required UUID), `title` (required; must be non-empty after trimming whitespace), and `options.dir` (project directory; when omitted, searches all project directories).

### `tagSession()`

Tags a session — `tagSession(sessionId, tag, options?)` returns `Promise<void>`. The `tag` parameter is `string | null`; pass `null` to clear the tag. Repeated calls are safe; the most recent tag wins. `options.dir` works as for `renameSession()`.

## `resolveSettings()`

Resolves the effective Claude Code settings for a given directory using the same merge engine as the CLI, **without spawning the Claude CLI**. Use it to inspect what configuration a `query()` call would see before invoking one.

This function is **alpha** and its API may change before stabilization. It reads MDM sources (macOS plist, Windows HKLM/HKCU) for parity with CLI startup, but does not execute the admin-configured `policyHelper` subprocess. `permissions.defaultMode` is returned as-is from all tiers including project settings, and the trust filter the CLI applies before honoring escalating permission modes is not applied.

The signature is `resolveSettings(options?): Promise<ResolvedSettings>`. All option fields are optional: `options.cwd` (default `process.cwd()`), `options.settingSources` (a `SettingSource[]`; pass `[]` to skip user, project, and local settings — managed policy settings load in all cases), `options.managedSettings` (restrictive policy-tier settings; non-restrictive keys such as `model` are silently dropped so this can tighten but not loosen managed policy), and `options.serverManagedSettings` (server-managed payload from `/api/claude_code/settings`; non-restrictive keys pass through unfiltered).

The return type `ResolvedSettings` has `effective` (merged `Settings` after applying all enabled sources in precedence order), `provenance` (for each top-level key, which source supplied the value), and `sources` (per-source raw settings, ordered lowest to highest precedence). The `SettingSource` union itself is documented under `Options.settingSources` ([cc_sdk_typescript_options](cc_sdk_typescript_options.md)).

```typescript
import { resolveSettings } from "@anthropic-ai/claude-agent-sdk";

const { effective, provenance } = await resolveSettings({
  cwd: "/path/to/project",
  settingSources: ["user", "project", "local"],
});

console.log(`Cleanup period: ${effective.cleanupPeriodDays} days`);
console.log(`Set by: ${provenance.cleanupPeriodDays?.source}`);
```

**Source**: https://code.claude.com/docs/en/agent-sdk/typescript
**Last Updated**: 2026-06-13
**Status**: Active
