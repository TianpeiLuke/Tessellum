---
tags:
  - resource
  - documentation
  - hermes_agent
  - deployment
  - windows
keywords:
  - windows wsl2
  - wsl filesystem boundary
  - wsl networking
  - netsh portproxy
  - mirrored vs nat networking
  - gpu passthrough wsl
topics:
  - Hermes Agent
  - Deployment
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/windows-wsl-quickstart
access_control_group: ["general"]
---

# Hermes Agent — Windows (WSL2) Install Guide

## Overview

This is the Windows-via-WSL2 deployment path for Hermes Agent: it runs the Hermes harness as plain Linux inside a lightweight WSL2 VM, alongside (not instead of) the native Windows install. You pick WSL2 when you need the dashboard's embedded terminal (`/chat` tab — a POSIX PTY, WSL2-only) or POSIX-heavy dev work; native Windows is fine for interactive chat, the gateway, cron, the browser tool, and MCP servers. The page treats WSL2 as two computers — the Windows host and a Linux VM — and documents the parts of that split affecting Hermes: installing WSL2, the Windows↔WSL filesystem boundary, bidirectional networking, keeping the gateway alive long-term, NVIDIA GPU passthrough, and common pitfalls.

## When to Pick WSL2 vs Native

**When to pick WSL2 over native:**
- You want the dashboard's embedded terminal (`/chat` tab) — that pane requires a POSIX PTY and is WSL2-only.
- You're doing POSIX-heavy development and want Hermes sessions to share the same filesystem / paths as your dev tools.
- You already have a WSL2 environment and don't want to maintain a second install.

**When native is fine (or better):**
- Interactive chat, gateway (Telegram/Discord/etc.), cron scheduler, browser tool, MCP servers, and most features run natively on Windows.
- You don't want to think about crossing the WSL↔Windows boundary every time you reference a file or open a URL.

## Why WSL2 (vs Native Windows)

The native Windows install runs in Windows directly (Windows terminals, `C:\Users\…` paths, processes), using Git Bash to run shell commands — sidestepping the POSIX-vs-Windows gap without a rewrite. WSL2 instead runs a real Linux kernel in a lightweight VM, so Hermes inside it is essentially identical to Ubuntu: `fork`, `/tmp`, UNIX sockets, signal semantics, PTY-backed terminals, shells (`bash`/`zsh`), and tools (`rg`, `git`, `ffmpeg`) behave the Linux way. Practical consequence: the Hermes CLI, gateway, sessions, memory, skills, and tool runtimes all live inside the Linux VM, while Windows programs (browsers, native apps, signed-in Chrome) live outside it — and every time the two talk (share files, open URLs, control Chrome, hit a local model server, expose the gateway), you cross a boundary. Those boundaries are the subject of the guide.

## Install WSL2

From an **Admin PowerShell** or Windows Terminal:

```powershell
wsl --install
```

On a fresh Windows 10 22H2+ or Windows 11 box this installs the WSL2 kernel, the Virtual Machine Platform feature, and a default Ubuntu distro. Reboot when prompted; Ubuntu opens and asks for a Linux username + password (a **new Linux user**, unrelated to your Windows account). Verify WSL2 (not legacy WSL1) with `wsl --list --verbose` — expect `VERSION 2`; if a distro shows `VERSION 1`, convert with `wsl --set-version Ubuntu 2` and `wsl --set-default-version 2`. Hermes is unreliable on WSL1, which translates syscalls on the fly so procfs/signals/network diverge from real Linux.

**Distro choice:** Ubuntu (LTS) is what Hermes tests against; Debian works; Arch/NixOS work but the one-line installer assumes a Debian-derived `apt` system (see the Nix setup guide for that path).

**Enable systemd (recommended)** — the gateway is easier to manage with systemd. Enable it once inside the distro, then `wsl --shutdown` and reopen (`ps -p 1 -o comm=` should print `systemd`):

```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true

[interop]
enabled=true
appendWindowsPath=true

[automount]
options = "metadata,umask=22,fmask=11"
EOF
```

The `metadata` mount option matters — without it, files on `/mnt/c/...` can't store real Linux permission bits, breaking `chmod +x` on scripts under Windows paths.

