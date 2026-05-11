---
tags:
  - resource
  - analysis
  - argument
  - dks
  - bb_ontology
  - schema_evolution
  - transition_learning
  - meta_dks
  - graphrag
keywords:
  - DKS transition model
  - schema evolution
  - ontology bootstrapping
  - learned transitions
  - AutoSchemaKG
  - AdaKGC
  - OntoRAG
  - GraphRAG ontology
  - sub-kind parameterised edges
  - architectural composition
topics:
  - Dialectic Knowledge System
  - Knowledge Graph Schema
  - Ontology Learning
  - System Architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "2c"
folgezettel_parent: "2"
---

# Adapting DKS to Learn the BB-Internal Transition Model (FZ 2c)

## Thesis

[FZ 1c: `thought_bb_internal_transitions_evidence`](thought_bb_internal_transitions_evidence.md) documented the gap: BB_SCHEMA describes the *epistemic* layer of the ontology but says nothing about the *architectural* layer where most real-corpus transitions live. The AB Slipbot QA evidence — 46% of trails being same-BB chains, scoring higher than cross-BB chains — proves the gap is operationally critical, not theoretical.

This note answers the *adaptation* question: **how should DKS learn the transition model over time?** Drawing on 2024-2026 knowledge-graph literature (schema-adaptable KGs, GraphRAG-driven schema discovery, ontology-bootstrapping pipelines) and the existing DKS phase structure (Phases 6-9 of `plan_dks_expansion`), the lean is a **three-stage hybrid**: bootstrap from corpus statistics → LLM-validated formalisation → meta-DKS-driven schema co-evolution. The transition model is not a static lookup table; it is a learned, dialectically-revised artifact that lives in the event-sourced schema (D3) and grows under meta-DKS discipline (Phase 9).

The long-term story: by Phase 11+, the BB ontology is a *two-layer* graph (epistemic + architectural) where Layer A is human-authored at v0.0.x and Layer B is meta-DKS-induced from the corpus the system is actually accumulating. Both layers are typed, both queryable, both auditable — but Layer B *grows* with the substrate.

## The literature & industry landscape (2024-2026)

The problem FZ 1c surfaces is not unique to Tessellum. The broader knowledge-graph community has spent the last two years exactly on this question: *how does an ontology evolve when the corpus reveals patterns the schema didn't anticipate?* Three converging trends matter:

### Trend 1: Schema induction over static declaration

**AutoSchemaKG** (Wang et al., 2024) induces schemas from large-scale corpora via unsupervised clustering and relation discovery. Multi-stage prompts tailored to different relation types — extract candidates, cluster by surface form, validate against a small held-out gold set — let the schema evolve iteratively as more content arrives. Critically: the relation vocabulary is *not* pre-declared. Same-type relations emerge naturally (e.g., `Person → Person`, `Company → Company`) without special-casing.

**AdaKGC** (Liu et al., 2025) tackles *schema drift* — the gap between yesterday's schema and today's data — through two mechanisms: Schema-Enriched Prefix Instruction (SPI) injects current schema state into prompts; Schema-Constrained Dynamic Decoding (SDD) lets the model respect schema constraints at generation time without full retraining. The schema is treated as a *parameter* of the generation process, not a constant.

For DKS, the takeaway: **schema is what the runtime treats as schema this cycle**. We can refresh it between cycles without rebuilding anything.

### Trend 2: Two-phase ontology bootstrapping (GraphRAG → Ontology RAG)

Production-grade RAG pipelines (deepsense.ai, TrustGraph, neo4j-graphrag) have converged on a two-phase pattern:

1. **Phase α** — open-vocabulary extraction. Use a GraphRAG-style LLM to *discover* what entity types and relations naturally emerge from a document corpus. No schema; everything goes.
2. **Phase β** — formalise the top-K most-frequent types/relations into a closed ontology. Re-extract under the closed schema for production-grade Ontology RAG. The 5-10 entity types that "matter most" become first-class; the long tail gets discarded or generalised.

