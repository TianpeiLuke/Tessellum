---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - daemon
keywords:
  - openclaw daemon command
  - gateway service lifecycle
  - daemon install start stop restart uninstall
  - daemon status health probe
  - secretref token drift check
  - launchd systemd schtasks service
  - safe restart skip-deferral
  - prefer openclaw gateway
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/daemon
access_control_group: ["general"]
---

# OpenClaw — `openclaw daemon` Service Lifecycle Command

## Overview

This note is the procedure reference for `openclaw daemon`, the legacy CLI alias for OpenClaw Gateway service management, mirroring the `cli/daemon` source page. `openclaw daemon ...` maps to the same service-control surface as `openclaw gateway ...` service commands, exposing the operator service lifecycle: `status`, `install`, `uninstall`, `start`, `stop`, and `restart`. It covers each subcommand, its per-subcommand options, the SecretRef-aware token-drift / health-probe checks the command runs, the safe-restart drain behavior, and the documentation's directive to prefer `openclaw gateway` going forward. The command installs the supervised service via the platform service manager (`launchd` / `systemd` / `schtasks`).

## Usage

The command surface is invoked as `openclaw daemon <subcommand>`:

```bash
openclaw daemon status
openclaw daemon install
openclaw daemon start
openclaw daemon stop
openclaw daemon restart
openclaw daemon uninstall
```

## Subcommands

Each subcommand controls one part of the supervised gateway service lifecycle:

- `status`: show service install state and probe Gateway health.
- `install`: install service (`launchd` / `systemd` / `schtasks`).
- `uninstall`: remove service.
- `start`: start service.
- `stop`: stop service.
- `restart`: restart service.

## Common options

Per-subcommand flags (from the source page's Common options):

- `status`: `--url`, `--token`, `--password`, `--timeout`, `--no-probe`, `--require-rpc`, `--deep`, `--json`
- `install`: `--port`, `--runtime <node|bun>`, `--token`, `--force`, `--json`
- `restart`: `--safe`, `--skip-deferral`, `--force`, `--wait <duration>`, `--json`
- lifecycle (`uninstall|start|stop`): `--json`

### Status: health probe and auth-ref resolution

`status` resolves configured auth SecretRefs for probe auth when possible. If a required auth SecretRef is unresolved in this command path, `daemon status --json` reports `rpc.authWarning` when probe connectivity/auth fails; pass `--token` / `--password` explicitly or resolve the secret source first. If the probe succeeds, unresolved auth-ref warnings are suppressed to avoid false positives.

### Status: deep scan and plugin-aware validation

`status --deep` adds a best-effort system-level service scan. When it finds other gateway-like services, human output prints cleanup hints and warns that one gateway per machine is still the normal recommendation. `status --deep` also runs config validation in plugin-aware mode and surfaces configured plugin manifest warnings (for example missing channel config metadata) so install and update smoke checks catch them. Default `status` keeps the fast read-only path that skips plugin validation.

### Token-drift checks (status / install)

On Linux systemd installs, `status` token-drift checks include both `Environment=` and `EnvironmentFile=` unit sources. Drift checks resolve `gateway.auth.token` SecretRefs using merged runtime env (service command env first, then process env fallback). If token auth is not effectively active (explicit `gateway.auth.mode` of `password` / `none` / `trusted-proxy`, or mode unset where password can win and no token candidate can win), token-drift checks skip config token resolution.

### Install: SecretRef validation and fail-closed rules

When token auth requires a token and `gateway.auth.token` is SecretRef-managed, `install` validates that the SecretRef is resolvable but does not persist the resolved token into service environment metadata. If token auth requires a token and the configured token SecretRef is unresolved, install fails closed. If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, install is blocked until mode is set explicitly. On macOS, `install` keeps LaunchAgent plists owner-only and loads managed service environment values through an owner-only file and wrapper instead of serializing API keys or auth-profile env refs into `EnvironmentVariables`.

### Multiple gateways on one host

If you intentionally run multiple gateways on one host, isolate ports, config/state, and workspaces; see the gateway runbook's multiple-gateways-same-host guidance.

### Restart: safe-restart and deferral

`restart --safe` asks the running Gateway to preflight active work and schedule one coalesced restart after active work drains. Plain `restart` keeps the existing service-manager behavior; `--force` remains the immediate override path. `restart --safe --skip-deferral` runs the OpenClaw-aware safe restart but bypasses the active-work deferral gate so the Gateway emits the restart immediately even when blockers are reported — an operator escape hatch when a stuck task run pins the safe restart; it requires `--safe`.

## Prefer

`openclaw daemon` is a legacy alias. Use the `openclaw gateway` command ([oc_cli_gateway_run](oc_cli_gateway_run.md); docs at `https://docs.openclaw.ai/cli/gateway`) for current docs and examples.

**Source**: OpenClaw documentation — `cli/daemon` (mirror `inbox/openclaw_docs/cli/daemon.md`)
**Last Updated**: 2026-06-22
**Status**: Active
