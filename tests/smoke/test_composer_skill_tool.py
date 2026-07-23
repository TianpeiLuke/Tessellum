"""Skills-as-tools + capability registry.

Covers:
  - build_skill_tool: projects a compiled pipeline into a SkillTool contract
    (input/output schema, side_effects from materializer verbs, gates,
    mcp_deps from the sidecar, routing key from frontmatter + lead step).
  - CapabilityRegistry: from_skill_dir discovery, by_side_effect, and
    two-tier route (unique match → skill; 0-or-many → needs_llm_selector).

Pure projection + lookup; no LLM, no network.
"""

from __future__ import annotations

from pathlib import Path

from tessellum.composer import (
    CapabilityRegistry,
    RoutingKey,
    SkillTool,
    build_skill_tool,
)
from tessellum.composer.skill_tool import McpDep


def _write_skill(
    tmp_path: Path,
    name: str,
    *,
    building_block: str = "procedure",
    topic: str = "Test Domain",
    steps_yaml: str,
    canonical_steps: str,
) -> Path:
    # Built without textwrap.dedent — the injected multi-line body has no
    # indentation, which would zero out dedent's common-prefix and leave the
    # frontmatter indented (breaking the `---` fences). Compose flush-left.
    canonical = (
        "---\n"
        "tags:\n  - resource\n  - skill\n"
        "keywords:\n  - alpha\n  - beta\n  - gamma\n"
        f"topics:\n  - {topic}\n"
        "language: markdown\n"
        "date of note: 2026-05-10\n"
        "status: active\n"
        f"building_block: {building_block}\n"
        f"pipeline_metadata: ./{name}.pipeline.yaml\n"
        "---\n\n"
        f"# {name}\n\n"
        f"{canonical_steps}\n"
    )
    sidecar = "version: \"1.0\"\npipeline:\n" + steps_yaml
    md = tmp_path / f"{name}.md"
    md.write_text(canonical, encoding="utf-8")
    (tmp_path / f"{name}.pipeline.yaml").write_text(sidecar, encoding="utf-8")
    return md


_PRODUCER_STEPS = """\
  - section_id: step_1
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: body_markdown_to_file
    expected_output_schema:
      type: object
      required: [output_path, body_markdown]
    prompt_template: "Write."
    output_key: written
"""

_PRODUCER_CANON = "## Step 1: write <!-- :: section_id = step_1 :: -->\n\nWrite {{leaf.id}}."


def test_build_skill_tool_producer(tmp_path: Path) -> None:
    md = _write_skill(
        tmp_path, "skill_make_note",
        building_block="concept", topic="Knowledge",
        steps_yaml=_PRODUCER_STEPS, canonical_steps=_PRODUCER_CANON,
    )
    t = build_skill_tool(md)
    assert isinstance(t, SkillTool)
    assert t.skill_name == "skill_make_note"
    assert t.pipeline_version == "1.0"
    assert "produces_notes" in t.side_effects
    assert not t.is_read_only
    assert t.input_schema is not None and "output_path" in t.input_schema["required"]
    assert t.output_schema is not None
    assert "compile_contract" in t.gates
    assert "tool_free_backend" in t.gates  # body_markdown_to_file requires it
    assert t.routing_key.produces_bb == "concept"
    assert t.routing_key.input_kind == "note_set"  # per_leaf lead
    assert t.routing_key.domain == "Knowledge"
    assert t.step_count == 1


_READONLY_STEPS = """\
  - section_id: step_1
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: []
    materializer: no_op
    expected_output_schema:
      type: object
      required: [answer]
    prompt_template: "Answer."
    output_key: answer
"""

_READONLY_CANON = "## Step 1: answer <!-- :: section_id = step_1 :: -->\n\nAnswer the query."


def test_build_skill_tool_read_only_query(tmp_path: Path) -> None:
    md = _write_skill(
        tmp_path, "skill_answer_query",
        building_block="procedure", topic="Retrieval",
        steps_yaml=_READONLY_STEPS, canonical_steps=_READONLY_CANON,
    )
    t = build_skill_tool(md)
    assert t.is_read_only
    assert t.side_effects == frozenset({"read_only"})
    # "answer"/"query" in the name → query input_kind regardless of aggregation.
    assert t.routing_key.input_kind == "query"


