"""P2 (core) smoke — typed NoteIntentGraph + projection + create-only overlay.

Covers the P2 self-contained core action items and the gate-to-P2b acceptance:
  - A2.3: frozen NoteIntent / NoteIntentGraph — create-only disposition,
          REQUIRED provenance, forbid-extra, unique note_ids.
  - A2.4: project_note_intent_graph — pure, order-preserving, one leaf per
          intent with exactly {"note","target_path","source_ref"}.
  - A2.5: OverlayWriter — create-only, writes under overlay_root and NEVER
          under the live vault, fail-closed collision (overlay + base vault),
          path-escape rejection, optional rollback-parity recorder.

GATE-TO-P2b deliverables:
  GATE-1  model rejects non-create disposition + provenance-free intent
  GATE-2  projection purity / order / shape
  GATE-3  overlay writes under overlay_root, never the vault
  GATE-4  create-collision fail-closed (overlay + base vault)
  GATE-5  path-escape rejection
"""

from __future__ import annotations

import hashlib

import pytest
from pydantic import ValidationError

from tessellum.composer import (
    ClaimProvenance,
    NoteIntent,
    NoteIntentGraph,
    OverlayError,
    OverlayWriter,
    note_intent_content_id,
    project_note_intent_graph,
)


def _intent(**overrides) -> NoteIntent:
    """Build a valid create NoteIntent; override any field."""
    fields = {
        "note_id": "n1",
        "thesis": "the single point this note makes",
        "building_block": "concept",
        "target_path": "resources/term_dictionary/term_n1.md",
        "provenance": (ClaimProvenance(span_id="s1", source_ref="src://a"),),
    }
    fields.update(overrides)
    return NoteIntent(**fields)


# ── A2.3 — model cases (GATE-1) ────────────────────────────────────────────


@pytest.mark.parametrize("disp", ["update", "merge", "drop"])
def test_note_intent_mutation_requires_preimage(disp: str) -> None:
    # P9 (A9.2): update/merge/drop are enabled but REQUIRE expected_preimage
    # (the target must exist; the promotion CAS checks the pinned pre-image).
    with pytest.raises(ValidationError):
        _intent(disposition=disp)  # no preimage → invalid
    # with a preimage it is valid.
    ok = _intent(disposition=disp, expected_preimage="deadbeef")
    assert ok.disposition == disp


def test_note_intent_skip_is_allowed_noop() -> None:
    # P9: skip is an explicit no-op; a preimage is optional.
    assert _intent(disposition="skip").disposition == "skip"


def test_note_intent_rejects_provenance_free() -> None:
    # provenance=() violates min_length=1 — an intent with zero source spans
    # is invalid.
    with pytest.raises(ValidationError):
        _intent(provenance=())


def test_note_intent_rejects_preimage_on_create() -> None:
    with pytest.raises(ValidationError):
        _intent(expected_preimage="deadbeef")


def test_note_intent_rejects_self_dependency() -> None:
    with pytest.raises(ValidationError):
        _intent(note_id="n1", depends_on=("n1",))


def test_provenance_rejects_blank_fields() -> None:
    with pytest.raises(ValidationError):
        ClaimProvenance(span_id="", source_ref="src://a")
    with pytest.raises(ValidationError):
        ClaimProvenance(span_id="s1", source_ref="")


def test_models_frozen_and_forbid_extra() -> None:
    intent = _intent()
    # frozen → attribute reassignment rejected.
    with pytest.raises(ValidationError):
        intent.thesis = "mutated"  # type: ignore[misc]
    # extra="forbid" → unknown field rejected at construction.
    with pytest.raises(ValidationError):
        _intent(bogus=1)
    graph = NoteIntentGraph(objective_id="obj-1", intents=(intent,))
    with pytest.raises(ValidationError):
        graph.objective_id = "obj-2"  # type: ignore[misc]
    with pytest.raises(ValidationError):
        NoteIntentGraph(objective_id="obj-1", intents=(intent,), bogus=1)


