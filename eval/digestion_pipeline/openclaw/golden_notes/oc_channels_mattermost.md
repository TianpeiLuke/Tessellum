---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - mattermost
keywords:
  - openclaw mattermost channel setup
  - mattermost bot token base url
  - mattermost native slash commands callback
  - mattermost chatmode oncall onmessage onchar
  - mattermost replyToMode threading sessions
  - mattermost dmPolicy groupPolicy allowlist
  - mattermost dmChannelRetry
  - mattermost preview streaming partial block progress
  - mattermost multi-account directory adapter
  - mattermost troubleshooting slash commands
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/mattermost
access_control_group: ["general"]
---

# OpenClaw — Connecting the Mattermost Channel

## Overview

This note is the operator procedure for connecting OpenClaw to **Mattermost**, a self-hostable team messaging platform, mirroring the `channels/mattermost` source page. The Mattermost channel ships as a downloadable plugin that connects with a **bot token + WebSocket events** and supports channels, groups, and DMs. The procedure walks through plugin install, minimal bot-token/base-URL config, opt-in native `oc_*` slash commands and their callback reachability, environment variables, channel chat modes, threading/session routing, DM and group access control, outbound target resolution, DM-channel retry, preview streaming, reactions, the directory adapter, multi-account config, and troubleshooting. The interactive-buttons message-tool surface and the external-script Direct-API/HMAC contract are split into the sibling model note [oc_channels_mattermost_buttons](oc_channels_mattermost_buttons.md).

## Install

Install the Mattermost plugin before configuring the channel. Current packaged OpenClaw releases already bundle it; older or custom installs add it manually. Install from the npm registry with `openclaw plugins install @openclaw/mattermost`, or from a local checkout with `openclaw plugins install ./path/to/local/mattermost-plugin`. See the Plugins docs (`/tools/plugin`) for details.

## Quick setup

The minimal bring-up is four steps: ensure the plugin is available (bundled in current releases, or installed via the commands above); create a Mattermost bot account and copy the **bot token**; copy the Mattermost **base URL** (e.g., `https://chat.example.com`); then configure OpenClaw and start the gateway with the minimal config below.

```json5
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
    },
  },
}
```

## Native slash commands

Native slash commands are **opt-in**. When enabled, OpenClaw registers `oc_*` slash commands via the Mattermost API and receives callback POSTs on the gateway HTTP server. Enable them under `channels.mattermost.commands` with `native: true`, `nativeSkills: true`, a `callbackPath` (default `/api/channels/mattermost/command`), and an optional `callbackUrl` for when Mattermost cannot reach the gateway directly (reverse proxy / public URL).

```json5
{
  channels: {
    mattermost: {
      commands: {
        native: true,
        nativeSkills: true,
        callbackPath: "/api/channels/mattermost/command",
        // Use when Mattermost cannot reach the gateway directly (reverse proxy/public URL).
        callbackUrl: "https://gateway.example.com/api/channels/mattermost/command",
      },
    },
  },
}
```

**Behavior notes.** `native: "auto"` defaults to disabled for Mattermost — set `native: true` to enable. If `callbackUrl` is omitted, OpenClaw derives one from the gateway host/port + `callbackPath`. For multi-account setups, `commands` can be set at the top level or under `channels.mattermost.accounts.<id>.commands` (account values override top-level fields). Command callbacks are validated with the per-command tokens Mattermost returns when OpenClaw registers `oc_*` commands. OpenClaw refreshes current Mattermost command registration before accepting each callback, so stale tokens from deleted or regenerated slash commands stop being accepted without a gateway restart. Callback validation **fails closed** if the Mattermost API cannot confirm the command is still current; failed validations are cached briefly, concurrent lookups are coalesced, and fresh lookup starts are rate-limited per command to bound replay pressure. Slash callbacks also fail closed when registration failed, startup was partial, or the callback token does not match the resolved command's registered token (a token valid for one command cannot reach upstream validation for a different command).

**Reachability requirement.** The callback endpoint must be reachable from the Mattermost server. Do not set `callbackUrl` to `localhost` unless Mattermost runs on the same host/network namespace as OpenClaw, and do not set it to your Mattermost base URL unless that URL reverse-proxies `/api/channels/mattermost/command` to OpenClaw. A quick check is `curl https://<gateway-host>/api/channels/mattermost/command` — a GET should return `405 Method Not Allowed` from OpenClaw, not `404`.

