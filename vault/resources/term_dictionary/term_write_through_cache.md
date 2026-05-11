---
tags:
  - resource
  - terminology
  - system_design
  - caching
  - design_patterns
keywords:
  - write-through cache
  - caching strategy
  - cache consistency
  - synchronous write
  - cache-database consistency
  - write latency
  - DAX
  - DynamoDB Accelerator
topics:
  - system design
  - caching strategies
  - distributed systems
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: Write-Through Cache

## Definition

**Write-Through Cache** is a caching strategy in which every write operation goes to both the cache and the underlying database **synchronously** -- the write is only acknowledged as complete when both the cache and the database have been updated. This guarantees that the cache is always consistent with the database at the cost of higher write latency, because every write must wait for two sequential writes (cache + database) before returning a success response to the client. Write-through is the "safety-first" caching pattern: it trades write performance for the certainty that no read from the cache will ever return stale data.

## Context

Write-through is one of the **5 core caching strategies** discussed in system design:

| Strategy | Write Path | Read Path | Consistency | Latency |
|----------|-----------|-----------|-------------|---------|
| **Cache-Aside (Lazy Loading)** | App writes to DB only; cache populated on read miss | App checks cache, on miss reads DB and populates cache | Eventual (cache may be stale until TTL expires or invalidation) | Low write, variable read |
| **Read-Through** | Same as cache-aside but cache library handles reads | Cache intercepts reads; on miss, loads from DB automatically | Eventual (same as cache-aside) | Low write, variable read |
| **Write-Through** | App writes to cache; cache writes to DB synchronously | App reads from cache (always fresh) | **Strong** -- cache and DB always in sync | **High write**, low read |
| **Write-Back (Write-Behind)** | App writes to cache only; cache writes to DB asynchronously | App reads from cache | Eventual (async lag); risk of data loss on cache failure | Low write, low read |
| **Write-Around** | App writes directly to DB, bypassing cache | App reads from cache; cache populated on read miss | Eventual (cache stale until miss triggers reload) | Low write, variable read |

Write-through is most commonly paired with read-through to create a **fully transparent caching layer** where the application only interacts with the cache, never directly with the database. This combination simplifies application code but introduces the write latency penalty inherent to synchronous dual writes.

## Key Characteristics

### Write Flow

```
Client Write Request
        │
        ▼
   ┌─────────┐
   │  Cache   │ ── 1. Write data to cache
   └────┬─────┘
        │
        ▼
   ┌─────────┐
   │ Database │ ── 2. Write data to database (synchronous)
   └────┬─────┘
        │
        ▼
 Acknowledge success to client
 (only after BOTH writes complete)
```

The critical property is **synchronous completion**: the write is not acknowledged until both the cache and database have durably stored the data. If either write fails, the entire operation fails, maintaining consistency.

### Read Flow

```
Client Read Request
        │
        ▼
   ┌─────────┐
   │  Cache   │ ── Always returns fresh data (cache hit)
   └─────────┘
```

Because every write updates the cache first, read operations always find fresh data in the cache. Cache misses only occur for data that has never been written through the cache (e.g., data written before the cache was introduced, or data written by other systems that bypass the cache).

### Consistency Guarantee

- **Strong consistency**: After a write completes, any subsequent read from the cache is guaranteed to return the latest value
- **No stale reads**: Unlike cache-aside or write-around, there is no window where the cache contains outdated data
- **Simplifies invalidation**: No need for TTL-based expiry or manual cache invalidation because the cache is always updated on write

### Write Latency Penalty

- Every write incurs the latency of **two sequential writes** (cache + database)
- The total write latency is approximately: `latency_cache_write + latency_db_write`
- For network-attached caches (e.g., Redis, DAX), the additional network hop adds measurable latency
- Under write-heavy workloads, this latency penalty can significantly degrade overall throughput

### Write-Through vs. Write-Back vs. Write-Around

