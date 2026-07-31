---
tags:
  - resource
  - terminology
  - idempotency-key
  - api-design
  - deduplication
  - at-most-once-delivery
keywords:
  - Idempotency key
  - idempotent request
  - dedup token
  - Stripe Idempotency-Key
  - replay protection
topics:
  - API design
  - Distributed systems patterns
  - OpenClaw architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/Idempotence
access_control_group: ["general"]
---

# Idempotency Key

## Definition

An **idempotency key** is a client-generated unique identifier (typically a UUIDv4 or a cryptographic hash) attached to a non-idempotent HTTP request so that the receiving server can detect retries and return the original response instead of re-executing the underlying side effect. The transport layer remains *at-least-once delivery* — networks and load balancers may duplicate any in-flight request — but the key-indexed dedup table on the server upgrades the **effect** to *at-most-once* (and, when paired with a guaranteed-retry client, to effectively *exactly-once* in the application's externally observable state). Stripe popularised the pattern in 2017 with their `Idempotency-Key` HTTP header on every POST and the IETF HTTPAPI working group is now standardising it as [draft-ietf-httpapi-idempotency-key-header](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/).

Mathematically the pattern is the API-design analog of an idempotent operation in algebra: `f(f(x)) = f(x)` ([Wikipedia: Idempotence](https://en.wikipedia.org/wiki/Idempotence)). The server cache makes the *write* idempotent from the client's perspective even when the underlying domain operation (charge a card, mint an instance) is not naturally idempotent. The key must be unique per *logical operation* — re-using it for a different request body is itself an error (AWS returns `IdempotentParameterMismatch`; Stripe returns a fingerprint-mismatch error after API v2).

## Context

The pattern appears across the industry in three distinct shapes. (1) **HTTP header form** — Stripe's `Idempotency-Key`, the IETF draft, and most fintech APIs (Adyen, Shopify, Worldpay) carry the key as a request header and dedup against a server-side cache with a 24-hour to 30-day TTL ([Stripe blog](https://stripe.com/blog/idempotency); [Stripe API reference](https://docs.stripe.com/api/idempotent_requests); [MDN Idempotency-Key](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Idempotency-Key)). (2) **Body-field form** — AWS's `ClientToken` / `ClientRequestToken` is a 36-64 ASCII-character field embedded in the request body for EC2, ECS, EBS, Lambda, EKS, and most control-plane APIs; mismatched parameters on a re-used token return `IdempotentParameterMismatch` ([AWS EC2 docs](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html); [AWS Builders' Library](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)). (3) **Message-broker form** — Kafka's exactly-once semantics use a producer-id + sequence-number tuple as the broker-side dedup key ([Confluent delivery semantics](https://docs.confluent.io/kafka/design/delivery-semantics.html)).

In OpenClaw the pattern surfaces in two production paths. (a) The macOS Canvas A2UI bridge derives an idempotency key on every `userAction` envelope from the in-canvas web view, falling back to a fresh UUID when the caller omits one, and forwards it as `GatewayAgentInvocation.idempotencyKey` so double-clicks and reconnect-driven retries collapse to a single agent run. (b) The voice-call webhook security layer maintains three per-provider replay caches (`twilioReplayCache`, `plivoReplayCache`, `telnyxReplayCache`) keyed by `provider:scope:sha256(signed-material)` with a 10-minute sliding window — a smaller, security-driven instantiation of the same pattern that protects against signature replay rather than client retries.

## Key Characteristics

- **Client-generated** — the client mints the key (UUIDv4 or sha256 digest) so the dedup boundary lives on the client's notion of a single logical operation; server-generated keys cannot deduplicate retries that target a stateless server pool.
- **Server-side TTL cache** — Stripe uses 24h (API v1) / 30d (API v2), AWS uses operation-specific windows up to 24h, OpenClaw uses 10 min for voice webhooks. Cached entries store the full original response (status + body) so the dedup return is byte-identical.
- **At-most-once effect over at-least-once delivery** — the transport keeps retrying; the key turns "executed N times" into "executed once, returned N times". True *exactly-once delivery* across an unreliable network is impossible (a well-known result), but exactly-once *effect* is achievable when both sides cooperate.
- **Per-operation scope** — the key must be unique per logical operation. Re-using it with different parameters is a fingerprint-mismatch error (AWS) or a 400 (Stripe API v2); re-using it with the same parameters is a successful replay.
- **Interaction with retry policies** — works hand-in-glove with exponential backoff and [Circuit Breaker](term_circuit_breaker.md); the client retries safely, the server short-circuits the duplicate.
- **Independent of authentication** — the key is not a credential; it travels alongside the auth header (Bearer token / OAuth / signed request) but does not replace it.

## Related Terms

## Related Code Snippets

- [Canvas A2UI File Watcher + Action Bridge](../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md): Pattern 4 derives the idempotency key on every `userAction` envelope and forwards it as `GatewayAgentInvocation.idempotencyKey`.
- [Voice-Call Webhook Replay Cache](../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md): Patterns 1-3 implement a sha256-keyed sliding-window dedup cache that is structurally identical to a Stripe-style idempotency-key store, scoped to webhook signature replay.

## References
- [Designing robust and predictable APIs with idempotency (Stripe Engineering blog)](https://stripe.com/blog/idempotency)
- [Idempotent requests (Stripe API Reference)](https://docs.stripe.com/api/idempotent_requests)
- [draft-ietf-httpapi-idempotency-key-header — The Idempotency-Key HTTP Header Field (IETF)](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)
- [Idempotence (Wikipedia)](https://en.wikipedia.org/wiki/Idempotence)
- [Idempotency-Key header (MDN Web Docs)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Idempotency-Key)
- [Ensuring idempotency in Amazon EC2 API requests (AWS docs)](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html)
- [Making retries safe with idempotent APIs (AWS Builders' Library)](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)
- [Message Delivery Guarantees for Apache Kafka (Confluent)](https://docs.confluent.io/kafka/design/delivery-semantics.html)
