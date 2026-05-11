"""Integration tests for the ``skill_tessellum_dks_cycle`` skill canonical
and its Composer-pipeline sidecar.

DKS Phase 1 (v0.0.40) shipped the pure-Python API; v0.0.43 lifted it to
``tessellum.dks`` (its own top-level module, peer to ``tessellum.composer``).
Phase 2 (v0.0.42) wraps the same 7-component closed loop into a Composer
skill — canonical body + ``.pipeline.yaml`` sidecar that share section_id
anchors. These tests confirm:

1. The canonical's frontmatter, body, and link discipline pass
   ``tessellum format check``.
2. The canonical + sidecar pair loads via ``tessellum.composer.loader`` and
   declares exactly 7 steps in the right order.
3. The pair compiles to a 7-node DAG via ``tessellum.composer.compiler``,
   with the right dependency edges.
4. The 7 expected_output_schemas match the field surface of the Phase 1
   dataclasses (so the skill's prompt contract stays in sync with
   ``dks.py``).
"""

from __future__ import annotations

from pathlib import Path


from tessellum.composer.compiler import compile_skill
from tessellum.composer.loader import load_pipeline
from tessellum.composer.skill_extractor import list_section_ids
from tessellum.format import is_valid, validate


SKILL_PATH = Path(__file__).resolve().parents[2] / (
    "vault/resources/skills/skill_tessellum_dks_cycle.md"
)
SIDECAR_PATH = SKILL_PATH.with_name("skill_tessellum_dks_cycle.pipeline.yaml")


EXPECTED_STEP_IDS = (
    "step_1_observation_capture",
    "step_2_argument_a",
    "step_3_argument_b",
    "step_4_disagreement_detection",
    "step_5_counter_argument_capture",
    "step_6_pattern_discovery",
    "step_7_rule_improvement",
)


def test_skill_canonical_exists():
    assert SKILL_PATH.is_file(), f"missing {SKILL_PATH}"
    assert SIDECAR_PATH.is_file(), f"missing {SIDECAR_PATH}"


def test_skill_canonical_passes_format_check():
    """Canonical body must pass the YAML + link validator."""
    issues = validate(SKILL_PATH)
    errors = [i for i in issues if i.severity.value == "error"]
    assert errors == [], (
        f"skill canonical failed format check with {len(errors)} error(s): {errors}"
    )
    assert is_valid(SKILL_PATH)


def test_canonical_declares_all_7_step_anchors():
    """Every sidecar section_id has a matching `<!-- :: section_id = X :: -->`
    anchor in the canonical body."""
    canonical_anchors = set(list_section_ids(SKILL_PATH))
    for step_id in EXPECTED_STEP_IDS:
        assert step_id in canonical_anchors, (
            f"missing canonical anchor for {step_id}; "
            f"found: {sorted(canonical_anchors)}"
        )


def test_pipeline_loads_and_has_7_steps():
    """The canonical + sidecar pair loads cleanly and produces 7 steps."""
    pipeline = load_pipeline(SKILL_PATH)
    assert pipeline is not None, "pipeline_metadata: none — expected sidecar"
    assert len(pipeline.pipeline) == 7
    assert tuple(s.section_id for s in pipeline.pipeline) == EXPECTED_STEP_IDS


def test_pipeline_dependency_edges():
    """Confirm the 7-step DAG matches the Phase 2 design:

        step_1
          ├── step_2
          ├── step_3
          └── step_4 ← (2, 3)
                └── step_5
                      └── step_6
                            └── step_7
    """
    pipeline = load_pipeline(SKILL_PATH)
    deps = {s.section_id: tuple(s.depends_on) for s in pipeline.pipeline}

    assert deps["step_1_observation_capture"] == ()
    assert deps["step_2_argument_a"] == ("step_1_observation_capture",)
    assert deps["step_3_argument_b"] == ("step_1_observation_capture",)
    assert deps["step_4_disagreement_detection"] == (
        "step_2_argument_a",
        "step_3_argument_b",
    )
    assert deps["step_5_counter_argument_capture"] == (
        "step_4_disagreement_detection",
    )
    assert deps["step_6_pattern_discovery"] == ("step_5_counter_argument_capture",)
    assert deps["step_7_rule_improvement"] == ("step_6_pattern_discovery",)


