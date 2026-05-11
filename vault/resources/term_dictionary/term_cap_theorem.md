---
tags:
  - resource
  - terminology
  - distributed_systems
  - database
  - computer_science
  - system_design
keywords:
  - CAP theorem
  - Brewer's theorem
  - consistency
  - availability
  - partition tolerance
  - distributed systems
  - trade-off
  - CP system
  - AP system
topics:
  - distributed database design
  - system design trade-offs
  - data consistency models
language: markdown
date of note: 2026-04-17
status: active
building_block: concept
related_wiki: null
---

# CAP Theorem - Brewer's Theorem

## Definition

The CAP theorem, introduced by Eric Brewer in 2000 and formally proved by Seth Gilbert and Nancy Lynch in 2002, states that a distributed data store can guarantee at most two of three properties simultaneously: Consistency (every read returns the most recent write), Availability (every request receives a non-error response), and Partition Tolerance (the system continues operating despite arbitrary message loss between nodes). Since network partitions are inevitable in distributed systems, the practical choice reduces to CP (consistent but may reject requests during partitions) or AP (available but may return stale data during partitions).

## Context

The CAP theorem is a foundational concept in distributed systems design and is frequently referenced in system design interviews, database selection decisions, and architecture reviews. In the context of Amazon's infrastructure, services like DynamoDB are designed as AP systems (favoring availability with eventual consistency), while systems requiring strong consistency (e.g., transactional databases) operate as CP systems. For ML pipeline infrastructure, understanding CAP trade-offs is relevant when designing data ingestion pipelines, feature stores, and model registries that must balance freshness against availability.

## Key Characteristics

