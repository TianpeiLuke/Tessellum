---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - typescript
keywords:
  - query object
  - runtime control methods
  - applyflagsettings
  - interrupt and rewind
  - setpermissionmode setmodel
  - mcp server control
  - streaming input mode
  - warmquery methods
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

# Claude Agent SDK (TypeScript) — The `Query` Object

## Overview

The `Query` object is the interface returned by [`query()`](cc_sdk_typescript_query_function.md). It extends `AsyncGenerator<SDKMessage, void>`, so a consumer iterates it for the streamed message turns, but it also exposes a **runtime-control surface** of methods for steering a session that is already running: interrupting, rewinding files, switching model and permission mode, applying arbitrary flag settings, managing MCP servers, introspecting the session, streaming further input, and tearing down. The same method table appears on the `WarmQuery` handle's child `Query` returned by `startup()`.

Several methods are usable **only in streaming input mode** (i.e., when `prompt` is an `AsyncIterable<SDKUserMessage>` rather than a single string). This note documents the method signatures, the `applyFlagSettings()` flag-settings layer and its which-keys-apply rules, the `WarmQuery` methods, and the typed return shapes (`SDKControlInitializeResponse`, `McpSetServersResult`, `RewindFilesResult`). The *concepts* behind each surface — file checkpointing, permissions, MCP — are linked out, not duplicated.

## The `Query` Interface

`Query` extends the async generator with control methods:

```typescript
interface Query extends AsyncGenerator<SDKMessage, void> {
  interrupt(): Promise<void>;
  rewindFiles(
    userMessageId: string,
    options?: { dryRun?: boolean }
  ): Promise<RewindFilesResult>;
  setPermissionMode(mode: PermissionMode): Promise<void>;
  setModel(model?: string): Promise<void>;
  setMaxThinkingTokens(maxThinkingTokens: number | null): Promise<void>;
  applyFlagSettings(settings: { [K in keyof Settings]?: Settings[K] | null }): Promise<void>;
  initializationResult(): Promise<SDKControlInitializeResponse>;
  supportedCommands(): Promise<SlashCommand[]>;
  supportedModels(): Promise<ModelInfo[]>;
  supportedAgents(): Promise<AgentInfo[]>;
  mcpServerStatus(): Promise<McpServerStatus[]>;
  accountInfo(): Promise<AccountInfo>;
  reconnectMcpServer(serverName: string): Promise<void>;
  toggleMcpServer(serverName: string, enabled: boolean): Promise<void>;
  setMcpServers(servers: Record<string, McpServerConfig>): Promise<McpSetServersResult>;
  streamInput(stream: AsyncIterable<SDKUserMessage>): Promise<void>;
  stopTask(taskId: string): Promise<void>;
  close(): void;
}
```

## Methods

Grouped by purpose (descriptions per the source method table):

