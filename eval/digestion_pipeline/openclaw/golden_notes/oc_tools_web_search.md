---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web
keywords:
  - openclaw web_search tool
  - web search provider matrix
  - web search auto-detection precedence
  - tools.web.search config
  - web_search tool parameters
  - web search provider comparison
  - group:web tool profile
  - openclaw configure --section web
topics:
  - OpenClaw
  - Web Search
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/web
access_control_group: ["general"]
---

# OpenClaw — Configuring the `web_search` Tool

## Overview

This note is the procedure for enabling and configuring OpenClaw's `web_search` agent tool: choosing among 14+ search providers, the auto-detection precedence order used when no provider is pinned, the `tools.web.search` config block, the tool's parameters, call examples, and tool-profile allowlisting. It mirrors the `web_search`-facing portion of the `tools/web` source page — intro, Quick start, Choosing a provider, Provider comparison, Auto-detection, Setting up web search, Config, Tool parameters, Examples, and Tool profiles. The native OpenAI/Codex hosted-search path, the guarded-fetch network-safety (SSRF) policy, API-key SecretRef storage, and the `x_search` X-posts tool live in the sibling note [oc_tools_web_x_search_safety](oc_tools_web_x_search_safety.md); the `web_fetch` tool lives in [oc_tools_web_fetch](oc_tools_web_fetch.md).

## What `web_search` Is

The `web_search` tool searches the web using your configured provider and returns results; results are cached by query for 15 minutes (configurable). OpenClaw also includes `x_search` for X (formerly Twitter) posts and `web_fetch` for lightweight URL fetching — in this phase `web_fetch` stays local while `web_search` and `x_search` can use xAI Responses under the hood. `web_search` is a lightweight HTTP tool, not browser automation: for JS-heavy sites or logins use the Web Browser tool, and for fetching a specific URL use Web Fetch.

## Quick Start

Enabling `web_search` is a three-step flow. First, choose a provider and complete any required setup — some providers are key-free while others use API keys (see the provider pages). Second, configure it with `openclaw configure --section web`, which stores the provider and any needed credential; you can also set an env var (for example `BRAVE_API_KEY`) and skip this step for API-backed providers. Third, the agent can call the tool:

```javascript
await web_search({ query: "OpenClaw plugin SDK" });
```

For X posts, the agent uses `await x_search({ query: "dinner recipes" });` (the `x_search` tool is documented in the sibling note).

## Choosing a Provider

The page presents a provider card group; each card links to that provider's own page. The available `web_search` providers are: **Brave Search** (structured results with snippets, supports `llm-context` mode, country/language filters, free tier available), **Codex Hosted Search** (AI-synthesized grounded answers through your Codex app-server account), **DuckDuckGo** (key-free, unofficial HTML-based integration, no API key needed), **Exa** (neural + keyword search with content extraction — highlights, text, summaries), **Firecrawl** (structured results, best paired with `firecrawl_search` and `firecrawl_scrape` for deep extraction), **Gemini** (AI-synthesized answers with citations via Google Search grounding), **Grok** (AI-synthesized answers with citations via xAI web grounding), **Kimi** (AI-synthesized answers with citations via Moonshot web search; ungrounded chat fallbacks fail explicitly), **MiniMax Search** (structured results via the MiniMax Token Plan search API), **Ollama Web Search** (search via a signed-in local Ollama host or the hosted Ollama API), **Parallel** (paid Parallel Search API via `PARALLEL_API_KEY`; higher rate limits and objective tuning), **Parallel Search (Free)** (key-free opt-in; Parallel's free Search MCP with LLM-optimized dense excerpts and no API key), **Perplexity** (structured results with content extraction controls and domain filtering), **SearXNG** (self-hosted meta-search, no API key needed, aggregates Google/Bing/DuckDuckGo and more), and **Tavily** (structured results with search depth, topic filtering, and `tavily_extract` for URL extraction).

### Provider Comparison

