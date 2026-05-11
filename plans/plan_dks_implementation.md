---
tags:
  - project
  - plan
  - tessellum
  - dks
  - dialectic
  - composer
  - implementation
keywords:
  - DKS implementation plan
  - dialectic knowledge system runtime
  - 7-component closed loop
  - warrant precision
  - dialectical adequacy
  - R-P productive half
  - System P runtime
topics:
  - Dialectic Knowledge System
  - System Architecture
  - v0.2 Roadmap
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
---

# Plan — Implement DKS (Dialectic Knowledge System) Runtime

## Problem

The **Dialectic Knowledge System (DKS)** is the closed-loop dialectic protocol that turns Tessellum's typed substrate from a static reference library into a *learning* knowledge system. Its design is fully specified in the Architecture and Dialectic trails — what's missing is the runtime.

As of v0.0.37 the gap is concrete and named: per the R-Cross gap audit ([FZ 1a1b1](../vault/resources/analysis_thoughts/thought_cqrs_r_cross_gap_audit.md)), **R-P (Schema ⊥ Runtime co-evolution) is held only by absence**. The schema is closed at 8 BB types + 10 epistemic edges; the runtime that should co-evolve with it isn't shipped; therefore R-P has nothing to enforce against. Building DKS is what activates R-P from "latent" to "actively enforced."

This plan specifies how DKS gets implemented and integrated with the existing composer / retrieval / format / capture subsystems without violating R-P, R-D, or R-Cross.

## What DKS is (from the trail)

Per [`thought_dks_design_synthesis`](../vault/resources/analysis_thoughts/thought_dks_design_synthesis.md) (FZ 2a), DKS is **a closed-loop, 7-component protocol that runs on a typed substrate to turn observed disagreement into improved warrants**:

| # | Component | What it produces | BB type |
|--:|-----------|------------------|---------|
| 1 | Observation source | Typed records of what happened | `empirical_observation` |
| 2 | Argument generator A | A typed claim with a warrant, drawn from existing rules | `argument` |
| 3 | Argument generator B | A second typed claim with a different warrant (for cross-check) | `argument` |
| 4 | Disagreement detector | A typed `contradicts` edge between A and B | (edge — a relation) |
| 5 | Counter-argument capture | A typed counter-argument naming which Toulmin component is broken | `counter_argument` |
| 6 | Pattern discovery | A typed model aggregating contradictions into structural regularities | `model` |
| 7 | Rule improvement | A revised warrant (procedure or concept) that prevents the same contradiction in future cycles | `procedure` / `concept` |

The loop **closes** when step 7's revised warrant feeds back into the next cycle's step 2 / step 3. Each step corresponds to one BB-to-BB epistemic edge — R-P's enforcement guarantees this 1:1 mapping holds in code.

## Why we need it

Four reasons DKS is the highest-leverage v0.2 work:

1. **R-P becomes enforceable.** Without DKS, the BB schema is unchallenged — there's no runtime to test it against. With DKS, every new BB-edge addition has to be justified by a runtime phase that produces it, and vice versa. The schema becomes provably load-bearing.
2. **The substrate becomes a learning system.** Today Tessellum is an accumulating typed-knowledge library. Each note added makes the vault bigger but doesn't *update* anything that came before. DKS closes the loop: counter-arguments revise the warrants of future arguments. The vault gets smarter over time without a new training corpus.
3. **The COE skill becomes the first instance of a general pattern.** `skill_tessellum_write_coe` is a *one-shot* DKS cycle (5 Whys → counter-argument-as-root-cause → action items as revised procedures). DKS generalises it: same loop, run continuously over observations rather than once per incident.
4. **Folgezettel becomes machine-produced.** FZ trails today are hand-authored — Trail 1 (Architecture), Trail 2 (Dialectic), Trail 3 (Retrieval) were each composed by a human reasoning step-by-step. DKS makes that argumentative descent **automatic**: every cycle leaves an FZ trail behind it as a side-effect of running. The dialectic and the trail are two views of the same thing.

## DKS and Folgezettel are the same mechanism

This is the load-bearing design observation. The full argument lives in [`thought_dks_fz_integration`](../vault/resources/analysis_thoughts/thought_dks_fz_integration.md) (FZ 2a1); a short version follows because it shapes every phase of the implementation.

