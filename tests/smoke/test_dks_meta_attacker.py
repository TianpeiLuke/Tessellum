"""Smoke tests for tessellum.dks.meta attacker strategies (Phase B.3).

Covers:

- ``MetaCounterArgument`` dataclass shape.
- ``NoOpAttacker`` returns empty list (default behaviour, preserves v0.0.52).
- ``LLMAttacker`` parses well-formed LLM responses.
- ``LLMAttacker`` returns ``[]`` on malformed JSON / unexpected shapes.
- ``LLMAttacker`` filters out-of-range proposal indices + unknown attack kinds.
- ``LLMAttacker`` dedups same-(index, kind) attacks.
- Survive thresholds (strict / majority / permissive) decide the right outcome.
- ``MetaCycle`` integrates attacker + threshold end-to-end.
"""

from __future__ import annotations

import json

import pytest

from tessellum.bb.types import BBType, EpistemicEdgeType
from tessellum.composer.llm import MockBackend
from tessellum.dks.meta import (
    Attacker,
    DEFAULT_MIN_CYCLES,
    HeuristicProposer,
    LLMAttacker,
    MetaCounterArgument,
    MetaCycle,
    MetaObservation,
    NoOpAttacker,
    SchemaEditProposal,
)
from tessellum.dks.meta.runtime import _LLM_ATTACKER_SYSTEM_PROMPT, _proposal_survives


# ── MetaCounterArgument dataclass ──────────────────────────────────────────


def test_meta_counter_argument_construction():
    ca = MetaCounterArgument(
        attacked_proposal_index=0,
        attack_kind="input_bias",
        reason="observation source is structurally skewed",
        strength="strong",
    )
    assert ca.attacked_proposal_index == 0
    assert ca.attack_kind == "input_bias"
    assert ca.strength == "strong"


def test_meta_counter_argument_strength_default():
    ca = MetaCounterArgument(
        attacked_proposal_index=0, attack_kind="weak_signal", reason="x"
    )
    assert ca.strength == "moderate"


# ── NoOpAttacker (default behaviour, v0.0.52 preservation) ─────────────────


def test_noop_attacker_returns_empty():
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=25,
        toulmin_failure_counts={"warrant": 23, "undercutting": 2},
    )
    p = SchemaEditProposal(
        kind="add",
        edge=EpistemicEdgeType(BBType.MODEL, BBType.PROCEDURE, "test"),
    )
    assert NoOpAttacker().attack([p], obs) == []
    assert NoOpAttacker().attack([], obs) == []


# ── LLMAttacker parsing ────────────────────────────────────────────────────


def _proposal_list() -> list[SchemaEditProposal]:
    return [
        SchemaEditProposal(
            kind="add",
            edge=EpistemicEdgeType(
                BBType.MODEL, BBType.PROCEDURE, "warrant_codification"
            ),
            motivating_observation="warrant dominates",
        )
    ]


def _obs() -> MetaObservation:
    return MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=25,
        toulmin_failure_counts={"warrant": 23, "undercutting": 2},
    )


def test_llm_attacker_parses_single_attack():
    response = json.dumps(
        {
            "attacks": [
                {
                    "attacked_proposal_index": 0,
                    "attack_kind": "input_bias",
                    "reason": "the 92% rate is induced by warrant-shaped observations",
                    "strength": "strong",
                }
            ]
        }
    )
    backend = MockBackend(default=response)
    attacks = LLMAttacker(backend=backend).attack(_proposal_list(), _obs())
    assert len(attacks) == 1
    assert attacks[0].attack_kind == "input_bias"
    assert attacks[0].strength == "strong"


def test_llm_attacker_empty_proposals_skips_llm_call():
    backend = MockBackend(default="should-not-be-called")
    attacks = LLMAttacker(backend=backend).attack([], _obs())
    assert attacks == []
    assert backend.calls == []


def test_llm_attacker_malformed_json_returns_empty():
    backend = MockBackend(default="not-json")
    assert LLMAttacker(backend=backend).attack(_proposal_list(), _obs()) == []


def test_llm_attacker_filters_out_of_range_proposal_index():
    response = json.dumps(
        {
            "attacks": [
                {
                    "attacked_proposal_index": 5,  # out of range (1 proposal)
                    "attack_kind": "input_bias",
                    "reason": "x",
                    "strength": "moderate",
                },
                {
                    "attacked_proposal_index": 0,
                    "attack_kind": "weak_signal",
                    "reason": "y",
                    "strength": "weak",
                },
            ]
        }
    )
    backend = MockBackend(default=response)
    attacks = LLMAttacker(backend=backend).attack(_proposal_list(), _obs())
    assert len(attacks) == 1
    assert attacks[0].attacked_proposal_index == 0


def test_llm_attacker_filters_unknown_attack_kind():
    response = json.dumps(
        {
            "attacks": [
                {
                    "attacked_proposal_index": 0,
                    "attack_kind": "fabricated_kind",
                    "reason": "x",
                    "strength": "moderate",
                },
            ]
        }
    )
    backend = MockBackend(default=response)
    assert LLMAttacker(backend=backend).attack(_proposal_list(), _obs()) == []


def test_llm_attacker_dedups_same_index_and_kind():
    response = json.dumps(
        {
            "attacks": [
                {
                    "attacked_proposal_index": 0,
                    "attack_kind": "input_bias",
                    "reason": "first",
                    "strength": "strong",
                },
                {
                    "attacked_proposal_index": 0,
                    "attack_kind": "input_bias",  # same (index, kind) → drop
                    "reason": "second",
                    "strength": "weak",
                },
                {
                    "attacked_proposal_index": 0,
                    "attack_kind": "overgeneralisation",  # different kind → keep
                    "reason": "third",
                    "strength": "moderate",
                },
            ]
        }
    )
    backend = MockBackend(default=response)
    attacks = LLMAttacker(backend=backend).attack(_proposal_list(), _obs())
    assert len(attacks) == 2
    assert {a.attack_kind for a in attacks} == {"input_bias", "overgeneralisation"}


