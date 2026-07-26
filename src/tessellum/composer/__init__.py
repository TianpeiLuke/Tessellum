"""tessellum.composer — typed-contract pipeline runtime for skill-driven note construction.

Composer is the bridge between System P (capture) and System D (retrieval) —
a planner-centric orchestrator that compiles skill canonicals into typed DAGs
of LLM calls.

A skill is **one self-contained markdown file**:

- ``vault/resources/skills/skill_<name>.md`` — each pipeline step is an H2
  section with a ``<!-- :: section_id = X :: -->`` anchor, a leading
  ``​```yaml`` contract block (the typed step declaration), and the step's
  prompt prose. Prose-only sections (Setup, Resources, description) carry no
  contract block and are not pipeline steps. There is no separate
  ``.pipeline.yaml`` sidecar — contract and prompt live together in the
  section, so cross-file drift is structurally impossible.

Public API surface:

  - :func:`load_pipeline`, :class:`Pipeline`, :class:`ContractViolation` — loader + types
  - :func:`compile_skill`, :class:`CompiledPipeline`, :class:`CompilerError` — compiler
  - :func:`execute_step`, :func:`execute_step_with_retry`, :class:`StepResult` — executor
  - :func:`run_pipeline`, :class:`RunResult` — scheduler
  - :class:`LLMBackend`, :class:`MockBackend`, :class:`AnthropicBackend` — backends

Example::

    from tessellum.composer import compile_skill, run_pipeline, MockBackend
    pipeline = compile_skill(Path("vault/resources/skills/skill_foo.md"))
    result = run_pipeline(pipeline, leaves=[...], backend=MockBackend(), vault_root=...)
"""

