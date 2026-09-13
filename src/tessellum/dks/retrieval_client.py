"""DKS P-side retrieval client — the productive half of R-Cross.

R-Cross (one of the three R-rules from FZ 1a1b) says **System P calls
System D; System D never calls System P**. This module operationalises
the *productive* half: a typed client that lets DKS read through
retrieval, with no path back.

The client is intentionally a thin adapter — it wraps
:func:`tessellum.retrieval.hybrid_search` and re-exposes the fields a
DKS step actually needs (note id, name, score, BM25/dense ranks). The
typing is independent of the underlying retrieval module so the boundary
stays explicit; if retrieval's internal types change, the contract here
doesn't.

Usage from a DKS step:

>>> from tessellum.dks import RetrievalClient
>>> client = RetrievalClient(db_path="data/tessellum.db")
>>> hits = client.search("warrant + scope mismatch", k=10)
>>> [h.note_name for h in hits]
['thought_dks_evolution', 'thought_dks_design_synthesis', ...]

Step 1 (observation capture) and step 6 (pattern discovery) are the
intended primary consumers — both ask "has this observation /
contradiction pattern shown up before?" against the indexed substrate.

The port also carries a **bounded link expansion** (:meth:`RetrievalClient
.expand_links`), which is how :mod:`tessellum.dks.reach` walks the authored
``note_links`` graph without ever importing :mod:`tessellum.indexer`. It is a
read of the same index through the same port, and the port's defining property
is unchanged: there is still no ``index``/``update``/``delete`` surface here.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

MAX_EXPANSION_HOPS: int = 2
"""Hard ceiling on :meth:`RetrievalClient.expand_links`'s ``hops``.

