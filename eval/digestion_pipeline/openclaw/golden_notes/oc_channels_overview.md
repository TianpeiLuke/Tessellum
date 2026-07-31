---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - messaging
keywords:
  - openclaw chat channels
  - supported messaging platforms
  - channel connects via gateway
  - telegram media conversion
  - slack mpim group routing
  - whatsapp install-on-demand baileys
  - bot loop protection
  - ambient room events
  - dm pairing allowlist
topics:
  - OpenClaw
  - Chat Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/channels
access_control_group: ["general"]
---

# OpenClaw — Chat Channels Overview

## Overview

This note covers the OpenClaw **chat channels** model — the set of messaging platforms OpenClaw can talk to and how it connects them — mirroring the `channels` source page. OpenClaw can talk to you on any chat app you already use, and **each channel connects via the Gateway**: text is supported everywhere, while media and reactions vary by channel. It covers the cross-channel delivery notes (Telegram media conversion, Slack MPIM group routing, WhatsApp install-on-demand, bot-loop protection, and ambient room events), the supported-channel matrix of roughly thirty platforms with their transport and packaging, and the operational notes on running channels simultaneously, fastest setup, group behavior, DM pairing/allowlists, and troubleshooting.

## Delivery Notes

Several cross-channel delivery behaviors apply on the outbound path regardless of which platform is used:

- **Telegram media conversion** — Telegram replies that contain markdown image syntax, such as `![alt](url)`, are converted into media replies on the final outbound path when possible.
- **Slack MPIM group routing** — Slack multi-person DMs route as group chats, so group policy, mention behavior, and group-session rules apply to MPIM conversations.
- **WhatsApp install-on-demand** — WhatsApp setup is install-on-demand: onboarding can show the setup flow before the plugin package is installed, and the Gateway loads the external ClawHub/npm plugin only when the channel is actually active.
- **Bot loop protection** — Channels that accept bot-authored inbound messages can use shared bot loop protection to prevent bot pairs from replying to each other indefinitely.
- **Ambient room events** — Supported always-on rooms can use ambient room events so unmentioned room chatter becomes quiet context unless the agent sends with the `message` tool.

## Supported Channels

The page lists roughly thirty supported channels, each with its underlying transport/API and packaging (bundled plugin, downloadable plugin, or separately/externally installed). The matrix below reproduces every entry verbatim from the source:

| Channel | Transport / API and notes |
|---|---|
| Discord | Discord Bot API + Gateway; supports servers, channels, and DMs. |
| Feishu | Feishu/Lark bot via WebSocket (bundled plugin). |
| Google Chat | Google Chat API app via HTTP webhook (downloadable plugin). |
| iMessage | Native macOS integration via the `imsg` bridge on a signed-in Mac (or SSH wrapper when the Gateway runs elsewhere), including private API actions for replies, tapbacks, effects, attachments, and group management. Preferred for new OpenClaw iMessage setups when host permissions and Messages access fit. |
| IRC | Classic IRC servers; channels + DMs with pairing/allowlist controls. |
| LINE | LINE Messaging API bot (downloadable plugin). |
| Matrix | Matrix protocol (downloadable plugin). |
| Mattermost | Bot API + WebSocket; channels, groups, DMs (downloadable plugin). |
| Microsoft Teams | Bot Framework; enterprise support (bundled plugin). |
| Nextcloud Talk | Self-hosted chat via Nextcloud Talk (bundled plugin). |
| Nostr | Decentralized DMs via NIP-04 (bundled plugin). |
| QQ Bot | QQ Bot API; private chat, group chat, and rich media (bundled plugin). |
| Signal | signal-cli; privacy-focused. |
| Slack | Bolt SDK; workspace apps. |
| SMS | Twilio-backed SMS through the Gateway webhook (bundled plugin). |
| Synology Chat | Synology NAS Chat via outgoing+incoming webhooks (bundled plugin). |
| Telegram | Bot API via grammY; supports groups. |
| Tlon | Urbit-based messenger (bundled plugin). |
| Twitch | Twitch chat via IRC connection (bundled plugin). |
| Voice Call | Telephony via Plivo or Twilio (plugin, installed separately). |
| WebChat | Gateway WebChat UI over WebSocket. |
| WeChat | Tencent iLink Bot plugin via QR login; private chats only (external plugin). |
| WhatsApp | Most popular; uses Baileys and requires QR pairing. |
| Yuanbao | Tencent Yuanbao bot (external plugin). |
| Zalo | Zalo Bot API; Vietnam's popular messenger (bundled plugin). |
| Zalo ClawBot | Personal Zalo assistant via QR login; owner-bound (external plugin). |
| Zalo Personal | Zalo personal account via QR login (bundled plugin). |

Transport patterns recur across the matrix: WebSocket-based channels (Feishu, Mattermost, WebChat) maintain a bidirectional connection; webhook-based channels (Google Chat, Synology Chat, SMS) receive inbound HTTP triggers; and several QR-login channels (WeChat, Zalo ClawBot, Zalo Personal) pair a personal account. Packaging spans bundled plugins (shipped with OpenClaw), downloadable plugins (Google Chat, LINE, Matrix, Mattermost), and separately/externally installed plugins (Voice Call, WeChat, Yuanbao, Zalo ClawBot).

## Notes

The page closes with operational guidance for choosing and running channels:

- **Simultaneous channels** — Channels can run simultaneously; configure multiple and OpenClaw will route per chat.
- **Fastest setup** — Fastest setup is usually **Telegram** (simple bot token). WhatsApp requires QR pairing and stores more state on disk.
- **Groups** — Group behavior varies by channel; see the Groups documentation.
- **DM pairing and allowlists** — DM pairing and allowlists are enforced for safety; see the gateway Security documentation.
- **Troubleshooting** — See the Channel troubleshooting documentation.
- **Model providers** — Model providers are documented separately; see Model Providers.

**Source**: OpenClaw documentation — `channels` (mirror `inbox/openclaw_docs/channels.md`)
**Last Updated**: 2026-06-22
**Status**: Active
