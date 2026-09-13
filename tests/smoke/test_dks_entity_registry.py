"""Query-time DKS P1 — the entity registry and the authored O(N) relations seed.

Gate deliverables:
 - resolution admits RELIABLE alias kinds only; a keyword-dump alias is retained
   for lexical use but is structurally refused by the resolution index (the
   measured false-link regression, encoded as a constraint);
 - the spine projection is deterministic and skips structural hubs;
 - the authored seed is O(N) in entities with ZERO pair-enumerated rows, and a
   single-valued authored field yields exactly one row per (subject, predicate);
 - the runtime registry store round-trips the projection and refuses a
   non-authored row through the authored-seed door.

The store tests live here (rather than under ``tests/runtime``) because they
exercise the same P1 projection end to end: emit rows in ``dks``, persist them in
``runtime``, read them back unchanged.
"""

from __future__ import annotations

import dataclasses
import sqlite3

import pytest

from tessellum.dks.entity_registry import (
    DEFAULT_RELATION_FIELDS,
    EXCLUSION_ALIAS_KIND,
    RELIABLE_ALIAS_KINDS,
    AuthoredRelation,
    Entity,
    EntityAlias,
    EntityRegistry,
    LiteralObjectResolver,
    MentionRecord,
    NoteFacts,
    RegistrySink,
    RegistrySource,
    RelationFieldSpec,
    ResolutionIndex,
    SpineSpec,
    UnreliableAliasError,
    aggregate_candidates,
    audit_authored_seed,
    link_candidates,
    norm,
    project_spine,
    registry_content_digest,
    seed_authored_relations,
)
from tessellum.runtime.registry_store import RegistryStore, RegistryStoreError

TERM = "resources/term_dictionary/term_vector_search.md"
TEAM = "areas/teams/team_platform.md"
TOOL = "areas/tools/tool_query_planner.md"
REPO = "areas/code_repos/repo_ingest_pipeline.md"


def _defining_notes() -> tuple[NoteFacts, ...]:
    """Four defining notes plus three that must NOT become entities."""
    return (
        NoteFacts(
            note_id=TERM,
            note_name="term_vector_search",
            second_category="terminology",
            keywords=("nearest neighbour search", "ANN"),
            folgezettel="4a1",
            file_path=TERM,
            content_hash="h-term",
        ),
        NoteFacts(
            note_id=TEAM,
            note_name="team_platform",
            second_category="team",
            file_path=TEAM,
            content_hash="h-team",
        ),
        NoteFacts(
            note_id=TOOL,
            note_name="tool_query_planner",
            second_category="tool",
            keywords=("planner",),
            file_path=TOOL,
            content_hash="h-tool",
        ),
        NoteFacts(
            note_id=REPO,
            note_name="repo_ingest_pipeline",
            second_category="code_repo",
            file_path=REPO,
            content_hash="h-repo",
        ),
        # structural noise: a hub, a README, and a section sub-note — all carry a
        # DEFINING second-category but none of them is a leaf entity.
        NoteFacts(note_id="0_entry_points/entry_terms.md", note_name="entry_terms",
                  second_category="terminology"),
        NoteFacts(note_id="areas/teams/README.md", note_name="README",
                  second_category="team"),
        NoteFacts(note_id="areas/tools/tool_suite_overview.md",
                  note_name="tool_suite_overview", second_category="tool"),
    )


# ── the spine projection ────────────────────────────────────────────────────


def test_spine_projects_one_entity_per_defining_note() -> None:
    entities, aliases = project_spine(_defining_notes())
    assert [e.entity_id for e in entities] == sorted([TERM, TEAM, TOOL, REPO])
    by_id = {e.entity_id: e for e in entities}
    assert by_id[TOOL].entity_type == "tool"        # second-category → entity type
    assert by_id[REPO].entity_type == "repository"
    assert by_id[TERM].entity_type == "concept"
    assert all(e.source_layer == "spine" for e in entities)
    assert all(e.entity_id == e.note_id for e in entities)  # vault identity reused
    # the canonical name is a canonical-kind alias; keywords are keyword-kind.
    term_aliases = {(a.alias, a.alias_kind) for a in aliases if a.entity_id == TERM}
    assert ("term_vector_search", "canonical") in term_aliases
    assert ("ANN", "keyword") in term_aliases


