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

## Related Notes

**Terms**
- [term_model_router](../../term_dictionary/term_model_router.md) — routes requests across models/providers; relevance: provider routing is exactly OpenRouter sub-provider selection.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider adapter pattern; relevance: routing config flows through the provider adapter to `extra_body.provider`.
- [term_load_balancer](../../term_dictionary/term_load_balancer.md) — distributes load by policy; relevance: `sort: price/throughput/latency` ranks sub-providers like a policy-driven balancer.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: routing picks which provider serves the LLM request.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — model/provider inventory; relevance: `only`/`ignore`/`order` whitelist against the OpenRouter provider catalog.
- [term_failover](../../term_dictionary/term_failover.md) — switch on failure; relevance: §Provider Routing vs Fallback contrasts sub-provider routing with cross-provider failover.
- [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — throttle handling; relevance: throughput/latency sort and `order` fallbacks mitigate provider rate caps.
- [term_haproxy](../../term_dictionary/term_haproxy.md) — load-balancer exemplar; relevance: concrete analogue of priority-order + health-aware routing.
- (+ [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md); +Phase 0: [term_provider_routing](../../term_dictionary/term_provider_routing.md) — the OpenRouter sub-provider-selection concept this note documents; +fin: term_nous_portal, term_openrouter)

**Code-Repos**
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider registry/dispatch; relevance: implements mapping `provider_routing.*` → `extra_body.provider` on every OpenRouter call.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `AIAgent` construction; relevance: routing params (`providers_allowed`/`providers_order`/`provider_sort`) are passed when creating the agent.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — config load; relevance: `~/.hermes/config.yaml` `provider_routing:` loaded at CLI/gateway startup.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway-mode load; relevance: same routing config applied when the gateway starts.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties routing into the provider boot path.

**Snippets**
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: where `provider_routing:` config is read and attached to provider construction.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: dispatches to the OpenRouter adapter carrying routing params.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base interface; relevance: the adapter contract that maps routing → request body.
- [snippet_hermes_agent_core_anthropic_adapter_client](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_client.md) — adapter client construction; relevance: pattern for passing provider-selection params at client build.
- [snippet_hermes_agent_gw_runner_provider_boot](../../code_snippets/snippet_hermes_agent_gw_runner_provider_boot.md) — gateway provider boot; relevance: same routing config applied when the gateway starts.
- [snippet_hermes_agent_core_runtime_helpers_switch_client](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_switch_client.md) — client switch; relevance: rebuilds the client with routing options on provider change.
- [snippet_hermes_agent_cli_main_provider_flows](../../code_snippets/snippet_hermes_agent_cli_main_provider_flows.md) — CLI provider flows; relevance: `~/.hermes/config.yaml` provider/routing load at CLI startup.
- [snippet_hermes_agent_core_auxiliary_proxy_url](../../code_snippets/snippet_hermes_agent_core_auxiliary_proxy_url.md) — proxy/base-url resolution; relevance: provider base-URL/endpoint resolution underneath routing.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter provider plugin; relevance: implements the `extra_body.provider` mapping (`sort`/`only`/`ignore`/`order`/`require_parameters`/`data_collection`).
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: registers OpenRouter + the other adapters routing selects among.

**Docs**
- [hermes_fallback_providers](hermes_fallback_providers.md) — cross-provider failover; relevance: the explicit "routing vs fallback" contrast (+fin).
- [hermes_credential_pools](hermes_credential_pools.md) — same-provider rotation; relevance: third resilience layer below routing/fallback (+fin).
- [hermes_config_files_precedence](hermes_config_files_precedence.md) — config keys; relevance: SP02 owns the `provider_routing:` key catalog (+fin).
- [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md) — model/provider config; relevance: routing sits in the same provider-config arc (+fin).
- [hermes_subscription_proxy](hermes_subscription_proxy.md) — Portal routing note; relevance: Portal traffic still respects per-model routing (+fin).
- [cc_model_selection](../claude_code/cc_model_selection.md) — model selection; relevance: analogous "pick which model/provider" control.
- [cc_restrict_model_selection](../claude_code/cc_restrict_model_selection.md) — model allowlist; relevance: analogous to `only`/`ignore` whitelisting.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — LLM gateway routing; relevance: analogous provider-routing layer.
- [cc_llm_gateway_litellm](../claude_code/cc_llm_gateway_litellm.md) — LiteLLM multi-provider; relevance: direct analogue of multi-provider routing config.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — gateway config; relevance: analogous provider-routing-through-a-gateway setup.
- **[OpenClaw — Per-Agent Overrides and Multi-Agent Routing Config](../openclaw/oc_gateway_config_agents_routing.md)** — This note is the procedure reference for configuring **per-agent overrides** (`agents.list[]`) and **multi-agent routing** (`bindings`) on the OpenClaw gateway

**Source**: `inbox/hermes_agent_docs/user-guide/features/provider-routing.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing
**Last Updated**: 2026-06-19
**Status**: Active
