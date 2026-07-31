---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - ntfy
keywords:
  - ntfy push notifications
  - http pub-sub
  - topic as identity
  - ntfy home channel cron
  - self-hosting ntfy
  - outgoing-only one-way
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/ntfy
access_control_group: ["general"]
---

# Hermes Messaging — ntfy

## Overview

ntfy is a simple HTTP-based pub-sub notification service, and this page is the runbook for wiring it up as a Hermes messaging channel. You subscribe to a topic from the ntfy mobile app, publish messages to that topic to talk to the agent, and the agent's reply comes back as a push notification on your phone. It works against the free public `ntfy.sh` server or any self-hosted instance, and against any client that can make HTTP requests (phones, browsers, scripts, watches).

Unlike most other Hermes platforms, ntfy needs **no SDK, no daemon, and no Node.js** — the adapter uses `httpx`, which is already a Hermes dependency. The setup arc is: pick a topic, subscribe on the phone, set three `.env` variables, restart the gateway. The one concept that needs care before deploying is the **identity model**: ntfy has no authenticated user identity, so the topic name itself acts as both the channel and the trust boundary. This note is the user-facing setup layer; the gateway runner, allowlist, stream consumer, and standalone sender it drives are documented in the linked snippet/code-repo notes.

## Prerequisites

- A topic name (any unique string — `hermes-myname-2026` works fine).
- The ntfy mobile app installed and subscribed to that topic.
- Optional: a self-hosted ntfy server, or an `ntfy.sh` account token for private/reserved topics.

No SDK, no daemon, no Node.js — the adapter rides on the already-bundled `httpx`.

## Configure Hermes

### Via setup wizard

```bash
hermes gateway setup
```

Select **ntfy** and follow the prompts.

### Via environment variables

Add these to `~/.hermes/.env`:

```
NTFY_TOPIC=hermes-myname-2026
NTFY_ALLOWED_USERS=hermes-myname-2026
NTFY_HOME_CHANNEL=hermes-myname-2026
```

The full variable reference (verbatim from the source table):

| Variable | Required | Description |
|---|---|---|
| `NTFY_TOPIC` | Yes | Topic to subscribe to (incoming messages) |
| `NTFY_SERVER_URL` | Optional | Server URL (default: `https://ntfy.sh`) — point to a self-hosted ntfy for privacy |
| `NTFY_TOKEN` | Optional | Bearer token (e.g. `tk_xyz`) or `user:pass` for Basic auth |
| `NTFY_PUBLISH_TOPIC` | Optional | Different topic for outgoing replies (defaults to `NTFY_TOPIC`) |
| `NTFY_MARKDOWN` | Optional | Set `true` to send replies with `X-Markdown: true` header |
| `NTFY_ALLOWED_USERS` | Recommended | Comma-separated topic names allowed (treated as user IDs; see below) |
| `NTFY_ALLOW_ALL_USERS` | Optional | Set `true` to allow every publisher — only safe for private topics with read tokens |
| `NTFY_HOME_CHANNEL` | Optional | Default topic for cron / notification delivery |
| `NTFY_HOME_CHANNEL_NAME` | Optional | Human label for the home channel |

## Identity Model — Read This Before Deploying

ntfy has no native authenticated user identity. The `title` field on a published message is **publisher-controlled** and can be anything the sender wants. The Hermes adapter does **NOT** use `title` for authorization — doing so would let any publisher who knows the topic spoof an allowed user.

Instead, **the topic name itself is the identity**. Every message published to the topic is treated as coming from the same logical user (the topic). `NTFY_ALLOWED_USERS` is therefore typically just the topic name itself — a single-entry allowlist that gates the whole channel.

This means **anyone who knows the topic can talk to the agent**. To make that a real trust boundary:

- **Self-host ntfy** and lock the topic down with Access Control — only clients holding the read/write token can publish.
- Or **use a private topic on ntfy.sh** (reserved topics require an account) and protect it with an `NTFY_TOKEN`.
- Or **pick a long, unguessable topic name** (`hermes-7d4f9c8b-2026`) and treat it as the shared secret. This is the lightest setup but the topic name leaks via any logs or screenshots.

