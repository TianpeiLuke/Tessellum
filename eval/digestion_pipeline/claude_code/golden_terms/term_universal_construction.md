---
tags:
  - resource
  - terminology
  - concurrency
  - wait_free_synchronization
keywords:
  - universal construction
  - universality of consensus
  - wait-free universal construction
  - lock-free universal construction
  - sequential to concurrent transformation
  - log-of-nodes construction
  - consensus universality
topics:
  - Concurrency
  - Concurrent Objects
  - Consensus
  - Universality
language: markdown
date of note: 2026-07-01
status: active
building_block: concept
related_wiki: null
access_control_group: ["general"]
---

# Universal Construction

## Definition

A universal construction is a general method that transforms any object with a deterministic [sequential specification](term_sequential_object.md) into a [linearizable](term_linearizability.md) [concurrent object](term_concurrent_object.md), using [consensus](term_consensus.md) objects plus atomic read–write [registers](term_atomic_register.md) as its building blocks. Introduced by Maurice Herlihy in "Wait-Free Synchronization" (1991), it makes concrete the *universality of consensus*: because consensus objects have infinite [consensus number](term_consensus_number.md), a supply of them plus registers is strong enough to implement *anything*. The construction yields a [lock-free](term_lock_free.md) object directly, and a [wait-free](term_wait_free.md) object once a [helping mechanism](term_helping_mechanism.md) is added.

The classic form is the **log-of-nodes construction**: the object state is represented implicitly as a shared log of applied method invocations. To apply an operation, a thread creates a node holding its invocation and competes with other threads to append it — the winner of a per-node [consensus](term_consensus_protocol.md) decides which node becomes the log's next entry. Every thread then replays the agreed log against a *private* copy of the sequential object to compute its response, so no thread ever needs a lock and no partial state is ever observed by another thread.

## Context

The universal construction is the centerpiece of *The Art of Multiprocessor Programming* (AOMP) Chapter 6, "Universality of Consensus," which answers the question left open by Chapter 5's [consensus number](term_consensus_number.md) hierarchy: knowing that [compare-and-set](term_compare_and_set.md) has consensus number $\infty$, *what can you actually build with it?* Chapter 5 ranks synchronization primitives by the number of threads for which they can solve consensus; Chapter 6 shows that this ranking is not merely a curiosity but a completeness result — a class with consensus number $n$ is **universal** for $n$ threads, meaning it can implement any [concurrent object](term_concurrent_object.md) shared by $n$ threads.

A class of objects is called a **universal class** (see [universal class](term_universal_class.md)) if, together with registers, it can implement any object with a sequential specification. The universal construction is the constructive proof that consensus objects form such a class, which by transitivity makes any primitive of infinite consensus number (such as `compareAndSet`) universal. This mirrors, from the shared-memory side, the negative message-passing result of [FLP impossibility](term_flp_impossibility.md): where FLP shows asynchronous message passing cannot solve consensus deterministically under one crash, Herlihy's universality shows that *if* you are handed consensus in shared memory, you can bootstrap it into every wait-free data structure. The construction is also where correctness reasoning leans on auxiliary [ghost variables](term_ghost_variable.md) — logical state such as sequence numbers and per-thread "last applied" pointers that exist to make the linearizability argument go through.

## Key Characteristics

- **Sequential-to-concurrent transformer**: takes an arbitrary deterministic [sequential object](term_sequential_object.md) and produces a [linearizable](term_linearizability.md) concurrent one, with no algorithm-specific cleverness required per object.
- **Consensus + registers is the toolkit**: the only strong primitive needed is a [consensus](term_consensus.md) object; everything else is atomic [read–write registers](term_atomic_register.md), which is exactly what universality of consensus asserts.
- **Log-based state**: object state is the (implicit) sequence of applied invocations; a thread computes its response by replaying the log against a private copy — writers never mutate shared object state in place.
- **Two progress tiers from one design**: appending via consensus alone gives a [lock-free](term_lock_free.md) construction; adding a [helping mechanism](term_helping_mechanism.md) (threads announce and complete each other's pending operations) upgrades it to [wait-free](term_wait_free.md).
- **Universality = completeness of the hierarchy**: it proves a class of consensus number $n$ can implement *any* $n$-thread object, so [compare-and-set](term_compare_and_set.md) ($\infty$) is universal for any number of threads.
- **Generality over efficiency**: it is a proof of what is *possible*, not a recipe for fast structures — the copy-and-replay overhead makes it impractical as a drop-in, but it grounds the theory of what wait-free synchronization can achieve.

## Related Terms


## References

- [Non-blocking algorithm — Wikipedia](https://en.wikipedia.org/wiki/Non-blocking_algorithm)
- [Herlihy, M. (1991). Wait-Free Synchronization. ACM TOPLAS 13(1):124-149. DOI 10.1145/114005.102808.](https://doi.org/10.1145/114005.102808)

---

**Last Updated**: 2026-07-01
**Status**: Active
</content>
</invoke>
