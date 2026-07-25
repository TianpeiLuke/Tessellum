# `tessellum.dks` — Reference

API, symbols, and signatures for the Dialectic Knowledge System runtime. See [../dks.md](../dks.md) for the design narrative.

## Files

| File | Role |
|------|------|
| `dks/core.py` | The implementation: the 7 component-output dataclasses, `DKSWarrant`, `DKSCycleResult`, `DKSCycle` (the 7-step dispatcher + N>2 path), `DKSRunner` (multi-cycle warrant threading), `WarrantChange`/`DKSRunResult`, `allocate_cycle_fz`, `aggregate_warrant_changes`. |
| `dks/__init__.py` | Public API surface — re-exports everything callers should import via `from tessellum.dks import ...`. `core.py` is not the documented surface (`core.py:3-7`). |
| `dks/dung.py` | Standalone Dung abstract argumentation framework: `DungAF` + `grounded_labelling` + `grounded_extension`. Additive; N=2 collapses to the single-edge outcome. |
| `dks/confidence.py` | Confidence gate: `DKSConfidenceModel` protocol, `ConstantConfidence`, `CalibratedConfidence`, `decide_escalation`, `calibrate_from_traces`, `CalibrationResult`, and the three module defaults. |
| `dks/persistence.py` | `WarrantRegistry` (in-memory current set) + `WarrantHistory` (append-only JSONL log) + `HistoryEntry` + `load_warrants_from_vault`. |
| `dks/retrieval_client.py` | `RetrievalClient` / `RetrievalHit` — read-only P→D adapter over `tessellum.retrieval.hybrid_search`. |
| `dks/fsm.py` | `DKSStateMachine.walk` — re-expresses a cycle as a typed `BBPath` walk over `BB_SCHEMA`. Additive alternative dispatcher; delegates to `DKSCycle.run`. |
| `dks/meta/types.py` | Meta-meta-schema (`META_SCHEMA`, `META_STATES`, `MetaEdgeType`) + `MetaObservation`, `SchemaEditProposal`, `MetaCounterArgument`, the attack/threshold vocabularies. |
| `dks/meta/runtime.py` | `MetaCycle` (build→filter→survive→emit) + `HeuristicProposer`/`LLMProposer`, `NoOpAttacker`/`LLMAttacker`, `MetaCycleResult`, `DEFAULT_MIN_CYCLES`, event-log I/O. |
| `cli/dks.py` | `tessellum dks` — the 4-mode entrypoint (run / `--report` / `--calibrate` / `--meta`) + trace serialization. |

## Core (`dks/core.py`)

### Type aliases

- `ToulminComponent = Literal["premise", "warrant", "counter-example", "undercutting"]` — which Toulmin component an attack targets (`core.py:61-72`).
- `CycleMode = Literal["fresh", "extend", "branch"]` — where the cycle root lives in the FZ graph (`core.py:74-82`).
- `CounterStrength = Literal["weak", "moderate", "strong"]` (`core.py:84`).
- `WarrantChangeKind = Literal["added", "revised", "superseded"]` (`core.py:1149`).

### The seven component dataclasses

All frozen. Five are BB-node subclasses whose `bb_type` is fixed by the parent (`init=False`); `DKSWarrant`, `DKSContradicts`, and `DKSRuleRevision` are plain records.

| Dataclass | Base | Key fields |
|-----------|------|-----------|
| `DKSObservation` (step 1) | `EmpiricalObservationNode` | `summary: str`, `timestamp: str \| None` (`core.py:90-105`) |
| `DKSWarrant` | — | Toulmin 6-tuple: `claim`, `data`, `warrant`, `backing`, `qualifier`, `rebuttal` (`core.py:108-122`) |
| `DKSArgument` (step 2/3) | `ArgumentNode` | `warrant: DKSWarrant`, `evidence: str`, `perspective: str` (`core.py:124-139`) |
| `DKSContradicts` (step 4) | — | `attacker_fz`, `attacked_fz`, `reason`. No FZ node — a link (`core.py:142-154`) |
| `DKSCounterArgument` (step 5) | `CounterArgumentNode` | `attacked_fz`, `broken_component: ToulminComponent`, `counter_claim`, `reason`, `strength: CounterStrength` (`core.py:157-173`) |
| `DKSPattern` (step 6) | `ModelNode` | `description: str`, `observed: tuple[str, ...]` (`core.py:176-187`) |
| `DKSRuleRevision` (step 7) | — | `folgezettel`, `revised_warrant: DKSWarrant`, `supersedes: str \| None` (`core.py:190-201`) |

