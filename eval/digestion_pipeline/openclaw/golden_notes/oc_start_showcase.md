---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - showcase
keywords:
  - openclaw showcase
  - community projects gallery
  - chat-native builds
  - browser automation no api
  - build a skill in minutes
  - voice phone bridge
  - home hardware automation
  - openclaw real-world reach
topics:
  - OpenClaw
  - Showcase
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/start/showcase
access_control_group: ["general"]
---

# OpenClaw — Showcase: The Community-Evidence Case for OpenClaw's Real-World Reach

## Overview

This note digests the OpenClaw **Showcase** page (`start/showcase`) as an argument: the claim is that OpenClaw is not a toy demo but a platform on which people ship real PR-review loops, mobile apps, home automation, voice systems, devtools, and memory-heavy workflows from the channels they already use. The page supports that claim with a curated gallery of community-built projects, grouped into eight themed clusters — Fresh from Discord, Automation and workflows, Knowledge and memory, Voice and phone, Infrastructure and deployment, Home and hardware, Community projects, and a Submit-your-project call to action. This note mirrors all eight clusters, treats the gallery as the evidence base, and draws out the three recurring through-lines the source itself foregrounds: chat-native builds (Telegram / WhatsApp / Discord / terminals), real automation "without waiting for an API" (browser control), and physical-world integrations (printers, vacuums, cameras, home systems).

## The Claim and Its Through-Lines

The source opens with the thesis verbatim: "OpenClaw projects are not toy demos." The supporting evidence is framed around three properties the page repeats across clusters: builds happen **chat-native** "from the channels they already use — chat-native builds on Telegram, WhatsApp, Discord, and terminals"; automation runs "without waiting for an API" via browser control ("No APIs, just browser control"); and the agent reaches into the **physical world** with "printers, vacuums, cameras, and home systems." A fourth implicit through-line, visible across the gallery, is "build a skill in minutes" — multiple projects describe asking the agent to generate a new skill on the fly. Each cluster below reproduces the source's own one-line framing plus its project entries (author handle and tags as given), so the evidence is faithful to what the page actually lists rather than paraphrased into generic capabilities.

## Fresh from Discord

Framing (source): "Recent standouts across coding, devtools, mobile, and chat-native product building." Entries:

- **PR Review to Telegram Feedback** (@bangnokia · `review` `github` `telegram`) — OpenCode finishes the change, opens a PR, OpenClaw reviews the diff and replies in Telegram with suggestions plus a clear merge verdict.
- **Wine Cellar Skill in Minutes** (@prades_maxime · `skills` `local` `csv`) — asked "Robby" (@openclaw) for a local wine cellar skill; it requests a sample CSV export and a store path, then builds and tests the skill (962 bottles in the example).
- **Tesco Shop Autopilot** (@marchattonhere · `automation` `browser` `shopping`) — weekly meal plan, regulars, book delivery slot, confirm order. "No APIs, just browser control."
- **SNAG screenshot-to-Markdown** (@am-will · `devtools` `screenshots` `markdown`) — hotkey a screen region, Gemini vision, instant Markdown in your clipboard.
- **Agents UI** (@kitze · `ui` `skills` `sync`) — desktop app to manage skills and commands across Agents, Claude, Codex, and OpenClaw.
- **Telegram voice notes (papla.media)** (Community · `voice` `tts` `telegram`) — wraps papla.media TTS and sends results as Telegram voice notes (no annoying autoplay).
- **CodexMonitor** (@odrobnik · `devtools` `codex` `brew`) — Homebrew-installed helper to list, inspect, and watch local OpenAI Codex sessions (CLI + VS Code).
- **Bambu 3D Printer Control** (@tobiasbischoff · `hardware` `3d-printing` `skill`) — control and troubleshoot BambuLab printers: status, jobs, camera, AMS, calibration, and more.
- **Vienna transport (Wiener Linien)** (@hjanuschka · `travel` `transport` `skill`) — real-time departures, disruptions, elevator status, and routing for Vienna's public transport.
- **ParentPay school meals** (@George5562 · `automation` `browser` `parenting`) — automated UK school meal booking via ParentPay; uses mouse coordinates for reliable table cell clicking.
- **R2 upload (Send Me My Files)** (@julianengel · `files` `r2` `presigned-urls`) — upload to Cloudflare R2/S3 and generate secure presigned download links; useful for remote OpenClaw instances.
- **iOS app via Telegram** (@coard · `ios` `xcode` `testflight`) — built a complete iOS app with maps and voice recording, deployed to TestFlight entirely via Telegram chat.
- **Oura Ring health assistant** (@AS · `health` `oura` `calendar`) — personal AI health assistant integrating Oura ring data with calendar, appointments, and gym schedule.
- **Kev's Dream Team (14+ agents)** (@adam91holt · `multi-agent` `orchestration`) — 14+ agents under one gateway with an Opus 4.5 orchestrator delegating to Codex workers; see the technical write-up and Clawdspace for agent sandboxing.
- **Linear CLI** (@NessZerra · `devtools` `linear` `cli`) — CLI for Linear that integrates with agentic workflows (Claude Code, OpenClaw); manage issues, projects, and workflows from the terminal.
- **Beeper CLI** (@jules · `messaging` `beeper` `cli`) — read, send, and archive messages via Beeper Desktop; uses the Beeper local MCP API so agents can manage all your chats (iMessage, WhatsApp, and more) in one place.

## Automation and Workflows

Framing (source): "Scheduling, browser control, support loops, and the 'just do the task for me' side of the product." Entries:

- **Winix air purifier control** (@antonplex · `automation` `hardware` `air-quality`) — Claude Code discovered and confirmed the purifier controls, then OpenClaw takes over to manage room air quality.
- **Pretty sky camera shots** (@signalgaining · `automation` `camera` `skill`) — triggered by a roof camera; ask OpenClaw to snap a sky photo whenever it looks pretty. It designed a skill and took the shot.
- **Visual morning briefing scene** (@buddyhadry · `automation` `briefing` `telegram`) — a scheduled prompt generates one scene image each morning (weather, tasks, date, favorite post or quote) via an OpenClaw persona.
- **Padel court booking** (@joshp123 · `automation` `booking` `cli`) — Playtomic availability checker plus booking CLI.
- **Accounting intake** (Community · `automation` `email` `pdf`) — collects PDFs from email, preps documents for a tax consultant; monthly accounting on autopilot.
- **Couch potato dev mode** (@davekiss · `telegram` `migration` `astro`) — rebuilt an entire personal site via Telegram (Notion to Astro, 18 posts migrated, DNS to Cloudflare) without opening a laptop.
- **Job search agent** (@attol8 · `automation` `api` `skill`) — searches job listings, matches against CV keywords, returns relevant opportunities with links; built in 30 minutes using the JSearch API.
- **Jira skill builder** (@jdrhyne · `jira` `skill` `devtools`) — OpenClaw connected to Jira, then generated a new skill on the fly (before it existed on ClawHub).
- **Todoist skill via Telegram** (@iamsubhrajyoti · `todoist` `skill` `telegram`) — automated Todoist tasks and had OpenClaw generate the skill directly in Telegram chat.
- **TradingView analysis** (@bheem1798 · `finance` `browser` `automation`) — logs into TradingView via browser automation, screenshots charts, performs technical analysis on demand. "No API needed — just browser control."
- **Slack auto-support** (@henrymascot · `slack` `automation` `support`) — watches a company Slack channel, responds helpfully, forwards notifications to Telegram; autonomously fixed a production bug in a deployed app without being asked.

## Knowledge and Memory

Framing (source): "Systems that index, search, remember, and reason over personal or team knowledge." Entries:

- **xuezh Chinese learning** (@joshp123 · `learning` `voice` `skill`) — Chinese learning engine with pronunciation feedback and study flows via OpenClaw.
- **WhatsApp memory vault** (Community · `memory` `transcription` `indexing`) — ingests full WhatsApp exports, transcribes 1k+ voice notes, cross-checks with git logs, outputs linked markdown reports.
- **Karakeep semantic search** (@jamesbrooksco · `search` `vector` `bookmarks`) — adds vector search to Karakeep bookmarks using Qdrant plus OpenAI or Ollama embeddings.
- **Inside-Out-2 memory** (Community · `memory` `beliefs` `self-model`) — a separate memory manager that turns session files into memories, then beliefs, then an evolving self model.

## Voice and Phone

Framing (source): "Speech-first entry points, phone bridges, and transcription-heavy workflows." Entries:

- **Clawdia phone bridge** (@alejandroOPI · `voice` `vapi` `bridge`) — a Vapi voice assistant to OpenClaw HTTP bridge; near real-time phone calls with your agent.
- **OpenRouter transcription** (@obviyus · `transcription` `multilingual` `skill`) — multi-lingual audio transcription via OpenRouter (Gemini, and more); available on ClawHub.

## Infrastructure and Deployment

Framing (source): "Packaging, deployment, and integrations that make OpenClaw easier to run and extend." Entries:

- **Home Assistant add-on** (@ngutman · `homeassistant` `docker` `raspberry-pi`) — OpenClaw gateway running on Home Assistant OS with SSH tunnel support and persistent state.
- **Home Assistant skill** (ClawHub · `homeassistant` `skill` `automation`) — control and automate Home Assistant devices via natural language.
- **Nix packaging** (@openclaw · `nix` `packaging` `deployment`) — a batteries-included nixified OpenClaw configuration for reproducible deployments.
- **CalDAV calendar** (ClawHub · `calendar` `caldav` `skill`) — a calendar skill using khal and vdirsyncer for self-hosted calendar integration.

## Home and Hardware

Framing (source): "The physical-world side of OpenClaw: homes, sensors, cameras, vacuums, and other devices." Entries:

- **GoHome automation** (@joshp123 · `home` `nix` `grafana`) — Nix-native home automation with OpenClaw as the interface, plus Grafana dashboards.
- **Roborock vacuum** (@joshp123 · `vacuum` `iot` `plugin`) — control your Roborock robot vacuum through natural conversation.

## Community Projects

Framing (source): "Things that grew beyond a single workflow into broader products or ecosystems." Entry:

- **StarSwap marketplace** (Community · `marketplace` `astronomy` `webapp`) — a full astronomy gear marketplace, built with and around the OpenClaw ecosystem.

## Submit Your Project

The page closes with a three-step submission flow (rendered as an MDX `<Steps>` block) inviting contributions to the gallery: (1) **Share it** — post in #self-promotion on the OpenClaw Discord or tweet @openclaw on X; (2) **Include details** — say what it does, link the repo or demo, and add a screenshot if you have one; (3) **Get featured** — standout projects are added to this page. An `<Info>` callout at the top of the page repeats the same "Want to be featured?" prompt with the Discord and X links. This self-submission loop is itself part of the argument: the showcase is a living, community-sourced corpus, which is why the page warns it reflects "recent standouts" rather than a static, exhaustive list.

**Source**: OpenClaw documentation — `start/showcase` (mirror `inbox/openclaw_docs/start/showcase.md`)
**Last Updated**: 2026-06-22
**Status**: Active
