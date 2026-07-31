---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - configuration
keywords:
  - claudeagentoptions
  - python agent sdk options
  - permission mode
  - mcp server config
  - agentdefinition subagent
  - thinkingconfig effort level
  - setting sources
  - timeout env vars
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/python
access_control_group: ["general"]
---

# Claude Agent SDK (Python) — `ClaudeAgentOptions` and Config Types

## Overview

`ClaudeAgentOptions` is the master configuration dataclass for a Python Agent SDK run — passed as `options=` to [`query()`](cc_sdk_python_entry_points.md) and `ClaudeSDKClient`. Nearly every Claude Code feature (tools, permissions, MCP servers, subagents, skills, thinking, sandbox, session control) surfaces as a field here. This note documents that dataclass field-by-field plus the **companion config types** it references — the permission types (`PermissionMode`, `CanUseTool`, `PermissionResult*`, `PermissionUpdate`, `PermissionRuleValue`, `ToolPermissionContext`), prompt/setting types (`SystemPromptPreset`, `SettingSource`, `OutputFormat`, `ToolsPreset`), the subagent/thinking types (`AgentDefinition`, `ThinkingConfig`, `EffortLevel`), the MCP-config family (`McpServerConfig` and variants), and `Transport`, `SdkMcpTool`, `SdkBeta`, `SdkPluginConfig`.

