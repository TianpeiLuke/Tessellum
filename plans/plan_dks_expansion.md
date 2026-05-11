---
tags:
  - project
  - plan
  - tessellum
  - dks
  - dialectic
  - fsm
  - bb_ontology
  - meta_dks
  - learning
keywords:
  - DKS expansion plan
  - FSM refactor
  - meta-DKS
  - schema learning
  - learned confidence model
  - multi-perspective debate
  - Dung semantics
  - dialectical adequacy
  - TESS-005 validator
  - bb audit
topics:
  - Dialectic Knowledge System
  - System Design
  - Folgezettel
  - v0.2 Roadmap
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
---

# Plan — Expand and Improve DKS Around the FSM-on-BB-Graph Framing

## Problem

The 5-phase `plan_dks_implementation.md` is fully shipped (Phases 1-5 at v0.0.40, v0.0.42, v0.0.43, v0.0.44, v0.0.45). The runtime is feature-complete *per that plan*: closed-loop cycle, multi-cycle orchestration, P-side retrieval, TESS-004, confidence-gate mechanism, warrant persistence, inter-cycle telemetry.

What FZ 1b and FZ 2a2 surface, that the original plan did not see, is that **DKS is a finite-state machine on the BB ontology graph** — and the three *learning levels* the FSM lens makes separable are unevenly addressed:

| Level | Today's status | What's missing |
|-------|----------------|-----------------|
| **1 — Instance** (every cycle adds typed nodes + edges) | ✓ operational | Telemetry surfaces are per-cycle, not corpus-wide |
| **2 — Edge-weight** (transition preferences bias from counter outcomes) | partial — warrant threading + `--report` top-attacked exist; the gate is `ConstantConfidence` placeholder | A *learned* confidence model that reads telemetry; retrieval-grounded warrant selection |
| **3 — Schema** (δ itself mutates when sustained failures show the schema is wrong) | not implemented — schema is closed at 8+10 + 1 DKS extension | The meta-DKS runtime; schema-mutation discipline; versioned BB_SCHEMA |

The dispatcher refactor (replacing the 7 hand-coded `_step_*` methods with `DKSStateMachine.walk()` over `BB_SCHEMA`) is *load-bearing* for Level 3 but not for Levels 1-2. v0.0.47 lands the *data structure* (`tessellum.bb` module: `BBType` + `BB_SCHEMA` + `BBGraph`); the *dispatcher* still walks the schema implicitly via seven hand-coded steps. The plan below changes that.

## What DKS is now (v0.0.47 baseline)

| Layer | Module | Status |
|---|---|---|
| BB ontology — schema graph | `tessellum.bb.types` (BBType, BB_SCHEMA — 16 typed edges) | ✓ shipped v0.0.47 |
| BB ontology — corpus graph | `tessellum.bb.graph` (BBNode, BBEdge, BBGraph) | ✓ shipped v0.0.47 |
| DKS — single-cycle core | `tessellum.dks.core` (DKSCycle, 7-component dataclasses) | ✓ shipped v0.0.40 |
| DKS — multi-cycle orchestration | `tessellum.dks.core` (DKSRunner, WarrantChange) | ✓ shipped v0.0.43 |
| DKS — confidence gating | `tessellum.dks.confidence` (ConstantConfidence, decide_escalation) | ✓ shipped v0.0.45 — mechanism only, no learned signal |
| DKS — warrant persistence | `tessellum.dks.persistence` (WarrantRegistry, WarrantHistory) | ✓ shipped v0.0.45 |
| DKS — P-side retrieval | `tessellum.dks.retrieval_client` (RetrievalClient) | ✓ shipped v0.0.44 |
| DKS — composer skill | `vault/resources/skills/skill_tessellum_dks_cycle.md` + sidecar | ✓ shipped v0.0.42 |
| DKS — CLI | `tessellum dks <jsonl>`, `tessellum dks --report` | ✓ shipped v0.0.43 + v0.0.45 |
| Validator — TESS-004 | counter_argument body must link to BB=argument note | ✓ shipped v0.0.44 |
| LLMJudge — 6-dim rubric | epistemic_congruence added | ✓ shipped v0.0.44 |
| **Dispatcher refactor** | 7 hand-coded step methods → single `walk()` over BB_SCHEMA | deferred per FZ 2a2 |
| **Meta-DKS** | schema-mutation runtime | not implemented |
| **Learned confidence** | calibrated model reading past telemetry | not implemented |
| **N-perspective debate** | only A vs B today | deferred per original plan §6+ |

## Design principles for the expansion

Five principles inherited from `plan_dks_implementation.md` + sharpened by the FSM lens:

1. **DKS is a System P runtime, not a third system.** Same as before; FZ 1a1 hasn't changed.
2. **Each cycle deposits typed BBNodes + BBEdges into the corpus.** Now phrased graph-theoretically: every cycle is one walk through BB_SCHEMA.
3. **Schema changes must follow R-P discipline.** v0.0.47 records *one* schema extension (`CTR → MOD` in `BB_SCHEMA_DKS_EXTENSIONS`). Phase 9's meta-DKS turns "the runtime that proposes schema edits" from documentation into mechanism — but the discipline (every edit is itself dialectical) doesn't relax.
4. **Public API is stable across phases.** Tessellum is pre-v0.1 alpha; we can move internals freely. We don't break v0.0.45-era imports without a forcing function.
5. **Telemetry first, optimisation second.** Every phase ships its observation surface (`--report` fields, BBGraph metrics, validator counts) before it ships its decision surface (learned models, schema edits). You can't tune what you can't see.

