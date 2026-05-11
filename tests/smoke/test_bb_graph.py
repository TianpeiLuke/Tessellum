"""Smoke tests for tessellum.bb.graph — BBNode, BBEdge, BBGraph.

Validates:

  - BBGraph.schema() builds the synthetic schema graph (8 nodes, 16 edges)
  - BBGraph.from_db() loads a corpus graph from a built index DB
  - Body-link edges + folgezettel-parent edges are both surfaced
  - Edge type-checking (corpus edge → schema edge) works
  - Untyped-edge detection surfaces edges with no schema match
  - edges_by_type telemetry counts realised edges per label
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tessellum.bb import BB_SCHEMA, BBEdge, BBGraph, BBNode, BBType
from tessellum.indexer import build


# ── Schema graph ────────────────────────────────────────────────────────────


def test_schema_graph_has_8_nodes_and_16_edges():
    g = BBGraph.schema()
    assert g.node_count == 8
    assert g.edge_count == 16
    # All 8 BB types are represented exactly once
    assert {n.bb_type for n in g} == set(BBType)


def test_schema_graph_provenance_is_schema():
    g = BBGraph.schema()
    for e in g.edges():
        assert e.provenance == "schema"
        assert e.edge_type is not None  # every schema edge knows its type


def test_schema_graph_nodes_of_type_returns_one_per_type():
    g = BBGraph.schema()
    for bb in BBType:
        nodes = g.nodes_of_type(bb)
        assert len(nodes) == 1
        assert nodes[0].bb_type is bb


def test_schema_graph_out_edges_for_model_has_predicting_and_codifying():
    g = BBGraph.schema()
    out = g.out_edges(BBType.MODEL.value)
    labels = {e.edge_type.label for e in out if e.edge_type is not None}
    assert "predicting" in labels
    assert "codifying" in labels


# ── Corpus graph (from_db) ──────────────────────────────────────────────────


_NOTE_TEMPLATE = textwrap.dedent(
    """\
    ---
    tags:
      - {category}
      - {tag2}
    keywords: [{kw1}, {kw2}, {kw3}]
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


def _note(
    vault: Path,
    *,
    sub: str,
    slug: str,
    bb: str,
    body: str,
    fz: str | None = None,
    parent: str | None = None,
    tag2: str = "analysis",
    category: str = "resource",
) -> Path:
    (vault / sub).mkdir(parents=True, exist_ok=True)
    fz_lines = []
    if fz is not None:
        fz_lines.append(f'folgezettel: "{fz}"')
        fz_lines.append(f'folgezettel_parent: "{parent or ""}"')
    fz_block = "\n".join(fz_lines)
    path = vault / sub / f"{slug}.md"
    path.write_text(
        _NOTE_TEMPLATE.format(
            category=category, tag2=tag2,
            kw1="a", kw2="b", kw3="c",
            bb=bb, title=slug.replace("_", " ").title(),
            body=body, fz_block=fz_block,
        )
    )
    return path


@pytest.fixture
def corpus_db(tmp_path):
    """Build a small vault with one example each of several BB types, then index."""
    v = tmp_path / "v"
    v.mkdir()

    # An observation, an argument, a counter, a model — wired by body-links
    # and folgezettel parents.
    _note(
        v, sub="resources/analysis_thoughts", slug="obs_one", bb="empirical_observation",
        fz="1", parent="",
        body="No links.",
    )
    _note(
        v, sub="resources/analysis_thoughts", slug="arg_one", bb="argument",
        fz="1a", parent="1",
        body="Body links to [obs_one](obs_one.md).",
    )
    _note(
        v, sub="resources/analysis_thoughts", slug="counter_one", bb="counter_argument",
        fz="1aa", parent="1a",
        body="Attacks [arg_one](arg_one.md).",
    )
    _note(
        v, sub="areas/models", slug="model_one", bb="model",
        fz="1aaa", parent="1aa",
        body="Pattern from [counter_one](../analysis_thoughts/counter_one.md).",
        tag2="model", category="area",
    )

    db_path = tmp_path / "tess.db"
    build(v, db_path, with_dense=False)
    return db_path


