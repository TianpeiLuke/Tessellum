---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - workboard
keywords:
  - openclaw workboard cli
  - workboard list create show
  - workboard cards sqlite state
  - workboard slash command parity
  - operator.read operator.write scopes
  - workboard plugin enable
  - workboard troubleshooting no cards
  - dev profile state root
topics:
  - OpenClaw
  - Workboard CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/workboard
access_control_group: ["general"]
---

# OpenClaw — `openclaw workboard` Card CLI

## Overview

This note is the operator procedure for the `openclaw workboard` terminal command — the CLI surface for the bundled Workboard plugin that lets an operator list, create, and inspect cards, plus ask the running Gateway to dispatch ready work into subagent worker runs. It mirrors the `cli/workboard` source page and covers everything except the `dispatch` mechanics: enabling the plugin, the `list` / `create` / `show` subcommands and their flags, the plugin-owned SQLite state model, slash-command parity, the read-vs-write permission scopes, and the three common troubleshooting paths. The `dispatch` subcommand's internals — the Gateway RPC `workboard.cards.dispatch` call, the 7-step dispatch loop, conservative selection, claim/block-on-failure, and the data-only fallback — are documented in the sibling note [oc_cli_workboard_dispatch](oc_cli_workboard_dispatch.md); this note references that note's outputs where troubleshooting needs them.

## Enabling the Plugin

`openclaw workboard` is the terminal surface for the bundled Workboard plugin. The plugin must be enabled (and the Gateway restarted) before the command is usable:

```bash
openclaw plugins enable workboard
openclaw gateway restart
```

The command reads and writes the **same plugin-owned SQLite database** used by the Control UI dashboard and the Workboard agent tools, so a card created from the CLI is immediately visible everywhere the plugin surfaces. Card ids can be passed by full id or by an unambiguous prefix wherever a subcommand accepts a card id.

## Usage

The four subcommands and their flag surfaces:

```bash
openclaw workboard list [--board <id>] [--status <status>] [--json]
openclaw workboard create <title...> [--notes <text>] [--status <status>] [--priority <priority>] [--agent <id>] [--board <id>] [--labels <items>] [--json]
openclaw workboard show <id> [--json]
openclaw workboard dispatch [--url <url>] [--token <token>] [--timeout <ms>] [--json]
```

## `list`

Lists cards, optionally narrowed to one board or status, with `--json` for machine output:

```bash
openclaw workboard list
openclaw workboard list --board default --status ready
openclaw workboard list --json
```

Text output is compact — one line per card. The columns are: id prefix, status, priority, board id, optional agent id, and title. A representative line is `7f4a2c10  ready     high    default agent-a  Fix stale worker heartbeat`.

The flags are: `--board <id>` limits results to one board namespace; `--status <status>` limits results to one Workboard status; and `--json` prints the full card list as machine JSON.

## `create`

Creates a card directly in Workboard SQLite state from a title plus optional metadata:

```bash
openclaw workboard create "Fix stale worker heartbeat" --priority high --labels bug,workboard
openclaw workboard create "Write Workboard docs" --status ready --agent docs-agent --board docs --notes "Cover CLI, slash command, dispatch, and SQLite state."
```

The flags are: `--notes <text>` sets initial card notes; `--status <status>` sets the initial status (default `todo`); `--priority <priority>` sets priority (default `normal`); `--agent <id>` assigns the card to an agent or owner id; `--board <id>` stores the card on a board namespace; `--labels <items>` takes comma-separated labels; and `--json` prints the created card as machine JSON. `create` writes directly to Workboard SQLite state, and the card is immediately visible in the Control UI Workboard tab and to Workboard tools.

## `show`

Inspects a single card by id (full id or unambiguous prefix):

```bash
openclaw workboard show 7f4a2c10
openclaw workboard show 7f4a2c10 --json
```

Text output prints the compact card line plus its notes. JSON output (`--json`) returns the full card record, including execution metadata, attempts, comments, links, proof, artifacts, worker logs, protocol state, diagnostics, and automation metadata.

## Slash Command Parity

Command-capable channels can use the matching slash command instead of the terminal:

```text
/workboard list
/workboard show 7f4a2c10
/workboard create Fix stale worker heartbeat
/workboard dispatch
```

Slash-command `dispatch` also uses the Gateway subagent runtime, so it follows the same claim, worker-start, and failure behavior as the dashboard and the CLI Gateway path (the mechanics of which are in [oc_cli_workboard_dispatch](oc_cli_workboard_dispatch.md)). `/workboard list` and `/workboard show` are **read** commands for authorized command senders. `/workboard create` and `/workboard dispatch` **mutate** board state and require owner status on chat surfaces, or a Gateway client with `operator.write` or `operator.admin`.

## Permissions

The CLI `dispatch` path calls the Gateway RPC with `operator.read` and `operator.write` scopes. A read-only Gateway token can inspect Workboard data through read methods, but it cannot create cards or dispatch workers. Local `list`, `create`, and `show` commands operate on the local OpenClaw state directory used by the current profile; use `--dev` or `--profile <name>` on the top-level `openclaw` command when you need a different state root.

## Troubleshooting

### No Cards Appear

Confirm the plugin is enabled for the same profile and state root by running `openclaw plugins inspect workboard --runtime --json`. If the dashboard shows cards but the CLI does not, check that both commands use the same `--dev` or `--profile` setting.

### Dispatch Says Data-Only

Start or restart the Gateway with `openclaw gateway restart`, verify it with `openclaw gateway status --deep`, then retry `openclaw workboard dispatch`. Data-only fallback is useful for local state cleanup, but worker runs need a live Gateway — see [oc_cli_workboard_dispatch](oc_cli_workboard_dispatch.md) for what the data-only fallback can and cannot do.

### Dispatch Starts Nothing

Check for at least one `ready` card without an active claim by running `openclaw workboard list --status ready`. Cards can also be skipped when the same owner already has running or review work. Move completed work to `done`, release stale claims through the Workboard tools, or run dispatch again after the active worker finishes — the conservative one-card-per-owner selection rules driving this are described in [oc_cli_workboard_dispatch](oc_cli_workboard_dispatch.md).

**Source**: OpenClaw documentation — `cli/workboard` (mirror `inbox/openclaw_docs/cli/workboard.md`)
**Last Updated**: 2026-06-22
**Status**: Active