def test_llm_attacker_system_prompt_lists_valid_kinds():
    sp = _LLM_ATTACKER_SYSTEM_PROMPT
    for kind in (
        "insufficient_evidence",
        "input_bias",
        "overgeneralisation",
        "collides_with_existing",
        "weak_signal",
    ):
        assert kind in sp


def test_llm_attacker_prompt_carries_proposals_and_observation():
    backend = MockBackend(default='{"attacks": []}')
    LLMAttacker(backend=backend).attack(_proposal_list(), _obs())
    assert len(backend.calls) == 1
    prompt = backend.calls[0].user_prompt
    assert "warrant_codification" in prompt
    assert "cycles_examined: 25" in prompt
    assert "toulmin_failure_counts" in prompt


# ── Survive threshold (aggregation) ────────────────────────────────────────


def _attack(idx: int, kind: str, strength: str) -> MetaCounterArgument:
    return MetaCounterArgument(
        attacked_proposal_index=idx,
        attack_kind=kind,  # type: ignore[arg-type]
        reason="test",
        strength=strength,  # type: ignore[arg-type]
    )


def test_threshold_strict_requires_zero_attacks():
    assert _proposal_survives([], "strict") is True
    assert _proposal_survives([_attack(0, "weak_signal", "weak")], "strict") is False


def test_threshold_permissive_tolerates_non_strong():
    assert _proposal_survives([_attack(0, "input_bias", "weak")], "permissive") is True
    assert _proposal_survives([_attack(0, "input_bias", "moderate")], "permissive") is True
    assert _proposal_survives([_attack(0, "input_bias", "strong")], "permissive") is False


def test_threshold_majority_default_rule():
    # No attacks → survives
    assert _proposal_survives([], "majority") is True
    # 1 strong → survives (<=1 strong allowed)
    assert _proposal_survives([_attack(0, "x", "strong")], "majority") is True
    # 2 strong → fails
    assert (
        _proposal_survives(
            [_attack(0, "a", "strong"), _attack(0, "b", "strong")],
            "majority",
        )
        is False
    )
    # 3 moderate → fails (limit is <=2)
    assert (
        _proposal_survives(
            [
                _attack(0, "a", "moderate"),
                _attack(0, "b", "moderate"),
                _attack(0, "c", "moderate"),
            ],
            "majority",
        )
        is False
    )
    # 1 strong + 2 moderate → survives
    assert (
        _proposal_survives(
            [
                _attack(0, "a", "strong"),
                _attack(0, "b", "moderate"),
                _attack(0, "c", "moderate"),
            ],
            "majority",
        )
        is True
    )


# ── MetaCycle integration: attacker + threshold end-to-end ─────────────────


def test_metacycle_default_attacker_is_noop():
    cycle = MetaCycle(observation=_obs())
    assert isinstance(cycle.attacker, NoOpAttacker)
    assert cycle.survive_threshold == "majority"


def test_metacycle_noop_attacker_preserves_v052_behaviour():
    """With NoOpAttacker (default), survival = all filtered proposals."""
    result = MetaCycle(observation=_obs()).run()
    assert len(result.proposals) == 1
    assert len(result.surviving) == 1
    assert result.attacks == ()


def test_metacycle_llm_attacker_kills_proposal_at_strict_threshold():
    """With strict threshold + one attack → 0 survivors."""
    attacker_response = json.dumps(
        {
            "attacks": [
                {
                    "attacked_proposal_index": 0,
                    "attack_kind": "input_bias",
                    "reason": "warrant rate is input-induced",
                    "strength": "weak",
                }
            ]
        }
    )
    cycle = MetaCycle(
        observation=_obs(),
        attacker=LLMAttacker(backend=MockBackend(default=attacker_response)),
        survive_threshold="strict",
    )
    result = cycle.run()
    assert len(result.proposals) == 1
    assert len(result.attacks) == 1
    assert len(result.surviving) == 0


def test_metacycle_llm_attacker_keeps_proposal_at_majority_threshold():
    """Same single weak attack → survives under majority (default)."""
    attacker_response = json.dumps(
        {
            "attacks": [
                {
                    "attacked_proposal_index": 0,
                    "attack_kind": "input_bias",
                    "reason": "warrant rate is input-induced",
                    "strength": "weak",
                }
            ]
        }
    )
    cycle = MetaCycle(
        observation=_obs(),
        attacker=LLMAttacker(backend=MockBackend(default=attacker_response)),
        survive_threshold="majority",
    )
    result = cycle.run()
    assert len(result.surviving) == 1
    assert len(result.attacks) == 1


def test_metacycle_dialectical_path_propagates_to_events():
    """When attacker kills proposal, no events should land even with --apply."""
    attacker_response = json.dumps(
        {
            "attacks": [
                {
                    "attacked_proposal_index": 0,
                    "attack_kind": "input_bias",
                    "reason": "test",
                    "strength": "strong",
                },
                {
                    "attacked_proposal_index": 0,
                    "attack_kind": "weak_signal",
                    "reason": "test",
                    "strength": "strong",
                },
            ]
        }
    )
    cycle = MetaCycle(
        observation=_obs(),
        attacker=LLMAttacker(backend=MockBackend(default=attacker_response)),
        survive_threshold="majority",  # 2 strong > 1 strong limit → killed
        dry_run=False,
    )
    result = cycle.run()
    assert len(result.surviving) == 0
    assert len(result.events_landed) == 0
