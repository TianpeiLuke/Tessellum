---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_search
keywords:
  - openclaw brave search
  - brave web_search provider
  - brave_api_key
  - websearch mode llm-context
  - web_search tool parameters
  - brave search plan credit
  - plugins.entries.brave.config
  - websearch baseurl proxy
topics:
  - OpenClaw
  - Web Search Tools
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/brave-search
access_control_group: ["general"]
---

# OpenClaw — Brave Search `web_search` Provider Setup

## Overview

This note is the operator/agent procedure for enabling the Brave Search API as OpenClaw's `web_search` provider, mirroring the `tools/brave-search` source page. It covers getting a Brave Search API key, the config block that wires Brave under `plugins.entries.brave.config.webSearch.*` (plus the `tools.web.search` selector), the `web_search` tool parameters the model calls, and the plan/credit, caching, mode (`web` vs `llm-context`), and diagnostics notes. OpenClaw supports the Brave Search API as a `web_search` provider; provider-specific Brave settings now live under `plugins.entries.brave.config.webSearch.*`, while the legacy `tools.web.search.apiKey` still loads through a compatibility shim but is no longer the canonical path.

## Get an API key

The page gives three steps to obtain and wire a Brave Search API key:

1. Create a Brave Search API account at [https://brave.com/search/api/](https://brave.com/search/api/).
2. In the dashboard, choose the **Search** plan and generate an API key.
3. Store the key in config or set `BRAVE_API_KEY` in the Gateway environment.

## Config example

The provider is enabled by an `plugins.entries.brave.config.webSearch` block plus a `tools.web.search` selector that picks `brave` as the provider; the config below is reproduced verbatim from the source page:

```json5
{
  plugins: {
    entries: {
      brave: {
        config: {
          webSearch: {
            apiKey: "BRAVE_API_KEY_HERE",
            mode: "web", // or "llm-context"
            baseUrl: "https://api.search.brave.com", // optional proxy/base URL override
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "brave",
        maxResults: 5,
        timeoutSeconds: 30,
      },
    },
  },
}
```

`webSearch.mode` controls the Brave transport: `web` (default) is normal Brave web search returning titles, URLs, and snippets; `llm-context` uses the Brave LLM Context API and returns pre-extracted text chunks and sources for grounding. `webSearch.baseUrl` can point Brave requests at a trusted Brave-compatible proxy or gateway — OpenClaw appends `/res/v1/web/search` or `/res/v1/llm/context` to the configured base URL and keeps the base URL in the cache key. Public endpoints must use `https://`; `http://` is accepted only for trusted loopback or private-network proxy hosts.

## Tool parameters

The `web_search` tool the agent/model calls accepts these parameters (verbatim from the page's `<ParamField>` entries):

- `query` (string, **required**) — search query.
- `count` (number, default `5`) — number of results to return (1–10).
- `country` (string) — 2-letter ISO country code (e.g. `US`, `DE`).
- `language` (string) — ISO 639-1 language code for search results (e.g. `en`, `de`, `fr`).
- `search_lang` (string) — Brave search-language code (e.g. `en`, `en-gb`, `zh-hans`).
- `ui_lang` (string) — ISO language code for UI elements.
- `freshness` (`'day' | 'week' | 'month' | 'year'`) — time filter; `day` is 24 hours.
- `date_after` (string) — only results published after this date (`YYYY-MM-DD`).
- `date_before` (string) — only results published before this date (`YYYY-MM-DD`).

The page's worked examples (verbatim) show country/language scoping, recent-results freshness, and a date-range search:

```javascript
// Country and language-specific search
await web_search({
  query: "renewable energy",
  country: "DE",
  language: "de",
});

// Recent results (past week)
await web_search({
  query: "AI news",
  freshness: "week",
});

// Date range search
await web_search({
  query: "AI developments",
  date_after: "2024-01-01",
  date_before: "2024-06-30",
});
```

## Notes

The page documents plan, mode, caching, and diagnostics behavior to keep in mind:

- OpenClaw uses the Brave **Search** plan. A legacy subscription (e.g. the original Free plan with 2,000 queries/month) remains valid but does not include newer features like LLM Context or higher rate limits.
- Each Brave plan includes **\$5/month in free credit** (renewing). The Search plan costs \$5 per 1,000 requests, so the credit covers 1,000 queries/month. Set a usage limit in the Brave dashboard to avoid unexpected charges; see the Brave API portal for current plans.
- The Search plan includes the LLM Context endpoint and AI inference rights. Storing results to train or tune models requires a plan with explicit storage rights (see the Brave Terms of Service).
- `llm-context` mode returns grounded source entries instead of the normal web-search snippet shape.
- `llm-context` mode supports `freshness` and bounded `date_after` + `date_before` ranges. It does not support `ui_lang`; `date_before` without `date_after` is rejected because Brave requires custom freshness ranges to include both start and end dates.
- `ui_lang` must include a region subtag like `en-US`.
- Results are cached for 15 minutes by default (configurable via `cacheTtlMinutes`).
- Custom `webSearch.baseUrl` values are included in Brave cache identity, so proxy-specific responses do not collide.
- Enable the `brave.http` diagnostics flag to log Brave request URLs/query params, response status/timing, and search-cache hit/miss/write events while troubleshooting. The flag never logs the API key or response bodies, but search queries can be sensitive.

**Source**: OpenClaw documentation — `tools/brave-search` (mirror `inbox/openclaw_docs/tools/brave-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
