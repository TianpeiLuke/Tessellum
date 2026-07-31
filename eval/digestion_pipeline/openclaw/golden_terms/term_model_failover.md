---
tags:
  - resource
  - terminology
  - openclaw
  - model-failover
  - llm-reliability
  - cooldown-probe
keywords:
  - Model Failover
  - LLM fallback ladder
  - cooldown probe
  - FailoverError
  - transient-vs-permanent error
  - provider rotation
topics:
  - LLM reliability
  - Failover patterns
  - OpenClaw architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://docs.openclaw.ai/concepts/model-failover
access_control_group: ["general"]
---

# Model Failover

## Definition

**Model Failover** is the LLM-specific flavor of failover: the runtime mechanism by which an agent that just received a non-fatal error from a primary `(provider, model)` pair attempts the same request against the next pair in an ordered fallback ladder, repeating until one succeeds or the ladder is exhausted. It differs from the [general failover concept](term_failover.md) in three material ways — (1) the unit of failover is a logical model identity, not a host or process; (2) "failure" is not binary, since rate-limit (HTTP 429), context-overflow, auth-permanent, billing, and transient-network errors each demand different rotation rules; and (3) the decision to walk down is coupled to a **cooldown probe** that periodically retries the primary instead of permanently demoting it.

OpenClaw's `src/agents/model-fallback.ts` (≈1,290 LOC) implements a three-way-split design: a **failover ladder** entry that classifies abort-vs-failover and dedups candidates, a **cooldown probe** layer that decides skip / attempt / suspend per provider using a per-key probe-attempt map with TTL pruning and LRU cap, and a **transient-cooldown + observation** tail that preserves probe slots on non-candidate failures and emits decision-log events via `onFallbackStep`. Errors flow through a typed `FailoverError` envelope (closed-enum `FailoverReason`, optional HTTP status, suspend flag) that is coerced from raw provider exceptions before any rotation decision is taken.

## Context

Model failover is the standard reliability pattern for LLM gateway / router products. **LiteLLM** Router maintains an in-order fallback list and applies a fixed cooldown (default ≈60s, configurable via `cooldown_time`) once a deployment exceeds `allowed_fails` within a minute; **OpenRouter** and **Portkey** offer the same primitive with transparent provider rotation; **Bifrost**, **agentgateway**, and similar gateways trigger on HTTP 429 / 5xx and respect the `Retry-After` header from upstream responses. OpenClaw uses model failover inside its agent runtime: whenever the agent loop dispatches an inference call and the primary returns a `FailoverError` (rate-limit, transient network, billing, or auth-revoked), the runtime walks an effective fallback chain that is either configured per agent or rotated via an override-vs-config IIFE.

What distinguishes OpenClaw from LiteLLM-style chains is the **cooldown-probe slot**: instead of a flat "model X is cooling down for N seconds" rule, the runtime maintains a `lastProbeAttempt` map and lets at most one in-flight call per provider per throttle window re-test the primary — so a rate-limited provider does not stay demoted past its actual recovery point, but also does not get hammered concurrently by every session. The runtime also distinguishes **persistent** (auth, auth_permanent) from **transient** (billing-soft, network, timeout) reasons and routes them to different verdicts (`skip` / `attempt` / `suspend_lanes`) via the `resolveCooldownDecision` router.

## Key Characteristics

- **Abort-vs-failover discrimination**: `shouldRethrowAbort` rethrows genuine `AbortError` (user cancel) immediately, never walking the ladder; only `FailoverError`-coerced exceptions trigger rotation.
- **Typed `FailoverError` envelope**: closed-enum `FailoverReason`, optional `status` / `code` / `provider` / `model` / `profileId` / `lane` / `suspend`; raw provider errors are coerced via `coerceToFailoverError` before any rotation logic.
- **Candidate collector closure**: `createModelCandidateCollector` dedups `(provider, model)` pairs and gates allowlist entries — the ladder is built once per call, not mutated mid-iteration.
- **Per-candidate try-wrapper**: `runFallbackCandidate` isolates each attempt; failures are pushed to a `FallbackAttempt[]` array via `recordFailedCandidateAttempt` for the terminal envelope.
- **Cooldown-probe slot logic**: `lastProbeAttempt` map (TTL-pruned + LRU-capped) records the most recent probe per provider key; `isProbeThrottleOpen` and `shouldProbePrimaryDuringCooldown` reserve at most one probe per throttle window.
- **Image-fallback pool**: `resolveImageFallbackCandidates` collects primary + configured image fallbacks separately, since image-capable models have a narrower candidate set than text-only ones.
- **Override-vs-config rotation IIFE**: the effective fallback chain is selected at call-site by an IIFE that prefers `runOptions.fallbacks` (caller override) over `config.fallbacks` (agent default).
- **`CooldownDecision` router**: turns `(reason, primary_or_not, probe_slot_available)` into one of `{skip, attempt, suspend_lanes}`; auth / auth_permanent always `skip`, billing routes to `attempt + probe` or `suspend_lanes`.
- **Transient-cooldown preservation**: `shouldPreserveTransientCooldownProbeSlot` returns the probe slot to the pool when a failure was not the candidate's fault (e.g., user abort during probe), so the next caller can re-try.
- **Fire-on-step observation hooks**: `onFallbackStep` callback gates decision-log emission; success-path observation only fires on **non-trivial** paths (`i > 0` or non-empty attempts or `attemptedDuringCooldown`).
- **`FallbackSummaryError` terminal envelope**: when the ladder is exhausted, carries `attempts[]` + `soonestCooldownExpiry` + session attribution; collapses to a single `rethrow` when only one attempt was made (avoids wrapping a real error in a useless summary).
- **Per-provider, not per-model, cooldown**: a 429 from `anthropic/claude-sonnet-4` cools down all `anthropic/*` lanes until the probe slot reopens — provider-level rate limits are the dominant failure mode.

## Related Terms


### Related Code Snippets

- **[snippet_openclaw_agents_model_fallback_ladder](../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md)**: failover ladder entry, abort discrimination, and `FallbackSummaryError` envelope (L1-L450).
- **[snippet_openclaw_agents_model_fallback_cooldown](../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md)**: cooldown-probe slot logic, image-fallback pool, override-vs-config rotation, and `CooldownDecision` router (L432-L831).
- **[snippet_openclaw_agents_model_fallback_observation](../code_snippets/snippet_openclaw_agents_model_fallback_observation.md)**: transient-cooldown preservation, observation hooks, and terminal summary writer (L832-L1290).
- **[snippet_openclaw_agents_failover_error](../code_snippets/snippet_openclaw_agents_failover_error.md)**: typed `FailoverError` class, signal classifier, and `coerceToFailoverError` consumed by the ladder.

## References

- [Failover (Wikipedia)](https://en.wikipedia.org/wiki/Failover)
- [Circuit Breaker Design Pattern (Wikipedia)](https://en.wikipedia.org/wiki/Circuit_breaker_design_pattern)
- [LiteLLM Reliability — Fallbacks and Cooldown](https://docs.litellm.ai/docs/proxy/reliability)
- [OpenAI Cookbook — How to handle rate limits (exponential backoff)](https://cookbook.openai.com/examples/how_to_handle_rate_limits)
- [Portkey — Retries, Fallbacks, and Circuit Breakers in LLM apps](https://portkey.ai/blog/retries-fallbacks-and-circuit-breakers-in-llm-apps/)
- [OpenClaw Docs — Model failover](https://docs.openclaw.ai/concepts/model-failover)
- [OpenClaw source — src/agents/model-fallback.ts](https://github.com/openclaw/openclaw/blob/main/src/agents/model-fallback.ts)
