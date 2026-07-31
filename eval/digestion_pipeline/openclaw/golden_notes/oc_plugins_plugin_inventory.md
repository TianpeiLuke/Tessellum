---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - plugin_inventory
keywords:
  - openclaw plugin inventory
  - core npm package plugin
  - official external package
  - source checkout only
  - clawhub npm distribution
  - openclaw plugins install
  - plugins inventory gen
  - bundled vs installable plugin
topics:
  - OpenClaw
  - Plugin Inventory
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/plugin-inventory
access_control_group: ["general"]
---

# OpenClaw — The Generated Plugin Inventory and Distribution Tiers

## Overview

This note models the OpenClaw **plugin inventory**: the generated, canonical catalog of every OpenClaw plugin classified by how it is distributed — built into the core npm package, published as an official external package, or kept source-checkout-only. It mirrors the `plugins/plugin-inventory` source page, which is generated from `extensions/*/package.json`, `openclaw.plugin.json`, and the root npm package `files` exclusions, and regenerated with `pnpm plugins:inventory:gen`. The page covers three distribution-tier definitions, the install route that each catalog entry advertises, and the three flat catalogs (**72** core npm plugins, **54** official external packages, **3** source-checkout-only plugins). This is a declarative reference taxonomy, not a procedure — the install commands below are quoted as canonical facts of an entry's install route, with the full step-by-step install/update/uninstall flow living in the linked Manage-plugins and permission notes.

## How the Inventory Is Generated

The inventory page is **generated**, not hand-maintained: it is produced from each extension's `extensions/*/package.json`, its `openclaw.plugin.json` manifest, and the root npm package `files` exclusions (which decide whether a plugin's files are published in the core artifact or excluded from it). Regenerate it with one command:

```bash
pnpm plugins:inventory:gen
```

Each catalog entry records three facts: the **package** name (the npm scope `@openclaw/<id>`), the **distribution route** (the install source — `included in OpenClaw`, `npm`, and/or `ClawHub`), and a one-line **description** of the capability the plugin adds.

## Distribution-Tier Definitions

The inventory classifies every plugin into exactly one of three distribution tiers:

- **Core npm package** — built into the `openclaw` npm package and available without a separate plugin install.
- **Official external package** — an OpenClaw-maintained plugin omitted from the core npm package, kept in this official inventory, and installed on demand through ClawHub and/or npm.
- **Source checkout only** — a repo-local plugin omitted from published npm artifacts and not advertised as an installable package.

A key distinction: a **source checkout is different from an npm install**. After `pnpm install`, bundled plugins load from `extensions/<id>`, so local edits and package-local workspace dependencies are available — i.e. running from the repo source picks up the in-tree plugin code directly rather than the published package.

## Install Route per Entry

Each entry's distribution route is what decides whether an install is needed. Plugins whose route says `included in OpenClaw` are already present in the core package and need no install. **Official external packages need one install, then a Gateway restart.** The canonical install flow (using Discord, an official external package, as the worked example) is:

```bash
openclaw plugins install @openclaw/discord
openclaw gateway restart
openclaw plugins inspect discord --runtime --json
```

During the launch cutover, ordinary bare package specs still install from npm. Use `clawhub:@openclaw/discord` or `npm:@openclaw/discord` when you need an explicit source. After install, follow the plugin's setup doc (such as the Discord channel doc) to add credentials and channel config; `Manage plugins` covers update, uninstall, and publishing commands.

## Core npm Package (72 plugins)

Plugins built into the `openclaw` npm package — available without a separate install (route `included in OpenClaw`). This tier is dominated by **model providers** (e.g. `@openclaw/anthropic-provider`, `@openclaw/openai-provider`, `@openclaw/google-plugin`, `@openclaw/openrouter-provider`, `@openclaw/ollama-provider`, `@openclaw/litellm-provider`, `@openclaw/mistral-provider`, `@openclaw/copilot-proxy`, `@openclaw/vllm-provider`, `@openclaw/together-provider`), plus bundled **channels** (`@openclaw/telegram`, `@openclaw/signal`, `@openclaw/imessage`, `@openclaw/irc`, `@openclaw/mattermost`, `@openclaw/sms`, `@openclaw/clickclack`), **memory** (`@openclaw/memory-core`, `@openclaw/memory-wiki`), **media/speech** (`@openclaw/azure-speech`, `@openclaw/elevenlabs-speech`, `@openclaw/deepgram-provider`, `@openclaw/microsoft-speech`, `@openclaw/tts-local-cli`), **web search/fetch** (`@openclaw/duckduckgo-plugin`, `@openclaw/searxng-plugin`, `@openclaw/tavily-plugin`, `@openclaw/web-readability-plugin`), and core tools/utilities. Representative non-provider entries:

- **admin-http-rpc** (`@openclaw/admin-http-rpc`) — OpenClaw admin HTTP RPC endpoint.
- **browser** (`@openclaw/browser-plugin`) — adds agent-callable tools.
- **canvas** (`@openclaw/canvas-plugin`) — experimental Canvas control and A2UI rendering surfaces for paired nodes.
- **codex-supervisor** (`@openclaw/codex-supervisor`) — supervise Codex app-server sessions from OpenClaw.
- **document-extract** (`@openclaw/document-extract-plugin`) — extract text and fallback page images from local document attachments.
- **file-transfer** (`@openclaw/file-transfer`) — fetch, list, and write files on paired nodes via dedicated node commands; bypasses bash stdout truncation by using base64 over `node.invoke` for binaries up to 16 MB.
- **memory-wiki** (`@openclaw/memory-wiki`) — persistent wiki compiler and Obsidian-friendly knowledge vault for OpenClaw.
- **oc-path** (`@openclaw/oc-path`) — adds the `openclaw path` CLI for `oc://` workspace file addressing.
- **migrate-claude** (`@openclaw/migrate-claude`) — imports Claude Code and Claude Desktop instructions, MCP servers, skills, and safe configuration into OpenClaw.
- **migrate-hermes** (`@openclaw/migrate-hermes`) — imports Hermes configuration, memories, skills, and supported credentials into OpenClaw.
- **policy** (`@openclaw/policy`) — adds policy-backed doctor checks for workspace conformance.
- **voyage** (`@openclaw/voyage-provider`) — adds memory embedding provider support.
- **webhooks** (`@openclaw/webhooks`) — authenticated inbound webhooks that bind external automation to OpenClaw TaskFlows.
- **workboard** (`@openclaw/workboard`) — dashboard workboard for agent-owned issues and sessions.

