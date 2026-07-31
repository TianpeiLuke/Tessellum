---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - tool_execution
keywords:
  - agent sdk tool execution
  - built-in tools
  - allowed_tools disallowed_tools
  - permission_mode
  - parallel tool execution
  - readonlyhint
  - tool capability ladder
  - mcp tools
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/agent-loop
access_control_group: ["general"]
---

# Agent SDK — Tool Execution

## Overview

Tools give an Agent SDK agent the ability to take action. Without tools, Claude can only respond with text; with tools it can read files, run commands, search code, and interact with external services. This note covers the SDK's **built-in tool set**, how three options (`allowed_tools` / `disallowed_tools` / `permission_mode`) interact to decide which tool calls run, and how the SDK runs multiple tool calls in a turn either **in parallel** (read-only tools) or **sequentially** (state-modifying tools).

The same set of tools that powers Claude Code ships with the SDK. Tool execution is the action half of the [agent loop](cc_agent_sdk_agent_loop.md): Claude requests tools, the SDK runs each requested tool and collects the results, and those results feed back to Claude for the next decision. The full permission-mode reference lives in the [loop controls](cc_agent_sdk_loop_controls.md) note; the complete rule syntax is in the permissions reference linked below.

## Built-in tools

The SDK includes the same tools that power Claude Code, grouped into six categories:

| Category | Tools | What they do |
| :--- | :--- | :--- |
| **File operations** | `Read`, `Edit`, `Write` | Read, modify, and create files |
| **Search** | `Glob`, `Grep` | Find files by pattern, search content with regex |
| **Execution** | `Bash` | Run shell commands, scripts, git operations |
| **Web** | `WebSearch`, `WebFetch` | Search the web, fetch and parse pages |
| **Discovery** | `ToolSearch` | Dynamically find and load tools on-demand instead of preloading all of them |
| **Orchestration** | `Agent`, `Skill`, `AskUserQuestion`, `TaskCreate`, `TaskUpdate` | Spawn subagents, invoke skills, ask the user, track tasks |

Beyond built-in tools, you can:

- **Connect external services** with MCP servers (databases, browsers, APIs) — see [`/agent-sdk/mcp`](https://code.claude.com/docs/en/agent-sdk/mcp).
- **Define custom tools** with custom tool handlers — see [`/agent-sdk/custom-tools`](https://code.claude.com/docs/en/agent-sdk/custom-tools).
- **Load project skills** via setting sources for reusable workflows — see [`cc_agent_sdk_settingsources_and_features`](cc_agent_sdk_settingsources_and_features.md).

### The tool capability ladder

Which tools you grant via `allowed_tools` defines what the agent can do. The quickstart frames this as a ladder of escalating capability:

| Tools | What the agent can do |
| :--- | :--- |
| `Read`, `Glob`, `Grep` | Read-only analysis |
| `Read`, `Edit`, `Glob` | Analyze and modify code |
| `Read`, `Edit`, `Bash`, `Glob`, `Grep` | Full automation |

## Tool permissions

Claude determines which tools to call based on the task, but you control whether those calls are allowed to execute. You can auto-approve specific tools, block others entirely, or require approval for everything. Three options work together to determine what runs:

- **`allowed_tools` / `allowedTools`** auto-approves listed tools. A read-only agent with `["Read", "Glob", "Grep"]` in its allowed tools list runs those tools without prompting. Tools not listed are still available but require permission.
- **`disallowed_tools` / `disallowedTools`** blocks listed tools, regardless of other settings.
- **`permission_mode` / `permissionMode`** controls what happens to tools that aren't covered by allow or deny rules. See the [loop controls](cc_agent_sdk_loop_controls.md) note for the available modes.

You can also scope individual tools with rules like `"Bash(npm *)"` to allow only specific commands. The full rule syntax and the order rules are checked before a tool runs are documented in the permissions reference: [`/agent-sdk/permissions`](https://code.claude.com/docs/en/agent-sdk/permissions).

When a tool is denied, Claude receives a rejection message as the tool result and typically attempts a different approach or reports that it couldn't proceed.

## Parallel tool execution

When Claude requests multiple tool calls in a single turn, both SDKs can run them concurrently or sequentially depending on the tool:

- **Read-only tools** (like `Read`, `Glob`, `Grep`, and MCP tools marked as read-only) can run **concurrently**.
- **Tools that modify state** (like `Edit`, `Write`, and `Bash`) run **sequentially** to avoid conflicts.

Custom tools default to sequential execution. To enable parallel execution for a custom tool, set `readOnlyHint` in its annotations. Both the TypeScript and Python SDKs use this field name from the MCP SDK.

**Source**: https://code.claude.com/docs/en/agent-sdk/agent-loop
**Last Updated**: 2026-06-13
**Status**: Active