This is a reference for *what to configure*. The *semantics* live elsewhere: setting sources / system prompts in [SDK sessions](https://code.claude.com/docs/en/agent-sdk/sessions), MCP / custom tools in [custom tools](https://code.claude.com/docs/en/agent-sdk/custom-tools), permissions in [permissions](https://code.claude.com/docs/en/agent-sdk/permissions), and the full `SandboxSettings` family in [cc_sdk_python_tool_io_and_sandbox](cc_sdk_python_tool_io_and_sandbox.md).

> **`@dataclass` vs `TypedDict`:** `@dataclass` types (`ClaudeAgentOptions`, `AgentDefinition`, `PermissionResultAllow`) are runtime objects with attribute access (`result.behavior`). `TypedDict` types (`SystemPromptPreset`, `ThinkingConfigEnabled`, `McpStdioServerConfig`, `ToolsPreset`) are **plain dicts** requiring key access (`config["budget_tokens"]`, not `config.budget_tokens`). The `ClassName(field=value)` call syntax works for both, but only dataclasses produce attributed objects.

## `ClaudeAgentOptions`

The configuration dataclass for Claude Code queries:

```python
@dataclass
class ClaudeAgentOptions:
    tools: list[str] | ToolsPreset | None = None
    allowed_tools: list[str] = field(default_factory=list)
    system_prompt: str | SystemPromptPreset | None = None
    mcp_servers: dict[str, McpServerConfig] | str | Path = field(default_factory=dict)
    strict_mcp_config: bool = False
    permission_mode: PermissionMode | None = None
    continue_conversation: bool = False
    resume: str | None = None
    max_turns: int | None = None
    max_budget_usd: float | None = None
    disallowed_tools: list[str] = field(default_factory=list)
    model: str | None = None
    fallback_model: str | None = None
    betas: list[SdkBeta] = field(default_factory=list)
    output_format: dict[str, Any] | None = None
    can_use_tool: CanUseTool | None = None
    hooks: dict[HookEvent, list[HookMatcher]] | None = None
    fork_session: bool = False
    agents: dict[str, AgentDefinition] | None = None
    setting_sources: list[SettingSource] | None = None
    sandbox: SandboxSettings | None = None
    plugins: list[SdkPluginConfig] = field(default_factory=list)
    thinking: ThinkingConfig | None = None
    effort: EffortLevel | None = None
    enable_file_checkpointing: bool = False
    session_store_flush: SessionStoreFlushMode = "batched"
    # ...cwd, cli_path, settings, add_dirs, env, extra_args, max_buffer_size,
    # stderr, user, include_partial_messages, include_hook_events, skills,
    # session_store, permission_prompt_tool_name, fallback_model, etc.
```

Key fields (selected; full list and per-field defaults in source):

| Field | Type | Purpose |
| :--- | :--- | :--- |
| `tools` / `allowed_tools` / `disallowed_tools` | list / `ToolsPreset` | Tool set, auto-approve list, deny list. `allowed_tools` does **not** restrict to those tools — unlisted tools fall through to `permission_mode` / `can_use_tool`; a scoped deny `"Bash(rm *)"` blocks matching calls in every mode incl. `bypassPermissions`. |
| `system_prompt` | `str` / `SystemPromptPreset` | Custom string or the `claude_code` preset (with optional `append`). |
| `mcp_servers` / `strict_mcp_config` | `dict[str, McpServerConfig]` / `bool` | MCP servers (or config-file path); `strict_mcp_config=True` ignores `.mcp.json`, user settings, plugin servers, and claude.ai connectors. |
| `permission_mode` / `can_use_tool` / `hooks` | `PermissionMode` / `CanUseTool` / hook map | Permission gating, the per-call permission callback, and event interceptors. |
| `continue_conversation` / `resume` / `fork_session` | `bool` / `str` / `bool` | Continue most recent, resume a session ID, or fork to a new ID on resume. |
| `max_turns` / `max_budget_usd` | `int` / `float` | Cap agentic turns; stop when client-side cost estimate hits a USD ceiling. |
| `agents` / `skills` / `plugins` | `dict[str, AgentDefinition]` / list / `list[SdkPluginConfig]` | Programmatic subagents, skill selection (`"all"` or names — auto-adds the `Skill` tool), and local plugin loading. |
| `thinking` / `effort` / `betas` | `ThinkingConfig` / `EffortLevel` / `list[SdkBeta]` | Extended-thinking config, reasoning effort, beta flags. |
| `setting_sources` / `sandbox` / `enable_file_checkpointing` | list / `SandboxSettings` / `bool` | Which filesystem settings to load; programmatic sandbox; file-change tracking for rewind. |

### Handle slow or stalled API responses

The CLI subprocess reads timeout / stall env vars; pass them through `ClaudeAgentOptions.env`:

```python
options = ClaudeAgentOptions(
    env={
        "API_TIMEOUT_MS": "120000",
        "CLAUDE_CODE_MAX_RETRIES": "2",
        "CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS": "120000",
    },
)
```

- `API_TIMEOUT_MS` — per-request timeout (default `600000` ms); applies to main loop and subagents.
- `CLAUDE_CODE_MAX_RETRIES` — max API retries (default `10`); worst-case wall time ≈ `API_TIMEOUT_MS × (retries + 1)` plus backoff.
- `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` — stall watchdog for `run_in_background` subagents (default `600000`); on stall, aborts the subagent and surfaces the error to the parent. Not for synchronous subagents.
- `CLAUDE_ENABLE_STREAM_WATCHDOG=1` + `CLAUDE_STREAM_IDLE_TIMEOUT_MS` — aborts when headers arrived but the body stops streaming (`CLAUDE_STREAM_IDLE_TIMEOUT_MS` default/min `300000`).

## Prompt, output, and setting types

| Type | Form | Shape / values |
| :--- | :--- | :--- |
| `SystemPromptPreset` | `TypedDict` | `{type: "preset", preset: "claude_code", append?: str, exclude_dynamic_sections?: bool}`. `exclude_dynamic_sections` moves per-session context (cwd, git flag, memory paths) into the first user message to improve prompt-cache reuse. |
| `OutputFormat` | dict | `{"type": "json_schema", "schema": {...}}` — pass as the `output_format` field; both keys required. |
| `ToolsPreset` | `TypedDict` | `{type: "preset", preset: "claude_code"}` — Claude Code's default tool set. |
| `SettingSource` | `Literal["user","project","local"]` | `user` = `~/.claude/settings.json`; `project` = `.claude/settings.json`; `local` = `.claude/settings.local.json`. Omitting / `None` loads all three (CLI default); `[]` disables filesystem settings (in SDK 0.1.59 and earlier `[]` was a no-op). Precedence high→low: local > project > user; programmatic options override all three; managed policy settings override programmatic options. |

## Permission types

| Type | Definition |
| :--- | :--- |
| `PermissionMode` | `Literal["default", "acceptEdits", "plan", "dontAsk", "bypassPermissions"]` — `dontAsk` denies anything not pre-approved instead of prompting; `bypassPermissions` skips checks but explicit `ask` rules still prompt. |
| `CanUseTool` | `Callable[[str, dict[str, Any], ToolPermissionContext], Awaitable[PermissionResult]]` — receives `tool_name`, `input_data`, `context`; returns an Allow or Deny. |
| `ToolPermissionContext` | `@dataclass` with `signal`, `suggestions: list[PermissionUpdate]`, `blocked_path`, `decision_reason`, `title`, `display_name`, `description`. |
| `PermissionResult` | `PermissionResultAllow \| PermissionResultDeny`. |
| `PermissionResultAllow` | `@dataclass`: `behavior="allow"`, `updated_input: dict \| None`, `updated_permissions: list[PermissionUpdate] \| None`. |
| `PermissionResultDeny` | `@dataclass`: `behavior="deny"`, `message: str=""`, `interrupt: bool=False`. |
| `PermissionUpdate` | `@dataclass`: `type` (`addRules`/`replaceRules`/`removeRules`/`setMode`/`addDirectories`/`removeDirectories`), `rules`, `behavior` (`allow`/`deny`/`ask`), `mode`, `directories`, `destination` (`userSettings`/`projectSettings`/`localSettings`/`session`). |
| `PermissionRuleValue` | `@dataclass`: `tool_name: str`, `rule_content: str \| None`. |

## Subagent, thinking, and beta types

`AgentDefinition` (`@dataclass`) defines a subagent programmatically. **Field names use camelCase** (`disallowedTools`, `permissionMode`, `maxTurns`) to match the wire format shared with the TypeScript SDK — passing snake_case raises `TypeError`:

```python
@dataclass
class AgentDefinition:
    description: str          # required: when to use this agent
    prompt: str              # required: the agent's system prompt
    tools: list[str] | None = None              # allowed tools (omit = inherit all)
    disallowedTools: list[str] | None = None
    model: str | None = None                     # "sonnet"/"opus"/"haiku"/"inherit"/full ID
    skills: list[str] | None = None              # skills preloaded at startup
    memory: Literal["user", "project", "local"] | None = None
    mcpServers: list[str | dict[str, Any]] | None = None
    initialPrompt: str | None = None
    maxTurns: int | None = None
    background: bool | None = None               # run as non-blocking background task
    effort: EffortLevel | int | None = None
    permissionMode: PermissionMode | None = None
```

- `ThinkingConfig` — union of three `TypedDict`s (plain dicts at runtime): `{type: "adaptive", display?}`, `{type: "enabled", budget_tokens: int, display?}`, `{type: "disabled"}`. `display` is `"summarized"` or `"omitted"` (API default `"omitted"` on Opus 4.7+; set `"summarized"` to receive `ThinkingBlock` content). `thinking` takes precedence over the deprecated `max_thinking_tokens`.
- `EffortLevel` — `Literal["low", "medium", "high", "xhigh", "max"]`; `xhigh` is extended reasoning (Opus 4.8 / 4.7; falls back to `high` elsewhere).
- `SdkBeta` — `Literal["context-1m-2025-08-07"]` (retired 2026-04-30; the 1M context window is now standard on Sonnet 4.6 / Opus 4.6+ without a beta header).

## MCP, transport, and plugin config types

| Type | Form | Shape |
| :--- | :--- | :--- |
| `McpServerConfig` | union | `McpStdioServerConfig \| McpSSEServerConfig \| McpHttpServerConfig \| McpSdkServerConfig`. |
| `McpStdioServerConfig` | `TypedDict` | `type?: "stdio"`, `command: str`, `args?`, `env?`. |
| `McpSSEServerConfig` / `McpHttpServerConfig` | `TypedDict` | `type: "sse"`/`"http"`, `url: str`, `headers?`. |
| `McpSdkServerConfig` | `TypedDict` | `type: "sdk"`, `name: str`, `instance: Any` (in-process server from `create_sdk_mcp_server()`). |
| `McpServerStatusConfig` | union | `McpServerConfig` variants + an output-only `claudeai-proxy` variant; SDK status form drops `instance`. |
| `McpStatusResponse` | `TypedDict` | `{mcpServers: list[McpServerStatus]}` — returned by `get_mcp_status()`. |
| `McpServerStatus` | `TypedDict` | `name`, `status` (`connected`/`failed`/`needs-auth`/`pending`/`disabled`), `serverInfo?`, `error?`, `config?`, `scope?`, `tools?`. |
| `SdkMcpTool` | `@dataclass` (`Generic[T]`) | `name`, `description`, `input_schema`, `handler: Callable[[T], Awaitable[dict]]`, `annotations?` (authoring guide → custom tools). |
| `Transport` | ABC | Low-level custom transport: `connect`, `write`, `read_messages`, `close`, `is_ready`, `end_input`. Internal API; may change. |
| `SdkPluginConfig` | `TypedDict` | `{type: "local", path: str}` — only local plugins currently supported. |

**Source**: https://code.claude.com/docs/en/agent-sdk/python
**Last Updated**: 2026-06-13
**Status**: Active
