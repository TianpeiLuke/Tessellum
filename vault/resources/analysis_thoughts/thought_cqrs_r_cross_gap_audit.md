---
tags:
  - resource
  - analysis
  - argument
  - cqrs
  - audit
  - rcross
  - gap_analysis
keywords:
  - R-Cross gap audit
  - R-P gap
  - R-D gap
  - CQRS rule enforcement
  - architectural lens audit
  - system boundary verification
topics:
  - System Architecture
  - CQRS
  - Audit
  - Tessellum Foundations
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "1a1b1"
folgezettel_parent: "1a1b"
---

# Gap Audit: Tessellum Through the R-Cross Lens

## Thesis

The three CQRS discipline rules introduced at [FZ 1a1b](thought_cqrs_r_cross_rules.md) — **R-P** (Schema ⊥ Runtime co-evolution), **R-D** (Descriptive purity), and **R-Cross** (System boundary) — give the architect a checklist. This note runs that checklist over Tessellum's current codebase (v0.0.36) and surfaces the gaps each rule reveals.

The system review at [FZ-sibling](thought_src_tessellum_system_review.md) checked the codebase against the *abstract* CQRS commitment ("one boundary, two disciplines, one substrate"). This audit checks it against the *concrete* three rules. Some gaps surface only through the rule-specific lens — the R-Cross lens sees boundary discipline; the R-P lens sees schema-runtime co-evolution; the R-D lens sees retrieval-internal layering. The same code passes one lens and fails another.

## Verdict per rule

| Rule | Status | Severity |
|------|--------|----------|
| **R-P** (Schema ⊥ Runtime co-evolve) | **Held by absence** — schema is closed at 8 BB types + 10 edges, but the runtime (DKS) that should co-evolve with it isn't shipped | Latent: no current violations, but no enforcement either |
| **R-D** (Descriptive purity) | **Partially satisfied** — candidate generation is content-aware (BM25 + dense); BB-as-pre-router was correctly rejected; but BB-aware re-rank (Stage 3-4) isn't built yet | Open work: half the rule is enforced, half is deferred |
| **R-Cross** (System boundary) | **Satisfied at the import-graph level; latent at runtime** — composer / retrieval / indexer don't cross-import, but no in-process P-to-D call exists either | Mixed: defensive half works; productive half not wired |

The codebase has **no active R-rule violation today**. What it has is **deferred or latent enforcement** of each rule's positive half — the rule says X is allowed (or required), and Tessellum hasn't built X yet.

## R-P — Schema ⊥ Runtime co-evolution

### What R-P requires

Schema and Runtime must co-evolve. Adding a BB type requires the DKS protocol to gain a phase that produces it; adding a DKS phase requires the ontology to gain the edge whose source/target produces what the phase consumes/emits.

### What's true today

- The BB enum is **closed at 8 types** in `format/building_blocks.py`. The `EPISTEMIC_EDGES` tuple is closed at 10 directed edges. Both are exported but neither has a public mutation path.
- The DKS runtime that would co-evolve with the schema is **not shipped**. [`thought_dks_design_synthesis`](thought_dks_design_synthesis.md) documents the 7-component pattern as the v0.2+ delta.
- **Therefore R-P is held by absence** — there's nothing for the schema to co-evolve *with*, so there's nothing to enforce against. The schema is stable; the runtime is empty; the co-evolution rule has a trivial pass.

### The R-P gap

| Aspect | Gap |
|--------|-----|
| **Co-evolution enforcement** | The rule can't be tested today because the runtime is absent. When DKS lands, the *first* test the R-P lens must produce is: "does adding DKS phase X without an edge for X violate R-P?" |
| **Sub-kind leakage prevention** | The validator currently doesn't have a rule that says "sub-kinds (e.g., `concept:process` vs `concept:thing`) belong in System D facets, not in `tags[1]`." Tessellum's tag convention does this *by convention* (tags[2..] are domain tags, not BB-sub-kinds) but the rule isn't validator-encoded |
| **BB ontology edge enforcement** | The 10 epistemic edges in `EPISTEMIC_EDGES` are declarative data; the validator doesn't check that, e.g., a `counter_argument` note actually links to an `argument` note it claims to attack. The graph relationship is data, not invariant |

### How to close the R-P gap

1. **Ship DKS runtime** — a `composer/dks.py` module wires the 7-component cycle. R-P then becomes testable: any new phase must declare its producing edge.
2. **Add a validator rule** — `TESS-004` (or similar): a `counter_argument` must link to an `argument` it attacks (the validator can check the `## See Also` / `## Related` section for the back-reference). Promotes the BB-edge relationship from declarative data to invariant.
3. **Document sub-kind banishment explicitly** — `term_format_spec.md`'s "Tag conventions" section should call out: BB sub-kinds belong in System D, never in `tags[1]`.

