"""Smoke tests for tessellum.retrieval.best_first_bfs."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tessellum.indexer import build
from tessellum.retrieval import GraphHit, best_first_bfs


_NOTE_TEMPLATE = """\
---
tags:
  - resource
  - terminology
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
building_block: concept
---

# {name}

{body}
"""


def _make_note(name: str, body: str) -> str:
    return _NOTE_TEMPLATE.format(name=name, body=body)


@pytest.fixture
def graph_db(tmp_path):
    """A small linked vault for graph traversal:

        seed → A → C
        seed → B
        seed → D → E

    Plus an unrelated island (F, no links to anything else).
    """
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)

    (v / "resources/term_dictionary/term_seed.md").write_text(
        _make_note(
            "Seed",
            "Links to [A](term_a.md), [B](term_b.md), and [D](term_d.md).",
        )
    )
    (v / "resources/term_dictionary/term_a.md").write_text(
        _make_note("A", "Onward to [C](term_c.md).")
    )
    (v / "resources/term_dictionary/term_b.md").write_text(
        _make_note("B", "Leaf — no further links.")
    )
    (v / "resources/term_dictionary/term_c.md").write_text(
        _make_note("C", "Two hops from seed.")
    )
    (v / "resources/term_dictionary/term_d.md").write_text(
        _make_note("D", "Leads to [E](term_e.md).")
    )
    (v / "resources/term_dictionary/term_e.md").write_text(
        _make_note("E", "Two hops from seed via D.")
    )
    (v / "resources/term_dictionary/term_f.md").write_text(
        _make_note("F", "Isolated island — links to nothing.")
    )
    db_path = tmp_path / "graph.db"
    build(v, db_path, with_dense=False)  # graph traversal doesn't need embeddings
    return db_path


def test_bfs_returns_typed_hits(graph_db):
    hits = best_first_bfs(graph_db, "resources/term_dictionary/term_seed.md")
    assert isinstance(hits, list)
    assert all(isinstance(h, GraphHit) for h in hits)


def test_bfs_excludes_seed_from_results(graph_db):
    hits = best_first_bfs(graph_db, "resources/term_dictionary/term_seed.md")
    note_ids = {h.note_id for h in hits}
    assert "resources/term_dictionary/term_seed.md" not in note_ids


def test_bfs_returns_depth_1_neighbors(graph_db):
    hits = best_first_bfs(graph_db, "resources/term_dictionary/term_seed.md", k=20)
    depth_1 = [h for h in hits if h.depth == 1]
    names = {h.note_name for h in depth_1}
    # seed's direct neighbors are A, B, D
    assert names == {"term_a", "term_b", "term_d"}


def test_bfs_max_depth_limits_traversal(graph_db):
    hits = best_first_bfs(
        graph_db,
        "resources/term_dictionary/term_seed.md",
        k=20,
        max_depth=1,
    )
    # With max_depth=1, only direct neighbors (A, B, D); not C or E.
    names = {h.note_name for h in hits}
    assert names == {"term_a", "term_b", "term_d"}


def test_bfs_reaches_depth_2(graph_db):
    hits = best_first_bfs(
        graph_db,
        "resources/term_dictionary/term_seed.md",
        k=20,
        max_depth=2,
    )
    names = {h.note_name for h in hits}
    # All depth-1 + depth-2 nodes (A, B, C, D, E)
    assert "term_c" in names  # 2 hops via A
    assert "term_e" in names  # 2 hops via D


def test_bfs_skips_islands(graph_db):
    """F has no links from/to seed; should not appear regardless of depth."""
    hits = best_first_bfs(
        graph_db,
        "resources/term_dictionary/term_seed.md",
        k=20,
        max_depth=10,
    )
    names = {h.note_name for h in hits}
    assert "term_f" not in names


def test_bfs_score_is_inverse_depth_plus_one(graph_db):
    hits = best_first_bfs(
        graph_db, "resources/term_dictionary/term_seed.md", k=20, max_depth=2
    )
    for h in hits:
        expected = 1.0 / (1.0 + h.depth)
        assert abs(h.score - expected) < 1e-9


def test_bfs_path_includes_seed_and_target(graph_db):
    hits = best_first_bfs(graph_db, "resources/term_dictionary/term_seed.md", k=5)
    for h in hits:
        assert h.path[0] == "resources/term_dictionary/term_seed.md"
        assert h.path[-1] == h.note_id
        assert len(h.path) == h.depth + 1


def test_bfs_k_limits_results(graph_db):
    hits = best_first_bfs(
        graph_db, "resources/term_dictionary/term_seed.md", k=2
    )
    assert len(hits) <= 2


def test_bfs_k_zero_returns_empty(graph_db):
    hits = best_first_bfs(
        graph_db, "resources/term_dictionary/term_seed.md", k=0
    )
    assert hits == []


def test_bfs_max_depth_zero_returns_empty(graph_db):
    hits = best_first_bfs(
        graph_db,
        "resources/term_dictionary/term_seed.md",
        max_depth=0,
    )
    assert hits == []


def test_bfs_unknown_seed_returns_empty(graph_db):
    hits = best_first_bfs(graph_db, "does/not/exist.md")
    assert hits == []


def test_bfs_missing_db_raises(tmp_path):
    with pytest.raises(FileNotFoundError, match="not found"):
        best_first_bfs(tmp_path / "missing.db", "anything.md")


def test_bfs_undirected_traversal_follows_inbound_links(graph_db):
    """BFS treats links as undirected — a note linked TO from seed is
    still a depth-1 neighbor (and conversely)."""
    # Seed links to A, B, D (outbound). Run BFS *from A* — seed should
    # appear as a depth-1 neighbor (inbound link from seed → A means
    # seed is now A's undirected neighbor).
    hits = best_first_bfs(
        graph_db, "resources/term_dictionary/term_a.md", k=20, max_depth=1
    )
    names = {h.note_name for h in hits}
    assert "term_seed" in names
    assert "term_c" in names  # A's outbound neighbor


def test_bfs_hub_threshold_skips_popular_nodes(tmp_path):
    """A node with in_degree above hub_threshold should not expand its
    neighbors (it appears as a hit, but its onward connections are
    suppressed)."""
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    # Make a hub: 5 nodes all link to term_hub.
    (v / "resources/term_dictionary/term_hub.md").write_text(
        _make_note(
            "Hub",
            "From hub: [A](term_a.md), [B](term_b.md), "
            "[C](term_c.md), [D](term_d.md), [E](term_e.md).",
        )
    )
    for child in ["a", "b", "c", "d", "e"]:
        (v / f"resources/term_dictionary/term_{child}.md").write_text(
            _make_note(
                f"Child {child}",
                f"Links back to [hub](term_hub.md).",
            )
        )
    # term_hub has in_degree 5 (each child links to it).
    # Add a seed that links only to one child.
    (v / "resources/term_dictionary/term_seed.md").write_text(
        _make_note("Seed", "Single edge to [A](term_a.md).")
    )
    db = tmp_path / "hub.db"
    build(v, db, with_dense=False)
    # With hub_threshold=4, term_hub (in_degree=5) is hub-skipped:
    # we reach it (depth 2 via A → hub) but don't expand to other children.
    hits = best_first_bfs(
        db,
        "resources/term_dictionary/term_seed.md",
        k=20,
        max_depth=4,
        hub_threshold=4,
    )
    names = {h.note_name for h in hits}
    # Should reach term_hub
    assert "term_hub" in names
    # But should NOT reach b, c, d, e via hub — only A directly.
    # Actually, term_a links back to hub with no other children, but
    # the children all link to hub, not to each other. With hub-skip
    # at hub, the children b/c/d/e should NOT appear as hits.
    assert "term_b" not in names
    assert "term_c" not in names


def test_bfs_against_real_tessellum_vault():
    """Smoke against the real Tessellum vault — BFS from term_cqrs."""
    repo = Path(__file__).resolve().parents[2]
    vault = repo / "vault"
    if not vault.is_dir():
        pytest.skip(f"real vault not found at {vault}")
    db_path = repo / "data" / "tessellum-test-graph.db"
    db_path.parent.mkdir(exist_ok=True)
    try:
        build(vault, db_path, force=True, with_dense=False)
        hits = best_first_bfs(
            db_path, "resources/term_dictionary/term_cqrs.md", k=10
        )
        assert len(hits) >= 1
        # All hits should have at least 1 hop from the seed.
        for h in hits:
            assert h.depth >= 1
            assert h.path[0] == "resources/term_dictionary/term_cqrs.md"
    finally:
        if db_path.is_file():
            db_path.unlink()
