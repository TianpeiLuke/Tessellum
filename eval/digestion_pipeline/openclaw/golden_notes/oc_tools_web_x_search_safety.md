---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web
keywords:
  - openclaw native openai web search
  - openclaw native codex web search
  - web search network safety ssrf
  - guarded fetch fake-ip range
  - storing web search api keys secretref
  - x_search xai grok x posts
  - tools.web.search.openaiCodex
  - x_search config parameters
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

# OpenClaw — Native Web Search, Network Safety, and `x_search`

## Overview

This note is the native-search-and-safety half of the OpenClaw `tools/web` page (the `web_search` provider-selection half lives in the sibling `oc_tools_web_search` note). It covers four procedures: enabling and bounding OpenAI's and Codex's provider-owned hosted `web_search`, the guarded-fetch **network-safety** policy that governs managed search HTTP calls (SSRF defense + the narrow fake-IP DNS allowance), storing provider API keys via config file / env var / SecretRef, and the `x_search` tool that queries X (formerly Twitter) posts through xAI. Every claim, config key, and code block below is grounded in `inbox/openclaw_docs/tools/web.md`.

## Native OpenAI web search

Direct OpenAI Responses models use OpenAI's hosted `web_search` tool **automatically** when OpenClaw web search is enabled and **no managed provider is pinned**. This is provider-owned behavior in the bundled OpenAI plugin and applies only to native OpenAI API traffic — not OpenAI-compatible proxy base URLs or Azure routes. To keep the managed `web_search` tool for OpenAI models instead, set `tools.web.search.provider` to another provider such as `brave`; to disable both managed search and native OpenAI search, set `tools.web.search.enabled: false`.

A separate opt-in path lets direct OpenAI ChatGPT Responses traffic use OpenAI's hosted `web_search` tool: it is gated by `tools.web.search.openaiCodex.enabled: true` and applies only to eligible `openai/*` models using `api: "openai-chatgpt-responses"`. Note that OpenAI Responses models are also the one exception to managed auto-detection — while `tools.web.search.provider` is unset they use OpenAI's native web search instead of the auto-detected managed providers, so route them through the managed path by setting `tools.web.search.provider` to `parallel-free` (or another provider).

## Native Codex web search

The Codex app-server runtime uses Codex's hosted `web_search` tool automatically when web search is enabled and no managed provider is selected. Native hosted search and OpenClaw's managed `web_search` dynamic tool are **mutually exclusive**, so managed search cannot bypass native domain restrictions. OpenClaw uses the managed tool when hosted search is unavailable, explicitly disabled, or replaced by a selected managed provider. OpenClaw keeps Codex's standalone `web.run` extension disabled because production app-server traffic rejects its user-defined `web` namespace.

The Codex native-search procedure and its options:

- Configure native search under `tools.web.search.openaiCodex`.
- Set `tools.web.search.provider: "codex"` to provision Codex Hosted Search as the managed `web_search` provider for any parent model. Each call runs a bounded ephemeral Codex app-server turn and **fails if Codex does not emit a hosted `webSearch` item**.
- `mode: "cached"` is the default preference, but Codex resolves it to live external access for unrestricted app-server turns; set `"live"` to request live access explicitly.
- Set `tools.web.search.provider` to a managed provider such as `brave` to use OpenClaw's managed `web_search` instead.
- Set `tools.web.search.openaiCodex.enabled: false` to opt out of Codex-hosted search; other managed providers remain available.
- Restricting the Codex native tool surface also keeps managed `web_search` available.
- When `allowedDomains` is set, automatic managed fallback **fails closed** if hosted search is unavailable so the native allowlist cannot be bypassed.
- Tool-disabled LLM-only runs disable both native and managed search.
- `tools.web.search.enabled: false` disables both managed and native search.

