---
tags:
  - resource
  - analysis
  - argument
  - dks
  - meta_dks
  - validation
  - empirical
keywords:
  - meta-DKS validation
  - v0.0.53 dogfood
  - Toulmin failure distribution
  - warrant dominance
  - heuristic proposer evidence
  - schema_events.jsonl artifact
  - LLM proposer prompt design
topics:
  - Dialectic Knowledge System
  - Meta-DKS
  - Empirical Validation
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "2c1a"
folgezettel_parent: "2c1"
---

# Meta-DKS Validation Evidence — v0.0.53 Dogfood Run (FZ 2c1a)

## Thesis

[FZ 2c1](thought_meta_dks_design.md) (the meta-DKS design synthesis shipped at v0.0.52) committed to a heuristic-based proposer for the schema-mutation runtime: when one Toulmin component exceeds 50% of counter-argument firings, propose the corresponding typed edge from a 3-entry lookup table. The design note asserted this is *mechanism, not deployable production runtime* — the LLM-driven proposer is deferred to Phase B.

Phase V of [`plan_meta_dks_validation_and_polish`](../../../plans/plan_meta_dks_validation_and_polish.md) validates that mechanism against real telemetry rather than synthesised test fixtures. This note documents the dogfood run: 25 observations sourced from the Tessellum vault's own open-questions sections were fed to `tessellum dks --backend anthropic`, the cycle traces were then fed to `tessellum dks --meta --apply`, and one schema edit landed.

**Two findings shape Phase B's prompt design**:

1. **The heuristic fires correctly on the dominant signal.** Of 25 cycles, 23 produced `warrant` counters and 2 produced `undercutting` counters. Meta-DKS's Toulmin-dominance heuristic fired exactly once: `add model → procedure (warrant_codification)`, motivated by 92% warrant rate. The proposal is well-formed, the migration note was authored, the event landed in `schema_events.jsonl`. The end-to-end mechanism works.
2. **The Toulmin distribution is not representative — and the heuristic has no way to know that.** Zero cycles produced `premise` or `counter-example` counters. The observation set was framed as unsettled methodological/architectural claims, which structurally invite warrant attacks (questioning inferential rules) rather than premise attacks (questioning data adequacy) or counter-example attacks (citing breaking cases). The v0.0.52 heuristic accepts this lopsided distribution at face value; the Phase B LLM-driven proposer needs a representativeness check.

The narrative below sequences the run's evidence, isolates what the heuristic *would have missed* even if more cycles had run, and crystallises the recommendations into a Phase B prompt-design specification.

## The 25-observation set

Sourced deterministically by [`scripts/curate_validation_observations.py`](../../../scripts/curate_validation_observations.py) from open-questions sections in `vault/resources/analysis_thoughts/`. Balance: 8 Trail 1 (Architecture) + 9 Trail 2 (Dialectic) + 8 Trail 3 (Retrieval). Each entry phrased as an empirical claim or open situation, not as a question — the input shape DKS step 1 expects.

The full set lives at `runs/dks/validation_v0_0_53/observations.jsonl`. The curation script is reproducible: re-running it always produces the same JSONL. Examples:

| FZ source | Summary fragment | Predicted Toulmin failure |
|-----------|------------------|---------------------------|
| FZ-1 | "BB ontology defines 10 directed epistemic edges, but empirical evidence shows ~46% same-BB transitions..." | counter-example |
| FZ-2 | "DKS was derived from Dung+Toulmin+IBIS but introduces one novel mechanism... whether the closed loop is load-bearing is empirically untested" | warrant |
| FZ-2c1 | "Meta-DKS's cold-start guard (20 cycles) is unvalidated... whether the threshold should scale with vault size is unresolved" | premise |
| FZ-3 | "Hybrid RRF +12pp Hit@5 lift... but Hit@K-to-answer-quality ρ=0.37, may be benchmark theater" | warrant |
| FZ-5j | "Hub dilution predicts BFS underperforms content-based retrieval in scale-free KGs with α<2.0... empirical validation across 3+ KGs not conducted" | premise |

**Prediction** (from curation): mix of warrant, counter-example, and premise failures. **Reality**: 23 warrant + 2 undercutting + 0 premise + 0 counter-example. Discrepancy analysed in §"Blind spots discovered" below.

## Cycle run telemetry

