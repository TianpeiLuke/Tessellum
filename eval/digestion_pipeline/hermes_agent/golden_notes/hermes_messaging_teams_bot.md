---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - microsoft_teams
keywords:
  - hermes teams bot
  - microsoft teams webhook
  - teams.cli registration
  - bot framework jwt
  - adaptive card approvals
  - teams allowed users
topics:
  - Hermes Agent
  - Messaging Gateway
  - Microsoft Teams
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/teams
access_control_group: ["general"]
---

# Hermes Agent — Microsoft Teams Bot Setup

## Overview

This is the procedure for connecting Hermes Agent to Microsoft Teams **as a bot**. Unlike Slack's Socket Mode, Teams does not open an outbound connection — it delivers messages by **calling a public HTTPS webhook**, so the Hermes instance needs a publicly reachable endpoint: either a dev tunnel (for local development) or a real domain (for production). The webhook listens on port `3978` by default (overridable with `TEAMS_PORT`) at the path `/api/messages`, and every inbound request is authenticated by the Teams Bot Framework — requests without valid JWTs are rejected.

The setup is six steps: install `@microsoft/teams.cli` (which automates bot registration without the Azure portal), expose the webhook port over a tunnel, create the bot to obtain `CLIENT_ID`/`CLIENT_SECRET`/`TENANT_ID`, write those Azure-AD credentials into `~/.hermes/.env`, start the gateway, and install the app in Teams. Access is gated by `TEAMS_ALLOWED_USERS` (a comma-separated list of AAD object IDs). Two notable features layer on top: **Interactive Approval Cards** (Adaptive Cards with Allow Once / Allow Session / Always Allow / Deny buttons that replace typing `/approve`) and **Meeting Summary Delivery** (the same Teams adapter also delivers meeting summaries when the Teams meeting pipeline plugin is enabled — one integration surface, not two). The meeting-summary pipeline runtime itself is documented in the companion note [hermes_messaging_teams_meetings_pipeline](hermes_messaging_teams_meetings_pipeline.md); the Graph app registration it depends on is owned elsewhere.

## How the Bot Responds

The bot's response trigger depends on conversation context:

| Context | Behavior |
|---------|----------|
| **Personal chat (DM)** | Bot responds to every message. No @mention needed. |
| **Group chat** | Bot only responds when @mentioned. |
| **Channel** | Bot only responds when @mentioned. |

Teams delivers @mentions as regular messages carrying `<at>BotName</at>` tags, which Hermes strips automatically before processing.

For source or local installs, include the Teams extra so the bundled adapter can import the Microsoft Teams SDK: `uv sync --extra teams` (or, for editable installs, `uv pip install -e ".[teams]"`).

> Run `hermes gateway setup` and pick **Microsoft Teams** for a guided walk-through.

## Step 1: Install the Teams CLI

The `@microsoft/teams.cli` automates bot registration — no Azure portal needed. Install and authenticate it with `npm install -g @microsoft/teams.cli@preview` followed by `teams login`. To verify the login and find your own AAD object ID (needed for `TEAMS_ALLOWED_USERS`), run `teams status --verbose`.

## Step 2: Expose the Webhook Port

Teams cannot deliver messages to `localhost`. For local development, use any tunnel tool to get a public HTTPS URL. The default port is `3978` — change it with `TEAMS_PORT` if needed.

```bash
# devtunnel (Microsoft)
devtunnel create hermes-bot --allow-anonymous
devtunnel port create hermes-bot -p 3978 --protocol https  # replace 3978 with TEAMS_PORT if changed
devtunnel host hermes-bot

# ngrok
ngrok http 3978  # replace 3978 with TEAMS_PORT if changed

# cloudflared
cloudflared tunnel --url http://localhost:3978  # replace 3978 with TEAMS_PORT if changed
```

Copy the `https://` URL from the output — it is used in the next step. Leave the tunnel running while developing. For production, point the bot's endpoint at the server's public domain instead (see Production Deployment).

## Step 3: Create the Bot

```bash
teams app create \
  --name "Hermes" \
  --endpoint "https://<your-tunnel-url>/api/messages"
```

The CLI outputs the `CLIENT_ID`, `CLIENT_SECRET`, and `TENANT_ID`, plus an install link for Step 6. The client secret won't be shown again, so it must be saved at this point.

## Step 4: Configure Environment Variables

Add to `~/.hermes/.env`:

```bash
# Required
TEAMS_CLIENT_ID=<your-client-id>
TEAMS_CLIENT_SECRET=<your-client-secret>
TEAMS_TENANT_ID=<your-tenant-id>

# Restrict access to specific users (recommended)
# Use AAD object IDs from `teams status --verbose`
TEAMS_ALLOWED_USERS=<your-aad-object-id>
```

## Step 5: Start the Gateway

```bash
HERMES_UID=$(id -u) HERMES_GID=$(id -g) docker compose up -d gateway
```

This starts the gateway. The default webhook port is `3978` (override with `TEAMS_PORT`). Verify it is running with `curl http://localhost:3978/health` (should return `ok`) and tail logs with `docker logs -f hermes`, looking for `[teams] Webhook server listening on 0.0.0.0:3978/api/messages`.

## Step 6: Install the App in Teams

Run `teams app get <teamsAppId> --install-link`, open the printed link in a browser (it opens directly in the Teams client), and after installing, send a direct message to the bot — it's ready.

## Configuration Reference

The adapter can be configured either via environment variables or `~/.hermes/config.yaml`.

