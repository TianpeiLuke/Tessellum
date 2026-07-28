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

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

# ── Enums (Literal types) ──────────────────────────────────────────────────

WireFormat = Literal["json", "markdown_with_frontmatter", "xml_tag_list", "none"]
OperationVerb = Literal["PRODUCE", "APPLY", "DESCRIBE"]


# ── PlanDoc — the thin typed dataflow envelope (P22; FZ 20k9c1a1a1b7c2f) ─────

# The plan-skill output keys the gate + downstream steps read under canonical
# names, mapped from the write-plan materializer's aliases. The SINGLE source of
# truth for the E6 bridge — previously a private dict in digestion.py.
_PLAN_DOC_KEY_ALIASES: dict[str, tuple[str, ...]] = {
    "plan_path": ("output_path",),
    "plan_text": ("body_markdown",),
    "total_notes": ("planned_note_count", "estimated_note_count"),
}

# The large, durable artifacts that travel between digestion phases BY REFERENCE
# (P21-full; FZ 20k9c1a1a1b7c2j) — the driver injects them into a consumer's
# prompt via the ``{{artifact.X}}`` namespace instead of a step re-emitting them
# through the LLM (lossy by construction). The SINGLE source of truth shared by
# the driver's artifact store (``digestion``) and the compiler's re-emission
# lint (``compiler``); keep them in lockstep from here.
_ARTIFACT_KEYS: tuple[str, ...] = ("plan_text", "source_excerpt", "planned_notes")


class PlanDoc(BaseModel):
    """A thin typed envelope over the digestion ``plan_doc`` dataflow.

    **NOT** a rigid plan spine (the demoted P6/P7 ``NoteIntentGraph`` is a
    separate, still-dead-on-the-native-path thing). This is the *light dataflow
    type* the design review (FZ 20k9c1a1a1b7c2f) called for: it folds the three
    scattered plan-of-record guards that lived as imperative code in
    ``digestion._normalize_plan_doc_keys`` into one validated construction —

    1. the **E6 alias bridge** (``output_path``→``plan_path``,
       ``body_markdown``→``plan_text``, ``planned_note_count`` /
       ``estimated_note_count``→``total_notes``),
    2. the **longest-of ``plan_text`` guard** (a lossy re-emission can't shrink
       the plan of record below the authoritative ``body_markdown``), and
    3. the **P21-core ``total_notes`` floor** (you cannot declare fewer notes
       than you enumerated in ``planned_notes``).

    ``extra="allow"`` (the ``loader.PipelineStep`` precedent) so the ~dozen
    non-envelope keys a real plan carries (``members``, ``routing_decision``,
    ``note_intent_graph``, ``execute_leaves``, ``section_coverage_map``, …)
    round-trip untouched. It is adopted ONLY at the ``_normalize_plan_doc_keys``
    boundary as a validating constructor: :meth:`from_dict` runs the folds,
    :meth:`to_normalized_dict` writes the canonical values back; ``plan_doc``
    stays a plain mutable ``dict`` everywhere else (so the ~15 ``setdefault`` /
    ``clear`` / ``update`` / ``[]=`` sites — incl. the P24 snapshot-restore —
    are unchanged). Frozen: a constructed envelope is a value, not live state.
    """

    model_config = ConfigDict(frozen=True, extra="allow")

    # Every envelope field is deliberately ``Any``, not a strict type. The
    # pre-P22 imperative ``_normalize_plan_doc_keys`` NEVER validated or coerced
    # a value's type — it only *conditionally* wrote a value it had already
    # type-checked (``plan_text`` only when ``isinstance(str)``, ``total_notes``
    # only the enumerated ``len``). A strict ``str``/``int`` field would raise a
    # ``ValidationError`` on a garbage/``None``/non-str value that the old code
    # left UNTOUCHED (then rejected cleanly by the fail-closed plan gate), so
    # strict typing would break P22's byte-identity invariant and abort the
    # phase instead of returning an orderly gate rejection. ``Any`` makes the
    # envelope a faithful value-carrier over the untyped dict; the FOLD (below)
    # is where the type checks live, exactly mirroring the old code.
    plan_path: Any = ""
    plan_text: Any = ""
    total_notes: Any = 0
    planned_notes: tuple[Any, ...] = ()
    ready: Any = False
    failures: Any = ()
    verdict: dict | None = None

    @model_validator(mode="before")
    @classmethod
    def _fold_plan_of_record(cls, data: Any) -> Any:
        """Run the three folds on the raw dict BEFORE field validation.

        BYTE-IDENTICAL to the pre-P22 imperative ``_normalize_plan_doc_keys``:
        each fill only touches an absent/empty canonical key; the longest-of +
        floor are monotonic; a non-list ``planned_notes`` or a garbage
        ``total_notes`` is left exactly as-is. Idempotent. Mutates a COPY —
        never the caller's dict (the digestion adapter writes back in place)."""
        if not isinstance(data, dict):
            return data
        d = dict(data)  # copy: don't mutate the caller's dict during validation

        # 1. Alias fold — fill an absent/empty canonical from its first present
        #    alias (never clobber a value the plan already set canonically).
        for canonical, aliases in _PLAN_DOC_KEY_ALIASES.items():
            if d.get(canonical) not in (None, "", 0):
                continue
            for alias in aliases:
                val = d.get(alias)
                if val not in (None, "", 0):
                    d[canonical] = val
                    break

        # 2. plan_text of record = the longest of {plan_text, body_markdown}
        #    (a downstream re-emission summarizes; the longest copy is truth).
        body = d.get("body_markdown")
        ptext = d.get("plan_text")
        if isinstance(body, str) and isinstance(ptext, str) and len(body) > len(ptext):
            d["plan_text"] = body

        # 3. total_notes floor = the enumerated planned_notes count (you cannot
        #    declare fewer notes than you enumerated). A LARGER declared total (a
        #    master plan enumerating a subset) is preserved. Guarded on ``list``
        #    only — and a non-int total is left untouched when there is no floor
        #    — to match the pre-P22 imperative behaviour exactly (nothing
        #    downstream reads a non-int total as a count).
        planned = d.get("planned_notes")
        if isinstance(planned, list) and planned:
            total = d.get("total_notes")
            if not isinstance(total, int) or total < len(planned):
                d["total_notes"] = len(planned)
        return d

    @classmethod
    def from_dict(cls, plan_doc: dict[str, Any]) -> "PlanDoc":
        """Build a normalized envelope from a raw ``plan_doc`` dict."""
        return cls.model_validate(plan_doc)

    def to_normalized_dict(self) -> dict[str, Any]:
        """The full dict: the validated envelope fields merged with every extra
        key the plan carried (losslessly). ``planned_notes``/``failures`` are
        emitted as ``list`` (their common dict shape) when they are the
        tuple the field coerced them to; a non-tuple value is passed verbatim.

        NB the digestion adapter does NOT use this — it writes the canonical
        envelope attributes back into the live dict in place. This method exists
        for tests / debugging / a future by-value consumer."""
        out = dict(self.__pydantic_extra__ or {})
        out.update(
            plan_path=self.plan_path,
            plan_text=self.plan_text,
            total_notes=self.total_notes,
            planned_notes=list(self.planned_notes) if isinstance(self.planned_notes, tuple) else self.planned_notes,
            ready=self.ready,
            failures=list(self.failures) if isinstance(self.failures, tuple) else self.failures,
        )
        if self.verdict is not None:
            out["verdict"] = self.verdict
        return out


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
    KIND_RE_EMISSION = "RE_EMISSION"  # P21-full: a no_op step re-emits an artifact

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
