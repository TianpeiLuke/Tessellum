---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - irc
keywords:
  - openclaw irc channel
  - channels.irc config
  - irc grouppolicy allowlist
  - irc allowfrom gotcha
  - irc mention gating requireMention
  - irc toolsbysender per-channel tools
  - nickserv identify register
  - irc environment variables
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/irc
access_control_group: ["general"]
---

# OpenClaw — Connecting IRC Channels and DMs

## Overview

This note is the procedure for connecting OpenClaw to IRC — classic channels (`#room`) and direct messages — mirroring the `channels/irc` source page. IRC ships as a bundled plugin but is configured in the main config under `channels.irc`. The procedure covers the quick-start config block, the IRC-specific security defaults, the two-gate access-control model (channel access vs sender access) plus the `allowFrom` DM-vs-channel gotcha, mention-gating reply triggering, public-channel tool hardening, NickServ identify/register, the supported environment variables, and troubleshooting. Full channel field semantics that overlap with other surfaces live in the Groups page (linked); this note reproduces only the load-bearing IRC config snippets verbatim.

## Quick start

1. Enable IRC config in `~/.openclaw/openclaw.json`.
2. Set at least `enabled`, `host`, `port`, `tls`, `nick`, and `channels`:

```json5
{
  channels: {
    irc: {
      enabled: true,
      host: "irc.example.com",
      port: 6697,
      tls: true,
      nick: "openclaw-bot",
      channels: ["#openclaw"],
    },
  },
}
```

3. Start/restart the gateway with `openclaw gateway run`.

Prefer a private IRC server for bot coordination. If you intentionally use a public IRC network, common choices include Libera.Chat, OFTC, and Snoonet. Avoid predictable public channels for bot or swarm backchannel traffic.

## Security defaults

- IRC uses raw TCP/TLS sockets **outside** OpenClaw's operator-managed forward proxy routing. In deployments that require all egress through that forward proxy, set `channels.irc.enabled=false` unless direct IRC egress is explicitly approved.
- `channels.irc.dmPolicy` defaults to `"pairing"`.
- `channels.irc.groupPolicy` defaults to `"allowlist"`.
- With `groupPolicy="allowlist"`, set `channels.irc.groups` to define allowed channels.
- Use TLS (`channels.irc.tls=true`) unless you intentionally accept plaintext transport.

## Access control

There are two separate "gates" for IRC channels:

1. **Channel access** (`groupPolicy` + `groups`): whether the bot accepts messages from a channel at all.
2. **Sender access** (`groupAllowFrom` / per-channel `groups["#channel"].allowFrom`): who is allowed to trigger the bot inside that channel.

The relevant config keys are: `channels.irc.allowFrom` (DM sender access — the DM allowlist); `channels.irc.groupAllowFrom` (channel sender access — the group sender allowlist); `channels.irc.groups["#channel"]` (per-channel controls: channel + sender + mention rules); and `channels.irc.groupPolicy="open"`, which allows unconfigured channels but leaves them **still mention-gated by default**.

Allowlist entries should use stable sender identities (`nick!user@host`). Bare nick matching is mutable and only enabled when `channels.irc.dangerouslyAllowNameMatching: true`.

### Common gotcha: `allowFrom` is for DMs, not channels

If you see a log like `irc: drop group sender alice!ident@host (policy=allowlist)`, it means the sender was not allowed for **group/channel** messages. Fix it by either setting `channels.irc.groupAllowFrom` (global for all channels) or setting a per-channel sender allowlist at `channels.irc.groups["#channel"].allowFrom`. For example, to allow anyone in `#tuirc-dev` to talk to the bot:

```json5
{
  channels: {
    irc: {
      groupPolicy: "allowlist",
      groups: {
        "#tuirc-dev": { allowFrom: ["*"] },
      },
    },
  },
}
```

## Reply triggering (mentions)

Even if a channel is allowed (via `groupPolicy` + `groups`) and the sender is allowed, OpenClaw defaults to **mention-gating** in group contexts. That means you may see logs like `drop channel … (missing-mention)` unless the message includes a mention pattern that matches the bot.

To make the bot reply in an IRC channel **without** needing a mention, disable mention gating for that channel with `requireMention: false`:

```json5
{
  channels: {
    irc: {
      groupPolicy: "allowlist",
      groups: {
        "#tuirc-dev": {
          requireMention: false,
          allowFrom: ["*"],
        },
      },
    },
  },
}
```

To allow **all** IRC channels (no per-channel allowlist) and still reply without mentions, use `groupPolicy: "open"` with a `"*"` wildcard group entry: `groups: { "*": { requireMention: false, allowFrom: ["*"] } }`.

## Security note (recommended for public channels)

If you allow `allowFrom: ["*"]` in a public channel, anyone can prompt the bot. To reduce risk, restrict tools for that channel. The simplest form applies the **same tools for everyone** in the channel via a `tools.deny` list:

```json5
{
  channels: {
    irc: {
      groups: {
        "#tuirc-dev": {
          allowFrom: ["*"],
          tools: {
            deny: ["group:runtime", "group:fs", "gateway", "nodes", "cron", "browser"],
          },
        },
      },
    },
  },
}
```

To grant **different tools per sender** (owner gets more power), use `toolsBySender` to apply a stricter policy to `"*"` and a looser one to your nick:

```json5
{
  channels: {
    irc: {
      groups: {
        "#tuirc-dev": {
          allowFrom: ["*"],
          toolsBySender: {
            "*": {
              deny: ["group:runtime", "group:fs", "gateway", "nodes", "cron", "browser"],
            },
            "id:eigen": {
              deny: ["gateway", "nodes", "cron"],
            },
          },
        },
      },
    },
  },
}
```

`toolsBySender` keys should use `id:` for IRC sender identity values: `id:eigen`, or `id:eigen!~eigen@174.127.248.171` for stronger matching. Legacy unprefixed keys are still accepted and matched as `id:` only. The first matching sender policy wins; `"*"` is the wildcard fallback. For more on group access vs mention-gating (and how they interact), see the Groups page (`oc_channels_groups_policy`).

## NickServ

To identify with NickServ after connect, set `channels.irc.nickserv` with `enabled: true`, a `service` (e.g. `"NickServ"`), and a `password`. An optional one-time registration on connect uses `register: true` with a `registerEmail`. Disable `register` after the nick is registered to avoid repeated REGISTER attempts.

```json5
{
  channels: {
    irc: {
      nickserv: {
        enabled: true,
        service: "NickServ",
        password: "your-nickserv-password",
        register: true,
        registerEmail: "bot@example.com",
      },
    },
  },
}
```

## Environment variables

The default account supports these environment variables: `IRC_HOST`, `IRC_PORT`, `IRC_TLS`, `IRC_NICK`, `IRC_USERNAME`, `IRC_REALNAME`, `IRC_PASSWORD`, `IRC_CHANNELS` (comma-separated), `IRC_NICKSERV_PASSWORD`, and `IRC_NICKSERV_REGISTER_EMAIL`. Note that `IRC_HOST` **cannot** be set from a workspace `.env`; see Workspace `.env` files under `/gateway/security`.

## Troubleshooting

- If the bot connects but never replies in channels, verify `channels.irc.groups` **and** whether mention-gating is dropping messages (`missing-mention`). If you want it to reply without pings, set `requireMention: false` for the channel.
- If login fails, verify nick availability and the server password.
- If TLS fails on a custom network, verify host/port and certificate setup.

**Source**: OpenClaw documentation — `channels/irc` (mirror `inbox/openclaw_docs/channels/irc.md`)
**Last Updated**: 2026-06-22
**Status**: Active
