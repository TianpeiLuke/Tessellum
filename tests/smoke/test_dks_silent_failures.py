"""Phase C smoke — DKS silent-failure telemetry.

v0.0.60 of plan_composer_dks_robustness §C. Covers:

  - silent_failures recorded on retrieval-client exception
  - silent_failures recorded on _llm_check_disagreement exception
  - silent_failures recorded on garbage-JSON parse (the bigger one —
    a backend returning unparseable text was previously invisible)
  - silent_failures empty on a clean run (back-compat)
  - MetaObservation.silent_failure_count aggregates correctly

Preserves the Phase 5 decide_escalation contract — graceful
degradation still happens. We're only making the silence
observable, not changing semantics.
"""

from __future__ import annotations

import json


from tessellum.composer.llm import MockBackend
from tessellum.dks import (
    DKSCycle,
    DKSObservation,
    MetaObservation,
)
from tessellum.dks.core import DKSCycleResult


def _argument_response(claim: str) -> str:
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


_FULL_LOOP_RESPONSES = {
    "(conservative)": _argument_response("A"),
    "(exploratory)": _argument_response("B"),
    "counter-argument": json.dumps(
        {
            "broken_component": "warrant",
            "counter_claim": "c",
            "reason": "r",
            "strength": "moderate",
        }
    ),
    "pattern discovery": json.dumps({"description": "p", "observed": ["t"]}),
    "rule revision": json.dumps(
        {"claim": "R", "data": "D", "warrant": "Rw", "supersedes": ""}
    ),
}


# ── silent_failures starts empty on a clean run ────────────────────────────


def test_silent_failures_empty_on_clean_run():
    obs = DKSObservation(folgezettel="1", summary="x")
    backend = MockBackend(responses=_FULL_LOOP_RESPONSES)
    result = DKSCycle(observation=obs, warrants=(), backend=backend).run()
    assert isinstance(result, DKSCycleResult)
    assert result.silent_failures == ()


# ── Retrieval failure → silent_failure recorded ────────────────────────────


class _RaisingRetrievalClient:
    """Retrieval client that always raises — for silent-failure testing."""

    def search(self, query, k=5):
        raise RuntimeError("simulated retrieval crash")


def test_silent_failure_recorded_on_retrieval_exception():
    obs = DKSObservation(folgezettel="1", summary="x")
    backend = MockBackend(responses=_FULL_LOOP_RESPONSES)
    result = DKSCycle(
        observation=obs,
        warrants=(),
        backend=backend,
        retrieval_client=_RaisingRetrievalClient(),
    ).run()
    # Retrieval was attempted at least once (argument steps grounded prompts)
    # → at least one silent failure recorded.
    assert len(result.silent_failures) >= 1
    assert all(
        "_format_retrieval_context" in entry for entry in result.silent_failures
    )
    # Graceful degradation preserved — cycle still produced arguments.
    assert result.argument_a is not None
    assert result.argument_b is not None


# ── Garbage JSON → silent_failure recorded ─────────────────────────────────


def test_silent_failure_recorded_on_garbage_json():
    """Backend returns text that can't be parsed as JSON or a JSON object
    extracted from it → silent_failure entry recorded; cycle continues."""
    obs = DKSObservation(folgezettel="1", summary="x")
    # Garbage response for the argument step — no { } to extract.
    backend = MockBackend(default="this is not json at all")
    result = DKSCycle(observation=obs, warrants=(), backend=backend).run()
    # Both arguments produced (with empty data); silent_failures has entries
    # for each garbage parse.
    assert len(result.silent_failures) >= 2
    assert all(
        "_step_argument" in entry or "_step_" in entry
        for entry in result.silent_failures
    )


def test_silent_failure_recorded_on_semantic_disagreement_exception():
    """semantic_disagreement=True with a backend that raises → silent_failure."""
    obs = DKSObservation(folgezettel="1", summary="x")

    class _RaiseOnSecondCall:
        backend_id = "raise"

        def __init__(self):
            self.calls = 0

        def call(self, request):
            self.calls += 1
            # Disagreement check is one of the later calls — raise specifically
            # when the user_prompt mentions "semantic disagreement"
            if "semantic disagreement" in request.user_prompt:
                raise RuntimeError("simulated LLM crash on disagreement step")
            # Otherwise return canned full-loop responses
            from tessellum.composer.llm import LLMResponse

            content = "{}"
            for pattern, resp in _FULL_LOOP_RESPONSES.items():
                if pattern in request.user_prompt:
                    content = resp
                    break
            return LLMResponse(
                content=content,
                elapsed_ms=0.0,
                backend_id=self.backend_id,
                metadata={},
            )

    backend = _RaiseOnSecondCall()
    result = DKSCycle(
        observation=obs,
        warrants=(),
        backend=backend,
        semantic_disagreement=True,
    ).run()
    # silent_failures has the disagreement-step entry
    assert any(
        "_llm_check_disagreement" in entry for entry in result.silent_failures
    )
    # Cycle still completed (fell back to string-compare for disagreement)
    assert result.argument_a is not None


# ── MetaObservation aggregates silent_failure_count ────────────────────────


def test_meta_observation_silent_failure_count_default_zero():
    obs = MetaObservation(
        timestamp="2026-05-11T00:00:00+00:00",
        cycles_examined=10,
        toulmin_failure_counts={"warrant": 8},
    )
    assert obs.silent_failure_count == 0


def test_meta_observation_silent_failure_count_populated():
    obs = MetaObservation(
        timestamp="2026-05-11T00:00:00+00:00",
        cycles_examined=10,
        toulmin_failure_counts={"warrant": 8},
        silent_failure_count=5,
    )
    assert obs.silent_failure_count == 5


def test_llm_proposer_prompt_includes_silent_failure_count():
    """Verify the LLMProposer prompt template surfaces silent_failure_count."""
    from tessellum.dks.meta import LLMProposer

    obs = MetaObservation(
        timestamp="2026-05-11T00:00:00+00:00",
        cycles_examined=20,
        toulmin_failure_counts={"warrant": 16, "premise": 4},
        silent_failure_count=7,
    )
    backend = MockBackend(default=json.dumps({"proposals": []}))
    LLMProposer(backend=backend).generate(obs)
    prompt = backend.calls[0].user_prompt
    assert "silent_failure_count" in prompt
    assert "7" in prompt
