---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - ansible
keywords:
  - openclaw ansible install
  - openclaw-ansible playbook
  - hardened openclaw deployment
  - tailscale ufw docker isolation
  - 4-layer defense in depth
  - openclaw systemd service
  - openclaw production server install
  - nmap attack surface check
topics:
  - OpenClaw
  - Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/ansible
access_control_group: ["general"]
---

# OpenClaw — Automated Hardened Install with Ansible

## Overview

This note is the **procedure** for deploying OpenClaw to production Debian/Ubuntu servers with the `openclaw-ansible` automated installer, mirroring the `install/ansible` source page. It covers the prerequisites, the one-command quick-start install, exactly what the playbook installs (Tailscale, UFW, Docker, Node.js 24 + pnpm, host-based OpenClaw, a hardened systemd service), the post-install onboarding steps and quick commands, the 4-layer defense-in-depth security architecture and its `nmap` attack-surface verification, the manual playbook path, idempotent updating, and troubleshooting. The `openclaw-ansible` repo is the source of truth for Ansible deployment; this page (and note) is a quick overview — detailed security architecture and troubleshooting live in the repo docs (see References).

## Prerequisites

| Requirement | Details |
| --- | --- |
| **OS** | Debian 11+ or Ubuntu 20.04+ |
| **Access** | Root or sudo privileges |
| **Network** | Internet connection for package installation |
| **Ansible** | 2.14+ (installed automatically by the quick-start script) |

## What you get

- **Firewall-first security** — UFW + Docker isolation (only SSH + Tailscale accessible).
- **Tailscale VPN** — secure remote access without exposing services publicly.
- **Docker** — isolated sandbox containers, localhost-only bindings.
- **Defense in depth** — 4-layer security architecture.
- **Systemd integration** — auto-start on boot with hardening.
- **One-command setup** — complete deployment in minutes.

## Quick start

A single command performs the complete install (it bootstraps Ansible 2.14+ automatically):

```bash
curl -fsSL https://raw.githubusercontent.com/openclaw/openclaw-ansible/main/install.sh | bash
```

## What gets installed

The Ansible playbook installs and configures, in order:

1. **Tailscale** — mesh VPN for secure remote access.
2. **UFW firewall** — SSH + Tailscale ports only.
3. **Docker CE + Compose V2** — for the default agent sandbox backend.
4. **Node.js 24 + pnpm** — runtime dependencies (Node 22 LTS, currently `22.19+`, remains supported).
5. **OpenClaw** — host-based, not containerized.
6. **Systemd service** — auto-start with security hardening.

The gateway runs directly on the host (not in Docker). Agent sandboxing is optional; this playbook installs Docker because it is the default sandbox backend. See Sandboxing (`/gateway/sandboxing`) for details and other backends.

## Post-Install Setup

After the playbook completes, finish onboarding through these steps:

1. **Switch to the openclaw user** — `sudo -i -u openclaw`.
2. **Run the onboarding wizard** — the post-install script guides you through configuring OpenClaw settings.
3. **Connect messaging providers** — log in to WhatsApp, Telegram, Discord, or Signal with `openclaw channels login`.
4. **Verify the installation** — `sudo systemctl status openclaw` and follow logs with `sudo journalctl -u openclaw -f`.
5. **Connect to Tailscale** — join your VPN mesh for secure remote access.

### Quick commands

```bash
# Check service status
sudo systemctl status openclaw

# View live logs
sudo journalctl -u openclaw -f

# Restart gateway
sudo systemctl restart openclaw

# Provider login (run as openclaw user)
sudo -i -u openclaw
openclaw channels login
```

## Security architecture

The deployment uses a 4-layer defense model:

1. **Firewall (UFW)** — only SSH (22) + Tailscale (41641/udp) exposed publicly.
2. **VPN (Tailscale)** — gateway accessible only via VPN mesh.
3. **Docker isolation** — DOCKER-USER iptables chain prevents external port exposure.
4. **Systemd hardening** — NoNewPrivileges, PrivateTmp, unprivileged user.

To verify your external attack surface, scan all ports against the server:

```bash
nmap -p- YOUR_SERVER_IP
```

Only port 22 (SSH) should be open. All other services (gateway, Docker) are locked down. Docker is installed for agent sandboxes (isolated tool execution), not for running the gateway itself — see Multi-Agent Sandbox and Tools (`/tools/multi-agent-sandbox-tools`) for sandbox configuration.

## Manual installation

If you prefer manual control over the automation, replace the one-command quick start with these steps:

1. **Install prerequisites** — `sudo apt update && sudo apt install -y ansible git`.
2. **Clone the repository** — `git clone https://github.com/openclaw/openclaw-ansible.git` then `cd openclaw-ansible`.
3. **Install Ansible collections** — `ansible-galaxy collection install -r requirements.yml`.
4. **Run the playbook** — `./run-playbook.sh`. Alternatively, run directly and then manually execute the setup script afterward:

```bash
ansible-playbook playbook.yml --ask-become-pass
# Then run: /tmp/openclaw-setup.sh
```

## Updating

The Ansible installer sets up OpenClaw for manual updates; see Updating (`/install/updating`) for the standard update flow (documented in the development-channels note). To re-run the Ansible playbook (for example, for configuration changes), `cd openclaw-ansible` and run `./run-playbook.sh` — this is idempotent and safe to run multiple times.

## Troubleshooting

- **Firewall blocks my connection** — ensure you can access via Tailscale VPN first; SSH access (port 22) is always allowed; the gateway is only accessible via Tailscale by design.
- **Service will not start** — check logs with `sudo journalctl -u openclaw -n 100`, verify permissions with `sudo ls -la /opt/openclaw`, then test a manual start: `sudo -i -u openclaw`, `cd ~/openclaw`, `openclaw gateway run`.
- **Docker sandbox issues** — verify Docker is running (`sudo systemctl status docker`), check the sandbox image (`sudo docker images | grep openclaw-sandbox`), and build it if missing from a source checkout (`cd /opt/openclaw/openclaw`, `sudo -u openclaw ./scripts/sandbox-setup.sh`); for npm installs without a source checkout, see `https://docs.openclaw.ai/gateway/sandboxing#images-and-setup`.
- **Provider login fails** — make sure you are running as the `openclaw` user: `sudo -i -u openclaw` then `openclaw channels login`.

**Source**: OpenClaw documentation — `install/ansible` (mirror `inbox/openclaw_docs/install/ansible.md`)
**Last Updated**: 2026-06-22
**Status**: Active