**Folgezettel** ([`term_folgezettel`](../vault/resources/term_dictionary/term_folgezettel.md)) is the *spatial* encoding of argumentative descent — `1 → 1a → 1a1 → 1a1a` says "this note descends from that one in the order thinking developed." Luhmann used FZ to record how one slip led to the next.

**DKS** ([`term_dialectic_knowledge_system`](../vault/resources/term_dictionary/term_dialectic_knowledge_system.md)) is the *temporal* mechanism that produces argumentative descent — observation → argument → counter → pattern → revised warrant.

They are not two systems that *integrate*; they are **one system viewed from two axes**:

| Axis | View |
|------|------|
| **Spatial** (FZ) | The relationship between any two nodes is `descends-from` — visible by reading their `folgezettel:` IDs |
| **Temporal** (DKS) | The relationship between any two nodes is `produced-by` — visible by tracing the cycle that emitted them |

Every DKS cycle **must produce a Folgezettel trail** as its substrate output. The 7 components map onto a 6-node trail descent (the 4th component is an edge, not a node):

```
DKS component               →    FZ position
─────────────────────────────────────────────────
Step 1: Observation         →    cycle root (FZ N)
Step 2: Argument A          →    FZ N.a
Step 3: Argument B          →    FZ N.b (sibling — different perspective)
Step 4: Disagreement edge   →    (not a node — a contradicts link from N.b to N.a or vice versa)
Step 5: Counter-argument    →    FZ N.a.a if attacking A; FZ N.b.a if attacking B
Step 6: Pattern             →    FZ N.a.a.a (descends from the counter that revealed it)
Step 7: Rule revision       →    FZ N.a.a.a.a (leaf — the cycle's deposited warrant change)
```

Each cycle therefore deposits a **6-node FZ trail** into the vault. Multi-cycle runs either:

- **Start a fresh trail** when the observation has no prior connection — `cycle_id = N+1`, root at FZ (N+1).
- **Extend an existing trail** when the new observation refutes / extends a prior cycle's leaf — the new cycle descends from the prior cycle's leaf FZ ID.
- **Branch an existing trail** when the new cycle attacks a *previous* argument (not the leaf) — sibling branching at the attacked argument's FZ position.

The choice is part of DKS's step 1 (observation capture): the runtime decides where in the FZ graph this cycle lives based on whether the observation refers to existing warrants.

### Consequences for the implementation

1. **Every DKS-produced note has `folgezettel:` + `folgezettel_parent:` fields set** by the runtime — not optional, not deferrable. The seed manifest's `_SEED_VAULT_MANIFEST` already includes notes with these fields; DKS does the same automatically.
2. **The validator's TESS-004 rule becomes stronger** than the simple "counter_argument must link to argument" version. It can require that `counter_argument`'s `folgezettel_parent` resolves to a `building_block: argument` note. The link discipline is enforced through the FZ field, not through fragile string-matching in the body.
3. **`entry_folgezettel_trails.md` gains a new trail family**: hand-authored trails (the existing Trails 1, 2, 3) and DKS-produced trails. Both shapes use the same FZ machinery; the distinction is *origin*, not *structure*. The trail map records this provenance.
4. **The eval framework gains a new dimension via FZ alignment**: epistemic congruence (the 6th LLMJudge dim) can use FZ-graph traversal to check whether a cycle's response honoured the trail's argumentative descent.
5. **`tessellum composer dks --report` (Phase 5) can surface FZ-graph metrics**: which trail branches most active, which warrants most attacked, where the dialectic is alive vs dormant.

The implementation is therefore not "DKS *plus* an FZ writer." It's "DKS *as* the FZ writer the system was waiting for."

## Design principles

