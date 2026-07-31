---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - navigation
keywords:
  - openclaw docs hubs
  - openclaw documentation map
  - docs hubs page
  - find any openclaw doc
  - deep dive docs not in left nav
  - openclaw topical clusters
  - core concepts gateway tools platforms
topics:
  - OpenClaw
  - Documentation Navigation
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/start/hubs
access_control_group: ["general"]
---

# OpenClaw — Docs Hubs (Complete Documentation Map)

## Overview

This note describes the OpenClaw **Docs hubs** page (`start/hubs`), the complete documentation map that links to every OpenClaw doc — including the deep dives and reference docs that do NOT appear in the left navigation. The page opens with a note steering new users to [Getting Started](https://docs.openclaw.ai/start/getting-started), then groups every page into thirteen topical clusters: Start here, Installation + updates, Core concepts, Providers + ingress, Gateway + operations, Tools + automation, Nodes/media/voice, Platforms, macOS companion app (advanced), Plugins, Workspace + templates, Project, and Testing + release. It is the canonical "find any doc" index, complementing the more selective curated [docs-directory](oc_start_docs_directory.md). This note mirrors the cluster structure and explains when to use each cluster, rather than re-dumping every link (downstream targets are deferred to their home sub-plans).

## What the Hubs Page Is For

The hubs page is the exhaustive discovery surface for the OpenClaw documentation. Its stated purpose: "Use these hubs to discover every page, including deep dives and reference docs that don't appear in the left nav." Where the left-nav and the curated docs-directory surface only the most-used pages, the hubs page enumerates the full corpus organized by topic. The leading `<Note>` block directs anyone new to OpenClaw to start with Getting Started rather than browsing the map. Most cluster links are site-relative paths (e.g. `/concepts/agent-loop`); a few are anchor links into a longer page (e.g. `/automation/cron-jobs#webhooks`, `/automation/cron-jobs#gmail-pubsub-integration`) or absolute local-host URLs (the Dashboard link is `http://127.0.0.1:18789/`, the local Gateway address).

## Cluster Map (13 Topical Groups)

The clusters below mirror the source page's H2 sections in order. Representative entries are listed; each entry links to a page whose detail lives in that topic's home sub-plan (deferred — not re-dumped here).

### Start here

The day-0 landing cluster: `Index` (`/`), `Getting Started`, `Onboarding`, `Onboarding (CLI)` (`/start/wizard`), `Setup`, `Dashboard (local Gateway)` (`http://127.0.0.1:18789/`), `Help`, `Docs directory`, `Configuration`, `Configuration examples`, `OpenClaw assistant` (`/start/openclaw`), `Showcase`, and `Lore`. This is the cluster a first-time reader uses; it includes the same getting-started/onboarding/lore pages captured as sibling `oc_start_*` notes in this series.

### Installation + updates

Install-method and upgrade docs: `Docker`, `Nix`, `Updating / rollback` (`/install/updating`), and the experimental `Bun workflow` (`/install/bun`). Use this cluster to pick an install path or to roll a deployment forward/back.

### Core concepts

The largest cluster — the conceptual model of OpenClaw: `Architecture`, `Features`, `Network hub` (`/network`), `Agent runtime` (`/concepts/agent`), `Agent workspace`, `Memory`, `Agent loop`, `Streaming + chunking`, `Multi-agent routing`, `Compaction`, `Sessions` (`/concepts/session`), `Session pruning`, `Session tools` (`/concepts/session-tool`), `Queue`, `Slash commands` (`/tools/slash-commands`), `RPC adapters` (`/reference/rpc`), `TypeBox schemas`, `Timezone handling`, `Presence`, `Discovery + transports` (`/gateway/discovery`), `Bonjour`, `Channel routing`, `Groups`, `Group messages`, `Model failover`, and `OAuth`. Use this cluster to understand how the gateway, agent runtime, sessions, and routing work.

### Providers + ingress

Inbound channels and model providers: `Chat channels hub` (`/channels`), `Model providers hub` (`/providers/models`), `WhatsApp`, `Telegram`, `Slack`, `Discord`, `Mattermost`, `Signal`, `QQ Bot` (`/channels/qqbot`), `iMessage`, `Location parsing` (`/channels/location`), `WebChat` (`/web/webchat`), `Webhooks` (`/automation/cron-jobs#webhooks`), and `Gmail Pub/Sub` (`/automation/cron-jobs#gmail-pubsub-integration`). Use this cluster to connect a messaging channel or pick a model backend.

### Gateway + operations

Running and operating the Gateway: `Gateway runbook` (`/gateway`), `Network model` (`/network#core-model`), `Gateway pairing`, `Gateway lock` (`/gateway/gateway-lock`), `Background process`, `Health`, `Heartbeat`, `Doctor`, `Logging`, `Sandboxing`, `Dashboard` (`/web/dashboard`), `Control UI` (`/web/control-ui`), `Remote access` (`/gateway/remote`), `Remote gateway README` (`/gateway/remote-gateway-readme`), `Tailscale`, `Security`, and `Troubleshooting`. Use this cluster to deploy, secure, monitor, and debug a running gateway.

### Tools + automation

The agent's tool surface and scheduled work: `Tools surface` (`/tools`), `OpenProse` (`/prose`), `CLI reference` (`/cli`), `Exec tool`, `PDF tool`, `Elevated mode` (`/tools/elevated`), `Cron jobs` (`/automation/cron-jobs`), `Automation`, `Thinking + verbose` (`/tools/thinking`), `Models` (`/concepts/models`), `Sub-agents` (`/tools/subagents`), `Agent send CLI` (`/tools/agent-send`), `Terminal UI` (`/web/tui`), `Browser control` (`/tools/browser`), `Browser (Linux troubleshooting)`, and `Polls` (`/cli/message`). Use this cluster to extend agent capabilities or schedule recurring work.

### Nodes, media, voice

Device nodes and rich-media features: `Nodes overview` (`/nodes`), `Camera`, `Images`, `Audio`, `Location command` (`/nodes/location-command`), `Voice wake` (`/nodes/voicewake`), and `Talk mode` (`/nodes/talk`). Use this cluster for camera/image/audio and voice-interaction features.

### Platforms

Per-platform install and behavior: `Platforms overview` (`/platforms`), `macOS`, `iOS`, `Android`, `Windows Hub` (`/platforms/windows`), `Linux`, and `Web surfaces` (`/web`). Use this cluster to find platform-specific guidance.

### macOS companion app (advanced)

Deep macOS-app internals: `macOS dev setup`, `macOS menu bar`, `macOS voice wake`, `macOS voice overlay`, `macOS WebChat`, `macOS Canvas`, `macOS child process`, `macOS health`, `macOS icon`, `macOS logging`, `macOS permissions`, `macOS remote`, `macOS signing`, `macOS gateway (launchd)` (`/platforms/mac/bundled-gateway`), `macOS XPC`, `macOS skills`, and `macOS Peekaboo`. Use this advanced cluster when building, signing, or deeply customizing the macOS companion app.

### Plugins

Extending OpenClaw via plugins: `Plugins overview` (`/tools/plugin`), `Building plugins` (`/plugins/building-plugins`), `Plugin hooks` (`/plugins/hooks`), `Plugin manifest`, `Agent tools` (`/plugins/building-plugins#registering-agent-tools`), `Plugin bundles` (`/plugins/bundles`), `ClawHub`, `Capability cookbook` (`/tools/capability-cookbook`), `Voice call plugin` (`/plugins/voice-call`), and `Zalo user plugin` (`/plugins/zalouser`). Use this cluster to author or install plugins.

### Workspace + templates

Skills and the workspace template files: `Skills` (`/tools/skills`), `ClawHub`, `Skills config` (`/tools/skills-config`), `Default AGENTS` (`/reference/AGENTS.default`), and the `/reference/templates/*` set — `Templates: AGENTS`, `Templates: BOOTSTRAP`, `Templates: HEARTBEAT`, `Templates: IDENTITY`, `Templates: SOUL`, `Templates: TOOLS`, and `Templates: USER`. Use this cluster for the workspace-file templates (the same AGENTS/BOOTSTRAP/IDENTITY/SOUL/USER files seeded at first-run bootstrapping) and skills configuration.

### Project

Project meta-docs: `Credits` (`/reference/credits`).

### Testing + release

Contributor/release docs: `Testing` (`/reference/test`), `Release policy` (`/reference/RELEASING`), and `Device models` (`/reference/device-models`). Use this cluster for testing guidance and release process.

## Hubs vs. Docs Directory

The hubs page and the curated `docs-directory` page serve complementary navigation roles. The hubs page is exhaustive — it links *every* page, including deep dives and reference docs absent from the left nav, organized into 13 topical clusters. The docs-directory is selective — it groups only the most-used pages into a few clusters (Start here, Providers and UX, Companion apps, Operations and safety). A reader hunting for any specific page (especially an advanced/deep-dive doc) uses the hubs map; a reader wanting a quick-access shortlist uses the docs-directory. The page's own `## Related` section closes by linking back to `Getting started`, reinforcing that new users should begin there rather than in the full map.

**Source**: OpenClaw documentation — `start/hubs` (mirror `inbox/openclaw_docs/start/hubs.md`)
**Last Updated**: 2026-06-22
**Status**: Active
