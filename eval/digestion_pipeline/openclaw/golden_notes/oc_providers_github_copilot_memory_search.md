---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - memory_search
keywords:
  - github copilot embeddings
  - openclaw memory search provider
  - memorySearch.provider github-copilot
  - copilot embedding model discovery
  - text-embedding-3-small
  - copilot /embeddings endpoint
  - github token embedding exchange
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/github-copilot
access_control_group: ["general"]
---

# OpenClaw — GitHub Copilot as the Memory-Search Embedding Provider

## Overview

This note is the procedure for using a logged-in GitHub Copilot subscription as the embedding provider for OpenClaw **memory search** — no separate API key required. It mirrors the **Memory search embeddings** section of the `providers/github-copilot` source page (its `### Config` and `### How it works` subsections only). The companion note `oc_providers_github_copilot_provider` covers the model-provider/agent-runtime half of the same page (device-login, SDK harness, Copilot Proxy, transport selection); the two share the same GitHub-token-to-Copilot-API token-exchange path. Use this when you want OpenClaw to embed memory-search content through Copilot rather than a dedicated embedding key.

## Memory Search Embeddings

GitHub Copilot can serve as an embedding provider for memory search in addition to its model-provider role. If you have a Copilot subscription and have logged in (via the device-login flow or an environment-variable token — see `oc_providers_github_copilot_provider`), OpenClaw can use it for embeddings **without a separate API key**: it reuses the same GitHub token already resolved for the Copilot provider.

### Config

Set `memorySearch.provider` explicitly to `"github-copilot"` to use GitHub Copilot embeddings. If a GitHub token is available, OpenClaw discovers the available embedding models from the Copilot API and picks the best one automatically. The `model` key is optional — supply it only to override the auto-discovered model:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "github-copilot",
        // Optional: override the auto-discovered model
        model: "text-embedding-3-small",
      },
    },
  },
}
```

The config lives under `agents.defaults.memorySearch` — a distinct config surface from the model-provider setup (`agents.defaults.model`), which is why this is documented as a separate procedure from the provider/runtime note.

### How it works

When `memorySearch.provider` is `"github-copilot"`, OpenClaw runs the following token-exchange-to-`/embeddings` flow:

1. OpenClaw resolves your GitHub token (from env vars or auth profile).
2. Exchanges it for a short-lived Copilot API token.
3. Queries the Copilot `/models` endpoint to discover available embedding models.
4. Picks the best model (prefers `text-embedding-3-small`).
5. Sends embedding requests to the Copilot `/embeddings` endpoint.

The GitHub-token resolution and short-lived-token exchange (steps 1–2) are the same mechanics the Copilot model provider uses, so a single Copilot login covers both the model and embedding surfaces. Model availability depends on your GitHub plan: if no embedding models are available, OpenClaw skips Copilot and tries the next provider — so a Copilot plan without embedding entitlement (or a failed token exchange) falls through gracefully rather than erroring the memory-search path.

**Source**: OpenClaw documentation — `providers/github-copilot` (Memory search embeddings; mirror `inbox/openclaw_docs/providers/github-copilot.md`)
**Last Updated**: 2026-06-22
**Status**: Active
