---
tags:
  - resource
  - documentation
  - claude_code
  - configuration
  - directory_map
keywords:
  - .claude directory
  - claude code configuration files
  - project vs global config
  - committed vs gitignored
  - when files load
  - choose the right file
  - file reference table
  - settings.json
topics:
  - Claude Code
  - Configuration
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/claude-directory
access_control_group: ["general"]
---

# Claude Code — The `.claude` Directory

## Overview

Claude Code reads instructions, settings, skills, subagents, workflows, rules, and memory from two locations: your **project directory** (the repo you're working in, with most config under `.claude/`) and **`~/.claude`** in your home directory. Project files are meant to be committed to git so your team shares them; files in `~/.claude` are personal configuration that applies across every project you work in. On Windows, `~/.claude` resolves to `%USERPROFILE%\.claude`, and if you set `CLAUDE_CONFIG_DIR` (env vars → see [env vars reference](https://code.claude.com/docs/en/env-vars)) every `~/.claude` path lives under that directory instead.

Most users only ever edit `CLAUDE.md` and `settings.json`; the rest of the directory is optional — you add skills, rules, or subagents as you need them. This note maps every file the docs' interactive explorer covers: each node's purpose, scope, whether it's committed or gitignored, and **when it loads**. (The data Claude Code *writes* as you work — transcripts, caches, snapshots — is the application-data lifecycle, covered separately in [Application Data](cc_claude_application_data.md).)

## Project files (`your-project/`)

These live in your repo. Three files sit at the project root; the rest live under `.claude/`.

| File | Commit | One-liner | When it loads |
|---|---|---|---|
| `CLAUDE.md` | committed | Project instructions Claude reads every session | Loaded into context at the start of every session (also works at `.claude/CLAUDE.md`) |
| `.mcp.json` | committed | Project-scoped MCP servers, shared with your team | Servers connect when the session begins; tool schemas are deferred by default and load on demand via tool search |
| `.worktreeinclude` | committed | Gitignored files to copy into new worktrees | Read when Claude creates a git worktree via `--worktree`, the `EnterWorktree` tool, or subagent `isolation: worktree` |

`.mcp.json` holds the project-scoped MCP servers your whole team uses; personal servers you keep to yourself go in `~/.claude.json` instead. `.worktreeinclude` lists gitignored files (e.g. `.env`) to copy from your main repo into each fresh worktree checkout, using `.gitignore` syntax — only files that both match a pattern and are gitignored get copied.

### Inside `.claude/`

Everything Claude Code reads that is specific to this project. Commit most files here so your team shares them; a few (like `settings.local.json`) are automatically gitignored. Each file's badge shows which.

| Node | Commit | Purpose / when it loads |
|---|---|---|
| `settings.json` | committed | Permissions, hooks, statusLine, model, env, outputStyle. **Enforced** (unlike CLAUDE.md guidance). Overrides global `~/.claude/settings.json`; local settings, CLI flags, and managed settings override it. |
| `settings.local.json` | gitignored | Personal settings overrides for this project; same schema as `settings.json`. Highest of the user-editable settings files; CLI flags and managed settings still take precedence. |
| `rules/` | committed | Topic-scoped instructions. Rules **without** `paths:` load at session start (like CLAUDE.md); rules **with** `paths:` load when a matching file enters context. |
| `skills/<name>/SKILL.md` | committed | Reusable prompts invoked with `/name` or auto-invoked by Claude; folder bundles SKILL.md plus supporting files. |
| `commands/*.md` | committed | Single-file prompts invoked with `/name` — the same mechanism as skills. For new workflows, prefer skills. |
| `output-styles/*.md` | committed | Project-scoped output styles (if your team shares one); applied at session start when selected via the `outputStyle` setting. |
| `agents/*.md` | committed | Subagent definitions with their own system prompt, tool access, and optionally model; each runs in a fresh context window. |
| `workflows/*.js` | committed | Dynamic workflow scripts that orchestrate many subagents; loaded at startup, each file becomes a `/<name>` command. |
| `agent-memory/<name>/` | committed | Persistent memory for subagents with `memory: project`; first 200 lines (capped at 25KB) of the subagent's `MEMORY.md` load into its system prompt — distinct from main-session auto memory. |

Per the source, `settings.json` is the key distinction in kind: it is **enforced** (permissions control which commands/tools Claude can use; hooks run your scripts), whereas `CLAUDE.md` and `rules/` are *guidance Claude reads*, not configuration Claude Code enforces. Array settings like `permissions.allow` combine across all scopes; scalar settings like `model` use the most specific value. "Commands and skills are now the same mechanism" — a file at `commands/deploy.md` creates `/deploy` the same way `skills/deploy/SKILL.md` does, but skills can bundle reference docs, templates, or scripts alongside the prompt (if a skill and command share a name, the skill takes precedence).

## Global files (`~/.claude/`)

The personal counterpart that applies across every project and is never committed to any repository.

| Node | Badge | Purpose / when it loads |
|---|---|---|
| `~/.claude.json` | local | App state and UI preferences: theme, OAuth session, per-project trust decisions, your personal MCP servers, IDE toggles (`autoConnectIde`, `externalEditorContext`). Read at session start; written back when you change `/config` or approve trust prompts. Mostly managed through `/config`. |
| `~/.claude/CLAUDE.md` | local | Personal preferences across every project; loaded alongside the project CLAUDE.md at session start (both in context). When instructions conflict, project-level takes priority. |
| `~/.claude/settings.json` | local | Default settings for all projects (same keys as project settings.json). Project and local `settings.json` override any matching keys. Unlike CLAUDE.md, settings merge key by key rather than both loading into context. |
| `~/.claude/keybindings.json` | local | Custom keyboard shortcuts for the interactive CLI; read at session start and hot-reloaded on edit. Run `/keybindings` to create it; Ctrl+C/D/M and Caps Lock are reserved. |
| `~/.claude/themes/*.json` | local | Custom color themes (built-in `base` preset + `overrides`); read at session start, hot-reloaded, listed in `/theme`. |
| `~/.claude/projects/<project>/memory/` | local | **Auto memory** — Claude's notes to itself, per project, keyed by repo path. `MEMORY.md` (the index) loads at session start; topic files read on demand. |
| `~/.claude/rules/` | local | User-level rules applying to every project; same load rules as project `rules/`. |
| `~/.claude/skills/`, `commands/`, `agents/`, `workflows/` | local | Personal counterparts to the project versions, available in every project. A project workflow/agent with the same name takes precedence. |
| `~/.claude/output-styles/*.md` | local | Custom system-prompt sections; built-in Explanatory and Learning styles ship with Claude Code, custom styles go here. Take effect on the next session (the system prompt is fixed at startup for caching). |
| `~/.claude/agent-memory/` | autogen | Persistent memory for subagents with `memory: user`, persisting across all projects; for project-scoped subagent memory use `.claude/agent-memory/`. |

## What's not shown

The explorer covers files you author and edit. A few related files live elsewhere:

| File | Location | Purpose |
|---|---|---|
| `managed-settings.json` | System-level, varies by OS | Enterprise-enforced settings you can't override — take precedence over everything (see [server-managed settings](https://code.claude.com/docs/en/server-managed-settings)) |
| `CLAUDE.local.md` | Project root | Your private preferences for this project, loaded alongside CLAUDE.md; create it manually and add it to `.gitignore` |
| Installed plugins | `~/.claude/plugins` | Cloned marketplaces, installed plugin versions, and per-plugin data, managed by `claude plugin` commands; orphaned versions deleted 7 days after a plugin update or uninstall (see [plugin caching](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)) |

`~/.claude` also holds data Claude Code writes as you work — transcripts, prompt history, file snapshots, caches, and logs — covered in [Application Data](cc_claude_application_data.md).

## Choose the right file

Different kinds of customization live in different files. The source's decision table maps the change you want to the file that owns it:

| You want to | Edit | Scope |
|---|---|---|
| Give Claude project context and conventions | `CLAUDE.md` | project or global |
| Allow or block specific tool calls | `settings.json` `permissions` or `hooks` | project or global |
| Run a script before or after tool calls | `settings.json` `hooks` | project or global |
| Set environment variables for the session | `settings.json` `env` | project or global |
| Keep personal overrides out of git | `settings.local.json` | project only |
| Add a prompt or capability you invoke with `/name` | `skills/<name>/SKILL.md` | project or global |
| Define a specialized subagent with its own tools | `agents/*.md` | project or global |
| Orchestrate many subagents from a script | `workflows/*.js` | project or global |
| Connect external tools over MCP | `.mcp.json` | project only |
| Change how Claude formats responses | `output-styles/*.md` | project or global |

## Precedence

Several things can override what you put in these files:

- **Managed settings** deployed by your organization take precedence over everything.
- **CLI flags** like `--permission-mode` or `--settings` override `settings.json` for that session.
- Some **environment variables** take precedence over their equivalent setting, but this varies — check the [environment variables reference](https://code.claude.com/docs/en/env-vars) for each one.

See [settings precedence](https://code.claude.com/docs/en/settings#settings-precedence) for the full order. Note this is distinct from how CLAUDE.md layers: global and project CLAUDE.md are both *loaded into context*, whereas `settings.json` files *merge key by key* with the most specific scope winning for scalar values.

## Example: a project `settings.json`

The explorer's `settings.json` node ships this example — allow `npm test`/`npm run` without prompting, block `rm -rf`, and run Prettier after Claude edits or writes files:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test *)",
      "Bash(npm run *)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  },
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
      }]
    }]
  }
}
```

**Source**: https://code.claude.com/docs/en/claude-directory
**Last Updated**: 2026-06-13
**Status**: Active
