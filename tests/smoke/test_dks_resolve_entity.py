"""Query-time DKS P1 — the tiered mention→entity resolver (step 1).

Gate deliverables:
 - a mention resolves to a CANONICAL TYPED entity, with authored exclusions
   applied at every tier (not only the exact one);
 - an AMBIGUOUS mention returns candidates and resolves nothing — the anchor
   everything downstream depends on is unique or it is a candidate set;
 - the tiers run cheapest-first (exact alias → full text → dense), are
   type-preferring, and read through injected search backends so the test is
   deterministic and the index is never touched;
 - a keyword-dump alias cannot resolve, even when it is the only surface form.
"""

from __future__ import annotations

import pytest

from tessellum.dks.entity_registry import (
    ANY_OBJECT_TYPE,
    EXCLUSION_ALIAS_KIND,
    Entity,
    EntityAlias,
    EntityRegistry,
    NoteFacts,
    RelationFieldSpec,
    audit_authored_seed,
    seed_authored_relations,
)
from tessellum.dks.resolve_entity import (
    DISAMBIGUATED_SCORE,
    EXACT_SCORE,
    FULL_TEXT_RELAXED_SCORE,
    FULL_TEXT_TYPED_SCORE,
    EntityResolver,
    EntitySearchHit,
    MappingSearchBackend,
    RetrievalSearchBackend,
    TypedObjectResolver,
)

TOOL = "areas/tools/tool_query_planner.md"
MODEL = "areas/models/model_planner.md"
TEAM = "areas/teams/team_platform.md"
TERM = "resources/term_dictionary/term_vector_search.md"


def _entity(entity_id: str, name: str, entity_type: str) -> Entity:
    return Entity(
        entity_id=entity_id,
        canonical_name=name,
        entity_type=entity_type,
        note_id=entity_id,
        file_path=entity_id,
    )


def _registry(*, exclude_model_planner: bool = False) -> EntityRegistry:
    """Four entities; ``planner`` is a deliberate collision across two types."""
    aliases = [
        EntityAlias(TOOL, "tool_query_planner", "canonical", "note_name"),
        EntityAlias(TOOL, "planner", "variant", "glossary"),
        EntityAlias(MODEL, "model_planner", "canonical", "note_name"),
        EntityAlias(MODEL, "planner", "variant", "glossary"),
        EntityAlias(TEAM, "team_platform", "canonical", "note_name"),
        EntityAlias(TEAM, "Platform", "variant", "glossary"),
        EntityAlias(TERM, "term_vector_search", "canonical", "note_name"),
        EntityAlias(TERM, "VI", "acronym", "glossary"),
        # a keyword-dump alias: retained for lexical use, never for resolution.
        EntityAlias(TERM, "nearest neighbour search", "keyword", "keywords"),
    ]
    if exclude_model_planner:
        aliases.append(EntityAlias(MODEL, "planner", EXCLUSION_ALIAS_KIND, "glossary"))
    return EntityRegistry(
        entities=(
            _entity(TOOL, "tool_query_planner", "tool"),
            _entity(MODEL, "model_planner", "model"),
            _entity(TEAM, "team_platform", "team"),
            _entity(TERM, "term_vector_search", "concept"),
        ),
        aliases=tuple(aliases),
    )


# ── clause 1: a mention resolves to a canonical typed entity ────────────────


def test_exact_alias_resolves_to_a_canonical_typed_entity() -> None:
    result = EntityResolver(_registry()).resolve("term_vector_search")
    assert result.resolved and result.entity_id == TERM
    assert result.canonical_name == "term_vector_search"
    assert result.entity_type == "concept"          # TYPED, not just an id
    assert result.method == "exact_alias"
    assert result.score == EXACT_SCORE
    assert result.candidates == ()


def test_resolution_is_normalization_insensitive() -> None:
    resolver = EntityResolver(_registry())
    for surface in ("VI", "vi", "  Vi  "):
        assert resolver.resolve(surface).entity_id == TERM


def test_type_preference_breaks_a_collision_without_guessing() -> None:
    resolver = EntityResolver(_registry())
    assert resolver.resolve("planner", "tool").entity_id == TOOL
    assert resolver.resolve("planner", "model").entity_id == MODEL


