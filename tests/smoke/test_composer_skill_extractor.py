"""Smoke tests for tessellum.composer.skill_extractor (single-file format)."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tessellum.composer.skill_extractor import (
    SkillExtractionError,
    iter_step_sections,
    list_section_ids,
    load_skill_section,
    split_contract_and_prompt,
)

# A skill with markers. Step sections carry a leading ```yaml``` contract
# block; prose sections (no contract block) are not pipeline steps.
_SKILL_WITH_MARKERS = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - skill
    keywords:
      - alpha
      - beta
      - gamma
    topics:
      - X
      - Y
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    ---

    # Test Skill

    ## First section <!-- :: section_id = first_section :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: first_out
    ```

    Body of the first section.
    Spans multiple lines.

    ## Second section <!-- :: section_id = second_section :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: [first_section]
    materializer: no_op
    output_key: second_out
    ```

    Body of the second section.

    ## Section without anchor

    This section has no anchor — extractor must ignore it.

    ## Third section <!-- :: section_id = step_3_third :: -->

    Body of the third section — prose only, no contract block, so it is
    NOT a pipeline step.

    Final paragraph.
    """
)

_SKILL_NO_ANCHORS = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - skill
    keywords:
      - a
      - b
      - c
    topics:
      - X
      - Y
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    ---

    # Skill with no anchors

    ## Plain heading

    No <!-- :: section_id :: --> anchor anywhere.
    """
)


@pytest.fixture
def skill_with_markers(tmp_path):
    p = tmp_path / "skill_test.md"
    p.write_text(_SKILL_WITH_MARKERS, encoding="utf-8")
    return p


@pytest.fixture
def skill_no_anchors(tmp_path):
    p = tmp_path / "skill_no_anchors.md"
    p.write_text(_SKILL_NO_ANCHORS, encoding="utf-8")
    return p


def test_load_skill_section_returns_body_text(skill_with_markers):
    text = load_skill_section(skill_with_markers, "first_section")
    assert "Body of the first section." in text
    assert "Spans multiple lines" in text


def test_load_skill_section_excludes_heading_line(skill_with_markers):
    text = load_skill_section(skill_with_markers, "first_section")
    assert "## First section" not in text
    assert "<!-- :: section_id" not in text


def test_load_skill_section_stops_at_next_h2(skill_with_markers):
    """A section's body shouldn't bleed into the next section's content."""
    text = load_skill_section(skill_with_markers, "first_section")
    assert "Body of the second section" not in text
    assert "Body of the third section" not in text


def test_load_skill_section_handles_section_followed_by_anchorless_section(
    skill_with_markers,
):
    """If the next H2 has no anchor, the body still cuts at it."""
    text = load_skill_section(skill_with_markers, "second_section")
    assert "Body of the second section." in text
    assert "no anchor" not in text  # next section's content excluded


def test_load_skill_section_unknown_id_raises(skill_with_markers):
    with pytest.raises(SkillExtractionError, match="not found"):
        load_skill_section(skill_with_markers, "nonexistent")


def test_load_skill_section_no_anchors_raises(skill_no_anchors):
    with pytest.raises(SkillExtractionError, match="no section_id anchors"):
        load_skill_section(skill_no_anchors, "anything")


def test_list_section_ids_in_document_order(skill_with_markers):
    ids = list_section_ids(skill_with_markers)
    assert ids == ["first_section", "second_section", "step_3_third"]


# ── split_contract_and_prompt ────────────────────────────────────────────────


def test_split_contract_and_prompt_parses_leading_yaml(skill_with_markers):
    body = load_skill_section(skill_with_markers, "first_section")
    contract, prompt = split_contract_and_prompt(body)
    assert contract is not None
    assert contract["role"] == "CORE"
    assert contract["materializer"] == "no_op"
    assert contract["output_key"] == "first_out"
    # The contract block is stripped from the prompt prose.
    assert prompt.startswith("Body of the first section.")
    assert "role: CORE" not in prompt
    assert "```yaml" not in prompt


def test_split_contract_and_prompt_none_for_prose_section(skill_with_markers):
    body = load_skill_section(skill_with_markers, "step_3_third")
    contract, prompt = split_contract_and_prompt(body)
    assert contract is None
    assert prompt.startswith("Body of the third section")


def test_split_contract_and_prompt_ignores_non_leading_fence():
    """A ```yaml fence that isn't the FIRST thing is prose, not a contract."""
    body = "Some prose first.\n\n```yaml\nrole: CORE\n```\n"
    contract, prompt = split_contract_and_prompt(body)
    assert contract is None
    assert prompt.startswith("Some prose first.")


def test_split_contract_and_prompt_raises_on_non_mapping():
    body = "```yaml\n- just\n- a\n- list\n```\n\nprompt"
    with pytest.raises(SkillExtractionError, match="must be a mapping"):
        split_contract_and_prompt(body)


# ── iter_step_sections ───────────────────────────────────────────────────────


def test_iter_step_sections_returns_only_contract_sections(skill_with_markers):
    steps = iter_step_sections(skill_with_markers)
    # Two sections have contract blocks; the third is prose-only.
    assert [s.section_id for s in steps] == ["first_section", "second_section"]
    assert steps[0].contract["output_key"] == "first_out"
    assert steps[1].contract["depends_on"] == ["first_section"]
    assert steps[0].prompt.startswith("Body of the first section.")


def test_iter_step_sections_empty_when_no_contract_blocks(skill_no_anchors):
    assert iter_step_sections(skill_no_anchors) == []


def test_extractor_works_against_real_skill_canonical():
    """The shipped skill_tessellum_format_check.md has anchored H2s."""
    skill = (
        Path(__file__).resolve().parents[2]
        / "vault"
        / "resources"
        / "skills"
        / "skill_tessellum_format_check.md"
    )
    if not skill.is_file():
        pytest.skip(f"real skill not found at {skill}")
    ids = list_section_ids(skill)
    assert "skill_description" in ids
    assert len(ids) >= 5
    # Each ID must yield a non-empty body
    for sid in ids:
        body = load_skill_section(skill, sid)
        assert body, f"section {sid} is empty"
