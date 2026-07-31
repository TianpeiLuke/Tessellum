---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - twitch
keywords:
  - openclaw twitch channel
  - twitch chat irc bot
  - twitch access token oauth
  - twitch token refresh
  - twitch allowFrom allowedRoles
  - twitch multi-account accounts
  - requireMention twitch
  - twitch 500 character chunking
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/twitch
access_control_group: ["general"]
---

# OpenClaw — Twitch Chat Channel Setup

## Overview

This note is the procedure for configuring the OpenClaw **Twitch** chat channel, mirroring the `channels/twitch` source page. Twitch chat support runs over an IRC connection: OpenClaw connects as a Twitch user (a dedicated bot account) to receive and send messages in a channel's chat room. The note covers the bundled plugin, the beginner quick-setup flow, what the channel is, detailed setup (generating credentials, configuring the bot, access control), optional token refresh, multi-account support, the full configuration reference (account config + provider options), tool actions, safety/ops guidance, and message limits.

## Bundled plugin

Twitch ships as a **bundled plugin** in current OpenClaw releases, so normal packaged builds do not need a separate install. If you are on an older build or a custom install that excludes Twitch, install the npm package directly: `openclaw plugins install @openclaw/twitch` (npm registry) or `openclaw plugins install ./path/to/local/twitch-plugin` (local checkout). Use the bare package to follow the current official release tag; pin an exact version only when you need a reproducible install. See the Plugins page (`/tools/plugin`, linked under References) for plugin-install rules.

## Quick setup (beginner)

