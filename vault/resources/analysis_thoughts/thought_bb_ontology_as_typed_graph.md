---
tags:
  - resource
  - analysis
  - argument
  - ontology
  - building_blocks
  - graph_theory
  - schema
keywords:
  - BB ontology graph
  - typed graph
  - schema vs corpus
  - BB schema
  - epistemic edges
  - graph properties
  - finite state schema
  - DKS substrate
topics:
  - Building Block Ontology
  - Graph Theory
  - System Architecture
  - Tessellum Foundations
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "1b"
folgezettel_parent: "1"
---

# BB Ontology as a Typed Graph: Schema, Corpus, and the Finite-State Substrate of DKS (FZ 1b)

## Thesis

[FZ 1: `thought_building_block_ontology_relationships`](thought_building_block_ontology_relationships.md) defined the BB ontology as **8 types + 10 directed relationships** — answering the static "what type is this and what does it connect to?" question. This note sharpens that definition: the ontology is not just a *taxonomy with arrows*; it is a **typed directed graph with two layers** — a **schema graph** (finite, closed at 8 nodes + 10 edges, lives in code) and a **corpus graph** (open, growing per cycle, lives in the vault as notes + links). The schema is the *finite state machine* that constrains valid transitions; the corpus is the *trace* the runtime leaves walking that FSM.

This two-layer reading is what makes [DKS](thought_dks_evolution.md) (FZ 2) *implementable* as a graph walker rather than as seven hand-coded steps. The 7 DKS components are seven edges of the schema graph; one DKS cycle is one walk through them, depositing N nodes + M edges into the corpus.

## The two graphs

The BB ontology is two graphs at the same time, related by instance-of:

| Layer | What it contains | Cardinality | Where it lives |
|-------|------------------|--------------|----------------|
| **Schema graph** (closed, finite) | The 8 BB types (nodes) + 10 epistemic relationships (edges) | Fixed at 8 + 10 by spec | `tessellum.format.frontmatter_spec` (VALID_BUILDING_BLOCKS); FZ 1 mermaid |
| **Corpus graph** (open, growing) | Concrete BB-typed notes (instances of nodes) + body-link / FZ-parent edges (instances of relations) | Monotonically growing; one new node per BB-typed note written | `vault/**/*.md`; the `notes` + `note_links` tables in the unified index |

Every corpus node is an *instance-of* exactly one schema node (its `building_block:` value). Every corpus edge — whether a body link or a `folgezettel_parent` reference — is either an instance of a schema edge (when the source and target BB types match a row in the 10-edge table) or a stray reference (links the validator can flag).

Schema-level statements are about *what's allowed* (`counter_argument → argument` is a valid edge type). Corpus-level statements are about *what actually exists* (`counter_my_thing.md` body-links to `argument_their_thing.md`). The interplay is where the format validator + TESS-004 rule (Phase 4) earn their keep — they enforce that corpus instances honour schema types.

## Schema graph — the FSM

Drawing the schema explicitly as a state-machine view rather than the topological cycle view in FZ 1:

```
         (schema graph — 8 nodes, 10 edges; cycle is closed via CTR → OBS)

         ┌─────────────────────────────────────────────────────────────────┐
         ▼                                                                 │
    ┌────────────┐    [naming]    ┌────────┐  [structuring]  ┌─────────┐   │
 ┌─►│ empirical_ │ ───────────► │concept │ ─────────────► │  model  │   │
 │  │observation │              │        │                │         │   │
 │  └────────────┘              └────────┘                └────┬────┘   │
 │        ▲                                                 [pred]│      │
 │        │                                                       ▼      │
 │   [execution data]                          ┌──────────────────────┐  │
 │        │                                    │     hypothesis       │  │
 │  ┌────────────┐  [codifying]                └─────────┬────────────┘  │
 │  │ procedure  │ ◄─────────── (model)                  │ [testing]     │
 │  └────────────┘                                       ▼               │
 │                                                  ┌──────────┐         │
 │                                                  │ argument │         │
 │                                                  └──────┬───┘         │
 │                                                         │ [challenging]
 │                                                         ▼            │
 │                                            ┌──────────────────┐     │
 └────[motivates new observations]── counter_ │ counter_argument │     │
                                              └──────────────────┘     │
                                                                       │
                                              navigation ─[indexes]──► (all 7 others)
                                                                       │
                                          (cycle closure via CTR → OBS)┘
```

(The mermaid in FZ 1 has the same topology; the textual rendering here emphasises the cycle.)

### Schema-graph properties

The schema graph has properties that the corpus inherits:

