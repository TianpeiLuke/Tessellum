---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_search
keywords:
  - openclaw gemini web search
  - google search grounding
  - GEMINI_API_KEY
  - websearch apikey precedence
  - gemini-2.5-flash web search
  - ssrf-guarded citation resolution
  - websearch baseurl override
  - tools web search provider gemini
topics:
  - OpenClaw
  - Web Search Tools
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/gemini-search
access_control_group: ["general"]
---

# OpenClaw — Configuring Gemini as a Web Search Provider

## Overview

This note is the procedure for configuring **Gemini** as OpenClaw's `web_search` provider, mirroring the `tools/gemini-search` source page. OpenClaw supports Gemini models with built-in Google Search grounding, which returns AI-synthesized answers backed by live Google Search results with citations (unlike providers that return a plain list of links and snippets). The steps below cover obtaining and storing an API key, the JSON5 plugin/tool config block, the three-source credential precedence chain, how grounding and SSRF-guarded citation resolution work, the supported `web_search` parameters, model selection, and base-URL overrides for routing through an operator proxy.

## Get an API key

Two steps:

1. **Create a key** — Go to [Google AI Studio](https://aistudio.google.com/apikey) and create an API key.
2. **Store the key** — Set `GEMINI_API_KEY` in the Gateway environment, reuse `models.providers.google.apiKey`, or configure a dedicated web-search key via:

```bash
openclaw configure --section web
```

For a gateway install, put env keys in `~/.openclaw/.env`.

## Config

Gemini web search is enabled by configuring the `google` plugin's `webSearch` block and pointing the shared web-search tool at the `gemini` provider:

```json5
{
  plugins: {
    entries: {
      google: {
        config: {
          webSearch: {
            apiKey: "AIza...", // optional if GEMINI_API_KEY or models.providers.google.apiKey is set
            baseUrl: "https://generativelanguage.googleapis.com/v1beta", // optional; falls back to models.providers.google.baseUrl
            model: "gemini-2.5-flash", // default
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "gemini",
      },
    },
  },
}
```

All three `webSearch` keys are optional — `apiKey` may be omitted if `GEMINI_API_KEY` or `models.providers.google.apiKey` is set, and `baseUrl` and `model` fall back to documented defaults.

## Credential precedence

Gemini web search resolves its API key from three sources in this order: `plugins.entries.google.config.webSearch.apiKey` first, then `GEMINI_API_KEY`, then `models.providers.google.apiKey`. For base URLs the precedence is the dedicated `plugins.entries.google.config.webSearch.baseUrl` first, falling back to `models.providers.google.baseUrl` when the dedicated value is unset.

## How it works

Unlike traditional search providers that return a list of links and snippets, Gemini uses Google Search grounding to produce AI-synthesized answers with inline citations. The results include both the synthesized answer and the source URLs. Citation handling and SSRF protection behave as follows:

- Citation URLs from Gemini grounding are automatically resolved from Google redirect URLs to direct URLs.
- Redirect resolution uses the SSRF guard path (HEAD + redirect checks + http/https validation) before returning the final citation URL.
- Redirect resolution uses strict SSRF defaults, so redirects to private/internal targets are blocked.

## Supported parameters

Gemini search supports `query`, `freshness`, `date_after`, and `date_before`. `count` is accepted for shared `web_search` compatibility, but Gemini grounding still returns one synthesized answer with citations rather than an N-result list. The `freshness` parameter accepts `day`, `week`, `month`, `year`, and the shared shortcuts `pd`, `pw`, `pm`, and `py`. OpenClaw converts these values, or an explicit `date_after`/`date_before` range, into Gemini Google Search grounding's `timeRangeFilter`. `country`, `language`, and `domain_filter` are not supported.

## Model selection

The default model is `gemini-2.5-flash` (described as fast and cost-effective). Any Gemini model that supports grounding can be used via `plugins.entries.google.config.webSearch.model`.

## Base URL overrides

Set `plugins.entries.google.config.webSearch.baseUrl` when Gemini web search must route through an operator proxy or custom Gemini-compatible endpoint. If that is unset, Gemini web search reuses `models.providers.google.baseUrl`. A plain `https://generativelanguage.googleapis.com` value is normalized to `https://generativelanguage.googleapis.com/v1beta`; custom proxy paths are kept as provided after trimming trailing slashes.

**Source**: OpenClaw documentation — `tools/gemini-search` (mirror `inbox/openclaw_docs/tools/gemini-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
