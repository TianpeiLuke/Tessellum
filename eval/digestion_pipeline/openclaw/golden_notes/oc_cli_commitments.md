---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - commitments
keywords:
  - openclaw commitments command
  - inferred follow-up commitments
  - commitments list dismiss
  - commitment status pending sent dismissed snoozed expired
  - commitment json output store path
  - heartbeat delivered commitments
  - openclaw cli follow-up management
topics:
  - OpenClaw
  - CLI commitments command
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/commitments
access_control_group: ["general"]
---

# OpenClaw — `openclaw commitments` CLI Command

## Overview

This note documents the procedure for using the `openclaw commitments` CLI command to list and manage **inferred follow-up commitments** — opt-in, short-lived follow-up memories OpenClaw creates from conversation context. It mirrors the `cli/commitments` source page: the command's `read_when` use-cases (inspect inferred follow-ups, dismiss pending check-ins, audit what heartbeat may deliver), the `list` / `dismiss` subcommands and the no-subcommand default, the four filter/format options (`--all`, `--agent`, `--status`, `--json`), worked invocation examples, and the text-vs-JSON output fields. The conceptual model behind commitments is owned elsewhere ([Inferred commitments](https://docs.openclaw.ai/concepts/commitments)) and is linked, not redefined here.

## What the command manages

`openclaw commitments` lists and manages inferred follow-up commitments. Commitments are opt-in, short-lived follow-up memories created from conversation context; the conceptual guide is the `/concepts/commitments` page (linked, not duplicated). The command is the operator surface for inspecting those follow-ups, dismissing pending check-ins, and auditing what the gateway heartbeat may deliver.

## Usage

With no subcommand, `openclaw commitments` lists pending commitments. The `list` subcommand is the explicit form of that default, and `dismiss` removes one or more commitments by id.

```bash
openclaw commitments [--all] [--agent <id>] [--status <status>] [--json]
openclaw commitments list [--all] [--agent <id>] [--status <status>] [--json]
openclaw commitments dismiss <id...> [--json]
```

## Options

The same filter/format options apply to the default listing and to `list`; `dismiss` accepts `--json`.

- `--all`: show all statuses instead of only pending commitments.
- `--agent <id>`: filter to one agent id.
- `--status <status>`: filter by status. Values: `pending`, `sent`, `dismissed`, `snoozed`, or `expired`.
- `--json`: output machine-readable JSON.

## Examples

These are the worked invocations from the source page, each shown verbatim. The first lists pending commitments (the no-subcommand default); `--all` widens to every stored status; `--agent` and `--status` narrow the listing; `dismiss` takes one or more ids; and the final example exports the full set as JSON.

```bash
# List pending commitments
openclaw commitments

# List every stored commitment
openclaw commitments --all

# Filter to one agent
openclaw commitments --agent main

# Find snoozed commitments
openclaw commitments --status snoozed

# Dismiss one or more commitments
openclaw commitments dismiss cm_abc123 cm_def456

# Export as JSON
openclaw commitments --all --json
```

## Output

Text output includes, per commitment:

- commitment id
- status
- kind
- earliest due time
- scope
- suggested check-in text

JSON output (`--json`) also includes the commitment **store path** and the full stored records, in addition to the text fields above.

**Source**: OpenClaw documentation — `cli/commitments` (mirror `inbox/openclaw_docs/cli/commitments.md`)
**Last Updated**: 2026-06-22
**Status**: Active
