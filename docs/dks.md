# DKS — Dialectic Knowledge System runtime

## 1. Purpose

`src/tessellum/dks/` is the closed-loop dialectic engine that turns Tessellum's typed atomic-note substrate into a *learning* knowledge system: each observation is argued from N perspectives, disagreements are detected as `contradicts` edges, a counter-argument names the broken Toulmin component, a pattern is discovered, and one or more revised warrants close the loop — every component deposited as a typed Building-Block (BB) node on the Folgezettel graph. It is a peer runtime to Composer/retrieval/indexer (`dks/__init__.py:16-19` — "Built on Composer primitives; not owned by it"), sharing only Composer's `LLMBackend` abstraction (`core.py:57`).

## 2. Architecture / data flow

One cycle (`DKSCycle.run`, `core.py:557-684`) is a fixed 7-component pipeline over an `LLMBackend`:

```
observation                    (step 1, cycle root FZ)
   -> argument A               (step 2, FZ N.a)          perspective[0]
   -> argument B               (step 3, FZ N.b)          perspective[1]
   -> contradicts edge         (step 4, no FZ — a link, not a node)
   -> counter-argument         (step 5, FZ <attacked>.a) names broken Toulmin component
   -> pattern / model          (step 6, FZ <counter>.a)
   -> revised warrant(s)       (step 7, FZ <pattern>.a leaf)  -> procedure/concept note
```

The step->BB->FZ mapping table is inlined at `core.py:30-40`. Steps 2/3/5/6/7 are LLM round-trips; step 4 is local (`_step_disagreement`, `core.py:886`) unless `--semantic-disagreement` adds an LLM check. Warrants thread across cycles: `DKSRunner` (`core.py:1211-1320`) feeds each cycle the current set (`initial_warrants` + every prior revision) and emits a chronological `WarrantChange` diff.

The recursion has a second floor: **meta-DKS** (`dks/meta/`) runs the *same* dialectic shape one level up, over the schema itself — reading cycle telemetry, proposing schema edits, attacking them, and landing survivors as `SchemaEditEvent`s into `BB_SCHEMA_USER_EXTENSIONS`.

Persistence is out-of-band: DKS classes produce JSON-line records; the CLI writes them to `runs/dks/`. Neither the registry nor the history mutates the vault substrate — the warrant *files* are materialised separately by the DKS Composer skill's step-7 (`persistence.py:20-23`).

## 3. Key modules + abstractions

| File | Role |
|------|------|
| `core.py` | The implementation. 7 component-output dataclasses, `DKSCycle` (the 7-step dispatcher + N>2 path), `DKSRunner` (multi-cycle warrant threading), `allocate_cycle_fz` (fresh/extend/branch FZ allocator), `DKSCycleResult`/`DKSRunResult`. |
| `__init__.py` | Public API surface — re-exports everything callers should import (`from tessellum.dks import ...`); `core.py` itself is not the documented surface (`core.py:5-7`). |
| `dung.py` | Standalone Dung Abstract Argumentation Framework: `DungAF` (frozen `(arguments, attacks)`) + `grounded_labelling` (fixpoint in/out/undec) + `grounded_extension`. Additive; N=2 collapses to the single-edge outcome (`dung.py:22-26`). |
| `confidence.py` | Confidence gate: `DKSConfidenceModel` protocol, `ConstantConfidence`, `CalibratedConfidence` (recency-weighted attack rate), `decide_escalation`, `calibrate_from_traces`, `DEFAULT_CONFIDENCE_THRESHOLD=0.85`. |
| `persistence.py` | `WarrantRegistry` (in-memory current set, add/supersede/snapshot) + `WarrantHistory` (append-only JSONL log) + `load_warrants_from_vault` (reads `dks`-tagged `procedure_*`/`concept_*` notes). |
| `retrieval_client.py` | `RetrievalClient` — read-only P->D adapter over `tessellum.retrieval.hybrid_search`; the productive half of R-Cross. |
| `fsm.py` | `DKSStateMachine.walk` — re-expresses a cycle as a typed `BBPath` walk over `BB_SCHEMA`; additive alternative dispatcher, does not change `DKSCycle`. |
| `meta/types.py` | Meta-meta-schema (`META_SCHEMA`, 5 states + 4 edges, PR-gated) + `MetaObservation`, `SchemaEditProposal`, `MetaCounterArgument`, the 5-kind attack vocabulary, `SURVIVE_THRESHOLD`. |
| `meta/runtime.py` | `MetaCycle` (build->filter->survive->emit) + `HeuristicProposer`/`LLMProposer`, `NoOpAttacker`/`LLMAttacker`, survival aggregation, event-log I/O. |
| `cli/dks.py` | `tessellum dks` — the 4-mode entrypoint (run / `--report` / `--calibrate` / `--meta`) + trace serialisation. |