def test_spine_skips_hubs_readmes_and_section_subnotes() -> None:
    entities, _ = project_spine(_defining_notes())
    names = {e.canonical_name for e in entities}
    assert "entry_terms" not in names       # hub prefix
    assert "README" not in names            # directory README
    assert "tool_suite_overview" not in names  # section/overview sub-note


def test_spine_skips_non_defining_categories() -> None:
    notes = (
        NoteFacts(note_id="archives/doc_release.md", note_name="doc_release",
                  second_category="documentation"),
    )
    entities, aliases = project_spine(notes)
    assert entities == () and aliases == ()


def test_spine_projection_is_deterministic_under_input_order() -> None:
    notes = _defining_notes()
    forward = project_spine(notes)
    reverse = project_spine(tuple(reversed(notes)))
    assert forward == reverse
    a = EntityRegistry(entities=forward[0], aliases=forward[1])
    b = EntityRegistry(entities=reverse[0], aliases=reverse[1])
    assert registry_content_digest(a) == registry_content_digest(b)


def test_spine_spec_is_data_not_code() -> None:
    # a vault names its own defining categories; the projection is configured,
    # not forked.
    spec = SpineSpec(defining_categories={"measurement": "metric"})
    notes = (NoteFacts(note_id="areas/metrics/metric_latency.md",
                       note_name="metric_latency", second_category="measurement"),)
    entities, _ = project_spine(notes, spec=spec)
    assert [e.entity_type for e in entities] == ["metric"]


# ── the reliability constraint (the measured lesson, as a constraint) ────────


def test_reliable_alias_kinds_exclude_the_keyword_dump() -> None:
    assert RELIABLE_ALIAS_KINDS == frozenset({"canonical", "acronym", "variant"})
    assert "keyword" not in RELIABLE_ALIAS_KINDS
    assert EXCLUSION_ALIAS_KIND not in RELIABLE_ALIAS_KINDS  # negative, not a source


def test_resolution_index_refuses_a_keyword_alias() -> None:
    keyword = EntityAlias(entity_id=TERM, alias="ANN", alias_kind="keyword",
                          source="keywords")
    with pytest.raises(UnreliableAliasError):
        ResolutionIndex.build((keyword,), {TERM: "concept"})


def test_registry_retains_keyword_aliases_but_never_resolves_them() -> None:
    entities, aliases = project_spine(_defining_notes())
    registry = EntityRegistry(entities=entities, aliases=aliases)
    # retained on the registry (lexical/full-text use) ...
    assert any(a.alias_kind == "keyword" and a.alias == "ANN" for a in registry.aliases)
    # ... and absent from the resolution index, which therefore cannot raise.
    index = registry.resolution_index()
    assert index.candidates_for(norm("ANN")) == ()
    assert index.candidates_for(norm("term_vector_search")) != ()


def test_exclusion_alias_blocks_one_pair_without_removing_the_entity() -> None:
    aliases = (
        EntityAlias(entity_id=TOOL, alias="planner", alias_kind="variant"),
        EntityAlias(entity_id=REPO, alias="planner", alias_kind="variant"),
        EntityAlias(entity_id=REPO, alias="planner", alias_kind=EXCLUSION_ALIAS_KIND),
    )
    index = ResolutionIndex.build(aliases, {TOOL: "tool", REPO: "repository"})
    assert index.is_excluded(norm("planner"), REPO)
    assert [r.entity_id for r in index.candidates_for(norm("planner"))] == [TOOL]


# ── candidates: the promotion queue, deterministic and non-guessing ──────────


def test_candidate_aggregation_is_deterministic_and_counts_distinct_notes() -> None:
    mentions = (
        MentionRecord("n1", "Vector Index", "concept"),
        MentionRecord("n2", "vector index", "concept"),
        MentionRecord("n2", "vector index", "concept"),
        MentionRecord("n3", "ingest pipeline", "repository"),
    )
    rows = aggregate_candidates(mentions)
    shuffled = aggregate_candidates(tuple(reversed(mentions)))
    assert rows == shuffled                      # order-invariant
    by_norm = {c.surface_norm: c for c in rows}
    assert by_norm["vector index"].mention_count == 3
    assert by_norm["vector index"].distinct_notes == 2
    assert 0.0 < by_norm["vector index"].confidence < 1.0


