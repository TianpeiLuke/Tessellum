---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - sandbox
keywords:
  - openclaw agent sandbox
  - docker sandbox backend
  - agents.defaults.sandbox
  - sandbox mode non-main
  - sandbox scope agent session shared
  - workspace mount isolation
  - openclaw_sandbox env var
  - untrusted multi-tenant agent isolation
topics:
  - OpenClaw
  - Agent Sandbox
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/install/docker
access_control_group: ["general"]
---

# OpenClaw — The Docker-Backend Agent Sandbox

## Overview

This note explains the **agent sandbox** concept from the `install/docker` source page (the "Agent sandbox" H2 and its "Quick enable" H3, plus the sandbox-specific troubleshooting). It is distinct from the containerized-gateway *deploy* procedure: the sandbox is an architectural isolation feature gated by `agents.defaults.sandbox` that runs agent tool execution inside isolated Docker containers while the gateway process itself stays on the host. The full sandbox reference (images, security notes, multi-agent profiles) lives at `/gateway/sandboxing`; this note documents only what the Docker install page mirrors — the concept, the scope/workspace/policy model, the quick-enable config, and the common failure modes.

## What the Agent Sandbox Is

When `agents.defaults.sandbox` is enabled with the Docker backend, the gateway runs agent tool execution (shell, file read/write, etc.) inside isolated Docker containers while the gateway itself stays on the host. This gives a hard wall around untrusted or multi-tenant agent sessions **without** containerizing the entire gateway — meaning the sandbox is independent of whether the gateway runs in Docker. The Docker source page is explicit that the default sandbox backend uses Docker when sandboxing is enabled, but sandboxing is **off by default** and does **not** require the full gateway to run in Docker; SSH and OpenShell sandbox backends are also available.

## Scope, Workspace, and Policy

Sandbox **scope** can be per-agent (the default), per-session, or shared. Each scope gets its own workspace mounted at `/workspace` inside the sandbox container. Beyond the workspace mount, you can also configure allow/deny tool policies, network isolation, resource limits, and browser containers per sandbox. These knobs are what make the sandbox a trust boundary rather than just a separate filesystem: the allow/deny tool policy plus network isolation constrain *what* a sandboxed agent can do, while the per-scope `/workspace` mount constrains *where* it can read and write.

The source page defers the complete configuration surface to three references rather than restating them here: [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing) (the complete sandbox reference), [OpenShell](https://docs.openclaw.ai/gateway/openshell) (interactive shell access to sandbox containers), and [Multi-Agent Sandbox and Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) (per-agent overrides). A Codex caveat applies even with the OpenClaw sandbox active: Codex code-mode turns are still constrained to Codex `workspace-write`, and you must **not** mount the host Docker socket into agent sandbox containers.

## Quick Enable

The minimal config opts an agent into the sandbox via the `agents.defaults.sandbox` block, choosing a `mode` and a `scope` (verbatim from source, JSON5):

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        scope: "agent", // session | agent | shared
      },
    },
  },
}
```

`mode` selects which agents are sandboxed (`off`, `non-main`, or `all`); `scope` selects the container-sharing granularity (`session`, `agent`, or `shared`). To build the default sandbox image from a source checkout:

```bash
scripts/sandbox-setup.sh
```

For npm installs without a source checkout, the source page points to *Sandboxing § Images and setup* for inline `docker build` commands. When enabling the sandbox during the Docker gateway setup itself, the install flow uses the `OPENCLAW_SANDBOX=1` env var (with optional `OPENCLAW_DOCKER_SOCKET` for rootless Docker) — the setup script mounts `docker.sock` only after sandbox prerequisites pass, and resets `agents.defaults.sandbox.mode` to `off` if sandbox setup cannot complete. That enable-during-setup path is documented in the containerized-gateway note.

## Troubleshooting

The Docker page lists three sandbox-specific failure modes:

- **Image missing or sandbox container not starting** — build the sandbox image with [`scripts/sandbox-setup.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/sandbox-setup.sh) (source checkout) or the inline `docker build` command from *Sandboxing § Images and setup* (npm install), or set `agents.defaults.sandbox.docker.image` to your custom image. Containers are auto-created per session on demand.
- **Permission errors in sandbox** — set `docker.user` to a UID:GID that matches your mounted workspace ownership, or chown the workspace folder.
- **Custom tools not found in sandbox** — OpenClaw runs commands with `sh -lc` (login shell), which sources `/etc/profile` and may reset PATH; set `docker.env.PATH` to prepend your custom tool paths, or add a script under `/etc/profile.d/` in your Dockerfile.

**Source**: OpenClaw documentation — `install/docker` (Agent sandbox + Quick enable; mirror `inbox/openclaw_docs/install/docker.md`)
**Last Updated**: 2026-06-22
**Status**: Active
