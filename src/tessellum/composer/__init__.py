"""tessellum.composer — typed-contract pipeline runtime for skill-driven note construction.

Composer is the bridge between System P (capture) and System D (retrieval) —
a planner-centric orchestrator that compiles skill canonicals + pipeline.yaml
sidecars into typed DAGs of LLM calls. See ``plans/plan_composer_port.md`` in
the source repo for the full architecture.

The pairing is **two files per skill**:

- ``vault/resources/skills/skill_<name>.md``         — canonical procedure (markdown)
- ``vault/resources/skills/skill_<name>.pipeline.yaml`` — typed contract (YAML)

linked via ``<!-- :: section_id = X :: -->`` anchor comments and the
canonical's frontmatter ``pipeline_metadata:`` field.

**v0.0.9 — Wave 1 (Foundation, this release)**:

Pure data + library. No CLI, no LLM dispatch, no compiler. The library lets
you load and validate sidecars in Python:

    from tessellum.composer import load_pipeline, Pipeline, ContractViolation
    pipeline = load_pipeline(Path("vault/resources/skills/skill_foo.md"))

**Future waves**:

- v0.0.10 — Wave 1 user-facing surface: ``tessellum composer validate`` CLI,
  starter sidecar template, ``tessellum capture skill`` paired-sidecar emission.
- Wave 2 — Compiler (DAG build, contract validation, zero LLM calls).
- Wave 3 — Executor (placeholder resolution, materializer dispatch, runtime).
- Wave 4 — LLM bridge (Anthropic SDK + optional MCP dispatcher).
- Wave 5+ — Scale (batch runner, eval framework).
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
    ExecutorError,
    StepResult,
    execute_step,
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
from tessellum.composer.scheduler import RunResult, run_pipeline
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
    # Compiler (Wave 2)
    "compile_skill",
    "CompiledPipeline",
    "CompiledStep",
    "CompilerError",
    "to_dag_json",
    # LLM backend (Wave 3)
    "LLMBackend",
    "LLMRequest",
    "LLMResponse",
    "MockBackend",
    # LLM backend (Wave 4 — requires [agent] extras)
    "AnthropicBackend",
    # Materializers (Wave 3)
    "materialize",
    "MaterializedOutput",
    "MaterializerError",
    # Executor + scheduler (Wave 3)
    "execute_step",
    "StepResult",
    "ExecutorError",
    "run_pipeline",
    "RunResult",
    # Batch runner (Wave 5a)
    "BatchJob",
    "BatchJobResult",
    "BatchResult",
    "run_batch",
]
