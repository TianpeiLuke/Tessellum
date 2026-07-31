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

## Related Notes

### Related Notes (Claude Code Series)

- [Agent SDK — The Agent Loop](cc_agent_sdk_agent_loop.md) — relevance: tool execution is the action half of the loop this note opens with; the loop note covers turns/messages while this note covers what runs *inside* each tool-call step.
- [Agent SDK — Controlling How the Loop Runs](cc_agent_sdk_loop_controls.md) — relevance: this note defers the full `permission_mode` reference to loop-controls; that sibling owns the permission-mode family this note only summarizes.
- [Agent SDK — Control Tool Access](cc_sdk_tool_access_control.md) — relevance: deepens this note's `allowed_tools`/`disallowed_tools` treatment into the availability-vs-permission two-layer model and the `mcp__{server}__{tool}` naming for the MCP tools this note says extend the built-ins.
- [Agent SDK — Defining a Custom Tool](cc_sdk_custom_tool_definition.md) — relevance: this note states custom tools default to sequential and you set `readOnlyHint` to opt into parallel; the custom-tool note is where that annotation is defined and attached.
- [Claude Code — Built-in Tools](cc_built_in_tools.md) — relevance: the SDK ships "the same tools that power Claude Code"; this sibling is the Claude Code product view of the same built-in tool categories this note tables for the SDK surface.

### Related Notes (Out-of-Series)

- [Claude Code](../../term_dictionary/term_claude_code.md) — relevance: the SDK exposes the same built-in tools that "power Claude Code"; the product term anchors the tool set this note documents as a library surface.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — relevance: Claude requests tools, the SDK runs them, results feed back — tool execution IS the function-calling mechanism this note describes.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — relevance: each built-in and custom tool is defined by a descriptor (name, schema, `readOnlyHint` annotation); it grounds the tool-definition layer the parallel-execution rule keys off.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — relevance: built-in tools (file/search/execution/web/discovery/orchestration) are the harness's tool layer; the harness term frames the capability set that turns the model into an agent.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — relevance: the `allowed_tools`/`disallowed_tools`/`permission_mode` interplay deciding which tool calls run is the graduated-trust permission gating the term defines.
- [Deny-First](../../term_dictionary/term_deny_first.md) — relevance: `disallowed_tools` blocks listed tools "regardless of other settings," and unlisted tools require approval — the deny-by-default / deny-takes-precedence posture the term names.
- [Subagent](../../term_dictionary/term_subagent.md) — relevance: the orchestration tool row (`Agent`, `Skill`, `TaskCreate`) includes spawning subagents, grounding that built-in orchestration capability the tool table lists.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — relevance: you connect external services via MCP servers, and MCP read-only tools can run in parallel — MCP extends the tool set this note describes beyond the built-ins.
- [Tool: Popular Open-Source MCP Servers](../../tools/tool_popular_mcp_servers.md) — relevance: a catalog of the community MCP servers you connect to grow the agent's tool set beyond the built-ins this note tables; the real-world inventory behind the "connect external services with MCP" bullet.
- [Tool: Security-Review MCP](../../tools/tool_security_review_mcp.md) — relevance: a concrete read-only-style MCP server whose tools would be gated by the `allowed_tools`/`permission_mode` controls this note describes and run in parallel under the read-only rule.
- [MCP Gateway Group-Based Authorization](../org_docs/org_mcp_gateway_concepts_authorization.md) — relevance: an organizational authorization layer for MCP tool calls — the org-context analog of this note's allow/deny permission gating, applied to the MCP tools it says extend the built-ins.
- [Project: SuperAgent](../../../projects/project_superagent.md) — relevance: a production agent that wires backend subagents in via agent-as-a-tool MCP servers — a concrete consumer of the MCP tool-extension and orchestration (`Agent`/subagent) capabilities this note's tool table lists.
- [Band SDK — get_tool_schemas / execute_tool_call](../band/band_sdk_reference_agent_core.md) — the Band agent-core SDK reference covering tool-schema declaration and (incl. MCP) tool-call dispatch; relevance: This Claude Agent SDK doc on declaring allowed tools and executing (incl. MCP) tool calls is the direct external analog of Band's `get_tool_schemas` (declaration) + `execute_tool_call` (dispatch). A reader studying CC SDK tool execution would benefit from the Band parallel showing the same declare-then-dispatch pattern in another SDK.

**Source**: https://code.claude.com/docs/en/agent-sdk/agent-loop
**Last Updated**: 2026-06-13
**Status**: Active