## Resolved decisions (8 open questions → 7 decided, 1 empirical)

Decisions taken before Phase 6 starts. The design principle for each is stated; the principle drives the resolution and any subsequent revisit. Each decision is referenced from the phase it affects.

### D1 (Phase 8) — `BBNode` payload shape

**Resolution: subclass-per-`BBType` frozen dataclasses with `kw_only=True`. NO `metadata` dict.**

Principle: *Parse, don't validate.* A metadata dict — typed or not — defers schema decisions to runtime. Subclasses make the BB-type-specific payload first-class; the discriminator (`bb_type: ClassVar[BBType]`) is the same one v0.0.47's DKS dataclasses already carry; `match` works; handler signatures are statically checkable.

```python
@dataclass(frozen=True, kw_only=True)
class BBNode:
    note_id: str
    note_name: str
    folgezettel: str | None = None
    folgezettel_parent: str | None = None
    note_status: str | None = None

@dataclass(frozen=True, kw_only=True)
class ArgumentNode(BBNode):
    bb_type: ClassVar[BBType] = BBType.ARGUMENT
    warrant: DKSWarrant
    evidence: str
    perspective: str = ""
```

Phase 8 consequence: `DKSObservation` / `DKSArgument` / `DKSCounterArgument` / `DKSPattern` / `DKSRuleRevision` become aliases for the corresponding `*Node` subclasses. Backward-compatible imports survive.

### D2 (Phase 7) — Confidence calibration target

**Resolution: 10% default false-gate rate; configurable via `--target-false-gate-rate <float>`; `--calibrate` mode emits the achieved rate from past traces.**

Principle: *Make tuning observable, not baked.* 10% is a Pareto-balanced default for the most common case (some cost saving, low quality drift). Cost-sensitive deployments tighten; quality-sensitive deployments loosen. The principle is "make the achieved rate visible," not "10% is correct" — and `--calibrate` is what surfaces it.

Phase 7 consequence: `CalibratedConfidence` takes `target_false_gate_rate=0.10` constructor kwarg; threshold adjusts to achieve the target on past data via a small line-search.

### D3 (Phase 9) — Schema mutation discipline

**Resolution: Event-sourced schema. Schema state is retractable; schema history is append-only.**

Principle: *Immutability of history, not state.* The dialectical pattern itself argues for retractable: a counter argues against a prior argument; the same applies to schema edits. Event sourcing gives both reversibility and full audit trail.

```python
@dataclass(frozen=True)
class SchemaEditEvent:
    timestamp: str              # UTC ISO-8601
    kind: Literal["added", "retracted", "refined"]
    edge: EpistemicEdgeType
    motivating_failure: str     # FZ of the cycle observation that drove it
    superseded_by: str | None = None  # for "refined" events
```

`BB_SCHEMA_USER_EXTENSIONS` is computed as `fold(SCHEMA_EVENT_LOG)` — walk the log, apply add/retract/refine, output the current set. The log lives at `runs/dks/meta/schema_events.jsonl` (parallel to `runs/dks/warrant_history.jsonl`). Retracting an edge auto-converts any realised corpus edges that instantiated it to *untyped* — a TESS-005 warning that flags the migration, not a silent break.

### D4 (Phase 9) — Meta-meta-schema location

**Resolution: Python module at `tessellum.dks.meta.META_SCHEMA`. PR-gated. No YAML alternative.**

Principle: *Configuration in code when it's load-bearing for correctness.* The meta-meta-schema is the recursion stop — architectural commitment, not deployment config. Code keeps it visible in PR review (a diff against `META_SCHEMA = (...)` is unmissable), allows type annotations, and lives next to the runtime that uses it.

### D5 (Phase 10) — Argument perspectives in YAML

**Resolution: New optional YAML field `argument_perspective: <string>`. Open vocabulary. Validator: must be a string when present.**

Principle: *Round-trip data through the substrate.* If perspective only lives in memory, meta-DKS (Phase 9) can't observe per-perspective failure distributions across cycles — which is the explicit motivation for multi-perspective. Open-vocabulary because the perspectives space is open: "skeptical", "devil's-advocate", "domain-expert" should all work without code changes.

Phase 10 consequence: `ArgumentNode.perspective: str` maps to this YAML field on materialisation. Phase 6's TESS-005 ignores it (no schema implication).

### D6 (Phase 6) — `tessellum bb` CLI namespace

**Resolution: Top-level `tessellum bb` subcommand group. `audit` is one operation under it.**

Principle: *Cohesive namespaces match module boundaries + leave headroom.* The `bb` module is a peer of `format` / `dks` / `composer` / `retrieval` / `fz` — every peer has its own top-level CLI group. Match the shape:

```
tessellum bb audit              # vault-wide graph telemetry (Phase 6)
tessellum bb walk <fz>          # FSM walk visualisation (Phase 8+)
tessellum bb validate-schema    # meta-DKS schema-edit validation (Phase 9+)
tessellum bb show <bb-type>     # nodes of one BB type (future)
tessellum bb migrate            # retroactive schema-edit validation (Phase 9)
```

