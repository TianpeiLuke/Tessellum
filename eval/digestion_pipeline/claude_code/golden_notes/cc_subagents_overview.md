---
tags:
  - resource
  - documentation
  - claude_code
  - subagents
  - delegation
keywords:
  - subagents
  - specialized ai assistants
  - own context window
  - custom system prompt
  - tool access
  - independent permissions
  - built-in subagents
  - explore plan general-purpose
  - automatic delegation
topics:
  - Claude Code
  - Subagents
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/sub-agents
access_control_group: ["general"]
---

# Claude Code — Subagents Overview

## Overview

**Subagents** are specialized AI assistants that handle specific types of tasks. You use one when a side task would flood your main conversation with search results, logs, or file contents you won't reference again: the subagent does that work in its own context and returns only the summary. You define a custom subagent when you keep spawning the same kind of worker with the same instructions.

Each subagent runs in its **own context window** with a **custom system prompt**, **specific tool access**, and **independent permissions**. When Claude encounters a task that matches a subagent's `description`, it delegates to that subagent, which works independently and returns results. Claude uses each subagent's description to decide when to delegate, so a clear description is what lets Claude know when to use it. Subagents work within a single session — to run many independent sessions in parallel and monitor them from one place, see [agent view](https://code.claude.com/docs/en/agent-view); for sessions that communicate with each other, see [agent teams](cc_agent_teams_overview.md).

## What Subagents Help You Do

Subagents serve five purposes:

- **Preserve context** by keeping exploration and implementation out of your main conversation.
- **Enforce constraints** by limiting which tools a subagent can use.
- **Reuse configurations** across projects with user-level subagents.
- **Specialize behavior** with focused system prompts for specific domains.
- **Control costs** by routing tasks to faster, cheaper models like Haiku.

Claude Code includes several built-in subagents and lets you create custom ones with custom prompts, tool restrictions, permission modes, hooks, and skills (see [Create a Subagent](cc_create_a_subagent.md) and the [configuration reference](cc_subagent_configuration_reference.md)).

## Built-in Subagents

Claude Code includes built-in subagents that Claude automatically uses when appropriate. Each inherits the parent conversation's permissions with additional tool restrictions. **Explore** and **Plan** skip your CLAUDE.md files and the parent session's git status to keep research fast and inexpensive; every other built-in and custom subagent loads both.

The core three:

- **Explore** — a fast, **read-only** agent optimized for searching and analyzing codebases. **Model**: Haiku (fast, low-latency). **Tools**: read-only (denied Write and Edit). **Purpose**: file discovery, code search, codebase exploration. Claude delegates to Explore when it needs to search or understand a codebase without making changes, keeping exploration results out of the main conversation. When invoking it, Claude specifies a thoroughness level: **quick** for targeted lookups, **medium** for balanced exploration, or **very thorough** for comprehensive analysis.
- **Plan** — a research agent used during plan mode to gather context before presenting a plan. **Model**: inherits from the main conversation. **Tools**: read-only (denied Write and Edit). **Purpose**: codebase research for planning. Exploration output stays in a separate context window while the main conversation remains read-only.
- **General-purpose** — a capable agent for complex, multi-step tasks that require both exploration and action. **Model**: inherits from the main conversation. **Tools**: all tools. **Purpose**: complex research, multi-step operations, code modifications. Claude delegates here when a task requires both exploration and modification, complex reasoning to interpret results, or multiple dependent steps.

Two additional helper agents are typically invoked automatically, so you don't use them directly: **statusline-setup** (model Sonnet, used when you run `/statusline` to configure your status line) and **claude-code-guide** (model Haiku, used when you ask questions about Claude Code features).

Built-in subagents are always registered in interactive sessions. To block a specific built-in type, add it to `permissions.deny`. To prevent Claude from delegating to any subagent, deny the `Agent` tool itself. In non-interactive mode and the Agent SDK, set `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1` to remove all built-in types and supply only your own.

**Source**: https://code.claude.com/docs/en/sub-agents
**Last Updated**: 2026-06-13
**Status**: Active
