"""Smoke tests for ``tessellum.format.link_checker``."""

from __future__ import annotations

import textwrap

from tessellum.format import parse_note, parse_text
from tessellum.format.link_checker import check_links

_VALID_FM = textwrap.dedent(
    """
    tags: [resource, terminology]
    keywords: [a, b, c]
    topics: [A, B]
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: concept
    """
).strip()


def _note_with_body(body: str):
    return parse_text(f"---\n{_VALID_FM}\n---\n{body}\n")


def test_link_001_missing_md_extension():
    note = _note_with_body("See [foo](bar) for details.")
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-001" in rule_ids


def test_link_002_absolute_path():
    note = _note_with_body("See [foo](/abs/bar.md).")
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-002" in rule_ids


def test_link_003_broken_target(tmp_path):
    p = tmp_path / "host.md"
    p.write_text(
        f"---\n{_VALID_FM}\n---\nSee [foo](does_not_exist.md).\n",
        encoding="utf-8",
    )
    note = parse_note(p)
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-003" in rule_ids


def test_link_003_resolves_when_target_exists(tmp_path):
    other = tmp_path / "other.md"
    other.write_text("body\n", encoding="utf-8")
    p = tmp_path / "host.md"
    p.write_text(
        f"---\n{_VALID_FM}\n---\nSee [other](other.md).\n",
        encoding="utf-8",
    )
    note = parse_note(p)
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-003" not in rule_ids


def test_link_006_orphan_no_internal_links():
    note = _note_with_body("Body has no internal links at all.")
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-006" in rule_ids


def test_link_006_not_emitted_with_internal_link():
    note = _note_with_body("See [other](other.md) for details.")
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-006" not in rule_ids


def test_external_links_skipped():
    note = _note_with_body(
        "See [home](https://example.com) and [mail](mailto:a@b.c)."
    )
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-001" not in rule_ids
    assert "LINK-002" not in rule_ids
    # No internal md links → orphan
    assert "LINK-006" in rule_ids


def test_anchor_only_links_skipped():
    note = _note_with_body("Jump to [section](#anchor) and [other](#another).")
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-001" not in rule_ids


def test_non_md_extensions_skipped():
    note = _note_with_body(
        "See [diagram](arch.png) and [paper](paper.pdf) and [code](script.py)."
    )
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-001" not in rule_ids


def test_config_file_extensions_skipped():
    """Links to common config-file formats (.toml, .cfg, .ini, .lock, .env)
    should not trip LINK-001. Surfaced when the migration plan linked to
    pyproject.toml from plans/."""
    note = _note_with_body(
        "See [build](pyproject.toml), [setup](setup.cfg), [legacy](setup.ini), "
        "[deps](poetry.lock), [secrets](.env)."
    )
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-001" not in rule_ids


def test_placeholder_targets_skipped():
    note = _note_with_body(
        "See [foo](-) and [bar](<placeholder>) and [baz](...)."
    )
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-001" not in rule_ids


def test_directory_targets_skipped():
    note = _note_with_body("See [docs](docs/) for more.")
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-001" not in rule_ids


def test_fenced_code_block_links_ignored():
    body = textwrap.dedent(
        """
        Real link: [a](good.md)

        ```python
        # this is not a link: [fake](bad-no-extension)
        ```
        """
    ).strip()
    note = _note_with_body(body)
    rule_ids = {i.rule_id for i in check_links(note)}
    # The link inside the code block should NOT trigger LINK-001
    assert "LINK-001" not in rule_ids


def test_link_with_anchor_fragment_validates_path_only():
    note = _note_with_body("See [section](good.md#some-section).")
    # path part is good.md → has .md extension, so LINK-001 doesn't fire
    rule_ids = {i.rule_id for i in check_links(note)}
    assert "LINK-001" not in rule_ids
