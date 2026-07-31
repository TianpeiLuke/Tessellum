---
tags:
  - resource
  - documentation
  - hermes_agent
  - provider_routing
  - llm_infrastructure
keywords:
  - provider routing
  - openrouter sub-provider selection
  - provider_routing config block
  - sort price throughput latency
  - only ignore order whitelist
  - extra_body.provider mapping
  - provider routing vs fallback
topics:
  - Hermes Agent
  - Provider Routing
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing
access_control_group: ["general"]
---

# Hermes Agent — Provider Routing

## Overview

Provider routing is Hermes Agent's fine-grained control over **which underlying AI providers handle requests, and how they're prioritized, when using OpenRouter as the LLM provider**. OpenRouter routes requests to many providers (e.g., Anthropic, Google, AWS Bedrock, Together AI); provider routing lets the operator optimize for cost, speed, quality, or enforce specific provider requirements via a `provider_routing` block in `~/.hermes/config.yaml`. The preferences map onto OpenRouter's `extra_body.provider` field on every API call. It only applies when using OpenRouter — it has no effect on direct provider connections (e.g., connecting directly to the Anthropic API). For automatic failover to an entirely *different* provider when the primary model fails, see [Fallback Providers](hermes_fallback_providers.md) — a distinct mechanism.

> Traffic routed through the Nous Portal (see SP14 provider catalog) still respects per-model routing and priority configs, and Portal subscribers get 10% off token-billed providers.

## Configuration

Add a `provider_routing` section to `~/.hermes/config.yaml`. The full set of keys (with their defaults and inline meaning) is the canonical block — SP02 owns the config-key catalog reference; this note owns the concept/procedure:

```yaml
provider_routing:
  sort: "price"           # How to rank providers
  only: []                # Whitelist: only use these providers
  ignore: []              # Blacklist: never use these providers
  order: []               # Explicit provider priority order
  require_parameters: false  # Only use providers that support all parameters
  data_collection: null   # Control data collection ("allow" or "deny")
```

Provider routing only applies when using OpenRouter. It has no effect with direct provider connections (e.g., connecting directly to the Anthropic API).

## Options

Each key in the `provider_routing` block controls one aspect of sub-provider selection:

- **`sort`** — controls how OpenRouter ranks available providers for a request:
  - `"price"` — cheapest provider first
  - `"throughput"` — fastest tokens-per-second first
  - `"latency"` — lowest time-to-first-token first
- **`only`** — whitelist of provider names. When set, **only** these providers are used; all others are excluded.
- **`ignore`** — blacklist of provider names. These providers are **never** used, even if they offer the cheapest or fastest option.
- **`order`** — explicit priority order. Providers listed first are preferred; unlisted providers are used as fallbacks.
- **`require_parameters`** — when `true`, OpenRouter only routes to providers that support **all** parameters in the request (like `temperature`, `top_p`, `tools`, etc.). This avoids silent parameter drops.
- **`data_collection`** — controls whether providers can use prompts for training. Options are `"allow"` or `"deny"`.

A representative single-option block (the others follow the same shape):

```yaml
provider_routing:
  order:
    - "Anthropic"
    - "Google"
    - "AWS Bedrock"
```

## Practical Examples

The source pairs each optimization goal with a minimal config:

- **Optimize for Cost** — route to the cheapest available provider (good for high-volume usage and development): `sort: "price"`.
- **Optimize for Speed** — prioritize low-latency providers for interactive use: `sort: "latency"`.
- **Optimize for Throughput** — best for long-form generation where tokens-per-second matters: `sort: "throughput"`.
- **Lock to Specific Providers** — ensure all requests go through a specific provider for consistency via `only`.
- **Avoid Specific Providers** — exclude providers (e.g., for data privacy) via `ignore` combined with `data_collection: "deny"`.
- **Preferred Order with Fallbacks** — try preferred providers first, fall back to others if unavailable.

Options can be combined. For example, sort by price but exclude certain providers and require parameter support:

```yaml
provider_routing:
  sort: "price"
  ignore: ["Together"]
  require_parameters: true
  data_collection: "deny"
```

## How It Works

Provider routing preferences are passed to the OpenRouter API via the `extra_body.provider` field on **every** API call. This applies to both:

- **CLI mode** — configured in `~/.hermes/config.yaml`, loaded at startup
- **Gateway mode** — same config file, loaded when the gateway starts

The routing config is read from `config.yaml` and passed as parameters when creating the `AIAgent`:

```
providers_allowed  ← from provider_routing.only
providers_ignored  ← from provider_routing.ignore
providers_order    ← from provider_routing.order
provider_sort      ← from provider_routing.sort
provider_require_parameters ← from provider_routing.require_parameters
provider_data_collection    ← from provider_routing.data_collection
```

## Default Behavior

When no `provider_routing` section is configured (the default), OpenRouter uses its own default routing logic, which generally balances cost and availability automatically.

## Provider Routing vs. Fallback Models

Provider routing controls which **sub-providers within OpenRouter** handle requests. For automatic failover to an entirely **different** provider when the primary model fails, see [Fallback Providers](hermes_fallback_providers.md). The two layers are complementary: routing picks the best sub-provider inside OpenRouter; fallback switches to a wholly separate provider on failure.

**Source**: `inbox/hermes_agent_docs/user-guide/features/provider-routing.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing
**Last Updated**: 2026-06-19
**Status**: Active
