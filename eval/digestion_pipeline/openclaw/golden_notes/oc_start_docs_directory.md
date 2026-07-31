---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - docs_directory
keywords:
  - openclaw docs directory
  - curated docs index
  - start here cluster
  - providers and ux
  - companion apps
  - operations and safety
  - docs hubs vs directory
  - openclaw navigation index
topics:
  - OpenClaw
  - Docs Directory
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/start/docs-directory
access_control_group: ["general"]
---

# OpenClaw — Docs Directory (Curated Index)

## Overview

This note covers the OpenClaw **docs directory** — a curated, quick-access index that groups the most-used OpenClaw documentation pages into four clusters: **Start here**, **Providers and UX**, **Companion apps**, and **Operations and safety**, plus a **Related** pointer back to the quickstart and the full docs map. It mirrors the `start/docs-directory` source page, which is explicitly a *curated index* rather than an exhaustive map: the page's own `<Note>` tells new readers to begin with [Getting Started](https://docs.openclaw.ai/start/getting-started) and to consult [Docs hubs](https://docs.openclaw.ai/start/hubs) for the complete page map. This note captures the curated grouping and when to use the directory versus the full hubs map; the downstream targets are deferred to their home docs (gateway, concepts, channels, tools, install, platforms, web, automation, reference).

## When to Use the Docs Directory

The docs directory is the **shortlist** of high-traffic pages — a fast on-ramp once you already know roughly what you are looking for. The source page frames its role with two pointers in a leading `<Note>`: if you are new, start with **Getting Started** (the install → onboard → verify → first-message quickstart); for a *complete* map of every page (including deep dives not on the left nav), use the **Docs hubs** page. So the directory is the curated middle ground — broader than the quickstart, narrower and more opinionated than the hubs map.

## Start here

The most-used entry pages and core operational references. The source page lists, in order:

- **Docs hubs (all pages linked)** — `/start/hubs`, the complete map.
- **Help** — `/help`.
- **Configuration** — `/gateway/configuration`.
- **Configuration examples** — `/gateway/configuration-examples`.
- **Slash commands** — `/tools/slash-commands`.
- **Multi-agent routing** — `/concepts/multi-agent`.
- **Updating and rollback** — `/install/updating`.
- **Pairing (DM and nodes)** — `/channels/pairing`.
- **Nix mode** — `/install/nix`.
- **OpenClaw assistant setup** — `/start/openclaw`.
- **Skills** — `/tools/skills`.
- **Skills config** — `/tools/skills-config`.
- **Workspace templates** — `/reference/templates/AGENTS`.
- **RPC adapters** — `/reference/rpc`.
- **Gateway runbook** — `/gateway`.
- **Nodes (iOS and Android)** — `/nodes`.
- **Web surfaces (Control UI)** — `/web`.
- **Discovery and transports** — `/gateway/discovery`.
- **Remote access** — `/gateway/remote`.

## Providers and UX

The user-facing surfaces and messaging channels. The source page lists: **WebChat** (`/web/webchat`), **Control UI (browser)** (`/web/control-ui`), **Telegram** (`/channels/telegram`), **Discord** (`/channels/discord`), **Mattermost** (`/channels/mattermost`), **QQ Bot** (`/channels/qqbot`), **iMessage** (`/channels/imessage`), **Groups** (`/channels/groups`), **WhatsApp group messages** (`/channels/group-messages`), **Media images** (`/nodes/images`), and **Media audio** (`/nodes/audio`).

## Companion apps

The native client apps across platforms. The source page lists exactly five: **macOS app** (`/platforms/macos`), **iOS app** (`/platforms/ios`), **Android app** (`/platforms/android`), **Windows Hub** (`/platforms/windows`), and **Linux app** (`/platforms/linux`).

## Operations and safety

The runbook, scheduling, and security pages for operating a gateway. The source page lists: **Sessions** (`/concepts/session`), **Cron jobs** (`/automation/cron-jobs`), **Webhooks** (`/automation/cron-jobs#webhooks`), **Gmail hooks (Pub/Sub)** (`/automation/cron-jobs#gmail-pubsub-integration`), **Security** (`/gateway/security`), and **Troubleshooting** (`/gateway/troubleshooting`). Note that Webhooks and Gmail Pub/Sub are anchored sub-sections of the single Cron jobs page rather than standalone pages.

**Source**: OpenClaw documentation — `start/docs-directory` (mirror `inbox/openclaw_docs/start/docs-directory.md`)
**Last Updated**: 2026-06-22
**Status**: Active
