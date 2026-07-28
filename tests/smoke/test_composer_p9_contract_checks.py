"""P9 (FZ 20k9c1a1a1b7c2e) — the compiler's advertised integrity checks.

The compiler documented (contracts.py) checks it did not enforce: 8 of 11
``ContractViolation.KIND_*`` were dead. P9 lights up the checkable ones —

- wire_format / operation_verb OVERRIDE mismatch → HARD (structural, inert on
  the shipped corpus: no skill declares an override).
- MCP-dependency resolution (name ∈ registry, calls ⊆ available_tools) → WARN,
  hard behind ``strict_mcp`` (the registry is user-extensible).
- APPLY ground-truth + directive (requires_existing_files ⇒ applies_to_files /
  query + ``{{existing.X}}`` refs + "APPLY mode") → WARN, hard behind
  ``strict_apply`` (surfaces two latent real-skill mis-declarations).
- prompt ⊇ required-fields (prose side) → WARN, hard behind
  ``strict_field_coverage`` (heuristic; the trivial-prompt test corpus makes it
  never-hard-by-default).

The governing invariant: warn-by-default breaks NOTHING (every shipped skill +
the synthetic test corpus still compiles); a strict_* flag turns one family hard.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tessellum.composer import ContractViolation, compile_skill


def _write(tmp_path: Path, name: str, text: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(text), encoding="utf-8")
    return p


_FRONT = """\
    ---
    tags: [resource, skill]
    keywords: [a, b, c]
    topics: [X, Y]
    language: markdown
    date of note: 2026-07-28
    status: active
    building_block: procedure
    ---

    # Demo
    """


# ── Check 2a — wire_format / operation_verb override mismatch (HARD) ─────────


def test_wire_format_override_mismatch_raises_hard(tmp_path: Path):
    skill = _FRONT + textwrap.dedent(
        """\

        ## Step w <!-- :: section_id = step_w :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        wire_format: markdown_with_frontmatter
        output_key: out
        ```

        Do it.
        """
    )
    # no_op's contract wire_format is "json"; declaring a different format contradicts it.
    with pytest.raises(ContractViolation) as exc:
        compile_skill(_write(tmp_path, "skill_wf.md", skill))
    assert exc.value.kind == ContractViolation.KIND_WIRE_FORMAT_MISMATCH


def test_operation_verb_override_mismatch_raises_hard(tmp_path: Path):
    skill = _FRONT + textwrap.dedent(
        """\

        ## Step v <!-- :: section_id = step_v :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        operation_verb: PRODUCE
        output_key: out
        ```

        Do it.
        """
    )
    # no_op is DESCRIBE; declaring PRODUCE contradicts it.
    with pytest.raises(ContractViolation) as exc:
        compile_skill(_write(tmp_path, "skill_ov.md", skill))
    assert exc.value.kind == ContractViolation.KIND_OPERATION_VERB_MISMATCH


def test_matching_override_is_accepted(tmp_path: Path):
    skill = _FRONT + textwrap.dedent(
        """\

        ## Step ok <!-- :: section_id = step_ok :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        wire_format: json
        operation_verb: DESCRIBE
        output_key: out
        ```

        Do it.
        """
    )
    # An override that AGREES with the contract (no_op = json / DESCRIBE) compiles clean.
    compile_skill(_write(tmp_path, "skill_ok.md", skill))


# ── Check 5 — MCP resolution (WARN default, hard under strict_mcp) ───────────

_MCP_SKILL = _FRONT + textwrap.dedent(
    """\

    ## Step m <!-- :: section_id = step_m :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: out
    mcp_dependencies:
    - name: no-such-mcp
      calls: []
    ```

    Do it.
    """
)


def test_unknown_mcp_warns_by_default(tmp_path: Path):
    cp = compile_skill(_write(tmp_path, "skill_mcp.md", _MCP_SKILL))
    assert any("UNKNOWN_MCP" in w for w in cp.contract_warnings)


def test_unknown_mcp_raises_under_strict(tmp_path: Path):
    with pytest.raises(ContractViolation) as exc:
        compile_skill(_write(tmp_path, "skill_mcp2.md", _MCP_SKILL), strict_mcp=True)
    assert exc.value.kind == ContractViolation.KIND_UNKNOWN_MCP


def test_unknown_mcp_tool_warns(tmp_path: Path):
    skill = _FRONT + textwrap.dedent(
        """\

        ## Step m <!-- :: section_id = step_m :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        output_key: out
        mcp_dependencies:
        - name: session-mcp
          calls:
          - not_a_real_tool
        ```

        Do it.
        """
    )
    cp = compile_skill(_write(tmp_path, "skill_mcptool.md", skill))
    assert any("UNKNOWN_MCP_TOOL" in w for w in cp.contract_warnings)


def test_valid_mcp_dependency_no_warning(tmp_path: Path):
    skill = _FRONT + textwrap.dedent(
        """\

        ## Step m <!-- :: section_id = step_m :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        output_key: out
        mcp_dependencies:
        - name: session-mcp
          calls:
          - get_session_metadata
        ```

        Do it.
        """
    )
    cp = compile_skill(_write(tmp_path, "skill_mcpok.md", skill))
    assert not any("UNKNOWN_MCP" in w for w in cp.contract_warnings)


# ── Check 6/7 — APPLY ground-truth + directive (WARN default) ────────────────


def test_apply_without_ground_truth_warns(tmp_path: Path):
    skill = _FRONT + textwrap.dedent(
        """\

        ## Step a <!-- :: section_id = step_a :: -->

        ```yaml
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: edits_apply_xml_tags
        output_key: out
        expected_output_schema:
          type: object
          required: [edits]
        ```

        Edit the file. APPLY mode — emit edits.
        """
    )
    cp = compile_skill(_write(tmp_path, "skill_apply.md", skill))
    assert any("APPLY_WITHOUT_GROUND_TRUTH" in w for w in cp.contract_warnings)


def test_apply_without_ground_truth_raises_under_strict(tmp_path: Path):
    skill = _FRONT + textwrap.dedent(
        """\

        ## Step a <!-- :: section_id = step_a :: -->

        ```yaml
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: edits_apply_xml_tags
        output_key: out
        expected_output_schema:
          type: object
          required: [edits]
        ```

        Edit the file. APPLY mode — emit edits.
        """
    )
    with pytest.raises(ContractViolation) as exc:
        compile_skill(_write(tmp_path, "skill_apply2.md", skill), strict_apply=True)
    assert exc.value.kind == ContractViolation.KIND_APPLY_WITHOUT_GROUND_TRUTH


def test_missing_apply_directive_warns(tmp_path: Path):
    skill = _FRONT + textwrap.dedent(
        """\

        ## Step a <!-- :: section_id = step_a :: -->

        ```yaml
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: edits_apply_xml_tags
        output_key: out
        applies_to_files:
        - notes/target.md
        expected_output_schema:
          type: object
          required: [edits]
        ```

        Edit {{existing.notes/target.md}} — but no directive phrase here.
        """
    )
    cp = compile_skill(_write(tmp_path, "skill_nodir.md", skill))
    assert any("MISSING_APPLY_DIRECTIVE" in w for w in cp.contract_warnings)


def test_existing_path_not_referenced_warns(tmp_path: Path):
    skill = _FRONT + textwrap.dedent(
        """\

        ## Step a <!-- :: section_id = step_a :: -->

        ```yaml
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: edits_apply_xml_tags
        output_key: out
        applies_to_files:
        - notes/target.md
        expected_output_schema:
          type: object
          required: [edits]
        ```

        APPLY mode — edit the file but never reference the existing content.
        """
    )
    cp = compile_skill(_write(tmp_path, "skill_noref.md", skill))
    assert any("EXISTING_PATH_NOT_REFERENCED" in w for w in cp.contract_warnings)


# ── Check 1 — prompt ⊇ required-fields (WARN; heuristic) ─────────────────────


def test_prompt_missing_required_field_warns(tmp_path: Path):
    skill = _FRONT + textwrap.dedent(
        """\

        ## Step p <!-- :: section_id = step_p :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: body_markdown_to_file
        output_key: out
        expected_output_schema:
          type: object
          required: [output_path, body_markdown]
        ```

        Write the body markdown for the note.
        """
    )
    cp = compile_skill(_write(tmp_path, "skill_field.md", skill))
    # The prose mentions body markdown but NOT output_path → a field-coverage warning.
    assert any("output_path" in w and "MISSING_REQUIRED_OUTPUT_FIELD" in w
               for w in cp.contract_warnings)


def test_field_coverage_normalizer_accepts_spaced_mention(tmp_path: Path):
    """A snake_case field mentioned in prose with spaces/hyphens is NOT flagged
    (the normalizer collapses separators)."""
    skill = _FRONT + textwrap.dedent(
        """\

        ## Step p <!-- :: section_id = step_p :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: body_markdown_to_file
        output_key: out
        expected_output_schema:
          type: object
          required: [output_path, body_markdown]
        ```

        Emit the output path and the body markdown for the note.
        """
    )
    cp = compile_skill(_write(tmp_path, "skill_field2.md", skill))
    assert not any("MISSING_REQUIRED_OUTPUT_FIELD" in w for w in cp.contract_warnings)


# ── The regression guard: shipped skills + test corpus never HARD-fail ───────


def test_shipped_skills_compile_clean_under_default_flags():
    """Every shipped skill compiles WITHOUT raising under the default (warn)
    flags — P9's warn-by-default must break nothing. The 4 digestion skills +
    dks_cycle carry zero contract warnings; the APPLY-heavy capture skills carry
    warnings (the latent mis-declarations) but do NOT raise."""
    repo = Path(__file__).resolve().parents[2]
    skills = sorted((repo / "vault" / "resources" / "skills").glob("skill_*.md"))
    if not skills:
        pytest.skip("real vault skills not present")
    clean_digestion = {
        "skill_tessellum_plan_digestion",
        "skill_tessellum_augment_digestion_plan",
        "skill_tessellum_review_digestion_plan",
        "skill_tessellum_execute_digestion_plan",
    }
    for s in skills:
        cp = compile_skill(s)  # must not raise
        if s.stem in clean_digestion:
            assert cp.contract_warnings == (), (
                f"{s.stem} should have zero P9 contract warnings, got: "
                + "; ".join(cp.contract_warnings)
            )
