---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - operations
keywords:
  - hermes gateway setup
  - gateway commands
  - dm pairing
  - admin vs regular users
  - background sessions
  - circuit breaker
  - service management
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging
access_control_group: ["general"]
---

# Hermes Gateway — Day-2 Operations

## Overview

This is the **operations procedure** for running the Hermes Messaging Gateway: how you set it up, drive it from the CLI and inside chat, secure it, and keep it healthy across platforms. The gateway *model* — the single background process that fans 20+ platform adapters through a per-chat session store into the AIAgent plus a 60s cron tick — lives in the architecture note ([hermes_messaging_gateway_architecture](hermes_messaging_gateway_architecture.md)); this is its *operate-it* counterpart, covering the `hermes gateway setup` wizard, the `gateway` command family, the in-chat slash-command surface, the allowlist / DM-pairing / admin-tier security model, interrupting and steering a busy agent, isolated `/background` sessions, systemd/launchd service install, and multi-platform day-2 controls (`/platform`, the circuit breaker, restart auto-resume, mobile progress defaults). Session reset policies, the capability matrix, and the silence-token model belong to the architecture note.

## Quick Setup

The easiest way to configure messaging platforms is the interactive wizard `hermes gateway setup`: arrow-key platform selection, shows which are already configured, and offers to start or restart the gateway when done.

## Gateway Commands

The `hermes gateway` command family runs the process in the foreground, configures platforms (`setup`, above), installs it as a managed service, and controls/inspects the default service. On Linux, `--system` variants target the boot-time system service.

```bash
hermes gateway              # Run in foreground
hermes gateway setup        # Configure messaging platforms interactively
hermes gateway install      # Install as a user service (Linux) / launchd service (macOS)
sudo hermes gateway install --system   # Linux only: install a boot-time system service
hermes gateway start        # Start the default service
hermes gateway stop         # Stop the default service
hermes gateway status       # Check default service status
hermes gateway status --system         # Linux only: inspect the system service explicitly
```

## Chat Commands (Inside Messaging)

Once connected, slash commands run from inside any chat: conversation control (`/new` or `/reset`, `/retry`, `/undo`, `/compress`, `/rollback`); session naming/resume (`/title`, `/resume`, `/status`, `/usage`, `/insights`); model/behavior (`/model [provider:model]`, `/personality`, `/reasoning`, `/voice`); access introspection (`/whoami` — admin / user / unrestricted on this scope); execution control (`/stop`, `/approve`, `/deny` for a pending dangerous command); home-channel and MCP (`/sethome`, `/reload-mcp`); plus `/update`, `/help`, `/background <prompt>`, and `/<skill-name>` to invoke any installed skill.

## Security

**By default the gateway denies any user not in an allowlist or paired via DM** — the safe default for a bot with terminal access. Restrict access with per-platform allowlists (recommended), a single cross-platform `GATEWAY_ALLOWED_USERS`, or — not recommended here — `GATEWAY_ALLOW_ALL_USERS=true`.

```bash
# Restrict to specific users (recommended):
TELEGRAM_ALLOWED_USERS=123456789,987654321
DISCORD_ALLOWED_USERS=123456789012345678
SIGNAL_ALLOWED_USERS=+155****4567,+155****6543

# Or allow
GATEWAY_ALLOWED_USERS=123456789,987654321

# Or explicitly allow all users (NOT recommended for bots with terminal access):
GATEWAY_ALLOW_ALL_USERS=true
```

