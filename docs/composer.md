# Composer

## Purpose

Composer compiles a prose skill canonical + its `.pipeline.yaml` sidecar into a typed, contract-checked DAG (`CompiledPipeline`) with zero LLM calls, then executes that DAG against a set of leaves through a pluggable LLM backend, materializing each step's response into the vault (System P). It ships two run entry points — a serial reference path (`run_pipeline`) that is the byte-identical default, and an opt-in v4 dynamic path (`run_pipeline_dynamic`) that adds self-claiming parallelism, resume manifests, gates, fix loops, budgets, and credential pooling — every one of which is gated behind a non-`None` argument so the default stays at serial parity (IDENT-4).

## Architecture / data flow

```
skill_*.md (canonical, prose SOP + section anchors)
   +  skill_*.pipeline.yaml (sidecar: per-step declarations)
        │
        │  loader.load_pipeline  →  Pipeline (Pydantic, 2-stage validated)
        ▼
   compiler.compile_skill  (ZERO LLM)
        │  · resolve + validate materializer contracts
        │  · check expected_output_schema.required ⊇ required_output_fields
        │  · topo-sort by depends_on; reject cycles + forward refs
        │  · extract each step's prompt-section text from the canonical
        │  · context-budget estimate (warn @70%, error over hard cap)
        ▼
   CompiledPipeline (steps in topological order)
        │
        ├── run_pipeline           (serial reference; IDENT-4 default)
        └── run_pipeline_dynamic   (v4; opt-in machinery behind non-None args)
                │
                │  per (step × leaf):
                ▼
   executor.execute_step_with_retry
        │  resolve {{leaf.X}}/{{upstream.Y}}/{{retry.X}}  →  LLMRequest
        │  watchdog(120s) → backend.call → schema-validate → materialize
        ▼
   materializer.materialize  →  writes note file(s) under vault_root
        │
        ▼   (dynamic path only, all opt-in)
   close_gate → fix loop → wave_gate → manifest.save → statistics.json / trace
```

The canonical is the single prose source; the sidecar lifts the machine-readable per-step declarations (`role`, `aggregation`, `materializer`, `depends_on`, `expected_output_schema`, …) out of it. `section_id` is the join key: each sidecar step must have a matching `<!-- :: section_id = X :: -->` anchor in the canonical (`loader.load_pipeline` Stage 3 rejects orphans). The compiler produces a typed object; the scheduler drives it; the executor is the unit operation the scheduler iterates; the materializer is the only sanctioned filesystem side-effect channel.

## Key modules + abstractions

