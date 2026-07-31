---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_search
keywords:
  - openclaw ollama web search
  - ollama web_search provider
  - tools.web.search.provider ollama
  - ollama signin web search
  - OLLAMA_API_KEY hosted search
  - ollama webSearch baseUrl
  - local ollama proxy web_search
  - key-free web search provider
topics:
  - OpenClaw
  - Web Search Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/ollama-search
access_control_group: ["general"]
---

# OpenClaw — Configuring Ollama as a Web Search Provider

## Overview

This note is the procedure for configuring **Ollama Web Search** as OpenClaw's bundled `web_search` provider, mirroring the `tools/ollama-search` source page. Ollama Web Search uses Ollama's web-search API and returns structured results with titles, URLs, and snippets. It supports two paths: a **key-free local/self-hosted** path (a reachable Ollama host plus `ollama signin`, no web-search-specific API key by default) and a **direct hosted** path (the Ollama provider base URL set to `https://ollama.com` with a real `OLLAMA_API_KEY`). It covers the setup steps, the `tools.web.search.provider: "ollama"` config switch, host/base-URL reuse from the model provider, bearer-auth reuse, and the local-proxy-vs-hosted-endpoint behavior.

## Setup

Ollama Web Search is selected through three steps:

1. **Start Ollama** — make sure Ollama is installed and running.
2. **Sign in** — run `ollama signin`.
3. **Choose Ollama Web Search** — run `openclaw configure --section web`, then select **Ollama Web Search** as the provider.

For local or self-hosted Ollama, this setup does not need an API key by default. It does require an Ollama host that is reachable from OpenClaw and `ollama signin`. If you already use Ollama for models, Ollama Web Search reuses the same configured host (no separate host needs to be supplied).

```bash
ollama signin
openclaw configure --section web
```

## Config

The minimal config selects Ollama as the search provider:

```json5
{
  tools: {
    web: {
      search: {
        provider: "ollama",
      },
    },
  },
}
```

An optional Ollama host override can be set on the plugin entry:

```json5
{
  plugins: {
    entries: {
      ollama: {
        config: {
          webSearch: {
            baseUrl: "http://ollama-host:11434",
          },
        },
      },
    },
  },
}
```

If you already configure Ollama as a model provider, the web-search provider can reuse that host instead of declaring it separately:

```json5
{
  models: {
    providers: {
      ollama: {
        baseUrl: "http://ollama-host:11434",
      },
    },
  },
}
```

The Ollama model provider uses `baseUrl` as the canonical key. The web-search provider also honors `baseURL` on `models.providers.ollama` for compatibility with OpenAI SDK-style config examples. If no explicit Ollama base URL is set, OpenClaw uses `http://127.0.0.1:11434`. If your Ollama host expects bearer auth, OpenClaw reuses `models.providers.ollama.apiKey` (or the matching env-backed provider auth) for requests to that configured host.

For the direct hosted path, point the Ollama provider base URL at `https://ollama.com` and supply a real `OLLAMA_API_KEY`:

```json5
{
  models: {
    providers: {
      ollama: {
        baseUrl: "https://ollama.com",
        apiKey: "OLLAMA_API_KEY",
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "ollama",
      },
    },
  },
}
```

## Notes

- No web-search-specific API key field is required for this provider.
- If the Ollama host is auth-protected, OpenClaw reuses the normal Ollama provider API key when present.
- If `baseUrl` is `https://ollama.com`, OpenClaw calls `https://ollama.com/api/web_search` directly and sends the configured Ollama API key as bearer auth.
- If the configured host does not expose web search and `OLLAMA_API_KEY` is set, OpenClaw can fall back to `https://ollama.com/api/web_search` without sending that env key to the local host.
- OpenClaw warns during setup if Ollama is unreachable or not signed in, but it does not block selection.
- OpenClaw does not auto-select Ollama Web Search when no higher-priority credentialed provider is configured; choose it explicitly with `tools.web.search.provider: "ollama"`.
- Local Ollama daemon hosts use the local proxy endpoint `/api/experimental/web_search`, which signs and forwards to Ollama Cloud.
- `https://ollama.com` hosts use the public hosted endpoint `/api/web_search` directly with bearer API-key auth.

**Source**: OpenClaw documentation — `tools/ollama-search` (mirror `inbox/openclaw_docs/tools/ollama-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
