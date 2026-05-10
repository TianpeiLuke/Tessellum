---
tags:
  - resource
  - analysis
  - argument
  - cqrs
  - architecture
  - design_history
keywords:
  - CQRS design evolution
  - three invariance regimes
  - two systems not three
  - System P System D
  - prescriptive vs descriptive
  - Ontology DKS coupling
  - architectural pivot
topics:
  - System Architecture
  - CQRS
  - Design History
  - Tessellum Foundations
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "1a"
folgezettel_parent: "1"
---

# How the CQRS Architecture for Tessellum Evolved

## Thesis

The CQRS shape Tessellum ships with — **System P (prescriptive, write side: typed authoring) ⊥ System D (descriptive, read side: retrieval) ⊥ one shared substrate (the vault)** — did not arrive fully formed. It was the product of a four-step argumentative descent that started with the typed Building Block graph and ended with a single re-drawing of the system boundary. This note narrates that descent so a future contributor understands *why* the two-system split is the right one and not the obvious one.

## The descent in four steps

### Step 1 — The substrate: 10 typed epistemic edges (FZ 1)

The starting point was [`thought_building_block_ontology_relationships`](thought_building_block_ontology_relationships.md) — the 8-type Building Block taxonomy promoted to a directed graph by adding 10 labeled epistemic edges. The graph is the substrate: every claim about how Tessellum should behave at runtime ultimately reduces to a claim about how this graph is read, written, traversed, or extended.

No architecture yet — just a typed vocabulary plus relationships.

### Step 2 — First framing: three independent invariance regimes (rejected)

The first architectural model proposed three peer-equal layers:

| Layer | Operates on | Discipline |
|---|---|---|
| L1 — **Ontology** | The static BB graph | Declarative (BB types + 10 edges; refuse to grow ad-hoc) |
| L2 — **Retrieval** | The graph, read-only | Computational (BM25 + dense + RRF + best-first BFS) |
| L3 — **DKS** | The graph, write-back | Procedural (6-phase dialectic that updates warrants) |

Each layer was framed as an *invariance regime* — something to defend against its own failure mode (schema rot, retrieval drift, dialectic conflation). Three layers, two boundaries (L1↔L2 and L2↔L3), three disciplines.

This framing felt clean but was wrong in one specific way that took an explicit counter-argument to surface.

### Step 3 — The counter: the seam is in the wrong place

The pivot was the observation that **two of the three regimes are coupled, and the third is genuinely separate**:

| Question | Answer | Implication |
|---|---|---|
| Does DKS depend on the Ontology? | Yes — DKS's protocol is *expressed* in BB-edge vocabulary. Change the edges and the protocol shifts. | L1 and L3 co-vary. |
| Does Retrieval depend on the Ontology? | No — Retrieval operates on whatever the substrate holds (text + frontmatter + links) regardless of which edge types are valid. | L2 is independent. |
| Can DKS call Retrieval? Can Retrieval call DKS? | DKS may read Retrieval results; Retrieval never invokes DKS. | Asymmetric — L2↔L3 is a one-way calls relationship. |
| Can the Ontology call DKS? Can DKS call the Ontology? | Neither — DKS *implements* the Ontology. They are specification and runtime of one thing. | L1↔L3 is not a calls relationship at all. |

The three-regime model treated L1↔L3 as a boundary equivalent to L2↔L3, but the boundary tests don't agree. **L1 and L3 are facets (static schema + dynamic execution) of one prescriptive system.** L2 is a different *kind* of operation entirely — computation over whatever the prescriptive system has produced.

There are two systems, not three. One boundary, not two.

### Step 4 — The synthesis: System P ⊥ System D over one substrate (FZ 1a1)

The cleaned-up architecture in [`thought_synthesis_two_systems_cqrs_value_proposition`](thought_synthesis_two_systems_cqrs_value_proposition.md) makes one boundary the architectural commitment:

```
                ┌──────────────────────────────────────┐
                │  vault/  (markdown + YAML)           │
                │  the shared substrate                │
                └────────────┬─────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            │                                 │
            ▼                                 ▼
  ┌─────────────────────┐         ┌─────────────────────┐
  │  System P            │         │  System D            │
  │  (Prescriptive)      │         │  (Descriptive)       │
  │                      │         │                      │
  │  Ontology (static)   │         │  Retrieval           │
  │  + DKS (dynamic)     │         │  (BM25 + dense +     │
  │                      │         │   RRF + BFS)         │
  │                      │         │                      │
  │  declares            │         │  computes            │
  │  writes              │         │  reads               │
  └─────────────────────┘         └─────────────────────┘
```

The two systems differ on every axis worth distinguishing:

| Axis | System P | System D |
|---|---|---|
| Operation kind | Declaration | Computation |
| Direction | Writes the substrate | Reads the substrate |
| Authority | Typed prescriptive knowledge (what *should* hold) | Statistical / structural inference (what *appears* to hold) |
| Failure mode | Schema rot, drift between schema and runtime | Retrieval drift, hit-quality regression |
| Discipline | Refuse to grow ad-hoc; require dialectic for warrant updates | Refuse to mutate the substrate; optimize for answer quality |

The seam is **declaration vs computation**, not three peer layers. Once that boundary is the architectural commitment, every downstream decision (where the runtime traces live, how the indexer is invoked, what Composer does, where MCP plugs in) falls out cleanly — they are all positioned relative to one boundary, not negotiated across three.

## Why the four-step descent was necessary

The two-system shape is *obvious in retrospect* — CQRS is a well-known pattern. But three properties of the design made it non-obvious in advance:

1. **Ontology and DKS look like different things.** A static schema and a runtime protocol seem like different architectural layers; the fact that DKS is *the runtime of the schema* takes explicit testing to see.
2. **Three boundaries are easier to negotiate than one.** A three-layer model lets you defer "which side does X belong on?" by inventing a middle layer. A two-system model forces you to pick a side for every piece of work, which is harder up front but cleaner downstream.
3. **CQRS is usually pitched at the storage layer.** The conventional CQRS pattern splits *databases* (write store vs read store). Tessellum's split is at the *knowledge* layer — same shape, different substrate. It takes the BB ontology to make this analogy load-bearing rather than decorative.

## What this means for users

The descent is encoded in the seed vault. A new Tessellum user who reads [`term_cqrs`](../term_dictionary/term_cqrs.md) sees the destination but not the journey. This note is the journey — useful when:

- A contributor asks "why this architecture and not the more obvious three-layer one?"
- A user wonders why the runtime trace directory (`runs/composer/`) sits outside both `vault/` (substrate) and `data/` (System D build output) — because *runtime* traces don't belong on either side of the read/write boundary; they document the bridge between them.
- A future architectural change comes up. The criterion is: does the change preserve the *one* boundary? If not, you're recreating the three-regime confusion.

## Related Notes

- [`thought_building_block_ontology_relationships`](thought_building_block_ontology_relationships.md) — FZ 1 — the substrate the descent starts from
- [`thought_synthesis_two_systems_cqrs_value_proposition`](thought_synthesis_two_systems_cqrs_value_proposition.md) — FZ 1a1 — the synthesis this evolution arrives at
- [`thought_cqrs_essence_for_tessellum`](thought_cqrs_essence_for_tessellum.md) — FZ 1a1a — the distilled essence for users
- [`term_cqrs`](../term_dictionary/term_cqrs.md) — the term-dictionary canonical definition
- [`term_building_block`](../term_dictionary/term_building_block.md) — the 8 BB types Step 1 starts from
- [`term_dialectic_knowledge_system`](../term_dictionary/term_dialectic_knowledge_system.md) — the DKS runtime that turned out to be a System P facet

## See Also

- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — the FZ trail this note sits in

---

**Last Updated**: 2026-05-10
**Status**: Active — FZ 1a in the Architecture trail
