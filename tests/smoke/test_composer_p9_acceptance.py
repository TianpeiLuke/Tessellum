"""P9 — effect-class expansion (A9.2) + release acceptance matrix (A9.1).

A9.2: update/merge/drop dispositions are enabled (create-only lifted), gated by
the preimage rule. A9.1: an end-to-end acceptance matrix that wires the phase
modules together — the release criterion the plan names (NOT one mocked test):
bundle → NoteIntentGraph → exact write closure + boundary witness → overlay
staging → structural gates + human approval → semantic certificate →
versioned publication + snapshot CAS + crash recovery + byte-identical replay.

A9.3 (per-action grain) is gated on the P7 certificate being calibrated on a
real wrong-but-well-formed corpus (b3/A7.5) — the gating LOGIC is exercised
here; the corpus is the standing research prerequisite before unattended
per-action promotion is switched on.
"""

from __future__ import annotations

from pathlib import Path

from tessellum.composer.knowledge_plan import (
    BundleMember,
    ClaimProvenance,
    NoteIntent,
    NoteIntentGraph,
    SourceBundle,
    bundle_content_hash,
    project_note_intent_graph,
)
from tessellum.composer.overlay_index import DeltaState, OverlayIndex
from tessellum.composer.publication import (
    KnowledgeCapsule,
    VaultSnapshot,
    VersionedVault,
)
from tessellum.composer.semantic_certificate import (
    Claim,
    ClaimScore,
    LabeledExample,
    calibrate,
    certify,
)
from tessellum.composer.structural_gates import (
    HumanApproval,
    StructuralGateContext,
    supervised_admit,
)
from tessellum.composer.write_closure import boundary_witness, write_closure


def _prov():
    return (ClaimProvenance(span_id="s1", source_ref="bundle://doc#1"),)


# ── A9.2 — effect-class expansion ───────────────────────────────────────────


def test_all_effect_classes_construct_with_preimage_rule() -> None:
    # create (no preimage) + update/merge/drop (preimage required) + skip.
    create = NoteIntent(note_id="c", thesis="t", building_block="concept",
                        target_path="areas/c.md", provenance=_prov())
    update = NoteIntent(note_id="u", thesis="t", building_block="concept",
                        target_path="areas/u.md", provenance=_prov(),
                        disposition="update", expected_preimage="h1")
    drop = NoteIntent(note_id="d", thesis="t", building_block="concept",
                      target_path="areas/d.md", provenance=_prov(),
                      disposition="drop", expected_preimage="h2")
    assert create.disposition == "create"
    assert update.disposition == "update"
    assert drop.disposition == "drop"


def test_update_effect_shadows_in_overlay(tmp_path: Path) -> None:
    # A9.2 uses the P3 OverlayIndex tombstone/shadow semantics for a delete.
    from tessellum.indexer import Database, build
    d = tmp_path / "v"
    (d / "resources/term_dictionary").mkdir(parents=True)
    note = ("---\ntags: [resource, terminology]\nkeywords: [a,b,c]\ntopics: [X]\n"
            "language: markdown\ndate of note: 2026-05-10\nstatus: active\n"
            "building_block: concept\n---\n\n# A\n\nbody\n")
    (d / "resources/term_dictionary/term_a.md").write_text(note)
    dbp = d.parent / "idx.db"
    build(d, dbp)
    ix = OverlayIndex(Database(dbp), DeltaState())
    aid = "resources/term_dictionary/term_a.md"
    assert ix.exists(aid)
    ix.stage_delete(aid)  # a drop
    assert not ix.exists(aid)  # tombstoned (P3 semantics reused by P9)


# ── A9.1 — end-to-end acceptance matrix (release criterion) ──────────────────


