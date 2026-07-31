---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - tool_access
keywords:
  - mcp tool name format
  - mcp__server__tool
  - allowed tools
  - disallowed tools
  - availability vs permission
  - remove built-in tools
  - tools option
  - sdk tool access control
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/custom-tools
access_control_group: ["general"]
---

# Agent SDK — Control Tool Access

## Overview

Once you register an MCP server and its tools with the Agent SDK, you control which tools Claude can use through two distinct layers — **availability** (whether a tool appears in Claude's context at all) and **permission** (whether a call is approved once Claude attempts it). This note covers the `mcp__{server_name}__{tool_name}` name format that addresses MCP tools and how the `tools`, `allowedTools`, and `disallowedTools` options act on those two layers. The full permission-evaluation order is owned by the SDK permissions page (linked out, not duplicated here).

## Tool name format

When MCP tools are exposed to Claude, their names follow a specific format:

- **Pattern:** `mcp__{server_name}__{tool_name}`
- **Example:** A tool named `get_temperature` in server `weather` becomes `mcp__weather__get_temperature`

All the access-control options below are written against these fully qualified MCP names.

## Configure allowed tools

The `tools` option and the allowed/disallowed lists affect two layers:

- **Availability** — controls whether a tool appears in Claude's context. The `tools` option and bare-name `disallowedTools` entries change availability.
- **Permission** — controls whether a call is approved once Claude attempts it. `allowedTools` and scoped `disallowedTools` rules change permission only.

The table below summarizes how each option behaves:

| Option | Layer | Effect |
| :--- | :--- | :--- |
| `tools: ["Read", "Grep"]` | Availability | Only the listed built-ins are in Claude's context. Unlisted built-ins are removed. MCP tools are unaffected. |
| `tools: []` | Availability | All built-ins are removed. Claude can only use your MCP tools. |
| allowed tools | Permission | Listed tools run without a permission prompt. Unlisted tools remain available; calls go through the permission flow. |
| disallowed tools | Both | A bare tool name such as `"Bash"` removes the tool from Claude's context, the same as omitting it from `tools`. A scoped rule such as `"Bash(rm *)"` leaves the tool in context and denies only matching calls. |

## Removing built-ins versus scoped denials

To remove a built-in entirely, omit it from `tools` or list its bare name in `disallowedTools` (Python: `disallowed_tools`); both keep the tool out of context so Claude never attempts it. A scoped `disallowedTools` rule blocks matching calls but leaves the tool visible, so Claude may waste a turn trying it.

For the full evaluation order across `allowedTools`, `disallowedTools`, and permission modes, see [Configure permissions](https://code.claude.com/docs/en/agent-sdk/permissions).

**Source**: https://code.claude.com/docs/en/agent-sdk/custom-tools
**Last Updated**: 2026-06-13
**Status**: Active
