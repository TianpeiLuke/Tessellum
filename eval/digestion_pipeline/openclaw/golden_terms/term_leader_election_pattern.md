---
tags:
  - resource
  - terminology
  - distributed_systems
  - cloud_design_pattern
  - microservices
keywords:
  - Leader Election
  - leader election pattern
  - coordinator election
  - primary election
  - failover
  - Bully algorithm
  - Ring algorithm
  - distributed lock
  - single-writer coordination
topics:
  - Distributed Systems
  - Cloud Design Patterns
  - Coordination and Consensus
language: markdown
date of note: 2026-07-27
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Leader Election Pattern

## Definition

**Leader Election** is a distributed-coordination design pattern in which a set of peer nodes agree that exactly one of them will act as the **leader** (also called coordinator, primary, or master node), taking sole responsibility for a shared task, resource, or decision. Electing a single leader ensures consistency and avoids the conflicts, duplicated work, and contention that arise when multiple equal peers try to act on the same resource concurrently. The elected leader coordinates the actions of the other instances -- for example, serializing writes to a shared store, partitioning work among followers, or arbitrating access to an external system. Crucially, the pattern is paired with **failover**: the peers continuously detect the leader's liveness, and when the current leader crashes, becomes unreachable, or is partitioned away, the remaining nodes trigger a new election to choose a replacement so the system keeps making progress.

As described by the Microsoft Azure Architecture Center, leader election is most valuable when a group of collaborating instances must be coordinated but cannot tolerate more than one node performing a role at a time. The election itself is a hard problem in the presence of partial failure and network partitions, so robust implementations delegate it to a proven **consensus** algorithm (Raft, Paxos/Multi-Paxos) or to a dedicated coordination service (Apache ZooKeeper, etcd, Kubernetes Lease objects) rather than hand-rolling an ad-hoc scheme. Classical computer-science algorithms -- the **Bully algorithm** and **Ring algorithm** -- are the textbook foundations, but production systems almost always build on consensus or a coordination service because those correctly handle the split-brain and fencing concerns that naive election schemes miss.

## Context

Leader election underpins a large fraction of stateful distributed infrastructure. In **leader-based (primary/secondary) replication**, one replica is elected primary and accepts all writes while followers replicate its log; when the primary fails, an election promotes a follower. Distributed databases and log systems (e.g. Kafka controller/partition leaders, MongoDB primary election, CockroachDB/etcd ranges) rely on it for single-writer semantics. **Distributed locks** and "run this job exactly once across the fleet" patterns are leader election in disguise. In Kubernetes, controllers and operators use the `client-go` leaderelection package backed by `Lease` objects so that only one replica of a control-loop is active at a time while others stand by hot for failover.

The concrete mechanisms vary by substrate. **Apache ZooKeeper** implements election through its ZAB atomic-broadcast protocol and exposes a well-known recipe using **ephemeral sequential znodes**: each candidate creates a sequential ephemeral node, and the one holding the lowest sequence number is the leader; because ephemeral nodes vanish when the owner's session expires, leader death is detected automatically and the next-lowest node takes over. **etcd** uses the Raft consensus algorithm internally and offers **lease-based** election where leadership is tied to a TTL lease that must be kept alive. Raft and Paxos provide the safety guarantees (a single leader per term, quorum-based commitment) that make these systems correct under partition.

## Key Characteristics

- **Single active leader (mutual exclusion):** at most one node holds leadership for a given role or term, guaranteeing serialized, conflict-free action on the coordinated resource.
- **Failure detection triggers re-election:** followers monitor the leader via heartbeats, health checks, or session/lease expiry; loss of liveness starts a new election so the system self-heals.
- **Consensus / quorum foundation:** correct implementations require agreement among a majority (quorum) of nodes, typically via Raft or Paxos, to prevent two nodes from both believing they are leader.
- **Split-brain avoidance and fencing:** the pattern must guard against a partitioned old leader continuing to act; fencing tokens, terms/epochs, and quorum requirements prevent two simultaneous leaders from corrupting shared state.
- **Lease / TTL and heartbeat based:** leadership is often held via a time-bounded lease that must be renewed; if renewal stops (crash or partition), the lease expires and leadership is up for grabs.
- **Substrate choice:** built either on a coordination service (ZooKeeper ephemeral sequential znodes, etcd leases, Kubernetes `Lease`) or a consensus library, rather than a bespoke protocol.
- **Classical algorithms:** the Bully algorithm (highest-ID node wins, higher-ID nodes bully lower ones) and Ring algorithm (election messages circulate a logical ring) are the canonical CS reference implementations.
- **Graceful step-down:** a well-behaved leader relinquishes leadership on shutdown so a successor is elected quickly instead of waiting for a lease timeout.

## Related Terms


## References

- [Microsoft Azure Architecture Center. "Leader Election pattern."](https://learn.microsoft.com/en-us/azure/architecture/patterns/leader-election) -- Canonical cloud-pattern write-up: when to elect a leader, failover, and the recommendation to use a proven consensus/coordination mechanism.
- [Apache ZooKeeper. "ZooKeeper Recipes and Solutions -- Leader Election."](https://zookeeper.apache.org/doc/current/recipes.html#sc_leaderElection) -- The ephemeral-sequential-znode leader-election recipe, plus ZAB-backed coordination primitives.
- [etcd Documentation. "etcd concurrency / election API."](https://etcd.io/docs/latest/dev-guide/api_concurrency_reference_v3/) -- Lease-based leader election built on etcd's Raft implementation.
- [Kubernetes client-go leaderelection package.](https://pkg.go.dev/k8s.io/client-go/tools/leaderelection) -- Lease-object-based leader election used by Kubernetes controllers and operators for active/standby control loops.
- [Ongaro, D. and Ousterhout, J. (2014). "In Search of an Understandable Consensus Algorithm (Raft)." USENIX ATC.](https://raft.github.io/raft.pdf) -- The Raft paper, whose leader-election phase (terms, votes, randomized timeouts) is the foundation of etcd, Consul, and many others.
- [Lamport, L. (2001). "Paxos Made Simple."](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf) -- The consensus algorithm underlying distinguished-proposer (leader) coordination in classic replicated state machines.
- [Wikipedia. "Leader election."](https://en.wikipedia.org/wiki/Leader_election) -- Overview of the classical Bully and Ring algorithms and the general distributed-systems problem statement.
