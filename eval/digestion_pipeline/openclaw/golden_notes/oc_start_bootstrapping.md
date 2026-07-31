---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - bootstrapping
keywords:
  - openclaw bootstrapping
  - first-run ritual
  - agent workspace seeding
  - agents.md identity.md user.md soul.md
  - bootstrap.md removed after first run
  - openclaw onboard --skip-bootstrap
  - gateway host workspace
  - embedded local model bootstrap
topics:
  - OpenClaw
  - Bootstrapping
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/start/bootstrapping
access_control_group: ["general"]
---

# OpenClaw — Agent Bootstrapping (First-Run Ritual)

## Overview

This note explains OpenClaw **bootstrapping**: the first-run ritual that prepares an agent workspace and collects identity details. It happens after onboarding, when the agent starts for the first time. Mirroring the `start/bootstrapping` source page, it covers what bootstrapping does (seeding the workspace files, the one-question-at-a-time Q&A, writing identity and preferences, and removing `BOOTSTRAP.md` so it runs once), the special handling for embedded/local-model runs, how to skip it for a pre-seeded workspace, and the fact that it always runs on the gateway host.

## What bootstrapping does

On the first agent run, OpenClaw bootstraps the workspace (default `~/.openclaw/workspace`):

- Seeds `AGENTS.md`, `BOOTSTRAP.md`, `IDENTITY.md`, `USER.md`.
- Runs a short Q&A ritual (one question at a time).
- Writes identity + preferences to `IDENTITY.md`, `USER.md`, `SOUL.md`.
- Removes `BOOTSTRAP.md` when finished so it only runs once.

For embedded/local model runs, OpenClaw keeps `BOOTSTRAP.md` out of the privileged system context. On the primary interactive first run, it still passes the file contents in the user prompt so models that do not reliably call the `read` tool can complete the ritual. If the current run cannot safely access the workspace, the agent gets a limited bootstrap note instead of a generic greeting.

## Skipping bootstrapping

To skip this for a pre-seeded workspace, run `openclaw onboard --skip-bootstrap`.

## Where it runs

Bootstrapping always runs on the **gateway host**. If the macOS app connects to a remote Gateway, the workspace and bootstrapping files live on that remote machine. When the Gateway runs on another machine, edit workspace files on the gateway host (for example, `user@gateway-host:~/.openclaw/workspace`).

**Source**: OpenClaw documentation — `start/bootstrapping` (mirror `inbox/openclaw_docs/start/bootstrapping.md`)
**Last Updated**: 2026-06-22
**Status**: Active
