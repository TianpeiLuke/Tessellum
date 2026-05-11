---
tags:
  - resource
  - terminology
  - system_design
  - distributed_systems
  - performance
keywords:
  - throughput
  - QPS
  - queries per second
  - TPS
  - transactions per second
  - requests per second
  - RPS
  - bandwidth
  - capacity
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

# Throughput

## Definition

Throughput is the **amount of work a system completes per unit of time** — the rate at which requests, transactions, or data units are successfully processed. Common units include queries per second (QPS), transactions per second (TPS), requests per second (RPS), and bytes per second for data pipelines. Throughput measures a system's aggregate capacity, in contrast to latency which measures per-request responsiveness.

Throughput and latency are the two fundamental performance metrics in system design. A system optimized for throughput maximizes the total work done (batch processing, data pipelines), while a system optimized for latency minimizes the wait time per request (real-time APIs, user-facing services). The two often trade off against each other — batching increases throughput but adds latency.

## Context

Throughput is the primary capacity planning metric for distributed systems. It determines how many users a system can serve, how much data a pipeline can process, and when horizontal scaling is needed. System design interviews typically frame requirements as "the system must handle X QPS at peak," making throughput the starting point for architecture decisions like database selection, caching strategy, and sharding.

In abuse prevention systems, throughput requirements vary by pipeline: real-time scoring services handle 10K-100K+ QPS (every checkout triggers a risk evaluation), batch scoring pipelines process millions of records per hour, and investigation queries operate at much lower throughput but require complex analytics. The B-tree vs LSM tree storage engine choice is fundamentally a throughput trade-off: B-tree optimizes read throughput, LSM tree optimizes write throughput.

## Key Characteristics

- **Units vary by context**: QPS/RPS for API services, TPS for databases, records/second for batch pipelines, bytes/second (bandwidth) for network and storage — always specify the unit
- **Peak vs sustained**: Systems must handle peak throughput (e.g., Black Friday traffic spikes) which can be 5-10x sustained throughput — capacity planning uses peak estimates with headroom
- **Throughput-latency relationship**: As throughput approaches system capacity, latency increases non-linearly (queuing theory: Little's Law states L = λW where L is queue length, λ is arrival rate, W is wait time) — systems degrade gracefully until a saturation point, then collapse
- **Horizontal scaling for throughput**: Adding more nodes (horizontal scaling) increases aggregate throughput linearly; this is why throughput-constrained systems favor horizontally scalable architectures (NoSQL, microservices)
- **Write throughput vs read throughput**: Most systems have asymmetric read/write throughput — caching amplifies read throughput while write throughput requires sharding or write-optimized storage engines
- **Batching increases throughput**: Amortizing per-request overhead (connection setup, serialization, disk seeks) over multiple items increases throughput at the cost of per-item latency
- **Throughput bottleneck identification**: In a pipeline of components, the component with the lowest throughput is the bottleneck — overall system throughput cannot exceed the bottleneck's capacity (Amdahl's Law analog)
- **Goodput vs throughput**: Goodput is the throughput of successful, non-redundant work — retries, timeouts, and error responses consume throughput without contributing useful work

## Throughput at Different System Tiers

| Tier | Typical Throughput | Limiting Factor |
|------|-------------------|-----------------|
| **Single Redis node** | ~100K-1M QPS | CPU (single-threaded event loop) |
| **PostgreSQL (read)** | ~10K-50K QPS | Disk I/O, connection pool |
| **PostgreSQL (write)** | ~1K-10K TPS | WAL fsync, lock contention |
| **Cassandra cluster** | ~100K-1M writes/s | Linear with nodes (LSM tree) |
| **Kafka cluster** | ~1M-10M msgs/s | Disk sequential I/O, network |
| **DynamoDB** | Virtually unlimited | Provisioned or on-demand capacity |
| **Load balancer (L4)** | ~1M-10M RPS | Network bandwidth, connection tracking |

## Related Terms

- **[TPS](term_tps.md)**: Transactions Per Second — the most common throughput unit in buyer abuse systems for model deployments, URES evaluations, and capacity planning
- **[Latency](term_latency.md)**: The complementary performance metric — time per request; throughput measures aggregate rate, latency measures individual wait time
- **[Scalability](term_scalability.md)**: A system's ability to increase throughput by adding resources (vertical or horizontal scaling)
- **[SLO](term_slo.md)**: Service Level Objectives may include throughput targets alongside latency percentiles
- **[SLI](term_sli.md)**: Throughput (requests/second, error rate) as a Service Level Indicator for capacity monitoring
- **[SAR](term_sar.md)**: Scalability, Availability, Reliability — throughput is the primary measure under the Scalability dimension
- **[Load Balancer](term_load_balancer.md)**: Distributes requests across servers to maximize aggregate throughput
- **[Sharding](term_sharding.md)**: Horizontal data partitioning to increase write throughput beyond single-node limits
- **[Database Replication](term_database_replication.md)**: Read replicas increase read throughput; write throughput requires sharding
- **[LSM Tree](term_lsm_tree.md)**: Write-optimized storage engine that maximizes write throughput via sequential I/O
- **[B-Tree](term_b_tree.md)**: Read-optimized storage engine that maximizes read throughput via in-place index lookups
- **[Storage Engine](term_storage_engine.md)**: B-tree vs LSM tree choice is fundamentally a read throughput vs write throughput trade-off
- **[Rate Limiting](term_rate_limiting.md)**: Caps per-client throughput to protect overall system capacity and fairness
- **[Batch Processing](term_batch_processing.md)**: Maximizes throughput by processing data in bulk — trades latency for aggregate processing rate
- **[Message Queue](term_message_queue.md)**: Decouples producers and consumers to smooth throughput spikes and prevent backpressure
- **[In-Memory Database](term_in_memory_database.md)**: Achieves highest throughput by eliminating disk I/O from the data path
- **[Key-Value Store](term_key_value_store.md)**: Highest throughput database category due to O(1) operations and simple data model
- **[RDBMS](term_rdbms.md)**: Write throughput limited by ACID overhead (WAL, locking); read throughput strong with B-tree indexes
- **[Availability](term_availability.md)**: Throughput collapse (system unable to process requests) is an availability failure
- **[OLTP](term_oltp.md)**: Transaction throughput (TPS) is the primary metric for OLTP workloads
- **[Leader-Based Replication](term_leader_based_replication.md)**: Write throughput bottlenecked at the single leader; read throughput scales with replicas
- **[Leaderless Replication](term_leaderless_replication.md)**: Write throughput scales with nodes since any node accepts writes

## References

- [Digest: SAR — Scalability, Availability, Reliability (Episode 13)](../digest/digest_sddd_sar_podcast.md) — throughput as the primary scalability capacity metric
- [Digest: How to Pick a Database (Episode 3)](../digest/digest_sddd_database_selection_podcast.md) — read/write throughput as the key workload characteristic for database selection
- [Digest: Scale Your System with Database Sharding (Episode 6)](../digest/digest_sddd_sharding_podcast.md) — sharding as the primary strategy for scaling write throughput
- [Digest: Everything to Know About Replication (Episode 7)](../digest/digest_sddd_replication_podcast.md) — replication for scaling read throughput; leader bottleneck for writes
- [Little's Law (Wikipedia)](https://en.wikipedia.org/wiki/Little%27s_law) — L = λW: the fundamental relationship between throughput, latency, and queue depth
