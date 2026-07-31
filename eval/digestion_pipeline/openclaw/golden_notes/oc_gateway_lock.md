---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - gateway_lock
keywords:
  - openclaw gateway lock
  - single instance gateway guard
  - gateway lock file
  - exclusive websocket bind
  - GatewayLockError EADDRINUSE
  - ws 127.0.0.1 18789
  - stale lock reclaim
  - systemd RestartPreventExitStatus 78
topics:
  - OpenClaw
  - Gateway Lock
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/gateway-lock
access_control_group: ["general"]
---

# OpenClaw — The Gateway Single-Instance Lock

## Overview

This note models the OpenClaw **gateway lock**: the single-instance guard that guarantees only one gateway process runs per base port on a host, built from a per-config lock file plus an exclusive WebSocket listener bind. It mirrors the `gateway/gateway-lock` source page, covering why the guard exists, the lock-file-plus-bind mechanism (including stale-lock reclaim), the `GatewayLockError` / `EADDRINUSE` error surface, and the operational behavior under a service supervisor (systemd exit-code 78, macOS PID guard).

The lock is a **model** — a small invariant-enforcing mechanism with defined startup, conflict, and shutdown states — rather than a step-by-step procedure. Its single guarantee: a healthy gateway holding the control port stays in control, and any second starter either reclaims a dead owner's lock or fails fast with a clear error.

## Why the Lock Exists

The guard solves three problems the source page enumerates:

- **One instance per base port per host.** Only one gateway instance may run per base port on the same host; additional gateways must use isolated profiles and unique ports.
- **Crash resilience.** The guard must survive crashes / `SIGKILL` without leaving stale lock files that would permanently block a restart.
- **Fail-fast on conflict.** When the control port is already occupied, startup must fail fast with a clear error rather than hang or silently mis-bind.

## Mechanism: Lock File + Exclusive WebSocket Bind

The guard is a two-part mechanism — a state lock file and an exclusive TCP listener — evaluated in a fixed startup order:

1. The gateway first **acquires a per-config lock file** under the state lock directory and **probes the configured port** for an existing listener.
2. **Stale-lock reclaim:** if the recorded lock owner is gone, the port is free, or the lock is stale, startup **reclaims the lock and continues**. This is what lets the gateway survive a crash/`SIGKILL` — a dead owner's lock does not permanently block a restart.
3. The gateway then **binds the HTTP/WebSocket listener** (default `ws://127.0.0.1:18789`) using an **exclusive TCP listener**. The exclusive bind is the authoritative enforcement point: the OS itself rejects a second binder.
4. If the bind fails with `EADDRINUSE`, startup throws a `GatewayLockError` (see Error Surface below).
5. **On shutdown** the gateway closes the HTTP/WebSocket server and **removes the lock file**, returning the port and lock to a clean state for the next start.

The lock file and the port probe are the cooperative, process-aware layer; the exclusive bind is the hard, OS-enforced layer that catches any starter that bypassed or raced the lock-file check.

## Error Surface

Two distinct `GatewayLockError` forms are thrown at the bind step:

- **Port already held by a gateway** — if another process holds the port, startup throws:
  `GatewayLockError("another gateway instance is already listening on ws://127.0.0.1:<port>")`.
- **Other bind failures** — surface as:
  `GatewayLockError("failed to bind gateway socket on ws://127.0.0.1:<port>: …")`.

Note that the port-occupied error is identical whether the holder is another gateway instance or an unrelated process occupying the same port — the message says "another gateway instance is already listening," but the underlying `EADDRINUSE` does not distinguish the two cases.

## Operational Notes

- **Port occupied by a non-gateway process.** If the port is occupied by *another* process, the error is the same; free the port or choose another with `openclaw gateway --port <port>`.
- **Under a service supervisor.** A new gateway process that sees an existing **healthy `/healthz` responder** leaves that process in control. On **systemd**, the duplicate starter exits with **code 78**, so the default **`RestartPreventExitStatus=78`** stops **`Restart=always`** from looping on a lock or `EADDRINUSE` conflict. If the existing process never becomes healthy, retries are **bounded** and startup fails with a clear lock error instead of looping forever.
- **macOS PID guard.** The macOS app still maintains its own lightweight **PID guard** before spawning the gateway; the runtime lock is enforced by the lock file plus the HTTP/WebSocket bind. The PID guard and the runtime lock are complementary layers, not a single mechanism.

**Source**: OpenClaw documentation — `gateway/gateway-lock` (mirror `inbox/openclaw_docs/gateway/gateway-lock.md`)
**Last Updated**: 2026-06-22
**Status**: Active
