---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - zalouser
keywords:
  - openclaw zalouser channel
  - zalo personal account zca-js
  - zalouser qr login pairing
  - zalouser dmpolicy allowfrom id-only
  - dangerouslyallownamematching break-glass
  - zalouser group requireMention gating
  - zalouser multi-account profile
  - zalouser_profile zca_profile env vars
  - openclaw directory peers groups
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/zalouser
access_control_group: ["general"]
---

# OpenClaw — Automating a Personal Zalo Account (`zalouser`)

## Overview

This note is the procedure for the OpenClaw **Zalo Personal** channel (`zalouser`) — an experimental, unofficial integration that automates a **personal Zalo user account** in-process via the native `zca-js` library inside OpenClaw. It mirrors the `channels/zalouser` source page: the bundled-plugin status (and manual npm install fallback), the beginner QR-login quick setup, what the integration is and why the channel id is `zalouser`, discovering peer/group IDs with the directory CLI, the chunking/streaming limits, ID-only DM and group access control with the `dangerouslyAllowNameMatching` break-glass, group mention gating, profile-based multi-account setup with environment-variable profile resolution, typing/reaction/acknowledgement behavior, and troubleshooting. The source flags this as **Status: experimental** and warns that it is an unofficial integration that may result in account suspension or ban — use at your own risk.

## Bundled plugin

Zalo Personal ships as a **bundled plugin** in current OpenClaw releases, so normal packaged builds do not need a separate install. On an older build or a custom install that excludes Zalo Personal, install the npm package directly: install via CLI with `openclaw plugins install @openclaw/zalouser`, pin a version with `openclaw plugins install @openclaw/zalouser@2026.5.2`, or install from a source checkout with `openclaw plugins install ./path/to/local/zalouser-plugin`. Plugin details are at `/tools/plugin`. No external `zca`/`openzca` CLI binary is required.

## Quick setup (beginner)

The fastest path: (1) ensure the Zalo Personal plugin is available — current packaged OpenClaw releases already bundle it, and older/custom installs can add it manually with the commands above; (2) log in via QR on the Gateway machine with `openclaw channels login --channel zalouser` and scan the QR code with the Zalo mobile app; (3) enable the channel with the config below; (4) restart the Gateway (or finish setup); (5) DM access defaults to pairing, so approve the pairing code on first contact. The minimal enable config:

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

## What it is

The integration runs entirely in-process via `zca-js`, uses native event listeners to receive inbound messages, and sends replies directly through the JS API (text/media/link). It is designed for "personal account" use cases where the official Zalo Bot API is not available.

## Naming

The channel id is `zalouser` to make it explicit that this automates a **personal Zalo user account** (unofficial). The id `zalo` is kept reserved for a potential future official Zalo API integration (documented in the sibling `oc_channels_zalo` note).

## Finding IDs (directory)

Use the directory CLI to discover peers/groups and their IDs — needed because access control is ID-only (see below). The source documents these commands:

```bash
openclaw directory self --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory groups list --channel zalouser --query "work"
```

## Limits

Outbound text is chunked to ~**2000 characters** (Zalo client limits). Streaming is **blocked by default**.

## Access control (DMs)

`channels.zalouser.dmPolicy` supports `pairing | allowlist | open | disabled` (default `pairing`). `channels.zalouser.allowFrom` should use **stable Zalo user IDs**; it can also reference static sender access groups with `accessGroup:<name>`. During interactive setup, entered names can be resolved to IDs using the plugin's in-process contact lookup. If a raw name remains in config, startup resolves it only when `channels.zalouser.dangerouslyAllowNameMatching: true` is enabled — without that opt-in, runtime sender checks are **ID-only** and raw names are ignored for authorization. Approve pairing requests via `openclaw pairing list zalouser` then `openclaw pairing approve zalouser <code>`.

## Group access (optional)