| File | Role |
|---|---|
| `loader.py` | Resolves the canonical's `pipeline_metadata:` field, reads the sidecar YAML, and validates it in three stages: (1) jsonschema against `schemas/pipeline.schema.json`, (2) Pydantic V2 model construction (`Pipeline`/`PipelineStep`/`MCPDependency`/`Query`), (3) cross-file `section_id`↔anchor consistency. Returns `Pipeline` or `None` (`pipeline_metadata: none`). |
| `compiler.py` | `compile_skill` — the zero-LLM compile: `_topological_sort` (cycle + forward-ref + duplicate-id detection), `_compile_step` (contract resolution + `required_output_fields` check + prompt-section extraction), `_validate_context_budgets`. Emits `CompiledPipeline`/`CompiledStep`; `to_dag_json` serializes it. |
| `contracts.py` | The three typed contract families as frozen Pydantic models + registries: `MaterializerContract` (5 concrete subclasses in `MATERIALIZER_CONTRACTS`), `LLMBackendContract` (`BACKEND_CONTRACTS`), `MCPContract` (`MCP_CONTRACTS`, ships `session-mcp`). `ContractViolation` exception with typed `KIND_*` tags. |
| `materializer.py` | `materialize` dispatch → 5 concrete materializers (`no_op`, `body_markdown_to_file`, `body_markdown_frontmatter_to_file`, `edits_apply_to_files`, `edits_apply_xml_tags`), one per contract. Parses the wire format, writes/applies files under `vault_root`, returns `MaterializedOutput`. |
| `llm.py` | `LLMBackend` protocol + `LLMRequest`/`LLMResponse`. Four backends: `MockBackend`, `AnthropicBackend`, `BedrockBackend`, `PooledBackend`. |
| `executor.py` | `execute_step` (resolve → watchdog dispatch → schema-validate → materialize) and `execute_step_with_retry` (separate logic/crash budgets, same-error short-circuit, opt-in backoff). `classify_error` → `ErrorClass`; `full_jitter_backoff`. |
| `scheduler.py` | `run_pipeline` (serial) + `run_pipeline_dynamic` (self-claiming parallel). Pure `compute_ready_set` core + `ReadySetState`/`SkipReason`. Typed outcome union `StepOutcome` + `classify_outcome`. Trace/statistics writers; wave-gate + close-gate drivers. |
| `manifest.py` | `Manifest` — durable, atomically-written, rebuildable resume projection. 4-state lifecycle, CAS `claim`, `mark_done`-before-release, `rebuild_from_vault`, `.bak` rotation. |
| `gates.py` | The one `Gate` abstraction at three scopes (plan/session/wave). `GateSuite` composition, `build_close_gate` (format + grounding), `build_wave_gate` (dedup), `GroundingVerdict`. Reuses `tessellum.format.validate`. |
| `fix.py` | `run_fix_loop` — checkpoint-before-fix + revert-to-BEST close-gate repair; `FixContext` (informed); `make_llm_fixer`. |
| `credential_pool.py` | `CredentialPool` (least-used lease, error-class rotation, differentiated cooldowns) + `RunBudget` (atomic `try_spend`) + per-stage `EffortLevel`. `classify_rotation_cause`. |
| `context_assembler.py` | Swappable input-side `ContextAssembler` ABC (`full_source`/`windowed`), percentage-scaled fail-soft bounds, read-path hardening (`is_safe_read_path`). |
| `planning.py` | `$0` change-detection pre-gate (`content_fingerprint`, `partition_unchanged_leaves`) + selective depth (`classify_planning_depth`). |
| `signoff.py` | `run_sign_off` — the plan→execute approver ladder: program gate → agent judge → human. |
| `skill_tool.py` | `SkillTool` projection + `CapabilityRegistry` two-tier router ("skills as tools"). |
| `batch.py` | `run_batch` — many `(skill, leaves)` jobs in parallel with file-based resume (over the *serial* `run_pipeline`). |
| `eval.py` | Scenario framework: structural assertions + `LLMJudge` 6-dim rubric. |

### Compile: canonical + sidecar → `CompiledPipeline`

`compile_skill` (`compiler.py:183`) is pure logic — no LLM. `load_pipeline` returns the validated `Pipeline`, or `None` for `pipeline_metadata: none` (in which case an empty `CompiledPipeline` is returned). Then, per step:

- **Materializer contract validation** (`_compile_step`, `compiler.py:392`). A step's `materializer` key must resolve in `MATERIALIZER_CONTRACTS`; an unknown key raises `ContractViolation(KIND_UNKNOWN_MATERIALIZER)`. For `CORE`/`DEFERRED` steps, the step's `expected_output_schema.required` must be a superset of the contract's `required_output_fields`; a gap raises `ContractViolation(KIND_MISSING_REQUIRED_OUTPUT_FIELD)`. `INFRA`'s `no_op` contract has empty required fields, so the check is skipped.
- **Topological sort + DAG hygiene** (`_topological_sort`, `compiler.py:325`). Validates every `depends_on` target exists, rejects **forward references** (a dep must appear *earlier* in the pipeline list — author-confusion guard), and runs DFS cycle detection (`on_stack` recursion set). Duplicate `section_id`s are surfaced explicitly. The sidecar list is already in dependency order once forward refs are banned, so it is returned as-is.
- **Prompt-section extraction.** `load_skill_section(skill_path, section_id)` pulls the step's body text out of the canonical; a miss becomes `CompilerError`.
- **Context-budget validation** (`_validate_context_budgets`, `compiler.py:232`). Estimates each step's rendered prompt size as `sum(upstream soft caps) + len(prompt_section_text)`, using each producer's `expected_output_schema.max_chars` (default `DEFAULT_PER_UPSTREAM_SOFT_CAP_CHARS = 25_000`). Over the per-step hard cap (`max_prompt_chars` or `HARD_PROMPT_CAP_CHARS = 150_000`) → `CompilerError`; over `WARN_AT_PROMPT_FRACTION = 0.7` → a non-fatal `budget_warnings` entry.