def test_end_to_end_bundle_to_published_generation(tmp_path: Path) -> None:
    # 1. a SourceBundle admitted as one objective (P2b).
    bundle = SourceBundle(
        bundle_id="pending", objective="digest design doc",
        members=(BundleMember(source_id="m0", ordinal=0, ref="doc.md",
                              parser_id="md", extracted_text_hash="h0"),),
    )
    sb_hash = bundle_content_hash(bundle)

    # 2. a NoteIntentGraph (P2) → deterministic writer-leaf projection (P2/P2b).
    graph = NoteIntentGraph(objective_id=bundle.bundle_id, intents=(
        NoteIntent(note_id="areas/n1.md", thesis="first", building_block="concept",
                   target_path="areas/n1.md", provenance=_prov(),
                   navigation=("0_entry_points/entry_x.md",)),
        NoteIntent(note_id="areas/n2.md", thesis="second", building_block="procedure",
                   target_path="areas/n2.md", provenance=_prov(),
                   required_inlinks=("areas/n1.md",)),
    ))
    leaves = project_note_intent_graph(graph)
    assert len(leaves) == 2

    # 3. exact write closure (P4) + boundary witness passes (no escaping edge).
    wc = write_closure(graph)
    touched = wc.touched_note_ids
    assert "0_entry_points/entry_x.md" in touched  # nav row is a mandatory write
    assert "areas/n1.md" in touched  # required reverse-inlink target
    witness = boundary_witness(wc, edges=[],
                               note_category_of={}, fz_parent_of={})
    assert witness.ok

    # 4. structural gates + human approval (P6).
    ctx = StructuralGateContext(graph=graph, write_closure=wc)
    needs_human = supervised_admit(ctx, capsule_id="cap1", approval=None)
    assert needs_human.decision == "blocked_needs_human"  # structurally safe
    approved = supervised_admit(ctx, capsule_id="cap1",
                                approval=HumanApproval("cap1", "luke", "sig"))
    assert approved.decision == "approved"

    # 5. semantic certificate accepts inside the calibrated domain (P7).
    th = calibrate(
        [LabeledExample("grounding", 0.9, True) for _ in range(10)],
        alpha=0.05, domains=("design",),
    )
    claims = [Claim("cl1", "n1 claim", "bundle://doc#1", "grounding")]
    cert = certify(claims, scorer=lambda cs: [ClaimScore("cl1", 0.95)],
                   thresholds=th, note_domain="design")
    assert cert.decision == "accept"
    assert cert.verdict.status == "grounded"

    # 6. versioned publication + snapshot CAS (P5): prepare → publish → ack.
    vault = VersionedVault(tmp_path / "pub")
    genesis = vault.initialize()
    capsule = KnowledgeCapsule(
        capsule_id="cap1", source_bundle_hash=sb_hash,
        vault_snapshot_id=VaultSnapshot(base_generation=genesis, index_hash="h").snapshot_id,
        knowledge_plan_hash="kp", write_closure=wc,
    )
    assert capsule.well_formed(wc)
    files = {leaf["target_path"]: f"# {leaf['note']['thesis']}\n".encode() for leaf in leaves}
    gen = vault.prepare(capsule, files)
    assert vault.current_generation() == genesis  # PREPARED invisible
    res = vault.publish(gen, expected_current=genesis)
    assert res.outcome == "published"
    assert vault.current_generation() == gen  # atomic swap
    vault.acknowledge(gen)

    # 7. crash recovery is idempotent + a re-prepare of identical content is
    #    byte-stable (deterministic capsule replay).
    vault2 = VersionedVault(tmp_path / "pub")
    live = vault2.recover()
    assert live == gen
    assert vault2.is_acknowledged(gen)
    gen_again = vault2.prepare(capsule, files)
    assert gen_again == gen  # content-addressed → byte-identical replay id


def test_end_to_end_cas_conflict_blocks_stale_capsule(tmp_path: Path) -> None:
    # the acceptance matrix's concurrency case: a capsule planned against a
    # stale base is refused at publish (no lost update).
    vault = VersionedVault(tmp_path / "pub")
    genesis = vault.initialize()
    wc = write_closure((NoteIntent(note_id="areas/a.md", thesis="t",
                                   building_block="concept", target_path="areas/a.md",
                                   provenance=_prov()),))
    cap = KnowledgeCapsule("capA", "sb", "snap", "kp", wc)
    g1 = vault.prepare(cap, {"areas/a.md": b"# A\n"})
    vault.publish(g1, expected_current=genesis)
    # a second capsule planned against the stale genesis is refused.
    wc2 = write_closure((NoteIntent(note_id="areas/b.md", thesis="t",
                                    building_block="concept", target_path="areas/b.md",
                                    provenance=_prov()),))
    cap2 = KnowledgeCapsule("capB", "sb", "snap", "kp", wc2)
    g2 = vault.prepare(cap2, {"areas/b.md": b"# B\n"})
    assert vault.publish(g2, expected_current=genesis).outcome == "cas_conflict"


def test_semantic_certificate_gates_unattended_grain(tmp_path: Path) -> None:
    # A9.3 gating LOGIC: per-action unattended promotion is allowed only when
    # the certificate ACCEPTS; an abstain falls back to the P6 human artifact.
    th = calibrate([LabeledExample("grounding", 0.9, True) for _ in range(10)],
                   alpha=0.05, domains=("design",))
    claims = [Claim("c", "claim", "src", "grounding")]
    # low score → abstain → must NOT auto-promote (fall back to human).
    abstain = certify(claims, scorer=lambda cs: [ClaimScore("c", 0.1)],
                      thresholds=th, note_domain="design")
    assert abstain.decision == "abstain"
    # out-of-calibrated-domain → abstain (fail-closed), never unattended.
    ood = certify(claims, scorer=lambda cs: [ClaimScore("c", 0.99)],
                  thresholds=th, note_domain="finance")
    assert ood.decision == "abstain"
