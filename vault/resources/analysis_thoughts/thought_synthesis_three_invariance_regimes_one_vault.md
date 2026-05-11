---
tags:
  - resource
  - analysis
  - argument
  - synthesis
  - star_synthesis
  - ontology
  - retrieval
  - dks
  - architecture
  - meta
keywords:
  - three invariance regimes
  - federation of disciplines
  - type vs index vs cycle
  - one vault three protocols
  - ontology retrieval DKS synthesis
  - design discipline separation
  - shared vocabulary anti-pattern
  - architectural boundary
  - FZ 7g1 trail synthesis
  - sharpened argument
topics:
  - Knowledge Management
  - System Architecture
  - Information Retrieval
  - Dialectic Knowledge System
  - Epistemology
language: markdown
date of note: 2026-04-24
status: active
building_block: argument
folgezettel: "7g1a1a1a1"
folgezettel_parent: "7g1a1a1a"
author: lukexie
---

# ★ Synthesis: One Vault, Three Invariance Regimes — Why Ontology, Retrieval, and DKS Must Be Designed as Independent Disciplines (FZ 7g1a1a1a1)

## The Sharpened Thesis

The seven-note chain from FZ 7g to FZ 7g1a1a1a is *one* argument expressed in stages. Stated in its sharpest form:

> **The vault has three layers because three distinct invariance regimes exist. Each regime has a different thing that must stay constant across change, a different thing that is allowed to drift, a different design discipline. Treating them as one system — the original sin the chain diagnosed — confuses the three regimes and produces design errors at every layer.**

The three regimes are:

| Layer | What is **invariant** | What is **allowed to drift** | Design discipline |
|---|---|---|---|
| **1 — Ontology** | The 8 BB types and 10 epistemic edges (FZ 7g) | Sub-kinds, project areas, individual notes | Declarative typing |
| **2 — Retrieval** | The interface (`query → ranked list`) and the schema-free computation | Substrate content, sub-kinds, link density | Computational ranking |
| **3 — DKS** | The dialectic protocol (observe → name → structure → predict → test → challenge → re-observe) | Warrants, rules, gap reports, individual cycle outcomes | Procedural production |

These regimes touch the same notes but defend different invariants against different threats. They cannot be collapsed without violating at least two of them.

---

## What the Trail Actually Diagnosed

Restated in one paragraph: the vault community had been treating the BB Ontology (FZ 7g) as if it answered three questions when it answered only one. **It answers "what kind of knowledge is this and what should follow it epistemically?"** It does not answer "where does this data physically come from in the system?" (FZ 7g1's deep-dive) and it does not answer "how do I find existing notes about X?" (FZ 7g1a1a's retrieval). The first two attempts to extend FZ 7g (typed architectural edges in FZ 7g1a; treating sub-kinds as schema in the same note) failed because they tried to repurpose ontology vocabulary for problems ontology was never designed to solve.

The chain's net intellectual move: **stop overloading "ontology"**.

---

## Three Invariance Regimes, In Detail

### Layer 1 — Ontology: Invariant Types, Drifting Substrate

**What stays constant**: Sascha's 6 BB types + the vault's 2 additions (procedure, navigation) = 8 types. The 10 directed epistemic edges (Naming, Structuring, Predicting, Codifying, Testing, Challenging, Motivates, Execution, Indexes — FZ 7g). These are claims about how *knowledge itself* matures. They are invariant because they describe the universal structure of inquiry, not the contents of any particular vault.

**What drifts**: The notes that fill these slots. The sub-kinds (`note_second_category`) — 94 today, more tomorrow. The PARA Areas of Responsibility ([Forte](../digest/digest_para_method_forte.md)). The Circle of Control ([Covey](../digest/digest_7_habits_covey.md), [term](../term_dictionary/term_circle_of_influence.md)) of whoever is editing the vault.

