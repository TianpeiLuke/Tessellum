---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - tlon
keywords:
  - openclaw tlon channel
  - urbit ship setup
  - channels.tlon config
  - dmAllowlist ownerShip approval
  - allowPrivateNetwork ssrf
  - autoAcceptGroupInvites groupInviteAllowlist
  - tlon delivery targets cli cron
  - tloncorp tlon-skill bundled
topics:
  - OpenClaw
  - Channels
  - Tlon
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/tlon
access_control_group: ["general"]
---

# OpenClaw — Configuring the Tlon (Urbit) Channel

## Overview

This note is the setup-and-configuration procedure for the OpenClaw **Tlon** channel — a decentralized messenger built on Urbit. OpenClaw connects to your Urbit ship and can respond to DMs and group chat messages, where group replies require an `@` mention by default and can be further restricted via allowlists. It mirrors the `channels/tlon` source page: the bundled plugin, ship setup (including private/LAN ships), group channels, access control, the owner/approval and auto-accept system, CLI/cron delivery targets, the bundled skill, the capabilities matrix, troubleshooting, and the full `channels.tlon.*` configuration reference. Status: bundled plugin; DMs, group mentions, thread replies, rich text formatting, and image uploads are supported, while polls are not yet supported.

## Bundled plugin

Tlon ships as a bundled plugin in current OpenClaw releases, so normal packaged builds do not need a separate install. If you are on an older build or a custom install that excludes Tlon, install a current npm package via the CLI against the npm registry, or install a local checkout when running from a git repo:

```bash
openclaw plugins install @openclaw/tlon
openclaw plugins install ./path/to/local/tlon-plugin
```

Use the bare package to follow the current official release tag; pin an exact version only when you need a reproducible install.

## Setup

The setup flow is: (1) ensure the Tlon plugin is available — current packaged OpenClaw releases already bundle it, and older/custom installs add it with the commands above; (2) gather your ship URL and login code; (3) configure `channels.tlon`; (4) restart the gateway; (5) DM the bot or mention it in a group channel. The minimal single-account config is:

```json5
{
  channels: {
    tlon: {
      enabled: true,
      ship: "~sampel-palnet",
      url: "https://your-ship-host",
      code: "lidlut-tabwed-pillex-ridrup",
      ownerShip: "~your-main-ship", // recommended: your ship, always allowed
    },
  },
}
```

## Private/LAN ships

By default, OpenClaw blocks private/internal hostnames and IP ranges for SSRF protection. If your ship runs on a private network (localhost, LAN IP, or internal hostname), you must explicitly opt in with `allowPrivateNetwork: true`:

```json5
{
  channels: {
    tlon: {
      url: "http://localhost:8080",
      allowPrivateNetwork: true,
    },
  },
}
```

This applies to URLs like `http://localhost:8080`, `http://192.168.x.x:8080`, and `http://my-ship.local:8080`. The source warns: only enable this if you trust your local network, because the setting disables SSRF protections for requests to your ship URL.

## Group channels

Auto-discovery is enabled by default. You can also pin channels manually via `groupChannels`, or disable auto-discovery via `autoDiscoverChannels: false`:

```json5
{
  channels: {
    tlon: {
      groupChannels: ["chat/~host-ship/general", "chat/~host-ship/support"],
      autoDiscoverChannels: false,
    },
  },
}
```

## Access control

The DM allowlist (`dmAllowlist`) lists ships allowed to DM the bot; an empty allowlist means no DMs are allowed (use `ownerShip` for the approval flow). Group channels are restricted by default: `defaultAuthorizedShips` lists ships authorized for all channels, and `authorization.channelRules` sets per-channel rules with `mode: "restricted"` (plus `allowedShips`) or `mode: "open"`:

```json5
{
  channels: {
    tlon: {
      dmAllowlist: ["~zod", "~nec"],
      defaultAuthorizedShips: ["~zod"],
      authorization: {
        channelRules: {
          "chat/~host-ship/general": {
            mode: "restricted",
            allowedShips: ["~zod", "~nec"],
          },
          "chat/~host-ship/announcements": {
            mode: "open",
          },
        },
      },
    },
  },
}
```

## Owner and approval system

