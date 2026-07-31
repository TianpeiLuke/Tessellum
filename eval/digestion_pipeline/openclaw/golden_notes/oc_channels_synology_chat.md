---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - synology_chat
keywords:
  - openclaw synology chat
  - synology chat webhook channel
  - synology-chat incoming outgoing webhook
  - synology chat dmpolicy allowlist
  - synology chat token verification
  - openclaw channels add synology-chat
  - synology chat multi-account webhookpath
  - synology chat outbound user_id target
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/synology-chat
access_control_group: ["general"]
---

# OpenClaw — Synology Chat Channel Setup

## Overview

This note is the procedure for configuring the OpenClaw **Synology Chat** channel, mirroring the `channels/synology-chat` source page. Synology Chat is a bundled-plugin direct-message channel that uses Synology Chat webhooks: the plugin accepts inbound messages from a Synology Chat **outgoing webhook** and sends replies through a Synology Chat **incoming webhook**. The note covers the bundled plugin (and manual install), the quick-setup flow, environment variables, DM policy and access control, outbound delivery, multi-account configuration, the security notes, and troubleshooting — every H2 the sub-plan's coverage map assigns to this note.

## Bundled plugin

Synology Chat ships as a **bundled plugin** in current OpenClaw releases, so normal packaged builds do not need a separate install. On an older build or a custom install that excludes Synology Chat, install it manually from a local checkout:

```bash
openclaw plugins install ./path/to/local/synology-chat-plugin
```

The source page links the Plugins doc (`/tools/plugin`) for plugin-install details.

## Quick setup

The setup flow is: (1) ensure the Synology Chat plugin is available — current packaged releases already bundle it, older/custom installs add it manually from a source checkout with the command above, `openclaw onboard` now shows Synology Chat in the same channel-setup list as `openclaw channels add`, and non-interactive setup uses `openclaw channels add --channel synology-chat --token <token> --url <incoming-webhook-url>`. (2) In Synology Chat integrations, create an **incoming webhook** and copy its URL, and create an **outgoing webhook** with your secret token. (3) Point the outgoing webhook URL to your OpenClaw gateway: `https://gateway-host/webhook/synology` by default, or your custom `channels.synology-chat.webhookPath`. (4) Finish setup in OpenClaw — guided via `openclaw onboard`, or direct via `openclaw channels add --channel synology-chat --token <token> --url <incoming-webhook-url>`. (5) Restart the gateway and send a DM to the Synology Chat bot.

For webhook auth, OpenClaw accepts the outgoing webhook token from `body.token`, then `?token=...`, then headers, in that order. Accepted header forms are `x-synology-token`, `x-webhook-token`, `x-openclaw-token`, and `Authorization: Bearer <token>`. Empty or missing tokens **fail closed**.

The minimal config (json5) shows the canonical channel keys:

```json5
{
  channels: {
    "synology-chat": {
      enabled: true,
      token: "synology-outgoing-token",
      incomingUrl: "https://nas.example.com/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=...",
      webhookPath: "/webhook/synology",
      dmPolicy: "allowlist",
      allowedUserIds: ["123456"],
      rateLimitPerMinute: 30,
      allowInsecureSsl: false,
    },
  },
}
```

## Environment variables

For the **default account**, you can use env vars: `SYNOLOGY_CHAT_TOKEN`, `SYNOLOGY_CHAT_INCOMING_URL`, `SYNOLOGY_NAS_HOST`, `SYNOLOGY_ALLOWED_USER_IDS` (comma-separated), `SYNOLOGY_RATE_LIMIT`, and `OPENCLAW_BOT_NAME`. Config values override env vars. Note that `SYNOLOGY_CHAT_INCOMING_URL` **cannot** be set from a workspace `.env`; the source page links its Workspace `.env` files section (`/gateway/security`) for that restriction.

## DM policy and access control

