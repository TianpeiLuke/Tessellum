---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_search
keywords:
  - openclaw parallel search
  - parallel-free search mcp
  - parallel web_search provider
  - PARALLEL_API_KEY
  - tools.web.search.provider parallel
  - parallel objective search_queries
  - parallel base url override
  - llm-optimized dense excerpts
topics:
  - OpenClaw
  - Web Search Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/parallel-search
access_control_group: ["general"]
---

# OpenClaw — Configuring Parallel as a Web Search Provider

## Overview

This note is the procedure for wiring [Parallel](https://parallel.ai/) into OpenClaw as the backing `web_search` provider, mirroring the `tools/parallel-search` source page. The Parallel plugin ships two distinct providers: **Parallel Search (Free)** (`parallel-free`), Parallel's hosted key-free [Search MCP](https://docs.parallel.ai/integrations/mcp/search-mcp) that requires no account or API key, and **Parallel Search** (`parallel`), Parallel's paid Search API that requires a `PARALLEL_API_KEY` and offers higher rate limits and objective tuning. Both return ranked, LLM-optimized excerpts from a web index built for AI agents. The procedure below covers installing the plugin, provisioning the paid API key, the `plugins.entries.parallel.config.webSearch` + `tools.web.search.provider` config block, the base-URL override for the paid provider, the `objective` / `search_queries` / `count` / `session_id` / `client_model` tool parameters, and the result-shaping / caching behavior.

## Provider Selection

Set `tools.web.search.provider` to `parallel-free` or `parallel` to choose one explicitly — selection is not automatic. The free `parallel-free` provider requires no API key, but it still must be selected as the managed provider; it does not engage implicitly. One important interaction: **OpenAI Responses models use OpenAI's native web search when `tools.web.search.provider` is unset, so they bypass the Parallel providers** — set `tools.web.search.provider` to `parallel-free` or `parallel` to route them through Parallel instead.

## Install plugin

Install the official plugin, then restart Gateway:

```bash
openclaw plugins install @openclaw/parallel-plugin
openclaw gateway restart
```

## API key (paid provider)

`parallel-free` requires no API key (only explicit selection as the managed provider). The paid `parallel` provider needs an API key, provisioned in two steps: (1) **Create an account** — sign up at [platform.parallel.ai](https://platform.parallel.ai) and generate an API key from your dashboard; (2) **Store the key** — set `PARALLEL_API_KEY` in the Gateway environment, or configure it via `openclaw configure --section web`. For a gateway install, put `PARALLEL_API_KEY` in `~/.openclaw/.env`.

## Config

The plugin config lives under `plugins.entries.parallel.config.webSearch`; the provider switch lives under `tools.web.search.provider`. Use `"parallel-free"` for the free Search MCP, or `"parallel"` for the paid API-backed provider shown here. Both `apiKey` and `baseUrl` are optional in the plugin block:

```json5
{
  plugins: {
    entries: {
      parallel: {
        config: {
          webSearch: {
            apiKey: "par-...", // optional if PARALLEL_API_KEY is set
            baseUrl: "https://api.parallel.ai", // optional; OpenClaw appends /v1/search
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        // Use "parallel-free" for the free Search MCP, or "parallel" for
        // the paid API-backed provider shown here.
        provider: "parallel",
      },
    },
  },
}
```

As an environment alternative, set `PARALLEL_API_KEY` in the Gateway environment (in `~/.openclaw/.env` for a gateway install) instead of the inline `apiKey`.

## Base URL override

The base-URL override applies to the **paid `parallel` provider only**. The free `parallel-free` provider always uses `https://search.parallel.ai/mcp`.

Set `plugins.entries.parallel.config.webSearch.baseUrl` when Parallel requests should go through a compatible proxy or alternate Parallel endpoint (for example, the Cloudflare AI Gateway). OpenClaw normalizes bare hosts by prepending `https://` and appends `/v1/search` unless the path already ends there. The resolved endpoint is included in the search cache key, so results from different Parallel endpoints are not shared.

## Tool parameters

OpenClaw exposes Parallel's native search shape so the model can fill in both the natural-language goal and a few short keyword queries — the pairing Parallel [recommends](https://docs.parallel.ai/search/best-practices) for best results. The parameters are:

- **`objective`** (`string`, required) — natural-language description of the underlying question or goal (max 5000 chars). Should be self-contained.
- **`search_queries`** (`string[]`, required) — concise keyword search queries, 3-6 words each (1-5 entries, max 200 chars each). Provide 2-3 diverse queries for best results.
- **`count`** (`number`) — results to return (1-40).
- **`session_id`** (`string`) — optional Parallel session id (max 1000 chars on `parallel`; the free `parallel-free` Search MCP caps it at 100). Pass the `sessionId` from a previous Parallel result on follow-up searches that are part of the same task so Parallel can group related calls and improve subsequent results. An id past the limit is dropped and a fresh one is generated.
- **`client_model`** (`string`) — optional identifier of the model making the call (e.g. `claude-opus-4-7`, `gpt-5.5`). Lets Parallel tailor default settings for your model's capabilities. Pass the exact active model slug; do not shorten to a family alias.

## Notes

- Parallel ranks and compresses results based on LLM reasoning utility, not human click-through; expect dense excerpts in each result rather than full-page content.
- Result excerpts come back as the `excerpts` array and are also joined into the `description` field for compatibility with the generic `web_search` contract.
- Parallel returns a `session_id` on every response; OpenClaw surfaces it as `sessionId` in the tool payload so callers can group follow-up searches.
- `searchId`, `warnings`, and `usage` from Parallel are passed through when present.
- OpenClaw always forwards a resolved result count to Parallel as `advanced_settings.max_results`. The caller's `count` arg wins, then the top-level `tools.web.search.maxResults` setting, otherwise OpenClaw's generic `web_search` default (5). This keeps result volume consistent when switching between providers; Parallel on its own defaults to 10.
- Results are cached for 15 minutes by default (configurable via `cacheTtlMinutes`).
- The free `parallel-free` provider accepts the same parameters. It applies `count` client-side and generates a `session_id` per call when one is not supplied.

**Source**: OpenClaw documentation — `tools/parallel-search` (mirror `inbox/openclaw_docs/tools/parallel-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