`ContractViolation` (contract drift) and `CompilerError` (DAG/extraction errors) are distinct so callers can `except (CompilerError, ContractViolation)` to catch all compile-time failures.

### The two run entry points

**`run_pipeline` (serial reference, `scheduler.py:86`).** Iterates `pipeline.steps` in topological order, skipping `INFRA` steps. Per step it runs one leaf at a time (`scope_leaves = leaves` for `per_leaf`, else the synthetic `{"_id": "corpus"}`), accumulating each step's structured outputs into `upstream[output_key]` (a list for `per_leaf`, the single dict for corpus-wide). This is the IDENT-4 anchor — the behaviour every dynamic feature is measured byte-for-byte against.

**`run_pipeline_dynamic` (v4, `scheduler.py:459`).** Semantically byte-identical output, but per-leaf executions of every ready step run concurrently:

- **Self-claiming, no wave barrier.** `compute_ready_set` (`scheduler.py:422`) is a pure functional core over `ReadySetState` — it promotes every step whose `depends_on` are all `done` and that isn't already `done`/`in_flight`, emitting a closed `SkipReason` (`deps_unmet`/`concurrency_capped`) for the rest. No I/O, no clock, no LLM — reproducible and unit-testable; the effectful driver applies the result.
- **`ThreadPoolExecutor` (default 4 workers) + `FIRST_COMPLETED`.** Each promoted step's `(step × leaf)` tasks go to one shared pool. The loop `wait(..., return_when=FIRST_COMPLETED)`s; the instant a step's *whole* leaf scope finishes, `_publish_and_finish` publishes its `output_key` and marks it `done`, freeing dependents on the next promotion pass without waiting for unrelated in-flight steps (kills the intra-step straggler stall).
- **Frozen upstream snapshot at promotion.** Each promoted step's leaves are submitted with `snapshot = dict(upstream)` taken at promotion time. Workers only ever read their snapshot; the shared `upstream` is mutated on the **main thread only**, between promotions (`_publish_and_finish`), so a worker never reads mid-publish. Downstream steps therefore see the exact accumulated context the serial path produces.
- **Determinism.** `results` are keyed by `(topo_step_index, leaf_index)` and `step_results` are rebuilt via `sorted(results.keys())`, so the tuple order matches the serial path regardless of completion order.

### `execute_step_with_retry` (`executor.py:595`)

Wraps `execute_step` with **separate budgets**: `MAX_LOGIC_RETRIES = 3` (schema/materializer/contract failures) and `MAX_CRASH_RECOVERIES = 2` (backend raised, or watchdog stall — treated as crash-class/infra). Independent budgets so a flaky network can't starve the algorithmic retry slots and vice versa. A **same-error short-circuit** fires when the last 3 error hashes match (`_same_error_loop_fires`, hash of the first `200` sanitized chars) — bailing before the budget is even exhausted. Backoff is **opt-in**: `backoff=False` by default means `sleep_fn` is never called (byte-identical to pre-1.4); `backoff=True` sleeps `full_jitter_backoff(attempt)` between attempts. Each retry substitutes `{{retry.attempt}}`/`{{retry.error}}` into the prompt and prefixes a sanitized prior-error nudge onto the system prompt.

The **watchdog** (`_call_backend_with_timeout`, `executor.py:843`) runs `backend.call` in a 1-worker pool with `Future.result(timeout=N)` (`DEFAULT_TIMEOUT_SECONDS = 120`, overridable per step). On timeout the step returns a `stalled after Ns` `StepResult` **without cancelling** the in-flight call — it runs to completion in a daemon thread and its result is discarded. `classify_error` (`executor.py:478`) is a pure, deterministic string heuristic mapping an error string to `ErrorClass` ∈ {`transient`, `validation`, `rate_limit`, `auth`, `crash`}; empty → `crash` (fail-closed).