## R-D — Descriptive purity

### What R-D requires

Candidate generation is computational (dense + BM25). System P artifacts (BB types, FZ positions, link proximities) enter at re-rank (Stage 3) and context assembly (Stage 4), never at candidate generation (Stage 1).

### What's true today

- **Stage 1 (candidate gen)**: `retrieval/bm25.py` (lexical FTS5) + `retrieval/dense.py` (sentence-transformers + sqlite-vec) — content-aware, type-blind. ✓ R-D-clean.
- **Stage 2 (fusion)**: `retrieval/hybrid.py` does one-SQL RRF over BM25 + dense top-K — content-aware. ✓ R-D-clean.
- **Stage 3 (re-rank)**: **not implemented**. Hybrid returns the RRF-fused ranking directly; no BB-aware, FZ-aware, or link-aware re-rank stage exists.
- **Stage 4 (context assembly)**: **not implemented**. Hybrid returns hits; there is no BB-typed context-window assembler that uses Building Block roles to choose what gets included in the LLM prompt.
- `tessellum filter --bb <type>` is a **parallel surface**, not a re-rank step. It's a direct SQL `WHERE building_block = ?` on the `notes` table, bypassing retrieval entirely. Correctly placed — `filter` is the "I know the structural shape" surface, not the "I'm searching for content" surface.
- The historical refutation of *BB-aware pre-routing* (Strategy × BB heatmap is flat, [FZ 3](thought_retrieval_evolution.md) step 2) means BB types are correctly *not* used at Stage 1. ✓ R-D-clean.

### The R-D gap

| Aspect | Gap |
|--------|-----|
| **Stage 3 re-rank not built** | The retrieval pipeline goes Stage 1 (candidate gen) → Stage 2 (RRF fusion) → return. No BB-aware re-rank intervenes. System P typing is therefore *visible but unused* at the read path |
| **Stage 4 context assembly not built** | When the COE skill (or any future skill) wants context for an LLM call, it has no BB-typed assembler — it gets a flat list of hits. The "BB types as evaluation framework, not router" insight from FZ 5g (in the source vault) is documented but not operationalised |
| **No epistemic-congruence metric** | Per the AB note, the right place for BB typing inside System D is *evaluation* (epistemic congruence). Tessellum's eval framework ([`thought_dks_design_synthesis`](thought_dks_design_synthesis.md) Wave 5b) shipped with the LLMJudge 5-dim rubric (relevance / completeness / accuracy / clarity / structural integrity), but **none of the five dimensions explicitly score BB-type epistemic congruence** — does the retrieved set match the BB types the question implies it should? That dimension is missing |

### How to close the R-D gap

1. **Add Stage 3 re-rank module** — `retrieval/rerank.py` taking the hybrid top-K and re-ordering by BB-aware features (does the question imply an `empirical_observation` answer? Boost observations. Does it imply a `procedure`? Boost procedures).
2. **Add Stage 4 context assembler** — `retrieval/context_assembler.py` that takes top-K and assembles a BB-typed context window: include the seed term, the procedures it supports, the arguments it grounds, etc. Token-budgeted, BB-shape-aware.
3. **Add a 6th LLMJudge dimension** — `epistemic_congruence` — to the eval rubric: did retrieval surface notes whose BB types match the question's epistemic shape?

These three pieces together would close the R-D gap and put BB typing into the descriptive layer where it earns its keep — *evaluation* and *assembly*, not routing.

## R-Cross — System boundary

### What R-Cross requires

System P writes; System D reads. System P **may call** System D (to check whether knowledge already exists before authoring). System D **does NOT call** System P. The query path never crosses into System P.

### What's true today

- **Defensive half (D ↛ P)**: ✓ rigorously held. The import-graph check in [`thought_src_tessellum_system_review`](thought_src_tessellum_system_review.md) verified `retrieval/` and `indexer/` have **zero** imports from `composer/`. The query path cannot invoke a P-side component because there's no Python-level coupling.
- **Productive half (P → D)**: **latent**. The composer doesn't import retrieval either. Skill canonicals (e.g., `skill_tessellum_write_coe.md` step 4) say "use `tessellum search --bm25` for cross-references," but that's a *narrative instruction to the agent*, not a runtime invocation. When the agent executes step 4, it's running shell commands (or the agent's own tool-use), not a tessellum-internal call from composer → retrieval.
- **Substrate-only meeting point**: ✓ held. `vault/` is the only thing both systems touch directly. Run traces live in `runs/composer/`, outside both.

### The R-Cross gap

