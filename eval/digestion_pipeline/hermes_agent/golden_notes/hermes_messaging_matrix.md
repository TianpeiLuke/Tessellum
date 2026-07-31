---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - matrix
keywords:
  - matrix bot setup
  - mautrix homeserver
  - matrix access token
  - allowed users rooms allowlist
  - matrix session scope auto-threading
  - matrix tools reactions approvals
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/matrix
access_control_group: ["general"]
---

# Hermes Agent — Matrix Setup

## Overview

This page is the base **Matrix bot-setup procedure** for the Hermes messaging gateway: it connects Hermes as a bot to any Matrix homeserver (Synapse, Conduit, Dendrite, or matrix.org) so the agent can chat over the open, federated Matrix protocol. The bot connects through the `mautrix` Python SDK, runs each message through the full Hermes pipeline (tool use, memory, reasoning), and responds in real time — supporting text, files, images, audio, video, and optional end-to-end encryption (E2EE). Setup is a linear arc: create a bot account, obtain an access token (or password login), find your User ID, configure `~/.hermes/.env` / `config.yaml`, harden the allowlists, then start the gateway. This note owns base setup plus the session/mention/threading model, the six Matrix-scoped tools, media limits, and troubleshooting. The self-contained E2EE subsystem is split into [hermes_messaging_matrix_e2ee](hermes_messaging_matrix_e2ee.md), and the macOS `libolm` proxy-mode deployment model into [hermes_messaging_matrix_proxy_mode](hermes_messaging_matrix_proxy_mode.md).

## How Hermes Behaves

Behavior is context-dependent — the part most people want before setup:

- **DMs**: Hermes responds to every message; no `@mention` needed. Each DM has its own session. `MATRIX_DM_MENTION_THREADS=true` starts a thread when the bot is `@mentioned` in a DM.
- **Rooms**: By default an `@mention` is required. Set `MATRIX_REQUIRE_MENTION=false`, or add room IDs to `MATRIX_FREE_RESPONSE_ROOMS`, for free-response rooms. Room invites are auto-accepted.
- **Threads (MSC3440)**: Thread context is isolated from the main room timeline. Threads the bot already joined do not require a mention.
- **Auto-threading**: Hermes auto-creates a thread for each room response (`MATRIX_AUTO_THREAD=false` disables). `MATRIX_DM_AUTO_THREAD=true` (default false) also auto-threads DMs — distinct from `MATRIX_DM_MENTION_THREADS`.
- **Commands**: Normal `/commands` work; if your client reserves `/`, use `!commands` — Hermes normalizes known `!command` aliases to `/command`.
- **Interactive controls**: Dangerous-command approval and `/model` selection can use Matrix reactions, optionally limited to the requesting user.
- **Shared rooms**: Session history is isolated per user inside a room by default — two people in one room do not share a transcript unless explicitly disabled. The bot automatically joins rooms when invited.

## Capability Matrix

The Matrix adapter declares `yes` for text, threads, reactions, approvals, model picker, thinking panes, images, multiple images, files, voice/audio, video, and diagnostics. **E2EE** is mode-based (`off` / `optional` / `required`) — see [hermes_messaging_matrix_e2ee](hermes_messaging_matrix_e2ee.md).

### Session Model

By default each DM gets its own session, each thread its own session namespace, and each user in a shared room their own session inside it. Controlled by `config.yaml`:

```yaml
group_sessions_per_user: true
```

Set it to `false` only for one shared conversation per room. Shared sessions mean users share context growth and token costs, one person's tool-heavy task can bloat everyone else's context, and one in-flight run can interrupt another's follow-up.

### Mention and Threading Configuration

Configure mention and auto-threading via `config.yaml` (or the matching `MATRIX_*` environment variables):

