"""Smoke tests for tessellum.format — parser + validator."""

from __future__ import annotations

import re
import textwrap
from pathlib import Path

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


# ── TESS-004 — counter_argument must link to argument (Phase 4) ─────────────


_COUNTER_FM_ACTIVE = textwrap.dedent(
    """
    ---
    tags:
      - resource
      - analysis
      - dks
    keywords:
      - counter
      - argument
      - dialectic
    topics:
      - Topic A
      - Topic B
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: counter_argument
    folgezettel: "5a"
    folgezettel_parent: "5"
    ---
    """
).strip()


_ARGUMENT_FM = textwrap.dedent(
    """
    ---
    tags:
      - resource
      - analysis
    keywords:
      - argument
      - alpha
      - beta
    topics:
      - Topic A
      - Topic B
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: argument
    folgezettel: "5"
    folgezettel_parent: ""
    ---

    # The Attacked Argument
    """
).strip()


def _write_pair(tmp_path, counter_body: str, *, counter_status: str = "active"):
    """Returns the counter note's path after writing both files."""
    arg = tmp_path / "argument.md"
    arg.write_text(_ARGUMENT_FM + "\n")

    fm = _COUNTER_FM_ACTIVE.replace(f"status: active", f"status: {counter_status}")
    counter = tmp_path / "counter.md"
    counter.write_text(fm + "\n\n# Counter\n\n" + counter_body + "\n")
    return counter


def test_tess_004_counter_argument_with_argument_link_is_ok(tmp_path):
    """Counter that links to a real BB=argument note: no TESS-004."""
    body = "Attacks the argument: [the argument](argument.md)"
    counter_path = _write_pair(tmp_path, body)
    issues = [i for i in validate(counter_path) if i.rule_id == "TESS-004"]
    assert issues == []


def test_tess_004_counter_argument_without_any_link_is_error(tmp_path):
    """Counter with NO body links and status=active → TESS-004 error."""
    body = "This counter argues against the attacked claim but provides no link."
    counter_path = _write_pair(tmp_path, body)
    issues = [i for i in validate(counter_path) if i.rule_id == "TESS-004"]
    assert len(issues) == 1
    assert issues[0].severity is Severity.ERROR


def test_tess_004_counter_argument_linking_to_non_argument_is_error(tmp_path):
    """Counter that links to a concept (not BB=argument) → TESS-004 error."""
    concept = tmp_path / "concept.md"
    concept.write_text(
        _ARGUMENT_FM.replace("building_block: argument", "building_block: concept") + "\n"
    )
    body = "Links to a concept instead: [some concept](concept.md)"
    counter_path = _write_pair(tmp_path, body)
    issues = [i for i in validate(counter_path) if i.rule_id == "TESS-004"]
    assert len(issues) == 1
    assert issues[0].severity is Severity.ERROR


def test_tess_004_template_status_is_exempt(tmp_path):
    """status=template skips TESS-004 — templates can have placeholder links."""
    body = "Placeholder link: [argument](placeholder_argument.md)"
    counter_path = _write_pair(tmp_path, body, counter_status="template")
    issues = [i for i in validate(counter_path) if i.rule_id == "TESS-004"]
    assert issues == []


def test_tess_004_draft_status_is_exempt(tmp_path):
    """status=draft skips TESS-004 — work in progress."""
    body = "No link yet."
    counter_path = _write_pair(tmp_path, body, counter_status="draft")
    issues = [i for i in validate(counter_path) if i.rule_id == "TESS-004"]
    assert issues == []


def test_tess_004_non_counter_argument_notes_unaffected(tmp_path):
    """A note that is NOT a counter_argument never triggers TESS-004."""
    arg = tmp_path / "arg.md"
    arg.write_text(_ARGUMENT_FM + "\n\nBody with no link to any argument.\n")
    issues = [i for i in validate(arg) if i.rule_id == "TESS-004"]
    assert issues == []


def test_tess_004_skips_when_path_is_unknown():
    """In-memory note (parse_text) has note.path=None → TESS-004 silently skipped."""
    fm_text = "---\n" + _COUNTER_FM_ACTIVE.strip("-\n") + "\n---\n\nBody with no links.\n"
    note = parse_text(fm_text)
    assert note.path is None
    issues = [i for i in validate(note) if i.rule_id == "TESS-004"]
    assert issues == []


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


# ── TESS-005 — every BB→BB body-link should instantiate BB_SCHEMA (Phase 6) ─


