---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - claude_max_api_proxy
keywords:
  - claude-max-api-proxy
  - claude max subscription openai endpoint
  - openai_base_url localhost 3456
  - claude code cli proxy
  - openai-compatible custom endpoint
  - claude -p subscription billing
  - claude opus 4 sonnet haiku model ids
  - launchagent auto-start proxy
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/claude-max-api-proxy
access_control_group: ["general"]
---

# OpenClaw — Claude Max API Proxy Provider Setup

## Overview

This procedure documents how to use the community **`claude-max-api-proxy`** tool to expose a Claude Max/Pro subscription as an OpenAI-compatible API endpoint, then point OpenClaw at it as a custom `/v1` backend — mirroring the `providers/claude-max-api-proxy` source page. It covers when this path fits versus the native Anthropic API, how the proxy converts OpenAI-format requests through the Claude Code CLI to Anthropic, the install/start/test/configure steps, the built-in model-ID catalog, the proxy-route request-shaping caveats and macOS auto-start option, and the operational notes (community-tool status, subscription/auth prerequisites). The page opens with a load-bearing **Warning**: this is technical compatibility only — Anthropic has blocked some subscription usage outside Claude Code in the past, and you must verify Anthropic's current billing rules before relying on it. Anthropic's support docs treat `claude -p` as Agent SDK / programmatic usage; starting June 15, 2026, subscription-plan `claude -p` usage draws from a separate monthly Agent SDK credit first, then from usage credits at standard API rates if usage credits are enabled.

## Why Use This?

The page frames the choice as two cost routes. The **Anthropic API** approach pays per token through the Claude Console or cloud and is best for production apps, shared automation, and volume. The **Claude subscription proxy** approach follows Claude Code / `claude -p` plan and credit rules and is best for personal experiments with compatible tools. If you have a Claude Max or Pro subscription and want to use it with OpenAI-compatible tools, this proxy may fit some personal workflows — but it is **not** an unlimited flat-rate path. API keys remain the clearer policy and billing path for production use.

## How It Works

The proxy sits between an OpenAI-format client and Anthropic, using the locally authenticated Claude Code CLI as the bridge:

```
Your App → claude-max-api-proxy → Claude Code CLI / claude -p → Anthropic
     (OpenAI format)              (converts format)          (uses your login)
```

The proxy: (1) accepts OpenAI-format requests at `http://localhost:3456/v1/chat/completions`; (2) converts them to Claude Code CLI commands; (3) returns responses in OpenAI format (streaming supported).

## Getting Started

The proxy requires **Node.js 22+** and the **Claude Code CLI**. Install the proxy globally and verify the Claude CLI is authenticated:

```bash
npm install -g claude-max-api-proxy

# Verify Claude CLI is authenticated
claude --version
```

Start the server (it runs at `http://localhost:3456`):

```bash
claude-max-api
# Server runs at http://localhost:3456
```

Test the proxy with a health check, a model list, and a chat completion:

```bash
# Health check
curl http://localhost:3456/health

# List models
curl http://localhost:3456/v1/models

# Chat completion
curl http://localhost:3456/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

Finally, point OpenClaw at the proxy as a custom OpenAI-compatible endpoint. `OPENAI_API_KEY` is set to `"not-needed"`, `OPENAI_BASE_URL` is the proxy's `/v1` route, and the primary model is referenced under the `openai/` namespace:

```json5
{
  env: {
    OPENAI_API_KEY: "not-needed",
    OPENAI_BASE_URL: "http://localhost:3456/v1",
  },
  agents: {
    defaults: {
      model: { primary: "openai/claude-opus-4" },
    },
  },
}
```

## Built-in Catalog

The proxy exposes three model IDs that map to Claude models:

| Model ID          | Maps To         |
| ----------------- | --------------- |
| `claude-opus-4`   | Claude Opus 4   |
| `claude-sonnet-4` | Claude Sonnet 4 |
| `claude-haiku-4`  | Claude Haiku 4  |

## Advanced Configuration

**Proxy-style OpenAI-compatible notes.** This path uses the same proxy-style OpenAI-compatible route as other custom `/v1` backends, so OpenAI-native request shaping is suppressed: native OpenAI-only request shaping does not apply; there is no `service_tier`, no Responses `store`, no prompt-cache hints, and no OpenAI reasoning-compat payload shaping; and the hidden OpenClaw attribution headers (`originator`, `version`, `User-Agent`) are not injected on the proxy URL.

**Auto-start on macOS with LaunchAgent.** The page also documents creating a LaunchAgent property-list at `~/Library/LaunchAgents/com.claude-max-api.plist` (label `com.claude-max-api`, `RunAtLoad` and `KeepAlive` both true) whose `ProgramArguments` run `node` against `claude-max-api-proxy/dist/server/standalone.js`, then loading it with `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.claude-max-api.plist`. *(The full plist XML is reproduced verbatim in the source page; it is omitted here for density and is not load-bearing for the OpenClaw wiring.)*

## Notes

- This is a **community tool**, not officially supported by Anthropic or OpenClaw.
- Requires an active Claude Max/Pro subscription with Claude Code CLI authenticated.
- Inherits Claude Code `claude -p` billing, usage-credit, and rate-limit behavior.
- The proxy runs locally and does not send data to any third-party servers.
- Streaming responses are fully supported.

For native Anthropic integration with the Claude CLI or API keys, the page points to the Anthropic provider (`/providers/anthropic`); for OpenAI/Codex subscriptions, it points to the OpenAI provider (`/providers/openai`).

**Source**: OpenClaw documentation — `providers/claude-max-api-proxy` (mirror `inbox/openclaw_docs/providers/claude-max-api-proxy.md`)
**Last Updated**: 2026-06-22
**Status**: Active
