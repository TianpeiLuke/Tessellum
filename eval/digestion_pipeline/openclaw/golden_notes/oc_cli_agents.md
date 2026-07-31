---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - multi_agent
keywords:
  - openclaw agents command
  - isolated agents workspaces auth routing
  - routing bindings --bind channel account
  - binding scope upgrade behavior
  - agents add delete set-identity
  - agent identity files IDENTITY.md
  - openclaw multi-agent cli
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/agents
access_control_group: ["general"]
---

# OpenClaw — Managing Isolated Agents with `openclaw agents`

## Overview

This note is the procedure reference for `openclaw agents`, the CLI surface for managing isolated OpenClaw agents — each an independent bundle of **workspace + auth + routing**. It mirrors the `cli/agents` source page: listing agents, adding and deleting them, the routing-binding model (`--bind <channel>[:account]`, binding scope and the in-place upgrade behavior), the full subcommand surface with per-command options and notes, identity files (`IDENTITY.md`), and `set-identity`. Deep concept material (multi-agent routing, the agent workspace, per-agent skill visibility) is linked out, not duplicated here.

## What `openclaw agents` Does

`openclaw agents` manages isolated agents, where each agent is a workspace plus its own auth and routing bindings. Use routing bindings to pin inbound channel traffic to a specific agent. If you also want different visible skills per agent, you configure `agents.defaults.skills` and `agents.list[].skills` in `openclaw.json` (see the linked Skills config and Configuration reference) — skill visibility is set in config, not by this command.

## Examples

The page's example block shows the command's full breadth — list (optionally with bindings), add (optionally with a workspace and inline `--bind`), inspect bindings, bind/unbind, set identity, and delete:

```bash
openclaw agents list
openclaw agents list --bindings
openclaw agents add work --workspace ~/.openclaw/workspace-work
openclaw agents add work --workspace ~/.openclaw/workspace-work --bind telegram:*
openclaw agents add ops --workspace ~/.openclaw/workspace-ops --bind telegram:ops --non-interactive
openclaw agents bindings
openclaw agents bind --agent work --bind telegram:ops
openclaw agents unbind --agent work --bind telegram:ops
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
openclaw agents set-identity --agent main --avatar avatars/openclaw.png
openclaw agents delete work
```

## Routing Bindings

Routing bindings pin inbound channel traffic to a specific agent. List bindings with `openclaw agents bindings` (optionally `--agent <id>` or `--json`); add them with `openclaw agents bind`; and you can also add bindings at creation time via `agents add ... --bind`:

```bash
openclaw agents bind --agent work --bind telegram:ops --bind discord:guild-a
openclaw agents add work --workspace ~/.openclaw/workspace-work --bind telegram:* --bind discord:*
```

If you omit `accountId` (i.e. `--bind <channel>`), OpenClaw resolves it from plugin setup hooks, forced account binding, or the channel's configured account count. If you omit `--agent` for `bind` or `unbind`, OpenClaw targets the current default agent.

### `--bind` format

The `--bind` argument selects which channel accounts a binding matches:

| Format | Meaning |
| --- | --- |
| `--bind <channel>:*` | Match all accounts on the channel. |
| `--bind <channel>:<account>` | Match one account. |
| `--bind <channel>` | Match the default account only unless the CLI can safely resolve a plugin-specific account scope. |

### Binding scope behavior

The stored-binding semantics determine which traffic a binding catches and how re-binding the same agent/channel is reconciled:

- A stored binding without `accountId` matches the channel default account only.
- `accountId: "*"` is the channel-wide fallback (all accounts) and is less specific than an explicit account binding.
- If the same agent already has a matching channel binding without `accountId`, and you later bind with an explicit or resolved `accountId`, OpenClaw upgrades that existing binding in place instead of adding a duplicate.

This upgrade flow — a channel-only binding later refined to an account-scoped one — looks like:

```bash
# match all accounts on the channel
openclaw agents bind --agent work --bind telegram:*

# match a specific account
openclaw agents bind --agent work --bind telegram:ops

# initial channel-only binding
openclaw agents bind --agent work --bind telegram

# later upgrade to account-scoped binding
openclaw agents bind --agent work --bind telegram:alerts
```

