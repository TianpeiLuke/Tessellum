# `tessellum.composer` — Reference

API, symbols, and signatures for the typed-contract pipeline runtime. For the mental model and how work flows through it, see [../composer.md](../composer.md).

## File → role

| File | Role |
|------|------|
| `loader.py` | Resolves the canonical's `pipeline_metadata:` field, reads the sidecar YAML, validates in three stages — (1) jsonschema against `schemas/pipeline.schema.json`, (2) Pydantic V2 model construction, (3) cross-file `section_id`↔anchor consistency. Returns `Pipeline` or `None` (`pipeline_metadata: none`). |
| `skill_extractor.py` | `load_pipeline_metadata` (reads the canonical frontmatter field) + `load_skill_section(skill_path, section_id)` (pulls a step's prompt body from the canonical). Raises `SkillExtractionError`. |
| `compiler.py` | `compile_skill` — the zero-LLM compile. `_topological_sort` (cycle + forward-ref + duplicate-id), `_compile_step` (contract resolution + `required_output_fields` check + prompt extraction), `_validate_context_budgets`. Emits `CompiledPipeline`/`CompiledStep`; `to_dag_json` serializes it. |
| `contracts.py` | Three frozen-Pydantic contract families + registries: `MaterializerContract` (`MATERIALIZER_CONTRACTS`, 5 subclasses), `LLMBackendContract` (`BACKEND_CONTRACTS`), `MCPContract` (`MCP_CONTRACTS`, ships `session-mcp`). `ContractViolation` with typed `KIND_*` tags. |
| `materializer.py` | `materialize` dispatch → 5 concrete materializers, one per contract. Parses the wire format, writes/applies files under `vault_root`, returns `MaterializedOutput`. |
| `llm.py` | `LLMBackend` protocol + `LLMRequest`/`LLMResponse`. Four backends: `MockBackend`, `AnthropicBackend`, `BedrockBackend`, `PooledBackend`. |
| `executor.py` | `execute_step` (resolve → watchdog dispatch → schema-validate → materialize) + `execute_step_with_retry` (separate logic/crash budgets, same-error short-circuit, opt-in backoff). `classify_error` → `ErrorClass`; `full_jitter_backoff`. |
| `scheduler.py` | `run_pipeline` (serial) + `run_pipeline_dynamic` (self-claiming parallel). Pure `compute_ready_set` core over `ReadySetState`/`SkipReason`. `StepOutcome` union + `classify_outcome`. Trace/statistics writers; wave-gate + close-gate drivers. |
| `manifest.py` | `Manifest` — durable, atomically-written, rebuildable resume projection. 4-state lifecycle, CAS `claim`, `mark_done`-before-release, `rebuild_from_vault`, `.bak` rotation. |
| `gates.py` | One `Gate` abstraction at three scopes (plan/session/wave). `GateSuite`, `build_close_gate` (format + grounding), `build_wave_gate` (dedup), `GroundingVerdict`. Reuses `tessellum.format.validate`. |
| `fix.py` | `run_fix_loop` — checkpoint-before-fix + revert-to-BEST close-gate repair. `FixContext` (informed), `make_llm_fixer`, `score_issues`. |
| `credential_pool.py` | `CredentialPool` (least-used lease, error-class rotation, differentiated cooldowns) + `RunBudget` (atomic `try_spend`) + per-stage `EffortLevel`. `classify_rotation_cause`. |
| `context_assembler.py` | Swappable input-side `ContextAssembler` ABC (`full_source`/`windowed`), percentage-scaled fail-soft bounds, read-path hardening (`is_safe_read_path`). |
| `planning.py` | `$0` change-detection pre-gate (`content_fingerprint`, `leaf_fingerprint`, `partition_unchanged_leaves`, `should_skip_unchanged`) + selective depth (`classify_planning_depth`). |
| `signoff.py` | `run_sign_off` — the plan→execute approver ladder: program gate → agent judge → human. |
| `skill_tool.py` | `SkillTool` projection + `build_skill_tool` + `CapabilityRegistry` two-tier router ("skills as tools"). |
| `batch.py` | `run_batch` — many `(skill, leaves)` jobs in parallel with file-based resume, over the *serial* `run_pipeline`. |
| `eval.py` | Scenario framework: structural `Assertion`s + `LLMJudge` 6-dim rubric. |
| `session_mcp.py` | Read-only tools over the active Claude Code transcript (`SESSION_MCP_TOOLS` + accessors). |
| `schemas/pipeline.schema.json` | JSON Schema for the sidecar (loader stage 1). |

## Loader (`loader.py`)

- `load_pipeline(skill_path: Path | str) -> Pipeline | None` — three-stage validated load; `None` when `pipeline_metadata: none`.
- `Pipeline`, `PipelineStep` — Pydantic V2 models (also `MCPDependency`, `Query`).
- `PipelineValidationError` — raised on any stage failure.

## Skill extractor (`skill_extractor.py`)

- `load_pipeline_metadata(skill_path) -> str | None` — the canonical's `pipeline_metadata:` field.
- `load_skill_section(skill_path, section_id: str) -> str` — the prompt body for one step; miss raises `SkillExtractionError`.
- `SkillExtractionError(Exception)`.

## Compiler (`compiler.py`)

- `compile_skill(skill_path: Path | str) -> CompiledPipeline` — zero-LLM compile. Empty `CompiledPipeline` when the skill has no pipeline.
- `CompiledPipeline`, `CompiledStep` — the typed DAG (steps in topological order).
- `to_dag_json(pipeline: CompiledPipeline) -> dict` — serialize the DAG.
- `CompilerError(Exception)` — DAG/extraction failure (distinct from `ContractViolation` so `except (CompilerError, ContractViolation)` catches all compile-time errors).

Internal stages: `_topological_sort` (exists-check, forward-ref ban, DFS cycle detection, duplicate `section_id`), `_compile_step` (materializer resolution + `required_output_fields` superset check + prompt extraction), `_validate_context_budgets`.

### Compile constants

| Symbol | Value | Meaning |
|--------|-------|---------|
| `HARD_PROMPT_CAP_CHARS` | `150_000` | Per-step rendered-prompt hard cap; over → `CompilerError`. |
| `WARN_AT_PROMPT_FRACTION` | `0.7` | Fraction of the cap that emits a non-fatal `budget_warnings` entry. |
| `DEFAULT_PER_UPSTREAM_SOFT_CAP_CHARS` | `25_000` | Assumed size of each upstream output when no `max_chars` is declared. |

Per-step hard cap = `step.max_prompt_chars` if set, else `HARD_PROMPT_CAP_CHARS`. Estimate = `sum(upstream soft caps) + len(prompt_section_text)`.

## Contracts (`contracts.py`)

- `MaterializerContract` (frozen base) + `MATERIALIZER_CONTRACTS: dict[str, MaterializerContract]`. Subclasses: `NoOpContract`, `BodyMarkdownToFileContract`, `BodyMarkdownFrontmatterToFileContract`, `EditsApplyToFilesContract`, `EditsApplyXmlTagsContract`. Each declares `required_output_fields` and defaults `requires_tool_free_backend=True`.
- `LLMBackendContract` + `BACKEND_CONTRACTS` (ships `MockBackend` only).
- `MCPContract` + `MCP_CONTRACTS` (ships `session-mcp`); library users mutate the dict to register their own before compiling.
- `ContractViolation(Exception)` — typed `KIND_*` tags include `KIND_UNKNOWN_MATERIALIZER`, `KIND_MISSING_REQUIRED_OUTPUT_FIELD`.

Contract check per step: unknown materializer key → `KIND_UNKNOWN_MATERIALIZER`; for `CORE`/`DEFERRED` steps, `expected_output_schema.required` must ⊇ contract `required_output_fields`, else `KIND_MISSING_REQUIRED_OUTPUT_FIELD`. `INFRA`/`no_op` has empty required fields → check skipped.

## Materializer (`materializer.py`)

- `materialize(step, output, *, vault_root) -> MaterializedOutput` — dispatch over `_DISPATCH` to one of 5 handlers: `no_op`, `body_markdown_to_file`, `body_markdown_frontmatter_to_file`, `edits_apply_to_files`, `edits_apply_xml_tags`.
- `MaterializedOutput`, `MaterializerError(Exception)`.

## LLM backends (`llm.py`)

Protocol: `LLMBackend` with `backend_id: str` and `call(request: LLMRequest) -> LLMResponse`.

| Backend | Transport | Default model | Notes |
|---------|-----------|---------------|-------|
| `MockBackend` | none | — | substring-pattern → canned response; records `calls`; only backend in `BACKEND_CONTRACTS`. |
| `AnthropicBackend` | Anthropic Messages API | `claude-sonnet-4-6` | needs `[agent]` extras + `ANTHROPIC_API_KEY`. |
| `BedrockBackend` | `anthropic.AnthropicBedrock` | `us.anthropic.…` cross-region inference profile | ambient AWS chain (`AWS_PROFILE`); bare foundation-model ids 400 on on-demand invocation. |
| `PooledBackend` | wraps an inner backend | inherits | leases least-used key via injected `key_applier`; classifies failures via `classify_rotation_cause`, reports to the pool, re-raises. Tags served key *id* (not secret) in metadata. |

- `LLMRequest`, `LLMResponse`.

## Executor (`executor.py`)

- `execute_step(step, leaf, upstream, *, backend, vault_root, …) -> StepResult` — resolve `{{leaf.X}}`/`{{upstream.Y}}`/`{{retry.X}}` → `LLMRequest`, watchdog dispatch, schema-validate, materialize.
- `execute_step_with_retry(…, *, max_logic_retries=MAX_LOGIC_RETRIES, max_crash_recoveries=MAX_CRASH_RECOVERIES, backoff=False, sleep_fn=…) -> StepResult` — separate budgets, same-error short-circuit, opt-in backoff.
- `classify_error(error_msg: str) -> ErrorClass` — pure deterministic string heuristic; empty → `"crash"` (fail-closed).
- `full_jitter_backoff(attempt: int) -> float` — backoff delay.
- `StepResult`, `ExecutorError(Exception)`.

| Symbol | Value | Meaning |
|--------|-------|---------|
| `MAX_LOGIC_RETRIES` | `3` | Schema/materializer/contract-failure budget. |
| `MAX_CRASH_RECOVERIES` | `2` | Backend-raised / watchdog-stall budget (independent of logic budget). |
| `DEFAULT_TIMEOUT_SECONDS` | `120.0` | Watchdog timeout; overridable per step via `step.timeout_seconds`. |
| `ErrorClass` | Literal | `"transient"`, `"validation"`, `"rate_limit"`, `"auth"`, `"crash"`. |

Same-error short-circuit fires when the last 3 error hashes match (hash of the first 200 sanitized chars). Watchdog (`_call_backend_with_timeout`) runs `backend.call` in a 1-worker pool with `Future.result(timeout=N)`; on timeout returns a `stalled after Ns` result **without cancelling** the in-flight call.

## Scheduler (`scheduler.py`)

- `run_pipeline(pipeline, leaves, *, backend, vault_root, …) -> RunResult` — serial reference. Topological order, skips `INFRA`, one leaf at a time, accumulates each step's output into `upstream[output_key]`.
- `run_pipeline_dynamic(pipeline, leaves, *, backend, vault_root, max_workers=4, manifest=None, close_gate=None, wave_gate=None, budget=None, context_assembler=None, informed_fixer=None, …) -> RunResult` — self-claiming parallel; every v4 arg defaults `None` (= serial parity).
- `compute_ready_set(state: ReadySetState) -> …` — pure functional core; promotes steps whose deps are all `done`, emits `SkipReason` (`deps_unmet`/`concurrency_capped`) for the rest. No I/O, clock, or LLM.
- `ReadySetState`, `SkipReason`, `RunResult`.
- `classify_outcome(result: StepResult) -> StepOutcome` — pure; maps terminal error → `StepOutcomeKind`.
- `StepOutcome` — discriminated union; `.artifact` **raises `ValueError` unless `kind == "SUCCESS"`**.

`StepOutcomeKind` (`scheduler.py:233`), with `classify_outcome` precedence high→low: `BUDGET_EXHAUSTED` (global; emitted by the budget layer, never by `classify_outcome`) → `SAME_ERROR_LOOP` → `WATCHDOG_KILLED` → `CONTRACT_VIOLATION` (checked before the retry-budget marker) → `RETRY_EXHAUSTED` → `SUCCESS`.

Dynamic-path mechanics: one shared `ThreadPoolExecutor` (default 4 workers), `wait(..., return_when=FIRST_COMPLETED)`, `_publish_and_finish` publishes an `output_key` and marks `done` on the **main thread only**; each promoted step's workers read a frozen `snapshot = dict(upstream)` taken at promotion. `results` keyed by `(topo_step_index, leaf_index)`, rebuilt via `sorted(results.keys())` for serial-order determinism. Budget charge is `cost=1.0` per task before dispatch; a refusal halts the leaf with `BUDGET_EXHAUSTED` without calling the backend.

## Manifest (`manifest.py`)

- `Manifest` — `{leaf_id: ManifestEntry}` ledger; 4-state lifecycle `pending`/`in_progress`/`done`/`blocked`.
- `claim(leaf_id) -> bool` — CAS; succeeds only when absent/`pending`.
- `mark_done(leaf_id)` — durable-commit before claim release.
- `reclaim_stale(...)` — requeue only foreign, stale `in_progress` rows.
- `rebuild_from_vault(...)` — reconstruct `done` from which target notes exist on disk (IDENT-2).
- `save()` — serialize to unique `.tmp`, `fsync`, `os.replace`, rotate `.bak`→`.bak.1`→`.bak.2`.
- `load(...)` — sweep orphaned `.tmp`, integrity-check, fall back to newest good `.bak`, else start empty with a warning (fail-closed, IDENT-5).
- `ManifestEntry`, `AttemptRecord`, `ManifestError`, `MANIFEST_VERSION`, `VALID_STATUSES`.

Resume output-skip (skip an already-`done` leaf) is DEFERRED — the manifest is crash-safety only; a fresh dynamic run re-executes every task.

## Gates (`gates.py`)

- `Gate` — named, scoped (`plan`/`session`/`wave`), pure-program predicate.
- `GateSuite.evaluate(...)` — short-circuits at the first failing gate.
- `build_close_gate(...) -> GateSuite` — `format_predicate` (delegates to `tessellum.format.validate`) then `grounding_predicate` (reads a `GroundingVerdict`; `None`/`auth_blocked` → fail-closed FAIL).
- `build_wave_gate(...) -> GateSuite` — `duplicate_target_predicate` (exact-path dedup).
- `GroundingVerdict`, `GateResult`, `CompositeGateResult`, `DIGEST_GATES` (scope registry).

Gate-then-commit: the manifest row flips `done` and the `StepResult` is treated clean only after the gate passes; a FAIL becomes an errored/`blocked` result (never silently `done`).

## Fix loop (`fix.py`)

- `run_fix_loop(..., *, max_rounds, informed_fixer, …) -> FixLoopResult` — evaluate as-written (early-out if passing), checkpoint bytes+score before each fix, keep BEST snapshot (score = blocking-issue count, lower better), restore BEST on regression (`reverted=True`). Fixer crash = dead round, not a raise.
- `score_issues(issues) -> int` — blocking-issue count.
- `make_llm_fixer(backend) -> Callable[[FixContext], None]` — reference in-place LLM repairer.
- `FixContext` (current issues + prior `AttemptOutcome`s), `FixLoopResult`, `AttemptOutcome`.

## Credential pool + budgets (`credential_pool.py`)

- `CredentialPool` — least-used lease; on failure benches by `classify_rotation_cause`. Holds key **ids**, not secrets. Cooldowns are `available_at` timestamps surviving restart (`to_cooldowns`/`load_cooldowns`).
- `RunBudget.try_spend(cost) -> bool` — atomic all-or-nothing.
- `classify_rotation_cause(...)`, `effort_for_stage(...)`, `EffortLevel`, `DEFAULT_STAGE_EFFORT`, `CredentialPoolError`, `BudgetExhausted`.

| Cause | Cooldown | Lease |
|-------|----------|-------|
| `transient` | none | keep the key |
| `rate_limit` | `COOLDOWN_RATE_LIMIT_SECS = 3600.0` (1h) | bench + release |
| `quota` / `auth` | `COOLDOWN_QUOTA_SECS = 86400.0` (24h) | bench + release |

## Context assembler (`context_assembler.py`)

- `ContextAssembler` (ABC) — implement `strategy` + `_assemble_raw`; inherits fail-soft percentage-scaled bounds + preflight estimate.
- `FullSourceAssembler`, `WindowedAssembler`, `AssembledContext`.
- `get_assembler(strategy: str) -> ContextAssembler` — selects from `ASSEMBLER_REGISTRY`.
- `is_safe_read_path(path) -> bool` — read-path hardening.

## Planning (`planning.py`)

- `content_fingerprint(...)`, `leaf_fingerprint(...)` — positional `_id` excluded.
- `partition_unchanged_leaves(leaves, …) -> (to_run, skipped)` — skip only on exact fingerprint match; new/changed/unkeyed always run (fail-open). Runs at the leaf-admission layer, before the scheduler.
- `should_skip_unchanged(...) -> bool`.
- `classify_planning_depth(leaf) -> LeafComplexity` — `fast`|`full`, defaults `full`.

## Sign-off (`signoff.py`)

- `run_sign_off(..., *, program_gate, agent_judge, human_prompt, policy: SignOffPolicy) -> SignOffResult` — cheapest-first ladder: program gate (hard reject) → agent judge (`AgentVerdict`, approve/reject + confidence) → human (only on low confidence / high blast radius; `needs_human` when the rung is disabled).
- `SignOffPolicy`, `SignOffResult`, `AgentVerdict`.

## Skills-as-tools (`skill_tool.py`)

- `build_skill_tool(skill_path) -> SkillTool` — delegates compilation to `compile_skill`; projects `{input_schema, output_schema, side_effects, gates, mcp_deps, routing_key}`. Read-only view.
- `CapabilityRegistry` — two-tier route over `(produces_bb, input_kind, domain)`: unique match returns the skill; 0-or-many returns `needs_llm_selector` + candidates. Never calls an LLM.
- `SkillTool`, `RoutingKey`, `RouteDecision`, `McpDep`.

## Batch (`batch.py`)

- `run_batch(jobs, *, parallelism, resume=True, …) -> BatchResult` — many `(skill, leaves)` jobs in parallel over the **serial** `run_pipeline`; per-*job* resume (result-file existence), coarser than the manifest's per-*leaf* resume.
- `BatchJob`, `BatchJobResult`, `BatchResult`.

## Eval (`eval.py`)

- `run_eval(scenarios_dir, *, backend, judge_backend, …) -> EvalResult` — structural assertions + `LLMJudge` 6-dim rubric.
- `LLMJudge`, `JudgeScore`, `DEFAULT_RUBRIC_DIMENSIONS` (6-dim, overridable per scenario via `rubric_dimensions`).
- `Assertion`, `AssertionResult`, `EvalScenario`, `ScenarioResult`, `EvalError`, `load_scenario`, `load_scenarios`.

## Session-MCP (`session_mcp.py`)

Read-only tools over the active Claude Code transcript: `SESSION_MCP_TOOLS`, `get_session_metadata`, `get_tool_uses`, `read_recent_messages`, `resolve_transcript_path`, `search_transcript`.

## Package exports (`from tessellum.composer import …`)

`compile_skill`, `to_dag_json`, `CompiledPipeline`, `CompiledStep`, `CompilerError`; `load_pipeline`, `Pipeline`, `PipelineStep`, `PipelineValidationError`; `load_skill_section`, `load_pipeline_metadata`, `SkillExtractionError`; the contract families + registries + `ContractViolation`; `materialize`, `MaterializedOutput`, `MaterializerError`; the four backends + `LLMBackend`/`LLMRequest`/`LLMResponse`; `execute_step`, `execute_step_with_retry`, `classify_error`, `full_jitter_backoff`, `ErrorClass`, `StepResult`, `ExecutorError`, `MAX_LOGIC_RETRIES`, `MAX_CRASH_RECOVERIES`; `run_pipeline`, `run_pipeline_dynamic`, `RunResult`, `compute_ready_set`, `ReadySetState`, `SkipReason`, `StepOutcome`, `classify_outcome`; `Gate`, `GateResult`, `GateSuite`, `CompositeGateResult`, `GroundingVerdict`, `build_close_gate`, `build_wave_gate`, `DIGEST_GATES`; `run_fix_loop`, `make_llm_fixer`, `score_issues`, `FixContext`, `FixLoopResult`, `AttemptOutcome`; `partition_unchanged_leaves`, `should_skip_unchanged`, `content_fingerprint`, `leaf_fingerprint`, `classify_planning_depth`, `LeafComplexity`; `CredentialPool`, `RunBudget`, `classify_rotation_cause`, `effort_for_stage`, `DEFAULT_STAGE_EFFORT`, `CredentialPoolError`, `BudgetExhausted`; `ContextAssembler`, `FullSourceAssembler`, `WindowedAssembler`, `AssembledContext`, `get_assembler`, `is_safe_read_path`; `run_sign_off`, `SignOffPolicy`, `SignOffResult`, `AgentVerdict`; `build_skill_tool`, `SkillTool`, `CapabilityRegistry`, `RoutingKey`, `RouteDecision`, `McpDep`; `run_batch`, `BatchJob`, `BatchJobResult`, `BatchResult`; `Manifest`, `ManifestEntry`, `AttemptRecord`, `ManifestError`, `MANIFEST_VERSION`, `VALID_STATUSES`; `run_eval`, `LLMJudge`, `JudgeScore`, `DEFAULT_RUBRIC_DIMENSIONS`, and the rest of the eval framework; the session-MCP surface.

The DKS runtime is a **peer** module (`tessellum.dks`), not part of Composer, though it reuses Composer's `LLMBackend` abstractions.

## CLI — `tessellum composer <cmd>` (`cli/composer.py`)

Six subcommands (a subset of Tessellum's 11 top-level CLI commands; `dks` is a peer subcommand reusing Composer's `LLMBackend`):

| Command | Purpose | Flags |
|---------|---------|-------|
| `validate <skill\|dir>` | Sidecar schema + cross-file consistency. | `--format human\|json` |
| `compile <skill>` | Compile to typed DAG, zero LLM. | `--output`, `--format`, `--no-prompts` |
| `run <skill>` | Execute against leaves. | see below |
| `batch <jobs.json>` | Many `(skill, leaves)` jobs in parallel with resume. | `--parallelism`, `--no-resume` |
| `eval <scenarios_dir>` | Assertions + `LLMJudge` rubric. | `--backend`, `--judge-backend` |
| `scaffold-sidecar <skill>` | Generate a starter `.pipeline.yaml` from section anchors. | `--output`, `--force`, `--stdout` |

### `run` flags

Serial (always available): `--backend mock|anthropic|bedrock`, `--model`, `--region`, `--aws-profile`, `--leaves`, `--vault`, `--mock-responses`, `--dry-run`, `--no-trace`, `--runs-dir`, `--progress`, `--format`.

Dynamic path behind `--dynamic` (all ignored without it): `--workers` (default 4), `--manifest`, `--close-gate`, `--wave-gate`, `--fix-with-backend` (+ `--max-fix-rounds`, requires `--close-gate`), `--max-invocations`, `--max-cost`, `--stats`, `--context-strategy full_source|windowed` (+ `--context-max-chars`), `--skip-unchanged` (+ `--skip-unchanged-key`).

## Extension points

- **New materializer** — add a `MaterializerContract` subclass to `MATERIALIZER_CONTRACTS` + a handler in `materializer._DISPATCH`; the compiler validates against it automatically.
- **New backend** — implement the `LLMBackend` protocol (`backend_id` + `call`); optionally register an `LLMBackendContract` in `BACKEND_CONTRACTS` for compile-time tool-leakage/argv-overflow checks.
- **MCP contracts** — mutate `MCP_CONTRACTS` before compiling (ships `session-mcp` only). Compile-time `MCPContract` validation is data-only for now.
- **Context strategy** — subclass `ContextAssembler` (`strategy` + `_assemble_raw`), add to `ASSEMBLER_REGISTRY`; selected via `get_assembler`.
- **Gates** — add a pure `GatePredicate` + a `Gate` at the right scope; extend `build_close_gate`/`build_wave_gate` or the `DIGEST_GATES` registry. `plan`-scope is a placeholder (sign-off is the plan-time gate).
- **Fixer** — provide any `FixContext -> object` callable to `run_fix_loop` / `run_pipeline_dynamic(informed_fixer=…)`; `make_llm_fixer` is the reference. The legacy `(step, leaf, issues)` `fixer` shape is still accepted (`informed_fixer` takes precedence).
- **Sign-off rungs** — inject `program_gate`/`agent_judge`/`human_prompt` + a `SignOffPolicy`.
- **Eval rubric** — override `DEFAULT_RUBRIC_DIMENSIONS` per scenario via `rubric_dimensions`; new assertion kinds slot into `_check_assertion`.

## Deferred / unwired

- **Resume output-skip** — manifest is crash-safety only; a fresh dynamic run re-executes every task.
- **Cross-leaf scoping** — treated as `corpus_wide` in the scheduler.
- **APPLY-mode `{{existing.Z}}` pre-fetch** — not wired; the materializer reads existing files at write time.
- **Column-oriented batching** — deferred until backend pricing motivates it.
- **`applies_to_files_query` resolution** against the index DB — loader-accepted, resolved later by the compiler once the index is available.
- **`batch.py` runs over serial `run_pipeline`**, not the dynamic scheduler; resume is per-*job*, coarser than per-*leaf*.
