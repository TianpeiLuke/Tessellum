---
tags:
  - resource
  - documentation
  - claude_code
  - cli
  - commands
keywords:
  - claude cli commands
  - claude subcommands
  - start interactive session
  - resume conversation
  - background session management
  - claude update install auth
  - claude mcp plugin
  - typo suggestion
topics:
  - Claude Code
  - CLI Reference
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/cli-reference
access_control_group: ["general"]
---

# Claude Code — CLI Commands

## Overview

The `claude` binary exposes a catalog of subcommands for starting sessions, piping content, resuming conversations, managing updates and authentication, and operating background sessions. This note documents that command catalog from the CLI reference; the runtime **flags** that customize each command live in the sibling note [CLI Flags](cc_cli_flags.md).

Commands fall into a few groups: **starting and resuming sessions** (`claude`, `claude "query"`, `claude -p`, `claude -c`, `claude -r`), **lifecycle/install** (`claude update`, `claude install`), **authentication** (`claude auth login/logout/status`, `claude setup-token`), **background-session management** (`claude agents`, `attach`, `daemon`, `logs`, `respawn`, `rm`, `stop`), and **integrations** (`claude mcp`, `claude plugin`, `claude remote-control`, `claude ultrareview`, `claude project purge`, `claude auto-mode`). If you mistype a subcommand, Claude Code suggests the closest match and exits without starting a session.

## Start, pipe, and resume sessions

These are the everyday entry points into Claude Code:

- `claude` — start an interactive session.
- `claude "query"` — start an interactive session with an initial prompt (e.g. `claude "explain this project"`).
- `claude -p "query"` — query via the SDK, then exit (e.g. `claude -p "explain this function"`).
- `cat file | claude -p "query"` — process piped content (e.g. `cat logs.txt | claude -p "explain"`).
- `claude -c` — continue the most recent conversation in the current directory.
- `claude -c -p "query"` — continue via the SDK (e.g. `claude -c -p "Check for type errors"`).
- `claude -r "<session>" "query"` — resume a session by ID or name (e.g. `claude -r "auth-refactor" "Finish this PR"`).

## Update, install, and authenticate

- `claude update` — update to the latest version.
- `claude install [version]` — install or reinstall the native binary. Accepts a version like `2.1.118`, or `stable` or `latest` (e.g. `claude install stable`).
- `claude auth login` — sign in to your Anthropic account. Use `--email` to pre-fill your email address, `--sso` to force SSO authentication, and `--console` to sign in with Anthropic Console for API usage billing instead of a Claude subscription.
- `claude auth logout` — log out from your Anthropic account.
- `claude auth status` — show authentication status as JSON. Use `--text` for human-readable output. Exits with code 0 if logged in, 1 if not.
- `claude setup-token` — generate a long-lived OAuth token for CI and scripts. Prints the token to the terminal without saving it. Requires a Claude subscription. See [Generate a long-lived token](https://code.claude.com/docs/en/authentication).

## Manage background sessions

These commands monitor, dispatch, and control parallel [background sessions](https://code.claude.com/docs/en/agent-view):

- `claude agents` — open the agent view to monitor and dispatch parallel background sessions. Use `--cwd <path>` to show only sessions started under that directory, or `--json` to print active sessions as a JSON array for scripting (`--json --all` also includes completed background sessions). Pass `--permission-mode`, `--model`, `--effort`, or `--agent` to set defaults for dispatched sessions. Also accepts `--settings`, `--add-dir`, `--plugin-dir`, and `--mcp-config` like the top-level `claude` command. Opening agent view requires an interactive terminal.
- `claude attach <id>` — attach to a background session in this terminal.
- `claude logs <id>` — print recent output from a background session.
- `claude respawn <id>` — restart a background session, running or stopped, with its conversation intact. Use `--all` to restart every running session, e.g. to pick up an updated Claude Code binary.
- `claude rm <id>` — remove a background session from the list. The conversation transcript stays on your local machine, available through `claude --resume`.
- `claude stop <id>` — stop a background session. Also accepts `claude kill`.
- `claude daemon status` — print the background-session supervisor's state, version, socket directory, and worker count for diagnostics. Exits 1 if the supervisor isn't running.
- `claude daemon stop --any` — stop the background-session supervisor and the sessions it hosts. Pass `--keep-workers` to leave background sessions running so the next supervisor reconnects to them. `--any` confirms stopping an on-demand supervisor, which is the default.

## Configure integrations and run tools

- `claude mcp` — configure [Model Context Protocol (MCP) servers](https://code.claude.com/docs/en/mcp).
- `claude plugin` — manage [plugins](https://code.claude.com/docs/en/plugins) (alias: `claude plugins`); see the plugin reference for subcommands.
- `claude remote-control` — start a [Remote Control](https://code.claude.com/docs/en/remote-control) server to control Claude Code from Claude.ai or the Claude app. Runs in server mode (no local interactive session).
- `claude auto-mode defaults` — print the built-in [auto mode](https://code.claude.com/docs/en/permission-modes) classifier rules as JSON. Use `claude auto-mode config` to see your effective config with settings applied.
- `claude project purge [path]` — delete all local Claude Code state for a project: transcripts, task lists, debug logs, file-edit history, prompt history lines, and the project's entry in `~/.claude.json`. Omit `[path]` to pick from an interactive list. Flags: `--dry-run` to preview, `-y`/`--yes` to skip confirmation, `-i`/`--interactive` to confirm each item, `--all` for every project.
- `claude ultrareview [target]` — run [ultrareview](https://code.claude.com/docs/en/ultrareview) non-interactively. Prints findings to stdout and exits 0 on success or 1 on failure. Use `--json` for the raw payload and `--timeout <minutes>` to override the 30-minute default.

## Typo-suggestion behavior

If you mistype a subcommand, Claude Code suggests the closest match and exits without starting a session. For example, `claude udpate` prints `Did you mean claude update?`.

**Source**: https://code.claude.com/docs/en/cli-reference
**Last Updated**: 2026-06-13
**Status**: Active
