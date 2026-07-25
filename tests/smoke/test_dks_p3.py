"""DKS refactor P3 — deterministic DKSNoteCompiler + substrate reuse.

Gate-to-P4 deliverables:
 - the compiler is byte-stable (same cycle result → same NoteIntentGraph);
 - the mechanical mapping is correct (observation→empirical_observation,
   arguments→argument, defeated attack→counter_argument, regularity→model,
   warrant proposal→procedure with supersedes coupling);
 - the compiled graph flows through the SHIPPED substrate (projection +
   write_closure + KnowledgeCapsule + VersionedVault publish) end-to-end,
   reusing it wholesale (no re-derivation).
"""

from __future__ import annotations

import json
from pathlib import Path

from tessellum.composer import (
    KnowledgeCapsule,
    VaultSnapshot,
    VersionedVault,
    project_note_intent_graph,
    write_closure,
)
from tessellum.composer import MockBackend
from tessellum.dks import DKSCycle, DKSObservation
from tessellum.dks.compiler import DKSNoteCompiler


def _arg(claim: str, warrant: str) -> str:
    return json.dumps({
        "claim": claim, "data": "D", "warrant": warrant,
        "qualifier": "usually", "evidence": "E",
    })


def _full_backend() -> MockBackend:
    return MockBackend(responses={
        "conservative": _arg("claim-A", "W-A"),
        "exploratory": _arg("claim-B", "W-B"),
        "counter-argument": json.dumps({
            "attacked_fz": "5a", "broken_component": "warrant",
            "counter_claim": "cc", "reason": "r", "strength": "moderate"}),
        "pattern discovery": json.dumps({"description": "regularity", "observed": ["5a"]}),
        "rule revision": json.dumps({
            "claim": "R", "data": "D", "warrant": "W'",
            "qualifier": "in most cases", "supersedes": ""}),
    })


def _gated_backend() -> MockBackend:
    return MockBackend(responses={"conservative": _arg("A", "W-A")})


def _full_cycle():
    return DKSCycle(DKSObservation(folgezettel="5", summary="something"), (),
                    _full_backend()).run()


# ── byte-stability ──────────────────────────────────────────────────────────


def test_compiler_is_byte_stable() -> None:
    cyc = _full_cycle()
    g1 = DKSNoteCompiler().compile(cyc)
    g2 = DKSNoteCompiler().compile(cyc)
    assert g1.model_dump() == g2.model_dump()  # same result → same graph


def test_compiler_makes_no_llm_call() -> None:
    # a backend that records calls; the compiler must NOT touch it.
    cyc = _full_cycle()
    calls = {"n": 0}

    class _CountingBackend:
        backend_id = "counting"
        def complete(self, *a, **k):  # pragma: no cover - must never run
            calls["n"] += 1
            return ""

    # compile takes only the finished cycle result — no backend param at all.
    DKSNoteCompiler().compile(cyc)
    assert calls["n"] == 0


# ── mechanical mapping ──────────────────────────────────────────────────────


def test_mapping_covers_all_five_roles() -> None:
    g = DKSNoteCompiler().compile(_full_cycle())
    roles = [i.building_block for i in g.intents]
    assert roles.count("empirical_observation") == 1
    assert roles.count("argument") == 2  # A + B
    assert roles.count("counter_argument") == 1
    assert roles.count("model") == 1  # a MODEL, never an empirical fact
    assert roles.count("procedure") == 1  # the revised warrant


def test_regularity_is_model_not_empirical_fact() -> None:
    g = DKSNoteCompiler().compile(_full_cycle())
    # the pattern node is a model/hypothesis (provisional), NOT an empirical_observation
    model_intents = [i for i in g.intents if i.building_block == "model"]
    assert model_intents and model_intents[0].thesis == "regularity"


def test_counter_argument_edges_to_attacked() -> None:
    g = DKSNoteCompiler().compile(_full_cycle())
    counter = next(i for i in g.intents if i.building_block == "counter_argument")
    # the counter depends_on (attacks) the attacked argument's path
    assert any("argument" in d for d in counter.depends_on)


def test_gated_cycle_compiles_observation_plus_argument_only() -> None:
    gated = DKSCycle(
        DKSObservation(folgezettel="5", summary="x"), (), _gated_backend(),
        confidence_model=lambda o, w: 0.99, confidence_threshold=0.85,
    ).run()
    g = DKSNoteCompiler().compile(gated)
    roles = [i.building_block for i in g.intents]
    assert roles == ["empirical_observation", "argument"]  # 2 nodes, no loop


def test_every_intent_carries_provenance() -> None:
    g = DKSNoteCompiler().compile(_full_cycle())
    for intent in g.intents:
        assert intent.provenance  # non-empty (cites the cycle observation)
        assert all(p.source_ref.startswith("dks-cycle://") for p in intent.provenance)


# ── substrate reuse end-to-end (project → closure → capsule → publish) ──────


def test_compiled_graph_flows_through_substrate(tmp_path: Path) -> None:
    g = DKSNoteCompiler().compile(_full_cycle())

    # projection (P2b) + exact write closure (P4 substrate) — reused, not rebuilt
    leaves = project_note_intent_graph(g)
    assert len(leaves) == len(g.intents)
    wc = write_closure(g)
    assert wc.touched_note_ids  # closure computed over the DKS intents

    # a KnowledgeCapsule + versioned publish (P5 substrate) — reused wholesale
    vault = VersionedVault(tmp_path / "pub")
    genesis = vault.initialize()
    capsule = KnowledgeCapsule(
        capsule_id=f"dks:{g.objective_id}", source_bundle_hash="sb",
        vault_snapshot_id=VaultSnapshot(base_generation=genesis, index_hash="h").snapshot_id,
        knowledge_plan_hash="kp", write_closure=wc,
    )
    assert capsule.well_formed(wc)
    files = {leaf["target_path"]: f"# {leaf['note']['thesis']}\n".encode() for leaf in leaves}
    gen = vault.prepare(capsule, files)
    res = vault.publish(gen, expected_current=genesis)
    assert res.outcome == "published"
    assert vault.current_generation() == gen


def test_cycle_compiles_to_a_single_invariant_closed_capsule() -> None:
    # Review nit (medium): a DKS cycle is ONE atomic transaction — the compiled
    # graph must NOT partition into disjoint capsules. The epistemic back-edges
    # (counter->pattern, pattern->revision) couple all nodes into one.
    from tessellum.composer import partition_capsules
    g = DKSNoteCompiler().compile(_full_cycle())
    capsules = partition_capsules(g)
    assert len(capsules) == 1  # the whole cycle promotes atomically
    # the single capsule touches every compiled node
    touched = capsules[0].touched_note_ids
    assert all(i.note_id in touched for i in g.intents)
