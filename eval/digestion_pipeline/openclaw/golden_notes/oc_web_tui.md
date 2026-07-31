---
tags:
  - resource
  - documentation
  - openclaw
  - web
  - tui
keywords:
  - openclaw tui
  - openclaw chat local mode
  - tui gateway mode
  - tui keyboard shortcuts
  - tui slash commands
  - local shell exec tui
  - crestodian repair loop
  - tui connection troubleshooting
  - openclaw_theme terminal colors
topics:
  - OpenClaw
  - TUI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/web/tui
access_control_group: ["general"]
---

# OpenClaw — Using the Terminal UI (TUI)

## Overview

This note is the procedure for running and operating the OpenClaw **TUI**, the terminal client for driving OpenClaw agents from a shell. It covers the two run modes — **Gateway mode** (`openclaw tui`, connecting to a running Gateway over WebSocket) and **local/embedded mode** (`openclaw chat` / `openclaw tui --local`, running the embedded agent runtime directly) — plus the on-screen layout, the agents+sessions mental model, the send/deliver toggle, pickers and overlays, the keyboard-shortcut set, the slash-command catalog, `!`-prefixed local shell execution, the local config-repair loop (Crestodian), tool-output rendering, terminal colors, history/streaming, connection registration, CLI options, and connection troubleshooting. It mirrors the `web/tui` source page.

## Quick start

### Gateway mode

1. Start the Gateway: `openclaw gateway`.
2. Open the TUI: `openclaw tui`.
3. Type a message and press Enter.

To connect to a remote Gateway, pass the WebSocket URL and token explicitly; use `--password` instead if your Gateway uses password auth:

```bash
openclaw tui --url ws://<host>:<port> --token <gateway-token>
```

### Local mode

Run the TUI without a Gateway with `openclaw chat` or, equivalently, `openclaw tui --local`. Key behaviors: `openclaw chat` and `openclaw terminal` are aliases for `openclaw tui --local`; `--local` cannot be combined with `--url`, `--token`, or `--password`; local mode uses the embedded agent runtime directly, so most local tools work but Gateway-only features are unavailable. After a config file has authored settings, bare `openclaw` and `openclaw crestodian` also use this TUI shell, with **Crestodian** as the local setup and repair chat backend.

## What you see

The TUI screen has five regions: a **Header** (connection URL, current agent, current session); a **Chat log** (user messages, assistant replies, system notices, tool cards); a **Status line** (connection/run state — connecting, running, streaming, idle, error); a **Footer** (agent + session + model + goal state + think/fast/verbose/trace/reasoning + token counts + deliver, and, when `tui.footer.showRemoteHost` is enabled, the connection host for remote Gateway connections); and an **Input** (text editor with autocomplete).

## Mental model: agents + sessions

Agents are unique slugs (e.g. `main`, `research`) and the Gateway exposes the list; sessions belong to the current agent. Session keys are stored as `agent:<agentId>:<sessionKey>`: typing `/session main` expands to `agent:<currentAgent>:main`, while typing `/session agent:other:main` switches to that agent session explicitly. Session scope is either `per-sender` (default — each agent has many sessions) or `global` (the TUI always uses the `global` session and the picker may be empty). The current agent + session are always visible in the footer.

To show the Gateway host for non-local URL-backed connections, opt in with the following; loopback and embedded local connections never show a host label:

```bash
openclaw config set tui.footer.showRemoteHost true
```

