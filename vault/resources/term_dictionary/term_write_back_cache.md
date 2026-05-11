---
tags:
  - resource
  - terminology
  - system_design
  - caching
  - design_patterns
keywords:
  - write-back cache
  - write-behind cache
  - async flush
  - dirty bit
  - write coalescing
  - cache write policy
  - eventual consistency
  - data loss risk
  - flush strategy
topics:
  - System Design
  - Caching Strategies
  - Performance Optimization
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: Write-Back Cache (Write-Behind Cache)

## Definition

**Write-Back Cache** (also called **Write-Behind Cache**) is a caching strategy in which write operations are directed to the cache first, acknowledged to the client immediately, and then **asynchronously flushed** to the underlying database or backing store at a later time. This decouples write latency from database latency -- the application only waits for the fast cache write, not the slow disk write. The trade-off is a window of vulnerability: data that exists only in the cache has not yet been persisted, so a cache failure before the flush completes results in **data loss**. Write-back is the write-path counterpart of read-through caching and is the opposite of write-through, which writes to cache and database synchronously before acknowledging the client.

## Context

Write-back caching is one of three primary write-path strategies discussed in the SDDD podcast series ([Episode 4 -- Caching](../digest/digest_sddd_caching_podcast.md)), alongside write-through and write-around. The key design decision is where on the consistency-performance spectrum the system should sit:

- **Write-Through**: synchronous writes to both cache and DB -- strong consistency, higher write latency
- **Write-Back (Write-Behind)**: asynchronous DB writes after cache write -- low write latency, eventual consistency, data loss risk
- **Write-Around**: writes bypass cache entirely, go directly to DB -- cache populated only on read miss

Write-back is the preferred strategy for **write-heavy workloads** where throughput matters more than immediate durability -- for example, social media feed updates, analytics counters, logging pipelines, and real-time metrics. In combination with a read-through or cache-aside pattern on the read path, write-back provides a full caching solution that optimizes both reads and writes.

The term "write-back" originates from CPU cache architecture (L1/L2 hardware caches), where it describes the policy of modifying cache lines without immediately updating main memory. In distributed systems and application-level caching, the same concept is called "write-behind" because the database write happens *behind* (after) the cache write. The two terms are interchangeable, though "write-back" is more common in hardware contexts and "write-behind" in application/middleware contexts (e.g., Oracle Coherence, Ehcache).

## Key Characteristics

- **Write flow**: The application writes to the cache and receives an immediate acknowledgment. The cache is now the temporary source of truth. A background process asynchronously flushes the cached write to the database. The client never waits for the database write.

- **Dirty bit tracking**: Each cache entry that has been modified but not yet flushed to the database is marked with a **dirty bit** (or dirty flag). Only dirty entries need to be written back. Clean entries (unchanged or already flushed) can be evicted without a database write. This minimizes unnecessary I/O.

- **Flush strategies**: The cache must decide when to flush dirty entries to the backing store. Common strategies include:
  - **Time-based**: Flush at regular intervals (e.g., every 5 seconds). Predictable write cadence; staleness bounded by interval length.
  - **Count-based**: Flush after a threshold number of dirty entries accumulate (e.g., every 100 writes). Adapts to write volume.
  - **Size-based**: Flush when the dirty data reaches a memory threshold. Prevents unbounded memory growth.
  - **Eviction-triggered**: Flush when a dirty entry must be evicted to make room for new data. Lazy but memory-efficient.
  - **Hybrid**: Combine time-based and count-based (e.g., flush every 5 seconds or every 100 writes, whichever comes first).

- **Data loss risk**: The defining trade-off. Between the cache write and the async flush, data exists only in volatile memory. If the cache process crashes, is restarted, or loses power during this window, unflushed dirty entries are lost permanently. This risk can be mitigated but not eliminated: Redis AOF persistence, replication to standby nodes, or battery-backed write caches in hardware reduce the window but add complexity.

- **Write coalescing**: When the same key is updated multiple times before a flush, write-back caches can **coalesce** those updates into a single database write containing only the final value. This dramatically reduces database write traffic for frequently updated keys (e.g., a view counter that increments 1,000 times per second produces only one DB write per flush interval rather than 1,000).

