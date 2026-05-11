"""Smoke tests for tessellum.dks.meta proposer strategies (Phase B.2).

Covers:

- ``HeuristicProposer`` reproduces the v0.0.52 lookup-table behaviour
  (regression).
- ``LLMProposer`` parses well-formed LLM JSON output into
  :class:`SchemaEditProposal` objects.
- ``LLMProposer`` returns ``[]`` on malformed JSON / unexpected shapes.
- ``LLMProposer`` filters proposals naming unknown BBType values.
- The user prompt includes v0.0.53 enrichment fields
  (counter_strength_breakdown, sample_counter_quotes, source_metadata).
- ``MetaCycle`` accepts ``proposer=`` kwarg and delegates to it.
- Replay against the FZ 2c1a validation fixture using MockBackend
  produces a well-formed proposal.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tessellum.bb.types import BBType, EpistemicEdgeType
from tessellum.composer.llm import MockBackend
from tessellum.dks.meta import (
    DEFAULT_MIN_CYCLES,
    HeuristicProposer,
    LLMProposer,
    MetaCycle,
    MetaObservation,
    SchemaEditProposal,
)
from tessellum.dks.meta.runtime import _LLM_PROPOSER_SYSTEM_PROMPT


# ── HeuristicProposer regression ───────────────────────────────────────────


def _obs_warrant_dominant() -> MetaObservation:
    return MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=25,
        toulmin_failure_counts={"warrant": 23, "undercutting": 2},
    )


def test_heuristic_proposer_fires_on_warrant_dominance():
    proposals = HeuristicProposer().generate(_obs_warrant_dominant())
    assert len(proposals) == 1
    p = proposals[0]
    assert p.kind == "add"
    assert p.edge.source == BBType.MODEL
    assert p.edge.target == BBType.PROCEDURE
    assert p.edge.label == "warrant_codification"


def test_heuristic_proposer_silent_below_threshold():
    """Balanced distribution — no component crosses 50%."""
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=DEFAULT_MIN_CYCLES,
        toulmin_failure_counts={"warrant": 5, "premise": 5, "counter-example": 5},
    )
    assert HeuristicProposer().generate(obs) == []


def test_heuristic_proposer_target_failure_filter():
    obs = _obs_warrant_dominant()
    # warrant dominates but we ask for premise → no proposal
    proposals = HeuristicProposer().generate(obs, target_failure="premise")
    assert proposals == []


# ── LLMProposer parsing ────────────────────────────────────────────────────


def _llm_response_one_proposal() -> str:
    return json.dumps(
        {
            "proposals": [
                {
                    "kind": "add",
                    "edge": {
                        "source": "model",
                        "target": "procedure",
                        "label": "warrant_codification",
                    },
                    "motivating_observation": "23/25 warrant counters dominate.",
                    "expected_impact": "Reduces warrant-class failures.",
                    "input_bias_risk": "medium",
                }
            ]
        }
    )


def test_llm_proposer_parses_well_formed_response():
    backend = MockBackend(default=_llm_response_one_proposal())
    proposals = LLMProposer(backend=backend).generate(_obs_warrant_dominant())
    assert len(proposals) == 1
    p = proposals[0]
    assert p.kind == "add"
    assert p.edge.label == "warrant_codification"
    # input_bias_risk is prefixed onto motivating_observation
    assert "input_bias_risk=medium" in p.motivating_observation


def test_llm_proposer_returns_empty_on_malformed_json():
    backend = MockBackend(default="not-json")
    assert LLMProposer(backend=backend).generate(_obs_warrant_dominant()) == []


def test_llm_proposer_returns_empty_on_unexpected_shape():
    # Object missing "proposals" key
    backend = MockBackend(default=json.dumps({"foo": "bar"}))
    assert LLMProposer(backend=backend).generate(_obs_warrant_dominant()) == []
    # Top-level list, not object
    backend2 = MockBackend(default=json.dumps([1, 2, 3]))
    assert LLMProposer(backend=backend2).generate(_obs_warrant_dominant()) == []


def test_llm_proposer_filters_unknown_bbtype():
    """A proposal naming a non-existent BBType is dropped silently."""
    bad_payload = json.dumps(
        {
            "proposals": [
                {
                    "kind": "add",
                    "edge": {
                        "source": "model",
                        "target": "imaginary_bb_type",  # not a real BBType
                        "label": "foo",
                    },
                    "motivating_observation": "x",
                    "expected_impact": "y",
                    "input_bias_risk": "low",
                },
                {
                    "kind": "add",
                    "edge": {
                        "source": "model",
                        "target": "procedure",
                        "label": "valid_edge",
                    },
                    "motivating_observation": "x",
                    "expected_impact": "y",
                    "input_bias_risk": "low",
                },
            ]
        }
    )
    backend = MockBackend(default=bad_payload)
    proposals = LLMProposer(backend=backend).generate(_obs_warrant_dominant())
    assert len(proposals) == 1
    assert proposals[0].edge.label == "valid_edge"


def test_llm_proposer_filters_invalid_kind():
    bad_payload = json.dumps(
        {
            "proposals": [
                {
                    "kind": "invent_new_kind",
                    "edge": {"source": "model", "target": "procedure", "label": "x"},
                    "motivating_observation": "x",
                    "expected_impact": "y",
                    "input_bias_risk": "low",
                },
            ]
        }
    )
    backend = MockBackend(default=bad_payload)
    assert LLMProposer(backend=backend).generate(_obs_warrant_dominant()) == []


# ── LLMProposer prompt content (Phase V constraints C1, C3, C4) ────────────


def test_llm_proposer_prompt_includes_enrichment_fields():
    """The user prompt carries strength breakdown, sample quotes, source metadata."""
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=25,
        toulmin_failure_counts={"warrant": 23, "undercutting": 2},
        counter_strength_breakdown={
            "warrant": {"strong": 20, "moderate": 3, "weak": 0},
            "undercutting": {"strong": 2},
        },
        sample_counter_quotes={
            "warrant": ("The attacked warrant assumes a clean separation...",),
            "undercutting": ("The attacker's claim does not refute the warrant's conditions...",),
        },
        observation_source_metadata=(
            "25 observations from vault open-questions sections; "
            "structurally skewed toward warrant attacks."
        ),
    )
    backend = MockBackend(default=_llm_response_one_proposal())
    LLMProposer(backend=backend).generate(obs)
    assert len(backend.calls) == 1
    prompt = backend.calls[0].user_prompt
    # C3 — strength breakdown is in the prompt
    assert "counter_strength_breakdown" in prompt
    assert "strong" in prompt
    # C1 — sample counter quotes are in the prompt
    assert "sample_counter_quotes" in prompt
    assert "clean separation" in prompt
    # C4 — source metadata is in the prompt
    assert "observation_source_metadata" in prompt
    assert "structurally skewed" in prompt


def test_llm_proposer_system_prompt_documents_constraints():
    """System prompt must state the C1-C4 rules verbatim."""
    sp = _LLM_PROPOSER_SYSTEM_PROMPT
    assert "Toulmin components are first-class" in sp
    assert "Counter strengths weight the signal" in sp
    assert "input_bias_risk" in sp


def test_llm_proposer_propagates_target_failure_to_prompt():
    obs = _obs_warrant_dominant()
    backend = MockBackend(default=json.dumps({"proposals": []}))
    LLMProposer(backend=backend).generate(obs, target_failure="warrant")
    assert "warrant" in backend.calls[0].user_prompt
    assert "FILTER" in backend.calls[0].user_prompt


# ── MetaCycle accepts proposer kwarg ───────────────────────────────────────


def test_metacycle_default_proposer_is_heuristic():
    """Without a proposer kwarg, MetaCycle uses HeuristicProposer."""
    obs = _obs_warrant_dominant()
    cycle = MetaCycle(observation=obs)
    assert isinstance(cycle.proposer, HeuristicProposer)


def test_metacycle_accepts_llm_proposer():
    backend = MockBackend(default=_llm_response_one_proposal())
    cycle = MetaCycle(
        observation=_obs_warrant_dominant(),
        proposer=LLMProposer(backend=backend),
    )
    result = cycle.run()
    assert len(result.proposals) == 1
    assert result.proposals[0].edge.label == "warrant_codification"


def test_metacycle_proposer_swap_changes_output():
    """Same observation, two proposers → potentially different proposals."""
    obs = _obs_warrant_dominant()
    # Heuristic always fires one proposal on this obs
    h_result = MetaCycle(observation=obs).run()
    # LLM proposer returning empty array → zero proposals
    backend = MockBackend(default=json.dumps({"proposals": []}))
    llm_result = MetaCycle(
        observation=obs, proposer=LLMProposer(backend=backend)
    ).run()
    assert len(h_result.proposals) == 1
    assert len(llm_result.proposals) == 0


# ── Replay against FZ 2c1a validation fixture ──────────────────────────────


_VALIDATION_FIXTURE = Path(__file__).parent.parent / "fixtures" / "dks_meta" / "validation_v053"


def _build_observation_from_fixture() -> MetaObservation:
    """Reconstruct a MetaObservation from the Phase V validation traces."""
    from collections import Counter

    toulmin: Counter[str] = Counter()
    strength: dict[str, Counter[str]] = {}
    sample_quotes: dict[str, list[str]] = {}

    cycle_files = sorted(_VALIDATION_FIXTURE.glob("*_cycle_*.json"))
    for path in cycle_files:
        cycle = json.loads(path.read_text())
        counter = cycle.get("counter") or {}
        comp = counter.get("broken_component")
        if not comp:
            continue
        toulmin[comp] += 1
        strength.setdefault(comp, Counter())[counter.get("strength", "moderate")] += 1
        if len(sample_quotes.get(comp, [])) < 2:
            quote = (counter.get("reason") or "")[:160]
            if quote:
                sample_quotes.setdefault(comp, []).append(quote)

    return MetaObservation(
        timestamp="2026-05-11T06:20:21+00:00",
        cycles_examined=len(cycle_files),
        toulmin_failure_counts=dict(toulmin),
        counter_strength_breakdown={k: dict(v) for k, v in strength.items()},
        sample_counter_quotes={k: tuple(v) for k, v in sample_quotes.items()},
        observation_source_metadata=(
            "25 vault open-question observations; FZ 2c1a Phase V validation set."
        ),
    )


def test_validation_fixture_reproduces_phase_v_distribution():
    """The frozen fixture matches the Phase V Toulmin distribution exactly."""
    obs = _build_observation_from_fixture()
    assert obs.cycles_examined == 25
    assert obs.toulmin_failure_counts == {"warrant": 23, "undercutting": 2}
    # All counters fired at "strong" per Phase V findings
    assert obs.counter_strength_breakdown["warrant"]["strong"] == 23


def test_heuristic_replay_against_fixture_produces_one_proposal():
    """Phase V outcome: 1 proposal (warrant_codification). This is the regression test."""
    obs = _build_observation_from_fixture()
    proposals = HeuristicProposer().generate(obs)
    assert len(proposals) == 1
    assert proposals[0].edge.label == "warrant_codification"


def test_llm_replay_against_fixture_with_mock_backend():
    """LLM proposer with canned mock response also produces 1 proposal on fixture."""
    obs = _build_observation_from_fixture()
    backend = MockBackend(default=_llm_response_one_proposal())
    proposals = LLMProposer(backend=backend).generate(obs)
    assert len(proposals) == 1
    assert proposals[0].edge.label == "warrant_codification"
    # The prompt must carry the fixture's "clean separation" sample quote
    assert "clean separation" in backend.calls[0].user_prompt
