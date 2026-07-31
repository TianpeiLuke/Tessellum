---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - exec_approvals
keywords:
  - openclaw approvals cli
  - openclaw exec-policy
  - exec approvals allowlist
  - host approvals file precedence
  - yolo never prompt preset
  - tools.exec security ask askfallback
  - gateway node host approvals
  - exec-approvals.json state dir
topics:
  - OpenClaw
  - Exec Approvals CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/approvals
access_control_group: ["general"]
---

# OpenClaw — Editing Exec Approvals with `openclaw approvals` / `exec-policy`

## Overview

This procedure note documents the `openclaw approvals` CLI command (alias `openclaw exec-approvals`) and its local convenience sibling `openclaw exec-policy`, which edit exec approvals for the local host, the gateway host, or a node host. It mirrors the `cli/approvals` source page: host targeting (default local / `--gateway` / `--node`), the `exec-policy` local-only show/preset/set/sync flow, the `approvals get` effective-policy inspection and the host-approvals-file-vs-requested-`tools.exec`-policy precedence, replace-from-file (`--file`/`--stdin`, JSON5), the "Never prompt"/YOLO preset, allowlist add/remove helpers, the common option/targeting surface, and where approvals files live on disk.

## Host targeting model

`openclaw approvals` manages exec approvals for one of three host scopes: the **local host**, the **gateway host**, or a **node host**. By default, commands target the local approvals file on disk. Use `--gateway` to target the gateway, or `--node <id|name|ip>` to target a specific node. The command is aliased as `openclaw exec-approvals`. The page links two deeper references — [Exec approvals](https://docs.openclaw.ai/tools/exec-approvals) (the concept/tool deep-dive) and [Nodes](https://docs.openclaw.ai/nodes) (node resolution) — which are linked out, not duplicated here.

## `openclaw exec-policy`

`openclaw exec-policy` is the **local convenience command** for keeping the requested `tools.exec.*` config and the local host approvals file aligned in one step. Use it when you want to inspect the local requested policy, host approvals file, and effective merge; apply a local preset such as YOLO or deny-all; or synchronize local `tools.exec.*` and the local host approvals file.

```bash
openclaw exec-policy show
openclaw exec-policy show --json

openclaw exec-policy preset yolo
openclaw exec-policy preset cautious --json

openclaw exec-policy set --host gateway --security full --ask off --ask-fallback full
```

Output modes: with no `--json` the command prints the human-readable table view; with `--json` it prints machine-readable structured output.

`exec-policy` is intentionally **local-only**. It updates the local config file and the local approvals file together, and it does **not** push policy to the gateway host or a node host. `--host node` is rejected in this command because node exec approvals are fetched from the node at runtime and must be managed through node-targeted approvals commands instead; correspondingly, `openclaw exec-policy show` marks `host=node` scopes as node-managed at runtime instead of deriving an effective policy from the local approvals file. If you need to edit remote host approvals directly, keep using `openclaw approvals set --gateway` or `openclaw approvals set --node <id|name|ip>`.

## Common commands and precedence

```bash
openclaw approvals get
openclaw approvals get --node <id|name|ip>
openclaw approvals get --gateway
```

`openclaw approvals get` now shows the **effective exec policy** for local, gateway, and node targets: the requested `tools.exec` policy, the host approvals-file policy, and the effective result after precedence rules are applied.

Precedence is intentional: the host approvals file is the enforceable source of truth; the requested `tools.exec` policy can narrow or broaden intent, but the effective result is still derived from the host rules; `--node` combines the node host approvals file with gateway `tools.exec` policy, because both still apply at runtime; and if gateway config is unavailable, the CLI falls back to the node approvals snapshot and notes that the final runtime policy could not be computed.

## Replace approvals from a file

```bash
openclaw approvals set --file ./exec-approvals.json
openclaw approvals set --stdin <<'EOF'
{ version: 1, defaults: { security: "full", ask: "off", askFallback: "full" } }
EOF
openclaw approvals set --node <id|name|ip> --file ./exec-approvals.json
openclaw approvals set --gateway --file ./exec-approvals.json
```

`set` accepts **JSON5**, not only strict JSON. Use either `--file` or `--stdin`, **not both**.

## "Never prompt" / YOLO example

For a host that should never stop on exec approvals, set the host approvals defaults to `full` + `off`:

```bash
openclaw approvals set --stdin <<'EOF'
{
  version: 1,
  defaults: {
    security: "full",
    ask: "off",
    askFallback: "full"
  }
}
EOF
```

A node variant runs the same `--stdin` payload with `openclaw approvals set --node <id|name|ip>`. This changes the **host approvals file** only. To keep the requested OpenClaw policy aligned, also set the requested config:

```bash
openclaw config set tools.exec.host gateway
openclaw config set tools.exec.security full
openclaw config set tools.exec.ask off
```

Why `tools.exec.host=gateway` in this example: `host=auto` still means "sandbox when available, otherwise gateway"; YOLO is about **approvals, not routing**; and if you want host exec even when a sandbox is configured, make the host choice explicit with `gateway` or `/exec host=gateway`. Omitted `askFallback` defaults to `deny` — set `askFallback: "full"` explicitly when upgrading a no-UI host that should keep never-prompt behavior.

The local shortcut `openclaw exec-policy preset yolo` updates **both** the requested local `tools.exec.*` config and the local approvals defaults together; it is equivalent in intent to the manual two-step setup above, but only for the local machine.

## Allowlist helpers

```bash
openclaw approvals allowlist add "~/Projects/**/bin/rg"
openclaw approvals allowlist add --agent main --node <id|name|ip> "/usr/bin/uptime"
openclaw approvals allowlist add --agent "*" "/usr/bin/uname"

openclaw approvals allowlist remove "~/Projects/**/bin/rg"
```

## Common options and targeting

`get`, `set`, and `allowlist add|remove` all support `--node <id|name|ip>`, `--gateway`, and the shared node RPC options `--url`, `--token`, `--timeout`, `--json`. Targeting resolves as follows: no target flags means the local approvals file on disk; `--gateway` targets the gateway host approvals file; `--node` targets one node host after resolving id, name, IP, or id prefix. `allowlist add|remove` additionally supports `--agent <id>` (defaults to `*`).

## Notes

- `--node` uses the same resolver as `openclaw nodes` (id, name, ip, or id prefix).
- `--agent` defaults to `"*"`, which applies to all agents.
- The node host must advertise `system.execApprovals.get/set` (macOS app or headless node host).
- Approvals files are stored per host in the OpenClaw state dir (`$OPENCLAW_STATE_DIR/exec-approvals.json`, or `~/.openclaw/exec-approvals.json` when the variable is unset).

**Source**: OpenClaw documentation — `cli/approvals` (mirror `inbox/openclaw_docs/cli/approvals.md`)
**Last Updated**: 2026-06-22
**Status**: Active
