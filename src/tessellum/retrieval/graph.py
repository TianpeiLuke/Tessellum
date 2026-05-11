"""Best-first BFS over the note-link graph.

**No Personalized PageRank** — empirical measurement of the
Hit@K↔answer-quality correlation came out at ρ=0.37, meaning PPR's
expensive multi-hop walks optimized retrieval metrics that don't
translate to better answers. Best-first BFS is simpler, faster, and
Pareto-optimal in production.

Key design points:

1. **Undirected adjacency for traversal.** Note-link relationships flow
   conceptually both ways: if A links to B, B is also "near" A. We walk
   the undirected projection of the directed ``note_links`` graph.

2. **Directed in-degree as hub signal.** A note with many *inbound* links
   is a popular hub (term_zettelkasten, term_cqrs, etc.). We skip
   expanding neighbors of hubs above a threshold to prevent combinatorial
   blowup ("everything connects to everything via the most-linked note").

3. **Priority queue keyed on depth-major, hub-minor.** Closer-to-seed
   notes surface first; among ties, less-popular (= more-specific) notes
   are preferred. This gives focused, contextually-relevant results.

4. **Score is ``1 / (1 + depth)``.** Higher = closer-to-seed. Hub-skip
   affects ordering inside the priority queue but doesn't penalize the
   final score.
"""

from __future__ import annotations

import heapq
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import networkx as nx

DEFAULT_HUB_THRESHOLD = 50  # nodes with in_degree > this won't expand


@dataclass(frozen=True)
class GraphHit:
    """One hit from a graph-traversal search.

    Attributes:
        note_id: Vault-relative path of the matching note.
        note_name: Filename stem.
        score: ``1 / (1 + depth)`` — higher = closer to seed.
        depth: Hops from seed (1, 2, 3, ...). Seed itself is excluded
            from results.
        path: Sequence of ``note_id`` from seed to this hit (inclusive
            of both endpoints). ``len(path) == depth + 1``.
    """

    note_id: str
    note_name: str
    score: float
    depth: int
    path: tuple[str, ...]


def best_first_bfs(
    db_path: Path | str,
    seed: str,
    *,
    k: int = 20,
    max_depth: int = 3,
    hub_threshold: int = DEFAULT_HUB_THRESHOLD,
) -> list[GraphHit]:
    """Best-first BFS from a seed note over the link graph.

    Args:
        db_path: Index DB (output of ``tessellum index build``).
        seed: ``note_id`` (vault-relative path) of the starting note.
        k: Maximum number of hits.
        max_depth: Maximum hops from seed (default 3).
        hub_threshold: Nodes with directed in-degree > this are
            "hub-skipped": they appear as hits when first reached, but
            their neighbors are not expanded. Prevents combinatorial
            blowup through popular hub notes.

    Returns:
        List of ``GraphHit``, ordered by ascending priority (depth-major,
        in_degree-minor). The seed itself is excluded.

    Raises:
        FileNotFoundError: ``db_path`` doesn't exist.
        sqlite3.OperationalError: ``notes`` or ``note_links`` table
            missing (run ``tessellum index build``).
    """
    db = Path(db_path)
    if not db.is_file():
        raise FileNotFoundError(
            f"index DB not found at {db}. Run `tessellum index build` first."
        )

    if k <= 0 or max_depth <= 0:
        return []

    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    try:
        graph, names = _load_graph(conn)
    finally:
        conn.close()

    if seed not in graph:
        return []

    # Undirected view for traversal — conceptual relationships flow both ways.
    adj = graph.to_undirected(as_view=True)

    # In-degree of the DIRECTED graph as the hub signal.
    in_degrees = dict(graph.in_degree())

    # Priority queue. Tuple ordering: (priority, depth, node, path).
    # priority = (depth * 1000) + in_degree of node — depth-major sort
    # means we exhaust each depth ring before going deeper; in_degree
    # secondary tiebreaker prefers less-popular (more-specific) notes.
    visited: set[str] = {seed}
    pq: list[tuple[int, int, str, tuple[str, ...]]] = [(0, 0, seed, (seed,))]
    hits: list[GraphHit] = []

    while pq and len(hits) < k:
        priority, depth, node, path = heapq.heappop(pq)

        if node != seed:
            hits.append(
                GraphHit(
                    note_id=node,
                    note_name=names.get(node, _name_from_id(node)),
                    score=1.0 / (1.0 + depth),
                    depth=depth,
                    path=path,
                )
            )
            if len(hits) >= k:
                break

        if depth >= max_depth:
            continue

        # Hub-skip: don't expand neighbors of high-degree nodes (except seed,
        # which always expands — it's the user's chosen entry point).
        if node != seed and in_degrees.get(node, 0) > hub_threshold:
            continue

        for neighbor in adj.neighbors(node):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            new_priority = (depth + 1) * 1000 + in_degrees.get(neighbor, 0)
            heapq.heappush(
                pq,
                (new_priority, depth + 1, neighbor, path + (neighbor,)),
            )

    return hits


def _load_graph(conn: sqlite3.Connection) -> tuple[nx.DiGraph, dict[str, str]]:
    """Build a NetworkX DiGraph from the indexed DB.

    Returns:
        (graph, name_index) — graph has all notes as nodes; name_index
        maps note_id → note_name.
    """
    graph = nx.DiGraph()
    names: dict[str, str] = {}

    for row in conn.execute("SELECT note_id, note_name FROM notes"):
        graph.add_node(row["note_id"])
        names[row["note_id"]] = row["note_name"]

    for row in conn.execute(
        "SELECT source_note_id, target_note_id FROM note_links"
    ):
        graph.add_edge(row["source_note_id"], row["target_note_id"])

    return graph, names


def _name_from_id(note_id: str) -> str:
    """Fallback: derive note_name from note_id stem if not in the index."""
    return Path(note_id).stem
