---
tags:
  - resource
  - analysis
  - counter_argument
  - bb_ontology
  - schema
  - empirical_evidence
  - architectural_composition
  - retrieval
keywords:
  - BB internal transitions
  - same-BB edges
  - architectural composition
  - deep-dive trails
  - model BB overloading
  - sub-kind transitions
  - slipbot qa evidence
  - epistemic vs architectural ontology
topics:
  - Building Block Ontology
  - Knowledge Graph Schema
  - System Architecture
  - Empirical Evidence
language: markdown
date of note: 2026-05-10
status: active
building_block: counter_argument
folgezettel: "1c"
folgezettel_parent: "1"
---

# BB-Internal Transitions: Evidence They Are Critical and Should Be Allowed (FZ 1c)

## The challenge

[FZ 1: `thought_building_block_ontology_relationships`](thought_building_block_ontology_relationships.md) proposes the 8 BB types form a directed graph of 10 epistemic edges. [FZ 1b: `thought_bb_ontology_as_typed_graph`](thought_bb_ontology_as_typed_graph.md) sharpens this into the BB_SCHEMA + corpus split — 16 typed edges in total (8 epistemic + 7 navigation + 1 DKS extension). [FZ 2a2: `thought_dks_as_fsm_on_bb_graph`](thought_dks_as_fsm_on_bb_graph.md) formalises DKS as a finite-state machine over those 16 edges. **Every edge in BB_SCHEMA connects two different BB types. There is no same-type edge — no `model → model`, no `argument → argument`, no `procedure → procedure`.**

This note argues that the omission is a *load-bearing gap*. The parent AB project's empirical investigation (which AB FZ 7g1 documented before this trail diverged into Tessellum) shows BB-internal transitions are not a fringe case — they are the **modal pattern** in real query traffic and they score *higher* in quality than the cross-type transitions BB_SCHEMA was designed to capture. The current Tessellum schema is silent on the dominant traversal pattern in any non-trivial corpus.

This is not a benchmark-design issue (which retrieval handles at its own layer). It is an **ontology-design issue**: the directed graph that v0.0.47 calls "the BB schema" is incomplete as a description of how typed knowledge in a real vault is actually structured and traversed.

## Evidence: the AB Slipbot QA analysis

The AB project's Slipbot QA database (~700 production questions answered by an agent over a typed slipbox) reconstructed the *demand hop chain* — the sequence of BB-typed notes the answer trail walked — for 87 questions. The distribution (from AB FZ 7g1, source: `counter_bb_ontology_misses_same_bb_deep_dive.md`):

| Chain class | Count | % of chains | Avg rating | Avg quality |
|---|---|---|---|---|
| 2 model→model hops | 27 | 31% | 3.52 | 3.19 |
| 3 model→model→model hops | 8 | 9% | **4.13** | **4.04** |
| 4+ model hops | 5 | 6% | 4.00 | 3.85 |
| Other multi-hop (cross-BB) | 47 | 54% | mixed | mixed |

**Same-BB model chains account for ~46% of reconstructed trails. They also score *higher* on average rating + quality than the cross-BB chains the ontology was designed for.** This is reproducible empirical evidence over hundreds of real production questions — not a synthetic benchmark.

