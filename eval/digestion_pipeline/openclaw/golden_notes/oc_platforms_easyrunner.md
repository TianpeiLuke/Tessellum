---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - easyrunner
keywords:
  - openclaw easyrunner gateway
  - podman compatible compose
  - caddy reverse proxy gateway
  - openclaw gateway token
  - persistent config workspace volume
  - gateway bind lan port 1455
  - gateway probe status verify
  - openclaw doctor config migration
topics:
  - OpenClaw
  - Platforms
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/easyrunner
access_control_group: ["general"]
---

# OpenClaw — Hosting the Gateway on EasyRunner (Podman + Caddy)

## Overview

This note is the procedure for hosting the OpenClaw Gateway as a small containerized app on EasyRunner, behind EasyRunner's built-in Caddy proxy. It mirrors the `platforms/easyrunner` source page: the prerequisites and persistent volumes you need before you begin, the Podman-compatible Compose service definition (image, restart policy, environment, volumes, Caddy labels, run command), the persistent-volume Gateway config (bind/port/auth.token), how to verify the deployment with `gateway probe` / `gateway status` and host log checks, the update-and-backup flow, and the proxy/auth/volume/plugin troubleshooting cases. EasyRunner is assumed to run Podman-compatible Compose apps and to expose HTTPS through Caddy; this guide deploys the published OpenClaw container behind that proxy.

## Before you begin

The page lists five prerequisites for hosting the Gateway on EasyRunner: an EasyRunner server with a domain routed to it; a built or published OpenClaw container image; a persistent config volume for `/home/node/.openclaw`; a persistent workspace volume for `/workspace`; and a strong Gateway token or password.

On auth posture, the guidance is to keep device auth enabled when possible. If your reverse proxy deployment cannot carry device identity correctly, fix trusted-proxy settings first; use dangerous auth bypasses only for a fully private, operator-controlled network.

## Compose app

Create an EasyRunner app with a Compose file shaped like the following. It runs the `ghcr.io/openclaw/openclaw:latest` image with `restart: unless-stopped`, sets the gateway token and path environment, mounts the two named volumes, attaches Caddy labels that front the container at `openclaw.example.com` and reverse-proxy to upstream port `1455`, and runs the gateway bound to the LAN on port `1455`:

```yaml
services:
  openclaw:
    image: ghcr.io/openclaw/openclaw:latest
    restart: unless-stopped
    environment:
      OPENCLAW_GATEWAY_TOKEN: ${OPENCLAW_GATEWAY_TOKEN}
      OPENCLAW_HOME: /home/node
      OPENCLAW_STATE_DIR: /home/node/.openclaw
      OPENCLAW_CONFIG_PATH: /home/node/.openclaw/openclaw.json
      OPENCLAW_WORKSPACE_DIR: /workspace
    volumes:
      - openclaw-config:/home/node/.openclaw
      - openclaw-workspace:/workspace
    labels:
      caddy: openclaw.example.com
      caddy.reverse_proxy: "{{upstreams 1455}}"
    command: ["openclaw", "gateway", "--bind", "lan", "--port", "1455"]

volumes:
  openclaw-config:
  openclaw-workspace:
```

Replace `openclaw.example.com` with your Gateway hostname. Store `OPENCLAW_GATEWAY_TOKEN` in EasyRunner's secret/environment manager instead of committing it to the app definition.

## Configure OpenClaw

Inside the persistent config volume, keep the Gateway reachable only through the proxy and require auth. The page's example `openclaw.json` config binds the gateway to `lan` on port `1455` and sets the auth token from the `${OPENCLAW_GATEWAY_TOKEN}` env reference:

```json5
{
  gateway: {
    bind: "lan",
    port: 1455,
    auth: {
      token: "${OPENCLAW_GATEWAY_TOKEN}",
    },
  },
}
```

If Caddy terminates TLS for the Gateway, configure trusted proxy settings for the exact proxy path rather than disabling auth checks globally. The page cross-links Trusted proxy auth (`/gateway/trusted-proxy-auth`) for the proxy-path configuration details.

## Verify

From your workstation, probe and check status against the public Caddy hostname using the gateway token:

```bash
openclaw gateway probe --url https://openclaw.example.com --token <token>
openclaw gateway status --url https://openclaw.example.com --token <token>
```

From the EasyRunner host, check the app logs for a listening Gateway and no startup SecretRef, plugin, or channel auth failures.

## Updates and backups

The update-and-backup flow is: pull or build the new OpenClaw image, then redeploy the EasyRunner app; back up the `openclaw-config` volume before updates; back up `openclaw-workspace` if agents write durable project data there; and run `openclaw doctor` after major updates to catch config migrations and service warnings.

## Troubleshooting

The page documents four failure cases for a hosted EasyRunner Gateway. If `gateway probe` cannot connect, confirm the Caddy hostname points at the app and that the container listens on `0.0.0.0:1455`. If auth fails, rotate the token in EasyRunner secrets and the local client command together. If files are root-owned after restore, repair the mounted volumes so the container user can write `/home/node/.openclaw` and `/workspace`. If browser or channel plugins fail, check whether the required external binaries, network egress, and mounted credentials are available inside the container.

**Source**: OpenClaw documentation — `platforms/easyrunner` (mirror `inbox/openclaw_docs/platforms/easyrunner.md`)
**Last Updated**: 2026-06-22
**Status**: Active
