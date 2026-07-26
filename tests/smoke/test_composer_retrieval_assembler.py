"""RetrievalAugmentedAssembler — wire the hybrid retrieval stack into the
composer's input seam (the 'graph-retrieval assembler' the module anticipated).

Covers: passthrough when no db, prepends a bounded related-notes block from a
real built index (hybrid seeds + best-first-BFS neighborhood), budget cap,
fail-soft on a missing/broken index, and that the default assemblers are
unaffected.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.composer.context_assembler import (
    ASSEMBLER_REGISTRY,
    RetrievalAugmentedAssembler,
    _fts5_safe_query,
    get_assembler,
)
from tessellum.indexer.build import build


def _vault(tmp_path: Path) -> Path:
    """A tiny vault: 3 linked notes so BFS has a neighborhood to expand."""
    v = tmp_path / "vault"
    (v / "0_entry_points").mkdir(parents=True)
    (v / "resources").mkdir()
    (v / "0_entry_points" / "entry_reversal.md").write_text(
        "---\ntitle: Reversal\ntags: [entry_point]\n---\n# Reversal scoring\n"
        "The RnR BSM BERT model scores the reversal domain. See "
        "[BSM model](../resources/note_bsm_model.md) and "
        "[Recall](../resources/note_recall.md).\n",
        encoding="utf-8",
    )
    (v / "resources" / "note_bsm_model.md").write_text(
        "---\ntitle: BSM model\ntags: [resource]\n---\n# BSM BERT model\n"
        "The model computes reversal abuse scores. "
        "Links [Recall](note_recall.md).\n",
        encoding="utf-8",
    )
    (v / "resources" / "note_recall.md").write_text(
        "---\ntitle: Recall\ntags: [resource]\n---\n# Recall at fixed FPR\n"
        "Recall is measured at a fixed false positive rate for the model.\n",
        encoding="utf-8",
    )
    return v


def _index(tmp_path: Path) -> Path:
    # BM25-only build (with_dense=False) so the test never needs the ML model;
    # hybrid still works — dense simply drops, BM25 carries the seeds. This is
    # exactly the degraded-dense fallback path, which must still retrieve.
    db = tmp_path / "idx.db"
    build(_vault(tmp_path), db, with_dense=False)
    return db


def test_registry_has_retrieval_strategy() -> None:
    assert ASSEMBLER_REGISTRY.get("retrieval") is RetrievalAugmentedAssembler


def test_passthrough_when_no_db() -> None:
    a = get_assembler("retrieval")  # no db_path
    out = a.assemble("some source text about reversal")
    assert out.text == "some source text about reversal"  # unchanged


def test_prepends_related_notes_block(tmp_path: Path) -> None:
    db = _index(tmp_path)
    a = RetrievalAugmentedAssembler(db_path=db, query="reversal scoring model")
    out = a.assemble("SOURCE: a new note about reversal scoring.")
    assert "Related vault notes" in out.text
    assert "reference only" in out.text.lower()
    # the source is still present, AFTER the block.
    assert out.text.rstrip().endswith("SOURCE: a new note about reversal scoring.")
    # at least one real note from the vault was retrieved.
    assert "note_bsm_model" in out.text or "note_recall" in out.text or "entry_reversal" in out.text


def test_bfs_neighborhood_expands_beyond_seeds(tmp_path: Path) -> None:
    db = _index(tmp_path)
    # seed only 1 hybrid hit but allow BFS neighbors → the block should contain
    # more than one note (the seed plus its graph neighbors).
    a = RetrievalAugmentedAssembler(db_path=db, query="reversal", seeds=1, neighbors=8)
    out = a.assemble("src")
    note_lines = [ln for ln in out.text.splitlines() if ln.startswith("- ")]
    assert len(note_lines) >= 2, "BFS should expand the seed's neighborhood"


def test_dedup_no_repeated_notes(tmp_path: Path) -> None:
    db = _index(tmp_path)
    a = RetrievalAugmentedAssembler(db_path=db, query="reversal model recall")
    out = a.assemble("src")
    note_lines = [ln for ln in out.text.splitlines() if ln.startswith("- ")]
    assert len(note_lines) == len(set(note_lines)), "no note repeated in the block"


def test_retrieval_block_capped_to_budget(tmp_path: Path) -> None:
    db = _index(tmp_path)
    # tiny max_chars → the block budget (fraction of it) is small; the whole
    # assembled output must still stay within max_chars (base class bound).
    a = RetrievalAugmentedAssembler(db_path=db, query="reversal", max_chars=200)
    out = a.assemble("S" * 500)
    assert len(out.text) <= 200


def test_source_first_block_never_evicts_source(tmp_path: Path) -> None:
    # Review-fix: the source is the record; a prepended related block must NEVER
    # push the source tail past the base truncation. With a large source that
    # alone fills max_chars, the block is dropped entirely (source preserved).
    db = _index(tmp_path)
    a = RetrievalAugmentedAssembler(db_path=db, query="reversal",
                                    max_chars=300, retrieval_fraction=0.25)
    src = "SOURCE_START " + "x" * 400 + " SOURCE_END"
    out = a.assemble(src)
    assert "SOURCE_START" in out.text  # source head kept
    assert "Related vault notes" not in out.text  # block dropped, not the source


def test_moderate_source_keeps_both_block_and_full_source(tmp_path: Path) -> None:
    db = _index(tmp_path)
    a = RetrievalAugmentedAssembler(db_path=db, query="reversal", max_chars=4000)
    out = a.assemble("SOURCE_START small note SOURCE_END")
    assert "Related vault notes" in out.text
    assert "SOURCE_END" in out.text  # full source preserved alongside the block


def test_fail_soft_on_missing_index(tmp_path: Path) -> None:
    # a db path that doesn't exist → retrieval raises internally → degrade to
    # the bare source, never crash.
    a = RetrievalAugmentedAssembler(db_path=tmp_path / "nonexistent.db",
                                    query="reversal")
    out = a.assemble("the original source text")
    assert out.text == "the original source text"


def test_source_only_strategies_ignore_db_kwargs(tmp_path: Path) -> None:
    # get_assembler passing db_path/query to a source-only strategy is a no-op
    # (existing callers that never set them are unaffected either way).
    a = get_assembler("windowed", db_path=tmp_path / "x.db", query="q")
    assert a.strategy == "windowed"
    assert a.assemble("plain source").text == "plain source"


def test_retrieval_fraction_must_be_in_unit_interval() -> None:
    with pytest.raises(ValueError):
        RetrievalAugmentedAssembler(retrieval_fraction=0.0)
    with pytest.raises(ValueError):
        RetrievalAugmentedAssembler(retrieval_fraction=1.0)


# ── Review-fix regressions ──────────────────────────────────────────────────


def test_fts5_safe_query_strips_frontmatter_and_punctuation() -> None:
    # Review-fix (HIGH): a raw note source begins with YAML `---`, headers `#`,
    # and `:` / `(` — all FTS5 syntax errors. The sanitizer must reduce it to
    # bare tokens (no operator chars) so MATCH never raises.
    raw = "---\ntitle: Reversal (RnR)\ntags: [entry_point]\n---\n# Reversal-scoring\n"
    q = _fts5_safe_query(raw)
    assert q  # non-empty
    for bad in ("-", ":", "#", "(", ")", "[", "]", "\n"):
        assert bad not in q
    assert "reversal" in q and "scoring" in q


def test_fts5_safe_query_empty_when_no_tokens() -> None:
    assert _fts5_safe_query("---:#()[]") == ""
    assert _fts5_safe_query(None) == ""  # type: ignore[arg-type]


def test_raw_source_head_query_actually_retrieves(tmp_path: Path) -> None:
    # Review-fix (HIGH): with NO injected query, the query defaults to the raw
    # source head, which begins with frontmatter. Before the fix that head hit
    # FTS5 MATCH verbatim and silently no-op'd. Now it's sanitized, so a real
    # source retrieves.
    db = _index(tmp_path)
    a = RetrievalAugmentedAssembler(db_path=db)  # no query → uses source head
    src = (
        "---\ntitle: New reversal note\ntags: [resource]\n---\n"
        "# Reversal scoring model\nThe reversal BSM model scores abuse.\n"
    )
    out = a.assemble(src)
    assert "Related vault notes" in out.text
    assert any(
        n in out.text for n in ("note_bsm_model", "note_recall", "entry_reversal")
    )


def test_warns_when_retrieval_finds_nothing(tmp_path: Path) -> None:
    # Review-fix (MEDIUM): a retrieval that yields nothing must surface a
    # fail-soft warning (not silently degrade to bare source).
    db = _index(tmp_path)
    a = RetrievalAugmentedAssembler(db_path=db, query="zzzznomatchxyzzy")
    out = a.assemble("some source")
    assert out.text == "some source"  # bare source
    assert any("retrieval degraded" in w for w in out.warnings)


def test_warns_on_missing_index(tmp_path: Path) -> None:
    # Review-fix (MEDIUM): a missing/broken index degrades AND warns.
    a = RetrievalAugmentedAssembler(db_path=tmp_path / "nope.db", query="reversal")
    out = a.assemble("source text")
    assert out.text == "source text"
    assert any("retrieval degraded" in w for w in out.warnings)


def test_block_dropped_whole_not_char_sliced(tmp_path: Path) -> None:
    # Review-fix (MEDIUM): when the block budget can't even hold the header +
    # one note line, the WHOLE block is dropped — the anti-fabrication
    # disclaimer is never char-sliced mid-string into the output.
    db = _index(tmp_path)
    # A source large enough that the block budget (fraction of max_chars) is
    # smaller than the disclaimer header itself.
    a = RetrievalAugmentedAssembler(
        db_path=db, query="reversal", max_chars=600, retrieval_fraction=0.05
    )
    out = a.assemble("s" * 100)
    # The disclaimer header must never appear PARTIALLY — either the full
    # "reference only, NOT the source of record" phrase or none of it.
    if "Related vault notes" in out.text:
        assert "NOT the source of record" in out.text
    else:
        assert "Related vault notes" not in out.text
        assert any("retrieval block dropped" in w for w in out.warnings)


def test_warns_when_source_fills_budget(tmp_path: Path) -> None:
    # Review-fix (MEDIUM): source alone at/over max_chars → block dropped +
    # a visible warning that the source was preserved.
    db = _index(tmp_path)
    a = RetrievalAugmentedAssembler(db_path=db, query="reversal", max_chars=300)
    out = a.assemble("SOURCE_START " + "x" * 400)
    assert "SOURCE_START" in out.text
    assert "Related vault notes" not in out.text
    assert any("source fills the char budget" in w for w in out.warnings)


def test_pending_warning_is_thread_local(tmp_path: Path) -> None:
    # E3 (G5) fix: a SINGLE assembler instance is shared by reference across the
    # concurrent execute wave. The per-call fail-soft warning must be thread-
    # local — a degrading call in one thread must NOT leak its warning onto a
    # succeeding call in another. Hammer one shared instance concurrently with a
    # mix of hitting and no-hit queries and assert each result's warnings match
    # ITS OWN outcome.
    import threading

    db = _index(tmp_path)
    shared = RetrievalAugmentedAssembler(db_path=db)  # ONE instance, no query
    barrier = threading.Barrier(8)
    errors: list[str] = []
    lock = threading.Lock()

    def worker(i: int) -> None:
        barrier.wait()  # maximize interleaving
        for _ in range(15):
            if i % 2 == 0:
                # a hitting query → block present, no degrade warning
                out = shared.assemble("reversal BSM model recall abuse scores")
                if "Related vault notes" not in out.text:
                    with lock:
                        errors.append(f"t{i}: expected block, warnings={out.warnings}")
                if any("retrieval degraded" in w for w in out.warnings):
                    with lock:
                        errors.append(f"t{i}: hit call got a degrade warning leak")
            else:
                # a no-hit query → no block, a degrade warning that must belong
                # to THIS call only
                out = shared.assemble("zzzznomatch quuxnonsense wibblewobble")
                if "Related vault notes" in out.text:
                    with lock:
                        errors.append(f"t{i}: unexpected block on no-hit query")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors, errors[:5]
