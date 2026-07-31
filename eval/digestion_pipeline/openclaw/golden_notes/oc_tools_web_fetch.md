---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - web_fetch
keywords:
  - openclaw web_fetch tool
  - web fetch readability extraction
  - tools.web.fetch config
  - firecrawl fallback web fetch
  - usetrustedenvproxy dns pinning
  - web_fetch ssrf policy
  - extractmode markdown text
  - web_fetch caching limits
topics:
  - OpenClaw
  - Web Fetch
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/web-fetch
access_control_group: ["general"]
---

# OpenClaw — The `web_fetch` Tool: HTTP GET + Readability Extraction

## Overview

This note is the procedure for OpenClaw's **`web_fetch`** agent tool, which does a plain HTTP GET and extracts readable content (HTML to markdown or text) — it does **not** execute JavaScript. It mirrors the `tools/web-fetch` source page: how to call the enabled-by-default tool, the `url` / `extractMode` / `maxChars` parameters, the four-step fetch → extract → fallback → cache flow, the pending-fetch progress line, the `tools.web.fetch` config block, the optional Firecrawl fallback (provider selection, auto-detection, sandboxed-vs-non-sandboxed provider rules), trusted-env-proxy mode, the SSRF limits-and-safety policy, and tool-profile allowlisting. For JS-heavy sites or login-protected pages the source directs you to the Web Browser (`/tools/browser`) tool instead.

## Quick start

`web_fetch` is **enabled by default** — no configuration is needed, and the agent can call it immediately. The minimal call passes only the URL:

```javascript
await web_fetch({ url: "https://example.com/article" });
```

## Tool parameters

The tool accepts three parameters, copied verbatim from the source `ParamField` definitions:

- **`url`** (`string`, required) — URL to fetch. `http(s)` only.
- **`extractMode`** (`'markdown' | 'text'`, default `markdown`) — output format after main-content extraction.
- **`maxChars`** (`number`) — truncate output to this many characters.

## How it works

A `web_fetch` call runs through four ordered steps (the source `Steps` block):

1. **Fetch** — sends an HTTP GET with a Chrome-like User-Agent and an `Accept-Language` header, blocks private/internal hostnames, and re-checks redirects.
2. **Extract** — runs Readability (main-content extraction) on the HTML response.
3. **Fallback (optional)** — if Readability fails and Firecrawl is selected, retries through the Firecrawl API with bot-circumvention mode.
4. **Cache** — results are cached for 15 minutes (configurable) to reduce repeated fetches of the same URL.

## Progress updates

`web_fetch` emits a public progress line only when the fetch is still pending after five seconds:

```text
Fetching page content...
```

Fast cache hits and quick network responses finish before the timer fires, so they do not show a progress line; if the call is canceled the timer is cleared. When the fetch eventually completes the agent receives the normal tool result — the progress line is only channel UI state and never contains fetched page content.

## Config

The `tools.web.fetch` config block (verbatim from source, with the inline default comments) controls enablement, provider, size/output caps, timeouts, caching, redirects, the trusted-env-proxy toggle, Readability, User-Agent override, and the SSRF policy opt-ins:

```json5
{
  tools: {
    web: {
      fetch: {
        enabled: true, // default: true
        provider: "firecrawl", // optional; omit for auto-detect
        maxChars: 50000, // max output chars
        maxCharsCap: 50000, // hard cap for maxChars param
        maxResponseBytes: 2000000, // max download size before truncation
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        maxRedirects: 3,
        useTrustedEnvProxy: false, // let a trusted HTTP(S) env proxy resolve DNS
        readability: true, // use Readability extraction
        userAgent: "Mozilla/5.0 ...", // override User-Agent
        ssrfPolicy: {
          allowRfc2544BenchmarkRange: true, // opt-in for trusted fake-IP proxies using 198.18.0.0/15
          allowIpv6UniqueLocalRange: true, // opt-in for trusted fake-IP proxies using fc00::/7
        },
      },
    },
  },
}
```

## Firecrawl fallback