1. **DKS is a System P runtime, not a third system.** Per the two-systems synthesis at FZ 1a1, DKS is the *dynamic facet* of System P (the typed substrate is the static facet). DKS reads through System D (R-Cross's "P calls D" productive half) but never *is* System D.
2. **Each of the 7 components produces a typed atomic note in the vault.** No new persistence layer. The vault IS the runtime state. A DKS cycle leaves a typed trail through the substrate.
3. **DKS is invokable as a composer skill.** The runtime ships as `skill_tessellum_dks_cycle.md` + sidecar. Users (or agent orchestrators) call `tessellum composer run skill_tessellum_dks_cycle.md --leaves <observations>` to run one cycle, or `tessellum composer dks <observations>` (new CLI subcommand) for the multi-cycle case.
4. **Cycle traces land in `runs/dks/`** — outside `vault/` and `data/`, in the same shape as `runs/composer/` traces. Traces include the cycle's component-by-component output (each step's prompt, each step's response, each step's typed-note-produced).
5. **Confidence-gated escalation is a v0.2 ship-then-tune knob, not a v0.2 launch blocker.** First version: every observation runs the full 7-component cycle. Once we have telemetry on intra-record vs inter-cycle outputs, add the confidence gate.
6. **Termination is by dialectical adequacy, not vote.** Implemented by tracking the surviving-attack set per cycle; when it stabilises (the same warrant survives N cycles), the warrant is "adequate" and high-confidence agents can skip the full cycle.
7. **TESS-004 lands alongside DKS.** A validator rule that `counter_argument` notes must link to the `argument` they attack — promotes the BB-edge relationship from declarative data to invariant. Without it, R-P loses half its enforcement.

## Proposed approach — five phases

| Phase | Scope | Versions | LOC est. |
|-------|-------|----------|----------|
| **Phase 1** | DKS core data shapes + single-cycle dispatcher (Python API) | v0.0.40 | ~400 |
| **Phase 2** | DKS as a composer skill (canonical + sidecar with 7 steps) | v0.0.41 | ~200 LOC + ~600 YAML |
| **Phase 3** | Multi-cycle orchestration + `tessellum composer dks` CLI | v0.0.42 | ~300 |
| **Phase 4** | Integration: P-side retrieval client + TESS-004 validator + eval dim 6 | v0.0.43 | ~250 |
| **Phase 5** | Production polish: confidence gating + persistence + cross-cycle aggregation | v0.0.44 | ~350 |

Total: ~1,500 LOC + 600 YAML across 5 versions. Roughly 1-2 weeks at current cadence.

### Phase 1 — DKS core (~v0.0.40)

Deliverables:

- **`src/tessellum/composer/dks.py`** (~400 LOC) — the Python API:
  - Seven typed dataclasses, one per component output: `DKSObservation`, `DKSWarrant` (Toulmin-typed with `claim`/`data`/`warrant`/`backing`/`qualifier`/`rebuttal`), `DKSArgument`, `DKSContradicts` (edge — no FZ), `DKSCounterArgument` (with `broken_component: Literal["premise","warrant","counter-example","undercutting"]`), `DKSPattern`, `DKSRuleRevision`.
  - `DKSCycleResult` — aggregates all seven; properties `folgezettel_nodes` (the 5 FZ positions deposited) and `closed_loop` (whether step 7 fired).
  - `allocate_cycle_fz(existing_trails, mode, parent_fz)` — the FZ ID allocator implementing the three multi-cycle modes from FZ 2a1 (`fresh` / `extend` / `branch`). Pure function, deterministic given the input set.
  - `DKSCycle.run()` — drives the 7 steps through an `LLMBackend`. Each step is one `_step_N()` method that builds a prompt, calls the backend, parses the JSON response, allocates the next FZ ID, returns the typed dataclass.
- **`tests/smoke/test_dks_core.py`** — 15-20 unit tests:
  - FZ allocator handles all three modes (`fresh` / `extend` / `branch`); the allocator is deterministic.
  - Cycle produces 5 FZ nodes (`folgezettel_nodes` length) when all components fire.
  - Cycle short-circuits when A and B agree (no contradicts → no counter → no pattern → no revision); 3 nodes total.
  - The Toulmin classification in `DKSCounterArgument.broken_component` is one of the 4 literals.
  - The closed-loop property holds: revision's FZ has the pattern as parent, pattern's FZ has the counter as parent, counter's FZ has the attacked argument as parent.

Phase 1 deliberately does not touch the composer skill machinery. It's a pure Python API testable with `MockBackend` (no `[agent]` extras required). Tests demonstrate the loop closes and the FZ subtree is correctly shaped.

### Phase 2 — DKS as a composer skill (~v0.0.41)

Deliverables:

