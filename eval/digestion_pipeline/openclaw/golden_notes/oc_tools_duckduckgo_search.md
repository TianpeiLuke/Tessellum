---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_search
keywords:
  - openclaw duckduckgo search
  - key-free web_search provider
  - tools.web.search.provider duckduckgo
  - openclaw configure --section web
  - duckduckgo region safesearch
  - bot-challenge captcha scraping
  - experimental html search provider
topics:
  - OpenClaw
  - Web Search Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/duckduckgo-search
access_control_group: ["general"]
---

# OpenClaw — Configuring DuckDuckGo as a Key-Free Web Search Provider

## Overview

This note is the procedure for configuring **DuckDuckGo** as OpenClaw's `web_search` provider — the one key-free provider that needs no API key or account. It mirrors the `tools/duckduckgo-search` source page: the `openclaw configure --section web` setup step, the `tools.web.search.provider` config plus optional plugin-level region/SafeSearch settings, the per-query tool parameters (`query`/`count`/`region`/`safeSearch`), and the experimental HTML-scraping / bot-challenge caveats that distinguish DuckDuckGo from API-backed providers. Because DuckDuckGo scrapes DuckDuckGo's non-JavaScript search pages rather than calling an official API, OpenClaw treats it as an **experimental, unofficial** integration and recommends an API-backed provider for production use.

## Setup

No API key is needed — you only select DuckDuckGo as your provider. Run the interactive web-section configurator and pick `duckduckgo`:

```bash
openclaw configure --section web
# Select "duckduckgo" as the provider
```

## Config

The provider selection persists as `tools.web.search.provider`:

```json5
{
  tools: {
    web: {
      search: {
        provider: "duckduckgo",
      },
    },
  },
}
```

Region and SafeSearch defaults can be set at the plugin level under `plugins.entries.duckduckgo.config.webSearch`. The `region` field takes a DuckDuckGo region code and `safeSearch` accepts `"strict"`, `"moderate"`, or `"off"`:

```json5
{
  plugins: {
    entries: {
      duckduckgo: {
        config: {
          webSearch: {
            region: "us-en", // DuckDuckGo region code
            safeSearch: "moderate", // "strict", "moderate", or "off"
          },
        },
      },
    },
  },
}
```

## Tool parameters

The `web_search` tool, when backed by DuckDuckGo, exposes these typed parameters that the model can set per call:

- **`query`** (`string`, required) — the search query.
- **`count`** (`number`, default `5`) — results to return, in the range 1–10.
- **`region`** (`string`) — DuckDuckGo region code, e.g. `us-en`, `uk-en`, `de-de`.
- **`safeSearch`** (`'strict' | 'moderate' | 'off'`, default `moderate`) — SafeSearch level.

`region` and `safeSearch` can also be set in plugin config (see above); per-query tool parameters override the configured values.

## Notes

The source page records these operating caveats for the key-free provider:

- **No API key** — works after you select DuckDuckGo as your `web_search` provider.
- **Experimental** — gathers results from DuckDuckGo's non-JavaScript HTML search pages, not an official API or SDK.
- **Bot-challenge risk** — DuckDuckGo may serve CAPTCHAs or block requests under heavy or automated use.
- **HTML parsing** — results depend on page structure, which can change without notice.
- **Explicit selection** — OpenClaw does not choose DuckDuckGo automatically when no API-backed provider is configured.
- **SafeSearch defaults to moderate** when not configured.

For production use, the docs recommend [Brave Search](https://docs.openclaw.ai/tools/brave-search) (free tier available) or another API-backed provider.

**Source**: OpenClaw documentation — `tools/duckduckgo-search` (mirror `inbox/openclaw_docs/tools/duckduckgo-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
