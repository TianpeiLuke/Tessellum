---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - python
keywords:
  - tool input output schemas
  - built-in tools
  - claude-agent-sdk
  - sandbox settings
  - sandbox network config
  - unsandboxed commands
  - dangerouslydisablesandbox
  - permissions fallback
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

# Claude Code Python SDK — Tool I/O Schemas and Sandbox Configuration

## Overview

This note documents two parts of the `claude-agent-sdk` Python reference: the **input/output schemas of Claude Code's built-in tools** and the **sandbox configuration types**. The Python SDK does not export the tool schemas as types — they describe the dict structure of tool inputs and outputs as they appear in messages (the `ToolUseBlock`/`ToolResultBlock` content blocks). The sandbox types (`SandboxSettings`, `SandboxNetworkConfig`, `SandboxIgnoreViolations`) are `TypedDict` objects passed via the `sandbox` field of `ClaudeAgentOptions` to enable command sandboxing and configure network restrictions programmatically.

The built-in tools are the file, exec, search, web, task, and MCP-resource capabilities Claude uses to act; the sandbox layer isolates command execution and, when configured, routes unsandboxable commands back through the permission system. Configuration semantics live in [`cc_sdk_python_options_and_config_types`](cc_sdk_python_options_and_config_types.md); this note documents the I/O contracts and sandbox dicts themselves.

## Tool Input/Output Types

These describe the structure of tool inputs and outputs in messages. The SDK does not export them as types.

### File and execution tools

| Tool name | Input (key fields) | Output (key fields) |
|---|---|---|
| `Bash` | `command: str`; `timeout: int\|None` (ms, max 600000); `description: str\|None`; `run_in_background: bool\|None` | `output: str` (combined stdout+stderr); `exitCode: int`; `killed: bool\|None`; `shellId: str\|None` |
| `BashOutput` | `bash_id: str`; `filter: str\|None` (regex) | `output: str` (new output); `status: "running"\|"completed"\|"failed"`; `exitCode: int\|None` |
| `KillBash` | `shell_id: str` | `message: str`; `shell_id: str` |
| `Monitor` | `command: str` (each stdout line is an event); `description: str`; `timeout_ms: int\|None` (default 300000, max 3600000); `persistent: bool\|None` | `taskId: str`; `timeoutMs: int` (0 when persistent); `persistent: bool\|None` |
| `Read` | `file_path: str`; `offset: int\|None`; `limit: int\|None` | Text: `content: str`, `total_lines: int`, `lines_returned: int`. Images: `image: str` (base64), `mime_type: str`, `file_size: int` |
| `Write` | `file_path: str`; `content: str` | `message: str`; `bytes_written: int`; `file_path: str` |
| `Edit` | `file_path: str`; `old_string: str`; `new_string: str`; `replace_all: bool\|None` (default False) | `message: str`; `replacements: int`; `file_path: str` |
| `NotebookEdit` | `notebook_path: str`; `cell_id: str\|None`; `new_source: str`; `cell_type: "code"\|"markdown"\|None`; `edit_mode: "replace"\|"insert"\|"delete"\|None` | `message: str`; `edit_type: "replaced"\|"inserted"\|"deleted"`; `cell_id: str\|None`; `total_cells: int` |
| `Glob` | `pattern: str`; `path: str\|None` (defaults to cwd) | `matches: list[str]`; `count: int`; `search_path: str` |
| `Grep` | `pattern: str`; `path`/`glob`/`type`/`output_mode`/`-i`/`-n`/`-B`/`-A`/`-C`/`head_limit`/`multiline` (all optional) | content mode: `matches: [...]`, `total_matches: int`. files_with_matches mode: `files: list[str]`, `count: int` |

The `Grep` output `matches` entries carry `file`, `line_number`, `line`, `before_context`, and `after_context`. `output_mode` is `"content"`, `"files_with_matches"`, or `"count"`.

### Web, planning, and MCP-resource tools

