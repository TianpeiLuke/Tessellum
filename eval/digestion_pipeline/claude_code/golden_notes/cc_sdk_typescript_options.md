---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - typescript
keywords:
  - options config object
  - query() configuration
  - permissionmode allowedtools
  - mcpservers strictmcpconfig
  - env replace not merge
  - api timeout stall env vars
  - maxturns maxbudgetusd
  - settingsources
topics:
  - Claude Code
  - Agent SDK TypeScript
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/typescript
access_control_group: ["general"]
---

# Agent SDK (TypeScript) — The `Options` Configuration Object

## Overview

`Options` is the optional configuration object passed to the TypeScript Agent SDK's `query()` function (and to `startup()`). It is a flat TypeScript interface of ~50 typed keys that tune every behavior of the spawned Claude Code session — model selection and reasoning effort, which tools are exposed and auto-approved, permission mode and custom permission gates, MCP servers, subagents, session persistence and resume, sandboxing, settings sources, and turn/budget caps. Every key is optional and has a documented default; this note groups the high-traffic keys by purpose and flags two procedural gotchas (the `env` replace-not-merge behavior and the API-timeout/stall environment variables). The full ~50-row table is on the live `source_url`; this note is a navigable index, not a re-dump.

## Option Keys Grouped by Purpose

### Model, effort, and thinking

| Key | Type | Default | Purpose |
|---|---|---|---|
| `model` | `string` | Default from CLI | Claude model alias or full model name. |
| `fallbackModel` | `string` | `undefined` | Model to use if the primary model fails. |
| `effort` | `'low' \| 'medium' \| 'high' \| 'xhigh' \| 'max'` | Model default | How much effort Claude puts into a response; works with adaptive thinking to guide thinking depth. |
| `thinking` | `ThinkingConfig` | `{ type: 'adaptive' }` (supported models) | Controls Claude's thinking/reasoning behavior. |
| `maxThinkingTokens` | `number` | `undefined` | *Deprecated:* use `thinking` instead. |

### Tools and tool access

| Key | Type | Default | Purpose |
|---|---|---|---|
| `tools` | `string[] \| { type: 'preset'; preset: 'claude_code' }` | `undefined` | Tool configuration; array of names or the preset for Claude Code's default tools. |
| `allowedTools` | `string[]` | `[]` | Tools to auto-approve without prompting. Does **not** restrict Claude to only these tools; unlisted tools fall through to `permissionMode` and `canUseTool`. |
| `disallowedTools` | `string[]` | `[]` | Tools to deny. A bare name like `"Bash"` removes the tool from Claude's context; a scoped rule like `"Bash(rm *)"` keeps the tool but denies matching calls in every mode (including `bypassPermissions`). |
| `toolConfig` | `ToolConfig` | `undefined` | Configuration for built-in tool behavior. |
| `toolAliases` | `Record<string, string>` | `undefined` | Map built-in tool names to MCP tool names (e.g. `{ Bash: 'mcp__workspace__bash' }`). |
| `skills` | `string[] \| 'all'` | `undefined` | Skills available to the session; pass `'all'` or a list. When set, the SDK adds the `Skill` tool to `allowedTools` automatically. |

### Permissions

| Key | Type | Default | Purpose |
|---|---|---|---|
| `permissionMode` | `PermissionMode` | `'default'` | Permission mode for the session. |
| `canUseTool` | `CanUseTool` | `undefined` | Custom permission function for tool usage. |
| `allowDangerouslySkipPermissions` | `boolean` | `false` | Enable bypassing permissions; required for `permissionMode: 'bypassPermissions'`. |
| `permissionPromptToolName` | `string` | `undefined` | MCP tool name for permission prompts. |
| `planModeInstructions` | `string` | `undefined` | Custom plan-mode workflow body when `permissionMode` is `'plan'`. |

### MCP servers, agents, plugins

