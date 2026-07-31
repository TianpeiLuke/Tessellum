---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - gateway
keywords:
  - openclaw gateway run
  - gateway.mode=local startup guard
  - gateway bind auth guardrail
  - openclaw gateway restart --safe
  - gateway restart skip-deferral
  - gateway install wrapper
  - managed gateway service lifecycle
  - secretref install validation
  - gateway profiling startup trace
topics:
  - OpenClaw
  - Gateway CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/gateway
access_control_group: ["general"]
---

# OpenClaw — Running and Operating the Gateway (`openclaw gateway`)

## Overview

This note is the operating procedure for OpenClaw's Gateway process from the CLI — running it in the foreground, restarting it safely, profiling its startup, and installing/managing it as a long-lived OS service. The Gateway is OpenClaw's WebSocket server (channels, nodes, sessions, hooks); all subcommands here live under `openclaw gateway …`. It mirrors the `cli/gateway` source page sections **Run the Gateway** (Startup behavior, Options), **Restart the Gateway** (Gateway profiling), and **Manage the Gateway service** (Install with a wrapper, Command options, Lifecycle behavior, Auth and SecretRefs at install time). The companion **[oc_cli_gateway_query](oc_cli_gateway_query.md)** covers querying/diagnosing a *running* Gateway (`health`/`status`/`probe`/`call`/`discover`) — that surface is not repeated here.

## Run the Gateway

Run a local Gateway process:

```bash
openclaw gateway
openclaw gateway run    # foreground alias
```

### Startup behavior (guardrails)

- By default, the Gateway **refuses to start unless `gateway.mode=local`** is set in `~/.openclaw/openclaw.json`. Use `--allow-unconfigured` for ad-hoc/dev runs.
- `openclaw onboard --mode local` and `openclaw setup` are expected to write `gateway.mode=local`. If the file exists but `gateway.mode` is missing, the Gateway treats that as a broken/clobbered config — it refuses to "guess local" and you should repair it instead of assuming local mode implicitly.
- **Binding beyond loopback without auth is blocked** (safety guardrail).
- `lan`, `tailnet`, and `custom` bind modes currently resolve over **IPv4-only BYOH paths**. IPv6-only BYOH is not natively supported on this path today; use an IPv4 sidecar or proxy if the host itself is IPv6-only.
- `SIGUSR1` triggers an in-process restart when authorized (`commands.restart` is enabled by default; set `commands.restart: false` to block manual restart, while gateway tool/config apply/update remain allowed).
- `SIGINT`/`SIGTERM` handlers stop the gateway process but do **not** restore custom terminal state. If you wrap the CLI with a TUI or raw-mode input, restore the terminal before exit.

### Options

These flags apply to `openclaw gateway` / `openclaw gateway run`:

- `--port <port>` — WebSocket port (default comes from config/env; usually `18789`).
- `--bind <loopback|lan|tailnet|auto|custom>` — listener bind mode (`lan`/`tailnet`/`custom` resolve over IPv4-only paths).
- `--auth <token|password>` — auth mode override.
- `--token <token>` — token override (also sets `OPENCLAW_GATEWAY_TOKEN` for the process).
- `--password <password>` — password override. *(See the inline-password warning under Restart.)*
- `--password-file <path>` — read the gateway password from a file.
- `--tailscale <off|serve|funnel>` — expose the Gateway via Tailscale.
- `--tailscale-reset-on-exit` — reset Tailscale serve/funnel config on shutdown.
- `--bind custom + gateway.customBindHost` — expects an IPv4 address today; for IPv6-only BYOH put an IPv4 sidecar/proxy in front and point OpenClaw at that endpoint.
- `--allow-unconfigured` — allow start without `gateway.mode=local`; bypasses the startup guard for ad-hoc/dev bootstrap only (does not write or repair the config file).
- `--dev` — create a dev config + workspace if missing (skips `BOOTSTRAP.md`).
- `--reset` — reset dev config + credentials + sessions + workspace (requires `--dev`).
- `--force` — kill any existing listener on the selected port before starting.
- `--verbose` — verbose logs.
- `--cli-backend-logs` — only show CLI backend logs in the console (and enable stdout/stderr).
- `--ws-log <auto|full|compact>` (default `auto`) — websocket log style.
- `--compact` — alias for `--ws-log compact`.
- `--raw-stream` — log raw model stream events to jsonl.
- `--raw-stream-path <path>` — raw stream jsonl path.

## Restart the Gateway

```bash
openclaw gateway restart
openclaw gateway restart --safe
openclaw gateway restart --safe --skip-deferral
openclaw gateway restart --force
```

`openclaw gateway restart --safe` asks the running Gateway to preflight active OpenClaw work before restarting. If queued operations, reply delivery, embedded runs, or task runs are active, the Gateway reports the blockers, **coalesces duplicate safe restart requests**, and restarts once the active work drains. Plain `restart` keeps the existing service-manager behavior for compatibility. Use `--force` only when you explicitly want the immediate override path.

`openclaw gateway restart --safe --skip-deferral` runs the same OpenClaw-aware coordinated restart as `--safe` but bypasses the active-work deferral gate, so the Gateway emits the restart immediately even when blockers are reported. It is the operator escape hatch for when a deferral has been pinned by a stuck task run and `--safe` alone would wait indefinitely. `--skip-deferral` requires `--safe`.

> **Warning (source):** Inline `--password` can be exposed in local process listings. Prefer `--password-file`, env, or a SecretRef-backed `gateway.auth.password`.

### Gateway profiling

Startup/restart performance is instrumented via env flags and built-in benchmarks:

- `OPENCLAW_GATEWAY_STARTUP_TRACE=1` — log phase timings during Gateway startup, including per-phase `eventLoopMax` delay and plugin lookup-table timings for installed-index, manifest registry, startup planning, and owner-map work.
- `OPENCLAW_GATEWAY_RESTART_TRACE=1` — log restart-scoped `restart trace:` lines for restart signal handling, active-work drain, shutdown phases, next start, ready timing, and memory metrics.
- `OPENCLAW_DIAGNOSTICS=timeline` with `OPENCLAW_DIAGNOSTICS_TIMELINE_PATH=<path>` — write a best-effort JSONL startup diagnostics timeline for external QA harnesses. The flag can also be enabled with `diagnostics.flags: ["timeline"]` in config; the path is still env-provided. Add `OPENCLAW_DIAGNOSTICS_EVENT_LOOP=1` to include event-loop samples.

Benchmarks run against the built CLI entry (run `pnpm build` first):

```bash
pnpm test:startup:gateway -- --runs 5 --warmup 1
pnpm test:restart:gateway -- --case skipChannels --runs 1 --restarts 5
```

The startup benchmark records first process output, `/healthz`, `/readyz`, startup trace timings, event-loop delay, and plugin lookup-table timing details. The restart benchmark (macOS or Linux) uses `SIGUSR1`, enables both startup and restart traces in the child process, and records next `/healthz`, next `/readyz`, downtime, ready timing, CPU, RSS, and restart trace metrics. Treat `/healthz` as liveness and `/readyz` as usable readiness; trace lines and benchmark output are for owner attribution — do not treat one trace span or one sample as a complete performance conclusion.

## Manage the Gateway service

Run the Gateway as a managed OS service (launchd/systemd/schtasks) via these lifecycle commands:

```bash
openclaw gateway install
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway uninstall
```

### Install with a wrapper

Use `--wrapper` when the managed service must start through another executable, for example a secrets-manager shim or a run-as helper. The wrapper receives the normal Gateway args and is responsible for eventually exec'ing `openclaw` (or Node) with those args.

```bash
cat > ~/.local/bin/openclaw-doppler <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
exec doppler run --project my-project --config production -- openclaw "$@"
EOF
chmod +x ~/.local/bin/openclaw-doppler

openclaw gateway install --wrapper ~/.local/bin/openclaw-doppler --force
openclaw gateway restart
```

You can also set the wrapper through the environment. `gateway install` validates that the path is an executable file, writes the wrapper into service `ProgramArguments`, and persists `OPENCLAW_WRAPPER` in the service environment for later forced reinstalls, updates, and doctor repairs:

```bash
OPENCLAW_WRAPPER="$HOME/.local/bin/openclaw-doppler" openclaw gateway install --force
openclaw doctor
```

To remove a persisted wrapper, clear `OPENCLAW_WRAPPER` while reinstalling: `OPENCLAW_WRAPPER= openclaw gateway install --force` then `openclaw gateway restart`.

### Command options

Per-command flag sets for the service lifecycle:

- `gateway status`: `--url`, `--token`, `--password`, `--timeout`, `--no-probe`, `--require-rpc`, `--deep`, `--json`
- `gateway install`: `--port`, `--runtime <node|bun>`, `--token`, `--wrapper <path>`, `--force`, `--json`
- `gateway restart`: `--safe`, `--skip-deferral`, `--force`, `--wait <duration>`, `--json`
- `gateway uninstall|start`: `--json`
- `gateway stop`: `--disable`, `--json`

### Lifecycle behavior

- Use `gateway restart` to restart a managed service. **Do not chain `gateway stop` and `gateway start` as a restart substitute.**
- On macOS, `gateway stop` uses `launchctl bootout` by default, which removes the LaunchAgent from the current boot session without persisting a disable — KeepAlive auto-recovery remains active for future crashes and `gateway start` re-enables cleanly without a manual `launchctl enable`. Pass `--disable` to persistently suppress KeepAlive and RunAtLoad so the gateway does not respawn until the next explicit `gateway start`; use this when a manual stop should survive reboots or system restarts.
- `gateway restart --safe` asks the running Gateway to preflight active OpenClaw work and defer the restart until reply delivery, embedded runs, and task runs drain. `--safe` cannot be combined with `--force` or `--wait`.
- `gateway restart --wait 30s` overrides the configured restart drain budget for that restart. Bare numbers are milliseconds; units such as `s`, `m`, and `h` are accepted; `--wait 0` waits indefinitely.
- `gateway restart --safe --skip-deferral` runs the OpenClaw-aware safe restart but bypasses the deferral gate so the Gateway emits the restart immediately even when blockers are reported — operator escape hatch for stuck-task-run deferrals; requires `--safe`.
- `gateway restart --force` skips the active-work drain and restarts immediately. Use it when an operator has already inspected the listed task blockers and wants the gateway back now.
- Lifecycle commands accept `--json` for scripting.

### Auth and SecretRefs at install time

- When token auth requires a token and `gateway.auth.token` is SecretRef-managed, `gateway install` validates that the SecretRef is resolvable but does **not** persist the resolved token into service environment metadata.
- If token auth requires a token and the configured token SecretRef is unresolved, install **fails closed** instead of persisting fallback plaintext.
- For password auth on `gateway run`, prefer `OPENCLAW_GATEWAY_PASSWORD`, `--password-file`, or a SecretRef-backed `gateway.auth.password` over inline `--password`.
- In inferred auth mode, shell-only `OPENCLAW_GATEWAY_PASSWORD` does **not** relax install token requirements; use durable config (`gateway.auth.password` or config `env`) when installing a managed service.
- If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, install is **blocked** until mode is set explicitly.

**Source**: OpenClaw documentation — `cli/gateway` (mirror `inbox/openclaw_docs/cli/gateway.md`)
**Last Updated**: 2026-06-22
**Status**: Active