### `DKSCycleResult` (frozen dataclass, `core.py:207-363`)

Output of one cycle. Legacy scalar fields (`argument_a`, `argument_b`, `contradicts`, `counter`, `pattern`, `rule_revision`) plus multi-perspective tuples (`arguments`, `contradicts_edges`, `grounded_labelling`, `rule_revisions`) plus telemetry (`elapsed_ms`, `backend_id`, `escalation_decision`, `confidence_score`, `silent_failures`).

| Property | Returns | Meaning |
|----------|---------|---------|
| `folgezettel_nodes` | `tuple[str, ...]` | FZ positions deposited (excludes the contradicts edge). |
| `closed_loop` | `bool` | True iff `rule_revision is not None` (step 7 fired). |
| `surviving_argument_fzs` | `tuple[str, ...]` | Arguments labelled `"in"`; derived from `grounded_labelling`, else the N=2 fallback. Lex-sorted. |
| `gated` | `bool` | True iff `escalation_decision == "gated"`. |

Terminal-shape discriminator: `argument_b is None` iff the cycle was gated (2 FZ nodes: observation + A). Short-circuit-on-agreement → 3 nodes, `closed_loop=False`. Full loop → 6 nodes, `closed_loop=True`.

### `allocate_cycle_fz(existing_trails, mode="fresh", parent_fz=None) -> str`

Allocate the cycle-root FZ (`core.py:372-409`). `fresh` = next unused top-level integer; `extend`/`branch` = next letter-suffix child of `parent_fz` (mechanically identical at the allocator layer). Raises `ValueError` if `extend`/`branch` given no `parent_fz`. Internal: `_next_fresh_root`, `_next_child_of` (walks `a`..`z` then two-letter suffixes; `core.py:427-462`).

### `DKSCycle` (`core.py:475-1116`)

```python
DKSCycle(
    observation: DKSObservation,
    warrants: tuple[DKSWarrant, ...],
    backend: LLMBackend,
    *,
    confidence_model: object | None = None,
    confidence_threshold: float | None = None,   # defaults to DEFAULT_CONFIDENCE_THRESHOLD
    retrieval_client: object | None = None,
    semantic_disagreement: bool = False,
    perspectives: tuple[str, ...] = ("conservative", "exploratory"),
)
```

`run() -> DKSCycleResult`. `perspectives` must have ≥2 unique entries (`ValueError` otherwise). N>2 auto-activates `_run_n_perspective` (pairwise contradicts + Dung grounded labelling + multi-revision authoring). Per-step methods: `_step_argument`, `_step_disagreement`, `_step_counter`, `_step_pattern`, `_step_rule_revision`. Silent-failure sites: `_llm_check_disagreement`, `_format_retrieval_context`, and the JSON-parse swallow on every step (`_step_argument`, `_step_counter`, `_step_pattern`, `_step_rule_revision`).

### `DKSRunner` (`core.py:1211-1320`)

```python
DKSRunner(
    observations: tuple[DKSObservation, ...],
    backend: LLMBackend,
    *,
    initial_warrants: tuple[DKSWarrant, ...] = (),
    confidence_model=None, confidence_threshold=None,
    retrieval_client=None, semantic_disagreement=False,
    perspectives=("conservative", "exploratory"),
)
```

`run() -> DKSRunResult`. One cycle per observation; each cycle sees `initial_warrants` + every prior revision. Threads each `rule_revisions` entry into a `WarrantChange` (`added`, or `revised`+`superseded` pair).