- **Comparison with write-through**:

  | Dimension | Write-Back | Write-Through |
  |-----------|-----------|---------------|
  | **Write latency** | Low (cache only) | High (cache + DB) |
  | **Consistency** | Eventual | Strong |
  | **Data loss risk** | High (cache failure = data loss) | None (DB always current) |
  | **DB write load** | Low (batched, coalesced) | High (every write hits DB) |
  | **Complexity** | Higher (flush logic, dirty tracking) | Lower (synchronous path) |
  | **Best for** | Write-heavy, throughput-first | Read-after-write consistency |

- **Use cases**:
  - **Social media feeds**: Like counts, view counts, and feed rankings update frequently and tolerate eventual consistency
  - **Logging and metrics**: High-volume log ingestion where losing a few seconds of logs on cache failure is acceptable
  - **Analytics counters**: Page views, click counts, impression tracking -- write-heavy with tolerance for approximation
  - **Gaming leaderboards**: Scores updated in cache, periodically flushed to persistent storage
  - **IoT sensor data**: High-frequency sensor writes batched before database persistence
  - **Session state**: User session data written to cache for speed, periodically persisted for recovery

## Related Terms

- **[ACID](term_acid.md)** -- Write-back violates ACID durability during the dirty window; write-through preserves it. The choice depends on whether the application requires transactional guarantees
- **[Cache-Aside](term_cache_aside.md)** -- Alternative caching strategy where writes go directly to the database and cache is populated on read miss; contrasts with write-back's cache-first write path
- **[Cache Invalidation](term_cache_invalidation.md)** -- Write-back modifies cache entries directly on writes; invalidation is less relevant since the cache is the initial write target, but TTL and eviction still apply
- **[Cache Stampede](term_cache_stampede.md)** -- Write-back can mitigate read stampedes by keeping frequently written keys always warm in cache, but cold-start stampedes still apply after cache restart
- **[Caching](term_caching.md)** -- Parent concept covering caching layers, metrics, and distributed coherence; write-back is one of five core caching strategies
- **[CAP Theorem](term_cap_theorem.md)** -- Write-back caching is an AP (availability + partition tolerance) choice: it prioritizes availability (fast writes) over consistency (immediate DB sync)
- **[Change Data Capture](term_change_data_capture.md)** -- CDC captures database changes for downstream consumers; in a write-back system, CDC only sees changes after the async flush, introducing additional delay in the data pipeline
- **[Consistency](term_consistency.md)** -- Write-back trades strong consistency for performance; the dirty window introduces eventual consistency between cache and database
- **[Data Lakehouse](term_data_lakehouse.md)** -- Lakehouse transaction logs provide durability guarantees that write-back caching alone cannot; combining write-back with a durable log mitigates data loss risk
- **[Event-Driven Architecture](term_event_driven_architecture.md)** -- The async flush in write-back is conceptually similar to EDA's asynchronous event processing; both decouple producers from downstream persistence
- **[Eviction Policy](term_eviction_policy.md)** -- Eviction of dirty entries in a write-back cache triggers a flush to the database before removal; clean entries can be evicted without I/O
- **[Hexagonal Architecture](term_hexagonal_architecture.md)** -- The cache layer in write-back acts as a driven adapter, decoupling the application core from the database's write latency
- **[KV Cache](term_kv_cache.md)** -- Key-value cache used in LLM inference; shares the concept of volatile in-memory storage that may be lost, though KV cache is for computation reuse rather than write buffering
- **[LRU Cache](term_lru_cache.md)** -- The default eviction policy used within write-back caches; determines which dirty entries are flushed when cache space is needed
- **[Message Queue](term_message_queue.md)** -- Write-back caches often use message queues to durably buffer pending writes before flushing to the backing store, preventing data loss during cache failures
- **[Redis](term_redis.md)** -- In-memory data store that implements write-back semantics via AOF (Append-Only File) persistence; Redis write-back patterns trade durability for write throughput
- **[Stream Processing](term_stream_processing.md)** -- The async flush in write-back resembles micro-batch processing in stream systems; both buffer and batch writes for throughput
- **[Write-Ahead Log](term_write_ahead_log.md)** -- The complementary durability pattern: WAL writes the log before the data to prevent loss, while write-back writes the cache before the database to improve speed. WAL can be used alongside write-back to reduce data loss risk
- **[Write-Through Cache](term_write_through_cache.md)** -- The opposite write strategy: writes go to cache and database synchronously, providing strong consistency at the cost of higher write latency
- **[Write-Around Cache](term_write_around_cache.md)** -- Alternative write strategy where writes go directly to the database, bypassing the cache entirely; contrasts with write-back in that both avoid synchronous cache+DB writes, but for different reasons — write-back defers the DB write for speed, while write-around skips the cache write to avoid pollution

