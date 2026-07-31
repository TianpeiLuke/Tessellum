---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - clickclack
keywords:
  - openclaw clickclack channel
  - clickclack bot token
  - clickclack admin bot create
  - clickclack target syntax
  - clickclack bot scopes
  - allowAgentIdOverride
  - clickclack multiple bots accounts
  - clickclack troubleshooting
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/clickclack
access_control_group: ["general"]
---

# OpenClaw — Connecting the ClickClack Chat Channel

## Overview

This note is the procedure for connecting OpenClaw to a self-hosted **ClickClack** workspace through first-class ClickClack bot tokens, so an OpenClaw agent appears as a ClickClack bot user. ClickClack supports independent service bots and user-owned bots; a user-owned bot keeps an `owner_user_id` and receives only the token scopes you grant. It mirrors the `channels/clickclack` source page end to end — quick setup (create a bot token, configure `channels.clickclack`, run the gateway), running multiple bots via per-account connections, the `channel:` / `dm:` / `thread:` outbound target syntax, the `bot:read` / `bot:write` / `bot:admin` token scopes, and the common-failure troubleshooting checks.

## Quick setup

First create a bot token in ClickClack with the admin CLI. For a user-owned bot, add `--owner <user_id>`.

```bash
clickclack admin bot create \
  --workspace <workspace_id_or_slug> \
  --name "OpenClaw" \
  --handle openclaw \
  --scopes bot:write \
  --plain
```

Then configure OpenClaw. The channel block declares `enabled`, the `baseUrl`, a `token` SecretRef (`source: "env"`, `provider: "default"`, `id: "CLICKCLACK_BOT_TOKEN"`), the `workspace`, a `defaultTo` target, the `agentId`, and `replyMode`. The plugin entry sets `allowAgentIdOverride: true` (see Multiple bots for why):

```json5
{
  plugins: {
    entries: {
      clickclack: {
        llm: {
          allowAgentIdOverride: true,
        },
      },
    },
  },
  channels: {
    clickclack: {
      enabled: true,
      baseUrl: "https://app.clickclack.chat",
      token: { source: "env", provider: "default", id: "CLICKCLACK_BOT_TOKEN" },
      workspace: "default",
      defaultTo: "channel:general",
      agentId: "clickclack-bot",
      replyMode: "model",
    },
  },
}
```

Then export the token and run the gateway:

```bash
export CLICKCLACK_BOT_TOKEN="ccb_..."
openclaw gateway
```

If `plugins.allow` is a non-empty restrictive list, explicitly selecting ClickClack in channel setup or running `openclaw plugins enable clickclack` appends `clickclack` to that list; onboarding installation uses the same explicit-selection behavior. These paths do not override `plugins.deny` or a global `plugins.enabled: false` setting. Direct `openclaw plugins install clickclack` follows the normal plugin-install policy and also records ClickClack in an existing allowlist.

## Multiple bots

Each account opens its own ClickClack realtime connection and uses its own bot token. Set `defaultAccount` and define each bot under `channels.clickclack.accounts.*`, each with its own `token` SecretRef, `workspace`, `defaultTo`, `agentId`, and `replyMode`:

```json5
{
  plugins: {
    entries: {
      clickclack: {
        llm: {
          allowAgentIdOverride: true,
        },
      },
    },
  },
  channels: {
    clickclack: {
      enabled: true,
      baseUrl: "https://app.clickclack.chat",
      defaultAccount: "service",
      accounts: {
        service: {
          token: { source: "env", provider: "default", id: "CLICKCLACK_SERVICE_BOT_TOKEN" },
          workspace: "default",
          defaultTo: "channel:general",
          agentId: "service-bot",
          replyMode: "model",
        },
        peter: {
          token: { source: "env", provider: "default", id: "CLICKCLACK_PETER_BOT_TOKEN" },
          workspace: "default",
          defaultTo: "dm:usr_...",
          agentId: "peter-bot",
          replyMode: "model",
        },
      },
    },
  },
}
```

`replyMode: "model"` uses `api.runtime.llm.complete` directly for short bot replies. When an account sets `agentId`, OpenClaw requires the explicit `plugins.entries.clickclack.llm.allowAgentIdOverride` trust bit so the plugin can run completions for that bot agent. Keep it off if you only use the default agent route.

## Targets

Outbound targets follow the channel target grammar:

- `channel:<name-or-id>` sends to a workspace channel. Bare targets default to `channel:`.
- `dm:<user_id>` creates or reuses a direct conversation with that user.
- `thread:<message_id>` replies in an existing thread.

```bash
openclaw message send --channel clickclack --target channel:general --message "hello"
openclaw message send --channel clickclack --target dm:usr_123 --message "hello"
openclaw message send --channel clickclack --target thread:msg_123 --message "following up"
```

## Permissions

ClickClack token scopes are enforced by the ClickClack API. The three scopes are cumulative:

- `bot:read`: read workspace/channel/message/thread/DM/realtime/profile data.
- `bot:write`: `bot:read` plus channel messages, thread replies, DMs, and uploads.
- `bot:admin`: `bot:write` plus channel creation.

OpenClaw only needs `bot:write` for normal agent chat.

## Troubleshooting

- `ClickClack is not configured`: set `channels.clickclack.token` or `CLICKCLACK_BOT_TOKEN`.
- `workspace not found`: set `workspace` to the workspace id or slug returned by ClickClack.
- No inbound replies: confirm the token has realtime read access and the bot is not replying to its own messages.
- Channel sends fail: verify the bot is a member of the workspace and has `bot:write`.

**Source**: OpenClaw documentation — `channels/clickclack` (mirror `inbox/openclaw_docs/channels/clickclack.md`)
**Last Updated**: 2026-06-22
**Status**: Active
