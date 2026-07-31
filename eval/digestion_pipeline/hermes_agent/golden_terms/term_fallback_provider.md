---
tags:
  - resource
  - terminology
  - llm_infrastructure
  - llm-reliability
  - failover
keywords:
  - Fallback Provider
  - fallback_providers
  - fallback_model
  - cross-provider failover
  - primary model fallback
  - auxiliary task fallback
  - provider failover chain
topics:
  - LLM reliability
  - Provider resilience
  - Failover patterns
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Fallback Provider

## Definition

A **fallback provider** is a backup `(provider, model)` pair that an LLM agent runtime automatically switches to when its primary model fails, so that an in-flight conversation can continue against a different upstream instead of erroring out. It is the cross-provider layer of a multi-layer resilience stack: where [credential pools](term_credential_pool.md) rotate across multiple keys for the *same* provider, fallback providers fail over to a *different* provider entirely (e.g. from Anthropic native to OpenRouter, or from OpenRouter to Nous Portal). The term denotes both the configured backup entry and the mechanism that selects it.

In Hermes Agent the construct is configured as a top-level `fallback_providers:` list in `~/.hermes/config.yaml` (each entry requiring a `provider` and a `model`), or interactively via `hermes fallback`. The legacy singular `fallback_model` key is still honored for back-compat and migrated on write, with `fallback_providers` taking priority when both are set. Conceptually a fallback provider is the LLM-infrastructure realization of the classical [failover](term_failover.md) pattern — automatic switchover to a redundant component to preserve service continuity.

## Context

Fallback providers are a standard primitive of LLM gateway / router products: OpenRouter rotates across underlying providers, LiteLLM Router maintains an ordered fallback list with per-deployment cooldowns, and Portkey / Bifrost offer the same primitive triggered on HTTP 429 / 5xx. Within the Hermes provider-resilience stack the three layers are tried in order — same-provider credential-pool rotation first, then cross-provider fallback, then per-task auxiliary fallback for side jobs like vision, compression, and web extraction. Fallback differs from [provider routing](term_provider_routing.md) (OpenRouter sub-provider selection *within* one provider's catalog) in that it crosses provider boundaries.

The mechanism is invoked from the agent's main conversation loop: when the primary model raises a qualifying error, the runtime resolves credentials for the fallback, builds a new API client, swaps model/provider/client in place, resets the retry counter, and continues — preserving conversation history, tool calls, and context. Fallback also propagates into [subagent](term_subagent.md) delegation (children inherit the parent chain) and cron jobs, and auxiliary tasks on `provider: auto` walk the same chain before the built-in discovery chain. It is configured exclusively through `config.yaml` / `hermes fallback` (deliberately no environment-variable override).

## Key Characteristics

- **Cross-provider, not same-provider**: fails over to a *different* provider:model pair; same-provider key rotation is handled one layer below by credential pools.
- **Per-turn, not per-session (turn-scoped)**: each new user message restarts with the primary model restored; fallback activates for the failing turn only, at most once per turn — preventing cascading failover loops while giving the primary a fresh chance every turn.
- **Error-class triggered**: activates on rate limits (HTTP 429) and server errors (HTTP 500/502/503) *after exhausting retries*; on auth failures (401/403) and not-found (404) *immediately* (no point retrying); and on repeated malformed/empty responses.
- **Seamless in-place swap**: resolves fallback credentials → builds a new client → swaps model/provider/client → resets the retry counter, all while preserving conversation history and context.
- **Ordered, multi-entry chain**: `fallback_providers` is a list tried in order; the legacy `fallback_model` (singular) is migrated and superseded when both exist.
- **Custom-endpoint support**: a `provider: custom` entry with `base_url` + `key_env` fails over to any OpenAI-compatible endpoint, including local models.
- **Auxiliary-task fallback is independent**: side tasks (vision, web-extract, compression, skills-hub, MCP, approval, title-gen) each have their own provider chain; on `provider: auto` they try main model → `auxiliary.<task>.fallback_chain` → top-level `fallback_providers` → built-in discovery chain.
- **Capacity-error ladder for explicit aux providers**: HTTP 402 / daily-quota exhaustion / connection failures bypass the explicit-provider gate and walk primary aux → per-task `fallback_chain` → main agent model → warn-and-re-raise; transient 429 rate limits respect the explicit choice and do *not* trigger the ladder.
- **Graceful degradation for compression**: if no provider is available for context compression, the runtime drops middle turns without a summary rather than failing the session — a [graceful-degradation](term_graceful_degradation.md) rather than hard-fail outcome.
- **Inheritance**: subagent delegation and cron agents inherit the configured fallback chain; delegation can additionally override the primary provider:model for cost optimization.

## Related Terms


## References

- [Fallback Providers — Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers)
- [Failover (Wikipedia)](https://en.wikipedia.org/wiki/Failover)
- [High availability (Wikipedia)](https://en.wikipedia.org/wiki/High_availability)
- [LiteLLM — Fallbacks, Retries, and Cooldowns](https://docs.litellm.ai/docs/proxy/reliability)
- [OpenRouter — Provider Routing](https://openrouter.ai/docs/features/provider-routing)

---

**Last Updated**: 2026-06-19
**Status**: Active