**Steer / interrupt the run**
- `interrupt()` — interrupts the query (streaming input mode only).
- `rewindFiles(userMessageId, options?)` — restores files to their state at the specified user message; pass `{ dryRun: true }` to preview changes; requires `enableFileCheckpointing: true` (see [File checkpointing](https://code.claude.com/docs/en/agent-sdk/file-checkpointing)).
- `stopTask(taskId)` — stop a running background task by ID.

**Change session configuration mid-run**
- `setPermissionMode()` — changes the permission mode (streaming input mode only).
- `setModel()` — changes the model (streaming input mode only).
- `setMaxThinkingTokens()` — *deprecated*: use the `thinking` option instead.
- `applyFlagSettings(settings)` — merges settings into the session's flag-settings layer at runtime (streaming input mode only); see below.

**Introspect the session**
- `initializationResult()` — returns the full initialization result (supported commands, models, account info, output-style configuration) as a `SDKControlInitializeResponse`.
- `supportedCommands()` — available slash commands (`SlashCommand[]`).
- `supportedModels()` — available models with display info (`ModelInfo[]`).
- `supportedAgents()` — available subagents (`AgentInfo[]`).
- `mcpServerStatus()` — status of connected MCP servers (`McpServerStatus[]`).
- `accountInfo()` — account information (`AccountInfo`).

**Manage MCP servers dynamically**
- `reconnectMcpServer(serverName)` — reconnect an MCP server by name.
- `toggleMcpServer(serverName, enabled)` — enable or disable an MCP server by name.
- `setMcpServers(servers)` — dynamically replace the set of MCP servers for this session; returns which servers were added, removed, and any errors (`McpSetServersResult`).

**Drive input / tear down**
- `streamInput(stream)` — stream input messages to the query for multi-turn conversations.
- `close()` — close the query and terminate the underlying process; forcefully ends the query and cleans up all resources.

## `applyFlagSettings()` — the flag-settings layer

`applyFlagSettings()` changes [settings](https://code.claude.com/docs/en/settings) on a running session without restarting the query. Use it when a setting that has no dedicated setter needs to change mid-session, such as tightening `permissions` after the agent reads untrusted input. `setModel()` and `setPermissionMode()` are dedicated setters; `applyFlagSettings()` is the general form accepting any subset of settings keys (passing `model` here behaves the same as `setModel()`).

**Which keys take effect mid-session:**
- **Applied on the next turn**: `model`, `effortLevel`, `ultracode`, `permissions`, `hooks`, `skillOverrides`, `fastMode`, `awaySummaryEnabled`, `agent`. Switching `agent` also applies that agent's model override, hooks, and system prompt on the next turn.
- **No effect mid-session**: the system prompt options. These resolve once at startup, so the running session keeps the original value even though the call succeeds. To change them, start a new session.

Values write to the flag-settings layer — the same layer the inline `settings` option of `query()` populates at startup. Flag settings sit near the top of settings precedence: they override user, project, and local settings, and only managed policy settings can override them.

Successive calls **shallow-merge** top-level keys: a second call with `{ permissions: {...} }` replaces the entire prior `permissions` object rather than deep-merging. To clear a key from the flag layer and fall back to lower-precedence sources, pass `null` for that key. Passing `undefined` has no effect (JSON serialization drops it). Only available in streaming input mode.

```typescript
const q = query({ prompt: messageStream });

// Override the model for the rest of the session
await q.applyFlagSettings({ model: "claude-opus-4-6" });

// Later: clear the override and fall back to lower-precedence settings
await q.applyFlagSettings({ model: null });
```

> `applyFlagSettings()` is TypeScript-only. The Python SDK does not expose an equivalent method.

## `WarmQuery` methods

`WarmQuery` is the handle returned by [`startup()`](cc_sdk_typescript_query_function.md). The subprocess is already spawned and initialized, so calling `query()` on this handle writes the prompt to a ready process with no startup latency. It extends `AsyncDisposable`, so it works with `await using` for automatic cleanup.

- `query(prompt)` — send a prompt to the pre-warmed subprocess and return a `Query`; **can only be called once** per `WarmQuery`.
- `close()` — close the subprocess without sending a prompt; use to discard a warm query no longer needed.

## Typed return shapes

- **`SDKControlInitializeResponse`** (from `initializationResult()`) — `{ commands: SlashCommand[]; agents: AgentInfo[]; output_style: string; available_output_styles: string[]; models: ModelInfo[]; account: AccountInfo; fast_mode_state?: "off" | "cooldown" | "on" }`. When `initialize` is sent to an already-running session, the control-response wrapper (not this payload) also carries an optional `pending_permission_requests` array of in-flight `control_request` messages awaiting a reply — read it to surface in-flight permission prompts, since they will not be re-sent.
- **`McpSetServersResult`** (from `setMcpServers()`) — `{ added: string[]; removed: string[]; errors: Record<string, string> }`.
- **`RewindFilesResult`** (from `rewindFiles()`) — `{ canRewind: boolean; error?: string; filesChanged?: string[]; insertions?: number; deletions?: number }`.
- **`SlashCommand`** — `{ name: string; description: string; argumentHint: string; aliases?: string[] }`.
- **`AccountInfo`** — `{ email?: string; organization?: string; subscriptionType?: string; tokenSource?: string; apiKeySource?: string }`.

For the full field tables of `ModelInfo`, `AgentInfo`, `McpServerStatus`, and `McpServerConfig`, see the [tool & permission type catalog](cc_sdk_typescript_tool_and_permission_types.md) and the live source. The `Options` keys these methods mutate (`permissionMode`, `model`, `mcpServers`, `enableFileCheckpointing`) are documented in [Options](cc_sdk_typescript_options.md).

**Source**: https://code.claude.com/docs/en/agent-sdk/typescript
**Last Updated**: 2026-06-13
**Status**: Active
