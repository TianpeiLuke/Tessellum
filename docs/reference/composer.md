# `tessellum.composer` — Reference

API, symbols, and signatures for the typed-contract pipeline runtime. For the mental model and how work flows through it, see [../composer.md](../composer.md).

## File → role

| File | Role |
|------|------|
| `loader.py` | Reads every step section's contract block from the single-file canonical (via `skill_extractor.iter_step_sections`), validates each in two stages — (1) jsonschema against `schemas/pipeline.schema.json`, (2) Pydantic V2 model construction. Returns `Pipeline` or `None` (no step sections → no pipeline). Each step's `section_id` comes from its anchor, so contract↔section mismatch is structurally impossible. |
| `skill_extractor.py` | `iter_step_sections(skill_path)` (the step sections in document order, each a `(section_id, contract, prompt)` triple; prose-only sections skipped) + `split_contract_and_prompt(section_body)` (splits a section's leading ` ```yaml ` contract block from its prompt prose) + `load_skill_section(skill_path, section_id)` (the section's full body) + `list_section_ids`. Raises `SkillExtractionError`. |
| `compiler.py` | `compile_skill` — the zero-LLM compile. `_topological_sort` (cycle + forward-ref + duplicate-id), `_compile_step` (contract resolution + `required_output_fields` check + prompt extraction), `_validate_context_budgets`. Emits `CompiledPipeline`/`CompiledStep`; `to_dag_json` serializes it. |
| `contracts.py` | Three frozen-Pydantic contract families + registries: `MaterializerContract` (`MATERIALIZER_CONTRACTS`, 5 subclasses), `LLMBackendContract` (`BACKEND_CONTRACTS`), `MCPContract` (`MCP_CONTRACTS`, ships `session-mcp`). `ContractViolation` with typed `KIND_*` tags. |
| `materializer.py` | `materialize` dispatch → 5 concrete materializers, one per contract. Parses the wire format, writes/applies files under `vault_root`, returns `MaterializedOutput`. |
| `llm.py` | `LLMBackend` protocol + `LLMRequest`/`LLMResponse`. Four backends: `MockBackend`, `AnthropicBackend`, `BedrockBackend`, `PooledBackend`. |
| `executor.py` | `execute_step` (resolve → watchdog dispatch → schema-validate → materialize) + `execute_step_with_retry` (separate logic/crash budgets, same-error short-circuit, opt-in backoff). `classify_error` → `ErrorClass`; `full_jitter_backoff`. |
| `scheduler.py` | `run_pipeline` (serial) + `run_pipeline_dynamic` (self-claiming parallel). Pure `compute_ready_set` core over `ReadySetState`/`SkipReason`. Verified manifest resume reconstructs committed outputs. `StepOutcome` union + `classify_outcome`. Trace/statistics writers; cancellation, wave-gate, and close-gate drivers. |
| `digestion.py` | Native plan → augment → review → sign-off → execute phase driver over four compiled skill canonicals. `run_execute_wave` factors out the execute fan-out (reused by corpus digestion); `run_digestion_pipeline(stop_after="review")` returns an accepted plan without executing. |
| `manifest.py` | `Manifest` — durable, atomically-written resume projection. 4-state lifecycle, generation-aware CAS `claim`, owner-fenced `commit_success`, identity/artifact `verify_commit`, `rebuild_from_vault`, `.bak` rotation. |
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
| `schemas/pipeline.schema.json` | JSON Schema for a step's contract block (loader stage 1). |
| `proposals.py` | **(P0)** Typed change `Effect`s (`AddNote`/`UpdateNote`/`MergeNotes`/`DropNote`/`Reroute`/`AddReference`/`AddNavigation`) + `ChangeProposal`; content-addressed hashing (`content_hash`, `canonical_json_bytes`, `plan_revision_hash`); `Footprint`/`effect_footprint`/`effect_key`; snapshot-pinned merge (`merge_proposals`/`merge_or_raise`, `MergeResult`/`MergeConflict`); `collect_proposals`. |
| `knowledge_plan.py` | **(P2)** Typed knowledge-plan intent graph: `NoteIntent` (one BB, cited spans, declared entry points + required inlinks, disposition under the preimage rule), `NoteIntentGraph`, `ClaimProvenance`, `note_intent_content_id`, `project_note_intent_graph` (writer-leaf projection). `NoteDisposition` = `create`/`update`/`merge`/`drop`/`skip`. |
| `overlay.py` | **(P2)** `OverlayWriter` — stages note writes into a delta off to the side, never mutating the base vault. `OverlayWriteResult`, `OverlayError`. |
| `overlay_index.py` | **(P3)** `OverlayIndex(base, DeltaState)` — read-through view over base ⊕ delta answering gate/dedup/backlink/ghost queries without mutating the base index (shadow/tombstone/re-author semantics; `ghost_links`/`resolves_ghost`). |
| `write_closure.py` | **(P4)** `write_closure` (exact transactional write set from typed invariants — no graph/hub param), `boundary_witness` (no write-propagating edge escapes; unknown class fails closed), `validation_set` (bounded reverse-reachability re-check; spills, never truncates), `partition_capsules` (union-find over shared closures). |
| `publication.py` | **(P5)** `VersionedVault` — three-phase atomic commit (prepare → publish → acknowledge) with an atomic `CURRENT` pointer swap under an exclusive lock; `VaultSnapshot`/`read_set_matches` (lost-update CAS), `publish_with_cas` (bounded retry), `KnowledgeCapsule`, crash `recover()` + GC. |
| `structural_gates.py` | **(P6)** Capsule-level structural gate suite (no LLM) over the plan + overlay + write closure (`build_structural_gate_suite`); `supervised_admit` — publish iff the suite passes AND a bound `HumanApproval` is present. |
| `semantic_certificate.py` | **(P7)** `certify` (per-claim min-aggregate against a pluggable `ClaimScorer`, fail-closed abstain, emits `GroundingVerdict`); `calibrate` (per-class empirical thresholds); `measure_false_accept_rate` (the held-out gating measurement). Bundles no model, no corpus. |
| `lexical_scorer.py` · `claim_extraction.py` · `certificate_verifier.py` · `calibration_gate.py` | **Runnable certificate (C1–C4)** — a reference lexical `ClaimScorer`, note→`Claim` extraction, the `grounding_verifier` seam wiring, and the A7.5 go/no-go calibration gate that make the P7 certificate runnable + measurable now. Design: [../semantic-certificate.md](../semantic-certificate.md). |
| `planner_loop.py` | **(P8)** `run_planner_loop` — drives an injected planner to a terminal `complete`/`blocked`; ℕ-valued `Deficit` variant + three hard stops (depth, fuel, oscillation) prove termination. |
| `corpus_plan.py` | **Corpus digestion (M1/M2/M6/M7)** — the typed layer above `NoteIntentGraph`: `PlanShape` + `classify_plan_shape` (volume → shape), the hierarchical `CorpusPlan`/`SubObjective` model (derived master index, wave + dependency ordering), `term_ownership_gate`, `resolve_shared_cross_refs`, and `build_corpus_leaf` (bundle → one joint planning leaf). Pure; single-doc path untouched. |
| `corpus_digestion.py` | **Corpus digestion (M3/M4)** — the driver: `run_corpus_planning_wave` (plan every sub-objective, no execute) + `run_corpus_digestion` (plan → whole-corpus gate → execute each accepted sub-plan as its own transaction in dependency-layer order). |

