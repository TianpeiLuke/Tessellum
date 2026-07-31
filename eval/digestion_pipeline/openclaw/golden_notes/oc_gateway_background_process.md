---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - exec
keywords:
  - openclaw exec tool
  - process tool background sessions
  - exec yieldMs background timeout
  - child process bridging orphan
  - tools.exec config keys
  - OPENCLAW_SHELL exec
  - exec elevated sandbox
  - process poll log kill
topics:
  - OpenClaw
  - Background Process
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/gateway/background-process
access_control_group: ["general"]
---

# OpenClaw — Background exec and the process Tool

## Overview

This note covers the OpenClaw gateway's **background-process model**: how shell commands run through the `exec` tool, how long-running tasks are auto-backgrounded and kept in memory, how the `process` tool manages those background sessions, and how the child-process bridge helper avoids orphaned processes. It mirrors the `gateway/background-process` source page in full — the `exec` tool, child-process bridging, the `process` tool, and worked examples. OpenClaw runs shell commands through the `exec` tool and keeps long-running tasks in memory, while the `process` tool manages those background sessions.

## exec tool

The `exec` tool runs a shell command and is the gateway's primary command-execution surface. Its key parameters are: `command` (required); `yieldMs` (default `10000`) which auto-backgrounds the run after this delay; `background` (bool) which backgrounds immediately; `timeout` (seconds, default `tools.exec.timeoutSec`) which kills the process after the timeout, where setting `timeout: 0` is the only way to disable the exec process timeout for that call; `elevated` (bool) which runs outside the sandbox if elevated mode is enabled/allowed (`gateway` by default, or `node` when the exec target is `node`); `pty: true` when a real TTY is needed; plus `workdir` and `env`.

Its behavior is as follows. Foreground runs return output directly. When backgrounded — whether explicitly or by the `yieldMs` timeout — the tool returns `status: "running"` plus a `sessionId` and a short tail. Background and `yieldMs` runs inherit `tools.exec.timeoutSec` unless the call provides an explicit `timeout`. Output is kept in memory until the session is polled or cleared. If the `process` tool is disallowed, `exec` runs synchronously and ignores `yieldMs`/`background`. Spawned exec commands receive `OPENCLAW_SHELL=exec` for context-aware shell/profile rules. For long-running work that starts now, start it once and rely on automatic completion wake when it is enabled and the command emits output or fails; if automatic completion wake is unavailable, or you need quiet-success confirmation for a command that exited cleanly without output, use `process` to confirm completion. Do not emulate reminders or delayed follow-ups with `sleep` loops or repeated polling — use cron for future work.

## Child process bridging

When spawning long-running child processes outside the exec/process tools (for example, CLI respawns or gateway helpers), attach the **child-process bridge helper** so termination signals are forwarded and listeners are detached on exit/error. This avoids orphaned processes on systemd and keeps shutdown behavior consistent across platforms.

The background-process model is tuned by environment overrides: `OPENCLAW_BASH_YIELD_MS` sets the default yield (ms); `OPENCLAW_BASH_MAX_OUTPUT_CHARS` sets the in-memory output cap (chars); `OPENCLAW_BASH_PENDING_MAX_OUTPUT_CHARS` sets the pending stdout/stderr cap per stream (chars); `OPENCLAW_BASH_JOB_TTL_MS` sets the TTL for finished sessions (ms, bounded to 1m–3h); and `OPENCLAW_PROCESS_INPUT_WAIT_IDLE_MS` sets the idle-output threshold before writable background sessions are marked as likely waiting for input (default `15000` ms).

Config keys are the preferred control surface: `tools.exec.backgroundMs` (default `10000`); `tools.exec.timeoutSec` (default `1800`); `tools.exec.cleanupMs` (default `1800000`); `tools.exec.notifyOnExit` (default `true`) which enqueues a system event plus a heartbeat request when a backgrounded exec exits; and `tools.exec.notifyOnExitEmptySuccess` (default `false`) which, when true, also enqueues completion events for successful backgrounded runs that produced no output.

## process tool

The `process` tool manages backgrounded exec sessions through these actions: `list` (running + finished sessions); `poll` (drain new output for a session, also reporting exit status); `log` (read the aggregated output and show input recovery hints, supporting `offset` + `limit`); `write` (send stdin via `data`, optional `eof`); `send-keys` (send explicit key tokens or bytes to a PTY-backed session); `submit` (send Enter / carriage return to a PTY-backed session); `paste` (send literal text, optionally wrapped in bracketed paste mode); `kill` (terminate a background session); `clear` (remove a finished session from memory); and `remove` (kill if running, otherwise clear if finished).

Several notes govern session lifecycle and visibility. Only backgrounded sessions are listed/persisted in memory, and sessions are lost on process restart (no disk persistence). Session logs are only saved to chat history if you run `process poll`/`log` and the tool result is recorded. `process` is scoped per agent — it only sees sessions started by that agent. Use `poll`/`log` for status, logs, quiet-success confirmation, or completion confirmation when automatic completion wake is unavailable. Use `log` before recovering an interactive CLI so the current transcript, stdin state, and input-wait hint are visible together. Use `write`/`send-keys`/`submit`/`paste`/`kill` when you need input or intervention.

The tool also derives display and paging behavior. `process list` includes a derived `name` (command verb + target) for quick scans. `process list`, `poll`, and `log` report `waitingForInput` only when the session still has writable stdin and has been idle longer than the input-wait threshold. `process log` uses line-based `offset`/`limit`: when both `offset` and `limit` are omitted it returns the last 200 lines and includes a paging hint; when `offset` is provided and `limit` is omitted it returns from `offset` to the end (not capped to 200). Polling is for on-demand status, not wait-loop scheduling — if the work should happen later, use cron instead.

## Examples

Run a long task and poll later (the `exec` call backgrounds after `yieldMs`, then `process poll` drains output):

```json
{ "tool": "exec", "command": "sleep 5 && echo done", "yieldMs": 1000 }
```

```json
{ "tool": "process", "action": "poll", "sessionId": "<id>" }
```

Inspect an interactive session before sending input:

```json
{ "tool": "process", "action": "log", "sessionId": "<id>" }
```

Start immediately in background, then send stdin and PTY keys, and submit the current line:

```json
{ "tool": "exec", "command": "npm run build", "background": true }
```

```json
{ "tool": "process", "action": "write", "sessionId": "<id>", "data": "y\n" }
```

```json
{ "tool": "process", "action": "send-keys", "sessionId": "<id>", "keys": ["C-c"] }
```

**Source**: OpenClaw documentation — `gateway/background-process` (mirror `inbox/openclaw_docs/gateway/background-process.md`)
**Last Updated**: 2026-06-22
**Status**: Active