If the session has a [goal](https://docs.openclaw.ai/tools/goal), the footer shows its compact state such as `Pursuing goal`, `Goal paused (/goal resume)`, or `Goal achieved`. When started without `--session`, gateway-mode TUI resumes the last selected session for the same gateway, agent, and session scope if that session still exists; passing `--session`, `/session`, `/new`, or `/reset` remains explicit.

## Sending + delivery

Messages are sent to the Gateway, but delivery to providers is **off by default**. The TUI is an internal source surface like WebChat, not a generic outbound channel: harnesses that require `tools.message` for visible replies can satisfy the active TUI turn with a targetless `message.send`, while explicit provider delivery still uses normal configured channels and never falls back to `lastChannel`. Turn delivery on with `/deliver on`, the Settings panel, or by starting with `openclaw tui --deliver`.

## Pickers + overlays

The TUI exposes four pickers/overlays: the **Model picker** lists available models and sets the session override; the **Agent picker** chooses a different agent; the **Session picker** shows up to 50 sessions for the current agent updated in the last 7 days (use `/session <key>` to jump to an older known session); and **Settings** toggles deliver, tool output expansion, and thinking visibility.

## Keyboard shortcuts

- `Enter`: send message
- `Esc`: abort active run
- `Ctrl+C`: clear input (press twice to exit)
- `Ctrl+D`: exit
- `Ctrl+L`: model picker
- `Ctrl+G`: agent picker
- `Ctrl+P`: session picker
- `Ctrl+O`: toggle tool output expansion
- `Ctrl+T`: toggle thinking visibility (reloads history)

## Slash commands

**Core:** `/help`; `/status`; `/agent <id>` (or `/agents`); `/session <key>` (or `/sessions`); `/model <provider/model>` (or `/models`).

**Session controls:** `/think <off|minimal|low|medium|high>`; `/fast <status|on|off>`; `/verbose <on|full|off>`; `/trace <on|off>`; `/reasoning <on|off|stream>`; `/usage <off|tokens|full>`; `/goal [status] | /goal start <objective> | /goal pause|resume|complete|block|clear`; `/elevated <on|off|ask|full>` (alias: `/elev`); `/activation <mention|always>`; `/deliver <on|off>`.

**Session lifecycle:** `/new` or `/reset` (reset the session); `/abort` (abort the active run); `/settings`; `/exit`.

**Local mode only:** `/auth [provider]` opens the provider auth/login flow inside the TUI.

Other Gateway slash commands (for example, `/context`) are forwarded to the Gateway and shown as system output. See [Slash commands](https://docs.openclaw.ai/tools/slash-commands).

## Local shell commands

Prefix a line with `!` to run a local shell command on the TUI host. The TUI prompts once per session to allow local execution; declining keeps `!` disabled for the session. Commands run in a fresh, non-interactive shell in the TUI working directory (no persistent `cd`/env), and receive `OPENCLAW_SHELL=tui-local` in their environment. A lone `!` is sent as a normal message, and leading spaces do not trigger local exec.

## Repair configs from the local TUI

Use local mode when the current config already validates and you want the embedded agent to inspect it on the same machine, compare it against the docs, and help repair drift without depending on a running Gateway. If `openclaw config validate` is already failing, start with `openclaw configure` or `openclaw doctor --fix` first — `openclaw chat` does not bypass the invalid-config guard.

The typical loop is: (1) start local mode with `openclaw chat`; (2) ask the agent what you want checked, for example *"Compare my gateway auth config with the docs and suggest the smallest fix."*; (3) use local shell commands for exact evidence and validation; (4) apply narrow changes with `openclaw config set` or `openclaw configure`, then rerun `!openclaw config validate`; (5) if Doctor recommends an automatic migration or repair, review it and run `!openclaw doctor --fix`. The evidence/validation step (3) uses local `!`-prefixed commands:

```text
!openclaw config file
!openclaw docs gateway auth token secretref
!openclaw config validate
!openclaw doctor
```

Tips: prefer `openclaw config set` or `openclaw configure` over hand-editing `openclaw.json`; `openclaw docs "<query>"` searches the live docs index from the same machine; `openclaw config validate --json` is useful for structured schema and SecretRef/resolvability errors.

## Tool output, terminal colors, history + streaming

**Tool output:** tool calls show as cards with args + results, `Ctrl+O` toggles collapsed/expanded views, and while tools run partial updates stream into the same card. **Terminal colors:** the TUI keeps assistant body text in your terminal's default foreground so dark and light terminals both stay readable; if your terminal uses a light background and auto-detection is wrong, set `OPENCLAW_THEME=light` before launching `openclaw tui`, or set `OPENCLAW_THEME=dark` to force the original dark palette. **History + streaming:** on connect the TUI loads the latest history (default 200 messages), streaming responses update in place until finalized, and the TUI also listens to agent tool events for richer tool cards.

## Connection details

The TUI registers with the Gateway as `mode: "tui"`. Reconnects show a system message, and event gaps are surfaced in the log.

## Options

- `--local`: Run against the local embedded agent runtime
- `--url <url>`: Gateway WebSocket URL (defaults to config or `ws://127.0.0.1:<port>`)
- `--token <token>`: Gateway token (if required)
- `--password <password>`: Gateway password (if required)
- `--session <key>`: Session key (default: `main`, or `global` when scope is global)
- `--deliver`: Deliver assistant replies to the provider (default off)
- `--thinking <level>`: Override thinking level for sends
- `--message <text>`: Send an initial message after connecting
- `--timeout-ms <ms>`: Agent timeout in ms (defaults to `agents.defaults.timeoutSeconds`)
- `--history-limit <n>`: History entries to load (default `200`)

When you set `--url`, the TUI does not fall back to config or environment credentials: pass `--token` or `--password` explicitly, and missing explicit credentials is an error. In local mode, do not pass `--url`, `--token`, or `--password`.

## Troubleshooting

**No output after sending a message:** run `/status` in the TUI to confirm the Gateway is connected and idle/busy; check the Gateway logs with `openclaw logs --follow`; confirm the agent can run with `openclaw status` and `openclaw models status`; and if you expect messages in a chat channel, enable delivery (`/deliver on` or `--deliver`).

**Connection troubleshooting:** `disconnected` means the Gateway is not reachable — ensure it is running and your `--url/--token/--password` are correct; **no agents in picker** means you should check `openclaw agents list` and your routing config; an **empty session picker** means you might be in global scope or have no sessions yet.

**Source**: OpenClaw documentation — `web/tui` (mirror `inbox/openclaw_docs/web/tui.md`)
**Last Updated**: 2026-06-22
**Status**: Active