In all cases, do not put sensitive data through ntfy unless the underlying topic is access-controlled.

## Quick Start — Talk to Your Agent From Your Phone

1. Pick a topic name: `hermes-myname-2026`.
2. On your phone: install the ntfy app, tap **+**, enter `hermes-myname-2026`.
3. On the host:
   ```bash
   echo 'NTFY_TOPIC=hermes-myname-2026' >> ~/.hermes/.env
   echo 'NTFY_ALLOWED_USERS=hermes-myname-2026' >> ~/.hermes/.env
   hermes gateway restart
   ```
4. From the ntfy app, send a message to the topic. The agent's reply lands as a push notification.

## Using ntfy With Cron Jobs

Once `NTFY_HOME_CHANNEL` is set, cron jobs can deliver to ntfy:

```python
cronjob(
    action="create",
    schedule="every 1h",
    deliver="ntfy",          # uses NTFY_HOME_CHANNEL
    prompt="Check for alerts and summarise."
)
```

Or target a specific topic explicitly with `send_message(target="ntfy:alerts-channel", message="Done!")`. This works even when the cron runs **out-of-process** from the gateway — the plugin registers a `standalone_sender_fn` that opens its own HTTP connection.

## Self-Hosting ntfy

For full control (topic access control, message persistence policies, attachments, emoji tags), self-host the server:

```bash
# Docker
docker run -p 80:80 -it binwiederhier/ntfy serve

# Native
go install heckel.io/ntfy/v2@latest
ntfy serve
```

Then point Hermes at it by setting `NTFY_SERVER_URL=https://ntfy.mydomain.com`, `NTFY_TOPIC=hermes`, and (if access control is enabled) `NTFY_TOKEN=tk_abc123`.

## Markdown Formatting

ntfy clients render markdown when the publisher sets the `X-Markdown: true` header. Enable it for outgoing Hermes replies with `NTFY_MARKDOWN=true`, or in `config.yaml`:

```yaml
platforms:
  ntfy:
    extra:
      markdown: true
```

The mobile app supports a subset of CommonMark — bold, italic, lists, links, fenced code blocks.

## Outgoing-Only Setup (Notifications Without Inbound)

If you only want Hermes to *push* notifications to ntfy (cron summaries, alerts) and never accept messages back, set both `NTFY_TOPIC` and `NTFY_PUBLISH_TOPIC` to the same value and skip `NTFY_ALLOWED_USERS` entirely. With no allowlist, the agent never responds to inbound messages — your phone gets the pushes, but the conversation is one-way.

## Limits

- **Message size**: ntfy caps message bodies at 4096 chars. Hermes truncates with a warning when this is exceeded.
- **No typing indicators**: the protocol doesn't expose one; `send_typing` is a no-op.
- **No threads or attachments**: ntfy is plain push notifications. Long replies stay in the message body, no thread fanout.
- **No native user identity**: see the Identity Model section above.

## Troubleshooting

- **Auth failure / 401** — `NTFY_TOKEN` is wrong, or the token lacks publish/subscribe rights on this topic. The adapter halts its reconnect loop on 401 and the gateway runtime status shows `fatal: ntfy_unauthorized`. Fix the token and restart the gateway.
- **Topic not found / 404** — `NTFY_TOPIC` doesn't exist on the configured server. On ntfy.sh, topics are auto-created on first publish, so a 404 means you're pointed at a self-hosted server that doesn't have the topic provisioned. The adapter halts its reconnect loop with `fatal: ntfy_topic_not_found`.
- **Connected but no messages** — Check that `NTFY_ALLOWED_USERS` includes the topic name itself. With ntfy's identity model, the topic IS the user; leaving the allowlist empty rejects everything.
- **Reconnects every 60s** — The stream keepalive default is 55s; ntfy may have intermittent network issues. The adapter applies exponential backoff (2 → 5 → 10 → 30 → 60s) and resets to 0 once a stream stays alive ≥60s.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/ntfy.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/ntfy
**Last Updated**: 2026-06-19
**Status**: Active