### The seven component dataclasses (`core.py:90-202`)

Five are BB-node subclasses, so `bb_type` is fixed by the parent (`init=False`): `DKSObservation(EmpiricalObservationNode)`, `DKSArgument(ArgumentNode)`, `DKSCounterArgument(CounterArgumentNode)`, `DKSPattern(ModelNode)`. `DKSWarrant` is a plain Toulmin 6-tuple (claim/data/warrant/backing/qualifier/rebuttal). `DKSContradicts` and `DKSRuleRevision` are relation/output records. `DKSContradicts` deliberately has no FZ — "it's a relation, not a node" (`core.py:148-150`).

## 4. Invariants / design decisions + WHY

**Three terminal shapes, disambiguated by `argument_b`.** `DKSCycleResult` (`core.py:207-227`) is one of: (1) **full closed loop** — all 7 components, 6 FZ nodes, `closed_loop=True`; (2) **short-circuit on agreement** — A and B agree so step 4 returns `None`, 3 FZ nodes, `closed_loop=False` (`core.py:634-653`); (3) **confidence-gated** — the gate fired before any A/B comparison, only observation + A, 2 FZ nodes, `argument_b is None` (`core.py:589-609`). `argument_b is None` iff gated is the load-bearing discriminator (`core.py:222-226`, property `gated` at `core.py:360`). WHY: the gated path saves 6 of 7 backend round-trips (`core.py:563-564`), so cheap-vs-rich must be a first-class, observable distinction.

**Gating is opt-in and strictly-greater.** No `confidence_model` -> every cycle runs full (`core.py:490-492`). `decide_escalation` returns `gated` only when `confidence > threshold` (`confidence.py:98-109`) — equality falls through to full, a deliberate safety bias. `DEFAULT_CONFIDENCE_THRESHOLD=0.85` (`confidence.py:39`). WHY: high enough that easy cases skip, low enough that contested cases get the full treatment; tunable from telemetry via `--calibrate`.

**N=2 default keeps the single-edge logic; N>2 dispatches to Dung.** For 2 perspectives the legacy path runs and hard-codes the labelling `{A:"out", B:"in"}` (`core.py:678-681`) — B (exploratory) attacks A (conservative) by convention. For `len(perspectives) > 2`, `_run_n_perspective` (`core.py:690-837`) emits a `contradicts` edge for every claim-differing pair, builds a `DungAF`, and computes `grounded_labelling`. **Surviving warrants = the grounded extension** (arguments labelled `"in"`; `core.py:328-358`). WHY: multi-attack survival needs a principled, deterministic, always-defined answer — grounded semantics is the minimal complete extension, unique regardless of enumeration order (`dung.py:18-26`). `undec` is treated as "not surviving" for adequacy termination (`dung.py:44-46`).

**Multi-revision authoring on multiple survivors.** When grounded labelling yields >1 `"in"` argument, step 7 emits one `DKSRuleRevision` per survivor, each anchored as a child of *its own* survivor FZ (not the pattern FZ) via an independent LLM call (`core.py:797-816`, `_step_rule_revision` `surviving_argument` branch at `core.py:1037-1052`). WHY: distinct surviving warrants should yield distinct revisions. The legacy `rule_revision` field is preserved as `rule_revisions[0]` (`core.py:262-273`).

**FZ allocation: fresh/extend/branch.** `allocate_cycle_fz` (`core.py:372-409`) allocates the cycle root: `fresh` = next unused top-level integer; `extend`/`branch` = next letter-suffix child of `parent_fz`. Extend and branch are mechanically identical at the allocator layer; the distinction is semantic (`core.py:74-82`, `385-388`). Within a cycle, children are allocated by `_next_child_of` walking the alphabet, falling back to two-letter suffixes (`core.py:427-462`). WHY: each cycle deposits a self-consistent FZ subtree matching Tessellum's existing trail conventions.