(Each platform has its own `*_ALLOWED_USERS` variable — `SMS_`, `EMAIL_`, `MATTERMOST_`, `MATRIX_`, `DINGTALK_`, `FEISHU_`, `WECOM_`, `TEAMS_`, etc. — in that platform's native user-ID format.)

### DM Pairing (Alternative to Allowlists)

Instead of configuring user IDs, an unknown user gets a one-time pairing code when they DM the bot; the operator approves them from the CLI. Pairing codes expire after 1 hour, are rate-limited, and use cryptographic randomness.

```bash
# The user sees: "Pairing code: XKGH5N7P"
# You approve them with:
hermes pairing approve telegram XKGH5N7P

# Other pairing commands:
hermes pairing list          # View pending + approved users
hermes pairing revoke telegram 123456789  # Remove access
```

### Admins vs Regular Users

Allowlists answer "can this person reach the bot?" The **admin / user split** answers "once in, what may they do?" Every allowed user falls into one of two tiers per scope (DM vs group/channel):

- **Admin** — full access; runs every registered slash command (built-in + plugin) and every gated capability.
- **Regular user** — chats normally but runs only the slash commands you enable; the always-allowed floor is `/help` and `/whoami`.

Tiers are per platform and per scope (DM admin does not imply group/channel admin). They gate slash commands via the live command registry — built-ins and plugin commands, no per-feature wiring — while plain chat is unaffected. **Backward compat:** if `allow_admin_from` is unset for a scope the split is disabled there and every allowed user has full access, so existing installs keep working; opt in for the distinction.

```yaml
gateway:
  platforms:
    discord:
      extra:
        allow_from: ["111", "222", "333"]
        allow_admin_from: ["111"]                    # admins → all slash commands
        user_allowed_commands: [status, model]       # what non-admins may run
        # Optional: separate group/channel scope
        group_allow_admin_from: ["111"]
        group_user_allowed_commands: [status]
```

Use `/whoami` from any platform to see the active scope, your tier, and which slash commands you may run.

## Interrupting the Agent

Send any message while the agent works to interrupt it: in-progress terminal commands are killed immediately (SIGTERM, then SIGKILL after 1s); tool calls are cancelled (only the currently-executing one runs, the rest skipped); multiple messages sent during interruption join into one prompt; and `/stop` interrupts without queuing a follow-up.

### Queue vs interrupt vs steer (busy-input mode)

By default, messaging a busy agent interrupts it. Two other modes exist: `queue` (follow-ups wait and run as the next turn after the current task finishes) and `steer` (follow-ups injected into the current run via `/steer`, arriving after the next tool call — no interrupt, no new turn; falls back to `queue` if the agent hasn't started).

```yaml
display:
  busy_input_mode: steer   # or queue, or interrupt (default)
  busy_ack_enabled: true   # set to false to suppress the ⚡/⏳/⏩ chat reply entirely
```

The first time you message a busy agent on any platform, Hermes appends a one-line reminder explaining the knob; it fires once per install (`onboarding.seen.busy_input_prompt` latches it — delete the key to see it again). `display.busy_ack_enabled: false` silences only the chat reply; your input still queues/steers/interrupts as normal.

## Tool Progress Notifications

Control how much tool activity is shown via `display.tool_progress` (`off | new | all | verbose`) in `~/.hermes/config.yaml`; `tool_progress_command: true` enables `/verbose` in messaging; `tool_progress_grouping` (`accumulate` default — edit one bubble in place — or `separate`, one message per tool) controls grouping where message editing is supported. A related `gateway.message_timestamps.enabled` toggle (off by default) prepends a human-readable timestamp onto each user message *in the model's context* for temporal reasoning, while keeping persisted transcripts clean. When on, the bot sends status messages as it works (`💻 ls -la...`, `🔍 web_search...`).

## Background Sessions

`/background <prompt>` runs a prompt in a **separate background session** so the agent works on it independently while your main chat stays responsive; Hermes confirms with a task ID (e.g. `bg_143022_a1b2c3`).

### How It Works

Each `/background` prompt spawns a **separate agent instance** running asynchronously:

- **Isolated session** — its own conversation history; no knowledge of your current chat, sees only the prompt you give.
- **Same configuration** — inherits the current setup's model, provider, toolsets, reasoning settings, and provider routing.
- **Non-blocking** — your main chat stays fully interactive.
- **Result delivery** — on finish the result returns to the **same chat or channel**, prefixed `✅ Background task complete`; failures show `❌ Background task failed` with the error.

### Background Process Notifications

When the background agent uses `terminal(background=true)` to start long-running processes, the gateway can push status updates. Control via `display.background_process_notifications` (`all | result | error | off`) in `~/.hermes/config.yaml`, or `HERMES_BACKGROUND_NOTIFICATIONS`: `all` = running-output updates plus final completion (default); `result` = final completion only; `error` = final message only on non-zero exit; `off` = none. Background tasks are fire-and-forget — results arrive in the same chat.

## Service Management

Install the gateway as a managed service so it survives logout/reboot. **Linux (systemd):** `hermes gateway install` (user service) or `sudo hermes gateway install --system` (boot-time system service that still runs as your user); `start`/`stop`/`status` manage it; `journalctl --user -u hermes-gateway -f` for logs. Use a user service on laptops/dev boxes, a system service on VPS/headless hosts. On a headless VM, a user service plus `sudo loginctl enable-linger $USER` gives start-at-boot with zero root — also letting the `hermes update` auto-restart proceed without a password.

**macOS (launchd):** `hermes gateway install` writes a plist at `~/Library/LaunchAgents/ai.hermes.gateway.plist` with three env vars — `PATH` (full shell PATH plus venv `bin/` and `node_modules/.bin`), `VIRTUAL_ENV`, and `HERMES_HOME`. Plists are static, so re-run `install` after adding tools (e.g. ffmpeg) to capture the new PATH; `tail -f ~/.hermes/logs/gateway.log` for logs. Each `HERMES_HOME` gets its own service label (`hermes-gateway` / `ai.hermes.gateway` for the default `~/.hermes`, hashed suffixes otherwise); don't keep both user and system units installed — Hermes warns when it detects both, since start/stop/status becomes ambiguous.

## Operating a multi-platform gateway

A gateway typically runs several adapters at once (Telegram + Discord + Slack). These day-2 operations span all platforms.

### `/platform` command

Use `/platform` from any connected CLI session or chat to inspect and steer individual adapters without restarting the whole gateway: `/platform list` shows each adapter and its state (`running`, manually `paused`, or `paused-by-breaker`), `/platform pause <name>` stops dispatching new messages to one, and `/platform resume <name>` re-enables it. Pausing keeps the adapter loaded and its loops alive — incoming messages are dropped, but the connection stays open so resume is instant.

### Automatic circuit breaker

Each adapter is wrapped in a circuit breaker. Repeated retryable failures (network blips, rate-limit replies, 5xx responses, websocket disconnects) trip it: the adapter is auto-paused, an operator notification goes to another live platform's home channel when one is configured, and a structured log line is emitted. The breaker does **not** auto-resume — it stays open until you run `/platform resume <name>` manually, so a sustained outage doesn't make the gateway thrash reconnects. When a platform is paused, check the gateway log (`~/.hermes/logs/gateway.log` or the unit log — search the platform name and `circuit breaker` / `paused`), `/platform list` state/last-reason, and the provider's status page; once upstream is healthy, `/platform resume <name>` clears the breaker.

### Restart notifications and session resume

On restart (or shutdown with in-flight sessions), the gateway can send a one-shot "agent is back" / "agent was interrupted" message to each platform's home channel, controlled per-platform by `gateway_restart_notification` under `gateway.platforms.<platform>` in `gateway-config.yaml` (default `true`; set `false` to opt a noisy platform out — sent once per restart regardless of session count). Sessions caught mid tool-call or generation are flagged `restart_interrupted`; on next startup the gateway schedules an auto-resume for each, the user gets a heads-up, and the session picks up from the last committed turn on reply. On by default, logged at start (`Scheduled auto-resume for N restart-interrupted session(s)`); no config required.

### Mobile-friendly progress defaults and cleanup

Because Telegram is usually a mobile inbox, its defaults suit that surface: `tool_progress` and `busy_ack_detail` both default `off`, while `interim_assistant_messages` and `long_running_notifications` stay on (one edit-in-place "⏳ Working — N min" heartbeat). Re-enable verbose progress per platform under `display.platforms.<platform>`. Separately, `display.platforms.<platform>.cleanup_progress: true` (default `false`) auto-deletes tool-progress, heartbeat, and status-callback bubbles after the final response lands — honored only by adapters implementing `delete_message` (currently Telegram and Discord); failed runs skip cleanup so the bubbles stay as breadcrumbs.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/index.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging
**Last Updated**: 2026-06-19
**Status**: Active
