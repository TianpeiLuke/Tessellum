---
tags:
  - resource
  - documentation
  - claude_code
  - surfaces
  - integrations
keywords:
  - platforms and integrations
  - where to run claude code
  - cli desktop vs code jetbrains web mobile
  - connect your tools
  - chrome github gitlab slack integrations
  - work when you are away
  - dispatch remote control channels scheduled tasks
topics:
  - Claude Code
  - Platforms and Integrations
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/platforms
access_control_group: ["general"]
---

# Claude Code — Platforms and Integrations

## Overview

Claude Code runs the same underlying engine everywhere, but each surface is tuned for a different way of working. This page helps you pick the right platform for your workflow, connect the tools you already use, and choose a way to keep work going when you are not at your terminal. You can mix surfaces on the same project — configuration, project memory, and MCP servers are shared across the local surfaces.

## Where to run Claude Code

Choose a platform based on how you like to work and where your project lives:

- **CLI** — best for terminal workflows, scripting, and remote servers. Gives the full feature set, the Agent SDK, computer use on macOS (Pro and Max), and third-party providers.
- **Desktop** — best for visual review, parallel sessions, and managed setup. Gives a diff viewer, app preview, and computer use plus Dispatch on Pro and Max.
- **VS Code** — best for working inside VS Code without switching to a terminal. Gives inline diffs, an integrated terminal, and file context.
- **JetBrains** — best for working inside IntelliJ, PyCharm, WebStorm, or other JetBrains IDEs. Gives a diff viewer, selection sharing, and a terminal session.
- **Web** — best for long-running tasks that need little steering, or work that should continue when you are offline. Runs in Anthropic-managed cloud and continues after you disconnect.
- **Mobile** — best for starting and monitoring tasks while away from your computer. Provides cloud sessions from the Claude app for iOS and Android, Remote Control for local sessions, and Dispatch to Desktop on Pro and Max.

The CLI is the most complete surface for terminal-native work: scripting and the Agent SDK are CLI-only. Third-party providers also work in VS Code. Enterprise Desktop deployments support Vertex AI and gateway providers; for Bedrock or Foundry, use the CLI or VS Code (or the Cowork on 3P research preview). Desktop and the IDE extensions trade some CLI-only features for visual review and tighter editor integration. The web runs in Anthropic's cloud, so tasks keep going after you disconnect. Mobile is a thin client into those same cloud sessions or into a local session via Remote Control, and can send tasks to Desktop with Dispatch.

## Connect your tools

Integrations let Claude work with services outside your codebase:

- **Chrome** — controls your browser with your logged-in sessions; use it for testing web apps, filling forms, and automating sites without an API.
- **GitHub Actions** — runs Claude in your CI pipeline; use it for automated PR reviews, issue triage, and scheduled maintenance.
- **GitLab CI/CD** — the same as GitHub Actions, for GitLab; use it for CI-driven automation on GitLab.
- **Code Review** — reviews every PR automatically; use it for catching bugs before human review.
- **Slack** — responds to `@Claude` mentions in your channels; use it for turning bug reports into pull requests from team chat.

For integrations not listed here, MCP servers and connectors let you connect almost anything — Linear, Notion, Google Drive, or your own internal APIs.

## Work when you are away from your terminal

Claude Code offers several ways to work when you are not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up:

- **Dispatch** — triggered by messaging a task from the Claude mobile app; Claude runs on your machine (Desktop) after you pair the mobile app with Desktop. Best for delegating work while away, with minimal setup.
- **Remote Control** — triggered by driving a running session from claude.ai/code or the Claude mobile app; Claude runs on your machine (CLI or VS Code) after you run `claude remote-control`. Best for steering in-progress work from another device.
- **Channels** — triggered by push events from a chat app like Telegram or Discord, or your own server; Claude runs on your machine (CLI) after you install a channel plugin or build your own. Best for reacting to external events like CI failures or chat messages.
- **Slack** — triggered by mentioning `@Claude` in a team channel; Claude runs in the Anthropic cloud after you install the Slack app with Claude Code on the web enabled. Best for PRs and reviews from team chat.
- **Scheduled tasks** — triggered by a schedule you set; Claude runs on the CLI, Desktop, or cloud once you pick a frequency. Best for recurring automation like daily reviews.

If you are not sure where to start, install the CLI and run it in a project directory. If you would rather not use a terminal, Desktop gives you the same engine with a graphical interface.

**Source**: https://code.claude.com/docs/en/platforms
**Last Updated**: 2026-06-13
**Status**: Active
