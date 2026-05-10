"""Smoke tests for tessellum.format — parser + validator."""

from __future__ import annotations

import re
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

# Body has an internal markdown link so LINK-006 (orphan check) doesn't
# fire, which would otherwise make ``validate(note) == []`` always false.
# parse_text gives note.path == None so LINK-003 (target-exists) is skipped.
DEFAULT_BODY = "Body. See [other](other.md) for related material."


def _note(frontmatter_yaml: str, body: str = DEFAULT_BODY) -> Note:
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
    note = _note(VALID_FRONTMATTER.replace("- resource", "- resourcezz"))
    issues = [i for i in validate(note) if i.field == "tags[0]"]
    assert any(i.severity is Severity.ERROR for i in issues)


def test_invalid_building_block_is_error():
    note = _note(
        VALID_FRONTMATTER.replace("building_block: concept", "building_block: idea")
    )
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
    other = tmp_path / "other.md"
    other.write_text("text\n", encoding="utf-8")  # exists for LINK-003
    p = tmp_path / "note.md"
    p.write_text(
        f"---\n{VALID_FRONTMATTER.strip()}\n---\n{DEFAULT_BODY}\n",
        encoding="utf-8",
    )
    assert validate(p) == []
    assert validate(str(p)) == []


def test_issue_str_includes_severity_and_rule_id_and_field():
    issue = Issue(Severity.ERROR, "TEST-001", "tags[0]", "bad value")
    s = str(issue)
    assert "ERROR" in s
    assert "TEST-001" in s
    assert "tags[0]" in s
    assert "bad value" in s


_RULE_ID_RE = re.compile(r"^(YAML|LINK|TESS)-\d{3}$")


def test_every_issue_has_a_well_formed_rule_id():
    note = _note(
        textwrap.dedent(
            """
            tags:
              - resourcezz
              - terminology
              - Tessellum
            keywords:
              - alpha
            topics:
              - Topic A
            language: markdown
            date of note: not-a-date
            status: shipped
            building_block: idea
            note_second_category: terminology
            """
        ),
        body="Orphan body, no internal links.",
    )
    issues = validate(note)
    assert issues, "expected this fixture to produce many issues"
    for issue in issues:
        assert issue.rule_id, f"missing rule_id on {issue}"
        assert _RULE_ID_RE.match(issue.rule_id), (
            f"rule_id {issue.rule_id!r} doesn't match {_RULE_ID_RE.pattern}"
        )


def test_yaml_100_wiki_link_in_yaml_value_is_error():
    fm = textwrap.dedent(
        """
        tags:
          - resource
          - terminology
        keywords:
          - "[[term_foo]]"
          - bar
          - baz
        topics:
          - A
          - B
        language: markdown
        date of note: 2026-05-10
        status: active
        building_block: concept
        """
    )
    rule_ids = {i.rule_id for i in validate(_note(fm))}
    assert "YAML-100" in rule_ids


def test_yaml_101_markdown_link_in_yaml_value_is_error():
    fm = textwrap.dedent(
        """
        tags:
          - resource
          - terminology
        keywords:
          - "[term_foo](term_foo.md)"
          - bar
          - baz
        topics:
          - A
          - B
        language: markdown
        date of note: 2026-05-10
        status: active
        building_block: concept
        """
    )
    rule_ids = {i.rule_id for i in validate(_note(fm))}
    assert "YAML-101" in rule_ids


def test_severity_info_is_a_valid_severity_value():
    # INFO is a recognized third tier; no current YAML/LINK rule emits INFO
    # by default, but the type must exist for downstream skill canonical use.
    assert Severity.INFO.value == "info"
    issue = Issue(Severity.INFO, "TEST-999", None, "informational")
    assert issue.severity is Severity.INFO


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
    note = _note(
        VALID_FRONTMATTER.replace(
            "building_block: concept", f"building_block: {bb_value}"
        )
    )
    bb_issues = [i for i in validate(note) if i.field == "building_block"]
    assert bb_issues == []
