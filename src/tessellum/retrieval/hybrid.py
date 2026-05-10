"""Hybrid retrieval via Reciprocal Rank Fusion (RRF).

Combines BM25 (lexical) and dense (semantic) rankings into a single
ranked list by summing reciprocal-rank contributions from each ranker.
Per `plans/plan_retrieval_port.md` Wave 3 — the parent project measured
+12 percentage points Hit@5 over the best single strategy (FZ 5e1c3a1a1)
specifically because BM25 and dense retrieve *different* documents.

The RRF formula (Cormack, Clarke, Buettcher 2009):

    RRF_score(d) = Σ over rankers r: 1 / (k1 + rank_r(d))

Where ``k1`` is a smoothing constant (60 is the standard default; smaller
values amplify top-rank contributions, larger values flatten them) and
``rank_r(d)`` is the 1-indexed rank of document ``d`` in ranker ``r``'s
result list. Documents absent from a ranker's top-K contribute 0 from
that ranker.

Implementation note: we run ``bm25_search`` and ``dense_search``
sequentially in Python, then fuse. A single-SQL fusion (UNION ALL of
both top-K, group by note_id, sum reciprocal ranks) would shave a
millisecond on a hot DB but loses readability + reuse. For v0.0.15 we
optimize for clarity; revisit if profiling shows the dual roundtrip is
material.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tessellum.retrieval.bm25 import bm25_search
from tessellum.retrieval.dense import dense_search

# Cormack et al. recommend k1=60 as the smoothing constant. Smaller values
# (e.g. 10) amplify top-rank contributions; larger values (e.g. 100)
# flatten the fusion toward equal weighting.
DEFAULT_RRF_K1 = 60


@dataclass(frozen=True)
class HybridHit:
    """One ranked hit from a hybrid (BM25 + dense) search.

    Attributes:
        note_id: Vault-relative path of the matching note.
        note_name: Filename stem.
        score: RRF score — sum of ``1 / (k1 + rank)`` from each ranker
            this note appeared in. Higher = more relevant. Note that
            absolute values are small (typically ~0.01-0.03 with k1=60);
            the *ranking* is what matters, not the raw magnitudes.
        bm25_rank: 1-indexed rank in the BM25 result list, or ``None`` if
            this note was not in the BM25 top-K.
        dense_rank: 1-indexed rank in the dense result list, or ``None``
            if this note was not in the dense top-K.

    The two ``*_rank`` fields are diagnostic — they show *why* a note was
    retrieved. A note ranked 2 in BM25 and 5 in dense is a "both-rankers
    agree it's relevant" hit (high RRF). A note ranked 1 in dense but
    absent from BM25 is a "semantic-only" hit (lower RRF, but possibly
    interesting).
    """

    note_id: str
    note_name: str
    score: float
    bm25_rank: int | None
    dense_rank: int | None


def hybrid_search(
    db_path: Path | str,
    query: str,
    *,
    k: int = 20,
    k1: int = DEFAULT_RRF_K1,
    per_strategy_k: int | None = None,
) -> list[HybridHit]:
    """Hybrid retrieval: BM25 + dense fused via Reciprocal Rank Fusion.

    Args:
        db_path: Index DB (output of ``tessellum index build``). Must
            have both ``notes_fts`` (BM25) and ``notes_vec`` (dense)
            populated. ``--no-dense`` builds will return BM25-only
            results (dense ranks all None).
        query: Free-form query. Passed verbatim to both rankers — BM25
            applies FTS5 MATCH semantics; dense embeds via
            sentence-transformers.
        k: Maximum number of fused results.
        k1: RRF smoothing constant. Default 60 (Cormack et al. recommend).
        per_strategy_k: How many results to fetch from EACH ranker before
            fusing. Default ``max(2*k, 20)``. Larger values give richer
            fusion but cost more per query; smaller values may drop
            documents that would have ranked well after fusion.

    Returns:
        List of ``HybridHit``, sorted by descending RRF score.

    Raises:
        FileNotFoundError: ``db_path`` doesn't exist.
        sqlite3.OperationalError: ``notes_fts`` table missing (run
            ``tessellum index build``).
    """
    db = Path(db_path)
    if not db.is_file():
        raise FileNotFoundError(
            f"index DB not found at {db}. Run `tessellum index build` first."
        )

    if k <= 0:
        return []

    fetch_k = per_strategy_k if per_strategy_k is not None else max(k * 2, 20)

    bm25_hits = bm25_search(db, query, k=fetch_k, snippet_length=None)
    try:
        dense_hits = dense_search(db, query, k=fetch_k)
    except Exception:  # noqa: BLE001
        # If dense isn't available (e.g. the index was built --no-dense)
        # fall back to BM25-only fusion. Better than failing the query.
        dense_hits = []

    # Aggregate RRF scores per note_id, plus per-ranker ranks for
    # diagnostics. Note that we capture name from whichever ranker first
    # surfaced the note — both rankers should agree on note_name since
    # both join on note_id.
    score: dict[str, float] = {}
    bm25_rank: dict[str, int] = {}
    dense_rank: dict[str, int] = {}
    name: dict[str, str] = {}

    for rank, hit in enumerate(bm25_hits, start=1):
        score[hit.note_id] = score.get(hit.note_id, 0.0) + 1.0 / (k1 + rank)
        bm25_rank[hit.note_id] = rank
        name.setdefault(hit.note_id, hit.note_name)

    for rank, hit in enumerate(dense_hits, start=1):
        score[hit.note_id] = score.get(hit.note_id, 0.0) + 1.0 / (k1 + rank)
        dense_rank[hit.note_id] = rank
        name.setdefault(hit.note_id, hit.note_name)

    # Stable sort by descending score, breaking ties by note_id for
    # deterministic output across runs.
    ranked = sorted(
        score.items(),
        key=lambda nid_score: (-nid_score[1], nid_score[0]),
    )[:k]

    return [
        HybridHit(
            note_id=note_id,
            note_name=name[note_id],
            score=s,
            bm25_rank=bm25_rank.get(note_id),
            dense_rank=dense_rank.get(note_id),
        )
        for note_id, s in ranked
    ]
