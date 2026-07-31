---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - sessions
keywords:
  - openclaw sessions multiple chats
  - openclaw new reset compact
  - session idleminutes context truncation
  - openclaw logs where
  - openclaw gateway restart stop start
  - abort triggers stop the agent
  - queue steer followup collect interrupt
  - verbose trace reasoning off
topics:
  - OpenClaw
  - Sessions & Logging FAQ
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/faq
access_control_group: ["general"]
---

# OpenClaw — FAQ: Sessions, Logging & Chat Control

## Overview

This note answers the OpenClaw general-FAQ questions about managing conversations and controlling a running agent: starting fresh sessions and running multiple concurrent chats, finding logs and turning on more detail when something fails, restarting/stopping the Gateway service, the chat commands plus standalone abort triggers for "it will not stop", and a miscellaneous default-model question. It mirrors the four `help/faq` H2 sections assigned to this note — **Sessions and multiple chats**, **Logging and debugging**, **Chat commands, aborting tasks, and "it will not stop"**, and **Miscellaneous** — reproducing the verbatim commands and config keys from the source accordions. For env-var loading see `oc_help_environment`; for the dev-side debug toolkit see `oc_help_debugging`; for on-disk session storage see `oc_help_faq_storage_memory`.

## Sessions and Multiple Chats

**Start a fresh conversation.** Send `/new` or `/reset` as a standalone message.

**Automatic session reset.** Sessions can expire after `session.idleMinutes`, but this is disabled by default (default `0`). Set it to a positive value to enable idle expiry; when enabled, the *next* message after the idle period starts a fresh session id for that chat key. This does not delete transcripts — it just starts a new session.

```json5
{
  session: {
    idleMinutes: 240,
  },
}
```

**Teams of instances (one coordinator + many agents).** Possible via multi-agent routing and sub-agents — one coordinator agent plus several worker agents with their own workspaces and models. The source frames this as best seen as a "fun experiment": it is token heavy and often less efficient than one bot with separate sessions. The envisioned model is one bot you talk to, with different sessions for parallel work, that can also spawn sub-agents when needed.

**Context truncated mid-task.** Session context is limited by the model window; long chats, large tool outputs, or many files can trigger compaction or truncation. What helps: ask the bot to summarize the current state and write it to a file; use `/compact` before long tasks and `/new` when switching topics; keep important context in the workspace and ask the bot to read it back; use sub-agents for long or parallel work so the main chat stays smaller; pick a model with a larger context window if it happens often.

**"context too large" errors.** Use **Compact** (`/compact`, or `/compact <instructions>` to guide the summary — keeps the conversation but summarizes older turns) or **Reset** (`/new` / `/reset` — fresh session ID for the same chat key). If it keeps happening, enable or tune session pruning (`agents.defaults.contextPruning`) to trim old tool output, or use a larger-context model.

**Stale-history provider error.** The error `LLM request rejected: messages.content.tool_use.input field required` is a provider validation error — the model emitted a `tool_use` block without the required `input`, usually meaning the session history is stale or corrupted (often after long threads or a tool/schema change). Fix: start a fresh session with `/new` (standalone message).

**Heartbeat messages every 30 minutes.** Heartbeats run every **30m** by default (**1h** when using OAuth auth). Tune or disable:

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "2h", // or "0m" to disable
      },
    },
  },
}
```

If `HEARTBEAT.md` exists but is effectively empty (only blank lines, Markdown/HTML comments, headings like `# Heading`, fence markers, or empty checklist stubs), OpenClaw skips the heartbeat run to save API calls; if the file is missing, the heartbeat still runs and the model decides what to do. Per-agent overrides use `agents.list[].heartbeat`.

**Reset while keeping it installed.** Use `openclaw reset` (or non-interactive `openclaw reset --scope full --yes --non-interactive`), then re-run setup with `openclaw onboard --install-daemon`. Onboarding also offers Reset if it sees an existing config. If you used profiles (`--profile` / `OPENCLAW_PROFILE`), reset each state dir (defaults are `~/.openclaw-<profile>`). Dev reset: `openclaw gateway --dev --reset` (dev-only; wipes dev config + credentials + sessions + workspace).

**Group vs DM sessions and limits.** Direct chats collapse to the main session by default; groups/channels have their own session keys, and Telegram topics / Discord threads are separate sessions. There are no hard limits on workspaces/agents — dozens or hundreds are fine — but watch for disk growth (sessions + transcripts live under `~/.openclaw/agents/<agentId>/sessions/`), token cost (more agents means more concurrent model usage), and ops overhead (per-agent auth profiles, workspaces, channel routing). Keep one active workspace per agent (`agents.defaults.workspace`), prune old sessions if disk grows, and use `openclaw doctor` to spot stray workspaces and profile mismatches. Slack and other channels can be bound to specific agents via Multi-Agent Routing.

## Logging and Debugging

**Where logs are.** Structured file logs live at `/tmp/openclaw/openclaw-YYYY-MM-DD.log`. Set a stable path via `logging.file`; file log level is controlled by `logging.level`; console verbosity is controlled by `--verbose` and `logging.consoleLevel`. Fastest log tail is `openclaw logs --follow`. Service/supervisor logs (when the Gateway runs via launchd/systemd):

- macOS launchd stdout: `~/Library/Logs/openclaw/gateway.log` (profiles use `gateway-<profile>.log`; stderr is suppressed)
- Linux: `journalctl --user -u openclaw-gateway[-<profile>].service -n 200 --no-pager`
- Windows: `schtasks /Query /TN "OpenClaw Gateway (<profile>)" /V /FO LIST`

**Fastest way to get more detail when something fails.** Start the Gateway with `--verbose` to get more console detail, then inspect the log file for channel auth, model routing, and RPC errors.

