---
tags:
  - resource
  - documentation
  - claude_code
  - commands
  - reference
keywords:
  - claude code commands
  - slash command
  - built-in commands
  - bundled skill command
  - bundled workflow command
  - command arguments convention
  - mcp prompt command
  - command availability
topics:
  - Claude Code
  - Commands
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/commands
access_control_group: ["general"]
---

# Claude Code — Commands Reference

## Overview

**Commands** control Claude Code from inside a session — a quick way to switch models, manage permissions, clear context, run a workflow, and more. Type `/` to see every command available to you, or type `/` followed by letters to filter. A command is only recognized at the **start of your message**; text that follows the command name is passed to it as arguments.

This note catalogues the built-in commands grouped by the area of work they serve. Most are built-in commands whose behavior is coded into the CLI; two kinds of entries are marked distinctly — **Skill** (a bundled skill: a prompt handed to Claude, which Claude can also invoke automatically when relevant) and **Workflow** (a bundled dynamic workflow that fans work out across many subagents and runs in the background). To add your own commands, see [cc_skills_overview](cc_skills_overview.md). For the task-ordered journey through these commands across a session, see the companion [cc_commands_by_workflow](cc_commands_by_workflow.md).

## Argument and Availability Conventions

- **`<arg>`** indicates a **required** argument; **`[arg]`** indicates an **optional** one.
- **Not every command appears for every user.** Availability depends on your platform, plan, and environment. For example, `/desktop` only shows on macOS and Windows when signed in with a Claude subscription, and `/upgrade` only shows on Pro and Max plans. Some commands also carry minimum-version requirements (e.g. `/cd` requires v2.1.169 or later; earlier versions report `Unknown command: /cd`), and a few have been removed (`/pr-comments` removed in v2.1.91; `/vim` removed in v2.1.92).

## Session and Context