- **`vault/resources/skills/skill_tessellum_dks_cycle.md`** — canonical body with 7 anchored sections (one per component):
  - `## Step 1: Observation Capture <!-- :: section_id = step_1_observation_capture :: -->`
  - `## Step 2: Argument Generator A <!-- :: section_id = step_2_argument_a :: -->`
  - `## Step 3: Argument Generator B <!-- :: section_id = step_3_argument_b :: -->`
  - `## Step 4: Disagreement Detection <!-- :: section_id = step_4_disagreement_detection :: -->`
  - `## Step 5: Counter-Argument Capture <!-- :: section_id = step_5_counter_argument_capture :: -->`
  - `## Step 6: Pattern Discovery <!-- :: section_id = step_6_pattern_discovery :: -->`
  - `## Step 7: Rule Improvement <!-- :: section_id = step_7_rule_improvement :: -->`
- **`vault/resources/skills/skill_tessellum_dks_cycle.pipeline.yaml`** — Composer-compatible sidecar:
  - Each step's `materializer:` produces the right BB type:
    - Steps 1, 2, 3, 5, 6, 7 → `body_markdown_frontmatter_to_file` (produces a typed atomic note)
    - Step 4 → `no_op` (the `contradicts` edge is materialized as a link in the note bodies)
  - `expected_output_schema:` for each step enforces the BB-shape (e.g., step 5 requires `claim`, `target_argument_path`, `broken_toulmin_component`)
  - `mcp_dependencies:` on step 1 includes `session-mcp` (so observations can be extracted from the active session — like the COE skill does)
- **`tests/smoke/test_dks_skill.py`** — integration tests:
  - The skill validates via `tessellum composer validate`
  - The skill compiles to a 7-step DAG via `tessellum composer compile`
  - The skill runs end-to-end against `MockBackend` and produces 7 typed notes
  - Each produced note passes `tessellum format check`

The skill IS DKS at the user-invocable level. Phase 1's Python API is what the skill's executor invokes under the hood; Phase 2's skill is what users actually run.

### Phase 3 — Multi-cycle orchestration + CLI (~v0.0.42)

Deliverables:

- **`src/tessellum/composer/dks.py` extended** (~300 LOC) — multi-cycle support:
  - `DKSRunner` — runs N cycles in sequence, threading the surviving warrants from cycle N into cycle N+1's "existing rules" input
  - `DKSRunResult` — aggregates per-cycle results + the trail of warrant revisions
  - `_aggregate_warrant_changes()` — diffs the warrant set across cycles; tags revisions as `added`, `revised`, `superseded`
- **`tessellum composer dks <skill> --observations <jsonl>`** — new CLI subcommand:
  - Loads N observations from a JSONL file (one per line)
  - Runs the DKS cycle once per observation, threading the warrant set
  - Writes `runs/dks/<timestamp>_<cycle_id>.json` per cycle
  - Writes `runs/dks/<timestamp>_aggregate.json` summarising warrant changes across all cycles
- **`tests/cli/test_dks_cli.py`** — 8-10 CLI smoke tests:
  - `dks` subcommand exists and parses args correctly
  - Empty observation file → exit 0, no traces
  - 3-observation file → 3 cycle traces + 1 aggregate trace in `runs/dks/`
  - Invalid skill path → exit 2

### Phase 4 — Integration with existing systems (~v0.0.43)

This is where the R-Cross productive half lands.

Deliverables:

- **P-side retrieval client** (`src/tessellum/composer/retrieval_client.py` ~100 LOC):
  - `RetrievalClient.search(query, k=20) -> list[RetrievalHit]` — thin adapter that calls into `tessellum.retrieval.hybrid_search()` from a composer step
  - Read-only by construction (no writes; can't import retrieval-mutating code because retrieval doesn't have any)
  - The DKS step 1 and step 6 use this client to check whether observations / patterns already exist in the vault
  - This is the **productive half of R-Cross**: P calls D, formally, with a typed contract
- **TESS-004 validator rule** (`src/tessellum/format/validator.py` +30 LOC):
  - For each `building_block: counter_argument` note, scan the body for at least one link to a `building_block: argument` note ("the attacked argument")
  - Emit `TESS-004` error if no such link is found
  - Document in `vault/resources/term_dictionary/term_format_spec.md`
- **6th LLMJudge dimension `epistemic_congruence`** (`src/tessellum/composer/eval.py` +20 LOC):
  - Adds to `DEFAULT_RUBRIC_DIMENSIONS`: "Does the response honour the BB-type expectations the question implies?"
  - DKS cycles produce typed notes; the eval framework can now score whether they're typed correctly