`format check` is about YAML/links; `bb` is about graph topology. Single responsibility per CLI group.

### D7 (Phase 10) — Termination semantics

**Resolution: Generalise to Dung grounded labelling internally. Preserve `closed_loop` as a derived property.**

Principle: *Liskov substitution + extension.* Dung's grounded semantics is the umbrella; dialectical adequacy is the special case (N=1 attacker, surviving warrant labelled `in`). Generalising makes the runtime more powerful; preserving `closed_loop` as a query over the new mechanism means existing tests don't break.

```python
@property
def closed_loop(self) -> bool:
    if self.rule_revision is None:
        return False
    return self.dung_label(self.rule_revision.folgezettel) == "in"
```

For N=2 (today's default), Dung and adequacy give identical answers. Phase 10 docs flag adequacy as "the N=2 case of grounded labelling."

### D8 (Phase 9) — Schema-edit + corpus migration

**Resolution: Frozen-at-creation by default. Retroactive validation via separate `tessellum bb migrate` command.**

Principle: *Immutability of authored content + separation of write-time and read-time validation.* Every note records `bb_schema_version: <int>` in YAML at creation (auto-populated by the capture pipeline; defaults to the current version). TESS-005 validates against the recorded version — a note authored under v3 is judged by v3's rules forever.

`tessellum bb migrate --target-version current` opts into retroactive validation: emits a *report* of corpus edges that would be flagged under the current schema, so the user can decide whether to update notes or retract the schema edit. Pairs cleanly with D3 (event-sourced schema) — migrations are themselves events.

### Remaining open

Only one question retains genuine empirical uncertainty after the above:

- **Q2's value (10% default false-gate rate)** — the *principle* (configurable + observable) is fixed; the *default* is empirical. Tunable from telemetry once Phase 7 ships; revisit after the first month of `--calibrate` data.

Two phase-internal questions also remain (smaller scope):

- Phase 6's TESS-005 strictness for legacy vaults — leans WARNING globally, ERROR only when `tags` contains `dks`. Validate against real legacy vaults in Phase 6 testing.
- Phase 7's retrieval-grounding mode (pre-filter vs re-rank) — leans re-rank (don't drop warrants; let the agent see the full set sorted by relevance).

---

## Phase 6 — Validator + telemetry generalisation (v0.0.48) — small

The smallest, highest-leverage piece. Closes the easy half of the gap that FZ 1b flagged: corpus-edge validation today only fires on one BB→BB pair (TESS-004's counter→argument). Generalising it pays off immediately and lays groundwork for meta-DKS's observation source.

### Deliverables

- **`tessellum.format.validator` — TESS-005** (`+50 LOC`):
  - For every BB-typed note, every internal `.md` body-link that resolves to another BB-typed note must instantiate a declared `EpistemicEdgeType` (i.e. `(source.bb_type, target.bb_type)` must appear in `BB_SCHEMA`).
  - Untyped corpus edges → emit `TESS-005` ERROR (status: active) / WARNING (other statuses).
  - Skip rule: links between notes whose tags don't include `dks` (this is the legacy non-DKS-authored corpus; we don't break existing vault hygiene).
  - Subsumes TESS-004 (which becomes a special case — `(counter_argument, argument)` is *not* in BB_SCHEMA so TESS-004 keeps firing as a stricter rule).
- **`tessellum bb audit` — new CLI subcommand** (`+200 LOC`):
  - `tessellum bb audit [--db <path>] [--format human|json] [--show-untyped] [--show-by-type]`
  - Reads `BBGraph.from_db()` + emits: total node count by BBType, total edge count by EpistemicEdgeType, list of untyped edges, list of orphan BBNodes (no inbound/outbound corpus edges), list of unrealised schema edges (0 instances in the corpus).
  - The corpus-wide cousin of `tessellum dks --report` (which is run-scoped). Audit is vault-scoped.
- **`tessellum dks --report` extensions** (`+50 LOC`):
  - Add `bb_graph` section: realised edges-by-type counts pulled from `BBGraph.from_db()`; cross-references the per-run aggregate stats with the vault's structural state.
  - New flag `--include-bb-graph` (default off) to opt-in to the join (avoids forcing every report run to read the index DB).
- **Tests** — 12-15:
  - TESS-005 fires on untyped corpus edge (active status); skips on draft/template; the schema-extension edge `CTR → MOD` *passes* TESS-005.
  - `tessellum bb audit` smoke: small vault → expected counts; `--show-untyped` lists known cases; missing DB → exit 2.
  - `--report --include-bb-graph` joins cleanly.

### Why first

It's pure expansion (no public-API break, no refactor). It builds the *telemetry* meta-DKS will need at Phase 9 (top-K underused schema edges, top-K most-violated transitions). And it pays off immediately for hand-authored vault hygiene — TESS-005 is the kind of static-correctness backstop a user wants the moment they have BB-typed notes.

### Decisions

- D6: top-level `tessellum bb` namespace (resolved).
- TESS-005 strictness: WARNING globally, ERROR only when `tags` contains `dks` (phase-internal; validate against real legacy vaults in testing).

## Phase 7 — Learned confidence + retrieval-grounded warrants (v0.0.49) — medium