For DKS, this maps onto: Phase α = scanning the corpus with `BBGraph.from_db()` + computing the empirical (source.bb_type, target.bb_type) co-occurrence matrix; Phase β = meta-DKS proposing the top-K untyped transitions as candidate schema edges, with PR-style approval (D4) and event-sourced application (D3).

### Trend 3: Sub-kind discrimination + typed routing

**OntoRAG** (Sciencedirect 2025) + the OWL-schema-driven Ontology-Driven GraphRAG pipelines use *explicit* type-routing: the LLM is told "this entity is of type X with sub-kind Y; the valid relations from this position are ...". When the schema is precise enough, generation respects it; when it's not, the discovered relations feed back into schema growth.

**Tree-KG** (ACL Long 2025) treats the ontology as an expandable tree where new branches can be added without disturbing existing structure. Branch-additions are themselves events with provenance.

For DKS, this validates the [FZ 1c] lean: *don't* split the 8 BB types into 14+ — that's the static-schema-grows-aggressively trap. *Do* parameterise edges by sub-kind via the existing `note_second_category` field. Type discrimination at the *edge* level, not the *node* level.

### Trend 4: Continuous adaptation without retraining

Across all the 2025 surveys (Branzan; Awesome-GraphRAG; Logic Augmented Generation): the consensus is that schemas evolve *continuously*, not in big-bang rewrites. The mechanism is typically:

- **Append-only event log** of schema changes (D3 is the same pattern)
- **Versioned reads** of the schema per query / per cycle (D8 is the same pattern)
- **Constrained decoding** that respects the current schema state but flags violations as proposals
- **Periodic compaction** — when the event log grows beyond N events, fold into a new snapshot

DKS's Phase 5 + Phase 9 architecture already prefigures all four. The transition-model adaptation just instantiates these patterns for the architectural layer.

## Four adaptation strategies for DKS

Given the literature consensus + the existing Tessellum architecture, four strategies are available. They are not exclusive — the recommended approach (below) combines three.

### Strategy A: Static expansion

Manually author the architectural-edge family into BB_SCHEMA before any runtime use. Pick six edges per [FZ 1c]'s table (Implements / Routes To / Computes / Runs On / Sources From / Reads) and ship them as `BB_SCHEMA_ARCHITECTURAL` alongside the existing `BB_SCHEMA_EPISTEMIC`.

**Pros:** simple; type-checkable today; predictable.
**Cons:** assumes the project author knows all architectural edges for every domain Tessellum is deployed in. The AB six are valid for ML-pipeline corpora; legal-document corpora have entirely different architectural relations (e.g., `Statute → Statute amends/repeals/cites`); scientific corpora have others (`Theorem → Theorem implies/contradicts/specialises`). Static expansion encodes one domain's architectural vocabulary into the package, defeating the point of a *general* substrate.

**Verdict:** wrong-shaped for a multi-domain substrate. Useful as the *starter schema* for a specific deployment, not as the long-term mechanism.

### Strategy B: Corpus-statistics bootstrap

At install time (or on-demand via `tessellum bb learn-transitions`), scan the corpus's realised body-links via `BBGraph.from_db()`, compute the empirical frequency table of `(source.bb_type, source.note_second_category, target.bb_type, target.note_second_category)` tuples, and promote tuples above a threshold to candidate schema edges. The user reviews + approves; approved candidates land in `BB_SCHEMA_USER_EXTENSIONS`.

**Pros:** adaptive per deployment; uses existing telemetry surface; the threshold becomes the only tunable knob.
**Cons:** no label. The bootstrap can detect that `model[intent] → model[model]` happens 40 times but cannot tell whether the edge is "Implements", "Routes To", "Replaces", or "Documents". Edge *labels* require semantic interpretation the corpus statistics alone cannot supply.

**Verdict:** valid as the *evidence collection* phase, but insufficient on its own.

### Strategy C: LLM-validated formalisation (the Phase α → Phase β pattern)

The two-phase GraphRAG approach. Run Strategy B to get the frequency table (Phase α). Then use the LLM backend to *label* each candidate edge — given a sample of 5-10 corpus instances of the candidate transition, ask the model "what is the semantic relation between source and target here?" and cluster by the model's answers. The top-K labels per BB-pair become the candidate edge types; meta-DKS proposes them for inclusion in the schema (Phase β).

