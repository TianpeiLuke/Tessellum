---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - macos_vm
keywords:
  - openclaw macos vm install
  - lume apple silicon vm
  - hosted mac providers macstadium
  - openclaw imessage imsg integration
  - lume golden image clone reset
  - run vm headless no-display
  - openclaw channels login whatsapp qr
  - openclaw onboard install-daemon
topics:
  - OpenClaw
  - macOS VM Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/macos-vm
access_control_group: ["general"]
---

# OpenClaw — Install in a Sandboxed macOS VM (Lume / Hosted Mac)

## Overview

This procedure mirrors the `install/macos-vm` page: how to run the OpenClaw Gateway inside a sandboxed macOS virtual machine — either a local VM on an Apple Silicon Mac via **Lume** or a **hosted Mac provider** in the cloud — for strict isolation from your daily Mac and for macOS-only capabilities such as iMessage. It covers when to choose a macOS VM versus the recommended default, the Lume prerequisites and quick path, the full eight-step runbook (install Lume → create VM → Setup Assistant → get IP → SSH → install OpenClaw → configure channels → run headlessly), the iMessage (`imsg`) integration, saving and resetting a golden image, running 24/7, and troubleshooting. The source lists this VM path as a specialized option, not the recommended default for most users.

## Recommended Default (Most Users)

Before reaching for a macOS VM, the page recommends three lower-cost / higher-control defaults for an always-on Gateway: a **small Linux VPS** (always-on Gateway at low cost — see VPS hosting); **dedicated hardware** (a Mac mini or Linux box) when you want full control and a **residential IP** for browser automation, because many sites block data-center IPs so local browsing often works better; and a **hybrid** setup that keeps the Gateway on a cheap VPS and connects your Mac as a **node** when you need browser/UI automation (see Nodes and Gateway remote). Use a macOS VM specifically when you need macOS-only capabilities such as **iMessage** or want **strict isolation** from your daily Mac.

## macOS VM Options

### Local VM on Apple Silicon (Lume)

Run OpenClaw in a sandboxed macOS VM on an existing Apple Silicon Mac using **Lume**. This gives you a full macOS environment in isolation (the host stays clean), **iMessage support via `imsg`** (the default local path is impossible on Linux/Windows), instant reset by cloning VMs, and no extra hardware or cloud costs.

### Hosted Mac Providers (Cloud)

For macOS in the cloud, hosted Mac providers also work: **MacStadium** (hosted Macs) is named, and other hosted Mac vendors work too — follow their VM + SSH docs. Once you have SSH access to a hosted macOS VM, continue at **step 6** (Install OpenClaw) below; the Lume-specific steps 1–5 (install/create/Setup-Assistant/IP/SSH) are replaced by the provider's own provisioning flow.

## Quick Path (Lume, Experienced Users)

For experienced users the source gives a six-line summary: (1) Install Lume; (2) `lume create openclaw --os macos --ipsw latest`; (3) complete Setup Assistant and enable Remote Login (SSH); (4) `lume run openclaw --no-display`; (5) SSH in, install OpenClaw, configure channels; (6) Done. The expanded steps below ground each of these.

## What You Need (Lume)

The Lume prerequisites are: an **Apple Silicon Mac (M1/M2/M3/M4)**; **macOS Sequoia or later** on the host; **~60 GB free disk space per VM**; and **~20 minutes**.

## Step-by-Step Runbook (Steps 1–8)

### 1) Install Lume

