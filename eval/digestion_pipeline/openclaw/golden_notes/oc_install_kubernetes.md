---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - kubernetes
keywords:
  - openclaw kubernetes deploy
  - kustomize openclaw manifests
  - deploy.sh openclaw gateway token
  - kubectl port-forward openclaw 18789
  - openclaw-secrets openclaw-config configmap
  - persistentvolumeclaim 10gi agent state
  - kind local testing openclaw
  - pod security hardening readonlyrootfilesystem
  - openclaw_namespace custom namespace
  - ghcr.io openclaw image
topics:
  - OpenClaw
  - Kubernetes Deployment
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/kubernetes
access_control_group: ["general"]
---

# OpenClaw — Deploy to Kubernetes with Kustomize

## Overview

This procedure deploys the OpenClaw Gateway to a Kubernetes cluster using Kustomize, mirroring the `install/kubernetes` source page. It is a minimal starting point — not a production-ready deployment — covering the core resources and meant to be adapted to your environment. The page documents why Kustomize is used instead of Helm, the prerequisites, the `./scripts/k8s/deploy.sh` quick-start flow (including retrieving the Control UI token), local cluster testing with Kind, the two-option step-by-step deploy, the set of resources that get deployed, customization (agent instructions, gateway config, additional providers, custom namespace/image, and exposing beyond `port-forward`), re-deploy and teardown, the pod security/architecture notes, and the on-disk file structure of the deploy scripts and manifests.

## Why not Helm?

OpenClaw is a single container with some config files. The interesting customization is in agent content (markdown files, skills, config overrides), not infrastructure templating. Kustomize handles overlays without the overhead of a Helm chart. If your deployment grows more complex, a Helm chart can be layered on top of these manifests.

## What you need

- A running Kubernetes cluster (AKS, EKS, GKE, k3s, kind, OpenShift, etc.)
- `kubectl` connected to your cluster
- An API key for at least one model provider

## Quick start

Export your provider API key (replace `<PROVIDER>` with `ANTHROPIC`, `GEMINI`, `OPENAI`, or `OPENROUTER`), run the deploy script, then `port-forward` the Service and open the Control UI:

```bash
# Replace with your provider: ANTHROPIC, GEMINI, OPENAI, or OPENROUTER
export <PROVIDER>_API_KEY="..."
./scripts/k8s/deploy.sh

kubectl port-forward svc/openclaw 18789:18789 -n openclaw
open http://localhost:18789
```

To retrieve the configured shared secret for the Control UI — this deploy script creates token auth by default — read the `OPENCLAW_GATEWAY_TOKEN` key out of the Secret and base64-decode it:

```bash
kubectl get secret openclaw-secrets -n openclaw -o jsonpath='{.data.OPENCLAW_GATEWAY_TOKEN}' | base64 -d
```

For local debugging, `./scripts/k8s/deploy.sh --show-token` prints the token after deploy.

## Local testing with Kind

If you don't have a cluster, create one locally with Kind (`https://kind.sigs.k8s.io/`). `create-kind.sh` auto-detects docker or podman; pass `--delete` to tear the local cluster down, then deploy as usual with `./scripts/k8s/deploy.sh`:

```bash
./scripts/k8s/create-kind.sh           # auto-detects docker or podman
./scripts/k8s/create-kind.sh --delete  # tear down
```

## Step by step

### 1) Deploy

**Option A** — API key in environment (one step): export `<PROVIDER>_API_KEY` and run `./scripts/k8s/deploy.sh`. The script creates a Kubernetes Secret with the API key and an auto-generated gateway token, then deploys. If the Secret already exists, it preserves the current gateway token and any provider keys not being changed.

**Option B** — create the secret separately, by running the deploy with `--create-secret` first and then deploying:

```bash
export <PROVIDER>_API_KEY="..."
./scripts/k8s/deploy.sh --create-secret
./scripts/k8s/deploy.sh
```

Use `--show-token` with either command if you want the token printed to stdout for local testing.

### 2) Access the gateway

Forward the `openclaw` Service's port 18789 to localhost and open the Control UI with `kubectl port-forward svc/openclaw 18789:18789 -n openclaw` followed by `open http://localhost:18789` (same invocation as the Quick start).

