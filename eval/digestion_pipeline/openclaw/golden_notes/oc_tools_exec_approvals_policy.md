---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - exec_approvals
keywords:
  - openclaw exec approvals policy
  - tools.exec.mode deny allowlist ask auto full
  - exec security ask askFallback
  - effective policy stricter of config and host
  - exec-approvals.json storage schema
  - openclaw approvals get exec-policy show
  - strictInlineEval commandHighlighting
  - gateway node host trust model macOS split
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

# OpenClaw — Exec Approvals Policy Model and Storage

## Overview

This note covers the **declarative half** of OpenClaw's exec-approvals system: the policy resolution model, where it is enforced, its on-disk storage, and the individual policy knobs. Exec approvals are the **companion app / node host guardrail** for letting a sandboxed agent run commands on a real host (`gateway` or `node`) — a safety interlock where a command runs only when policy + allowlist + (optional) user approval all agree, stacking on top of tool policy and elevated gating (unless elevated is set to `full`, which skips approvals). It mirrors the `tools/exec-approvals` source page sections: the intro, *Inspecting the effective policy*, *Where it applies* (Trust model, macOS split), *Settings and storage*, and *Policy knobs* (`tools.exec.mode`, `exec.security`, `exec.ask`, `askFallback`, `strictInlineEval`, `commandHighlighting`). The operating workflows — YOLO setup, allowlist editing, approval flow, system events, denied behavior — live in the split sibling [oc_tools_exec_approvals_operations](oc_tools_exec_approvals_operations.md).

The effective policy is the **stricter** of `tools.exec.*` and the approvals defaults: if an approvals field is omitted, the `tools.exec` value is used. Host exec also uses local approvals state on that machine — a host-local `ask: "always"` in the execution host approvals file keeps prompting even if session or config defaults request `ask: "on-miss"`. For a mode-first overview of `deny`, `allowlist`, `ask`, `auto`, `full`, Codex Guardian mapping, and ACPX harness permissions, the page points to the OpenClaw `tools/permission-modes` reference (see References).

## Inspecting the effective policy

Three CLI surfaces inspect or synchronize the resolved policy:

| Command | What it shows |
| --- | --- |
| `openclaw approvals get` / `--gateway` / `--node <id\|name\|ip>` | Requested policy, host policy sources, and the effective result. |
| `openclaw exec-policy show` | Local-machine merged view. |
| `openclaw exec-policy set` / `preset` | Synchronize the local requested policy with the local host approvals file in one step. |

When a local scope requests `host=node`, `exec-policy show` reports that scope as node-managed at runtime instead of pretending the local approvals file is the source of truth. If the companion app UI is **not available**, any request that would normally prompt is resolved by the **ask fallback** (default: `deny`). Native chat approval clients can seed channel-specific affordances on the pending approval message — for example, Matrix seeds reaction shortcuts (`✅` allow once, `❌` deny, `♾️` allow always) while still leaving `/approve ...` commands in the message as a fallback.

## Where it applies

Exec approvals are enforced **locally on the execution host**: the **Gateway host** maps to the `openclaw` process on the gateway machine, and a **Node host** maps to the node runner (macOS companion app or headless node host).

### Trust model

The trust model frames exactly what approvals do and do not defend:

- Gateway-authenticated callers are trusted operators for that Gateway.
- Paired nodes extend that trusted operator capability onto the node host.
- Exec approvals reduce accidental execution risk, but are **not** a per-user auth boundary or filesystem read-only policy.
- Once approved, a command can mutate files according to the selected host or sandbox filesystem permissions.
- Approved node-host runs bind canonical execution context: canonical cwd, exact argv, env binding when present, and pinned executable path when applicable.
- For shell scripts and direct interpreter/runtime file invocations, OpenClaw also tries to bind one concrete local file operand. If that bound file changes after approval but before execution, the run is denied instead of executing drifted content.
- File binding is intentionally best-effort, **not** a complete semantic model of every interpreter/runtime loader path. If approval mode cannot identify exactly one concrete local file to bind, it refuses to mint an approval-backed run instead of pretending full coverage.

### macOS split

On macOS the enforcement is split across two processes: the **node host service** forwards `system.run` to the **macOS app** over local IPC, and the **macOS app** enforces approvals and executes the command in UI context.

## Settings and storage

