---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - matrix
keywords:
  - openclaw matrix channel setup
  - matrix plugin install clawhub
  - matrix accesstoken password auth
  - matrix interactive setup wizard
  - matrix autojoin allowlist invites
  - matrix allowlist target formats
  - matrix account id normalization
  - matrix cached credentials
  - matrix env vars
topics:
  - OpenClaw
  - Matrix Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/matrix
access_control_group: ["general"]
---

# OpenClaw — Installing and Configuring the Matrix Channel

## Overview

This note is the operator procedure for **installing and configuring the OpenClaw Matrix channel plugin** — the setup half of the `channels/matrix` source page. Matrix is a downloadable channel plugin that uses the official `matrix-js-sdk` and supports DMs, rooms, threads, media, reactions, polls, location, and E2EE. The procedure covers ClawHub plugin install, the two auth methods (`accessToken` vs `userId` + `password`), the interactive setup wizard, minimal token/password config, `autoJoin` invite gating, the stable `autoJoinAllowlist` / room / DM allowlist target formats, account-ID normalization for multi-account naming, on-disk cached credentials, and the `MATRIX_*` environment-variable matrix. Runtime message behavior (streaming, threads, reactions), the E2EE/verification command set, and the flat `channels.matrix` config-key reference are covered in sibling notes (see Related Notes).

## Install

Install Matrix from ClawHub before configuring the channel:

```bash
openclaw plugins install @openclaw/matrix
```

Bare plugin specs try ClawHub first, then npm fallback. To force the registry source, use `openclaw plugins install clawhub:@openclaw/matrix` or `openclaw plugins install npm:@openclaw/matrix`. To install from a local checkout, run `openclaw plugins install ./path/to/local/matrix-plugin`. `plugins install` registers AND enables the plugin, so no separate `openclaw plugins enable matrix` step is needed. The plugin still does nothing until you configure the channel below.

## Setup

The end-to-end setup is four steps:

1. Create a Matrix account on your homeserver.
2. Configure `channels.matrix` with either `homeserver` + `accessToken`, or `homeserver` + `userId` + `password`.
3. Restart the gateway.
4. Start a DM with the bot, or invite it to a room — fresh invites only land when `autoJoin` allows them (see Auto-join below).

### Interactive setup

```bash
openclaw channels add
openclaw configure --section channels
```

The wizard asks for: homeserver URL, auth method (access token or password), user ID (password auth only), optional device name, whether to enable E2EE, and whether to configure room access and auto-join. If matching `MATRIX_*` env vars already exist and the selected account has no saved auth, the wizard offers an env-var shortcut. To resolve room names before saving an allowlist, run `openclaw channels resolve --channel matrix "Project Room"`. When E2EE is enabled, the wizard writes the config and runs the same bootstrap as `openclaw matrix encryption setup` (see the encryption note).

### Minimal config

Token-based auth uses `homeserver` + `accessToken`:

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_xxx",
      dm: { policy: "pairing" },
    },
  },
}
```

Password-based auth uses `homeserver` + `userId` + `password` (the token is cached after first login):

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      userId: "@bot:example.org",
      password: "replace-me",
      deviceName: "OpenClaw Gateway",
    },
  },
}
```

## Auto-join

`channels.matrix.autoJoin` defaults to `off`. With the default, the bot will not appear in new rooms or DMs from fresh invites until you join manually. OpenClaw cannot tell at invite time whether an invited room is a DM or a group, so all invites — including DM-style invites — go through `autoJoin` first; `dm.policy` only applies later, after the bot has joined and the room has been classified.

Set `autoJoin: "allowlist"` plus `autoJoinAllowlist` to restrict which invites the bot accepts, or `autoJoin: "always"` to accept every invite. `autoJoinAllowlist` only accepts stable targets: `!roomId:server`, `#alias:server`, or `*`. Plain room names are rejected; alias entries are resolved against the homeserver, not against state claimed by the invited room.

```json5
{
  channels: {
    matrix: {
      autoJoin: "allowlist",
      autoJoinAllowlist: ["!ops:example.org", "#support:example.org"],
      groups: {
        "!ops:example.org": { requireMention: true },
      },
    },
  },
}
```

## Allowlist target formats

DM and room allowlists are best populated with stable IDs:

- DMs (`dm.allowFrom`, `groupAllowFrom`, `groups.<room>.users`): use `@user:server`. Display names are ignored by default because they are mutable; set `dangerouslyAllowNameMatching: true` only when you explicitly need compatibility with display-name entries.
- Room allowlist keys (`groups`, legacy `rooms`): use `!room:server` or `#alias:server`. Plain room names are ignored by default; set `dangerouslyAllowNameMatching: true` only when you explicitly need compatibility with joined-room name lookup.
- Invite allowlists (`autoJoinAllowlist`): use `!room:server`, `#alias:server`, or `*`. Plain room names are rejected.

## Account ID normalization

The wizard converts a friendly name into a normalized account ID. For example, `Ops Bot` becomes `ops-bot`. Punctuation is escaped in scoped env-var names so that two accounts cannot collide: `-` → `_X2D_`, so `ops-prod` maps to `MATRIX_OPS_X2D_PROD_*`.

## Cached credentials

Matrix stores cached credentials under `~/.openclaw/credentials/matrix/`:

- default account: `credentials.json`
- named accounts: `credentials-<account>.json`

When cached credentials exist there, OpenClaw treats Matrix as configured even if the access token is not in the config file — that covers setup, `openclaw doctor`, and channel-status probes.

## Environment variables

Environment variables are used when the equivalent config key is not set. The default account uses unprefixed names; named accounts insert the normalized account ID before the suffix.

| Default account       | Named account (`<ID>` is the normalized account ID) |
| --------------------- | --------------------------------------------------- |
| `MATRIX_HOMESERVER`   | `MATRIX_<ID>_HOMESERVER`                            |
| `MATRIX_ACCESS_TOKEN` | `MATRIX_<ID>_ACCESS_TOKEN`                          |
| `MATRIX_USER_ID`      | `MATRIX_<ID>_USER_ID`                               |
| `MATRIX_PASSWORD`     | `MATRIX_<ID>_PASSWORD`                              |
| `MATRIX_DEVICE_ID`    | `MATRIX_<ID>_DEVICE_ID`                             |
| `MATRIX_DEVICE_NAME`  | `MATRIX_<ID>_DEVICE_NAME`                           |
| `MATRIX_RECOVERY_KEY` | `MATRIX_<ID>_RECOVERY_KEY`                          |

For account `ops`, the names become `MATRIX_OPS_HOMESERVER`, `MATRIX_OPS_ACCESS_TOKEN`, and so on. The recovery-key env vars are read by recovery-aware CLI flows (`verify backup restore`, `verify device`, `verify bootstrap`) when you pipe the key in via `--recovery-key-stdin`. `MATRIX_HOMESERVER` cannot be set from a workspace `.env` (see the Workspace `.env` files note under gateway security).

**Source**: OpenClaw documentation — `channels/matrix` (mirror `inbox/openclaw_docs/channels/matrix.md`), Install / Setup / Interactive setup / Minimal config / Auto-join / Allowlist target formats / Account ID normalization / Cached credentials / Environment variables sections
**Last Updated**: 2026-06-22
**Status**: Active