**Mattermost egress allowlist.** If your callback targets private/tailnet/internal addresses, set Mattermost `ServiceSettings.AllowedUntrustedInternalConnections` to include the callback host/domain. Use host/domain entries, not full URLs — good: `gateway.tailnet-name.ts.net`; bad: `https://gateway.tailnet-name.ts.net`.

## Environment variables (default account)

If you prefer env vars, set these on the gateway host: `MATTERMOST_BOT_TOKEN=...` and `MATTERMOST_URL=https://chat.example.com`. Env vars apply only to the **default** account (`default`); other accounts must use config values. `MATTERMOST_URL` cannot be set from a workspace `.env` (see Workspace `.env` files at `/gateway/security`).

## Chat modes

Mattermost responds to DMs automatically; channel behavior is controlled by `chatmode`. The modes are `oncall` (default — respond only when @mentioned in channels), `onmessage` (respond to every channel message), and `onchar` (respond when a message starts with a trigger prefix). Configure `onchar` with `channels.mattermost.chatmode: "onchar"` plus `channels.mattermost.oncharPrefixes: [">", "!"]`. Notes: `onchar` still responds to explicit @mentions, and `channels.mattermost.requireMention` is honored for legacy configs but `chatmode` is preferred.

## Threading and sessions

Use `channels.mattermost.replyToMode` (e.g. `channels.mattermost.replyToMode: "all"`) to control whether channel and group replies stay in the main channel or start a thread under the triggering post. `off` (default) only replies in a thread when the inbound post is already in one; `first` starts a thread under a top-level channel/group post and routes the conversation to a thread-scoped session; `all` behaves the same as `first` for Mattermost today. Direct messages ignore this setting and stay non-threaded. Thread-scoped sessions use the triggering post id as the thread root, and `first` and `all` are currently equivalent because once Mattermost has a thread root, follow-up chunks and media continue in that same thread.

## Access control (DMs)

The default DM policy is `channels.mattermost.dmPolicy = "pairing"` (unknown senders get a pairing code). Approve via `openclaw pairing list mattermost` and `openclaw pairing approve mattermost <CODE>`. For public DMs, set `channels.mattermost.dmPolicy="open"` plus `channels.mattermost.allowFrom=["*"]`. `channels.mattermost.allowFrom` also accepts `accessGroup:<name>` entries (see Access groups at `/channels/access-groups`).

## Channels (groups)

The default group policy is `channels.mattermost.groupPolicy = "allowlist"` (mention-gated). Allowlist senders with `channels.mattermost.groupAllowFrom` (user IDs recommended), which also accepts `accessGroup:<name>` entries. Per-channel mention overrides live under `channels.mattermost.groups.<channelId>.requireMention`, or `channels.mattermost.groups["*"].requireMention` for a default. `@username` matching is mutable and only enabled when `channels.mattermost.dangerouslyAllowNameMatching: true`. Open channels use `channels.mattermost.groupPolicy="open"` (still mention-gated). Runtime note: if `channels.mattermost` is completely missing, runtime falls back to `groupPolicy="allowlist"` for group checks (even if `channels.defaults.groupPolicy` is set). Example:

```json5
{
  channels: {
    mattermost: {
      groupPolicy: "open",
      groups: {
        "*": { requireMention: true },
        "team-channel-id": { requireMention: false },
      },
    },
  },
}
```

## Targets for outbound delivery

Use these target formats with `openclaw message send` or cron/webhooks: `channel:<id>` for a channel, `user:<id>` for a DM, and `@username` for a DM (resolved via the Mattermost API). Bare opaque IDs (like `64ifufp...`) are **ambiguous** in Mattermost (user ID vs channel ID); OpenClaw resolves them **user-first** — if the ID exists as a user (`GET /api/v4/users/<id>` succeeds) it sends a **DM** by resolving the direct channel via `/api/v4/channels/direct`, otherwise the ID is treated as a **channel ID**. For deterministic behavior, always use the explicit prefixes (`user:<id>` / `channel:<id>`).

## DM channel retry

When OpenClaw sends to a Mattermost DM target and needs to resolve the direct channel first, it retries transient direct-channel creation failures by default. Tune that behavior globally with `channels.mattermost.dmChannelRetry`, or per-account with `channels.mattermost.accounts.<id>.dmChannelRetry`. This applies only to DM channel creation (`/api/v4/channels/direct`), not every Mattermost API call; retries apply to transient failures such as rate limits, 5xx responses, and network or timeout errors, while 4xx client errors other than `429` are treated as permanent and not retried.