### `DKSRunResult` (frozen, `core.py:1180-1208`)

Fields: `cycles`, `warrant_changes`, `final_warrants`, `elapsed_ms`, `backend_id`. Properties: `cycle_count`, `closed_loop_count`, `gated_count`.

### `WarrantChange` (frozen, `core.py:1162-1177`)

`cycle_id`, `kind: WarrantChangeKind`, `warrant: DKSWarrant | None`, `revision_fz: str | None`, `superseded_fz: str | None`. The `superseded` tombstone carries only the FZ (`warrant=None`).

- `aggregate_warrant_changes(changes) -> dict[str, int]` — count by kind (`core.py:1323-1330`).

## Dung AF (`dks/dung.py`)

- `DungLabel = Literal["in", "out", "undec"]` (`dung.py:38-46`).
- `DungAF` (frozen): `arguments: tuple[str, ...]`, `attacks: tuple[tuple[str, str], ...]`. Methods `attackers_of(arg_id)`, `attackees_of(arg_id)`. Attacks referencing unknown arguments are silently ignored (`dung.py:49-72`).
- `grounded_labelling(af: DungAF) -> dict[str, DungLabel]` — fixpoint iteration; unique, order-independent (`dung.py:78-129`).
- `grounded_extension(af: DungAF) -> tuple[str, ...]` — the `"in"` set, sorted (`dung.py:132-143`).

## Confidence (`dks/confidence.py`)

- `EscalationDecision = Literal["gated", "full"]` (`confidence.py:35`).
- `DEFAULT_CONFIDENCE_THRESHOLD: float = 0.85` (`confidence.py:39`).
- `DEFAULT_TARGET_FALSE_GATE_RATE: float = 0.10` (`confidence.py:115`).
- `DEFAULT_RECENCY_HALFLIFE_CYCLES: int = 50` (`confidence.py:125`).
- `DKSConfidenceModel` (Protocol): `__call__(observation, warrants: Sequence[DKSWarrant]) -> float` in `[0,1]` (`confidence.py:49-74`).
- `ConstantConfidence(score=0.0)` — fixed score; `0.0`→always full, `1.0`→always gated (`confidence.py:77-95`).
- `CalibratedConfidence(warrant_history=None, recency_halflife_cycles=50, baseline=0.5)` — recency-weighted attack-rate → `1 - attack_rate`; empty history → `baseline` (`confidence.py:161-205`).
- `decide_escalation(confidence, threshold=DEFAULT_CONFIDENCE_THRESHOLD) -> EscalationDecision` — `"gated"` iff `confidence > threshold` (strict) (`confidence.py:98-109`).
- `calibrate_from_traces(runs_dir, *, current_threshold=0.85, target_false_gate_rate=0.10) -> CalibrationResult` — replay `*_cycle_*.json`, report achieved false-gate rate, suggest a threshold (`confidence.py:240-317`).
- `CalibrationResult` (frozen): `cycles_examined`, `would_gate_count`, `false_gate_count`, `false_gate_rate`, `current_threshold`, `target_false_gate_rate`, `suggested_threshold: float | None` (`confidence.py:134-158`).

## Persistence (`dks/persistence.py`)

- `WarrantRegistry(warrants=())` — in-memory current set keyed by FZ. `add(fz, warrant)` (raises `ValueError` on duplicate FZ), `supersede(old_fz, new_fz, new_warrant)`, `snapshot() -> tuple[DKSWarrant, ...]`, `snapshot_with_fz()`, plus `__contains__`/`__iter__`/`__len__` (`persistence.py:47-123`).
- `HistoryEntry` (frozen): `timestamp: str`, `change: WarrantChange` (`persistence.py:129-140`).
- `WarrantHistory(path)` — append-only JSONL log. `record_change(change) -> HistoryEntry`, `record_changes(changes)`, `all() -> list[HistoryEntry]` (tolerant of malformed lines), `tail(n=10)`. Default path `runs/dks/warrant_history.jsonl` (`persistence.py:143-198`).
- `load_warrants_from_vault(vault_path) -> WarrantRegistry` — picks up `procedure_*`/`concept_*` notes with `building_block ∈ {procedure, concept}`, `"dks"` in `tags`, and a non-empty `folgezettel`. Never raises on a bad note (`persistence.py:253-312`).

