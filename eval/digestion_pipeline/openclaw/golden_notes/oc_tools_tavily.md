---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - tavily
keywords:
  - openclaw tavily tool
  - tavily_search tavily_extract
  - web_search provider tavily
  - tavily api key resolution
  - search_depth basic advanced
  - chunks_per_source requires query
  - tavily extract depth
topics:
  - OpenClaw
  - Tools
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/tavily
access_control_group: ["general"]
---

# OpenClaw — Tavily Search and Extract Tool

## Overview

This note is the procedure for enabling and using **Tavily** inside OpenClaw — a search API designed for AI applications. It mirrors the `tools/tavily` source page: how OpenClaw exposes Tavily (as the generic `web_search` provider OR as the explicit `tavily_search` / `tavily_extract` plugin tools), how to get and configure the API key, the full parameter tables for both tools, how to choose between `web_search`, `tavily_search`, and `tavily_extract`, and the advanced configuration (API-key resolution order, custom base URL, and the `chunks_per_source` requires-`query` rule). Tavily returns structured results optimized for LLM consumption with configurable search depth, topic filtering, domain filters, AI-generated answer summaries, and content extraction from URLs (including JavaScript-rendered pages).

## Tool Identity and Exposure

OpenClaw exposes Tavily in two ways: as the `web_search` provider for the generic search tool, and as explicit plugin tools `tavily_search` and `tavily_extract`. The plugin's identifying properties from the source page are:

| Property      | Value                               |
| ------------- | ----------------------------------- |
| Plugin id     | `tavily`                            |
| Auth          | `TAVILY_API_KEY` or config `apiKey` |
| Base URL      | `https://api.tavily.com` (default)  |
| Bundled tools | `tavily_search`, `tavily_extract`   |

## Getting Started

1. **Get an API key** — Create a Tavily account at `tavily.com`, then generate an API key in the dashboard.
2. **Configure the plugin and provider** — Enable the bundled `tavily` plugin and route the web search tool to the `tavily` provider:

```json5
{
  plugins: {
    entries: {
      tavily: {
        enabled: true,
        config: {
          webSearch: {
            apiKey: "tvly-...", // optional if TAVILY_API_KEY is set
            baseUrl: "https://api.tavily.com",
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "tavily",
      },
    },
  },
}
```

3. **Verify search runs** — Trigger a `web_search` from any agent, or call `tavily_search` directly.

Choosing Tavily in onboarding or `openclaw configure --section web` enables the bundled Tavily plugin automatically.

## Tool Reference: `tavily_search`

Use `tavily_search` when you want Tavily-specific search controls instead of generic `web_search`. Its parameters:

| Parameter         | Type         | Constraints / default                  | Description                                     |
| ----------------- | ------------ | -------------------------------------- | ----------------------------------------------- |
| `query`           | string       | required                               | Search query string. Keep under 400 characters. |
| `search_depth`    | enum         | `basic` (default), `advanced`          | `advanced` is slower but higher relevance.      |
| `topic`           | enum         | `general` (default), `news`, `finance` | Filter by topic family.                         |
| `max_results`     | integer      | 1-20                                   | Number of results.                              |
| `include_answer`  | boolean      | default `false`                        | Include a Tavily AI-generated answer summary.   |
| `time_range`      | enum         | `day`, `week`, `month`, `year`         | Filter results by recency.                      |
| `include_domains` | string array | (none)                                 | Only include results from these domains.        |
| `exclude_domains` | string array | (none)                                 | Exclude results from these domains.             |

Search depth tradeoff: `basic` is faster, high relevance, best for general-purpose queries (the default); `advanced` is slower, highest relevance, best for precision research and fact-finding.

## Tool Reference: `tavily_extract`

Use `tavily_extract` to extract clean content from one or more URLs. It handles JavaScript-rendered pages and supports query-focused chunking for targeted extraction. Its parameters:

| Parameter           | Type         | Constraints / default         | Description                                                 |
| ------------------- | ------------ | ----------------------------- | ----------------------------------------------------------- |
| `urls`              | string array | required, 1-20                | URLs to extract content from.                               |
| `query`             | string       | (optional)                    | Rerank extracted chunks by relevance to this query.         |
| `extract_depth`     | enum         | `basic` (default), `advanced` | Use `advanced` for JS-heavy pages, SPAs, or dynamic tables. |
| `chunks_per_source` | integer      | 1-5; **requires `query`**     | Chunks returned per URL. Errors if set without `query`.     |
| `include_images`    | boolean      | default `false`               | Include image URLs in results.                              |

Extract depth tradeoff: use `basic` for simple pages (try this first); use `advanced` for JS-rendered SPAs, dynamic content, and tables. Batch larger URL lists into multiple `tavily_extract` calls (max 20 per request), and use `query` plus `chunks_per_source` to get only relevant content instead of full pages.

## Choosing the Right Tool

The source page gives a decision table for which tool to reach for:

| Need                                 | Tool             |
| ------------------------------------ | ---------------- |
| Quick web search, no special options | `web_search`     |
| Search with depth, topic, AI answers | `tavily_search`  |
| Extract content from specific URLs   | `tavily_extract` |

The generic `web_search` tool with Tavily as the provider supports `query` and `count` (up to 20 results). For Tavily-specific controls (`search_depth`, `topic`, `include_answer`, domain filters, time range), use `tavily_search` instead.

## Advanced Configuration

**API key resolution order** — The Tavily client looks up its API key in this order: (1) `plugins.entries.tavily.config.webSearch.apiKey` (resolved through SecretRefs), then (2) `TAVILY_API_KEY` from the gateway environment. `tavily_extract` raises a setup error if neither is present.

**Custom base URL** — Override `plugins.entries.tavily.config.webSearch.baseUrl` if you front Tavily through a proxy. The default is `https://api.tavily.com`.

**`chunks_per_source` requires `query`** — `tavily_extract` rejects calls that pass `chunks_per_source` without a `query`. Tavily ranks chunks by query relevance, so the parameter is meaningless without one.

**Source**: OpenClaw documentation — `tools/tavily` (mirror `inbox/openclaw_docs/tools/tavily.md`)
**Last Updated**: 2026-06-22
**Status**: Active