Set an owner ship via `ownerShip` to receive approval requests when unauthorized users try to interact. The owner ship is **automatically authorized everywhere** — DM invites are auto-accepted and channel messages are always allowed — so you do not need to add the owner to `dmAllowlist` or `defaultAuthorizedShips`. When set, the owner receives DM notifications for: DM requests from ships not in the allowlist, mentions in channels without authorization, and group invite requests.

## Auto-accept settings

Setting `channels.tlon.autoAcceptDmInvites: true` auto-accepts DM invites for ships in `dmAllowlist`. For group invites, `channels.tlon.autoAcceptGroupInvites: true` auto-accepts invites from trusted ships, gated by `channels.tlon.groupInviteAllowlist` (e.g. `["~zod"]`). `autoAcceptGroupInvites` fails closed when `groupInviteAllowlist` is empty — set the allowlist to the ships whose group invites should be accepted automatically.

## Delivery targets (CLI/cron)

Use these targets with `openclaw message send` or cron delivery. For a DM, use `~sampel-palnet` or `dm/~sampel-palnet`. For a group, use `chat/~host-ship/channel` or `group:~host-ship/channel`.

## Bundled skill

The Tlon plugin includes a bundled skill (`@tloncorp/tlon-skill`) that provides CLI access to Tlon operations: **Contacts** (get/update profiles, list contacts), **Channels** (list, create, post messages, fetch history), **Groups** (list, create, manage members), **DMs** (send messages, react to messages), **Reactions** (add/remove emoji reactions to posts and DMs), and **Settings** (manage plugin permissions via slash commands). The skill is automatically available when the plugin is installed.

## Capabilities

| Feature | Status |
| --- | --- |
| Direct messages | Supported |
| Groups/channels | Supported (mention-gated by default) |
| Threads | Supported (auto-replies in thread) |
| Rich text | Markdown converted to Tlon format |
| Images | Uploaded to Tlon storage |
| Reactions | Via bundled skill |
| Polls | Not yet supported |
| Native commands | Supported (owner-only by default) |

## Troubleshooting

Run this diagnostic ladder first:

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
```

Common failures and fixes: **DMs ignored** — sender not in `dmAllowlist` and no `ownerShip` configured for the approval flow; **Group messages ignored** — channel not discovered or sender not authorized; **Connection errors** — check the ship URL is reachable and enable `allowPrivateNetwork` for local ships; **Auth errors** — verify the login code is current (codes rotate).

## Configuration reference

Full configuration lives at the gateway Configuration page. The Tlon provider options are: `channels.tlon.enabled` (enable/disable channel startup); `channels.tlon.ship` (bot's Urbit ship name, e.g. `~sampel-palnet`); `channels.tlon.url` (ship URL, e.g. `https://sampel-palnet.tlon.network`); `channels.tlon.code` (ship login code); `channels.tlon.allowPrivateNetwork` (allow localhost/LAN URLs, SSRF bypass); `channels.tlon.ownerShip` (owner ship for the approval system, always authorized); `channels.tlon.dmAllowlist` (ships allowed to DM, empty = none); `channels.tlon.autoAcceptDmInvites` (auto-accept DMs from allowlisted ships); `channels.tlon.autoAcceptGroupInvites` (auto-accept group invites from allowlisted ships); `channels.tlon.groupInviteAllowlist` (ships whose group invites may be auto-accepted); `channels.tlon.autoDiscoverChannels` (auto-discover group channels, default: true); `channels.tlon.groupChannels` (manually pinned channel nests); `channels.tlon.defaultAuthorizedShips` (ships authorized for all channels); `channels.tlon.authorization.channelRules` (per-channel auth rules); and `channels.tlon.showModelSignature` (append model name to messages).

## Notes

Group replies require a mention (e.g. `~your-bot-ship`) to respond. Thread replies: if the inbound message is in a thread, OpenClaw replies in-thread. Rich text: Markdown formatting (bold, italic, code, headers, lists) is converted to Tlon's native format. Images: URLs are uploaded to Tlon storage and embedded as image blocks.

**Source**: OpenClaw documentation — `channels/tlon` (mirror `inbox/openclaw_docs/channels/tlon.md`)
**Last Updated**: 2026-06-22
**Status**: Active
