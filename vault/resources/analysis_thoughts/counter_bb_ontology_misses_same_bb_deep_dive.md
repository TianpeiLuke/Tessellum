---
tags:
  - resource
  - analysis
  - counter_argument
  - ontology
  - building_blocks
  - retrieval
  - deep_dive
  - epistemology
keywords:
  - BB ontology critique
  - same-BB traversal
  - deep dive trail
  - model BB overloading
  - architectural composition
  - intent to ETL trail
  - Cradle profile
  - OTF variable
  - epistemic vs architectural
  - SlipBot deep dive questions
topics:
  - Knowledge Management
  - Ontology
  - Building Blocks
  - Information Retrieval
language: markdown
date of note: 2026-04-24
status: active
building_block: counter_argument
folgezettel: "7g1"
folgezettel_parent: "7g"
author: lukexie
---

# Counter: The BB Ontology Has No Edge for the Deep-Dive Trail — Same-BB Multi-Hop (intent → model → variable → Cradle → ETL) Lives Entirely Inside the "model" Type (FZ 7g1)

## The Challenge

[FZ 7g](thought_building_block_ontology_relationships.md) proposes that the 8 building block types form a **directed graph of 10 epistemic edges** (Naming, Structuring, Predicting, Codifying, Testing, Challenging, Execution, Indexing). Every edge in the ontology connects **two different types**. There is **no edge that begins and ends at the same type** — no model→model, no procedure→procedure, no concept→concept.

But the most common, highest-value SlipBot question pattern — the **deep-dive request** — is a multi-hop trail that lives **entirely inside the "model" building block**. A typical deep-dive trail is:

```
intent note (model BB)
  → model note     (model BB)
  → variable note  (model BB)
  → Cradle note    (model BB)
  → ETL note       (model BB)
```

Five hops. Same building block at every hop. **Zero edges in the FZ 7g ontology fire on this path.** The ontology is silent on the dominant traversal pattern in the vault's most-asked question genre.

This is not a benchmark-design issue (which [FZ 5k2c](counter_ontology_violations_in_real_multi_hop.md) addresses by splitting multi-hop into vertical/horizontal at the evaluation layer). This is an **ontology-design issue**: the directed graph FZ 7g calls "the ontology" is incomplete as a description of how knowledge in this vault is actually structured and traversed.

## Evidence: The QA Database Confirms Same-BB Deep Dives Dominate

### Hop-Chain Distribution (700 SlipBot questions, slipbot_qa.db)

Of the 87 questions where the answer trail's `demand_hop_chain` was reconstructed:

| Chain class | Count | % of chains | Avg rating | Avg quality |
|---|---|---|---|---|
| 2 model→model hops | 27 | 31% | 3.52 | 3.19 |
| 3 model→model→model hops | 8 | 9% | **4.13** | **4.04** |
| 4+ model hops | 5 | 6% | 4.00 | 3.85 |
| Other multi-hop (cross-BB) | 47 | 54% | mixed | mixed |

**Same-BB model chains account for ~46% of reconstructed trails.** They also score **higher** on average rating and quality than the cross-BB chains the ontology was designed for. The deep-dive pattern is not a fringe case — it is the modal pattern, and users find it valuable when answered.

### Concrete Deep-Dive Trails From SlipBot Questions

