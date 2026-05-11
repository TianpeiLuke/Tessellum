---
tags:
  - resource
  - terminology
  - distributed_systems
  - microservices
  - transaction_management
  - design_patterns
keywords:
  - Saga Pattern
  - saga
  - compensating transactions
  - choreography
  - orchestration
  - distributed transactions
  - eventual consistency
  - long-lived transactions
topics:
  - Distributed Systems
  - Microservices Architecture
  - Design Patterns
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
related_wiki: null
---

# Saga Pattern

## Definition

The **Saga Pattern** is a design pattern for managing distributed transactions across multiple services or databases without using a global lock-based protocol like Two-Phase Commit (2PC). Instead of coordinating a single atomic transaction, a saga decomposes the operation into a sequence of local transactions, each of which commits independently. If any step fails, previously completed steps are undone by executing **compensating transactions** — explicit inverse operations that semantically reverse the effect of the original transaction.

Originally proposed by Hector Garcia-Molina and Kenneth Salem in 1987 for long-lived transactions in a single database, the pattern was adopted by the microservices community as the standard approach for cross-service data consistency. Unlike 2PC, sagas do not hold distributed locks, making them non-blocking and partition-tolerant — but they sacrifice strong isolation (the "I" in ACID), requiring careful handling of intermediate states and data anomalies.

## Context

The Saga Pattern is the dominant approach for distributed transaction management in microservices architectures:

- **Microservices**: When a business operation (e.g., placing an order) spans Order Service, Payment Service, and Inventory Service, each with its own database, a saga coordinates the sequence of local commits with compensating rollbacks on failure
- **Event-driven systems**: Choreography-based sagas naturally fit event-driven architectures where services communicate via message brokers like Kafka or SNS/SQS
- **Cloud-native applications**: AWS Step Functions, Azure Durable Functions, and Temporal.io provide orchestrator infrastructure specifically designed for saga execution
- **Sharded databases**: When cross-shard transactions are too expensive via 2PC, sagas offer an alternative that trades consistency for performance — each shard commits independently with compensation on failure

## Key Characteristics

- **Two coordination styles**:
  - **Choreography**: Each service publishes events after completing its local transaction; other services subscribe and react — no central coordinator, but harder to debug and monitor
  - **Orchestration**: A central saga orchestrator directs participants step-by-step, handling routing, retries, and compensation — easier to understand and debug, but introduces a single point of coordination
- **Compensating transactions**: Each saga step must have a defined compensating action that semantically reverses it (e.g., `CancelOrder` compensates `CreateOrder`); compensation is not a database rollback but a forward-moving business operation
- **No distributed locks**: Unlike 2PC, sagas do not hold locks across services, eliminating the blocking problem and improving availability
- **Eventual consistency**: The system may be in an inconsistent intermediate state between saga steps; applications must tolerate and handle these transient inconsistencies
- **Idempotency requirement**: Both forward and compensating transactions must be idempotent to handle retries safely — network failures can cause duplicate message delivery
- **Semantic rollback, not physical**: Compensating transactions may not perfectly undo effects (e.g., a refund email cannot be "unsent"), requiring domain-specific strategies for irreversible side effects
- **Data anomalies**: Without isolation, sagas are susceptible to dirty reads (reading uncommitted intermediate state), lost updates, and fuzzy reads across concurrent saga instances

## Related Terms

- **[Two-Phase Commit](term_two_phase_commit.md)**: The lock-based alternative to sagas for distributed transactions; 2PC provides strong consistency but blocks during coordinator failure — sagas trade consistency for availability
- **[ACID](term_acid.md)**: The transaction properties that sagas partially sacrifice; sagas preserve atomicity (via compensation) and durability but weaken isolation and consistency
- **[BASE](term_base.md)**: The consistency model that sagas implement; Basically Available, Soft state, Eventually consistent — the opposite end of the spectrum from ACID
- **[Microservices Architecture](term_microservices_architecture.md)**: The architectural style that created widespread need for sagas; each microservice owns its database, making distributed transactions across services a core challenge
- **[Kafka](term_kafka.md)**: Message broker commonly used for choreography-based sagas; services publish and consume domain events through Kafka topics to coordinate saga steps
- **[CAP Theorem](term_cap_theorem.md)**: Sagas are an AP (Available, Partition-tolerant) approach that sacrifices strong consistency — the inverse of 2PC's CP approach
- **[Sharding](term_sharding.md)**: When cross-shard 2PC is too expensive, sagas offer an alternative coordination mechanism for multi-shard operations
- **[Consistent Hashing](term_consistent_hashing.md)**: Determines shard assignment and thus whether a transaction requires cross-shard coordination via saga or 2PC
- **[Command Pattern](term_command_pattern.md)**: The behavioral design pattern that underpins saga step encapsulation — each saga step is a command object with an execute and undo (compensate) method
- **[Change Data Capture](term_change_data_capture.md)**: CDC can trigger saga steps by capturing database changes as events, enabling the transactional outbox pattern for reliable event publishing
- **[Partition Tolerance](term_partition_tolerance.md)**: The CAP property that sagas preserve — unlike 2PC, sagas can make progress during network partitions by operating on local data
- **[PACELC](term_pacelc.md)**: Sagas choose low latency and availability over strong consistency both during partitions (PA) and normal operation (EL)
- **[Idempotency](term_idempotency.md)**: load-bearing primitive for safe retry — converts at-least-once delivery into effectively exactly-once processing; the foundation under sagas, CRDTs, and replication-log replay.

## References

- [Garcia-Molina, H. & Salem, K. — Sagas (SIGMOD 1987)](https://doi.org/10.1145/38713.38742) — original saga paper
- [Saga Design Pattern — Microsoft Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga)
- [Saga Pattern — microservices.io (Chris Richardson)](https://microservices.io/patterns/data/saga.html)
- [Saga Patterns — AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga.html)
- [Mastering Saga Patterns — Temporal.io](https://temporal.io/blog/mastering-saga-patterns-for-distributed-transactions-in-microservices)
