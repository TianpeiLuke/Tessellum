---
tags:
  - resource
  - terminology
  - system_design
  - security
  - api_design
keywords:
  - Rate Limiting
  - throttling
  - token bucket
  - leaky bucket
  - sliding window
  - fixed window
  - API protection
  - DDoS prevention
topics:
  - System Design
  - API Design
  - Security
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: Rate Limiting

## Definition

**Rate Limiting** is a system design technique that controls the number of requests a client can make to a service within a specified time window. When a client exceeds the allowed threshold, subsequent requests are rejected -- typically with an **HTTP 429 (Too Many Requests)** response -- until the window resets or sufficient capacity is restored. Rate limiting serves three primary purposes: (1) **API protection** -- preventing any single client from monopolizing server resources, (2) **fair usage enforcement** -- ensuring equitable access across all consumers, and (3) **DDoS prevention** -- mitigating denial-of-service attacks by capping inbound request volume at the edge. Rate limiters are commonly deployed at the API gateway layer so that blocked requests never reach application servers or databases, reducing backend load and improving overall system resilience.

## Context

Rate limiting is a foundational building block in modern distributed systems. Every major cloud provider (AWS API Gateway, GCP Apigee, Azure API Management) and open-source gateway (NGINX, Kong, Apache APISIX, Envoy) ships with built-in rate limiting capabilities. In abuse prevention contexts, rate limiting acts as a first line of defense: it throttles automated scripts, credential-stuffing bots, and scraping operations before deeper fraud-detection layers even engage. When combined with authentication and authorization, rate limiting enables tiered access models (free tier vs. premium tier) where different API consumers receive different throughput quotas.

### Where Rate Limiting Lives in the Stack

```
Client Request
     │
     ▼
┌──────────────┐   HTTP 429 if exceeded
│  API Gateway  │──────────────────────►  Client
│  (Rate        │
│   Limiter)    │
│              │   Pass if within limit
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Application  │
│  Server       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Database /   │
│  Backend      │
└──────────────┘
```

## Key Characteristics

### Rate Limiting Algorithms

| Algorithm | How It Works | Burst Handling | Memory Usage | Accuracy |
|-----------|-------------|----------------|-------------|----------|
| **Token Bucket** | Bucket holds tokens refilled at a fixed rate; each request consumes one token; rejected when empty | Allows bursts up to bucket capacity | Low (counter + timestamp per key) | Good -- smooths over time |
| **Leaky Bucket** | Requests enter a FIFO queue that drains at a constant rate; overflow is rejected | No bursts -- enforces constant output rate | Low (queue pointer + counter) | High -- strict uniform rate |
| **Fixed Window** | Counts requests in discrete time windows (e.g., per minute); resets at window boundary | Boundary problem: 2x burst at window edges | Very low (single counter) | Low -- edge-case spikes |
| **Sliding Window Log** | Stores timestamp of every request; counts entries within the sliding window | Smooth -- no boundary problem | High (one entry per request) | Very high -- exact count |
| **Sliding Window Counter** | Combines fixed window counts with weighted overlap from the previous window | Good balance -- smooths boundary | Low (two counters + timestamp) | Good -- approximation |

### Algorithm Deep Dives

#### Token Bucket

```
Configuration: bucket_size = 10, refill_rate = 2 tokens/sec

Time 0s:   Bucket = 10 tokens
Request 1: Bucket = 9  ✓ Allow
Request 2: Bucket = 8  ✓ Allow
  ...burst of 10 requests...
Request 10: Bucket = 0  ✓ Allow
Request 11: Bucket = 0  ✗ Reject (HTTP 429)
Time 1s:   Bucket = 2  (refilled)
Request 12: Bucket = 1  ✓ Allow
```

**Best for**: Most API rate limiting. Allows short bursts (accommodating bursty traffic patterns) while enforcing an average rate over time. Used by AWS, Stripe, and most major API providers.

#### Leaky Bucket

```
Configuration: queue_size = 5, drain_rate = 1 req/sec

Incoming:  [R1] [R2] [R3] [R4] [R5] [R6]
Queue:     [R1, R2, R3, R4, R5]  R6 → REJECTED (overflow)
Output:    R1 ──► R2 ──► R3 ──► R4 ──► R5  (1 per second)
```

**Best for**: Shaping outbound or downstream traffic to a constant rate. Ideal when the downstream dependency requires a steady, predictable load (e.g., writing to a rate-limited third-party API).

#### Fixed Window vs. Sliding Window

```
Fixed Window (limit = 100/min):
  ┌─────────────────────────────────────────────────┐
  │  Window 1 (00:00-01:00)  │  Window 2 (01:00-02:00)  │
  │  ...50 requests at 0:59  │  50 requests at 1:01...   │
  └─────────────────────────────────────────────────┘
  Problem: 100 requests in 2 seconds at boundary = 2x intended rate

Sliding Window Counter (limit = 100/min):
  At time 01:15 (25% into current window):
  Effective count = (prev_window_count × 0.75) + current_window_count
  Smooths the boundary spike with weighted approximation
```