def test_candidate_linking_refuses_an_ambiguous_match() -> None:
    aliases = (
        EntityAlias(entity_id=TOOL, alias="planner", alias_kind="variant"),
        EntityAlias(entity_id=REPO, alias="planner", alias_kind="variant"),
        EntityAlias(entity_id=TERM, alias="term_vector_search", alias_kind="canonical"),
    )
    index = ResolutionIndex.build(
        aliases, {TOOL: "tool", REPO: "repository", TERM: "concept"}
    )
    candidates = aggregate_candidates(
        (
            MentionRecord("n1", "planner", "service"),           # ambiguous, no same-type
            MentionRecord("n2", "term_vector_search", "concept"),  # unique + same type
        )
    )
    linked = {c.surface_norm: c for c in link_candidates(candidates, index)}
    assert linked["planner"].status == "candidate"          # queued, not guessed
    assert linked["planner"].resolved_entity_id is None
    assert linked["term_vector_search"].status == "linked"
    assert linked["term_vector_search"].resolved_entity_id == TERM


# ── the authored O(N) relations seed ────────────────────────────────────────


def _authored_node(index: int) -> NoteFacts:
    """One node with three SINGLE-valued authored relation fields."""
    return NoteFacts(
        note_id=f"areas/models/model_{index:02d}.md",
        note_name=f"model_{index:02d}",
        second_category="model",
        file_path=f"areas/models/model_{index:02d}.md",
        content_hash=f"h-{index:02d}",
        frontmatter={
            "owner": "team_platform",
            "parent_note": "term_vector_search",
            "source_url": "https://example.invalid/spec",
            "status": "active",          # not a relation field — must be ignored
            "note_name": f"model_{index:02d}",
        },
    )


def test_authored_seed_emits_one_row_per_subject_predicate_from_one_node() -> None:
    # THE acceptance clause: a single node's single-valued frontmatter yields at
    # most one row per (subject, predicate).
    rows = seed_authored_relations((_authored_node(0),))
    audit = audit_authored_seed(rows, field_count=len(DEFAULT_RELATION_FIELDS))
    assert audit.max_rows_per_subject_predicate == 1
    assert {r.predicate for r in rows} == {"owned_by", "part_of", "cites_source"}
    assert len(rows) == 3               # exactly the authored fields, nothing else
    assert all(r.origin == "authored" for r in rows)
    assert all(r.epistemic_status == "asserted" for r in rows)


def test_authored_seed_contains_zero_pair_enumerated_rows() -> None:
    nodes = tuple(_authored_node(i) for i in range(8))
    rows = seed_authored_relations(nodes)
    audit = audit_authored_seed(rows, field_count=len(DEFAULT_RELATION_FIELDS))
    assert audit.pair_enumerated_rows == 0
    assert audit.non_authored_rows == 0
    # the structural witness: every row is evidenced by its OWN subject's note,
    # and every object came out of that node's own frontmatter.
    frontmatter = {n.note_id: set(map(str, n.frontmatter.values())) for n in nodes}
    for row in rows:
        assert row.evidence_note == row.subject_id
        assert row.evidence_locator.startswith("frontmatter:")
        assert row.object_ref in frontmatter[row.subject_id]


def test_authored_seed_row_count_is_linear_in_entities() -> None:
    small = seed_authored_relations(tuple(_authored_node(i) for i in range(2)))
    large = seed_authored_relations(tuple(_authored_node(i) for i in range(8)))
    assert len(small) == 2 * 3
    assert len(large) == 8 * 3            # 4x the nodes → exactly 4x the rows
    audit = audit_authored_seed(large, field_count=len(DEFAULT_RELATION_FIELDS))
    assert audit.subject_count == 8
    assert audit.is_linear and audit.row_count <= audit.row_bound
    # a pair-enumerating build would emit at least N*(N-1) rows; this is O(N).
    assert audit.row_count < 8 * 7


def test_authored_seed_multivalued_field_stays_bounded_by_its_own_node() -> None:
    node = dataclasses.replace(
        _authored_node(0), frontmatter={"inputs": ["term_vector_search", "team_platform"]}
    )
    rows = seed_authored_relations((node,))
    audit = audit_authored_seed(rows, field_count=len(DEFAULT_RELATION_FIELDS))
    # one addressable row per authored VALUE, each with its own ordinal locator —
    # bounded by this node's frontmatter, never by the entity count.
    assert len(rows) == 2
    assert audit.max_rows_per_subject_predicate == 2 == len(node.frontmatter["inputs"])
    assert {r.evidence_locator for r in rows} == {
        "frontmatter:inputs[0]", "frontmatter:inputs[1]"
    }
    assert audit.pair_enumerated_rows == 0