def test_exclusion_applied_at_the_exact_tier_makes_a_collision_unique() -> None:
    # the authored exclusion says "this surface is NOT that entity", which turns
    # an ambiguous mention into a clean, typed resolution.
    result = EntityResolver(_registry(exclude_model_planner=True)).resolve("planner")
    assert result.entity_id == TOOL
    assert result.entity_type == "tool"
    assert result.method == "exact_alias"


def test_exclusion_applied_at_the_search_tiers_too() -> None:
    # a lexical or dense hit is no more entitled to override an authored
    # exclusion than an alias is.
    registry = EntityRegistry(
        entities=_registry().entities,
        aliases=(EntityAlias(MODEL, "route planning", EXCLUSION_ALIAS_KIND, "glossary"),),
    )
    backend = MappingSearchBackend({"route planning": (EntitySearchHit(MODEL, 0.91),)})
    assert EntityResolver(registry, full_text=backend).resolve(
        "route planning"
    ).method == "unresolved"
    assert EntityResolver(registry, dense=backend).resolve(
        "route planning"
    ).method == "unresolved"


def test_unknown_mention_is_unresolved_not_guessed() -> None:
    result = EntityResolver(_registry()).resolve("no such surface form")
    assert not result.resolved
    assert result.method == "unresolved"
    assert result.candidates == ()


# ── clause 2: an ambiguous mention returns candidates, never a guess ────────


def test_ambiguous_mention_returns_candidates_rather_than_a_guess() -> None:
    result = EntityResolver(_registry()).resolve("planner")
    assert result.entity_id is None                 # NOT a ranked pick
    assert result.is_ambiguous and result.method == "ambiguous"
    assert result.score == 0.0
    assert {c.entity_id for c in result.candidates} == {TOOL, MODEL}
    assert {c.entity_type for c in result.candidates} == {"tool", "model"}
    assert "2 candidates" in str(result)


def test_ambiguity_short_circuits_the_ranking_tiers() -> None:
    # letting a RANKER pick between two exact alias matches would reintroduce
    # the guess the exact tier just refused, so the later tiers never run.
    backend = MappingSearchBackend({"planner": (EntitySearchHit(MODEL, 0.99),)})
    result = EntityResolver(_registry(), full_text=backend, dense=backend).resolve(
        "planner"
    )
    assert result.method == "ambiguous" and result.entity_id is None


def test_ambiguity_prominence_tiebreak_is_opt_in_only() -> None:
    resolver = EntityResolver(
        _registry(), ambiguity="prominence", prominence={MODEL: 0.9, TOOL: 0.1}
    )
    result = resolver.resolve("planner")
    assert result.entity_id == MODEL
    assert result.method == "exact_alias_disambiguated"
    assert result.score == DISAMBIGUATED_SCORE
    # even when it picks, the candidate set travels with the answer.
    assert {c.entity_id for c in result.candidates} == {TOOL, MODEL}


def test_requested_type_is_reported_on_an_abstention() -> None:
    result = EntityResolver(_registry()).resolve("planner", "service")
    assert result.method == "ambiguous"             # no same-type match to prefer
    assert result.requested_type == "service"


# ── the tiers: cheapest first, injected, type-preferring ───────────────────


def test_keyword_dump_alias_never_resolves_even_as_the_only_surface() -> None:
    # the measured false-link regression: a frontmatter keyword list names
    # RELATED terms as often as the note's own entity.
    assert EntityResolver(_registry()).resolve(
        "nearest neighbour search"
    ).method == "unresolved"


def test_full_text_tier_runs_after_the_exact_tier_misses() -> None:
    backend = MappingSearchBackend(
        {"vector search": (EntitySearchHit(TERM, 0.42),)}
    )
    result = EntityResolver(_registry(), full_text=backend).resolve("vector search")
    assert result.entity_id == TERM
    assert result.method == "full_text"
    assert result.score == FULL_TEXT_TYPED_SCORE


def test_full_text_tier_relaxes_the_type_constraint_last() -> None:
    backend = MappingSearchBackend(
        {"vector search": (EntitySearchHit(TERM, 0.42), EntitySearchHit(TEAM, 0.30))}
    )
    resolver = EntityResolver(_registry(), full_text=backend)
    typed = resolver.resolve("vector search", "team")
    assert typed.entity_id == TEAM and typed.score == FULL_TEXT_TYPED_SCORE
    relaxed = resolver.resolve("vector search", "service")   # no hit of that type
    assert relaxed.entity_id == TERM and relaxed.score == FULL_TEXT_RELAXED_SCORE


