---
tags:
  - resource
  - documentation
  - claude_code
  - sandboxing
  - permissions
keywords:
  - sandbox vs permissions
  - complementary layers
  - permission rules
  - permission modes
  - os-level enforcement
  - auto-allow vs auto mode
  - sandbox is not a permission mode
  - setting vs rule mapping
topics:
  - Claude Code
  - Sandboxing
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/sandboxing
access_control_group: ["general"]
---

# Claude Code Sandbox vs Permissions

## Overview

Sandboxing, **permission rules**, and **permission modes** are three complementary layers in Claude Code, each controlling something different. Permission rules and permission modes decide *whether* a tool call runs and whether you are prompted; the sandbox restricts *what* a Bash command can access once it runs. Because they operate at different points and through different mechanisms, the sandbox is **not** itself a permission mode, and its auto-allow behavior is distinct from auto mode. This note explains how the layers interact — the rule/setting split, the merged filesystem and network configuration, and the per-mode comparison.

## Permission rules vs sandboxing

Permission rules and sandboxing control different things:

- **Permission rules** control which tools Claude Code can use and are evaluated **before any tool runs**. They apply to all tools: Bash, Read, Edit, WebFetch, MCP, and others.
- **Sandboxing** provides OS-level enforcement that restricts what Bash commands can access at the filesystem and network level. It applies **only to Bash commands and their child processes**.

The two layers also differ in *how* they are enforced. Claude Code evaluates permission decisions before a command runs, based on the command string and — in auto mode — a separate classifier's judgment about whether the command is safe. The operating system enforces the sandbox boundary on the running process, so it holds regardless of what the model chose to run and even if an allowed command does more than its name suggests.

### Setting-vs-rule mapping

Filesystem and network restrictions are configured through both sandbox settings and permission rules:

| Setting or rule | What it does |
| :--- | :--- |
| `sandbox.filesystem.allowWrite` | Grants subprocess write access to paths outside the working directory |
| `sandbox.filesystem.denyWrite` and `sandbox.filesystem.denyRead` | Block subprocess access to specific paths |
| `sandbox.filesystem.allowRead` | Re-allows reading specific paths within a `denyRead` region |
| `Edit` allow rules | Grant write access to specific paths, the same way `sandbox.filesystem.allowWrite` does |
| `Read` and `Edit` deny rules | Block access to specific files or directories |
| `WebFetch` allow and deny rules | Control domain access |
| Sandbox `allowedDomains` | Controls which domains Bash commands can reach |
| Sandbox `deniedDomains` | Blocks specific domains even when a broader `allowedDomains` wildcard would otherwise permit them |

Paths from **both** the `sandbox.filesystem` settings and the permission rules are **merged together** into the final sandbox configuration. The claude-code repository's examples directory includes starter settings configurations for common deployment scenarios, including sandbox-specific examples, to use as starting points.

## Permission modes vs the sandbox

`/sandbox` is **not** a permission mode. Permission modes decide whether a tool call runs and whether you are prompted first, while the sandbox restricts what a Bash command can access once it runs. They differ in what they control and what replaces the per-action prompt:

| | What it controls | What replaces the prompt |
| :--- | :--- | :--- |
| `/sandbox` | What a Bash command can access once it runs | The sandbox boundary itself, in auto-allow mode |
| Auto mode | Whether each tool call runs | A classifier that reviews actions |
| `--dangerously-skip-permissions` | Whether each tool call runs | Nothing. Protected path checks are also skipped; only explicit ask rules and removing `/` or your home directory still prompt |

The sandbox's **auto-allow mode** is separate from **auto mode**: auto-allow approves Bash commands because the sandbox boundary contains them, while auto mode uses a classifier to review actions. The two work independently and can be combined. To choose an isolation boundary for unattended runs, see [How isolation relates to permission modes](https://code.claude.com/docs/en/sandbox-environments#how-isolation-relates-to-permission-modes). For the auto-allow vs regular-permissions distinction within the sandbox itself, see [Sandbox modes](https://code.claude.com/docs/en/sandboxing#sandbox-modes).

**Source**: https://code.claude.com/docs/en/sandboxing
**Last Updated**: 2026-06-13
**Status**: Active
