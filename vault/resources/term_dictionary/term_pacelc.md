---
tags:
  - resource
  - terminology
  - system_design
  - distributed_systems
  - databases
keywords:
  - PACELC
  - partition
  - availability
  - consistency
  - latency
  - CAP extension
  - Daniel Abadi
  - trade-off
  - distributed database
  - PA/EL
  - PC/EC
  - PA/EC
  - PC/EL
topics:
  - distributed database design
  - system design trade-offs
  - data consistency models
  - latency-consistency trade-off
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
related_wiki: null
---

# PACELC Theorem

## Definition

**PACELC** is an extension of the CAP theorem proposed by Daniel Abadi of Yale University in a 2010 blog post, later formalized in a 2012 paper. The theorem states: **if there is a Partition (P), choose between Availability (A) and Consistency (C); Else (E), when running normally, choose between Latency (L) and Consistency (C)**. It adds the latency-consistency trade-off that CAP ignores during normal operation. The name is pronounced "pass-elk" and reads as: **P**artition? **A**vailability vs **C**onsistency : **E**lse, **L**atency vs **C**onsistency.

## Context

The PACELC theorem addresses a major limitation of the CAP theorem -- CAP only discusses what happens during network partition scenarios, but the vast majority of the time distributed systems run without partitions. As Abadi noted: "Ignoring the consistency/latency trade-off of replicated systems is a major oversight, as it is present at all times during system operation, whereas CAP is only relevant in the arguably rare case of network partitions." PACELC captures the everyday latency-consistency trade-off that database architects face in normal operation, making it a more practical and complete framework for reasoning about distributed system design. This concept is covered in the SDDD podcast series (Episode 2 - Fundamentals) as a foundational system design principle.

## Key Characteristics

- **Full PACELC formula**: `if P then {A, C} else {L, C}` -- during a partition, choose availability or consistency; during normal operation, choose low latency or strong consistency
- **Four PACELC quadrants**:

| Classification | During Partition | During Normal Operation | Examples |
|----------------|-----------------|------------------------|----------|
| **PA/EL** | Availability | Low Latency | Cassandra, DynamoDB (internal Dynamo), Riak, Cosmos DB |
| **PC/EC** | Consistency | Consistency | PostgreSQL, MySQL Cluster, VoltDB/H-Store, Google Megastore |
| **PA/EC** | Availability | Consistency | MongoDB (default config) |
| **PC/EL** | Consistency | Low Latency | Yahoo! PNUTS |

- **PA/EL systems**: Sacrifice consistency in all scenarios -- during partitions they remain available, and during normal operation they favor low latency over strong consistency. These are fully "eventually consistent" systems optimized for speed and availability
- **PC/EC systems**: Never sacrifice consistency -- they accept unavailability during partitions and higher latency during normal operation to guarantee strong consistency. These are traditional ACID-compliant relational databases
- **PA/EC systems**: A hybrid approach -- during partitions they favor availability (accepting stale reads), but during normal operation they enforce strong consistency. MongoDB's default single-primary replica set behavior exemplifies this
- **PC/EL systems**: The rarest quadrant -- during partitions they enforce consistency, but during normal operation they optimize for low latency. Yahoo! PNUTS is the canonical example
- **More practical than CAP**: CAP presents a binary choice that only applies during partitions. PACELC acknowledges that the latency-consistency trade-off is the one engineers face daily, since partitions are rare events
- **Tunable consistency**: Modern databases like DynamoDB and Cassandra allow per-request consistency tuning, meaning a single system can operate in different PACELC quadrants depending on the operation (e.g., DynamoDB supports both eventually consistent reads and strongly consistent reads)
- **Replication is the root cause**: The latency-consistency trade-off exists because data is replicated across nodes. Synchronous replication ensures consistency but adds latency; asynchronous replication reduces latency but allows stale reads

## Related Terms

