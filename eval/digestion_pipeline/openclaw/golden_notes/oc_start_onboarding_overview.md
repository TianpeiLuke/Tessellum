---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - onboarding
keywords:
  - openclaw onboarding overview
  - cli vs macos app onboarding
  - openclaw onboard command
  - what onboarding configures
  - custom provider compat mode
  - non-interactive onboarding
  - gateway port bind auth
  - base url api key model id alias
topics:
  - OpenClaw
  - Onboarding
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/start/onboarding-overview
access_control_group: ["general"]
---

# OpenClaw — Onboarding Overview (Choosing a Path)

## Overview

This note is the procedure for choosing between OpenClaw's two onboarding paths and knowing what each one configures, mirroring the `start/onboarding-overview` source page. OpenClaw has two onboarding paths — **CLI onboarding** and **macOS app onboarding** — and both configure auth, the Gateway, and optional chat channels; they differ only in how you interact with the setup. The note covers the path-selection decision table, the five things onboarding always configures, the CLI and macOS app entry commands, and the Custom Provider option for providers not listed in onboarding.

## Which path should I use?

Use the decision table below to pick a path. CLI onboarding runs on macOS, Linux, and Windows (native or WSL2) through a terminal wizard, is best for servers, headless setups, and full control, supports `--non-interactive` for scripts, and is launched with `openclaw onboard`. macOS app onboarding runs on macOS only through a guided UI in the app, is best for a desktop Mac and visual setup, is manual only (no automation), and is launched by opening the app.

|                | CLI onboarding                         | macOS app onboarding      |
| -------------- | -------------------------------------- | ------------------------- |
| **Platforms**  | macOS, Linux, Windows (native or WSL2) | macOS only                |
| **Interface**  | Terminal wizard                        | Guided UI in the app      |
| **Best for**   | Servers, headless, full control        | Desktop Mac, visual setup |
| **Automation** | `--non-interactive` for scripts        | Manual only               |
| **Command**    | `openclaw onboard`                     | Launch the app            |

Most users should start with **CLI onboarding** — it works everywhere and gives you the most control.

## What onboarding configures

Regardless of which path you choose, onboarding sets up the same five things:

1. **Model provider and auth** — API key, OAuth, or setup token for your chosen provider.
2. **Workspace** — directory for agent files, bootstrap templates, and memory.
3. **Gateway** — port, bind address, auth mode.
4. **Channels** (optional) — built-in and bundled chat channels such as iMessage, Discord, Feishu, Google Chat, Mattermost, Microsoft Teams, Telegram, WhatsApp, and more.
5. **Daemon** (optional) — background service so the Gateway starts automatically.

## CLI onboarding

Run the onboarding wizard in any terminal:

```bash
openclaw onboard
```

Add `--install-daemon` to also install the background service in one step. The full reference is [Onboarding (CLI)](https://docs.openclaw.ai/start/wizard), and the CLI command docs are at [`openclaw onboard`](https://docs.openclaw.ai/cli/onboard).

## macOS app onboarding

Open the OpenClaw app. The first-run wizard walks you through the same steps with a visual interface. The full reference is [Onboarding (macOS App)](https://docs.openclaw.ai/start/onboarding).

## Custom or unlisted providers

If your provider is not listed in onboarding, choose **Custom Provider** and enter:

- API compatibility mode (OpenAI-compatible, Anthropic-compatible, or auto-detect)
- Base URL and API key
- Model ID and optional alias

Multiple custom endpoints can coexist — each gets its own endpoint ID.

**Source**: OpenClaw documentation — `start/onboarding-overview` (mirror `inbox/openclaw_docs/start/onboarding-overview.md`)
**Last Updated**: 2026-06-22
**Status**: Active
