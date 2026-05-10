"""Smoke tests for tessellum.composer.skill_extractor."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tessellum.composer.skill_extractor import (
    SkillExtractionError,
    list_section_ids,
    load_pipeline_metadata,
    load_skill_section,
)

# Test fixtures —— a skill with markers and a skill without.
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
    pipeline_metadata: ./skill_test.pipeline.yaml
    ---

    # Test Skill

    ## First section <!-- :: section_id = first_section :: -->

    Body of the first section.
    Spans multiple lines.

    ## Second section <!-- :: section_id = second_section :: -->

    Body of the second section.

    ## Section without anchor

    This section has no anchor — extractor must ignore it.

    ## Third section <!-- :: section_id = step_3_third :: -->

    Body of the third section.

    Final paragraph.
    """
)

_SKILL_WITHOUT_PIPELINE = _SKILL_WITH_MARKERS.replace(
    "pipeline_metadata: ./skill_test.pipeline.yaml",
    "pipeline_metadata: none",
)

_SKILL_WITHOUT_FIELD = _SKILL_WITH_MARKERS.replace(
    "pipeline_metadata: ./skill_test.pipeline.yaml\n",
    "",
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
def skill_without_pipeline(tmp_path):
    p = tmp_path / "skill_test.md"
    p.write_text(_SKILL_WITHOUT_PIPELINE, encoding="utf-8")
    return p


@pytest.fixture
def skill_no_anchors(tmp_path):
    p = tmp_path / "skill_no_anchors.md"
    p.write_text(_SKILL_NO_ANCHORS, encoding="utf-8")
    return p


def test_load_skill_section_returns_body_text(skill_with_markers):
    text = load_skill_section(skill_with_markers, "first_section")
    assert text.startswith("Body of the first section.")
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
    assert text.startswith("Body of the second section.")
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


def test_load_pipeline_metadata_resolves_relative_path(skill_with_markers):
    sidecar = load_pipeline_metadata(skill_with_markers)
    assert sidecar is not None
    assert sidecar.is_absolute()
    assert sidecar.name == "skill_test.pipeline.yaml"
    assert sidecar.parent == skill_with_markers.parent


def test_load_pipeline_metadata_returns_none_for_sentinel(skill_without_pipeline):
    assert load_pipeline_metadata(skill_without_pipeline) is None


def test_load_pipeline_metadata_returns_none_when_field_absent(tmp_path):
    p = tmp_path / "skill_no_field.md"
    p.write_text(_SKILL_WITHOUT_FIELD, encoding="utf-8")
    assert load_pipeline_metadata(p) is None


def test_extractor_works_against_real_skill_canonical():
    """The shipped skill_tessellum_format_check.md has 10 anchored H2s."""
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
    assert "validation_rules_reference" in ids
    assert len(ids) >= 10
    # Each ID must yield a non-empty body
    for sid in ids:
        body = load_skill_section(skill, sid)
        assert body, f"section {sid} is empty"