## What gets deployed

All resources live in a single namespace `openclaw` (configurable via `OPENCLAW_NAMESPACE`):

```
Namespace: openclaw (configurable via OPENCLAW_NAMESPACE)
├── Deployment/openclaw        # Single pod, init container + gateway
├── Service/openclaw           # ClusterIP on port 18789
├── PersistentVolumeClaim      # 10Gi for agent state and config
├── ConfigMap/openclaw-config  # openclaw.json + AGENTS.md
└── Secret/openclaw-secrets    # Gateway token + API keys
```

## Customization

**Agent instructions** — Edit the `AGENTS.md` in `scripts/k8s/manifests/configmap.yaml` and redeploy with `./scripts/k8s/deploy.sh`.

**Gateway config** — Edit `openclaw.json` in `scripts/k8s/manifests/configmap.yaml`. See Gateway configuration (`/gateway/configuration`) for the full reference.

**Add providers** — Re-run with additional keys exported (e.g. both `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`) using `./scripts/k8s/deploy.sh --create-secret` then `./scripts/k8s/deploy.sh`; existing provider keys stay in the Secret unless you overwrite them. Or patch the Secret directly with `kubectl patch secret openclaw-secrets -n openclaw -p '{"stringData":{"<PROVIDER>_API_KEY":"..."}}'` and roll the deployment to pick it up with `kubectl rollout restart deployment/openclaw -n openclaw`.

**Custom namespace** — Override the target namespace inline: `OPENCLAW_NAMESPACE=my-namespace ./scripts/k8s/deploy.sh`.

**Custom image** — Edit the `image` field in `scripts/k8s/manifests/deployment.yaml`; the default is `ghcr.io/openclaw/openclaw:latest`, which you can pin to a specific version from `https://github.com/openclaw/openclaw/releases`.

**Expose beyond port-forward** — The default manifests bind the gateway to loopback inside the pod. That works with `kubectl port-forward`, but it does not work with a Kubernetes `Service` or Ingress path that needs to reach the pod IP. If you want to expose the gateway through an Ingress or load balancer: change the gateway bind in `scripts/k8s/manifests/configmap.yaml` from `loopback` to a non-loopback bind that matches your deployment model; keep gateway auth enabled and use a proper TLS-terminated entrypoint; and configure the Control UI for remote access using the supported web security model (for example HTTPS/Tailscale Serve and explicit allowed origins when needed).

## Re-deploy

Run `./scripts/k8s/deploy.sh` again. This applies all manifests and restarts the pod to pick up any config or secret changes.

## Teardown

Run `./scripts/k8s/deploy.sh --delete`. This deletes the namespace and all resources in it, including the PVC.

## Architecture notes

- The gateway binds to loopback inside the pod by default, so the included setup is for `kubectl port-forward`.
- No cluster-scoped resources — everything lives in a single namespace.
- Security: `readOnlyRootFilesystem`, `drop: ALL` capabilities, non-root user (UID 1000).
- The default config keeps the Control UI on the safer local-access path: loopback bind plus `kubectl port-forward` to `http://127.0.0.1:18789`.
- If you move beyond localhost access, use the supported remote model: HTTPS/Tailscale plus the appropriate gateway bind and Control UI origin settings.
- Secrets are generated in a temp directory and applied directly to the cluster — no secret material is written to the repo checkout.

## File structure

The deploy scripts and Kustomize manifests live under `scripts/k8s/`:

```
scripts/k8s/
├── deploy.sh                   # Creates namespace + secret, deploys via kustomize
├── create-kind.sh              # Local Kind cluster (auto-detects docker/podman)
└── manifests/
    ├── kustomization.yaml      # Kustomize base
    ├── configmap.yaml          # openclaw.json + AGENTS.md
    ├── deployment.yaml         # Pod spec with security hardening
    ├── pvc.yaml                # 10Gi persistent storage
    └── service.yaml            # ClusterIP on 18789
```

**Source**: OpenClaw documentation — `install/kubernetes` (mirror `inbox/openclaw_docs/install/kubernetes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
