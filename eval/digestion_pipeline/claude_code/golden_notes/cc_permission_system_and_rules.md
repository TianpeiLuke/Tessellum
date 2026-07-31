---
tags:
  - resource
  - documentation
  - claude_code
  - permissions
  - access_control
keywords:
  - permission system
  - allow ask deny rules
  - deny first evaluation order
  - permission rule syntax
  - tiered permission model
  - bare tool name deny
  - wildcard patterns
  - tool name wildcards
topics:
  - Claude Code
  - Permissions
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/permissions
access_control_group: ["general"]
---

# Claude Code — Permission System and Rule Syntax

## Overview

Claude Code supports **fine-grained permissions** so you can specify exactly what the agent is allowed to do and what it cannot. Permission settings can be checked into version control and distributed to all developers in an organization, as well as customized by individual developers. At the core are three pieces: a **tiered permission system** that classifies tools by risk, **allow/ask/deny rules** that grant or revoke access, and a **rule syntax** (`Tool` or `Tool(specifier)`) for matching specific tool uses.

These permission rules are enforced by Claude Code, **not by the model**: instructions in your prompt or `CLAUDE.md` shape what Claude tries to do, but they do not change what Claude Code allows. To grant or revoke access, use `/permissions`, the rules described here, a [permission mode](cc_permission_modes_overview.md), or a [PreToolUse hook](cc_permissions_hooks_and_working_directories.md).

## Permission system

Claude Code uses a tiered permission system to balance power and safety:

| Tool type | Example | Approval required | "Yes, don't ask again" behavior |
|---|---|---|---|
| Read-only | File reads, Grep | No | N/A |
| Bash commands | Shell execution | Yes | Permanently per project directory and command |
| File modification | Edit/write files | Yes | Until session end |

## Manage permissions

You can view and manage Claude Code's tool permissions with `/permissions`. This UI lists all permission rules and the `settings.json` file they are sourced from.

- **Allow** rules let Claude Code use the specified tool without manual approval.
- **Ask** rules prompt for confirmation whenever Claude Code tries to use the specified tool.
- **Deny** rules prevent Claude Code from using the specified tool.

Rules are evaluated in order: **deny, then ask, then allow.** The first match in that order determines the outcome, and rule specificity does not change the order. A matching ask rule prompts even when a more specific allow rule also matches the same call.

Deny rules behave differently depending on whether they name a tool or scope a pattern within one. A **bare tool name** like `Bash` removes the tool from Claude's context entirely, so Claude never sees it. A **scoped rule** like `Bash(rm *)` leaves the tool available and blocks matching calls when Claude attempts them.

## Permission rule syntax

Permission rules follow the format `Tool` or `Tool(specifier)`.

### Match all uses of a tool

To match all uses of a tool, use just the tool name without parentheses — for example, `Bash` matches all Bash commands, `WebFetch` matches all web fetch requests, and `Read` matches all file reads. `Bash(*)` is equivalent to `Bash` and matches all Bash commands. As a deny rule, both forms remove the tool from Claude's context.

### Use specifiers for fine-grained control

Add a specifier in parentheses to match specific tool uses: `Bash(npm run build)` matches the exact command `npm run build`, `Read(./.env)` matches reading the `.env` file in the current directory, and `WebFetch(domain:example.com)` matches fetch requests to example.com.

### Wildcard patterns

Bash rules support glob patterns with `*`, which can appear at any position in the command. This configuration allows npm and git commit commands while blocking git push:

```json theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

The space before `*` matters: `Bash(ls *)` matches `ls -la` but not `lsof`, while `Bash(ls*)` matches both. The `:*` suffix is an equivalent way to write a trailing wildcard, so `Bash(ls:*)` matches the same commands as `Bash(ls *)`. The permission dialog writes the space-separated form when you select "Yes, don't ask again" for a command prefix. The `:*` form is only recognized at the end of a pattern; in a pattern like `Bash(git:* push)`, the colon is treated as a literal character and won't match git commands.

### Tool name wildcards

Deny and ask rules also accept glob patterns in the tool-name position. The pattern must match the full tool name: `"*"` matches every tool, and `"mcp__*"` matches every MCP tool across all servers. A tool matched by a bare-name glob deny rule is removed from Claude's context, the same as a bare tool name. This configuration denies every MCP tool:

```json theme={null}
{
  "permissions": {
    "deny": [
      "mcp__*"
    ]
  }
}
```

Allow rules accept tool-name globs only after a literal `mcp__<server>__` prefix; the server segment must be glob-free so the rule names a specific server you configured. `mcp__puppeteer__*` matches every tool from the `puppeteer` server, and `mcp__github__get_*` matches its `get_` tools. An unanchored allow glob such as `"*"`, `"B*"`, or `"mcp__*"` is skipped with a warning and does not auto-approve anything. A deny or ask rule whose tool name matches no known tool produces a startup warning to catch typos; tool names containing `_` or `*` are exempt from the check.

**Source**: https://code.claude.com/docs/en/permissions
**Last Updated**: 2026-06-13
**Status**: Active