The beginner flow has six steps: (1) **Ensure the plugin is available** — current packaged releases already bundle it; older/custom installs add it manually with the commands above. (2) **Create a Twitch bot account** — a dedicated Twitch account for the bot (or use an existing account). (3) **Generate credentials** using [Twitch Token Generator](https://twitchtokengenerator.com/): select **Bot Token**, verify scopes `chat:read` and `chat:write` are selected, and copy the **Client ID** and **Access Token**. (4) **Find your Twitch user ID** using the StreamWeasels username-to-user-ID converter. (5) **Configure the token** via the env var `OPENCLAW_TWITCH_ACCESS_TOKEN=...` (default account only) or the config key `channels.twitch.accessToken` — if both are set, config takes precedence (the env fallback is default-account only). (6) **Start the gateway** with the configured channel.

The source includes a warning: add access control (`allowFrom` or `allowedRoles`) to prevent unauthorized users from triggering the bot, and `requireMention` defaults to `true`. The minimal config is:

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw", // Bot's Twitch account
      accessToken: "oauth:abc123...", // OAuth Access Token (or use OPENCLAW_TWITCH_ACCESS_TOKEN env var)
      clientId: "xyz789...", // Client ID from Token Generator
      channel: "vevisk", // Which Twitch channel's chat to join (required)
      allowFrom: ["123456789"], // (recommended) Your Twitch user ID only - get it from https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
    },
  },
}
```

## What it is

A Twitch channel is owned by the Gateway. Routing is **deterministic**: replies always go back to Twitch. Each account maps to an isolated session key `agent:<agentId>:twitch:<accountName>`. The `username` is the bot's account (who authenticates), while `channel` is which chat room to join.

## Setup (detailed)

### Generate credentials

Use [Twitch Token Generator](https://twitchtokengenerator.com/): select **Bot Token**, verify scopes `chat:read` and `chat:write` are selected, and copy the **Client ID** and **Access Token**. No manual app registration is needed. Tokens expire after several hours.

### Configure the bot

Provide the token either as an env var (default account only) — `OPENCLAW_TWITCH_ACCESS_TOKEN=oauth:abc123...` — or in config under `channels.twitch` with `enabled`, `username`, `accessToken`, `clientId`, and `channel`. If both env and config are set, config takes precedence.

### Access control (recommended)

Configure `channels.twitch.allowFrom` with the Twitch user ID(s) allowed to trigger the bot (recommended: your Twitch user ID only). Prefer `allowFrom` for a hard allowlist; use `allowedRoles` instead if you want role-based access. The available roles are `"moderator"`, `"owner"`, `"vip"`, `"subscriber"`, and `"all"`. The source explains **why user IDs?** — usernames can change, allowing impersonation, while user IDs are permanent (find yours with the StreamWeasels username-to-ID converter).

## Token refresh (optional)

Tokens from [Twitch Token Generator](https://twitchtokengenerator.com/) cannot be automatically refreshed — regenerate them when expired. For automatic token refresh, create your own Twitch application at the [Twitch Developer Console](https://dev.twitch.tv/console) and add `clientSecret` and `refreshToken` to config:

```json5
{
  channels: {
    twitch: {
      clientSecret: "your_client_secret",
      refreshToken: "your_refresh_token",
    },
  },
}
```

With these set, the bot automatically refreshes tokens before expiration and logs refresh events.

## Multi-account support

Use `channels.twitch.accounts` with per-account tokens (see the Configuration page, `/gateway/configuration`, linked under References, for the shared pattern). Each account needs its own token — one token per channel. Example (one bot account in two channels):

```json5
{
  channels: {
    twitch: {
      accounts: {
        channel1: {
          username: "openclaw",
          accessToken: "oauth:abc123...",
          clientId: "xyz789...",
          channel: "vevisk",
        },
        channel2: {
          username: "openclaw",
          accessToken: "oauth:def456...",
          clientId: "uvw012...",
          channel: "secondchannel",
        },
      },
    },
  },
}
```

## Access control

Per-account access control offers three modes. A **User ID allowlist (most secure)** sets `allowFrom: ["123456789", "987654321"]` under an account — `allowFrom` is a hard allowlist, so when set only those user IDs are allowed. **Role-based** access leaves `allowFrom` unset and configures `allowedRoles: ["moderator", "vip"]` instead. To **disable the @mention requirement** and respond to all messages, set `requireMention: false` (it defaults to `true`).

## Troubleshooting

First, run diagnostic commands:

```bash
openclaw doctor
openclaw channels status --probe
```

- **Bot does not respond to messages** — Check access control: ensure your user ID is in `allowFrom`, or temporarily remove `allowFrom` and set `allowedRoles: ["all"]` to test. Check the bot is in the channel: the bot must join the channel specified in `channel`.
- **Token issues** ("Failed to connect" or authentication errors) — Verify `accessToken` is the OAuth access token value (typically starts with the `oauth:` prefix); check the token has `chat:read` and `chat:write` scopes; if using token refresh, verify `clientSecret` and `refreshToken` are set.
- **Token refresh not working** — Check logs for refresh events (e.g. `Using env token source for mybot` and `Access token refreshed for user 123456 (expires in 14400s)`). If you see `token refresh disabled (no refresh token)`, ensure `clientSecret` and `refreshToken` are both provided.

## Config

### Account config

Per the source `ParamField` definitions, an account accepts: `username` (string) — bot username; `accessToken` (string) — OAuth access token with `chat:read` and `chat:write`; `clientId` (string) — Twitch Client ID (from Token Generator or your app); `channel` (string, **required**) — channel to join; `enabled` (boolean, default `true`) — enable this account; `clientSecret` (string) — optional, for automatic token refresh; `refreshToken` (string) — optional, for automatic token refresh; `expiresIn` (number) — token expiry in seconds; `obtainmentTimestamp` (number) — token obtained timestamp; `allowFrom` (string[]) — user ID allowlist; `allowedRoles` (`Array<"moderator" | "owner" | "vip" | "subscriber" | "all">`) — role-based access control; and `requireMention` (boolean, default `true`) — require @mention.

### Provider options

The provider-level keys are: `channels.twitch.enabled` — enable/disable channel startup; `channels.twitch.username` — bot username (simplified single-account config); `channels.twitch.accessToken` — OAuth access token (simplified single-account config); `channels.twitch.clientId` — Twitch Client ID (simplified single-account config); `channels.twitch.channel` — channel to join (simplified single-account config); and `channels.twitch.accounts.<accountName>` — multi-account config (all account fields above). The source's full example combines top-level simplified keys with an `accounts.default` block carrying the complete field set (`username`, `accessToken`, `clientId`, `channel`, `enabled`, `clientSecret`, `refreshToken`, `expiresIn: 14400`, `obtainmentTimestamp: 1706092800000`, `allowFrom`, `allowedRoles`).

## Tool actions

The agent can call the `twitch` tool with one action: `send` — send a message to a channel. Example call:

```json5
{
  action: "twitch",
  params: {
    message: "Hello Twitch!",
    to: "#mychannel",
  },
}
```

## Safety and ops

- **Treat tokens like passwords** — never commit tokens to git.
- **Use automatic token refresh** for long-running bots.
- **Use user ID allowlists** instead of usernames for access control.
- **Monitor logs** for token refresh events and connection status.
- **Scope tokens minimally** — only request `chat:read` and `chat:write`.
- **If stuck**: restart the gateway after confirming no other process owns the session.

## Limits

- **500 characters** per message (auto-chunked at word boundaries).
- Markdown is stripped before chunking.
- No rate limiting (uses Twitch's built-in rate limits).

**Source**: OpenClaw documentation — `channels/twitch` (mirror `inbox/openclaw_docs/channels/twitch.md`)
**Last Updated**: 2026-06-22
**Status**: Active