def test_from_db_loads_all_bb_typed_notes(corpus_db):
    g = BBGraph.from_db(corpus_db)
    assert g.node_count == 4
    # Each note is a BBNode of the expected type
    by_id = {n.note_id: n for n in g}
    bb_types = {n.bb_type for n in by_id.values()}
    assert bb_types == {
        BBType.EMPIRICAL_OBSERVATION,
        BBType.ARGUMENT,
        BBType.COUNTER_ARGUMENT,
        BBType.MODEL,
    }


def test_from_db_finds_body_link_edges(corpus_db):
    g = BBGraph.from_db(corpus_db)
    body_link_edges = [e for e in g.edges() if e.provenance == "body_link"]
    # arg→obs, counter→arg, model→counter
    assert len(body_link_edges) >= 3


def test_from_db_finds_folgezettel_parent_edges(corpus_db):
    g = BBGraph.from_db(corpus_db)
    fz_edges = [e for e in g.edges() if e.provenance == "folgezettel_parent"]
    # arg→obs (1a→1), counter→arg (1aa→1a), model→counter (1aaa→1aa)
    assert len(fz_edges) == 3


def test_from_db_types_edges_against_schema(corpus_db):
    """The arg→obs body-link should NOT match a schema edge (no ARG→OBS in BB_SCHEMA);
    counter→arg should NOT match either (BB_SCHEMA has ARG→CTR, not CTR→ARG);
    model→counter should NOT match (BB_SCHEMA has the reverse via CTR→MOD ext);
    the counter→arg folgezettel-parent edge (1aa→1a, CTR→ARG) is untyped."""
    g = BBGraph.from_db(corpus_db)
    untyped = g.untyped_edges()
    # We expect every realised edge in this fixture to be untyped — the
    # schema's directionality runs OBS→...→ARG→CTR→OBS, but our fixture
    # walks the link graph in the opposite direction (downstream-to-upstream).
    assert len(untyped) >= 3


def test_from_db_includes_dks_extension_for_ctr_to_mod():
    """Build a vault where a counter_argument body-links to a model. The corpus
    edge should match the BB_SCHEMA_DKS_EXTENSIONS entry (CTR→MOD)."""
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        v = Path(td) / "v"
        v.mkdir()
        _note(
            v, sub="areas/models", slug="model_ctr_to_mod", bb="model",
            fz="3", parent="",
            body="Pattern note. No outbound links.",
            tag2="model", category="area",
        )
        _note(
            v, sub="resources/analysis_thoughts", slug="counter_links_to_model", bb="counter_argument",
            fz="3a", parent="3",
            body="Pattern aggregates this in [model_ctr_to_mod](../../areas/models/model_ctr_to_mod.md).",
        )
        db = Path(td) / "tess.db"
        build(v, db, with_dense=False)

        g = BBGraph.from_db(db)
        # Find the CTR→MOD body-link edge
        ctr_to_mod = [
            e for e in g.edges()
            if e.provenance == "body_link"
            and g.node(e.source_note_id).bb_type is BBType.COUNTER_ARGUMENT
            and g.node(e.target_note_id).bb_type is BBType.MODEL
        ]
        assert len(ctr_to_mod) == 1
        edge_type = ctr_to_mod[0].edge_type
        assert edge_type is not None
        assert edge_type.label == "pattern_of_failure"


def test_edges_by_type_counts_realised_edges(corpus_db):
    g = BBGraph.from_db(corpus_db)
    counts = g.edges_by_type()
    # At least some "(untyped)" bucket exists for the fixture's reverse-direction edges
    assert "(untyped)" in counts
    assert counts["(untyped)"] >= 3


def test_node_lookup_by_id(corpus_db):
    g = BBGraph.from_db(corpus_db)
    # note_ids are vault-relative paths
    node = g.node("resources/analysis_thoughts/arg_one.md")
    assert node is not None
    assert node.bb_type is BBType.ARGUMENT
    assert node.folgezettel == "1a"
    assert node.folgezettel_parent == "1"


def test_missing_db_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        BBGraph.from_db(tmp_path / "missing.db")


def test_graph_iteration_and_containment(corpus_db):
    g = BBGraph.from_db(corpus_db)
    ids = [n.note_id for n in g]
    assert len(ids) == g.node_count
    assert ids[0] in g
    assert "not-a-real-note.md" not in g
