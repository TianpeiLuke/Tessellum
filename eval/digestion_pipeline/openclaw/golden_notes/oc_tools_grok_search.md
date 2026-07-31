---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_search
keywords:
  - grok web search
  - xai web-grounded responses
  - openclaw web_search provider grok
  - xai oauth web search
  - XAI_API_KEY
  - x_search code_execution
  - webSearch.apiKey baseUrl
  - tools.web.search.timeoutSeconds
topics:
  - OpenClaw
  - Web Search Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/grok-search
access_control_group: ["general"]
---

# OpenClaw — Configuring Grok (xAI) as a `web_search` Provider

## Overview

This note is the procedure for configuring **Grok** as an OpenClaw `web_search` provider, mirroring the `tools/grok-search` source page. Grok uses **xAI web-grounded responses** to produce AI-synthesized answers backed by live search results with citations (similar to Gemini's Google Search grounding). The procedure covers the xAI-OAuth-preferred onboarding flow, the API-key fallback and credential alternatives, the JSON5 config block, the related `x_search` follow-up, the supported `query` parameter and Grok's provider-specific 60-second default timeout, and base-URL / Responses-endpoint overrides. All claims are grounded in the mirror page; the cross-provider Web Search overview and `x_search` itself are owned elsewhere and only linked.

## Credential model and `x_search` / `code_execution` reuse

Grok web search **prefers your existing xAI OAuth sign-in when one is available**. If no OAuth profile exists, the same xAI API key can also power the built-in `x_search` tool for X (formerly Twitter) post search and the `code_execution` tool. If you store the key under `plugins.entries.xai.config.webSearch.apiKey`, OpenClaw reuses it as a fallback for the bundled xAI model provider too. For post-level X metrics such as reposts, replies, bookmarks, or views, the page advises preferring `x_search` with the exact post URL or status ID instead of a broad search query.

## Onboarding and configure

If you choose **Grok** during `openclaw onboard` or `openclaw configure --section web`, OpenClaw can use an existing xAI OAuth profile **without prompting for a separate web-search key**. If OAuth is not available, it falls back to xAI API-key setup. OpenClaw can also show a separate follow-up step to enable `x_search` with the same xAI credential. That follow-up: only appears after you choose Grok for `web_search`; is not a separate top-level web-search provider choice; and can optionally set the `x_search` model during the same flow. If you skip it, you can enable or change `x_search` later in config.

## Sign in or get an API key

The page documents a three-step onboarding sequence:

1. **Use xAI OAuth** — if you already signed in with xAI during onboarding or model auth, choose Grok as the `web_search` provider; no separate API key is required:

   ```bash
   openclaw onboard --auth-choice xai-oauth
   openclaw config set tools.web.search.provider grok
   ```

2. **Use an API key fallback** — get an API key from [xAI](https://console.x.ai/) when OAuth is unavailable or you intentionally want key-backed web-search config.
3. **Store the key** — set `XAI_API_KEY` in the Gateway environment, or configure via `openclaw configure --section web`.

## Config

The provider is wired by storing the (optional) xAI web-search credential under `plugins.entries.xai.config.webSearch` and selecting `grok` as the `tools.web.search.provider`:

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          webSearch: {
            apiKey: "xai-...", // optional if xAI OAuth or XAI_API_KEY is available
            baseUrl: "https://api.x.ai/v1", // optional Responses API proxy/base URL override
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "grok",
      },
    },
  },
}
```

**Credential alternatives** (any one of three): sign in with `openclaw models auth login --provider xai --method oauth`; set `XAI_API_KEY` in the Gateway environment; or store `plugins.entries.xai.config.webSearch.apiKey`. For a gateway install, put env vars in `~/.openclaw/.env`.

## How it works

Grok uses xAI web-grounded responses to synthesize answers with inline citations, similar to Gemini's Google Search grounding approach.

## Supported parameters

Grok search supports `query`. `count` is accepted for shared `web_search` compatibility, but Grok still returns one synthesized answer with citations rather than an N-result list. Provider-specific filters are not currently supported. Grok uses a provider-specific **60 second default timeout** because xAI Responses web-grounded searches can run longer than the shared `web_search` default; set `tools.web.search.timeoutSeconds` to override it.

## Base URL overrides

Set `plugins.entries.xai.config.webSearch.baseUrl` when Grok web search should route through an operator proxy or xAI-compatible Responses endpoint. OpenClaw posts to `<baseUrl>/responses` after trimming trailing slashes. `x_search` uses the same `webSearch.baseUrl` fallback unless `plugins.entries.xai.config.xSearch.baseUrl` is set.

**Source**: OpenClaw documentation — `tools/grok-search` (mirror `inbox/openclaw_docs/tools/grok-search.md`)
**Last Updated**: 2026-06-22
**Status**: Active