_APPLY_STEPS = """\
  - section_id: step_1
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: edits_apply_to_files
    expected_output_schema:
      type: object
      required: [edits]
    prompt_template: "Edit."
    output_key: applied
    mcp_dependencies:
      - name: builder-mcp
        calls: [ReadInternalWebsites]
        required: true
"""

_APPLY_CANON = "## Step 1: edit <!-- :: section_id = step_1 :: -->\n\nApply edits to {{leaf.id}}."


def test_build_skill_tool_apply_with_mcp(tmp_path: Path) -> None:
    md = _write_skill(
        tmp_path, "skill_fix_links",
        steps_yaml=_APPLY_STEPS, canonical_steps=_APPLY_CANON,
    )
    t = build_skill_tool(md)
    assert "applies_edits" in t.side_effects
    assert t.mcp_deps == (McpDep(name="builder-mcp", calls=("ReadInternalWebsites",), required=True),)


def test_registry_from_skill_dir_and_by_side_effect(tmp_path: Path) -> None:
    _write_skill(tmp_path, "skill_make_note", building_block="concept",
                 steps_yaml=_PRODUCER_STEPS, canonical_steps=_PRODUCER_CANON)
    _write_skill(tmp_path, "skill_answer_query", topic="Retrieval",
                 steps_yaml=_READONLY_STEPS, canonical_steps=_READONLY_CANON)
    # A stray .md with NO sidecar must be skipped (not a pipeline skill).
    (tmp_path / "skill_prose_only.md").write_text("# not a pipeline skill\n", encoding="utf-8")

    reg = CapabilityRegistry.from_skill_dir(tmp_path)
    assert set(reg.tools) == {"skill_make_note", "skill_answer_query"}
    assert [t.skill_name for t in reg.by_side_effect("produces_notes")] == ["skill_make_note"]
    assert [t.skill_name for t in reg.by_side_effect("read_only")] == ["skill_answer_query"]


def test_registry_route_unique_match(tmp_path: Path) -> None:
    _write_skill(tmp_path, "skill_make_note", building_block="concept", topic="Knowledge",
                 steps_yaml=_PRODUCER_STEPS, canonical_steps=_PRODUCER_CANON)
    _write_skill(tmp_path, "skill_answer_query", building_block="procedure", topic="Retrieval",
                 steps_yaml=_READONLY_STEPS, canonical_steps=_READONLY_CANON)
    reg = CapabilityRegistry.from_skill_dir(tmp_path)

    # Deterministic tier-1: exactly one skill produces a `concept` note-set.
    d = reg.route(produces_bb="concept", input_kind="note_set")
    assert d.skill_name == "skill_make_note"
    assert not d.needs_llm_selector


def test_registry_route_ambiguous_needs_selector(tmp_path: Path) -> None:
    # Two producers with the SAME routing key → open set → needs_llm_selector.
    _write_skill(tmp_path, "skill_make_note_a", building_block="concept", topic="Knowledge",
                 steps_yaml=_PRODUCER_STEPS, canonical_steps=_PRODUCER_CANON)
    _write_skill(tmp_path, "skill_make_note_b", building_block="concept", topic="Knowledge",
                 steps_yaml=_PRODUCER_STEPS, canonical_steps=_PRODUCER_CANON)
    reg = CapabilityRegistry.from_skill_dir(tmp_path)

    d = reg.route(produces_bb="concept", input_kind="note_set", domain="Knowledge")
    assert d.skill_name is None
    assert d.needs_llm_selector
    assert set(d.candidates) == {"skill_make_note_a", "skill_make_note_b"}


def test_registry_route_no_match_needs_selector(tmp_path: Path) -> None:
    _write_skill(tmp_path, "skill_make_note", building_block="concept",
                 steps_yaml=_PRODUCER_STEPS, canonical_steps=_PRODUCER_CANON)
    reg = CapabilityRegistry.from_skill_dir(tmp_path)
    # Nothing produces a `model` note → 0 candidates → defer to selector.
    d = reg.route(produces_bb="model")
    assert d.skill_name is None
    assert d.needs_llm_selector
    assert d.candidates == ()


def test_routing_key_equality() -> None:
    a = RoutingKey(produces_bb="concept", input_kind="note_set", domain="X")
    b = RoutingKey(produces_bb="concept", input_kind="note_set", domain="X")
    assert a == b  # frozen dataclass value equality (usable as a dict key)
