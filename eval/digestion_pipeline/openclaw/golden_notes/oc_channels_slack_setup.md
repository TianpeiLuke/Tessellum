---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - slack
keywords:
  - openclaw slack setup
  - slack socket mode vs http request urls
  - openclaw plugins install slack
  - slack app manifest oauth scopes
  - slack appToken botToken signingSecret
  - socket mode transport tuning pong timeout
  - slack webhookPath multi-account
  - connections:write app-level token
topics:
  - OpenClaw
  - Slack Channel Setup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/slack
access_control_group: ["general"]
---

# OpenClaw — Slack Channel Setup (Socket Mode vs HTTP Request URLs)

## Overview

This note is the setup procedure for the OpenClaw Slack channel, mirroring the setup half of the `channels/slack` source page: choosing the transport (Socket Mode vs HTTP Request URLs), installing `@openclaw/slack`, the per-transport quick-setup flow (app creation from a manifest, token capture, config patch, gateway start), Socket Mode transport tuning, and the app-manifest + OAuth-scope checklist. The Slack channel is production-ready for DMs and channels; the default mode is Socket Mode, with HTTP Request URLs also supported. The token/access model, messaging-runtime UX, and interactivity/ops/config-reference are deliberately out of scope here — they live in the sibling notes `oc_channels_slack_security_access`, `oc_channels_slack_messaging`, and `oc_channels_slack_interactivity`.

## Choosing Socket Mode or HTTP Request URLs

Both transports are production-ready and reach feature parity for messaging, slash commands, App Home, and interactivity — pick by deployment shape, not features. The decisive differences are: **Public Gateway URL** — not required for Socket Mode; required (DNS, TLS, reverse proxy or tunnel) for HTTP. **Outbound network** — Socket Mode needs outbound WSS to `wss-primary.slack.com` reachable; HTTP has no outbound WS, only inbound HTTPS. **Tokens** — Socket Mode needs Bot token + App-Level Token with `connections:write`; HTTP needs Bot token + Signing Secret. **Dev laptop / behind firewall** — Socket Mode works as-is; HTTP needs a public tunnel (ngrok, Cloudflare Tunnel, Tailscale Funnel) or staging Gateway. **Horizontal scaling** — one Socket Mode session per app per host (multiple Gateways need separate Slack apps); HTTP is a stateless POST handler, so multiple replicas can share one app behind a load balancer. **Multi-account on one Gateway** — Socket Mode opens its own WS per account; HTTP needs a unique `webhookPath` (default `/slack/events`) per account so registrations do not collide. **Slash command transport** — Socket Mode delivers over the WS and ignores `slash_commands[].url`; HTTP requires that `url` so Slack can POST. **Request signing** — Socket Mode does not use it (auth is the App-Level Token); HTTP verifies every signed request with `signingSecret`. **Recovery on drop** — Socket Mode auto-reconnects (Slack SDK plus OpenClaw bounded-backoff restart with pong-timeout tuning); HTTP has no persistent connection, so retries are per-request.

Pick Socket Mode for single-Gateway hosts, dev laptops, and on-prem networks that can reach `*.slack.com` outbound but cannot accept inbound HTTPS. Pick HTTP Request URLs when running multiple Gateway replicas behind a load balancer, when outbound WSS is blocked but inbound HTTPS is allowed, or when you already terminate Slack webhooks at a reverse proxy.

## Install

Install the Slack plugin before configuring the channel; `plugins install` registers and enables the plugin, but it does nothing until you configure the Slack app and channel settings:

```bash
openclaw plugins install @openclaw/slack
```

## Quick setup

