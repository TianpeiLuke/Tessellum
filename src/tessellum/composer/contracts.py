"""Typed producer/consumer contracts for the Composer's runtime layers.

Three contract families:

- **MaterializerContract** — declares wire_format + operation_verb +
  required_output_fields per materializer. The compiler walks each step's
  canonical against the materializer's contract and refuses to compile on
  drift.
- **LLMBackendContract** — declares an LLM backend's capabilities (tool
  surface, max user-message size, batching support). Catches D4-a tool
  leakage and argv-overflow at compile time.
- **MCPContract** — declares an MCP server's exposed tools, auth posture,
  rate limit. The compiler asserts every step's declared `mcp_dependencies`
  resolves against the registry.

Each is a frozen Pydantic V2 model. Concrete instances live in module-level
registries (`MATERIALIZER_CONTRACTS`, `BACKEND_CONTRACTS`, `MCP_CONTRACTS`).

:class:`ContractViolation` is the exception raised by the compiler when
declarations drift. Defined here so library users can catch it the same
way they import the contract types.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ── Enums (Literal types) ──────────────────────────────────────────────────

WireFormat = Literal["json", "markdown_with_frontmatter", "xml_tag_list", "none"]
OperationVerb = Literal["PRODUCE", "APPLY", "DESCRIBE"]


# ── MaterializerContract + concrete subclasses ─────────────────────────────


class MaterializerContract(BaseModel):
    """Declarative contract for a materializer's producer/consumer I/O.

    Subclasses bind concrete defaults for each materializer key. The
    compiler walks each step's canonical against the materializer's contract
    and refuses to compile on drift.

    All fields are immutable post-construction (frozen). Contract objects
    are singleton-like and shared across all step instances using the same
    materializer.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    materializer_key: str = Field(
        ...,
        description="Registry key matching the entry in MATERIALIZER_CONTRACTS.",
    )
    version: str = Field(
        default="1.0",
        description="Explicit contract version. Increment when any field "
        "default changes in a way that affects validation.",
    )
    wire_format: WireFormat = Field(
        ...,
        description="Structural shape of the agent's response: 'json', "
        "'markdown_with_frontmatter', 'xml_tag_list', or 'none'.",
    )
    operation_verb: OperationVerb = Field(
        ...,
        description="What the agent's response semantically commits to: "
        "PRODUCE (write new), APPLY (overwrite existing), DESCRIBE "
        "(informational, no side effect).",
    )
    requires_tool_free_backend: bool = Field(
        default=True,
        description="If True, the LLM backend MUST have no tool access. The "
        "materializer is the only legitimate side-effect channel; agents "
        "bypassing it produce undocumented writes.",
    )
    requires_existing_files: bool = Field(
        default=False,
        description="If True, the step MUST declare a non-empty "
        "`applies_to_files` list AND its prompt_template MUST reference "
        "{{existing.<path>}} for each declared file. True for APPLY-mode.",
    )
    apply_mode_directive_required: bool = Field(
        default=False,
        description="If True, the prompt_template MUST contain the literal "
        "phrase 'APPLY mode' to disambiguate APPLY vs DESCRIBE for the agent.",
    )
    required_output_fields: tuple[str, ...] = Field(
        default=(),
        description="Fields the agent's response must contain. Used by the "
        "compiler to verify the prompt_template instructs the agent to emit "
        "each field. Tuple (not list) so the model stays hashable + frozen.",
    )


class BodyMarkdownToFileContract(MaterializerContract):
    """Legacy JSON wire format for body writes.

    Kept for back-compat. New canonicals should use
    ``body_markdown_frontmatter_to_file``.
    """

    materializer_key: str = "body_markdown_to_file"
    version: str = "1.0"
    wire_format: WireFormat = "json"
    operation_verb: OperationVerb = "PRODUCE"
    requires_tool_free_backend: bool = True
    requires_existing_files: bool = False
    apply_mode_directive_required: bool = False
    required_output_fields: tuple[str, ...] = ("output_path", "body_markdown")


class BodyMarkdownFrontmatterToFileContract(MaterializerContract):
    """Markdown-with-frontmatter wire format.

    Agent emits ``---\\noutput_path: ...\\n---\\n<body>`` directly. No JSON-
    escape drift surface for natural-language content.
    """

    materializer_key: str = "body_markdown_frontmatter_to_file"
    version: str = "1.0"
    wire_format: WireFormat = "markdown_with_frontmatter"
    operation_verb: OperationVerb = "PRODUCE"
    requires_tool_free_backend: bool = True
    requires_existing_files: bool = False
    apply_mode_directive_required: bool = False
    required_output_fields: tuple[str, ...] = ("output_path",)


