---
tags:
  - resource
  - documentation
  - claude_code
  - tools
  - catalog
keywords:
  - built-in tools
  - tool catalog
  - permission required
  - toolname specifier
  - tool-specific permission rules
  - disable a tool
  - mcp custom tools
  - check available tools
topics:
  - Claude Code
  - Tools
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/tools-reference
access_control_group: ["general"]
---

# Claude Code — Built-in Tool Catalog

## Overview

Claude Code ships with a set of **built-in tools** that let it understand and modify your codebase. A **tool** is a named capability the model can invoke; the tool name is the exact string you use in [permission rules](https://code.claude.com/docs/en/permissions), subagent tool lists, and hook matchers. For the most part Claude decides when to use a tool on its own — you only name tools when configuring permissions, subagents, skills, or hooks. To **disable a tool entirely**, add its name to the `deny` array in your permission settings.

This note is the catalog: it enumerates the built-in tools and which ones require permission, gives the shared `ToolName(specifier)` rule format that governs every tool, and shows how to check the live tool set. Per-tool semantics are split out — see the sibling notes [cc_file_tool_behavior](cc_file_tool_behavior.md) (Read/Edit/Write/NotebookEdit/Glob/Grep) and [cc_execution_tool_behavior](cc_execution_tool_behavior.md) (Agent/Bash/Monitor/PowerShell/WebFetch/WebSearch/LSP).

## Extending the catalog

Two extension paths add capability without changing the built-in catalog:

- **Custom tools** come from connecting an [MCP server](https://code.claude.com/docs/en/mcp). These surface as additional `mcp__*` tool names.
- **Skills** are reusable prompt-based workflows. A skill runs through the existing `Skill` tool rather than adding a new tool entry, so writing a skill does not introduce a new catalog row.

## The built-in tools

The tools below are grouped by purpose. The "Permission Required" column reproduces the source's Yes/No for whether a tool prompts/checks against permission rules before running.

**File and search tools** (behavior detailed in [cc_file_tool_behavior](cc_file_tool_behavior.md)):

- `Read` — Reads the contents of files. Permission: No.
- `Write` — Creates or overwrites files. Permission: Yes.
- `Edit` — Makes targeted edits to specific files. Permission: Yes.
- `NotebookEdit` — Modifies Jupyter notebook cells. Permission: Yes.
- `Glob` — Finds files based on pattern matching. Permission: No.
- `Grep` — Searches for patterns in file contents. Permission: No.

**Execution, web, and code-intelligence tools** (behavior detailed in [cc_execution_tool_behavior](cc_execution_tool_behavior.md)):

- `Bash` — Executes shell commands in your environment. Permission: Yes.
- `PowerShell` — Executes PowerShell commands natively. Permission: Yes.
- `Monitor` — Runs a command in the background and feeds each output line back to Claude so it can react mid-conversation. Permission: Yes.
- `WebFetch` — Fetches content from a specified URL. Permission: Yes.
- `WebSearch` — Performs web searches. Permission: Yes.
- `LSP` — Code intelligence via language servers (definitions, references, type errors). Permission: No.

**Agent, team, and orchestration tools:**

- `Agent` — Spawns a [subagent](https://code.claude.com/docs/en/sub-agents) with its own context window to handle a task; also launches forked subagents. Permission: No.
- `Workflow` — Runs a dynamic workflow: a script that orchestrates many subagents in the background and returns one consolidated result. Permission: Yes.
- `SendMessage` — Sends a message to an agent-team teammate, or resumes a subagent by agent ID (only when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Permission: No.
- `TeamCreate` / `TeamDelete` — Create or disband an agent team (experimental, gated by the same env var). Permission: No.

**Task, planning, and clarification tools:**

- `AskUserQuestion` — Asks multiple-choice questions to gather requirements or clarify ambiguity. Permission: No.
- `EnterPlanMode` (No) / `ExitPlanMode` (Yes) — Switch to plan mode to design an approach, then present a plan for approval and exit.
- `TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` / `TaskStop` — Manage the task list and background tasks. Permission: No. (`TodoWrite` and `TaskOutput` are deprecated.)
- `Skill` — Executes a skill within the main conversation. Permission: Yes.

**MCP, scheduling, worktree, and notification tools:**

- `ListMcpResourcesTool` / `ReadMcpResourceTool` — List or read resources exposed by connected MCP servers. Permission: No.
- `ToolSearch` — Searches for and loads deferred tools when tool search is enabled. `WaitForMcpServers` waits for still-connecting MCP servers when tool search is disabled. Permission: No.
- `CronCreate` / `CronDelete` / `CronList` — Schedule, cancel, and list session-scoped scheduled tasks. Permission: No.
- `EnterWorktree` / `ExitWorktree` — Create/enter or exit an isolated git worktree. Permission: No.
- `PushNotification` — Sends a desktop (and, with Remote Control, phone) notification. `RemoteTrigger` and `ScheduleWakeup` back Routines and self-paced `/loop`. Permission: No.

Some tools (e.g. `PushNotification`, `RemoteTrigger`, `Monitor`, `ScheduleWakeup`) run through Anthropic-hosted infrastructure and are **not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry**. For the full per-tool description list, see the [tools reference](https://code.claude.com/docs/en/tools-reference).

## Configure tools with permission rules and hooks

You reference tool names directly when defining permissions and other configuration: in `permissions.allow`/`permissions.deny` (and the `/permissions` interface), the `--allowedTools`/`--disallowedTools` CLI flags, the Agent SDK's `allowedTools`/`disallowedTools` options, a subagent's `tools`/`disallowedTools` frontmatter, a skill's `allowed-tools` frontmatter, and a hook's `if` condition.

All of these accept the same rule format, **`ToolName(specifier)`**. The specifier depends on the tool, and several tools share a format:

| Rule format                    | Applies to                | Details                       |
| :----------------------------- | :------------------------ | :---------------------------- |
| `Bash(npm run *)`              | Bash, Monitor             | Command pattern matching      |
| `PowerShell(Get-ChildItem *)`  | PowerShell                | Command pattern matching      |
| `Read(~/secrets/**)`           | Read, Grep, Glob, LSP     | Path pattern matching         |
| `Edit(/src/**)`                | Edit, Write, NotebookEdit | Path pattern matching         |
| `Skill(deploy *)`              | Skill                     | Skill name matching           |
| `Agent(Explore)`               | Agent                     | Subagent type matching        |
| `WebFetch(domain:example.com)` | WebFetch                  | Domain matching               |
| `WebSearch`                    | WebSearch                 | No specifier; allow/deny whole tool |

Tools not listed (such as `ExitPlanMode` or `ShareOnboardingGuide`) accept only the bare tool name with no specifier. An `Edit(...)` allow rule also grants read access to the same path, so a matching `Read(...)` rule is not needed. Hook `matcher` fields use **bare tool names**, not the parenthesized rule format. For the full specifier syntax, see [Permissions](https://code.claude.com/docs/en/permissions) (rule-syntax detail is owned by the permissions reference).

## Check which tools are available

Your exact tool set depends on your provider, platform, and settings. To check what is loaded in a running session, ask Claude directly — for example, "What tools do you have access to?" — and Claude gives a conversational summary. For exact MCP tool names, run `/mcp`.

The [advisor tool](https://code.claude.com/docs/en/advisor) is a *server tool* that the API runs, rather than a tool Claude Code implements; it has no name you can reference in permission rules or hook matchers.

**Source**: https://code.claude.com/docs/en/tools-reference
**Last Updated**: 2026-06-13
**Status**: Active
