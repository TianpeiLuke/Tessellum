"""Query-time DKS P7 — seeded traversal with a hard hop budget (step 2).

Gate deliverable, stated as the plan states it: *a two-hop question whose bridge
note is not in the top-k by similarity is nonetheless reached via links, with hop
count and stopping reason recorded.*

The fixture is built so that clause is **proved, not assumed**. The bridge note
(``thought_planner_and_index_share_a_budget``) is about the *joint* of two
things, so a ranker keyed on either one does not surface it — and here the
similarity backend is deterministic and demonstrably omits it, checked directly
and again by running the same reach with no links at all. It is reachable only by
walking two authored links.

The rest of the file covers the other properties the phase owes: the budget is a
hard parameter (refused, not clamped), every stop is recorded with a reason and
an ``understood`` verdict, the re-retrieval trigger is itself bounded, seeding
comes from the resolved entity rather than raw keywords, and the traversal is
deterministic and model-free.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, Mapping

import pytest

from tessellum.dks import reach as reach_module
from tessellum.dks.entity_registry import EntityCandidateRef
from tessellum.dks.reach import (
    AMBIGUOUS_SEED_WEIGHT,
    HARD_MAX_HOPS,
    BudgetError,
    HopBudget,
    MappingLinkBackend,
    MappingSimilarityBackend,
    MissingHop,
    ReachedNote,
    SeededReach,
)
from tessellum.dks.resolve_entity import Resolution
from tessellum.dks.retrieval_client import (
    MAX_EXPANSION_HOPS,
    LinkNeighbour,
    RetrievalClient,
)

TOOL = "areas/tools/tool_query_planner.md"
LINK_GRAPH = "resources/term_dictionary/term_link_graph.md"
BRIDGE = "resources/analysis_thoughts/thought_planner_and_index_share_a_budget.md"
FAR = "resources/analysis_thoughts/thought_budget_accounting.md"
EXPANSION = "resources/term_dictionary/term_query_expansion.md"
RANKER = "resources/term_dictionary/term_ranker.md"

#: The authored link graph. ``TOOL -> LINK_GRAPH -> BRIDGE -> FAR`` is the chain
#: the reach has to walk; ``FAR`` sits one hop past the admitted ceiling.
ADJACENCY = {
    TOOL: (LINK_GRAPH, EXPANSION),
    LINK_GRAPH: (BRIDGE,),
    BRIDGE: (FAR,),
}

#: What similarity returns for the resolved entity's canonical name. The bridge
#: note is ABSENT — that absence is the premise of the acceptance clause.
RANKING = {"tool_query_planner": (TOOL, EXPANSION, RANKER)}


def _resolved(entity_id: str = TOOL, name: str = "tool_query_planner") -> Resolution:
    return Resolution(
        mention="query planner",
        entity_id=entity_id,
        canonical_name=name,
        entity_type="tool",
        method="exact_alias",
        score=1.0,
    )


def _unresolved() -> Resolution:
    return Resolution(
        mention="query planner",
        entity_id=None,
        canonical_name=None,
        entity_type=None,
        method="unresolved",
        score=0.0,
    )


def _ambiguous() -> Resolution:
    return Resolution(
        mention="planner",
        entity_id=None,
        canonical_name=None,
        entity_type=None,
        method="ambiguous",
        score=0.0,
        candidates=(
            EntityCandidateRef(TOOL, "tool"),
            EntityCandidateRef(EXPANSION, "concept"),
        ),
    )


def _reach(
    *,
    adjacency: Mapping[str, tuple[str, ...]] = ADJACENCY,
    similarity: bool = True,
    budget: HopBudget | None = None,
    on_ambiguous: Literal["abstain", "widen"] = "abstain",
) -> SeededReach:
    return SeededReach(
        expander=MappingLinkBackend(adjacency),
        similarity=MappingSimilarityBackend(RANKING) if similarity else None,
        budget=budget,
        on_ambiguous=on_ambiguous,
    )


# ── acceptance: the bridge note similarity cannot rank ───────────────────────


def test_similarity_demonstrably_excludes_the_bridge_note() -> None:
    """The premise of the clause, checked before the clause itself."""
    result = _reach().reach(_resolved())
    assert BRIDGE not in result.similarity_top_k
    assert result.similarity_top_k == (TOOL, EXPANSION, RANKER)


def test_without_links_the_bridge_note_is_unreachable() -> None:
    """Seeds + similarity alone never get there — so a hit below is the links'."""
    result = _reach(adjacency={}).reach(_resolved())
    assert BRIDGE not in result.note_ids
    assert result.note_ids == {TOOL, EXPANSION, RANKER}