### `StepOutcome` — typed discriminated union (`scheduler.py:256`)

`classify_outcome(StepResult)` (pure, no LLM) maps the executor's terminal `error` string onto a closed `StepOutcomeKind`: `SUCCESS`, `RETRY_EXHAUSTED`, `WATCHDOG_KILLED`, `SAME_ERROR_LOOP`, `CONTRACT_VIOLATION`, `BUDGET_EXHAUSTED`. The `.artifact` property **raises `ValueError` unless the kind is `SUCCESS`** — a caller structurally cannot consume a note that never validated. Precedence is deliberate: `BUDGET_EXHAUSTED` (global) → `SAME_ERROR_LOOP` → `WATCHDOG_KILLED` → `CONTRACT_VIOLATION` (checked *before* the retry-budget marker, so a contract defect that burned its retry budget still surfaces as the fix-routable cause) → `RETRY_EXHAUSTED`. `BUDGET_EXHAUSTED` is never produced by `classify_outcome` itself (a single `StepResult` can't see the global budget); it's emitted by the budget layer, present in the union so it's closed up-front.

### Resume manifest (`manifest.py`)

`Manifest` is a `{leaf_id: ManifestEntry}` ledger with a 4-state lifecycle (`pending`/`in_progress`/`done`/`blocked`). Design invariants:

- **Rebuildable projection (IDENT-2).** `rebuild_from_vault` reconstructs `done`-status purely from which target note files exist on disk — a lost/corrupt manifest is always recoverable from the vault; the manifest is never authoritative.
- **Atomic save + rotation.** `save` serializes to a uniquely-named `.tmp`, `fsync`s, `os.replace`s over the main file (atomic on POSIX/Windows), and rotates `.bak` → `.bak.1` → `.bak.2` (last three kept). `load` sweeps orphaned `.tmp`s, integrity-checks JSON shape, and falls back to the newest good `.bak`; if none is good it starts empty *with a logged warning* (fail-closed, IDENT-5).
- **CAS claim + mark-done-before-release.** `claim` is a compare-and-swap that succeeds only when a leaf is absent/`pending` — the single choke point against two workers owning one leaf. `mark_done` is the durable-commit step: a worker persists `done` *before* releasing its claim, so the leaf leaves the claimable set the moment the write lands (double-dispatch safety). `reclaim_stale` requeues only *foreign*, stale `in_progress` rows.
- **Resume output-skip is DEFERRED.** In the dynamic scheduler the manifest is a crash-safety projection only; output-reconstruction on resume (skip-a-done-leaf) is not wired, so a fresh run always executes every task (identical to serial). See `scheduler.py:508` docstring.

### Gate engine (`gates.py`)

