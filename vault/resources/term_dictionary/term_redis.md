---
tags:
  - resource
  - terminology
  - system_design
  - databases
  - caching
keywords:
  - Redis
  - Remote Dictionary Server
  - in-memory database
  - key-value store
  - cache
  - pub/sub
  - data structures
  - Redis Cluster
  - Redis Sentinel
topics:
  - System Design
  - Caching
  - Database Architecture
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
related_wiki: null
---

# Redis - Remote Dictionary Server

## Definition

**Redis** (Remote Dictionary Server) is an open-source, in-memory key-value data store used as a database, cache, message broker, and streaming engine. Created by Salvatore Sanfilippo in 2009, Redis stores all data in RAM, delivering sub-millisecond read and write latencies. Unlike simple caches that only support opaque string values, Redis provides a rich set of native data structures — strings, hashes, lists, sets, sorted sets, bitmaps, HyperLogLogs, geospatial indexes, and streams — each with its own set of atomic operations. This structural richness distinguishes Redis from pure key-value caches and makes it suitable for a wide range of use cases beyond simple caching, including real-time leaderboards, session management, rate limiting, and pub/sub messaging.

## Context

Redis is one of the most widely deployed in-memory data stores in modern distributed systems. AWS offers Amazon ElastiCache for Redis and Amazon MemoryDB for Redis as managed services. In abuse prevention and fraud detection systems, Redis serves several critical roles: caching feature vectors for real-time model inference, maintaining session state across distributed services, implementing rate limiters to throttle abusive behavior, and powering real-time counters for velocity checks (e.g., how many returns a buyer has initiated in the past 24 hours). Its pub/sub capability also supports event-driven architectures where abuse signals need to be broadcast across multiple downstream consumers with minimal latency.

In 2024, Redis transitioned from the BSD-3 open-source license to a dual license (RSALv2 / SSPLv1), prompting the Linux Foundation to create **Valkey** as a community-maintained BSD-licensed fork. This licensing shift is an important consideration for new deployments.

## Key Characteristics

- **In-memory storage**: All data resides in RAM, enabling O(1) key lookups and sub-millisecond latencies; memory is the primary bottleneck rather than disk I/O
- **Rich data structures**:
  - **Strings**: Binary-safe values up to 512 MB; support atomic increment/decrement (useful for counters and rate limiters)
  - **Hashes**: Field-value maps ideal for representing objects (e.g., user profiles, session attributes)
  - **Lists**: Doubly-linked lists supporting push/pop from both ends; used for queues, activity feeds, and bounded logs
  - **Sets**: Unordered collections of unique strings; support union, intersection, and difference operations
  - **Sorted Sets (ZSETs)**: Sets where each member has a score; enable range queries by score or rank (leaderboards, priority queues, time-series indexes)
  - **Streams**: Append-only log structures with consumer groups; used for event sourcing and message streaming
  - **Bitmaps and HyperLogLogs**: Space-efficient structures for membership tracking and cardinality estimation
- **Persistence options**:
  - **RDB (Redis Database) snapshots**: Point-in-time snapshots written to disk at configurable intervals; compact and fast to load but risk data loss between snapshots
  - **AOF (Append-Only File)**: Logs every write operation; more durable (can be configured to fsync every second or every write) but larger and slower to replay
  - **RDB + AOF hybrid**: Combines the fast restart of RDB with the durability of AOF; recommended for production