```yaml
matrix:
  require_mention: true           # Require @mention in rooms (default: true)
  allowed_users:                  # Matrix users allowed to trigger agent turns
    - "@alice:matrix.org"
  allowed_rooms:                  # Matrix rooms allowed to trigger agent turns
    - "!abc123:matrix.org"
  free_response_rooms:            # Rooms exempt from mention requirement
    - "!abc123:matrix.org"
  ignore_user_patterns:           # Bridge/appservice ghost users to ignore
    - "^@telegram_"
    - "^@whatsapp_"
  process_notices: false          # Ignore m.notice by default
  session_scope: room             # auto|room|thread; room is recommended for project rooms
  auto_thread: true               # Auto-create threads for responses (default: true)
  dm_mention_threads: false       # Create thread when @mentioned in DM (default: false)
```

`MATRIX_REACTIONS=false` turns off the processing-lifecycle emoji reactions (👀/✅/❌). Room-wide `@room` notifications are disabled by default; set `MATRIX_ALLOW_ROOM_MENTIONS=true` only where the bot may notify everyone. If upgrading from a version without `MATRIX_REQUIRE_MENTION` (which responded to all room messages), set it to `false` to preserve that behavior.

### Project Room Isolation

For one bot across multiple project rooms, use stable room-scoped sessions (`MATRIX_SESSION_SCOPE=room`, `MATRIX_AUTO_THREAD=false`). `MATRIX_SESSION_SCOPE` accepts: `auto` (backward-compatible default; `MATRIX_AUTO_THREAD` controls synthetic threads), `room` (unthreaded room messages stay in one stable session; real threads use their root), and `thread` (unthreaded room messages synthesize a session from the triggering event ID). Hermes includes the current room name, ID, topic, message ID, and a room-boundary note in the prompt; `/status` shows the room/session scope, and `/resume` will not silently resume a named session from another room unless you use `/resume --cross-room <session name>`. `MATRIX_SESSION_SCOPE=room` controls the room/thread lane; `group_sessions_per_user` controls whether users inside that room share the lane.

## Step 1: Create a Bot Account