from tessellum.composer.compiler import (
    CompiledPipeline,
    CompiledStep,
    CompilerError,
    compile_skill,
    to_dag_json,
)
from tessellum.composer.contracts import (
    BACKEND_CONTRACTS,
    BodyMarkdownFrontmatterToFileContract,
    BodyMarkdownToFileContract,
    ContractViolation,
    EditsApplyToFilesContract,
    EditsApplyXmlTagsContract,
    LLMBackendContract,
    MATERIALIZER_CONTRACTS,
    MCP_CONTRACTS,
    MCPContract,
    MaterializerContract,
    NoOpContract,
)
from tessellum.composer.executor import (
    MAX_CRASH_RECOVERIES,
    MAX_LOGIC_RETRIES,
    ErrorClass,
    ExecutorError,
    StepResult,
    classify_error,
    execute_step,
    execute_step_with_retry,
    full_jitter_backoff,
)
from tessellum.composer.llm import (
    AnthropicBackend,
    BedrockBackend,
    LLMBackend,
    LLMRequest,
    LLMResponse,
    MockBackend,
    PooledBackend,
)
from tessellum.composer.loader import (
    Pipeline,
    PipelineStep,
    PipelineValidationError,
    load_pipeline,
)
from tessellum.composer.manifest import (
    MANIFEST_VERSION,
    VALID_STATUSES,
    ArtifactRecord,
    AttemptRecord,
    Manifest,
    ManifestEntry,
    ManifestError,
)
from tessellum.composer.materializer import (
    MaterializedOutput,
    MaterializerError,
    materialize,
)
from tessellum.composer.batch import (
    BatchJob,
    BatchJobResult,
    BatchResult,
    run_batch,
)
from tessellum.composer.eval import (
    DEFAULT_RUBRIC_DIMENSIONS,
    Assertion,
    AssertionResult,
    EvalError,
    EvalResult,
    EvalScenario,
    JudgeScore,
    LLMJudge,
    ScenarioResult,
    load_scenario,
    load_scenarios,
    run_eval,
)
from tessellum.composer.context_assembler import (
    AssembledContext,
    ContextAssembler,
    FullSourceAssembler,
    WindowedAssembler,
    get_assembler,
    is_safe_read_path,
)
from tessellum.composer.credential_pool import (
    DEFAULT_STAGE_EFFORT,
    BudgetExhausted,
    CredentialPool,
    CredentialPoolError,
    RunBudget,
    classify_rotation_cause,
    effort_for_stage,
)
from tessellum.composer.fix import (
    AttemptOutcome,
    FixContext,
    FixLoopResult,
    make_llm_fixer,
    run_fix_loop,
    score_issues,
)
from tessellum.composer.gates import (
    DIGEST_GATES,
    CompositeGateResult,
    Gate,
    GateResult,
    GateSuite,
    GroundingVerdict,
    build_close_gate,
    build_plan_gate,
    build_wave_gate,
)
from tessellum.composer.planning import (
    LeafComplexity,
    classify_planning_depth,
    content_fingerprint,
    leaf_fingerprint,
    partition_unchanged_leaves,
    should_skip_unchanged,
)
from tessellum.composer.scheduler import (
    ReadySetState,
    RunResult,
    SkipReason,
    StepOutcome,
    classify_outcome,
    compute_ready_set,
    run_pipeline,
    run_pipeline_dynamic,
)
from tessellum.composer.digestion import (
    PHASE_SKILLS,
    DigestionResult,
    PhaseOutcome,
    run_digestion_pipeline,
    run_execute_wave,
)
from tessellum.composer.proposals import (
    AddNavigation,
    AddNote,
    AddReference,
    ChangeProposal,
    DropNote,
    Effect,
    FloatInCanonicalPayloadError,
    Footprint,
    MergeConflict,
    MergeNotes,
    MergeResult,
    ProposalConflictError,
    Reroute,
    UpdateNote,
    canonical_json_bytes,
    collect_proposals,
    content_hash,
    effect_footprint,
    effect_key,
    merge_or_raise,
    merge_proposals,
    plan_revision_hash,
)
from tessellum.composer.corpus_digestion import (
    CorpusDigestionResult,
    CorpusPlanningResult,
    SubPlanExecution,
    SubPlanOutcome,
    run_corpus_digestion,
    run_corpus_planning_wave,
)
from tessellum.composer.corpus_plan import (
    DEFAULT_CORPUS_LEAF_MAX_CHARS,
    PHASED_MAX_NOTES,
    PHASED_MAX_WORDS,
    SINGLE_PLAN_MAX_NOTES,
    SINGLE_PLAN_MAX_WORDS,
    CorpusPlan,
    MemberExcerpt,
    PlanShape,
    SharedCrossRef,
    SharedCrossRefResolution,
    SubObjective,
    SubObjectivePriority,
    SubObjectiveRow,
    TermOwnerRow,
    TermOwnershipResult,
    build_corpus_leaf,
    classify_plan_shape,
    corpus_plan_content_id,
    resolve_shared_cross_refs,
    term_ownership_gate,
)
from tessellum.composer.knowledge_plan import (
    ClaimProvenance,
    NoteDisposition,
    NoteIntent,
    NoteIntentGraph,
    note_intent_content_id,
    project_note_intent_graph,
)
from tessellum.composer.overlay import (
    OverlayError,
    OverlayWriteResult,
    OverlayWriter,
)
from tessellum.composer.overlay_index import (
    DeltaState,
    OverlayIndex,
)
from tessellum.composer.write_closure import (
    BoundaryWitness,
    ClosurePolicy,
    ValidationResult,
    WriteClosure,
    WriteEffect,
    boundary_witness,
    classify_edge,
    partition_capsules,
    validation_set,
    write_closure,
)
from tessellum.composer.publication import (
    ABSENT,
    KnowledgeCapsule,
    PublicationError,
    PublishResult,
    RetryPolicy,
    VaultSnapshot,
    VersionedVault,
    publish_with_cas,
    read_set_matches,
)
from tessellum.composer.structural_gates import (
    HumanApproval,
    StructuralGateContext,
    SupervisedResult,
    build_structural_gate_suite,
    supervised_admit,
)
from tessellum.composer.semantic_certificate import (
    Claim,
    ClaimScore,
    ConformalThresholds,
    LabeledExample,
    calibrate,
    certify,
    measure_false_accept_rate,
)
from tessellum.composer.lexical_scorer import (
    claim_support_score,
    make_lexical_scorer,
)
from tessellum.composer.claim_extraction import (
    MULTI_SOURCE_SEP,
    extract_claims,
    split_sentences,
)
from tessellum.composer.certificate_verifier import make_certificate_verifier
from tessellum.composer.calibration_gate import (
    MIN_HELD_OUT,
    CalibrationCorpus,
    CalibrationGateResult,
    CorpusExample,
    run_calibration_gate,
)
from tessellum.composer.planner_loop import (
    Deficit,
    LoopPolicy,
    LoopResult,
    Revision,
    run_planner_loop,
)
from tessellum.composer.signoff import (
    AgentVerdict,
    SignOffPolicy,
    SignOffResult,
    run_sign_off,
)
from tessellum.composer.skill_tool import (
    CapabilityRegistry,
    McpDep,
    RouteDecision,
    RoutingKey,
    SkillTool,
    build_skill_tool,
)
from tessellum.composer.session_mcp import (
    SESSION_MCP_TOOLS,
    get_session_metadata,
    get_tool_uses,
    read_recent_messages,
    resolve_transcript_path,
    search_transcript,
)
from tessellum.composer.skill_extractor import (
    SkillExtractionError,
    StepSection,
    iter_step_sections,
    list_section_ids,
    load_skill_section,
    split_contract_and_prompt,
)

