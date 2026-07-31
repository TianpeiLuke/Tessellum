---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - navigation
keywords:
  - messaging slash commands
  - gateway slash command surface
  - command surface matrix
  - destructive command confirmation
  - dangerous command approval
  - cli-only messaging-only both
topics:
  - Hermes Agent
  - Slash Commands
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: navigation
source_url: https://hermes-agent.nousresearch.com/docs/reference/slash-commands
access_control_group: ["general"]
---

# Hermes Agent — Messaging Slash Commands

## Overview

This is the **messaging-gateway slash-command reference** — the catalog of `/`-prefixed commands you can type inside a chat platform (Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant, Teams) to drive a running Hermes Agent session without leaving the conversation. It is one of two slash surfaces Hermes exposes; both are driven by the same central `COMMAND_REGISTRY` in `hermes_cli/commands.py`, but the messaging surface is dispatched by `gateway/run.py` (the interactive CLI surface is dispatched by `cli.py` — see the sibling note). Because the two surfaces share one registry but expose different subsets, this note also carries the **surface matrix** (which commands are CLI-only, messaging-only, or available on both) and the **destructive-command confirmation** behavior. Installed skills are exposed here too, as dynamic `/<skill-name>` commands. This note lists the command surface; the feature pages it links out to explain each command's behavior.

## Messaging slash commands

The messaging gateway supports these built-in commands inside Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant, and Teams chats. Session/lifecycle and configuration commands dominate; argument surfaces match their CLI counterparts where both exist.

| Command | Description |
|---------|-------------|
| `/start` | Platform-protocol handshake. Many platforms (Telegram, Discord, …) send `/start` automatically on first bot contact. Hermes acknowledges silently — no agent reply, no session burn — so handshakes don't waste a turn. Can also be sent explicitly to confirm reachability. |
| `/new` | Start a new conversation. |
| `/reset` | Reset conversation history. |
| `/status` | Show session info, followed by a local **Session recap** block (recent turn counts, top tools used, files touched, latest prompt + reply). |
| `/stop` | Kill all running background processes and interrupt the running agent. |
| `/model [provider:model]` | Show or change the model. Supports provider switches (`/model zai:glm-5`), custom endpoints, named custom providers, auto-detect (`/model custom`), and user-defined aliases. `--global` persists to `config.yaml`. **Note:** `/model` only switches between already-configured providers; to add a new provider or set API keys use `hermes model` from the terminal. |
| `/codex-runtime [auto\|codex_app_server\|on\|off]` | Toggle the Codex app-server runtime. Persists to `model.openai_runtime` and evicts the cached agent so the next message picks up the runtime. Effective next session. |
| `/personality [name]` | Set a personality overlay for the session. |
| `/fast [normal\|fast\|status]` | Toggle fast mode — OpenAI Priority Processing / Anthropic Fast Mode. |
| `/retry` | Retry the last message. |
| `/undo` | Remove the last exchange. |
| `/sethome` (alias: `/set-home`) | Mark the current chat as the platform home channel for deliveries. |
| `/compress [here [N] \| focus topic]` | Manually compress context. `/compress here [N]` keeps the most recent N exchanges (default 2) verbatim and summarizes the rest; a focus topic narrows what a full summary preserves. |
| `/topic [off\|help\|session-id]` | **Telegram DM only.** Manage user-managed multi-session topic mode (enable/status, `off`, `help`, or restore a session by id). |
| `/title [name]` | Set or show the session title. |
| `/resume [name]` | Resume a previously named session. |
| `/usage` | Token usage, estimated cost breakdown, context-window state, session duration, and — when available — an **Account limits** section pulled live from the provider's API. |
| `/insights [days]` | Show usage analytics. |
| `/reasoning [level\|show\|hide]` | Change reasoning effort or toggle reasoning display. |
| `/voice [on\|off\|tts\|join\|channel\|leave\|status]` | Control spoken replies. `join`/`channel`/`leave` manage Discord voice-channel mode. |
| `/rollback [number]` | List or restore filesystem checkpoints. |
| `/background <prompt>` | Run a prompt in a separate background session; results delivered back to the same chat when done. |
| `/queue <prompt>` (alias: `/q`) | Queue a prompt for the next turn without interrupting the current one. |
| `/steer <prompt>` | Inject a message after the next tool call without interrupting — picked up on the model's next iteration, not as a new turn. |
| `/goal <text>` | Set a standing goal (the Ralph loop); a judge model checks after each turn and auto-continues until done, paused/cleared, or the turn budget (default 20) is hit. Subcommands: `status`/`pause`/`resume`/`clear`. Setting a new goal mid-agent requires `/stop` first. |
| `/footer [on\|off\|status]` | Toggle the runtime-metadata footer on final replies (model, context %, cwd). |
| `/curator [status\|run\|pin\|archive]` | Background skill maintenance controls. |
| `/memory [pending\|approve\|reject\|approval]` | Review pending memory writes staged by the write-approval gate (`memory.write_approval`) right in chat, and toggle the gate. |
| `/skills [pending\|approve\|reject\|diff\|approval]` | Review pending **skill** writes staged by the write-approval gate (`skills.write_approval`). Shows a one-line gist; `/skills diff <id>` is truncated for chat. Only appears when the gate is on; search/install stay CLI-only. |
| `/kanban <action>` | Drive the multi-profile collaboration board from chat — same argument surface as the CLI. Bypasses the running-agent guard, so `unblock`/`comment`/`list --mine`/`boards switch` work mid-turn; `/kanban create …` auto-subscribes the chat to the task's terminal events. |
| `/reload-mcp` (alias: `/reload_mcp`) | Reload MCP servers from config. |
| `/yolo` | Toggle YOLO mode — skip all dangerous command approval prompts. |
| `/commands [page]` | Browse all commands and skills (paginated). |
| `/approve [session\|always]` | Approve and execute a pending dangerous command. `session` approves for this session only; `always` adds to the permanent allowlist. |
| `/deny` | Reject a pending dangerous command. |
| `/update` | Update Hermes Agent to the latest version. |
| `/restart` | Gracefully restart the gateway after draining active runs; confirms back to the requester's chat/thread when online. |
| `/debug` | Upload a debug report (system info + logs) and get shareable links. |
| `/help` | Show messaging help. |
| `/<skill-name>` | Invoke any installed skill by name. |