| Aspect | Gap |
|--------|-----|
| **No in-process P → D call** | The COE skill *narratively* uses `tessellum search`, but the composer pipeline has no executor-side `retrieval.hybrid_search()` invocation. If a skill genuinely needs deduplication-aware authoring, the executor would need a P-side handle into D's read API |
| **No formalised "P calls D" surface** | R-Cross says *P MAY call D*. If Tessellum wants to honour that affirmation, the composer executor should ship a thin retrieval-client (`retrieval/client.py` or composer-side reference) that satisfies the "P calls D for read-only context" pattern without violating the import-graph cleanliness |
| **Substrate-mediated calls left implicit** | The agent reads the substrate (notes, including the index) on its own via shell commands. This works but the *protocol* of "P calls D" lives only in skill prose. A reader of just the code can't tell which skills depend on cross-system reads vs. which are pure P-side |

### How to close the R-Cross gap

1. **Add a P-side retrieval client** — a thin module in `composer/` that allows a step's prompt to be augmented with a retrieval-result block before the LLM call. The client *reads* the index (System D's output) and emits typed `RetrievalContext` data. This is the formal "P calls D" pattern.
2. **Add an `mcp_dependencies`-like declaration for retrieval** — `retrieval_dependencies: [{strategy: hybrid, query_template: ...}]` in a step's sidecar. The compiler can then validate the retrieval shape and emit a typed contract.
3. **Document in `term_cqrs`** — that "P calls D" is implemented at the executor layer; "D does not call P" is implemented at the import-graph layer. Both halves of R-Cross have a *named home*.

These would lift R-Cross from "defensively true, productively latent" to "actively enforced in both directions."

## Cross-cutting summary

| Rule | Defensive half | Productive half |
|------|----------------|-----------------|
| **R-P** | Schema is closed at 8 types ✓ | Runtime co-evolves with schema ✗ (DKS not shipped) |
| **R-D** | Candidate gen is type-blind ✓ | BB types enter at Stages 3-4 ✗ (re-rank not shipped) |
| **R-Cross** | D doesn't call P ✓ | P calls D ✗ (no executor-side retrieval client) |

