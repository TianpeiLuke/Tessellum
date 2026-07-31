---
tags:
  - resource
  - documentation
  - claude_code
  - agent_view
  - dispatch
keywords:
  - dispatch background agents
  - claude --bg
  - background session
  - worktree isolation
  - claude agents
  - permission mode model effort
  - manage sessions from the shell
  - claude attach logs stop respawn
topics:
  - Claude Code
  - Agent View
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-view
access_control_group: ["general"]
---

# Dispatch Background Agents

## Overview

A **background session** is a full Claude Code conversation that keeps running without a terminal attached, monitored from [agent view](https://code.claude.com/docs/en/agent-view). This note is the **how-to for starting and managing those sessions**: the three dispatch entry points (the agent view input, `/background` from inside a session, and `claude --bg` from the shell), how each session's file edits are isolated in a git worktree, how to set the model / permission mode / effort, how settings, plugins, and MCP servers are loaded and passed through, and the shell commands that attach, inspect, stop, respawn, and remove sessions.

Each session starts in your working directory, uses your subscription quota independently, and persists its model, permission mode, and configuration flags across supervisor stop/restart. The monitoring side of agent view (state icons, peek/reply, organize, filter, shortcuts) is covered in [cc_agent_view_monitor.md](cc_agent_view_monitor.md); the supervisor process and on-disk state layout are covered in [cc_background_session_hosting.md](cc_background_session_hosting.md).

## Dispatch from agent view

Type a prompt in the input at the bottom of agent view and press `Enter` to start a new background session. The session is named automatically from the prompt; rename it later with `Ctrl+R`. Paste an image into the prompt to include a screenshot or diagram with the task.

Prefix or mention parts of the prompt to control how the session starts:

| Input | Effect |
| :--- | :--- |
| `<agent-name> <prompt>` | If the first word matches a custom subagent name, that subagent runs as the session's main agent with the configuration from its frontmatter |
| `@<agent-name>` | Mention a custom subagent anywhere in the prompt to run it as the main agent |
| `@<repo>` | Mention a repository under the directory you opened agent view from to run the session there |
| `/<command>` | Suggest skills and commands to dispatch as the prompt |
| `! <command>` | Run a shell command as a background job instead of starting a Claude session. The job appears as a row you can attach to, watch, and detach from |
| `#<number>` or a pull request URL | If a session is already working on that PR, select it instead of dispatching |
| `Shift+Enter` | Dispatch and immediately attach to the new session |

A small set of commands run in agent view itself instead of dispatching: `/exit` and `/quit` close agent view, and `/logout` signs you out. Every other command and skill is sent to a new background session as its first prompt.

When the same `@name` matches both a subagent and a sibling repository, the subagent takes precedence. The bare first-word match also applies, so a prompt that happens to begin with one of your subagent names dispatches that subagent rather than treating the word as plain text. Use the `@` form to be explicit, or start the prompt with a different word to avoid the match.

**Dispatch to a specific directory.** A new session runs in the directory you opened agent view from. To target a different directory: open `claude agents` in that directory; open `claude agents` in a parent directory that holds several repositories and mention one with `@<repo>`; or, from the shell, `cd` into the directory and run `claude --bg "<prompt>"`. When agent view is grouped by directory, the highlighted row's directory becomes the dispatch target.

## Dispatch from inside a session

Run `/background` or its alias `/bg` to move the current conversation into a background session. Pass a prompt such as `/bg run the test suite and fix any failures` to give one more instruction first. If Claude is responding when you run `/bg`, the response continues in the background session.

Backgrounding starts a fresh process that resumes from the saved conversation, so running subagents, monitors, and background commands do **not** transfer; Claude asks you to confirm before backgrounding when any are running. Once in the background, the session can start new subagents, monitors, and background commands, and those keep running across later detach and reattach.

Configuration flags from the original launch carry through to the backgrounded session, so its MCP servers, settings, and fallback model remain in effect: `--mcp-config` and `--strict-mcp-config`, `--settings`, `--add-dir`, `--plugin-dir`, `--fallback-model`, and `--allow-dangerously-skip-permissions`. Directories added during the session with `/add-dir` also carry through. Carrying `--allow-dangerously-skip-permissions` through keeps `bypassPermissions` reachable but grants nothing new — the mode still requires the same one-time interactive acceptance before any session can use it.

## Dispatch from your shell

Pass `--bg` to start a session that goes straight to the background:

```bash theme={null}
claude --bg "investigate the flaky SettingsChangeDetector test"
```

To run a specific subagent as the session's main agent, combine `--bg` with `--agent`; pass `--name` to set the session's display name in agent view instead of the auto-generated one:

```bash theme={null}
claude --agent code-reviewer --bg "address review comments on PR 1234"
claude --bg --name "flaky-test-fix" "investigate the flaky SettingsChangeDetector test"
```

After backgrounding, Claude prints the session's short ID and the commands for managing it (when you pass `--name`, the name appears after the short ID):

```text theme={null}
backgrounded · 7c5dcf5d · flaky-test-fix
  claude agents             list sessions
  claude attach 7c5dcf5d    open in this terminal
  claude logs 7c5dcf5d      show recent output
  claude stop 7c5dcf5d      stop this session
```

**Run a shell command instead of a Claude session.** Type `!` as the first character of the dispatch input (e.g. `! pytest -x`), or launch it directly with `claude --bg --exec 'pytest -x'`. The command runs as a PTY-backed job and appears as a row with the most recent output line as its status; no model is invoked and the output is not sent to any session. See the output by attaching, pressing `Space` to peek, or running `claude logs <id>`. The captured output stays in memory (not written to disk) and the row cleans up automatically about five minutes after the command exits.

## How file edits are isolated

Every background session — whether started from agent view, `/bg`, or `claude --bg` — starts in your working directory. Before editing files, Claude moves the session into an isolated git worktree under `.claude/worktrees/`, so parallel sessions can read the same checkout but each writes to its own (worktree mechanics: [worktrees](https://code.claude.com/docs/en/worktrees)).

Claude **skips** the worktree when: the session is already inside a linked git worktree (Claude-created or one you made with `git worktree add`); the working directory isn't a git repository and no `WorktreeCreate` hook is configured; or the write is outside the working directory.

To turn off worktree isolation for a repository where git worktrees are impractical, set `worktree.bgIsolation` to `"none"` in the project's `.claude/settings.json` (requires Claude Code v2.1.143 or later):

```json theme={null}
{
  "worktree": {
    "bgIsolation": "none"
  }
}
```

Outside a git repository, sessions write to the working directory directly and aren't isolated from each other, so avoid dispatching parallel sessions that edit the same files; with a different version control system, configure a `WorktreeCreate` hook. A subagent the background session spawns inherits the session's working directory, so its edits land in the session's worktree rather than your working copy — to give a subagent its own worktree, set `isolation: worktree` in its frontmatter or pass `isolation: "worktree"` when spawning it.

## Set the model, permission mode, and effort

The model in the agent view header is the dispatch default; new sessions use it, sourced from the `model` setting in your user settings. Override it for the whole agent view session with `--model`, or per-session by passing `--model` with `claude --bg`, by attaching and pressing `s` on a model in `/model` (persists if the session is respawned), or by dispatching a subagent whose frontmatter sets a `model` field.

A background session reads its settings from the directory it runs in. The permission mode depends on how the session started: backgrounding an existing session with `/bg` or `←` keeps the current mode (a session you switched to `acceptEdits` or `auto` stays there), while dispatching from the agent view input or `claude --bg` uses the `defaultMode` from that directory's settings, or the `permissionMode` from the dispatched subagent's frontmatter. The permission mode, model, effort, and carried configuration flags all persist when the supervisor later stops and restarts the process.

To set defaults for every session you dispatch from agent view, pass any of `--permission-mode`, `--model`, `--effort`, or `--agent` when opening it:

```bash theme={null}
claude agents --permission-mode plan --model opus --effort high
```

`--agent` sets the subagent used when a dispatch prompt does not name one; it defaults to the `agent` setting if set, otherwise the built-in catch-all `claude` agent (naming a subagent in the dispatch input overrides both). `claude agents` also accepts `--dangerously-skip-permissions` (shorthand for `--permission-mode bypassPermissions`) and `--allow-dangerously-skip-permissions` (makes `bypassPermissions` available in each dispatched session's `Shift+Tab` cycle without starting in that mode). Using `bypassPermissions` or `auto` is refused until you have accepted that mode by running `claude` with it once interactively, since those modes let an unwatched session act without approval (permission detail: [permissions](https://code.claude.com/docs/en/permissions)).

## Settings, plugins, and MCP servers

Agent view accepts the same configuration flags as `claude` (requires v2.1.142+). Each flag applies to agent view itself and is passed through to every dispatched session, so a plugin or MCP server loaded this way is available in those sessions too:

| Flag | Effect |
| :--- | :--- |
| `--settings <file-or-json>` | Override settings for agent view and dispatched sessions |
| `--add-dir <path>` | Grant file access to an additional directory |
| `--plugin-dir <path>` | Load a plugin from a local directory |
| `--mcp-config <file-or-json>` | Load MCP servers from a config file or JSON string |
| `--strict-mcp-config` | Use only the MCP servers from `--mcp-config`, ignoring other MCP configuration |

Repeat `--add-dir`, `--plugin-dir`, or `--mcp-config` once per value — the space-separated form (`--add-dir a b c`) is not supported with `claude agents`. Example opening agent view with a settings override and one extra directory: `claude agents --settings ./ci-settings.json --add-dir ../shared-lib`.

## Manage sessions from the shell

Every background session has a short ID (printed when you start with `claude --bg`, and equal to the session's directory name under `~/.claude/jobs/`). These commands are useful for scripting or when you don't want to open agent view:

| Command | Purpose |
| :--- | :--- |
| `claude agents` | Open agent view |
| `claude agents --cwd <path>` | Open agent view scoped to sessions started under `<path>` |
| `claude agents --json` | Print active sessions as a JSON array and exit (add `--all` to include completed sessions; each entry has `cwd`, `kind`, `startedAt`, and for background entries `id`, `state`, etc.) |
| `claude attach <id>` | Attach to a session in this terminal |
| `claude logs <id>` | Print the session's recent output |
| `claude stop <id>` | Stop a session (also accepts `claude kill`) |
| `claude respawn <id>` | Restart a session, running or stopped, with its conversation intact (e.g. to pick up an updated binary) |
| `claude respawn --all` | Restart every running session |
| `claude rm <id>` | Remove a session from the list; keeps a worktree with uncommitted changes and prints its path; transcript stays available via `claude --resume` |
| `claude daemon status` | Print the supervisor's state, version, socket directory, and worker count |
| `claude daemon stop --any` | Stop the supervisor and the sessions it hosts (pass `--keep-workers` to leave sessions running so the next supervisor reconnects) |

**Source**: https://code.claude.com/docs/en/agent-view
**Last Updated**: 2026-06-13
**Status**: Active
