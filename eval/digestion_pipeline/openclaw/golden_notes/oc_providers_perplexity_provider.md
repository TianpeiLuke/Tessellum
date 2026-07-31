---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - web_search
keywords:
  - openclaw perplexity provider
  - perplexity web search plugin
  - PERPLEXITY_API_KEY OPENROUTER_API_KEY
  - pplx- sk-or- key prefix transport
  - perplexity sonar openrouter
  - native perplexity search api filters
  - openclaw plugins install perplexity
  - daemon env var openclaw .env
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/perplexity-provider
access_control_group: ["general"]
---

# OpenClaw — Configuring the Perplexity Web Search Provider

## Overview

This note is the setup procedure for the OpenClaw **Perplexity provider** — a *web search provider* (not a model provider) that gives the agent web search through the Perplexity Search API or Perplexity Sonar via OpenRouter. It mirrors the `providers/perplexity-provider` source page: install the `@openclaw/perplexity-plugin`, set the API key (`PERPLEXITY_API_KEY` or `OPENROUTER_API_KEY`), let the plugin auto-select the transport by key prefix, optionally apply native-API search filters, and handle the daemon environment-variable caveat. This page documents the **provider** (how OpenClaw connects to Perplexity); how the agent *invokes* searches is the separate Perplexity **tool** page (`tools/perplexity-search`).

## Provider Summary

The header table on the source page fixes three properties of this provider:

| Property | Value |
| --- | --- |
| Type | Web search provider (not a model provider) |
| Auth | `PERPLEXITY_API_KEY` (direct) or `OPENROUTER_API_KEY` (via OpenRouter) |
| Config path | `plugins.entries.perplexity.config.webSearch.apiKey` |

The plugin "provides web search capabilities through the Perplexity Search API or Perplexity Sonar via OpenRouter." The API key (whichever transport) lives at the config path `plugins.entries.perplexity.config.webSearch.apiKey`.

## Install plugin

Install the official plugin, then restart the Gateway so it picks up the plugin:

```bash
openclaw plugins install @openclaw/perplexity-plugin
openclaw gateway restart
```

## Getting started

Setup is two steps on the source page: set the API key, then start searching.

**Step 1 — Set the API key.** Either run the interactive web-search configuration flow, or set the key directly. The interactive flow is `openclaw configure --section web`. To set the key directly:

```bash
openclaw config set plugins.entries.perplexity.config.webSearch.apiKey "pplx-xxxxxxxxxxxx"
```

**Step 2 — Start searching.** Once the key is configured, "the agent will automatically use Perplexity for web searches" — no additional steps are required.

## Search modes

The plugin **auto-selects the transport based on API key prefix** — you do not choose the mode explicitly; it is detected from the key:

- **Native Perplexity API (`pplx-`):** when the key starts with `pplx-`, OpenClaw uses the native Perplexity Search API. This transport returns structured results and supports domain, language, and date filters (see Native API filtering below).
- **OpenRouter / Sonar (`sk-or-`):** when the key starts with `sk-or-`, OpenClaw routes through OpenRouter using the Perplexity Sonar model. This transport returns AI-synthesized answers with citations.

The prefix→transport→features mapping from the source table:

| Key prefix | Transport | Features |
| --- | --- | --- |
| `pplx-` | Native Perplexity Search API | Structured results, domain/language/date filters |
| `sk-or-` | OpenRouter (Sonar) | AI-synthesized answers with citations |

## Native API filtering

Filtering options are **only available when using the native Perplexity API** (`pplx-` key). OpenRouter/Sonar searches do not support these parameters. When using the native Perplexity API, searches support the following filters:

| Filter | Description | Example |
| --- | --- | --- |
| Country | 2-letter country code | `us`, `de`, `jp` |
| Language | ISO 639-1 language code | `en`, `fr`, `zh` |
| Date range | Recency window | `day`, `week`, `month`, `year` |
| Domain filters | Allowlist or denylist (max 20 domains) | `example.com` |
| Content budget | Token limits per response / per page | `max_tokens`, `max_tokens_per_page` |

## Advanced configuration

The source page documents two advanced-configuration accordions.

**Environment variable for daemon processes.** If the OpenClaw Gateway runs as a daemon (launchd/systemd), make sure `PERPLEXITY_API_KEY` is available to that process. A key exported only in an interactive shell will not be visible to a launchd/systemd daemon unless that environment is explicitly imported — set the key in `~/.openclaw/.env` or via `env.shellEnv` to ensure the gateway process can read it.

**OpenRouter proxy setup.** If you prefer to route Perplexity searches through OpenRouter, set an `OPENROUTER_API_KEY` (prefix `sk-or-`) instead of a native Perplexity key. OpenClaw will detect the prefix and switch to the Sonar transport automatically. The source notes this is useful if you already have an OpenRouter account and want consolidated billing across multiple providers.

**Source**: OpenClaw documentation — `providers/perplexity-provider` (mirror `inbox/openclaw_docs/providers/perplexity-provider.md`)
**Last Updated**: 2026-06-22
**Status**: Active