| Variable | Description |
|----------|-------------|
| `TEAMS_CLIENT_ID` | Azure AD App (client) ID |
| `TEAMS_CLIENT_SECRET` | Azure AD client secret |
| `TEAMS_TENANT_ID` | Azure AD tenant ID |
| `TEAMS_ALLOWED_USERS` | Comma-separated AAD object IDs allowed to use the bot |
| `TEAMS_ALLOW_ALL_USERS` | Set `true` to skip the allowlist and allow anyone |
| `TEAMS_HOME_CHANNEL` | Conversation ID for cron/proactive message delivery |
| `TEAMS_HOME_CHANNEL_NAME` | Display name for the home channel |
| `TEAMS_PORT` | Webhook port (default: `3978`) |

Alternatively, configure via `~/.hermes/config.yaml`:

```yaml
platforms:
  teams:
    enabled: true
    extra:
      client_id: "your-client-id"
      client_secret: "your-secret"
      tenant_id: "your-tenant-id"
      port: 3978
```

## Features

### Interactive Approval Cards

When the agent needs to run a potentially dangerous command, it sends an Adaptive Card with four buttons instead of asking the user to type `/approve`:

- **Allow Once** — approve this specific command
- **Allow Session** — approve this pattern for the rest of the session
- **Always Allow** — permanently approve this pattern
- **Deny** — reject the command

Clicking a button resolves the approval inline and replaces the card with the decision.

### Meeting Summary Delivery (Teams Meeting Pipeline)

When the Teams meeting pipeline plugin is enabled, this same adapter also handles **outbound delivery of meeting summaries** — one Teams integration surface, not two. After a meeting's transcript is summarized, the writer posts the summary into the chosen Teams target. Pipeline summary delivery is configured under the `teams` platform entry alongside the bot config (the pipeline runtime itself is the companion note's subject):

```yaml
platforms:
  teams:
    enabled: true
    extra:
      # existing bot config (client_id, client_secret, tenant_id, port) ...

      # Meeting summary delivery (only used when the teams_pipeline plugin is enabled)
      delivery_mode: "graph"       # or "incoming_webhook"
      # For delivery_mode: graph — pick ONE of:
      chat_id: "19:meeting_..."    # post into a Teams chat
      # team_id: "..."             # OR post into a channel
      # channel_id: "..."
      # access_token: "..."        # optional; falls back to MSGRAPH_* app credentials
      # For delivery_mode: incoming_webhook:
      # incoming_webhook_url: "https://outlook.office.com/webhook/..."
```

| Mode | Use when | Trade-off |
|------|----------|-----------|
| `incoming_webhook` | Simple "post a summary into this channel" with a static Teams-generated URL. | No reply threading, no reactions, shows as the webhook's configured identity. |
| `graph` | Threaded channel posts or 1:1/group chat posts under the bot's identity via Microsoft Graph. | Requires the Graph app registration with `ChannelMessage.Send` (channel) or `Chat.ReadWrite.All` (chat) application permissions. |

If the `teams_pipeline` plugin is **not** enabled, these settings are inert — they only wire up when the pipeline runtime binds to the Graph webhook ingress.

## Production Deployment

For a permanent server, skip devtunnel and register the bot with the server's public HTTPS endpoint by running `teams app create --name "Hermes" --endpoint "https://your-domain.com/api/messages"`. To update the endpoint of an already-created bot, use `teams app update --id <teamsAppId> --endpoint "https://your-domain.com/api/messages"`. The configured port (`TEAMS_PORT`, default `3978`) must be reachable from the internet, and the TLS certificate must be valid — Teams rejects self-signed certificates.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `health` endpoint works but bot doesn't respond | Check that the tunnel is still running and the bot's messaging endpoint matches the tunnel URL |
| `KeyError: 'teams'` in logs | Restart the container — this is fixed in the current version |
| Bot responds with auth errors | Verify `TEAMS_CLIENT_ID`, `TEAMS_CLIENT_SECRET`, and `TEAMS_TENANT_ID` are all set correctly |
| `No inference provider configured` | Check that `ANTHROPIC_API_KEY` (or another provider key) is set in `~/.hermes/.env` |
| Bot receives messages but ignores them | The AAD object ID may not be in `TEAMS_ALLOWED_USERS`. Run `teams status --verbose` to find it |
| Tunnel URL changes on restart | devtunnel URLs are persistent with a named tunnel (`devtunnel create hermes-bot`). ngrok and cloudflared generate a new URL each run unless on a paid plan — update the bot endpoint with `teams app update` when it changes |
| Teams shows "This bot is not responding" | The webhook returned an error. Check `docker logs hermes` for tracebacks |
| `[teams] Failed to connect` in logs | The SDK failed to authenticate. Double-check credentials and that the tenant ID matches the account used in `teams login` |

## Security

The Security section's central directive is to **always set `TEAMS_ALLOWED_USERS`** with the AAD object IDs of authorized users — without it, anyone who can find or install the bot can interact with it. `TEAMS_CLIENT_SECRET` must be treated like a password and rotated periodically via the Azure portal or Teams CLI.

- Store credentials in `~/.hermes/.env` with permissions `600` (`chmod 600 ~/.hermes/.env`)
- The bot only accepts messages from users in `TEAMS_ALLOWED_USERS`; unauthorized messages are silently dropped
- The public endpoint (`/api/messages`) is authenticated by the Teams Bot Framework — requests without valid JWTs are rejected

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/teams.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/teams
**Last Updated**: 2026-06-19
**Status**: Active