def test_the_bridge_note_is_reached_over_two_authored_links() -> None:
    result = _reach().reach(_resolved())
    bridge = result.reached(BRIDGE)
    assert bridge is not None
    assert bridge.via == "link"
    assert bridge.hops == 2
    assert bridge.path == (TOOL, LINK_GRAPH, BRIDGE)


def test_the_bridge_note_is_reported_as_a_bridge() -> None:
    """``bridge_notes`` is the property as a field: reached by link, unranked."""
    result = _reach().reach(_resolved())
    assert BRIDGE in {n.note_id for n in result.bridge_notes}


def test_hop_count_and_stopping_reason_are_recorded() -> None:
    result = _reach().reach(_resolved())
    assert result.hop_count == 2
    assert result.hops_expanded == 2
    assert result.stopping_reason == "budget_exhausted"
    # A 2-hop budget on a 3-deep chain is a TRUNCATION, and says so: FAR was
    # never looked at, so the reach must not claim it exhausted the graph.
    assert result.understood is False
    assert FAR not in result.note_ids


# ── the budget is a hard parameter, not advice ───────────────────────────────


def test_a_budget_wider_than_the_admitted_reach_is_refused_not_clamped() -> None:
    with pytest.raises(BudgetError, match="outside the admitted reach"):
        HopBudget(max_hops=HARD_MAX_HOPS + 1)
    with pytest.raises(BudgetError):
        HopBudget(max_hops=0)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_notes": 0},
        {"lambda_cost": -0.1},
        {"seed_k": -1},
        {"max_reretrievals": -1},
    ],
)
def test_every_ceiling_is_validated_at_construction(kwargs: dict[str, Any]) -> None:
    with pytest.raises(BudgetError):
        HopBudget(**kwargs)


def test_a_one_hop_budget_stops_one_hop_short_of_the_bridge() -> None:
    result = _reach(budget=HopBudget(max_hops=1)).reach(_resolved())
    assert LINK_GRAPH in result.note_ids
    assert BRIDGE not in result.note_ids
    assert result.hop_count == 1
    assert result.stopping_reason == "budget_exhausted"


def test_the_note_cap_bounds_fan_out_and_records_the_truncation() -> None:
    result = _reach(budget=HopBudget(max_hops=2, max_notes=2)).reach(_resolved())
    assert len(result.notes) == 2
    assert result.stopping_reason == "budget_exhausted"
    assert result.understood is False


# ── the stopping rule: three reasons, told apart ─────────────────────────────


def test_an_exhausted_graph_inside_the_budget_reports_a_fixpoint() -> None:
    """Nothing at the ceiling and nothing left to expand — a real discharge."""
    result = _reach(adjacency={TOOL: (LINK_GRAPH,)}, similarity=False).reach(_resolved())
    assert result.note_ids == {TOOL, LINK_GRAPH}
    assert result.stopping_reason == "fixpoint"
    assert result.understood is True


def test_lambda_retires_the_frontier_without_a_single_expansion() -> None:
    """The deterministic λ comparison, doing the stopping — no model asked."""
    result = _reach(
        similarity=False, budget=HopBudget(max_hops=2, lambda_cost=1.5)
    ).reach(_resolved())
    assert result.stopping_reason == "retired_below_lambda"
    assert result.understood is True
    assert result.hops_expanded == 0
    assert result.note_ids == {TOOL}


def test_lambda_prunes_the_second_ring_by_expected_gain() -> None:
    """λ between the seed's gain (1.0) and hop 1's (0.5) buys exactly one ring."""
    result = _reach(
        similarity=False, budget=HopBudget(max_hops=2, lambda_cost=0.75)
    ).reach(_resolved())
    assert result.note_ids == {TOOL, LINK_GRAPH, EXPANSION}
    assert result.hops_expanded == 1
    assert result.stopping_reason == "retired_below_lambda"


