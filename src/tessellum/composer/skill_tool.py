"""SkillTool + Capability Registry — skills as typed, routable capabilities.

This realizes the "skills as tools" + "capability registry" design in
**Python** (the settled bridge-not-port conclusion: a full TypeScript port
is feasible-but-not-worth-it; the substrate stays Python, a thin TS shell
may call it later — so the capability model lives here, not in TS).

Two artifacts:

- **:class:`SkillTool`** — a skill promoted from a prose SOP into a typed,
  invokable capability. Compiled from the skill's canonical + pipeline
  sidecar into a stable ``{input_schema, output_schema, side_effects,
  gates, mcp_deps}`` contract plus a routing key
  ``{produces_bb, input_kind, domain}``. It is a *projection* over the
  already-compiled pipeline — it never re-implements compilation or
  contract logic (boundary doctrine: the compiler is the single source of
  truth; this is a read-only view for discovery + routing).

- **:class:`CapabilityRegistry`** — indexes SkillTools and answers "which
  skill produces X?" with **two-tier routing**: a deterministic closed
  table (``{produces_bb, input_kind, domain} -> skill``) for the known
  set, and an explicit ``needs_llm_selector`` signal for the open set
  (this module never calls an LLM — it hands the open-set decision back to
  the caller, keeping the boundary: programs route deterministically where
  they can, agents decide only the genuinely-ambiguous choice).

No LLM, no network — pure projection + lookup (the boundary doctrine).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from tessellum.composer.compiler import CompiledPipeline, compile_skill
from tessellum.composer.loader import load_pipeline

SideEffect = Literal["produces_notes", "applies_edits", "read_only"]
"""What a skill does to the vault, derived from its materializer verbs:

- ``produces_notes`` — at least one PRODUCE step (writes new note files).
- ``applies_edits`` — at least one APPLY step (edits existing files).
- ``read_only`` — only DESCRIBE / no_op steps (no filesystem mutation).
"""

InputKind = Literal["source_document", "query", "note_set", "corpus"]
"""The shape of input a skill consumes, inferred from its lead step's
aggregation + role. Part of the routing key."""


@dataclass(frozen=True)
class McpDep:
    """A skill's declared MCP dependency (projected from the sidecar)."""

    name: str
    calls: tuple[str, ...] = ()
    required: bool = True


@dataclass(frozen=True)
class RoutingKey:
    """The ``{produces_bb, input_kind, domain}`` key a registry routes on.

    Attributes:
        produces_bb: The building-block type the skill produces (from the
            canonical's ``building_block`` frontmatter), or ``None`` if
            unspecified.
        input_kind: The shape of input the skill consumes.
        domain: A coarse domain tag (first topic/tag), or ``None``.
    """

    produces_bb: str | None
    input_kind: InputKind
    domain: str | None = None


@dataclass(frozen=True)
class SkillTool:
    """A skill as a typed, invokable capability — a projection over its
    compiled pipeline.

    Attributes:
        skill_name: Filename stem (e.g. ``skill_tessellum_capture_term_note``).
        skill_path: Source canonical path.
        pipeline_version: Sidecar ``version``.
        input_schema: JSON Schema the skill's first CORE step expects (its
            entry contract), or ``None`` if unschematized.
        output_schema: JSON Schema the skill's last CORE step produces (its
            exit contract), or ``None``.
        side_effects: The set of vault effects this skill has.
        gates: The pure-program gate ids that guard this skill's stages
            (the ``requires_tool_free_backend`` + materializer-verb
            invariants surface here as named gates).
        mcp_deps: The skill's declared MCP dependencies.
        routing_key: The ``{produces_bb, input_kind, domain}`` this skill
            answers to.
        step_count: Number of steps in the compiled pipeline.
    """

    skill_name: str
    skill_path: Path
    pipeline_version: str
    input_schema: dict | None
    output_schema: dict | None
    side_effects: frozenset[SideEffect]
    gates: tuple[str, ...]
    mcp_deps: tuple[McpDep, ...]
    routing_key: RoutingKey
    step_count: int

    @property
    def is_read_only(self) -> bool:
        return self.side_effects == frozenset({"read_only"})