`dmPolicy: "allowlist"` is the recommended default. `allowedUserIds` accepts a list (or comma-separated string) of Synology user IDs. In `allowlist` mode, an **empty** `allowedUserIds` list is treated as misconfiguration and the webhook route will not start (use `dmPolicy: "open"` with `allowedUserIds: ["*"]` for allow-all). `dmPolicy: "open"` allows public DMs only when `allowedUserIds` includes `"*"`; with restrictive entries, only matching users can chat. `dmPolicy: "disabled"` blocks DMs.

Reply recipient binding stays on the stable numeric `user_id` by default. `channels.synology-chat.dangerouslyAllowNameMatching: true` is a break-glass compatibility mode that re-enables mutable username/nickname lookup for reply delivery. Pairing approvals work with `openclaw pairing list synology-chat` and `openclaw pairing approve synology-chat <CODE>`.

## Outbound delivery

Use numeric Synology Chat **user IDs** as targets. The source page shows three equivalent target forms — a bare numeric ID, a `synology-chat:` prefix, and a short `synology:` prefix:

```bash
openclaw message send --channel synology-chat --target 123456 --text "Hello from OpenClaw"
openclaw message send --channel synology-chat --target synology-chat:123456 --text "Hello again"
openclaw message send --channel synology-chat --target synology:123456 --text "Short prefix"
```

Media sends are supported by **URL-based file delivery**. Outbound file URLs must use `http` or `https`, and private or otherwise blocked network targets are rejected **before** OpenClaw forwards the URL to the NAS webhook (an SSRF guard).

## Multi-account

Multiple Synology Chat accounts are supported under `channels.synology-chat.accounts`. Each account can override `token`, incoming URL, webhook path, DM policy, and limits. Direct-message sessions are **isolated per account and user**, so the same numeric `user_id` on two different Synology accounts does not share transcript state. Give each enabled account a distinct `webhookPath`: OpenClaw now rejects duplicate exact paths and refuses to start named accounts that only inherit a shared webhook path in multi-account setups. If you intentionally need legacy inheritance for a named account, set `dangerouslyAllowInheritedWebhookPath: true` on that account or at `channels.synology-chat` — but duplicate exact paths are still rejected fail-closed. Prefer explicit per-account paths.

```json5
{
  channels: {
    "synology-chat": {
      enabled: true,
      accounts: {
        default: {
          token: "token-a",
          incomingUrl: "https://nas-a.example.com/...token=...",
        },
        alerts: {
          token: "token-b",
          incomingUrl: "https://nas-b.example.com/...token=...",
          webhookPath: "/webhook/synology-alerts",
          dmPolicy: "allowlist",
          allowedUserIds: ["987654"],
        },
      },
    },
  },
}
```

## Security notes

Keep `token` secret and rotate it if leaked. Keep `allowInsecureSsl: false` unless you explicitly trust a self-signed local NAS cert. Inbound webhook requests are **token-verified and rate-limited per sender**. Invalid-token checks use **constant-time** secret comparison and **fail closed**. Prefer `dmPolicy: "allowlist"` for production. Keep `dangerouslyAllowNameMatching` off unless you explicitly need legacy username-based reply delivery. Keep `dangerouslyAllowInheritedWebhookPath` off unless you explicitly accept shared-path routing risk in a multi-account setup.

## Troubleshooting

The source page enumerates these failure signatures and their causes. `Missing required fields (token, user_id, text)` — the outgoing webhook payload is missing one of the required fields; if Synology sends the token in headers, make sure the gateway/proxy preserves those headers. `Invalid token` — the outgoing webhook secret does not match `channels.synology-chat.token`, the request is hitting the wrong account/webhook path, or a reverse proxy stripped the token header before the request reached OpenClaw. `Rate limit exceeded` — too many invalid token attempts from the same source can temporarily lock that source out, and authenticated senders also have a separate per-user message rate limit. `Allowlist is empty. Configure allowedUserIds or use dmPolicy=open with allowedUserIds=["*"].` — `dmPolicy="allowlist"` is enabled but no users are configured. `User not authorized` — the sender's numeric `user_id` is not in `allowedUserIds`.

**Source**: OpenClaw documentation — `channels/synology-chat` (mirror `inbox/openclaw_docs/channels/synology-chat.md`)
**Last Updated**: 2026-06-22
**Status**: Active
