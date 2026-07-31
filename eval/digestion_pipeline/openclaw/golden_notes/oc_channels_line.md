---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - line
keywords:
  - openclaw line channel
  - line messaging api plugin
  - line webhook signature verification
  - channel access token channel secret
  - line dmpolicy pairing allowlist
  - channeldata.line flex messages
  - line acp conversation bindings
  - line outbound media
topics:
  - OpenClaw
  - LINE Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/line
access_control_group: ["general"]
---

# OpenClaw — Connecting LINE via the Messaging API

## Overview

This note is the operator-facing procedure for connecting OpenClaw to LINE through the LINE Messaging API, mirroring the `channels/line` source page. The plugin runs as a webhook receiver on the gateway and authenticates with your **channel access token** plus **channel secret**. The procedure covers plugin install, the LINE Developers Console webhook setup (with signature-integrity handling), minimal/public/file/multi-account configuration, DM and group access control, message-behavior limits, `channelData.line` rich messages, ACP conversation bindings, outbound media, and troubleshooting. As a status note: LINE is a downloadable plugin supporting direct messages, group chats, media, locations, Flex messages, template messages, and quick replies; reactions and threads are **not** supported.

## Install

Install the LINE plugin before configuring the channel with `openclaw plugins install @openclaw/line`. For a local checkout (when running from a git repo), install from the local path instead:

```bash
openclaw plugins install @openclaw/line
# Local checkout (when running from a git repo):
openclaw plugins install ./path/to/local/line-plugin
```

## Setup (webhook + signature)

Provision the LINE channel in the LINE Developers Console, then point its webhook at the gateway:

