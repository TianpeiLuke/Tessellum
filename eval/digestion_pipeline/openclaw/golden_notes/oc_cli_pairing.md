---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - pairing
keywords:
  - openclaw pairing
  - pairing approve
  - pairing list
  - dm pairing approval
  - owner bootstrap
  - commands.ownerallowfrom
  - pairing code
  - multi-account channel pairing
topics:
  - OpenClaw
  - CLI Pairing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/pairing
access_control_group: ["general"]
---

# OpenClaw — `openclaw pairing` (DM Pairing Approval)

## Overview

This note documents the `openclaw pairing` CLI command, which approves or inspects DM pairing requests for channels that support pairing. It mirrors the `cli/pairing` source page in full: the two subcommands (`pairing list`, `pairing approve`), their channel-selection and multi-account options, the `--notify` confirmation flag, and the first-approval owner-bootstrap that seeds `commands.ownerAllowFrom`. Pairing is the operator gate that decides which channel senders are allowed to DM the bot; this command is the surface an operator runs to grant that access.

## Commands

The page lists the canonical invocations. List pending requests for a channel, then approve a specific pairing code:

```bash
openclaw pairing list telegram
openclaw pairing list --channel telegram --account work
openclaw pairing list telegram --json

openclaw pairing approve <code>
openclaw pairing approve telegram <code>
openclaw pairing approve --channel telegram --account work <code> --notify
```

Pairing approval applies only to **channels that support pairing**. Per the page's Notes, the channel can be passed positionally (`pairing list telegram`) or explicitly with `--channel <channel>`, and extension channels are allowed as long as the channel id is valid.

## `pairing list`

Lists pending pairing requests for one channel.

Options:

- `[channel]` — positional channel id.
- `--channel <channel>` — explicit channel id.
- `--account <accountId>` — account id for multi-account channels.
- `--json` — machine-readable output.

Behavior notes from the source: if multiple pairing-capable channels are configured, you must provide a channel either positionally or with `--channel`. Extension channels are allowed as long as the channel id is valid.

## `pairing approve`

Approves a pending pairing code and allows that sender. The source gives three accepted usages:

- `openclaw pairing approve <channel> <code>`
- `openclaw pairing approve --channel <channel> <code>`
- `openclaw pairing approve <code>` — allowed when exactly one pairing-capable channel is configured.

Options:

- `--channel <channel>` — explicit channel id.
- `--account <accountId>` — account id for multi-account channels.
- `--notify` — send a confirmation back to the requester on the same channel.

## Owner Bootstrap

Approving a pairing code can also seed the command owner on first use. The source states this exactly: if `commands.ownerAllowFrom` is empty when you approve a pairing code, OpenClaw also records the approved sender as the command owner, using a channel-scoped entry such as `telegram:123456789`. This **only bootstraps the first owner** — later pairing approvals do not replace or expand `commands.ownerAllowFrom`. The command owner is the human operator account allowed to run owner-only commands and approve dangerous actions such as `/diagnostics`, `/export-trajectory`, `/config`, and exec approvals.

## Notes

Operational details consolidated from the page's Notes section:

- Channel input: pass it positionally (`pairing list telegram`) or with `--channel <channel>`.
- `pairing list` supports `--account <accountId>` for multi-account channels.
- `pairing approve` supports `--account <accountId>` and `--notify`.
- If only one pairing-capable channel is configured, `pairing approve <code>` is allowed (channel may be omitted).
- If you approved a sender before this bootstrap existed, run `openclaw doctor`; it warns when no command owner is configured and shows the `openclaw config set commands.ownerAllowFrom ...` command to fix it.

**Source**: OpenClaw documentation — `cli/pairing` (mirror `inbox/openclaw_docs/cli/pairing.md`)
**Last Updated**: 2026-06-22
**Status**: Active
