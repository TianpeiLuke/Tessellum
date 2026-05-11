---
tags:
  - resource
  - terminology
  - system_design
  - caching
  - distributed_systems
keywords:
  - cache stampede
  - thundering herd
  - dog-piling
  - cache avalanche
  - XFetch
  - probabilistic early expiration
  - request coalescing
  - singleflight
  - stale-while-revalidate
  - cache failure mode
topics:
  - System Design
  - Caching Failure Modes
  - Distributed Systems Resilience
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: Cache Stampede (Thundering Herd)

## Definition

A **cache stampede** is a failure scenario in which many requests simultaneously miss the cache -- typically after TTL expiry of a popular key -- causing all of them to hit the backing data store at once. Instead of a single request regenerating the cached value, hundreds or thousands of concurrent requests independently discover the cache miss, bypass the cache, and issue identical expensive queries to the database. The resulting load spike can overwhelm the database, cause cascading latency, and potentially bring down the entire system.

Also known as **thundering herd problem**, **dog-piling**, or **cache avalanche**.

The term "thundering herd" originates from operating systems, where it describes the scenario of many sleeping processes being woken simultaneously by a single event (e.g., a socket becoming readable), only for all but one to find the resource already claimed and go back to sleep -- wasting CPU cycles. In the caching context, the "herd" is the flood of concurrent requests that simultaneously discover an expired or missing cache entry.

## Context

Cache stampede is one of the most dangerous caching failure modes in high-traffic systems. It is paradoxically most severe for the *most popular* data -- the keys with the highest request rates suffer the worst stampedes because more requests arrive during the brief window between TTL expiry and cache repopulation. A homepage cache serving 50,000 RPS that expires can generate 1,000+ simultaneous database queries within 20 milliseconds.

The problem is a direct consequence of the Cache-Aside (lazy loading) pattern, where the application manages cache population on miss. Without explicit coordination, every request that encounters a miss independently attempts to rebuild the cache entry, creating redundant work and database load that scales with the request rate rather than the data complexity.

In abuse prevention infrastructure, cache stampede is particularly relevant for frequently accessed risk signals (e.g., customer risk scores, device fingerprint lookups, real-time abuse rate computations) that are cached with finite TTLs. A stampede on these keys can degrade enforcement latency precisely when the system is under highest load -- often during peak shopping events when abuse attempts also spike.

## Key Characteristics

### Trigger Scenarios

| Trigger | Description | Severity |
|---------|-------------|----------|
| **TTL expiry** | A popular key's time-to-live expires; all concurrent requests miss simultaneously | Most common; severity proportional to key popularity |
| **Cache restart / flush** | Cache node restarts or memory is flushed; all keys are lost at once | Catastrophic; every key stampedes simultaneously (cold start) |
| **Cold start** | New cache deployment or new cache node joins the cluster with empty memory | Severe for high-traffic services; the entire working set must be rebuilt |
| **Cache eviction** | LRU/LFU eviction removes a popular key under memory pressure | Unpredictable; eviction of a hot key triggers a targeted stampede |
| **Invalidation storm** | A bulk data update invalidates many related cache entries simultaneously | Severity depends on how many invalidated keys are actively requested |

### Mitigation Strategies

#### 1. Locking / Mutex (Leader Election for Cache Rebuild)

On cache miss, only the first request acquires a distributed lock (e.g., Redis `SET key lock_value EX timeout NX`) and rebuilds the cache. All other requests either wait for the lock to release and read the freshly populated cache, or return a stale fallback value.

```
Request 1 (miss) ──► Acquire lock ──► Query DB ──► Populate cache ──► Release lock
Request 2 (miss) ──► Lock held ──► Wait/poll ──► Read from cache
Request 3 (miss) ──► Lock held ──► Wait/poll ──► Read from cache
...
Request N (miss) ──► Lock held ──► Wait/poll ──► Read from cache
```

**Trade-offs**: Eliminates redundant DB queries but introduces lock contention, potential deadlocks (if the lock holder crashes), and added latency for waiting requests. Requires careful timeout tuning.

#### 2. Stale-While-Revalidate (Serve Stale, Refresh Async)

Maintain a logical TTL (when refresh should happen) and a physical TTL (when the entry is actually deleted). When the logical TTL expires, continue serving the stale value while a single background thread refreshes the cache asynchronously. Requests never see a miss.

```
Logical TTL expires
    │
    ├── Serve stale value to all requests (no miss visible)
    └── Background thread: Query DB ──► Update cache
```

**Trade-offs**: Near-zero user-facing latency impact and no stampede, but requires accepting temporarily stale data. The dual-TTL scheme adds implementation complexity.

#### 3. Probabilistic Early Expiration (XFetch Algorithm)