| Aspect | Write-Through | Write-Back | Write-Around |
|--------|--------------|------------|--------------|
| **Write latency** | High (2 synchronous writes) | Low (1 write to cache only) | Low (1 write to DB only) |
| **Consistency** | Strong | Eventual (async lag) | Eventual (stale cache until miss) |
| **Data loss risk** | None (DB is always up-to-date) | **High** (cache failure loses unsynced data) | None (DB is source of truth) |
| **Cache pollution** | Yes (infrequently-read data fills cache) | Yes | No (only read data enters cache) |
| **Best for** | Consistency-critical systems | Write-heavy, loss-tolerant systems | Read-heavy with infrequent writes |

### Use Cases

- **Financial systems**: Account balances, transaction records, and ledger entries where stale reads could cause double-spending or incorrect balances
- **Inventory management**: Stock counts must be accurate across all readers to prevent overselling
- **Session management**: User session data that must be immediately available across all application servers
- **Configuration stores**: System configuration that must be instantly visible after an update
- **E-commerce pricing**: Price changes must be immediately reflected to avoid selling at incorrect prices

### DynamoDB DAX as a Write-Through Example

**Amazon DynamoDB Accelerator (DAX)** is a fully managed, in-memory cache that implements both **read-through** and **write-through** caching for DynamoDB:

- **Write-through in DAX**: When an application writes through DAX, the item is first written to DynamoDB and then updated in the DAX item cache. The write is acknowledged only after both DynamoDB and DAX have been updated.
- **Extra latency**: A write through DAX incurs an additional network hop compared to writing directly to DynamoDB, resulting in slightly higher write latency.
- **Write-around alternative**: For bulk data loads or write-heavy workloads, applications can bypass DAX and write directly to DynamoDB (write-around), accepting that the DAX cache will be stale until the next read-through populates it.
- **Consistency model**: DAX with write-through ensures that any item written through DAX is immediately available for subsequent reads from DAX without stale data.

### Disadvantage: Cache Pollution

Write-through causes **cache pollution** -- data that is written but rarely or never read still occupies cache space. In a system where many keys are written but only a small subset are frequently read, write-through wastes expensive cache memory. This is why write-through is almost always combined with an eviction policy (e.g., LRU) to age out infrequently accessed data.

## Related Terms

### Caching Strategies
- **[Cache-Aside](term_cache_aside.md)** -- Alternative caching strategy where the application manages cache reads and writes independently; Cache-Aside uses invalidate-on-write while write-through updates the cache synchronously
- **[Cache Invalidation](term_cache_invalidation.md)** -- Write-through eliminates the need for explicit invalidation because the cache is always updated on write; other strategies rely on TTL or event-based invalidation
- **[Caching](term_caching.md)** -- Parent concept covering caching layers, metrics, and coherence; write-through is one of five core caching strategies
- **[Eviction Policy](term_eviction_policy.md)** -- Write-through causes cache pollution; pairing with LRU or LFU eviction manages cache size by removing infrequently accessed entries
- **[Write-Back Cache](term_write_back_cache.md)** -- The opposite write strategy: writes go to cache first and flush to DB asynchronously, trading consistency for low write latency
- **[Write-Around Cache](term_write_around_cache.md)** -- Alternative write strategy where writes bypass the cache entirely and go directly to the database; contrasts with write-through's synchronous cache update, avoiding cache pollution at the cost of cache misses on recently written data

### Caching and Data Access
- **[LRU Cache](term_lru_cache.md)** -- LRU eviction policy is commonly paired with write-through to manage cache size by evicting the least recently used entries that write-through populates
- **[KV Cache](term_kv_cache.md)** -- Key-value stores are the underlying data structure for most cache implementations including write-through caches
- **[Redis](term_redis.md)** -- In-memory data store commonly used as the cache layer in write-through configurations; Redis persistence modes complement write-through durability guarantees
- **[Write-Ahead Log](term_write_ahead_log.md)** -- WAL guarantees database durability on the DB side of the write-through pipeline; both WAL and write-through solve durability/consistency but at different layers

