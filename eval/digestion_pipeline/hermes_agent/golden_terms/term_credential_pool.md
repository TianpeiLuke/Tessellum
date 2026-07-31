---
tags:
  - resource
  - terminology
  - system_design
  - reliability
  - llm_infrastructure
  - authentication
keywords:
  - credential pool
  - credential pools
  - API key pool
  - key rotation
  - same-provider rotation
  - rate limit recovery
  - rotation strategy
topics:
  - LLM serving infrastructure
  - resilience and high availability
  - credential management
  - rate limiting
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Credential Pool

## Definition

A **credential pool** is a managed set of multiple interchangeable credentials (API keys and/or OAuth tokens) registered for the **same** upstream provider, from which a runtime selects one credential per request and automatically **rotates** to the next healthy credential when the current one hits a rate limit, billing quota, or auth-expiry error. It is an application of the general **resource-pooling pattern** (borrow a ready resource from a pool, use it, return it) applied to authentication material: instead of holding a single API key whose per-key rate/billing limits cap throughput, the caller pools several keys and spreads load across them, keeping a session alive without switching to a different provider.

In the LLM-agent context, credential pools are the **same-provider** resilience layer that sits *below* cross-provider failover. The problem it solves is the practical reality that a single API key (e.g. an OpenRouter or Anthropic key) is throttled or billing-capped independently of the underlying model's availability — so the cheapest, lowest-disruption way to survive a `429`/`402` is to swap to a second key on the *same* provider before doing anything more drastic.

## Context

Credential pools appear in the **provider-resilience stack** of LLM-serving agents, commonly structured as three layers tried in order: (1) **credential pool** — same-provider multi-key rotation; (2) [fallback providers](term_failover.md) — switch to a *different* provider entirely; (3) provider routing — sub-provider selection within an aggregator. Pools are tried first, and only when *all* pool keys for a provider are exhausted does the cross-provider `fallback_model` activate.

The concept is structurally analogous to other credential-management infrastructure — e.g. the [AWS SDK credential chain](term_aws_sdk_credential_chain.md) (an ordered lookup over credential *sources*) and Secrets Manager rotation patterns — though a credential pool rotates among *equivalent live credentials for one provider* rather than discovering a single best credential.

## Key Characteristics

- **Same-provider rotation (not failover).** A credential pool rotates keys *within* one provider; it is distinct from cross-provider [model failover](term_model_failover.md), which switches to a different provider entirely. Pools are the first, least-disruptive resilience layer; failover is the last resort once a pool is exhausted.
- **Auto-discovery + 1-key default.** If a single API key is present (e.g. in `.env`), the runtime auto-seeds it as a one-key pool; adding more keys is what unlocks rotation. Auto-seeded entries are re-synced on each pool load (removing an env var prunes its entry); manually added entries are never auto-pruned.
- **Error-class-specific recovery.** The rotation decision flow keys off the upstream HTTP error:
  - `429` (rate limit): retry the *same* key once for a transient blip; a second consecutive `429` rotates to the next key. A plan/usage-limit `429` rotates immediately (a hard cap will not clear on retry). Cooldown ~1 hour.
  - `402` (billing/quota): rotate to the next key immediately; cooldown ~24 hours.
  - `401` (auth expired): try refreshing the [OAuth token](term_oauth_token.md) first (per the RFC 6749 refresh-token grant); rotate only if refresh fails.
  - all keys exhausted: fall through to the configured cross-provider `fallback_model`.
- **Rotation strategies.** Selection policy is configurable per provider: `fill_first` (default — drain one key before moving on), `round_robin` (cycle evenly, like the [Round Robin](term_round_robin.md) load-balancing rule), `least_used` (pick the lowest request count), and `random`.
- **Reference-only secret storage.** Borrowed runtime secrets (env vars, Bitwarden/Vault/keyring/systemd references) are reference-only at the persistence boundary: only metadata persists (source ref, label, status, request count, a non-reversible fingerprint), not the raw key. OAuth/device-code state keeps the durable refresh tokens it needs.
- **Custom-endpoint pools.** OpenAI-compatible custom endpoints (Together.ai, RunPod, local servers) get their own pools keyed by endpoint name, stored under a `custom:` prefix.
- **Thread safety.** A single threading lock guards all pool mutations (`select()`, `mark_exhausted_and_rotate()`, `try_refresh_current()`, `mark_used()`) so the gateway can serve many concurrent sessions safely — the same concern addressed by a [thread binding policy](term_thread_binding_policy.md).
- **Not credential abuse.** A credential pool is a *defensive resilience* mechanism for keys you legitimately own; it is unrelated to credential stuffing (an account-takeover attack that replays stolen credential pairs).

## Related Terms


## References

- [RFC 6749 — The OAuth 2.0 Authorization Framework (§6 Refreshing an Access Token)](https://datatracker.ietf.org/doc/html/rfc6749#section-6) — the refresh-token grant the pool uses on a `401` before rotating an OAuth credential.
- [RFC 9110 — HTTP Semantics (§15.5.31 429 / §15.5.3 402)](https://datatracker.ietf.org/doc/html/rfc9110) — the `429 Too Many Requests` and `402 Payment Required` status semantics that drive per-error rotation.
- [Connection pool — Wikipedia](https://en.wikipedia.org/wiki/Connection_pool) — the general borrow/use/return resource-pooling pattern that credential pooling specializes for authentication material.

---

**Last Updated**: 2026-06-19
**Status**: Active