def test_step_4_is_no_op_other_steps_are_file_materializers():
    """Steps 1, 2, 3, 5, 6, 7 each materialise a typed atomic note via
    ``body_markdown_frontmatter_to_file``; step 4 is a ``no_op`` because
    the contradicts edge lives as a link in the attacker's body, not as
    a separate file."""
    pipeline = load_pipeline(SKILL_PATH)
    by_id = {s.section_id: s for s in pipeline.pipeline}

    for note_step in (
        "step_1_observation_capture",
        "step_2_argument_a",
        "step_3_argument_b",
        "step_5_counter_argument_capture",
        "step_6_pattern_discovery",
        "step_7_rule_improvement",
    ):
        assert by_id[note_step].materializer == "body_markdown_frontmatter_to_file", (
            f"{note_step} should materialise a markdown-with-frontmatter file"
        )

    assert by_id["step_4_disagreement_detection"].materializer == "no_op"


def test_skill_compiles_to_7_node_dag():
    """End-to-end compile: skill canonical + sidecar → CompiledPipeline."""
    compiled = compile_skill(SKILL_PATH)
    assert len(compiled.steps) == 7
    assert tuple(s.section_id for s in compiled.steps) == EXPECTED_STEP_IDS


def test_compiled_step_4_no_op_carries_contradicts_schema():
    """Step 4 is a no_op materialiser BUT it still declares an
    ``expected_output_schema`` because the disagreement edge feeds
    step 5's prompt. The schema must surface ``agreement``,
    ``attacker_fz``, ``attacked_fz``, ``reason``."""
    pipeline = load_pipeline(SKILL_PATH)
    step_4 = next(
        s for s in pipeline.pipeline if s.section_id == "step_4_disagreement_detection"
    )
    schema = step_4.expected_output_schema or {}
    required = set(schema.get("required", []))
    assert {"agreement", "attacker_fz", "attacked_fz"}.issubset(required), (
        f"step 4 schema missing core contradicts fields: required={required}"
    )


def test_step_5_output_path_pattern_targets_counter_dir():
    pipeline = load_pipeline(SKILL_PATH)
    step_5 = next(
        s for s in pipeline.pipeline if s.section_id == "step_5_counter_argument_capture"
    )
    schema = step_5.expected_output_schema or {}
    pattern = schema.get("properties", {}).get("output_path", {}).get("pattern", "")
    assert "resources/analysis_thoughts/counter_" in pattern, (
        f"counter must land under analysis_thoughts/; got pattern={pattern!r}"
    )


def test_step_7_output_path_pattern_covers_both_procedure_and_concept():
    """The revised warrant lands as either a procedure (under
    resources/skills/) or a concept (under resources/term_dictionary/).
    The output_path pattern must accept both shapes."""
    pipeline = load_pipeline(SKILL_PATH)
    step_7 = next(
        s for s in pipeline.pipeline if s.section_id == "step_7_rule_improvement"
    )
    schema = step_7.expected_output_schema or {}
    pattern = schema.get("properties", {}).get("output_path", {}).get("pattern", "")
    assert "procedure" in pattern, f"step 7 pattern must allow procedure_; got {pattern!r}"
    assert "concept" in pattern, f"step 7 pattern must allow concept_; got {pattern!r}"


def test_step_1_declares_optional_session_mcp_dependency():
    """Step 1 wires session-mcp the same way skill_tessellum_write_coe
    does — so the agent can extract observations from the active
    transcript when available, and degrades gracefully when not."""
    pipeline = load_pipeline(SKILL_PATH)
    step_1 = next(
        s for s in pipeline.pipeline if s.section_id == "step_1_observation_capture"
    )
    session_deps = [d for d in step_1.mcp_dependencies if d.name == "session-mcp"]
    assert len(session_deps) == 1, "step 1 should declare exactly one session-mcp dep"
    assert session_deps[0].required is False, (
        "session-mcp on step 1 must be optional — DKS runs without an active session too"
    )


def test_all_steps_are_core_role():
    """Every DKS step is CORE (LLM-dispatched). No DEFERRED steps in the
    cycle — multi-cycle orchestration arrives in Phase 3, not here."""
    pipeline = load_pipeline(SKILL_PATH)
    for step in pipeline.pipeline:
        assert step.role == "CORE", f"{step.section_id} role={step.role}, expected CORE"


def test_step_6_and_7_align_with_bb_routing():
    """Step 6 lands at areas/models/pattern_…; step 7 lands under
    resources/skills/procedure_… OR resources/term_dictionary/concept_….
    Confirms the BB-to-directory mapping documented in the canonical
    matches the sidecar's output_path patterns."""
    pipeline = load_pipeline(SKILL_PATH)
    step_6 = next(
        s for s in pipeline.pipeline if s.section_id == "step_6_pattern_discovery"
    )
    step_6_pattern = step_6.expected_output_schema.get("properties", {}).get("output_path", {}).get("pattern", "")
    assert "areas/models/pattern_" in step_6_pattern