`tessellum dks runs/dks/validation_v0_0_53/observations.jsonl --backend anthropic --runs-dir runs/dks/validation_v0_0_53/ --format json`

| Metric | Value |
|--------|------:|
| Cycles attempted | 25 |
| Cycles completed | 25 |
| Mean elapsed per cycle | 63s |
| Total wall-clock | 26 min |
| Closed-loop terminations | 25 / 25 |
| Confidence-gated short-circuits | 0 / 25 |
| Patterns produced | 25 / 25 |
| Rule revisions produced | 25 / 25 |
| Warrant changes — added | 25 |
| Warrant changes — revised | 0 |
| Warrant changes — superseded | 0 |
| Mean Folgezettel nodes per cycle | 6.0 (root + arg-A + arg-B + counter + pattern + revision) |

Every cycle ran the full 7-component path. The gate (Phase 5's `ConstantConfidence`) never short-circuited, consistent with the observation set being framed as substantive open questions where neither A nor B argument could be trivially produced. All 25 cycles used `mode: fresh`, so no warrant threading occurred — each cycle deposited a fresh warrant rather than revising a prior one.

## The Toulmin distribution — 92% warrant

The headline finding:

| Broken component | Count | Share |
|------------------|------:|------:|
| **warrant** | 23 | 92% |
| **undercutting** | 2 | 8% |
| **premise** | 0 | 0% |
| **counter-example** | 0 | 0% |

All 25 counter-arguments fired at `strength: strong`; no variation across the distribution.

The 50% dominance threshold for the v0.0.52 heuristic is crossed by a wide margin. The lookup table's mapping `warrant → MODEL→PROCEDURE warrant_codification` fired exactly once (heuristic dedups per cycle batch), producing the schema-edit proposal documented below.

### Substantive content of the "warrant" counters

The 92% warrant rate is structurally meaningful — the counter-arguments are genuinely attacking *inferential rules*, not data adequacy or specific instances. Three samples:

**Cycle 1 (FZ-1 — BB ontology completeness)**:
- Counter-claim: *"The distinction between prescriptive ontological validity and descriptive usage frequency collapses when the ontology is designed specifically to model epistemic structure."*
- Reason: *"The attacked warrant assumes a clean separation between prescriptive schema validity and empirical usage data, treating them as belonging to different logical registers..."*

**Cycle 9 (FZ-2 — DKS closed-loop novelty)**:
- Counter-claim: *"The closed feedback loop in DKS may be load-bearing for the learning claim only if warrant revision constitutes a stable trajectory..."*
- Reason: *"The attacked argument's warrant asserts that any foundational posit must be explicitly named, pragmatically justified, and held open to revision to be epistemically legitimate. But this very criterion..."*

**Cycle 17 (FZ-2c1 — meta-DKS retract evidence bar)**:
- Counter-claim: *"The absence of evidence that the 50-cycle bar causes harmful retention of false edges is not epistemically neutral..."*
- Reason: *"The warrant conflates two distinct epistemic situations: (1) absence of evidence where a fair evidential process has been operating, and (2) absence of evidence where the policy's own structure systematically..."*

All three explicitly attack the *bridge from data to claim* — the canonical Toulmin warrant role. The classifier is doing its job; the heuristic's interpretation of "warrant dominance ⇒ schema gap around warrant codification" is defensible from this evidence.

### The 2 "undercutting" cases

Cycles 15 (FZ-2c — three-stage adaptation pipeline) and 16 (FZ-2c — Layer A/B separation) produced `undercutting` counters. The distinction from warrant is meaningful: an undercutter does not deny the warrant's internal logic but removes the *ground on which the warrant can be applied*. Sample:

**Cycle 16**: *"The attacker's claim that boundary negotiation must be housed at a third, explicitly meta-architectural level does not refute the warrant's conditions but instead defeats the applicability..."*

The v0.0.52 heuristic's lookup table has **no mapping for `undercutting`** — these cases produce zero proposals even when they dominate. At 8% of the run, this didn't matter. If a future observation set produced (say) 60% undercutting, the heuristic would emit zero proposals despite the clear schema-class signal.

## The meta-DKS proposal — one edit landed

`tessellum dks --meta --runs-dir runs/dks/validation_v0_0_53/ --apply` produced:

```
dks --meta  (25 cycles examined; APPLIED)
  1 proposals, 1 surviving:
          add  model -> procedure  (warrant_codification)
               Toulmin failure mode 'warrant' dominates the counter-argument
               distribution (23/25 = 92.0%). Propose adding the related typed
               edge so the schema can declare the missing relationship.
  events appended to: runs/dks/validation_v0_0_53/meta/schema_events.jsonl
  migration note:     runs/dks/validation_v0_0_53/meta/migration_<ts>.md
```

The event in `schema_events.jsonl`:

```json
{"timestamp": "2026-05-11T06:20:54+00:00", "kind": "added",
 "edge": {"source": "model", "target": "procedure",
          "label": "warrant_codification"},
 "motivating_failure": "Toulmin failure mode 'warrant' dominates...",
 "superseded_by": null}
```

**This is not yet folded into `BB_SCHEMA_USER_EXTENSIONS`** — the v0.0.52 mechanism writes the event but does not auto-reload the schema. Re-running `tessellum` in a fresh process and calling `fold_schema_events(load_event_log(...))` does materialise the edge; the live schema in the validation venv remains unmodified post-run. This is intentional in v0.0.52 (the seed vault should not auto-mutate as a side effect of validation) but worth noting as a Phase B integration concern.

## Blind spots discovered

The validation surfaces four specific deficiencies the v0.0.52 heuristic cannot address. Each becomes a constraint on the Phase B LLM-driven proposer's prompt design.

### BS-1 — No representativeness check

The 92% warrant rate is a real signal *only if* the observation set is representative of what DKS will see in production. This run's set is structurally biased: every observation is an open methodological/architectural question, and questions of that shape almost mechanically invite warrant attacks. A production deployment ingesting (say) incident reports would skew premise-heavy; one ingesting benchmark results would skew counter-example-heavy.

**The heuristic has no signal for distinguishing "the schema is missing a warrant edge" from "the observation set is warrant-shaped."** It assumes the input is representative; it has no way to gate on representativeness.

→ Phase B.2 LLM proposer prompt must include a representativeness sanity check: given the observation summaries (or just their FZ-source/category metadata), is the distribution likely to be input-induced or schema-induced?

### BS-2 — No mapping for `undercutting`

The v0.0.52 lookup table covers warrant, counter-example, premise. Undercutting failures (8% in this run) generate zero proposals. The Toulmin literature distinguishes undercutting as a distinct attack mode for good reason; meta-DKS should have a schema-edit candidate for it.

→ Phase B.2 LLM proposer must reason about all four Toulmin components without relying on a fixed lookup, or the heuristic table should grow a fourth entry (cheap, but doesn't generalise).

### BS-3 — No strength gradation

All 25 counters fired at `strength: strong`. The Toulmin-failure-count metric the heuristic uses ignores strength entirely — a `weak` counter at 30 cycles and a `strong` counter at 30 cycles produce identical proposals. The v0.0.52 mechanism cannot down-weight noisy signals.

→ Phase B.2 must weight by counter strength: prefer `strong > moderate > weak`, and possibly drop `weak` counters from the failure-count metric entirely. Open question for the user: is `weak` strength a real category or an LLM-generation artifact?

### BS-4 — Warrant-revision telemetry is absent in fresh-mode runs

All 25 cycles ran `mode: fresh`. Zero warrants got revised or superseded; the warrant-attack-rate signal that Phase 5 ships is therefore zero for this run. The v0.0.52 `MetaObservation` *can* receive `top_attacked_warrants` data, but only when extend/branch modes have produced revisions. The validation run cannot exercise the cross-cycle attack signal.

→ Phase V's findings cover the *single-cycle* meta-DKS path well. A future validation should curate a 25-observation set with `mode: extend`/`branch` to exercise the warrant-threading path, or rely on the v0.0.53 production run to accumulate warrant revisions organically.

## Recommendations for Phase B (LLM proposer + attacker)

Five concrete prompt-design constraints, derived from BS-1 through BS-4:

| # | Constraint | Source |
|---|------------|--------|
| **C1** | The proposer prompt must receive the *full Toulmin distribution + sample counter-argument quotes*, not just aggregate counts | BS-1: aggregate masks input bias |
| **C2** | The proposer prompt must reason about all four Toulmin components symmetrically (no fixed lookup) | BS-2: undercutting has no v0.0.52 mapping |
| **C3** | The proposer prompt must receive counter strengths and weight accordingly | BS-3: strength is currently dropped |
| **C4** | The proposer must produce an explicit representativeness assessment as a field in its JSON output (e.g., `"input_bias_risk": "low/medium/high"` with a justification) | BS-1: the heuristic has no signal for this |
| **C5** | The attacker (B.3) must be able to fire a counter-argument of kind "the proposed edge is responsive to input bias, not a schema gap" | BS-1 + C4: if proposer flags input bias, attacker should use that |

Two procedural notes:

- **Default proposer for v0.0.53** should remain the heuristic (today's `HeuristicProposer`, refactored from `_generate_proposals`). The LLM proposer becomes opt-in via `--proposer llm`. Reason: the heuristic produces *exactly one* well-formed proposal on this validation set — it's not broken, it's just incomplete. The LLM proposer adds capability; it doesn't supplant.
- **The validation fixture** (cycle traces frozen at `tests/fixtures/dks_meta/validation_v053/`) becomes the gold-standard input for the Phase B LLM proposer's smoke tests. Assertions: the LLM proposer also returns 1 proposal on this set (recall test); the proposal mentions warrant attack pattern (precision test); the `input_bias_risk` field reports `medium` or `high` (representativeness test).

## Cost + time

- LLM cost: ~$0.85 (Anthropic, 25 cycles × ~4 calls/cycle × ~3K tokens/call avg)
- Wall-clock: 26 minutes (mean 63s/cycle, slower than the $30s estimate)
- Within the [plan_meta_dks_validation_and_polish](../../../plans/plan_meta_dks_validation_and_polish.md) budget (≤$5)

## Open questions

| # | Question |
|--:|----------|
| **OQ-2c1a-a** | Is `strength: weak` a real category? — leans yes (Toulmin counters can have low evidential force) but every counter in this run fired at `strong`, so we have no negative-case data. v0.0.53's first 20-50 production cycles will clarify. |
| **OQ-2c1a-b** | Should the validation set be regenerated each release, or frozen as v0.0.53's? — leans frozen (per plan_meta_dks_validation_and_polish OQ-V-a); v0.0.54+ can curate a different set when their scope demands it (e.g., when Phase 10 multi-perspective ships). |
| **OQ-2c1a-c** | What would a *premise-shaped* validation set look like? — concrete claims with specific data, e.g., "TESS-005 fires on N of M counter-argument notes" / "The 50-cycle retract bar produced 0 retracts on a 200-cycle production set" — observations where the data field of Toulmin's warrant pattern is itself the contestable surface. Worth assembling as a v0.0.54-class follow-up validation. |
| **OQ-2c1a-d** | Why did `mode: fresh` produce 25/25 closed-loop terminations with 0 gated? — the gate threshold (default 0.6 for ConstantConfidence) was apparently below every initial confidence. Either the prompts produce uniformly low confidence (likely) or the default threshold needs raising for substantive observations. Phase 7's CalibratedConfidence may surface this once the warrant_history.jsonl accumulates more data. |
| **OQ-2c1a-e** | Should `tessellum dks --meta` auto-reload the schema after `--apply`? — leans no for the seed vault (validation should not mutate the live schema as a side effect), but the post-apply state isn't actually queryable today either. A separate `tessellum dks meta-status --runs-dir <d>` showing the folded schema state would close this gap. Phase B candidate. |

## Related Notes

- **Parent**: [FZ 2c1: `thought_meta_dks_design`](thought_meta_dks_design.md) — the design synthesis this note validates
- **Grand-parent**: [FZ 2c: `thought_dks_transition_model_adaptation`](thought_dks_transition_model_adaptation.md) — the three-stage adaptation pipeline this validation feeds into
- **Plan**: [`plan_meta_dks_validation_and_polish`](../../../plans/plan_meta_dks_validation_and_polish.md) — Phase V is this note; Phase B operationalises the recommendations
- **Curation script**: [`scripts/curate_validation_observations.py`](../../../scripts/curate_validation_observations.py) — reproducible observation set

## See Also

- [`entry_dialectic_trail`](../../0_entry_points/entry_dialectic_trail.md) — Trail 2 per-trail entry point (this note is FZ 2c1a)
- [`entry_folgezettel_trails`](../../0_entry_points/entry_folgezettel_trails.md) — master FZ trail map

---

**Last Updated**: 2026-05-10
**Status**: Active — FZ 2c1a, Dialectic trail (validation evidence for v0.0.52 meta-DKS; informs Phase B LLM proposer prompt design)
