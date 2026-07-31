---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - exec
keywords:
  - openclaw exec tool
  - exec parameters command host pty
  - exec host auto sandbox gateway node routing
  - exec session overrides /exec
  - exec authorized senders authorization model
  - exec approval-pending status
  - background process yieldMs send-keys
topics:
  - OpenClaw
  - Exec Tool
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/exec
access_control_group: ["general"]
---

# OpenClaw — Exec Tool Usage (Parameters, Host Routing, `/exec`, Authorization)

## Overview

This note documents the invocation surface of OpenClaw's `exec` tool — the mutating shell tool that runs commands in the workspace (creating, editing, or deleting files wherever the selected host or sandbox filesystem permits). It covers the tool's parameters, the `host=auto/sandbox/gateway/node` routing rules and shell/PATH notes, the `/exec` per-session overrides, the authorized-sender authorization model, the `approval-pending` return contract (pointer to the approvals notes), and the foreground/background/`process` examples — mirroring the invocation half of the `tools/exec` source page. The configuration knobs (`tools.exec.*`), PATH handling, allowlist + safe bins, and the `apply_patch` subtool live in the split sibling note `oc_tools_exec_config`.

## What `exec` Is

`exec` runs shell commands in the workspace and is a mutating shell surface: commands can create, edit, or delete files wherever the selected host or sandbox filesystem permits. Disabling OpenClaw filesystem tools such as `write`, `edit`, or `apply_patch` does NOT make `exec` read-only. The tool supports foreground plus background execution via `process`; if `process` is disallowed, `exec` runs synchronously and ignores `yieldMs`/`background`. Background sessions are scoped per agent, so `process` only sees sessions from the same agent.

## Parameters

The `exec` tool accepts the following parameters (defaults and types copied verbatim from source):

- `command` (string, required) — Shell command to run.
- `workdir` (string, default `cwd`) — Working directory for the command.
- `env` (object) — Key/value environment overrides merged on top of the inherited environment.
- `yieldMs` (number, default `10000`) — Auto-background the command after this delay (ms).
- `background` (boolean, default `false`) — Background the command immediately instead of waiting for `yieldMs`.
- `timeout` (number, default `tools.exec.timeoutSec`) — Override the configured exec timeout for this call. Set `timeout: 0` only when the command should run without the exec process timeout.
- `pty` (boolean, default `false`) — Run in a pseudo-terminal when available. Use for TTY-only CLIs, coding agents, and terminal UIs.
- `host` (`'auto' | 'sandbox' | 'gateway' | 'node'`, default `auto`) — Where to execute. `auto` resolves to `sandbox` when a sandbox runtime is active and `gateway` otherwise.
- `security` (`'deny' | 'allowlist' | 'full'`) — Ignored for normal tool calls. `gateway` / `node` security is controlled by `tools.exec.security` and the host approvals file; elevated mode can force `security=full` only when the operator explicitly grants elevated access.
- `ask` (`'off' | 'on-miss' | 'always'`) — The baseline ask mode comes from `tools.exec.ask` and host approvals. For channel-origin model calls, per-call `ask` is ignored when the effective host ask is `off`; otherwise it can only harden to a stricter mode. Trusted internal/API callers that construct exec tools with an explicit `ask` value are unchanged.
- `node` (string) — Node id/name when `host=node`.
- `elevated` (boolean, default `false`) — Request elevated mode — escape the sandbox onto the configured host path. `security=full` is forced only when elevated resolves to `full`.

## Host Routing, Shell, and Execution Notes

The `host` parameter selects an execution target, not a hostname. Its routing and shell behavior follow these source notes:

- `host` defaults to `auto`: sandbox when a sandbox runtime is active for the session, otherwise gateway.
- `host` only accepts `auto`, `sandbox`, `gateway`, or `node`. It is not a hostname selector; hostname-like values are rejected before the command runs.
- `auto` is the default routing strategy, not a wildcard. Per-call `host=node` is allowed from `auto`; per-call `host=gateway` is only allowed when no sandbox runtime is active.
- `tools.exec.mode` is the normalized policy knob. Values are `deny`, `allowlist`, `ask`, `auto`, and `full`. `auto` runs deterministic allowlist/safe-bin matches directly and routes every remaining exec approval case through OpenClaw's native auto reviewer before asking a human. `ask` / `ask=always` still asks a human every time.
- With no extra config, `host=auto` still "just works": no sandbox means it resolves to `gateway`; a live sandbox means it stays in the sandbox.
- `elevated` escapes the sandbox onto the configured host path: `gateway` by default, or `node` when `tools.exec.host=node` (or the session default is `host=node`). It is only available when elevated access is enabled for the current session/provider.
- `gateway`/`node` approvals are controlled by the host approvals file.
- `node` requires a paired node (companion app or headless node host). If multiple nodes are available, set `exec.node` or `tools.exec.node` to select one. `exec host=node` is the only shell-execution path for nodes; the legacy `nodes.run` wrapper has been removed.
- `timeout` applies to foreground, background, `yieldMs`, gateway, sandbox, and node `system.run` execution. If omitted, OpenClaw uses `tools.exec.timeoutSec`; explicit `timeout: 0` disables the exec process timeout for that call.
- On non-Windows hosts, exec uses `SHELL` when set; if `SHELL` is `fish`, it prefers `bash` (or `sh`) from `PATH` to avoid fish-incompatible scripts, then falls back to `SHELL` if neither exists. On Windows hosts, exec prefers PowerShell 7 (`pwsh`) discovery (Program Files, ProgramW6432, then PATH), then falls back to Windows PowerShell 5.1.
- On non-Windows gateway hosts, bash and zsh exec commands use a startup snapshot: OpenClaw captures sourceable aliases/functions and a small safe environment set from shell startup files into `$OPENCLAW_STATE_DIR/cache/shell-snapshots/`, then sources that snapshot before each exec command. Secret-looking variables are excluded; sandbox and node exec do not use this snapshot. Set `OPENCLAW_EXEC_SHELL_SNAPSHOT=0` in the Gateway process environment to disable this snapshot path.
- Host execution (`gateway`/`node`) rejects `env.PATH` and loader overrides (`LD_*`/`DYLD_*`) to prevent binary hijacking or injected code.
- OpenClaw sets `OPENCLAW_SHELL=exec` in the spawned command environment (including PTY and sandbox execution) so shell/profile rules can detect exec-tool context.
- `openclaw channels login` is blocked from `exec` because it is an interactive channel-auth flow; run it in a terminal on the gateway host, or use the channel-native login tool from chat when one exists.
- Sandboxing is **off by default**. If sandboxing is off, implicit `host=auto` resolves to `gateway`. Explicit `host=sandbox` still fails closed instead of silently running on the gateway host. Enable sandboxing or use `host=gateway` with approvals.
- Script preflight checks (for common Python/Node shell-syntax mistakes) only inspect files inside the effective `workdir` boundary. If a script path resolves outside `workdir`, preflight is skipped for that file.
- For long-running work that starts now, start it once and rely on automatic completion wake when it is enabled and the command emits output or fails. Use `process` for logs, status, input, or intervention; do not emulate scheduling with sleep loops, timeout loops, or repeated polling. For work that should happen later or on a schedule, use cron instead of `exec` sleep/delay patterns.

## Session Overrides (`/exec`)

Use `/exec` to set **per-session** defaults for `host`, `security`, `ask`, and `node`. Send `/exec` with no arguments to show the current values.

```
/exec host=auto security=allowlist ask=on-miss node=mac-1
```

## Authorization Model

`/exec` is only honored for **authorized senders** (channel allowlists/pairing plus `commands.useAccessGroups`). It updates **session state only** and does not write config. Authorized external channel senders may set these session defaults. Internal gateway/webchat clients need `operator.admin` to persist them. To hard-disable exec, deny it via tool policy (`tools.deny: ["exec"]` or per-agent). Host approvals still apply unless you explicitly set `security=full` and `ask=off`.

## Exec Approvals (companion app / node host)

Sandboxed agents can require per-request approval before `exec` runs on the gateway or node host (see `oc_tools_exec_approvals_policy` for the policy, allowlist, and UI flow). When approvals are required, the exec tool returns immediately with `status: "approval-pending"` and an approval id. Once approved (or denied / timed out), the Gateway emits command progress and completion system events only for approved runs (`Exec running` / `Exec finished`). Denied or timed-out approvals are terminal and do not wake the agent session with a denial system event. On channels with native approval cards/buttons, the agent should rely on that native UI first and only include a manual `/approve` command when the tool result explicitly says chat approvals are unavailable or manual approval is the only path.

## Examples

Foreground:

```json
{ "tool": "exec", "command": "ls -la" }
```

Background + poll (polling is for on-demand status, not waiting loops; if automatic completion wake is enabled, the command can wake the session when it emits output or fails):

```json
{"tool":"exec","command":"npm run build","yieldMs":1000}
{"tool":"process","action":"poll","sessionId":"<id>"}
```

Send keys (tmux-style), submit (send CR only), and paste (bracketed by default):

```json
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Enter"]}
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["C-c"]}
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Up","Up","Enter"]}
{ "tool": "process", "action": "submit", "sessionId": "<id>" }
{ "tool": "process", "action": "paste", "sessionId": "<id>", "text": "line1\nline2\n" }
```

**Source**: OpenClaw documentation — `tools/exec` (mirror `inbox/openclaw_docs/tools/exec.md`)
**Last Updated**: 2026-06-22
**Status**: Active
