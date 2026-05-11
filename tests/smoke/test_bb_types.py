"""Smoke tests for tessellum.bb.types — the BB ontology schema.

Validates:

  - 8 BBType values (exact set)
  - BB_SCHEMA composition: 8 epistemic + 7 navigation + 1 DKS extension = 16
  - Every BB_SCHEMA_EPISTEMIC entry matches the FZ 1 narrative
  - The DKS extension `CTR → MOD` (pattern_of_failure) is in BB_SCHEMA
  - find_edge_type / edges_from / edges_to / is_valid_transition helpers
  - VALID_BUILDING_BLOCKS in format.frontmatter_spec is the same string set
"""

from __future__ import annotations


from tessellum.bb import (
    BB_SCHEMA,
    BB_SCHEMA_DKS_EXTENSIONS,
    BB_SCHEMA_EPISTEMIC,
    BB_SCHEMA_NAVIGATION,
    BBType,
    VALID_BB_TYPE_VALUES,
    edges_from,
    edges_to,
    find_edge_type,
    is_valid_transition,
)


# ── BBType ───────────────────────────────────────────────────────────────────


def test_bb_type_has_exactly_8_values():
    assert len(list(BBType)) == 8


def test_bb_type_values_match_format_spec_string_set():
    """BBType is the source of truth for VALID_BUILDING_BLOCKS."""
    from tessellum.format.frontmatter_spec import VALID_BUILDING_BLOCKS

    assert set(VALID_BUILDING_BLOCKS) == set(VALID_BB_TYPE_VALUES)
    assert set(VALID_BUILDING_BLOCKS) == {t.value for t in BBType}


def test_bb_type_str_round_trip():
    """BBType is a StrEnum — value comparison with strings works directly."""
    assert BBType.ARGUMENT == "argument"
    assert BBType("counter_argument") is BBType.COUNTER_ARGUMENT


def test_bb_type_exact_values():
    expected = {
        "empirical_observation",
        "concept",
        "model",
        "hypothesis",
        "argument",
        "counter_argument",
        "procedure",
        "navigation",
    }
    assert {t.value for t in BBType} == expected


# ── BB_SCHEMA composition ────────────────────────────────────────────────────


def test_bb_schema_composition_counts():
    """8 epistemic + 7 navigation + 1 DKS extension = 16."""
    assert len(BB_SCHEMA_EPISTEMIC) == 8
    assert len(BB_SCHEMA_NAVIGATION) == 7
    assert len(BB_SCHEMA_DKS_EXTENSIONS) == 1
    assert len(BB_SCHEMA) == 16


def test_bb_schema_concatenation():
    """BB_SCHEMA is exactly EPISTEMIC + NAVIGATION + DKS_EXTENSIONS in order."""
    assert (
        BB_SCHEMA
        == BB_SCHEMA_EPISTEMIC + BB_SCHEMA_NAVIGATION + BB_SCHEMA_DKS_EXTENSIONS
    )


def test_bb_schema_epistemic_matches_fz_1_narrative():
    """The 8 BB→BB epistemic edges match FZ 1's documented relationships."""
    labels_by_pair = {(e.source, e.target): e.label for e in BB_SCHEMA_EPISTEMIC}
    assert labels_by_pair == {
        (BBType.EMPIRICAL_OBSERVATION, BBType.CONCEPT): "naming",
        (BBType.CONCEPT, BBType.MODEL): "structuring",
        (BBType.MODEL, BBType.HYPOTHESIS): "predicting",
        (BBType.MODEL, BBType.PROCEDURE): "codifying",
        (BBType.HYPOTHESIS, BBType.ARGUMENT): "testing",
        (BBType.ARGUMENT, BBType.COUNTER_ARGUMENT): "challenging",
        (BBType.COUNTER_ARGUMENT, BBType.EMPIRICAL_OBSERVATION): "motivates_new",
        (BBType.PROCEDURE, BBType.EMPIRICAL_OBSERVATION): "execution_data",
    }


def test_bb_schema_navigation_is_indexes_to_each_other_type():
    """Navigation indexes the 7 non-NAV types; all 7 edges carry label 'indexes'."""
    nav_targets = {e.target for e in BB_SCHEMA_NAVIGATION}
    non_nav_types = set(BBType) - {BBType.NAVIGATION}
    assert nav_targets == non_nav_types
    assert all(e.label == "indexes" for e in BB_SCHEMA_NAVIGATION)
    assert all(e.source is BBType.NAVIGATION for e in BB_SCHEMA_NAVIGATION)


def test_bb_schema_dks_extension_is_ctr_to_mod():
    """The single DKS extension is `counter_argument → model` (pattern_of_failure)."""
    ext = BB_SCHEMA_DKS_EXTENSIONS[0]
    assert ext.source is BBType.COUNTER_ARGUMENT
    assert ext.target is BBType.MODEL
    assert ext.label == "pattern_of_failure"


def test_bb_schema_edges_are_frozen_dataclasses():
    """EpistemicEdgeType is frozen — edges can be hashed + used as dict keys."""
    s = {BB_SCHEMA[0], BB_SCHEMA[0]}
    assert len(s) == 1


# ── Lookups ──────────────────────────────────────────────────────────────────


def test_find_edge_type_finds_matching_pair():
    edge = find_edge_type(BBType.ARGUMENT, BBType.COUNTER_ARGUMENT)
    assert edge is not None
    assert edge.label == "challenging"


def test_find_edge_type_returns_none_for_unknown_pair():
    """No schema edge from procedure to argument directly."""
    assert find_edge_type(BBType.PROCEDURE, BBType.ARGUMENT) is None


def test_find_edge_type_respects_label_filter():
    edge = find_edge_type(BBType.MODEL, BBType.PROCEDURE, label="codifying")
    assert edge is not None
    edge_wrong = find_edge_type(BBType.MODEL, BBType.PROCEDURE, label="wrong_label")
    assert edge_wrong is None


def test_edges_from_returns_all_outgoing():
    """MODEL has 2 outgoing edges: predicting → HYP and codifying → PRO."""
    outgoing = edges_from(BBType.MODEL)
    assert len(outgoing) == 2
    targets = {e.target for e in outgoing}
    assert targets == {BBType.HYPOTHESIS, BBType.PROCEDURE}


def test_edges_to_returns_all_incoming():
    """EMPIRICAL_OBSERVATION has 3 incoming edges: motivates_new + execution_data + indexes."""
    incoming = edges_to(BBType.EMPIRICAL_OBSERVATION)
    sources = {e.source for e in incoming}
    assert sources == {
        BBType.COUNTER_ARGUMENT,  # motivates_new
        BBType.PROCEDURE,          # execution_data
        BBType.NAVIGATION,         # indexes
    }


def test_is_valid_transition_true_for_declared_edges():
    assert is_valid_transition(BBType.HYPOTHESIS, BBType.ARGUMENT) is True
    assert is_valid_transition(BBType.COUNTER_ARGUMENT, BBType.MODEL) is True  # DKS ext


def test_is_valid_transition_false_for_unknown_pairs():
    assert is_valid_transition(BBType.PROCEDURE, BBType.HYPOTHESIS) is False
    assert is_valid_transition(BBType.ARGUMENT, BBType.NAVIGATION) is False