Operationalises Level 2 learning: the FSM's transition *preferences* become data-driven instead of constant. Replaces `ConstantConfidence` with a model that reads past telemetry, and grounds argument-generation in retrieved warrants (rather than the full warrant set every time).

### Deliverables

- **`tessellum.dks.confidence` — `CalibratedConfidence`** (`+150 LOC`):
  - Reads `WarrantHistory` + (optional) `tessellum dks --report` aggregate JSON files to score `(observation, warrants) → [0, 1]`.
  - Signal sources: (a) recency-weighted warrant attack rate; (b) retrieval-similarity between observation and prior closed-loop observations (via `RetrievalClient`); (c) baseline rate (closed-loop count / total cycles).
  - Output is calibrated against `--report`'s `gated_rate` field — if 95% of "gated" cycles would have closed-looped, the model is over-confident; if 5% would have, it's under-confident. Calibration target: a stated false-gate rate (e.g. ≤10%).
  - Ships with a `--calibrate` mode that reads `runs/dks/` traces and emits a calibration report.
- **`tessellum.dks.core.DKSCycle` — retrieval-grounded warrants** (`+80 LOC`):
  - New optional kwarg `retrieval_client: RetrievalClient | None = None`. When passed, `_step_argument` queries the client for the top-K warrants most relevant to the observation summary; warrants are *ranked* before the prompt sees them, not just enumerated.
  - The argument step's prompt template gets a `{{retrieved_warrants}}` slot; existing warrant-set passthrough survives as fallback.