**Pros:** combines statistical signal (frequency) with semantic signal (LLM-labeled relation type); produces typed edges with names, not just adjacency claims.
**Cons:** LLM-labeling cost + reliability; the cluster step can collapse genuinely distinct relations into a generic label like "is-related-to."

**Verdict:** the right *formalisation* mechanism; pairs with B as the proposal pipeline.

### Strategy D: Meta-DKS-driven schema co-evolution

Plan 9's meta-DKS treats schema edits as dialectical artifacts: a proposed edge is an *argument* about how the schema should grow; the proposal is attacked by counter-arguments (e.g., "this label is too generic", "this edge already covered by edge X"); surviving proposals land via the event-sourced schema (D3).

**Pros:** uses the existing DKS dialectical discipline; every schema change is auditable + dialectically grounded; recursion stops at meta-meta-schema (D4).
**Cons:** requires Phase 9 to land first; produces small numbers of schema changes per cycle (meta-DKS is slow by design).

**Verdict:** the right *governance* mechanism; pairs with B+C as the approval gate.

## Recommended approach: three-stage hybrid

Compose B + C + D into a single transition-model adaptation pipeline:

```
Stage 1 — Discovery (Strategy B): tessellum bb learn-transitions
    Scans BBGraph.from_db() → empirical frequency table over
    (source.bb_type, source.note_second_category, target.bb_type,
     target.note_second_category) 4-tuples.
    Filter: keep tuples with count ≥ threshold (default 5).
    Output: a candidate-edge JSONL at runs/dks/meta/transition_candidates.jsonl.

Stage 2 — Formalisation (Strategy C): tessellum bb label-transitions
    For each candidate, sample N=5 corpus instances; ask the LLM
    backend to classify the relation. Cluster answers by surface
    form; pick the top-K labels per BB-pair.
    Output: enriched candidates at runs/dks/meta/transition_labels.jsonl
    with proposed edge labels + sample evidence.

Stage 3 — Governance (Strategy D): tessellum dks meta-cycle on candidates
    Meta-DKS treats each labelled candidate as a SchemaEditProposal
    (per D3). Argument generators A and B attack the proposal from
    different angles ("this label is too generic"; "this transition
    is already covered"); contradicts edges + counter-arguments
    surface failure modes; surviving proposals fold into
    BB_SCHEMA_USER_EXTENSIONS as SchemaEditEvents.
```

This is the *Two-Layer Schema Co-Evolution Pipeline*. Layer A (epistemic, the current 10 cross-type edges) stays human-authored at the project layer; Layer B (architectural, the same-BB sub-kind-parameterised edges) is corpus-induced, LLM-labelled, and dialectically-approved.

### Why this composition

Three properties that any one strategy alone misses but the composition guarantees:

1. **Falsifiability.** Strategy B + C + D together produce *typed claims about the schema* (Layer B candidates) that meta-DKS can attack. A candidate that survives the dialectic is by construction more trustworthy than one that's been hand-authored or auto-promoted by frequency alone.
2. **Domain-portability.** The three stages don't bake any domain-specific assumption into the package. ML-pipeline corpora discover `(model[intent], model[model], "Implements")`; legal corpora discover `(law[statute], law[statute], "amends")`; scientific corpora discover their own. The substrate stays general; the *schema instances* are deployment-specific.
3. **Reversibility.** D3's event-sourced schema means schema additions are reversible. A Layer B edge that proves wrong (later cycles find the label misclassified, or the BB-pair was an artifact of bad authoring) gets retracted as a `SchemaEditEvent.kind = "retracted"`, with the existing realised corpus edges becoming "untyped" again — surfaced by TESS-005 as a visible migration signal.

## Long-term: the transition matrix as a learned, queryable resource

Once the three-stage pipeline is operational (Phases 9 + 11+), the *transition matrix* — the full Layer B graph — becomes a first-class queryable resource. Three uses:

1. **DKS argument generation (steps 2-3)** can query "what architectural edges fire from a `model[intent]` source?" before producing the argument. The agent reasons over the schema, not just the warrant set. This grounds DKS's claim that "the substrate is queryable" (commitment 1 in [FZ 2a]) at a higher level than today: the substrate's *vocabulary of composition* is queryable, not just the substrate's *content*.

2. **DKS pattern discovery (step 6)** can identify architectural-pattern failure modes — "every time `model[etl] → model[cradle]` fires, the warrant about Cradle profile validity gets attacked." This is meta-pattern discovery: not just contradictions, but *recurring transition shapes that contradict*.

3. **Vault health audits** (`tessellum bb audit` extended) can flag missing transitions: "this `intent` note has no `Implements` edge to a `model` — is the deployment incomplete?" The schema becomes a *prescriptive* tool for vault structure, not just a *descriptive* type system.

By Phase 11+, the schema is a *contract* the corpus maintains with itself. Every realised edge type-checks against a schema entry; every schema entry has dialectical provenance; meta-DKS observes both. R-P's productive half is operational not just at the cycle level but at the substrate-vocabulary level.

## Integration with existing DKS phases

This adaptation work composes with the existing expansion plan without amendment:

| Phase | Touch | Nature |
|--:|-------|---------|
| 6 (v0.0.48) | `tessellum bb audit` ✓ shipped | Surfaces untyped edges + BB-pair counts — the *input* to Stage 1 |
| 7 (v0.0.49) | `CalibratedConfidence` + retrieval client ✓ shipped | Retrieval used in Stage 2's evidence sampling |
| 8 (v0.0.50) | dispatcher refactor → BB_SCHEMA-driven walk | Same dispatcher walks Layer A + Layer B uniformly |
| 9 (v0.0.51) | meta-DKS | Stage 3 ships here; the `tessellum dks meta` skill is the governance gate |
| **11** (v0.0.x+) | **NEW** `tessellum bb learn-transitions` + `tessellum bb label-transitions` | Stages 1 + 2; pairs with Phase 9's meta-DKS |

Phase 11 is the natural home for the discovery + labelling pipeline. It is *not* a v0.2-prerequisite: Phases 6-10 ship a usable DKS without it. Phase 11 is the long-term *adaptation* layer — what makes Tessellum's schema *self-evolving* rather than just *correctly-typed*.

## What this is NOT proposing

Five carve-outs to prevent over-interpretation:

1. **Not an automatic schema grower.** Stage 3's governance gate (meta-DKS) is dialectical, not statistical. Frequency alone never promotes a candidate; the candidate must survive attack.
2. **Not a replacement for Layer A.** The 10 epistemic edges + 7 navigation + 1 DKS extension stay human-authored and architecturally load-bearing. Layer B is *additive*.
3. **Not the same as splitting BB types.** The 8 types survive. Sub-kind discrimination happens at the edge layer via `note_second_category`, not at the node layer via new BB types.
4. **Not requiring re-classification of existing corpus.** Existing notes' `building_block` and `note_second_category` fields are already populated. The Layer B edges *type* the existing body links retroactively.
5. **Not auto-applied to v0.0.49.** This is a Phase 11+ proposal. v0.0.48-49 sees no immediate runtime change. The notes here + FZ 1c constrain how Phase 8-9 land so the pipeline remains *possible* without re-architecting.

## Open questions