def _infer_side_effects(compiled: CompiledPipeline) -> frozenset[SideEffect]:
    effects: set[SideEffect] = set()
    for step in compiled.steps:
        c = step.materializer_contract
        if c is None:
            continue
        if c.operation_verb == "PRODUCE":
            effects.add("produces_notes")
        elif c.operation_verb == "APPLY":
            effects.add("applies_edits")
    if not effects:
        effects.add("read_only")
    return frozenset(effects)


def _infer_input_kind(compiled: CompiledPipeline) -> InputKind:
    """Infer the lead-step input shape.

    A per-leaf lead step consumes a note-set (one invocation per note); a
    corpus-wide lead step consumes the whole corpus or a single query.
    Skills whose name implies query/answer are ``query``; otherwise a
    corpus-wide producer is treated as ``source_document`` (a single
    source digested into notes).
    """
    core = [s for s in compiled.steps if s.role != "INFRA"]
    if not core:
        return "corpus"
    lead = core[0]
    name = compiled.skill_name.lower()
    if "answer" in name or "search" in name or "query" in name:
        return "query"
    if lead.aggregation == "per_leaf":
        return "note_set"
    if lead.aggregation == "corpus_wide":
        return "source_document"
    return "corpus"


def _infer_gates(compiled: CompiledPipeline) -> tuple[str, ...]:
    """The pure-program invariants that guard this skill, as named gates.

    Projected from the compiled contracts — a tool-free-backend
    requirement and an APPLY step both imply gates the orchestrator must
    honour. This is a discovery view, not the gate engine itself.
    """
    gates: list[str] = ["compile_contract"]  # every skill passes P4.5
    for step in compiled.steps:
        c = step.materializer_contract
        if c is None:
            continue
        if getattr(c, "requires_tool_free_backend", False):
            gates.append("tool_free_backend")
        if getattr(c, "requires_existing_files", False):
            gates.append("existing_files_present")
        if getattr(c, "apply_mode_directive_required", False):
            gates.append("apply_mode_directive")
    # De-dup, preserve order.
    seen: set[str] = set()
    out: list[str] = []
    for g in gates:
        if g not in seen:
            seen.add(g)
            out.append(g)
    return tuple(out)


def _read_produces_bb(skill_path: Path) -> str | None:
    """Read the canonical's ``building_block`` frontmatter (best-effort)."""
    try:
        from tessellum.format.parser import parse_note

        note = parse_note(skill_path)
        bb = note.frontmatter.get("building_block")
        return str(bb) if bb else None
    except Exception:  # noqa: BLE001 — a missing/odd frontmatter is not fatal
        return None


def _read_domain(skill_path: Path) -> str | None:
    """Coarse domain = first topic, else first non-generic tag."""
    try:
        from tessellum.format.parser import parse_note

        note = parse_note(skill_path)
        topics = note.frontmatter.get("topics")
        if isinstance(topics, list) and topics:
            return str(topics[0])
        tags = note.frontmatter.get("tags")
        if isinstance(tags, list):
            for t in tags:
                if str(t) not in {"resource", "skill", "procedure"}:
                    return str(t)
    except Exception:  # noqa: BLE001
        return None
    return None


def build_skill_tool(skill_path: Path | str) -> SkillTool:
    """Compile a skill and project it into a :class:`SkillTool` contract.

    Delegates ALL compilation to :func:`compile_skill` (single source of
    truth) and reads the sidecar via :func:`load_pipeline` only for the
    ``mcp_dependencies`` the compiler drops. Everything else is a
    read-only projection over the compiled pipeline + canonical
    frontmatter.
    """
    skill_path = Path(skill_path)
    compiled = compile_skill(skill_path)

    core = [s for s in compiled.steps if s.role != "INFRA"]
    input_schema = core[0].expected_output_schema if core else None
    output_schema = core[-1].expected_output_schema if core else None

    # mcp_deps come from the loader layer (compiler drops them).
    mcp_deps: tuple[McpDep, ...] = ()
    pipeline = load_pipeline(skill_path)
    if pipeline is not None:
        deps: list[McpDep] = []
        for step in pipeline.pipeline:
            for d in step.mcp_dependencies:
                deps.append(McpDep(name=d.name, calls=tuple(d.calls), required=d.required))
        # De-dup by name (a skill may list the same MCP in several steps).
        by_name: dict[str, McpDep] = {}
        for d in deps:
            by_name.setdefault(d.name, d)
        mcp_deps = tuple(by_name.values())

    return SkillTool(
        skill_name=compiled.skill_name,
        skill_path=skill_path,
        pipeline_version=compiled.pipeline_version,
        input_schema=input_schema,
        output_schema=output_schema,
        side_effects=_infer_side_effects(compiled),
        gates=_infer_gates(compiled),
        mcp_deps=mcp_deps,
        routing_key=RoutingKey(
            produces_bb=_read_produces_bb(skill_path),
            input_kind=_infer_input_kind(compiled),
            domain=_read_domain(skill_path),
        ),
        step_count=compiled.step_count,
    )


