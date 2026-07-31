---
tags:
  - resource
  - documentation
  - claude_code
  - subagents
  - configuration
keywords:
  - subagent frontmatter fields
  - tools disallowedtools allowlist denylist
  - model resolution order
  - permissionmode subagent
  - mcpservers scope
  - skills preload
  - persistent memory scope
  - pretooluse conditional hooks
  - subagentstart subagentstop
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

# Claude Code — Subagent Configuration Reference

## Overview

A subagent is configured through the YAML frontmatter of its markdown definition file (or the equivalent JSON passed to `--agents`). This note is the exhaustive reference for that configuration: every supported frontmatter field, how the `model` is resolved, and the capability controls that govern what a subagent can do — tool allowlists/denylists, spawn restrictions, MCP scoping, permission modes, skill preloading, persistent memory, conditional hooks, and disabling specific subagents. It also covers the two ways to define lifecycle hooks (in frontmatter vs. in `settings.json`).

For how to create a subagent and choose its scope, see [cc_create_a_subagent](cc_create_a_subagent.md). For day-to-day invocation patterns, see [cc_work_with_subagents](cc_work_with_subagents.md).

## Supported frontmatter fields

Only `name` and `description` are required; all others are optional.

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Unique identifier using lowercase letters and hyphens. Hooks receive this value as `agent_type`. The filename does not have to match. |
| `description` | Yes | When Claude should delegate to this subagent. |
| `tools` | No | Tools the subagent can use. Inherits all tools if omitted. To preload Skills, use the `skills` field rather than listing `Skill` here. |
| `disallowedTools` | No | Tools to deny, removed from the inherited or specified list. |
| `model` | No | Model to use: `sonnet`, `opus`, `haiku`, `fable`, a full model ID (e.g., `claude-opus-4-8`), or `inherit`. Defaults to `inherit`. |
| `permissionMode` | No | Permission mode: `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, or `plan`. Ignored for plugin subagents. |
| `maxTurns` | No | Maximum number of agentic turns before the subagent stops. |
| `skills` | No | Skills to preload into the subagent's context at startup. The full skill content is injected, not just the description. |
| `mcpServers` | No | MCP servers available to this subagent (server name reference or inline definition). Ignored for plugin subagents. |
| `hooks` | No | Lifecycle hooks scoped to this subagent. Ignored for plugin subagents. |
| `memory` | No | Persistent memory scope: `user`, `project`, or `local`. Enables cross-session learning. |
| `background` | No | Set to `true` to always run this subagent as a background task. Default: `false`. |
| `effort` | No | Effort level when this subagent is active; overrides the session effort level. Options: `low`, `medium`, `high`, `xhigh`, `max` (available levels depend on the model). |
| `isolation` | No | Set to `worktree` to run the subagent in a temporary git worktree branched by default from your default branch. The worktree is automatically cleaned up if the subagent makes no changes. |
| `color` | No | Display color in the task list and transcript: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, or `cyan`. |
| `initialPrompt` | No | Auto-submitted as the first user turn when this agent runs as the main session agent (via `--agent` or the `agent` setting). Commands and skills are processed; prepended to any user-provided prompt. |

For security reasons, plugin subagents do not support `hooks`, `mcpServers`, or `permissionMode` — these fields are ignored when loading agents from a plugin.

## Choose a model

The `model` field accepts a model alias (`sonnet`, `opus`, `haiku`, `fable`), a full model ID such as `claude-opus-4-8` or `claude-sonnet-4-6` (the same values as the `--model` flag), or `inherit` to use the same model as the main conversation. If omitted, it defaults to `inherit`.

When Claude invokes a subagent it can also pass a per-invocation `model` parameter. Claude Code resolves the subagent's model in this order:

1. The `CLAUDE_CODE_SUBAGENT_MODEL` environment variable, if set
2. The per-invocation `model` parameter
3. The subagent definition's `model` frontmatter
4. The main conversation's model

## Control subagent capabilities

### Available tools and the allowlist/denylist

Subagents inherit the internal tools and MCP tools available in the main conversation by default. The following tools depend on the main conversation's UI or session state and are **not** available to subagents even when listed in `tools`: `AskUserQuestion`, `EnterPlanMode`, `ExitPlanMode` (unless the subagent's `permissionMode` is `plan`), `ScheduleWakeup`, and `WaitForMcpServers`.

Restrict tools with `tools` (allowlist) or `disallowedTools` (denylist). The `tools` example below exclusively allows Read, Grep, Glob, and Bash — the subagent cannot edit or write files or use any MCP tools:

```yaml
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