```json5
{
  channels: {
    mattermost: {
      dmChannelRetry: {
        maxRetries: 3,
        initialDelayMs: 1000,
        maxDelayMs: 10000,
        timeoutMs: 30000,
      },
    },
  },
}
```

## Preview streaming

Mattermost streams thinking, tool activity, and partial reply text into a single **draft preview post** that finalizes in place when the final answer is safe to send. The preview updates on the same post id instead of spamming the channel with per-chunk messages, and media/error finals cancel pending preview edits and use normal delivery instead of flushing a throwaway preview post. Enable via `channels.mattermost.streaming` with one of `off | partial | block | progress`. `partial` is the usual choice (one preview post edited as the reply grows, then finalized with the complete answer); `block` uses append-style draft chunks inside the preview post; `progress` shows a status preview while generating and only posts the final answer at completion; `off` disables preview streaming. If the stream cannot be finalized in place (for example the post was deleted mid-stream), OpenClaw falls back to sending a fresh final post so the reply is never lost. Thinking-only payloads are suppressed from channel posts, including text arriving as a `> Thinking` blockquote — set `/reasoning on` to see thinking in other surfaces, while the Mattermost final post keeps the answer only. See Streaming (`/concepts/streaming#preview-streaming-modes`) for the channel-mapping matrix.

## Reactions (message tool)

Use `message action=react` with `channel=mattermost`. `messageId` is the Mattermost post id; `emoji` accepts names like `thumbsup` or `:+1:` (colons are optional); set `remove=true` (boolean) to remove a reaction. Reaction add/remove events are forwarded as system events to the routed agent session. Reaction actions are configured by `channels.mattermost.actions.reactions` (enable/disable, default true), with a per-account override at `channels.mattermost.accounts.<id>.actions.reactions`. Examples (interactive buttons and their HMAC Direct-API path are documented in [oc_channels_mattermost_buttons](oc_channels_mattermost_buttons.md)):

```
message action=react channel=mattermost target=channel:<channelId> messageId=<postId> emoji=thumbsup
message action=react channel=mattermost target=channel:<channelId> messageId=<postId> emoji=thumbsup remove=true
```

## Directory adapter

The Mattermost plugin includes a directory adapter that resolves channel and user names via the Mattermost API, enabling `#channel-name` and `@username` targets in `openclaw message send` and cron/webhook deliveries. No configuration is needed — the adapter uses the bot token from the account config.

## Multi-account

Mattermost supports multiple accounts under `channels.mattermost.accounts`, each with its own `name`, `botToken`, and `baseUrl`. Note that env vars apply only to the `default` account; other accounts must set their credentials in config:

```json5
{
  channels: {
    mattermost: {
      accounts: {
        default: { name: "Primary", botToken: "mm-token", baseUrl: "https://chat.example.com" },
        alerts: { name: "Alerts", botToken: "mm-token-2", baseUrl: "https://alerts.example.com" },
      },
    },
  },
}
```

## Troubleshooting

**No replies in channels** — ensure the bot is in the channel and mention it (oncall), use a trigger prefix (onchar), or set `chatmode: "onmessage"`.

**Auth or multi-account errors** — check the bot token, base URL, and whether the account is enabled; remember env vars only apply to the `default` account.

**Native slash commands fail** — `Unauthorized: invalid command token.` means OpenClaw did not accept the callback token; typical causes are: slash command registration failed or only partially completed at startup, the callback is hitting the wrong gateway/account, Mattermost still has old commands pointing at a previous callback target, or the gateway restarted without reactivating slash commands. If native slash commands stop working, check logs for `mattermost: failed to register slash commands` or `mattermost: native slash commands enabled but no commands could be registered`. If `callbackUrl` is omitted and logs warn that the callback resolved to `http://127.0.0.1:18789/...`, that URL is probably only reachable when Mattermost runs on the same host/network namespace as OpenClaw — set an explicit externally reachable `commands.callbackUrl` instead.

**Buttons issues** are catalogued alongside the interactive-buttons contract in the sibling note [oc_channels_mattermost_buttons](oc_channels_mattermost_buttons.md).

**Source**: OpenClaw documentation — `channels/mattermost` (mirror `inbox/openclaw_docs/channels/mattermost.md`)
**Last Updated**: 2026-06-22
**Status**: Active
