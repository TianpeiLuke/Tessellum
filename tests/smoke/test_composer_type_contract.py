"""P4 (FZ 20k9d1b1a1a) — the note-type contract resolver.

Pure, DB-free tests for ``composer/type_contract.py``: reverse-resolve a leaf's
``target_path`` to its ``capture.REGISTRY`` flavor (longest-prefix on
``(destination, filename_prefix)``), and derive that flavor's section contract
(``BB_SPECS`` for primary flavors; the flavor's own template H2s for the four
``SECTION_DIVERGENT_FLAVORS``). Keyed on FLAVOR, never on ``building_block`` or
the coarser ``second_category``.
"""

from __future__ import annotations

import pytest

from tessellum import capture
from tessellum.composer import type_contract as tc
from tessellum.format.building_blocks import BB_SPECS, BuildingBlock


def test_reverse_index_longest_prefix() -> None:
    # Under resources/analysis_thoughts the specific prefixes must beat bare
    # thought_ — otherwise thought_observation_ would mis-resolve to argument.
    assert (
        tc.resolve_flavor("resources/analysis_thoughts/thought_observation_x.md")
        == "empirical_observation"
    )
    assert (
        tc.resolve_flavor("resources/analysis_thoughts/thought_hypothesis_x.md")
        == "hypothesis"
    )
    assert (
        tc.resolve_flavor("resources/analysis_thoughts/thought_counter_x.md")
        == "counter_argument"
    )
    assert tc.resolve_flavor("resources/analysis_thoughts/coe_x.md") == "coe"


def test_bare_thought_prefix_is_analysis_family() -> None:
    # The benign thought_ collision (argument/thought share destination, prefix,
    # bb_type, second_category). Assert the CONTRACT, never which flavor won.
    flavor = tc.resolve_flavor("resources/analysis_thoughts/thought_x.md")
    assert flavor is not None
    contract = tc.build_type_contract(flavor)
    assert contract.second_category == "analysis"
    assert contract.required_sections == ("Claim", "Reason", "Evidence", "References")


def test_entry_point_prefixes_and_navigation_default() -> None:
    assert tc.resolve_flavor("0_entry_points/entry_x.md") == "entry_point"
    assert (
        tc.resolve_flavor("0_entry_points/acronym_glossary_x.md")
        == "acronym_glossary"
    )
    # empty-prefix navigation flavor is the directory default (sorts LAST)
    assert tc.resolve_flavor("0_entry_points/random_index.md") == "navigation"


def test_override_dir_and_bare_name_unresolvable() -> None:
    # capture() destination= override dirs (areas/tools, resources/teams) are NOT
    # in REGISTRY → resolve to None (fail-soft). A bare filename likewise.
    assert tc.resolve_flavor("areas/tools/tool_x.md") is None
    assert tc.resolve_flavor("resources/teams/team_x.md") is None
    assert tc.resolve_flavor("README.md") is None
    assert tc.resolve_flavor("") is None


@pytest.mark.parametrize("flavor", sorted(capture.REGISTRY))
def test_each_flavor_roundtrips(flavor: str) -> None:
    # Every registered flavor resolves from its canonical path to a flavor with
    # the SAME (bb_type, second_category) as its spec (the benign thought_ tie is
    # allowed — argument and thought share both).
    spec = capture.REGISTRY[flavor]
    path = f"{spec.destination}/{spec.filename_prefix}x.md"
    resolved = tc.resolve_flavor(path)
    assert resolved is not None, f"{flavor} path {path} resolved to None"
    contract = tc.build_type_contract(resolved)
    assert contract.second_category == spec.second_category
    assert contract.building_block == spec.bb_type


def test_distinct_required_sections_per_flavor() -> None:
    # Anti-second_category-collapse: argument / counter_argument / hypothesis all
    # share second_category=analysis but have DISTINCT required sections — proof
    # the contract is keyed on the finer flavor, not second_category.
    arg = tc.build_type_contract("argument")
    counter = tc.build_type_contract("counter_argument")
    hyp = tc.build_type_contract("hypothesis")
    assert arg.required_sections == ("Claim", "Reason", "Evidence", "References")
    assert counter.required_sections == (
        "Counter-claim", "Reason", "Strength", "References",
    )
    assert hyp.required_sections == (
        "Hypothesis", "Reasoning", "Falsifiability", "References",
    )
    assert arg.second_category == counter.second_category == hyp.second_category == "analysis"
    assert arg.required_sections != counter.required_sections != hyp.required_sections


def test_primary_flavor_uses_bb_specs() -> None:
    concept = tc.build_type_contract("concept")
    assert concept.section_source == "BB_SPECS"
    assert concept.required_sections == BB_SPECS[BuildingBlock.CONCEPT].required_sections


@pytest.mark.parametrize("flavor", sorted(capture.SECTION_DIVERGENT_FLAVORS))
def test_section_divergent_uses_template_h2(flavor: str) -> None:
    # The 4 divergent flavors get their OWN template H2s, NOT the wrong
    # BB_SPECS[bb] section triple.
    contract = tc.build_type_contract(flavor)
    assert contract.section_source == "template"
    spec = capture.REGISTRY[flavor]
    bb_sections = BB_SPECS[BuildingBlock(spec.bb_type)].required_sections
    assert contract.required_sections != bb_sections
    assert contract.required_sections  # non-empty (templates are present)


def test_divergent_template_unreadable_failsoft(monkeypatch) -> None:
    # If a divergent flavor's template can't be read, _template_h2_sections
    # swallows the error and returns () → section_source="divergent-unreadable".
    # Break the underlying templates_dir() read (the caught failure point).
    tc._template_h2_sections.cache_clear()
    import tessellum.data as data_mod

    def _boom():
        raise OSError("templates dir gone")

    monkeypatch.setattr(data_mod, "templates_dir", _boom)
    contract = tc.build_type_contract("skill")
    assert contract.required_sections == ()
    assert contract.section_source == "divergent-unreadable"
    tc._template_h2_sections.cache_clear()


def test_resolve_note_contract_none_for_unresolvable() -> None:
    assert tc.resolve_note_contract("areas/tools/tool_x.md") is None
    assert tc.resolve_note_contract("README.md") is None


def test_render_contract_lists_sections() -> None:
    contract = tc.build_type_contract("concept")
    assert "`concept`" in contract.contract_md
    assert "second_category: terminology" in contract.contract_md
    for sec in ("Definition", "Examples", "References"):
        assert f"`## {sec}`" in contract.contract_md


def test_render_empty_sections_falls_back_to_template_shape() -> None:
    md = tc.render_type_contract("code_repo", "code_repos", ())
    assert "per-flavor template shape" in md
    assert "`code_repo`" in md
