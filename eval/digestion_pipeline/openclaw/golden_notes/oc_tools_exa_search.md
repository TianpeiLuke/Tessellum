---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_search
keywords:
  - openclaw exa search
  - exa web_search provider
  - EXA_API_KEY
  - exa neural keyword hybrid search
  - exa content extraction highlights summary
  - exa search modes
  - plugins.entries.exa baseUrl
  - openclaw configure --section web
topics:
  - OpenClaw
  - Tools
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/exa-search
access_control_group: ["general"]
---

# OpenClaw — Configuring Exa AI as a web_search Provider

## Overview

This note is the step-by-step procedure for wiring [Exa AI](https://exa.ai/) into OpenClaw as a `web_search` provider, mirroring the `tools/exa-search` source page. Exa offers neural, keyword, and hybrid search modes with built-in content extraction (highlights, text, summaries). The procedure covers installing the official plugin, obtaining and storing an `EXA_API_KEY`, the `plugins.entries.exa` config block plus a base-URL override, the per-query tool parameters (`query`/`count`/`type`/`freshness`/`date_after`/`date_before`/`contents`), the `contents` content-extraction options, the six search modes, and the behavioral notes (default extraction, caching, result limits, time-filter exclusivity).

## Install plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/exa-plugin
openclaw gateway restart
```

## Get an API key

1. **Create an account** — sign up at [exa.ai](https://exa.ai/) and generate an API key from your dashboard.
2. **Store the key** — set `EXA_API_KEY` in the Gateway environment, or configure via `openclaw configure --section web`.

## Config

Select Exa as the active `web_search` provider and (optionally) set the API key and base URL in the `exa` plugin entry:

```json5
{
  plugins: {
    entries: {
      exa: {
        config: {
          webSearch: {
            apiKey: "exa-...", // optional if EXA_API_KEY is set
            baseUrl: "https://api.exa.ai", // optional; OpenClaw appends /search
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "exa",
      },
    },
  },
}
```

**Environment alternative:** set `EXA_API_KEY` in the Gateway environment. For a gateway install, put it in `~/.openclaw/.env`.

## Base URL override

Set `plugins.entries.exa.config.webSearch.baseUrl` when Exa search requests should go through a compatible proxy or alternate Exa endpoint. OpenClaw normalizes bare hosts by prepending `https://` and appends `/search` unless the path already ends there. The resolved endpoint is included in the search cache key, so results from different Exa endpoints are not shared.

## Tool parameters

The `web_search` tool (when backed by Exa) accepts these parameters:

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `query` | `string` | yes | Search query. |
| `count` | `number` | no | Results to return (1–100). |
| `type` | `'auto' \| 'neural' \| 'fast' \| 'deep' \| 'deep-reasoning' \| 'instant'` | no | Search mode. |
| `freshness` | `'day' \| 'week' \| 'month' \| 'year'` | no | Time filter. |
| `date_after` | `string` | no | Results after this date (`YYYY-MM-DD`). |
| `date_before` | `string` | no | Results before this date (`YYYY-MM-DD`). |
| `contents` | `object` | no | Content extraction options (see below). |

### Content extraction

Exa can return extracted content alongside search results. Pass a `contents` object to enable it:

```javascript
await web_search({
  query: "transformer architecture explained",
  type: "neural",
  contents: {
    text: true, // full page text
    highlights: { numSentences: 3 }, // key sentences
    summary: true, // AI summary
  },
});
```

| Contents option | Type | Description |
| --- | --- | --- |
| `text` | `boolean \| { maxCharacters }` | Extract full page text |
| `highlights` | `boolean \| { maxCharacters, query, numSentences, highlightsPerUrl }` | Extract key sentences |
| `summary` | `boolean \| { query }` | AI-generated summary |

### Search modes

The `type` parameter selects how Exa retrieves results:

| Mode | Description |
| --- | --- |
| `auto` | Exa picks the best mode (default) |
| `neural` | Semantic/meaning-based search |
| `fast` | Quick keyword search |
| `deep` | Thorough deep search |
| `deep-reasoning` | Deep search with reasoning |
| `instant` | Fastest results |

## Notes

- If no `contents` option is provided, Exa defaults to `{ highlights: true }` so results include key sentence excerpts.
- Results preserve `highlightScores` and `summary` fields from the Exa API response when available.
- Result descriptions are resolved from highlights first, then summary, then full text — whichever is available.
- `freshness` and `date_after`/`date_before` cannot be combined — use one time-filter mode.
- Up to 100 results can be returned per query (subject to Exa search-type limits).
- Results are cached for 15 minutes by default (configurable via `cacheTtlMinutes`).
- Exa is an official API integration with structured JSON responses.

**Source**: OpenClaw documentation — `tools/exa-search` (mirror `inbox/openclaw_docs/tools/exa-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
