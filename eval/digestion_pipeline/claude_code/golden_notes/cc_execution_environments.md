---
tags:
  - resource
  - documentation
  - claude_code
  - agentic_loop
  - environments
keywords:
  - execution environments
  - local cloud remote control
  - anthropic-managed vms
  - interfaces
  - same agentic loop everywhere
  - terminal ide slack ci/cd
  - claude.ai/code
topics:
  - Claude Code
  - Environments and Interfaces
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/how-claude-code-works
access_control_group: ["general"]
---

# Claude Code — Execution Environments and Interfaces

## Overview

The agentic loop, tools, and capabilities of Claude Code are **the same everywhere** you use it. What changes is two orthogonal dimensions: **where the code executes** (the execution environment) and **how you interact with Claude** (the interface). The underlying agentic loop is identical across both — the environment and interface only determine where work runs and how you see it.

## Execution Environments

Claude Code runs in three environments, each with different tradeoffs for where your code executes:

- **Local** — code runs on **your machine**. This is the default and gives full access to your files, tools, and environment.
- **Cloud** — code runs on **Anthropic-managed VMs**. Used to offload tasks and to work on repos you don't have locally.
- **Remote Control** — code runs on **your machine but is controlled from a browser**, letting you use the web UI while keeping everything local.

## Interfaces

You can access Claude Code through several interfaces: the terminal, the desktop app, IDE extensions, claude.ai/code, Remote Control, Slack, and CI/CD pipelines. The interface determines how you see and interact with Claude, but the underlying agentic loop is identical regardless of which one you use. (Per-surface setup and detail are covered in [Platforms and Integrations](cc_platforms_and_integrations.md).)

**Source**: https://code.claude.com/docs/en/how-claude-code-works
**Last Updated**: 2026-06-13
**Status**: Active