| Q# | Question (abridged) | Demand Hop Chain | Rating |
|---|---|---|---|
| q207 | What is the end-to-end process for RnR? | model→procedure→model→model (area_rnr → etl_reversal_reclassification → cradle_rnr_bsm_kinesis → model_rnr_bsm_bert → staging tables → OTF variables) | 3 |
| q152 | Data source behind this RMP ruleset/intent? | model→model→model (ruleset → intent → MDS table) | 5 |
| q163 | Data source behind intent na-rnr-automation-stage-1? | model→model→model (ruleset → intent → MDS table) | 4 |
| q37 | Which intent is MTL model hosted in? | model→model→model (model_return_mtl → deployment → intent_flr_summary) | 4 |
| q19 | Dive deep into intent evaluation routing to human queues | model→model→model | 4 |
| q427 | KALE knowledge base for buyer abuse function ownership | model→model→model→procedure→model (across 10 capability areas) | 5 |
| q587 | System-design lens: what was missing in the abuse pipeline? | model→model→model→model→model→model | 5 |
| q628 | What is ATO and how does BAP detect ATO in MAA abuse? | concept→model→model→model | 5 |
| q278 | Workflow of customer return | model→model→procedure→procedure→model | 5 |
| q49 | Map evaluations to treatments | navigation→model→model→concept | 4 |

The literal trail in the user's challenge — **intent → model → variable → Cradle → ETL** — is materialized in q207. Every node along q207's deep-dive is a "model" BB note, but the *kind* of system layer changes at every hop: program area, ETL job, Cradle profile, Bedrock model, staging table, OTF variable.

## Why the BB Ontology Misses This: The "model" Type Is a System-Layer Aggregate

The FZ 7g ontology is built on Sascha's epistemic types: a "model" is "anything that shows relationships between entities". That definition is correct but **non-discriminating**. In practice, the vault classifies seven structurally distinct system layers as the same building block:

| Sub-kind of "model" | Example notes | What it actually represents |
|---|---|---|
| **area** | area_rnr, area_maa, area_hrq | Program / capability area (organizational layer) |
| **intent** | intent_ri_summary, intent_ql_summary | RMP ruleset configuration (decision layer) |
| **model** (proper) | model_rnr_bsm_bert, model_vista_vlm | Trained ML model (inference layer) |
| **variable / OTF datasheet** | variable catalog RI, OTF datasheet | Feature definition (feature layer) |
| **Cradle profile** | cradle_rnr_bsm_kinesis | Stream/batch compute spec (compute layer) |
| **ETL job** | etl_reversal_reclassification | Pipeline definition (data layer) |
| **table / data source** | table_d_customer_orders, data_source_mds | Persisted dataset (storage layer) |

These are seven **different epistemic objects** describing seven **different layers of the same production system**. A deep-dive question asks "trace this object across system layers", which mathematically requires moving between these sub-kinds. In FZ 7g's ontology, *all of those moves are invisible* — they all collapse into a single, unrepresented "model→model" non-edge.

## The Real Edge Is Architectural, Not Epistemic

The FZ 7g ontology describes the **epistemic lifecycle**: how raw observations mature into named concepts, structured models, predictions, tests, and counter-arguments. That is the lifecycle [FZ 7f](thought_slipbox_thinking_protocol.md) and the DKS protocol ([FZ 8c5c1a](../../projects/athelas_conv/athelas_conv_dialectic_knowledge_system.md)) operationalize.

But the deep-dive trail is not an epistemic move. Going from `intent_ri_summary` to `model_rnr_bsm_bert` is not naming, structuring, predicting, codifying, testing, or challenging. It is **architectural composition** — "what implements this", "what feeds this", "where does this run", "what does this read". These edges have a real, denotational meaning in the production system; they just have **no representation** in FZ 7g.

| Architectural edge | Sub-kind transition | Example |
|---|---|---|
| **Implements** | intent → model | intent_ri_summary calls model_return_mtl |
| **Routes To** | intent → ruleset / area | intent_flr_summary belongs to area_flr |
| **Computes** | model → variable | model_rnr_bsm_bert uses OTF variable X |
| **Runs On** | model → cradle | model_pfw_mtl deployed via cradle_pfw_mtl |
| **Sources From** | cradle → etl | cradle_rnr_bsm_kinesis reads etl_reversal_reclassification output |
| **Reads** | etl → table / data source | etl_reversal_reclassification consumes table_d_unified_concessions |

