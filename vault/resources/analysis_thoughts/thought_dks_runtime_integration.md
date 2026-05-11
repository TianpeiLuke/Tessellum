---
tags:
  - resource
  - analysis
  - argument
  - dks
  - folgezettel
  - dialectic
  - runtime
  - integration
keywords:
  - DKS runtime integration
  - P-side retrieval client
  - TESS-004 validator
  - epistemic congruence rubric
  - R-Cross productive half
  - dialectic adequacy
  - dks composer skill
  - dks cli
topics:
  - Dialectic Knowledge System
  - System Integration
  - System P Runtime
  - R-Cross Discipline
language: markdown
date of note: 2026-05-10
status: active
building_block: argument
folgezettel: "2b"
folgezettel_parent: "2"
---

# DKS Runtime Integration: How the Closed Loop Wires Into the Rest of Tessellum (FZ 2b)

## Thesis

The DKS design (FZ 2a) and its FZ duality (FZ 2a1) explain *what* the runtime is. This note answers the next question: *what does it touch?* The Phase 1-4 implementation lands DKS as a working system that exercises every other Tessellum subsystem along a typed contract — Composer dispatches its steps, Retrieval feeds its observation/pattern lookups, Format enforces its typed edges via TESS-004, Capture-style materialisers persist its outputs, and Eval's 6th rubric dimension scores whether its outputs honour the BB-type expectations. **DKS is the first runtime that exercises all four R-rules at once** (R-P, R-D, R-Cross — defensively and productively).

## The integration map

DKS is a *peer module* to Composer / Retrieval / Indexer / Format / Capture, not a feature inside any of them (this was clarified in the v0.0.43 refactor; see [`plan_dks_implementation`](../../../plans/plan_dks_implementation.md) for the package-layout rationale). The runtime sits at `tessellum.dks`; the relationships look like:

```
                                   tessellum.dks  (runtime)
                                         │
        ┌────────────────────┬───────────┼────────────┬─────────────┐
        ▼                    ▼           ▼            ▼             ▼
  tessellum.composer  tessellum.retrieval  tessellum.format  tessellum.indexer
  (LLMBackend +       (hybrid_search via   (TESS-004 +       (writes that DKS
   skill executor)     RetrievalClient)    BB enums)          reads through D)
        ▲                    ▲                                     ▲
        │                    │                                     │
        └─── DKS calls ──────┴─────────── DKS reads ────────────────┘
        (P-side; never reverse)
```

Each arrow is one-directional and typed. The boundary is what makes DKS *safe to extend* — adding a Phase 6+ capability (multi-agent debate, real-time mode, federation) lands inside `tessellum.dks/` and doesn't perturb the others.

## What each subsystem contributes

### Composer — the dispatcher

DKS uses Composer's `LLMBackend` abstraction (Mock / Anthropic) and the [`skill_tessellum_dks_cycle`](../skills/skill_tessellum_dks_cycle.md) canonical + sidecar pair. A single closed cycle is invokable two ways:

- As a **Composer skill**: `tessellum composer run skill_tessellum_dks_cycle.md --leaves <observation>` — flows through `compile_skill` + `run_pipeline`; each of the 7 steps is one materialised call against `body_markdown_frontmatter_to_file` (step 4 is `no_op` because the contradicts edge is a link, not a file).
- As a **direct Python call**: `DKSCycle(observation, warrants, backend).run()` — same loop, no composer plumbing; useful for embedding DKS inside other Python code.

Multi-cycle runs go through the dedicated [`tessellum dks <observations.jsonl>`](../../../src/tessellum/cli/dks.py) top-level CLI (peer of `tessellum fz`), which threads warrants via `DKSRunner` and writes per-cycle + aggregate traces to `runs/dks/`.

### Retrieval — the observation/pattern lookup (Phase 4)

DKS step 1 (observation capture) and step 6 (pattern discovery) need the same primitive: *"has this observation / contradiction pattern shown up before in the vault?"*. The plan calls this **the productive half of R-Cross** — System P (DKS) reads through System D (retrieval), with no return path.

