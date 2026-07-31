---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - features
keywords:
  - openclaw features
  - openclaw capability surface
  - built-in channels bundled plugin channels
  - embedded agent runtime multi-agent routing
  - 35+ model providers subscription auth
  - media in out generation
  - apps and interfaces mobile nodes
  - tools and automation web search cron lobster
topics:
  - OpenClaw
  - Features
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/features
access_control_group: ["general"]
---

# OpenClaw — Capability Surface (Features)

## Overview

This note captures the OpenClaw **capability surface** — the one-page "what OpenClaw supports" index from the `concepts/features` source page. It is a breadth-first enumeration (not a how-to) of the six capability clusters OpenClaw exposes from a single Gateway: chat **Channels**, the embedded **Agent** runtime, **Auth and providers**, **Media** in/out and generation, **Apps and interfaces** (including mobile nodes), and **Tools and automation**. The page is organized as a `Highlights` card grid, a fully enumerated `Full list`, and a `Related` card group that points onward to the experimental-features, agent-runtime, channels, and plugins docs. Every capability listed here is detailed in a dedicated doc elsewhere in the OpenClaw docs (and in this `oc_*` series); this note is the at-a-glance entry into that detail.

## Highlights

The source page opens with a card grid summarizing six headline capabilities:

- **Channels** — Discord, iMessage, Signal, Slack, Telegram, WhatsApp, WebChat, "and more with a single Gateway."
- **Plugins** — bundled plugins add Matrix, Nextcloud Talk, Nostr, Twitch, Zalo, "and more without separate installs in normal current releases."
- **Routing** — multi-agent routing with isolated sessions.
- **Media** — images, audio, video, documents, and image/video generation.
- **Apps and UI** — Windows Hub, Web Control UI, macOS app, and mobile nodes.
- **Mobile nodes** — iOS and Android nodes with pairing, voice/chat, and rich device commands.

## Full list

The full enumeration groups every supported capability under six headings.

### Channels

- Built-in channels include Discord, Google Chat, iMessage, IRC, Signal, Slack, Telegram, WebChat, and WhatsApp.
- Bundled plugin channels include Feishu, LINE, Matrix, Mattermost, Microsoft Teams, Nextcloud Talk, Nostr, QQ Bot, Synology Chat, Tlon, Twitch, Zalo, and Zalo Personal.
- Optional separately installed channel plugins include Voice Call and third-party packages such as WeChat.
- Third-party channel plugins can extend the Gateway further, such as WeChat.
- Group chat support with mention-based activation.
- DM safety with allowlists and pairing.

### Agent

- Embedded agent runtime with tool streaming.
- Multi-agent routing with isolated sessions per workspace or sender.
- Sessions: direct chats collapse into shared `main`; groups are isolated.
- Streaming and chunking for long responses.

### Auth and providers

- 35+ model providers (Anthropic, OpenAI, Google, and more).
- Subscription auth via OAuth (e.g. OpenAI Codex).
- Custom and self-hosted provider support (vLLM, SGLang, Ollama, and any OpenAI-compatible or Anthropic-compatible endpoint).

### Media

- Images, audio, video, and documents in and out.
- Shared image generation and video generation capability surfaces.
- Voice note transcription.
- Text-to-speech with multiple providers.

### Apps and interfaces

- WebChat and browser Control UI.
- macOS menu bar companion app.
- iOS node with pairing, Canvas, camera, screen recording, location, and voice.
- Android node with pairing, chat, voice, Canvas, camera, and device commands.

### Tools and automation

- Browser automation, exec, sandboxing.
- Web search (Brave, DuckDuckGo, Exa, Firecrawl, Gemini, Grok, Kimi, MiniMax Search, Ollama Web Search, Perplexity, SearXNG, Tavily).
- Cron jobs and heartbeat scheduling.
- Skills, plugins, and workflow pipelines (Lobster).

**Source**: OpenClaw documentation — `concepts/features` (mirror `inbox/openclaw_docs/concepts/features.md`)
**Last Updated**: 2026-06-22
**Status**: Active