The flow is the same shape for both transports: create the Slack app from a manifest, capture tokens, patch the OpenClaw config, and start the gateway. Open [api.slack.com/apps](https://api.slack.com/apps/new) → **Create New App** → **From a manifest** → select your workspace → paste a **Recommended** or **Minimal** manifest → **Next** → **Create**. **Recommended** matches the Slack plugin's full feature set (App Home, slash commands, files, reactions, pins, group DMs, emoji/usergroup reads); **Minimal** covers DMs, channel/group history, mentions, and slash commands but drops files, reactions, pins, group-DM (`mpim:*`), `emoji:read`, and `usergroups:read` for restrictive workspaces.

**Socket Mode (default):** After Slack creates the app, **Basic Information → App-Level Tokens → Generate Token and Scopes**: add `connections:write`, save, and copy the App-Level Token; **Install App → Install to Workspace**: copy the Bot User OAuth Token. Then patch the config with a SecretRef setup (recommended) and start the gateway:

```bash
export SLACK_APP_TOKEN=slack-app-token-example
export SLACK_BOT_TOKEN=slack-bot-token-example
cat > slack.socket.patch.json5 <<'JSON5'
{
  channels: {
    slack: {
      enabled: true,
      mode: "socket",
      appToken: { source: "env", provider: "default", id: "SLACK_APP_TOKEN" },
      botToken: { source: "env", provider: "default", id: "SLACK_BOT_TOKEN" },
    },
  },
}
JSON5
openclaw config patch --file ./slack.socket.patch.json5 --dry-run
openclaw config patch --file ./slack.socket.patch.json5
openclaw gateway
```

An env fallback (`SLACK_APP_TOKEN` / `SLACK_BOT_TOKEN`) is supported for the default account only.

**HTTP Request URLs:** When pasting the manifest, replace `https://gateway-host.example.com/slack/events` with your public Gateway URL. The three URL fields — `slash_commands[].url`, `event_subscriptions.request_url`, and `interactivity.request_url` / `message_menu_options_url` — all point at the same OpenClaw endpoint; Slack's schema requires them named separately, but OpenClaw routes by payload type so a single `webhookPath` (default `/slack/events`) is enough. Slash commands without `slash_commands[].url` silently no-op in HTTP mode. After Slack creates the app, **Basic Information → App Credentials**: copy the **Signing Secret**; **Install App → Install to Workspace**: copy the Bot User OAuth Token. Then patch the config and start the gateway:

```bash
export SLACK_BOT_TOKEN=slack-bot-token-example
export SLACK_SIGNING_SECRET=...
cat > slack.http.patch.json5 <<'JSON5'
{
  channels: {
    slack: {
      enabled: true,
      mode: "http",
      botToken: { source: "env", provider: "default", id: "SLACK_BOT_TOKEN" },
      signingSecret: { source: "env", provider: "default", id: "SLACK_SIGNING_SECRET" },
      webhookPath: "/slack/events",
    },
  },
}
JSON5
openclaw config patch --file ./slack.http.patch.json5 --dry-run
openclaw config patch --file ./slack.http.patch.json5
openclaw gateway
```

Give each multi-account HTTP account a distinct `webhookPath` (default `/slack/events`) so registrations do not collide.

## Socket Mode transport tuning

OpenClaw sets the Slack SDK client pong timeout to 15 seconds by default for Socket Mode; override the transport settings only when you need workspace- or host-specific tuning (workspaces that log Slack websocket pong/server-ping timeouts, or hosts with known event-loop starvation):

```json5
{
  channels: {
    slack: {
      mode: "socket",
      socketMode: {
        clientPingTimeout: 20000,
        serverPingTimeout: 30000,
        pingPongLoggingEnabled: false,
      },
    },
  },
}
```

`clientPingTimeout` is the pong wait after the SDK sends a client ping; `serverPingTimeout` is the wait for Slack server pings; app messages and events remain application state, not transport liveness signals. Key behavior: `socketMode` is ignored in HTTP Request URL mode. Base `channels.slack.socketMode` settings apply to all Slack accounts unless overridden; per-account overrides use `channels.slack.accounts.<accountId>.socketMode` and, because it is an object override, must include every socket tuning field you want for that account. Only `clientPingTimeout` has an OpenClaw default (`15000`); `serverPingTimeout` and `pingPongLoggingEnabled` are passed to the Slack SDK only when configured. Socket Mode restart backoff starts around 2 seconds and caps around 30 seconds — recoverable start, start-wait, and disconnect failures retry until the channel stops, while permanent account/credential errors (invalid auth, revoked tokens, missing scopes) fail fast instead of retrying forever.

## Manifest and scope checklist

The base Slack app manifest is the same for Socket Mode and HTTP Request URLs; only the `settings` block (and the slash command `url`) differs. The base manifest (Socket Mode default) declares `display_information`, a `bot_user` (`always_online: true`), an `app_home` with Home + Messages tabs, an `assistant_view`, one `/openclaw` slash command, the full `oauth_config.scopes.bot` list, and `settings.socket_mode_enabled: true` with the full `event_subscriptions.bot_events` set:

```json
{
  "oauth_config": {
    "scopes": {
      "bot": [
        "app_mentions:read", "assistant:write", "channels:history", "channels:read",
        "chat:write", "commands", "emoji:read", "files:read", "files:write",
        "groups:history", "groups:read", "im:history", "im:read", "im:write",
        "mpim:history", "mpim:read", "mpim:write", "pins:read", "pins:write",
        "reactions:read", "reactions:write", "usergroups:read", "users:read"
      ]
    }
  },
  "settings": {
    "socket_mode_enabled": true,
    "event_subscriptions": {
      "bot_events": [
        "app_home_opened", "app_mention", "assistant_thread_context_changed",
        "assistant_thread_started", "channel_rename", "member_joined_channel",
        "member_left_channel", "message.channels", "message.groups", "message.im",
        "message.mpim", "pin_added", "pin_removed", "reaction_added", "reaction_removed"
      ]
    }
  }
}
```

For **HTTP Request URLs mode**, replace `settings` with the HTTP variant (move `bot_events` under `event_subscriptions.request_url`, add an `interactivity` block with `is_enabled: true` plus `request_url` / `message_menu_options_url`) and add a `url` to each slash command — all set to the public Gateway URL. The default manifest also enables the Slack App Home **Home** tab (subscribed to `app_home_opened`; OpenClaw publishes a safe default Home view with `views.publish` — no conversation payload or private config), keeps the **Messages** tab enabled for DMs, and enables Slack assistant threads (`features.assistant_view`, `assistant:write`, `assistant_thread_started`, `assistant_thread_context_changed`) which route to their own OpenClaw thread sessions.

### Additional manifest settings

These extend the defaults. **Optional native slash commands:** multiple native slash commands can replace the single configured command — use `/agentstatus` instead of `/status` (which is reserved), and no more than 25 commands can be available at once; replace `features.slash_commands` with a subset of the available commands (and in HTTP mode add `"url": "https://gateway-host.example.com/slack/events"` to every entry). **Optional authorship scopes (write):** add the `chat:write.customize` bot scope to let outgoing messages use the active agent identity (custom username and icon) instead of the default Slack app identity; emoji icons use `:emoji_name:` syntax. **Optional user-token scopes (read):** if you configure `channels.slack.userToken`, typical read scopes are `channels:history`, `groups:history`, `im:history`, `mpim:history`, the matching `*:read` scopes, `users:read`, `reactions:read`, `pins:read`, `emoji:read`, and `search:read` (if you depend on Slack search reads).

**Source**: OpenClaw documentation — `channels/slack` (mirror `inbox/openclaw_docs/channels/slack.md`)
**Last Updated**: 2026-06-22
**Status**: Active