1. **It contains a cycle.** OBS → CON → MOD → HYP → ARG → CTR → OBS is the load-bearing dialectic loop. The graph is **not** a DAG; the cycle is what makes DKS's "closed loop" geometrically possible.
2. **One source-like node and one sink-like node?** No — every type is both producible and consumable. Even `empirical_observation` (often called "the source") is the *target* of `counter_argument → motivates new` and `procedure → execution data`. Even `procedure` (often called "the sink"; the action output) is the *source* of execution-data observations.
3. **One designated meta-node.** `navigation` is the only BB type that fans out to all others without participating in the cycle. It is the *routing* layer, orthogonal to the *epistemic* layer.
4. **One short-circuit edge.** `model → procedure` (codifying) is the path from theory to action — short-circuiting the hypothesis/argument/counter pipeline. The cycle has *two* feedback edges into OBS: one through CTR (the dialectic) and one through PRO (the operational loop).
5. **Edges are labelled, not just typed.** Each edge has a semantic verb (naming, structuring, predicting, codifying, testing, challenging, motivates-new, execution-data, indexes). The label is part of the edge type; the same pair `(MOD, HYP)` could in principle carry multiple labels (today it carries one: predicting).

These are *finite* properties — they don't grow with the corpus. Adding more notes doesn't add edges to the *schema*; it adds *instances* of existing edge types. The schema-vs-corpus split is what makes "DKS is an FSM" defensible.

## Corpus graph — the running tape

Every DKS cycle (and every hand-authored note) is a write to the corpus graph. Concretely, each closed-loop cycle deposits:

| Cycle step | New corpus node | New corpus edges |
|-----------:|------------------|-------------------|
| 1 (observation) | 1 × `empirical_observation` | (root — no parent) |
| 2 (argument A) | 1 × `argument` | OBS → ARG (schema edge: testing, via implicit hypothesis-collapse) + `folgezettel_parent` link |
| 3 (argument B) | 1 × `argument` | same as 2 |
| 4 (contradicts) | (no new node) | 1 × `contradicts` edge between A and B |
| 5 (counter) | 1 × `counter_argument` | ARG → CTR (challenging) + `folgezettel_parent` link |
| 6 (pattern) | 1 × `model` | CTR → MOD (**new schema edge proposed — see below**) |
| 7 (revision) | 1 × `procedure` or `concept` | MOD → PRO (codifying) OR MOD → CON (reverse of naming) + `folgezettel_parent` link |

That's 6 new corpus nodes + 5 corpus edges per closed cycle (or 3 nodes + 2 edges in the gated path; 3 nodes + 2 edges + 1 contradicts in the short-circuit-on-agreement path).

### A schema-graph gap DKS exposes

Note step 6's row: **CTR → MOD** is not in FZ 1's original 10 edges. The 10 edges have CTR → OBS (motivates new), but no edge for *"a counter-argument plus its siblings aggregate into a model of the failure pattern"*. The pattern-discovery step requires that edge.

This is R-P's productive half at work: the runtime exposes a missing schema edge. Two responses are available:

- **Add a new schema edge** `counter_argument → model` with a label like "aggregating" or "pattern-of-failure". Brings the total to 11.
- **Decline to add it** — assert that DKS's pattern-discovery is a procedural operation, not a typed substrate edge. Then the pattern note's `folgezettel_parent` is a *plumbing* link, not an epistemic edge.

Tessellum currently does the second (no `counter_argument → model` row in the spec); but the first is the cleaner reading if we take R-P seriously: schemas should mutate to match what the runtime needs. Recording the choice here so a future amendment can revisit.

## Data structure (what the implementation should look like)

The current implementation (`tessellum.dks.core`) has *per-component dataclasses* (`DKSObservation`, `DKSArgument`, ...). That's a reasonable surface, but it scatters the BB-graph structure across seven types. A graph-first refactor would lift the schema explicitly:

```python
# Schema layer (closed, finite, lives in tessellum.format / tessellum.bb)

class BBType(StrEnum):                           # 8 values
    EMPIRICAL_OBSERVATION = "empirical_observation"
    CONCEPT               = "concept"
    MODEL                 = "model"
    HYPOTHESIS            = "hypothesis"
    ARGUMENT              = "argument"
    COUNTER_ARGUMENT      = "counter_argument"
    PROCEDURE             = "procedure"
    NAVIGATION            = "navigation"

@dataclass(frozen=True)
class EpistemicEdgeType:                          # one of the 10 schema edges
    source: BBType
    target: BBType
    label: str                                    # "naming" | "structuring" | ...

BB_SCHEMA: tuple[EpistemicEdgeType, ...] = (
    EpistemicEdgeType(BBType.EMPIRICAL_OBSERVATION, BBType.CONCEPT, "naming"),
    EpistemicEdgeType(BBType.CONCEPT, BBType.MODEL, "structuring"),
    ...
)

# Corpus layer (open, growing; views over the unified index)

@dataclass(frozen=True)
class BBNode:                                     # one note in the vault
    note_id: str                                  # vault-relative path
    bb_type: BBType
    folgezettel: str | None
    folgezettel_parent: str | None
    # ... whatever fields the BB type requires

@dataclass(frozen=True)
class BBEdge:                                     # one realised relation
    source_id: str
    target_id: str
    edge_type: EpistemicEdgeType                  # which schema edge does it instantiate?
    provenance: str                               # "body_link" | "folgezettel_parent" | "contradicts"

# BBGraph = (set of BBNodes, set of BBEdges) — the union of schema + corpus
```

With this in place, the per-component DKS dataclasses become **views** over `BBNode`:

