"""P4 (FZ 20k9d1b1a1a) — wiring per-note type-contract enrichment into the wave.

Verifies the leaf-enrichment seam (``_enrich_leaves_with_type_contract``): each
projected note leaf gains ``type_contract`` + ``type_contract_md`` resolved from
its ``target_path``, passes through byte-identical when disabled or when the leaf
is the whole-plan fallback, and stamps an empty contract (never a sentinel) when
the type can't be resolved. Composes with the related-notes enrichment without
clobbering. Mirrors ``test_composer_related_notes_wiring.py``.
"""

from __future__ import annotations

from tessellum.composer.digestion import (
    _enrich_leaves_with_related_notes,
    _enrich_leaves_with_type_contract,
)
from tessellum.composer.knowledge_plan import (
    ClaimProvenance,
    NoteIntent,
    NoteIntentGraph,
    project_note_intent_graph,
)


def _leaves(target_path: str = "resources/term_dictionary/term_new.md",
            building_block: str = "concept") -> list[dict]:
    graph = NoteIntentGraph(
        objective_id="obj",
        intents=(
            NoteIntent(
                note_id="n1",
                thesis="a named concept the note defines",
                building_block=building_block,
                target_path=target_path,
                coverage=("topic",),
                provenance=(ClaimProvenance(span_id="s1", source_ref="src#1"),),
            ),
        ),
    )
    return project_note_intent_graph(graph)


def test_typed_leaf_stamps_contract() -> None:
    out = _enrich_leaves_with_type_contract(_leaves())
    leaf = out[0]
    assert leaf["type_contract"]["flavor"] == "concept"
    assert leaf["type_contract"]["second_category"] == "terminology"
    assert leaf["type_contract"]["required_sections"] == [
        "Definition", "Examples", "References",
    ]
    assert leaf["type_contract_md"].startswith("Type:")
    assert "`## Definition`" in leaf["type_contract_md"]


def test_unresolvable_typed_leaf_stamps_empty() -> None:
    # An unregistered destination + prefix → no flavor. Stamp empty (sentinel-
    # safe), not crash.
    out = _enrich_leaves_with_type_contract(
        _leaves(target_path="resources/teams/team_x.md")
    )
    assert out[0]["type_contract"] == {}
    assert out[0]["type_contract_md"] == ""


def test_whole_plan_fallback_leaf_passes_through() -> None:
    fallback = [{"plan_path": "plans/p.md", "total_notes": 3}]
    out = _enrich_leaves_with_type_contract(fallback)
    assert out[0] == fallback[0]
    assert "type_contract" not in out[0]
    assert "type_contract_md" not in out[0]


def test_original_leaf_not_mutated() -> None:
    leaves = _leaves()
    _enrich_leaves_with_type_contract(leaves)
    assert "type_contract" not in leaves[0]
    assert "type_contract_md" not in leaves[0]


def test_disabled_returns_unchanged() -> None:
    leaves = _leaves()
    out = _enrich_leaves_with_type_contract(leaves, enabled=False)
    assert out is leaves  # byte-identical off-switch


def test_building_block_override_does_not_change_resolution() -> None:
    # A per-note building_block override must NOT change resolution — the flavor
    # is resolved from target_path. An argument-BB note authored at a term path
    # still gets the concept (term) contract.
    out = _enrich_leaves_with_type_contract(
        _leaves(target_path="resources/term_dictionary/term_x.md", building_block="argument")
    )
    assert out[0]["type_contract"]["flavor"] == "concept"
    assert out[0]["type_contract"]["required_sections"] == [
        "Definition", "Examples", "References",
    ]


def test_compose_order_with_related_notes() -> None:
    # Chaining both enrichments (the run_execute_wave order) yields a leaf
    # carrying BOTH keys; neither clobbers the other.
    leaves = _enrich_leaves_with_related_notes(_leaves(), related_notes_db=None)
    out = _enrich_leaves_with_type_contract(leaves)
    leaf = out[0]
    assert "related_references_md" in leaf
    assert "type_contract_md" in leaf
    assert leaf["type_contract"]["flavor"] == "concept"


def test_per_leaf_failure_isolated(monkeypatch) -> None:
    # If resolution raises for one leaf, it degrades to an empty contract, never
    # crashing the wave. resolve_note_contract already wraps fail-soft; force the
    # inner resolve to raise to confirm the seam still returns.
    import tessellum.composer.type_contract as tcmod

    def _boom(_path: str):
        raise RuntimeError("resolver blew up")

    monkeypatch.setattr(tcmod, "resolve_flavor", _boom)
    out = _enrich_leaves_with_type_contract(_leaves())
    assert out[0]["type_contract"] == {}
    assert out[0]["type_contract_md"] == ""


def test_run_execute_wave_actually_stamps_type_contract(monkeypatch) -> None:
    # End-to-end guard: drive run_execute_wave (not the helper directly) and
    # assert the leaves handed to run_pipeline_dynamic carry type_contract_md.
    # This catches a regression that deletes the enrichment hook in
    # run_execute_wave — which the helper-only tests would NOT catch.
    import tessellum.composer.digestion as dig
    from tessellum.composer.knowledge_plan import (
        ClaimProvenance,
        NoteIntent,
        NoteIntentGraph,
    )

    captured: dict = {}

    monkeypatch.setattr(dig, "compile_skill", lambda _p: object())

    def _fake_dynamic(_compiled, *, leaves, **_kw):
        captured["leaves"] = leaves
        return object()  # RunResult stand-in; run_execute_wave returns it as-is

    monkeypatch.setattr(dig, "run_pipeline_dynamic", _fake_dynamic)

    graph = NoteIntentGraph(
        objective_id="obj",
        intents=(
            NoteIntent(
                note_id="n1",
                thesis="a named concept",
                building_block="concept",
                target_path="resources/term_dictionary/term_x.md",
                provenance=(ClaimProvenance(span_id="s1", source_ref="src#1"),),
            ),
        ),
    )
    dig.run_execute_wave(
        {"note_intent_graph": graph},
        skills_dir="/nonexistent",  # compile_skill is stubbed, never read
        backend=object(),
        vault_root="/tmp",
        dry_run=True,
    )
    leaf = captured["leaves"][0]
    assert leaf["type_contract"]["flavor"] == "concept"
    assert leaf["type_contract_md"].startswith("Type:")
    # related-notes enrichment also ran (composed, not clobbered)
    assert "related_references_md" in leaf