Conversely, `disallowedTools: Write, Edit` inherits every tool from the main conversation except Write and Edit (Bash, MCP tools, and everything else are kept). If both fields are set, `disallowedTools` is applied first, then `tools` is resolved against the remaining pool; a tool listed in both is removed.

### Restrict which subagents can be spawned

When an agent runs as the main thread with `claude --agent`, it can spawn subagents via the Agent tool. Use `Agent(agent_type)` syntax in `tools` to restrict which types it may spawn (in v2.1.63 the Task tool was renamed to Agent; existing `Task(...)` references still work as aliases):

```yaml
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

This is an allowlist: only `worker` and `researcher` can be spawned; any other type fails. Use `Agent` without parentheses (e.g., `tools: Agent, Read, Bash`) to allow spawning any subagent; omit `Agent` entirely and the agent cannot spawn any. To block specific agents while allowing all others, use `permissions.deny` instead. The `Agent(agent_type)` allowlist applies only to an agent running as the main thread with `claude --agent`; inside a subagent definition, listing `Agent` lets it spawn nested subagents but any type list in parentheses is ignored.

### Scope MCP servers to a subagent

Use `mcpServers` to give a subagent access to MCP servers that aren't in the main conversation. Each list entry is either an inline server definition (connected when the subagent starts, disconnected when it finishes) or a string referencing an already-configured server (which shares the parent session's connection):

```yaml
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---
```

Inline definitions use the same schema as `.mcp.json` entries (`stdio`, `http`, `sse`, `ws`). Defining a server inline here (rather than in `.mcp.json`) keeps its tool descriptions out of the main conversation's context. As of v2.1.153, main-session MCP restrictions — `--strict-mcp-config`, `--bare`, enterprise managed MCP configuration, and `allowedMcpServers`/`deniedMcpServers` policies — also cover servers declared in subagent frontmatter; a blocked server is skipped with a warning. Managed-settings restrictions apply to every subagent, but `--strict-mcp-config` does not filter servers passed inline via `--agents` or the SDK `agents` option, since those are explicit caller input.

### Permission modes

`permissionMode` controls how the subagent handles permission prompts. Subagents inherit the parent's permission context and can override the mode, except where the parent takes precedence.

| Mode | Behavior |
|---|---|
| `default` | Standard permission checking with prompts |
| `acceptEdits` | Auto-accept file edits and common filesystem commands for paths in the working directory or `additionalDirectories` |
| `auto` | Auto mode: a background classifier reviews commands and protected-directory writes |
| `dontAsk` | Auto-deny permission prompts (explicitly allowed tools still work) |
| `bypassPermissions` | Skip permission prompts |
| `plan` | Plan mode (read-only exploration) |

Use `bypassPermissions` with caution: it skips prompts and allows writes to directories such as `.git`, `.claude`, `.vscode`, `.cargo`, and others, though explicit `ask` rules and root/home removals like `rm -rf /` still prompt. Parent precedence: if the parent uses `bypassPermissions` or `acceptEdits`, that takes precedence and cannot be overridden. If the parent uses auto mode, the subagent inherits auto mode and any `permissionMode` in its frontmatter is ignored — the classifier evaluates its tool calls with the parent's block and allow rules.

### Preload skills

The `skills` field injects the full content of each listed skill into the subagent's context at startup, giving it domain knowledge without runtime discovery. For example, `skills:` with list entries `api-conventions` and `error-handling-patterns` preloads both skills' content into an `api-developer` subagent. This controls which skills are *preloaded*, not which the subagent can *access* — without it, the subagent can still discover and invoke project, user, and plugin skills through the Skill tool. To prevent skill invocation entirely, omit `Skill` from `tools` or add it to `disallowedTools`. You cannot preload skills that set `disable-model-invocation: true`; missing or disabled listed skills are skipped with a debug-log warning. This is the inverse of running a skill in a subagent (`context: fork`), which injects skill content into the agent you specify.

### Enable persistent memory

The `memory` field gives the subagent a persistent directory that survives across conversations, building up knowledge over time:

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

Choose the scope by how broadly the memory should apply:

| Scope | Location | Use when |
|---|---|---|
| `user` | `~/.claude/agent-memory/<name-of-agent>/` | learnings apply across all projects |
| `project` | `.claude/agent-memory/<name-of-agent>/` | knowledge is project-specific and shareable via version control |
| `local` | `.claude/agent-memory-local/<name-of-agent>/` | knowledge is project-specific but should not be checked into version control |

When memory is enabled, the subagent's system prompt includes instructions for reading/writing the memory directory plus the first 200 lines or 25KB of `MEMORY.md` (whichever comes first, with instructions to curate it past that limit), and Read, Write, and Edit tools are automatically enabled. `project` is the recommended default scope.

### Conditional rules with hooks

For dynamic control — allowing some operations of a tool while blocking others — use a `PreToolUse` hook to validate operations before they execute. This `db-reader` subagent allows only read-only database queries by running a validation script before each Bash command:

```yaml
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code passes hook input as JSON via stdin; the script extracts the command and exits with code 2 to block write operations (`INSERT`, `UPDATE`, `DELETE`, etc.). On Windows, write hook scripts in PowerShell and add `shell: powershell` to the hook entry. (The full validation-script body appears in [cc_subagent_examples](cc_subagent_examples.md).)

