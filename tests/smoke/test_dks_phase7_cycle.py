"""Smoke tests for Phase 7's DKSCycle additions (v0.0.49).

- retrieval_client kwarg + _format_retrieval_context prompt augmentation
- semantic_disagreement kwarg + LLM-based step-4 detection
- Default behaviour unchanged when neither is wired (Phase 1 back-compat)
"""

from __future__ import annotations

import json
import textwrap

import pytest

from tessellum.composer import MockBackend
from tessellum.dks import (
    DKSCycle,
    DKSObservation,
    RetrievalClient,
)
from tessellum.indexer import build


def _arg_response(claim: str) -> str:
    return json.dumps(
        {
            "claim": claim,
            "data": "D",
            "warrant": "W",
            "backing": "",
            "qualifier": "",
            "evidence": "E",
        }
    )


# ── Retrieval-grounded argument prompt ──────────────────────────────────────


@pytest.fixture
def retrieval_db(tmp_path):
    """Index a tiny vault for RetrievalClient."""
    v = tmp_path / "v"
    (v / "resources/term_dictionary").mkdir(parents=True)
    (v / "resources/term_dictionary" / "term_alpha.md").write_text(
        textwrap.dedent(
            """\
            ---
            tags: [resource, terminology]
            keywords: [a, b, c]
            topics: [Tx, Ty]
            language: markdown
            date of note: 2026-05-10
            status: active
            building_block: concept
            ---

            # Alpha

            Body mentioning alpha and signal.
            """
        )
    )
    db = tmp_path / "tess.db"
    build(v, db, with_dense=False)
    return db


def test_cycle_without_retrieval_client_back_compat():
    """No retrieval_client → prompt doesn't gain a retrieval block; behaviour
    identical to Phase 1."""
    backend = MockBackend(
        responses={
            "conservative": _arg_response("A"),
            "exploratory": _arg_response("A"),  # agree → short-circuit
        }
    )
    obs = DKSObservation(folgezettel="1", summary="alpha signal observed")
    result = DKSCycle(obs, (), backend).run()
    # Both backend calls should have happened — check there's no
    # "Related material" injected in the prompts:
    assert all(
        "Related material" not in call.user_prompt for call in backend.calls
    )
    assert result.closed_loop is False  # claims agreed


def test_cycle_with_retrieval_client_injects_substrate_context(retrieval_db):
    """retrieval_client wired → argument prompts get the substrate block."""
    backend = MockBackend(
        responses={
            "conservative": _arg_response("A"),
            "exploratory": _arg_response("A"),
        }
    )
    client = RetrievalClient(retrieval_db)
    obs = DKSObservation(folgezettel="1", summary="alpha signal")
    DKSCycle(obs, (), backend, retrieval_client=client).run()
    # The first argument call should include the substrate block
    arg_call = next(c for c in backend.calls if "conservative" in c.user_prompt)
    assert "Related material from the substrate" in arg_call.user_prompt
    assert "term_alpha" in arg_call.user_prompt


def test_cycle_with_retrieval_client_empty_db_skips_block(tmp_path):
    """Empty vault → search returns no hits → block omitted entirely."""
    # Build an empty index DB
    v = tmp_path / "v"
    v.mkdir()
    db = tmp_path / "empty.db"
    build(v, db, with_dense=False)

    backend = MockBackend(
        responses={
            "conservative": _arg_response("A"),
            "exploratory": _arg_response("A"),
        }
    )
    client = RetrievalClient(db)
    obs = DKSObservation(folgezettel="1", summary="no hits expected")
    DKSCycle(obs, (), backend, retrieval_client=client).run()
    arg_call = next(c for c in backend.calls if "conservative" in c.user_prompt)
    assert "Related material from the substrate" not in arg_call.user_prompt


# ── Semantic disagreement detection ─────────────────────────────────────────


def test_cycle_semantic_disagreement_off_by_default_uses_string_compare():
    """Default behaviour: string-compare. Same claim → no contradicts."""
    backend = MockBackend(
        responses={
            "conservative": _arg_response("Same exact claim"),
            "exploratory": _arg_response("Same exact claim"),
        }
    )
    obs = DKSObservation(folgezettel="1", summary="x")
    result = DKSCycle(obs, (), backend).run()
    assert result.contradicts is None


def test_cycle_semantic_disagreement_true_calls_llm():
    """semantic_disagreement=True → an extra LLM call for the disagreement check."""
    backend = MockBackend(
        responses={
            "conservative": _arg_response("Claim A"),
            "exploratory": _arg_response("Claim B"),
            "semantic disagreement check": json.dumps({"disagree": True}),
            "counter-argument": json.dumps(
                {
                    "broken_component": "warrant",
                    "counter_claim": "cc",
                    "reason": "r",
                    "strength": "moderate",
                }
            ),
            "pattern discovery": json.dumps(
                {"description": "p", "observed": ["t"]}
            ),
            "rule revision": json.dumps(
                {"claim": "R", "data": "D", "warrant": "Rw", "supersedes": ""}
            ),
        }
    )
    obs = DKSObservation(folgezettel="1", summary="x")
    result = DKSCycle(obs, (), backend, semantic_disagreement=True).run()
    # The semantic-check call should have happened
    semantic_calls = [
        c for c in backend.calls
        if "semantic disagreement check" in c.user_prompt
    ]
    assert len(semantic_calls) == 1
    # And A vs B differ → contradicts fires
    assert result.contradicts is not None


def test_cycle_semantic_disagreement_overrides_string_compare():
    """semantic_disagreement says NO disagreement → contradicts is None,
    even if strings differ."""
    backend = MockBackend(
        responses={
            "conservative": _arg_response("X is true"),
            "exploratory": _arg_response("X really is true"),  # strings differ
            "semantic disagreement check": json.dumps({"disagree": False}),
        }
    )
    obs = DKSObservation(folgezettel="1", summary="x")
    result = DKSCycle(obs, (), backend, semantic_disagreement=True).run()
    assert result.contradicts is None


def test_cycle_semantic_disagreement_falls_back_on_parse_failure():
    """LLM returns garbage → fall back to string-compare."""
    backend = MockBackend(
        responses={
            "conservative": _arg_response("Claim A"),
            "exploratory": _arg_response("Claim B"),
            "semantic disagreement check": "not even json",
        }
    )
    obs = DKSObservation(folgezettel="1", summary="x")
    # Even with semantic_disagreement=True, malformed LLM → fall back
    # to string-compare. "Claim A" != "Claim B" → contradicts fires.
    result = DKSCycle(obs, (), backend, semantic_disagreement=True).run()
    # The semantic call happened but parsing failed → fallback fires
    assert result.contradicts is not None