## Retrieval client (`dks/retrieval_client.py`)

- `RetrievalHit` (frozen): `note_id`, `note_name`, `score: float`, `bm25_rank: int | None`, `dense_rank: int | None` (`retrieval_client.py:34-48`).
- `RetrievalClient(db_path)` — read-only; raises `FileNotFoundError` if the DB is absent. `search(query, *, k=20) -> list[RetrievalHit]` (RRF hybrid; lazily imports `tessellum.retrieval.hybrid_search`). No `index`/`update`/`delete` (`retrieval_client.py:50-115`).

## FSM (`dks/fsm.py`)

- `BBPathStep` (frozen): `edge: EpistemicEdgeType | None`, `node: object` (`fsm.py:48-59`).
- `BBPath` (frozen): `steps: tuple[BBPathStep, ...]`, `terminal_state: BBType`, `elapsed_ms`. Properties `transition_count`, `nodes` (`fsm.py:61-87`).
- `TransitionHandler` (Protocol): `__call__(context: dict, edge: EpistemicEdgeType) -> object` (`fsm.py:92-106`).
- `DKSStateMachine` — construction mirrors `DKSCycle` plus `handlers: dict[tuple[BBType, BBType], TransitionHandler]`. `walk(observation, warrants=()) -> BBPath` delegates to `DKSCycle.run`; `last_result` exposes the `DKSCycleResult`. Step 4 is not a `BBPathStep`. Terminal state is `PROCEDURE` when a revision fired, else `ARGUMENT` (the `CONCEPT` variant is deferred) (`fsm.py:112-246`).

## Meta-DKS types (`dks/meta/types.py`)

- `META_STATES` (5), `MetaEdgeType(source, target, label)`, `META_SCHEMA` (4 transitions; not event-sourced, PR-gated) (`types.py:26-52`).
- `MetaObservation` (frozen): `timestamp`, `cycles_examined`, `top_attacked_warrants: tuple[tuple[str, int], ...]`, `toulmin_failure_counts: dict[str, int]`, `unrealised_schema_edges: tuple[EpistemicEdgeType, ...]`, `counter_strength_breakdown`, `sample_counter_quotes`, `observation_source_metadata`, `silent_failure_count`, `per_perspective_breakdown` (`types.py:58-131`).
- `SCHEMA_EDIT_PROPOSAL_KIND = Literal["add", "retract", "refine"]` (`types.py:137`).
- `SchemaEditProposal` (frozen): `kind`, `edge: EpistemicEdgeType`, `motivating_observation`, `expected_impact`, `supersedes: EpistemicEdgeType | None` (`types.py:140-158`).
- `META_ATTACK_KIND = Literal["insufficient_evidence", "input_bias", "overgeneralisation", "collides_with_existing", "weak_signal"]` (`types.py:164-176`).
- `MetaCounterArgument` (frozen): `attacked_proposal_index: int`, `attack_kind: META_ATTACK_KIND`, `reason: str`, `strength` (`types.py:183-199`).
- `SURVIVE_THRESHOLD = Literal["strict", "majority", "permissive"]` — `strict`=0 attacks; `majority`=≤1 strong AND ≤2 moderate; `permissive`=no strong (`types.py:205-213`).

## Meta-DKS runtime (`dks/meta/runtime.py`)

