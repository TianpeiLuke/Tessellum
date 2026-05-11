---
tags:
  - resource
  - terminology
  - distributed_systems
  - database
  - computer_science
keywords:
  - availability
  - high availability
  - fault tolerance
  - uptime
  - SLA
  - distributed systems
topics:
  - distributed database design
  - system reliability
language: markdown
date of note: 2026-04-17
status: active
building_block: concept
related_wiki: null
---

# Availability - System Availability in Distributed Systems

## Definition

In the context of the CAP theorem, availability means that every request to a non-failing node receives a response, without guarantee that it contains the most recent write. An available system never refuses to answer — it may return stale data, but it always responds. This is distinct from "high availability" in software engineering (measured as uptime percentage, e.g., 99.99%), though the concepts are related: CAP availability is a theoretical guarantee about response behavior, while high availability is an operational metric.

## Context

Availability is one of the three properties in the CAP theorem. AP (availability + partition tolerance) systems like DynamoDB and Cassandra prioritize responding to every request even during network partitions, accepting that some responses may be stale. In Amazon's infrastructure, availability is critical for customer-facing services where a timeout or error is worse than slightly stale data. For abuse prevention systems, availability ensures that risk scoring and enforcement decisions are always made, even if the underlying data is momentarily behind.

## Key Characteristics

- **CAP availability**: Every request to a non-failing node gets a response — a theoretical guarantee, not a percentage
- **High availability (operational)**: Measured as uptime (e.g., 99.99% = 52 minutes downtime/year) — an SLA metric
- **AP systems**: Cassandra, DynamoDB (default mode), CouchDB — always respond, may serve stale data
- **Replication**: Availability is achieved by replicating data across multiple nodes so that if one fails, others can serve requests
- **Failover**: Automatic switching to a standby node when the primary fails — a mechanism for achieving high availability
- **Trade-off with consistency**: During a network partition, an available system serves potentially stale data rather than returning an error
- **Graceful degradation**: Systems may reduce functionality (e.g., serve cached data) rather than become fully unavailable

## Related Terms

- **[CAP Theorem](term_cap_theorem.md)**: The impossibility theorem where availability is one of three properties
- **[Consistency](term_consistency.md)**: The CAP property traded against availability during network partitions
- **[Partition Tolerance](term_partition_tolerance.md)**: The CAP property that makes the C-vs-A trade-off necessary
- **[DynamoDB](term_ddb.md)**: AP-oriented key-value store — prioritizes availability with eventual consistency by default
- **[Microservices Architecture](term_microservices_architecture.md)**: Distributed architecture where each service must make its own availability trade-offs
- **[Space-Based Architecture](term_space_based_architecture.md)**: Achieves high availability through in-memory data replication
- **[OLTP](term_oltp.md)**: Transaction systems where availability must be balanced against consistency requirements
- **[ACID](term_acid.md)**: Transaction model that may sacrifice availability for consistency guarantees

- **[FLP Impossibility](term_flp_impossibility.md)**: FLP's liveness impossibility directly impacts availability
- **[SAR](term_sar.md)**: Scalability, Availability, Reliability framework — broadens CAP availability into an operational metric measured in nines, with the MTBF/MTTR formula and SLA/SLO/SLI hierarchy
- **[Cassandra](term_cassandra.md)**: Cassandra's masterless architecture ensures high availability -- the cluster continues serving requests even when multiple nodes fail
- **[Database Replication](term_database_replication.md)**: Replication is the primary mechanism for achieving high availability -- redundant copies allow failover when nodes fail
- **[PostgreSQL](term_postgresql.md)**: Streaming replication and tools like Patroni provide high availability for PostgreSQL clusters

- **[API Gateway](term_api_gateway.md)**: The gateway's own availability directly bounds the system's overall availability — it must be deployed in HA configurations
- **[CDN (Content Delivery Network)](term_cdn.md)**: CDNs improve system availability by serving cached content even when the origin is unreachable; edge redundancy provides geographic fault tolerance
- **[Circuit Breaker](term_circuit_breaker.md)**: Circuit breakers preserve overall system availability by isolating failing dependencies and enabling graceful degradation rather than total outage
- **[Consistent Hashing](term_consistent_hashing.md)**: Consistent hashing improves availability by minimizing disruption during node failures, ensuring only a fraction of keys are affected
- **[Load Balancer](term_load_balancer.md)**: Load balancers directly improve system availability by detecting unhealthy backends via health checks and redistributing traffic to healthy nodes
- **[Chaos Engineering](term_chaos_engineering.md)**: Validates availability guarantees by testing whether the system remains accessible during component failures
- **[Error Budget](term_error_budget.md)**: Error budget caps the allowed unavailability — `Availability = MTBF / (MTBF + MTTR)` determines how much error budget each incident consumes
- **[Failover](term_failover.md)**: The system property that failover directly enables; measured in nines where each additional nine demands more sophisticated failover strategies
- **[Graceful Degradation](term_graceful_degradation.md)**: The primary mechanism for maintaining high availability during partial failures — the system stays up even when components are down
- **[Health Check](term_health_check.md)**: Health checks are the primary mechanism for maintaining high availability by detecting failures and routing traffic around them
- **[MTBF](term_mtbf.md)**: System uptime measured in nines is directly computed from MTBF and MTTR via the availability formula A = MTBF / (MTBF + MTTR)
- **[MTTR](term_mttr.md)**: System uptime is directly computed from MTTR via A = MTBF / (MTBF + MTTR); reducing MTTR is the most effective lever for improving availability
- **[SLI](term_sli.md)**: Availability is one of the most common SLI types — availability SLI = successful requests / total requests
- **[Round Robin](term_round_robin.md)**: Round Robin improves system availability by distributing load across servers; combined with health checks, failed servers are removed from rotation
- **[Scalability](term_scalability.md)**: Highly available systems often require horizontal scaling with redundancy; scalability enables availability by ensuring capacity to absorb failures
- **[NGINX](term_nginx.md)**: NGINX improves availability through reverse proxying, health checks, and load balancing — routing around failed backends automatically
- **[PACELC](term_pacelc.md)**: PACELC extends CAP availability analysis to include the latency-consistency trade-off even when no partition exists
- **[REST](term_rest.md)**: Stateless REST APIs improve availability by eliminating server-side session state, allowing any healthy node to handle any request
- **[Session Persistence](term_session_persistence.md)**: Sticky sessions can compromise availability when pinned servers fail, as all sessions bound to that server are lost
- **[SLO](term_slo.md)**: Availability is one of the most common SLO types; measured in nines and linked to MTBF/MTTR via the availability formula
- **[Redundancy](term_redundancy.md)**: Redundancy is the foundation of high availability -- deploying duplicate components (servers, databases, network paths) ensures the system continues operating when individual components fail
- **[Active-Passive](term_active_passive.md)**: A high-availability pattern where a standby replica monitors the primary and takes over via failover when the primary fails, providing availability through warm/hot standby
- **[Latency](term_latency.md)**: High availability requires bounded latency — a system that responds but takes minutes is effectively unavailable
- **[Throughput](term_throughput.md)**: Throughput collapse (system unable to process requests) is an availability failure

## References

- [CAP Theorem — Wikipedia](https://en.wikipedia.org/wiki/CAP_theorem)
- [High Availability — AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/availability.html)
- Brewer, E. (2000). "Towards Robust Distributed Systems." PODC keynote.
