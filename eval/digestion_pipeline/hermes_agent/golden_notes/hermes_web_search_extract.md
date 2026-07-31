---
tags:
  - resource
  - documentation
  - hermes_agent
  - web_search
  - tools
keywords:
  - web_search
  - web_extract
  - SearXNG
  - Firecrawl
  - auxiliary model summarization
  - per-capability backend
  - xAI Grok web search
topics:
  - Hermes Agent
  - Web Tools
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/web-search
access_control_group: ["general"]
---

# Hermes Agent — Web Search & Extract

## Overview

Web Search & Extract is the pair of **model-callable web tools** Hermes Agent exposes so an agent can pull information from the open web: `web_search` (search the web and return ranked results) and `web_extract` (fetch and extract readable content from one or more URLs). Both are driven by a **single backend selection** — the agent always calls the same two tool names, while the provider behind them is swapped via configuration. Providers are chosen interactively through `hermes tools` or set directly in `config.yaml`.

The procedure on this page covers three things: picking among the **8 supported backends** (Firecrawl is the default; SearXNG and DDGS are free), wiring each backend's API key or URL, and the **per-capability split** that lets you run a free search backend alongside a paid extract backend. A distinguishing design point is that `web_extract` does not hand raw page markdown straight to the agent — it runs returned content through a size-driven **auxiliary-model summarization** path to keep the context window usable and costs down. For raw, interactive page content the source steers you to the [browser tool](hermes_browser_automation_backends.md) instead.

## Backends

`web_search` and `web_extract` are backed by eight providers. Search support is universal; extract support is limited to a subset, so search-only backends (Brave, DDGS, xAI) must be paired with an extract-capable provider when `web_extract` is needed.

| Provider | Env Var | Search | Extract | Free tier |
|----------|---------|--------|---------|-----------|
| **Firecrawl** (default) | `FIRECRAWL_API_KEY` | yes | yes | 500 credits/mo |
| **SearXNG** | `SEARXNG_URL` | yes | no | Free (self-hosted) |
| **Brave Search (free tier)** | `BRAVE_SEARCH_API_KEY` | yes | no | 2,000 queries/mo |
| **DDGS (DuckDuckGo)** | (no key) | yes | no | Free |
| **Tavily** | `TAVILY_API_KEY` | yes | yes | 1,000 searches/mo |
| **Exa** | `EXA_API_KEY` | yes | yes | 1,000 searches/mo |
| **Parallel** | `PARALLEL_API_KEY` | yes | yes | Paid |
| **xAI (Grok)** | `XAI_API_KEY` or `hermes auth login xai-oauth` | yes | no | Paid (SuperGrok or per-token) |

DDGS uses the `ddgs` Python package under the hood; if it is not installed, run `pip install ddgs` or let Hermes lazy-install it on first use. xAI runs Grok's server-side `web_search` tool on the Responses API — results are LLM-generated rather than index-backed, so titles, descriptions, and URL choice are all model output (see the xAI trust-model caveat below). Brave, DDGS, and xAI are **search-only**: pair them with Firecrawl / Tavily / Exa / Parallel when you also need `web_extract`.

For paid **Nous Portal** subscribers, web search and extract are available through the **Tool Gateway** via managed Firecrawl with no API key needed. New installs can run `hermes setup --portal` to log in and turn on all gateway tools at once; existing installs can flip just web via `hermes tools`.

## How `web_extract` handles long pages

Backends return raw page markdown, which can be huge (forum threads, docs sites, news with embedded comments). To keep the context window usable and costs down, `web_extract` runs returned content through the **`web_extract` auxiliary model** before handing it to the agent. Behavior is purely **size-driven**:

| Page size (characters) | What happens |
|------------------------|--------------|
| Under 5,000 | Returned as-is — no LLM call, full markdown reaches the agent |
| 5,000 – 500,000 | Single-pass summary via the `web_extract` auxiliary model, capped at ~5,000 chars of output |
| 500,000 – 2,000,000 | Chunked: split into 100k-char chunks, summarize each in parallel, then synthesize a final ~5,000-char summary |
| Over 2,000,000 | Refused with a hint to use a more focused source URL |

The summary keeps quotes, code blocks, and key facts in their original formatting — it is a content compressor, not a paraphraser. If summarization fails or times out, Hermes falls back to the first ~5,000 chars of raw content rather than a useless error.

By default (`auxiliary.web_extract.provider: "auto"`) the summarizing model is your **main chat model** — same provider and model as `hermes model`. On expensive reasoning models every long-page extract adds meaningful cost, so you can route extraction summaries to a cheap, fast model independent of your main:

```yaml
# ~/.hermes/config.yaml
auxiliary:
  web_extract:
    provider: openrouter
    model: google/gemini-3-flash-preview
    timeout: 360       # seconds; raise if you hit summarization timeouts
```

When you specifically need raw, unsummarized content (e.g. scraping a structured page where the LLM summary would drop fields), use `browser_navigate` + `browser_snapshot` instead — the browser tool returns the live accessibility tree without auxiliary-model rewriting (subject to its own 8,000-char snapshot cap).

## Setup

Run `hermes tools`, navigate to **Web Search & Extract**, and pick a provider; the wizard prompts for the required URL or API key and writes it to your config. Per-provider keys go in `~/.hermes/.env` (e.g. `FIRECRAWL_API_KEY`, `TAVILY_API_KEY`, `EXA_API_KEY`, `PARALLEL_API_KEY`). Self-hosted Firecrawl points at your own instance via `FIRECRAWL_API_URL=http://localhost:3002` (the API key is then optional). Tavily, Exa, and Parallel each provide both search and extract; their setup is just the env-var key.