You need a Matrix user account for the bot. Options: **(A) Register on your homeserver** (recommended) — use the admin API or registration tool, e.g. `register_new_matrix_user -c /etc/synapse/homeserver.yaml http://localhost:8008`, with a username like `hermes` (full ID `@hermes:your-server.org`); **(B) a public homeserver** — create an account in [Element Web](https://app.element.io); or **(C) your own account** — Hermes posts as you (useful for personal assistants).

## Step 2: Get an Access Token

Hermes authenticates two ways. **Option A — Access Token (recommended):** in Element go to **Settings → Help & About → Advanced** to read the token, or call the login API:

```bash
curl -X POST https://your-server/_matrix/client/v3/login \
  -H "Content-Type: application/json" \
  -d '{
    "type": "m.login.password",
    "user": "@hermes:your-server.org",
    "password": "your-password"
  }'
```

The response includes an `access_token` field. The token gives full access to the bot's account — never share or commit it; revoke a compromised token by logging out all sessions. **Option B — Password Login:** give Hermes the bot's user ID and password (`MATRIX_USER_ID` / `MATRIX_PASSWORD`) and it logs in on startup; simpler, but the password is stored in `.env`.

## Step 3: Find Your Matrix User ID

Hermes uses your Matrix User ID (format `@username:server`) to control who can interact with the bot. In Element, click your avatar → **Settings**; the User ID is shown at the top of the profile (e.g., `@alice:matrix.org`) — always starting with `@` and containing a `:` before the server name.

## Step 4: Configure Hermes Agent

**Option A — Interactive setup (recommended):** run `hermes gateway setup`, select **Matrix**, and provide the homeserver URL, access token (or user ID + password), and allowed user IDs. **Option B — Manual configuration** in `~/.hermes/.env` (access-token form shown; user ID auto-detected from the token if omitted):

```bash
# Required
MATRIX_HOMESERVER=https://matrix.example.org
MATRIX_ACCESS_TOKEN=***

# Security: restrict who can interact with the bot
MATRIX_ALLOWED_USERS=@alice:matrix.example.org
# Optional: restrict which rooms can trigger the bot
MATRIX_ALLOWED_ROOMS=!abc123:matrix.example.org
```

For password login, replace the token with `MATRIX_USER_ID` + `MATRIX_PASSWORD`. Multiple allowed users are comma-separated.

## Private Deployment Hardening

For private deployments, set **both** allowlists. If `MATRIX_ALLOWED_USERS` is unset, any sender who can reach the bot in a joined room can trigger a turn; if `MATRIX_ALLOWED_ROOMS` is unset, any joined room can. A locked-down deployment sets both (`MATRIX_ALLOWED_USERS=@alice:...,@bob:...` and `MATRIX_ALLOWED_ROOMS=!ops:...,!dmroom:...`). Bridge/appservice deployments need extra loop protection: Hermes always ignores its own events, appservice-style users whose localpart starts with `_`, duplicate event IDs, old startup events, edit replacements, and `m.notice` events by default. Add deployment-specific ghost patterns (`MATRIX_IGNORE_USER_PATTERNS='^@telegram_,^@slack_,^@whatsapp_'`), and set `MATRIX_PROCESS_NOTICES=true` only when a trusted workflow really sends `m.notice`. Diagnostics redact access tokens, recovery keys, device IDs, and message bodies. Treat federated rooms and untrusted homeservers as untrusted input: keep room allowlists tight, prefer DMs/private rooms for tool-heavy work, and avoid authorizing bridge ghosts or appservice puppets.

### Start the Gateway

Once configured, start the gateway with `hermes gateway`. The bot connects and starts syncing within a few seconds — send it a DM or message it in a joined room to test. It can run in the background or as a systemd service for persistent operation.

## Home Room

Designate a "home room" where the bot sends proactive messages (cron output, reminders, notifications). Type `/sethome` (or `!sethome` if your client intercepts slash commands) in any room the bot is in, or set it manually:

```bash
MATRIX_HOME_ROOM=!abc123def456:matrix.example.org
```

## Room allowlist (`allowed_rooms`)

Restrict the bot to a fixed set of rooms. When set, the bot **only** responds in listed rooms — messages elsewhere are silently ignored, even if the bot is mentioned. **DMs are exempt**, so authorized users can always reach the bot one-on-one. Empty/unset means no restriction; the room-ID check runs **before** any other gating (mention requirement, sender allowlist). Use the room's internal ID (`!abc...:server`), not its alias (`#room:server`) — find it in Element via Room → **Settings → Advanced**. See also the [admin/user slash command split](../../code_snippets/snippet_hermes_agent_gw_slash_access.md).

## Commands in Matrix

Hermes supports the same gateway commands in Matrix as elsewhere, including `/commands`, `/model`, `/stop`, `/queue`, `/steer`, `/goal`, `/subgoal`, `/background`, `/bg`, `/btw`, `/tasks`, and `/yolo`. Some clients reserve leading `/` and don't forward unknown slash commands; use `!` as a Matrix-safe alias (`!commands`, `!model gpt-5.5 --provider openrouter`, `!queue ...`, `!stop`). Hermes only normalizes `!command` when it is known to the gateway, a registered plugin command, or an installed skill command — ordinary exclamations like `!important` stay normal chat messages.

## Matrix Tools and Controls

In Matrix conversations Hermes exposes six Matrix-scoped tools: `matrix_send_reaction`, `matrix_redact_message`, `matrix_create_room`, `matrix_invite_user`, `matrix_fetch_history`, `matrix_set_presence`. These are not available in non-Matrix toolsets, and admin-style tools are disabled by default: redaction requires `MATRIX_TOOLS_ALLOW_REDACTION=true`, invites `MATRIX_TOOLS_ALLOW_INVITES=true`, room creation `MATRIX_TOOLS_ALLOW_ROOM_CREATE=true`, and public rooms additionally `MATRIX_ALLOW_PUBLIC_ROOMS=true`. Tools are limited to the current room by default; cross-room targets require `MATRIX_TOOLS_ALLOW_CROSS_ROOM=true`, and destructive cross-room actions additionally `MATRIX_TOOLS_ALLOW_CROSS_ROOM_DESTRUCTIVE=true`. If `MATRIX_ALLOWED_ROOMS` is set, tools may only target those rooms. Reaction controls: ✅ approve once, ♾️ approve always, ❌ deny, number reactions for `/model` choices. Set `MATRIX_APPROVAL_REQUIRE_SENDER=false` to let any authorized user operate an approval/model-picker prompt (default is requester-bound).

## Media Limits

Hermes uploads and downloads Matrix images, files, audio, and video via the Matrix media APIs; multiple generated images are sent as one ordered batch with captions and thread context preserved. By default media over 100 MB is rejected before upload/download — override with `MATRIX_MAX_MEDIA_BYTES=104857600`. Inbound media must use Matrix `mxc://` content URIs; Hermes rejects arbitrary HTTP(S) media URLs to avoid turning a federated room into an unrestricted downloader. Native voice messages (MSC3245) route to speech-to-text inbound and render as native voice bubbles outbound.

## Troubleshooting

- **Bot not responding:** It hasn't joined the room, your ID isn't in `MATRIX_ALLOWED_USERS`, the room isn't in `MATRIX_ALLOWED_ROOMS`, or a room message didn't mention the bot. Invite the bot (auto-joins), verify the full `@user:server` ID and room ID are allowlisted, mention the bot or add the room to `MATRIX_FREE_RESPONSE_ROOMS`, and restart.
- **Joins but silently drops every message (clock skew):** The host clock is ahead, so the adapter's 5-second startup-grace filter (`event_ts < startup_ts - 5`) treats every live event as "too old" (log: `Matrix: dropped N live events as 'too old' more than 30s after startup`). Fix: sync the clock with NTP (`sudo timedatectl set-ntp true`, or macOS `sudo sntp -sS time.apple.com`) and restart.
- **"Failed to authenticate" / "whoami failed":** Bad token or homeserver URL. Verify `MATRIX_HOMESERVER` (include `https://`, no trailing slash) and test via `curl -H "Authorization: Bearer YOUR_TOKEN" https://your-server/_matrix/client/v3/account/whoami`.
- **"mautrix not installed":** `pip install 'mautrix[encryption]'` (or `'hermes-agent[matrix]'`).
- **Bot connects/sends but ignores inbound:** Matrix handlers only fire when sync payloads run through mautrix's `handle_sync()`. A raw `client.sync()` poll leaves the adapter connected (send works) while inbound never reaches `_on_room_message`. Hermes uses an explicit sync loop calling `client.handle_sync()` on the initial and every incremental sync; verify handlers are registered before the first sync, and check logs for `sync event dispatch error`. The loop auto-retries every 5s on error.
- **Bridge messages loop or echo:** A bridge/appservice puppet relays bot output back as a new message. Keep bridge ghosts out of `MATRIX_ALLOWED_USERS`, add a matching `MATRIX_IGNORE_USER_PATTERNS` entry, and leave `MATRIX_PROCESS_NOTICES=false`.

Encryption-specific errors ("could not decrypt event") are covered in [hermes_messaging_matrix_e2ee](hermes_messaging_matrix_e2ee.md).

## Security

Always set `MATRIX_ALLOWED_USERS` and, for shared/private deployments, `MATRIX_ALLOWED_ROOMS`. Without them, anyone who can message the bot in a joined room may trigger the agent. Only authorize people and rooms you trust — authorized users have full access to the agent's capabilities, including tool use and system access.

## Notes

- **Any homeserver:** Works with Synapse, Conduit, Dendrite, matrix.org, or any spec-compliant homeserver.
- **Federation:** On a federated homeserver the bot can talk to users from other servers — add their full `@user:server` IDs to `MATRIX_ALLOWED_USERS`.
- **Auto-join:** The bot accepts room invites and joins automatically, responding immediately after.
- **Media support:** Sends/receives images, audio, video, and files via the Matrix content repository API.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/matrix.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/matrix
**Last Updated**: 2026-06-19
**Status**: Active