The default is `channels.zalouser.groupPolicy = "open"` (groups allowed); use `channels.defaults.groupPolicy` to override the default when unset. To restrict to an allowlist, set `channels.zalouser.groupPolicy = "allowlist"`, list allowed groups under `channels.zalouser.groups` (keys should be stable group IDs; names are resolved to IDs on startup only when `dangerouslyAllowNameMatching: true`), and control which senders in allowed groups can trigger the bot with `channels.zalouser.groupAllowFrom` (static sender access groups can be referenced with `accessGroup:<name>`). Set `groupPolicy = "disabled"` to block all groups. The configure wizard can prompt for group allowlists.

On startup, OpenClaw resolves group/user names in allowlists to IDs and logs the mapping only when `dangerouslyAllowNameMatching: true` is enabled. Group allowlist matching is **ID-only by default**; unresolved names are ignored for auth unless that flag is enabled. `channels.zalouser.dangerouslyAllowNameMatching: true` is a **break-glass compatibility mode** that re-enables mutable startup name resolution and runtime group-name matching. If `groupAllowFrom` is unset, runtime falls back to `allowFrom` for group sender checks. Sender checks apply to both normal group messages and control commands (for example `/new`, `/reset`). Example:

```json5
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["1471383327500481391"],
      groups: {
        "123456789": { allow: true },
        "Work Chat": { allow: true },
      },
    },
  },
}
```

### Group mention gating

`channels.zalouser.groups.<group>.requireMention` controls whether group replies require a mention. The resolution order is: exact group id/name -> normalized group slug -> `*` -> default (`true`). This applies both to allowlisted groups and open group mode. Quoting a bot message counts as an **implicit mention** for group activation, and authorized control commands (for example `/new`) can bypass mention gating. When a group message is skipped because mention is required, OpenClaw stores it as pending group history and includes it on the next processed group message. The group history limit defaults to `messages.groupChat.historyLimit` (fallback `50`); override per account with `channels.zalouser.historyLimit`. Example:

```json5
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groups: {
        "*": { allow: true, requireMention: true },
        "Work Chat": { allow: true, requireMention: false },
      },
    },
  },
}
```

## Multi-account

Accounts map to `zalouser` profiles in OpenClaw state. Example:

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      defaultAccount: "default",
      accounts: {
        work: { enabled: true, profile: "work" },
      },
    },
  },
}
```

## Environment variables

The Zalo Personal plugin can also read profile selection from environment variables: `ZALOUSER_PROFILE` is the profile name to use when no `profile` is set in channel or account config, and `ZCA_PROFILE` is a **legacy fallback** profile name, used only when `ZALOUSER_PROFILE` is not set. Profile names select the saved Zalo login credentials in OpenClaw state. The resolution order is: (1) explicit `profile` in config; (2) `ZALOUSER_PROFILE`; (3) `ZCA_PROFILE`; (4) the account id for non-default accounts, or `default` for the default account. For multi-account setups, prefer setting `profile` on each account in config so one environment variable does not make multiple accounts share the same login session.

## Typing, reactions, and delivery acknowledgements

OpenClaw sends a typing event before dispatching a reply (best-effort). The message reaction action `react` is supported for `zalouser` in channel actions, and `remove: true` removes a specific reaction emoji from a message (reaction semantics are documented at `/tools/reactions`). For inbound messages that include event metadata, OpenClaw sends delivered + seen acknowledgements (best-effort).

## Troubleshooting

**Login doesn't stick:** run `openclaw channels status --probe`, then re-login with `openclaw channels logout --channel zalouser && openclaw channels login --channel zalouser`.

**Allowlist/group name didn't resolve:** use numeric IDs in `allowFrom`/`groupAllowFrom` and stable group IDs in `groups`. If you intentionally need exact friend/group names, enable `channels.zalouser.dangerouslyAllowNameMatching: true`.

**Upgraded from old CLI-based setup:** remove any old external `zca` process assumptions — the channel now runs fully in OpenClaw without external CLI binaries.

**Source**: OpenClaw documentation — `channels/zalouser` (mirror `inbox/openclaw_docs/channels/zalouser.md`)
**Last Updated**: 2026-06-22
**Status**: Active
