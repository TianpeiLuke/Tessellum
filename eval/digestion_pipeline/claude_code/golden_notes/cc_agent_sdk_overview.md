---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - overview
keywords:
  - agent sdk
  - claude code as a library
  - query function
  - claudeagentoptions
  - built-in tools
  - python and typescript agents
  - agent sdk capabilities
  - claude code features
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/overview
access_control_group: ["general"]
---

# Agent SDK Overview

## Overview

The **Agent SDK** lets you build production AI agents with **Claude Code as a library**. It gives you the same tools, agent loop, and context management that power Claude Code, programmable in **Python and TypeScript**, so you can build agents that autonomously read files, run commands, search the web, and edit code. The SDK ships with built-in tools for reading files, running commands, and editing code, so your agent can start working immediately without you implementing tool execution yourself.

The entry point is the `query()` function, configured by `ClaudeAgentOptions` (Python) / an `options` object (TypeScript). You pass a `prompt` and an `allowed_tools` / `allowedTools` list, then iterate over the streamed messages as Claude reads files, finds bugs, and edits them.

```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)  # Claude reads the file, finds the bug, edits it


asyncio.run(main())
```

> Billing note: Starting June 15, 2026, Agent SDK and `claude -p` usage on subscription plans draws from a new monthly **Agent SDK credit**, separate from interactive usage limits.

## Capabilities

Everything that makes Claude Code powerful is available in the SDK. The overview presents each capability as a tab; the deep dives are linked out to their own pages.

- **Built-in tools** — Your agent can read files, run commands, and search codebases out of the box. Key tools include **Read** (read any file in the working directory), **Write** (create new files), **Edit** (precise edits to existing files), **Bash** (terminal commands, scripts, git operations), **Monitor** (watch a background script and react to each output line as an event), **Glob** (find files by pattern), **Grep** (search file contents with regex), **WebSearch**, **WebFetch**, and **AskUserQuestion** (ask the user clarifying questions with multiple-choice options). See [Tool execution](cc_agent_sdk_tool_execution.md).
- **Hooks** — Run custom code at key points in the agent lifecycle. SDK hooks use callback functions to validate, log, block, or transform agent behavior. Available hooks include `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, and more. See [Result and hooks](cc_agent_sdk_result_and_hooks.md) and the full [hooks reference](https://code.claude.com/docs/en/agent-sdk/hooks).
- **Subagents** — Spawn specialized agents to handle focused subtasks; the main agent delegates work and subagents report back. Define custom agents with `AgentDefinition`, invoked via the **Agent** tool (include `Agent` in `allowedTools` to auto-approve invocations). Messages from within a subagent's context carry a `parent_tool_use_id` field so you can track which messages belong to which subagent execution. See the [subagents reference](https://code.claude.com/docs/en/agent-sdk/subagents).
- **MCP** — Connect to external systems via the Model Context Protocol: databases, browsers, APIs, and hundreds more. For example, connecting the Playwright MCP server (`mcp_servers` / `mcpServers`) gives your agent browser-automation capabilities. See the [MCP reference](https://code.claude.com/docs/en/agent-sdk/mcp).
- **Permissions** — Control exactly which tools your agent can use: allow safe operations, block dangerous ones, or require approval for sensitive actions. `allowed_tools` pre-approves a tool set (e.g. a read-only agent that can analyze but not modify code). See [Loop controls](cc_agent_sdk_loop_controls.md) and the [permissions reference](https://code.claude.com/docs/en/agent-sdk/permissions).
- **Sessions** — Maintain context across multiple exchanges. Claude remembers files read, analysis done, and conversation history. Capture the `session_id` from the first query's init `SystemMessage`, then `resume` to continue with full context, or fork sessions to explore different approaches. See the [sessions reference](https://code.claude.com/docs/en/agent-sdk/sessions).

### Claude Code features

The SDK also supports Claude Code's filesystem-based configuration. With default options the SDK loads these from `.claude/` in your working directory and `~/.claude/`. To restrict which sources load, set `setting_sources` (Python) or `settingSources` (TypeScript) — see [settingSources and features](cc_agent_sdk_settingsources_and_features.md).

| Feature | Description | Location |
|---|---|---|
| Skills | Specialized capabilities Claude uses automatically or you invoke with `/name` | `.claude/skills/*/SKILL.md` |
| Commands | Custom commands in the legacy format (use skills for new custom commands) | `.claude/commands/*.md` |
| Memory | Project context and instructions | `CLAUDE.md` or `.claude/CLAUDE.md` |
| Plugins | Extend with skills, agents, hooks, and MCP servers | Programmatic via `plugins` option |

## Getting started and comparison

To install the SDK, set credentials, and run a first agent, see [Install and auth](cc_agent_sdk_install_and_auth.md); to follow the end-to-end tutorial, see [Quickstart bug fixer](cc_agent_sdk_quickstart_bug_fixer.md). For how the Agent SDK relates to the Client SDK, the Claude Code CLI, and Managed Agents, see [Compare to other tools](cc_agent_sdk_compare_to_other_tools.md).

The full changelogs and bug reporting live in the per-language GitHub repos (TypeScript and Python `CHANGELOG.md` / issues). Use of the Claude Agent SDK is governed by Anthropic's Commercial Terms of Service.

**Source**: https://code.claude.com/docs/en/agent-sdk/overview
**Last Updated**: 2026-06-13
**Status**: Active