_GENERIC_FM_TEMPLATE = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - analysis
    keywords: [a, b, c]
    topics: [Tx, Ty]
    language: markdown
    date of note: 2026-05-10
    status: {status}
    building_block: {bb}
    ---

    # {title}

    {body}
    """
)


def _write_note(tmp_path, slug, bb, body, status="active") -> Path:
    p = tmp_path / f"{slug}.md"
    p.write_text(
        _GENERIC_FM_TEMPLATE.format(
            status=status, bb=bb, title=slug.replace("_", " ").title(), body=body
        )
    )
    return p


def test_tess_005_realised_schema_edge_passes(tmp_path):
    """A body link in the *forward* direction of a BB_SCHEMA edge passes."""
    _write_note(tmp_path, "model_a", "model", "Body.")
    # OBS body links to MOD — reverse direction of OBS→CON→MOD. Not in
    # schema directly (no OBS→MOD edge). Use a real schema pair:
    # MOD→PRO (codifying). Source = model, target = procedure.
    _write_note(tmp_path, "procedure_a", "procedure", "Body.")
    src = _write_note(
        tmp_path, "model_src", "model",
        "Codifies into [procedure_a](procedure_a.md).",
    )
    issues = [i for i in validate(src) if i.rule_id == "TESS-005"]
    assert issues == []


def test_tess_005_back_reference_passes(tmp_path):
    """A body link in the *reverse* direction of a BB_SCHEMA edge passes.

    Schema: argument is produced by hypothesis (HYP→ARG, testing). A
    body link from argument back to hypothesis is the *back-reference*
    — the natural corpus pattern. Bidirectional match catches it.
    """
    _write_note(tmp_path, "hypothesis_a", "hypothesis", "Body.")
    src = _write_note(
        tmp_path, "argument_a", "argument",
        "Tests [hypothesis_a](hypothesis_a.md).",
    )
    issues = [i for i in validate(src) if i.rule_id == "TESS-005"]
    assert issues == []


def test_tess_005_same_bb_cross_reference_is_skipped(tmp_path):
    """ARG → ARG cross-reference is not a transition; rule skips it."""
    _write_note(tmp_path, "argument_a", "argument", "Body.")
    src = _write_note(
        tmp_path, "argument_b", "argument",
        "Cross-reference to [argument_a](argument_a.md).",
    )
    issues = [i for i in validate(src) if i.rule_id == "TESS-005"]
    assert issues == []


def test_tess_005_unrelated_pair_emits_warning(tmp_path):
    """ARG → CONCEPT is not in BB_SCHEMA in either direction → WARNING.

    Term lookups are legitimate corpus patterns but flagged for the
    user's awareness — they could be authoring mistakes, accepted
    documentation, or candidates for a schema extension.
    """
    _write_note(tmp_path, "concept_a", "concept", "Body.")
    src = _write_note(
        tmp_path, "argument_a", "argument",
        "References [concept_a](concept_a.md).",
    )
    issues = [i for i in validate(src) if i.rule_id == "TESS-005"]
    assert len(issues) == 1
    assert issues[0].severity is Severity.WARNING


def test_tess_005_template_status_is_exempt(tmp_path):
    """status=template skips TESS-005 — templates can have placeholders."""
    _write_note(tmp_path, "concept_a", "concept", "Body.")
    src = _write_note(
        tmp_path, "argument_a", "argument",
        "[concept_a](concept_a.md)",
        status="template",
    )
    issues = [i for i in validate(src) if i.rule_id == "TESS-005"]
    assert issues == []


def test_tess_005_skips_when_path_is_unknown():
    """In-memory note (parse_text) has note.path=None → rule skipped."""
    fm = VALID_FRONTMATTER + "building_block: argument\n"
    body = "Link to [concept_a](concept_a.md)"
    note = parse_text(f"---\n{fm.strip()}\n---\n{body}\n")
    assert note.path is None
    issues = [i for i in validate(note) if i.rule_id == "TESS-005"]
    assert issues == []


def test_tess_005_dks_extension_edge_passes(tmp_path):
    """The CTR→MOD DKS extension is in BB_SCHEMA — body link counter→model passes."""
    _write_note(tmp_path, "model_a", "model", "Body.")
    src = _write_note(
        tmp_path, "counter_one", "counter_argument",
        # Need a body link to an argument note for TESS-004 too:
        "[an_arg](an_arg.md). Pattern aggregates in [model_a](model_a.md).",
    )
    # Author the argument so TESS-004 is satisfied separately
    _write_note(tmp_path, "an_arg", "argument", "Body.")
    issues = [i for i in validate(src) if i.rule_id == "TESS-005"]
    assert issues == []