| Key | Type | Default | Purpose |
|---|---|---|---|
| `mcpServers` | `Record<string, McpServerConfig>` | `{}` | MCP server configurations. |
| `strictMcpConfig` | `boolean` | `false` | Use only servers passed in `mcpServers`; ignore project `.mcp.json`, user settings, plugin-provided servers, and claude.ai connectors. |
| `agents` | `Record<string, AgentDefinition>` | `undefined` | Programmatically define subagents. |
| `agent` | `string` | `undefined` | Agent name for the main thread (must be defined in `agents` or settings). |
| `agentProgressSummaries` | `boolean` | `false` | Generate one-line progress summaries for subagents, forwarded on `task_progress` events. |
| `forwardSubagentText` | `boolean` | `false` | Forward subagent text/thinking blocks as messages with `parent_tool_use_id` set, so consumers can render a nested transcript. |
| `plugins` | `SdkPluginConfig[]` | `[]` | Load custom plugins from local paths. |
| `onElicitation` | callback | `undefined` | Handle MCP elicitation requests when no hook handles them first; unhandled requests are declined automatically. |

### Hooks and message stream

| Key | Type | Default | Purpose |
|---|---|---|---|
| `hooks` | `Partial<Record<HookEvent, HookCallbackMatcher[]>>` | `{}` | Hook callbacks for events. |
| `includeHookEvents` | `boolean` | `false` | Include hook lifecycle events in the message stream. |
| `includePartialMessages` | `boolean` | `false` | Include partial message events. |
| `promptSuggestions` | `boolean` | `false` | Emit a `prompt_suggestion` message after each turn. |
| `outputFormat` | `{ type: 'json_schema', schema: JSONSchema }` | `undefined` | Define a structured output format for agent results. |

### Sessions and persistence

| Key | Type | Default | Purpose |
|---|---|---|---|
| `sessionId` | `string` | Auto-generated | Use a specific UUID instead of auto-generating. |
| `resume` | `string` | `undefined` | Session ID to resume. |
| `resumeSessionAt` | `string` | `undefined` | Resume a session at a specific message UUID. |
| `forkSession` | `boolean` | `false` | When resuming, fork to a new session ID instead of continuing the original. |
| `continue` | `boolean` | `false` | Continue the most recent conversation. |
| `persistSession` | `boolean` | `true` | When `false`, disable disk persistence; the session cannot be resumed. |
| `sessionStore` | `SessionStore` | `undefined` | Mirror transcripts to an external backend so any host can resume them. |
| `title` | `string` | `undefined` | Display title for the session. |

### Budget, turns, and system prompt (context shaping)

| Key | Type | Default | Purpose |
|---|---|---|---|
| `maxTurns` | `number` | `undefined` | Maximum agentic turns (tool-use round trips). |
| `maxBudgetUsd` | `number` | `undefined` | Stop the query when the client-side cost estimate reaches this USD value (compared against the same estimate as `total_cost_usd`). |
| `taskBudget` | `{ total: number }` | `undefined` | *Alpha.* API-side token budget; the model is told its remaining budget so it can pace and wrap up. |
| `systemPrompt` | `string \| { type: 'preset'; preset: 'claude_code'; append?; excludeDynamicSections? }` | `undefined` (minimal prompt) | System prompt config. The preset form uses Claude Code's prompt; `append` extends it; `excludeDynamicSections: true` moves per-session context into the first user message for better prompt-cache reuse across machines. |

### Settings sources

`settings` (`string \| Settings`) supplies an inline settings object or a path to a settings file and populates the flag-settings layer of the precedence order (changeable at runtime with `applyFlagSettings()` — see [`cc_sdk_typescript_query_object`](cc_sdk_typescript_query_object.md)). `settingSources` (`SettingSource[]`) controls which filesystem settings (`"user" | "project" | "local"`) load; pass `[]` to disable user/project/local settings, and note that managed policy settings load regardless. The default (omitted) loads all three, matching the CLI.

### Sandbox (TS shape)

`sandbox` (`SandboxSettings`, default `undefined`) configures command sandboxing programmatically. The type's high-level shape:

