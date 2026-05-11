"""Smoke tests for the `tessellum bb audit` CLI subcommand (Phase 6, v0.0.48).

Reads BBGraph.from_db() telemetry: node counts by BBType, edge counts by
schema label, untyped corpus edges, orphan nodes, unrealised schema edges.
"""

from __future__ import annotations

import json
import textwrap

import pytest

from tessellum.cli.main import main
from tessellum.indexer import build


_NOTE_TEMPLATE = textwrap.dedent(
    """\
    ---
    tags:
      - {category}
      - {tag2}
    keywords: [a, b, c]
    topics: [Tx, Ty]
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: {bb}
    {fz_block}
    ---

    # {title}

    {body}
    """
)


def _note(vault, sub, slug, bb, body, fz=None, parent=None, tag2="analysis", category="resource"):
    (vault / sub).mkdir(parents=True, exist_ok=True)
    fz_lines = []
    if fz is not None:
        fz_lines.append(f'folgezettel: "{fz}"')
        fz_lines.append(f'folgezettel_parent: "{parent or ""}"')
    (vault / sub / f"{slug}.md").write_text(
        _NOTE_TEMPLATE.format(
            category=category, tag2=tag2, bb=bb,
            title=slug.replace("_", " ").title(),
            body=body, fz_block="\n".join(fz_lines),
        )
    )


@pytest.fixture
def audit_db(tmp_path):
    """Vault: 1 obs + 1 arg + 1 counter + 1 model. Mixed corpus shape."""
    v = tmp_path / "v"
    v.mkdir()
    _note(v, "resources/analysis_thoughts", "obs_one", "empirical_observation",
          "Observation body.", fz="1", parent="")
    _note(v, "resources/analysis_thoughts", "arg_one", "argument",
          "From [obs_one](obs_one.md).", fz="1a", parent="1")
    _note(v, "resources/analysis_thoughts", "counter_one", "counter_argument",
          "Attacks [arg_one](arg_one.md).", fz="1aa", parent="1a")
    _note(v, "areas/models", "model_one", "model",
          "Pattern from [counter_one](../analysis_thoughts/counter_one.md).",
          fz="1aaa", parent="1aa", tag2="model", category="area")
    db = tmp_path / "tess.db"
    build(v, db, with_dense=False)
    return db


# ── Invocation errors ───────────────────────────────────────────────────────


def test_cli_bb_audit_missing_db_returns_2(tmp_path, capsys):
    code = main(["bb", "audit", "--db", str(tmp_path / "missing.db")])
    assert code == 2
    err = capsys.readouterr().err
    assert "not found" in err


def test_cli_bb_no_subcommand_returns_2(capsys):
    code = main(["bb"])
    assert code == 2
    err = capsys.readouterr().err
    assert "missing sub-subcommand" in err


# ── Human-format output ────────────────────────────────────────────────────


def test_cli_bb_audit_human_summary(audit_db, capsys):
    code = main(["bb", "audit", "--db", str(audit_db)])
    assert code == 0
    out = capsys.readouterr().out
    # Header includes node/edge counts
    assert "4 BB nodes" in out
    # Each BB type with count > 0 is listed
    assert "empirical_observation" in out
    assert "argument" in out
    assert "counter_argument" in out
    assert "model" in out


def test_cli_bb_audit_lists_untyped_edges(audit_db, capsys):
    """The fixture's body links point upstream (arg→obs, counter→arg,
    model→counter) — most are reverse-direction matches against
    BB_SCHEMA. Some may be untyped depending on schema coverage."""
    code = main(["bb", "audit", "--db", str(audit_db)])
    assert code == 0
    out = capsys.readouterr().out
    # The output should include the untyped-edges section header
    # (or at least the schema/edge tallies)
    assert "Edges" in out or "Untyped" in out


# ── JSON output ────────────────────────────────────────────────────────────


def test_cli_bb_audit_json_shape(audit_db, capsys):
    code = main(["bb", "audit", "--db", str(audit_db), "--format", "json"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    for field in (
        "node_count",
        "edge_count",
        "nodes_by_type",
        "edges_by_label",
        "untyped_edge_count",
        "untyped_edges_by_bb_pair",
        "orphan_node_count",
        "unrealised_schema_edges",
        "schema_edge_count",
        "realised_schema_edge_count",
    ):
        assert field in payload, f"audit JSON missing field {field!r}"
    assert payload["node_count"] == 4
    assert isinstance(payload["nodes_by_type"], dict)
    assert payload["nodes_by_type"]["argument"] == 1
    assert payload["schema_edge_count"] >= 16  # 8 epistemic + 7 nav + 1+ extensions


def test_cli_bb_audit_json_omits_verbose_untyped_list_by_default(audit_db, capsys):
    """Without --show-untyped, the verbose per-edge list is omitted from JSON."""
    code = main(["bb", "audit", "--db", str(audit_db), "--format", "json"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert "untyped_edges" not in payload
    # The aggregated counts are still present
    assert "untyped_edges_by_bb_pair" in payload


def test_cli_bb_audit_show_untyped_includes_verbose_list(audit_db, capsys):
    code = main(
        ["bb", "audit", "--db", str(audit_db), "--format", "json", "--show-untyped"]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert "untyped_edges" in payload
    assert isinstance(payload["untyped_edges"], list)


def test_cli_bb_audit_reports_unrealised_schema_edges(audit_db, capsys):
    """A small 4-node vault realises only a few schema edges; the rest
    are 'unrealised' — expected."""
    code = main(["bb", "audit", "--db", str(audit_db), "--format", "json"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    # Realised count is small; most schema edges are unrealised
    assert payload["realised_schema_edge_count"] < payload["schema_edge_count"]
    assert len(payload["unrealised_schema_edges"]) > 0


def test_banner_lists_bb_audit(capsys):
    code = main([])
    assert code == 0
    out = capsys.readouterr().out
    assert "tessellum bb audit" in out


def test_cli_bb_audit_orphan_detection(tmp_path, capsys):
    """A BB-typed note with no inbound or outbound corpus edges is an orphan."""
    v = tmp_path / "v"
    v.mkdir()
    _note(v, "resources/term_dictionary", "term_lone", "concept",
          "Isolated concept with no links.", tag2="terminology")
    db = tmp_path / "tess.db"
    build(v, db, with_dense=False)

    code = main(["bb", "audit", "--db", str(db), "--format", "json"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["orphan_node_count"] == 1
    assert payload["orphan_nodes"][0]["bb_type"] == "concept"
