---
tags:
  - resource
  - analysis
  - argument
  - cqrs
  - architecture
  - design_rules
  - rcross
keywords:
  - R-Cross rules
  - R-P prescriptive integrity
  - R-D descriptive purity
  - two sub-system boundaries
  - System P System D
  - schema runtime co-evolution
  - candidate generation purity
  - cross-system call direction
topics:
  - System Architecture
  - CQRS
  - Design Rules
  - Tessellum Foundations
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "1a1b"
folgezettel_parent: "1a1"
---

# The R-Cross Rules — Formal Discipline for the Two Sub-System Boundaries

## Thesis

The CQRS synthesis at [FZ 1a1](thought_synthesis_two_systems_cqrs_value_proposition.md) names **one architectural boundary** (declaration ⊥ computation, with one substrate between them). But the discipline that *defends* that boundary in day-to-day decisions reduces to **three rules**, each of which polices a distinct sub-system boundary:

> - **R-P** polices the boundary *inside System P* — Schema (Ontology) ⊥ Runtime (DKS).
> - **R-D** polices the boundary *inside System D* — Candidate generation ⊥ Re-rank + assembly.
> - **R-Cross** polices the boundary *between the two systems* — P writes, D reads, P may call D, D may never call P.

The CQRS essence ([FZ 1a1a](thought_cqrs_essence_for_tessellum.md)) is the *user-facing* version of the synthesis ("one boundary, two disciplines, one substrate"). This note is the *architect-facing* version: the three rules architects apply to every proposed change, and the violation patterns each rule rules out. A proposed change that violates any one is, by construction, wrong.

## The three rules

### R-P — Prescriptive integrity

> **Schema and Runtime must co-evolve.** Add a BB type only when the dialectic protocol gains a phase that produces it. Sub-kinds live in System D's facets, not System P's specifications.

R-P polices the seam *inside* System P. Ontology (Schema) and DKS (Runtime) are the static and dynamic facets of one prescriptive system. They are not stacked layers; they are specification and runtime of the same thing.

**What R-P rules out**:

- Growing BB types ad-hoc in response to a perceived missing slot. The BB graph is a closed set — eight types, ten edges — because the DKS protocol cycle uses exactly those types and edges as its program counter.
- Adding *sub-kinds* (e.g., "concept-of-process" vs "concept-of-thing") to the schema. Sub-kinds are operational ergonomics; they belong in System D's facets (BB-aware re-rank, BB-typed evaluation), not in the schema. The Schema-Runtime invariant degrades immediately if sub-kinds leak into the BB types.
- Changing DKS phases without adding a corresponding ontology edge. If the protocol needs a new step, the ontology needs a new edge whose source/target produces what the step consumes/emits.

R-P is the rule that keeps the BB ontology *small* and *load-bearing* over time.

### R-D — Descriptive purity

> **Candidate generation is computational (dense). System P artifacts enter at stages 3-4 (re-rank + context assembly), never at stage 1 (candidate generation).**

R-D polices the structure *inside* System D. Retrieval has four stages:

```
   Stage 1                  Stage 2              Stages 3-4
   ───────                  ───────              ──────────
   Candidate generation  →  Fusion           →   Re-rank + context assembly
   (BM25 + dense)            (RRF blend)         (BB-aware, FZ-aware, link-aware)
```

R-D's claim: candidate generation is *content-aware* (BM25 over body text, dense embeddings over semantic context). Typed System P artifacts — BB types, Folgezettel trail position, link-graph proximity — enter *after* candidate generation, in stages 3 and 4, where they refine ranking and assemble context.

**What R-D rules out**:

- BB-aware *pre-routing*: dispatching different BB types through different retrieval strategies before any content is retrieved. Refuted empirically by the retrieval benchmark ([FZ 3](thought_retrieval_evolution.md), step 2): Dense uniformly dominates all BB types; the Strategy × BB heatmap is flat. There is no BB whose questions are best served by a different strategy.
- LIKE-bound seed resolution: graph traversal whose seeds come from a SQL `LIKE` over note names. 11 of the 14 strategies in the foundational benchmark were dominated because they shared this bottleneck — `_resolve_terms() LIMIT 10` capped expansion at metadata depth.
- Optimising candidate generation for Hit@K. Hit@K and answer quality have only ρ = 0.37 correlation. Candidate generation should optimise for *content recall*; typed re-ranking should optimise for *epistemic congruence*.

R-D is the rule that keeps the System D candidate-generation layer *content-aware* and *type-blind*, ensuring its inputs are the substrate's content (not the substrate's typing metadata) and its outputs are then refined by typing at stages 3-4.

### R-Cross — System boundary

> **System P writes; System D reads. System P may call System D (to check whether knowledge already exists before authoring). System D does NOT call System P. The query path never crosses into System P.**

R-Cross polices the *boundary between* the two systems. It is the load-bearing CQRS commitment.

**What R-Cross rules out**:

- System D querying System P at runtime to decide what to retrieve. Examples: "look at the DKS state machine to decide which strategy to apply"; "consult the open-loop dialectic to bias the candidate set." Any query-path component that consults P-side state is an R-Cross violation.
- System P querying System D for *what should be authored*. P writes typed atomic notes by declaration. It may invoke D to check whether a similar note already exists (deduplication) — that's a *non-prescriptive* use of D's read API. But P does not *decide what to author* by polling D. That would invert the prescriptive/descriptive relationship.
- System D writing to the substrate. Retrieval reads, ranks, returns. Re-writing on retrieval is forbidden. If a query reveals a missing note, that's an authoring task (P), not a retrieval task (D).
- Cross-process IPC between P and D at the runtime level. P and D are not microservices; they are disciplines composed at the substrate. Adding an IPC layer between them is recreating distributed-systems failure modes that the substrate-share model designed out.

