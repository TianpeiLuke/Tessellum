---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - elevated
keywords:
  - openclaw elevated mode
  - sandbox break-out exec
  - /elevated on ask full off
  - tools.elevated.enabled allowFrom
  - elevated resolution order
  - elevatedDefault global default
  - bash chat command gate
topics:
  - OpenClaw
  - Elevated Mode
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/elevated
access_control_group: ["general"]
---

# OpenClaw — Elevated Mode (Sandbox Break-Out for `exec`)

## Overview

This note is the procedure for **elevated mode** in OpenClaw: the mechanism that lets a *sandboxed* agent break out of its sandbox and run `exec` commands on the host instead, behind configurable approval gates. It mirrors the `tools/elevated` source page — the `/elevated on|ask|full|off` directives, how a directive is checked-then-applied, the inline → session → global resolution order, the `tools.elevated.enabled` + per-channel `allowFrom` availability gating (plus the per-agent and Discord-fallback rules and allowlist entry formats), and the explicit list of what elevated does NOT control (tool policy, host-selection policy, the separate `/exec` directive, and the `!`/`/bash` chat-command gate). Elevated mode only changes behavior when the agent is sandboxed; for unsandboxed agents `exec` already runs on the host.

## Directives

Elevated mode is controlled per-session with slash commands. There are four directives, also available under the short `/elev` alias (`/elev on|off|ask|full`):

| Directive | What it does |
| --- | --- |
| `/elevated on` | Run outside the sandbox on the configured host path, keep approvals |
| `/elevated ask` | Same as `on` (alias) |
| `/elevated full` | Run outside the sandbox on the configured host path and skip approvals |
| `/elevated off` | Return to sandbox-confined execution |

Send `/elevated` with no argument to see the current level. The key distinction is that `on`/`ask` still honor configured exec approval rules, while only `full` skips approvals.

## How It Works

The procedure runs in three steps — check availability, set the level, then run commands outside the sandbox.

**1. Check availability.** Elevated must be enabled in config AND the sender must be on the allowlist. The config block is JSON5:

```json5
{
  tools: {
    elevated: {
      enabled: true,
      allowFrom: {
        discord: ["user-id-123"],
        whatsapp: ["+15555550123"],
      },
    },
  },
}
```

**2. Set the level.** Send a directive-only message to set the *session* default (e.g. `/elevated full`), or use the directive inline so it applies to that one message only:

```
/elevated on run the deployment script
```

**3. Commands run outside the sandbox.** With elevated active, `exec` calls leave the sandbox. The effective host is `gateway` by default, or `node` when the configured/session exec target is `node`. In `full` mode, exec approvals are skipped; in `on`/`ask` mode, configured approval rules still apply.

## Resolution Order

When deciding the elevated level for a given `exec` call, OpenClaw resolves in this precedence order (highest first):

1. **Inline directive** on the message (applies only to that message).
2. **Session override** (set by sending a directive-only message).
3. **Global default** (`agents.defaults.elevatedDefault` in config).

## Availability and Allowlists

Elevated availability is gated by several controls; **all gates must pass**, otherwise elevated is treated as unavailable:

- **Global gate**: `tools.elevated.enabled` (must be `true`).
- **Sender allowlist**: `tools.elevated.allowFrom` with per-channel lists.
- **Per-agent gate**: `agents.list[].tools.elevated.enabled` (can only *further restrict* — it cannot widen access beyond the global gate).
- **Per-agent allowlist**: `agents.list[].tools.elevated.allowFrom` (the sender must match *both* the global and the per-agent allowlists).
- **Discord fallback**: if `tools.elevated.allowFrom.discord` is omitted, `channels.discord.allowFrom` is used as fallback.

Allowlist entries support several prefix formats for matching senders:

| Prefix | Matches |
| --- | --- |
| (none) | Sender ID, E.164, or From field |
| `name:` | Sender display name |
| `username:` | Sender username |
| `tag:` | Sender tag |
| `id:`, `from:`, `e164:` | Explicit identity targeting |

## What Elevated Does Not Control

Elevated mode is narrowly scoped — it does not override the surrounding security model:

- **Tool policy**: if `exec` is denied by tool policy, elevated cannot override it.
- **Host selection policy**: elevated does not turn `auto` into a free cross-host override. It uses the configured/session exec target rules, choosing `node` only when the target is already `node`.
- **Separate from `/exec`**: the `/exec` directive adjusts per-session exec defaults for authorized senders and does not require elevated mode.

The **bash chat command** (the `!` prefix; `/bash` alias) is a *separate* gate that requires `tools.elevated` to be enabled in addition to its own `tools.bash.enabled` flag. Disabling elevated therefore also locks `!` shell commands out.

**Source**: OpenClaw documentation — `tools/elevated` (mirror `inbox/openclaw_docs/tools/elevated.md`)
**Last Updated**: 2026-06-22
**Status**: Active
