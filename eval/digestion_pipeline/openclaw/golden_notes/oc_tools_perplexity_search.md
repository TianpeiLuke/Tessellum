---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_search
keywords:
  - openclaw perplexity search
  - web_search provider perplexity
  - perplexity_api_key openrouter_api_key
  - perplexity sonar openrouter compatibility
  - web_search tool parameters
  - domain_filter freshness count
  - plugins.entries.perplexity.config.websearch
topics:
  - OpenClaw
  - Perplexity Web Search
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/perplexity-search
access_control_group: ["general"]
---

# OpenClaw — Configuring the Perplexity `web_search` Provider

## Overview

This note is the operator procedure for wiring OpenClaw's `web_search` agent tool to **Perplexity** as its search provider, mirroring the `tools/perplexity-search` source page. OpenClaw supports the **Perplexity Search API** as a `web_search` provider that returns structured results with `title`, `url`, and `snippet` fields; for compatibility it also supports legacy **Perplexity Sonar / OpenRouter** setups, where the provider switches to the chat-completions path and returns AI-synthesized answers with citations instead of structured Search API results. This note covers installing the plugin, getting a Perplexity API key, OpenRouter compatibility, the two config examples (Native and OpenRouter/Sonar), where to set the key, the tool parameters, and the behavior notes.

## Two paths: Search API vs. Sonar / OpenRouter

The provider runs in one of two modes, selected by config. By default with a Perplexity key it uses the **Native Perplexity Search API** path, returning structured `title` / `url` / `snippet` rows. The provider switches to the **legacy Sonar / OpenRouter chat-completions path** (returning one AI-synthesized answer with citations) if any of these is true: you use `OPENROUTER_API_KEY`; you store an `sk-or-...` key in `plugins.entries.perplexity.config.webSearch.apiKey`; or you set `plugins.entries.perplexity.config.webSearch.baseUrl` / `model`.

## Install plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/perplexity-plugin
openclaw gateway restart
```

## Getting a Perplexity API key

1. Create a Perplexity account at [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api).
2. Generate an API key in the dashboard.
3. Store the key in config or set `PERPLEXITY_API_KEY` in the Gateway environment.

## OpenRouter compatibility

If you were already using OpenRouter for Perplexity Sonar, keep `provider: "perplexity"` and set `OPENROUTER_API_KEY` in the Gateway environment, or store an `sk-or-...` key in `plugins.entries.perplexity.config.webSearch.apiKey`. Optional compatibility controls are `plugins.entries.perplexity.config.webSearch.baseUrl` and `plugins.entries.perplexity.config.webSearch.model`.

## Config examples

### Native Perplexity Search API

```json5
{
  plugins: {
    entries: {
      perplexity: {
        config: {
          webSearch: {
            apiKey: "pplx-...",
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "perplexity",
      },
    },
  },
}
```

### OpenRouter / Sonar compatibility

```json5
{
  plugins: {
    entries: {
      perplexity: {
        config: {
          webSearch: {
            apiKey: "<openrouter-api-key>",
            baseUrl: "https://openrouter.ai/api/v1",
            model: "perplexity/sonar-pro",
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "perplexity",
      },
    },
  },
}
```

## Where to set the key

**Via config:** run `openclaw configure --section web`. It stores the key in `~/.openclaw/openclaw.json` under `plugins.entries.perplexity.config.webSearch.apiKey`. That field also accepts SecretRef objects.

**Via environment:** set `PERPLEXITY_API_KEY` or `OPENROUTER_API_KEY` in the Gateway process environment. For a gateway install, put it in `~/.openclaw/.env` (or your service environment).

If `provider: "perplexity"` is configured and the Perplexity key SecretRef is unresolved with no env fallback, startup/reload **fails fast**.

## Tool parameters

These parameters apply to the **native Perplexity Search API path**:

- `query` (`string`, required) — search query.
- `count` (`number`, default `5`) — number of results to return (1–10).
- `country` (`string`) — 2-letter ISO country code (e.g. `US`, `DE`).
- `language` (`string`) — ISO 639-1 language code (e.g. `en`, `de`, `fr`).
- `freshness` (`'day' | 'week' | 'month' | 'year'`) — time filter; `day` is 24 hours.
- `date_after` (`string`) — only results published after this date (`YYYY-MM-DD`).
- `date_before` (`string`) — only results published before this date (`YYYY-MM-DD`).
- `domain_filter` (`string[]`) — domain allowlist/denylist array (max 20).
- `max_tokens` (`number`, default `25000`) — total content budget (max `1000000`).
- `max_tokens_per_page` (`number`, default `2048`) — per-page token limit.

For the **legacy Sonar / OpenRouter compatibility path**: `query`, `count`, and `freshness` are accepted; `count` is compatibility-only there (the response is still one synthesized answer with citations rather than an N-result list); and Search API-only filters such as `country`, `language`, `date_after`, `date_before`, `domain_filter`, `max_tokens`, and `max_tokens_per_page` return explicit errors.

```javascript
// Country and language-specific search
await web_search({
  query: "renewable energy",
  country: "DE",
  language: "de",
});

// Domain filtering (allowlist)
await web_search({
  query: "climate research",
  domain_filter: ["nature.com", "science.org", ".edu"],
});

// Domain filtering (denylist - prefix with -)
await web_search({
  query: "product reviews",
  domain_filter: ["-reddit.com", "-pinterest.com"],
});
```

### Domain filter rules

- Maximum 20 domains per filter.
- Cannot mix allowlist and denylist in the same request.
- Use `-` prefix for denylist entries (e.g., `["-reddit.com"]`).

## Notes

- Perplexity Search API returns structured web search results (`title`, `url`, `snippet`).
- OpenRouter or explicit `plugins.entries.perplexity.config.webSearch.baseUrl` / `model` switches Perplexity back to Sonar chat completions for compatibility.
- Sonar / OpenRouter compatibility returns one synthesized answer with citations, not structured result rows.
- Results are cached for 15 minutes by default (configurable via `cacheTtlMinutes`).

**Source**: OpenClaw documentation — `tools/perplexity-search` (mirror `inbox/openclaw_docs/tools/perplexity-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
