"""Wave 3 smoke — five materializers × happy/error paths."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tessellum.composer import (
    MaterializedOutput,
    MaterializerError,
    materialize,
)


# ── no_op (DESCRIBE) ──────────────────────────────────────────────────────


def test_no_op_parses_json(tmp_path: Path) -> None:
    out = materialize("no_op", '{"a": 1}', vault_root=tmp_path)
    assert isinstance(out, MaterializedOutput)
    assert out.structured == {"a": 1}
    assert out.files_written == ()
    assert out.files_applied == ()


def test_no_op_tolerates_non_json(tmp_path: Path) -> None:
    """Non-JSON wraps in {'text': …} so downstream placeholders still resolve."""
    out = materialize("no_op", "free-form text", vault_root=tmp_path)
    assert out.structured == {"text": "free-form text"}


def test_no_op_empty_response(tmp_path: Path) -> None:
    out = materialize("no_op", "", vault_root=tmp_path)
    assert out.structured == {}


# ── body_markdown_to_file (PRODUCE, JSON envelope) ────────────────────────


def test_body_markdown_to_file_writes(tmp_path: Path) -> None:
    payload = json.dumps({"output_path": "notes/foo.md", "body_markdown": "hello"})
    out = materialize("body_markdown_to_file", payload, vault_root=tmp_path)
    assert len(out.files_written) == 1
    written = out.files_written[0]
    assert written.read_text(encoding="utf-8") == "hello"


def test_body_markdown_to_file_dry_run(tmp_path: Path) -> None:
    payload = json.dumps({"output_path": "notes/foo.md", "body_markdown": "hello"})
    out = materialize("body_markdown_to_file", payload, vault_root=tmp_path, dry_run=True)
    assert out.files_written == ()
    assert not (tmp_path / "notes" / "foo.md").exists()


def test_body_markdown_to_file_missing_output_path(tmp_path: Path) -> None:
    with pytest.raises(MaterializerError, match="output_path"):
        materialize(
            "body_markdown_to_file",
            json.dumps({"body_markdown": "hello"}),
            vault_root=tmp_path,
        )


def test_body_markdown_to_file_invalid_json(tmp_path: Path) -> None:
    with pytest.raises(MaterializerError, match="not valid JSON"):
        materialize("body_markdown_to_file", "{not json", vault_root=tmp_path)


# ── body_markdown_frontmatter_to_file (PRODUCE, direct write) ─────────────


def test_body_markdown_frontmatter_to_file_writes(tmp_path: Path) -> None:
    text = (
        "---\n"
        "output_path: notes/bar.md\n"
        "tags:\n"
        "  - resource\n"
        "  - term\n"
        "---\n"
        "# Bar\n\nbody text\n"
    )
    out = materialize("body_markdown_frontmatter_to_file", text, vault_root=tmp_path)
    written = out.files_written[0]
    content = written.read_text(encoding="utf-8")
    # output_path stripped from frontmatter; remaining frontmatter preserved.
    assert "output_path" not in content
    assert "tags:" in content
    assert "# Bar" in content
    assert out.structured["output_path"] == "notes/bar.md"


def test_body_markdown_frontmatter_to_file_missing_frontmatter(tmp_path: Path) -> None:
    with pytest.raises(MaterializerError, match="missing YAML frontmatter"):
        materialize(
            "body_markdown_frontmatter_to_file",
            "# no frontmatter at all",
            vault_root=tmp_path,
        )


def test_body_markdown_frontmatter_to_file_missing_output_path(tmp_path: Path) -> None:
    text = "---\ntags: [a]\n---\nbody"
    with pytest.raises(MaterializerError, match="output_path"):
        materialize("body_markdown_frontmatter_to_file", text, vault_root=tmp_path)


# ── edits_apply_to_files (APPLY, JSON envelope) ───────────────────────────


def test_edits_apply_to_files_overwrites(tmp_path: Path) -> None:
    target = tmp_path / "x.md"
    target.write_text("old", encoding="utf-8")
    payload = json.dumps({"edits": [{"file": "x.md", "content": "new"}]})
    out = materialize("edits_apply_to_files", payload, vault_root=tmp_path)
    assert len(out.files_applied) == 1
    assert target.read_text(encoding="utf-8") == "new"


def test_edits_apply_to_files_missing_edits_field(tmp_path: Path) -> None:
    with pytest.raises(MaterializerError, match="edits"):
        materialize("edits_apply_to_files", json.dumps({}), vault_root=tmp_path)


def test_edits_apply_to_files_dry_run(tmp_path: Path) -> None:
    target = tmp_path / "x.md"
    target.write_text("old", encoding="utf-8")
    payload = json.dumps({"edits": [{"file": "x.md", "content": "new"}]})
    out = materialize("edits_apply_to_files", payload, vault_root=tmp_path, dry_run=True)
    assert out.files_applied == ()
    assert target.read_text(encoding="utf-8") == "old"


# ── edits_apply_xml_tags (APPLY, XML wire format) ─────────────────────────


def test_edits_apply_xml_tags_writes(tmp_path: Path) -> None:
    target = tmp_path / "y.md"
    target.write_text("old", encoding="utf-8")
    text = (
        "<edits>\n"
        "  <edit><file>y.md</file><content>new content</content></edit>\n"
        "</edits>"
    )
    out = materialize("edits_apply_xml_tags", text, vault_root=tmp_path)
    assert len(out.files_applied) == 1
    assert target.read_text(encoding="utf-8") == "new content"


def test_edits_apply_xml_tags_no_blocks(tmp_path: Path) -> None:
    with pytest.raises(MaterializerError, match="no <edit>"):
        materialize("edits_apply_xml_tags", "no edit blocks here", vault_root=tmp_path)


def test_edits_apply_xml_tags_multiple_edits(tmp_path: Path) -> None:
    text = (
        "<edits>\n"
        "<edit><file>a.md</file><content>aaa</content></edit>\n"
        "<edit><file>b.md</file><content>bbb</content></edit>\n"
        "</edits>"
    )
    out = materialize("edits_apply_xml_tags", text, vault_root=tmp_path)
    assert len(out.files_applied) == 2
    assert (tmp_path / "a.md").read_text(encoding="utf-8") == "aaa"
    assert (tmp_path / "b.md").read_text(encoding="utf-8") == "bbb"


# ── unknown materializer key ──────────────────────────────────────────────


def test_unknown_materializer_raises(tmp_path: Path) -> None:
    with pytest.raises(MaterializerError, match="unknown materializer"):
        materialize("not_a_real_key", "{}", vault_root=tmp_path)