Every deep-dive trail is a path through this graph. None of these edges appear in the FZ 7g ontology, because FZ 7g answers the question "**how does knowledge mature?**" while the deep-dive answers "**how does the system compose?**". Both are real ontologies of the vault. FZ 7g represents only the first.

## Three Possible Responses

### Response A: Split the "model" BB into sub-types

Promote the 7 sub-kinds (area, intent, model_proper, variable, cradle, etl, table) to first-class building blocks. The deep-dive becomes a chain of cross-type edges. Pros: the existing ontology grammar (cross-type edges) handles it cleanly. Cons: the BB schema explodes from 8 to 14+ types; Sascha's elegance is lost; existing classification on 6,186 notes would need migration; the same problem will recur (table sub-kinds, variable sub-kinds, etc.).

### Response B: Add an Architectural Edge Family — same-type, sub-kind-aware

Keep the 8 BB types intact. Add a parallel set of **same-BB edges** parameterized by `note_second_category` (the existing sub-kind proxy from [FZ 10b1](thought_bb_content_vs_category_source.md)):

```
model[intent]   --Implements-->     model[model]
model[model]    --Computes-->       model[variable]
model[model]    --Runs On-->        model[cradle]
model[cradle]   --Sources From-->   model[etl]
model[etl]      --Reads-->          model[table]
```

The ontology grows from 10 epistemic edges to **10 epistemic + N architectural edges**. The two edge families are kept distinct: epistemic edges describe knowledge maturity (FZ 7g), architectural edges describe system composition (this counter). The diagram in FZ 7g gets a second overlay layer (architectural) without disturbing the original.

### Response C: Acknowledge two ontologies — Epistemic and Architectural

Concede that FZ 7g is **one of two ontologies** the vault implicitly uses. Build a sibling note "Architectural Composition Ontology" with its own diagram and edges. The reasoning protocol [FZ 7f1](thought_thinking_protocol_building_block_expansion.md) gets a second mode: epistemic reasoning (matures knowledge) vs architectural reasoning (traces system layers). Multi-hop retrieval ([FZ 5k2d](thought_two_axis_multi_hop_benchmark_synthesis.md)) already implicitly does this with its vertical/horizontal axes — Response C makes that explicit at the ontology layer, not just the benchmark layer.

## Recommendation: Response B (with Response C framing)

Response B is the lowest-cost, highest-fidelity answer:

1. **Preserves FZ 7g intact.** No re-classification of 6,186 notes. Sascha's 6+2 typology survives.
2. **Adds the missing edges where they belong** — at the ontology layer, not just the benchmark layer. FZ 5k2c keeps benchmarking honest, but the ontology that drives the agent's reasoning protocol is still incomplete without these edges.
3. **Uses an existing signal** — `note_second_category` is already populated and validated by [FZ 10b](thought_bb_category_directory_mapping.md). No new metadata required.
4. **Frame architecturally (Response C)** in the FZ 7g note itself: state explicitly that the directed graph there is the **epistemic** ontology, and that an **architectural** ontology layered over the same nodes is a separate, complementary structure.

## What This Means for the Vault

If Response B is adopted:

- **Reasoning protocol** ([FZ 7f1](thought_thinking_protocol_building_block_expansion.md)): adds an 8th phase or an alternate trace — "Compose" — that walks architectural edges when the user query is a deep-dive ("trace", "end to end", "how does X get computed").
- **Retrieval** ([FZ 5k2d](thought_two_axis_multi_hop_benchmark_synthesis.md)): the "horizontal" multi-hop axis becomes a **typed traversal**, not just same-BB free walk. Architectural edges become the gold edges for Domain Recall@K.
- **Capture skills**: model-typed captures (intent, cradle, etl, variable) get explicit "architectural neighbors" sections that record the Implements / Computes / Runs On / Sources From / Reads edges as link rows. The skills already capture these *implicitly* via Related Notes; making them ontology-typed turns implicit into queryable.
- **Vault health** ([FZ 7c](analysis_building_block_vault_health.md)): adds "architectural completeness" — does every model→cradle edge exist, does every cradle→etl edge exist? Gaps point to missing model deployment notes, missing Cradle profile docs, etc.