Install Lume with the upstream installer script, then ensure `~/.local/bin` is on your `PATH` if it is not already, and verify the install:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/lume/scripts/install.sh)"
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc && source ~/.zshrc   # only if ~/.local/bin not on PATH
lume --version
```

The source links the Lume Installation guide for details.

### 2) Create the macOS VM, 4) Get IP, 5) SSH In

Create the VM (downloads macOS; a **VNC window opens automatically** and the download can take a while), then after Setup Assistant get the VM IP (usually `192.168.64.x`) and SSH in (replace `youruser` with the account you created and the IP with your VM's IP):

```bash
lume create openclaw --os macos --ipsw latest   # step 2: create the VM
lume get openclaw                                # step 4: look for the IP (usually 192.168.64.x)
ssh youruser@192.168.64.X                        # step 5: SSH in with your VM account
```

### 3) Complete Setup Assistant

In the VNC window: select language and region; **skip Apple ID** (or sign in if you want iMessage later); create a user account (remember the username and password); and skip all optional features. After setup completes, perform two macOS settings changes: **enable SSH** via System Settings -> General -> Sharing and enable "Remote Login"; and for headless VM use, **enable auto-login** via System Settings -> Users & Groups, select "Automatically log in as:", and choose the VM user.

### 6) Install OpenClaw (Inside the VM)

Inside the VM, install OpenClaw globally via npm and run onboarding with the daemon installed:

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

Follow the onboarding prompts to set up your model provider (Anthropic, OpenAI, etc.). This is the entry point hosted-Mac-provider users jump to after gaining SSH access.

### 7) Configure Channels

Edit the config file at `~/.openclaw/openclaw.json` (the source uses `nano ~/.openclaw/openclaw.json`) and add your channels. The source's example config block:

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551234567"],
    },
    telegram: {
      botToken: "YOUR_BOT_TOKEN",
    },
  },
}
```

Then log in to WhatsApp (scan QR) with `openclaw channels login`. (The troubleshooting table warns the QR scan must be run while logged into the VM, not the host.)

### 8) Run the VM Headlessly

Stop the VM and restart it without a display, then verify over SSH:

```bash
lume stop openclaw
lume run openclaw --no-display
ssh youruser@192.168.64.X "openclaw status"
```

The VM runs in the background and **OpenClaw's daemon keeps the gateway running**. `openclaw status` over SSH reports liveness.

## Bonus: iMessage Integration

The source calls iMessage "the killer feature of running on macOS" — use the iMessage channel with `imsg` to add Messages to OpenClaw. Inside the VM: (1) sign in to Messages; (2) install `imsg`; (3) grant **Full Disk Access** and **Automation** permission for the process running OpenClaw/`imsg`; (4) verify RPC support with `imsg rpc --help`. Then add the iMessage block to your OpenClaw config (note `cliPath: "imsg"` and `dbPath: "~/Library/Messages/chat.db"`):

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "imsg",
      dbPath: "~/Library/Messages/chat.db",
    },
  },
}
```

Restart the gateway; the agent can then send and receive iMessages. The source links the iMessage channel page for full setup details.

## Save a Golden Image, Reset, and Run 24/7

Before customizing further, snapshot the clean state with `lume stop openclaw` then `lume clone openclaw openclaw-golden`. To reset anytime, stop and delete the working VM, re-clone from the golden image, and re-run headless: `lume stop openclaw && lume delete openclaw`, then `lume clone openclaw-golden openclaw`, then `lume run openclaw --no-display`. For **running 24/7**, keep the VM up by keeping your Mac plugged in, disabling sleep in System Settings → Energy Saver, and using `caffeinate` if needed; for true always-on the source recommends a dedicated Mac mini or a small VPS (see VPS hosting).

## Troubleshooting

The source's troubleshooting table, reproduced verbatim:

| Problem | Solution |
|---|---|
| Can't SSH into VM | Check "Remote Login" is enabled in VM's System Settings |
| VM IP not showing | Wait for VM to fully boot, run `lume get openclaw` again |
| Lume command not found | Add `~/.local/bin` to your PATH |
| WhatsApp QR not scanning | Ensure you're logged into the VM (not host) when running `openclaw channels login` |

**Source**: OpenClaw documentation — `install/macos-vm` (mirror `inbox/openclaw_docs/install/macos-vm.md`)
**Last Updated**: 2026-06-22
**Status**: Active