### Disable specific subagents

Prevent Claude from using specific subagents by adding them to the `deny` array in settings, using the format `Agent(subagent-name)` (e.g., `"deny": ["Agent(Explore)", "Agent(my-custom-agent)"]`). This works for both built-in and custom subagents. You can also use the CLI flag `claude --disallowedTools "Agent(Explore)"`.

## Define hooks for subagents

Subagents can define hooks that run during their lifecycle. There are two ways to configure them: in the subagent's **frontmatter** (run only while that subagent is active) or in **`settings.json`** (run in the main session when subagents start or stop).

### Hooks in subagent frontmatter

Frontmatter hooks run only while that specific subagent is active and are cleaned up when it finishes. They fire when the agent is spawned as a subagent (Agent tool or @-mention) and when it runs as the main session via `--agent` or the `agent` setting. All hook events are supported; the most common are `PreToolUse` (before a tool, matcher = tool name), `PostToolUse` (after a tool, matcher = tool name), and `Stop` (when the subagent finishes — converted to `SubagentStop` at runtime). When the agent is invoked as a subagent, `Stop` hooks in frontmatter are automatically converted to `SubagentStop` events. A common pattern validates Bash commands with `PreToolUse` and runs a linter after edits with `PostToolUse` (matcher `"Edit|Write"`).

### Project-level hooks for subagent events

Configure hooks in `settings.json` that respond to subagent lifecycle events in the main session: `SubagentStart` (when a subagent begins) and `SubagentStop` (when a subagent completes), both matching on the agent type name. This example runs a setup script only when the `db-agent` subagent starts, and a cleanup script when any subagent stops:

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

For the complete hook configuration format, see the [Hooks reference](https://code.claude.com/docs/en/hooks).

**Source**: https://code.claude.com/docs/en/sub-agents
**Last Updated**: 2026-06-13
**Status**: Active