- **Impossible trinity**: No distributed system can simultaneously guarantee all three properties — designers must choose which two to prioritize
- **Partition tolerance is non-negotiable**: In real-world networks, partitions happen; the real choice is between C and A during a partition
- **CP systems**: Sacrifice availability for consistency — return errors or timeouts rather than stale data (e.g., HBase, MongoDB with strong read concern, ZooKeeper)
- **AP systems**: Sacrifice consistency for availability — return potentially stale data but always respond (e.g., DynamoDB, Cassandra, CouchDB)
- **Eventual consistency**: A common AP compromise where the system guarantees that, given enough time without new updates, all replicas converge to the same value
- **PACELC extension**: Eric Brewer later noted that even when there is no partition (P), there is still a trade-off between latency (L) and consistency (C) — extending CAP to PACELC
- **Not binary**: Modern systems often allow tunable consistency levels per operation (e.g., DynamoDB's strongly consistent reads vs eventually consistent reads)

## Related Terms

- **[DynamoDB](term_ddb.md)**: Amazon's AP-oriented key-value store — exemplifies availability-first design with optional strong consistency
- **[Redshift](term_redshift.md)**: Amazon's data warehouse — CP-oriented for analytical queries requiring consistent snapshots
- **[Neptune](term_neptune.md)**: Graph database — consistency model relevant for knowledge graph queries
- **[SQL](term_sql.md)**: Relational query language — traditionally associated with ACID (strong consistency) databases
- **[OLTP](term_oltp.md)**: Online transaction processing — requires strong consistency (CP trade-off)
- **[Microservices Architecture](term_microservices_architecture.md)**: Distributed architecture pattern where CAP trade-offs arise at every service boundary
- **[Space-Based Architecture](term_space_based_architecture.md)**: Architecture pattern that addresses CAP by replicating data in-memory across nodes
- **[ETL](term_etl.md)**: Extract-Transform-Load — data pipeline pattern where consistency vs availability trade-offs affect data freshness
- **[SAR](term_sar.md)**: Scalability, Availability, Reliability framework — the CAP availability-consistency trade-off is a specific instance of the SAR reliability-availability tension
- **[Knowledge Graph](term_knowledge_graph.md)**: Graph-structured data store where CAP applies to distributed graph queries
- **[Vector Database](term_vector_database.md)**: Similarity search stores — AP-oriented for low-latency nearest neighbor queries
- **[Data Lakehouse](term_data_lakehouse.md)**: Hybrid storage architecture balancing consistency (ACID transactions) with availability (distributed storage)

- **[FLP Impossibility](term_flp_impossibility.md)**: More fundamental than CAP — proves consensus itself is impossible in async systems with one fault
- **[Amdahl's Law](term_amdahls_law.md)**: Another fundamental limitation result — CAP limits distributed stores, Amdahl's limits parallel speedup
- **[MongoDB](term_mongodb.md)**: Document-oriented NoSQL database — CP system, strong consistency via single-primary replica sets
- **[NoSQL](term_nosql.md)**: NoSQL databases explicitly navigate CAP trade-offs (AP vs CP)
- **[Consistency](term_consistency.md)**: One of the three CAP properties
- **[Availability](term_availability.md)**: One of the three CAP properties
- **[Partition Tolerance](term_partition_tolerance.md)**: One of the three CAP properties
- **[B-Tree](term_b_tree.md)**: B-Tree databases traditionally operate as CP systems with strong consistency
- **[Cassandra](term_cassandra.md)**: Cassandra is an AP system -- prioritizes availability and partition tolerance with tunable consistency per operation
- **[Database Replication](term_database_replication.md)**: Replication is the mechanism that delivers availability and partition tolerance -- the CAP trade-off determines consistency behavior during partitions
- **[PostgreSQL](term_postgresql.md)**: Single-node PostgreSQL is CP by default; distributed extensions make different trade-offs
- **[Sharding](term_sharding.md)**: Sharded systems must navigate the CAP trade-off -- partitions between shards force a choice between consistency and availability
- **[Two-Phase Commit](term_two_phase_commit.md)**: 2PC is a CP protocol -- it guarantees consistency across distributed participants at the cost of availability, blocking if the coordinator fails during a partition
- **[Saga Pattern](term_saga_pattern.md)**: Sagas are an AP approach to distributed transactions -- they maintain availability by using compensating actions instead of global locks, accepting eventual consistency

- **[API Gateway](term_api_gateway.md)**: Gateway routing decisions interact with consistency-availability trade-offs across partitioned services
- **[CDN (Content Delivery Network)](term_cdn.md)**: CDNs prioritize Availability and Partition Tolerance over strong Consistency; cached content may be stale during TTL windows
- **[HAProxy](term_haproxy.md)**: HAProxy's health checks and failover mechanisms are practical implementations of availability guarantees in the face of partition tolerance
- **[NGINX](term_nginx.md)**: NGINX load balancing decisions interact with CAP trade-offs -- IP hash provides session consistency while round robin maximizes availability
- **[Reverse Proxy](term_reverse_proxy.md)**: Reverse proxies with caching introduce consistency-availability trade-offs (stale cache vs backend availability)
- **[Round Robin](term_round_robin.md)**: Distributed systems behind a Round Robin load balancer still face CAP trade-offs; consistent hashing addresses partition tolerance more gracefully
- **[Session Persistence](term_session_persistence.md)**: CAP trade-offs govern session replication strategies -- consistency requires synchronous replication while availability favors local session state
- **[Circuit Breaker](term_circuit_breaker.md)**: Circuit breakers implement an availability-favoring strategy during partition-like conditions — returning fallback responses instead of waiting for unreachable dependencies
- **[Consistent Hashing](term_consistent_hashing.md)**: Key mechanism in AP systems (like DynamoDB and Cassandra) that choose availability over strict consistency during partitions
- **[Load Balancer](term_load_balancer.md)**: Load balancers are a primary mechanism for achieving the Availability guarantee in CAP — distributing traffic and rerouting around failures
- **[Chaos Engineering](term_chaos_engineering.md)**: Chaos engineering tests CAP trade-offs by injecting network partitions and observing whether the system correctly chooses consistency or availability
- **[Error Budget](term_error_budget.md)**: The consistency-availability trade-off in distributed stores; error budget quantifies how much availability can be sacrificed for consistency-preserving operations
- **[Failover](term_failover.md)**: During network partitions, failover forces the CP vs AP trade-off — failover to a stale replica sacrifices consistency for availability
- **[Graceful Degradation](term_graceful_degradation.md)**: AP systems inherently employ graceful degradation by returning potentially stale data rather than errors during partitions
- **[Health Check](term_health_check.md)**: Health checks interact with CAP trade-offs — during a partition, a health check timeout may incorrectly mark a consistent (CP) node as unhealthy
- **[SLI](term_sli.md)**: The consistency-availability trade-off determines which SLIs are prioritized — CP systems prioritize correctness SLIs, AP systems prioritize availability SLIs
- **[SLO](term_slo.md)**: The CAP availability-consistency trade-off directly affects what SLOs a distributed data store can realistically commit to
- **[Message Queue](term_message_queue.md)**: Asynchronous messaging enables AP-style designs by decoupling producers from consumers and absorbing partition-induced delays
- **[PACELC](term_pacelc.md)**: PACELC extends CAP by adding the latency-consistency trade-off when no partition exists — if Partition, trade A vs C; Else, trade L vs C
- **[Pub/Sub](term_pub_sub.md)**: Pub/Sub systems face CAP trade-offs — message ordering vs availability during broker partitions
- **[Rate Limiting](term_rate_limiting.md)**: Distributed rate limiters face CAP trade-offs: strong consistency across nodes vs. availability when the shared state store is partitioned
- **[REST](term_rest.md)**: Stateless REST APIs simplify availability in distributed systems; caching introduces consistency trade-offs governed by CAP
- **[Scalability](term_scalability.md)**: Scaling distributed systems horizontally introduces more partition points, making CAP trade-offs increasingly relevant at each service boundary
- **[WebSocket](term_websocket.md)**: WebSocket-based real-time systems must choose between strong and eventual consistency for message delivery across distributed nodes during partitions
- **[Write-Back Cache](term_write_back_cache.md)**: Write-back caching trades consistency for availability and low latency — dirty cache entries may be lost during partitions before flushing to the database
- **[Write-Through Cache](term_write_through_cache.md)**: Write-through caching provides strong consistency between cache and database at the cost of higher write latency, reflecting the CAP consistency-latency trade-off
- **[Fault Tolerance](term_fault_tolerance.md)**: Fault tolerance relates to partition tolerance in CAP — a fault-tolerant system must handle network partitions gracefully, choosing between consistency and availability when faults occur
- **[Latency](term_latency.md)**: CAP theorem's partition tolerance forces a consistency-availability choice; PACELC extends this to include the latency trade-off in normal operation
- **[TPS](term_tps.md)**: At high TPS, network partitions force a choice between consistency and availability

## References

- [CAP Theorem — Wikipedia](https://en.wikipedia.org/wiki/CAP_theorem)
- Brewer, E. (2000). "Towards Robust Distributed Systems." ACM Symposium on Principles of Distributed Computing (PODC) keynote.
- Gilbert, S. & Lynch, N. (2002). "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services." ACM SIGACT News, 33(2), 51–59.
- [Brewer's CAP Theorem — GeeksforGeeks](https://www.geeksforgeeks.org/brewers-cap-theorem/)