def test_authored_seed_ignores_nullish_values_and_unknown_fields() -> None:
    node = dataclasses.replace(
        _authored_node(0),
        frontmatter={"owner": "TBD", "parent_note": "  ", "unrelated": "team_platform"},
    )
    assert seed_authored_relations((node,)) == ()


def test_authored_seed_is_deterministic_and_replay_idempotent() -> None:
    nodes = tuple(_authored_node(i) for i in range(4))
    first = seed_authored_relations(nodes)
    second = seed_authored_relations(tuple(reversed(nodes)))
    assert first == second                                  # content-addressed ids
    assert len({r.relation_id for r in first}) == len(first)


def test_authored_seed_keeps_literal_only_fields_literal() -> None:
    # a field spec'd object_type=None never resolves, whatever the resolver says.
    rows = seed_authored_relations(
        (_authored_node(0),),
        fields={"source_url": RelationFieldSpec("cites_source", None)},
        resolver=LiteralObjectResolver(),
    )
    assert [r.object_kind for r in rows] == ["literal"]
    assert rows[0].object_ref == "https://example.invalid/spec"


def test_authored_seed_carries_a_validity_interval_slot() -> None:
    # NULL for an undated authored fact, but present — a role relation without
    # the interval confidently returns a FORMER holder.
    rows = seed_authored_relations((_authored_node(0),))
    owned = next(r for r in rows if r.predicate == "owned_by")
    assert owned.valid_from is None and owned.valid_to is None
    assert dataclasses.replace(owned, valid_from="2020-01-01").valid_from == "2020-01-01"


# ── the runtime store: persistence for the pure projection ──────────────────


def _built_registry() -> tuple[EntityRegistry, tuple[AuthoredRelation, ...]]:
    entities, aliases = project_spine(_defining_notes())
    candidates = link_candidates(
        aggregate_candidates((MentionRecord("n1", "term_vector_search", "concept"),)),
        EntityRegistry(entities=entities, aliases=aliases).resolution_index(),
    )
    registry = EntityRegistry(entities=entities, aliases=aliases, candidates=candidates)
    rows = seed_authored_relations(tuple(_authored_node(i) for i in range(3)))
    return registry, rows


def test_store_implements_the_registry_ports(tmp_path) -> None:
    # the Dependency Rule in one assertion: dks OWNS the ports, runtime backs
    # them, and nothing in dks/ imports runtime/ to make that true.
    store = RegistryStore.open(tmp_path / "registry.db")
    assert isinstance(store, RegistrySource)
    assert isinstance(store, RegistrySink)


def test_store_round_trips_the_projection_unchanged(tmp_path) -> None:
    store = RegistryStore.open(tmp_path / "registry.db")
    registry, rows = _built_registry()
    assert store.replace_spine(registry.entities, registry.aliases) == 4
    store.replace_candidates(registry.candidates)
    assert store.replace_authored_relations(rows) == len(rows)
    loaded = store.load_registry()
    assert registry_content_digest(loaded) == registry_content_digest(registry)
    # keyword aliases survive the round trip and still cannot resolve.
    assert any(a.alias_kind == "keyword" for a in loaded.aliases)
    assert loaded.resolution_index().candidates_for(norm("ANN")) == ()


def test_store_reads_relations_by_subject_never_by_enumeration(tmp_path) -> None:
    store = RegistryStore.open(tmp_path / "registry.db")
    registry, rows = _built_registry()
    store.replace_spine(registry.entities, registry.aliases)
    store.replace_authored_relations(rows)
    subject = rows[0].subject_id
    owned = store.relations_for(subject, "owned_by")
    assert [r.subject_id for r in owned] == [subject]
    assert owned[0].evidence_note == subject
    assert len(store.relations_for(subject)) == 3
    assert store.relations_for("areas/models/model_99.md") == ()