## Loader (`loader.py`)

- `load_pipeline(skill_path: Path | str) -> Pipeline | None` — reads every step section's contract block from the canonical, two-stage validated load; `None` when the canonical has no step sections (no contract blocks).
- `Pipeline`, `PipelineStep` — Pydantic V2 models (also `MCPDependency`, `Query`).
- `PipelineValidationError` — raised on any stage failure.

## Skill extractor (`skill_extractor.py`)

- `iter_step_sections(skill_path) -> list[StepSection]` — the pipeline step sections in document order; each `StepSection` is a `(section_id, contract, prompt)` triple. Sections with no leading contract block (prose) are skipped.
- `split_contract_and_prompt(section_body) -> tuple[dict | None, str]` — split a section body into its parsed leading ` ```yaml ` contract block (`None` if absent) and the remaining prompt prose.
- `load_skill_section(skill_path, section_id: str) -> str` — the full body text for one section (heading excluded, contract block included); miss raises `SkillExtractionError`.
- `list_section_ids(skill_path) -> list[str]` — every `section_id` anchor in document order (steps and prose).
- `StepSection`, `SkillExtractionError(Exception)`.

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

- `materialize(materializer_key, response_text, *, vault_root, dry_run=False, effect_guard=None, effect_recorder=None) -> MaterializedOutput` — dispatch over `_DISPATCH` to one of 5 handlers: `no_op`, `body_markdown_to_file`, `body_markdown_frontmatter_to_file`, `edits_apply_to_files`, `edits_apply_xml_tags`.
- `MaterializedOutput`, `MaterializerError(Exception)`.

All write/apply paths must be relative and resolve beneath `vault_root`; absolute
and traversal paths raise `MaterializerError`. Multi-edit handlers validate all
targets before writing any. The optional `effect_guard` context factory wraps
each filesystem write; `effect_recorder(target)` runs inside that guard
immediately before mutation. If the recorder also exposes
`record_postimage(target, content)`, the intended SHA-256 state is recorded
before atomic publication.

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

- `execute_step(step, *, leaf, upstream, backend, vault_root, budget=None, …) -> StepResult` — resolve `{{leaf.X}}`/`{{upstream.Y}}`/`{{retry.X}}` → budgeted `LLMRequest`, watchdog dispatch, schema-validate, materialize.
- `execute_step_with_retry(…, *, max_logic_retries=MAX_LOGIC_RETRIES, max_crash_recoveries=MAX_CRASH_RECOVERIES, budget=None, backoff=False, sleep_fn=…) -> StepResult` — separate retry budgets, shared per-dispatch run budget, same-error short-circuit, opt-in backoff.
- `classify_error(error_msg: str) -> ErrorClass` — pure deterministic string heuristic; empty → `"crash"` (fail-closed).
- `full_jitter_backoff(attempt: int) -> float` — backoff delay.
- `StepResult`, `ExecutorError(Exception)`.

| Symbol | Value | Meaning |
|--------|-------|---------|
| `MAX_LOGIC_RETRIES` | `3` | Schema/materializer/contract-failure budget. |
| `MAX_CRASH_RECOVERIES` | `2` | Backend-raised / watchdog-stall budget (independent of logic budget). |
| `DEFAULT_TIMEOUT_SECONDS` | `120.0` | Watchdog timeout; overridable per step via `step.timeout_seconds`. |
| `ErrorClass` | Literal | `"transient"`, `"validation"`, `"rate_limit"`, `"auth"`, `"crash"`. |

Same-error short-circuit fires when the last 3 error hashes match (hash of the first 200 sanitized chars). The shared `RunBudget`, when supplied, charges immediately before every backend attempt; refusal returns `run budget exhausted` without consuming a retry slot. Watchdog (`_call_backend_with_timeout`) runs `backend.call` on a daemon thread and waits on an event for `N` seconds; on timeout it returns a `stalled after Ns` result at the deadline **without cancelling** the in-flight call.

## Scheduler (`scheduler.py`)

- `run_pipeline(pipeline, *, leaves=None, backend, vault_root, …) -> RunResult` — serial reference. Topological order, skips `INFRA`, one leaf at a time, accumulates each step's output into `upstream[output_key]`.
- `run_pipeline_dynamic(pipeline, *, leaves=None, backend, vault_root, max_workers=4, manifest=None, run_id=None, generation=0, capability_version=None, manifest_stale_secs=300.0, close_gate=None, wave_gate=None, budget=None, context_assembler=None, informed_fixer=None, cancellation_check=None, effect_guard=None, effect_recorder=None, …) -> RunResult` — self-claiming parallel with verified resume, cooperative cancellation, and optional fenced effects; optional controls preserve serial behavior when omitted.
- `compute_ready_set(state: ReadySetState) -> …` — pure functional core; promotes steps whose deps are all `done`, emits `SkipReason` (`deps_unmet`/`concurrency_capped`) for the rest. No I/O, clock, or LLM.
- `ReadySetState`, `SkipReason`, `RunResult`.
- `classify_outcome(result: StepResult) -> StepOutcome` — pure; maps terminal error → `StepOutcomeKind`.
- `StepOutcome` — discriminated union; `.artifact` **raises `ValueError` unless `kind == "SUCCESS"`**.

`StepOutcomeKind` (`scheduler.py:233`), with `classify_outcome` precedence high→low: a `"run budget exhausted"` marker maps to `BUDGET_EXHAUSTED`, then `SAME_ERROR_LOOP` → `WATCHDOG_KILLED` → `CONTRACT_VIOLATION` (checked before the retry-budget marker) → `RETRY_EXHAUSTED` → `SUCCESS`.

Dynamic-path mechanics: one shared `ThreadPoolExecutor` (default 4 workers), `wait(..., return_when=FIRST_COMPLETED)`, `_publish_and_finish` publishes an `output_key` and marks `done` on the **main thread only**; each promoted step's workers read a frozen `snapshot = dict(upstream)` taken at promotion. `results` keyed by `(topo_step_index, leaf_index)`, rebuilt via `sorted(results.keys())` for serial-order determinism. Budget charge is `cost=1.0` per task before dispatch; a refusal halts the leaf with `BUDGET_EXHAUSTED` without calling the backend. `cancellation_check` runs before dispatch and before materialization. `effect_guard`, when supplied, wraps materializer writes, fix-loop restoration, and manifest saves; arbitrary fixers and trace/event/statistics writers are not automatically fenced.

## Manifest (`manifest.py`)

- `Manifest` — `{leaf_id: ManifestEntry}` ledger; 4-state lifecycle `pending`/`in_progress`/`done`/`blocked`.
- `claim(leaf_id, run_id, now, *, generation=None) -> bool` — CAS; succeeds only when absent/`pending`, recording owner, heartbeat, and optional execution generation.
- `mark_done(leaf_id)` — durable-commit before claim release.
- `commit_success(leaf_id, *, run_id, generation, plan_hash, input_hash, capability_version, structured_output, artifacts, now) -> bool` — owner- and generation-fenced successful commit; stale workers cannot close a reclaimed leaf.
- `verify_commit(leaf_id, *, vault_root, generation, plan_hash, input_hash, capability_version) -> bool` — require exact execution identity and re-hash every recorded artifact before reuse.
- `prepare_retry(leaf_id, *, run_id) -> bool` — clear invalid terminal or same-owner entries without stealing foreign live work.
- `release_for_retry(leaf_id, *, run_id, generation) -> bool` — owner-fenced release after execution failure.
- `invalidate_commit(...) -> bool` — clear exactly the committed identity rejected by a later wave gate.
- `reclaim_stale(...)` — requeue only foreign, stale `in_progress` rows.
- `rebuild_from_vault(...)` — reconstruct existence-only `done` entries from target notes on disk. Those entries lack verification identity and cannot produce resume skips.
- `save()` — serialize to unique `.tmp`, `fsync`, `os.replace`, rotate `.bak`→`.bak.1`→`.bak.2`.
- `load(...)` — sweep orphaned `.tmp`, integrity-check, fall back to newest good `.bak`, else start empty with a warning (fail-closed, IDENT-5).
- `ArtifactRecord.from_path(path, *, vault_root)` — store a vault-relative path plus byte size and SHA-256; paths outside `vault_root` raise `ManifestError`.
- `ManifestEntry`, `ArtifactRecord`, `AttemptRecord`, `ManifestError`, `MANIFEST_VERSION` (`"1.1"`), `VALID_STATUSES`.

At promotion, the scheduler derives `plan_hash` from the skill bytes plus pipeline version and `input_hash` from the step id, leaf, and frozen upstream snapshot. A `done` entry is skipped only when generation, plan, input, capability version, commit timestamp, and every artifact hash verify. It then reconstructs `StepResult.materialized.structured` and artifact paths from the manifest so downstream steps receive the original upstream value. Verification failure returns terminal/same-owner state to `pending`; a foreign live claim remains fenced. With a wave gate, clean entries stay `in_progress` until the wave passes.

## Gates (`gates.py`)

- `Gate` — named, scoped (`plan`/`session`/`wave`), pure-program predicate.
- `GateSuite.evaluate(...)` — short-circuits at the first failing gate.
- `build_close_gate(...) -> GateSuite` — `format_predicate` (delegates to `tessellum.format.validate`) then `grounding_predicate` (reads a `GroundingVerdict`; `None`/`auth_blocked` → fail-closed FAIL).
- `build_wave_gate(...) -> GateSuite` — `duplicate_target_predicate` (exact-path dedup).
- `GroundingVerdict`, `GateResult`, `CompositeGateResult`, `DIGEST_GATES` (scope registry).

Gate-then-commit: the manifest row flips `done` and the `StepResult` is treated clean only after the gate passes; a FAIL becomes an errored/`blocked` result (never silently `done`).

## Fix loop (`fix.py`)

- `run_fix_loop(*, note_path, evaluate, fixer, max_rounds, cancellation_check=None, effect_guard=None, effect_recorder=None) -> FixLoopResult` — evaluate as-written (early-out if passing), checkpoint bytes+score before each fix, keep BEST snapshot (score = blocking-issue count, lower better), restore BEST on regression (`reverted=True`). Fixer crash = dead round, not a raise.
- `score_issues(issues) -> int` — blocking-issue count.
- `make_llm_fixer(backend, *, system_prompt=…, render_prompt=…, max_tokens=8000, encoding="utf-8", budget=None, cancellation_check=None, effect_guard=None, effect_recorder=None) -> InformedFixer` — reference in-place LLM repairer; the optional shared budget charges each repair call.
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
- `get_assembler(strategy: str = "full_source", *, max_chars=DEFAULT_MAX_CONTEXT_CHARS) -> ContextAssembler` — selects from `ASSEMBLER_REGISTRY`.
- `is_safe_read_path(path, *, workspace_root) -> bool` — fail-closed workspace confinement, secret-path rejection, and binary sniffing.

## Planning (`planning.py`)

- `content_fingerprint(source: str | bytes | Path) -> str`.
- `leaf_fingerprint(leaf: dict, *, source_key: str | None = None) -> str` — positional `_id` excluded.
- `partition_unchanged_leaves(leaves, prior_fingerprints, *, id_key="_id", source_key=None) -> (to_run, skipped, fresh_fingerprints)` — skip only on exact fingerprint match; new/changed/unkeyed always run.
- `should_skip_unchanged(leaf_id, source, prior_fingerprints) -> (skip, fingerprint)`.
- `classify_planning_depth(complexity: LeafComplexity) -> PlanningDepth` — returns `fast` or `full`, defaulting conservatively to `full`.

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

- `run_eval(scenarios: list[EvalScenario], *, backend, judge=None, dry_run=False) -> EvalResult` — structural assertions plus an optional `LLMJudge` rubric.
- `LLMJudge`, `JudgeScore`, `DEFAULT_RUBRIC_DIMENSIONS` (6-dim, overridable per scenario via `rubric_dimensions`).
- `Assertion`, `AssertionResult`, `EvalScenario`, `ScenarioResult`, `EvalError`, `load_scenario`, `load_scenarios`.

## Session-MCP (`session_mcp.py`)

Read-only tools over the active Claude Code transcript: `SESSION_MCP_TOOLS`, `get_session_metadata`, `get_tool_uses`, `read_recent_messages`, `resolve_transcript_path`, `search_transcript`.

## Knowledge-transaction track (P0–P9)

The additive layer that turns a multi-document digestion into one snapshot-pinned transaction: plan typed edits, stage them, prove them safe, publish atomically. Every phase is byte-identical when its opt-in path is off. Design narrative: [../composer.md](../composer.md#the-knowledge-transaction).

### Typed proposals + intent graph + overlay (P0–P3)

| Symbol | Kind | Role |
|---|---|---|
| `Effect` (`AddNote`/`UpdateNote`/`MergeNotes`/`DropNote`/`Reroute`/`AddReference`/`AddNavigation`) | frozen models | The seven typed change effects; each names the notes it touches. |
| `ChangeProposal` | frozen model | A named bundle of effects with a content-addressed identity. |
| `Footprint`, `effect_footprint`, `effect_key` | dataclass + fns | The set of notes/edges an effect touches; the conflict key merge uses. |
| `content_hash`, `canonical_json_bytes`, `plan_revision_hash` | functions | Deterministic content-addressing (float-in-payload rejected via `FloatInCanonicalPayloadError`). |
| `merge_proposals`, `merge_or_raise`, `MergeResult`, `MergeConflict`, `ProposalConflictError` | fns + types | Snapshot-pinned merge of two proposals; conflicts on overlapping footprints. |
| `collect_proposals` | function | Gather proposals from a source. |
| `NoteIntent` | frozen model | One planned note: `note_id`, `building_block`, `provenance: tuple[ClaimProvenance,…]`, `navigation` (entry points), `required_inlinks`, `depends_on`, `disposition`, `expected_preimage`. Validator enforces the **preimage rule** (create forbids preimage; update/merge/drop require it; skip is a no-op) + self-dep guard. |
| `NoteIntentGraph` | frozen model | The typed plan (a set of `NoteIntent`s); the transaction's unit of planning. |
| `ClaimProvenance` | frozen model | `span_id` + `source_ref` — a claim's citation. |
| `NoteDisposition` | Literal | `"create" | "update" | "merge" | "drop" | "skip"`. |
| `note_intent_content_id`, `project_note_intent_graph` | functions | Content id of an intent; projection of the graph into writer leaves. |
| `OverlayWriter`, `OverlayWriteResult`, `OverlayError` | class + types | Stages note writes into a delta off to the side; never mutates the base vault. |
| `OverlayIndex`, `DeltaState` | class + dataclass | Read-through view over base ⊕ delta: `note_by_id`/`all_notes`/`links_from`/`links_to`/counts + `ghost_links`/`resolves_ghost`. Update shadows, delete tombstones, re-author declares its own edges, `(source,target)` dupes collapse, `stage_add` un-tombstones. |

### Exact write closure (P4, `write_closure.py`)

| Symbol | Kind | Role | Signature / fields |
|---|---|---|---|
| `WriteEffect` | frozen dataclass | One mandatory write from a materialization invariant. | `note_id`, `kind: Literal["note","navigation","reverse_inlink","fz_inlink","index"]`, `origin`. |
| `WriteClosure` | frozen dataclass | The exact transactional write set. | `writes: tuple[WriteEffect,…]`; `touched_note_ids -> frozenset[str]`. |
| `BoundaryWitness` | frozen dataclass | Proof no write-propagating edge exits the set. | `ok: bool`, `escaping`, `unknown`. `ok` iff no escaping AND no unknown class. |
| `ClosurePolicy` | dataclass | Tunable bounds for the validation heuristic ONLY (never the write set). | `hub_threshold=50`, `validation_depth=2`, `spill_fraction=0.10`, `spill_abs=None`. |
| `ValidationResult` | frozen dataclass | Bounded set to RE-CHECK + spill flag. | `to_revalidate`, `spilled`, `size`, `bound`. `spilled = size > bound`; full set always returned. |
| `write_closure` | function | Exact write set; mandatory writes always included. | `write_closure(intents, *, entry_point_of=None) -> WriteClosure`. No hub/graph param. |
| `classify_edge` | function | Edge class from structural signals, not stored `link_type`. | source cat absent → `"unknown"`. Propagating = `{navigation, fz_parent, backlink}`. |
| `boundary_witness` | function | Prove no propagating edge escapes; fails closed on unknown. | `(closure, *, edges, note_category_of, fz_parent_of, reciprocal_pairs=None)`. |
| `validation_set` | function | Bounded reverse-reachability re-check; drops entry points, cuts at hubs, spills. | `bound = spill_abs or max(1, int(corpus_size*spill_fraction))`. |
| `partition_capsules` | function | Split intents into invariant-closed capsules (union-find over shared closures). | Same capsule iff closures overlap; deterministic, order-independent. |

### Versioned publication + snapshot CAS (P5, `publication.py`)

On-disk layout: `root/CURRENT` (pointer, swapped by one atomic `os.replace`), `root/generations/<gen>/` (immutable published), `root/staging/<gen>/` (prepared, invisible), a `COMMITTED` marker (written before the swap; the recovery keep/GC signal), an `ACKNOWLEDGED` marker, `capsule.json`, `.publish.lock`.

| Symbol | Kind | Role | Signature / fields |
|---|---|---|---|
| `ABSENT` | `str` sentinel | Read-set marker: a path's *absence* was relied on (phantom protection). | Used as a `read_set` value. |
| `VaultSnapshot` | frozen dataclass | Pinned base view at planning time; source of the CAS predicate. | `base_generation`, `index_hash`, `read_set: dict[str,str|ABSENT]`, `candidate_query_hashes`; `snapshot_id` (order-independent SHA-256). |
| `KnowledgeCapsule` | frozen dataclass | Binds a transaction's provenance to its exact write set. | `capsule_id`, `source_bundle_hash`, `vault_snapshot_id`, `knowledge_plan_hash`, `write_closure`, `preimage_hashes`, `postimage_hashes`; `well_formed(expected_closure) -> bool`. |
| `PublicationError` | exception | Protocol violation (unprepared/unpublished gen, path escape, reserved control filename). NOT raised for a CAS conflict. |
| `PublishResult` | frozen dataclass | Publish outcome. | `outcome: Literal["published","cas_conflict","blocked"]`, `generation`, `detail`. |
| `RetryPolicy` | dataclass | Bounds the CAS re-plan loop. | `max_attempts=3`. |
| `VersionedVault` | class | Generation-versioned root; the three-phase commit lives here. | `prepare(capsule, files)` (idempotent, fsync'd) → `publish(gen, *, expected_current, cas_check=None)` (compare+promote+swap under one lock) → `acknowledge(gen)`; `current_generation()` (read ONCE per reader); `recover(*, genesis_keep=None)` (under the publish lock); `collect_staging`/`collect_orphan_generations` (never touch CURRENT or a COMMITTED gen). |
| `publish_with_cas` | function | Bounded CAS-retry driver; terminates as `blocked`, never livelocks. | `(vault, generation, *, expected_current, snapshot, read_current, replan, policy=None)`. |
| `read_set_matches` | function | The CAS predicate closing the lost-update hazard. | True iff every read-set path still hashes the same AND every `ABSENT`-pinned path is still absent. |

### Structural supervised constructor (P6, `structural_gates.py`)

`build_structural_gate_suite()` runs, in order (all block on ERROR except the advisory relevance cap): `STRUCT-COVERAGE` (≥1 cited span), `STRUCT-PROVENANCE` (span + source per claim), `STRUCT-BB-ATOMIC` (exactly one BB), `STRUCT-DISPOSITION` (known effect class; unknown fails closed), `STRUCT-NAV-CLOSURE` (each declared entry point is a mandatory write), `STRUCT-INLINK-CLOSURE` (each required backlink is a write), `STRUCT-REF-INTEGRITY` (no dangling reference in base ⊕ delta; *skipped when no overlay supplied*), `STRUCT-LINK-RELEVANCE` (≤ cap, WARNING only).

| Symbol | Kind | Role | Fields / signature |
|---|---|---|---|
| `HumanApproval` | frozen dataclass | Sign-off artifact bound to one capsule id (no replay onto a mutated capsule). | `capsule_id`, `approver`, `signature`, `reason=""`. Signature is **presence-checked only** — crypto verification is the caller's job. |
| `StructuralGateContext` | frozen dataclass | The no-LLM read surface every predicate consumes. | `graph: NoteIntentGraph`, `overlay: OverlayIndex|None=None`, `write_closure: WriteClosure|None=None`, `relevance_link_cap=12`. |
| `SupervisedResult` | frozen dataclass | The admission decision. | `decision`, `structural_passed`, `first_failure_cause`, `detail`, `blocking_rules`. |
| `build_structural_gate_suite` | function | Build the ordered capsule-level suite. | `() -> GateSuite`. |
| `supervised_admit` | function | Publish iff suite passes AND a bound valid approval is present; else block (fail closed). | `(context, *, capsule_id, approval=None, suite=None) -> SupervisedResult`. |

`SupervisedResult.decision` states: `approved` (suite passed + bound valid approval — the only publish-eligible state), `blocked_structural` (suite failed; returned before the approval check), `blocked_needs_human` (structurally clean but no/mismatched/unsigned approval). Constant `DEFAULT_RELEVANCE_LINK_CAP = 12`.

### Calibrated semantic certificate (P7, `semantic_certificate.py`)

Injection contract `ClaimScorer = Callable[[list[Claim]], list[ClaimScore]]` — the real NLI/SummaC model is injected here; the module bundles no model, no corpus. Failure classes: `grounding`, `coverage`, `duplicate`, `edge_relevance`.

| Symbol | Kind | Role | Signature / fields |
|---|---|---|---|
| `Claim` | frozen dataclass | A checkable claim + its cited span, tagged with a failure class. | `claim_id`, `text`, `source_ref`, `failure_class="grounding"`. |
| `ClaimScore` | frozen dataclass | Per-claim score in [0,1]; `abstained` is fail-closed. | `claim_id`, `score`, `abstained=False`. |
| `ConformalThresholds` | frozen dataclass | Per-class cutoffs from calibration + audit metadata. | `thresholds`, `alpha`, `n_calibration`, `domains`; `threshold_for(cls)`. |
| `LabeledExample` | frozen dataclass | A calibration/eval example (`correct=True` ⇒ faithful). | `failure_class`, `score`, `correct`. |
| `calibrate` | function | LOWEST cutoff whose accepted-region empirical false-accept rate ≤ α, per class; infeasible → `1.01` (always abstain). Empirical **in-sample** bound (conformal-style), validated out-of-sample by `measure_false_accept_rate`. | `(examples, *, alpha, domains=()) -> ConformalThresholds`. |
| `certify` | function | Score claims, MIN-aggregate, accept/abstain fail-closed, emit `GroundingVerdict`. | `(claims, *, scorer, thresholds, note_domain=None) -> CertificateResult`. Abstains on empty set / out-of-domain / scorer abstain / below-threshold. |
| `measure_false_accept_rate` | function | The A7.5 gating measurement: per-class empirical FAR under the thresholds; must be below α on a real wrong-but-well-formed corpus before unattended gating. | `(examples, thresholds) -> dict[FailureClass, float]`. |

### Runnable certificate — C1–C4 (`lexical_scorer` / `claim_extraction` / `certificate_verifier` / `calibration_gate`)

Makes the P7 certificate runnable + A7.5-measurable with a reference baseline (design: [../semantic-certificate.md](../semantic-certificate.md)). The real NLI/SummaC model + labelled corpus remain external.

| Symbol | Kind | Role |
|---|---|---|
| `claim_support_score(claim_text, span_text) -> float` | function | **C1** — directional content-word containment in [0,1]. Bag-of-words; cannot judge negation/paraphrase (baseline only). |
| `make_lexical_scorer(span_text_of) -> ClaimScorer` | function | **C1** — a reference `ClaimScorer` from an injected `span_text_of(source_ref) -> str \| None`; unresolvable span → abstain (fail-closed). Drops into `certify(...)` / the DKS router in place of the real model. |
| `extract_claims(body, provenance, *, failure_class="grounding", note_id="note") -> list[Claim]` | function | **C2** — prose sentences → grounding claims cited against the union of sources; no provenance → `[]` (→ abstain). Drops frontmatter / fences / tables / link-only lines; deterministic `claim_id`s. |
| `split_sentences(body) -> list[str]` · `MULTI_SOURCE_SEP` | function · const | **C2** helpers. |
| `make_certificate_verifier(*, scorer, thresholds, body_of=…, provenance_of=…, note_domain_of=None) -> Callable[[step, leaf, result], GroundingVerdict]` | function | **C3** — builds the runtime `grounding_verifier` from the certificate (extract → certify → `result.verdict`). Opt-in (default byte-identical); skips malformed provenance rows without crashing. |
| `CorpusExample` · `CalibrationCorpus` | frozen dataclasses | **C4** — a labelled example (`example_id`, `failure_class`, `score`, `correct`, `domain`) and the corpus; `.split()` is a deterministic, stratified train/held-out split. |
| `run_calibration_gate(corpus, *, alpha, min_held_out=…, min_recall=…, min_held_out_per_class=…) -> CalibrationGateResult` | function | **C4** — the A7.5 go/no-go: fit on train, then on held-out require FAR ≤ α (SOUND) + recall ≥ min (USEFUL) + per-class evidence (SUFFICIENT). `unattended_ok` only when all three hold for every present class. |
| `CalibrationGateResult` | frozen dataclass | `unattended_ok`, `alpha`, `thresholds`, `held_out_far`, `held_out_recall`, `n_train`/`n_held_out`, `reasons`. |

### Bounded planner loop (P8, `planner_loop.py`)

| Symbol | Kind | Role | Fields / signature |
|---|---|---|---|
| `Deficit` | frozen dataclass | Deterministic ℕ progress variant; `total`=0 ⇒ discharged. Rejects negative components. | `ghosts`, `broken_links`, `undigested_terms`, `coverage_gaps` (all `int`); `total`, `as_tuple()`. |
| `Revision` | frozen dataclass | One planner revision + its route/contract signature. | `revision_id`, `route_signature`, `deficit`. |
| `LoopPolicy` | dataclass | The three hard stops + frozen-universe flag. | `depth_ceiling=8`, `fuel=16`, `oscillation_window=4`, `frozen_universe=True`. |
| `LoopResult` | frozen dataclass | Terminal outcome + trace. | `outcome: Literal["complete","blocked"]`, `revisions`, `reason`, `fuel_spent`; `deficit_trace`. |
| `run_planner_loop` | function | Drive the injected planner to a terminal state; never livelocks. | `(initial, *, propose, policy=None) -> LoopResult`. Completion (deficit 0) checked BEFORE any blocking rule. |

Blocking bounds (all → `blocked`): frozen-universe non-decrease, revision-depth ceiling, fuel budget, oscillation (consecutive non-progressing route reuse), planner returns `None`.

## Corpus digestion (`corpus_plan.py` + `corpus_digestion.py`)

The additive multi-document layer: a set of documents is fanned into one planning run and, above a volume threshold, decomposed into a master index + N self-contained sub-plans, each executed as its own transaction. Single-source `run_digestion_pipeline` is untouched. Design: [../digestion.md](../digestion.md#corpus-digestion--many-documents-one-coordinated-pass).

### Shape + plan model (`corpus_plan.py`)

| Symbol | Kind | Role |
|---|---|---|
| `PlanShape` | Literal | `"single_plan"` / `"single_plan_phased"` / `"master_plus_subplans"` (matches the plan skill enum). |
| `classify_plan_shape(total_words, est_note_count) -> PlanShape` | function | Volume → shape; the stronger axis wins. Thresholds: `SINGLE_PLAN_MAX_WORDS`/`PHASED_MAX_WORDS`, `SINGLE_PLAN_MAX_NOTES`/`PHASED_MAX_NOTES`. |
| `SubObjective` | frozen model | One sub-plan skeleton: `sub_id`, `topic`, `priority` (`P1`→`P3`), `member_ordinals` (its bundle slice), `est_note_count`, `depends_on`. Its `NoteIntentGraph` is filled at M3. |
| `CorpusPlan` | frozen model | Master index + sub-objectives; validates shape / unique ids / acyclic deps / term-owner / bundle partition. `master_index()` (derived, never stored), `wave_order()` (priority-major, dependency-respecting), `dependency_layers()` (ordered layers; cyclic → `ValueError`). |
| `SubObjectiveRow` | frozen model | One derived master-index row. |
| `TermOwnerRow` / `SharedCrossRef` | frozen models | `term` → `owner_sub_id`; a `target` + `relationship` every sub-plan links. |
| `corpus_plan_content_id(plan) -> str` | function | Order-stable id (reuses P0 `canonical_json_bytes`). |
| `build_corpus_leaf(bundle, member_contents) -> dict` | function | Windows each member HEAD/TAIL into one joint leaf (`members` + corpus keys); budgets the RENDERED size ≤ `DEFAULT_CORPUS_LEAF_MAX_CHARS`; fails loud on a member missing content. |
| `term_ownership_gate(plan, introduced_terms) -> TermOwnershipResult` | function | Fail-closed: every introduced term needs exactly one owner (else unowned / ambiguous / unknown / orphan is reported). |
| `resolve_shared_cross_refs(shared_cross_refs, *, exists=None) -> SharedCrossRefResolution` | function | Dedup by target (first wins); with an injected `exists(target)` predicate, drops refs to notes absent from the snapshot. Reports `dropped_missing` / `dropped_duplicate`. |

### Driver (`corpus_digestion.py`)

| Symbol | Kind | Role |
|---|---|---|
| `run_corpus_planning_wave(corpus_plan, bundle, member_contents, *, skills_dir, backend, vault_root, …, shared_cross_refs=None) -> CorpusPlanningResult` | function | Plans each sub-objective (slice → joint leaf → plan→augment→review→sign-off); NO execute. A rejected/failed sub-objective is blocked; the wave continues. |
| `run_corpus_digestion(corpus_plan, bundle, member_contents, *, skills_dir, backend, vault_root, …, introduced_terms=None, shared_cross_ref_exists=None, execute_max_workers=4, max_sub_plan_workers=1, **execute_kwargs) -> CorpusDigestionResult` | function | Term-ownership gate → planning wave → whole-corpus human gate → execute each accepted sub-plan as its own transaction in dependency-layer order. `max_sub_plan_workers > 1` runs a layer's independent sub-plans concurrently. |
| `SubPlanOutcome` / `CorpusPlanningResult` | frozen dataclasses | Per-sub-objective planning outcome (`accepted`, `plan_doc`, …) + the wave rollup (`all_accepted`, `accepted_count`, `blocked_count`). |
| `SubPlanExecution` / `CorpusDigestionResult` | frozen dataclasses | Per-sub-plan execute outcome (`promoted`, `status`, `run`) + the end result: `planning`, `corpus_sign_off`, `executions` (dependency-layer order), `term_ownership`, `shared_cross_refs`, `bundle_status` (`complete` / `partially_promoted` / `blocked`). |

## Package exports (`from tessellum.composer import …`)

`compile_skill`, `to_dag_json`, `CompiledPipeline`, `CompiledStep`, `CompilerError`; `load_pipeline`, `Pipeline`, `PipelineStep`, `PipelineValidationError`; `iter_step_sections`, `split_contract_and_prompt`, `load_skill_section`, `list_section_ids`, `StepSection`, `SkillExtractionError`; the contract families + registries + `ContractViolation`; `materialize`, `MaterializedOutput`, `MaterializerError`; the four backends + `LLMBackend`/`LLMRequest`/`LLMResponse`; `execute_step`, `execute_step_with_retry`, `classify_error`, `full_jitter_backoff`, `ErrorClass`, `StepResult`, `ExecutorError`, `MAX_LOGIC_RETRIES`, `MAX_CRASH_RECOVERIES`; `run_pipeline`, `run_pipeline_dynamic`, `RunResult`, `compute_ready_set`, `ReadySetState`, `SkipReason`, `StepOutcome`, `classify_outcome`; `Gate`, `GateResult`, `GateSuite`, `CompositeGateResult`, `GroundingVerdict`, `build_plan_gate`, `build_close_gate`, `build_wave_gate`, `DIGEST_GATES`; `run_digestion_pipeline`, `DigestionResult`, `PhaseOutcome`, `PHASE_SKILLS`; `run_fix_loop`, `make_llm_fixer`, `score_issues`, `FixContext`, `FixLoopResult`, `AttemptOutcome`; `partition_unchanged_leaves`, `should_skip_unchanged`, `content_fingerprint`, `leaf_fingerprint`, `classify_planning_depth`, `LeafComplexity`; `CredentialPool`, `RunBudget`, `classify_rotation_cause`, `effort_for_stage`, `DEFAULT_STAGE_EFFORT`, `CredentialPoolError`, `BudgetExhausted`; `ContextAssembler`, `FullSourceAssembler`, `WindowedAssembler`, `AssembledContext`, `get_assembler`, `is_safe_read_path`; `run_sign_off`, `SignOffPolicy`, `SignOffResult`, `AgentVerdict`; `build_skill_tool`, `SkillTool`, `CapabilityRegistry`, `RoutingKey`, `RouteDecision`, `McpDep`; `run_batch`, `BatchJob`, `BatchJobResult`, `BatchResult`; `Manifest`, `ManifestEntry`, `ArtifactRecord`, `AttemptRecord`, `ManifestError`, `MANIFEST_VERSION`, `VALID_STATUSES`; `run_eval`, `LLMJudge`, `JudgeScore`, `DEFAULT_RUBRIC_DIMENSIONS`, and the rest of the eval framework; the session-MCP surface. **Knowledge-transaction track (P0–P9):** the typed `Effect`s + `ChangeProposal` + merge/hash surface; `NoteIntent`, `NoteIntentGraph`, `NoteDisposition`, `ClaimProvenance`, `project_note_intent_graph`; `OverlayWriter`, `OverlayIndex`, `DeltaState`; `write_closure`, `boundary_witness`, `validation_set`, `partition_capsules` + their result types; `VersionedVault`, `VaultSnapshot`, `KnowledgeCapsule`, `publish_with_cas`, `read_set_matches`, `ABSENT`; `build_structural_gate_suite`, `supervised_admit`, `HumanApproval`, `StructuralGateContext`, `SupervisedResult`; `calibrate`, `certify`, `measure_false_accept_rate`, `Claim`, `ClaimScore`, `ConformalThresholds`, `LabeledExample`; `run_planner_loop`, `Deficit`, `Revision`, `LoopPolicy`, `LoopResult`. **Corpus digestion:** `run_execute_wave`; `PlanShape`, `classify_plan_shape`, `SubObjective`, `SubObjectivePriority`, `CorpusPlan`, `SubObjectiveRow`, `corpus_plan_content_id`, `build_corpus_leaf`, `term_ownership_gate`, `resolve_shared_cross_refs` + their result types; `run_corpus_planning_wave`, `CorpusPlanningResult`, `SubPlanOutcome`, `run_corpus_digestion`, `CorpusDigestionResult`, `SubPlanExecution`. **Runnable certificate (C1–C4):** `claim_support_score`, `make_lexical_scorer`, `extract_claims`, `split_sentences`, `MULTI_SOURCE_SEP`, `make_certificate_verifier`, `CorpusExample`, `CalibrationCorpus`, `CalibrationGateResult`, `run_calibration_gate`, `MIN_HELD_OUT`.

The DKS runtime is a **peer** module (`tessellum.dks`), not part of Composer, though it reuses Composer's `LLMBackend` abstractions.

## CLI — `tessellum composer <cmd>` (`cli/composer.py`)

Seven subcommands under one of Tessellum's 12 top-level CLI groups; `dks` is a peer group reusing Composer's `LLMBackend`:

| Command | Purpose | Flags |
|---------|---------|-------|
| `validate <skill\|dir>` | Validate each step section's contract block against the schema. | `--format human\|json` |
| `compile <skill>` | Compile to typed DAG, zero LLM. | `--output`, `--format`, `--no-prompts` |
| `run <skill>` | Execute against leaves. | see below |
| `batch <jobs.json>` | Many `(skill, leaves)` jobs in parallel with resume. | `--parallelism`, `--no-resume` |
| `eval <scenarios_dir>` | Assertions + `LLMJudge` rubric. | `--backend`, `--judge-backend` |
| `scaffold-sidecar <skill>` | Print a starter contract block per section anchor, to paste into the canonical. | `--stdout` |
| `digest --source <json>` | Run plan → augment → review → sign-off → execute. | `--skills-dir`, `--vault`, `--backend`, `--require-agent-signoff`, `--dry-run`, `--format` |

### `run` flags

Serial (always available): `--backend mock|anthropic|bedrock`, `--model`, `--region`, `--aws-profile`, `--leaves`, `--vault`, `--mock-responses`, `--dry-run`, `--no-trace`, `--runs-dir`, `--progress`, `--format`.

Dynamic path behind `--dynamic` (all ignored without it): `--workers` (default 4), `--manifest`, `--close-gate`, `--wave-gate`, `--fix-with-backend` (+ `--max-fix-rounds`, requires `--close-gate`), `--max-invocations`, `--max-cost`, `--stats`, `--context-strategy full_source|windowed` (+ `--context-max-chars`), `--skip-unchanged` (+ `--skip-unchanged-key`).

## Extension points

- **New materializer** — add a `MaterializerContract` subclass to `MATERIALIZER_CONTRACTS` + a handler in `materializer._DISPATCH`; the compiler validates against it automatically.
- **New backend** — implement the `LLMBackend` protocol (`backend_id` + `call`); optionally register an `LLMBackendContract` in `BACKEND_CONTRACTS` for compile-time tool-leakage/argv-overflow checks.
- **MCP contracts** — mutate `MCP_CONTRACTS` before compiling (ships `session-mcp` only). Compile-time `MCPContract` validation is data-only for now.
- **Context strategy** — subclass `ContextAssembler` (`strategy` + `_assemble_raw`), add to `ASSEMBLER_REGISTRY`; selected via `get_assembler`.
- **Gates** — add a pure `GatePredicate` + a `Gate` at the right scope; extend `build_plan_gate`/`build_close_gate`/`build_wave_gate` or the `DIGEST_GATES` registry.
- **Fixer** — provide any `FixContext -> object` callable to `run_fix_loop` / `run_pipeline_dynamic(informed_fixer=…)`; `make_llm_fixer` is the reference. The legacy `(step, leaf, issues)` `fixer` shape is still accepted (`informed_fixer` takes precedence).
- **Sign-off rungs** — inject `program_gate`/`agent_judge`/`human_prompt` + a `SignOffPolicy`.
- **Eval rubric** — override `DEFAULT_RUBRIC_DIMENSIONS` per scenario via `rubric_dimensions`; new assertion kinds slot into `_check_assertion`.

## Deferred / unwired

- **Cross-leaf scoping** — treated as `corpus_wide` in the scheduler.
- **APPLY-mode `{{existing.Z}}` pre-fetch** — not wired; the materializer reads existing files at write time.
- **Column-oriented batching** — deferred until backend pricing motivates it.
- **`applies_to_files_query` resolution** against the index DB — loader-accepted, resolved later by the compiler once the index is available.
- **`batch.py` runs over serial `run_pipeline`**, not the dynamic scheduler; resume is per-*job*, coarser than per-*leaf*.