- **[CAP Theorem](term_cap_theorem.md)**: The foundational theorem that PACELC extends -- CAP addresses only the partition scenario, PACELC adds the normal-operation trade-off
- **[Consistency](term_consistency.md)**: Appears twice in PACELC -- the "C" in both the partition clause and the else clause, representing the fundamental consistency guarantee
- **[Availability](term_availability.md)**: The "A" in PACELC -- favored over consistency during partitions by PA systems (Cassandra, DynamoDB)
- **[Partition Tolerance](term_partition_tolerance.md)**: The "P" in PACELC -- the triggering condition that determines which trade-off applies
- **[ACID](term_acid.md)**: PC/EC systems are fully ACID-compliant, choosing consistency over both availability and latency
- **[NoSQL](term_nosql.md)**: Most NoSQL databases are PA/EL systems, explicitly trading consistency for availability and low latency
- **[FLP Impossibility](term_flp_impossibility.md)**: A more fundamental impossibility result -- while PACELC describes trade-offs, FLP proves consensus itself is impossible in asynchronous systems with faults
- **[LSM Tree](term_lsm_tree.md)**: LSM tree compaction strategies directly affect the latency-consistency trade-off that PACELC describes
- **[DynamoDB](term_ddb.md)**: Originally PA/EL (internal Dynamo); modern DynamoDB supports tunable consistency, allowing per-read PA/EL or PA/EC behavior
- **[MongoDB](term_mongodb.md)**: Default PA/EC system -- available during partitions but strongly consistent during normal operation via single-primary writes
- **[Microservices Architecture](term_microservices_architecture.md)**: PACELC trade-offs arise at every service boundary in microservices, where each service may choose a different consistency-latency profile
- **[Space-Based Architecture](term_space_based_architecture.md)**: Addresses PACELC trade-offs by replicating data in-memory across nodes, typically operating as PA/EL
- **[Event-Driven Architecture](term_event_driven_architecture.md)**: Asynchronous event propagation inherently trades consistency for latency, operating in the EL space
- **[Vector Database](term_vector_database.md)**: Similarity search stores that typically operate as PA/EL, favoring low-latency approximate results over strict consistency
- **[Elasticsearch](term_elasticsearch.md)**: Near-real-time search engine that operates as PA/EL, trading consistency for search latency
- **[Amdahl's Law](term_amdahls_law.md)**: Another fundamental limitation result -- PACELC limits distributed store trade-offs, Amdahl's limits parallel speedup
- **[BASE](term_base.md)**: PA/EL systems in PACELC adopt the BASE consistency model -- Basically Available, Soft state, Eventually consistent -- the design philosophy that prioritizes availability and low latency over strong consistency
- **[Database Replication](term_database_replication.md)**: Replication is the root cause of the PACELC trade-off -- synchronous replication ensures consistency but adds latency, while asynchronous replication reduces latency but allows stale reads
- **[Two-Phase Commit](term_two_phase_commit.md)**: 2PC is a PC/EC protocol under PACELC -- it trades latency for consistency during normal operation and sacrifices availability for consistency during partitions
- **[Latency](term_latency.md)**: PACELC formalizes the consistency-latency trade-off: even without network partitions, systems trade latency for consistency (EL vs EC)

## References

### Academic References
- Abadi, D. (2012). "Consistency Tradeoffs in Modern Distributed Database System Design." *IEEE Computer*, 45(2), 37-42. [PDF](https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf)
- Abadi, D. (2010). "Problems with CAP, and Yahoo's little known NoSQL system." [Blog post](http://dbmsmusings.blogspot.com/2010/04/problems-with-cap-and-yahoos-little.html)

### External References
- [PACELC Theorem -- Wikipedia](https://en.wikipedia.org/wiki/PACELC_design_principle)
- [PACELC Theorem -- ScyllaDB Glossary](https://www.scylladb.com/glossary/pacelc-theorem/)
- [Beyond CAP: Unveiling the PACELC Theorem -- DEV Community](https://dev.to/ashokan/beyond-cap-unveiling-the-pacelc-theorem-for-modern-systems-465j)
- [PACELC Theorem Explained -- Medium](https://medium.com/distributed-systems-series/pacelc-theorem-explained-distributed-systems-series-9c509febb8f8)

---

**Last Updated**: April 19, 2026
**Status**: Active -- extension of CAP theorem capturing the latency-consistency trade-off during normal operation