One `Gate` abstraction — a named, scoped, **pure-program** predicate — reused at three scopes (plan/session/wave); there is no second mechanism. `build_close_gate` composes the per-session commit check ordered cheapest-first: `format_predicate` (delegates to `tessellum.format.validate` — frontmatter + links + BB-typed-edges, no re-implementation) then `grounding_predicate` (the only semantic check, but still a program: it *reads* an independently-produced `GroundingVerdict`; a `None` or `auth_blocked` verdict is fail-closed FAIL, never a plausibility pass). `build_wave_gate` provides `duplicate_target_predicate` (exact-path dedup a per-session gate structurally can't see). `GateSuite.evaluate` short-circuits at the first failing gate. **Gate-then-commit ordering:** the note file is written during capture, but the manifest row flips `done` and the `StepResult` is treated as clean *only after* the gate passes — a FAIL turns an otherwise-clean capture into an errored/`blocked` result (never silently `done` — the lifecycle-terminator invariant, `scheduler.py:670`+).

### Fix loop (`fix.py`)

On a close-gate FAIL, `run_fix_loop` repairs non-regressively: it evaluates as-written (early-out if already passing), then **checkpoints the note bytes + score before each fix and keeps the BEST-scoring snapshot** (score = blocking-issue count, lower better). Up to `max_rounds` it builds an informed `FixContext` (current issues + prior-attempt outcomes so the fixer doesn't repeat a failed strategy), runs the fixer, re-gates, and promotes a better result. If the on-disk note is no longer the BEST snapshot (a later fix regressed), it **restores the BEST bytes** (`reverted=True`). A fixer crash is a dead round, not a raise. `make_llm_fixer` wraps any backend into a `FixContext -> None` in-place repairer; the loop owns the checkpoint/revert safety so the fixer only has to *attempt* an improvement.

### Planning economics (`planning.py`)

Both pure/deterministic, both inform the driver (they don't dispatch). The `$0` change-detection pre-gate runs at the **leaf-admission layer** (before the scheduler, so it never interferes with mid-DAG `upstream` accumulation): `partition_unchanged_leaves` splits leaves into `(to_run, skipped)` by comparing each leaf's `content_fingerprint`/`leaf_fingerprint` (positional `_id` excluded) against the recorded fingerprint — skip only on an exact match, always run new/changed/unkeyed leaves (fail-open). `classify_planning_depth` routes a leaf `fast`|`full` from cheap signals, defaulting to `full` when in doubt (a mis-routed novel leaf costs more than an over-planned trivial one).

### Sign-off (`signoff.py`)

`run_sign_off` is the plan→execute approver ladder, cheapest-first: (1) **program gate** — a pure structural pre-filter; a fail rejects outright. (2) **agent judge** — an agent-as-judge returning approve/reject + confidence. (3) **human** — a suspend/approve/resume seam reached *only* on low agent confidence or high blast radius. Rung callables are injected; this module owns the ladder logic, not the model/UI calls. When the human rung is required but disabled, it returns `needs_human` for an out-of-band decision.

### Backends (`llm.py`)

Four backends implement the `LLMBackend` protocol (`call(LLMRequest) -> LLMResponse`):

- **`MockBackend`** — substring-pattern → canned response, no network; records `calls` for test assertions. The only backend in `BACKEND_CONTRACTS` by default.
- **`AnthropicBackend`** — Anthropic Messages API (`[agent]` extras + `ANTHROPIC_API_KEY`). Default model `claude-sonnet-4-6`.
- **`BedrockBackend`** — same Claude Messages surface via `anthropic.AnthropicBedrock`; ambient AWS credential chain (`AWS_PROFILE`), no embedded secret. Default model is the `us.anthropic.…` cross-region inference profile (bare foundation-model ids reject on-demand invocation with a 400).
- **`PooledBackend`** — wraps an inner backend with a `CredentialPool`: leases the least-used key per call via an injected provider-specific `key_applier`, and on an exception classifies the cause (`classify_rotation_cause`) and reports it to the pool — a hard rate-limit/quota/auth benches+releases the key (next attempt leases a different one), a transient blip keeps the lease — then re-raises so the executor's retry ladder handles the retry. Tags the served key id (not the secret) in response metadata.

`CredentialPool`/`RunBudget` (`credential_pool.py`) are pure bookkeeping (timestamps passed in). Rotation causes bench for **absolute** cooldowns: `transient` → keep the key; `rate_limit` → `COOLDOWN_RATE_LIMIT_SECS = 3600` (1h); `quota`/`auth` → `COOLDOWN_QUOTA_SECS = 86400` (24h). Cooldowns are `available_at` timestamps that survive a restart (`to_cooldowns`/`load_cooldowns`). `RunBudget.try_spend` is atomic all-or-nothing; the dynamic scheduler charges `cost=1.0` per task before dispatch and halts a refused leaf with `BUDGET_EXHAUSTED` *without* calling the backend (`scheduler.py:622`) — the runaway-fan-out breaker a static compile gate can't catch.

### Skills-as-tools (`skill_tool.py`)

`build_skill_tool` compiles a skill (delegating *all* compilation to `compile_skill` — single source of truth) and projects it into a `SkillTool`: `{input_schema, output_schema, side_effects, gates, mcp_deps, routing_key}`. It's a read-only view for discovery/routing, never a re-implementation of compilation. `CapabilityRegistry` routes two-tier: a deterministic closed table over `(produces_bb, input_kind, domain)` returns the skill on a unique match; 0-or-many matches return `needs_llm_selector` with the candidate list — this module never calls an LLM, it hands the open-set semantic choice back to the caller.

## Invariants / design decisions + WHY

- **Compile is zero-LLM.** All structure/contract/DAG decisions are program logic; no model is consulted at compile time. WHY: compilation must be deterministic, cheap, and CI-runnable — contract drift should fail a build, not cost tokens.
- **The whole v4 feature set is opt-in behind non-`None` args; default = serial parity (IDENT-4).** `run_pipeline` is the reference. In `run_pipeline_dynamic`, `manifest`/`close_gate`/`budget`/`wave_gate`/`context_assembler`/`fixer` all default `None` and each docstring states "= parity". WHY: a new capability must never silently change existing output; parity is the acceptance test.
- **Materializer is the only side-effect channel; contracts default `requires_tool_free_backend=True`.** WHY: agents that bypass the materializer produce undocumented writes; forcing a tool-free backend makes the materializer the single audited write path.
- **Separate logic vs crash retry budgets + same-error short-circuit.** WHY: an algorithmic defect and an infra flake have different remedies and shouldn't share a budget; three identical errors mean retrying won't help, so bail early.
- **Watchdog is non-cancelling.** WHY: Python can't safely kill a thread mid-call; marking the step stalled and discarding the background result is simpler, portable, and correct.
- **`StepOutcome.artifact` raises unless `SUCCESS`.** WHY: a discriminated-union discipline that makes it a *type error* to consume the output of a step that never validated.
- **Manifest is a rebuildable projection, atomically written, fail-closed on load (IDENT-2/5).** WHY: the vault is the source of truth; a lost or half-written manifest must never corrupt a resume — it's regenerated from disk or falls back to a good backup.
- **Gate-then-commit + mark-done-before-release.** WHY: a note only "counts" once it passes its close-gate, and a leaf only leaves the claimable set once `done` is durably persisted — together they prevent silent-`done` blocks and double-dispatch.
- **Grounding gate consumes a verdict, fail-closed.** WHY: the gate stays a pure program (agent produces evidence, program decides); an unverifiable source is a FAIL, never a plausibility pass, so fabrication can't slip through.
- **Frozen upstream snapshot at promotion + main-thread-only publish.** WHY: gives lock-free reads of accumulated context that are byte-identical to the serial accumulation order.
- **Credential ids, never secrets.** WHY: `CredentialPool` holds key *ids*; the caller maps id→secret out of band, so this module never touches a credential.
- **No PageRank in retrieval; the composer does not rank notes.** Composer writes/updates notes; retrieval (System D) is a separate subsystem. (Consistent with the 1.0 fact that retrieval has no PageRank.)

## Public API / CLI

Package exports (`from tessellum.composer import …`): `compile_skill`, `to_dag_json`, `CompiledPipeline`/`CompiledStep`, `run_pipeline`, `run_pipeline_dynamic`, `RunResult`, `execute_step`/`execute_step_with_retry`, `classify_error`/`classify_outcome`, `StepOutcome`, `Manifest`, `RunBudget`, `CredentialPool`, `build_close_gate`/`build_wave_gate`, `GroundingVerdict`, `run_fix_loop`/`make_llm_fixer`, `get_assembler`, `partition_unchanged_leaves`, `run_sign_off`, `CapabilityRegistry`/`build_skill_tool`, `run_batch`, `run_eval`/`LLMJudge`, and the four backends (`MockBackend`/`AnthropicBackend`/`BedrockBackend`/`PooledBackend`).

**CLI — `tessellum composer <cmd>` (6 subcommands, `cli/composer.py`):**

- `validate <skill|dir>` — sidecar schema + cross-file consistency (`--format human|json`).
- `compile <skill>` — compile to typed DAG, zero LLM (`--output`, `--format`, `--no-prompts`).
- `run <skill>` — execute against leaves.
- `batch <jobs.json>` — many `(skill, leaves)` jobs in parallel with resume (`--parallelism`, `--no-resume`).
- `eval <scenarios_dir>` — assertions + `LLMJudge` rubric (`--backend`, `--judge-backend`).
- `scaffold-sidecar <skill>` — generate a starter `.pipeline.yaml` from the canonical's section anchors (`--output`, `--force`, `--stdout`).

`run` flags: `--backend mock|anthropic|bedrock`, `--model`, `--region`, `--aws-profile`, `--leaves`, `--vault`, `--mock-responses`, `--dry-run`, `--no-trace`, `--runs-dir`, `--progress`, `--format`. The v4 dynamic path is behind `--dynamic`, which enables: `--workers` (default 4), `--manifest`, `--close-gate`, `--wave-gate`, `--fix-with-backend` (+ `--max-fix-rounds`, requires `--close-gate`), `--max-invocations`, `--max-cost`, `--stats`, `--context-strategy full_source|windowed` (+ `--context-max-chars`), and `--skip-unchanged` (+ `--skip-unchanged-key`). Without `--dynamic`, all of these are ignored and `run_pipeline` (serial) runs.

> Note: `cli/composer.py`'s module docstring lists "Six subcommands" and this doc's 6 composer commands are a subset of Tessellum's 11 top-level CLI commands; `dks` is a peer subcommand that reuses Composer's `LLMBackend` abstractions but is otherwise independent.

## Extension points

- **New materializer.** Add a `MaterializerContract` subclass to `MATERIALIZER_CONTRACTS` (`contracts.py`) + a handler in `materializer._DISPATCH`. The compiler validates against it automatically.
- **New LLM backend.** Implement the `LLMBackend` protocol (`backend_id` + `call`); optionally register an `LLMBackendContract` in `BACKEND_CONTRACTS` for compile-time tool-leakage/argv-overflow checks.
- **MCP contracts.** `MCP_CONTRACTS` ships only `session-mcp`; library users mutate the dict to register their own before invoking the compiler (`contracts.py:337`). MCP-dependency *compile-time validation* is documented as data-only for now (`compiler.py` "Out of scope": `MCPContract` validation "can grow when the runtime needs them").
- **Context strategy.** Subclass `ContextAssembler` (implement `strategy` + `_assemble_raw`) and add it to `ASSEMBLER_REGISTRY`; inherits fail-soft bounding + preflight estimate. Selected by config string via `get_assembler`.
- **Gates.** Add a pure `GatePredicate` and a `Gate` at the right scope; extend `build_close_gate`/`build_wave_gate` or the `DIGEST_GATES` scope registry. `plan`-scope is a placeholder (the sign-off approver is the plan-time gate).
- **Fixer.** Provide any `FixContext -> object` callable to `run_fix_loop`/`run_pipeline_dynamic(informed_fixer=…)`; `make_llm_fixer` is the reference LLM implementation. The legacy `(step, leaf, issues)` `fixer` shape is still accepted (adapted; `informed_fixer` takes precedence).
- **Sign-off rungs.** Inject `program_gate`/`agent_judge`/`human_prompt` callables + a `SignOffPolicy` into `run_sign_off`.
- **Eval rubric.** `DEFAULT_RUBRIC_DIMENSIONS` (6-dim) is overridable per scenario via `rubric_dimensions`; new assertion kinds slot into `_check_assertion`.

### Deferred / unwired (called out honestly)

- **Resume output-skip** (skip an already-`done` leaf on resume) is DEFERRED — the manifest is crash-safety only today; a fresh dynamic run re-executes every task.
- **Cross-leaf scoping** is treated as `corpus_wide` in the scheduler for now.
- **APPLY-mode `{{existing.Z}}` pre-fetch** is not wired — the materializer reads existing files at write time.
- **Column-oriented batching** (grouping N `per_leaf` instances into one LLM call) is deferred until backend pricing motivates it.
- **`applies_to_files_query` resolution** against the index DB is loader-accepted but resolved later by the compiler when the index is available.
- **`batch.py` runs over the serial `run_pipeline`**, not the dynamic scheduler; its resume is per-*job* (result-file existence), coarser than the manifest's per-*leaf* resume.
