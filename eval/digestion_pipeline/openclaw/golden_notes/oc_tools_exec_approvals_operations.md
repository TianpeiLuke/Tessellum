---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - exec_approvals
keywords:
  - openclaw exec approvals operations
  - yolo mode no-approval
  - exec-policy preset yolo
  - per-agent allowlist argPattern
  - auto-allow skill clis
  - exec approval flow systemRunPlan
  - exec running finished system events
  - denied approval fail-closed
topics:
  - OpenClaw
  - Exec Approvals
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/exec-approvals
access_control_group: ["general"]
---

# OpenClaw — Operating Exec Approvals (YOLO, Allowlists, Approval Flow)

## Overview

This note is the operational half of OpenClaw's host exec-approvals procedure, mirroring the second part of the `tools/exec-approvals` source page (from "YOLO mode" through "Implications"). It covers the day-to-day workflows operators run against the approvals system: setting up no-approval YOLO mode across both policy layers, building per-agent allowlists (including `argPattern` argument restriction and the full entry-field schema), auto-allowing skill CLIs, editing approvals through the Control UI or `openclaw approvals` CLI, the request→resolve→forward approval flow with its canonical `systemRunPlan` binding, the `Exec running`/`Exec finished` system events, and the fail-closed denied-approval behavior. The declarative policy model (effective-policy resolution, `exec-approvals.json` storage, and the `tools.exec.mode`/`security`/`ask`/`askFallback`/`strictInlineEval`/`commandHighlighting` knobs) is the companion note [oc_tools_exec_approvals_policy](oc_tools_exec_approvals_policy.md).

## YOLO mode (no-approval)

If you want host exec to run without approval prompts, you must open **both** policy layers — the requested exec policy in OpenClaw config (`tools.exec.*`) **and** the host-local approvals policy in the execution host approvals file. OpenClaw defaults an omitted `askFallback` to `deny`, so set host `askFallback` to `full` explicitly when a no-UI approval prompt should fall back to allow. The three settings that together constitute YOLO are:

| Layer                 | YOLO setting               |
| --------------------- | -------------------------- |
| `tools.exec.security` | `full` on `gateway`/`node` |
| `tools.exec.ask`      | `off`                      |
| Host `askFallback`    | `full`                     |

Important distinctions the source emphasizes: `tools.exec.host=auto` chooses **where** exec runs (sandbox when available, otherwise gateway), whereas YOLO chooses **how** host exec is approved (`security=full` plus `ask=off`). In YOLO mode OpenClaw does **not** add a separate heuristic command-obfuscation approval gate or script-preflight rejection layer on top of the configured host exec policy. Also, `auto` does not make gateway routing a free override from a sandboxed session: a per-call `host=node` request is allowed from `auto`, but `host=gateway` is only allowed from `auto` when no sandbox runtime is active — for a stable non-auto default, set `tools.exec.host` or use `/exec host=...` explicitly.

CLI-backed providers that expose their own noninteractive permission mode can follow this policy. The Claude CLI adds `--permission-mode bypassPermissions` when OpenClaw's effective exec policy is YOLO. For OpenClaw-managed Claude live sessions, OpenClaw's effective exec policy is authoritative over Claude's native permission mode: YOLO normalizes live launches to `--permission-mode bypassPermissions`, and a restrictive effective exec policy normalizes live launches to `--permission-mode default`, even if raw Claude backend args specify another mode. For a more conservative setup, tighten OpenClaw exec policy back to `allowlist` / `on-miss` or `deny`.

### Persistent gateway-host "never prompt" setup

Set the requested config policy, then match the host approvals file so both layers agree:

```bash
openclaw config set tools.exec.host gateway
openclaw config set tools.exec.security full
openclaw config set tools.exec.ask off
openclaw gateway restart
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

### Local shortcut

`openclaw exec-policy preset yolo` updates both layers in one step: the local `tools.exec.host/security/ask` and the local approvals file defaults (including `askFallback: "full"`). It is intentionally local-only — to change gateway-host or node-host approvals remotely, use `openclaw approvals set --gateway` or `openclaw approvals set --node <id|name|ip>`.

```bash
openclaw exec-policy preset yolo
```

### Node host

For a node host, apply the same approvals file on that node instead:

```bash
openclaw approvals set --node <id|name|ip> --stdin <<'EOF'
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

Local-only limitations apply to node scopes: `openclaw exec-policy` does not synchronize node approvals; `openclaw exec-policy set --host node` is rejected; and node exec approvals are fetched from the node at runtime, so node-targeted updates must use `openclaw approvals --node ...`.

### Session-only shortcut

`/exec security=full ask=off` changes only the current session. `/elevated full` is a break-glass shortcut that skips exec approvals only when both the requested policy and the host approvals file resolve to `security: "full"` and `ask: "off"`; a stricter host file (such as `ask: "always"`) still prompts. If the host approvals file stays stricter than config, the stricter host policy still wins.

## Allowlist (per agent)

Allowlists are **per agent** — if multiple agents exist, switch which agent you are editing in the macOS app. Patterns are glob matches and can be resolved binary path globs or bare command-name globs. Bare names match only commands invoked through `PATH`, so `rg` can match `/opt/homebrew/bin/rg` when the command is `rg`, but **not** `./rg` or `/tmp/rg`; use a path glob when you want to trust one specific binary location. Legacy `agents.default` entries are migrated to `agents.main` on load, and shell chains such as `echo ok && pwd` still need every top-level segment to satisfy allowlist rules. Example patterns: `rg`, `~/Projects/**/bin/peekaboo`, `~/.local/bin/*`, `/opt/homebrew/bin/rg`.

