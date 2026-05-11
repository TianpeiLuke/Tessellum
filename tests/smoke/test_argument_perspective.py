"""Smoke tests for argument_perspective field + per-perspective MetaObservation (Phase I.3).

Covers:

- DKSArgument records the perspective passed to _step_argument.
- DKSCycleResult.arguments carries the perspective per argument.
- Cycle trace serialiser emits argument_perspective for each argument.
- MetaObservation.per_perspective_breakdown field defaults to empty.
- LLMProposer prompt mentions per_perspective_breakdown.
- template_argument.md template includes argument_perspective placeholder.
"""

from __future__ import annotations

import json


from tessellum.composer.llm import MockBackend
from tessellum.dks.core import DKSCycle, DKSObservation
from tessellum.dks.meta import LLMProposer, MetaObservation


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


_COUNTER_RESPONSE = json.dumps(
    {
        "broken_component": "warrant",
        "counter_claim": "c",
        "reason": "r",
        "strength": "moderate",
    }
)
_PATTERN_RESPONSE = json.dumps({"description": "p", "observed": ["t"]})
_REVISION_RESPONSE = json.dumps(
    {"claim": "R", "data": "D", "warrant": "Rw", "supersedes": ""}
)


def _build_observation(fz: str = "9") -> DKSObservation:
    return DKSObservation(folgezettel=fz, summary="test")


# ── DKSArgument.perspective populated ──────────────────────────────────────


def test_dks_argument_records_perspective():
    """N=2 cycle: argument_a has perspective='conservative', argument_b has 'exploratory'."""
    obs = _build_observation()
    responses = {
        "(conservative)": _argument_response("A"),
        "(exploratory)": _argument_response("B"),
        "counter-argument": _COUNTER_RESPONSE,
        "pattern discovery": _PATTERN_RESPONSE,
        "rule revision": _REVISION_RESPONSE,
    }
    result = DKSCycle(
        observation=obs, warrants=(), backend=MockBackend(responses=responses)
    ).run()
    assert result.argument_a.perspective == "conservative"
    assert result.argument_b.perspective == "exploratory"


def test_dks_argument_records_perspective_n3():
    obs = _build_observation()
    responses = {
        "(p1)": _argument_response("A"),
        "(p2)": _argument_response("B"),
        "(p3)": _argument_response("C"),
        "counter-argument": _COUNTER_RESPONSE,
        "pattern discovery": _PATTERN_RESPONSE,
        "rule revision": _REVISION_RESPONSE,
    }
    result = DKSCycle(
        observation=obs,
        warrants=(),
        backend=MockBackend(responses=responses),
        perspectives=("p1", "p2", "p3"),
    ).run()
    perspectives = [a.perspective for a in result.arguments]
    assert perspectives == ["p1", "p2", "p3"]


# ── MetaObservation per_perspective_breakdown ──────────────────────────────


def test_meta_observation_per_perspective_default_empty():
    obs = MetaObservation(
        timestamp="2026-05-11T00:00:00+00:00",
        cycles_examined=10,
        toulmin_failure_counts={"warrant": 8, "premise": 2},
    )
    assert obs.per_perspective_breakdown == {}


def test_meta_observation_per_perspective_populated():
    obs = MetaObservation(
        timestamp="2026-05-11T00:00:00+00:00",
        cycles_examined=10,
        toulmin_failure_counts={"warrant": 8, "premise": 2},
        per_perspective_breakdown={
            "conservative": {"warrant": 6, "premise": 1},
            "exploratory": {"warrant": 2, "premise": 1},
        },
    )
    assert obs.per_perspective_breakdown["conservative"]["warrant"] == 6


def test_llm_proposer_prompt_includes_per_perspective_breakdown():
    """The LLM proposer prompt mentions per_perspective_breakdown verbatim."""
    obs = MetaObservation(
        timestamp="2026-05-11T00:00:00+00:00",
        cycles_examined=20,
        toulmin_failure_counts={"warrant": 18, "premise": 2},
        per_perspective_breakdown={
            "conservative": {"warrant": 14},
            "exploratory": {"warrant": 4, "premise": 2},
        },
    )
    backend = MockBackend(default=json.dumps({"proposals": []}))
    LLMProposer(backend=backend).generate(obs)
    prompt = backend.calls[0].user_prompt
    assert "per_perspective_breakdown" in prompt
    assert "conservative" in prompt
    assert "exploratory" in prompt


# ── Template includes argument_perspective ─────────────────────────────────


def test_template_argument_includes_perspective_placeholder():
    """template_argument.md frontmatter must include argument_perspective: line."""
    from tessellum.data import templates_dir

    text = (templates_dir() / "template_argument.md").read_text(encoding="utf-8")
    assert "argument_perspective:" in text


def test_capture_argument_writes_perspective_placeholder(tmp_path):
    """After `tessellum capture argument`, the file frontmatter has argument_perspective."""
    from tessellum.capture import capture, REGISTRY

    vault = tmp_path / "vault"
    destinations = {spec.destination for spec in REGISTRY.values()}
    for dest in destinations:
        (vault / dest).mkdir(parents=True, exist_ok=True)
    result = capture("argument", "my_arg", vault_root=vault)
    text = result.path.read_text(encoding="utf-8")
    assert "argument_perspective:" in text