__all__ = [
    # Contracts
    "MaterializerContract",
    "BodyMarkdownToFileContract",
    "BodyMarkdownFrontmatterToFileContract",
    "EditsApplyToFilesContract",
    "EditsApplyXmlTagsContract",
    "NoOpContract",
    "MATERIALIZER_CONTRACTS",
    "LLMBackendContract",
    "BACKEND_CONTRACTS",
    "MCPContract",
    "MCP_CONTRACTS",
    "ContractViolation",
    # Pipeline models + loader
    "Pipeline",
    "PipelineStep",
    "load_pipeline",
    "PipelineValidationError",
    # Skill extractor
    "load_skill_section",
    "split_contract_and_prompt",
    "iter_step_sections",
    "list_section_ids",
    "StepSection",
    "SkillExtractionError",
    # Compiler
    "compile_skill",
    "CompiledPipeline",
    "CompiledStep",
    "CompilerError",
    "to_dag_json",
    # LLM backends
    "LLMBackend",
    "LLMRequest",
    "LLMResponse",
    "MockBackend",
    "AnthropicBackend",  # requires the ``[agent]`` extras
    "BedrockBackend",  # requires the ``[agent]`` extras + AWS creds
    "PooledBackend",  # wraps a backend with a CredentialPool
    # Materializers
    "materialize",
    "MaterializedOutput",
    "MaterializerError",
    # Executor + scheduler
    "execute_step",
    "execute_step_with_retry",
    "MAX_LOGIC_RETRIES",
    "MAX_CRASH_RECOVERIES",
    "StepResult",
    "ExecutorError",
    # Error classification + backoff (Phase 1.4, v4)
    "classify_error",
    "full_jitter_backoff",
    "ErrorClass",
    "run_pipeline",
    "run_pipeline_dynamic",
    "RunResult",
    "compute_ready_set",
    "ReadySetState",
    "SkipReason",
    "StepOutcome",
    "classify_outcome",
    # Gate engine (Phase 3)
    "Gate",
    "GateResult",
    "GateSuite",
    "CompositeGateResult",
    "GroundingVerdict",
    "build_close_gate",
    "build_plan_gate",
    "build_wave_gate",
    "DIGEST_GATES",
    # Fix stage + planner economics (Phase 4)
    "FixContext",
    "FixLoopResult",
    "AttemptOutcome",
    "run_fix_loop",
    "make_llm_fixer",
    "score_issues",
    "LeafComplexity",
    "classify_planning_depth",
    "content_fingerprint",
    "should_skip_unchanged",
    "leaf_fingerprint",
    "partition_unchanged_leaves",
    # Credential pool + budgets (Phase 5)
    "CredentialPool",
    "CredentialPoolError",
    "classify_rotation_cause",
    "RunBudget",
    "BudgetExhausted",
    "effort_for_stage",
    "DEFAULT_STAGE_EFFORT",
    # Context assembler + sign-off approver (Phase 6)
    "ContextAssembler",
    "FullSourceAssembler",
    "WindowedAssembler",
    "AssembledContext",
    "get_assembler",
    "is_safe_read_path",
    "SignOffPolicy",
    "SignOffResult",
    "AgentVerdict",
    "run_sign_off",
    # Digestion phase driver (plan → augment → review → execute)
    "run_digestion_pipeline",
    "run_execute_wave",
    "DigestionResult",
    "PhaseOutcome",
    "PHASE_SKILLS",
    # Typed change proposals + snapshot-pinned merge/hash (P0)
    "AddNote",
    "UpdateNote",
    "MergeNotes",
    "DropNote",
    "Reroute",
    "AddReference",
    "AddNavigation",
    "Effect",
    "ChangeProposal",
    "Footprint",
    "effect_footprint",
    "effect_key",
    "content_hash",
    "canonical_json_bytes",
    "FloatInCanonicalPayloadError",
    "ProposalConflictError",
    "MergeConflict",
    "MergeResult",
    "plan_revision_hash",
    "merge_proposals",
    "merge_or_raise",
    "collect_proposals",
    # Typed knowledge-plan intent graph + writer-leaf projection (P2, A2.3/A2.4)
    "ClaimProvenance",
    "NoteDisposition",
    "NoteIntent",
    "NoteIntentGraph",
    "note_intent_content_id",
    "project_note_intent_graph",
    # corpus_plan (M1 + M2)
    "PlanShape",
    "SINGLE_PLAN_MAX_WORDS",
    "PHASED_MAX_WORDS",
    "SINGLE_PLAN_MAX_NOTES",
    "PHASED_MAX_NOTES",
    "classify_plan_shape",
    "SubObjectivePriority",
    "SubObjective",
    "TermOwnerRow",
    "SharedCrossRef",
    "CorpusPlan",
    "SubObjectiveRow",
    "corpus_plan_content_id",
    "TermOwnershipResult",
    "term_ownership_gate",
    "SharedCrossRefResolution",
    "resolve_shared_cross_refs",
    "DEFAULT_CORPUS_LEAF_MAX_CHARS",
    "MemberExcerpt",
    "build_corpus_leaf",
    # corpus_digestion (M3 + M4)
    "SubPlanOutcome",
    "CorpusPlanningResult",
    "run_corpus_planning_wave",
    "SubPlanExecution",
    "CorpusDigestionResult",
    "run_corpus_digestion",
    # Create-only staging overlay writer (P2, A2.5)
    "OverlayWriter",
    "OverlayError",
    "OverlayWriteResult",
    # Read-through overlay index over base ⊕ delta (P3, A3.1/A3.2)
    "OverlayIndex",
    "DeltaState",
    # Exact write closure + validation heuristic + partition (P4, A4.2-A4.5)
    "WriteEffect",
    "WriteClosure",
    "BoundaryWitness",
    "ClosurePolicy",
    "ValidationResult",
    "write_closure",
    "classify_edge",
    "boundary_witness",
    "validation_set",
    "partition_capsules",
    # Versioned publication + snapshot CAS (P5, A5.1-A5.4)
    "VaultSnapshot",
    "KnowledgeCapsule",
    "VersionedVault",
    "PublicationError",
    "PublishResult",
    "RetryPolicy",
    "read_set_matches",
    "publish_with_cas",
    "ABSENT",
    # Structural supervised constructor (P6, A6.1/A6.2)
    "StructuralGateContext",
    "build_structural_gate_suite",
    "HumanApproval",
    "SupervisedResult",
    "supervised_admit",
    # Calibrated semantic certificate (P7, A7.2-A7.5)
    "Claim",
    "ClaimScore",
    "ConformalThresholds",
    "LabeledExample",
    "calibrate",
    "certify",
    "measure_false_accept_rate",
    # semantic certificate — runnable pieces (C1-C4)
    "claim_support_score",
    "make_lexical_scorer",
    "MULTI_SOURCE_SEP",
    "extract_claims",
    "split_sentences",
    "make_certificate_verifier",
    "CalibrationCorpus",
    "CalibrationGateResult",
    "CorpusExample",
    "MIN_HELD_OUT",
    "run_calibration_gate",
    # Bounded planner search (P8, A8.1-A8.3)
    "Deficit",
    "Revision",
    "LoopPolicy",
    "LoopResult",
    "run_planner_loop",
    # Skills-as-tools + capability registry
    "SkillTool",
    "build_skill_tool",
    "CapabilityRegistry",
    "RoutingKey",
    "RouteDecision",
    "McpDep",
    # Batch runner
    "BatchJob",
    "BatchJobResult",
    "BatchResult",
    "run_batch",
    # Resume manifest (Composer v4, Phase 1)
    "Manifest",
    "ManifestEntry",
    "ArtifactRecord",
    "AttemptRecord",
    "ManifestError",
    "MANIFEST_VERSION",
    "VALID_STATUSES",
    # Eval framework
    "DEFAULT_RUBRIC_DIMENSIONS",
    "Assertion",
    "AssertionResult",
    "EvalError",
    "EvalResult",
    "EvalScenario",
    "JudgeScore",
    "LLMJudge",
    "ScenarioResult",
    "load_scenario",
    "load_scenarios",
    "run_eval",
    # Session-MCP (read the active Claude Code transcript)
    "SESSION_MCP_TOOLS",
    "get_session_metadata",
    "get_tool_uses",
    "read_recent_messages",
    "resolve_transcript_path",
    "search_transcript",
    # NOTE: the DKS (Dialectic Knowledge System) runtime is a peer
    # module — import from :mod:`tessellum.dks` directly. DKS uses
    # Composer's LLMBackend abstractions but is not part of Composer.
]
