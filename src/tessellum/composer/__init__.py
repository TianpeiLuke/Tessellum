"""tessellum.composer — typed-contract pipeline runtime for skill-driven note construction.

Composer is the bridge between System P (capture) and System D (retrieval) —
a planner-centric orchestrator that compiles skill canonicals + pipeline.yaml
sidecars into typed DAGs of LLM calls.

The pairing is **two files per skill**:

- ``vault/resources/skills/skill_<name>.md``           — canonical procedure (markdown)
- ``vault/resources/skills/skill_<name>.pipeline.yaml`` — typed contract (YAML)

linked via ``<!-- :: section_id = X :: -->`` anchor comments and the
canonical's frontmatter ``pipeline_metadata:`` field.

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
    ExecutorError,
    StepResult,
    execute_step,
    execute_step_with_retry,
)
from tessellum.composer.llm import (
    AnthropicBackend,
    LLMBackend,
    LLMRequest,
    LLMResponse,
    MockBackend,
)
from tessellum.composer.loader import (
    Pipeline,
    PipelineStep,
    PipelineValidationError,
    load_pipeline,
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
from tessellum.composer.scheduler import RunResult, run_pipeline
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
    load_pipeline_metadata,
    load_skill_section,
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
    "load_pipeline_metadata",
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
    "run_pipeline",
    "RunResult",
    # Batch runner
    "BatchJob",
    "BatchJobResult",
    "BatchResult",
    "run_batch",
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