- **Update `term_dialectic_knowledge_system.md`** — points at the live runtime, not just at the deferred concept
- **Update `entry_dialectic_trail.md`** — adds a row noting the runtime ships at v0.0.43
- **`thought_dks_runtime_integration.md`** (NEW thought note, FZ 2b in the Dialectic trail) — synthesis of how the runtime integrates with composer + retrieval + format + capture; the closing leaf of Trail 2

### Phase 5 — Production polish (~v0.0.44)

Deliverables:

- **Confidence gating** (`src/tessellum/composer/dks.py` +100 LOC):
  - `DKSConfidenceModel` — minimal: a function `(observation, warrants) -> float in [0, 1]`
  - If confidence > threshold: skip steps 2-7, just produce one argument and trust it
  - If confidence ≤ threshold: run the full 7-component cycle
  - Telemetry: each cycle records `escalation_decision: {gated, full}` so an analyst can tune the threshold from data
- **Warrant persistence + cross-cycle aggregation** (`src/tessellum/composer/dks.py` +150 LOC):
  - `WarrantRegistry` — typed wrapper over the substrate's `procedure` and `concept` notes that DKS treats as the current warrant set
  - `WarrantHistory` — append-only log of warrant revisions; lives under `runs/dks/warrant_history.jsonl`
  - DKS reads the current registry at the start of each cycle, writes new revisions at the end
- **Inter-cycle telemetry** — `tessellum composer dks --report` shows:
  - How many cycles in the last N runs hit dialectical adequacy
  - How many warrants were revised vs superseded
  - Top-K most frequently-attacked warrants (signals where the substrate is weakest)
- **Cross-validation** — re-run [`thought_cqrs_r_cross_gap_audit`](../vault/resources/analysis_thoughts/thought_cqrs_r_cross_gap_audit.md)'s checklist after Phase 5 lands and confirm every "productive half" gap is now closed.

## Integration points

The plan touches every existing subsystem; here's how each one accommodates the new runtime without breaking its commitments:

| Subsystem | DKS integration | R-rule status |
|-----------|------------------|---------------|
| **`composer/`** | DKS lives at `composer/dks.py` (Phase 1); invokes Composer's executor + materializers + LLM backend (Phase 2-3) | All Composer Wave 1-5b infrastructure unchanged; DKS is an *application* of the contract pipeline |
| **`retrieval/`** | DKS reads through `composer/retrieval_client.py` (Phase 4 — the P-side client). DKS never imports retrieval directly | R-Cross productive half ✓ |
| **`indexer/`** | DKS reads only the index (System D output); never writes to `data/` | R-Cross defensive half ✓ (no change) |
| **`format/`** | TESS-004 lands here (Phase 4); the validator gains one new rule | R-P promoted from "held by absence" to "enforced" |
| **`capture.py`** | DKS produces typed notes via materializers, not via capture flavors. No new flavor needed; `counter_argument` and friends already in REGISTRY | No change |
| **`init.py`** | Seed manifest gains `runs/dks/.gitkeep` (Phase 3); DKS-related how-to gets added in Phase 4 | No change |
| **`cli/`** | New subcommand `tessellum composer dks` (Phase 3) | Standard Composer extension |
| **MCP** | DKS step 1 uses `session-mcp` (shipped v0.0.36) to extract observations from the active transcript | MCPContract registry already accommodates |

## What this plan does NOT do

Five things deliberately deferred beyond v0.0.44 ("Phase 6+"):