- `DEFAULT_MIN_CYCLES: int = 20` — cold-start guard (`runtime.py:51-56`).
- `Proposer` (Protocol): `generate(observation, target_failure=None) -> list[SchemaEditProposal]` (`runtime.py:68-84`).
- `HeuristicProposer` — Toulmin-dominance (>50%, via `_TOULMIN_TO_PROPOSED_EDGE`) + unrealised-edge retraction (≥50 cycles). `undercutting` maps to no edge (`runtime.py:87-139`, `719-742`).
- `LLMProposer(backend, max_tokens=2000)` — LLM-backed; malformed JSON → `[]`; unknown BBType strings skipped. Captures `input_bias_risk` as a `motivating_observation` prefix (no dedicated field) (`runtime.py:186-300`).
- `Attacker` (Protocol): `attack(proposals, observation) -> list[MetaCounterArgument]` (`runtime.py:314-334`).
- `NoOpAttacker` — returns `[]` (default). `LLMAttacker(backend, max_tokens=2000)` — dialectical attack; dedups by `(index, kind)` (`runtime.py:336-506`).
- `MetaCycleResult` (frozen): `observation`, `proposals`, `surviving`, `events_landed`, `elapsed_ms`, `dry_run`, `attacks`, `survive_threshold` (`runtime.py:533-556`).
- `MetaCycle(observation, min_cycles=20, target_failure=None, dry_run=True, proposer=HeuristicProposer(), attacker=NoOpAttacker(), survive_threshold="majority")` — `run() -> MetaCycleResult`. Below `min_cycles` → empty result. Filter drops duplicates, already-existing `BB_SCHEMA` edges, and retractions of edges absent from `BB_SCHEMA` (retracting a core/DKS-extension edge that IS in `BB_SCHEMA` is allowed). Events emitted only when `dry_run=False` (`runtime.py:562-713`).
- `load_event_log(path) -> tuple[SchemaEditEvent, ...]`; `write_event_log(path, events, *, append=True)` (`runtime.py:775-810`).

## Import surface (`tessellum.dks`)

Re-exported from `__init__.py:36-201`:

- **Core cycle:** `DKSCycle`, `DKSRunner`, `allocate_cycle_fz`, `aggregate_warrant_changes`, the 7 component dataclasses, `DKSWarrant`, `DKSCycleResult`, `WarrantChange`, `DKSRunResult`, and the 4 type aliases.
- **Dung AF:** `DungAF`, `DungLabel`, `grounded_extension`, `grounded_labelling`.
- **Confidence:** `DEFAULT_CONFIDENCE_THRESHOLD`, `DEFAULT_TARGET_FALSE_GATE_RATE`, `DEFAULT_RECENCY_HALFLIFE_CYCLES`, `DKSConfidenceModel`, `ConstantConfidence`, `CalibratedConfidence`, `EscalationDecision`, `CalibrationResult`, `decide_escalation`, `calibrate_from_traces`.
- **Persistence:** `WarrantRegistry`, `WarrantHistory`, `HistoryEntry`, `load_warrants_from_vault`.
- **P-side retrieval:** `RetrievalClient`, `RetrievalHit`.
- **FSM:** `BBPath`, `BBPathStep`, `DKSStateMachine`, `TransitionHandler`.
- **Meta-DKS:** `DEFAULT_MIN_CYCLES`, `META_SCHEMA`, `MetaEdgeType`, `MetaObservation`, `SchemaEditProposal`, `SCHEMA_EDIT_PROPOSAL_KIND`, `MetaCounterArgument`, `META_ATTACK_KIND`, `SURVIVE_THRESHOLD`, `MetaCycle`, `MetaCycleResult`, `Proposer`, `HeuristicProposer`, `LLMProposer`, `Attacker`, `NoOpAttacker`, `LLMAttacker`, `load_event_log`, `write_event_log`.

## CLI (`cli/dks.py`)

`tessellum dks` is one of Tessellum's 12 CLI commands, with four mutually-short-circuiting modes (`run_dks_cli`, `cli/dks.py:267-278`, checked in order: `--report` → `--calibrate` → `--meta` → run). Exit codes: `0` success (zero cycles allowed), `2` invocation error.

### Run (default)

`tessellum dks <observations.jsonl>`. JSONL, one observation per line; required string `summary`, optional `timestamp`/`mode`/`parent_fz`. Writes `<UTC-ts>_cycle_<FZ>.json` per cycle + `<UTC-ts>_aggregate.json`, appends `warrant_history.jsonl`, under `--runs-dir` unless `--no-trace`.

