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

## Related Notes

### Related Notes (Claude Code Series)

- [Agent SDK — The Agent Loop](cc_agent_sdk_agent_loop.md) — relevance: this overview says the SDK gives you "the same agent loop" that powers Claude Code; this sibling is the deep dive on that loop (turns, `max_turns`/`max_budget_usd`) the overview promises.
- [Agent SDK — Tool Execution](cc_agent_sdk_tool_execution.md) — relevance: the overview's first capability ("Built-in tools — read files, run commands, search codebases") and its `allowed_tools` mention are detailed here; the overview links it directly via the [Tool execution] callout.
- [Compare the Agent SDK to Other Claude Tools](cc_agent_sdk_compare_to_other_tools.md) — relevance: the overview's "Getting started and comparison" section points here for how the Agent SDK relates to the Client SDK, the Claude Code CLI, and Managed Agents.
- [Agent SDK Quickstart — Build a Bug-Fixing Agent](cc_agent_sdk_quickstart_bug_fixer.md) — relevance: the overview's `query()` snippet ("Find and fix the bug in auth.py") is realized end-to-end in this quickstart, the procedural follow-on the overview links.
- [Agent SDK — Install and Authenticate](cc_agent_sdk_install_and_auth.md) — relevance: the overview directs first-time readers here to install the package, set credentials, and run a first agent before building.
- [Agent SDK — Result and Hooks](cc_agent_sdk_result_and_hooks.md) — relevance: the overview's "Hooks" capability (callbacks at `PreToolUse`/`PostToolUse`/etc.) is the subject this sibling documents, linked from the Capabilities list.
- [Agent SDK — settingSources and Features](cc_agent_sdk_settingsources_and_features.md) — relevance: the "Claude Code features" table (Skills/Commands/Memory/Plugins) and the `setting_sources` control are exactly what this sibling expands on, linked from that section.

### Related Notes (Out-of-Series)

- [Claude Code](../../term_dictionary/term_claude_code.md) — relevance: Claude Code is the agentic coding tool whose tools/agent loop/context management this SDK exposes as a library; the page frames the SDK as "Claude Code as a library," so the term is the definitional anchor.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — relevance: the SDK is the agent harness (tools + context management + execution loop wrapping the LLM) made programmatic in Python/TypeScript; this note documents that harness as a packaged dependency.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — relevance: the page's headline is agents that "autonomously read files, run commands, search the web, edit code"; the SDK is the tooling for building exactly the autonomous-coding-agent category this term defines.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — relevance: the Capabilities tab dedicates an MCP section (connect databases/browsers/APIs as tools) and lists MCP among the SDK's first-class extension surfaces, making MCP a capability this overview teaches.
- [Subagent](../../term_dictionary/term_subagent.md) — relevance: a Capabilities tab covers spawning specialized subagents via `AgentDefinition`/the Agent tool, with `parent_tool_use_id` tracking — a core SDK capability the overview introduces.
- [Skills](../../term_dictionary/term_skills.md) — relevance: the "Claude Code features" table lists Skills (`.claude/skills/*/SKILL.md`) as a filesystem feature the SDK loads, one of the extension surfaces this overview enumerates.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — relevance: the SDK's value proposition is that Claude "handles tool execution" for you; the built-in agentic tool-use loop this note describes is the function-calling/tool-use mechanism made automatic.
- [Tool: Strands Agents — Open-Source AI Agents SDK](../../tools/tool_strands_agents.md) — relevance: AWS's model-driven agent SDK is the closest peer to the Claude Agent SDK — another library that runs the plan/tool/MCP loop for you — so it is the natural comparison alternative for builders choosing an agent SDK.
- [Tool: Cline](../../tools/tool_cline.md) — relevance: Cline is an autonomous coding agent (read/edit files, run commands) of exactly the category the overview says the SDK builds, useful as a built-product reference for what an Agent-SDK-style agent looks like.
- [Project: Rule-Generation Agent](../../../projects/project_rule_generation_agent.md) — relevance: a production rule-generation agent whose key technology is explicitly the "Claude Agent SDK" plus Agent Skills and function calls — a concrete production agent built on the very SDK this overview introduces.
- [Tutorial: Claude Code — Getting Started (CLI)](../tutorials/tutorial_claude_code_getting_started.md) — relevance: the organization's internal getting-started path for Claude Code (the same engine the SDK packages), covering plugins/skills/MCP servers that the SDK's "Claude Code features" table loads from `.claude/`.
- [Agentic AI System Golden Path — Overview](../org_docs/org_agentic_golden_path_overview.md) — relevance: the organization's golden path for building agentic systems (model + external tools + MCP) is the org-context complement to this generic SDK overview, framing where an Agent-SDK agent fits among Strands/AgentCore/LangGraph.
- [Band SDK Overview](../band/band_sdk_overview.md) — Band's agent-SDK overview (its composition layer over the platform, framework adapters, ClaudeSDKAdapter); relevance: the closest external precedent to this note — an "agent SDK overview" for an agentic platform offered as a library — already lists this note in its outbound Related Notes, so a reverse link is the cleanest cross-platform contrast for a reader comparing the Claude Agent SDK's composition/quick-start model.
- [Band SDK Architecture](../band/band_sdk_architecture.md) — Band's composition-based SDK design (an agent framework offered as an embeddable library composed around your code via Agent.create); relevance: the band note names this its closest external precedent and prime analogy (query/options mirroring Agent.create composition), so a reader of the Claude Agent SDK overview benefits from the reciprocal link to Band's parallel design.
- [Band LangGraph Adapter](../band/band_adapter_langgraph.md) — Band's concrete SDK-adapter tutorial (instantiate agent with options, run it, extend with tools); relevance: closest external SDK-adapter precedent that mirrors the instantiate-adapter / Agent.create()/run() / add-custom-tools shape on a different platform.

**Source**: https://code.claude.com/docs/en/agent-sdk/overview
**Last Updated**: 2026-06-13
**Status**: Active