Phase 4 ships [`tessellum.dks.RetrievalClient`](../../../src/tessellum/dks/retrieval_client.py): a typed adapter around `hybrid_search` (BM25 + dense via RRF). Read-only by construction — no `index()`, `update()`, or `delete()` surface; the underlying retrieval module exposes no mutating operations either; R-Cross holds *productively* now, not just defensively.

A typical usage from inside step 1:

```python
client = RetrievalClient(db_path="data/tessellum.db")
prior_hits = client.search(observation.summary, k=10)
# If any hit's note is itself an empirical_observation with high RRF
# overlap, step 1 may re-cycle the prior FZ rather than allocate a new
# root — extend mode in DKSRunner, instead of fresh mode.
```

The client's `db_path` is constructed once per cycle; reuse across the 7 steps is trivial. Failure mode: missing index DB → `FileNotFoundError` at construction, caught by the cycle's outer dispatcher.

### Format — the structural guard (Phase 4 lands TESS-004)

The validator was already enforcing the YAML field discipline (YAML-010..099) and the folgezettel pair (TESS-001 / TESS-002 / TESS-003). Phase 4 adds **TESS-004**: a `building_block: counter_argument` note with `status: active` must have at least one body link to a `building_block: argument` note. The static, single-file rule cannot inspect the index, but it can resolve markdown links on disk and parse the target's frontmatter — that's enough to make the typed edge structurally observable.

The rule has an authoring-state exemption: `status: template` / `draft` / `stub` / `archived` are skipped. Templates exist to be copied and filled; drafts are still in progress. Only once a counter is `status: active` does the missing-argument-link become an error. (This matches the open-question lean in [`plan_dks_implementation`](../../../plans/plan_dks_implementation.md): "warning during authoring, error once `status: active`.")

TESS-004 + the FZ-pair rules (TESS-001/002) together promote the BB-edge declaration *from comment to invariant*. R-P (Schema ⊥ Runtime co-evolution) moves from "held by absence" to "actively enforced".

### Eval — the content-quality probe (Phase 4 adds the 6th dim)

`DEFAULT_RUBRIC_DIMENSIONS` grows from 5 to 6 with the addition of **`epistemic_congruence`**: *"Does the output honour the BB-type expectations the question implies?"* DKS cycles produce typed notes (`empirical_observation` / `argument` / `counter_argument` / `model` / `procedure` / `concept`), and the LLMJudge can now score whether they're typed correctly — not just whether they're clear or complete in the abstract.

The judge prompt template iterates over dimensions dynamically, so the addition is a single-line edit; the CLI's canned default-response generator (`tessellum composer eval` without `--judge-mock-responses`) now reads from `DEFAULT_RUBRIC_DIMENSIONS` instead of hardcoding the dim list. This is a small but load-bearing change: future rubric additions for DKS-specific properties (e.g. `dialectical_adequacy` in Phase 5) require no further plumbing.

### Capture — no new flavor needed

`counter_argument`, `argument`, `empirical_observation`, `model`, `procedure`, `concept` are all already in the capture flavor REGISTRY. DKS produces these notes via the Composer-skill's `body_markdown_frontmatter_to_file` materialiser, not via the `tessellum capture` CLI flavor. No new capture flavor is required for DKS-emitted notes; the materialiser writes the YAML + body directly, and the indexer picks up the new files on the next `tessellum index build`.

### Indexer — read-only consumer

DKS never writes to `data/`. The indexer's read-side products (`notes_fts`, `notes_vec`, `note_links`) are consumed via the retrieval client. R-Cross's defensive half (P does not mutate D) is held by construction — DKS imports `tessellum.retrieval`, which itself imports no DKS or composer code. The dependency graph stays a DAG.

## R-Cross — both halves now enforced

[`thought_cqrs_r_cross_rules`](thought_cqrs_r_cross_rules.md) (FZ 1a1b) and [`thought_cqrs_r_cross_gap_audit`](thought_cqrs_r_cross_gap_audit.md) (FZ 1a1b1) named the four halves:

| Rule | Defensive half | Productive half | Status pre-Phase 4 | Status post-Phase 4 |
|------|----------------|------------------|--------------------|---------------------|
| **R-P** (Schema ⊥ Runtime) | BB schema closed at 8 + 10 edges | Schema mutates only when runtime needs it | Held by absence (no runtime) | TESS-004 + DKS runtime exercise every typed edge |
| **R-D** (Descriptive purity) | Candgen never reads BB types | BB types enter at Stages 3-4 only | ✓ (no change needed) | ✓ (no change needed) |
| **R-Cross** (P calls D; D never calls P) | DKS never mutates retrieval (no API to mutate) | DKS reads through a typed P-side client | Held by absence | RetrievalClient lands; productive half active |

The remaining gap pre-v0.0.44 was the productive half: R-P had no runtime to exercise it; R-Cross had no client to formalise P's read of D. Phase 4 closes both. The substrate is now actively constrained by the runtime that uses it, and the runtime is constrained by the typed contract its client honours.

## What this enables next

Three things become possible once the integration is wired:

1. **Multi-cycle sessions can reuse prior FZ subtrees.** When step 1 calls `RetrievalClient.search(observation.summary)` and finds a high-overlap prior observation, the cycle can run in `extend` mode instead of `fresh` mode — descending from the prior cycle's leaf rather than starting a new root. The 6-node trail becomes a 12+ node DAG of related contradictions.
2. **Counter-argument link discipline becomes machine-auditable at commit time.** TESS-004 means a CI step (`tessellum format check vault/`) can fail PRs that add active counter_arguments without naming the attacked argument. R-P enforcement moves from "documentation" to "test gate".
3. **DKS skill outputs become rubric-scorable.** With `epistemic_congruence` in the default rubric, `tessellum composer eval` can score whether a DKS cycle's produced notes are *typed correctly* — not just whether the prose is fluent. This is the metric Phase 5's confidence gate needs as input.

## What remains for Phase 5

Phase 5 (v0.0.45) ships the last load-bearing piece: **confidence gating** + **warrant persistence**. The runtime is wired today; what's missing is a way to *decide when to run the full 7-component cycle vs. when to short-circuit*. The gate reads from telemetry the integration enables — TESS-004 pass-rate, `epistemic_congruence` mean score, prior-cycle adequacy — to decide whether the next observation deserves the full loop. Once that lands, DKS is production-grade and the v0.2 work is the headline polish: federated DKS, multi-agent debate beyond two arguments, real-time streaming. None of those require structural changes to the integration sketched here.

## Related Notes

- **Parent**: [FZ 2: `thought_dks_evolution`](thought_dks_evolution.md) — six-step descent that arrived at DKS
- **Sibling (synthesis)**: [FZ 2a: `thought_dks_design_synthesis`](thought_dks_design_synthesis.md) — the 7-component pattern
- **Sibling sharpening**: [FZ 2a1: `thought_dks_fz_integration`](thought_dks_fz_integration.md) — DKS × FZ duality
- **R-Cross rules**: [FZ 1a1b: `thought_cqrs_r_cross_rules`](thought_cqrs_r_cross_rules.md) — the three rules this integration exercises
- **R-Cross gap audit**: [FZ 1a1b1: `thought_cqrs_r_cross_gap_audit`](thought_cqrs_r_cross_gap_audit.md) — the productive-half gaps Phase 4 closes
- **Plan**: [`plan_dks_implementation`](../../../plans/plan_dks_implementation.md) — the 5-phase implementation plan
- **Term**: [`term_dialectic_knowledge_system`](../term_dictionary/term_dialectic_knowledge_system.md) — DKS canonical
- **Skill**: [`skill_tessellum_dks_cycle`](../skills/skill_tessellum_dks_cycle.md) — the agent-invocable surface
- **CLI source**: [`src/tessellum/cli/dks.py`](../../../src/tessellum/cli/dks.py) — `tessellum dks <observations.jsonl>`
- **Retrieval client**: [`src/tessellum/dks/retrieval_client.py`](../../../src/tessellum/dks/retrieval_client.py) — P-side R-Cross client