Approvals live in a local JSON file on the execution host. When `OPENCLAW_STATE_DIR` is set, the file follows that state directory; otherwise it uses the default OpenClaw state directory:

```text
$OPENCLAW_STATE_DIR/exec-approvals.json
# otherwise
~/.openclaw/exec-approvals.json
```

The default approval socket follows the same root: `$OPENCLAW_STATE_DIR/exec-approvals.sock`, or `~/.openclaw/exec-approvals.sock` when the variable is unset. The example schema shows the `version`, `socket` (with `path` + base64url `token`), `defaults`, and per-agent `agents` blocks (each carrying `security`/`ask`/`askFallback`/`autoAllowSkills` plus its `allowlist`):

```json
{
  "version": 1,
  "socket": {
    "path": "~/.openclaw/exec-approvals.sock",
    "token": "base64url-token"
  },
  "defaults": {
    "security": "deny",
    "ask": "on-miss",
    "askFallback": "deny",
    "autoAllowSkills": false
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "askFallback": "deny",
      "autoAllowSkills": true,
      "allowlist": [
        {
          "id": "B0C8C0B3-2C2D-4F8A-9A3C-5A4B3C2D1E0F",
          "pattern": "~/Projects/**/bin/rg",
          "source": "allow-always",
          "commandText": "rg -n TODO",
          "lastUsedAt": 1737150000000,
          "lastUsedCommand": "rg -n TODO",
          "lastResolvedPath": "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

## Policy knobs

### `tools.exec.mode`

`tools.exec.mode` is the **preferred normalized policy surface** for host exec. Its values are: `deny` — block host exec; `allowlist` — run only allowlisted commands without asking; `ask` — use allowlist policy and ask on misses; `auto` — use allowlist policy, run deterministic matches directly, and send approval misses through OpenClaw's native auto reviewer before falling back to a human approval route; and `full` — run host exec without approval prompts. Legacy `tools.exec.security` / `tools.exec.ask` remain supported and still win when set at the narrower session or agent scope.

### `exec.security`

The `security` field is typed `"deny" | "allowlist" | "full"`: `deny` blocks all host exec requests; `allowlist` allows only allowlisted commands; `full` allows everything (equivalent to elevated).

### `exec.ask`

The `ask` field is typed `"off" | "on-miss" | "always"` and configures the baseline approval prompt behavior from `tools.exec.ask` and host approvals defaults. The per-call `ask` tool parameter (the Exec tool's `parameters`, documented in [oc_tools_exec_usage](oc_tools_exec_usage.md)) can only **harden** that baseline, and channel-origin model calls ignore it when the effective host ask is `off`. Values: `off` — never prompt; `on-miss` — prompt only when the allowlist does not match; `always` — prompt on every command (`allow-always` durable trust does **not** suppress prompts when the effective ask mode is `always`).

### `askFallback`

The `askFallback` field is typed `"deny" | "allowlist" | "full"` and is the resolution when a prompt is required but no UI is reachable. If this field is omitted, OpenClaw defaults to `deny`. Values: `deny` — block; `allowlist` — allow only if the allowlist matches; `full` — allow.

### `tools.exec.strictInlineEval`

`strictInlineEval` is a boolean. When `true`, OpenClaw treats inline code-eval forms as approval-only **even if the interpreter binary itself is allowlisted** — a defense-in-depth measure for interpreter loaders that do not map cleanly to one stable file operand. The forms strict mode catches include `python -c`; `node -e`, `node --eval`, `node -p`; `ruby -e`; `perl -e`, `perl -E`; `php -r`; `lua -e`; and `osascript -e`. In strict mode these commands still need explicit approval, and `allow-always` does not persist new allowlist entries for them automatically.

### `tools.exec.commandHighlighting`

`commandHighlighting` is a boolean defaulting to `false` that controls **only presentation** in exec approval prompts. When enabled, OpenClaw may attach parser-derived command spans so Web approval prompts can highlight command tokens. This setting does **not** change `security`, `ask`, allowlist matching, strict inline-eval behavior, approval forwarding, or command execution. It can be set globally under `tools.exec.commandHighlighting` or per agent under `agents.list[].tools.exec.commandHighlighting`.

**Source**: OpenClaw documentation — `tools/exec-approvals` (mirror `inbox/openclaw_docs/tools/exec-approvals.md`)
**Last Updated**: 2026-06-22
**Status**: Active
