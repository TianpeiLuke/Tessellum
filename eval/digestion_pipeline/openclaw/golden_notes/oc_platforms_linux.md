---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - linux
keywords:
  - openclaw linux gateway
  - linux vps quick path
  - openclaw onboard install-daemon
  - systemd user service openclaw-gateway
  - ssh tunnel 18789 gateway
  - oom_score_adj 1000 child
  - openclaw doctor repair migrate
  - node 24 recommended runtime
topics:
  - OpenClaw
  - Linux Platform
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/linux
access_control_group: ["general"]
---

# OpenClaw — Running the Gateway on Linux

## Overview

This procedure note covers running the OpenClaw **Gateway** on Linux, mirroring the `platforms/linux` source page. It documents the recommended runtime (Node, not Bun), the beginner VPS quick path (install + onboard daemon + SSH tunnel + authenticate the dashboard), where to follow install and gateway runbook flows, how to install the Gateway as a service via the CLI, the canonical minimal `systemd` **user** unit template (with enable), and Linux memory-pressure / OOM-kill biasing (raising transient child `oom_score_adj` to `1000`) plus how to verify it. Native Linux companion **node** apps do not yet exist — the Gateway is supported, mobile/companion nodes are covered by the sibling platform notes. Every command, flag, path, and env var below is reproduced verbatim from the source page.

## Runtime support and recommendation

The Gateway is fully supported on Linux. **Node is the recommended runtime.** Bun is *not* recommended for the Gateway because of WhatsApp/Telegram bugs. Native Linux companion apps are planned, and contributions are welcome if you want to help build one — so on Linux today you run the gateway-host side, not a packaged companion node app.

## Beginner quick path (VPS)

The fastest way to bring up a Linux Gateway on a VPS, then reach its dashboard from a laptop over an SSH tunnel:

1. Install Node 24 (recommended; Node 22 LTS, currently `22.19+`, still works for compatibility).
2. `npm i -g openclaw@latest`
3. `openclaw onboard --install-daemon`
4. From your laptop: `ssh -N -L 18789:127.0.0.1:18789 <user>@<host>`
5. Open `http://127.0.0.1:18789/` and authenticate with the configured shared secret (token by default; password if you set `gateway.auth.mode: "password"`).

The full Linux server guide is the *Linux Server* (`/vps`) page, and a step-by-step VPS example is the *exe.dev* (`/install/exe-dev`) walkthrough. The SSH local-forward (`-N -L 18789:127.0.0.1:18789`) maps the laptop's loopback port to the VPS gateway's loopback WebSocket/HTTP port `18789`, so the dashboard at `http://127.0.0.1:18789/` is reached without exposing the gateway publicly.

## Install

Linux install and update flows are documented on dedicated pages (link-outs, not duplicated here):

- *Getting Started* — `/start/getting-started`
- *Install & updates* — `/install/updating`
- Optional flows: *Bun (experimental)* `/install/bun`, *Nix* `/install/nix`, *Docker* `/install/docker`

## Gateway

Operating and configuring the gateway is covered by the gateway runbook (link-outs):

- *Gateway runbook* — `/gateway`
- *Configuration* — `/gateway/configuration`

## Gateway service install (CLI)

To install the Gateway as a managed service, use one of these CLI entry points (any one):

```
openclaw onboard --install-daemon
openclaw gateway install
openclaw configure
```

When using `openclaw configure`, select **Gateway service** when prompted. To repair or migrate an existing install, run:

```
openclaw doctor
```

## System control (systemd user unit)

OpenClaw installs a `systemd` **user** service by default. Use a **system** service for shared or always-on servers. `openclaw gateway install` and `openclaw onboard --install-daemon` already render the current canonical unit for you; write one by hand only when you need a custom system/service-manager setup. The full service guidance lives in the *Gateway runbook* (`/gateway`).

Minimal setup — create `~/.config/systemd/user/openclaw-gateway[-<profile>].service`:

```
[Unit]
Description=OpenClaw Gateway (profile: <profile>, v<version>)
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

Then enable it:

```
systemctl --user enable --now openclaw-gateway[-<profile>].service
```

Note the unit fields reproduced verbatim: `Restart=always` with `RestartSec=5` for auto-restart, `SuccessExitStatus=0 143` (143 = SIGTERM-clean shutdown), `KillMode=control-group`, and `WantedBy=default.target` so the user unit starts on the user's default target.

## Memory pressure and OOM kills

On Linux, the kernel chooses an OOM victim when a host, VM, or container cgroup runs out of memory. The Gateway can be a poor victim because it owns long-lived sessions and channel connections, so OpenClaw biases transient child processes to be killed before the Gateway when possible.

For eligible Linux child spawns, OpenClaw starts the child through a short `/bin/sh` wrapper that raises the child's own `oom_score_adj` to `1000`, then `exec`s the real command. This is an unprivileged operation because the child is only increasing its own OOM-kill likelihood. Covered child process surfaces include: supervisor-managed command children, PTY shell children, MCP stdio server children, and OpenClaw-launched browser/Chrome processes.

The wrapper is Linux-only and is skipped when `/bin/sh` is unavailable. It is also skipped if the child env sets `OPENCLAW_CHILD_OOM_SCORE_ADJ=0`, `false`, `no`, or `off`. To verify a covered child process:

```bash
cat /proc/<child-pid>/oom_score_adj
```

The expected value for covered children is `1000`; the Gateway process should keep its normal score, usually `0`. This does not replace normal memory tuning — if a VPS or container repeatedly kills children, increase the memory limit, reduce concurrency, or add stronger resource controls such as systemd `MemoryMax=` or container-level memory limits.

**Source**: OpenClaw documentation — `platforms/linux` (mirror `inbox/openclaw_docs/platforms/linux.md`)
**Last Updated**: 2026-06-22
**Status**: Active