- **`tessellum.dks.core.DKSCycle._step_disagreement` — semantic detection** (`+50 LOC`):
  - Replaces the current string-compare with one optional LLM call: "are these two claims substantively different?" → boolean.
  - Off by default (preserves Phase 1's local-only step 4); opt-in via `confidence_model.semantic_disagreement = True` or a DKSCycle constructor kwarg.
  - Falls back to string-compare when LLM call fails.
- **`tessellum dks` CLI — wiring**:
  - `--confidence-model {constant,calibrated}` (default `constant`)
  - `--calibrate-from <runs-dir>` (used with `--confidence-model=calibrated`)
  - `--retrieval-db <path>` (passes through to RetrievalClient)
- **Tests** — 15-20:
  - CalibratedConfidence reads a synthetic WarrantHistory + returns scores in [0,1]
  - Same input twice = same score (deterministic)
  - High-attack-rate warrant set → lower confidence
  - Retrieval-grounded `_step_argument` queries the client + injects results into the prompt
  - Semantic-disagreement LLM call is opt-in; default still string-compare

### Why second

It's mostly internal to `tessellum.dks` — no schema mutations, no validator extensions, no API breaks. It operationalises the Level 2 learning that v0.0.45 shipped the *mechanism* for but not the *signal*. Pays off in real LLM-cost savings: a calibrated gate at threshold 0.85 saves 6 of 7 backend calls per gated observation.

### What it doesn't do

- Doesn't change `BB_SCHEMA`. The runtime gets smarter; the substrate's type system doesn't shift.
- Doesn't refactor the dispatcher. The 7 hand-coded steps still exist; we just augment two of them.
- Doesn't address the cold-start problem (no past telemetry → no signal). `CalibratedConfidence` falls back to `ConstantConfidence(0.0)` when telemetry is empty.

### Decisions

- D2: 10% default false-gate rate, configurable via `--target-false-gate-rate <float>` + `--calibrate` mode (resolved; value is empirical and tunable from telemetry).
- Retrieval grounding mode: re-rank (don't drop warrants; phase-internal).

## Phase 8 — Dispatcher refactor (v0.0.50) — medium-large

The deferred FZ 2a2 work. Replaces the 7 hand-coded `_step_*` methods with a generic walker over `BB_SCHEMA`. Per-component dataclasses survive as typed views over `BBNode`; the public API is preserved. This phase exists primarily as the prerequisite for Phase 9 (meta-DKS), but it also pays off in clarity and extensibility for any future walker.

### Deliverables

- **`tessellum.dks.fsm` — new module** (`+250 LOC`):
  - `class DKSStateMachine`:
    - Holds the schema (`BB_SCHEMA`), backend, optional confidence_model, optional retrieval_client.
    - `walk(observation) -> BBPath` drives the cycle:
      1. Compute confidence; decide gated vs full.
      2. Look up valid transitions out of `q₀ = OBS` via `BB_SCHEMA`.
      3. For each step, dispatch to a transition handler registered for `(source_type, target_type, label)`.
      4. Terminate when state ∈ F (procedure / concept / argument-when-gated).
  - `BBPath` dataclass: ordered tuple of `(BBNode, EpistemicEdgeType)` pairs; the full walk.
  - **Transition handler registry**: one handler per BB→BB edge type the cycle actually walks. Handlers take `(observation, warrants, context, edge) → BBNode`. Today's `_step_argument` becomes one handler; `_step_counter` another; etc.
- **`tessellum.dks.core` — per-component dataclasses as views** (`+80 LOC, –200 LOC net`):
  - `DKSObservation`, `DKSArgument`, `DKSCounterArgument`, `DKSPattern`, `DKSRuleRevision` become *view dataclasses* with `from_bb_node(node: BBNode) -> Self` and `to_bb_node() -> BBNode` round-trip methods.
  - The instance fields they carry (warrant, evidence, broken_component, etc.) live in extra `metadata: dict` on `BBNode`, OR in the dataclass fields with a clear separator.
  - DKSCycle (legacy class) survives as a thin wrapper around `DKSStateMachine.walk()` so v0.0.49-era callers don't break.
- **`tessellum dks` CLI** — internals point at `DKSStateMachine`; user-visible behaviour unchanged.
- **Tests** — 15-20:
  - `DKSStateMachine.walk()` produces the same cycle output as `DKSCycle.run()` for matching MockBackend responses (back-compat).
  - The 3 terminal paths (closed loop, short-circuit, gated) reachable via FSM walker.
  - Adding a 4th argument perspective requires only registering one handler (smoke test for Phase 10 readiness).
  - Per-component dataclass round-trip: `BBNode → DKSObservation → BBNode` is identity.

### Why this lands here

Two reasons:

1. **Meta-DKS (Phase 9) is far cheaper with a graph-walker dispatcher.** Without it, every meta-cycle has to either rewrite the per-component code or work around it. The dispatcher refactor is the *enabler*.
2. **Phase 7's retrieval-grounding + semantic disagreement** added complexity to two of the seven hand-coded steps. Refactoring after those land lets us put the new complexity in handlers, not in conditional branches inside the dispatcher.

### What it doesn't do

- Doesn't change the user-visible behaviour. Existing tests pass without modification.
- Doesn't add new BB edges or new transitions. The schema stays at v0.0.47's 16 edges.
- Doesn't change the FZ subtree shape per cycle (still 6/3/2 nodes depending on terminal).

### Decisions

- D1: subclass-per-`BBType` frozen dataclasses with `kw_only=True` (resolved). Existing `DKSObservation`/`DKSArgument`/etc. become aliases for the corresponding `*Node` subclasses; backward-compatible.
- Transition handler registry: instance-scoped (`DKSStateMachine` holds its own). Lets meta-DKS swap handlers without touching cycle-level DKS.

## Phase 9 — Meta-DKS (v0.0.51) — large

The big one. R-P's productive half at its strongest: a *second* DKS walker whose substrate is the schema itself. When the cycle-level DKS keeps hitting the same Toulmin failure on the same warrant shape, meta-DKS proposes a schema edit (add a BB type, add an edge, refine a label). The edit is itself dialectical — it's authored as an argument, attacked, possibly retracted.

### Deliverables

- **`tessellum.dks.meta` — new module** (`+400 LOC`):
  - `MetaObservation`: top-K most-attacked warrants + their Toulmin-failure distribution + (optional) unrealised schema edges from `BBGraph.from_db(...).edges_by_type()`.
  - `SchemaEditProposal`: a typed argument *about* schema. Fields include the proposed change (add edge `(SRC, TGT, label)`; deprecate edge `(...)`; tighten constraint on existing edge), the failure pattern that motivates it, the predicted impact.
  - `MetaCycle`: walks a *meta-FSM* — observation is a MetaObservation, arguments are SchemaEditProposals, counter-arguments attack the proposals, pattern aggregates schema-evolution patterns across meta-cycles, revisions update `BB_SCHEMA_DKS_EXTENSIONS` (or a new `BB_SCHEMA_USER_EXTENSIONS`).
  - The meta-FSM's δ is *itself* a small schema: meta-observation → meta-argument → meta-counter → meta-pattern → meta-revision. We do not infinite-regress: the meta-meta-schema is human-authored.
- **`tessellum.bb.types` — schema versioning** (`+50 LOC`):
  - `BB_SCHEMA_VERSION`: int; bumps on every schema edit landed by meta-DKS.
  - `BB_SCHEMA_USER_EXTENSIONS`: tuple — meta-DKS-emitted edges. Distinct from `BB_SCHEMA_DKS_EXTENSIONS` (which is for runtime-driven edits the project author records).
  - Migration discipline: every schema change goes through `tessellum bb schema-edit` (a new CLI surface for meta-DKS to deposit edits + emit a migration note documenting why).
- **`tessellum dks meta` — new CLI subcommand** (`+150 LOC`):
  - `tessellum dks meta [--runs-dir <dir>] [--target-failure premise|warrant|counter-example|undercutting] [--dry-run]`
  - Reads cycle-level traces, runs `MetaCycle` against the aggregated observations, proposes 0-N schema edits.
  - Default `--dry-run` (proposes but does not apply); `--apply` actually writes to `BB_SCHEMA_USER_EXTENSIONS` and emits a migration note at `vault/resources/analysis_thoughts/schema_edit_<slug>.md`.
- **`vault/resources/skills/skill_tessellum_dks_meta_cycle.md` + sidecar** — composer skill for the meta-cycle (mirrors Phase 2's dks-cycle skill but at the schema level).
- **`vault/resources/analysis_thoughts/thought_meta_dks_design.md`** — new FZ note (FZ 2c or similar) — the meta-DKS design synthesis. Documents the meta-FSM, the human-authored meta-meta-schema, the migration discipline. Sibling of 2a2 (FSM) and 2b (runtime integration).
- **Tests** — 20-25:
  - `MetaCycle` over canned observations proposes a schema edit
  - `--dry-run` doesn't mutate BB_SCHEMA
  - `--apply` mutates `BB_SCHEMA_USER_EXTENSIONS` *and* emits a migration note that validates clean
  - Cycle-level DKS sees the new edge on the next run (re-imports schema; doesn't require process restart? — open question)
  - Recursion safety: meta-DKS cannot mutate the meta-meta-schema (which lives in human-edited code)

### Why this is the centrepiece

Phase 9 is what closes Level 3 learning. Without it, R-P's productive half is "the architect manually edits BB_SCHEMA when they notice a pattern" — same as v0.0.47. With it, the system observes its own dialectic and proposes how it should grow. That is the *operational* form of "schema co-evolves with runtime" that R-P names.

The reason this lands as one phase (and not split) is that the meta-FSM is structurally identical to the cycle-FSM — the same 7-component pattern, the same dialectical adequacy termination, the same WarrantChange diff. What's different is the substrate: the meta-runtime walks a *schema-of-schemas*, not BB_SCHEMA itself. Building the two together makes the recursion self-consistent.

### What it doesn't do

- Doesn't allow arbitrary schema rewrites. The meta-meta-schema (the schema for meta-DKS itself) is human-authored and held fixed. Recursion stops one level up.
- Doesn't auto-apply edits in production by default. `--dry-run` is the default; humans approve via merge of the migration note.
- Doesn't federate across vaults. Each vault's schema evolves independently. Cross-vault learning is a v0.3+ research direction (see "What this plan does NOT do").

### Decisions

- D3: event-sourced schema — retractable state, append-only history (resolved). `BB_SCHEMA_USER_EXTENSIONS` is `fold(SCHEMA_EVENT_LOG)`; events live at `runs/dks/meta/schema_events.jsonl`.
- D4: `tessellum.dks.meta.META_SCHEMA` in code, PR-gated (resolved).
- D8: frozen-at-creation validation + `tessellum bb migrate` for opt-in retroactive checks (resolved).
- Cold-start handling: `--dry-run` produces an empty proposal set; first meaningful run requires ≥ N cycle-level runs (lean: N=20 minimum for a Toulmin-failure distribution to be statistically meaningful; configurable via `--min-cycles`).

## Phase 10 — Multi-perspective debate + Dung labelling (v0.0.52) — medium

The "debate club" deferral from the original plan §6+. The FSM admits N arguments naturally; today's A/B is just N=2. Three things change when N>2.

### Deliverables

- **`tessellum.dks.core.DKSCycle` — N-argument support** (`+150 LOC`):
  - New kwarg `perspectives: tuple[str, ...]` (default `("conservative", "exploratory")`). When provided, the cycle generates one argument per perspective.
  - Step 4's pairwise contradicts becomes a graph: for each pair `(arg_i, arg_j)` where `i < j` and claims differ, emit a `DKSContradicts` edge.
  - The corpus deposits N argument nodes instead of 2; the FZ subtree grows to `1 + N + (counters) + 1 + 1` (root + N arguments + per-attacked-argument counters + pattern + revision).
- **`tessellum.dks.dung` — Abstract Argumentation Framework labelling** (`+200 LOC`):
  - `class DungAF(arguments, attacks)`: builds the AF from the cycle's arguments + contradicts edges.
  - `def grounded_labelling(af) -> dict[arg_id, label]`: implements Dung's grounded semantics — `in` / `out` / `undec`.
  - The surviving warrant set (after step 7) is the set of arguments labelled `in`. Multi-attack adequacy termination becomes: the warrant survives iff its grounded label is `in` after all attacks have been considered.
- **`tessellum.dks.core.DKSRuleRevision` — multi-survivor support** (`+50 LOC`):
  - When multiple arguments survive (Dung label `in`), the revision step picks the strongest survivor (lowest Toulmin failure rate in prior cycles) or emits multiple revisions tagged with their FZs.
- **`tessellum dks` CLI** — `--perspectives <comma-separated>` flag passes through to DKSRunner.
- **Tests** — 15-20:
  - 3-perspective cycle produces 3 argument nodes; contradicts edges form the right pairwise graph
  - Dung grounded labelling on a small AF returns expected labels
  - Adequacy termination: a warrant attacked by 2 sibling arguments but defended by 1 emits the right label
  - Back-compat: 2-perspective default produces same output as Phase 1's A/B cycle

### Why last

It's the literature-rich expansion (MAD, IBIS, Dung) but it doesn't unlock anything Phases 6-9 don't already provide. Useful when DKS is being applied to research contexts where binary A/B isn't enough — e.g. evaluating an LLM's reasoning quality across multiple framings, or running an open-ended thesis exploration.

The phase exists because the user asked the plan to "expand and improve DKS" — multi-perspective is the most-named expansion direction in the literature. Sequencing it last lets the prior phases stabilise first.

### What it doesn't do

- Doesn't introduce reinforcement learning over the perspective set. The perspectives are fixed at cycle construction; learned perspective selection is a v0.3+ research direction.
- Doesn't change the BB ontology. All N arguments are still typed as `BBType.ARGUMENT`; all pairwise contradicts are still typed as the same edge relation.

### Decisions

- D5: new optional YAML field `argument_perspective: <string>`, open vocabulary (resolved). `ArgumentNode.perspective` maps to it; meta-DKS queries the index by this field for per-perspective failure distributions.
- D7: Dung grounded labelling internally; `closed_loop` preserved as a derived property (resolved). For N=2 (today's default), Dung and adequacy give identical answers.
- Meta-DKS observes N-argument cycles via the same `WarrantChange` aggregation as A/B, with the failure distribution stratified by perspective.

## Integration points across all phases

| Subsystem | Phase 6 | Phase 7 | Phase 8 | Phase 9 | Phase 10 |
|-----------|--------|--------|--------|--------|---------|
| `tessellum.bb` | adds telemetry consumers | unchanged | unchanged (becomes the dispatcher's primary input) | adds `BB_SCHEMA_USER_EXTENSIONS` + versioning | unchanged |
| `tessellum.dks.core` | unchanged | adds retrieval grounding + semantic detection | refactors steps into handlers | (no change — meta-DKS is a separate module) | adds N-arg support + multi-survivor revisions |
| `tessellum.dks.confidence` | unchanged | replaces ConstantConfidence with CalibratedConfidence | unchanged | unchanged (meta-DKS has its own confidence model) | unchanged |
| `tessellum.dks.persistence` | unchanged | CalibratedConfidence reads WarrantHistory | unchanged | meta-DKS writes to a new MetaHistory | unchanged |
| `tessellum.dks.retrieval_client` | unchanged | DKSCycle consumes it | unchanged | unchanged | unchanged |
| `tessellum.format.validator` | adds TESS-005 | unchanged | unchanged | adds TESS-006 (every meta-edit migration note must link to the failure observation) | unchanged |
| `tessellum.composer.eval` | unchanged | calibration target = `epistemic_congruence` mean score | unchanged | meta-DKS's outputs scored against a new `schema_coherence` dim? (open) | unchanged |
| `tessellum.cli` | adds `bb audit`; extends `dks --report` | extends `dks` flags | unchanged (dispatcher refactor is internal) | adds `dks meta` | adds `--perspectives` to `dks` |

## What this plan does NOT do

Six things deliberately deferred beyond Phase 10:

- **External observation sources.** Today observations come from JSONL or session-mcp. Inbox watchers, API ingestion, webhook receivers — v0.3+ research.
- **Cross-vault federation.** Each Tessellum vault's DKS evolves independently. Federation requires a serialisation format for BB_SCHEMA + a merge discipline; not a v0.2+ priority.
- **Real-time / streaming mode.** DKS runs batch (one explicit invocation = N cycles). Streaming requires a daemon model + a back-pressure story; deferred.
- **MCP server exposing DKS to agents.** A natural integration — `tessellum dks` becomes a tool in Claude Code's MCP registry — but it's surface-level work, not core. Deferred to v0.1 polish work alongside the FZ-trail + composer skills.
- **Pluggable termination criteria.** Dialectical adequacy + Dung grounded semantics (Phase 10) are the two we ship. Pollock's defeat semantics, Caminada's labelling — research alternatives, not v0.2 priorities.
- **DKS for non-text substrates.** Today every BBNode is a markdown file. Image-grounded observations, code-grounded warrants, audio-grounded contradicts — a v0.3+ generalisation.

Recording these so the next plan author can find them.

## Sequence and rationale

The five phases are sequenced for *unlocking*, not *dependency-only*:

```
   Phase 6   ──→   Phase 9
   (TESS-005       (meta-DKS reads the same untyped-edge + edge-count
    + bb audit)     telemetry Phase 6 exposes)

   Phase 7   ──→   Phase 8
   (learned        (dispatcher refactor folds Phase 7's retrieval +
    confidence)     semantic-detect complexity into handlers cleanly)

   Phase 8   ──→   Phase 9
   (dispatcher     (meta-DKS swaps the cycle-level handler registry
    refactor)       to inject new edge types from BB_SCHEMA_USER_EXTENSIONS)

   Phase 9   ←──   (foundational; ships before Phase 10's perspective expansion
                    so meta-DKS observations include perspective-distribution signal)
```

So a strict-dependency order is: 6, 7, 8, 9, 10. Phases 6 and 7 are parallelisable; phases 8-9-10 are sequential.

| Phase | Version | LOC est. | Forcing function |
|-------|---------|----------|--------------------|
| 6 | v0.0.48 | ~300 | None — pure addition |
| 7 | v0.0.49 | ~280 | Phase 5's gate mechanism shipped; learning signal exists |
| 8 | v0.0.50 | ~330 | Phase 7 stacked complexity on two steps; refactor before adding more |
| 9 | v0.0.51 | ~600 | The biggest one. Closes Level 3 learning. R-P productive half at its strongest. |
| 10 | v0.0.52 | ~370 | Pure expansion; lands last so phases 6-9 stabilise first |

Total: ~1,880 LOC across 5 versions. Roughly 2-3 weeks at current cadence.

## How this plan was derived

Three sources, in order of weight:

1. **FZ 2a2's three learning levels**. The structure of the plan mirrors them: Phase 6 strengthens Level 1's telemetry; Phase 7 operationalises Level 2's signal; Phase 9 implements Level 3's mechanism.
2. **FZ 1b's data structure proposal**. Phase 8 implements the dispatcher form `tessellum.bb` was authored for; Phase 9's meta-DKS uses `BB_SCHEMA_USER_EXTENSIONS` as the runtime-mutable surface.
3. **The original `plan_dks_implementation.md`'s deferrals**. "Multi-agent debate beyond two arguments" → Phase 10. "Learned confidence gating" → Phase 7. Phase 9 (meta-DKS) is the resolution of R-P's productive half flagged across FZ 1a1b1, FZ 2b, and the v0.0.45 cross-validation amendment.

What's *new* (not derived from any prior plan / note):
- The TESS-005 generalisation. v0.0.47 made it possible (corpus edges have `edge_type` typing now); v0.0.44's TESS-004 made it discoverable.
- The schema-versioning discipline (`BB_SCHEMA_VERSION`, `BB_SCHEMA_USER_EXTENSIONS`, migration notes). Required by Phase 9 to land safely.
- The meta-meta-schema recursion stop. The honest answer to "meta-DKS could go infinitely meta" — the meta-meta is human-authored; recursion halts.

## Open questions — resolution status

The 8 cross-phase questions originally listed here have been resolved against best-practice design principles. The full reasoning lives in the [Resolved decisions](#resolved-decisions-8-open-questions-7-decided-1-empirical) section above; this is the status summary.

| # | Resolution | Affects | Confidence |
|--:|------------|---------|------------|
| D1 | Subclass-per-`BBType` frozen dataclasses w/ `kw_only=True` (no metadata dict) | Phase 8 | high |
| D2 | 10% default false-gate rate; configurable + `--calibrate` observable | Phase 7 | medium (value is empirical; mechanism is fixed) |
| D3 | Event-sourced schema (retractable state, append-only history) | Phase 9 | high |
| D4 | `tessellum.dks.meta.META_SCHEMA` in code, PR-gated | Phase 9 | very high |
| D5 | YAML field `argument_perspective:` (optional, open vocab) | Phase 10 | high |
| D6 | Top-level `tessellum bb` CLI group | Phase 6 | very high |
| D7 | Dung grounded internally; `closed_loop` preserved as derived property | Phase 10 | high |
| D8 | Frozen-at-creation; retroactive via `tessellum bb migrate` | Phase 9 | high |

Only **D2's value** (10% default) is empirically tunable; the mechanism is fixed. Two phase-internal questions remain low-risk and decided at phase-start (Phase 6's TESS-005 legacy strictness; Phase 7's retrieval pre-filter-vs-rerank).

### Cross-cutting consequences that simplify the implementation

Three resolutions compose into stronger guarantees than the sum:

1. **D1 + D7** — `DKSStateMachine.walk()` (Phase 8) returns a `BBPath` whose nodes are subclass-typed and whose termination uses Dung labelling. Unified type story; one walker, one termination rule.
2. **D3 + D8** — schema is event-sourced *and* note-versioned. Every corpus note carries `bb_schema_version`; every schema change is a `SchemaEditEvent`; migrations are first-class CLI operations. Meta-DKS's "edit" reduces to "emit an event" — the rest follows.
3. **D4 + D5** — meta-DKS reads two YAML fields per note (`argument_perspective` for cycle-level signal, `bb_schema_version` for migration safety) and one Python constant (`META_SCHEMA`). Three load-bearing surfaces; all visible; all type-checked.

## See Also

- [`plan_dks_implementation`](plan_dks_implementation.md) — the original 5-phase plan (v0.0.40 → v0.0.45), now fully shipped. This plan is its successor.
- [`thought_dks_evolution`](../vault/resources/analysis_thoughts/thought_dks_evolution.md) — FZ 2 — the design descent
- [`thought_dks_design_synthesis`](../vault/resources/analysis_thoughts/thought_dks_design_synthesis.md) — FZ 2a — the 7-component pattern
- [`thought_dks_fz_integration`](../vault/resources/analysis_thoughts/thought_dks_fz_integration.md) — FZ 2a1 — the FZ-duality view
- [`thought_dks_as_fsm_on_bb_graph`](../vault/resources/analysis_thoughts/thought_dks_as_fsm_on_bb_graph.md) — FZ 2a2 — the FSM formalism this plan operationalises
- [`thought_dks_runtime_integration`](../vault/resources/analysis_thoughts/thought_dks_runtime_integration.md) — FZ 2b — how the runtime integrates with composer / retrieval / format / eval
- [`thought_bb_ontology_as_typed_graph`](../vault/resources/analysis_thoughts/thought_bb_ontology_as_typed_graph.md) — FZ 1b — the BB ontology as a typed graph (the data structure side)
- [`thought_cqrs_r_cross_rules`](../vault/resources/analysis_thoughts/thought_cqrs_r_cross_rules.md) — FZ 1a1b — the three R-rules this plan completes
- [`thought_cqrs_r_cross_gap_audit`](../vault/resources/analysis_thoughts/thought_cqrs_r_cross_gap_audit.md) — FZ 1a1b1 — the gap audit (Phase 5 cross-validated; Phase 9 closes Level 3)

---

**Last Updated**: 2026-05-10 (resolutions amendment — 7 of 8 open questions decided against best-practice design principles)
**Status**: Approved — Phases 6-10 ready to execute. Phase 6 starts on this commit's heels. Ships across 5 versions as v0.0.48 → v0.0.52.