The design admits 1–2 hops of authored-link reach and nothing wider; a request
past this is an error rather than a silent clamp, so the bound stays a parameter
a caller has to reckon with instead of advice it can drift past."""

DEFAULT_EXPANSION_K: int = 50
"""Default cap on neighbours returned by one expansion, before hop filtering."""


@dataclass(frozen=True)
class RetrievalHit:
    """One ranked hit from a DKS-side retrieval call.

    Mirrors :class:`tessellum.retrieval.hybrid.HybridHit` but lives in
    the DKS module so the P→D contract is explicit and DKS callers
    aren't coupled to retrieval's internal types.
    """

    note_id: str
    note_name: str
    score: float
    bm25_rank: int | None
    dense_rank: int | None
    snippet: str | None = None
    """The quoted source SPAN (BM25 excerpt) an argument's evidence cites (P1
    A1.1). ``None`` when the hit surfaced only via dense retrieval or snippets
    were disabled."""


@dataclass(frozen=True)
class LinkNeighbour:
    """One note reached from a seed over the authored ``note_links`` graph.

    Similarity ranks notes; links *connect* them, and the two are different
    reads. ``hops`` is the link distance from the seed the expansion started
    at (never 0 — the seed itself is not its own neighbour) and ``path`` is the
    note ids walked, seed first, so a caller can cite the route it took as
    evidence rather than asserting an unexplained adjacency.
    """

    note_id: str
    note_name: str
    hops: int
    path: tuple[str, ...]


class RetrievalClient:
    """Read-only client for the unified index, scoped for DKS steps.

    Constructed with the index DB path. Each ``search()`` is one
    Reciprocal-Rank-Fusion hybrid call. The client never writes — there
    is no ``index()``, ``update()``, or ``delete()`` surface, and the
    underlying retrieval module exposes no mutating operations either.
    R-Cross discipline: P calls D; D never calls P; P cannot mutate D
    through this client.

    Args:
        db_path: The unified index DB (output of ``tessellum index
            build``). Validated at construction; raises
            :class:`FileNotFoundError` if missing.

    Raises:
        FileNotFoundError: when ``db_path`` does not exist.
    """

    def __init__(self, db_path: Path | str) -> None:
        path = Path(db_path)
        if not path.is_file():
            raise FileNotFoundError(
                f"index DB not found at {path}. "
                f"Run `tessellum index build` first."
            )
        self.db_path: Path = path

    def search(
        self,
        query: str,
        *,
        k: int = 20,
        snippet_length: int | None = 30,
    ) -> list[RetrievalHit]:
        """Hybrid (BM25 + dense) retrieval, ranked by RRF.

        Thin adapter over :func:`tessellum.retrieval.hybrid_search`.
        The default ``k=20`` is the canonical fan-out for warrant
        grounding — large enough for evidence diversity, small enough
        to keep the warrant prompt within the LLM context budget.

        Args:
            query: Free-form text. Passed verbatim to both rankers.
            k: Maximum number of fused results. Default 20.
            snippet_length: Max tokens in each hit's BM25 snippet (the
                quoted source span, P1 A1.1). Default 30; ``None`` disables
                snippet generation.

        Returns:
            List of :class:`RetrievalHit`, descending by RRF score.
            Empty list if ``k <= 0`` or the index has no matching notes.
        """
        # Import lazily so this module stays importable in environments
        # without dense-embedding dependencies until search() actually
        # runs. Retrieval is an optional dependency of DKS; the core
        # cycle works without it.
        from tessellum.retrieval import hybrid_search

        raw_hits = hybrid_search(self.db_path, query, k=k, snippet_length=snippet_length)
        return [
            RetrievalHit(
                note_id=h.note_id,
                note_name=h.note_name,
                score=h.score,
                bm25_rank=h.bm25_rank,
                dense_rank=h.dense_rank,
                snippet=getattr(h, "snippet", None),
            )
            for h in raw_hits
        ]

    def expand_links(
        self,
        seed: str,
        *,
        hops: int = 1,
        k: int = DEFAULT_EXPANSION_K,
        hub_threshold: int | None = None,
    ) -> list[LinkNeighbour]:
        """Bounded expansion from one seed note over the authored link graph.

        Thin adapter over :func:`tessellum.retrieval.best_first_bfs` — the
        undirected projection of ``note_links``, hub-skipped so a popular note
        appears as a hit without exploding the walk through it. This is the
        *reach* read: it surfaces a note the rankers cannot rank, because the
        authored link is evidence of relatedness that no similarity score sees.

        The bound is a hard parameter, not advice. ``hops`` above
        :data:`MAX_EXPANSION_HOPS` raises rather than clamping, so an unbounded
        traversal cannot be requested by accident; ``k`` caps the fan-out.

        Args:
            seed: ``note_id`` (vault-relative path) to expand from. A seed that
                is not in the index yields an empty list, not an error — an
                unknown anchor is a miss, not a failure.
            hops: Maximum link distance, ``1 <= hops <= MAX_EXPANSION_HOPS``.
            k: Maximum neighbours returned. Default
                :data:`DEFAULT_EXPANSION_K`.
            hub_threshold: Directed in-degree above which a note is reported
                but not expanded through. ``None`` uses retrieval's own
                ``DEFAULT_HUB_THRESHOLD`` rather than restating it here.

        Returns:
            List of :class:`LinkNeighbour`, nearest-first (depth-major,
            in-degree-minor). The seed itself is excluded.

        Raises:
            ValueError: when ``hops`` is outside ``1..MAX_EXPANSION_HOPS`` or
                ``k`` is negative.
        """
        if not 1 <= hops <= MAX_EXPANSION_HOPS:
            raise ValueError(
                f"hops={hops} is outside the admitted reach 1..{MAX_EXPANSION_HOPS}; "
                "the hop budget is a hard bound, not a hint"
            )
        if k < 0:
            raise ValueError(f"k={k} must be non-negative")
        # Lazy import for the same reason ``search`` defers: retrieval is an
        # optional dependency of DKS and this module must stay importable
        # without it.
        from tessellum.retrieval.graph import DEFAULT_HUB_THRESHOLD, best_first_bfs

        raw_hits = best_first_bfs(
            self.db_path,
            seed,
            k=k,
            max_depth=hops,
            hub_threshold=DEFAULT_HUB_THRESHOLD if hub_threshold is None else hub_threshold,
        )
        return [
            LinkNeighbour(
                note_id=h.note_id,
                note_name=h.note_name,
                hops=h.depth,
                path=h.path,
            )
            for h in raw_hits
        ]


__all__ = [
    "DEFAULT_EXPANSION_K",
    "MAX_EXPANSION_HOPS",
    "LinkNeighbour",
    "RetrievalHit",
    "RetrievalClient",
]