# ── seeding comes from the resolved entity, never raw keywords ───────────────


def test_an_unresolved_anchor_abstains_instead_of_seeding_on_keywords() -> None:
    result = _reach().reach(_unresolved())
    assert result.stopping_reason == "no_seed"
    assert result.understood is False
    assert result.notes == ()
    assert result.seeds == ()


def test_an_ambiguous_anchor_abstains_by_default() -> None:
    assert _reach().reach(_ambiguous()).stopping_reason == "no_seed"


def test_widening_an_ambiguous_anchor_is_opt_in_and_weighted_as_half() -> None:
    result = _reach(similarity=False, on_ambiguous="widen").reach(_ambiguous())
    assert result.stopping_reason != "no_seed"
    assert set(result.seeds) == {TOOL, EXPANSION}
    for seed in result.seeds:
        record = result.reached(seed)
        assert record is not None and record.weight == AMBIGUOUS_SEED_WEIGHT


def test_similarity_is_queried_on_the_canonical_name_not_the_mention() -> None:
    """The mention is ``"query planner"``; only the canonical name is a key here,
    so a non-empty top-k proves the resolved entity did the seeding."""
    result = _reach().reach(_resolved())
    assert result.similarity_top_k
    assert result.reached(RANKER) is not None
    assert result.reached(RANKER).via == "similarity"  # type: ignore[union-attr]


def test_the_anchor_outranks_its_own_similarity_hit() -> None:
    """The entity is rank 0 in the ranking too; the anchor record must win, so
    the reach's strongest seed is the resolved entity and not a ranker's guess."""
    anchor = _reach().reach(_resolved()).reached(TOOL)
    assert anchor is not None
    assert anchor.via == "entity" and anchor.weight == 1.0


def test_similarity_seeds_are_skipped_when_no_backend_is_supplied() -> None:
    result = _reach(similarity=False).reach(_resolved())
    assert result.similarity_top_k == ()
    assert RANKER not in result.note_ids


# ── the re-retrieval trigger, itself bounded ─────────────────────────────────


def test_a_missing_hop_triggers_a_second_bounded_reach() -> None:
    reacher = _reach(similarity=False, budget=HopBudget(max_hops=1))
    first = reacher.reach(_resolved())
    assert BRIDGE not in first.note_ids

    again = reacher.reach_again(
        first, [MissingHop(from_note_id=LINK_GRAPH, question="what connects these?")]
    )
    assert BRIDGE in again.note_ids
    assert again.reretrievals == 1
    assert again.missing_hops[0].from_note_id == LINK_GRAPH
    # the earlier notes keep their original provenance
    assert again.reached(TOOL).hops == 0  # type: ignore[union-attr]


def test_the_re_retrieval_trigger_refuses_past_its_own_ceiling() -> None:
    reacher = _reach(similarity=False, budget=HopBudget(max_hops=1))
    first = reacher.reach(_resolved())
    once = reacher.reach_again(first, [MissingHop(LINK_GRAPH, "q1")])
    twice = reacher.reach_again(once, [MissingHop(BRIDGE, "q2")])
    assert twice.reretrievals == 1  # not incremented — the call was refused
    assert twice.note_ids == once.note_ids
    assert twice.stopping_reason == "budget_exhausted"


def test_reporting_no_missing_hop_is_a_no_op() -> None:
    reacher = _reach(similarity=False)
    first = reacher.reach(_resolved())
    assert reacher.reach_again(first, []) == first


# ── determinism and purity ──────────────────────────────────────────────────


def test_two_identical_reaches_are_byte_identical() -> None:
    a = _reach().reach(_resolved())
    b = _reach().reach(_resolved())
    assert a == b
    assert [n.note_id for n in a.notes] == [n.note_id for n in b.notes]


def test_notes_are_ordered_nearest_and_strongest_first() -> None:
    notes = _reach().reach(_resolved()).notes
    assert [n.hops for n in notes] == sorted(n.hops for n in notes)
    assert notes[0].note_id == TOOL  # the anchor, weight 1.0