**Failure mode**: Schema rot. If the type set is allowed to drift (e.g., FZ 7g1a's typed architectural edges parameterized by sub-kind), the ontology decays into a folksonomy that cannot drive prescriptive reasoning anymore. **Defended by**: refusing to add new edge types in response to operational pressure. The pressure belongs at Layer 2.

**Discipline**: Declarative typing. Stable across users, projects, time. Rare and deliberate revisions only.

### Layer 2 — Retrieval: Invariant Interface, Drifting Implementation

**What stays constant**: The interface — the user gives a query, the system returns a ranked list of notes. The interface does not know about types, edges, sub-kinds, projects, or PARA Areas. It only knows: query in, notes out.

**What drifts**: The implementation. Today: dense retrieval (sentence-transformers) for candidate generation, hybrid re-rank using PPR + BB alignment + link context (FZ 5e1c1c, refined in FZ 7g1a1a1a). Tomorrow: better embeddings, learned re-rankers, fine-tuned bi-encoders. The substrate content drifts continuously — the retriever recomputes on every query.

**Failure mode**: Coupling to ontology. FZ 5e2 and FZ 5h1 measured this directly: BB-routed strategies are Pareto-dominated by uniform dense retrieval. Inserting ontology between the user and the index *hurts*. **Defended by**: keeping the candidate-generation step schema-free.

**Discipline**: Computational ranking. Optimized for Hit@K, latency, and answer quality — *not* for ontological purity. The graph and the BB labels enter only at re-ranking and context assembly, where embeddings are blind ([FZ 5e1c1b](thought_structural_retrieval_value_beyond_embeddings.md): multi-hop chains, FZ trail ordering, BB filtering).

### Layer 3 — DKS: Invariant Protocol, Drifting Warrants

**What stays constant**: The dialectic cycle. Six phases: observe → name → structure → predict → test → challenge → re-observe. The same shape works in Athelas-Conv (1,855 conversations → 23 rules), and would work in any domain with enough disagreement signal ([FZ 8c5c1a3](analysis_dks_novelty_assessment.md): generalizes to ATO, seller abuse, content moderation, claims, MO governance).

**What drifts**: The warrants (Toulmin's "rule" component). The rules. The patterns. The gap reports. Every cycle ends with a different warrant set than it started with. The system's *contents* are perpetually in motion; the system's *protocol* is fixed.

**Failure mode**: Being conflated with retrieval. DKS was sometimes pitched as "the answer engine on the slipbox." It is not. It is the *write protocol* — the engine that produces and updates warrants. Asking DKS to answer a user query is a category error: it would trigger a multi-hour write cycle for a question that needs sub-second retrieval. **Defended by**: routing user queries to Layer 2; routing scheduled production to Layer 3.

**Discipline**: Procedural production. Stateful, multi-cycle, ontology-dependent. Operates on Layer 1's prescriptive edges as production steps. Calls Layer 2 as a subroutine when it needs to check existing knowledge.

---

## The Corrected Design Rules

Six rules that follow from the three-regime view. Each replaces a tempting confusion:

| Rule | Replaces |
|---|---|
| **R1**: Add BB types only when the *epistemic structure of inquiry* gains a new kind. Never add types in response to a new project, tool, or sub-domain. | Adding "model" sub-types to fix the deep-dive (FZ 7g1a). |
| **R2**: Edge labels in Layer 1 are prescriptive ("do this next"); edge labels in Layer 2 do not exist. The retriever sees an unlabeled link graph. | Treating typed edges as a retrieval signal (FZ 7g1a). |
| **R3**: Sub-kinds (`note_second_category`) are query-time facets, never edge schemas. They live in the WHERE clause, not in the ontology. | Schematizing sub-kinds (FZ 7g1a1's diagnosis). |
| **R4**: Candidate generation is dense; everything else is hybrid. Graph signals enter at re-rank and context assembly, never at candidate generation. | PPR-primary recipes (FZ 7g1a1a v1, corrected in FZ 7g1a1a1a). |
| **R5**: DKS is allowed to call retrieval; retrieval is not allowed to call DKS. Background processes call foreground primitives, never the reverse. | Conflating DKS with the answer engine (FZ 7g1a1a1's diagnosis). |
| **R6**: When in doubt about which layer owns a behavior, ask which invariant it defends. If it must work across users, projects, and time → Layer 1. If it must work per-query, schema-free → Layer 2. If it must close a write-side loop on its own state → Layer 3. | "Just put it in DKS" / "just add an ontology edge". |

---

## What Changed About Each Layer After the Trail

### Layer 1 (Ontology) — Smaller and Cleaner

FZ 7g stands as written. What changed: the *temptation* to extend it has a name now (R1). The 10 epistemic edges are no longer asked to do retrieval work or to encode system architecture. They describe knowledge maturation and nothing else. The literature contribution sharpens: the BB Ontology is "an ontology over Sascha's typology with directed reasoning edges," not "the schema of the abuse domain."

### Layer 2 (Retrieval) — Empirically Grounded and Architecturally Bounded

The FZ 5 trail (4,823 questions × 14 strategies) had quietly produced two enormous results — Pareto dominance of dense retrieval (FZ 5e2) and refutation of BB pre-routing (FZ 5h1) — that this chain only used in the final step. The within-BB recipe in FZ 7g1a1a is now the recipe in FZ 7g1a1a1a: dense for candidates, graph for re-rank, BB for assembly. The interface ("query → ranked list") is the contract; the implementation is free to evolve.

### Layer 3 (DKS) — Scope Narrowed, Contribution Sharpened

DKS was sometimes pitched as a thinking engine over the vault — a phrase that quietly included retrieval. After this chain, DKS is the **write-side protocol** that produces warrants from disagreement. Its literature gap is "closed-loop dialectic for warrant precision" ([FZ 8c5c1a3](analysis_dks_novelty_assessment.md), [FZ 8c5c1a9](thought_dks_literature_review_and_contribution.md)) — a sharper, more publishable claim than "a system over the slipbox." The 32.7% F1 improvement in Athelas-Conv ([FZ 1a1](thought_rq5_answered_by_dks.md)) is warrant precision, not Hit@K.

---

## What This Enables Next

Five things the federation-of-disciplines view makes operationally tractable:

1. **Independent optimization**. Each layer can be improved without coordinating with the other two. Better embeddings improve Layer 2; new sub-kinds appear without disturbing Layer 1; DKS cycle improvements happen on a hours-cadence without affecting retrieval latency.

2. **Cleaner staffing / responsibility**. Layer 1 is editorial (rare, careful). Layer 2 is engineering (continuous, measurable). Layer 3 is research (long cycles, formal models). Different stakeholders, different review processes.

3. **Cleaner publication strategy**. DKS publishes against MAD / formal argumentation / closed-loop knowledge construction literature. Retrieval publishes against IR / Graph-RAG / hybrid retrieval literature. Ontology publishes against PKM / Zettelkasten / typed knowledge literature. No paper is forced to be all three.

4. **A possible Layer 0 — Ingestion**. Capture skills (`slipbox-digest-paper`, `slipbox-capture-term-note`, `slipbox-digest-quip`, OCR, transcription) all produce typed BB notes from external sources. They are not retrieval; not DKS; not the substrate itself. They are **ingestion** — converting the world's content into Layer 1 vocabulary. Promoting this to Layer 0 (and possibly a Layer 4 — Presentation, for diagram exports, knowledge-graph visualizations, agent skills exposing the vault) yields a tidy 5-layer model.

5. **A clean meta-question for the research program**. With layers separated, the [FZ 5 meta-question](thought_meta_question_value_of_typed_knowledge.md) ("does typed knowledge improve retrieval?") gets its true answer: typed knowledge (Layer 1) improves *re-ranking and context assembly* but not *candidate generation*. The value is real, measurable, and bounded — exactly the FZ 5e1c1c hybrid-retrieval prediction.

---

## The Meta-Lesson

The trail produces one sentence that generalizes beyond this vault:

> **A long-lived knowledge system attracts conflations because everything in it shares vocabulary. The discipline of the system is to defend the boundaries between things that share words but not invariants.**

The vault community was not wrong to notice that BB types appear in retrieval, in DKS, and in the ontology. The mistake was assuming this overlap meant the three could be designed as one. Shared vocabulary is what *enables* the three layers to interoperate cleanly; treating shared vocabulary as evidence of a shared problem is what *prevents* clean interoperation.

This is recognizably an old lesson — Conway's Law, the principle of separation of concerns, [Sascha's "Focus" principle](../digest/digest_atomicity_guide_sascha.md), Covey's [Circle of Influence](../term_dictionary/term_circle_of_influence.md). The chain re-derived it in this vault's own language. The shape of the lesson recurs because the underlying pressure recurs: *every* multi-purpose system tempts its operators to fuse what should remain distinct.

---

## Open Questions

| # | Open Question |
|---|---|
| **OQ-7g1a1a1a1-a** | Should this synthesis be promoted to a top-level FZ branch (its own number, alongside FZ 7) given that it reframes how the entire vault is understood? Or does it correctly belong as a leaf of the chain that produced it? |
| **OQ-7g1a1a1a1-b** | The five-layer extension (Ingestion + Substrate + Retrieval + DKS + Presentation) deserves its own thought note. Is it a child of this synthesis or a parallel branch under a new "vault architecture" trail? |
| **OQ-7g1a1a1a1-c** | The "shared vocabulary, separate invariants" principle is general — does the vault have other instances where it applies (e.g., "skill" used to mean both atomic capability and pipeline-orchestrating macro)? |
| **OQ-7g1a1a1a1-d** | The DKS literature contribution ("closed-loop dialectic for warrant precision") is sharper after this chain — should the FZ 8c5c1a9 literature review be revised to lead with this single claim? |

---

## Related Notes

### Sharpening Counter
- **[FZ 7g1a1a1a1a: Counter — Two Systems, Not Three](counter_two_systems_not_three_ontology_and_dks_are_one.md)**: argues this synthesis over-fragmented. Ontology + DKS are static/dynamic facets of one **Prescriptive System** (declaration); Retrieval is the **Descriptive System** (computation). Architectural pattern: **[CQRS](../term_dictionary/term_cqrs.md)**. Six rules collapse to three; R5 promoted to the load-bearing rule.

### The Chain This Synthesizes
- [FZ 7g](thought_building_block_ontology_relationships.md) — the original BB Ontology (Layer 1).
- [FZ 7g1](counter_bb_ontology_misses_same_bb_deep_dive.md) — counter: deep-dive trails are real.
- [FZ 7g1a](thought_two_layer_bb_ontology_epistemic_plus_architectural.md) — first attempt: typed architectural edges (refuted).
- [FZ 7g1a1](counter_subkinds_are_emergent_areas_of_responsibility.md) — counter: sub-kinds are emergent (PARA + Circle of Control).
- [FZ 7g1a1a](thought_within_bb_navigation_is_retrieval_not_ontology.md) — reframe: within-BB navigation is retrieval (recipe v1).
- [FZ 7g1a1a1](thought_dks_constructs_knowledge_retrieval_consumes_it.md) — synthesis: three layers (this note's direct predecessor).
- [FZ 7g1a1a1a](thought_fz5_evidence_confirms_three_layer_and_sharpens_within_bb_recipe.md) — empirical confirmation + recipe v2.

### Layer 2 Evidence (FZ 5 Retrieval Trail)
- [FZ 5e2](counter_dense_retrieval_refutes_bb_strategy_routing.md) — Pareto dominance of dense retrieval.
- [FZ 5h1](counter_uniform_retrieval_supersedes_bb_prerouting.md) — BB pre-routing refuted.
- [FZ 5e1c1c](thought_hybrid_retrieval_dense_plus_graph.md) — hybrid retrieval recipe.
- [FZ 5e1c1b](thought_structural_retrieval_value_beyond_embeddings.md) — three tasks where structure is non-redundant.

### Layer 3 (DKS) Notes Affected
- [FZ 8c5c1a](../../projects/athelas_conv/athelas_conv_dialectic_knowledge_system.md) — DKS Design (write-side protocol).
- [FZ 8c5c1a3](analysis_dks_novelty_assessment.md) — Novelty Assessment (literature contribution sharpened).
- [FZ 8c5c1a9](thought_dks_literature_review_and_contribution.md) — Literature Review (sharper after synthesis).
- [FZ 8c5c1a10](thought_dks_is_thinking_protocol_on_slipbox_kg.md) — needs third entity (Retrieval).
- [FZ 1a1](thought_rq5_answered_by_dks.md) — RQ5 is a write-side question, not a retrieval question.

### Source Lenses
- [Digest: PARA Method (Forte)](../digest/digest_para_method_forte.md) — Areas of Responsibility = sub-kind drift.
- [Digest: 7 Habits (Covey)](../digest/digest_7_habits_covey.md) — Circle of Control = bounded sub-kind authority.
- [Digest: Atomicity Guide (Sascha)](../digest/digest_atomicity_guide_sascha.md) — Focus principle = the boundary discipline this synthesis re-derives.

### Entry Points
- [Entry: Argument Trail](../../0_entry_points/entry_abuse_slipbox_argument_trail.md) — this note is FZ 7g1a1a1a1 (★).

---

**Last Updated**: 2026-04-24
