---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - vps
keywords:
  - openclaw linux server vps
  - run gateway on cloud vps
  - tailnet only ssh hardening
  - shared company agent trust boundary
  - node_compile_cache startup tuning
  - openclaw_no_respawn systemd
  - openclaw vps provider picker
  - pair nodes to cloud gateway
topics:
  - OpenClaw
  - VPS / Linux Server Hosting
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/vps
access_control_group: ["general"]
---

# OpenClaw — Running the Gateway on a Linux Server / Cloud VPS

## Overview

This note is the procedure for running the OpenClaw **Gateway** on any Linux server or cloud VPS, mirroring the `vps` source page. It covers picking a hosting provider, how a cloud deployment is structured (the Gateway owns state on the VPS while you connect remotely), hardening the box's admin access before install, the trust boundary for a shared company agent, pairing local nodes to a cloud Gateway, and the generic small-VM / ARM startup tuning (`NODE_COMPILE_CACHE`, `OPENCLAW_NO_RESPAWN`, and a systemd unit checklist). The page positions the VPS as the source of truth that owns state and workspace, with the recommended secure default being a loopback-bound Gateway reached over an SSH tunnel or Tailscale Serve.

## Pick a provider

The page lists hosting-provider cards, each linking to its dedicated install guide (owned by the `install/*` docs, not duplicated here). The providers and their one-line descriptions are:

- **Railway** (`/install/railway`) — One-click, browser setup.
- **Northflank** (`/install/northflank`) — One-click, browser setup.
- **DigitalOcean** (`/install/digitalocean`) — Simple paid VPS.
- **Oracle Cloud** (`/install/oracle`) — Always Free ARM tier.
- **Fly.io** (`/install/fly`) — Fly Machines.
- **Hetzner** (`/install/hetzner`) — Docker on Hetzner VPS.
- **Hostinger** (`/install/hostinger`) — VPS with one-click setup.
- **GCP** (`/install/gcp`) — Compute Engine.
- **Azure** (`/install/azure`) — Linux VM.
- **exe.dev** (`/install/exe-dev`) — VM with HTTPS proxy.
- **Raspberry Pi** (`/install/raspberry-pi`) — ARM self-hosted.

**AWS (EC2 / Lightsail / free tier)** also works well. The page also points to a community video walkthrough at `x.com/techfrenAJ/status/2014934471095812547`, noting it is a community resource that may become unavailable.

## How cloud setups work

A cloud deployment is organized around the VPS owning all state:

- The **Gateway runs on the VPS** and owns state + workspace.
- You connect from your laptop or phone via the **Control UI** or **Tailscale/SSH**.
- Treat the VPS as the source of truth and **back up** the state + workspace regularly.
- Secure default: keep the Gateway on loopback and access it via SSH tunnel or Tailscale Serve. If you bind to `lan` or `tailnet`, require `gateway.auth.token` or `gateway.auth.password`.

Related pages on the source: Gateway remote access (`/gateway/remote`) and the Platforms hub (`/platforms`).

## Harden admin access first

Before installing OpenClaw on a public VPS, decide how you want to administer the box itself — this is separate from how you reach the Gateway:

- If you want Tailnet-only admin access, install Tailscale first, join the VPS to your tailnet, verify a second SSH session over the Tailscale IP or MagicDNS name, then restrict public SSH.
- If you are not using Tailscale, apply the equivalent hardening for your SSH path before exposing more services.
- This is separate from Gateway access: you can still keep OpenClaw bound to loopback and use an SSH tunnel or Tailscale Serve for the dashboard.

Tailscale-specific Gateway options live in the Tailscale page (`/gateway/tailscale`).

## Shared company agent on a VPS

Running a single agent for a team is a valid setup when every user is in the same trust boundary and the agent is business-only. The hardening steps are:

- Keep it on a dedicated runtime (VPS/VM/container + dedicated OS user/accounts).
- Do not sign that runtime into personal Apple/Google accounts or personal browser/password-manager profiles.
- If users are adversarial to each other, split by gateway/host/OS user.

Full security-model details are in the Security page (`/gateway/security`).

## Using nodes with a VPS

You can keep the Gateway in the cloud and pair **nodes** on your local devices (Mac/iOS/Android/headless). Nodes provide local screen/camera/canvas and `system.run` capabilities while the Gateway stays in the cloud. The page links to Nodes (`/nodes`) and Nodes CLI (`/cli/nodes`) for the pairing details.

## Startup tuning for small VMs and ARM hosts

If CLI commands feel slow on low-power VMs (or ARM hosts), enable Node's module compile cache by appending the following to `~/.bashrc`:

```bash
grep -q 'NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache' ~/.bashrc || cat >> ~/.bashrc <<'EOF'
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
mkdir -p /var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
EOF
source ~/.bashrc
```

What these settings do, per the source:

- `NODE_COMPILE_CACHE` improves repeated command startup times.
- `OPENCLAW_NO_RESPAWN=1` keeps routine Gateway restarts in-process, which avoids extra process handoffs and keeps PID tracking simple on small hosts.
- First command run warms the cache; subsequent runs are faster.
- For Raspberry Pi specifics, see Raspberry Pi (`/install/raspberry-pi`).

### systemd tuning checklist (optional)

For VM hosts using `systemd`, the page suggests:

- Add service env for a stable startup path: `OPENCLAW_NO_RESPAWN=1` and `NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache`.
- Keep restart behavior explicit: `Restart=always`, `RestartSec=2`, and `TimeoutStartSec=90`.
- Prefer SSD-backed disks for state/cache paths to reduce random-I/O cold-start penalties.

For the standard `openclaw onboard --install-daemon` path, edit the user unit:

```bash
systemctl --user edit openclaw-gateway.service
```

```ini
[Service]
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Restart=always
RestartSec=2
TimeoutStartSec=90
```

If you deliberately installed a system unit instead, edit `openclaw-gateway.service` via `sudo systemctl edit openclaw-gateway.service`. The page links out for further context: how `Restart=` policies help automated recovery (`redhat.com/en/blog/systemd-automate-recovery`), and for Linux OOM behavior, child-process victim selection, and `exit 137` diagnostics, the Linux memory-pressure-and-OOM-kills section (`/platforms/linux#memory-pressure-and-oom-kills`).

**Source**: OpenClaw documentation — `vps` (mirror `inbox/openclaw_docs/vps.md`)
**Last Updated**: 2026-06-22
**Status**: Active