## Notes — surface matrix (CLI-only / messaging-only / both)

The two surfaces share one registry but expose different subsets. The §Notes matrix from the source resolves which commands live where:

- **CLI-only commands:** `/skin`, `/snapshot`, `/gquota`, `/reload`, `/tools`, `/toolsets`, `/browser`, `/config`, `/cron`, `/platforms`, `/paste`, `/image`, `/statusbar`, `/plugins`, `/busy`, `/indicator`, `/redraw`, `/clear`, `/history`, `/save`, `/copy`, `/handoff`, `/quit`.
- **Messaging-only commands:** `/sethome`, `/update`, `/restart`, `/approve`, `/deny`, `/topic`, `/commands`.
- **Both surfaces:** `/status`, `/version`, `/background`, `/queue`, `/steer`, `/voice`, `/reload-mcp`, `/reload-skills`, `/rollback`, `/debug`, `/fast`, `/footer`, `/curator`, `/kanban`, `/sessions`, `/yolo`.
- **Partial-surface caveats:**
  - `/skills` is **CLI-only for search/browse/install**; its write-approval review subcommands (`pending`, `approve`, `reject`, `diff`, `approval`) also work on messaging when `skills.write_approval` is on. `/memory` works on **both** surfaces.
  - `/verbose` is **CLI-only by default**, but can be enabled for messaging by setting `display.tool_progress_command: true` in `config.yaml`.
  - `/voice join`, `/voice channel`, and `/voice leave` are only meaningful on **Discord**.
  - In the TUI, `/sessions` shows live sessions in the current TUI process; use `/resume [name]` or `hermes --tui --resume <id-or-title>` for saved or closed transcripts.

## Confirmation prompts for destructive commands

The CLI prompts before running slash commands that throw away unsaved session state. The current destructive set is:

| Command | What it destroys |
|---------|------------------|
| `/clear` | Clears the screen and starts a fresh session — current session ID and in-memory history are gone. |
| `/new` / `/reset` | Starts a fresh session (new session ID + empty history). |
| `/undo` | Removes the last user/assistant exchange from history. |
| `/exit --delete` / `/quit --delete` | Exits **and** permanently deletes the current session's SQLite history and on-disk transcripts. |

For each, the CLI opens a three-choice modal: **Approve Once** (proceed this time), **Always Approve** (proceed and persist `approvals.destructive_slash_confirm: false` so future destructive commands run without prompting), or **Cancel**.

**Inline skip** — append `now`, `--yes`, or `-y` to bypass the modal for a single invocation:

```
/reset now
/new --yes my-session
/clear -y
/undo -y
```

This is useful when the modal doesn't render correctly on your terminal (e.g. native Windows PowerShell) or when scripting against the CLI. Set `approvals.destructive_slash_confirm: false` in `~/.hermes/config.yaml` to disable the prompts globally; set it back to `true` to re-enable.

**Source**: `inbox/hermes_agent_docs/reference/slash-commands.md` · https://hermes-agent.nousresearch.com/docs/reference/slash-commands
**Last Updated**: 2026-06-19
**Status**: Active