### Consistency and Database Theory
- **[Consistency](term_consistency.md)** -- Write-through cache provides strong consistency between cache and database, analogous to strong consistency in distributed systems
- **[ACID Properties](term_acid.md)** -- Write-through ensures the cache reflects ACID-committed state in the database; the synchronous write pattern mirrors ACID's durability guarantee
- **[CAP Theorem](term_cap_theorem.md)** -- Write-through trades availability (higher write latency, potential write failure if either store is down) for consistency
- **[NoSQL](term_nosql.md)** -- NoSQL databases like DynamoDB and Redis are commonly used as either the cache layer or the backing store in write-through architectures

### Database and Storage
- **[DynamoDB](term_ddb.md)** -- DAX (DynamoDB Accelerator) is a production write-through cache implementation; DynamoDB itself supports both eventually consistent and strongly consistent reads
- **[Event-Driven Architecture](term_event_driven_architecture.md)** -- Write-back caching often uses event-driven async writes; write-through avoids this complexity by using synchronous writes

### System Design Context
- **[OLTP](term_oltp.md)** -- Write-through caching is most relevant for OLTP systems where read-after-write consistency is critical for transactional workloads
- **[Data Engineering Lifecycle](term_data_engineering_lifecycle.md)** -- Caching strategy selection (write-through vs. write-back vs. cache-aside) is a key architectural decision in the serving layer of the data engineering lifecycle

## References

### External References

- [Amazon DynamoDB Accelerator (DAX): A Read-Through/Write-Through Cache for DynamoDB -- AWS Database Blog](https://aws.amazon.com/blogs/database/amazon-dynamodb-accelerator-dax-a-read-throughwrite-through-cache-for-dynamodb/)
- [DAX and DynamoDB Consistency Models -- AWS Documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.consistency.html)
- [Caching Patterns -- Database Caching Strategies Using Redis -- AWS Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)
- [Caching Strategies: Cache-Aside, Read-Through, Write-Through, Write-Back -- System Design Space](https://system-design.space/en/chapter/caching-strategies/)
- [Write-Through Caching Strategy -- Enjoy Algorithms](https://www.enjoyalgorithms.com/blog/write-through-caching-strategy/)
- [Read-Through, Write-Through, Write-Behind Caching -- Oracle Coherence Documentation](https://docs.oracle.com/cd/E13924_01/coh.340/e13819/readthrough.htm)
- [Caching Strategies -- AlgoMaster.io](https://algomaster.io/learn/system-design/caching-strategies)
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media. Chapter 5: Replication.

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | Write-Through Cache |
| **Category** | Caching Strategy / Design Pattern |
| **Core Mechanism** | Write to cache + database synchronously; acknowledge only after both complete |
| **Consistency** | Strong -- cache is always in sync with the database |
| **Write Latency** | High (two sequential writes per operation) |
| **Read Latency** | Low (always cache hit for previously written data) |
| **Data Loss Risk** | None (database is always up-to-date) |
| **Cache Pollution** | Yes (infrequently-read data fills cache; pair with LRU eviction) |
| **Best Paired With** | Read-through for a fully transparent caching layer |
| **Real-World Example** | DynamoDB DAX (read-through + write-through for DynamoDB) |
| **Ideal Use Cases** | Financial systems, inventory, session management, configuration stores |
| **Avoid When** | Write-heavy workloads with low read-to-write ratio; bulk data loads |

**Key Insight**: Write-through cache is the caching strategy you choose when correctness trumps performance. By paying the write latency tax upfront (synchronous dual write), you eliminate the entire class of stale-read bugs that plague cache-aside and write-around patterns. The trade-off is straightforward: every write is slower, but every read is guaranteed fresh. In consistency-critical domains like financial systems and inventory management, this trade-off is almost always worth it. The pattern becomes particularly powerful when combined with read-through (as in DynamoDB DAX), creating a transparent caching layer where the application code is completely unaware that a cache exists -- reads and writes flow through the cache automatically, with the cache handling all synchronization with the database.

---

**Last Updated**: April 19, 2026
**Status**: Active -- system design caching strategy from SDDD Podcast Episode 4 (Caching)