class EditsApplyToFilesContract(MaterializerContract):
    """Legacy JSON wire format for edits-apply.

    Prone to operation-verb drift (agent emits status report instead of
    patches). Deprecated in favor of ``edits_apply_xml_tags``.
    """

    materializer_key: str = "edits_apply_to_files"
    version: str = "1.0"
    wire_format: WireFormat = "json"
    operation_verb: OperationVerb = "APPLY"
    requires_tool_free_backend: bool = True
    requires_existing_files: bool = True
    apply_mode_directive_required: bool = False
    required_output_fields: tuple[str, ...] = ("edits",)


class EditsApplyXmlTagsContract(MaterializerContract):
    """XML tag list with APPLY-mode prompt directive.

    Agent emits ``<edits><edit><file>...</file><content>...</content></edit></edits>``
    with the prompt explicitly instructing APPLY (not DESCRIBE).
    """

    materializer_key: str = "edits_apply_xml_tags"
    version: str = "1.0"
    wire_format: WireFormat = "xml_tag_list"
    operation_verb: OperationVerb = "APPLY"
    requires_tool_free_backend: bool = True
    requires_existing_files: bool = True
    apply_mode_directive_required: bool = True
    required_output_fields: tuple[str, ...] = ("edits",)


class NoOpContract(MaterializerContract):
    """Informational steps — no filesystem side effect.

    Examples: pre-flight check verdicts, atomicity decisions, research
    findings consumed by downstream steps. Output is structured JSON but
    no file is written.
    """

    materializer_key: str = "no_op"
    version: str = "1.0"
    wire_format: WireFormat = "json"
    operation_verb: OperationVerb = "DESCRIBE"
    requires_tool_free_backend: bool = True
    requires_existing_files: bool = False
    apply_mode_directive_required: bool = False
    required_output_fields: tuple[str, ...] = ()


MATERIALIZER_CONTRACTS: dict[str, MaterializerContract] = {
    "body_markdown_to_file": BodyMarkdownToFileContract(),
    "body_markdown_frontmatter_to_file": BodyMarkdownFrontmatterToFileContract(),
    "edits_apply_to_files": EditsApplyToFilesContract(),
    "edits_apply_xml_tags": EditsApplyXmlTagsContract(),
    "no_op": NoOpContract(),
}


# ── ContractViolation exception ────────────────────────────────────────────


class ContractViolation(Exception):
    """Raised by the compiler when a step's canonical declaration drifts
    from its materializer / backend / MCP contract.

    The exception message is actionable: identifies the step, the violation
    kind, what was found, what was expected, and a suggested fix.
    """

    KIND_UNKNOWN_MATERIALIZER = "UNKNOWN_MATERIALIZER"
    KIND_WIRE_FORMAT_MISMATCH = "WIRE_FORMAT_MISMATCH"
    KIND_MISSING_REQUIRED_OUTPUT_FIELD = "MISSING_REQUIRED_OUTPUT_FIELD"
    KIND_MISSING_APPLY_DIRECTIVE = "MISSING_APPLY_DIRECTIVE"
    KIND_APPLY_WITHOUT_GROUND_TRUTH = "APPLY_WITHOUT_GROUND_TRUTH"
    KIND_EXISTING_PATH_NOT_REFERENCED = "EXISTING_PATH_NOT_REFERENCED"
    KIND_BACKEND_HAS_TOOLS = "BACKEND_HAS_TOOLS"
    KIND_ARGV_OVERFLOW_EXPECTED = "ARGV_OVERFLOW_EXPECTED"
    KIND_UNKNOWN_MCP = "UNKNOWN_MCP"
    KIND_UNKNOWN_MCP_TOOL = "UNKNOWN_MCP_TOOL"

    def __init__(
        self,
        step_id: str,
        kind: str,
        message: str,
        suggested_fix: str | None = None,
    ) -> None:
        self.step_id = step_id
        self.kind = kind
        self.message = message
        self.suggested_fix = suggested_fix
        full = f"step {step_id!r} contract violation [{kind}]: {message}"
        if suggested_fix:
            full += f"\n  → fix: {suggested_fix}"
        super().__init__(full)