## Open Questions

| # | Open Question |
|---|---|
| **OQ-7g1-a** | Is there a closed set of architectural edges (4–6), or is each system layer pair its own edge type? |
| **OQ-7g1-b** | Should architectural edges be drawn between sub-kinds within other BBs too (e.g., procedure[onboarding] → procedure[OTF setup] for the q594 procedure-chain pattern), or are they unique to "model"? |
| **OQ-7g1-c** | Does the agent need to *know* it is doing an architectural traversal vs an epistemic one, or can both edge families be searched uniformly with the user query selecting the path? |

---

## Related Notes

### Folgezettel Trail
- **★ Trail outcome [FZ 7g1a1a1a1](thought_synthesis_three_invariance_regimes_one_vault.md)**: where the chain this counter opened concludes — the deep-dive problem this note diagnosed is *real* (Layer 2 retrieval owns it) but is *not* an ontology problem (Layer 1 is preserved intact).
- **Parent [FZ 7g](thought_building_block_ontology_relationships.md)**: the BB Ontology this note counters — its 10 cross-type edges miss every same-BB edge in the deep-dive pattern.
- **Child [FZ 7g1a](thought_two_layer_bb_ontology_epistemic_plus_architectural.md)**: **answer** to this counter — proposes a two-layer ontology with Layer A (epistemic, unchanged) + Layer B (6 architectural edges parameterized by sub-kind). The user's deep-dive trail becomes a typed path.
- **Sibling [FZ 7c](analysis_building_block_vault_health.md)**: the model BB is the largest single block (16% of notes); this counter explains why that block is internally heterogeneous.
- **Sibling [FZ 7f1](thought_thinking_protocol_building_block_expansion.md)**: the 7-phase edge-guided reasoning protocol — currently only walks epistemic edges.
- **Cousin [FZ 5k2c](counter_ontology_violations_in_real_multi_hop.md)**: same problem at the **benchmark-design** layer (proposes vertical/horizontal split); this note addresses it at the **ontology-design** layer (proposes architectural edges).
- **Cousin [FZ 10b](thought_bb_category_directory_mapping.md)**: identifies that "model" is the most polymorphic BB (no dominant attractor, 12 directories) and that `note_second_category` discriminates the sub-kinds — the proxy this counter uses for architectural edges.
- **Cousin [FZ 10b1](thought_bb_content_vs_category_source.md)**: BB and category are orthogonal — this note operationalizes the orthogonality at the edge layer.

### Evidence
- **[Real SlipBot Questions Validate Multi-Hop](thought_real_slipbot_questions_validate_multi_hop.md)** — 19 of 50 random SlipBot questions are multi-hop; same-BB dominates.
- **[SlipBot Question Hop Classification](../../archives/experiments/experiment_slipbot_question_hop_classification.md)** — full classification table with deep-dive trails (q207, q152, q163, q19, q427, q587).
- **[Empirical Trail Analysis](analysis_empirical_ontology_trails_in_vault.md)** — 38,563 emp_obs→model→concept trails in the link graph; same model→model dominance observed.

### Sub-kind Proxies (Architectural Layer Identifiers)
- **[Knowledge Building Blocks](../term_dictionary/term_knowledge_building_blocks.md)** — overview of the 8-type taxonomy.
- **[Knowledge Building Blocks: Model](../term_dictionary/term_knowledge_building_blocks_model.md)** — the type this counter argues is overloaded.

### Entry Points
- **[Entry: Argument Trail](../../0_entry_points/entry_abuse_slipbox_argument_trail.md)** — this note is FZ 7g1.

---

**Last Updated**: 2026-04-24
