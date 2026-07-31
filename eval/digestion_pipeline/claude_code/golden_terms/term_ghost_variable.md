---
tags:
  - resource
  - terminology
  - concurrency
  - wait_free_synchronization
keywords:
  - ghost variable
  - auxiliary variable
  - ghost state
  - history variable
  - proof variable
  - Owicki-Gries
  - concur
  - start
  - universal construction proof
topics:
  - Concurrency
  - Program Verification
  - Universality of Consensus
language: markdown
date of note: 2026-07-01
status: active
building_block: concept
related_wiki: null
access_control_group: ["general"]
---

# Ghost Variable (Auxiliary Variable)

## Definition

A ghost (a.k.a. auxiliary) variable is a variable added to an algorithm purely to reason about its correctness: it does not appear in the executable code and does not alter the program's behavior in any way. Because a ghost variable can be read and written only by other ghost updates — never by ordinary program statements, and it never influences any real variable, control-flow branch, or return value — erasing every ghost variable and every assignment to it leaves an execution whose observable behavior on the real (program) variables is identical. Formally, if $g$ is a ghost variable and $\pi$ is any execution of the instrumented program, the projection of $\pi$ onto the real variables equals an execution of the original program; ghost state exists only at the verification level.

In *The Art of Multiprocessor Programming* (AOMP) the technique is used in the proof of the wait-free [universal construction](term_universal_construction.md). To argue that every announced method call is eventually applied (the *helping* property), the proof augments the atomic apply step with ghost variables such as $\text{concur}(A)$ and $\text{start}(A)$, which are read and written only inside the atomic angle-bracket blocks $\langle \ldots \rangle$ that model each indivisible step. Here $\text{start}(A)$ records the value of the log's sequence counter at the moment thread $A$ announces its pending call, and $\text{concur}(A)$ accumulates the set of method calls that are appended to the shared log concurrently with $A$'s pending announcement; these bookkeeping quantities let the proof state the loop invariant and the helping lemmas without changing what the construction actually computes.

As a general program-verification and model-checking technique, auxiliary variables predate AOMP: they were introduced by Susan Owicki and David Gries in their 1976 axiomatic method for parallel programs, where a dedicated inference rule permits adding auxiliary variables (often recording control flow or history) to a program solely to make a Hoare-style partial-correctness proof go through, then discarding them. The same idea appears today under the names *ghost state*, *ghost code*, and *history variables* in deductive verifiers and separation logics.

## Context

Ghost variables appear in AOMP Chapter 6, "Universality of Consensus," which shows that [consensus](term_consensus.md) is *universal*: any object with a [sequential specification](term_sequential_object.md) can be implemented in a wait-free manner from atomic registers and objects that solve consensus (equivalently, from any object whose [consensus number](term_consensus_number.md) is $\infty$, such as [compare-and-set](term_compare_and_set.md), for which $\mathrm{cons}(\cdot)=\infty$). The chapter builds first a lock-free [universal construction](term_universal_construction.md) and then upgrades it to a wait-free one by adding a [helping mechanism](term_helping_mechanism.md); it is the wait-freedom argument — proving that no thread starves because its announced call is always applied within a bounded number of steps — that relies on the ghost variables $\text{concur}(A)$ and $\text{start}(A)$.

The role of ghost variables here is purely evidentiary: they carry information about the *history* of the execution (which calls were concurrent, when a thread started) that is not present in the object's real state, and they let the proof relate a thread's local progress to global progress. This is the same distinction Herlihy's consensus/universality hierarchy draws elsewhere — the object being constructed remains a [linearizable](term_linearizability.md) [concurrent object](term_concurrent_object.md) with an ordinary sequential specification, while the ghost variables live only in the correctness argument. Because they cannot affect execution, ghost variables can be freely assumed atomic, unbounded, or globally visible without weakening the implementation's real progress guarantees such as [wait-freedom](term_wait_free.md).

## Key Characteristics

- **No runtime effect**: a ghost variable never appears in compiled/executable code; adding or removing it, and its updates, leaves observable behavior on real variables unchanged.
- **One-directional information flow**: real variables may be copied into ghost variables, but no ghost variable may influence a real variable, branch, or return value — otherwise it would change behavior and cease to be a ghost.
- **History-carrying**: ghost variables typically record information about the *history* of a computation (e.g., $\text{concur}(A)$, $\text{start}(A)$, loop-iteration counts) that the program's real state does not retain; hence the synonym *history variable*.
- **Updated atomically with real steps**: in AOMP the ghost updates sit inside the atomic angle-bracket blocks $\langle \ldots \rangle$ modeling each indivisible action, so ghost and real state advance together in the proof.
- **A proof device, not an implementation**: they exist to state invariants and lemmas (here, the helping lemmas for the wait-free [universal construction](term_universal_construction.md)); they can be assumed atomic and unbounded because they cost nothing at runtime.
- **General verification technique**: introduced by Owicki–Gries (1976) for axiomatic proofs of parallel programs and now standard as *ghost state* / *ghost code* in Hoare logics, separation logics, and model checking.

## Related Terms


## References

- [Owicki, S. and Gries, D. (1976). An axiomatic proof technique for parallel programs I. Acta Informatica 6:319-340.](https://doi.org/10.1007/BF00268134)
- [Owicki, S. and Gries, D. (1976). Verifying properties of parallel programs: an axiomatic approach. Communications of the ACM 19(5):279-285.](https://doi.org/10.1145/360051.360224)
- [Filliâtre, J.-C., Gondelman, L., and Paskevich, A. (2016). The Spirit of Ghost Code. Formal Methods in System Design 48(3):152-174.](https://doi.org/10.1007/s10703-016-0243-x)

---

**Last Updated**: 2026-07-01
**Status**: Active