| # | Open question |
|--:|----------------|
| **OQ-2c-a** | At what corpus size does Stage 1's frequency-table approach become statistically meaningful? — lean: ≥ 100 BB-typed notes minimum; for `model` sub-kinds specifically, ≥ 20 instances per sub-kind. |
| **OQ-2c-b** | Should Stage 2's LLM-labelling use the same Composer pipeline as DKS cycles, or a separate `skill_tessellum_label_transitions` skill? — leans separate skill (the labelling cycle is its own dialectic; reuses the 7-component template). |
| **OQ-2c-c** | What's the relationship between Layer B edges and TESS-005's WARNING severity? — lean: when a body link instantiates a Layer B edge, TESS-005 emits INFO (or no message); when neither layer matches, WARNING (current behaviour). |
| **OQ-2c-d** | Do Layer B edges have *strength* / *confidence* attached (per AutoSchemaKG's per-edge confidence), or are they binary present/absent? — lean: binary in v1; learned confidence is Phase 12+. |
| **OQ-2c-e** | When the corpus shifts (e.g., a deployment moves from ML-pipelines to legal-documents), how does the transition matrix migrate? — lean: per-corpus snapshots; cross-corpus federation is v0.3+ research. |

## Related Notes

- **Parent**: [FZ 2: `thought_dks_evolution`](thought_dks_evolution.md) — the design descent
- **Sibling (★ synthesis)**: [FZ 2a: `thought_dks_design_synthesis`](thought_dks_design_synthesis.md) — the 7-component pattern this note's adaptation extends
- **Sibling (FZ duality)**: [FZ 2a1: `thought_dks_fz_integration`](thought_dks_fz_integration.md)
- **Sibling (FSM formalism)**: [FZ 2a2: `thought_dks_as_fsm_on_bb_graph`](thought_dks_as_fsm_on_bb_graph.md) — the FSM the transition model parameterises
- **Sibling (runtime integration)**: [FZ 2b: `thought_dks_runtime_integration`](thought_dks_runtime_integration.md)
- **Cross-trail (the gap)**: [FZ 1c: `thought_bb_internal_transitions_evidence`](thought_bb_internal_transitions_evidence.md) — the evidence this note's strategy addresses
- **Cross-trail (graph foundation)**: [FZ 1b: `thought_bb_ontology_as_typed_graph`](thought_bb_ontology_as_typed_graph.md)
- **Plan reference**: [`plan_dks_expansion`](../../../plans/plan_dks_expansion.md) — Phase 8 + Phase 9 are prerequisites; Phase 11 is where Stage 1 + 2 live

## See Also

- [`entry_dialectic_trail`](../../0_entry_points/entry_dialectic_trail.md) — Trail 2 per-trail entry point (this note is FZ 2c)
- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail map

## Sources

Literature surveyed for this note's adaptation strategy:

- [From LLMs to Knowledge Graphs: Building Production-Ready Graph Systems in 2025](https://medium.com/@claudiubranzan/from-llms-to-knowledge-graphs-building-production-ready-graph-systems-in-2025-2b4aff1ec99a) — Branzan's 2025 production-graph overview
- [Tree-KG: An Expandable Knowledge Graph Construction](https://aclanthology.org/2025.acl-long.907.pdf) — ACL 2025; expandable-tree ontology architecture
- [Schema-Adaptable Knowledge Graphs](https://www.emergentmind.com/topics/schema-adaptable-knowledge-graph-construction) — summary covering AutoSchemaKG, AdaKGC, and adjacent work
- [LLM-empowered knowledge graph construction: A survey](https://arxiv.org/html/2510.20345v1) — arXiv 2510.20345
- [On the Evolution of Knowledge Graphs: A Survey and Perspective](https://arxiv.org/html/2310.04835v3) — arXiv 2310.04835
- [Schema Generation for Large Knowledge Graphs Using Large Language Models](https://arxiv.org/abs/2506.04512) — arXiv 2506.04512
- [Ontology-Driven Knowledge Graph for GraphRAG](https://deepsense.ai/resource/ontology-driven-knowledge-graph-for-graphrag/) — deepsense.ai, April 2025
- [Ontology RAG: Schema-Driven Knowledge Extraction](https://trustgraph.ai/guides/key-concepts/ontology-rag/) — TrustGraph (production GraphRAG vendor)
- [Ontology Learning and Knowledge Graph Construction: A Comparison of Approaches and Their Impact on RAG Performance](https://arxiv.org/html/2511.05991v1) — arXiv 2511.05991
- [GraphRAG Publications Overview for July 2025](https://datavera.org/en/graphrag-july2025.html) — datavera GraphRAG round-up
- [Awesome-GraphRAG](https://github.com/DEEP-PolyU/Awesome-GraphRAG) — DEEP-PolyU curated list of graph-based RAG resources

---

**Last Updated**: 2026-05-10
**Status**: Active — FZ 2c, Dialectic trail (third branch from DKS root; companion to FZ 1c's evidence note; specifies the three-stage adaptation pipeline for Phase 11+)
