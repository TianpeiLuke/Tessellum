"""Smoke tests for tessellum.retrieval.router."""

from __future__ import annotations

import pytest

from tessellum.retrieval import RouterDecision, classify_query


def test_classify_empty_query_returns_hybrid_fallback():
    decision = classify_query("")
    assert decision.strategy == "hybrid"
    assert "empty" in decision.reason.lower()


def test_classify_whitespace_query_returns_hybrid():
    decision = classify_query("   \n\t   ")
    assert decision.strategy == "hybrid"


def test_classify_vault_path_returns_bfs():
    decision = classify_query("resources/term_dictionary/term_cqrs.md")
    assert decision.strategy == "bfs"
    assert "path" in decision.reason.lower()


def test_classify_single_token_returns_bm25():
    decision = classify_query("composer")
    assert decision.strategy == "bm25"


def test_classify_short_identifier_returns_bm25():
    decision = classify_query("term_cqrs")
    assert decision.strategy == "bm25"


def test_classify_question_returns_hybrid():
    decision = classify_query("How does Composer compile pipelines?")
    assert decision.strategy == "hybrid"


def test_classify_multi_word_returns_hybrid():
    decision = classify_query("retrieve relevant notes about CQRS")
    assert decision.strategy == "hybrid"


def test_classify_decision_is_typed():
    decision = classify_query("foo")
    assert isinstance(decision, RouterDecision)
    assert decision.strategy in {"metadata", "bfs", "bm25", "dense", "hybrid"}
    assert decision.reason
