---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - raspberry_pi
keywords:
  - openclaw raspberry pi install
  - always-on self-hosted gateway
  - raspberry pi os lite 64-bit
  - node.js 24 nodesource
  - openclaw onboard install-daemon
  - ssh tunnel control ui 18789
  - arm64 aarch64 binary notes
  - swap swappiness low ram pi
  - systemd user service linger
  - cloud api model fallbacks
topics:
  - OpenClaw
  - Install — Raspberry Pi
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/raspberry-pi
access_control_group: ["general"]
---

# OpenClaw — Always-On Gateway on a Raspberry Pi

## Overview

This procedure hosts a persistent, always-on OpenClaw Gateway on a Raspberry Pi for cheap self-hosting, mirroring the `install/raspberry-pi` source page. Because the Pi only runs the Gateway (models run in the cloud via API), even a modest Pi handles the workload well — typical hardware cost is **$35–80 one-time**, with no monthly fees. The note covers hardware/RAM compatibility, prerequisites, the headless 9-step setup (flash 64-bit OS, SSH in, install Node 24, add swap, install OpenClaw, onboard, verify, tunnel to the Control UI), low-RAM/low-power performance tuning, the recommended cloud-model config, ARM64 binary caveats, state persistence and backups, and Pi-specific troubleshooting.

## Hardware compatibility

The source page rates Pi models for running the Gateway. **Pi 5 (4/8 GB)** is Best (fastest, recommended); **Pi 4 (4 GB)** is Good (the sweet spot for most users); **Pi 4 (2 GB)** is OK (add swap); **Pi 4 (1 GB)** is Tight (possible with swap, minimal config); **Pi 3B+ (1 GB)** is Slow (works but sluggish); and **Pi Zero 2 W (512 MB)** is No (not recommended). The stated **Minimum** is 1 GB RAM, 1 core, 500 MB free disk, and a 64-bit OS. The **Recommended** baseline is 2 GB+ RAM, a 16 GB+ SD card (or USB SSD), and Ethernet.

## Prerequisites

- Raspberry Pi 4 or 5 with 2 GB+ RAM (4 GB recommended).
- MicroSD card (16 GB+) or USB SSD (better performance).
- Official Pi power supply.
- Network connection (Ethernet or WiFi).
- 64-bit Raspberry Pi OS (required — do not use 32-bit).
- About 30 minutes.

## Setup (9 steps)

The setup is a headless, SSH-driven sequence of nine steps.

1. **Flash the OS** — Use **Raspberry Pi OS Lite (64-bit)** (no desktop needed for a headless server). Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/), choose OS **Raspberry Pi OS Lite (64-bit)**, and in the settings dialog pre-configure the hostname (`gateway-host`), enable SSH, set a username and password, and configure WiFi (if not using Ethernet). Flash to the SD card or USB drive, insert it, and boot the Pi.
2. **Connect via SSH** — `ssh user@gateway-host`.
3. **Update the system** — Run `sudo apt update && sudo apt upgrade -y`, install `git curl build-essential`, and set the timezone (important for cron and reminders) with `sudo timedatectl set-timezone America/Chicago`.
4. **Install Node.js 24** — Add the NodeSource repo and install (see the code block below), then confirm with `node --version`.
5. **Add swap** (important for 2 GB or less) — Create and enable a 2G swapfile and reduce swappiness (see the code block below).
6. **Install OpenClaw** — `curl -fsSL https://openclaw.ai/install.sh | bash`.
7. **Run onboarding** — `openclaw onboard --install-daemon`, then follow the wizard. **API keys are recommended over OAuth for headless devices**, and **Telegram is the easiest channel to start with**.
8. **Verify** — `openclaw status`, `systemctl --user status openclaw-gateway.service`, and follow logs with `journalctl --user -u openclaw-gateway.service -f`.
9. **Access the Control UI** — From your computer, get a dashboard URL from the Pi, then open an SSH tunnel in another terminal (see the code block below).

The two install steps run verbatim:

```bash
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs
node --version
```

Step 5 adds and tunes swap:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Reduce swappiness for low-RAM devices
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