**Silent-failure observability.** Three backend-call sites fall back gracefully rather than crash: the semantic-disagreement check, retrieval-context formatting, and argument JSON parse (`core.py:286-294`). Each appends a one-line record to `DKSCycleResult.silent_failures` (`core.py:275-294`) *before* falling back — semantics unchanged, but the silence is now countable (surfaced to meta-DKS via `MetaObservation.silent_failure_count`). WHY: a backend silently failing every other call produces misleading Toulmin distributions; the meta-proposer must be able to discount degraded runs.

**R-Cross: P calls D, D never calls P.** `RetrievalClient` (`retrieval_client.py:50-115`) exposes only `search()` — no `index`/`update`/`delete`, and the underlying module has no mutating ops. Constructed against the index DB path (raises `FileNotFoundError` if absent). Retrieval is an *optional* dependency imported lazily inside `search()` (`retrieval_client.py:99-103`); the core cycle works without it, and retrieval hits only *augment* the argument prompt — they never replace warrants (`core.py:846-852`).

**Meta-schema is human-authored, PR-gated — the recursion stops one level up.** `META_SCHEMA` (5 states, 4 transitions; `meta/types.py:26-52`) is *not* event-sourced: "the recursion has to stop somewhere or we have an infinite tower of meta-meta-meta-schemas" (`meta/types.py:8-12`). Meta-DKS edits `BB_SCHEMA` (the ~16-edge typed schema: 8 epistemic + 7 navigation + 1+ DKS extensions, versioned + event-sourced via `BB_SCHEMA_USER_EXTENSIONS`); nothing edits `META_SCHEMA` automatically (`meta/__init__.py:11-14`). Schema edits do not retroactively invalidate corpus notes — frozen-at-creation discipline, each note carries `bb_schema_version` (`meta/__init__.py:34-39`).

**Meta-cycle: build -> filter -> survive -> emit, defaulting to dry-run.** `MetaCycle.run` (`meta/runtime.py:594-626`) has a cold-start guard — no proposals below `min_cycles` (`DEFAULT_MIN_CYCLES=20`, `meta/runtime.py:51-56`), because a Toulmin distribution needs ~20 cycles to be meaningful. Filter drops duplicates, already-existing edges, and non-`USER_EXTENSIONS` retractions (`meta/runtime.py:660-692`). Survival: `NoOpAttacker` (default) -> every well-formed proposal survives; `LLMAttacker` -> the `survive_threshold` decides (`strict` = zero attacks / `majority` = <=1 strong AND <=2 moderate / `permissive` = no strong; `meta/runtime.py:512-527`, `types.py:205-213`). Events land only when `dry_run=False` (i.e. `--apply`; `meta/runtime.py:613-615`). WHY: schema self-editing is high-stakes, so it is dialectical, evidence-gated, and write-guarded by default.

**FSM is additive.** `DKSStateMachine.walk` (`fsm.py:144-170`) delegates to `DKSCycle.run` and lifts the result into a typed `BBPath`; step 4 does not appear as a `BBPathStep` since it's an edge annotation, not a transition (`fsm.py:188-193`). It exists for handler-injection and meta/multi-perspective extension, not to replace the hand-coded cycle (`fsm.py:14-27`). Note (unwired): `_terminal_state_from_result` maps every revision to `PROCEDURE` today; the `CONCEPT` variant is deferred until `DKSRuleRevision` exposes its target BB type (`fsm.py:222-246`).

## 5. Public API / CLI

**Python API** (import from `tessellum.dks`, listed in `__init__.py:126-201`): `DKSCycle`, `DKSRunner`, `allocate_cycle_fz`, the 7 component dataclasses + `DKSCycleResult`/`DKSRunResult`; `DungAF`/`grounded_labelling`/`grounded_extension`; confidence gate (`ConstantConfidence`/`CalibratedConfidence`/`decide_escalation`/`calibrate_from_traces`); persistence (`WarrantRegistry`/`WarrantHistory`/`load_warrants_from_vault`); FSM (`DKSStateMachine`/`BBPath`); meta (`MetaCycle`/`HeuristicProposer`/`LLMProposer`/`NoOpAttacker`/`LLMAttacker`/`load_event_log`/`write_event_log`).