### HTTP Response Headers

When implementing rate limiting, standard HTTP headers communicate limit state to clients:

| Header | Purpose | Example |
|--------|---------|---------|
| `X-RateLimit-Limit` | Maximum requests allowed in the window | `X-RateLimit-Limit: 1000` |
| `X-RateLimit-Remaining` | Requests remaining in the current window | `X-RateLimit-Remaining: 742` |
| `X-RateLimit-Reset` | Unix timestamp when the window resets | `X-RateLimit-Reset: 1713571200` |
| `Retry-After` | Seconds to wait before retrying (on 429) | `Retry-After: 30` |

### Rate Limiting Dimensions

Rate limits can be applied across multiple dimensions:

| Dimension | Description | Use Case |
|-----------|-------------|----------|
| **Per user / API key** | Each authenticated user gets their own quota | Standard API access control |
| **Per IP address** | Limits by source IP | Unauthenticated endpoints, DDoS mitigation |
| **Per endpoint** | Different limits for different API paths | Expensive endpoints (search, reports) get lower limits |
| **Per service tier** | Free, basic, premium get different quotas | SaaS pricing models |
| **Global** | Total system-wide request cap | Protecting backend capacity |

### Distributed Rate Limiting Challenges

In distributed deployments (multiple API gateway instances), rate limiting introduces coordination challenges:

```
                    ┌──────────────┐
Client A ──────────►│  Gateway 1   │──┐
                    └──────────────┘  │    ┌─────────────────────┐
                                      ├───►│  Shared State       │
                    ┌──────────────┐  │    │  (Redis / Memcached)│
Client B ──────────►│  Gateway 2   │──┘    └─────────────────────┘
                    └──────────────┘
```

| Challenge | Description | Mitigation |
|-----------|-------------|------------|
| **Consistency** | Multiple nodes must agree on current count | Centralized store (Redis) with atomic operations (INCR + EXPIRE) |
| **Latency** | Every request requires a round-trip to shared state | Local caching with periodic sync; accept slight over-limit |
| **Single point of failure** | Redis outage disables all rate limiting | Fail-open policy (allow requests) or fail-closed (reject all); Redis Cluster for HA |
| **Race conditions** | Concurrent requests may read stale counts | Lua scripts for atomic read-check-increment in Redis |
| **Clock skew** | Nodes with different clocks disagree on windows | Use centralized timestamp from Redis; NTP synchronization |
| **Scalability ceiling** | Single Redis handles ~100K-200K ops/sec | Shard by user/key across Redis Cluster nodes |

### Client-Side Best Practices

When consuming rate-limited APIs, clients should implement:

1. **Exponential backoff with jitter** -- On receiving 429, wait `min(base * 2^attempt + random_jitter, max_delay)` before retrying
2. **Respect Retry-After headers** -- Always honor the server's suggested wait time
3. **Proactive throttling** -- Track `X-RateLimit-Remaining` and slow down before hitting the limit
4. **Request batching** -- Combine multiple operations into fewer API calls where possible
5. **Circuit breaking** -- Stop retrying after a maximum number of attempts to avoid thundering herd

## Related Terms

### System Design and Architecture
- **[Term: Event-Driven Architecture](term_event_driven_architecture.md)** -- Asynchronous event-driven patterns reduce synchronous request pressure; rate limiting protects synchronous API endpoints that EDA replaces with async flows
- **[Term: Microservices Architecture](term_microservices_architecture.md)** -- Rate limiting is essential in microservices to prevent cascading failures when one service overwhelms another
- **[Term: Hexagonal Architecture](term_hexagonal_architecture.md)** -- Rate limiter can be implemented as an adapter at the port layer, keeping business logic decoupled from throttling concerns
- **[Term: CAP Theorem](term_cap_theorem.md)** -- Distributed rate limiters face CAP trade-offs: strong consistency across nodes vs. availability when the shared state store is partitioned
- **[Term: SLA (Service Level Agreement)](term_sla.md)** -- Rate limits are often codified in SLAs; exceeding them triggers 429 responses as contractual enforcement

### Design Patterns
- **[Term: Proxy Pattern](term_proxy_pattern.md)** -- Rate limiter commonly implemented as a proxy or decorator that intercepts requests before forwarding to the real service
- **[Term: Strategy Pattern](term_strategy_pattern.md)** -- Different rate limiting algorithms (token bucket, sliding window) can be swapped via the strategy pattern at runtime
- **[Term: Deep Modules](term_deep_modules.md)** -- A well-designed rate limiter is a deep module: simple interface (allow/deny) hiding complex algorithm, distributed state, and configuration logic

