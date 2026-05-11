---
tags:
  - resource
  - terminology
  - system_design
  - distributed_systems
  - performance
keywords:
  - latency
  - response time
  - p50
  - p95
  - p99
  - tail latency
  - round-trip time
  - RTT
  - sub-millisecond
  - percentile latency
topics:
  - System Design
  - Performance Engineering
  - Distributed Systems
language: markdown
date of note: 2026-04-20
status: active
building_block: concept
related_wiki: null
---

# Latency

## Definition

Latency is the **time elapsed between initiating a request and receiving the response** — the duration a user or system waits for a single operation to complete. In distributed systems, latency is the primary measure of responsiveness and is reported as percentile distributions (p50, p95, p99) rather than averages, because averages hide the experience of the worst-affected users.

Latency and throughput are the two fundamental performance metrics in system design. While throughput measures how much work a system can handle per unit time, latency measures how long each unit of work takes. The two are related but not interchangeable — a system can have high throughput but high latency (batch processing), or low latency but low throughput (single-threaded in-memory cache).

## Context

Latency is a first-class design constraint in every tier of a distributed architecture: network latency between services, disk I/O latency in storage engines, query latency in databases, and end-to-end latency experienced by users. SLOs (Service Level Objectives) are typically defined in terms of latency percentiles — e.g., "p99 response time < 200ms."

In abuse prevention systems, latency constraints are critical because scoring decisions must complete within the checkout or API request path. Real-time abuse scoring requires sub-100ms latency, driving architectural choices like in-memory caches (Redis), pre-computed feature stores, and edge-deployed models. Investigation-time queries can tolerate higher latency (seconds to minutes).

## Key Characteristics

- **Percentile reporting**: Latency is measured as p50 (median), p95, p99, and p99.9 percentiles — p99 captures the experience of the 1% worst-affected requests, which often correspond to the most valuable customers
- **Tail latency amplification**: In fan-out architectures where a single user request touches N backend services, the overall latency is bounded by the slowest service — even a 1% slow path (p99) affects most users when N is large
- **Components of latency**: Total latency = network RTT + queuing delay + processing time + serialization/deserialization — each component can be optimized independently
- **Network latency floor**: Speed of light imposes a minimum ~1ms per 200km of fiber; cross-region calls add 50-150ms of irreducible network latency
- **Latency vs response time**: Strictly, latency is the time before any response begins (time-to-first-byte), while response time includes the full transfer — in practice the terms are used interchangeably
- **Latency-throughput trade-off**: Batching increases throughput by amortizing overhead but adds latency (wait time to fill the batch) — tuning the batch size balances this trade-off
- **Caching reduces latency**: Moving data closer to the requester (CDN, application cache, in-memory database) reduces latency by eliminating slower data paths
- **Consistency-latency trade-off**: Strong consistency (synchronous replication) adds latency; eventual consistency (async replication) reduces latency at the cost of stale reads — formalized in the PACELC theorem

## Latency at Different System Tiers

| Tier | Typical Latency | Example |
|------|----------------|---------|
| **L1 cache reference** | ~1 ns | CPU cache hit |
| **RAM access** | ~100 ns | In-memory database read |
| **SSD random read** | ~100 μs | B-tree index lookup |
| **HDD random read** | ~10 ms | Sequential scan on spinning disk |
| **Same-datacenter RTT** | ~0.5 ms | Service-to-service call |
| **Cross-region RTT** | ~50-150 ms | US-East to EU-West |
| **DNS resolution** | ~10-50 ms | First request to new domain |

## Related Terms

- **[Throughput](term_throughput.md)**: The complementary performance metric — work completed per unit time; latency measures per-request time, throughput measures aggregate capacity
- **[TPS](term_tps.md)**: Complementary metric — TPS measures aggregate throughput rate while latency measures per-request time; Little's Law connects them
- **[SLO](term_slo.md)**: Service Level Objectives are typically defined as latency percentile targets (e.g., p99 < 200ms)
- **[SLI](term_sli.md)**: Service Level Indicators — latency percentiles are the most common SLI type for request-driven services
- **[SAR](term_sar.md)**: Scalability, Availability, Reliability framework — latency is the primary quality target under the Scalability dimension
- **[Quantile](term_quantile.md)**: The statistical concept underlying percentile latency reporting (p50, p95, p99)
- **[CDN](term_cdn.md)**: Content Delivery Networks reduce latency by serving content from edge locations closer to users
- **[Cache-Aside](term_cache_aside.md)**: Caching pattern that reduces read latency by serving from in-memory cache instead of database
- **[In-Memory Database](term_in_memory_database.md)**: RAM-resident databases achieve sub-millisecond latency by eliminating disk I/O
- **[Load Balancer](term_load_balancer.md)**: Distributes requests to reduce latency by avoiding overloaded servers
- **[Rate Limiting](term_rate_limiting.md)**: Protects latency for well-behaved clients by throttling excessive requests
- **[B-Tree](term_b_tree.md)**: Read-optimized storage engine with O(log n) lookup latency; the default for latency-sensitive read workloads
- **[LSM Tree](term_lsm_tree.md)**: Write-optimized storage engine that trades read latency for write throughput
- **[PACELC](term_pacelc.md)**: Theorem formalizing the consistency-latency trade-off: even without network partitions, systems trade latency for consistency
- **[Replication Lag](term_replication_lag.md)**: The latency between a write on the leader and its visibility on replicas — a direct measure of staleness
- **[MTTR](term_mttr.md)**: Mean Time to Recovery — a latency metric for failure recovery rather than normal operations
- **[Scalability](term_scalability.md)**: A system's ability to maintain latency targets as load increases
- **[Availability](term_availability.md)**: High availability requires bounded latency — a system that responds but takes minutes is effectively unavailable
- **[Key-Value Store](term_key_value_store.md)**: Achieves the lowest database read latency via O(1) hash-based lookups
- **[Batch Processing](term_batch_processing.md)**: Sacrifices latency for throughput — processes data in bulk with higher end-to-end delay

## References

- [Digest: SAR — Scalability, Availability, Reliability (Episode 13)](../digest/digest_sddd_sar_podcast.md) — latency as the primary scalability quality target; SLO definition
- [Digest: How to Pick a Database (Episode 3)](../digest/digest_sddd_database_selection_podcast.md) — benchmark latency at p50, p95, p99 for database selection
- [Digest: Everything to Know About Caching (Episode 4)](../digest/digest_sddd_caching_podcast.md) — caching as the primary latency reduction strategy
- [Jeff Dean — Numbers Every Programmer Should Know](https://brenocon.com/dean_perf.html) — canonical latency reference table for system designers