Persistent effective Codex search-policy changes start a fresh bound thread so an already loaded app-server thread cannot keep stale hosted-search access; transient per-turn restrictions use a temporary restricted thread and preserve the existing binding for later resume. Example config provisioning Codex Hosted Search from non-Codex parent models too:

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        // Optional: use Codex Hosted Search from non-Codex parent models too.
        provider: "codex",
        openaiCodex: {
          enabled: true,
          mode: "cached",
          allowedDomains: ["example.com"],
          contextSize: "high",
          userLocation: {
            country: "US",
            city: "New York",
            timezone: "America/New_York",
          },
        },
      },
    },
  },
}
```

For runtimes and providers that do not support native Codex search, Codex can use the managed `web_search` fallback through OpenClaw's dynamic tool namespace; use an explicit managed provider when you need OpenClaw's provider-specific network controls instead of Codex-hosted search. Selecting `provider: "codex"` enables the bundled `codex` plugin and uses the same `tools.web.search.openaiCodex` restrictions shown above. Authenticate the Codex app-server first with `openclaw models auth login --provider openai`. The parent agent can use any model or runtime; only the bounded search worker runs through Codex.

## Network safety

Managed HTTP `web_search` provider calls use OpenClaw's **guarded fetch** path. For trusted provider API hosts, OpenClaw allows Surge, Clash, and sing-box fake-IP DNS answers in `198.18.0.0/15` and `fc00::/7` **only for that provider hostname**; other private, loopback, link-local, and metadata destinations remain blocked. Codex Hosted Search is the exception: its bounded worker delegates network access to Codex app-server's hosted `web_search` tool.

This automatic fake-IP allowance does **not** apply to arbitrary `web_fetch` URLs. For `web_fetch`, enable `tools.web.fetch.ssrfPolicy.allowRfc2544BenchmarkRange` and `tools.web.fetch.ssrfPolicy.allowIpv6UniqueLocalRange` explicitly, and only when your trusted proxy owns those synthetic ranges (these opt-ins are detailed in the `oc_tools_web_fetch` sibling note).

## Storing API keys

Provider key fields can be set either in the config file or via environment variable. Run `openclaw configure --section web`, or set the key directly in config — config-file form (Brave shown):

```json5
{
  plugins: {
    entries: {
      brave: {
        config: {
          webSearch: {
            apiKey: "YOUR_KEY", // pragma: allowlist secret
          },
        },
      },
    },
  },
}
```

Environment-variable form — set the provider env var in the Gateway process environment (for a gateway install, put it in `~/.openclaw/.env`):

```bash
export BRAVE_API_KEY="YOUR_KEY"
```

All provider key fields support **SecretRef** objects. Plugin-scoped SecretRefs under `plugins.entries.<plugin>.config.webSearch.apiKey` are resolved for the installed API-backed web-search providers — including Brave, Exa, Firecrawl, Gemini, Grok, Kimi, MiniMax, Parallel, Perplexity, and Tavily — whether the provider is picked explicitly via `tools.web.search.provider` or selected through auto-detect. In auto-detect mode OpenClaw resolves only the *selected* provider key: non-selected SecretRefs stay inactive, so you can keep multiple providers configured without paying resolution cost for the ones you are not using.

## x_search

`x_search` queries X (formerly Twitter) posts using xAI and returns AI-synthesized answers with citations. It accepts natural-language queries and optional structured filters. OpenClaw only enables the built-in xAI `x_search` tool on the request that serves this tool call. Per the xAI docs, `x_search` supports keyword search, semantic search, user search, and thread fetch; for per-post engagement stats such as reposts, replies, bookmarks, or views, prefer a targeted lookup for the exact post URL or status ID, because broad keyword searches may find the right post but return less complete per-post metadata. A good pattern is: locate the post first, then run a second `x_search` query focused on that exact post.

For `x_search`, configure `plugins.entries.xai.config.xSearch.*`. It uses the same xAI auth profile as chat, or the `XAI_API_KEY` / plugin web-search credential used by Grok web search. Legacy `tools.web.x_search.*` config is auto-migrated by `openclaw doctor --fix`. When you choose Grok during `openclaw onboard` or `openclaw configure --section web`, OpenClaw can also offer optional `x_search` setup with the same credential — a separate follow-up step inside the Grok path, not a separate top-level web-search provider choice; if you pick another provider, OpenClaw does not show the `x_search` prompt.

### x_search config

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          xSearch: {
            enabled: true,
            model: "grok-4-1-fast-non-reasoning",
            baseUrl: "https://api.x.ai/v1", // optional, overrides webSearch.baseUrl
            inlineCitations: false,
            maxTurns: 2,
            timeoutSeconds: 30,
            cacheTtlMinutes: 15,
          },
          webSearch: {
            apiKey: "xai-...", // optional if an xAI auth profile or XAI_API_KEY is set
            baseUrl: "https://api.x.ai/v1", // optional shared xAI Responses base URL
          },
        },
      },
    },
  },
}
```

`x_search` posts to `<baseUrl>/responses` when `plugins.entries.xai.config.xSearch.baseUrl` is set. If that field is omitted, it falls back to `plugins.entries.xai.config.webSearch.baseUrl`, then the legacy `tools.web.search.grok.baseUrl`, and finally the public xAI endpoint.

### x_search parameters

| Parameter | Description |
| --- | --- |
| `query` | Search query (required) |
| `allowed_x_handles` | Restrict results to specific X handles |
| `excluded_x_handles` | Exclude specific X handles |
| `from_date` | Only include posts on or after this date (YYYY-MM-DD) |
| `to_date` | Only include posts on or before this date (YYYY-MM-DD) |
| `enable_image_understanding` | Let xAI inspect images attached to matching posts |
| `enable_video_understanding` | Let xAI inspect videos attached to matching posts |

### x_search example

```javascript
await x_search({
  query: "dinner recipes",
  allowed_x_handles: ["nytfood"],
  from_date: "2026-03-01",
});

// Per-post stats: use the exact status URL or status ID when possible
await x_search({
  query: "https://x.com/huntharo/status/1905678901234567890",
});
```

**Source**: OpenClaw documentation — `tools/web` (mirror `inbox/openclaw_docs/tools/web.md`), native-search / network-safety / `x_search` sections
**Last Updated**: 2026-06-22
**Status**: Active
