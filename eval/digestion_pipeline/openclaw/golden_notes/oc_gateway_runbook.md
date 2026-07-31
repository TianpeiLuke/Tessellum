---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - runbook
keywords:
  - openclaw gateway runbook
  - openclaw gateway start status
  - openclaw gateway install restart stop
  - multiple gateways same host
  - gateway remote access ssh tunnel tailscale
  - launchd systemd scheduled task supervision
  - gateway liveness readiness gap recovery
  - gateway common failure signatures
  - openclaw dev profile gateway
topics:
  - OpenClaw
  - Gateway Operations
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway
access_control_group: ["general"]
---

# OpenClaw — Gateway Day-1/Day-2 Runbook

## Overview

This note is the operator runbook for the OpenClaw **Gateway** service — the day-1 startup and day-2 operations procedures from the `gateway` source page. It covers the 5-minute local startup (start, verify health, validate channel readiness), the operator command set, running multiple isolated gateways on one host, remote access via Tailscale/VPN or SSH tunnel, supervised service install and lifecycle per OS (launchd / systemd / Scheduled Task), the dev profile quick path, the operational checks ladder (liveness / readiness / gap recovery), and the common failure signatures table. The runtime/protocol *model* of the gateway (always-on multiplexed process, OpenAI-compatible endpoints, port/bind precedence, hot-reload modes, protocol handshake, safety guarantees) is a separate concept note — see **[oc_gateway_runtime_protocol](oc_gateway_runtime_protocol.md)**.

## 5-minute local startup

The first-run startup is a three-step procedure: (1) start the Gateway, (2) verify service health, then (3) validate channel readiness. The start command picks the listen port; `--verbose` mirrors debug/trace to stdio; `--force` force-kills any listener already on the selected port before starting:

```bash
# Step 1 — start the Gateway
openclaw gateway --port 18789
openclaw gateway --port 18789 --verbose   # debug/trace mirrored to stdio
openclaw gateway --force                  # force-kill listener on the port, then start
# Step 2 — verify service health
openclaw gateway status
openclaw status
openclaw logs --follow
# Step 3 — validate channel readiness (live per-account probe)
openclaw channels status --probe
```

For Step 2, the healthy baseline is `Runtime: running`, `Connectivity probe: ok`, and a `Capability: ...` line that matches what you expect; use `openclaw gateway status --require-rpc` when you need read-scope RPC proof, not just reachability. For Step 3, a reachable gateway runs live per-account channel probes and optional audits, while an unreachable gateway makes the CLI fall back to config-only channel summaries instead of live probe output.

Gateway config reload watches the active config file path (resolved from profile/state defaults, or `OPENCLAW_CONFIG_PATH` when set); the default mode is `gateway.reload.mode="hybrid"`. After the first successful load the running process serves the active in-memory config snapshot, and a successful reload swaps that snapshot atomically. (Hot-reload mode semantics are documented in the runtime/protocol note.)

## Operator command set

The day-2 operator commands for managing a running or supervised gateway are:

```bash
openclaw gateway status
openclaw gateway status --deep   # adds a system-level service scan
openclaw gateway status --json
openclaw gateway install
openclaw gateway restart
openclaw gateway stop
openclaw secrets reload
openclaw logs --follow
openclaw doctor
```

`gateway status --deep` is for extra service discovery (LaunchDaemons / systemd system units / schtasks), not a deeper RPC health probe.

## Multiple gateways (same host)

Most installs should run one gateway per machine; a single gateway can host multiple agents and channels. You only need multiple gateways when you intentionally want isolation or a rescue bot.

Useful checks when investigating multiple gateways on a host, plus an example of two isolated instances:

```bash
# investigate co-resident gateways
openclaw gateway status --deep
openclaw gateway probe
# run two isolated instances (unique port + config + state)
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json OPENCLAW_STATE_DIR=~/.openclaw-a openclaw gateway --port 19001
OPENCLAW_CONFIG_PATH=~/.openclaw/b.json OPENCLAW_STATE_DIR=~/.openclaw-b openclaw gateway --port 19002
```

What to expect: `gateway status --deep` can report `Other gateway-like services detected (best effort)` and print cleanup hints when stale launchd/systemd/schtasks installs are still around. `gateway probe` can warn about `multiple reachable gateway identities` when distinct gateways answer, or when OpenClaw cannot prove reachable targets are the same gateway — an SSH tunnel, proxy URL, or configured remote URL to the same gateway is one gateway with multiple transports, even when transport ports differ. If that is intentional, isolate ports, config/state, and workspace roots per gateway.

Checklist per instance: a unique `gateway.port`, a unique `OPENCLAW_CONFIG_PATH`, a unique `OPENCLAW_STATE_DIR`, and a unique `agents.defaults.workspace`. Detailed setup is documented at the `/gateway/multiple-gateways` leaf page.

