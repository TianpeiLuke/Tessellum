---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - exe_dev
keywords:
  - openclaw exe.dev install
  - openclaw vm gateway deploy
  - nginx reverse proxy openclaw
  - exe.xyz https remote access
  - openclaw devices approve pairing
  - shelley automated install
  - openclaw config patch remote
  - gateway auth token mode
topics:
  - OpenClaw
  - Install (exe.dev)
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/exe-dev
access_control_group: ["general"]
---

# OpenClaw — Install on an exe.dev VM (HTTPS Proxy + Remote Access)

## Overview

This note is the procedure for deploying the OpenClaw Gateway on an [exe.dev](https://exe.dev) virtual machine so it is reachable from a laptop at `https://<vm-name>.exe.xyz`, mirroring the `install/exe-dev` source page. It covers the beginner quick path (one-click provisioning via exe.dev's Shelley agent), the prerequisites, the automated install prompt, the five-step manual installation (create VM, install prerequisites, install OpenClaw, set up an nginx reverse proxy to the gateway port `18789`, then access the Control UI and grant device-pairing privileges), the remote channel setup via a single `config patch`, how remote access/HTTPS is handled by exe.dev, and the update flow. The page assumes exe.dev's default **exeuntu** image; if a different distro is picked, package names map accordingly. The VM is kept **stateful** because OpenClaw stores `openclaw.json`, per-agent `auth-profiles.json`, sessions, and channel/provider state under `~/.openclaw/`, plus the workspace under `~/.openclaw/workspace/`.

## Beginner Quick Path

The fastest route uses exe.dev's agent (Shelley) to provision OpenClaw with no manual steps:

1. Open [https://exe.new/openclaw](https://exe.new/openclaw).
2. Fill in your auth key/token as needed.
3. Click "Agent" next to your VM and wait for Shelley to finish provisioning.
4. Open `https://<vm-name>.exe.xyz/` and authenticate with the configured shared secret. This guide uses **token auth** by default, but password auth also works if you switch `gateway.auth.mode`.
5. Approve any pending device pairing requests with `openclaw devices approve <requestId>`.

## What You Need

- An exe.dev account.
- `ssh exe.dev` access to [exe.dev](https://exe.dev) virtual machines (optional).

## Automated Install with Shelley

Shelley, exe.dev's agent, can install OpenClaw instantly using a prompt. The prompt instructs Shelley to set up OpenClaw with the non-interactive and accept-risk onboarding flags, add the supplied auth/token, configure nginx to forward from the default port `18789` to the root location on the default enabled site config (with WebSocket support enabled), do pairing via `openclaw devices list` / `openclaw devices approve <request id>`, and confirm the dashboard shows OpenClaw health OK. Because exe.dev handles forwarding from port `8000` to ports `80`/`443` and HTTPS, the final reachable address is `<vm-name>.exe.xyz` with no port specification. The verbatim prompt is:

```
Set up OpenClaw (https://docs.openclaw.ai/install) on this VM. Use the non-interactive and accept-risk flags for openclaw onboarding. Add the supplied auth or token as needed. Configure nginx to forward from the default port 18789 to the root location on the default enabled site config, making sure to enable Websocket support. Pairing is done by "openclaw devices list" and "openclaw devices approve <request id>". Make sure the dashboard shows that OpenClaw's health is OK. exe.dev handles forwarding from port 8000 to port 80/443 and HTTPS for us, so the final "reachable" should be <vm-name>.exe.xyz, without port specification.
```

## Manual Installation

### 1) Create the VM, 2) Install Prerequisites, 3) Install OpenClaw

From your device, create a new exe.dev VM and connect to it (`ssh exe.dev new`, then `ssh <vm-name>.exe.xyz`). Keep this VM **stateful**: OpenClaw stores `openclaw.json`, per-agent `auth-profiles.json`, sessions, and channel/provider state under `~/.openclaw/`, plus the workspace under `~/.openclaw/workspace/`. On the VM, install the prerequisites, then run the OpenClaw install script:

```bash
# From your device
ssh exe.dev new
ssh <vm-name>.exe.xyz

# 2) On the VM — prerequisites
sudo apt-get update
sudo apt-get install -y git curl jq ca-certificates openssl

# 3) On the VM — install OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash
```

### 4) Set Up nginx to Proxy OpenClaw to Port 8000

Edit `/etc/nginx/sites-enabled/default` so the server listens on ports `80` and `8000` and proxies the root location to the gateway at `127.0.0.1:18789`. The block enables WebSocket upgrade (`Upgrade` / `Connection: "upgrade"`), sets standard proxy headers, and uses long `86400s` read/send timeouts for long-lived connections:

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    listen 8000;
    listen [::]:8000;

    server_name _;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;

        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Standard proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout settings for long-lived connections
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

These headers **overwrite** forwarded metadata instead of preserving client-supplied chains: OpenClaw trusts forwarded IP metadata only from explicitly configured proxies, and append-style `X-Forwarded-For` chains are treated as a hardening risk.

### 5) Access OpenClaw and Grant Privileges

Access `https://<vm-name>.exe.xyz/` (see the Control UI output from onboarding). If it prompts for auth, paste the configured shared secret from the VM. This guide uses token auth, so retrieve `gateway.auth.token` with `openclaw config get gateway.auth.token` (or generate one with `openclaw doctor --generate-gateway-token`). If you changed the gateway to password auth, use `gateway.auth.password` / `OPENCLAW_GATEWAY_PASSWORD` instead. Approve devices with `openclaw devices list` and `openclaw devices approve <requestId>`. When in doubt, use Shelley from the browser.

## Remote Channel Setup

For remote hosts, prefer one `config patch` call over many SSH calls to `config set`. Keep real tokens in the VM environment or `~/.openclaw/.env`, and put only SecretRefs in `openclaw.json`. First, on the VM, make the service environment contain the secrets it needs:

```bash
cat >> ~/.openclaw/.env <<'EOF'
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
DISCORD_BOT_TOKEN=...
OPENAI_API_KEY=sk-...
EOF
```

From the local machine, create a JSON5 patch file (`openclaw.remote.patch.json5`) that points `secrets.providers.default` at `source: "env"`, enables the Slack channel in `mode: "socket"` (with `botToken`/`appToken` SecretRefs, `groupPolicy: "open"`, `requireMention: false`), enables the Discord channel (`token` SecretRef, `dmPolicy: "disabled"`, `groupPolicy: "allowlist"`), and sets the agent defaults (`model.primary: "openai/gpt-5.5"` with `fastMode: true`). Pipe it to the VM with a dry-run first, then apply, then restart and check health:

```bash
ssh <vm-name>.exe.xyz 'openclaw config patch --stdin --dry-run' < ./openclaw.remote.patch.json5
ssh <vm-name>.exe.xyz 'openclaw config patch --stdin' < ./openclaw.remote.patch.json5
ssh <vm-name>.exe.xyz 'openclaw gateway restart && openclaw health'
```

Use `--replace-path` when a nested allowlist should become exactly the patch value — for example, replacing a Discord channel allowlist: `openclaw config patch --stdin --replace-path "channels.discord.guilds[\"123\"].channels"`.

## Remote Access

Remote access is handled by exe.dev's authentication. By default, HTTP traffic from port `8000` is forwarded to `https://<vm-name>.exe.xyz` with **email auth** — exe.dev terminates HTTPS for you, so the gateway itself only listens on the loopback proxy target (`127.0.0.1:18789`).

## Updating

Update the global package, run the doctor, restart the gateway, and verify health:

```bash
npm i -g openclaw@latest
openclaw doctor
openclaw gateway restart
openclaw health
```

See the [Updating](https://docs.openclaw.ai/install/updating) guide for the full update flow.

**Source**: OpenClaw documentation — `install/exe-dev` (mirror `inbox/openclaw_docs/install/exe-dev.md`)
**Last Updated**: 2026-06-22
**Status**: Active