@dataclass(frozen=True)
class RouteDecision:
    """The outcome of a registry route query.

    Attributes:
        skill_name: The chosen skill, or ``None`` when routing is
            deferred to the open-set selector.
        needs_llm_selector: ``True`` when the closed table had 0 or >1
            candidates and a semantic choice must be made by an agent —
            this module never makes that call (boundary doctrine).
        candidates: All skill names matching the key (for the selector).
    """

    skill_name: str | None
    needs_llm_selector: bool
    candidates: tuple[str, ...] = ()


@dataclass
class CapabilityRegistry:
    """Indexes :class:`SkillTool`s and routes a task to one, two-tier.

    Not frozen — tools are registered incrementally. The closed table maps
    a full ``(produces_bb, input_kind, domain)`` key to a *unique* skill;
    ambiguity (0 or >1) returns ``needs_llm_selector`` rather than
    guessing.
    """

    tools: dict[str, SkillTool] = field(default_factory=dict)

    def register(self, tool: SkillTool) -> None:
        self.tools[tool.skill_name] = tool

    @classmethod
    def from_skill_dir(cls, skills_dir: Path | str) -> "CapabilityRegistry":
        """Build a registry from every ``skill_*.md`` in a directory that
        has a paired ``.pipeline.yaml`` sidecar (Bucket-A skills)."""
        skills_dir = Path(skills_dir)
        reg = cls()
        for md in sorted(skills_dir.glob("skill_*.md")):
            sidecar = md.with_name(md.stem + ".pipeline.yaml")
            if not sidecar.is_file():
                continue  # not a pipeline skill (no typed contract)
            try:
                reg.register(build_skill_tool(md))
            except Exception:  # noqa: BLE001 — skip a skill that won't compile
                continue
        return reg

    def by_side_effect(self, effect: SideEffect) -> list[SkillTool]:
        return [t for t in self.tools.values() if effect in t.side_effects]

    def route(
        self,
        *,
        produces_bb: str | None = None,
        input_kind: InputKind | None = None,
        domain: str | None = None,
    ) -> RouteDecision:
        """Route a task to a SkillTool by (subset of) the routing key.

        Tier 1 (deterministic): filter tools whose routing key matches
        every *provided* dimension. Exactly one match → route to it. Tier
        2 (open set): 0 or >1 matches → ``needs_llm_selector`` with the
        candidate list, deferring the semantic choice to an agent.
        """
        cands = []
        for t in self.tools.values():
            k = t.routing_key
            if produces_bb is not None and k.produces_bb != produces_bb:
                continue
            if input_kind is not None and k.input_kind != input_kind:
                continue
            if domain is not None and k.domain != domain:
                continue
            cands.append(t.skill_name)
        cands.sort()
        if len(cands) == 1:
            return RouteDecision(skill_name=cands[0], needs_llm_selector=False,
                                 candidates=tuple(cands))
        return RouteDecision(skill_name=None, needs_llm_selector=True,
                             candidates=tuple(cands))


__all__ = [
    "SideEffect",
    "InputKind",
    "McpDep",
    "RoutingKey",
    "SkillTool",
    "build_skill_tool",
    "RouteDecision",
    "CapabilityRegistry",
]
