---
tags:
  - resource
  - terminology
  - distributed_systems
  - databases
  - consensus_protocols
  - transaction_management
keywords:
  - 2PC
  - Two-Phase Commit
  - two-phase commit protocol
  - distributed transactions
  - atomic commitment
  - prepare-commit
  - coordinator
  - participant
  - blocking protocol
topics:
  - Distributed Systems
  - Database Transaction Management
  - Consensus Protocols
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
related_wiki: null
---

# 2PC - Two-Phase Commit

## Definition

**Two-Phase Commit (2PC)** is a distributed consensus protocol that coordinates all participants in a distributed transaction to agree on whether to commit or abort, ensuring atomicity across multiple database nodes or services. Developed by Jim Gray in 1978, it is the foundational atomic commitment protocol used when a single logical transaction spans multiple independent data stores that each maintain their own durability guarantees.

The protocol operates in two phases: a **Prepare phase** (Phase 1) where the coordinator asks each participant to vote YES (prepared to commit) or NO (must abort), and a **Commit phase** (Phase 2) where the coordinator broadcasts a global COMMIT (if all voted YES) or ABORT (if any voted NO). Each participant must durably log its vote before responding, ensuring crash recovery can determine the correct outcome.

## Context

2PC is relevant across any distributed data system that requires strong consistency guarantees:

- **Sharded databases**: When a transaction touches rows on multiple shards (cross-shard transactions), 2PC ensures either all shards commit or all abort. This is the primary mechanism for ACID transactions in sharded MySQL (via Vitess), PostgreSQL (via Citus), and Google Spanner.
- **Microservices architectures**: When a business operation spans multiple services with independent databases, 2PC can coordinate the distributed transaction — though modern architectures often prefer the Saga pattern due to 2PC's blocking nature.
- **Distributed databases**: Systems like Google Spanner, CockroachDB, and TiDB implement variants of 2PC (often combined with Paxos or Raft) for cross-partition transactions.
- **Message brokers**: Apache Kafka's transactional API uses a variant of 2PC to coordinate exactly-once semantics across producer writes and consumer offset commits.

## Key Characteristics

- **Atomicity guarantee**: All participants commit or all abort — no partial commits are possible, preserving the "A" in ACID across distributed nodes
- **Blocking protocol**: If the coordinator crashes after collecting votes but before broadcasting the decision, participants that voted YES are stuck holding locks indefinitely until the coordinator recovers; this is the fundamental weakness of 2PC
- **Write-Ahead Logging (WAL)**: Both coordinator and participants durably log protocol state transitions (PREPARE, COMMIT, ABORT) before sending messages, enabling crash recovery
- **Two-round communication**: Requires 2 round-trips between coordinator and all participants (prepare + commit), adding latency proportional to the slowest participant
- **Coordinator as single point of failure**: The coordinator is the bottleneck — its failure blocks all participants; Three-Phase Commit (3PC) was designed to address this but adds complexity and a third round-trip
- **Lock contention under high concurrency**: Participants hold exclusive locks on affected rows from PREPARE until COMMIT/ABORT, increasing contention and reducing throughput in high-concurrency workloads
- **Not partition-tolerant**: In the presence of network partitions, 2PC cannot make progress — it sacrifices availability for consistency (CP in CAP theorem terms)

## Related Terms

- **[ACID](term_acid.md)**: The set of transaction properties (Atomicity, Consistency, Isolation, Durability) that 2PC enforces across distributed nodes; 2PC is the mechanism that extends ACID from single-node to multi-node transactions
- **[BASE](term_base.md)**: The alternative consistency model (Basically Available, Soft state, Eventually consistent) that relaxes ACID guarantees; systems choosing BASE over ACID typically use Saga patterns instead of 2PC
- **[Saga Pattern](term_saga_pattern.md)**: The non-blocking alternative to 2PC for distributed transactions; uses compensating transactions instead of distributed locks, trading strong consistency for availability
- **[Sharding](term_sharding.md)**: Horizontal data partitioning that creates the need for 2PC when transactions cross shard boundaries; the sharding digest identifies "design for single-shard transactions" as the primary mitigation for 2PC overhead
- **[CAP Theorem](term_cap_theorem.md)**: The impossibility result constraining distributed systems; 2PC is a CP protocol that sacrifices availability during coordinator failure or network partitions
- **[PACELC](term_pacelc.md)**: Extension of CAP that adds latency-consistency trade-off during normal operation; 2PC incurs latency cost (two round-trips) to achieve strong consistency even when no partitions exist
- **[FLP Impossibility](term_flp_impossibility.md)**: The theoretical result proving no deterministic consensus protocol can guarantee termination in asynchronous systems with even one crash failure; 2PC's blocking behavior is a direct consequence of FLP
- **[Consistent Hashing](term_consistent_hashing.md)**: The algorithm used to assign data to shards; determines which shards a transaction touches and thus whether 2PC is needed
- **[Write-Ahead Log](term_write_ahead_log.md)**: The durability mechanism that both coordinator and participants use to log 2PC state transitions before sending messages, enabling crash recovery
- **[Database Replication](term_database_replication.md)**: Replication across nodes for read scalability and durability; 2PC coordinates writes across replicas when strong consistency is required (synchronous replication)
- **[Kafka](term_kafka.md)**: Apache Kafka's transactional API uses a variant of 2PC to coordinate exactly-once semantics across producer writes and consumer offset commits
- **[Microservices Architecture](term_microservices_architecture.md)**: The architectural style where services own their data stores, creating the need for distributed transaction coordination via 2PC or Saga
- **[Partition Tolerance](term_partition_tolerance.md)**: The CAP property that 2PC sacrifices — during network partitions, 2PC blocks rather than making unilateral commit/abort decisions
- **[Consistency](term_consistency.md)**: The CAP/ACID property that 2PC preserves at the cost of availability and latency; all nodes see the same data after a 2PC transaction completes
- **[Latency](term_latency.md)**: Two-phase commit adds significant latency to distributed transactions due to synchronous coordination across participants
- **[Throughput](term_throughput.md)**: Two-phase commit reduces throughput by holding locks during the prepare phase; design for single-shard transactions to avoid
- **[Idempotency](term_idempotency.md)**: load-bearing primitive for safe retry — converts at-least-once delivery into effectively exactly-once processing; the foundation under sagas, CRDTs, and replication-log replay.

## References

- [Two-phase commit protocol — Wikipedia](https://en.wikipedia.org/wiki/Two-phase_commit_protocol)
- [Gray, J. — Notes on Data Base Operating Systems (1978)](https://doi.org/10.1007/3-540-08755-9_9) — original 2PC description
- [Distributed Transactions and 2PC — DesignGurus](https://www.designgurus.io/answers/detail/how-do-distributed-transactions-work-and-what-is-two-phase-commit-2pc)
- [Two-Phase Commit Explained — Ajit Singh](https://singhajit.com/distributed-systems/two-phase-commit/)