## Remote access

The preferred remote-access path is Tailscale/VPN; the fallback is an SSH tunnel. Open a loopback-forwarding tunnel:

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

Then connect clients locally to `ws://127.0.0.1:18789`. SSH tunnels do **not** bypass gateway auth: for shared-secret auth, clients still must send `token`/`password` even over the tunnel, and for identity-bearing modes the request still has to satisfy that auth path. See the `/gateway/remote`, `/gateway/authentication`, and `/gateway/tailscale` leaf pages for the full remote-access and auth configuration.

## Supervision and service lifecycle

Use supervised runs for production-like reliability. Each OS uses its native service manager; in all cases `openclaw gateway install` registers the service and `openclaw gateway status` / `restart` / `stop` manage it. The install/manage commands per OS:

```bash
# macOS (launchd) and the common manage commands
openclaw gateway install
openclaw gateway status
openclaw gateway restart
openclaw gateway stop
# Linux (systemd user)
systemctl --user enable --now openclaw-gateway[-<profile>].service
sudo loginctl enable-linger <user>   # persistence after logout
```

Use `openclaw gateway restart` for restarts — do not chain `openclaw gateway stop` and `openclaw gateway start` as a restart substitute. On macOS, `gateway stop` uses `launchctl bootout` by default; this removes the LaunchAgent from the current boot session without persisting a disable, so KeepAlive auto-recovery still works after unexpected crashes and `gateway start` re-enables cleanly. To persistently suppress auto-respawn across reboots, pass `--disable`: `openclaw gateway stop --disable`. LaunchAgent labels are `ai.openclaw.gateway` (default) or `ai.openclaw.<profile>` (named profile), and `openclaw doctor` audits and repairs service config drift. On Linux systemd-user, `openclaw gateway install` registers the unit and lingering keeps it running after logout. When you need a custom install path, a manual user-unit body is:

```ini
[Unit]
Description=OpenClaw Gateway
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway --port 18789
Restart=always
RestartSec=5
TimeoutStopSec=30
TimeoutStartSec=30
SuccessExitStatus=0 143
KillMode=control-group

[Install]
WantedBy=default.target
```

**Windows (native).** Native Windows managed startup uses a Scheduled Task named `OpenClaw Gateway` (or `OpenClaw Gateway (<profile>)` for named profiles); if Scheduled Task creation is denied, OpenClaw falls back to a per-user Startup-folder launcher that points at `gateway.cmd` inside the state directory. The operator commands are `openclaw gateway install`, `openclaw gateway status --json`, `openclaw gateway restart`, and `openclaw gateway stop`.

**Linux (system service).** For multi-user/always-on hosts, use a system unit installed under `/etc/systemd/system/openclaw-gateway[-<profile>].service` (same service body as the user unit; adjust `ExecStart=` if the `openclaw` binary lives elsewhere), then `sudo systemctl daemon-reload` and `sudo systemctl enable --now openclaw-gateway[-<profile>].service`. Do not also let `openclaw doctor --fix` install a user-level gateway service for the same profile/port — Doctor refuses that automatic install when it finds a system-level OpenClaw gateway service; use `OPENCLAW_SERVICE_REPAIR_POLICY=external` when the system unit owns the lifecycle.

## Dev profile quick path

For an isolated development gateway, run `openclaw --dev setup`, then `openclaw --dev gateway --allow-unconfigured`, then `openclaw --dev status`. Defaults include isolated state/config and base gateway port `19001`.

## Operational checks

The operational-check ladder runs from a bare transport probe up to channel readiness.

**Liveness.** Open a WS and send `connect`; expect a `hello-ok` response with a snapshot.

**Readiness.** Run the readiness ladder: `openclaw gateway status`, then `openclaw channels status --probe`, then `openclaw health`.

**Gap recovery.** Events are not replayed. On sequence gaps, refresh state (`health`, `system-presence`) before continuing.

## Common failure signatures

| Signature | Likely issue |
| --- | --- |
| `refusing to bind gateway ... without auth` | Non-loopback bind without a valid gateway auth path |
| `another gateway instance is already listening` / `EADDRINUSE` | Port conflict |
| `Gateway start blocked: set gateway.mode=local` | Config set to remote mode, or local-mode stamp is missing from a damaged config |
| `unauthorized` during connect | Auth mismatch between client and gateway |

For full diagnosis ladders, use the `/gateway/troubleshooting` leaf page.

**Source**: OpenClaw documentation — `gateway` (mirror `inbox/openclaw_docs/gateway.md`)
**Last Updated**: 2026-06-22
**Status**: Active