After the upgrade, routing for that binding is scoped to `telegram:alerts`. If you also want default-account routing, you must add it explicitly (for example `--bind telegram:default`). To remove bindings, use `openclaw agents unbind --agent work --bind telegram:ops` or `openclaw agents unbind --agent work --all`; `unbind` accepts either `--all` or one or more `--bind` values, **not both**.

## Command Surface

### `agents`

Running `openclaw agents` with no subcommand is equivalent to `openclaw agents list`.

### `agents list`

Options: `--json`; `--bindings` (include full routing rules, not only per-agent counts/summaries).

### `agents add [name]`

Options: `--workspace <dir>`; `--model <id>`; `--agent-dir <dir>`; `--bind <channel[:accountId]>` (repeatable); `--non-interactive`; `--json`.

Notes:

- Passing any explicit add flags switches the command into the non-interactive path.
- Non-interactive mode requires both an agent name and `--workspace`.
- `main` is reserved and cannot be used as the new agent id.
- In interactive mode, auth seeding copies only portable static profiles (`api_key` and static `token` by default). OAuth refresh-token profiles remain available only by read-through inheritance from the real `main` agent store. If the configured default agent is not `main`, sign in separately for OAuth profiles on the new agent.

### `agents bindings`

Options: `--agent <id>`; `--json`.

### `agents bind`

Options: `--agent <id>` (defaults to the current default agent); `--bind <channel[:accountId]>` (repeatable); `--json`.

### `agents unbind`

Options: `--agent <id>` (defaults to the current default agent); `--bind <channel[:accountId]>` (repeatable); `--all`; `--json`.

### `agents delete <id>`

Options: `--force`; `--json`.

Notes:

- `main` cannot be deleted.
- Without `--force`, interactive confirmation is required.
- Workspace, agent state, and session transcript directories are moved to Trash, not hard-deleted.
- When the Gateway is reachable, deletion is sent through the Gateway so config and session-store cleanup share the same writer as runtime traffic. If the Gateway cannot be reached, the CLI falls back to the offline local path.
- If another agent's workspace is the same path, inside this workspace, or contains this workspace, the workspace is retained and `--json` reports `workspaceRetained`, `workspaceRetainedReason`, and `workspaceSharedWith`.

## Identity Files

Each agent workspace can include an `IDENTITY.md` at the workspace root. Example path: `~/.openclaw/workspace/IDENTITY.md`. `set-identity --from-identity` reads from the workspace root (or an explicit `--identity-file`). Avatar paths resolve relative to the workspace root.

## Set Identity

`set-identity` writes fields into `agents.list[].identity`: `name`, `theme`, `emoji`, and `avatar` (a workspace-relative path, an http(s) URL, or a data URI).

Options: `--agent <id>`; `--workspace <dir>`; `--identity-file <path>`; `--from-identity`; `--name <name>`; `--theme <theme>`; `--emoji <emoji>`; `--avatar <value>`; `--json`.

Notes:

- `--agent` or `--workspace` can be used to select the target agent.
- If you rely on `--workspace` and multiple agents share that workspace, the command fails and asks you to pass `--agent`.
- When no explicit identity fields are provided, the command reads identity data from `IDENTITY.md`.

Load identity from `IDENTITY.md`, or override fields explicitly:

```bash
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
openclaw agents set-identity --agent main --name "OpenClaw" --emoji "🦞" --avatar avatars/openclaw.png
```

The resulting config sample for an agent's identity (JSON5):

```json5
{
  agents: {
    list: [
      {
        id: "main",
        identity: {
          name: "OpenClaw",
          theme: "space lobster",
          emoji: "🦞",
          avatar: "avatars/openclaw.png",
        },
      },
    ],
  },
}
```

**Source**: OpenClaw documentation — `cli/agents` (mirror `inbox/openclaw_docs/cli/agents.md`)
**Last Updated**: 2026-06-22
**Status**: Active
