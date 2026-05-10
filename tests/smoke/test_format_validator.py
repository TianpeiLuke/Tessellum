"""Smoke tests for tessellum.format — parser + validator."""

from __future__ import annotations

import textwrap

import pytest

from tessellum.format import (
    Issue,
    Note,
    Severity,
    is_valid,
    parse_text,
    validate,
)


def _note(frontmatter_yaml: str, body: str = "Body.") -> Note:
    return parse_text(f"---\n{frontmatter_yaml.strip()}\n---\n{body}\n")


VALID_FRONTMATTER = textwrap.dedent(
    """
    tags:
      - resource
      - terminology
      - tessellum
    keywords:
      - alpha
      - beta
      - gamma
    topics:
      - Topic A
      - Topic B
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: concept
    """
)


def test_valid_note_has_no_issues():
    note = _note(VALID_FRONTMATTER)
    assert validate(note) == []
    assert is_valid(note)


def test_missing_required_fields_emit_errors():
    note = _note(
        textwrap.dedent(
            """
            tags:
              - resource
              - terminology
            language: markdown
            status: active
            building_block: concept
            """
        )
    )
    fields = {i.field for i in validate(note) if i.severity is Severity.ERROR}
    assert "keywords" in fields
    assert "topics" in fields
    assert "date of note" in fields


def test_invalid_para_bucket_is_error():
    note = _note(
        VALID_FRONTMATTER.replace("- resource", "- resourcezz")
    )
    issues = [i for i in validate(note) if i.field == "tags[0]"]
    assert any(i.severity is Severity.ERROR for i in issues)


def test_invalid_building_block_is_error():
    note = _note(VALID_FRONTMATTER.replace("building_block: concept", "building_block: idea"))
    issues = [i for i in validate(note) if i.field == "building_block"]
    assert any(i.severity is Severity.ERROR for i in issues)
    assert not is_valid(note)


def test_invalid_status_is_error():
    note = _note(VALID_FRONTMATTER.replace("status: active", "status: shipped"))
    issues = [i for i in validate(note) if i.field == "status"]
    assert any(i.severity is Severity.ERROR for i in issues)


def test_bad_date_format_is_error():
    note = _note(VALID_FRONTMATTER.replace("2026-05-10", "May 10, 2026"))
    issues = [i for i in validate(note) if i.field == "date of note"]
    assert any(i.severity is Severity.ERROR for i in issues)


def test_few_keywords_is_warning_not_error():
    fm = textwrap.dedent(
        """
        tags:
          - resource
          - terminology
        keywords:
          - alpha
        topics:
          - Topic A
          - Topic B
        language: markdown
        date of note: 2026-05-10
        status: active
        building_block: concept
        """
    )
    issues = validate(_note(fm))
    keyword_issues = [i for i in issues if i.field == "keywords"]
    assert len(keyword_issues) == 1
    assert keyword_issues[0].severity is Severity.WARNING
    # warning alone does not invalidate
    assert is_valid(_note(fm))


def test_uppercase_tag_is_error():
    note = _note(VALID_FRONTMATTER.replace("- tessellum", "- Tessellum"))
    issues = [i for i in validate(note) if i.field and i.field.startswith("tags[")]
    assert any(i.severity is Severity.ERROR for i in issues)


def test_folgezettel_without_parent_is_error():
    fm = VALID_FRONTMATTER + 'folgezettel: "1a"\n'
    issues = [i for i in validate(_note(fm)) if i.field == "folgezettel_parent"]
    assert any(i.severity is Severity.ERROR for i in issues)


def test_folgezettel_parent_without_folgezettel_is_error():
    fm = VALID_FRONTMATTER + 'folgezettel_parent: "1"\n'
    issues = [i for i in validate(_note(fm)) if i.field == "folgezettel"]
    assert any(i.severity is Severity.ERROR for i in issues)


def test_folgezettel_pair_with_null_parent_is_ok():
    fm = VALID_FRONTMATTER + 'folgezettel: "1"\nfolgezettel_parent: null\n'
    note = _note(fm)
    fz_issues = [
        i for i in validate(note) if i.field in {"folgezettel", "folgezettel_parent"}
    ]
    assert fz_issues == []
    assert is_valid(note)


def test_legacy_fz_parent_alias_is_accepted():
    fm = VALID_FRONTMATTER + 'folgezettel: "1a"\nfz_parent: "1"\n'
    note = _note(fm)
    fz_issues = [
        i for i in validate(note) if i.field in {"folgezettel", "folgezettel_parent"}
    ]
    assert fz_issues == []


def test_note_second_category_field_is_forbidden():
    fm = VALID_FRONTMATTER + "note_second_category: terminology\n"
    issues = [i for i in validate(_note(fm)) if i.field == "note_second_category"]
    assert any(i.severity is Severity.ERROR for i in issues)


def test_validate_accepts_path(tmp_path):
    p = tmp_path / "note.md"
    p.write_text(f"---\n{VALID_FRONTMATTER.strip()}\n---\nBody.\n", encoding="utf-8")
    assert validate(p) == []
    assert validate(str(p)) == []


def test_issue_str_includes_severity_and_field():
    issue = Issue(Severity.ERROR, "tags[0]", "bad value")
    s = str(issue)
    assert "ERROR" in s
    assert "tags[0]" in s
    assert "bad value" in s


@pytest.mark.parametrize(
    "bb_value",
    [
        "concept",
        "procedure",
        "model",
        "argument",
        "counter_argument",
        "hypothesis",
        "empirical_observation",
        "navigation",
    ],
)
def test_all_eight_building_blocks_are_accepted(bb_value):
    note = _note(VALID_FRONTMATTER.replace("building_block: concept", f"building_block: {bb_value}"))
    bb_issues = [i for i in validate(note) if i.field == "building_block"]
    assert bb_issues == []
