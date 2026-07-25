"""DKS refactor P1 — provenance floor (source spans + tri-temporal time).

A1.1 claim-level spans: the BM25 snippet (the quoted source SPAN) now flows
     through hybrid_search -> RetrievalClient -> the argument retrieval-context
     block, instead of being dropped at the fusion layer.
A1.2 tri-temporal stamping: DKSObservation + DKSWarrant carry t_claim /
     t_evidence / t_outcome; a predictive warrant is scorable only when its
     outcome is strictly after its full information set (temporal_holdout_valid).
"""

from __future__ import annotations

from pathlib import Path

from tessellum.dks import (
    DKSObservation,
    DKSWarrant,
    temporal_holdout_valid,
)
from tessellum.dks.retrieval_client import RetrievalClient, RetrievalHit
from tessellum.indexer import build
from tessellum.retrieval.hybrid import hybrid_search


_NOTE = """\
---
tags: [resource, terminology]
keywords: [alpha, beta, gamma]
topics: [X]
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
---

# {name}

{body}
"""


def _mk_index(tmp_path: Path) -> Path:
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary/term_warrant.md").write_text(
        _NOTE.format(
            name="Warrant Precision",
            body="A warrant licenses the move from data to claim. Warrant "
            "precision improves through dialectic disagreement and counter-arguments.",
        )
    )
    db = tmp_path / "idx.db"
    build(v, db)
    return db


# ── A1.1 — source spans flow through to the retrieval context ───────────────


def test_hybrid_search_carries_bm25_snippet(tmp_path: Path) -> None:
    db = _mk_index(tmp_path)
    hits = hybrid_search(db, "warrant precision dialectic", k=5, snippet_length=30)
    assert hits
    # at least one hit surfaced via BM25 carries a non-empty snippet (the span)
    assert any(h.snippet for h in hits)
    # the snippet quotes the source text (highlight markers around matched terms)
    joined = " ".join(h.snippet or "" for h in hits)
    assert "warrant" in joined.lower()


def test_hybrid_search_default_no_snippet_is_backward_compatible(tmp_path: Path) -> None:
    db = _mk_index(tmp_path)
    # default snippet_length=None preserves the prior behavior (no snippet).
    hits = hybrid_search(db, "warrant", k=5)
    assert hits
    assert all(h.snippet is None for h in hits)


def test_retrieval_client_exposes_span(tmp_path: Path) -> None:
    db = _mk_index(tmp_path)
    client = RetrievalClient(db)
    hits = client.search("warrant precision", k=5)  # default snippet_length=30
    assert hits
    assert any(h.snippet for h in hits)


def test_format_retrieval_context_injects_span() -> None:
    # unit-test the formatter directly with a stub client that returns a span.
    from tessellum.dks.core import DKSCycle
    from tessellum.composer import MockBackend

    class _StubClient:
        def search(self, query, *, k=5, **_):
            return [
                RetrievalHit(
                    note_id="resources/term_dictionary/term_warrant.md",
                    note_name="Warrant Precision", score=0.9,
                    bm25_rank=1, dense_rank=None,
                    snippet="a <<<warrant>>> licenses data to claim",
                )
            ]

    cycle = DKSCycle(
        DKSObservation(folgezettel="5", summary="q"),
        (), MockBackend(responses={}), retrieval_client=_StubClient(),
    )
    block = cycle._format_retrieval_context()
    assert "span:" in block
    assert "warrant" in block  # the quoted span made it into the prompt block


def test_format_retrieval_context_no_span_falls_back() -> None:
    from tessellum.dks.core import DKSCycle
    from tessellum.composer import MockBackend

    class _StubClient:
        def search(self, query, *, k=5, **_):
            return [RetrievalHit("n", "N", 0.5, None, 1, snippet=None)]  # dense-only

    cycle = DKSCycle(
        DKSObservation(folgezettel="5", summary="q"),
        (), MockBackend(responses={}), retrieval_client=_StubClient(),
    )
    block = cycle._format_retrieval_context()
    assert "N (score=" in block
    assert "span:" not in block  # no snippet → no span suffix


# ── A1.2 — tri-temporal stamping + holdout validity ─────────────────────────


def test_observation_and_warrant_carry_tri_temporal_fields() -> None:
    obs = DKSObservation(
        folgezettel="5", summary="x",
        t_claim="2026-01-01T00:00:00Z", t_evidence="2026-01-02T00:00:00Z",
        t_outcome="2026-02-01T00:00:00Z",
    )
    assert obs.t_claim == "2026-01-01T00:00:00Z"
    w = DKSWarrant(
        claim="c", data="d", warrant="w",
        t_claim="2026-01-01T00:00:00Z", t_outcome="2026-03-01T00:00:00Z",
    )
    assert w.t_outcome == "2026-03-01T00:00:00Z"
    # backward-compatible default: absent stamps are None.
    assert DKSWarrant(claim="c", data="d", warrant="w").t_claim is None


def test_temporal_holdout_valid_requires_outcome_after_info_set() -> None:
    # outcome strictly after both claim and evidence → valid.
    assert temporal_holdout_valid(
        t_claim="2026-01-01T00:00:00Z",
        t_evidence="2026-01-02T00:00:00Z",
        t_outcome="2026-02-01T00:00:00Z",
    )


def test_temporal_holdout_rejects_leakage() -> None:
    # outcome inside the information set (== evidence) → leakage → invalid.
    assert not temporal_holdout_valid(
        t_claim="2026-01-01T00:00:00Z",
        t_evidence="2026-02-01T00:00:00Z",
        t_outcome="2026-02-01T00:00:00Z",
    )
    # outcome BEFORE the claim → invalid.
    assert not temporal_holdout_valid(
        t_claim="2026-03-01T00:00:00Z",
        t_evidence=None,
        t_outcome="2026-01-01T00:00:00Z",
    )


def test_temporal_holdout_rejects_missing_times() -> None:
    assert not temporal_holdout_valid(None, None, "2026-02-01T00:00:00Z")  # no info time
    assert not temporal_holdout_valid("2026-01-01T00:00:00Z", None, None)  # no outcome