| Tool name | Input (key fields) | Output (key fields) |
|---|---|---|
| `WebFetch` | `url: str`; `prompt: str` | `bytes: int`; `code: int`; `codeText: str`; `result: str`; `durationMs: int`; `url: str` |
| `WebSearch` | `query: str`; `allowed_domains: list[str]\|None`; `blocked_domains: list[str]\|None` | `query: str`; `results: list[...]`; `durationSeconds: float` |
| `ExitPlanMode` | `plan: str` | `message: str`; `approved: bool\|None` |
| `AskUserQuestion` | `questions: [...]` (1-4; each has `question`, `header` max 12 chars, `options` 2-4 with `label`/`description`, `multiSelect`); `answers: dict\|None` (populated by permission system) | `questions: [...]`; `answers: dict[str, str]` (multi-select comma-separated) |
| `ListMcpResources` (tool name `ListMcpResourcesTool`) | `server: str\|None` (filter) | `resources: [...]` (`uri`, `name`, `description`, `mimeType`, `server`); `total: int` |
| `ReadMcpResource` (tool name `ReadMcpResourceTool`) | `server: str`; `uri: str` | `contents: [...]` (`uri`, `mimeType`, `text`, `blob`); `server: str` |

`AskUserQuestion` asks the user clarifying questions during execution. Its answers are populated by the permission system; multi-select answers may be a list of labels or a comma-joined string.

### Task tracking tools

> As of Claude Code v2.1.142, `TodoWrite` is disabled by default. Use `TaskCreate`, `TaskGet`, `TaskUpdate`, and `TaskList` instead, or set `CLAUDE_CODE_ENABLE_TASKS=0` to revert to `TodoWrite`.

| Tool name | Input (key fields) | Output (key fields) |
|---|---|---|
| `TaskCreate` | `subject: str`; `description: str`; `activeForm: str\|None`; `metadata: dict\|None` | `task: {"id": str, "subject": str}` |
| `TaskUpdate` | `taskId: str`; `status`/`subject`/`description`/`activeForm`/`owner`/`metadata` (optional); `addBlocks`/`addBlockedBy: list[str]\|None` | `success: bool`; `taskId: str`; `updatedFields: list[str]`; `error: str\|None`; `statusChange: {...}\|None` |
| `TaskGet` | `taskId: str` | `task: {...}\|None` (`id`, `subject`, `description`, `status`, `blocks`, `blockedBy`); `None` when ID not found |
| `TaskList` | `{}` | `tasks: [...]` (each `id`, `subject`, `status`, `owner`, `blockedBy`) |
| `TodoWrite` | `todos: [...]` (each `content`, `status` pending/in_progress/completed, `activeForm`) | `message: str`; `stats: {total, pending, in_progress, completed}` |

### Agent tool

The `Agent` tool (previously `Task`, which is still accepted as an alias) spawns a specialized subagent. Its input/output is shown verbatim:

```python theme={null}
# Input
{
    "description": str,  # A short (3-5 word) description of the task
    "prompt": str,  # The task for the agent to perform
    "subagent_type": str,  # The type of specialized agent to use
}

# Output
{
    "result": str,  # Final result from the subagent
    "usage": dict | None,  # Token usage statistics
    "total_cost_usd": float | None,  # Estimated total cost in USD
    "duration_ms": int | None,  # Execution duration in milliseconds
}
```

## Sandbox Configuration

`SandboxSettings`, `SandboxNetworkConfig`, and `SandboxIgnoreViolations` are passed via the `sandbox` field of `ClaudeAgentOptions` to enable command sandboxing and configure network restrictions programmatically.

### `SandboxSettings`

```python theme={null}
class SandboxSettings(TypedDict, total=False):
    enabled: bool
    autoAllowBashIfSandboxed: bool
    excludedCommands: list[str]
    allowUnsandboxedCommands: bool
    network: SandboxNetworkConfig
    ignoreViolations: SandboxIgnoreViolations
    enableWeakerNestedSandbox: bool
```

| Property | Type | Default | Description |
|---|---|---|---|
| `enabled` | `bool` | `False` | Enable sandbox mode for command execution |
| `autoAllowBashIfSandboxed` | `bool` | `True` | Auto-approve bash commands when sandbox is enabled |
| `excludedCommands` | `list[str]` | `[]` | Commands that always bypass sandbox restrictions (e.g., `["docker"]`); run unsandboxed automatically without model involvement |
| `allowUnsandboxedCommands` | `bool` | `True` | Allow the model to request running commands outside the sandbox. When `True`, the model can set `dangerouslyDisableSandbox` in tool input, falling back to the permissions system |
| `network` | `SandboxNetworkConfig` | `None` | Network-specific sandbox configuration |
| `ignoreViolations` | `SandboxIgnoreViolations` | `None` | Configure which sandbox violations to ignore |
| `enableWeakerNestedSandbox` | `bool` | `False` | Enable a weaker nested sandbox for compatibility |

