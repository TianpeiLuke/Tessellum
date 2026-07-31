---
tags:
  - resource
  - documentation
  - claude_code
  - sandboxing
  - isolation
keywords:
  - sandbox runtime
  - whole-process isolation
  - dev container
  - custom container
  - virtual machine
  - microvm
  - claude code on the web
  - default-deny firewall
topics:
  - Claude Code
  - Sandboxing
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/sandbox-environments
access_control_group: ["general"]
---

# Sandbox Runtime and Containers

## Overview

Beyond the per-command Bash sandbox, Claude Code can be wrapped so that the **whole process** — file tools, MCP servers, and hooks included — runs inside an isolation boundary. This note walks through the whole-process isolation setups from the [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments) page: the `@anthropic-ai/sandbox-runtime` package (deny-by-default, host-OS based, no Docker), Docker-based **dev containers** and **custom containers**, a dedicated **virtual machine** for kernel-level separation, and the Anthropic-hosted **Claude Code on the web** VM.

These approaches differ from the built-in [sandboxed Bash tool](https://code.claude.com/docs/en/sandbox-environments#sandboxed-bash-tool), which restricts only Bash commands and leaves file tools, MCP servers, and hooks running directly on the host. Choose among them with the comparison/decision matrix in [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments); this note is the setup detail for the whole-process options.

## Sandbox runtime

The [`@anthropic-ai/sandbox-runtime`](https://github.com/anthropic-experimental/sandbox-runtime) package wraps an entire process in the same Seatbelt or bubblewrap isolation that the built-in Bash sandbox uses. Running Claude Code through it constrains every tool, hook, and MCP server in the session, not only Bash. The runtime is a **beta research preview**, and its configuration format may change as the package evolves.

The runtime **denies all write and network access by default**, so configure it before launching Claude Code through it. In `~/.srt-settings.json`, or a file you pass with `--settings`, allow:

- write access to at least your project directory and Claude Code's configuration paths `~/.claude` and `~/.claude.json`
- the network domains your session needs, including `api.anthropic.com` or your configured provider's endpoint

See the package README for the full configuration schema.

Once the settings file is in place, launch Claude Code with `npx` and pass `claude` as the command to wrap:

```bash
npx @anthropic-ai/sandbox-runtime claude
```

Claude Code starts inside the sandbox with the filesystem and network boundaries you configured. The same command works for sandboxing standalone MCP servers or other helper processes.

## Dev containers

A dev container runs Claude Code inside a Docker container that VS Code or a compatible editor manages, with your project mounted in. You can define your own with a `.devcontainer/` directory in your repository.

The claude-code repository publishes an [example dev container](https://code.claude.com/docs/en/devcontainer) with a **default-deny iptables firewall** as a starting point. Copy it into your repository and adjust the firewall allowlist, base image, and pinned Claude Code version to fit your environment. Because the firewall blocks unapproved egress, a configuration like this supports running Claude Code with `--dangerously-skip-permissions` for unattended work.

## Custom container

You can run Claude Code in any Docker or OCI container image with your own network policies, mounted volumes, and seccomp profiles. This is the most common path for organizations with existing container infrastructure or CI runners.

Several managed sandbox and remote execution services can host the container for you. The same checklist applies as for any container you operate: review what is mounted writable, what credentials and tokens are reachable inside it, and what the network egress policy allows.

You can layer the built-in Bash sandbox inside the container for per-command restrictions. Unprivileged containers need the nested-sandbox setting described in [Sandbox limitations and troubleshooting](cc_sandbox_limitations_and_troubleshooting.md).

## Virtual machine

A dedicated virtual machine provides the **strongest separation**, with its own kernel and, in cloud or microVM deployments, its own virtualized hardware. Options include cloud instances, local hypervisors, and microVMs such as Firecracker.

Use this approach when you are evaluating untrusted code, when your security policy requires kernel-level separation between the agent and the host, or when no host-level approach meets your compliance requirements. Docker Desktop's sandboxes feature provides a microVM with its own Docker daemon and workspace sync, which can run Claude Code on hosts that already have Docker Desktop.

## Claude Code on the web

[Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) runs each session in an isolated, **Anthropic-managed virtual machine**. A network proxy enforces a default allowlist, and a separate proxy holds your GitHub token outside the sandbox while issuing scoped credentials for repository access inside it.

Use this approach when you want full VM isolation without provisioning infrastructure yourself, or when you are delegating tasks from a device that does not have a local development environment. It requires a Claude subscription and a connected GitHub account, and sessions clone your repository from GitHub. See [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) for plan availability and GitHub authentication options.

**Source**: https://code.claude.com/docs/en/sandbox-environments
**Last Updated**: 2026-06-13
**Status**: Active
