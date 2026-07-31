---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_search
keywords:
  - openclaw kimi web search
  - moonshot web search provider
  - kimi_api_key moonshot_api_key
  - kimi-k2.6 web search model
  - moonshot.ai moonshot.cn base url
  - kimi_web_search_ungrounded error
  - tools.web.search.kimi baseurl
  - grounding evidence search_results citations
topics:
  - OpenClaw
  - Web Search Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/kimi-search
access_control_group: ["general"]
---

# OpenClaw — Configuring Kimi (Moonshot) as a `web_search` Provider

## Overview

This note is the procedure for enabling **Kimi** as an OpenClaw `web_search` provider, mirroring the `tools/kimi-search` source page. Kimi uses **Moonshot web search** to produce AI-synthesized answers with inline citations, the same grounded-response approach used by Gemini and Grok. It covers getting and storing a Moonshot API key (`KIMI_API_KEY` / `MOONSHOT_API_KEY`), the `plugins.entries.moonshot` + `tools.web.search` config, the `.ai` vs `.cn` region/base-URL reuse from chat config (and the HTTP 401 host-mismatch caveat), how grounding evidence is required for success (and the `kimi_web_search_ungrounded` structured error otherwise), and the supported parameters (`query`, with `count` accepted for compatibility only).

## Get an API key

Create a key from [Moonshot AI](https://platform.moonshot.cn/), then store it for the Gateway in one of two ways:

- Set `KIMI_API_KEY` **or** `MOONSHOT_API_KEY` in the Gateway environment, or
- Configure interactively via the `web` section:

```bash
openclaw configure --section web
```

When you choose **Kimi** during `openclaw onboard` or `openclaw configure --section web`, OpenClaw can also ask for:

- the Moonshot API region — either `https://api.moonshot.ai/v1` or `https://api.moonshot.cn/v1`; and
- the default Kimi web-search model (defaults to `kimi-k2.6`).

## Config

Kimi is configured under the `moonshot` plugin entry's `webSearch` block, with `tools.web.search.provider` set to `"kimi"`:

```json5
{
  plugins: {
    entries: {
      moonshot: {
        config: {
          webSearch: {
            apiKey: "sk-...", // optional if KIMI_API_KEY or MOONSHOT_API_KEY is set
            baseUrl: "https://api.moonshot.ai/v1",
            model: "kimi-k2.6",
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "kimi",
      },
    },
  },
}
```

### Region / base-URL reuse and the host-mismatch caveat

If you use the China API host for chat (`models.providers.moonshot.baseUrl`: `https://api.moonshot.cn/v1`), OpenClaw reuses that same host for Kimi `web_search` when `tools.web.search.kimi.baseUrl` is omitted, so keys from [platform.moonshot.cn](https://platform.moonshot.cn/) do not hit the international endpoint by mistake (which often returns HTTP 401). Override with `tools.web.search.kimi.baseUrl` when you need a different search base URL.

### Credential and default-value precedence

The **environment alternative** is to set `KIMI_API_KEY` or `MOONSHOT_API_KEY` in the Gateway environment; for a gateway install, put it in `~/.openclaw/.env`. If you omit `baseUrl`, OpenClaw defaults to `https://api.moonshot.ai/v1`. If you omit `model`, OpenClaw defaults to `kimi-k2.6`.

## How it works

Kimi uses Moonshot web search to synthesize answers with inline citations, similar to Gemini and Grok's grounded response approach.

OpenClaw treats Kimi `web_search` as successful **only after Moonshot returns native web-search grounding evidence**, such as a replayable `$web_search` tool payload, `search_results`, or citation URLs. If Kimi stops immediately with a plain chat answer like "I cannot browse the internet" and no grounding evidence, OpenClaw returns a structured `kimi_web_search_ungrounded` error instead of wrapping that text as a search result. The remediation is to retry the query, switch to a structured provider such as Brave, or use `web_fetch` / the browser tool when you already have a target URL.

## Supported parameters

Kimi search supports `query`.

`count` is accepted for shared `web_search` compatibility, but Kimi still returns one synthesized answer with citations rather than an N-result list. Provider-specific filters are not currently supported.

**Source**: OpenClaw documentation — `tools/kimi-search` (mirror `inbox/openclaw_docs/tools/kimi-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
