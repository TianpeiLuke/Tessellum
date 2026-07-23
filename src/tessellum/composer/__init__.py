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
    "DigestionResult",
    "PhaseOutcome",
    "PHASE_SKILLS",
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