- **Single-threaded event loop**: Command processing runs on a single thread using an event-driven, non-blocking I/O model (epoll/kqueue); eliminates lock contention and context switching. Redis 6+ introduced multi-threaded I/O for network read/write to increase throughput on multi-core systems, but command execution remains single-threaded
- **Pub/Sub messaging**: Publishers send messages to channels; subscribers receive them in real time. Supports pattern-based subscriptions. Not durable — messages are lost if no subscriber is listening. For durable messaging, Redis Streams with consumer groups are preferred
- **Redis Sentinel (high availability)**: A monitoring system that watches Redis primary and replica nodes, performs automatic failover when the primary becomes unreachable, and serves as a configuration provider for clients. Sentinel is a distributed system of multiple sentinel processes that reach quorum-based consensus on failure detection
- **Redis Cluster (horizontal scaling)**: Distributes data across multiple nodes using hash-slot-based sharding. The keyspace is divided into 16,384 hash slots; each node owns a subset. Clients route commands based on `CRC16(key) mod 16384`. Supports automatic resharding and replica failover within each shard. Linear throughput scaling up to 1,000 nodes
- **Atomic operations and transactions**: All individual commands are atomic. MULTI/EXEC provides transaction-like batching (all-or-nothing execution). Lua scripting enables server-side atomic execution of complex logic
- **Eviction policies**: When memory is full, Redis supports configurable eviction: `noeviction` (return errors), `allkeys-lru`, `allkeys-lfu`, `volatile-lru`, `volatile-lfu`, `volatile-ttl`, `allkeys-random`, `volatile-random` — enabling Redis to function as a bounded cache with LRU or LFU semantics

## Redis vs Memcached

| Dimension | Redis | Memcached |
|-----------|-------|-----------|
| **Data structures** | Strings, hashes, lists, sets, sorted sets, streams, bitmaps, HyperLogLogs, geospatial | Strings only |
| **Persistence** | RDB snapshots, AOF, or hybrid | None (pure volatile cache) |
| **Pub/Sub** | Built-in pub/sub + Streams | Not supported |
| **Threading** | Single-threaded command execution (multi-threaded I/O in 6+) | Multi-threaded (scales across CPU cores) |
| **Replication** | Primary-replica with Sentinel or Cluster | No built-in replication |
| **Eviction** | Multiple policies (LRU, LFU, TTL-based, random) | LRU only |
| **Scripting** | Lua scripting for server-side logic | Not supported |
| **Use case fit** | Rich caching, session store, queues, leaderboards, rate limiting, real-time analytics | Simple high-throughput string caching |

**When to choose Memcached**: When you need a simple, multi-threaded, volatile string cache with maximum raw throughput and minimal operational complexity. Memcached's multi-threaded architecture can outperform Redis on multi-core machines for simple get/set workloads.

**When to choose Redis**: When you need data structure versatility, persistence, pub/sub, scripting, or built-in high availability. Redis is the default choice for most new projects unless the use case is strictly simple string caching.

## Related Terms

