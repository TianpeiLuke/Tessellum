---
tags:
  - resource
  - documentation
  - hermes_agent
  - integrations
  - navigation
keywords:
  - hermes integrations
  - ai providers and routing
  - tool servers mcp
  - web search backends
  - voice and tts
  - messaging platforms
  - external system connections
topics:
  - Hermes Agent
  - Integrations
language: markdown
date of note: 2026-06-19
status: active
building_block: navigation
source_url: https://hermes-agent.nousresearch.com/docs/integrations/
access_control_group: ["general"]
---

# Hermes Agent — Integrations Overview

## Overview

The Integrations Overview is the **router page** for every external system Hermes Agent connects to — AI inference, tool servers, IDE workflows, programmatic access, and more. Each section is a short directory entry that names the integration class and links out to the page that actually teaches setup and usage, so this note is a navigation index, not a feature deep-dive. The source page opens with a single recommendation: if you only set up one integration, set up [Nous Portal](hermes_nous_portal_subscription.md) — one OAuth login covers 300+ models plus the four Tool Gateway tools (web search, image generation, TTS, browser automation). The integration classes span inference/routing, MCP tool servers, web-search backends, browser automation, voice/TTS, IDE (ACP), the API server, memory/personalization, 27+ messaging platforms, home automation, plugins, and batch training/evaluation.

## AI Providers & Routing

Hermes supports multiple AI inference providers out of the box; configure interactively with `hermes model` or set them in `config.yaml`. The page indexes three sub-classes:

- **AI Providers** — OpenRouter, Anthropic, OpenAI, Google, and any OpenAI-compatible endpoint, with per-provider auto-detection of vision, streaming, and tool use. (Owned by [hermes_inference_providers_cloud](hermes_inference_providers_cloud.md) + [hermes_local_self_hosted_llm](hermes_local_self_hosted_llm.md).)
- **Provider Routing** — fine-grained control over which underlying providers handle OpenRouter requests, optimizing for cost/speed/quality via sorting, allowlists, denylists, and explicit priority ordering. (Routing/proxy layer → [hermes_provider_routing_proxies](hermes_provider_routing_proxies.md); feature internals → SP09.)
- **Fallback Providers** — automatic failover to backup LLM providers on errors, including primary-model fallback and independent auxiliary-task fallback for vision, compression, and web extraction. (→ [hermes_provider_routing_proxies](hermes_provider_routing_proxies.md).)

## Tool Servers (MCP)

- **MCP Servers** — connect Hermes to external tool servers via the Model Context Protocol, accessing tools from GitHub, databases, file systems, browser stacks, internal APIs, and more without writing native Hermes tools. The source notes support for both stdio and SSE transports, per-server tool filtering, and capability-aware resource/prompt registration. (MCP feature → SP09.)

## Web Search Backends

The `web_search` and `web_extract` tools support eight backend providers, configured via `config.yaml` or `hermes tools`. The source's backend table covers Firecrawl (default), SearXNG, Brave (free tier), DuckDuckGo (ddgs), Tavily, Exa, Parallel, and xAI — each with its env var and search/extract/crawl capability flags. Quick setup mirrors the source:

```yaml
web:
  backend: firecrawl    # firecrawl | searxng | brave-free | ddgs | tavily | exa | parallel | xai
```

If `web.backend` is not set, the backend is auto-detected from whichever API key is available; self-hosted Firecrawl is supported via `FIRECRAWL_API_URL`. (Web-search backends → SP08.)

## Browser Automation

Full browser automation with multiple backends for navigating sites, filling forms, and extracting information: **Browserbase** (managed cloud browsers with anti-bot tooling, CAPTCHA solving, residential proxies), **Browser Use** (alternative cloud browser provider), **Local Chromium-family CDP** (connect to a running Chrome/Brave/Chromium/Edge via `/browser connect`), and **Local Chromium** (headless local browser via the `agent-browser` CLI).

## Voice & TTS Providers

Text-to-speech and speech-to-text across all messaging platforms. The source's TTS table lists Edge TTS (default, free), ElevenLabs (paid), OpenAI TTS (paid), MiniMax (paid), xAI TTS (paid), and NeuTTS (free). Speech-to-text supports six providers: local faster-whisper (free, on-device), a local command wrapper, Groq, OpenAI Whisper API, Mistral, and xAI. Voice-message transcription works across Telegram, Discord, WhatsApp, and other platforms.

## IDE & Editor Integration

- **IDE Integration (ACP)** — use Hermes inside ACP-compatible editors such as VS Code, Zed, and JetBrains. Hermes runs as an ACP server, rendering chat messages, tool activity, file diffs, and terminal commands inside the editor. (ACP feature → SP09/18.)

## Programmatic Access

- **API Server** — expose Hermes as an OpenAI-compatible HTTP endpoint, so any frontend that speaks the OpenAI format (Open WebUI, LobeChat, LibreChat, NextChat, ChatBox) can connect and use Hermes as a backend with its full toolset. (API-server feature → SP09.)

## Memory & Personalization

- **Built-in Memory** — persistent, curated memory via `MEMORY.md` and `USER.md` files; the agent maintains bounded stores of personal notes and user-profile data that survive across sessions.
- **Memory Providers** — plug in external memory backends; eight are supported: Honcho (dialectic reasoning), OpenViking (tiered retrieval), Mem0 (cloud extraction), Hindsight (knowledge graphs), Holographic (local SQLite), RetainDB (hybrid search), ByteRover (CLI-based), and Supermemory. (Memory providers → SP05.)

## Messaging Platforms

Hermes runs as a gateway bot on 27+ messaging platforms, all configured through the same `gateway` subsystem — Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, Email, SMS, DingTalk, Feishu/Lark, WeCom (+ Callback), Weixin, BlueBubbles, QQ Bot, Yuanbao, Home Assistant, Microsoft Teams (+ Meetings + Graph Webhook), Google Chat, LINE, ntfy, SimpleX, Open WebUI, and Webhooks. The source points to the Messaging Gateway overview for the platform comparison table and setup guide. (Messaging platforms → SP11-13.)

## Home Automation

- **Home Assistant** — control smart-home devices via four dedicated tools (`ha_list_entities`, `ha_get_state`, `ha_list_services`, `ha_call_service`). The Home Assistant toolset activates automatically when `HASS_TOKEN` is configured.

## Plugins

- **Plugin System** — extend Hermes with custom tools, lifecycle hooks, and CLI commands without modifying core code; plugins are discovered from `~/.hermes/plugins/`, project-local `.hermes/plugins/`, and pip-installed entry points.
- **Build a Plugin** — a step-by-step guide for creating Hermes plugins with tools, hooks, and CLI commands.

## Training & Evaluation

- **Batch Processing** — run the agent across hundreds of prompts in parallel, generating structured ShareGPT-format trajectory data for training-data generation or evaluation.

**Source**: `inbox/hermes_agent_docs/integrations/index.md` · https://hermes-agent.nousresearch.com/docs/integrations/
**Last Updated**: 2026-06-19
**Status**: Active
