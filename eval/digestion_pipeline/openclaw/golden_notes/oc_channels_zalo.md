---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - zalo
keywords:
  - openclaw zalo channel
  - zalo bot api marketplace bot
  - zalo dmpolicy pairing
  - zalo long-polling vs webhook
  - zalo webhooksecret x-bot-api-secret-token
  - zalo grouppolicy allowlist marketplace
  - zalo capabilities matrix
  - zalo accounts botToken tokenFile
  - openclaw message send channel zalo
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/zalo
access_control_group: ["general"]
---

# OpenClaw — Connecting the Zalo Bot API Channel

## Overview

This note is the procedure for configuring the OpenClaw **Zalo Bot API** channel — a Gateway-owned channel that runs a Zalo bot for 1:1 conversations using Zalo Bot Creator / Marketplace bots. It mirrors the `channels/zalo` source page: the bundled-plugin status (and manual npm install fallback), the beginner and fast-path bot-token setup, the deterministic inbound→reply behavior, the 2000-character / media-cap limits, DM pairing and the group-policy schema (groups unavailable in practice for Marketplace bots), long-polling vs webhook ingress, the supported-message-types and Marketplace-bot capability matrix, CLI/cron delivery targets, troubleshooting, and the legacy-flat-key-vs-`accounts.<id>` configuration reference. The page is marked **Status: experimental** with DMs supported.

## Bundled plugin

Zalo ships as a **bundled plugin** in current OpenClaw releases, so normal packaged builds do not need a separate install. On an older build or a custom install that excludes Zalo, install the npm package directly: install via CLI with `openclaw plugins install @openclaw/zalo`, pin a version with `openclaw plugins install @openclaw/zalo@2026.5.2`, or install from a source checkout with `openclaw plugins install ./path/to/local/zalo-plugin`. The source links plugin details to `/tools/plugin`.

## Quick setup (beginner)

The fastest path: (1) ensure the Zalo plugin is available — current packaged OpenClaw releases already bundle it, and older/custom installs can add it manually with the commands above; (2) set the token, either via env `ZALO_BOT_TOKEN=...` or via config `channels.zalo.accounts.default.botToken: "..."`; (3) restart the gateway (or finish setup); (4) DM access is `pairing` by default, so approve the pairing code on first contact. The minimal config:

```json5
{
  channels: {
    zalo: {
      enabled: true,
      accounts: {
        default: {
          botToken: "12345689:abc-xyz",
          dmPolicy: "pairing",
        },
      },
    },
  },
}
```

## What it is

Zalo is a Vietnam-focused messaging app whose Bot API lets the Gateway run a bot for 1:1 conversations — a good fit for support or notifications where you want **deterministic routing back to Zalo**. The page reflects current OpenClaw behavior for **Zalo Bot Creator / Marketplace bots**; **Zalo Official Account (OA) bots** are a different Zalo product surface and may behave differently. The channel is a Zalo Bot API channel owned by the Gateway, routing is deterministic (replies go back to Zalo; the model never chooses channels), DMs share the agent's main session, and the Capabilities section shows current Marketplace-bot support.

## Setup (fast path)

**1) Create a bot token (Zalo Bot Platform).** Go to `https://bot.zaloplatforms.com` and sign in, create a new bot and configure its settings, then copy the full bot token (typically `numeric_id:secret`). For Marketplace bots, the usable runtime token may appear in the bot's welcome message after creation.

**2) Configure the token (env or config).** Use the same `channels.zalo.accounts.default` shape shown in Quick setup, with `botToken` and `dmPolicy: "pairing"`. If you later move to a Zalo bot surface where groups are available, you can add group-specific config such as `groupPolicy` and `groupAllowFrom` explicitly; for current Marketplace-bot behavior, see Capabilities. The env option `ZALO_BOT_TOKEN=...` works for the default account only. Multi-account support uses `channels.zalo.accounts` with per-account tokens and an optional `name`. Then restart the gateway — Zalo starts when a token is resolved (env or config) — and approve the pairing code when the bot is first contacted (DM access defaults to pairing).

## How it works (behavior)

Inbound messages are normalized into the shared channel envelope with media placeholders. Replies always route back to the same Zalo chat. The channel uses long-polling by default, with webhook mode available by setting `channels.zalo.webhookUrl`.

## Limits

Outbound text is chunked to **2000 characters** (the Zalo API limit). Media downloads/uploads are capped by `channels.zalo.mediaMaxMb` (default **5**). Streaming is **blocked by default** because the 2000-character limit makes streaming less useful.

## Access control (DMs)

The default is `channels.zalo.dmPolicy = "pairing"`: unknown senders receive a pairing code and their messages are ignored until approved (codes expire after **1 hour**). Approve via `openclaw pairing list zalo` then `openclaw pairing approve zalo <CODE>`. Pairing is the default token exchange (details at `/channels/pairing`). The `channels.zalo.allowFrom` list accepts **numeric user IDs** only — no username lookup is available.

## Access control (Groups)

For **Zalo Bot Creator / Marketplace bots**, group support was **not available in practice** because the bot could not be added to a group at all. The group-related config keys therefore exist in the schema but were not usable for Marketplace bots: `channels.zalo.groupPolicy` controls group inbound handling (`open | allowlist | disabled`); `channels.zalo.groupAllowFrom` restricts which sender IDs can trigger the bot in groups; if `groupAllowFrom` is unset, Zalo falls back to `allowFrom` for sender checks; and as a runtime note, if `channels.zalo` is missing entirely, runtime still falls back to `groupPolicy="allowlist"` for safety.