def test_store_rebuild_is_idempotent_and_digest_stable(tmp_path) -> None:
    registry, rows = _built_registry()
    digests = []
    for name in ("a.db", "b.db"):
        store = RegistryStore.open(tmp_path / name)
        store.replace_spine(registry.entities, registry.aliases)
        store.replace_candidates(registry.candidates)
        store.replace_authored_relations(rows)
        store.replace_authored_relations(rows)   # replay → same content
        store.put_meta("built_at", "2020-01-01T00:00:00Z")
        digests.append(store.content_digest())
    assert digests[0] == digests[1]              # meta excluded from the digest


def test_store_refuses_a_non_authored_row_through_the_seed_door(tmp_path) -> None:
    store = RegistryStore.open(tmp_path / "registry.db")
    registry, rows = _built_registry()
    store.replace_spine(registry.entities, registry.aliases)
    smuggled = dataclasses.replace(rows[0], origin="resolved")
    with pytest.raises(RegistryStoreError):
        store.replace_authored_relations((*rows, smuggled))


def test_store_reseed_leaves_resolved_rows_in_place(tmp_path) -> None:
    # P12's query-derived rows layer ON TOP of the authored seed; a reseed must
    # not drop them, so the delete is scoped to origin='authored'.
    store = RegistryStore.open(tmp_path / "registry.db")
    registry, rows = _built_registry()
    store.replace_spine(registry.entities, registry.aliases)
    store.replace_authored_relations(rows)
    conn = sqlite3.connect(store.path)
    try:
        conn.execute(
            "INSERT INTO relations(relation_id, subject_id, predicate, object_ref,"
            " object_kind, evidence_note, evidence_locator, origin)"
            " VALUES ('r-resolved', ?, 'owned_by', 'team_platform', 'literal', ?,"
            " 'body:12-40', 'resolved')",
            (rows[0].subject_id, rows[0].subject_id),
        )
        conn.commit()
    finally:
        conn.close()
    store.replace_authored_relations(rows)
    conn = sqlite3.connect(store.path)
    try:
        surviving = conn.execute(
            "SELECT count(*) FROM relations WHERE origin = 'resolved'"
        ).fetchone()[0]
    finally:
        conn.close()
    assert surviving == 1
    # ... and relations_for reads the authored layer only.
    assert all(r.origin == "authored" for r in store.relations_for(rows[0].subject_id))


def test_store_spine_replacement_drops_stale_entities_and_aliases(tmp_path) -> None:
    store = RegistryStore.open(tmp_path / "registry.db")
    registry, _ = _built_registry()
    store.replace_spine(registry.entities, registry.aliases)
    trimmed = tuple(e for e in registry.entities if e.entity_id != REPO)
    trimmed_aliases = tuple(a for a in registry.aliases if a.entity_id != REPO)
    assert store.replace_spine(trimmed, trimmed_aliases) == 3
    loaded = store.load_registry()
    assert {e.entity_id for e in loaded.entities} == {e.entity_id for e in trimmed}
    assert all(a.entity_id != REPO for a in loaded.aliases)


def test_store_keeps_a_promoted_entity_across_a_spine_reseed(tmp_path) -> None:
    # replace_spine writes (and deletes) the SPINE layer only: a promoted
    # candidate arrives by a different path and must survive a vault reseed.
    store = RegistryStore.open(tmp_path / "registry.db")
    registry, _ = _built_registry()
    store.replace_spine(registry.entities, registry.aliases)
    promoted = Entity(
        entity_id="areas/services/service_gateway.md",
        canonical_name="service_gateway",
        entity_type="service",
        note_id="areas/services/service_gateway.md",
        file_path="areas/services/service_gateway.md",
        source_layer="promoted",
    )
    conn = sqlite3.connect(store.path)
    try:
        conn.execute(
            "INSERT INTO entities(entity_id, canonical_name, entity_type, note_id,"
            " file_path, source_layer, scope) VALUES (?, ?, ?, ?, ?, 'promoted', 'local')",
            (promoted.entity_id, promoted.canonical_name, promoted.entity_type,
             promoted.note_id, promoted.file_path),
        )
        conn.commit()
    finally:
        conn.close()
    assert store.replace_spine(registry.entities, registry.aliases) == 4
    loaded = store.load_registry()
    assert promoted.entity_id in {e.entity_id for e in loaded.entities}
    assert len(loaded.entities) == 5
    # a promoted entity the projection did not offer is never dropped, and never
    # counted as spine.
    assert sum(1 for e in loaded.entities if e.source_layer == "promoted") == 1