- **Multi-agent debate beyond two arguments.** Phase 1-5 ship the two-argument (A vs B) version. Three+ arguments (the AB literature called this "debate club") wait until usage shows the binary version is insufficient.
- **External-data observation sources.** Observations come from the active session (via session-mcp) or from user-supplied JSONL. No web scraping, no API ingestion, no `inbox/` watcher.
- **Cross-vault federation.** Each Tessellum vault runs its own DKS. Federation (DKS over many vaults' warrants) is a v0.3+ research direction.
- **Real-time / streaming mode.** DKS runs are batch (one explicit invocation = N cycles). Streaming (DKS reacts to every new observation as it lands) requires a daemon model we don't have yet.
- **Pluggable termination criteria beyond dialectical adequacy.** The literature has other adequacy notions (Pollock's defeat semantics, Caminada's labeling). Phase 5 ships Dung-grounded labelling only.

These are recorded so the next plan author can find them.

## Migration steps for Phase 1 (when we start)

Execute as one focused commit (Phase 1 only; subsequent phases get their own plan iteration or commit batch):

1. **Author `src/tessellum/composer/dks.py`** with the 5 dataclasses + `DKSCycle.run()` + `MockBackend`-driven test runner.
2. **Add `tests/smoke/test_dks_core.py`** (15-20 tests covering the cycle, termination, BB-typing, degraded cases).
3. **Export from `composer/__init__.py`**: `DKSCycle`, `DKSCycleResult`, `DKSObservation`, `DKSWarrant`, `DKSArgument`, `DKSCounterArgument`.
4. **Update `composer/__init__.py`'s `__all__`** to include the new names.
5. **Run the suite**: 488 + ~18 new tests = ~506 expected pass count.
6. **Bump v0.0.40, write CHANGELOG entry, commit + push, PyPI.**

Phases 2-5 follow the same pattern: focused commits, one major piece per version.

## Open questions

- **Warrant storage: in the substrate or in a separate file?** The plan says "in the substrate" (each warrant is a `procedure` / `concept` note). The alternative is `runs/dks/warrant_history.jsonl` only. Lean: substrate is the source of truth (R-P discipline); the JSONL is the audit log of revisions, not the current state.
- **Argument generator differentiation**: how do A and B differ when both come from the same warrant set and the same model? Options: (1) different system prompts ("be conservative" vs "be exploratory"); (2) different models (`claude-opus-4-7` vs `claude-sonnet-4-6`); (3) different sampling temperatures. Lean: (1) ships first because it's prompt-only; (2) and (3) layer on later.
- **Pattern discovery (step 6) substrate**: does it run only when ≥ N contradictions have accumulated, or every cycle? Lean: every cycle, but the prompt instructs the agent to return "no new pattern" when the data is insufficient.
- **Confidence gate threshold default**: per the FZ trail, "the MAD literature shows debate degrades on simple tasks." What's the right initial threshold? Lean: 0.85 — high enough that easy cases skip the full cycle, low enough that contested cases get the full treatment. Tunable from telemetry in Phase 5.
- **TESS-004 strictness**: error or warning? A new `counter_argument` note created via `tessellum capture counter_argument <slug>` won't yet have the link to an argument — the template includes a placeholder. Should that placeholder produce an error or a warning? Lean: warning during authoring, error once `status: active`. The validator can check status.

## See Also

- [`plan_composer_port`](plan_composer_port.md) — the 6-wave Composer port; DKS is the first major *application* built on top of it
- [`plan_retrieval_port`](plan_retrieval_port.md) — the 5-wave Retrieval port; the P-side retrieval client (Phase 4) is its public consumer
- [`thought_dks_evolution`](../vault/resources/analysis_thoughts/thought_dks_evolution.md) — FZ 2 — the six-step descent that arrived at the design this plan implements
- [`thought_dks_design_synthesis`](../vault/resources/analysis_thoughts/thought_dks_design_synthesis.md) — FZ 2a — the 7-component synthesis this plan operationalises
- [`thought_cqrs_r_cross_rules`](../vault/resources/analysis_thoughts/thought_cqrs_r_cross_rules.md) — FZ 1a1b — the three rules the implementation must respect
- [`thought_cqrs_r_cross_gap_audit`](../vault/resources/analysis_thoughts/thought_cqrs_r_cross_gap_audit.md) — FZ 1a1b1 — names the productive-half gaps this plan closes
- [`thought_src_tessellum_system_review`](../vault/resources/analysis_thoughts/thought_src_tessellum_system_review.md) — the system review whose DKS-runtime finding motivates this plan
- [`term_dialectic_knowledge_system`](../vault/resources/term_dictionary/term_dialectic_knowledge_system.md) — DKS canonical (gets updated in Phase 4 to point at the live runtime)
- [`skill_tessellum_write_coe`](../vault/resources/skills/skill_tessellum_write_coe.md) — the existing one-shot DKS instance; the pattern DKS generalises

---

**Last Updated**: 2026-05-10
**Status**: Active — draft pending user approval, then ships across 5 versions as v0.0.40 → v0.0.44.
