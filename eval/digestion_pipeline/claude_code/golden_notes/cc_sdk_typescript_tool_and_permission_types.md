---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - type_catalog
keywords:
  - toolinputschemas
  - tooloutputschemas
  - permission types
  - permissionupdate
  - canusetool
  - permissionmode
  - mcpserverconfig
  - agentdefinition
  - typescript agent sdk types
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: model
source_url: https://code.claude.com/docs/en/agent-sdk/typescript
access_control_group: ["general"]
---

# Claude Agent SDK (TypeScript) — Tool, Permission & Config Type Catalog

## Overview

The TypeScript Agent SDK exports a flat catalog of types describing the **shape of the data** that flows through a session: the per-tool input/output schemas (`ToolInputSchemas`/`ToolOutputSchemas`), the permission primitives (`PermissionMode`, `CanUseTool`, `PermissionResult`, `PermissionUpdate`, …), and the config/metadata records for agents, MCP servers, plugins, models, and usage. All are exported from `@anthropic-ai/claude-agent-sdk` and used for type-safe tool interactions, permission callbacks, and introspection.

This note is a **navigable index** of those type names with a one-line gloss each — not a re-dump of every field table. For exhaustive field lists, follow the `source_url`. The *concepts* behind tools live in the custom-tools / MCP page (B20A) and permissions in the hooks/permissions page (B20C); the message/hook type catalog is its sibling note [`cc_sdk_typescript_message_and_hook_types`](cc_sdk_typescript_message_and_hook_types.md).

## Tool Input Types

`ToolInputSchemas` is the union of all built-in tool input types — the typed argument shape each callable tool accepts. Each member type is named `<Tool>Input` (some use file-prefixed names, e.g. `FileEditInput`). The union:

```typescript
type ToolInputSchemas =
  | AgentInput
  | AskUserQuestionInput
  | BashInput
  | TaskOutputInput
  | EnterWorktreeInput
  | ExitPlanModeInput
  | FileEditInput
  | FileReadInput
  | FileWriteInput
  | GlobInput
  | GrepInput
  | ListMcpResourcesInput
  | McpInput
  | MonitorInput
  | NotebookEditInput
  | ReadMcpResourceInput
  | SubscribeMcpResourceInput
  | SubscribePollingInput
  | TaskCreateInput
  | TaskGetInput
  | TaskListInput
  | TaskStopInput
  | TaskUpdateInput
  | TodoWriteInput
  | UnsubscribeMcpResourceInput
  | UnsubscribePollingInput
  | WebFetchInput
  | WebSearchInput
  | WorkflowInput;
```