When group access is available on a bot surface, the group policy values are: `groupPolicy: "disabled"` blocks all group messages; `groupPolicy: "open"` allows any group member (mention-gated); and `groupPolicy: "allowlist"` is the fail-closed default where only allowed senders are accepted. If you use a different Zalo bot product surface and have verified working group behavior, document that separately rather than assuming it matches the Marketplace-bot flow.

## Long-polling vs webhook

The default is long-polling (no public URL required). Webhook mode is enabled by setting `channels.zalo.webhookUrl` and `channels.zalo.webhookSecret`, with these constraints: the webhook secret must be **8-256 characters**; the webhook URL must use **HTTPS**; Zalo sends events with an `X-Bot-Api-Secret-Token` header for verification; the Gateway HTTP server handles webhook requests at `channels.zalo.webhookPath` (defaults to the webhook URL path); requests must use `Content-Type: application/json` (or `+json` media types); duplicate events (`event_name + message_id`) are ignored for a short replay window; and burst traffic is rate-limited per path/source and may return **HTTP 429**. Note that `getUpdates` (polling) and webhook are **mutually exclusive** per Zalo API docs.

## Supported message types

For a quick support snapshot, see the Capabilities matrix below; these notes add detail where behavior needs extra context. **Text messages** have full support with 2000-character chunking. **Plain URLs in text** behave like normal text input. **Link previews / rich link cards** did not reliably trigger a reply (see Capabilities). **Image messages** had unreliable inbound handling — a typing indicator without a final reply (see Capabilities). **Stickers** and **voice notes / audio files / video / generic file attachments** reflect the Marketplace-bot status in Capabilities. **Unsupported types** are logged (for example, messages from protected users).

## Capabilities

This table summarizes current **Zalo Bot Creator / Marketplace bot** behavior in OpenClaw, copied verbatim from the source page:

| Feature                     | Status                                  |
| --------------------------- | --------------------------------------- |
| Direct messages             | ✅ Supported                            |
| Groups                      | ❌ Not available for Marketplace bots   |
| Media (inbound images)      | ⚠️ Limited / verify in your environment |
| Media (outbound images)     | ⚠️ Not re-tested for Marketplace bots   |
| Plain URLs in text          | ✅ Supported                            |
| Link previews               | ⚠️ Unreliable for Marketplace bots      |
| Reactions                   | ❌ Not supported                        |
| Stickers                    | ⚠️ No agent reply for Marketplace bots  |
| Voice notes / audio / video | ⚠️ No agent reply for Marketplace bots  |
| File attachments            | ⚠️ No agent reply for Marketplace bots  |
| Threads                     | ❌ Not supported                        |
| Polls                       | ❌ Not supported                        |
| Native commands             | ❌ Not supported                        |
| Streaming                   | ⚠️ Blocked (2000 char limit)            |

## Delivery targets (CLI/cron)

Use a chat id as the target. Example: `openclaw message send --channel zalo --target 123456789 --message "hi"`.

## Troubleshooting

**Bot doesn't respond:** check that the token is valid with `openclaw channels status --probe`; verify the sender is approved (pairing or `allowFrom`); and check gateway logs with `openclaw logs --follow`.

**Webhook not receiving events:** ensure the webhook URL uses HTTPS; verify the secret token is 8-256 characters; confirm the gateway HTTP endpoint is reachable on the configured path; and check that `getUpdates` polling is not running (they are mutually exclusive).

## Configuration reference (Zalo)

The full configuration reference lives at `/gateway/configuration`. The flat top-level keys (`channels.zalo.botToken`, `channels.zalo.dmPolicy`, and similar) are a **legacy single-account shorthand**; prefer `channels.zalo.accounts.<id>.*` for new configs. Both forms are documented because both exist in the schema.

Provider options (flat / single-account): `channels.zalo.enabled` enables/disables channel startup; `channels.zalo.botToken` is the bot token from Zalo Bot Platform; `channels.zalo.tokenFile` reads the token from a regular file path (symlinks are rejected); `channels.zalo.dmPolicy` is `pairing | allowlist | open | disabled` (default `pairing`); `channels.zalo.allowFrom` is the DM allowlist of user IDs, where `open` requires `"*"` and the wizard asks for numeric IDs; `channels.zalo.groupPolicy` is `open | allowlist | disabled` (default `allowlist`, present in config — see Capabilities and Access control (Groups) for Marketplace-bot behavior); `channels.zalo.groupAllowFrom` is the group sender allowlist of user IDs and falls back to `allowFrom` when unset; `channels.zalo.mediaMaxMb` is the inbound/outbound media cap in MB (default 5); `channels.zalo.webhookUrl` enables webhook mode (HTTPS required); `channels.zalo.webhookSecret` is the webhook secret (8-256 chars); `channels.zalo.webhookPath` is the webhook path on the gateway HTTP server; and `channels.zalo.proxy` is a proxy URL for API requests.

Multi-account options mirror these per account: `channels.zalo.accounts.<id>.botToken` (per-account token), `.tokenFile` (per-account regular token file, symlinks rejected), `.name` (display name), `.enabled` (enable/disable account), `.dmPolicy` (per-account DM policy), `.allowFrom` (per-account allowlist), `.groupPolicy` (per-account group policy, present in config), `.groupAllowFrom` (per-account group sender allowlist), `.webhookUrl`, `.webhookSecret`, `.webhookPath` (per-account webhook URL/secret/path), and `.proxy` (per-account proxy URL).

**Source**: OpenClaw documentation — `channels/zalo` (mirror `inbox/openclaw_docs/channels/zalo.md`)
**Last Updated**: 2026-06-22
**Status**: Active
