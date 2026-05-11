---
tags:
  - resource
  - terminology
  - system_design
  - caching
  - distributed_systems
keywords:
  - cache invalidation
  - TTL
  - time-to-live
  - purge
  - ban
  - refresh
  - stale-while-revalidate
  - thundering herd
  - cache stampede
  - consistency
  - freshness
  - event-driven invalidation
  - version-based invalidation
  - tag-based invalidation
topics:
  - System Design
  - Distributed Systems
  - Caching
  - Data Consistency
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
related_wiki: null
---

# Term: Cache Invalidation

## Definition

**Cache invalidation** is the process of removing, updating, or marking stale data in a cache so that subsequent reads fetch fresh data from the source of truth. It is the mechanism by which a system maintains coherence between cached copies and the authoritative data store. Phil Karlton's famous quote captures the challenge: *"There are only two hard things in Computer Science: cache invalidation and naming things."* The difficulty arises because invalidation requires solving a distributed coordination problem -- the cache must know when its data has become stale, but the write may happen on a completely different node, service, or even data center. Invalidation too aggressively destroys the latency benefit of caching; invalidation too lazily serves stale data to users.

## Context

Cache invalidation is one of the hardest problems in distributed systems because it sits at the intersection of consistency, latency, and availability. Every caching layer -- from browser caches and CDN edges to distributed caches (Redis, Memcached) and in-process caches -- must answer the question: *when should this cached entry be considered stale?* The answer determines the system's consistency guarantees.

In the [SDDD Caching Episode](../digest/digest_sddd_caching_podcast.md), invalidation is identified as one of the five independent dimensions of the caching design space (alongside placement, strategy, eviction, and scope). Unlike eviction (which removes entries to reclaim space), invalidation removes entries to maintain correctness. The choice of invalidation strategy directly constrains the staleness window -- the maximum time a client may observe outdated data.

For abuse detection systems, cache invalidation is especially critical: enforcement actions (account suspensions, refund blocks) must be reflected immediately, while less critical data (aggregate risk scores, historical signals) can tolerate eventual consistency with TTL-based invalidation.

## Key Characteristics

- **TTL-based expiration**: Each cache entry is assigned a time-to-live; the entry is automatically discarded after the TTL elapses. Simple and passive, but creates a staleness window equal to the TTL duration. The universal baseline strategy.
- **Event-based (active) invalidation**: When the source of truth changes, an event is published (via message bus, webhook, or CDC stream) that triggers cache invalidation. Provides near-real-time consistency but requires reliable event infrastructure.
- **Version-based invalidation**: Each cache entry carries a version number or ETag. On read, the client sends the version to the server; if it matches, the cached copy is still valid. Used extensively in HTTP caching (`If-None-Match`, `If-Modified-Since`).
- **Purge pattern**: Explicitly delete a specific cache key immediately after a write. The most direct form of active invalidation -- simple but tightly couples the write path to cache topology.
- **Ban pattern**: Invalidate all cache entries matching a pattern (URL regex, header match, tag). Useful for bulk invalidation scenarios like CMS deployments or config changes.
- **Tag-based invalidation**: Cache entries are tagged with logical labels (e.g., `product:123`, `category:electronics`). Invalidating a tag removes all entries carrying that tag. Enables precise, semantic invalidation without knowing every individual cache key.
- **Refresh / Stale-While-Revalidate**: Serve the stale cached entry immediately while asynchronously fetching a fresh version in the background. Prioritizes availability over consistency -- the client never sees a cache miss, but may see briefly stale data.
- **Cascading invalidation in multi-layer caches**: When caches are layered (browser -> CDN -> distributed cache -> database), invalidation must propagate through all layers. A purge at the distributed cache layer does nothing if the CDN edge still serves a stale copy. Multi-layer invalidation requires coordinated strategies across layers.
- **Consistency vs freshness trade-off**: Aggressive invalidation (short TTL, event-driven purge) improves freshness but increases load on the source of truth and reduces cache hit rate. Relaxed invalidation (long TTL, passive expiration) maximizes cache benefit but widens the staleness window.
- **Thundering herd on mass invalidation**: When many cache entries expire or are purged simultaneously, all requests fall through to the database, potentially overwhelming it. Mitigations include staggered TTLs (adding random jitter), request coalescing, lease-based locking, and probabilistic early expiration.

## Invalidation Strategy Decision Framework

| Strategy | Trigger | Granularity | Staleness Window | Complexity | Best For |
|----------|---------|-------------|-----------------|------------|----------|
| **TTL Expiration** | Clock (passive) | Per-key | 0 to TTL duration | Low | Universal baseline; acceptable staleness |
| **Purge** | Write event (active) | Single key | Near-zero | Low | Known key after mutation |
| **Ban** | Deploy/bulk event | Bulk (pattern) | Near-zero | Medium | CMS publish, config deploy |
| **Refresh** | Background fetch | Single key | Brief (async gap) | Medium | High-availability content |
| **Stale-While-Revalidate** | Read (async) | Single key | Brief (one request) | Medium | CDN edge, availability-first |
| **Event-Driven (CDC/Pub-Sub)** | Data change event | Per-entity | Sub-second | High | Strong consistency requirement |
| **Version/ETag** | Client validation | Per-key | Zero (validated) | Medium | HTTP caching, API responses |
| **Tag-Based** | Tag invalidation | Group of keys | Near-zero | High | Content systems, e-commerce catalogs |