**Start/stop/restart the Gateway service.** Use the gateway helpers `openclaw gateway status` and `openclaw gateway restart`. If you run the gateway manually, `openclaw gateway --force` can reclaim the port. To completely stop then start the supervised service (launchd on macOS, systemd on Linux): `openclaw gateway stop` then `openclaw gateway start`; if you are running in the foreground, stop with Ctrl-C then `openclaw gateway run`. ELI5 distinction: `openclaw gateway restart` restarts the background service, while `openclaw gateway` runs the gateway in the foreground for the current terminal session.

**Restart after closing a Windows terminal.** There are three Windows install modes. (1) Windows Hub local setup — the native app manages a local app-owned WSL Gateway; open OpenClaw Companion from the Start menu or tray, then use Gateway Setup or the Connections tab. (2) Manual WSL2 Gateway — open PowerShell, enter WSL, then `openclaw gateway status` / `openclaw gateway restart` (or `openclaw gateway run` in the foreground if no service). (3) Native Windows CLI/Gateway — open PowerShell and run `openclaw gateway status` / `openclaw gateway restart` (or `openclaw gateway run` for manual foreground).

**Gateway up but replies never arrive.** Run a quick health sweep:

```bash
openclaw status
openclaw models status
openclaw channels status
openclaw logs --follow
```

Common causes: model auth not loaded on the gateway host (check `models status`); channel pairing/allowlist blocking replies (check channel config + logs); WebChat/Dashboard open without the right token. If remote, confirm the tunnel/Tailscale connection is up and the Gateway WebSocket is reachable.

**"Disconnected from gateway: no reason."** This usually means the UI lost the WebSocket connection. Check: is the Gateway running (`openclaw gateway status`); is it healthy (`openclaw status`); does the UI have the right token (`openclaw dashboard`); if remote, is the tunnel/Tailscale link up — then tail logs with `openclaw logs --follow`.

**Telegram `setMyCommands` fails.** Start with `openclaw channels status` and `openclaw channels logs --channel telegram`, then match the error. `BOT_COMMANDS_TOO_MUCH` means the Telegram menu has too many entries — OpenClaw already trims to the Telegram limit and retries with fewer commands, but some entries still need dropping; reduce plugin/skill/custom commands or disable `channels.telegram.commands.native` if you do not need the menu. `TypeError: fetch failed`, `Network request for 'setMyCommands' failed!`, or similar network errors mean (on a VPS/proxy) you should confirm outbound HTTPS is allowed and DNS works for `api.telegram.org`. If the Gateway is remote, look at logs on the Gateway host.

**TUI shows no output.** Confirm the Gateway is reachable and the agent can run via `openclaw status`, `openclaw models status`, `openclaw logs --follow`. In the TUI use `/status` to see current state; if you expect replies in a chat channel, make sure delivery is enabled (`/deliver on`).

## Chat Commands, Aborting Tasks, and "It Will Not Stop"

**Stop internal system messages showing in chat.** Most internal or tool messages only appear when **verbose**, **trace**, or **reasoning** is enabled for that session. Fix in the chat where you see it:

```
/verbose off
/trace off
/reasoning off
```

If still noisy, check session settings in the Control UI and set verbose to **inherit**, and confirm you are not using a bot profile with `verboseDefault` set to `on` in config.

**Stop/cancel a running task.** Send one of the abort-trigger phrases as a standalone message (no slash) — these are abort triggers, not slash commands: `stop`, `stop action`, `stop current action`, `stop run`, `stop current run`, `stop agent`, `stop the agent`, `stop openclaw`, `openclaw stop`, `stop don't do anything`, `stop do not do anything`, `stop doing anything`, `please stop`, `stop please`, `abort`, `esc`, `wait`, `exit`, `interrupt`. For background processes (from the exec tool), you can ask the agent to run `process action:kill sessionId:XXX`. Most commands must be sent as a standalone message that starts with `/`, but a few shortcuts (like `/status`) also work inline for allowlisted senders.

**"Cross-context messaging denied" (send Discord from Telegram).** OpenClaw blocks cross-provider messaging by default — a tool call bound to Telegram won't send to Discord unless explicitly allowed. Enable it for the agent and restart the gateway after editing config:

```json5
{
  tools: {
    message: {
      crossContext: {
        allowAcrossProviders: true,
        marker: { enabled: true, prefix: "[from {channel}] " },
      },
    },
  },
}
```

**Bot seems to "ignore" rapid-fire messages.** Mid-run prompts are steered into the active run by default. Use `/queue` to choose active-run behavior — `steer` (guide the active run at the next model boundary), `followup` (queue messages and run them one at a time after the current run ends), `collect` (queue compatible messages and reply once after the current run ends), `interrupt` (abort the current run and start fresh). Default mode is `steer`; you can add options like `debounce:0.5s cap:25 drop:summarize` for queued modes.

## Miscellaneous

**Default model for Anthropic with an API key.** In OpenClaw, credentials and model selection are separate. Setting `ANTHROPIC_API_KEY` (or storing an Anthropic API key in auth profiles) enables authentication, but the actual default model is whatever you configure in `agents.defaults.model.primary` (for example, `anthropic/claude-sonnet-4-6` or `anthropic/claude-opus-4-6`). If you see `No credentials found for profile "anthropic:default"`, the Gateway couldn't find Anthropic credentials in the expected `auth-profiles.json` for the agent that's running.

**Source**: OpenClaw documentation — `help/faq` (Sessions and multiple chats / Logging and debugging / Chat commands, aborting tasks, "it will not stop" / Miscellaneous) (mirror `inbox/openclaw_docs/help/faq.md`)
**Last Updated**: 2026-06-22
**Status**: Active