def test_records_are_frozen() -> None:
    note = ReachedNote(note_id=TOOL, hops=0, via="entity", path=(TOOL,), weight=1.0)
    with pytest.raises(Exception):
        note.hops = 3  # type: ignore[misc]


def test_module_is_pure_no_runtime_import_no_model_call() -> None:
    src = Path(reach_module.__file__).read_text(encoding="utf-8")
    assert "tessellum.runtime" not in src
    for banned in (
        "LLMBackend",
        "LLMRequest",
        "sqlite3",
        "Path(",
        "read_text",
        "write_text",
        "tessellum.indexer",
    ):
        assert banned not in src, f"{banned} breaks the purity of dks/reach"


def test_the_str_render_names_the_stop() -> None:
    text = str(_reach().reach(_resolved()))
    assert "budget_exhausted" in text and "TRUNCATED" in text


# ── the port: bounded, and still read-only ──────────────────────────────────


_NOTE = """\
---
tags:
  - resource
  - terminology
keywords:
  - {kw}
topics:
  - X
language: markdown
date of note: 2026-09-12
status: active
building_block: concept
---

# {title}

Body of {title}.{link}
"""


@pytest.fixture
def linked_db(tmp_path):
    """Three notes in a chain: alpha -> beta -> gamma. ``gamma`` shares no
    keyword with ``alpha``, so it is the indexed analogue of a bridge note."""
    from tessellum.indexer import build

    vault = tmp_path / "v"
    folder = vault / "resources/term_dictionary"
    folder.mkdir(parents=True)
    (folder / "term_alpha.md").write_text(
        _NOTE.format(
            kw="alpha", title="Alpha", link=" See [Beta](term_beta.md)."
        )
    )
    (folder / "term_beta.md").write_text(
        _NOTE.format(
            kw="beta", title="Beta", link=" See [Gamma](term_gamma.md)."
        )
    )
    (folder / "term_gamma.md").write_text(
        _NOTE.format(kw="gamma", title="Gamma", link="")
    )
    db = tmp_path / "tess.db"
    build(vault, db, with_dense=False)
    return db


def test_expand_links_walks_the_authored_note_links(linked_db) -> None:
    client = RetrievalClient(linked_db)
    seed = "resources/term_dictionary/term_alpha.md"
    one = client.expand_links(seed, hops=1)
    assert [n.note_id for n in one] == ["resources/term_dictionary/term_beta.md"]
    assert isinstance(one[0], LinkNeighbour) and one[0].hops == 1

    two = client.expand_links(seed, hops=2)
    gamma = next(n for n in two if n.note_name == "term_gamma")
    assert gamma.hops == 2
    assert gamma.path[0] == seed


def test_expand_links_refuses_an_unbounded_request(linked_db) -> None:
    client = RetrievalClient(linked_db)
    for hops in (0, MAX_EXPANSION_HOPS + 1):
        with pytest.raises(ValueError, match="hard bound"):
            client.expand_links("resources/term_dictionary/term_alpha.md", hops=hops)


def test_expand_links_on_an_unknown_seed_is_a_miss_not_an_error(linked_db) -> None:
    assert RetrievalClient(linked_db).expand_links("nope.md", hops=1) == []


def test_the_port_gains_no_mutating_surface(linked_db) -> None:
    """The protected property from the plan's bucket ①: extending the port with
    a read is fine; gaining a write is not."""
    public = {n for n in dir(RetrievalClient(linked_db)) if not n.startswith("_")}
    assert public == {"db_path", "search", "expand_links"}
    assert not public & {"index", "update", "delete", "insert", "write", "append"}


def test_the_real_client_satisfies_the_expansion_port(linked_db) -> None:
    """Structural typing, so ``reach`` never imports ``indexer`` to walk links."""
    reacher = SeededReach(expander=RetrievalClient(linked_db))
    result = reacher.reach(
        _resolved(entity_id="resources/term_dictionary/term_alpha.md", name="term_alpha")
    )
    assert "resources/term_dictionary/term_gamma.md" in result.note_ids
    assert result.hop_count == 2
    assert result.stopping_reason == "budget_exhausted"