### Restricting arguments with argPattern

Add `argPattern` when an allowlist entry should match a binary **and** a specific argument shape. OpenClaw evaluates the regular expression against the parsed command arguments, excluding the executable token (`argv[0]`). For hand-authored entries, arguments are joined with a single space, so anchor the pattern when you need an exact match. The example entry below allows `python3 safe.py` while making `python3 other.py` an allowlist miss:

```json
{
  "version": 1,
  "agents": {
    "main": {
      "allowlist": [
        {
          "pattern": "python3",
          "argPattern": "^safe\\.py$"
        }
      ]
    }
  }
}
```

If a path-only entry for the same binary is also present, unmatched arguments can still fall back to that path-only entry; omit the path-only entry when the goal is to restrict the binary to the declared arguments. Entries saved by approval flows can use an internal separator format for exact argv matching — prefer the UI or approval flow to regenerate those entries instead of hand-editing the encoded value. If OpenClaw cannot parse argv for a command segment, entries with `argPattern` do not match. Each allowlist entry supports these fields:

| Field              | Meaning                                                       |
| ------------------ | ------------------------------------------------------------- |
| `pattern`          | Resolved binary path glob or bare command-name glob           |
| `argPattern`       | Optional argv regex; omitted entries are path-only            |
| `id`               | Stable UUID used for UI identity                              |
| `source`           | Entry source, such as `allow-always`                          |
| `commandText`      | Command text captured when an approval flow created the entry |
| `lastUsedAt`       | Last-used timestamp                                           |
| `lastUsedCommand`  | Last command that matched                                     |
| `lastResolvedPath` | Last resolved binary path                                     |

## Auto-allow skill CLIs

When **Auto-allow skill CLIs** is enabled, executables referenced by known skills are treated as allowlisted on nodes (macOS node or headless node host). This uses `skills.bins` over the Gateway RPC to fetch the skill bin list; disable it if you want strict manual allowlists. The source flags this as an **implicit convenience allowlist**, separate from manual path allowlist entries, intended for trusted operator environments where Gateway and node are in the same trust boundary. If you require strict explicit trust, keep `autoAllowSkills: false` and use manual path allowlist entries only.

## Control UI editing

Use the **Control UI → Nodes → Exec approvals** card to edit defaults, per-agent overrides, and allowlists: pick a scope (Defaults or an agent), tweak the policy, add or remove allowlist patterns, then **Save**. The UI shows last-used metadata per pattern so you can keep the list tidy. The target selector chooses **Gateway** (local approvals) or a **Node** — nodes must advertise `system.execApprovals.get/set` (macOS app or headless node host), and if a node does not advertise exec approvals yet, edit its local approvals file directly. The `openclaw approvals` CLI also supports gateway or node editing (see [oc_cli_approvals](oc_cli_approvals.md)).

## Approval flow

When a prompt is required, the gateway broadcasts `exec.approval.requested` to operator clients. The Control UI and macOS app resolve it via `exec.approval.resolve`, and the gateway then forwards the approved request to the node host. For `host=node`, approval requests include a canonical `systemRunPlan` payload, which the gateway uses as the authoritative command/cwd/session context when forwarding approved `system.run` requests. This canonical-plan binding matters for async approval latency:

- The node exec path prepares one canonical plan up front.
- The approval record stores that plan and its binding metadata.
- Once approved, the final forwarded `system.run` call reuses the stored plan instead of trusting later caller edits.
- If the caller changes `command`, `rawCommand`, `cwd`, `agentId`, or `sessionKey` after the approval request was created, the gateway rejects the forwarded run as an approval mismatch.

## System events

Exec lifecycle is surfaced as system messages: `Exec running` (only if the command exceeds the running notice threshold) and `Exec finished`. These are posted to the agent's session after the node reports the event. Gateway-host exec approvals emit the same lifecycle events when the command finishes (and optionally when running longer than the threshold). Approval-gated execs reuse the approval id as the `runId` in these messages for easy correlation.

## Denied approval behavior

When an async exec approval is denied, OpenClaw treats the host command as terminal and fail-closed — the command does not run. For main-agent sessions with an originating session, the denial is delivered as an internal session followup that tells the agent the async command did not run, preserving transcript continuity without exposing stale command output and letting the agent stop waiting on the async command (avoiding a missing-result repair). If session delivery is unavailable, OpenClaw falls back to a concise operator or direct-chat denial when a safe route exists. Denials for subagent sessions are **not** posted back into the subagent.

## Implications

- **`full`** is powerful; prefer allowlists when possible.
- **`ask`** keeps you in the loop while still allowing fast approvals.
- Per-agent allowlists prevent one agent's approvals from leaking into others.
- Approvals only apply to host exec requests from **authorized senders** — unauthorized senders cannot issue `/exec`.
- `/exec security=full` is a session-level convenience for authorized operators and skips approvals by design. To hard-block host exec, set approvals security to `deny` or deny the `exec` tool via tool policy.

**Source**: OpenClaw documentation — `tools/exec-approvals` (operations half; mirror `inbox/openclaw_docs/tools/exec-approvals.md`)
**Last Updated**: 2026-06-22
**Status**: Active
