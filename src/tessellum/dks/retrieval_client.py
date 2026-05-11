"""DKS P-side retrieval client — the productive half of R-Cross.

R-Cross (one of the three R-rules from FZ 1a1b) says **System P calls
System D; System D never calls System P**. Phase 1-3 held R-Cross only
defensively (DKS doesn't import any retrieval-mutating code, and there
isn't any to import). Phase 4 lands the *productive* half: a typed
client that lets DKS read through retrieval, with no path back.

This client is intentionally a thin adapter — it wraps
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
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


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
    ) -> list[RetrievalHit]:
        """Hybrid (BM25 + dense) retrieval, ranked by RRF.

        Thin adapter over :func:`tessellum.retrieval.hybrid_search`. The
        default ``k=20`` matches the plan's specification at FZ 1a1b1 /
        plans/plan_dks_implementation.md Phase 4.

        Args:
            query: Free-form text. Passed verbatim to both rankers.
            k: Maximum number of fused results. Default 20.

        Returns:
            List of :class:`RetrievalHit`, descending by RRF score.
            Empty list if ``k <= 0`` or the index has no matching notes.
        """
        # Import lazily so this module stays importable in environments
        # without dense-embedding dependencies until search() actually
        # runs. Retrieval is the consumer's optional dependency — DKS
        # core (Phase 1) works without it.
        from tessellum.retrieval import hybrid_search

        raw_hits = hybrid_search(self.db_path, query, k=k)
        return [
            RetrievalHit(
                note_id=h.note_id,
                note_name=h.note_name,
                score=h.score,
                bm25_rank=h.bm25_rank,
                dense_rank=h.dense_rank,
            )
            for h in raw_hits
        ]


__all__ = [
    "RetrievalHit",
    "RetrievalClient",
]