### Data Structures and Caching
- **[Term: LRU Cache](term_lru_cache.md)** -- LRU eviction strategies apply to rate limiter state management; least-recently-seen keys can be evicted to bound memory usage
- **[Term: Observability in Agent Systems](term_observability_agent_systems.md)** -- Rate limiter metrics (rejection rate, 429 count, latency percentiles) are critical observability signals for system health

### API Infrastructure
- **[API Gateway](term_api_gateway.md)**: API Gateways are the primary deployment layer for rate limiters, enforcing request quotas at the edge before traffic reaches backend services

### Infrastructure
- **[GraphQL](term_graphql.md)**: GraphQL's single-endpoint design requires rate limiting strategies based on query complexity scoring and depth limiting rather than simple per-endpoint request counting
- **[NGINX](term_nginx.md)**: NGINX is commonly used to implement rate limiting at the reverse proxy layer via the `limit_req` module before requests reach application servers

### Abuse Prevention
- **[Term: Blocklist](term_blocklist.md)** -- Rate limiting is a soft enforcement mechanism; blocklisting is the hard enforcement counterpart for known-bad actors
- **[Term: Safelist](term_safelist.md)** -- Safelisted clients may bypass rate limits entirely, representing the opposite enforcement pole
- **[Term: Abuse Polygraph](term_abuse_polygraph.md)** -- Rate limiting feeds behavioral signals (request frequency, burst patterns) into abuse detection models
- **[Redis](term_redis.md)**: Redis is the most common shared state store for distributed rate limiters -- atomic INCR + EXPIRE commands and Lua scripting enable accurate, low-latency rate limit enforcement across multiple gateway instances
- **[Graceful Degradation](term_graceful_degradation.md)**: Rate limiting is a form of graceful degradation -- load shedding rejects a percentage of requests to protect the system from overload, preserving core functionality for the remaining traffic
- **[Latency](term_latency.md)**: Rate limiting protects latency for well-behaved clients by throttling excessive requests before they cause congestion
- **[Throughput](term_throughput.md)**: Rate limiting caps per-client throughput to protect overall system capacity and ensure fairness
- **[TPS](term_tps.md)**: Rate limiting caps per-client TPS to protect aggregate system capacity and ensure fairness

## References

### External References
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media. -- Chapter 1 discusses reliability, scalability, and maintainability trade-offs relevant to rate limiting.
- Newman, S. (2021). *Building Microservices*, 2nd ed. O'Reilly Media. -- Covers rate limiting as a resilience pattern in inter-service communication.
- Xu, A. (2020). *System Design Interview*. Byte Code LLC. -- Chapter 4: "Design a Rate Limiter" -- comprehensive walkthrough of algorithms and distributed challenges.
- Google Cloud Architecture Center. "Rate-limiting strategies and techniques." -- https://cloud.google.com/architecture/rate-limiting-strategies-techniques
- IETF RFC 6585 (2012). "Additional HTTP Status Codes" -- Defines HTTP 429 (Too Many Requests). -- https://datatracker.ietf.org/doc/html/rfc6585
- Stripe API Documentation. "Rate limiting." -- https://docs.stripe.com/rate-limits -- Industry-standard implementation reference.

## Summary

| Aspect | Details |
|--------|---------|
| **Type** | System design technique / infrastructure pattern |
| **Core principle** | Control request throughput per client within a time window |
| **Primary purposes** | API protection, fair usage, DDoS prevention |
| **Key algorithms** | Token bucket, leaky bucket, fixed window, sliding window log, sliding window counter |
| **Rejection signal** | HTTP 429 (Too Many Requests) with Retry-After header |
| **Deployment layer** | API gateway / reverse proxy (edge) |
| **Distributed challenge** | Shared state consistency across nodes (Redis, Memcached) |
| **Key trade-off** | Strictness vs. availability -- fail-open allows excess traffic; fail-closed risks blocking legitimate users |

**Key Insight**: Rate limiting is deceptively simple at the single-node level -- a counter and a clock -- but becomes a distributed systems problem at scale. The core tension is between **accuracy** (exact enforcement of limits) and **availability** (not adding latency or failure modes). Token bucket is the pragmatic default for most APIs because it accommodates bursty traffic while enforcing average rates. The architectural decision of where to place the rate limiter (edge gateway vs. application middleware vs. per-service) determines the blast radius of both enforcement and failure. In abuse prevention, rate limiting is the first, fastest, and cheapest defense layer: it stops volumetric attacks before they reach the expensive fraud-detection pipeline, but it cannot distinguish between a legitimate power user and a sophisticated attacker -- that distinction requires the deeper behavioral analysis that downstream abuse-detection systems provide.

---

**Last Updated**: April 19, 2026
**Status**: Active -- foundational system design concept for API protection, scalability, and abuse prevention