```python
DKSObservation       = BBNode[bb_type=EMPIRICAL_OBSERVATION]
DKSArgument          = BBNode[bb_type=ARGUMENT, plus structured warrant fields]
DKSCounterArgument   = BBNode[bb_type=COUNTER_ARGUMENT, plus broken_component]
DKSPattern           = BBNode[bb_type=MODEL]
DKSRuleRevision      = BBNode[bb_type ∈ {PROCEDURE, CONCEPT}]
```

The 7 DKS steps then become explicit FSM transitions:

```python
def dks_step_to_edge(step: int) -> EpistemicEdgeType: ...   # 1→OBS-root, 2→testing, ..., 7→codifying
```

This refactor is *not* required for v0.0.45's runtime to work — the per-component dataclasses are fine as a surface. The graph-first refactor's value is downstream: it makes meta-DKS (the runtime that watches DKS and proposes schema additions) *cheap* — meta-DKS just walks the corpus graph counting unused schema edges and over-used ones.

## Three implications

1. **The schema is finite.** 8 nodes + 10 edges. Closing the schema at this cardinality means the corpus's type system is *checkable* — you can write a validator that says "this corpus edge is allowed" by looking at the source's `building_block:`, the target's `building_block:`, and asking whether `(source_bb, target_bb)` is in the schema. TESS-004 (Phase 4) does exactly this for one edge type (`counter_argument → argument`).
2. **The schema is mutable** — but mutable slowly, by a different runtime than the cycle. The DKS *cycle* (intra-record loop) writes corpus instances; it does not add new BB types or edge types. A future meta-DKS (inter-cycle, weekly) watches the cycle and proposes schema edits when the existing schema repeatedly fails to type-check the runtime's outputs. R-P's productive half is precisely "the schema co-evolves with the runtime that exercises it." Today we exercise R-P defensively (the schema is closed; the runtime conforms); the productive half lands when meta-DKS proposes its first edit.
3. **The corpus's growth pattern is the system's "behaviour."** Counting corpus nodes by BB type and corpus edges by schema-edge-type is what `tessellum dks --report` (Phase 5) does at the cycle level. Extending it to the *full* corpus, not just `runs/dks/`, is the obvious v0.2 telemetry surface. A vault with 200 arguments and 5 counter-arguments has a *different* behavioural signature from one with 200 arguments and 100 counter-arguments — and the difference is observable from the graph alone.

## What changes in DKS once this lens is adopted

FZ 2a says "each DKS component corresponds to one BB-to-BB epistemic edge". This note sharpens that claim by exposing the graph the components walk:

| FZ 2a's claim | This note's sharpening |
|---|---|
| The 7 components are 7 BB edges | The 7 components are 7 transitions in a *finite-state machine* whose states are the 8 BB types and whose transition relation is exactly the 10-edge schema |
| DKS forms a cycle in the BB graph | DKS *walks* a cycle; one cycle = one walk = one set of corpus additions |
| Add/remove a component → add/remove a BB edge | Add/remove a component → add/remove a *transition function entry* in the FSM |

[FZ 2a2: `thought_dks_as_fsm_on_bb_graph`](thought_dks_as_fsm_on_bb_graph.md) extends this further — formalising DKS as a finite-state machine, separating the FSM-as-mechanism from the corpus-as-tape, and laying out the three learning levels (instance / edge-weight / schema) that the graph-theoretic lens makes visible.

## Related Notes

- **Parent**: [FZ 1: `thought_building_block_ontology_relationships`](thought_building_block_ontology_relationships.md) — the original taxonomy + 10-edge ontology
- **Sibling**: [FZ 1a: `thought_cqrs_design_evolution`](thought_cqrs_design_evolution.md) — Trail 1's CQRS branch (uses the same schema but applies it to read/write separation)
- **Child (proposed)**: [FZ 2a2: `thought_dks_as_fsm_on_bb_graph`](thought_dks_as_fsm_on_bb_graph.md) — DKS formalised as an FSM walker on this graph
- **Cross-trail**: [FZ 2a: `thought_dks_design_synthesis`](thought_dks_design_synthesis.md) — the 7-component pattern that this note's graph foundation underpins
- **R-Cross relation**: [FZ 1a1b: `thought_cqrs_r_cross_rules`](thought_cqrs_r_cross_rules.md) — R-P (Schema ⊥ Runtime) is the rule the schema-vs-corpus split formalises

## Related Terms

- [`term_building_block`](../term_dictionary/term_building_block.md) — the 8 BB types this note's schema enumerates
- [`term_epistemic_function`](../term_dictionary/term_epistemic_function.md) — the function each BB performs
- [`term_dialectic_knowledge_system`](../term_dictionary/term_dialectic_knowledge_system.md) — the runtime that walks this graph

## See Also

- [`entry_architecture_trail`](../../0_entry_points/entry_architecture_trail.md) — Trail 1 per-trail entry point (this note is FZ 1b)
- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail map

---

**Last Updated**: 2026-05-10
**Status**: Active — FZ 1b, Architecture trail (second branch from the BB ontology root; sibling to the CQRS chain at 1a)