**CLI** — `tessellum dks` (`cli/dks.py`), one of Tessellum's 11 commands, with four mutually-short-circuiting modes (`run_dks_cli`, `cli/dks.py:267-278`):

- **Run** (default): `tessellum dks <observations.jsonl>`. JSONL, one observation per line, required `summary`, optional `timestamp`/`mode`/`parent_fz` (`cli/dks.py:16-19`). Writes `<ts>_cycle_<FZ>.json` per cycle + `<ts>_aggregate.json`, and appends `warrant_history.jsonl`, under `--runs-dir` (default `./runs/dks/`) unless `--no-trace`.
- **`--report`**: inter-cycle telemetry across past `*_aggregate.json` (closed/gated rates, top-attacked warrant FZs); `--report-last N`, `--include-bb-graph` (+ `--bb-db`) joins corpus BBGraph counts.
- **`--calibrate`**: replays per-cycle `confidence_score`/`closed_loop`, reports achieved false-gate rate at `--gate-threshold`, suggests a threshold hitting `--target-false-gate-rate` (default 0.10).
- **`--meta`** (+ `--apply` to write): builds a `MetaObservation` from traces, runs `MetaCycle`; knobs `--min-cycles`, `--target-failure`, `--proposer {heuristic,llm}`, `--attacker {none,llm}`, `--survive-threshold {strict,majority,permissive}`.

Shared flags: `--backend {mock,anthropic}` (default `mock`, no network; `anthropic` needs `[agent]` extras + `ANTHROPIC_API_KEY`), `--model`, `--mock-responses`, `--initial-warrants`, `--confidence-model {constant,calibrated}`, `--gate-confidence`, `--gate-threshold`, `--retrieval-db`, `--perspectives`, `--semantic-disagreement`, `--format {human,json}`. Backends: DKS shares the Composer `LLMBackend` — Mock is the default; Anthropic is opt-in. Exit codes: `0` success (zero cycles allowed), `2` invocation error (`cli/dks.py:24-27`).

## 6. Extension points

- **Confidence signal**: implement the `DKSConfidenceModel` protocol (`__call__(observation, warrants) -> float`, `confidence.py:49-74`). The gating *mechanism* (`decide_escalation`) is separate from the *signal*; `CalibratedConfidence` documents a retrieval-similarity future extension as out-of-scope (`confidence.py:170-176`).
- **Perspectives**: pass `perspectives=(...)` to `DKSCycle`/`DKSRunner` (must be >=2 and unique, `core.py:526-533`) or `--perspectives a,b,c`; N>2 auto-activates the pairwise-contradicts + Dung path.
- **Meta proposer/attacker strategies**: implement the `Proposer.generate` / `Attacker.attack` protocols (`meta/runtime.py:68-84`, `314-334`) and pass into `MetaCycle`. The heuristic Toulmin->edge lookup table (`_TOULMIN_TO_PROPOSED_EDGE`, `meta/runtime.py:719-742`) is the extension seam for new dominance rules; `undercutting` intentionally maps to no edge (LLMProposer reasons about it directly).
- **FSM transition handlers**: `DKSStateMachine.handlers` is a `{(BBType, BBType): TransitionHandler}` registry (`fsm.py:141`) for overriding one BB edge without touching cycle code.
- **Warrant sourcing**: `load_warrants_from_vault` (`persistence.py:253-312`) picks up exactly `dks`-tagged `procedure_*`/`concept_*` notes; `WarrantRegistry.add/supersede` is the book-keeping seam (learned warrant-quality scoring is explicitly out of scope, `persistence.py:57-60`).

### Deferred / unwired (stated honestly)

- FSM terminal state is always `PROCEDURE`; the `CONCEPT` terminal is deferred (`fsm.py:222-246`).
- `LLMProposer` captures `input_bias_risk` as a `motivating_observation` prefix — `SchemaEditProposal` has no dedicated field yet (`meta/runtime.py:191-197`, `287-294`).
- `WarrantHistory`/`WarrantRegistry` never write vault files; materialising warrant notes is the DKS Composer skill's job (`persistence.py:20-23`).
- `DKSContradicts` deposits no FZ node — it is materialised as a link only.