- **[LRU Cache](term_lru_cache.md)**: Redis implements LRU and LFU eviction policies when used as a bounded cache — the eviction strategy determines which keys are removed under memory pressure
- **[LSM Tree](term_lsm_tree.md)**: Redis is often used as a caching layer in front of LSM tree databases to mitigate their read amplification
- **[KV Cache](term_kv_cache.md)**: Redis is a general-purpose key-value cache; KV cache in the LLM context refers to transformer attention caching — different domain, same fundamental pattern of storing computed results for reuse
- **[NoSQL](term_nosql.md)**: Redis belongs to the key-value paradigm within the NoSQL family — schema-free, horizontally scalable, optimized for specific access patterns over general-purpose querying
- **[DynamoDB](term_ddb.md)**: AWS managed NoSQL key-value/document store — DynamoDB is disk-based and designed for persistent storage at scale, while Redis is in-memory and optimized for speed; they are complementary rather than competing
- **[CAP Theorem](term_cap_theorem.md)**: Redis Cluster is a CP system by default (favors consistency over availability during partitions), while Redis Sentinel provides AP-like behavior with automatic failover
- **[Caching](term_caching.md)**: Redis is the most widely used distributed caching layer — it sits between the application and the primary database, reducing load and latency
- **[Event-Driven Architecture](term_event_driven_architecture.md)**: Redis pub/sub and Streams enable event-driven patterns — publishing abuse signals, session events, or feature updates to multiple consumers
- **[ACID](term_acid.md)**: Redis provides atomicity at the single-command level and supports transactions via MULTI/EXEC, but does not provide full ACID guarantees across distributed operations
- **[Consistency](term_consistency.md)**: Redis replication is asynchronous by default — replicas may lag behind the primary, creating an eventual consistency window
- **[Elasticsearch](term_elasticsearch.md)**: Both are in-memory-heavy stores, but Elasticsearch is optimized for full-text search and analytics while Redis is optimized for low-latency key-based access and data structure operations
- **[Availability](term_availability.md)**: Redis Sentinel and Cluster both target high availability through replica promotion and automatic failover
- **[BASE](term_base.md)**: Redis Cluster follows BASE consistency — Basically Available with eventual consistency across replicas; asynchronous replication means writes may be lost during failover
- **[Consistent Hashing](term_consistent_hashing.md)**: Hash-based partitioning algorithm used by Redis Cluster to distribute hash slots across nodes; determines which node stores a given key
- **[Database Replication](term_database_replication.md)**: Redis Sentinel and Redis Cluster use asynchronous replication for high availability; each primary node replicates to one or more replicas for failover
- **[Partition Tolerance](term_partition_tolerance.md)**: Redis Cluster handles network partitions by isolating unreachable nodes and continuing to serve hash slots owned by reachable nodes
- **[Scalability](term_scalability.md)**: Redis Cluster provides horizontal scalability through hash-slot-based sharding across multiple nodes, scaling throughput linearly
- **[Pub/Sub](term_pub_sub.md)**: Redis includes built-in pub/sub messaging (fire-and-forget, at-most-once delivery) and Streams (durable, consumer-group-based pub/sub), implementing the publish-subscribe pattern for real-time event distribution
- **[Eviction Policy](term_eviction_policy.md)**: Redis provides eight configurable eviction policies (allkeys-lru, allkeys-lfu, volatile-lru, volatile-ttl, etc.) that determine which keys to remove when memory is full
- **[Sharding](term_sharding.md)**: Redis Cluster implements hash-slot-based sharding across nodes, dividing the keyspace into 16,384 hash slots distributed across the cluster
- **[Message Queue](term_message_queue.md)**: Redis Lists and Streams can function as lightweight message queues for task distribution, though dedicated brokers (SQS, RabbitMQ) are preferred for production queue workloads
- **[Microservices Architecture](term_microservices_architecture.md)**: Redis serves as shared state infrastructure in microservices — session store, distributed cache, pub/sub bus, and rate limiter across service boundaries
- **[Rate Limiting](term_rate_limiting.md)**: Redis is the standard backend for distributed rate limiters; atomic INCR operations and TTL-based key expiry enable sliding window and token bucket algorithms
- **[Write-Back Cache](term_write_back_cache.md)**: Redis AOF persistence and replication can mitigate write-back cache data loss risk by providing lightweight durability for deferred database writes
- **[Write-Through Cache](term_write_through_cache.md)**: Redis is commonly used as the cache layer in write-through architectures, where writes go to both Redis and the database synchronously
- **[Graceful Degradation](term_graceful_degradation.md)**: Redis caches serve as a primary fallback mechanism for graceful degradation -- serving cached data from Redis when the origin service is unavailable maintains partial functionality
- **[Memcached](term_memcached.md)**: The primary alternative to Redis for distributed caching — Memcached is a simpler, multi-threaded, volatile string cache that can outperform Redis for pure get/set workloads, while Redis provides richer data structures, persistence, and pub/sub
- **[Latency](term_latency.md)**: Redis achieves sub-millisecond latency for all operations by keeping data entirely in RAM
- **[Throughput](term_throughput.md)**: A single Redis node handles 100K-1M QPS; limited by CPU (single-threaded event loop)

## References

- [Redis Documentation — redis.io](https://redis.io/docs/)
- [Redis — Wikipedia](https://en.wikipedia.org/wiki/Redis)
- [What is Redis? — IBM](https://www.ibm.com/think/topics/redis)
- [Redis vs Memcached — AWS](https://aws.amazon.com/elasticache/redis-vs-memcached/)
- [Redis Sentinel — High Availability](https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/)
- [Redis Cluster Tutorial — Scaling](https://redis.io/tutorials/operate/redis-at-scale/scalability/)
- Carlson, J. (2013). *Redis in Action*. Manning Publications.
