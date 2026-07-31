---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - directory
keywords:
  - openclaw directory command
  - channel contacts peers lookup
  - directory self peers groups
  - message send target id
  - per-channel id formats
  - config-backed directory results
  - directory json output
  - channel directory adapter
topics:
  - OpenClaw
  - CLI Directory
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/directory
access_control_group: ["general"]
---

# OpenClaw — `openclaw directory` Channel Lookup Command

## Overview

This note documents the `openclaw directory` CLI command — the operator procedure for looking up channel contacts/peers, groups, and "me" (self) for any messaging channel that supports directory lookups, mirroring the `cli/directory` source page. Its purpose is to help an operator find the IDs they can paste into other commands (especially `openclaw message send --target ...`), so it functions as an ID-discovery aid rather than a state-changing operation. The note covers the common flags (`--channel` / `--account` / `--json`), the config-backed nature of results and the unsupported-adapter behavior, the worked `message send` hand-off, the per-channel ID formats (WhatsApp, Telegram, Slack, Discord, Matrix, Microsoft Teams, Zalo, Zalo Personal), and the three subcommand groups `self`, `peers`, and `groups`.

## Common Flags

The command takes three common flags that select the channel/account and shape the output:

- `--channel <name>`: channel id/alias. Required when multiple channels are configured; auto-selected when only one channel is configured.
- `--account <id>`: account id. Defaults to the channel default.
- `--json`: output JSON.

## Notes (Behavior)

- `directory` is meant to help you find IDs you can paste into other commands (especially `openclaw message send --target ...`).
- For many channels, results are config-backed (allowlists / configured groups) rather than a live provider directory.
- Installed channel plugins can still omit directory support; in that case the command reports the unsupported directory operation instead of reinstalling the plugin.
- Default output is `id` (and sometimes `name`) separated by a tab; use `--json` for scripting.

## Using Results with `message send`

The typical workflow is to list peers for a channel to discover a target ID, then hand that ID to `openclaw message send --target`:

```bash
openclaw directory peers list --channel slack --query "U0"
openclaw message send --channel slack --target user:U012ABCDEF --message "hello"
```

## ID Formats (by Channel)

Each channel has its own target-ID format. Use these to interpret directory output and to build a `--target` for `message send`:

- WhatsApp: `+15551234567` (DM), `1234567890-1234567890@g.us` (group), `120363123456789@newsletter` (Channel/Newsletter outbound target)
- Telegram: `@username` or numeric chat id; groups are numeric ids
- Slack: `user:U…` and `channel:C…`
- Discord: `user:<id>` and `channel:<id>`
- Matrix (plugin): `user:@user:server`, `room:!roomId:server`, or `#alias:server`
- Microsoft Teams (plugin): `user:<id>` and `conversation:<id>`
- Zalo (plugin): user id (Bot API)
- Zalo Personal / `zalouser` (plugin): thread id (DM/group) from `zca` (`me`, `friend list`, `group list`)

## Self ("me")

The `directory self` subcommand looks up the channel's own ("me") identity for a given channel:

```bash
openclaw directory self --channel zalouser
```

## Peers (Contacts/Users)

The `directory peers list` subcommand lists a channel's contacts/users; it accepts `--query` for filtering and `--limit` to bound the result count:

```bash
openclaw directory peers list --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory peers list --channel zalouser --limit 50
```

## Groups

The `directory groups list` subcommand lists a channel's groups (with optional `--query` filtering), and `directory groups members` lists the members of a specific group identified by `--group-id`:

```bash
openclaw directory groups list --channel zalouser
openclaw directory groups list --channel zalouser --query "work"
openclaw directory groups members --channel zalouser --group-id <id>
```

**Source**: OpenClaw documentation — `cli/directory` (mirror `inbox/openclaw_docs/cli/directory.md`)
**Last Updated**: 2026-06-22
**Status**: Active
