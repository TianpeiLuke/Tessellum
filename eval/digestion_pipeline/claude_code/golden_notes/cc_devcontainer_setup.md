---
tags:
  - resource
  - documentation
  - claude_code
  - dev_containers
  - setup
keywords:
  - dev container
  - devcontainer.json
  - claude code dev container feature
  - rebuild container
  - sign in to claude code
  - reference container
  - bind-mounted workspace
  - github codespaces
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

# Claude Code — Dev Container Setup

## Overview

A [development container](https://containers.dev/), or dev container, lets you define an identical, isolated environment that every engineer on your team can run. With Claude Code installed in that container, commands Claude runs execute inside it rather than on the host machine, while edits to your project files appear in your local repository as you work. This note covers the install-and-run path: how the container wraps Claude Code, adding the Claude Code Dev Container Feature to `devcontainer.json`, rebuilding, signing in, and trying the reference container.

Hardening a working container — persisting authentication across rebuilds, enforcing organization policy, restricting network egress, and running without permission prompts — is covered in the sibling note [Dev Container Hardening](cc_devcontainer_hardening.md).

## How dev containers work with your editor

A dev container runs as a Docker container, either on your machine or on a cloud host such as GitHub Codespaces. An editor that supports the Dev Containers spec — such as VS Code, GitHub Codespaces, a JetBrains IDE, or Cursor — connects to that container: you browse and edit files in the editor as usual, but the integrated terminal, language servers, and build tools all run inside the container rather than on your host. Editors without dev container support, such as plain Vim, are not part of this workflow.

Claude Code runs inside the container, so it sees the same files, dependencies, and tools as the rest of your project's toolchain. In VS Code you can use either the [Claude Code extension panel](https://code.claude.com/docs/en/vs-code) or run `claude` in the integrated terminal; both run inside the container and share the same `~/.claude` configuration. The host repository is bind-mounted into the container as the workspace.

## Add Claude Code to your dev container

Claude Code installs into any dev container through the [Claude Code Dev Container Feature](https://github.com/anthropics/devcontainer-features/tree/main/src/claude-code). The settings work with any tool that supports the Dev Containers spec, such as VS Code, GitHub Codespaces, or JetBrains IDEs; the steps below use VS Code as an example. When you open the container in VS Code or Codespaces, the feature also adds the Claude Code VS Code extension; other editors ignore that part.

**Step 1 — Create or update `devcontainer.json`.** Save the following as `.devcontainer/devcontainer.json` in your repository, or add the `features` block to your existing file. The version tag at the end, such as `:1.0`, pins the feature's install script, not the Claude Code release: the feature installs the latest Claude Code, and Claude Code auto-updates itself inside the container by default. To pin the CLI version or disable auto-update, see [Dev Container Hardening](cc_devcontainer_hardening.md).

```json .devcontainer/devcontainer.json theme={null}
{
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/anthropics/devcontainer-features/claude-code:1.0": {}
  }
}
```

Replace the `image` line with your project's base image or remove it if your existing file uses a Dockerfile.

**Step 2 — Rebuild the container.** Open the VS Code Command Palette with `Cmd+Shift+P` on Mac or `Ctrl+Shift+P` on Windows and Linux, and run **Dev Containers: Rebuild Container**. For other tools, follow that tool's rebuild action (GitHub Codespaces rebuild, the Dev Containers CLI, or your IDE's dev container documentation).

**Step 3 — Sign in to Claude Code.** Open a terminal in the rebuilt container and run `claude`, then follow the authentication prompt.

### Authentication prompt

What you see at the authentication prompt depends on your provider:

- **Anthropic**: sign in through a browser with your Claude or Anthropic Console account.
- **Amazon Bedrock, Google Vertex AI, or Microsoft Foundry**: Claude Code uses your cloud provider credentials, with no browser prompt.

For cloud providers, pass credentials into the container as environment variables through `containerEnv`, a Codespaces secret, or your cloud's workload identity rather than mounting credential files from the host. See the [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), or [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry) pages for the credential chain Claude Code reads, and [Choose your API provider](https://code.claude.com/docs/en/admin-setup#choose-your-api-provider) to decide which path fits your organization.

If the browser sign-in completes but the callback never reaches the container, copy the code shown in the browser and paste it at the `Paste code here if prompted` prompt in the terminal. This can happen when the editor's port forwarding doesn't route the localhost callback.

## Try the reference container

The [`anthropics/claude-code`](https://github.com/anthropics/claude-code/tree/main/.devcontainer) repository includes an example dev container that combines the CLI, the egress firewall, persistent volumes, and a Zsh-based shell. It is provided as a working example rather than a maintained base image; use it to see how the pieces fit together before applying them to your own configuration. The steps: (1) install VS Code and the Dev Containers extension; (2) clone the Claude Code repository and open it in VS Code; (3) when prompted, click **Reopen in Container**, or run **Dev Containers: Reopen in Container** from the Command Palette; (4) once the container finishes building, open a terminal with `` Ctrl+` `` and run `claude` to sign in and start your first session.

To use this configuration with your own project, copy the `.devcontainer/` directory into your repository and adjust the Dockerfile for your toolchain, or return to *Add Claude Code to your dev container* to add only the feature to a setup you already have. The reference configuration consists of three files; none are required when you add Claude Code through the feature, but they show one way to combine the pieces:

| File | Purpose |
| --- | --- |
| `devcontainer.json` | Volume mounts, `runArgs` capabilities, VS Code extensions, and `containerEnv` |
| `Dockerfile` | Base image, development tools, and the Claude Code install |
| `init-firewall.sh` | Blocks all outbound network traffic except the allowed domains |

## Next steps

Once Claude Code is running in your dev container, the pages below cover the rest of an organization rollout: choosing an authentication path, delivering managed policy outside the repository, monitoring usage, and understanding what Claude Code stores and sends. The persist-auth, managed-policy, egress, and no-prompts mechanics are digested in [Dev Container Hardening](cc_devcontainer_hardening.md).

- [Set up Claude Code for your organization](https://code.claude.com/docs/en/admin-setup): choose an authentication provider, decide how policy reaches devices, and plan the rollout.
- [Server-managed settings](https://code.claude.com/docs/en/server-managed-settings): deliver managed policy from the Claude.ai admin console so engineers cannot bypass it by editing repository files.
- [Monitor usage and audit activity](https://code.claude.com/docs/en/monitoring-usage): export OpenTelemetry metrics and review what your team is running.
- [Explore the `.claude` directory](https://code.claude.com/docs/en/claude-directory): what the volume mount holds, including credentials, settings, and session history.
- [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments): compare dev containers with the built-in Bash sandbox, custom containers, and VMs.

**Source**: https://code.claude.com/docs/en/devcontainer
**Last Updated**: 2026-06-13
**Status**: Active