def test_dense_tier_runs_last_and_reports_the_backend_score() -> None:
    dense = MappingSearchBackend({"knn lookup": (EntitySearchHit(TERM, 0.77),)})
    resolver = EntityResolver(_registry(), full_text=MappingSearchBackend(), dense=dense)
    result = resolver.resolve("knn lookup")
    assert result.method == "dense"
    assert result.score == pytest.approx(0.77)      # a real similarity, not a constant


def test_search_tiers_ignore_hits_that_are_not_registered_entities() -> None:
    backend = MappingSearchBackend(
        {"a phrase": (EntitySearchHit("archives/doc_release.md", 0.99),)}
    )
    result = EntityResolver(_registry(), full_text=backend, dense=backend).resolve(
        "a phrase"
    )
    assert result.method == "unresolved"            # a plain note is not an anchor


def test_search_limit_is_honoured_by_the_backend_seam() -> None:
    hits = tuple(EntitySearchHit(f"n{i}", 0.5) for i in range(10)) + (
        EntitySearchHit(TERM, 0.4),
    )
    backend = MappingSearchBackend({"long tail": hits})
    assert EntityResolver(_registry(), full_text=backend, search_limit=3).resolve(
        "long tail"
    ).method == "unresolved"
    assert EntityResolver(_registry(), full_text=backend, search_limit=20).resolve(
        "long tail"
    ).entity_id == TERM


def test_retrieval_backend_adapts_the_read_only_port() -> None:
    # the production backend reads through RetrievalClient, which has no
    # index/update/delete surface — resolution cannot mutate the index.
    class _StubClient:
        def search(self, query, *, k=20, snippet_length=30):
            assert k == 5
            return [type("H", (), {"note_id": TERM, "score": 0.61})()]

    backend = RetrievalSearchBackend(client=_StubClient())  # type: ignore[arg-type]
    assert backend("anything", limit=5) == (EntitySearchHit(TERM, 0.61),)
    assert not hasattr(RetrievalSearchBackend, "index")


# ── the resolver as the authored seed's object resolver ─────────────────────


def test_typed_object_resolver_links_only_on_the_expected_type() -> None:
    resolve = TypedObjectResolver(resolver=EntityResolver(_registry()))
    assert resolve("team_platform", "team") == (TEAM, "entity")
    # right surface, WRONG expected type → the authored value stays a literal
    # rather than landing on whatever entity shares the form.
    assert resolve("team_platform", "repository") == ("team_platform", "literal")
    assert resolve("team_platform", ANY_OBJECT_TYPE) == (TEAM, "entity")
    assert resolve("https://example.invalid/x", None) == (
        "https://example.invalid/x", "literal",
    )


def test_typed_object_resolver_keeps_an_ambiguous_object_literal() -> None:
    resolve = TypedObjectResolver(resolver=EntityResolver(_registry()))
    assert resolve("planner", ANY_OBJECT_TYPE) == ("planner", "literal")


def test_authored_seed_with_a_real_resolver_is_still_o_n() -> None:
    # wiring the resolver in changes object_kind, never the row COUNT: the seed
    # still reads one attribute per node and never enumerates pairs.
    nodes = tuple(
        NoteFacts(
            note_id=f"areas/models/model_{i:02d}.md",
            note_name=f"model_{i:02d}",
            second_category="model",
            frontmatter={"owner": "team_platform", "inputs": "term_vector_search"},
        )
        for i in range(6)
    )
    fields = {
        "owner": RelationFieldSpec("owned_by", "team"),
        "inputs": RelationFieldSpec("consumes", ANY_OBJECT_TYPE),
    }
    rows = seed_authored_relations(
        nodes,
        fields=fields,
        resolver=TypedObjectResolver(resolver=EntityResolver(_registry())),
    )
    audit = audit_authored_seed(rows, field_count=len(fields))
    assert audit.row_count == 6 * 2 == audit.row_bound
    assert audit.max_rows_per_subject_predicate == 1
    assert audit.pair_enumerated_rows == 0
    assert {r.object_ref for r in rows} == {TEAM, TERM}    # objects were LINKED
    assert {r.object_kind for r in rows} == {"entity"}
