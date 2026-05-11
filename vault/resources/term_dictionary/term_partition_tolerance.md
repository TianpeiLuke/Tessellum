---
tags:
  - resource
  - terminology
  - distributed_systems
  - database
  - computer_science
  - networking
keywords:
  - partition tolerance
  - network partition
  - split brain
  - distributed systems
  - fault tolerance
topics:
  - distributed database design
  - network reliability
language: markdown
date of note: 2026-04-17
status: active
building_block: concept
related_wiki: null
---

# Partition Tolerance - Network Partition Tolerance in Distributed Systems

## Definition

In the context of the CAP theorem, partition tolerance means that the system continues to operate despite arbitrary message loss or delay between nodes in the network. A network partition occurs when a communication break divides the cluster into two or more groups that cannot reach each other. A partition-tolerant system must continue functioning (either consistently or availably) even when some nodes cannot communicate. Since network partitions are inevitable in any distributed system spanning multiple machines, data centers, or regions, partition tolerance is effectively non-negotiable — making the real CAP choice between consistency and availability.

## Context

Network partitions occur in practice due to switch failures, cable cuts, DNS issues, cloud availability zone outages, or cross-region latency spikes. In Amazon's infrastructure, services are designed to tolerate partitions across availability zones (AZs) within a region and across regions globally. For ML pipeline infrastructure, partition tolerance is relevant when data loading steps pull from distributed data sources (Redshift, S3, DynamoDB) that may experience transient network issues — the pipeline must handle these gracefully rather than failing silently.

## Key Characteristics

- **Non-negotiable in practice**: Any system running on a network can experience partitions — the question is not "if" but "when"
- **Split brain**: When a partition divides a cluster, each side may independently accept writes, leading to conflicting data — a key challenge partition-tolerant systems must address
- **Partition detection**: Systems use heartbeats, timeouts, and gossip protocols to detect when nodes become unreachable
- **Partition recovery**: After a partition heals, the system must reconcile divergent state — strategies include last-write-wins, vector clocks, and conflict-free replicated data types (CRDTs)
- **CP during partition**: System rejects writes/reads to maintain consistency (e.g., leader-based systems that refuse requests when the leader is unreachable)
- **AP during partition**: System continues serving requests from both sides, accepting temporary inconsistency
- **Multi-region replication**: Cross-region deployments face higher partition probability due to longer network paths

## Related Terms

- **[CAP Theorem](term_cap_theorem.md)**: The impossibility theorem where partition tolerance is one of three properties
- **[Consistency](term_consistency.md)**: The CAP property that may be sacrificed to maintain availability during partitions
- **[Availability](term_availability.md)**: The CAP property that may be sacrificed to maintain consistency during partitions
- **[DynamoDB](term_ddb.md)**: Designed to tolerate partitions across AZs with automatic failover
- **[Microservices Architecture](term_microservices_architecture.md)**: Each service boundary is a potential partition point
- **[Space-Based Architecture](term_space_based_architecture.md)**: Handles partitions through in-memory data grids with replication
- **[Neptune](term_neptune.md)**: Multi-AZ graph database with automatic failover during partitions
- **[ETL](term_etl.md)**: Data pipelines must handle transient network partitions between source and destination

- **[FLP Impossibility](term_flp_impossibility.md)**: Partitioned nodes are indistinguishable from crashed ones — the ambiguity FLP exploits

- **[Health Check](term_health_check.md)**: Network partitions can cause health check probes to timeout, creating false-negative health assessments that incorrectly remove healthy nodes from rotation
- **[PACELC](term_pacelc.md)**: PACELC extends the partition tolerance trade-off by adding the latency-consistency trade-off during normal (non-partitioned) operation
- **[CDN (Content Delivery Network)](term_cdn.md)**: CDN design inherently handles network partitions; edge servers continue serving cached content independently of origin connectivity
- **[Consistent Hashing](term_consistent_hashing.md)**: Consistent hashing supports partition-tolerant designs by enabling each node to independently compute key ownership without a central coordinator
- **[Load Balancer](term_load_balancer.md)**: Load balancers help systems tolerate network partitions by routing traffic only to reachable, healthy nodes within a partition
- **[Round Robin](term_round_robin.md)**: Round Robin does not handle network partitions between load balancer and backends; health checks serve as the partition detection mechanism
- **[Session Persistence](term_session_persistence.md)**: Session data must survive server isolation during partitions; session replication strategies are governed by partition tolerance requirements
- **[BASE](term_base.md)**: BASE systems choose availability over consistency during partitions, making partition tolerance the CAP property that motivates the BASE model
- **[Cache Invalidation](term_cache_invalidation.md)**: Network partitions make coordinated invalidation across distributed caches unreliable, forcing tolerance of stale data
- **[Database Replication](term_database_replication.md)**: Replication across nodes makes partition tolerance possible but forces the consistency-availability trade-off
## References

- [CAP Theorem — Wikipedia](https://en.wikipedia.org/wiki/CAP_theorem)
- [Network Partition — Wikipedia](https://en.wikipedia.org/wiki/Network_partition)
- Brewer, E. (2012). "CAP Twelve Years Later: How the 'Rules' Have Changed." IEEE Computer, 45(2), 23–29.
