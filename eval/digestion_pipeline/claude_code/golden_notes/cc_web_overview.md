---
tags:
  - resource
  - documentation
  - claude_code
  - web
  - cloud
keywords:
  - claude code on the web
  - cloud session
  - anthropic-managed vm
  - claude.ai/code
  - clone configure work push
  - parallel tasks
  - research preview
  - monitor from mobile
topics:
  - Claude Code
  - Web
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/claude-code-on-the-web
access_control_group: ["general"]
---

# Claude Code on the Web — Overview

## Overview

**Claude Code on the web** runs tasks on **Anthropic-managed cloud infrastructure** at [claude.ai/code](https://claude.ai/code) instead of on your machine. You submit a task from your browser or the Claude mobile app, Claude clones your GitHub repository into an **isolated virtual machine**, makes changes, and pushes a branch for you to review. Sessions persist even if you close the browser and persist across devices, so a task you start on your laptop can be reviewed from your phone later. As of these docs, the surface is in **research preview** for Pro, Max, and Team users, and for Enterprise users with premium seats or Chat + Claude Code seats.

This note is the identity page for the web surface: what it is, the clone→configure→work→push lifecycle a session follows, and what kinds of work it fits. The onboarding walkthrough lives in [Web Quickstart](cc_web_quickstart.md); the per-session VM itself is detailed in [Cloud Environment](cc_cloud_environment.md).

## What it is

Claude Code on the web runs on Anthropic-managed cloud infrastructure rather than your machine. You submit tasks from claude.ai/code in your browser or the Claude mobile app. You need a GitHub repository to get started: Claude clones it into an isolated VM, makes changes, and pushes a branch for you to review. Because the work runs in the cloud, sessions persist across devices.

Claude Code **behaves the same everywhere** — what changes between surfaces is *where code executes* and *whether your local config is available*. On the web, code runs on an Anthropic cloud VM, you chat from claude.ai or the mobile app, only the repo (not your local config) is available, and the session keeps running if you disconnect. The full cross-surface comparison (web vs Remote Control vs Terminal CLI vs Desktop app) is in [Remote Control vs Web and Deep Links](cc_remote_vs_web_and_deep_links.md).

## How sessions run

When you submit a task, the session moves through four phases:

1. **Clone and prepare** — your repository is cloned to an Anthropic-managed VM, and your setup script runs if configured.
2. **Configure network** — internet access is set based on your environment's access level.
3. **Work** — Claude analyzes code, makes changes, runs tests, and checks its work. You can watch and steer throughout, or step away and come back when it's done.
4. **Push the branch** — when Claude reaches a stopping point, it pushes its branch to GitHub. You review the diff, leave inline comments, create a PR, or send another message to keep going.

The session does **not** close when the branch is pushed. PR creation and further edits all happen within the same conversation.

## What it's good for

Claude Code on the web works well for:

- **Parallel tasks** — run several independent tasks at once, each in its own session and branch, without managing multiple worktrees.
- **Repos you don't have locally** — Claude clones the repo fresh every session, so you don't need it checked out.
- **Tasks that don't need frequent steering** — submit a well-defined task, do something else, and review the result when Claude is done.
- **Code questions and exploration** — understand a codebase or trace how a feature is implemented without a local checkout.

For work that needs your local config, tools, or environment, running Claude Code locally or using [Remote Control](cc_remote_control.md) is a better fit.

**Source**: https://code.claude.com/docs/en/claude-code-on-the-web
**Last Updated**: 2026-06-13
**Status**: Active
