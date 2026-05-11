---
tags:
  - resource
  - terminology
  - distributed_systems
  - computer_science
  - consensus
  - impossibility
keywords:
  - FLP impossibility
  - Fischer Lynch Paterson
  - consensus
  - asynchronous
  - distributed computing
  - fault tolerance
  - deterministic
  - impossibility result
topics:
  - distributed consensus
  - theoretical limits of distributed systems
language: markdown
date of note: 2026-04-17
status: active
building_block: concept
related_wiki: null
---

# FLP Impossibility - Fischer-Lynch-Paterson Impossibility Result

## Definition

The FLP impossibility result, published by Michael Fischer, Nancy Lynch, and Michael Paterson in 1985, proves that no deterministic algorithm can guarantee consensus in an asynchronous distributed system if even a single process can crash. Consensus requires all non-faulty processes to agree on a single value, and the FLP result shows that any deterministic consensus protocol has at least one execution in which it never terminates. This is widely regarded as "perhaps the most important theorem in all of distributed computing" (Tim Roughgarden) and fundamentally shapes how distributed systems are designed.

## Context

The FLP result explains why practical consensus protocols like Paxos and Raft use timeouts, randomization, or partial synchrony assumptions to circumvent the impossibility. In purely asynchronous systems (where there is no bound on message delivery time), you cannot distinguish a crashed process from a slow one — and this ambiguity is what makes consensus impossible. The theorem does not say consensus is never achievable; it says no single deterministic protocol can guarantee termination in all possible executions. This is why real-world systems (including Amazon's distributed infrastructure) rely on failure detectors, leader election with timeouts, and eventual consistency models.

## Key Characteristics

- **The core result**: In an asynchronous system with even one faulty process, no deterministic consensus protocol can guarantee both safety (agreement) and liveness (termination) in all executions
- **Asynchronous model**: No upper bound on message delivery time or process execution speed — the key assumption that makes the result hold
- **One fault is enough**: The impossibility holds even if only a single process can crash — not a majority, just one
- **Safety vs liveness**: The protocol can always maintain safety (never disagree), but cannot guarantee liveness (may run forever without deciding)
- **Circumventions**: Practical systems bypass FLP through:
  - **Randomization**: Probabilistic consensus (e.g., Ben-Or protocol) — terminates with probability 1
  - **Partial synchrony**: Assume messages are eventually delivered within a bound (e.g., Paxos, Raft)
  - **Failure detectors**: Oracle that eventually identifies crashed processes (e.g., Chandra-Toueg)
  - **Timeouts**: Practical approximation of failure detection — if no response in T seconds, assume crashed
- **Relationship to CAP**: FLP is more fundamental — CAP says you can't have C+A+P; FLP says you can't even solve consensus (a prerequisite for C) in async systems with faults

## Related Terms

- **[CAP Theorem](term_cap_theorem.md)**: CAP constrains distributed data stores; FLP constrains the consensus protocols that underpin them — FLP is the deeper result
- **[Consistency](term_consistency.md)**: Strong consistency requires consensus among replicas — FLP shows this consensus cannot be guaranteed deterministically in async systems
- **[Availability](term_availability.md)**: FLP's liveness impossibility directly impacts availability — a protocol that never terminates is unavailable
- **[Partition Tolerance](term_partition_tolerance.md)**: Network partitions create the asynchrony that FLP exploits — a partitioned node is indistinguishable from a crashed one
- **[ACID](term_acid.md)**: ACID transactions in distributed databases require consensus for commit — FLP limits how this can be achieved
- **[Microservices Architecture](term_microservices_architecture.md)**: Distributed coordination between microservices faces FLP constraints
- **[DynamoDB](term_ddb.md)**: Bypasses FLP by using eventual consistency (no consensus needed for AP mode) and Paxos-like protocols for strong consistency mode
- **[Structured Programming](term_structured_programming.md)**: Like Dijkstra's structured programming theorem, FLP establishes fundamental limits on what algorithms can achieve

- **[Amdahl's Law](term_amdahls_law.md)**: Parallel speedup limit — together with FLP and CAP, forms the core impossibility results of distributed computing
- **[PACELC](term_pacelc.md)**: PACELC extends CAP (which FLP underlies) by adding the latency-consistency trade-off even without partitions — FLP constrains the consensus protocols that enable strong consistency in PACELC's ELC case
- **[BASE](term_base.md)**: BASE bypasses FLP by not requiring consensus -- eventually consistent systems avoid the impossibility result by accepting temporary divergence
- **[Two-Phase Commit](term_two_phase_commit.md)**: 2PC's blocking problem is a direct consequence of FLP -- if the coordinator crashes, participants cannot deterministically reach consensus on commit or abort in an asynchronous system

## References

- Fischer, M., Lynch, N., & Paterson, M. (1985). "Impossibility of Distributed Consensus with One Faulty Process." *Journal of the ACM*, 32(2), 374–382.
- [FLP Impossibility — Wikipedia](https://en.wikipedia.org/wiki/Consensus_(computer_science)#Impossibility_results)
- [FLP Impossibility and Theoretical Limits — kindatechnical.com](https://kindatechnical.com/distributed-systems/flp-impossibility-and-theoretical-limits.html)
- [Different Perspectives on FLP Impossibility — arXiv](https://arxiv.org/html/2210.02695v9)
- Roughgarden, T. "Lecture 5: FLP Impossibility." Stanford CS 265.