R-Cross is the rule that makes the substrate the *only* meeting point. Everything else flows through the file system, not through inter-system invocations.

## Why three rules, not one

A naïve reading of CQRS sees only one rule: "split read and write." But that rule alone underdetermines the architecture. *Where* do you split? *What* counts as a read? Can the read side know about the write side's typing? Can the write side know about the read side's evidence?

The three rules answer those questions concretely:

| Rule | Polices | Answer |
|------|---------|--------|
| **R-P** | The internal cohesion of System P | Schema and Runtime co-evolve; no ad-hoc growth |
| **R-D** | The internal cohesion of System D | Candidate gen is content-aware; typing enters at re-rank |
| **R-Cross** | The interface between P and D | P writes, D reads, P may call D, D may not call P |

Without R-P, System P fragments (schema rot, sub-kind leakage). Without R-D, System D regresses (typed pre-routing, Hit@K-driven changes). Without R-Cross, the substrate-as-only-meeting-point property collapses (query-path dependencies on P-state).

The three rules are *not* independent — they are the same boundary discipline applied at three different junctures. But each rule is *separately* falsifiable: a proposed change can violate R-P while satisfying R-D and R-Cross, for example, and the architect needs to name *which* rule the change violates to know what to push back on.

## The recognition checklist

When evaluating any proposed change to the codebase, walk the three rules in order:

```
1. R-P: Does this grow System P's schema in a way the runtime can't already
        consume? If yes → the schema is drifting from the runtime.
        Either add a runtime phase that consumes it, or push the proposal
        into System D's facets (re-rank, evaluation).

2. R-D: Does this move System P artifacts (BB types, FZ positions, link
        proximities) into Stage 1 (candidate generation)? If yes → typing
        is corrupting content-aware retrieval. Move it to Stage 3-4.

3. R-Cross: Does this make System D depend on System P state at query
        time? Or System P decide what to author by polling System D?
        If either, the substrate is no longer the only meeting point.
        Find the substrate-mediated form of the same dependency.
```

If a change passes all three, ship it. If it fails any, name which rule, and either rework the change or — rarely — argue that the rule itself is wrong and present the case.

## What this means for Tessellum

R-P, R-D, R-Cross are not abstract design philosophy. They are tests Tessellum's codebase satisfies (or fails) at concrete points:

- **R-P** is enforced by the closed 8-type BB enum in `format/building_blocks.py`. A new contributor can't add a 9th BB without editing the enum and the EPISTEMIC_EDGES tuple in lockstep — and the absent DKS runtime means there's nothing yet *consuming* a new edge, which is itself an R-P signal that the schema is at the right size for the runtime.
- **R-D** is enforced by the retrieval design ([FZ 3a](thought_retrieval_synthesis.md)): hybrid RRF default with BM25 + dense candidate generation; `tessellum filter --bb <type>` is a *separate* metadata-filter surface, not a BB-aware pre-routing of `search`. BB types live in metadata and in (future) re-rank stages, never in candidate generation.
- **R-Cross** is enforced by the import graph: `composer/` doesn't import `retrieval/` or `indexer/`; `retrieval/` and `indexer/` don't import `composer/`. The system review at [`thought_src_tessellum_system_review`](thought_src_tessellum_system_review.md) verified this empirically.

A future architectural change that fails any of these tests should be rejected — not because "CQRS says so" abstractly, but because one of the three concrete rules names what breaks.

## Related Notes

- [`thought_synthesis_two_systems_cqrs_value_proposition`](thought_synthesis_two_systems_cqrs_value_proposition.md) — FZ 1a1 — the synthesis whose discipline these three rules formalize
- [`thought_cqrs_essence_for_tessellum`](thought_cqrs_essence_for_tessellum.md) — FZ 1a1a — sibling node; the user-facing distillation of the same synthesis
- [`thought_cqrs_r_cross_gap_audit`](thought_cqrs_r_cross_gap_audit.md) — FZ 1a1b1 — descendant; applies the R-Cross lens to Tessellum's current codebase
- [`thought_cqrs_design_evolution`](thought_cqrs_design_evolution.md) — FZ 1a — the four-step descent that arrived at the synthesis
- [`thought_building_block_ontology_relationships`](thought_building_block_ontology_relationships.md) — FZ 1 — the typed substrate the rules operate over
- [`thought_dks_design_synthesis`](thought_dks_design_synthesis.md) — FZ 2a — DKS as System P's runtime; R-P's enforcement target
- [`thought_retrieval_synthesis`](thought_retrieval_synthesis.md) — FZ 3a — System D's design; R-D's enforcement target
- [`term_cqrs`](../term_dictionary/term_cqrs.md) — canonical term definition

## See Also

- [`entry_architecture_trail`](../../0_entry_points/entry_architecture_trail.md) — per-trail entry point; this node is FZ 1a1b
- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail map

---

**Last Updated**: 2026-05-10
**Status**: Active — FZ 1a1b, Architecture trail