Step 9 reaches the Control UI over an SSH tunnel — get the URL from the Pi (`ssh user@gateway-host 'openclaw dashboard --no-open'`), then forward the port:

```bash
ssh -N -L 18789:127.0.0.1:18789 user@gateway-host
```

Open the printed URL in your local browser. For always-on remote access, the source points to **Tailscale integration** (`/gateway/tailscale`).

## Performance tips

**Use a USB SSD** — SD cards are slow and wear out; a USB SSD dramatically improves performance (see the [Pi USB boot guide](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#usb-mass-storage-boot)).

**Enable module compile cache** — Speeds up repeated CLI invocations on lower-power Pi hosts. The source appends to `~/.bashrc`: `export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache` (with `mkdir -p` of that path) and `export OPENCLAW_NO_RESPAWN=1`, then `source ~/.bashrc`. `OPENCLAW_NO_RESPAWN=1` keeps routine Gateway restarts in-process, which avoids extra process handoffs and keeps PID tracking simple on small hosts.

**Reduce memory usage** — For headless setups, free GPU memory and disable unused services: `echo 'gpu_mem=16' | sudo tee -a /boot/config.txt` and `sudo systemctl disable bluetooth`.

**systemd drop-in for stable restarts** — If the Pi is mostly running OpenClaw, add a service drop-in with `systemctl --user edit openclaw-gateway.service`:

```ini
[Service]
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Restart=always
RestartSec=2
TimeoutStartSec=90
```

Then run `systemctl --user daemon-reload && systemctl --user restart openclaw-gateway.service`. On a headless Pi, also enable lingering once so the user service survives logout: `sudo loginctl enable-linger "$(whoami)"`.

## Recommended model setup

Since the Pi only runs the gateway, the source recommends cloud-hosted API models, with a primary model and a fallback ladder:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-6",
        "fallbacks": ["openai/gpt-5.4-mini"]
      }
    }
  }
}
```

Per the source: do not run local LLMs on a Pi — even small models are too slow to be useful; let Claude or GPT do the model work.

## ARM binary notes

Most OpenClaw features work on ARM64 without changes (Node.js, Telegram, WhatsApp/Baileys, Chromium). The binaries that occasionally lack ARM builds are typically optional Go/Rust CLI tools shipped by skills. Verify a missing binary's release page for `linux-arm64` / `aarch64` artifacts before falling back to building from source.

## Persistence and backups

OpenClaw state lives under two paths: `~/.openclaw/` holds `openclaw.json`, the per-agent `auth-profiles.json`, channel/provider state, and sessions; `~/.openclaw/workspace/` holds the agent workspace (SOUL.md, memory, artifacts). These survive reboots. Take a portable snapshot with `openclaw backup create`. Keeping these on an SSD improves both performance and longevity over the SD card.

## Troubleshooting

- **Out of memory** — Verify swap is active with `free -h`. Disable unused services (`sudo systemctl disable cups bluetooth avahi-daemon`). Use API-based models only.
- **Slow performance** — Use a USB SSD instead of an SD card. Check for CPU throttling with `vcgencmd get_throttled` (should return `0x0`).
- **Service will not start** — Check logs with `journalctl --user -u openclaw-gateway.service --no-pager -n 100` and run `openclaw doctor --non-interactive`. If this is a headless Pi, also verify lingering is enabled: `sudo loginctl enable-linger "$(whoami)"`.
- **ARM binary issues** — If a skill fails with "exec format error", check whether the binary has an ARM64 build. Verify architecture with `uname -m` (should show `aarch64`).
- **WiFi drops** — Disable WiFi power management: `sudo iwconfig wlan0 power off`.

## Next steps

The source links onward to **Channels** (`/channels`, connect Telegram, WhatsApp, Discord, and more), **Gateway configuration** (`/gateway/configuration`, all config options), and [Updating](oc_install_updating.md) (keep OpenClaw up to date). Related pages are **Install overview** (`/install`), **Linux server** (`/vps`), and **Platforms** (`/platforms`).

**Source**: OpenClaw documentation — `install/raspberry-pi` (mirror `inbox/openclaw_docs/install/raspberry-pi.md`)
**Last Updated**: 2026-06-22
**Status**: Active
