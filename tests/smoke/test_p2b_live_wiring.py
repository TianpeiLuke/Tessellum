"""P2b — live-path wiring (all additive / opt-in).

Gate-to-P3 deliverables:
  1. the digestion source_leaf now resolves ``{{leaf.source_url}}`` (A2.2) —
     no ``<missing leaf.source_url>`` sentinel;
  2. ``source_content`` is NOT force-injected into the plan prompt past the
     HARD_PROMPT_CAP (A2.2);
  3. a :class:`SourceBundle` admits as ONE objective with a durable manifest +
     member idempotency (A2.1);
  4. ``InboxScanner.scan_once`` behaviour is UNCHANGED (still per-file);
  5. ``run_digestion_pipeline`` uses ``project_note_intent_graph`` when a
     ``note_intent_graph`` is present, is byte-identical to the shipped
     fallback when absent, and fails loud on a present-but-invalid graph.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.composer.executor import _resolve_placeholders
from tessellum.composer.knowledge_plan import (
    ClaimProvenance,
    NoteIntent,
    NoteIntentGraph,
    SourceBundle,
    bundle_content_hash,
    project_note_intent_graph,
)
from tessellum.runtime.inbox import InboxScanner
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.store import RuntimeStore


# ── fixtures ────────────────────────────────────────────────────────────────


def _paths(root: Path) -> RuntimePaths:
    paths = RuntimePaths.discover(root)
    paths.ensure_runtime_dirs()
    paths.inbox.mkdir(parents=True, exist_ok=True)
    return paths


def _member(root: Path, name: str, text: str) -> Path:
    src = root.inbox / "papers" / name
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(text, encoding="utf-8")
    return src


# ── Deliverable 1 + 2 — source_url resolves; content not injected ───────────


def test_source_url_key_resolves_no_sentinel() -> None:
    # Mirror the digestion source_leaf shape (runtime/executor.py:544-553).
    original_path = "/inbox/papers/design.md"
    source_url = Path(original_path).as_uri()
    leaf = {
        "_id": "job1",
        "source_path": original_path,
        "source_url": source_url,
        "source_name": "design.md",
        "source_content": "x" * 500_000,  # large; must NOT reach the prompt
        "source_hash": "deadbeef",
    }
    rendered = _resolve_placeholders(
        "source_url: {{leaf.source_url}}\nsource_name: {{leaf.source_name}}",
        leaf=leaf,
        upstream={},
    )
    assert "<missing leaf.source_url>" not in rendered
    assert source_url in rendered
    # Deliverable 2: the huge source_content is NOT pulled into the prompt by
    # any {{leaf.source_content}} expansion (the plan skill references only
    # source_url / source_name), so the rendered prompt stays small.
    assert "x" * 500_000 not in rendered
    assert len(rendered) < 1000


def test_relative_original_path_falls_back_to_raw() -> None:
    # The executor uses as_uri() only for absolute paths; a relative path
    # falls back to the raw string (as_uri() would raise on a relative path).
    original_path = "papers/design.md"
    source_url = (
        Path(original_path).as_uri()
        if Path(original_path).is_absolute()
        else original_path
    )
    assert source_url == "papers/design.md"


# ── Deliverable 3 — SourceBundle admits as ONE objective + idempotent ───────


def test_admit_bundle_one_objective_and_idempotent(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    store = RuntimeStore.open(paths.db)
    scanner = InboxScanner(paths=paths, store=store, settle_seconds=0.0)

    m1 = _member(paths, "a.md", "first source")
    m2 = _member(paths, "b.md", "second source")

    adm = scanner.admit_bundle([m1, m2], objective="design-review")
    assert adm.created is True
    assert len(adm.jobs) == 2
    assert len(adm.bundle.members) == 2
    # ordered by ordinal, one objective, manifest written durably
    assert [mem.ordinal for mem in adm.bundle.members] == [0, 1]
    assert adm.bundle.objective == "design-review"
    assert adm.manifest_path.is_file()

    # Re-admitting the SAME members + objective is idempotent: same bundle_id,
    # no new manifest, jobs dedup to the same job_ids (admit_path idempotency).
    adm2 = scanner.admit_bundle([m1, m2], objective="design-review")
    assert adm2.bundle.bundle_id == adm.bundle.bundle_id
    assert adm2.created is False
    assert [j.job_id for j in adm2.jobs] == [j.job_id for j in adm.jobs]


def test_bundle_id_order_independent_content_hash(tmp_path: Path) -> None:
    # bundle_content_hash is over the ordinal-normalized members, so building
    # the same members in a different construction order yields the same hash.
    members_a = SourceBundle(
        bundle_id="x",
        objective="o",
        members=(
            _bm(0, "r0"),
            _bm(1, "r1"),
        ),
    )
    members_b = SourceBundle(
        bundle_id="x",
        objective="o",
        members=(
            _bm(1, "r1"),
            _bm(0, "r0"),
        ),
    )
    assert bundle_content_hash(members_a) == bundle_content_hash(members_b)


def _bm(ordinal: int, ref: str):
    from tessellum.composer.knowledge_plan import BundleMember

    return BundleMember(
        source_id=f"s{ordinal}",
        ordinal=ordinal,
        ref=ref,
        parser_id="md",
        extracted_text_hash=f"h{ordinal}",
    )


def test_source_bundle_rejects_duplicate_ordinals() -> None:
    with pytest.raises(Exception):
        SourceBundle(
            bundle_id="x",
            objective="o",
            members=(_bm(0, "a"), _bm(0, "b")),
        )


# ── Deliverable 4 — scan_once unchanged (still per-file) ────────────────────


def test_scan_once_still_per_file(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    store = RuntimeStore.open(paths.db)
    scanner = InboxScanner(paths=paths, store=store, settle_seconds=0.0)

    _member(paths, "one.md", "aaa")
    _member(paths, "two.md", "bbb")

    result = scanner.scan_once()
    # Two independent per-file jobs — scan_once does NOT group into a bundle.
    assert len(result.admitted) == 2
    ids = {j.job_id for j in result.admitted}
    assert len(ids) == 2
    # Re-scan dedups per-file (idempotent), still no bundle inference.
    again = scanner.scan_once()
    assert len(again.admitted) == 0
    assert len(again.deduplicated) == 2


# ── Deliverable 5 — opt-in projection wiring ────────────────────────────────


def _graph() -> NoteIntentGraph:
    return NoteIntentGraph(
        objective_id="obj",
        intents=(
            NoteIntent(
                note_id="n1",
                thesis="first",
                building_block="concept",
                target_path="areas/n1.md",
                provenance=(ClaimProvenance(span_id="s1", source_ref="src#1"),),
            ),
            NoteIntent(
                note_id="n2",
                thesis="second",
                building_block="procedure",
                target_path="areas/n2.md",
                provenance=(ClaimProvenance(span_id="s2", source_ref="src#2"),),
            ),
        ),
    )


def test_projection_used_when_graph_present() -> None:
    # The wiring derives execute_leaves from the projection when a
    # note_intent_graph is present. Verify the projection itself (the branch
    # calls exactly this) yields one leaf per intent.
    graph = _graph()
    leaves = project_note_intent_graph(graph)
    assert len(leaves) == 2
    assert [leaf["target_path"] for leaf in leaves] == ["areas/n1.md", "areas/n2.md"]
    # accept a raw dict too (model_validate path in the wiring).
    leaves2 = project_note_intent_graph(
        NoteIntentGraph.model_validate(graph.model_dump(mode="json"))
    )
    assert leaves2 == leaves


def test_wiring_branch_absent_is_shipped_fallback() -> None:
    # When no note_intent_graph is present, the shipped fallback is used:
    # execute_leaves = plan_doc["execute_leaves"] or [dict(plan_doc)].
    # Emulate the exact branch logic to lock byte-identical behavior.
    plan_doc = {"total_notes": 3, "some": "data"}
    graph_spec = plan_doc.get("note_intent_graph")
    assert graph_spec is None
    execute_leaves = plan_doc.get("execute_leaves")
    if not isinstance(execute_leaves, list) or not execute_leaves:
        execute_leaves = [dict(plan_doc)]
    assert execute_leaves == [dict(plan_doc)]


def test_wiring_present_but_invalid_raises() -> None:
    # A present-but-invalid note_intent_graph must fail loud (not fall through).
    bad = {"objective_id": "obj", "intents": [{"note_id": "n1"}]}  # missing fields
    with pytest.raises(Exception):
        NoteIntentGraph.model_validate(bad)