### `--report`

Inter-cycle telemetry across past `*_aggregate.json` (closed/gated rates, warrant-change totals, top-attacked warrant FZs). With `--report-last N`, only the most recent N runs; with `--include-bb-graph` (+ `--bb-db`), joins `BBGraph.from_db()` corpus counts.

### `--calibrate`

Replays per-cycle `confidence_score`/`closed_loop`, reports the achieved false-gate rate at `--gate-threshold` (default 0.85), suggests a threshold hitting `--target-false-gate-rate` (default 0.10).

### `--meta` (+ `--apply` to write)

Builds a `MetaObservation` from traces, runs `MetaCycle`, prints proposals; `--apply` writes surviving `SchemaEditEvent`s to `runs/dks/meta/schema_events.jsonl` + a migration note.

### Flag table

| Flag | Default | Applies to | Meaning |
|------|---------|-----------|---------|
| `observations` | — | run | JSONL path (optional with `--report`/`--calibrate`/`--meta`). |
| `--report` | off | mode | Inter-cycle telemetry; skips the run. |
| `--report-last N` | all | report | Most recent N runs by mtime. |
| `--include-bb-graph` | off | report | Join corpus BBGraph telemetry. |
| `--bb-db PATH` | `data/tessellum.db` | report/meta | Index DB for BBGraph (report join; meta `unrealised_schema_edges`). |
| `--calibrate` | off | mode | Threshold-calibration replay; skips the run. |
| `--target-false-gate-rate F` | `0.10` | calibrate | Target false-gate rate. |
| `--confidence-model {constant,calibrated}` | `constant` | run | `constant`→`ConstantConfidence(--gate-confidence)`; `calibrated`→`CalibratedConfidence` reading `warrant_history.jsonl`. |
| `--gate-confidence F` | none | run | Constant confidence score in `[0,1]`; gates when `> --gate-threshold`. |
| `--gate-threshold F` | `0.85` | run/calibrate | Override the gate threshold. |
| `--retrieval-db PATH` | none | run | Build a `RetrievalClient`; adds a substrate block to argument prompts. |
| `--perspectives a,b,...` | `conservative,exploratory` | run | Comma-separated, ≥2 unique. N>2 activates pairwise contradicts + Dung. |
| `--semantic-disagreement` | off | run | One LLM call at step 4 instead of string-compare. |
| `--meta` | off | mode | Schema-mutation runtime; skips the run. |
| `--apply` | off | meta | Write surviving events (else dry-run). |
| `--min-cycles N` | `20` | meta | Cold-start guard. |
| `--target-failure {premise,warrant,counter-example,undercutting}` | all | meta | Filter proposals to one Toulmin component. |
| `--proposer {heuristic,llm}` | `heuristic` | meta | Proposal strategy. |
| `--attacker {none,llm}` | `none` | meta | Attack stage. |
| `--survive-threshold {strict,majority,permissive}` | `majority` | meta | Survival policy (`--attacker llm` only). |
| `--initial-warrants PATH` | none | run | JSON list of starting warrants. |
| `--backend {mock,anthropic}` | `mock` | run/meta | `anthropic` needs `[agent]` extras + `ANTHROPIC_API_KEY`. |
| `--model ID` | `claude-sonnet-4-6` | run/meta | Anthropic model ID. |
| `--mock-responses PATH` | none | run/meta | Prompt-substring → canned response (MockBackend). |
| `--runs-dir DIR` | `runs/dks` | all | Trace output directory. |
| `--no-trace` | off | run | Skip writing trace files. |
| `--format {human,json}` | `human` | all | Output format. |

### Observation JSONL fields

| Field | Required | Meaning |
|-------|----------|---------|
| `summary` | yes (string) | The observation text. |
| `timestamp` | no | Free-form timestamp carried onto the observation node. |
| `mode` | no (`"fresh"`) | `fresh` / `extend` / `branch`. |
| `parent_fz` | for `extend`/`branch` | FZ the cycle descends from / branches off. |
