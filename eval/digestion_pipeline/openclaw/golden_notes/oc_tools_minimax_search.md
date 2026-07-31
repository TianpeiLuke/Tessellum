---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_search
keywords:
  - openclaw minimax web_search
  - minimax token plan search
  - minimax_code_plan_key
  - minimax_oauth_token
  - tools.web.search provider minimax
  - minimax cn global region
  - minimax_api_host region resolution
  - openclaw configure section web
topics:
  - OpenClaw
  - Web Search Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/minimax-search
access_control_group: ["general"]
---

# OpenClaw — Configuring MiniMax as a `web_search` Provider

## Overview

This note is the procedure for wiring **MiniMax** in as an OpenClaw `web_search` provider through the MiniMax **Token Plan search API**, mirroring the `tools/minimax-search` source page. MiniMax returns structured search results with titles, URLs, snippets, and related queries. The procedure covers obtaining a Token Plan credential, the accepted environment-variable aliases, the `plugins.entries.minimax` + `tools.web.search` config block, the CN-vs-global region resolution order, and the two supported tool parameters (`query`, `count`). Per-provider model/image/speech/auth detail and the generic `web_search` contract (auto-detection across all providers) live on sibling pages and are linked, not restated.

## Get a Token Plan credential

Two steps register the credential:

1. **Create a key** — create or copy a MiniMax Token Plan key from the [MiniMax Platform](https://platform.minimax.io/user-center/basic-information/interface-key). OAuth setups can reuse `MINIMAX_OAUTH_TOKEN` instead.
2. **Store the key** — set `MINIMAX_CODE_PLAN_KEY` in the Gateway environment, or configure interactively via `openclaw configure --section web`.

OpenClaw also accepts `MINIMAX_CODING_API_KEY`, `MINIMAX_OAUTH_TOKEN`, and `MINIMAX_API_KEY` as env aliases. `MINIMAX_API_KEY` should point at a **search-enabled** Token Plan credential; ordinary MiniMax model API keys may not be accepted by the Token Plan search endpoint.

## Config

Select MiniMax as the search provider and (optionally) supply the key/region in the plugin config block:

```json5
{
  plugins: {
    entries: {
      minimax: {
        config: {
          webSearch: {
            apiKey: "sk-cp-...", // optional if a MiniMax Token Plan env var is set
            region: "global", // or "cn"
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "minimax",
      },
    },
  },
}
```

**Environment alternative:** set `MINIMAX_CODE_PLAN_KEY`, `MINIMAX_CODING_API_KEY`, `MINIMAX_OAUTH_TOKEN`, or `MINIMAX_API_KEY` in the Gateway environment. For a gateway install, put it in `~/.openclaw/.env`.

## Region selection

MiniMax Search uses these endpoints:

- **Global:** `https://api.minimax.io/v1/coding_plan/search`
- **CN:** `https://api.minimaxi.com/v1/coding_plan/search`

If `plugins.entries.minimax.config.webSearch.region` is unset, OpenClaw resolves the region in this order:

1. `tools.web.search.minimax.region` / plugin-owned `webSearch.region`
2. `MINIMAX_API_HOST`
3. `models.providers.minimax.baseUrl`
4. `models.providers.minimax-portal.baseUrl`

That means CN onboarding or `MINIMAX_API_HOST=https://api.minimaxi.com/...` automatically keeps MiniMax Search on the CN host too. Even when you authenticated MiniMax through the OAuth `minimax-portal` path, web search still registers as provider id `minimax`; the OAuth provider base URL is used as a region hint for CN/global host selection, and `MINIMAX_OAUTH_TOKEN` can satisfy the MiniMax Search bearer credential.

## Supported parameters

| Parameter | Type    | Constraints | Description |
| --------- | ------- | ----------- | ----------- |
| `query`   | string  | required    | Search query string. |
| `count`   | integer | 1-10        | Number of results to return. OpenClaw trims the returned list to this size. |

Provider-specific filters are not currently supported.

**Source**: OpenClaw documentation — `tools/minimax-search` (mirror `inbox/openclaw_docs/tools/minimax-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
