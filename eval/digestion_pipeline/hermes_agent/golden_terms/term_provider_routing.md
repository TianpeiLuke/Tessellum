---
tags:
  - resource
  - terminology
  - llm_infrastructure
  - agent_framework
  - routing
keywords:
  - provider routing
  - OpenRouter provider routing
  - extra_body.provider
  - sub-provider selection
  - sort price throughput latency
  - only ignore order
  - require_parameters
  - data_collection
  - Hermes
topics:
  - LLM serving and inference
  - provider selection
  - cost and latency optimization
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Term: Provider Routing

## Definition

**Provider Routing** is the mechanism by which an LLM aggregator — most prominently [OpenRouter](https://openrouter.ai) — selects *which underlying AI provider* (Anthropic, Google, AWS Bedrock, Together AI, DeepInfra, etc.) serves a given model request, and *in what priority order* candidate providers are tried. A single OpenRouter model id (e.g. `anthropic/claude-sonnet-4`) is frequently hosted by several underlying providers at different prices, throughputs, latencies, and parameter-support levels; provider routing is the fine-grained policy layer that lets a caller optimize for cost, speed, quality, data-privacy, or hard provider requirements rather than accepting the aggregator's default balance.

It is a *sub-provider* selection concept — it chooses **among the providers behind one aggregator endpoint**, distinct from cross-provider failover (switching to an entirely different provider/account when the primary fails). In the [Hermes](term_hermes_agent.md) agent, provider routing is expressed as a `provider_routing:` block in `~/.hermes/config.yaml`, which the agent maps onto OpenRouter's `extra_body.provider` request field on every API call. Because it operates only against an aggregator's multi-provider catalog, provider routing has no effect when connecting directly to a single provider's API.

## Context

Provider routing lives in the **LLM serving / inference** layer of agent frameworks and LLM gateways:

- **Hermes agent**: the `provider_routing:` config block (sort / only / ignore / order / require_parameters / data_collection) is read at CLI or gateway startup and passed as `providers_allowed`, `providers_ignored`, `providers_order`, `provider_sort`, `provider_require_parameters`, and `provider_data_collection` parameters when constructing the `AIAgent`. The agent's OpenRouter [provider plugin](term_provider_plugin.md) attaches these as `extra_body.provider` on each outbound request.
- **OpenRouter**: the upstream aggregator that actually performs the ranking and dispatch across 300+ providers, applying the caller's `provider` preferences before selecting a backend.
- **Nous Portal traffic** still respects per-model routing and priority configs.
- It sits ABOVE the other two layers of a resilience stack — cross-provider [fallback providers](term_fallback_provider.md) (failover to a different provider on error) and same-provider credential pools (multi-key rotation). Provider routing decides the *preference order within the aggregator*; the §"Provider Routing vs. Fallback Models" contrast in the source docs makes this distinction explicit.

## Key Characteristics

- **Aggregator-scoped**: only applies when the provider is an aggregator like OpenRouter; no effect on direct single-provider connections (e.g. the native Anthropic API).
- **Ranking policy via `sort`**: `"price"` (cheapest first), `"throughput"` (highest tokens-per-second first), or `"latency"` (lowest time-to-first-token first) — analogous to least-cost / fastest-response strategies in a classic [load balancer](term_load_balancer.md).
- **Whitelist / denylist / explicit order**: `only` restricts to an allowed provider set; `ignore` excludes named providers even if cheapest/fastest; `order` sets an explicit priority sequence (listed providers preferred, unlisted used as fallbacks) — the priority-order strategy of a balancer like [HAProxy](term_haproxy.md).
- **`require_parameters`**: when `true`, routes only to providers that support *all* parameters in the request (`temperature`, `top_p`, `tools`, …), avoiding silent parameter drops.
- **`data_collection`**: `"allow"` or `"deny"` controls whether providers may use prompts for training — a data-privacy guardrail.
- **Composable**: options combine (e.g. sort by price, ignore certain providers, require parameter support, deny data collection).
- **Request-body mechanism**: preferences are serialized to the aggregator's `extra_body.provider` field on every call; the same config is applied identically in CLI mode and gateway mode.
- **Default behavior**: with no `provider_routing` section, OpenRouter applies its own default logic, generally balancing cost and availability automatically.
- **Distinct from failover**: routing controls *sub-providers within one aggregator*; for automatic switchover to an entirely different provider on primary-model failure, see fallback providers / [model failover](term_model_failover.md).

## Related Terms


## References

- [Provider Routing — Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing/)
- [OpenRouter — Provider Routing](https://openrouter.ai/docs/features/provider-routing)
- [Load balancing (computing) — Wikipedia](https://en.wikipedia.org/wiki/Load_balancing_(computing))

---

**Last Updated**: 2026-06-19
**Status**: Active