### SearXNG (free, self-hosted)

SearXNG is a privacy-respecting, open-source metasearch engine aggregating 70+ engines — **no API key required**, just point Hermes at a running instance. It is **search-only**, so `web_extract` requires a separate extract provider. The recommended path is self-hosting with Docker, which gives a private instance with no rate limits:

```yaml
# ~/searxng/docker-compose.yml
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8888:8080"
    volumes:
      - ./searxng:/etc/searxng:rw
    environment:
      - SEARXNG_BASE_URL=http://localhost:8888/
    restart: unless-stopped
```

After `docker compose up -d`, SearXNG ships with JSON output **disabled** by default — copy the generated `settings.yml` out of the container, add `json` under the `formats` block (alongside `html`), copy it back, and `docker restart searxng`. Verify with `curl -s "http://localhost:8888/search?q=test&format=json"`; a `403 Forbidden` means JSON is still disabled. Then set `SEARXNG_URL=http://localhost:8888` in `.env` and select it. Public instances (listed at searx.space) work too but carry rate limits, variable uptime, and may disable JSON at any time, so self-hosting is recommended for production.

Because SearXNG handles only search, pair it with an extract provider via the per-capability keys:

```yaml
# ~/.hermes/config.yaml
web:
  search_backend: "searxng"
  extract_backend: "firecrawl"   # or tavily, exa, parallel
```

### xAI (Grok)

xAI routes `web_search` through Grok's server-side web_search tool on the Responses API — Grok runs the actual searching and returns the top results as structured JSON. It works with either credential path with no new env vars or setup wizard: set `XAI_API_KEY` in `.env`, or for SuperGrok subscribers run `hermes auth login xai-oauth`. Then select `web.backend: "xai"`. Optional knobs include `xai.model` (a reasoning model is required by web_search; `grok-build-0.1` default), mutually-exclusive `allowed_domains` / `excluded_domains` (max 5 each), and `timeout` (90s default). On a 401 the provider performs **a single forced OAuth-token refresh and retries** (covers mid-window revocation and opaque tokens the proactive expiry check cannot decode); env-var credentials skip the retry.

The xAI **trust model** differs from index-backed providers: Grok is an LLM choosing which URLs to surface and writing the titles/descriptions itself, so a maliciously crafted query (e.g. injected via untrusted upstream input) can in principle steer Grok into emitting attacker-chosen URLs. Treat returned URLs as model-generated links — validate before fetching, especially when the query came from untrusted input.

## Configuration

A single backend sets one provider for all web capabilities; per-capability keys override it for search vs extract independently (e.g. free SearXNG search + paid Firecrawl extract):

```yaml
# ~/.hermes/config.yaml
web:
  backend: "searxng"            # firecrawl | searxng | brave-free | ddgs | tavily | exa | parallel | xai
  search_backend: "searxng"     # optional: used by web_search
  extract_backend: "firecrawl"  # optional: used by web_extract
```

When per-capability keys are empty, both fall through to `web.backend`; when that is also empty, the backend is **auto-detected** from whichever credentials are present. The resolution precedence per capability is: (1) `web.search_backend` / `web.extract_backend`, (2) `web.backend`, (3) auto-detect from env vars. Auto-detection order is `FIRECRAWL_API_KEY`/`FIRECRAWL_API_URL` → `PARALLEL_API_KEY` → `TAVILY_API_KEY` → `EXA_API_KEY` → `SEARXNG_URL`. **xAI is deliberately NOT in the auto-detection chain** — having `XAI_API_KEY` set does not auto-route web through xAI, because those credentials are also used for inference / TTS / image gen; opt in explicitly with `web.backend: "xai"`.

## Verify your setup

Run `hermes setup` to see which web backend is detected (e.g. `Web Search & Extract (searxng)`). Or check via the CLI by activating the venv and running the web-tools module directly, which prints the active backend and its status:

```bash
source ~/.hermes/hermes-agent/.venv/bin/activate
python -m tools.web_tools
```

## Troubleshooting

- **`web_search` returns `{"success": false}`** — check `SEARXNG_URL` is reachable; HTTP 403 means JSON format is disabled (add `json` to `formats` and restart); a connection error may mean the container is not running (`docker ps | grep searxng`).
- **`web_extract` says "search-only backend"** — SearXNG cannot extract; set `web.extract_backend` to a provider that supports extraction (firecrawl / tavily / exa / parallel).
- **SearXNG returns 0 results** — some public instances disable engines/categories; try a different query, a different public instance, or self-host.
- **Rate limited on a public instance** — switch to a self-hosted Docker instance, which has no rate limits.
- **`web_extract` returns truncated content with a "summarization timed out" note** — raise `auxiliary.web_extract.timeout` (default 360s on fresh installs, 30s if the key is missing), switch the `web_extract` auxiliary task to a faster model, or use `browser_navigate` where summarization is the wrong tool.

## Optional skill: `searxng-search`

For agents that need SearXNG via `curl` directly (e.g. as a fallback when the web toolset is unavailable), install the optional skill with `hermes skills install official/research/searxng-search`. It teaches the agent to call the SearXNG JSON API via `curl` or Python, filter by category (`general`, `news`, `science`, etc.), handle pagination and errors, and fall back gracefully when SearXNG is unreachable.

**Source**: `inbox/hermes_agent_docs/user-guide/features/web-search.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/web-search
**Last Updated**: 2026-06-19
**Status**: Active