The sandbox depends on platform support and, on Linux, tools like `bubblewrap` and `socat`. By default, when `enabled` is `True` but the sandbox can't start, commands run unsandboxed with a warning on stderr — differing from the TypeScript SDK, where `failIfUnavailable` defaults to `true`. Set `"failIfUnavailable": True` to stop instead (the SDK forwards the undeclared key to Claude Code, which honors it); `query()` then reports a `ResultMessage` with `subtype="error_during_execution"` and the reason in `errors`.

### `SandboxNetworkConfig`

Network settings for sandboxed Bash commands when `enabled` is `True`. They do not restrict the `WebFetch` tool, which uses permission rules instead.

```python theme={null}
class SandboxNetworkConfig(TypedDict, total=False):
    allowedDomains: list[str]
    deniedDomains: list[str]
    allowManagedDomainsOnly: bool
    allowUnixSockets: list[str]
    allowAllUnixSockets: bool
    allowLocalBinding: bool
    allowMachLookup: list[str]
    httpProxyPort: int
    socksProxyPort: int
```

| Property | Default | Description |
|---|---|---|
| `allowedDomains` | `[]` | Domains sandboxed processes can access |
| `deniedDomains` | `[]` | Domains sandboxed processes cannot access; takes precedence over `allowedDomains` |
| `allowManagedDomainsOnly` | `False` | Managed-settings only; no effect when set via SDK options |
| `allowUnixSockets` | `[]` | Unix socket paths processes can access (e.g., Docker socket) |
| `allowAllUnixSockets` | `False` | Allow access to all Unix sockets |
| `allowLocalBinding` | `False` | Allow binding to local ports (e.g., dev servers) |
| `allowMachLookup` | `[]` | macOS only: XPC/Mach service names to allow (trailing wildcard supported) |
| `httpProxyPort` | `None` | HTTP proxy port for network requests |
| `socksProxyPort` | `None` | SOCKS proxy port for network requests |

**Unix socket security**: `allowUnixSockets` can grant access to powerful system services — allowing `/var/run/docker.sock` effectively grants full host access via the Docker API, bypassing sandbox isolation. The built-in sandbox proxy enforces the allowlist by requested hostname and does not terminate or inspect TLS traffic, so techniques such as domain fronting can potentially bypass it.

### `SandboxIgnoreViolations`

```python theme={null}
class SandboxIgnoreViolations(TypedDict, total=False):
    file: list[str]
    network: list[str]
```

`file` (default `[]`) holds file-path patterns to ignore violations for; `network` (default `[]`) holds network patterns to ignore violations for.

### Permissions Fallback for Unsandboxed Commands

When `allowUnsandboxedCommands` is enabled, the model can request to run commands outside the sandbox by setting `dangerouslyDisableSandbox: True` in the tool input. These requests fall back to the existing permissions system, invoking your `can_use_tool` handler so you can implement custom authorization logic.

`excludedCommands` vs `allowUnsandboxedCommands`: `excludedCommands` is a static list that always bypasses the sandbox automatically (the model has no control); `allowUnsandboxedCommands` lets the model decide at runtime whether to request unsandboxed execution via `dangerouslyDisableSandbox: True`.

```python theme={null}
async def can_use_tool(
    tool: str, input: dict, context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    # Check if the model is requesting to bypass the sandbox
    if tool == "Bash" and input.get("dangerouslyDisableSandbox"):
        if is_command_authorized(input.get("command")):
            return PermissionResultAllow()
        return PermissionResultDeny(
            message="Command not authorized for unsandboxed execution"
        )
    return PermissionResultAllow()
```

This pattern enables auditing model requests, implementing allowlists, and adding approval workflows. Commands running with `dangerouslyDisableSandbox: True` have full system access, so the `can_use_tool` handler must validate them carefully. If `permission_mode` is `bypassPermissions` and `allowUnsandboxedCommands` is enabled, the model can autonomously execute unsandboxed commands without prompts (an explicit `ask` rule still forces one) — effectively allowing it to escape sandbox isolation silently.

**Source**: https://code.claude.com/docs/en/agent-sdk/python
**Last Updated**: 2026-06-13
**Status**: Active