# ── LLMBackendContract ─────────────────────────────────────────────────────


class LLMBackendContract(BaseModel):
    """Declarative contract for an LLM backend's capabilities.

    Catches tool-leakage (when a materializer requires a tool-free backend
    but the configured backend has tool access) and subprocess argv-overflow
    at compile time.

    The default registry ships ``mock`` (for testing) plus the
    ``anthropic`` bridge under the ``[agent]`` extras.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    backend_id: str = Field(..., description="Stable backend identifier.")
    version: str = Field(default="1.0", description="Explicit contract version.")
    allowed_tools: tuple[str, ...] = Field(
        default=(),
        description="Tools the backend permits the agent to call. Empty "
        "tuple = tool-free (no Read/Write/Bash/MCP). Materializers that "
        "declare requires_tool_free_backend=True compile-error against any "
        "backend with allowed_tools != ().",
    )
    max_user_message_chars: int = Field(
        ...,
        description="Subprocess argv has a hard OS limit (~256KB on macOS). "
        "Set conservatively below the OS limit for CLI-based backends. Use "
        "a very large value for SDK / mock backends.",
    )
    requires_tempfile_for_long_prompts: bool = Field(
        default=False,
        description="If True, the scheduler MUST pass the system prompt via "
        "a tempfile rather than via argv. True for CLI-based backends to "
        "avoid argv overflow.",
    )
    supports_batched_dispatch: bool = Field(
        default=True,
        description="If True, the backend can handle batched per_leaf "
        "dispatch (one call with N items, JSON-envelope response). Most "
        "backends do; mock may not.",
    )


BACKEND_CONTRACTS: dict[str, LLMBackendContract] = {
    "mock": LLMBackendContract(
        backend_id="mock",
        allowed_tools=(),
        max_user_message_chars=10_000_000,
        requires_tempfile_for_long_prompts=False,
        supports_batched_dispatch=True,
    ),
}


# ── MCPContract ────────────────────────────────────────────────────────────


class MCPContract(BaseModel):
    """Declarative contract for an MCP server's capabilities.

    The compiler asserts every step's declared ``mcp_dependencies`` resolves
    against the ``MCP_CONTRACTS`` registry, and that each tool name in
    ``mcp_dependencies[].calls`` is in this contract's ``available_tools``.

    Tessellum ships with an empty registry — no built-in MCPs. Library users
    register their own MCPContract instances at runtime by populating the
    ``MCP_CONTRACTS`` dict before invoking the compiler.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(
        ...,
        description="Stable MCP identifier; matches the MCP_CONTRACTS key "
        "AND the mcp_dependencies[].name pattern in pipeline.schema.json.",
    )
    version: str = Field(default="1.0", description="Contract version.")
    available_tools: tuple[str, ...] = Field(
        default=(),
        description="Tool names this MCP exposes. The compiler validates "
        "step.mcp_dependencies[*].calls entries against this list.",
    )
    auth_required: bool = Field(
        default=True,
        description="If True, the dispatcher must verify auth context "
        "before any LLM call that depends on this MCP.",
    )
    rate_limit_qps: float | None = Field(
        default=None,
        description="If set, dispatcher enforces a per-second cap on calls. "
        "None = no documented rate limit.",
    )
    fallback_strategy: Literal[
        "fail_fast", "degrade", "retry_then_fail"
    ] = Field(
        default="fail_fast",
        description="What the dispatcher does on transient MCP error. "
        "fail_fast = bubble error immediately; degrade = return a degraded "
        "result and let the prompt's degradation branch handle absence; "
        "retry_then_fail = exponential backoff up to N retries.",
    )


MCP_CONTRACTS: dict[str, MCPContract] = {
    "session-mcp": MCPContract(
        name="session-mcp",
        version="1.0",
        available_tools=(
            "get_session_metadata",
            "get_tool_uses",
            "read_recent_messages",
            "search_transcript",
        ),
        auth_required=False,        # local-only — reads the active transcript file
        rate_limit_qps=None,        # local read; no upstream quota
        fallback_strategy="degrade",   # if transcript can't be located, return degraded result
    ),
}
"""Built-in MCP contracts. Tessellum ships ``session-mcp`` (read-only
access to the active Claude Code transcript, implemented in
:mod:`tessellum.composer.session_mcp`). Library users add their own MCPs
by mutating this dict before invoking the compiler.
"""