**Install Hermes inside WSL** — once a WSL2 shell is open, the installer treats WSL2 as plain Linux (nothing WSL-specific):

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.bashrc
hermes
```

## Filesystem: Crossing the Windows ↔ WSL2 Boundary

There are **two filesystems**, and where you put files matters for performance, correctness, and tool visibility. The two directions:

| Direction | Path inside | Path you use |
|---|---|---|
| Windows disk, seen from WSL | `C:\Users\you\Documents` | `/mnt/c/Users/you/Documents` |
| WSL disk, seen from Windows | `/home/you/code` | `\\wsl$\Ubuntu\home\you\code` (or `\\wsl.localhost\Ubuntu\...` on newer builds) |

Both are real and both work, but they are **not the same filesystem** — they're bridged by a 9P network protocol with real performance and semantic consequences.

**Rule of thumb: keep everything Linux-ish inside the Linux filesystem** — the Hermes install (`~/.hermes/`), git repos worked from WSL (`~/code/...`), models, datasets, venvs. What that buys you: **fast I/O** (`/mnt/c` goes through 9P, 10–100× slower than native ext4 — `git status` on a 10k-file repo can take 15+ seconds under `/mnt/c`); **correct permissions** (Linux bits are best-effort on `/mnt/c`, causing `ssh` "bad permissions" or silent `chmod +x` failures); **reliable file watchers** (inotify across 9P is flaky); and **no case-sensitivity surprises**. Put things on `/mnt/c` only when a file must live Windows-side (open from a Windows GUI app, or Windows Chrome DevTools MCP needs a Windows-reachable cwd).

**Getting files back and forth** — Windows→WSL via Explorer (`\\wsl.localhost\Ubuntu`, drag-drop) or `wsl cp /mnt/c/Users/you/Downloads/file.pdf ~/incoming/`; WSL→Windows via `cp ~/reports/output.pdf /mnt/c/Users/you/Desktop/`. Install `wslu` once (`sudo apt install wslu`) for `wslview <file>` (open with the Windows default handler), `explorer.exe .` (open the current WSL dir in Explorer), and path conversion: `wslpath -w ~/code/project` → `\\wsl.localhost\Ubuntu\home\you\code\project`, `wslpath -u 'C:\Users\you'` → `/mnt/c/Users/you`.

**Line endings, BOMs, and git** — files edited Windows-side may get `CRLF`, so Linux `bash`/Python breaks with `bad interpreter: /bin/bash^M` or BOM'd `.env` failures. The fix is a sane git config inside WSL (`git config --global core.autocrlf input` + `core.eol lf`); for files that already have CRLF, `sudo apt install dos2unix` then `dos2unix path/to/script.sh`.

**"Clone inside WSL or on `/mnt/c`?"** — clone inside WSL, always, unless you have a specific reason not to: a typical Hermes workflow (`hermes chat`, tool calls that `rg` the repo, file watchers, background gateway) is dramatically faster against `~/code/myrepo`. One exception: MCP bridges that launch Windows binaries — if using `chrome-devtools-mcp` through `cmd.exe`, Windows may emit a `UNC` warning when cwd is `~`, so start Hermes from somewhere under `/mnt/c/` to give the Windows process a drive-letter cwd.

## Networking: WSL ↔ Windows

WSL2 runs in a VM with its own network stack, so `localhost` inside WSL is **not the same as** `localhost` on Windows — two separate hosts. For each service you decide direction and pick the right bridge. Two cases come up constantly.

**Case 1 — Hermes in WSL talks to a service on Windows** (most common: Ollama, LM Studio, or a llama-server on Windows). The canonical how-to lives in the providers guide (WSL2 Networking for Local Models — don't duplicate it). Short version: on **Windows 11 22H2+**, turn on mirrored networking (`networkingMode=mirrored` in `%USERPROFILE%\.wslconfig`, then `wsl --shutdown`) so `localhost` works both ways; on **Windows 10 / older builds**, use the Windows host IP (WSL virtual network's default gateway), bind the Windows server to `0.0.0.0` (not just `127.0.0.1`), and add a firewall rule for the port.

**Case 2 — Something on Windows (or your LAN) talks to Hermes in WSL** (the reverse direction): using the web dashboard from a Windows browser, the OpenAI-compatible API server (exposed by `hermes gateway` when `API_SERVER_ENABLED=true`), or a messaging gateway whose platform pings a local webhook (use `cloudflared`/`ngrok` rather than raw port forwarding).

- **Subcase 2a (from the Windows host itself):** on Windows 11 22H2+ with mirrored mode there is nothing to do — a WSL bind to `0.0.0.0:8080` (or even `127.0.0.1:8080`) is reachable at `http://localhost:8080`. On NAT mode, WSL2's localhost forwarding generally maps Linux-side `127.0.0.1` binds to Windows `localhost`; if not, bind `0.0.0.0` or find the VM IP (`ip -4 addr show eth0 | grep inet`) and hit that.
- **Subcase 2b (from another LAN device):** the real pain — traffic flows LAN device → Windows host → WSL VM, so set up both hops: (1) bind all interfaces inside WSL (`0.0.0.0`), (2) port-forward Windows → WSL VM (automatic in mirrored mode; manual per port in NAT mode), (3) point the LAN device at `http://<windows-lan-ip>:8080`. The NAT-mode port-proxy (Admin PowerShell):

```powershell
# Grab the WSL VM's current IP (it changes on every WSL restart under NAT)
$wslIp = (wsl hostname -I).Trim().Split(' ')[0]

# Forward Windows port 8080 → WSL:8080
netsh interface portproxy add v4tov4 `
  listenaddress=0.0.0.0 listenport=8080 `
  connectaddress=$wslIp connectport=8080

# Allow it through Windows Firewall
New-NetFirewallRule -DisplayName "Hermes WSL 8080" `
  -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow
```

Remove later with `netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=8080`. Because the WSL VM IP drifts on each NAT restart, a one-shot rule survives only until the next `wsl --shutdown` — for anything persistent, use mirrored mode or a Windows-login script. For webhooks from cloud messaging providers (Telegram `setWebhook`, Slack events), use `cloudflared` tunnels instead of port-forwarding.

## Running Hermes Services Long-Term on Windows

The Tool Gateway and the API server are long-lived; WSL2 gives a few options to keep them up.

**Desktop shortcut (quick interactive launcher)** — create it Windows-side (right-click desktop → New → Shortcut) targeting your distro:

```text
wt.exe -w 0 -p "Ubuntu" wsl.exe -d Ubuntu --cd ~ -- bash -ic "hermes"
```

Name it `Hermes`. It opens Windows Terminal, starts WSL, drops into the Linux home dir, and launches Hermes (if `hermes` isn't on PATH yet, `source ~/.bashrc` once, or use `uv run hermes` inside your checkout). Optional polish: a custom `.ico` (Properties → Change Icon), pinning to Start/Taskbar.

**Inside WSL with systemd (recommended)** — if systemd is enabled, `hermes gateway` and the API server work like any Linux machine. The gateway setup wizard offers to install a systemd user unit so the gateway starts automatically with WSL:

```bash
hermes gateway setup
```

**Making WSL itself start on Windows login** — WSL's VM only stays alive while something uses it. To keep the gateway reachable without a terminal open, boot a WSL process at login via Task Scheduler — Trigger: At log on; Action: Start a program, Program `C:\Windows\System32\wsl.exe`, Arguments `-d Ubuntu --exec /bin/sh -c "sleep infinity"`. That keeps the VM alive so the systemd-managed gateway stays running (Windows 11's newer `wsl --install --no-launch` auto-start flows also work; `sleep infinity` is the portable version).

## GPU Passthrough (Local Models)

WSL2 supports **NVIDIA** GPUs natively since WSL kernel 5.10.43+ — install the standard NVIDIA driver on Windows (do **not** install a Linux NVIDIA driver inside WSL), and `nvidia-smi` inside WSL sees the GPU; CUDA toolkits, `torch`, `vllm`, `sglang`, and `llama-server` then build against it as usual. AMD ROCm and Intel Arc support inside WSL2 is still evolving and outside Hermes's test matrix. If you run a Windows-native local-model server (Ollama for Windows, LM Studio) already using your GPU through Windows drivers, you don't need WSL GPU passthrough at all — follow Case 1 and hit it over the network from WSL.

## Common Pitfalls

- **"Connection refused" to Windows-hosted Ollama / LM Studio** — usually the server is bound to `127.0.0.1` and needs `0.0.0.0` (Ollama: `OLLAMA_HOST=0.0.0.0`), or a firewall rule is missing.
- **Massive slowness on `git status` / `hermes chat` in a repo** — you're probably under `/mnt/c/...`; move the repo to `~/code/...` for an order-of-magnitude speedup.
- **`bad interpreter: /bin/bash^M` on scripts** — CRLF from a Windows editor; `dos2unix script.sh` and set `core.autocrlf input` in your WSL git config.
- **"UNC paths are not supported" from Windows binaries via MCP** — Hermes's cwd is inside the Linux filesystem and `cmd.exe` can't use it; start Hermes from `/mnt/c/...` for that session, or `cd` to a Windows-reachable path first.
- **Clock drift after sleep/hibernate** — WSL2's clock can lag minutes after resume, breaking cert-based work (OAuth, HTTPS APIs); fix with `sudo hwclock -s` or run `ntpdate` at login.
- **DNS stops working after mirrored mode or on VPN** — mirrored mode proxies host DNS into WSL; override `resolv.conf` (`generateResolvConf=false` in `/etc/wsl.conf`, then write your own with `1.1.1.1` or your VPN's DNS).
- **`hermes` not found after install** — the installer adds `~/.local/bin` to PATH via `~/.bashrc`; `source ~/.bashrc` (or open a new terminal).
- **Windows Defender slow on WSL files** — Defender scans via the 9P bridge when files are accessed from Windows; if you only touch WSL files from inside WSL it doesn't matter, otherwise exclude the distro path from real-time scanning.
- **Running out of disk** — WSL2 stores a sparse VHDX that grows but doesn't auto-shrink; reclaim with `wsl --shutdown` then `Optimize-VHD -Path <path-to-ext4.vhdx> -Mode Full` (Hyper-V tools) or the `diskpart` path in the WSL docs.

**Source**: `inbox/hermes_agent_docs/user-guide/windows-wsl-quickstart.md` · https://hermes-agent.nousresearch.com/docs/user-guide/windows-wsl-quickstart
**Last Updated**: 2026-06-19
**Status**: Active
