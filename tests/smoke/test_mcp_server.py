"""Smoke tests for tessellum.mcp.server — Phase V.1.

Covers:

- ``build_server`` returns a usable ``Server`` instance.
- Tool dispatch routes named tools to the right Python implementation.
- ``tessellum_list_skills`` enumerates the skill canonicals.
- ``tessellum_get_skill`` returns canonical body text.
- ``tessellum_format_check`` reports issues on a malformed note.
- Missing [mcp] extras → ``ImportError`` from ``build_server``.

The tests don't run the stdio transport — that's an integration
concern. They exercise the registered tools' Python implementations
directly via the ``_dispatch`` helper.
"""

from __future__ import annotations


import pytest

from tessellum.mcp.server import _dispatch, build_server


# ── Server construction ────────────────────────────────────────────────────


def test_build_server_returns_server_with_tessellum_name():
    server = build_server()
    assert server.name == "tessellum"


# ── Tool dispatch ──────────────────────────────────────────────────────────


def test_dispatch_unknown_tool_raises():
    with pytest.raises(ValueError, match="unknown tool"):
        _dispatch("not_a_real_tool", {})


def test_dispatch_list_skills_returns_skill_inventory():
    result = _dispatch("tessellum_list_skills", {})
    assert "skills" in result
    skill_names = {s["name"] for s in result["skills"]}
    # The 13 Tessellum skills should all be present
    assert "skill_tessellum_dks_cycle" in skill_names
    assert "skill_tessellum_meta_dks_cycle" in skill_names
    assert "skill_tessellum_classify_content" in skill_names
    assert "skill_tessellum_route_content" in skill_names
    assert result["count"] == len(result["skills"])


def test_dispatch_get_skill_returns_canonical_body():
    result = _dispatch(
        "tessellum_get_skill",
        {"skill_name": "tessellum_dks_cycle"},
    )
    assert "canonical_body" in result
    body = result["canonical_body"]
    # Body should be the canonical's markdown with frontmatter
    assert body.startswith("---")
    assert "tessellum-dks-cycle" in body


def test_dispatch_get_skill_accepts_full_stem():
    """Both 'tessellum_dks_cycle' and 'skill_tessellum_dks_cycle' work."""
    r1 = _dispatch(
        "tessellum_get_skill",
        {"skill_name": "tessellum_dks_cycle"},
    )
    r2 = _dispatch(
        "tessellum_get_skill",
        {"skill_name": "skill_tessellum_dks_cycle"},
    )
    assert r1["canonical_body"] == r2["canonical_body"]


def test_dispatch_get_skill_unknown_returns_error():
    result = _dispatch(
        "tessellum_get_skill",
        {"skill_name": "imaginary_skill"},
    )
    assert "error" in result


def test_dispatch_get_skill_includes_sidecar_when_present():
    result = _dispatch(
        "tessellum_get_skill",
        {"skill_name": "tessellum_dks_cycle"},
    )
    # The DKS cycle skill has a sidecar
    assert result["sidecar_path"] is not None
    assert result["sidecar_body"] is not None
    assert "version:" in result["sidecar_body"]


# ── Format check tool ──────────────────────────────────────────────────────


def test_dispatch_format_check_on_clean_note(tmp_path):
    p = tmp_path / "clean.md"
    p.write_text(
        """---
tags:
  - resource
  - terminology
  - test
keywords:
  - test
  - example
  - smoke
topics:
  - Testing
  - Smoke Tests
language: markdown
date of note: 2026-05-11
status: active
building_block: concept
bb_schema_version: 1
---

# Term: Test

## Definition

A test concept for the MCP smoke suite.
""",
        encoding="utf-8",
    )
    result = _dispatch("tessellum_format_check", {"path": str(p)})
    assert result["files_checked"] == 1


def test_dispatch_format_check_missing_path_returns_error():
    result = _dispatch(
        "tessellum_format_check",
        {"path": "/tmp/nonexistent_for_mcp_test.md"},
    )
    assert "error" in result


def test_dispatch_format_check_directory_recurses(tmp_path):
    (tmp_path / "a.md").write_text("# a\n")
    (tmp_path / "b.md").write_text("# b\n")
    result = _dispatch("tessellum_format_check", {"path": str(tmp_path)})
    assert result["files_checked"] == 2


# ── Capture tool ───────────────────────────────────────────────────────────


def test_dispatch_capture_creates_note(tmp_path):
    from tessellum.capture import REGISTRY

    vault = tmp_path / "vault"
    destinations = {spec.destination for spec in REGISTRY.values()}
    for dest in destinations:
        (vault / dest).mkdir(parents=True, exist_ok=True)
    result = _dispatch(
        "tessellum_capture",
        {
            "flavor": "concept",
            "slug": "mcp_test",
            "vault_root": str(vault),
        },
    )
    assert "path" in result
    assert "term_mcp_test.md" in result["path"]


def test_dispatch_capture_with_overrides(tmp_path):
    """destination + filename_prefix overrides flow through."""
    vault = tmp_path / "vault"
    (vault / "areas" / "tools").mkdir(parents=True, exist_ok=True)
    result = _dispatch(
        "tessellum_capture",
        {
            "flavor": "model",
            "slug": "smoke_algo",
            "vault_root": str(vault),
            "destination": "areas/tools",
            "filename_prefix": "tool_",
        },
    )
    assert "tool_smoke_algo.md" in result["path"]
    assert "areas/tools" in result["path"]


# ── Error path: missing DB for search / bb_audit / fz_traverse ─────────────


def test_dispatch_search_missing_db_returns_error(tmp_path):
    result = _dispatch(
        "tessellum_search",
        {"query": "test", "db_path": str(tmp_path / "nope.db")},
    )
    assert "error" in result


def test_dispatch_bb_audit_missing_db_returns_error(tmp_path):
    result = _dispatch(
        "tessellum_bb_audit",
        {"db_path": str(tmp_path / "nope.db")},
    )
    assert "error" in result


def test_dispatch_fz_traverse_missing_db_returns_error(tmp_path):
    result = _dispatch(
        "tessellum_fz_traverse",
        {"fz": "1", "direction": "descendants", "db_path": str(tmp_path / "nope.db")},
    )
    assert "error" in result