def test_graph_rejects_duplicate_note_ids() -> None:
    a = _intent(note_id="dup", target_path="a/x.md")
    b = _intent(note_id="dup", target_path="a/y.md")
    with pytest.raises(ValidationError):
        NoteIntentGraph(objective_id="obj-1", intents=(a, b))


def test_graph_requires_objective_id() -> None:
    with pytest.raises(ValidationError):
        NoteIntentGraph(objective_id="", intents=())


# ── A2.4 — projection cases (GATE-2) ───────────────────────────────────────


def test_projection_one_leaf_per_intent_order_preserving() -> None:
    intents = (
        _intent(note_id="a", target_path="a/a.md"),
        _intent(note_id="b", target_path="b/b.md"),
        _intent(note_id="c", target_path="c/c.md"),
    )
    graph = NoteIntentGraph(objective_id="obj-1", intents=intents)
    leaves = project_note_intent_graph(graph)

    assert len(leaves) == 3
    # order preserved (declared order, no sort).
    assert [leaf["note"]["note_id"] for leaf in leaves] == ["a", "b", "c"]
    for leaf, intent in zip(leaves, intents):
        # exactly the three named top-level keys, nothing else.
        assert set(leaf.keys()) == {"note", "target_path", "source_ref"}
        assert leaf["target_path"] == intent.target_path
        # content_id stamped into the note payload, reusing P0 canonical hash.
        assert leaf["note"]["content_id"] == note_intent_content_id(intent)
        assert leaf["note"]["note_id"] == intent.note_id
        # no _id key — scheduler.run_pipeline_dynamic auto-injects it.
        assert "_id" not in leaf


def test_projection_distinct_source_refs_first_seen_order() -> None:
    intent = _intent(
        note_id="a",
        provenance=(
            ClaimProvenance(span_id="s1", source_ref="src://b"),
            ClaimProvenance(span_id="s2", source_ref="src://a"),
            ClaimProvenance(span_id="s3", source_ref="src://b"),  # dup ref
        ),
    )
    graph = NoteIntentGraph(objective_id="obj-1", intents=(intent,))
    leaf = project_note_intent_graph(graph)[0]
    # distinct, first-seen order (b before a; dup b dropped).
    assert leaf["source_ref"] == ["src://b", "src://a"]
    # non-empty (provenance is non-empty by model rule).
    assert leaf["source_ref"]
    # full span→ref mapping preserved losslessly inside "note".
    assert len(leaf["note"]["provenance"]) == 3


def test_projection_pure_no_mutation() -> None:
    intents = (
        _intent(note_id="a", target_path="a/a.md"),
        _intent(note_id="b", target_path="b/b.md"),
    )
    graph = NoteIntentGraph(objective_id="obj-1", intents=intents)
    before = graph.model_dump(mode="json")

    first = project_note_intent_graph(graph)
    second = project_note_intent_graph(graph)

    # deterministic: two calls yield equal results.
    assert first == second
    # input graph unchanged (frozen; deep-equal a re-dump).
    assert graph.model_dump(mode="json") == before
    # mutating a returned leaf must not affect the graph or a fresh projection.
    first[0]["note"]["note_id"] = "TAMPERED"
    assert project_note_intent_graph(graph)[0]["note"]["note_id"] == "a"


def test_projection_empty_graph() -> None:
    graph = NoteIntentGraph(objective_id="obj-1", intents=())
    assert project_note_intent_graph(graph) == []


# ── A2.5 — overlay writer cases (GATE-3/4/5) ───────────────────────────────


def test_overlay_writes_under_overlay_never_vault(tmp_path) -> None:
    overlay_root = tmp_path / "overlay"
    vault_root = tmp_path / "vault"
    writer = OverlayWriter(overlay_root, base_vault_root=vault_root)
    intent = _intent(target_path="resources/term_dictionary/term_n1.md")

    result = writer.materialize(intent, body="hi")

    overlay_file = overlay_root / intent.target_path
    vault_file = vault_root / intent.target_path
    assert overlay_file.exists()
    assert overlay_file.read_bytes() == b"hi"
    # GATE-3: the live vault is NEVER written.
    assert not vault_file.exists()
    assert not vault_root.exists()  # base vault dir was never even created.
    assert result.created is True
    assert result.content_hash == hashlib.sha256(b"hi").hexdigest()
    assert result.overlay_path == overlay_file.resolve()
    assert result.target_path == intent.target_path