The source tabulates each provider by result style, supported filters, and API-key requirement. Key rows: **Brave** — structured snippets; country, language, time, `llm-context` mode filters; `BRAVE_API_KEY`. **Codex Hosted Search** — AI-synthesized + source URLs; domains, context size, user location filters; no key (uses Codex/OpenAI sign-in). **DuckDuckGo** — structured snippets; no filters; key-free. **Exa** — structured + extracted; neural/keyword mode, date, content extraction; `EXA_API_KEY`. **Firecrawl** — structured snippets; filters via the `firecrawl_search` tool; `FIRECRAWL_API_KEY`. **Gemini** — AI-synthesized + citations; `GEMINI_API_KEY`. **Grok** — AI-synthesized + citations; xAI OAuth, `XAI_API_KEY`, or `plugins.entries.xai.config.webSearch.apiKey`. **Kimi** — AI-synthesized + citations, fails on ungrounded chat fallbacks; `KIMI_API_KEY` / `MOONSHOT_API_KEY`. **MiniMax Search** — structured snippets; region (`global` / `cn`) filter; `MINIMAX_CODE_PLAN_KEY` / `MINIMAX_CODING_API_KEY` / `MINIMAX_OAUTH_TOKEN`. **Ollama Web Search** — structured snippets; no key for signed-in local hosts, `OLLAMA_API_KEY` for direct `https://ollama.com` search. **Parallel** — dense excerpts ranked for LLM context; `PARALLEL_API_KEY` (paid). **Parallel Search (Free)** — dense excerpts; key-free (free Search MCP). **Perplexity** — structured snippets; country, language, time, domains, content-limit filters; `PERPLEXITY_API_KEY` / `OPENROUTER_API_KEY`. **SearXNG** — structured snippets; categories, language filters; no key (self-hosted). **Tavily** — structured snippets; filters via the `tavily_search` tool; `TAVILY_API_KEY`.

## Auto-detection

The source's `## Auto-detection` heading is a pointer into the precedence behavior detailed under "Setting up web search" below: provider lists in docs and setup flows are alphabetical, but auto-detection keeps a separate precedence order. When no `provider` is configured, OpenClaw selects a provider from the precedence list rather than the alphabetical card order.

## Setting Up Web Search (Precedence Order)

If no `provider` is set, OpenClaw checks providers in this order and uses the first one that is ready. API-backed providers come first: **1. Brave** — `BRAVE_API_KEY` or `plugins.entries.brave.config.webSearch.apiKey` (order 10); **2. MiniMax Search** — `MINIMAX_CODE_PLAN_KEY` / `MINIMAX_CODING_API_KEY` / `MINIMAX_OAUTH_TOKEN` / `MINIMAX_API_KEY` or `plugins.entries.minimax.config.webSearch.apiKey` (order 15); **3. Gemini** — `plugins.entries.google.config.webSearch.apiKey`, `GEMINI_API_KEY`, or `models.providers.google.apiKey` (order 20); **4. Grok** — xAI OAuth, `XAI_API_KEY`, or `plugins.entries.xai.config.webSearch.apiKey` (order 30); **5. Kimi** — `KIMI_API_KEY` / `MOONSHOT_API_KEY` or `plugins.entries.moonshot.config.webSearch.apiKey` (order 40); **6. Perplexity** — `PERPLEXITY_API_KEY` / `OPENROUTER_API_KEY` or `plugins.entries.perplexity.config.webSearch.apiKey` (order 50); **7. Firecrawl** — `FIRECRAWL_API_KEY` or `plugins.entries.firecrawl.config.webSearch.apiKey` (order 60); **8. Exa** — `EXA_API_KEY` or `plugins.entries.exa.config.webSearch.apiKey`, optional `plugins.entries.exa.config.webSearch.baseUrl` overrides the Exa endpoint (order 65); **9. Tavily** — `TAVILY_API_KEY` or `plugins.entries.tavily.config.webSearch.apiKey` (order 70); **10. Parallel** — paid Parallel Search API via `PARALLEL_API_KEY` or `plugins.entries.parallel.config.webSearch.apiKey`, optional `plugins.entries.parallel.config.webSearch.baseUrl` overrides the endpoint (order 75). Configured-endpoint providers come after that: **11. SearXNG** — `SEARXNG_BASE_URL` or `plugins.entries.searxng.config.webSearch.baseUrl` (order 200).

Key-free providers such as **Parallel Search (Free)**, **DuckDuckGo**, **Ollama Web Search**, and **Codex Hosted Search** are available only when you select them explicitly with `tools.web.search.provider` or through `openclaw configure --section web`; OpenClaw does not send managed `web_search` queries to a key-free provider just because no API-backed provider is configured. OpenAI Responses models are an exception: while `tools.web.search.provider` is unset, they use OpenAI's native web search instead of the managed providers above — set `tools.web.search.provider` to `parallel-free` (or another provider) to route them through the managed path. All provider key fields support SecretRef objects; in auto-detect mode OpenClaw resolves only the selected provider key, leaving non-selected SecretRefs inactive so you can keep multiple providers configured without paying resolution cost for the ones you are not using.

