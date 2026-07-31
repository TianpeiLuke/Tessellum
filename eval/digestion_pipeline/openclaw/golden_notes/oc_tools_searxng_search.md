---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_search
keywords:
  - openclaw searxng web search
  - self-hosted key-free search provider
  - searxng provider config
  - SEARXNG_BASE_URL env var
  - web search auto-detection order 200
  - searxng network guard ssrf
  - searxng format=json api
  - tools.web.search.provider searxng
topics:
  - OpenClaw
  - Web Search Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/searxng-search
access_control_group: ["general"]
---

# OpenClaw — SearXNG Self-Hosted Web Search Provider

## Overview

This note is the procedure for configuring **SearXNG** as OpenClaw's `web_search` provider, mirroring the `tools/searxng-search` source page. SearXNG is an open-source meta-search engine that aggregates results from Google, Bing, DuckDuckGo, and other sources, and OpenClaw supports it as a **self-hosted, key-free** provider. Its advantages over commercial providers are that it is **free and unlimited** (no API key or commercial subscription required), **privacy / air-gap** friendly (queries never leave your network), and **works anywhere** (no region restrictions on commercial search APIs). The procedure below covers running an instance, setting `provider: "searxng"` plus the plugin `webSearch` config, the `SEARXNG_BASE_URL` environment variable and its auto-detection order, the transport/network-guard rules, the plugin config field reference, and the behavior notes.

## Setup

Setup is two steps. First, **run a SearXNG instance** — the simplest path is a Docker container:

```bash
docker run -d -p 8888:8080 searxng/searxng
```

Or use any existing SearXNG deployment you have access to (see the SearXNG documentation for production setup). Second, **configure** OpenClaw to use it, either interactively or via the environment variable. The interactive path runs the web configuration section and selects `searxng` as the provider:

```bash
openclaw configure --section web
# Select "searxng" as the provider
```

Alternatively, set the env var and let auto-detection find it:

```bash
export SEARXNG_BASE_URL="http://localhost:8888"
```

## Config

Select SearXNG as the active `web_search` provider via `tools.web.search.provider`:

```json5
{
  tools: {
    web: {
      search: {
        provider: "searxng",
      },
    },
  },
}
```

Plugin-level settings for the SearXNG instance live under `plugins.entries.searxng.config.webSearch`:

```json5
{
  plugins: {
    entries: {
      searxng: {
        config: {
          webSearch: {
            baseUrl: "http://localhost:8888",
            categories: "general,news", // optional
            language: "en", // optional
          },
        },
      },
    },
  },
}
```

The `baseUrl` field also accepts SecretRef objects.

**Transport rules** govern which scheme/host combinations are permitted:

- `https://` works for public or private SearXNG hosts.
- `http://` is only accepted for trusted private-network or loopback hosts.
- Public SearXNG hosts must use `https://`.
- Private/internal hosts use the self-hosted network guard; public `https://` hosts stay on the strict web-search guard and cannot redirect to private addresses.

## Environment variable

Set `SEARXNG_BASE_URL` as an alternative to config:

```bash
export SEARXNG_BASE_URL="http://localhost:8888"
```

When `SEARXNG_BASE_URL` is set and no explicit provider is configured, auto-detection picks SearXNG automatically — but at the lowest priority, so any API-backed provider with a key wins first.

## Plugin config reference

| Field        | Description                                                        |
| ------------ | ------------------------------------------------------------------ |
| `baseUrl`    | Base URL of your SearXNG instance (required)                       |
| `categories` | Comma-separated categories such as `general`, `news`, or `science` |
| `language`   | Language code for results such as `en`, `de`, or `fr`              |

## Notes

- **JSON API** — uses SearXNG's native `format=json` endpoint, not HTML scraping. For the JSON API to work, the SearXNG instance must have the `json` format enabled in its `settings.yml` under `search.formats`.
- **Image result URLs** — image-category results include `img_src` when SearXNG returns a direct image URL.
- **No API key** — works with any SearXNG instance out of the box.
- **Base URL validation** — `baseUrl` must be a valid `http://` or `https://` URL; public hosts must use `https://`.
- **Network guard** — private/internal SearXNG endpoints opt in to private-network access; public `https://` SearXNG endpoints keep strict SSRF protection.
- **Auto-detection order** — SearXNG is checked after API-backed providers with configured keys (order 200). Key-free providers such as DuckDuckGo or Ollama Web Search are not auto-selected without an explicit provider choice.
- **Self-hosted** — you control the instance, queries, and upstream search engines.
- **Categories** default to `general` when not configured.
- **Category fallback** — if a non-`general` category request succeeds but returns zero results, OpenClaw retries the same query once with `general` before returning an empty result set.

**Source**: OpenClaw documentation — `tools/searxng-search` (mirror `inbox/openclaw_docs/tools/searxng-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