def test_overlay_stub_body_deterministic(tmp_path) -> None:
    # No explicit body → deterministic stub from the typed intent.
    w1 = OverlayWriter(tmp_path / "o1")
    w2 = OverlayWriter(tmp_path / "o2")
    intent = _intent()
    r1 = w1.materialize(intent)
    r2 = w2.materialize(intent)
    assert r1.content_hash == r2.content_hash  # process-stable, no clock/random
    written = (tmp_path / "o1" / intent.target_path).read_text(encoding="utf-8")
    assert written.startswith("---\n")
    assert intent.thesis in written


def test_overlay_refuses_existing_in_overlay(tmp_path) -> None:
    overlay_root = tmp_path / "overlay"
    intent = _intent(target_path="a/existing.md")
    pre = overlay_root / intent.target_path
    pre.parent.mkdir(parents=True)
    pre.write_text("already here", encoding="utf-8")

    writer = OverlayWriter(overlay_root)
    with pytest.raises(OverlayError, match="already exists"):
        writer.materialize(intent, body="new")
    # GATE-4a: pre-existing content untouched.
    assert pre.read_text(encoding="utf-8") == "already here"


def test_overlay_refuses_existing_in_base_vault(tmp_path) -> None:
    overlay_root = tmp_path / "overlay"
    vault_root = tmp_path / "vault"
    intent = _intent(target_path="a/existing.md")
    base = vault_root / intent.target_path
    base.parent.mkdir(parents=True)
    base.write_text("live vault note", encoding="utf-8")

    writer = OverlayWriter(overlay_root, base_vault_root=vault_root)
    with pytest.raises(OverlayError, match="already exists"):
        writer.materialize(intent, body="new")
    # GATE-4b: overlay copy was NOT created; base vault untouched.
    assert not (overlay_root / intent.target_path).exists()
    assert base.read_text(encoding="utf-8") == "live vault note"


def test_overlay_rejects_path_escape(tmp_path) -> None:
    writer = OverlayWriter(tmp_path / "overlay")
    # relative .. escape.
    escape = _intent(target_path="../evil.md")
    with pytest.raises(OverlayError, match="escapes"):
        writer.materialize(escape, body="x")
    # absolute path.
    absolute = _intent(target_path="/etc/evil.md")
    with pytest.raises(OverlayError, match="relative"):
        writer.materialize(absolute, body="x")
    # nothing was written anywhere.
    assert not (tmp_path / "evil.md").exists()


def test_overlay_records_effect_for_rollback_parity(tmp_path) -> None:
    class _FakeJournal:
        def __init__(self) -> None:
            self.recorded: list = []
            self.postimages: list = []

        def __call__(self, path) -> None:
            self.recorded.append(path)

        def record_postimage(self, path, content) -> None:
            self.postimages.append((path, content))

    journal = _FakeJournal()
    overlay_root = tmp_path / "overlay"
    writer = OverlayWriter(overlay_root, effect_recorder=journal)
    intent = _intent(target_path="a/rec.md")

    result = writer.materialize(intent, body="hi")
    # VaultEffectJournal-style parity proven without importing runtime.
    assert journal.recorded == [result.overlay_path]
    assert journal.postimages == [(result.overlay_path, b"hi")]


def test_overlay_refuses_non_create_defense(tmp_path) -> None:
    # The model blocks non-create construction, so exercise the writer-level
    # guard via a minimal duck NoteIntent-like object.
    class _DuckIntent:
        disposition = "update"
        expected_preimage = None
        target_path = "a/x.md"
        thesis = "t"

    writer = OverlayWriter(tmp_path / "overlay")
    with pytest.raises(OverlayError, match="create-only"):
        writer.materialize(_DuckIntent())  # type: ignore[arg-type]
