---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - render
keywords:
  - openclaw render deploy
  - render blueprint render.yaml
  - infrastructure as code openclaw
  - openclaw_gateway_token generatevalue
  - render persistent disk data
  - healthcheckpath health render
  - render custom domain tls
  - render scaling cold start
topics:
  - OpenClaw
  - Install on Render
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/render
access_control_group: ["general"]
---

# OpenClaw — Deploy on Render with a Blueprint

## Overview

This note is the step-by-step procedure for deploying the OpenClaw Gateway on [Render](https://render.com) using its Infrastructure-as-Code (IaC) `render.yaml` **Blueprint**, mirroring the `install/render` source page. The Blueprint defines the entire stack declaratively — the web service, the persistent disk, and the environment variables — so the deploy is a single click and the infrastructure is versioned alongside the code. The note walks through prerequisites, the Blueprint deploy link, the `render.yaml` fields, plan/disk trade-offs, reaching the Control UI, the Render Dashboard operations (logs / shell / env / auto-deploy), custom domains, scaling, backup/migration, and the four troubleshooting cases. Code and config keys are reproduced verbatim from the source.

## Prerequisites

Two things are required before deploying:

- A [Render account](https://render.com) (free tier available).
- An API key from your preferred [model provider](https://docs.openclaw.ai/providers).

## Deploy with a Render Blueprint

Use the one-click deploy link `https://render.com/deploy?repo=https://github.com/openclaw/openclaw`. Clicking it will:

1. Create a new Render service from the `render.yaml` Blueprint at the root of the repo.
2. Build the Docker image and deploy.

Once deployed, the service URL follows the pattern `https://<service-name>.onrender.com`.

## Understanding the Blueprint

Render Blueprints are YAML files that define the infrastructure. The `render.yaml` in the OpenClaw repository configures everything needed to run OpenClaw — verbatim:

```yaml
services:
  - type: web
    name: openclaw
    runtime: docker
    plan: starter
    healthCheckPath: /health
    envVars:
      - key: OPENCLAW_GATEWAY_PORT
        value: "8080"
      - key: OPENCLAW_STATE_DIR
        value: /data/.openclaw
      - key: OPENCLAW_WORKSPACE_DIR
        value: /data/workspace
      - key: OPENCLAW_GATEWAY_TOKEN
        generateValue: true # auto-generates a secure token
    disk:
      name: openclaw-data
      mountPath: /data
      sizeGB: 1
```

The key Blueprint features used (each load-bearing for state persistence and health):

| Feature | Purpose |
| --- | --- |
| `runtime: docker` | Builds from the repo's Dockerfile |
| `healthCheckPath` | Render monitors `/health` and restarts unhealthy instances |
| `generateValue: true` | Auto-generates a cryptographically secure value |
| `disk` | Persistent storage that survives redeploys |

The recurring required-state-persistence pattern is encoded here: `OPENCLAW_STATE_DIR=/data/.openclaw` and `OPENCLAW_WORKSPACE_DIR=/data/workspace` point at the disk mounted at `/data`, and `OPENCLAW_GATEWAY_TOKEN` is auto-generated as the admin secret rather than hard-coded.

## Choosing a plan

The plan determines spin-down behavior and disk availability:

| Plan | Spin-down | Disk | Best for |
| --- | --- | --- | --- |
| Free | After 15 min idle | Not available | Testing, demos |
| Starter | Never | 1GB+ | Personal use, small teams |
| Standard+ | Never | 1GB+ | Production, multiple channels |

The Blueprint defaults to `starter`. To use the free tier, change `plan: free` in your fork's `render.yaml` — but note that no persistent disk means OpenClaw state resets on each deploy.

## After deployment

### Access the Control UI

The web dashboard is available at `https://<your-service>.onrender.com/`. Connect using the configured shared secret: this deploy template auto-generates `OPENCLAW_GATEWAY_TOKEN` (find it in **Dashboard → your service → Environment**); if you replace it with password auth, use that password instead.

## Render Dashboard features

Render exposes four operational surfaces from the service dashboard.

### Logs

View real-time logs in **Dashboard → your service → Logs**. They can be filtered by Build logs (Docker image creation), Deploy logs (service startup), and Runtime logs (application output).

### Shell access

For debugging, open a shell session via **Dashboard → your service → Shell**. The persistent disk is mounted at `/data`.

### Environment variables

Modify variables in **Dashboard → your service → Environment**. Changes trigger an automatic redeploy.

### Auto-deploy

If you use the original OpenClaw repository, Render will not auto-deploy your OpenClaw. To update it, run a manual Blueprint sync from the dashboard.

## Custom domain

To attach a custom domain:

1. Go to **Dashboard → your service → Settings → Custom Domains**.
2. Add your domain.
3. Configure DNS as instructed (CNAME to `*.onrender.com`).
4. Render provisions a TLS certificate automatically.

## Scaling

Render supports both horizontal and vertical scaling. **Vertical**: change the plan to get more CPU/RAM. **Horizontal**: increase the instance count (Standard plan and above). For OpenClaw, vertical scaling is usually sufficient; horizontal scaling requires sticky sessions or external state management.

## Backups and migration

Export the state, config, auth profiles, and workspace at any time using the shell access in the Render Dashboard:

```bash
openclaw backup create
```

This creates a portable backup archive with OpenClaw state plus any configured workspace. See [Backup](https://docs.openclaw.ai/cli/backup) for details.

## Troubleshooting

Four failure cases the source page documents:

- **Service will not start** — Check the deploy logs in the Render Dashboard. Common issues are a missing `OPENCLAW_GATEWAY_TOKEN` (verify it is set in **Dashboard → Environment**) and a port mismatch (ensure `OPENCLAW_GATEWAY_PORT=8080` is set so the gateway binds to the port Render expects).
- **Slow cold starts (free tier)** — Free tier services spin down after 15 minutes of inactivity, so the first request after spin-down takes a few seconds while the container starts. Upgrade to the Starter plan for always-on.
- **Data loss after redeploy** — This happens on the free tier (no persistent disk). Upgrade to a paid plan, or regularly export a full backup via `openclaw backup create` in the Render shell.
- **Health check failures** — Render expects a 200 response from `/health` within 30 seconds. If builds succeed but deploys fail, the service may be taking too long to start; check the build logs for errors and whether the container runs locally with `docker build && docker run`.

## Next steps

- Set up messaging channels: [Channels](https://docs.openclaw.ai/channels).
- Configure the Gateway: [Gateway configuration](https://docs.openclaw.ai/gateway/configuration).
- Keep OpenClaw up to date: [Updating](https://docs.openclaw.ai/install/updating).

**Source**: OpenClaw documentation — `install/render` (mirror `inbox/openclaw_docs/install/render.md`)
**Last Updated**: 2026-06-22
**Status**: Active