A handful of core entries also advertise external routes: `@openclaw/cohere-provider` lists `included in OpenClaw; npm; ClawHub: clawhub:@openclaw/cohere-provider`, indicating it is both bundled and separately installable.

## Official External Packages (54 plugins)

OpenClaw-maintained plugins omitted from the core npm package and installed on demand via `npm` and/or `ClawHub`. Most entries carry the route `npm; ClawHub` (some list an explicit ClawHub spec such as `clawhub:@openclaw/<id>`; a few list ClawHub first, e.g. `matrix` and `whatsapp` show `ClawHub: clawhub:@openclaw/...; npm`). This tier is heavy on **channels** and **harness/runtime/provider** plugins. Representative entries:

- **acpx** (`@openclaw/acpx`) — OpenClaw ACP runtime backend with plugin-owned session and transport management.
- **amazon-bedrock** (`@openclaw/amazon-bedrock-provider`) — OpenClaw Amazon Bedrock provider plugin with model discovery, embeddings, and guardrail support.
- **amazon-bedrock-mantle** (`@openclaw/amazon-bedrock-mantle-provider`) — Amazon Bedrock Mantle provider plugin for OpenAI-compatible model routing.
- **anthropic-vertex** (`@openclaw/anthropic-vertex-provider`) — Anthropic Vertex provider plugin for Claude models on Google Vertex AI.
- **codex** (`@openclaw/codex`) — OpenClaw Codex app-server harness and model provider plugin with a Codex-managed GPT catalog.
- **copilot** (`@openclaw/copilot`) — registers the GitHub Copilot agent runtime.
- **diagnostics-otel** (`@openclaw/diagnostics-otel`) — diagnostics OpenTelemetry exporter for metrics, traces, and logs.
- **diagnostics-prometheus** (`@openclaw/diagnostics-prometheus`) — diagnostics Prometheus exporter for runtime metrics.
- **diffs** (`@openclaw/diffs`) — read-only diff viewer plugin and file renderer for agents (with companion `@openclaw/diffs-language-pack`).
- **discord** (`@openclaw/discord`) — Discord channel plugin for channels, DMs, commands, and app events.
- **feishu** (`@openclaw/feishu`) — Feishu/Lark channel plugin (community maintained by @m1heng).
- **google-meet** (`@openclaw/google-meet`) — Google Meet participant plugin for joining calls through Chrome or Twilio transports.
- **llama-cpp** (`@openclaw/llama-cpp-provider`) — local GGUF embeddings through node-llama-cpp.
- **lobster** (`@openclaw/lobster`) — Lobster workflow tool plugin for typed pipelines and resumable approvals.
- **memory-lancedb** (`@openclaw/memory-lancedb`) — LanceDB-backed long-term memory plugin with auto-recall, auto-capture, and vector search.
- **msteams** (`@openclaw/msteams`) — Microsoft Teams channel plugin for bot conversations.
- **openshell** (`@openclaw/openshell-sandbox`) — sandbox backend for the NVIDIA OpenShell CLI with mirrored local workspaces and SSH command execution.
- **slack** (`@openclaw/slack`) — Slack channel plugin for channels, DMs, commands, and app events.
- **tokenjuice** (`@openclaw/tokenjuice`) — compacts exec and bash tool results with tokenjuice reducers.
- **voice-call** (`@openclaw/voice-call`) — voice-call plugin for Twilio, Telnyx, and Plivo phone calls.

Additional external channels include `whatsapp`, `matrix`, `line`, `nostr`, `googlechat`, `synology-chat`, `nextcloud-talk`, `tlon`, `twitch`, `qqbot`, `zalo`, and `zalouser`; additional external providers/search include `deepseek`, `groq`, `cerebras`, `qwen`, `kimi`, `deepinfra`, `cloudflare-ai-gateway-provider`, `gmi`, `arcee`, `chutes`, `kilocode`, `stepfun`, `qianfan`, `brave`, `exa`, `perplexity`, `firecrawl`, `parallel`, `pixverse`, `gradium`, and `inworld`. (One external entry, `parallel`, links to `/tools/parallel-search` rather than the `/plugins/reference/` path used by the others.)

## Source Checkout Only (3 plugins)

Repo-local plugins omitted from published npm artifacts and not advertised as installable packages — all QA-internal:

- **qa-channel** (`@openclaw/qa-channel`) — adds the QA Channel surface for sending and receiving OpenClaw messages.
- **qa-lab** (`@openclaw/qa-lab`) — OpenClaw QA lab plugin with private debugger UI and scenario runner.
- **qa-matrix** (`@openclaw/qa-matrix`) — Matrix QA transport runner and substrate.

**Source**: OpenClaw documentation — `plugins/plugin-inventory` (mirror `inbox/openclaw_docs/plugins/plugin-inventory.md`)
**Last Updated**: 2026-06-22
**Status**: Active