1. Create a LINE Developers account and open the Console: [https://developers.line.biz/console/](https://developers.line.biz/console/).
2. Create (or pick) a Provider and add a **Messaging API** channel.
3. Copy the **Channel access token** and **Channel secret** from the channel settings.
4. Enable **Use webhook** in the Messaging API settings.
5. Set the webhook URL to your gateway endpoint (HTTPS required):

```
https://gateway-host/line/webhook
```

The gateway responds to LINE's webhook verification (GET) and acknowledges signed inbound events (POST) immediately after signature and payload validation; agent processing continues asynchronously. If you need a custom path, set `channels.line.webhookPath` or `channels.line.accounts.<id>.webhookPath` and update the URL accordingly.

**Security note.** LINE signature verification is body-dependent (HMAC over the raw body), so OpenClaw applies strict pre-auth body limits and timeout before verification. OpenClaw processes webhook events from the verified raw request bytes; upstream middleware-transformed `req.body` values are ignored for signature-integrity safety.

## Configure

The minimal config enables the channel with the token/secret pair and defaults DMs to pairing:

```json5
{
  channels: {
    line: {
      enabled: true,
      channelAccessToken: "LINE_CHANNEL_ACCESS_TOKEN",
      channelSecret: "LINE_CHANNEL_SECRET",
      dmPolicy: "pairing",
    },
  },
}
```

A public DM config opens DMs to everyone by setting `dmPolicy: "open"` together with `allowFrom: ["*"]`:

```json5
{
  channels: {
    line: {
      enabled: true,
      channelAccessToken: "LINE_CHANNEL_ACCESS_TOKEN",
      channelSecret: "LINE_CHANNEL_SECRET",
      dmPolicy: "open",
      allowFrom: ["*"],
    },
  },
}
```

For the default account only, credentials can come from env vars instead: `LINE_CHANNEL_ACCESS_TOKEN` and `LINE_CHANNEL_SECRET`. Credentials may also be read from token/secret files via `tokenFile` and `secretFile`; both must point to regular files (symlinks are rejected). Multiple LINE accounts are configured under `channels.line.accounts.<id>`, each with its own `channelAccessToken`, `channelSecret`, and `webhookPath` (e.g. an account `marketing` mounting `webhookPath: "/line/marketing"`).

## Access control

Direct messages default to pairing: unknown senders get a pairing code and their messages are ignored until approved. Approve pending DMs with the pairing CLI:

```bash
openclaw pairing list line
openclaw pairing approve line <CODE>
```

Allowlists and policies govern who may interact:

- `channels.line.dmPolicy`: `pairing | allowlist | open | disabled`.
- `channels.line.allowFrom`: allowlisted LINE user IDs for DMs; `dmPolicy: "open"` requires `["*"]`.
- `channels.line.groupPolicy`: `allowlist | open | disabled`.
- `channels.line.groupAllowFrom`: allowlisted LINE user IDs for groups.
- Per-group overrides: `channels.line.groups.<groupId>.allowFrom`.
- Static sender access groups can be referenced from `allowFrom`, `groupAllowFrom`, and per-group `allowFrom` with `accessGroup:<name>`.
- Runtime note: if `channels.line` is completely missing, runtime falls back to `groupPolicy="allowlist"` for group checks (even if `channels.defaults.groupPolicy` is set).

LINE IDs are case-sensitive. Valid IDs look like: **User** = `U` + 32 hex chars; **Group** = `C` + 32 hex chars; **Room** = `R` + 32 hex chars.

## Message behavior

- Text is chunked at 5000 characters.
- Markdown formatting is stripped; code blocks and tables are converted into Flex cards when possible.
- Streaming responses are buffered; LINE receives full chunks with a loading animation while the agent works.
- Media downloads are capped by `channels.line.mediaMaxMb` (default 10).
- Inbound media is saved under `~/.openclaw/media/inbound/` before it is passed to the agent, matching the shared media store used by other bundled channel plugins.

## Channel data (rich messages)

Use `channelData.line` to send quick replies, locations, Flex cards, or template messages:

```json5
{
  text: "Here you go",
  channelData: {
    line: {
      quickReplies: ["Status", "Help"],
      location: {
        title: "Office",
        address: "123 Main St",
        latitude: 35.681236,
        longitude: 139.767125,
      },
      flexMessage: {
        altText: "Status card",
        contents: {
          /* Flex payload */
        },
      },
      templateMessage: {
        type: "confirm",
        text: "Proceed?",
        confirmLabel: "Yes",
        confirmData: "yes",
        cancelLabel: "No",
        cancelData: "no",
      },
    },
  },
}
```

The LINE plugin also ships a `/card` command for Flex message presets, e.g. `/card info "Welcome" "Thanks for joining!"`.

## ACP support

LINE supports ACP (Agent Communication Protocol) conversation bindings. `/acp spawn <agent> --bind here` binds the current LINE chat to an ACP session without creating a child thread. Configured ACP bindings and active conversation-bound ACP sessions work on LINE like other conversation channels. See the OpenClaw `tools/acp-agents` docs (cross-ref `/tools/acp-agents`, listed under References) for details.

## Outbound media

The LINE plugin supports sending images, videos, and audio files through the agent message tool. Media is sent via the LINE-specific delivery path with appropriate preview and tracking handling:

- **Images**: sent as LINE image messages with automatic preview generation.
- **Videos**: sent with explicit preview and content-type handling.
- **Audio**: sent as LINE audio messages.

Outbound media URLs must be public HTTPS URLs. OpenClaw validates the target hostname before handing the URL to LINE and rejects loopback, link-local, and private-network targets. Generic media sends fall back to the existing image-only route when a LINE-specific path is not available.

## Troubleshooting

- **Webhook verification fails:** ensure the webhook URL is HTTPS and the `channelSecret` matches the LINE console.
- **No inbound events:** confirm the webhook path matches `channels.line.webhookPath` and that the gateway is reachable from LINE.
- **Media download errors:** raise `channels.line.mediaMaxMb` if media exceeds the default limit.

**Source**: OpenClaw documentation — `channels/line` (mirror `inbox/openclaw_docs/channels/line.md`)
**Last Updated**: 2026-06-22
**Status**: Active