## References

### Vault References
- [Digest: Everything to Know About Caching -- SDDD Episode 4](../digest/digest_sddd_caching_podcast.md) -- primary source; covers write-back as one of three write strategies alongside write-through and write-around
- [Digest: SDDD Series Overview](../digest/digest_sddd_series.md) -- series index for the System Design Deep Dive podcast

### External References
- [Write Behind Cache -- AlgoMaster.io](https://algomaster.io/learn/system-design/write-behind-cache) -- detailed write-behind pattern explanation with diagrams
- [Write Through and Write Back in Cache -- GeeksforGeeks](https://www.geeksforgeeks.org/computer-organization-architecture/write-through-and-write-back-in-cache/) -- hardware cache write policies comparison
- [Cache Write Policies -- System Design -- GeeksforGeeks](https://www.geeksforgeeks.org/system-design/cache-write-policies-system-design/) -- system design perspective on cache write strategies
- [Caching Strategy: Write-Behind (Write-Back) Pattern -- EnjoyAlgorithms](https://www.enjoyalgorithms.com/blog/write-behind-caching-pattern/) -- flush strategies, write coalescing, and implementation details
- [Read-Through, Write-Through, Write-Behind Caching -- Oracle Coherence](https://docs.oracle.com/cd/E13924_01/coh.340/e13819/readthrough.htm) -- enterprise middleware perspective on write-behind with coalescing and batching
- [What Is Write-Back? -- TechTarget](https://www.techtarget.com/whatis/definition/write-back) -- concise definition of write-back caching in hardware and software contexts
- [Understanding Write-Through, Write-Around, and Write-Back Caching -- Shahriar Tajbakhsh](https://shahriar.svbtle.com/Understanding-writethrough-writearound-and-writeback-caching-with-python) -- Python implementation comparison of cache write policies

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Write-Back Cache (Write-Behind Cache) |
| **Also Known As** | Write-Behind, Lazy Write, Deferred Write |
| **Core Mechanism** | Write to cache first, flush to DB asynchronously |
| **Write Latency** | Low (cache write only; DB write is deferred) |
| **Consistency Model** | Eventual (dirty window between cache write and DB flush) |
| **Data Loss Risk** | High (unflushed dirty entries lost on cache failure) |
| **Key Optimization** | Write coalescing -- multiple updates to same key merged into one DB write |
| **Dirty Tracking** | Dirty bit per cache entry; only dirty entries flushed |
| **Flush Triggers** | Time-based, count-based, size-based, eviction-triggered, or hybrid |
| **Contrast** | Write-Through (sync, strong consistency, no data loss) |
| **Best For** | Write-heavy workloads: counters, analytics, logging, social feeds, IoT |

**Key Insight**: Write-back caching is fundamentally a bet that cache reliability is good enough to justify deferred persistence. By absorbing writes into fast, volatile memory and batching them into fewer, larger database operations, write-back can deliver orders-of-magnitude improvements in write throughput and dramatically reduce database load. The critical design question is not whether to use write-back, but how to size the dirty window -- too small and you lose the batching benefit; too large and the data loss exposure becomes unacceptable. The best implementations combine write-back with a lightweight durability mechanism (e.g., Redis AOF, replication to a standby cache, or a write-ahead log) to narrow the vulnerability window while preserving the throughput advantage. Write coalescing is the often-overlooked superpower: for hot keys that are updated thousands of times per second, write-back reduces database writes from N to 1 per flush interval -- a reduction that no synchronous strategy can match.

---

**Last Updated**: April 19, 2026
**Status**: Active -- system design caching strategy from SDDD podcast series (Episode 4)