```typescript theme={null}
type SandboxSettings = {
  enabled?: boolean;
  failIfUnavailable?: boolean;
  autoAllowBashIfSandboxed?: boolean;
  excludedCommands?: string[];
  allowUnsandboxedCommands?: boolean;
  network?: SandboxNetworkConfig;
  filesystem?: SandboxFilesystemConfig;
  ignoreViolations?: Record<string, string[]>;
  enableWeakerNestedSandbox?: boolean;
  ripgrep?: { command: string; args?: string[] };
};
```

`enabled` turns sandboxing on (`failIfUnavailable: false` falls back to unsandboxed with a stderr warning), `excludedCommands` always bypass the sandbox automatically, and `allowUnsandboxedCommands` lets the model request unsandboxed execution via `dangerouslyDisableSandbox: true` in tool input — which then falls through to your `canUseTool` handler. `network` (`SandboxNetworkConfig` — `allowedDomains`/`deniedDomains`/`allowLocalBinding`/`allowUnixSockets`/proxy ports) and `filesystem` (`SandboxFilesystemConfig` — `allowWrite`/`denyWrite`/`denyRead`) carry the per-domain detail. The full field tables and the sandboxing **concept** live on the [source page](https://code.claude.com/docs/en/agent-sdk/typescript) and the [Sandboxing](https://code.claude.com/docs/en/sandboxing) / [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment) pages.

### Process, environment, and runtime

Remaining keys cover the spawned process and execution environment: `abortController`, `cwd`, `additionalDirectories`, `executable` (`'bun' | 'deno' | 'node'`), `executableArgs`, `extraArgs`, `pathToClaudeCodeExecutable`, `spawnClaudeCodeProcess` (run Claude Code in VMs/containers/remote), `stderr` callback, `debug`/`debugFile`, `enableFileCheckpointing` (enables `rewindFiles()`), `betas`, `loadTimeoutMs`/`sessionStoreFlush` (alpha, `sessionStore`-only), and `managedSettings`. See the [source page](https://code.claude.com/docs/en/agent-sdk/typescript) for the exhaustive table.

## The `env` Replace-Not-Merge Gotcha

`env` (`Record<string, string | undefined>`, default `process.env`) sets environment variables for the subprocess. **When set, it replaces the subprocess environment instead of merging with `process.env`.** To keep inherited variables like `PATH`, spread `process.env` first:

```typescript theme={null}
options: {
  env: { ...process.env, YOUR_VAR: 'value' },
}
```

Setting `CLAUDE_AGENT_SDK_CLIENT_APP` in `env` identifies your app in the User-Agent header.

## Handle Slow or Stalled API Responses

The CLI subprocess reads several environment variables that control API timeouts and stall detection. Pass them through the `env` option (remembering the spread-`process.env` pattern above):

```typescript theme={null}
const result = query({
  prompt: "Analyze this code",
  options: {
    env: {
      ...process.env,
      API_TIMEOUT_MS: "120000",
      CLAUDE_CODE_MAX_RETRIES: "2",
      CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS: "120000",
    },
  },
});
```

- `API_TIMEOUT_MS`: per-request timeout on the Anthropic client (ms). Default `600000`. Applies to the main loop and all subagents.
- `CLAUDE_CODE_MAX_RETRIES`: maximum API retries. Default `10`. Each retry gets its own `API_TIMEOUT_MS` window, so worst-case wall time is roughly `API_TIMEOUT_MS × (CLAUDE_CODE_MAX_RETRIES + 1)` plus backoff.
- `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`: stall watchdog for subagents launched with `run_in_background`. Default `600000`. Resets on each stream event; on stall it aborts the subagent, marks the task failed, and surfaces the error to the parent with any partial result. Does not apply to synchronous subagents.
- `CLAUDE_ENABLE_STREAM_WATCHDOG=1` with `CLAUDE_STREAM_IDLE_TIMEOUT_MS`: aborts the request when headers have arrived but the body stops streaming. Unset, the default is server-controlled on the direct Anthropic API and off on other providers. `CLAUDE_STREAM_IDLE_TIMEOUT_MS` defaults to `300000` and is clamped to that minimum; the aborted request goes through the normal retry path.

**Source**: https://code.claude.com/docs/en/agent-sdk/typescript
**Last Updated**: 2026-06-13
**Status**: Active
