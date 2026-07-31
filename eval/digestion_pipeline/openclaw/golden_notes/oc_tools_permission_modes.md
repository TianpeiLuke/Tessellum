---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - permission_modes
keywords:
  - openclaw permission modes
  - tools.exec.mode
  - deny allowlist ask auto full
  - codex guardian approval mapping
  - acpx harness permissions
  - permissionmode noninteractivepermissions
  - exec approvals stricter of two layers
  - openclaw exec-policy show
topics:
  - OpenClaw
  - Permission Modes
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/permission-modes
access_control_group: ["general"]
---

# OpenClaw — Permission Modes (host exec, Codex Guardian, ACPX)

## Overview

This note is the procedure for choosing and configuring OpenClaw **permission modes** — the authority surface that decides how much an agent can do before it runs host commands, writes files, or asks a backend harness for extra access. It mirrors the `tools/permission-modes` source page and covers: the recommended `auto` default, the five `tools.exec.mode` values (`deny` / `allowlist` / `ask` / `auto` / `full`) and how they differ from `tools.exec.host`, the Codex Guardian approval mapping for native Codex app-server sessions, the separate ACPX harness `permissionMode` / `nonInteractivePermissions` settings, and the goal→config decision matrix plus the "stricter result of two layers" rule. The full exec policy, allowlist schema, and local approvals file are NOT duplicated here — they live in the linked `oc_tools_exec_approvals` (to03) doc.

A load-bearing distinction up front (source Note): **permission mode is separate from `tools.exec.host=auto`**. `tools.exec.host` chooses *where* a command runs; `tools.exec.mode` chooses *how* host exec is approved.

## Recommended default

Start with `tools.exec.mode: "auto"` when you want OpenClaw to use allowlists first, then Codex native auto-review or a human approval route for misses — useful host access for coding agents without making every miss a human prompt. Set it, read the current approvals, and restart the Gateway so the change applies:

```bash
openclaw config set tools.exec.mode auto
openclaw approvals get
openclaw gateway restart
```

Then verify the effective policy:

```bash
openclaw exec-policy show
```

In `auto` mode, OpenClaw runs deterministic allowlist matches directly. Approval misses go through OpenClaw's native auto reviewer first, then fall back to the configured human approval route when needed.

## OpenClaw host exec modes

`tools.exec.mode` is the normalized policy surface for host `exec`. The five modes form a deny→full graduated-trust ladder:

| Mode        | Behavior                                     | Use when                                              |
| ----------- | -------------------------------------------- | ----------------------------------------------------- |
| `deny`      | Block host exec.                             | No host commands are allowed.                         |
| `allowlist` | Run only allowlisted commands.               | You have a known-safe command set.                    |
| `ask`       | Run allowlist matches and ask on misses.     | A human should review new commands.                   |
| `auto`      | Run allowlist matches, then use auto-review. | Coding sessions need practical guarded access.        |
| `full`      | Run host exec without prompts.               | This trusted host/session should skip approval gates. |

For the full host exec policy, local approvals file, allowlist schema, safe bins, and forwarding behavior, see the Exec approvals doc (`/tools/exec-approvals`).

## Codex Guardian mapping

For native Codex app-server sessions, `tools.exec.mode: "auto"` maps to Codex Guardian-reviewed approvals when the local Codex requirements allow it. OpenClaw usually sends:

| Codex field         | Typical value     |
| ------------------- | ----------------- |
| `approvalPolicy`    | `on-request`      |
| `approvalsReviewer` | `auto_review`     |
| `sandbox`           | `workspace-write` |

In `auto` mode, OpenClaw does **not** preserve legacy unsafe Codex overrides such as `approvalPolicy: "never"` or `sandbox: "danger-full-access"`. Use `tools.exec.mode: "full"` only when you intentionally want the no-approval posture. For app-server setup, auth order, and native Codex runtime details, see the Codex harness doc (`/plugins/codex-harness`).

## ACPX harness permissions

ACPX sessions are non-interactive, so they cannot click a TTY permission prompt. ACPX uses separate harness-level settings under `plugins.entries.acpx.config`:

| Setting                     | Common value    | Meaning                                     |
| --------------------------- | --------------- | ------------------------------------------- |
| `permissionMode`            | `approve-reads` | Auto-approve reads only.                    |
| `permissionMode`            | `approve-all`   | Auto-approve writes and shell commands.     |
| `permissionMode`            | `deny-all`      | Deny all permission prompts.                |
| `nonInteractivePermissions` | `fail`          | Abort when a prompt would be required.      |
| `nonInteractivePermissions` | `deny`          | Deny the prompt and continue when possible. |

Set ACPX permissions separately from OpenClaw exec approvals, then restart the Gateway:

```bash
openclaw config set plugins.entries.acpx.config.permissionMode approve-all
openclaw config set plugins.entries.acpx.config.nonInteractivePermissions fail
openclaw gateway restart
```

Use `approve-all` as the ACPX break-glass equivalent of a no-prompt harness session. For setup details and failure modes, see the ACP agents setup doc (`/tools/acp-agents-setup#permission-configuration`).

## Choosing a mode

Map your goal to the config to set:

| Goal                                          | Configure                                                   |
| --------------------------------------------- | ----------------------------------------------------------- |
| Block host commands completely                | `tools.exec.mode: "deny"`                                   |
| Let known-safe commands run only              | `tools.exec.mode: "allowlist"`                              |
| Ask a human for every new command shape       | `tools.exec.mode: "ask"`                                    |
| Use Codex/OpenClaw auto-review before humans  | `tools.exec.mode: "auto"`                                   |
| Skip host exec approvals entirely             | `tools.exec.mode: "full"` plus matching host approvals file |
| Make non-interactive ACPX sessions write/exec | `plugins.entries.acpx.config.permissionMode: "approve-all"` |

If a command still prompts or fails after changing mode, inspect both layers:

```bash
openclaw approvals get
openclaw exec-policy show
```

**Layer interaction (the stricter-of-two rule):** host exec uses the stricter result of OpenClaw config and the host-local approvals file. ACPX harness permissions do not loosen host exec approvals, and host exec approvals do not loosen ACPX harness prompts — the two surfaces are independent and neither relaxes the other.

**Source**: OpenClaw documentation — `tools/permission-modes` (mirror `inbox/openclaw_docs/tools/permission-modes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