Each request independently decides whether to refresh the cache *before* the TTL expires, with the probability of refresh increasing exponentially as the TTL approaches zero. This is formalized by the **XFetch algorithm** (Vattani, Chierichetti, and Lowenstein, 2015):

```
current_time > expiry - (delta * beta * log(random()))
```

Where `delta` is the recomputation time, `beta` is a tuning parameter (default 1.0), and `random()` is uniform on (0, 1]. As `current_time` approaches `expiry`, the inequality is satisfied with increasing probability, causing one request to preemptively refresh the cache before the mass expiry event.

**Trade-offs**: Elegant, lock-free, and statistically optimal. Requires no coordination between processes. However, it does not guarantee exactly one refresh (multiple early refreshes are possible but statistically unlikely), and it requires knowing or estimating the recomputation time `delta`.

#### 4. Request Coalescing (Singleflight)

When a cache miss occurs, the first request initiates the database query and registers itself as the "in-flight" request for that key. Subsequent requests for the same key within that window are not executed independently; instead, they subscribe to the result of the in-flight request and receive the same response. This is the **singleflight** pattern (named after Go's `golang.org/x/sync/singleflight` package).

```
Request 1 (miss) ──► Start DB query ──► [result] ──► Populate cache
Request 2 (miss) ──► Join flight ───────► [same result]
Request 3 (miss) ──► Join flight ───────► [same result]
```

**Trade-offs**: Guarantees exactly one database query per key per miss window. Simple to implement in-process. However, distributed singleflight across multiple application instances requires external coordination (e.g., Redis-based coalescing).

#### 5. Cache Warming (Proactive Population)

Pre-load popular keys into the cache before they are requested, either during deployment (from access logs or a known hot-key list) or continuously via a background process that monitors TTL and refreshes keys before expiry.

**Trade-offs**: Eliminates cold-start stampedes entirely but requires maintaining a list of hot keys, adds background processing overhead, and can waste cache memory on keys that are no longer popular.

### Mitigation Comparison

| Strategy | Redundant DB Queries | Latency Impact | Staleness | Implementation Complexity | Coordination Required |
|----------|---------------------|----------------|-----------|--------------------------|----------------------|
| **Locking / Mutex** | 1 query | Waiting requests blocked | None (fresh on unlock) | Medium | Distributed lock |
| **Stale-While-Revalidate** | 1 query | None (serve stale) | Brief stale window | Medium | None (async refresh) |
| **XFetch (Probabilistic)** | ~1 query (statistical) | None (early refresh) | None (refreshed before expiry) | Low | None (independent) |
| **Request Coalescing** | 1 query | Waiting requests share result | None | Low (in-process) / Medium (distributed) | In-process or distributed |
| **Cache Warming** | 0 queries (proactive) | None | None (preemptive) | Medium | Hot-key list |

### Combined Defense

In practice, production systems combine multiple strategies for defense in depth:

1. **XFetch + Singleflight**: Probabilistic early refresh eliminates the cold expiry window; singleflight deduplicates any remaining concurrent misses. The database never sees a stampede.
2. **Stale-While-Revalidate + Locking**: Serve stale data instantly while a locked background refresh runs. Users see no latency spike and the database sees exactly one query.
3. **Cache Warming + TTL Jitter**: Pre-load hot keys on deploy; add random jitter to TTLs (e.g., TTL = base_ttl + random(0, jitter_range)) so keys expire at different times rather than simultaneously.

### When to Apply Stampede Protection

Not every cache key needs stampede protection. Overengineering every cache path adds unnecessary complexity. Apply targeted protection based on:

- **High request rate**: Keys serving hundreds or thousands of RPS
- **Expensive recomputation**: Keys whose backing query is slow (> 100ms)
- **Critical path**: Keys on the request critical path where latency spikes cause user-visible degradation
- **Hot keys with uniform TTL**: Keys that expire at the same time across the fleet

## Related Terms

- **[Term: Caching](term_caching.md)** -- Parent concept covering caching layers, metrics (hit ratio, miss penalty), and distributed coherence; cache stampede is one of the critical failure modes within caching systems
- **[Term: Cache-Aside](term_cache_aside.md)** -- The caching strategy most susceptible to cache stampede, as the application manages cache population on miss without built-in coordination
- **[Term: LRU Cache](term_lru_cache.md)** -- LRU eviction of a hot key under memory pressure is one trigger scenario for a cache stampede
- **[Term: KV Cache](term_kv_cache.md)** -- Key-value cache in LLM inference; while a different domain, it shares the concept of cache pressure and memory management under concurrent access
- **[Term: Availability](term_availability.md)** -- Cache stampede degrades system availability by overwhelming the database; mitigation strategies are availability-preserving patterns
- **[Term: CAP Theorem](term_cap_theorem.md)** -- Stale-while-revalidate mitigation trades consistency for availability during the refresh window, reflecting the CAP trade-off
- **[Term: Consistency](term_consistency.md)** -- Several stampede mitigations (stale-while-revalidate, probabilistic early expiration) accept brief inconsistency to preserve availability
- **[Term: Consistent Hashing](term_consistent_hashing.md)** -- Partitioning strategy for distributed caches; a cache node departure triggers stampedes for all keys that hash to the departing node
- **[Term: CDN](term_cdn.md)** -- Content Delivery Networks experience cache stampede at the edge layer when popular content TTLs expire across edge nodes simultaneously
- **[Circuit Breaker](term_circuit_breaker.md)**: Fault tolerance pattern that prevents cascading failures when cache stampedes overwhelm backend databases; circuit breakers halt requests to failing backends during stampede recovery
- **[Term: Availability Heuristic](term_availability_heuristic.md)** -- Cognitive bias relevant to stampede analysis: engineers overweight recent stampede incidents when designing caching policy, potentially over-engineering low-risk paths
- **[Term: SLA](term_sla.md)** -- Cache stampede directly threatens SLA compliance by causing latency spikes and potential downtime; stampede protection is an SLA defense mechanism
- **[Term: Event-Driven Architecture](term_event_driven_architecture.md)** -- Event-driven cache invalidation (pub/sub) can trigger invalidation storms that cause stampedes if many keys are invalidated simultaneously
- **[Term: Observer Pattern](term_observer_pattern.md)** -- Singleflight / request coalescing uses an observer-like subscription model where waiting requests observe the result of the in-flight request
- **[Term: Proxy Pattern](term_proxy_pattern.md)** -- Request coalescing proxies act as intermediaries that deduplicate identical cache-miss requests before forwarding to the database
- **[Rate Limiting](term_rate_limiting.md)**: Request throttling mechanism that limits the blast radius of cache stampedes by capping concurrent requests to the backend during cache miss storms
- **[Redis](term_redis.md)**: Primary cache backend where stampedes occur; Redis Lua scripts and SETNX enable distributed locking strategies (singleflight) to mitigate stampede conditions
- **[Write-Back Cache](term_write_back_cache.md)**: Write-back caching keeps frequently written keys always warm in cache, mitigating read stampedes — but cold-start stampedes still apply after cache restart
- **[Write-Through Cache](term_write_through_cache.md)**: Write-through keeps written keys always present in cache, reducing stampede risk for keys on the write path — but TTL expiry can still trigger stampedes for read-heavy keys
- **[Cache Invalidation](term_cache_invalidation.md)**: Mass cache invalidation (purge, ban, or TTL expiry of many keys simultaneously) is a primary trigger for cache stampedes; invalidation strategy directly determines stampede risk
- **[Eviction Policy](term_eviction_policy.md)**: LRU/LFU eviction of a hot key under memory pressure is a trigger scenario for cache stampede, as the evicted key generates a burst of cache misses

## References

### External References
- [Cache Stampede -- Wikipedia](https://en.wikipedia.org/wiki/Cache_stampede)
- [Thundering Herd Problem -- Wikipedia](https://en.wikipedia.org/wiki/Thundering_herd_problem)
- [Vattani, A.; Chierichetti, F.; Lowenstein, K. (2015). "Optimal Probabilistic Cache Stampede Prevention." PVLDB, 8(8), 886--897.](https://cseweb.ucsd.edu/~avattani/papers/cache_stampede.pdf)
- [Cache Stampede & The Thundering Herd Problem -- Medium](https://medium.com/@sonal.sadafal/cache-stampede-the-thundering-herd-problem-d31d579d93fd)
- [How to Handle Cache Stampede (Thundering Herd) in Redis -- OneUptime](https://oneuptime.com/blog/post/2026-01-21-redis-cache-stampede/view)
- [Cache Stampede Prevention -- Redis Patterns](https://redis.antirez.com/fundamental/cache-stampede-prevention.html)
- [Sometimes I Cache: Implementing Lock-Free Probabilistic Caching -- Cloudflare Blog](https://blog.cloudflare.com/sometimes-i-cache/)
- [The Thundering Herd Problem: Mitigation Strategies for Cache Stampedes -- System Design Review](https://systemdr.substack.com/p/the-thundering-herd-problem-mitigation)
- [A Crash Course in Caching -- Final Part -- ByteByteGo](https://blog.bytebytego.com/p/a-crash-course-in-caching-final-part)

---

**Last Updated**: April 19, 2026
**Status**: Active -- system design concept covering cache stampede triggers, mitigation strategies (locking, stale-while-revalidate, XFetch, singleflight, warming), and trade-off comparison