| Command | Purpose |
|---|---|
| `/clear [name]` | Start a new conversation with empty context; the previous one stays in `/resume`. Pass a name to label it. To free context while continuing, use `/compact`. Aliases: `/reset`, `/new`. |
| `/compact [instructions]` | Free up context by summarizing the conversation so far; optionally pass focus instructions. See [how compaction handles rules, skills, and memory](https://code.claude.com/docs/en/context-window). |
| `/context [all]` | Visualize current context usage as a colored grid; shows optimization suggestions and capacity warnings. Pass `all` to expand the per-item breakdown. |
| `/btw <question>` | Ask a quick side question without adding to the conversation. |
| `/resume [session]` | Resume a conversation by ID or name, or open the picker; background sessions appear marked `bg` (v2.1.144+). Alias: `/continue`. |
| `/branch [name]` | Branch the conversation at this point to try a different direction without losing the original (return with `/resume`). To hand a side task to a background subagent instead, use `/fork`. |
| `/rename [name]` | Rename the current session; without a name, auto-generates one from history. |
| `/recap` | Generate a one-line summary of the current session on demand. |
| `/export [filename]` | Export the current conversation as plain text (to a file, or a copy/save dialog). |
| `/copy [N]` | Copy the last assistant response to clipboard; `/copy 2` copies the second-to-last. Interactive picker when code blocks are present. |
| `/teleport` | Pull a Claude Code on the web session into this terminal. Alias: `/tp`. |
| `/remote-control` | Make this session available for remote control from claude.ai. Alias: `/rc`. |
| `/desktop` | Continue the session in the Claude Code Desktop app (macOS/Windows + subscription). Alias: `/app`. |
| `/goal [condition\|clear]` | Set a goal Claude keeps working toward across turns until the condition is met. |

## Model and Effort

| Command | Purpose |
|---|---|
| `/model [model]` | Switch the AI model and save it as default; with no argument opens a picker (`s` for session-only). See [adjust effort level](https://code.claude.com/docs/en/model-config#adjust-effort-level). |
| `/effort [level\|auto]` | Set the model effort level: `low`, `medium`, `high`, `xhigh`, `max`, or `ultracode` (`max`/`ultracode` are session-only); `auto` resets to the model default. |
| `/advisor [model\|off]` | Enable or disable the advisor tool, which consults a second model for guidance at key moments (v2.1.98+). |
| `/fast [on\|off]` | Toggle fast mode on or off. |

## Agents and Parallel Work

| Command | Purpose |
|---|---|
| `/agents` | Manage agent (subagent) configurations. |
| `/fork <directive>` | Spawn a forked subagent that inherits the full conversation and works on the directive while you keep going (v2.1.161+); its result returns when done. |
| `/background [prompt]` | Detach the current session to run as a background agent and free this terminal. Alias: `/bg`. |
| `/tasks` | View and manage everything running in the background. Also `/bashes`. |
| `/stop` | Stop the current background session (only while attached). |
| `/batch <instruction>` | **Skill.** Orchestrate large-scale changes in parallel: decompose work into 5–30 independent units, then spawn one background subagent per unit in an isolated git worktree. Requires a git repository. |
| `/deep-research <question>` | **Workflow.** Fan out web searches, fetch and cross-check sources, and synthesize a cited report. |
| `/workflows` | Open the workflow progress view to watch, pause, resume, or save running and completed workflows. |
| `/schedule [description]` | Create, update, list, or run routines that execute on Anthropic-managed cloud infrastructure. Alias: `/routines`. |

## Review and Ship

| Command | Purpose |
|---|---|
| `/diff` | Open an interactive diff viewer showing uncommitted changes and per-turn diffs. |
| `/code-review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [target]` | **Skill.** Review the current diff for correctness bugs and cleanups; `--fix` applies findings, `--comment` posts inline GitHub PR comments, `ultra` runs a deep cloud review. |
| `/review [PR]` | Review a pull request locally in your current session. |
| `/security-review` | Analyze pending branch changes for security vulnerabilities (injection, auth issues, data exposure). |
| `/simplify [target]` | **Skill.** Review changed code for cleanup opportunities and apply fixes; four review agents run in parallel (v2.1.154+). Does not look for correctness bugs — use `/code-review` for those. |
| `/ultrareview [PR]` | Run a deep, multi-agent cloud-sandbox review. Preferred invocation is now `/code-review ultra`. |
| `/run` | **Skill.** Launch and drive your project's app to see a change working in the running app, not just in tests (v2.1.145+). |
| `/run-skill-generator` | **Skill.** Teach `/run` and `/verify` how to build, launch, and drive your app by writing a per-project skill (v2.1.145+). |
| `/verify` | **Skill.** Confirm a code change does what it should by building, running, and observing the app rather than relying on tests (v2.1.145+). |
| `/autofix-pr [prompt]` | Spawn a Claude Code on the web session that watches the current branch's PR and pushes fixes when CI fails or reviewers comment. Requires the `gh` CLI. |
| `/install-github-app` | Set up the Claude GitHub Actions app for a repository. |
| `/ultraplan <prompt>` | Draft a plan in an ultraplan session, review it in your browser, then execute remotely or send it to your terminal. |
| `/plan [description]` | Enter plan mode directly from the prompt; pass a description to start with that task. |

## Setup, Memory, and Config

| Command | Purpose |
|---|---|
| `/init` | Initialize a project with a `CLAUDE.md` guide. Set `CLAUDE_CODE_NEW_INIT=1` for an interactive flow covering skills, hooks, and personal memory. |
| `/memory` | Edit `CLAUDE.md` memory files, enable/disable auto-memory, and view auto-memory entries. |
| `/config` | Open the Settings interface to adjust theme, model, output style, and other preferences. Alias: `/settings`. |
| `/permissions` | Manage allow, ask, and deny rules for tool permissions in an interactive dialog. Alias: `/allowed-tools`. |
| `/sandbox` | Toggle sandbox mode (supported platforms only). |
| `/mcp [reconnect <server>\|enable\|disable [<server>\|all]]` | Manage MCP server connections and OAuth; with no argument opens the interactive list. |
| `/hooks` | View hook configurations for tool events. |
| `/skills` | List available skills; `t` sorts by token count, `Space` hides a skill, `Enter` saves. |
| `/reload-skills` | Re-scan skill and command directories so on-disk changes apply without restarting (v2.1.152+). |
| `/plugin [subcommand]` | Manage Claude Code plugins (`list`, `install`, `enable`, `disable`). |
| `/reload-plugins [--force]` | Reload all active plugins to apply pending changes without restarting. |
| `/add-dir <path>` | Add a working directory for file access during the current session (most `.claude/` config is not discovered from it). |
| `/cd <path>` | Move this session to a new working directory, preserving the prompt cache (v2.1.169+). |
| `/statusline` | Configure Claude Code's status line. |
| `/keybindings` | Open your keyboard shortcuts file. |
| `/theme` | Change the color theme (auto, light/dark, daltonized, ANSI, custom). |
| `/tui [default\|fullscreen]` | Set the terminal UI renderer and relaunch with the conversation intact. |
| `/login` / `/logout` | Sign in to / out from your Anthropic account. |

## Diagnostics and Recovery

| Command | Purpose |
|---|---|
| `/rewind` | Rewind conversation and/or code to a previous point, or summarize from a selected message. Aliases: `/checkpoint`, `/undo`. |
| `/doctor` | Diagnose and verify your Claude Code installation and settings; press `f` to have Claude fix issues. |
| `/debug [description]` | **Skill.** Enable debug logging for the session and troubleshoot by reading the debug log. |
| `/feedback [report]` | Submit feedback, report a bug, or share your conversation. Aliases: `/bug`, `/share`. |
| `/heapdump` | Write a JavaScript heap snapshot and memory breakdown for diagnosing high memory usage. |
| `/status` | Open the Settings interface (Status tab) showing version, model, account, and connectivity. |
| `/usage` | Show session cost, plan usage limits, and activity stats. Aliases: `/cost`, `/stats`. |
| `/loop [interval] [prompt]` | **Skill.** Run a prompt repeatedly while the session stays open. Alias: `/proactive`. |
| `/insights` | Generate a report analyzing your sessions — project areas, interaction patterns, and friction points. |
| `/help` | Show help and available commands. |

> This is a representative grouping of the most-used built-in commands, not the complete CLI table. The source page lists additional environment-, plan-, and platform-specific entries (e.g. `/setup-bedrock`, `/setup-vertex`, `/chrome`, `/voice`, `/team-onboarding`, `/passes`, `/stickers`, `/radio`). Per-command deep pages are linked out below and in [cc_commands_by_workflow](cc_commands_by_workflow.md); see the source page for the full table.

## Bundled Skills and Workflows

The source table marks two kinds of entries that are not plain built-ins:

- **Skill** — a bundled skill that works like skills you write yourself: a prompt handed to Claude, which Claude can also invoke automatically when relevant. In this catalogue: `/batch`, `/claude-api`, `/code-review`, `/debug`, `/fewer-permission-prompts`, `/loop`, `/run`, `/run-skill-generator`, `/simplify`, `/verify`. See [cc_bundled_skills](cc_bundled_skills.md).
- **Workflow** — a bundled dynamic workflow that fans work out across many subagents and runs in the background. In this catalogue: `/deep-research`.

## MCP Prompts as Commands

MCP servers can expose **prompts that appear as commands**. These use the format `/mcp__<server>__<prompt>` and are dynamically discovered from connected servers. See [MCP prompts](https://code.claude.com/docs/en/mcp#use-mcp-prompts-as-commands) for details.

**Source**: https://code.claude.com/docs/en/commands
**Last Updated**: 2026-06-13
**Status**: Active