Concrete examples (verbatim from AB's experiment table):

- q207 — *"end-to-end process for RnR"* — chain: `model→procedure→model→model` walking `area_rnr → etl_reversal_reclassification → cradle_rnr_bsm_kinesis → model_rnr_bsm_bert → staging tables → OTF variables`. Five hops. Every node is `building_block: model`. Rating 3.
- q152 — *"data source behind this RMP ruleset/intent?"* — chain: `model→model→model` (ruleset → intent → MDS table). Rating 5.
- q587 — *"system-design lens: what was missing in the abuse pipeline?"* — chain: `model→model→model→model→model→model`. Six hops, all `model`. Rating 5.
- q427 — *"KALE knowledge base for buyer abuse function ownership"* — `model→model→model→procedure→model` across 10 capability areas. Rating 5.

**The literal trail "intent → model → variable → Cradle → ETL" exists in q207's hop chain.** Every node along this trail is a `building_block: model` note, but the *kind of system layer* changes at every hop: program area, ETL job, Cradle profile, Bedrock model, staging table, OTF variable.

## Why BB_SCHEMA misses this

The 8 BB types are built on Sascha's epistemic taxonomy — a `model` is "anything that shows relationships between entities." That definition is correct but **non-discriminating**. In any non-trivial production vault, the `model` building block collapses several structurally distinct *system layers* into one type:

| Sub-kind of `model` | Example notes | What it actually represents |
|---|---|---|
| **area** | area_rnr, area_maa, area_hrq | Program / capability area (organisational layer) |
| **intent** | intent_ri_summary, intent_ql_summary | RMP ruleset configuration (decision layer) |
| **model (proper)** | model_rnr_bsm_bert, model_vista_vlm | Trained ML model (inference layer) |
| **variable / OTF datasheet** | variable catalogue, OTF datasheet | Feature definition (feature layer) |
| **Cradle profile** | cradle_rnr_bsm_kinesis | Stream/batch compute spec (compute layer) |
| **ETL job** | etl_reversal_reclassification | Pipeline definition (data layer) |
| **table / data source** | table_d_customer_orders, data_source_mds | Persisted dataset (storage layer) |

Seven different *epistemic objects* describing seven different *layers of the same production system*. A deep-dive query asks "trace this object across system layers" — which mathematically requires moving between these sub-kinds. In BB_SCHEMA's current shape, *all of those moves are invisible*. They all collapse into a single, unrepresented `model → model` non-edge.

The same gap exists for `procedure → procedure` (onboarding → OTF setup → operational handoff), for `concept → concept` (term cross-referencing between definitional notes), and for `navigation → navigation` (entry-point cross-references between trail TOCs). FZ 1b's existing telemetry (`tessellum bb audit`) on a real vault already surfaces this: a vault with hundreds of `model` notes will have many `model → model` body links, all flagged untyped by the current schema.

## The real edge family is architectural, not epistemic

[FZ 1: BB ontology relationships](thought_building_block_ontology_relationships.md) describes the **epistemic lifecycle**: how raw observations mature into named concepts, structured models, predictions, tests, and counter-arguments. That is the cycle [FZ 2a: DKS design synthesis](thought_dks_design_synthesis.md) and DKS's 7-component protocol operationalise.

But the deep-dive trail is not an epistemic move. Going from `intent_ri_summary` to `model_rnr_bsm_bert` is not naming, structuring, predicting, codifying, testing, or challenging. It is **architectural composition** — "what implements this", "what feeds this", "where does this run", "what does this read". These edges have a real, denotational meaning in the production system; they have **no representation** in BB_SCHEMA today.

| Architectural edge | Sub-kind transition | Example |
|---|---|---|
| **Implements** | `model[intent] → model[model]` | intent_ri_summary calls model_return_mtl |
| **Routes to** | `model[intent] → model[area]` | intent_flr_summary belongs to area_flr |
| **Computes** | `model[model] → model[variable]` | model_rnr_bsm_bert uses OTF variable X |
| **Runs on** | `model[model] → model[cradle]` | model_pfw_mtl deployed via cradle_pfw_mtl |
| **Sources from** | `model[cradle] → model[etl]` | cradle reads etl_reversal output |
| **Reads** | `model[etl] → model[table]` | etl consumes table_d_unified_concessions |

Every deep-dive trail is a path through this graph. None of these edges appear in BB_SCHEMA. The epistemic ontology answers *"how does knowledge mature?"*; the architectural ontology answers *"how does the system compose?"*. Both are real ontologies of any non-trivial vault. BB_SCHEMA today represents only the first.

## What this means for DKS

Three concrete consequences for the current implementation:

1. **TESS-005's warnings are not all benign.** Phase 6 (v0.0.48) shipped TESS-005 as WARNING-only with same-BB exemption. The exemption *underflagging* of architectural edges. A vault with 200 model→model body-links — all valid architectural compositions — gets a clean TESS-005 report, but the schema is *not actually describing* those links. The current behaviour is "ignore the elephant"; the architectural layer is invisible by design.

2. **DKS Phase 9 (meta-DKS) sees an empty signal.** Meta-DKS's whole point is to propose schema extensions from runtime patterns. But TESS-005 + BB_SCHEMA together produce zero signal about architectural patterns — same-BB body links are skipped before they reach any aggregator. Meta-DKS will see only the cross-type transitions that *already* fit the schema; the dominant traversal pattern in real corpora will be invisible to it.

3. **DKS step 6's pattern discovery has a narrower aperture than the runtime needs.** The pattern-discovery step (`CTR → MOD` via `pattern_of_failure`, in BB_SCHEMA_DKS_EXTENSIONS) aggregates contradictions into a model. But the architectural patterns in a real corpus — the `model[intent] → model[model] → model[variable]` chains — are *higher-quality patterns* than the contradiction-only patterns DKS currently looks for. Real production vaults learn from architectural composition, not just from disagreement.

## The lean: two layers, not one

The AB resolution (FZ 7g1a) proposes a **two-layer ontology**: Layer A (epistemic, the current 10-edge core) preserved intact, plus Layer B (architectural, same-BB edges parameterised by sub-kind) added in parallel. The two are kept distinct: epistemic edges describe knowledge maturity; architectural edges describe system composition. Same nodes, two edge families.

Tessellum's `note_second_category` (the `tags[1]` source-of-truth introduced in v0.0.30 — see `term_format_spec`) is already populated and validated. It is the natural discriminator for sub-kinds. Layer B edges live as `(source.bb_type, source.note_second_category, target.bb_type, target.note_second_category, label)` 5-tuples.

This is *not* the same as splitting `model` into 7 BB types (which would balloon the schema and require re-classifying every model note in the corpus). It is a *parallel* family of edges that uses the existing sub-kind signal to make same-BB transitions queryable and type-checkable.

## What this note does NOT do

Four things deliberately deferred:

1. **Doesn't add Layer B edges to `BB_SCHEMA` today.** v0.0.49 ships the *evidence* and the *design lens*; the schema change is a Phase 9-class architectural decision that goes through meta-DKS once that lands.
2. **Doesn't change TESS-005's behaviour.** v0.0.48's same-BB skip is currently right *because* the schema doesn't model same-BB edges — flagging them as errors would be misleading. When Layer B lands, TESS-005 generalises naturally (type-check against both layers; only warn when neither matches).
3. **Doesn't relitigate the 8 BB types.** Sascha's typology survives. The change is at the edge layer, not the node layer.
4. **Doesn't presume the architectural edge set is fixed.** The AB analysis named six edges (Implements / Routes to / Computes / Runs on / Sources from / Reads); other domains (legal corpora, scientific writing, code analysis) will have different architectural edges. The mechanism must be *learnable*, not hard-coded.

The companion note [FZ 2c: `thought_dks_transition_model_adaptation`](thought_dks_transition_model_adaptation.md) (forthcoming) treats the *adaptation* question: how DKS should learn the transition model over time, drawing on knowledge-graph literature + industry practice.

## Open questions

| # | Open question |
|--:|----------------|
| **OQ-1c-a** | Is `note_second_category` the right sub-kind discriminator, or should sub-kind be a new YAML field (`bb_subtype:`) with closed enums per BB type? — leans `note_second_category` (already populated; pragmatic). |
| **OQ-1c-b** | Is the architectural-edge set closed per BB type (small finite list — 6 for `model`, maybe 4 for `procedure`, ...) or open-vocabulary like `tags`? — leans closed-per-type but learnable (the discovery process is open; the per-snapshot vocabulary is closed). |
| **OQ-1c-c** | Does the agent need to *know* whether it is doing an architectural traversal vs an epistemic one, or can both edge families be searched uniformly with the user query selecting the path? — affects DKS's argument-generation prompt structure (see FZ 2c). |
| **OQ-1c-d** | Should Layer B edges be exposed in `tessellum.bb.types.BB_SCHEMA` directly, or in a parallel `BB_SCHEMA_ARCHITECTURAL` tuple? — leans the latter for separation of concerns. |
| **OQ-1c-e** | When Layer B is learned (per FZ 2c), at what frequency does the schema refresh — every N cycles, on-demand, or on PR review only? — meta-DKS-class question; defers to Phase 9. |

## Related Notes

- **Parent**: [FZ 1: `thought_building_block_ontology_relationships`](thought_building_block_ontology_relationships.md) — the BB ontology this note counters
- **Sibling (epistemic-focused)**: [FZ 1a: `thought_cqrs_design_evolution`](thought_cqrs_design_evolution.md) — the CQRS chain
- **Sibling (graph-formalised)**: [FZ 1b: `thought_bb_ontology_as_typed_graph`](thought_bb_ontology_as_typed_graph.md) — the typed-graph foundation
- **Companion forward-reference**: [FZ 2c: `thought_dks_transition_model_adaptation`](thought_dks_transition_model_adaptation.md) — how DKS should adapt + learn the transition model

## Related Terms

- [`term_building_block`](../term_dictionary/term_building_block.md) — the 8 BB types
- [`term_format_spec`](../term_dictionary/term_format_spec.md) — `note_second_category` source-of-truth

## See Also

- [`entry_architecture_trail`](../../0_entry_points/entry_architecture_trail.md) — Trail 1 per-trail entry point (this note is FZ 1c)
- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail map

---

**Last Updated**: 2026-05-10
**Status**: Active — FZ 1c, Architecture trail (third branch from the BB ontology root; documents the architectural-layer gap before FZ 2c addresses the adaptation strategy)