Per-tool input gloss (selected; tool name in **bold** where it differs from the type's stem):

- **Agent** (`AgentInput`, previously `Task`, still accepted as alias) — `description`, `prompt`, `subagent_type`, optional `model` (`sonnet`/`opus`/`haiku`/`fable`), `resume`, `run_in_background`, `max_turns`, `mode`, `isolation: "worktree"`. Launches a subagent for multi-step tasks.
- **Bash** (`BashInput`) — `command`, optional `timeout`, `description`, `run_in_background`, `dangerouslyDisableSandbox`.
- **Monitor** (`MonitorInput`) — runs a background script and streams each stdout line to Claude as an event; `persistent: true` for session-length watches.
- **TaskOutput** (`TaskOutputInput`) — `task_id`, `block`, `timeout`; retrieves output from a background task.
- **Edit** (`FileEditInput`) — `file_path`, `old_string`, `new_string`, optional `replace_all`.
- **Read** (`FileReadInput`) — `file_path`, optional `offset`, `limit`, `pages` (PDF page ranges).
- **Write** (`FileWriteInput`) — `file_path`, `content`.
- **Glob** (`GlobInput`) — `pattern`, optional `path`.
- **Grep** (`GrepInput`) — ripgrep wrapper: `pattern`, optional `path`, `glob`, `type`, `output_mode`, `-i`/`-n`/`-B`/`-A`/`-C`, `context`, `head_limit`, `offset`, `multiline`.
- **TaskStop** (`TaskStopInput`) — `task_id` (or deprecated `shell_id`).
- **NotebookEdit** (`NotebookEditInput`) — `notebook_path`, `new_source`, optional `cell_id`, `cell_type`, `edit_mode`.
- **WebFetch** (`WebFetchInput`) — `url`, `prompt`.
- **WebSearch** (`WebSearchInput`) — `query`, optional `allowed_domains`/`blocked_domains`.
- **Workflow** (`WorkflowInput`) — runs a dynamic workflow (Agent SDK v0.3.149+): one of `script`, `name`, or `scriptPath` required; optional `args`, `resumeFromRunId`.
- **Task tools** (`TaskCreateInput`/`TaskUpdateInput`/`TaskGetInput`/`TaskListInput`) — structured task tracking; replace `TodoWriteInput`, which is disabled by default as of SDK 0.3.142.
- **ExitPlanMode** (`ExitPlanModeInput`), **ListMcpResources** (`ListMcpResourcesInput`), **ReadMcpResource** (`ReadMcpResourceInput`), **EnterWorktree** (`EnterWorktreeInput`) — plan exit, MCP resource discovery/read, git worktree entry.

## Tool Output Types

`ToolOutputSchemas` is the union of all built-in tool output types — the actual response data each tool returns. Each member is named `<Tool>Output`. Notable shapes:

- `AgentOutput` — discriminated on `status`: `"completed"` (carries `content`, `usage`, `totalTokens`, optional `resolvedModel`), `"async_launched"` (background, with `outputFile`), `"sub_agent_entered"` (interactive). `resolvedModel` requires Claude Code v2.1.174+.
- `BashOutput` — `stdout`/`stderr` split, `interrupted`, optional `backgroundTaskId`, `rawOutputPath`, `structuredContent`, etc.
- `FileEditOutput` / `FileWriteOutput` — structured diff (`structuredPatch`), `originalFile`, optional `gitDiff`.
- `FileReadOutput` — discriminated on `type`: `"text"`, `"image"`, `"notebook"`, `"pdf"`, `"parts"`.
- `GlobOutput`/`GrepOutput` — file lists and (for Grep) content/count modes.
- `WebFetchOutput`/`WebSearchOutput` — fetched content with HTTP metadata; web results.
- `WorkflowOutput` — `status: "async_launched"` always; final result arrives later as a task completion. Check `error` (set when the script fails its syntax check) before treating the run as started.
- `TaskCreateOutput`/`TaskUpdateOutput`/`TaskGetOutput`/`TaskListOutput`/`TaskStopOutput`, `ExitPlanModeOutput`, `MonitorOutput`, `ListMcpResourcesOutput`, `ReadMcpResourceOutput`, `EnterWorktreeOutput`, `TodoWriteOutput` — round out the union.

## Permission Types

The typed primitives of the permission system:

- `PermissionMode` — `"default" | "acceptEdits" | "bypassPermissions" | "plan" | "dontAsk" | "auto"`. `auto` uses a model classifier to approve/deny each tool call; `bypassPermissions` still prompts on explicit ask rules.
- `CanUseTool` — a custom permission callback `(toolName, input, options) => Promise<PermissionResult>`. The `options` carry `signal`, `suggestions` (`PermissionUpdate[]`), `blockedPath`, `decisionReason`, `toolUseID`, `agentID`.
- `PermissionResult` — discriminated on `behavior`: `"allow"` (optional `updatedInput`, `updatedPermissions`) or `"deny"` (`message`, optional `interrupt`).
- `PermissionUpdate` — union of `addRules`/`replaceRules`/`removeRules` (each with `rules`, `behavior`, `destination`), `setMode`, `addDirectories`/`removeDirectories`.
- `PermissionBehavior` — `"allow" | "deny" | "ask"`.
- `PermissionUpdateDestination` — `"userSettings" | "projectSettings" | "localSettings" | "session" | "cliArg"`.
- `PermissionRuleValue` — `{ toolName: string; ruleContent?: string }`.
- `ToolConfig` — built-in tool behavior config (currently `askUserQuestion.previewFormat: "markdown" | "html"`).

`CanUseTool` is the central control-point type an embedding app implements to gate each tool call:

```typescript
type CanUseTool = (
  toolName: string,
  input: Record<string, unknown>,
  options: {
    signal: AbortSignal;
    suggestions?: PermissionUpdate[];
    blockedPath?: string;
    decisionReason?: string;
    toolUseID: string;
    agentID?: string;
  }
) => Promise<PermissionResult>;
```

## Agent, MCP & Config / Metadata Types

The remaining config and introspection records (drawn from the `Types` and `Other Types` sections):

- `AgentDefinition` — a programmatically defined subagent: required `description` + `prompt`; optional `tools`/`disallowedTools`, `model`, `mcpServers` (`AgentMcpServerSpec[]`), `skills`, `initialPrompt`, `maxTurns`, `background`, `memory`, `effort`, `permissionMode`.
- `AgentMcpServerSpec` — `string | Record<string, McpServerConfigForProcessTransport>`; names a parent server or inlines one.
- `AgentInfo` — introspection record for an invocable subagent: `name`, `description`, optional `model`.
- `McpServerConfig` — union of transports: `McpStdioServerConfig`, `McpSSEServerConfig`, `McpHttpServerConfig`, `McpSdkServerConfigWithInstance` (plus `McpClaudeAIProxyServerConfig` in the status variant).
- `McpServerStatus` / `McpServerStatusConfig` — connected-server status (`"connected" | "failed" | "needs-auth" | "pending" | "disabled"`) with tool annotations and the reported config union.
- `SdkPluginConfig` — `{ type: "local"; path; skipMcpDiscovery? }`; loads a local plugin's skills/hooks/agents/commands (and optionally its MCP servers).
- `ModelInfo` — available-model metadata: `value`, `displayName`, `description`, optional `supportsEffort`, `supportedEffortLevels`, `supportsAdaptiveThinking`, `supportsFastMode`.
- `Usage` / `NonNullableUsage` / `ModelUsage` — token-usage stats; `ModelUsage.costUSD` is a client-side estimate.
- `CallToolResult` — MCP tool result (from `@modelcontextprotocol/sdk`): `content[]`, optional `structuredContent`, `isError`.
- `ThinkingConfig` — `{ type: "adaptive" }` (Opus 4.6+) | `{ type: "enabled"; budgetTokens? }` | `{ type: "disabled" }`, with optional `display: "summarized" | "omitted"`.

> Field-level tables for every type above are in the live reference at the `source_url`; this catalog indexes the type *names* and their role.

**Source**: https://code.claude.com/docs/en/agent-sdk/typescript
**Last Updated**: 2026-06-13
**Status**: Active