**Practical default**: Combine TTL (passive baseline, e.g., 5 minutes) with Purge (active invalidation on writes). This limits staleness to the TTL duration while ensuring writes are reflected immediately when the application knows about the mutation.

## Related Terms

- **[Term: LRU Cache](term_lru_cache.md)** -- Eviction policy that removes least-recently-used entries to reclaim space; eviction is distinct from invalidation (space vs correctness)
- **[Term: KV Cache](term_kv_cache.md)** -- Key-value caching in LLM inference; invalidation of stale KV entries affects generation quality
- **[Term: Consistency](term_consistency.md)** -- The data consistency spectrum (strong, eventual, causal) that invalidation strategy directly determines
- **[Term: CAP Theorem](term_cap_theorem.md)** -- The impossibility theorem that forces a trade-off between consistency and availability; invalidation strategy is how caching systems navigate this trade-off
- **[Cache-Aside](term_cache_aside.md)**: Application-managed caching pattern where invalidation is the application's responsibility — the cache-aside pattern defines when and how invalidation must occur
- **[Caching](term_caching.md)**: Parent concept; cache invalidation is the correctness mechanism that ensures cached data remains consistent with the source of truth
- **[Term: Change Data Capture](term_change_data_capture.md)** -- CDC streams database changes as events, enabling real-time cache invalidation without coupling the write path to cache logic
- **[Term: Event-Driven Architecture](term_event_driven_architecture.md)** -- EDA provides the pub-sub infrastructure for event-based cache invalidation
- **[Eviction Policy](term_eviction_policy.md)**: Eviction removes entries for capacity management while invalidation removes entries for correctness — the two mechanisms are complementary but serve different purposes
- **[Term: Observer Pattern](term_observer_pattern.md)** -- The design pattern underlying event-based invalidation: caches observe data sources and react to change notifications
- **[Term: Write-Ahead Log](term_write_ahead_log.md)** -- WAL provides the ordered event log that CDC-based invalidation systems consume
- **[Term: Availability](term_availability.md)** -- The CAP property that stale-while-revalidate and TTL-based strategies prioritize over strict consistency
- **[Term: Partition Tolerance](term_partition_tolerance.md)** -- Network partitions make coordinated invalidation across distributed caches unreliable
- **[Term: Stream Processing](term_stream_processing.md)** -- Stream processors (Kafka, Flink) can consume change events and trigger cache invalidation in real time
- **[Term: Proxy Pattern](term_proxy_pattern.md)** -- Caching proxies (Varnish, Nginx) implement ban and purge invalidation at the reverse proxy layer
- **[Pub/Sub](term_pub_sub.md)**: Publish-subscribe messaging pattern used to broadcast cache invalidation events across distributed nodes; Redis pub/sub is the most common implementation for cache invalidation propagation
- **[Redis](term_redis.md)**: Primary in-memory cache whose entries require invalidation; Redis pub/sub and keyspace notifications enable event-driven invalidation across distributed cache nodes
- **[Write-Back Cache](term_write_back_cache.md)**: Write-back modifies cache entries directly on writes; invalidation is less relevant since the cache is the initial write target, but TTL and eviction still apply
- **[Write-Through Cache](term_write_through_cache.md)**: Write-through eliminates the need for explicit invalidation because the cache is always updated synchronously on every write — the strongest consistency guarantee among caching strategies
- **[Write-Around Cache](term_write_around_cache.md)**: Write-around avoids some invalidation complexity since writes bypass the cache entirely — there is no stale cache entry to invalidate on write, though the cache may serve stale data until TTL expiration or the next read miss

## References

### Vault References
- [Digest: Everything to Know About Caching -- SDDD Episode 4](../digest/digest_sddd_caching_podcast.md) -- Primary source; Section 6 covers invalidation methods (Purge, Refresh, Ban, TTL, Stale-While-Revalidate) and Section 8 covers thundering herd failure modes
- [Digest: SDDD Series Overview](../digest/digest_sddd_series.md) -- Series index for the System Design Deep Dive podcast

### External References
- Karlton, P. (attributed). "There are only two hard things in Computer Science: cache invalidation and naming things."
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*, Chapter 5: Replication and Chapter 11: Stream Processing. O'Reilly Media.
- [DesignGurus -- Caching in System Design Interviews](https://www.designgurus.io/blog/caching-system-design-interview) -- Invalidation methods taxonomy
- [HelloInterview -- Caching for System Design Interviews](https://www.hellointerview.com/learn/system-design/core-concepts/caching) -- Caching layers and invalidation strategies
- [Cache Invalidation Strategies -- OneUptime](https://oneuptime.com/blog/post/2026-01-30-cache-invalidation-strategies/view) -- TTL-based vs event-driven comparison
- [Mastering Cache Invalidation in Distributed Systems -- NumberAnalytics](https://www.numberanalytics.com/blog/ultimate-guide-cache-invalidation-distributed-systems) -- Comprehensive guide to distributed cache invalidation patterns

---

**Last Updated**: April 19, 2026
**Status**: Active -- system design concept; central to caching strategy selection in distributed systems
