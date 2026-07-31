---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - tui
keywords:
  - openclaw tui
  - openclaw chat terminal
  - local embedded agent runtime
  - gateway websocket url token
  - tui secretref auth resolution
  - tui session key agent workspace
  - tui footer showRemoteHost goal
  - openclaw config repair loop
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/tui
access_control_group: ["general"]
---

# OpenClaw — The `openclaw tui` Terminal UI Command

## Overview

This note documents the `openclaw tui` command — the procedure for opening OpenClaw's terminal UI either connected to a running Gateway or running in **local embedded mode** — mirroring the `cli/tui` source page. It covers the full option table (`--local`, `--url`, `--token`, `--password`, `--session`, `--deliver`, `--thinking`, `--message`, `--timeout-ms`, `--history-limit`), the `chat` / `terminal` aliases (which imply `--local`), the operational Notes (SecretRef auth resolution, agent-workspace auto-select, the footer host label, local-mode `/auth` and plugin approval gates, `/goal` session goals), runnable Examples, and the local-mode config repair loop driven from inside the TUI.

## Usage and Modes

`openclaw tui` opens the terminal UI connected to the Gateway, or runs it in **local embedded mode**. Two operating modes are supported: a Gateway-backed mode (the default — the TUI attaches to a running Gateway over its WebSocket URL, which is remote-friendly) and a `--local` mode that runs against the local embedded agent runtime directly instead of a Gateway. Local mode uses the embedded agent runtime directly; most local tools work, but Gateway-only features are unavailable.

## Options

The full option table from the source page (flag, default, description):

| Flag | Default | Description |
| --- | --- | --- |
| `--local` | `false` | Run against the local embedded agent runtime instead of a Gateway. |
| `--url <url>` | `gateway.remote.url` from config | Gateway WebSocket URL. |
| `--token <token>` | (none) | Gateway token if required. |
| `--password <pass>` | (none) | Gateway password if required. |
| `--session <key>` | `main` (or `global` when scope is global) | Session key. Inside an agent workspace it auto-selects that agent unless prefixed. |
| `--deliver` | `false` | Deliver assistant replies through configured channels. |
| `--thinking <level>` | (model default) | Thinking level override. |
| `--message <text>` | (none) | Send an initial message after connecting. |
| `--timeout-ms <ms>` | `agents.defaults.timeoutSeconds` | Agent timeout. Invalid values log a warning and are ignored. |
| `--history-limit <n>` | `200` | History entries to load on attach. |

## Aliases and Notes

`openclaw chat` and `openclaw terminal` invoke the same command with `--local` implied — that is, `chat` and `terminal` are aliases for `openclaw tui --local`. The source page documents the following operational notes:

- `--local` cannot be combined with `--url`, `--token`, or `--password`.
- `tui` resolves configured gateway auth SecretRefs for token/password auth when possible (`env` / `file` / `exec` providers).
- When launched from inside a configured agent workspace directory, the TUI auto-selects that agent for the session key default (unless `--session` is explicitly `agent:<id>:...`).
- To show the Gateway hostname in the footer for non-local URL-backed connections, run `openclaw config set tui.footer.showRemoteHost true`. The host label is off by default and never appears for loopback or embedded local connections.
- Local mode uses the embedded agent runtime directly. Most local tools work, but Gateway-only features are unavailable.
- Local mode adds `/auth [provider]` inside the TUI command surface.
- Plugin approval gates still apply in local mode. Tools that require approval prompt for a decision in the terminal; nothing is silently auto-approved because the Gateway is not involved.
- Session goals appear in the footer and can be managed with `/goal`.

## Examples

The source page lists these invocations, including the agent-workspace auto-select case:

```bash
openclaw chat
openclaw tui --local
openclaw tui
openclaw tui --url ws://127.0.0.1:18789 --token <token>
openclaw tui --session main --deliver
openclaw chat --message "Compare my config to the docs and tell me what to fix"
# when run inside an agent workspace, infers that agent automatically
openclaw tui --session bugfix
```

## Config Repair Loop

Local mode is the recommended path to repair configuration from the same terminal: use local mode when the current config **already validates** and you want the embedded agent to inspect it, compare it against the docs, and help repair it. If `openclaw config validate` is already failing, use `openclaw configure` or `openclaw doctor --fix` first — `openclaw chat` does not bypass the invalid-config guard. Start the session with:

```bash
openclaw chat
```

Then, inside the TUI, the source shows these `!`-prefixed shell-out commands used to inspect config and the relevant docs:

```text
!openclaw config file
!openclaw docs gateway auth token secretref
!openclaw config validate
!openclaw doctor
```

Apply targeted fixes with `openclaw config set` or `openclaw configure`, then rerun `openclaw config validate`.

**Source**: OpenClaw documentation — `cli/tui` (mirror `inbox/openclaw_docs/cli/tui.md`)
**Last Updated**: 2026-06-22
**Status**: Active