If Readability extraction fails, `web_fetch` can fall back to Firecrawl (`/tools/firecrawl`) for bot-circumvention and better extraction. Configuration sets `tools.web.fetch.provider` (optional; omit for auto-detect from available credentials) and the Firecrawl plugin under `plugins.entries.firecrawl`:

```json5
{
  tools: {
    web: {
      fetch: {
        provider: "firecrawl", // optional; omit for auto-detect from available credentials
      },
    },
  },
  plugins: {
    entries: {
      firecrawl: {
        enabled: true,
        config: {
          webFetch: {
            // apiKey: "fc-...", // optional; omit for keyless starter access
            baseUrl: "https://api.firecrawl.dev",
            onlyMainContent: true,
            maxAgeMs: 86400000, // cache duration (1 day)
            timeoutSeconds: 60,
          },
        },
      },
    },
  },
}
```

`plugins.entries.firecrawl.config.webFetch.apiKey` is optional and supports SecretRef objects; legacy `tools.web.fetch.firecrawl.*` config is auto-migrated by `openclaw doctor --fix`. If you configure a Firecrawl API-key SecretRef and it is unresolved with no `FIRECRAWL_API_KEY` env fallback, gateway startup fails fast. Firecrawl `baseUrl` overrides are locked down: hosted traffic uses `https://api.firecrawl.dev`; self-hosted overrides must target private or internal endpoints, and `http://` is accepted only for those private targets.

The source states the current runtime behavior of provider selection and the sandbox boundary:

- `tools.web.fetch.provider` selects the fetch fallback provider explicitly.
- If `provider` is omitted, OpenClaw auto-detects the first ready web-fetch provider from configured credentials. Non-sandboxed `web_fetch` can use installed plugins that declare `contracts.webFetchProviders` and register a matching provider at runtime; the official Firecrawl plugin provides this fallback.
- Sandboxed `web_fetch` calls allow bundled providers plus installed providers whose official npm or ClawHub provenance is verified — today that permits the official Firecrawl plugin, while third-party external fetch plugins stay excluded.
- If Readability is disabled, `web_fetch` skips straight to the selected provider fallback; if no provider is available, it fails closed.

## Trusted env proxy

If your deployment requires `web_fetch` to go through a trusted outbound HTTP(S) proxy, set `tools.web.fetch.useTrustedEnvProxy: true`. In this mode OpenClaw still applies hostname-based SSRF checks before sending the request, but it lets the proxy resolve DNS instead of doing local DNS pinning — enable this only when the proxy is operator-controlled and enforces outbound policy after DNS resolution. If no HTTP(S) proxy env var is configured, or the target host is excluded by `NO_PROXY`, `web_fetch` falls back to the normal strict path with local DNS pinning.

## Limits and safety

The source enumerates the limits-and-safety guarantees:

- `maxChars` is clamped to `tools.web.fetch.maxCharsCap`.
- Response body is capped at `maxResponseBytes` before parsing; oversized responses are truncated with a warning.
- Private/internal hostnames are blocked.
- `tools.web.fetch.ssrfPolicy.allowRfc2544BenchmarkRange` and `tools.web.fetch.ssrfPolicy.allowIpv6UniqueLocalRange` are narrow opt-ins for trusted fake-IP proxy stacks; leave them unset unless your proxy owns those synthetic ranges and enforces its own destination policy.
- Redirects are checked and limited by `maxRedirects`.
- `useTrustedEnvProxy` is an explicit opt-in and should only be enabled for operator-controlled proxies that still enforce outbound policy after DNS resolution.
- `web_fetch` is best-effort — some sites need the Web Browser (`/tools/browser`).

## Tool profiles

If you use tool profiles or allowlists, add `web_fetch` or `group:web` (the `group:web` allowlist includes `web_fetch`, `web_search`, and `x_search`):

```json5
{
  tools: {
    allow: ["web_fetch"],
    // or: allow: ["group:web"]  (includes web_fetch, web_search, and x_search)
  },
}
```

**Source**: OpenClaw documentation — `tools/web-fetch` (mirror `inbox/openclaw_docs/tools/web-fetch.md`)
**Last Updated**: 2026-06-22
**Status**: Active
