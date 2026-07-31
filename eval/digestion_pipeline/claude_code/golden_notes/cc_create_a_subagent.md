---
tags:
  - resource
  - documentation
  - claude_code
  - subagents
  - procedure
keywords:
  - create a subagent
  - /agents command
  - subagent scope
  - subagent markdown file
  - yaml frontmatter
  - --agents cli flag
  - subagent priority
  - managed settings
topics:
  - Claude Code
  - Subagents
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/sub-agents
access_control_group: ["general"]
---

# Create a Subagent

## Overview

A subagent is a specialized agent defined by a Markdown file with YAML frontmatter and a system-prompt body, runnable from any project on your machine. There are three ways to create one: the guided `/agents` command (recommended), a hand-written Markdown file on disk, or a JSON definition passed via the `--agents` CLI flag for the current session only. This note covers the creation workflow — the `/agents` quickstart, where to store a definition (the scope/priority hierarchy), and the file format. The exhaustive frontmatter field table, model resolution, capability controls, and hooks live in [Subagent Configuration Reference](cc_subagent_configuration_reference.md).

## Quickstart: the `/agents` command

The `/agents` command is the recommended way to create and manage subagents. The walkthrough below creates a user-level code-improvement subagent. Open the interface in Claude Code:

```text
/agents
```

Then work through the guided **Steps**:

1. **Choose a location** — switch to the **Library** tab, select **Create new agent**, then choose **Personal**. This saves to `~/.claude/agents/` so it is available in all your projects.
2. **Generate with Claude** — select **Generate with Claude** and describe the subagent; Claude generates the identifier, description, and system prompt for you.
3. **Select tools** — for a read-only reviewer, deselect everything except **Read-only tools**. Keeping all tools selected makes the subagent inherit all tools available to the main conversation.
4. **Select model** — choose which model the subagent uses (the example uses **Sonnet**).
5. **Choose a color** — pick a background color so you can identify which subagent is running in the UI.
6. **Configure memory** — select **User scope** for a [persistent memory directory](cc_subagent_configuration_reference.md) at `~/.claude/agent-memory/`, or **None** to skip persisting learnings.
7. **Save and try it out** — review the configuration summary, then press `s` or `Enter` to save (or `e` to save and edit in your editor). The subagent is available immediately.

Subagents created through the `/agents` interface take effect immediately without a restart. The **Running** tab lists live and recently finished subagents and lets you open or stop them; the **Library** tab lets you view all available subagents (built-in, user, project, and plugin), create new ones, edit configuration and tool access, delete custom subagents, and see which are active when duplicates exist.

## Choose the subagent scope

Subagents are stored in different locations depending on scope. When multiple subagents share the same name, the higher-priority location wins:

| Location | Scope | Priority | How to create |
| :--- | :--- | :--- | :--- |
| Managed settings | Organization-wide | 1 (highest) | Deployed via managed settings |
| `--agents` CLI flag | Current session | 2 | Pass JSON when launching Claude Code |
| `.claude/agents/` | Current project | 3 | Interactive or manual |
| `~/.claude/agents/` | All your projects | 4 | Interactive or manual |
| Plugin's `agents/` directory | Where plugin is enabled | 5 (lowest) | Installed with [plugins](https://code.claude.com/docs/en/plugins) |

**Project subagents** (`.claude/agents/`) are ideal for subagents specific to a codebase; check them into version control so your team can use and improve them collaboratively. They are discovered by walking up from the current working directory; directories added with `--add-dir` grant file access only and are not scanned for subagents. **User subagents** (`~/.claude/agents/`) are personal subagents available in all your projects.

Claude Code scans `.claude/agents/` and `~/.claude/agents/` recursively, so you can organize definitions into subfolders such as `agents/review/`. The subdirectory path does not affect identity — identity comes only from the `name` frontmatter field — so keep `name` values unique across the whole tree (if two files in one scope share a name, Claude Code keeps one and discards the other without warning). Plugin `agents/` directories are also scanned recursively, but there a subfolder becomes part of the scoped identifier: `agents/review/security.md` in plugin `my-plugin` registers as `my-plugin:review:security`. **Managed subagents** are deployed by organization administrators and take precedence over project and user subagents with the same name.

**CLI-defined subagents** are passed as JSON when launching Claude Code. They exist only for that session and are not saved to disk, making them useful for quick testing or automation scripts. You can define multiple subagents in a single `--agents` call:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

The `--agents` flag accepts JSON with the same frontmatter fields as file-based subagents (see [Subagent Configuration Reference](cc_subagent_configuration_reference.md)). Use `prompt` for the system prompt, equivalent to the Markdown body in file-based subagents.

## Write subagent files

Subagent files use YAML frontmatter for configuration, followed by the system prompt in Markdown:

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

The frontmatter defines the subagent's metadata and configuration; the body becomes the system prompt that guides behavior. Subagents receive only this system prompt (plus basic environment details like working directory), **not** the full Claude Code system prompt. Only `name` and `description` are required — the complete field reference is in [Subagent Configuration Reference](cc_subagent_configuration_reference.md).

A subagent starts in the main conversation's current working directory. Within a subagent, `cd` commands do not persist between Bash or PowerShell tool calls and do not affect the main conversation's working directory. To give the subagent an isolated copy of the repository instead, set `isolation: worktree`.

**Restart-to-load rule:** subagents are loaded at session start. If you add or edit a subagent file directly on disk, restart your session to load it. Subagents created through the `/agents` interface take effect immediately without a restart.

**Source**: https://code.claude.com/docs/en/sub-agents
**Last Updated**: 2026-06-13
**Status**: Active
