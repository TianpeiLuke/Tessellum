---
tags:
  - resource
  - terminology
  - concurrency
  - wait_free_synchronization
keywords:
  - universal class
  - universality
  - universal object
  - universal type
  - consensus number
  - universal construction
  - wait-free
  - synchronization power
topics:
  - Concurrency
  - Concurrent Objects
  - Universality of Consensus
language: markdown
date of note: 2026-07-01
status: active
building_block: concept
related_wiki: null
access_control_group: ["general"]
---

# Universal Class

## Definition

A class $C$ of shared objects is **universal** in a system of $n$ threads if and only if, given enough objects of $C$ plus any number of read–write registers, one can build a [wait-free](term_wait_free.md) [linearizable](term_linearizability.md) implementation of *any* [concurrent object](term_concurrent_object.md) — equivalently, if and only if $C$ has [consensus number](term_consensus_number.md) at least $n$: $\mathrm{cons}(C) \ge n$. The universal class is the bridge from Chapter 5's consensus-number hierarchy to the [universal construction](term_universal_construction.md): once a class can solve $n$-thread [consensus](term_consensus.md), that same consensus power is exactly what a generic algorithm needs to serialize arbitrary method calls into a wait-free object for $n$ threads.

Note: this is the concurrency sense of "universal." Do **not** conflate it with the unrelated statistical-physics notion of a "universality class" (a set of systems sharing the same critical exponents near a phase transition). In *The Art of Multiprocessor Programming* (AOMP), "universal" always means "strong enough to implement any concurrent object wait-free."

## Context

In AOMP Chapter 6, "Universality of Consensus," a class of objects is called universal when it can be used, together with atomic registers, to implement any other object in a wait-free manner. This is the payoff of Chapter 5's [consensus number](term_consensus_number.md) machinery: Chapter 5 ranks object classes by the largest $n$ for which they solve consensus, and Chapter 6 shows that this same ranking is a *sufficiency* result, not merely a necessity result — an object class with consensus number $n$ is not just capable of consensus but capable of everything, for $n$ threads. Maurice Herlihy's 1991 paper "Wait-Free Synchronization" (ACM TOPLAS 13(1):124–149) established this equivalence, defining the consensus/universality hierarchy in which a type's synchronization power is measured by the number of processes for which it solves consensus.

The canonical universal primitive is [compare-and-set](term_compare_and_set.md) (compareAndSet / compare-and-swap), whose consensus number is $\infty$ — it solves consensus for any number of threads and is therefore universal for every $n$. This is why modern multiprocessor architectures expose a CAS-style instruction: a single universal primitive suffices, in principle, to build any lock-free or wait-free data structure. By contrast, plain [atomic registers](term_atomic_register.md) have consensus number $1$ and are universal only in a trivial single-thread system, while classes such as [Common2](term_common2.md) sit at consensus number $2$ and are universal only for two threads.

## Key Characteristics

- **Relative to a thread count**: universality is defined for a specific system of $n$ threads; a class universal for $n$ threads need not be universal for $n+1$. "Universal" without qualification usually means universal for every $n$ (consensus number $\infty$).
- **Consensus-number characterization**: $C$ is universal for $n$ threads $\iff \mathrm{cons}(C) \ge n$. The consensus number is thus both a necessary and a sufficient measure of synchronization power.
- **Constructive, not just existential**: universality is proved by exhibiting a [universal construction](term_universal_construction.md) — an explicit algorithm that turns a [sequential object](term_sequential_object.md)'s specification into a wait-free concurrent implementation using consensus objects plus registers.
- **Registers are "free"**: read–write registers may be used without limit in the construction; they contribute no consensus power ($\mathrm{cons} = 1$) but supply the bookkeeping memory.
- **Wait-free target**: the implemented object must be wait-free and [linearizable](term_linearizability.md); the [helping mechanism](term_helping_mechanism.md) in the wait-free universal construction is what upgrades a merely lock-free construction to wait-free.
- **compareAndSet is universal**: because $\mathrm{cons}(\text{CAS}) = \infty$, a single CAS object (with registers) is universal for any number of threads — the theoretical justification for CAS in hardware.
- **Hierarchy is robust**: a class of consensus number $n$ cannot implement (for more than $n$ threads) any class of higher consensus number, so universality collapses cleanly onto the numeric hierarchy.

## Related Terms


## References

- [Non-blocking algorithm — Wikipedia](https://en.wikipedia.org/wiki/Non-blocking_algorithm)
- [Herlihy, M. (1991). Wait-Free Synchronization. ACM TOPLAS 13(1):124-149.](https://cs.brown.edu/~mph/Herlihy91/p124-herlihy.pdf)

---

**Last Updated**: 2026-07-01
**Status**: Active