A pattern emerges: **Tessellum's R-rules each have a "defensive" half (what's forbidden) that is rigorously held, and a "productive" half (what's enabled or expected) that is deferred to v0.2+ work.** The defensive halves are sufficient for the codebase to be *consistent with* the CQRS commitment; the productive halves are required for the codebase to *fully realise* it.

This is not a hidden gap — it's the architectural acknowledgment that v0.1 ships the *boundary* and v0.2+ ships the *use* of the boundary.

## Priority order for closing the gaps

If the next development phase were to close R-rule gaps, the load-bearing order is:

| # | Gap to close | Rule | Why this order |
|---|--------------|------|---------------|
| 1 | DKS runtime (composer/dks.py + 7-component dispatcher) | R-P | Without runtime co-evolution there's nothing for R-P to police. This is the foundation |
| 2 | P-side retrieval client (composer-internal handle into hybrid_search) | R-Cross | Lets skills do deduplication-aware authoring without violating the import graph |
| 3 | Stage 3 BB-aware re-rank (retrieval/rerank.py) | R-D | Puts BB typing into System D where it earns its keep (re-rank, not routing) |
| 4 | Stage 4 BB-typed context assembler (retrieval/context_assembler.py) | R-D | Lets the executor produce BB-shape-aware LLM context |
| 5 | Epistemic congruence eval dimension | R-D | Closes the loop — eval now measures whether retrieval honours BB-type expectations |
| 6 | TESS-004 validator rule (counter_argument must link to argument) | R-P | Promotes BB-edge relationship from data to invariant |

Items 1-2 are foundational (without them, items 3-5 have nowhere to live). Items 3-5 close the R-D productive half. Item 6 sharpens R-P. The full enforcement of the three rules requires all six.

## Verdict

Tessellum **holds the negative half of each R-rule** (what's forbidden never happens) and **defers the positive half** (what's enabled isn't wired yet). The codebase is *consistent with* CQRS today but doesn't *fully exercise* it. Closing the productive halves is the v0.2+ work that turns the architectural commitment into operational behaviour.

The three rules give the architect a concrete checklist for that future work. Every step in the priority order above can be evaluated by asking which rule's productive half it advances — and any proposed *alternative* step can be challenged by asking which rule's defensive half it undermines.

## Related Notes

- [`thought_cqrs_r_cross_rules`](thought_cqrs_r_cross_rules.md) — FZ 1a1b — the three rules this audit applies
- [`thought_src_tessellum_system_review`](thought_src_tessellum_system_review.md) — sibling-of-trail; the codebase audit through the abstract CQRS lens
- [`thought_synthesis_two_systems_cqrs_value_proposition`](thought_synthesis_two_systems_cqrs_value_proposition.md) — FZ 1a1 — the synthesis the rules formalize
- [`thought_cqrs_essence_for_tessellum`](thought_cqrs_essence_for_tessellum.md) — FZ 1a1a — the user-facing essence; sibling of 1a1b
- [`thought_dks_design_synthesis`](thought_dks_design_synthesis.md) — FZ 2a — DKS runtime; R-P's productive half
- [`thought_retrieval_synthesis`](thought_retrieval_synthesis.md) — FZ 3a — System D's design; R-D's enforcement target
- [`term_cqrs`](../term_dictionary/term_cqrs.md) — canonical term
- [`term_dialectic_knowledge_system`](../term_dictionary/term_dialectic_knowledge_system.md) — DKS as System P runtime

## Status After Phase 5 (v0.0.45) — Cross-Validation

DKS Phase 5 shipped on 2026-05-10. Re-running the checklist above:

| Rule | Defensive half (pre-Phase-4) | Productive half (post-Phase-5) | Status |
|------|------------------------------|--------------------------------|--------|
| **R-P** (Schema ⊥ Runtime co-evolve) | Closed BB + edge schema; no runtime violating it | DKS runtime exercises every BB-to-BB edge end-to-end (Phase 1-3); TESS-004 + format validator enforce edge presence statically (Phase 4); WarrantRegistry + WarrantHistory + DKSConfidenceModel let the runtime mutate the warrant set with auditable persistence (Phase 5) | **Held — both halves** |
| **R-D** (Descriptive purity) | Candidate generation is content-aware; BB-as-pre-router stays rejected | DKS does not write to the index; D-side stays BB-agnostic at Stage 1-2 by construction; the optional BB-aware re-rank at Stage 3-4 remains a deferred enhancement (separate work) | **Defensive half held**; productive half partial (not a DKS-phase deliverable) |
| **R-Cross** (System boundary) | DKS imports no mutating retrieval code; retrieval exposes no mutating API | `tessellum.dks.RetrievalClient` (Phase 4) is the typed, read-only P-side adapter over `hybrid_search`; DKS step 1 + step 6 use it; the `--report` CLI mode (Phase 5) reads through it for inter-cycle telemetry | **Held — both halves** |

**R-P** moves from "held by absence" to "actively enforced": the runtime exists, runs, and writes typed notes that the validator can structurally check. The 8-BB / 10-edge schema is now tested against by every DKS cycle that fires — schema-runtime co-evolution is observable in the corpus, not just promised by the architecture.

**R-Cross** moves from "satisfied at the import-graph level" to "satisfied with a typed runtime contract". The dependency DAG was always one-directional; what was missing was the P-side client that proved P actually *does* read D, formally and without bypass. `RetrievalClient` is that proof; its `db_path` + `search` public surface is the entire contract.

**R-D**'s productive-half gap (BB-aware re-rank at Stage 3-4) was named in the original audit as "open work; half the rule is enforced, half is deferred". Phase 5 did not close it — it isn't a DKS deliverable. The work belongs to a future retrieval-side phase (likely v0.2+ Retrieval Phase 2). Recording this here so the next audit cycle starts from the right baseline.

### What changed materially in v0.0.45 vs v0.0.36

- The R-P productive half required a runtime to enforce it; DKS Phase 1-5 ships that runtime end-to-end.
- The R-Cross productive half required a typed read client; Phase 4's `RetrievalClient` ships it.
- The "no active violation today" claim still holds (it was true at v0.0.36 too); the difference is that the *enforcement mechanism* is now load-bearing in the operational sense, not just a documentation claim.

### What this means for the next audit

The next R-rule audit (planned for after the first non-DKS application of the runtime, likely v0.2+) should focus on:

1. Whether DKS-emitted warrants stay typed correctly under sustained load (TESS-004 + `epistemic_congruence` rubric will surface the answer)
2. Whether R-D's BB-aware re-rank introduces back-door coupling — the dial-down to Stage 1-2 candidate generation must remain BB-agnostic
3. Whether new runtimes built on the same pattern (e.g. a code-review loop atop Composer + Retrieval + Format) reuse the R-Cross client discipline rather than reinventing it

## See Also

- [`entry_architecture_trail`](../../0_entry_points/entry_architecture_trail.md) — per-trail entry point; this node is FZ 1a1b1
- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail map
- [`thought_dks_runtime_integration`](thought_dks_runtime_integration.md) — FZ 2b — Phase 4+5's runtime integration synthesis; the closing leaf of Trail 2

---

**Last Updated**: 2026-05-10 (Phase 5 cross-validation amendment)
**Status**: Active — FZ 1a1b1, Architecture trail (leaf of the R-Cross branch); productive halves of R-P and R-Cross now closed by DKS Phases 1-5