## Config (`tools.web.search`)

The top-level `web_search` config block:

```json5
{
  tools: {
    web: {
      search: {
        enabled: true, // default: true
        provider: "brave", // or omit for auto-detection
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
    },
  },
}
```

Provider-specific config (API keys, base URLs, modes) lives under `plugins.entries.<plugin>.config.webSearch.*`. Gemini can also reuse `models.providers.google.apiKey` and `models.providers.google.baseUrl` as lower-priority fallbacks after its dedicated web-search config and `GEMINI_API_KEY`; Grok can also reuse an xAI OAuth auth profile from `openclaw models auth login --provider xai --method oauth`, with API-key config remaining the fallback. `tools.web.search.provider` is validated against the web-search provider ids declared by bundled and installed plugin manifests — a typo such as `"brvae"` fails config validation instead of silently falling back to auto-detection. If a configured provider only has stale plugin evidence (such as a leftover `plugins.entries.<plugin>` block after uninstalling a third-party plugin), OpenClaw keeps startup resilient and reports a warning so you can reinstall the plugin or run `openclaw doctor --fix` to clean up the stale config. The separate `web_fetch` fallback provider selection (`tools.web.fetch.provider`) is documented in [oc_tools_web_fetch](oc_tools_web_fetch.md). When you choose **Kimi** during `openclaw onboard` or `openclaw configure --section web`, OpenClaw can also ask for the Moonshot API region (`https://api.moonshot.ai/v1` or `https://api.moonshot.cn/v1`) and the default Kimi web-search model (defaults to `kimi-k2.6`).

## Tool Parameters

The `web_search` tool accepts these parameters: `query` — the search query (required); `count` — results to return (1–10, default 5); `country` — 2-letter ISO country code (e.g. "US", "DE"); `language` — ISO 639-1 language code (e.g. "en", "de"); `search_lang` — search-language code (Brave only); `freshness` — time filter `day`, `week`, `month`, or `year`; `date_after` — results after this date (YYYY-MM-DD); `date_before` — results before this date (YYYY-MM-DD); `ui_lang` — UI language code (Brave only); `domain_filter` — domain allowlist/denylist array (Perplexity only); `max_tokens` — total content budget, default 25000 (Perplexity only); `max_tokens_per_page` — per-page token limit, default 2048 (Perplexity only).

Not all parameters work with all providers. Brave `llm-context` mode rejects `ui_lang`, and `date_before` also needs `date_after` because Brave custom freshness ranges require both start and end dates. Gemini, Grok, and Kimi return one synthesized answer with citations; they accept `count` for shared-tool compatibility but it does not change the grounded answer shape, and Gemini supports `freshness`, `date_after`, and `date_before` by converting them to Google Search grounding time ranges. Perplexity behaves the same way when you use the Sonar/OpenRouter compatibility path (`plugins.entries.perplexity.config.webSearch.baseUrl` / `model` or `OPENROUTER_API_KEY`). SearXNG accepts `http://` only for trusted private-network or loopback hosts, and public SearXNG endpoints must use `https://`. Firecrawl and Tavily only support `query` and `count` through `web_search` — use their dedicated tools for advanced options.

## Examples

```javascript
// Basic search
await web_search({ query: "OpenClaw plugin SDK" });

// German-specific search
await web_search({ query: "TV online schauen", country: "DE", language: "de" });

// Recent results (past week)
await web_search({ query: "AI developments", freshness: "week" });

// Date range
await web_search({
  query: "climate research",
  date_after: "2024-01-01",
  date_before: "2024-06-30",
});

// Domain filtering (Perplexity only)
await web_search({
  query: "product reviews",
  domain_filter: ["-reddit.com", "-pinterest.com"],
});
```

## Tool Profiles

If you use tool profiles or allowlists, add `web_search`, `x_search`, or `group:web` (the `group:web` profile includes `web_search`, `x_search`, and `web_fetch`):

```json5
{
  tools: {
    allow: ["web_search", "x_search"],
    // or: allow: ["group:web"]  (includes web_search, x_search, and web_fetch)
  },
}
```

**Source**: OpenClaw documentation — `tools/web` (mirror `inbox/openclaw_docs/tools/web.md`)
**Last Updated**: 2026-06-22
**Status**: Active
