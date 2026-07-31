---
tags:
  - resource
  - documentation
  - claude_code
  - dev_containers
  - hardening
keywords:
  - dev container hardening
  - persist authentication
  - named volume mount
  - managed-settings.json
  - containerenv policy
  - restrict network egress
  - init-firewall
  - dangerously-skip-permissions
topics:
  - Claude Code
  - Dev Containers
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/devcontainer
access_control_group: ["general"]
---

# Claude Code — Harden a Dev Container

## Overview

Once Claude Code is installed in a dev container (see [Add Claude Code to your dev container](cc_devcontainer_setup.md)), four self-contained hardening topics keep the environment reproducible, governed, and contained: **persist authentication** so engineers don't re-sign-in every rebuild, **enforce organization policy** so the same settings apply on every machine, **restrict network egress** so the container can only reach the domains it needs, and **run without permission prompts** safely when the container's isolation justifies it. Each topic is independent — apply the ones that match your setup.

The page opens with a security warning that frames why this matters: while a dev container provides substantial protections, no system is immune to all attacks. When run with `--dangerously-skip-permissions`, a dev container does not prevent a malicious project from exfiltrating anything accessible inside the container, including the Claude Code credentials stored in `~/.claude`. Only use dev containers with trusted repositories and monitor Claude's activities. Avoid mounting host secrets such as `~/.ssh` or cloud credential files into the container; prefer repository-scoped or short-lived tokens.

## Persist authentication and settings across rebuilds

By default the container's home directory is discarded on rebuild, so engineers must sign in again each time. Claude Code stores its authentication token, user settings, and session history under `~/.claude`. Mount a named volume at that path to keep this state across rebuilds. The following example mounts a volume at the home directory of the `node` user:

```json devcontainer.json theme={null}
"mounts": [
  "source=claude-code-config,target=/home/node/.claude,type=volume"
]
```

Replace `/home/node` with the home directory of your container's `remoteUser`. If you mount the volume somewhere other than `~/.claude`, set [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/en/env-vars) to the mount path so Claude Code reads and writes there.

To isolate state per project rather than sharing one volume across all repositories, include the `${devcontainerId}` variable in the source name. The reference configuration uses `source=claude-code-config-${devcontainerId}` for this purpose.

In GitHub Codespaces, `~/.claude` persists across stopping and starting a codespace, but is still cleared when you rebuild the container, so the volume mount above applies there too. To carry authentication across codespaces, store `ANTHROPIC_API_KEY` or a `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token` as a Codespaces secret; Codespaces makes secrets available as environment variables inside the container automatically.

## Enforce organization policy

A dev container is a convenient place to apply organization policy, because the same image and configuration run on every engineer's machine.

Claude Code reads `/etc/claude-code/managed-settings.json` on Linux and applies it at the highest precedence in the settings hierarchy, so values there override anything an engineer sets in `~/.claude` or the project's `.claude/` directory. Copy the file into place from your Dockerfile:

```dockerfile Dockerfile theme={null}
RUN mkdir -p /etc/claude-code
COPY managed-settings.json /etc/claude-code/managed-settings.json
```

Because the Dockerfile lives in the repository, anyone with write access can change or remove this step. For policy that engineers cannot bypass by editing repository files, deliver managed settings through [server-managed settings](https://code.claude.com/docs/en/server-managed-settings) or your MDM instead. See [managed settings files](https://code.claude.com/docs/en/settings#settings-files) for the available keys and the other delivery paths.

To set environment variables that apply to every Claude Code session in the container, add them to `containerEnv` in your `devcontainer.json`. The following example opts out of telemetry and error reporting and prevents Claude Code from auto-updating after install:

```json devcontainer.json theme={null}
"containerEnv": {
  "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
  "DISABLE_AUTOUPDATER": "1"
}
```

The Dev Container Feature always installs the latest Claude Code release. To pin a specific Claude Code version for reproducible builds, install it from your Dockerfile with `npm install -g @anthropic-ai/claude-code@X.Y.Z` instead of using the feature, and set `DISABLE_AUTOUPDATER` as shown above. For the full list of policy controls including permission rules, tool restrictions, and MCP server allowlists, see [Set up Claude Code for your organization](https://code.claude.com/docs/en/admin-setup).

To make MCP servers available inside the container, define them at project scope in a `.mcp.json` file at the repository root so they are checked in alongside your dev container configuration. Install any binaries that local stdio servers depend on in your Dockerfile, and add remote server domains to your network allowlist.

## Restrict network egress

You can limit the container's outbound traffic to only the domains Claude Code needs. See [Network access requirements](https://code.claude.com/docs/en/network-config#network-access-requirements) for the inference and authentication domains, and [Telemetry services](https://code.claude.com/docs/en/data-usage#telemetry-services) for the optional telemetry and error reporting connections and how to disable them.

The reference container includes an `init-firewall.sh` script that blocks all outbound traffic except the domains Claude Code and your development tools need. Running a firewall inside a container requires extra permissions, so the reference adds the `NET_ADMIN` and `NET_RAW` capabilities through `runArgs`. The firewall script and these capabilities are not required for Claude Code itself: you can leave them out and rely on your own network controls instead.

## Run without permission prompts

Because the container runs Claude Code as a non-root user and confines command execution to the container, you can pass `--dangerously-skip-permissions` for unattended operation. The CLI rejects this flag when launched as root, so confirm `remoteUser` is set to a non-root account.

Skipping permission prompts removes your opportunity to review tool calls before they run. Claude can still modify any file in the bind-mounted workspace, which appears directly on your host, and reach anything the container's network policy allows. Pair this flag with the network egress restrictions above to limit what a bypassed session can reach.

If you want fewer prompts without disabling safety checks, consider [auto mode](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode) instead, which has a classifier review actions before they run. To prevent engineers from using `--dangerously-skip-permissions` at all, set `permissions.disableBypassPermissionsMode` to `"disable"` in [managed settings](https://code.claude.com/docs/en/settings#permission-settings).

**Source**: https://code.claude.com/docs/en/devcontainer
**Last Updated**: 2026-06-13
**Status**: Active
