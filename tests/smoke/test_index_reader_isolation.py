"""FZ 20k9d3 P0 — hazard-bounding: a reader during a live index rebuild sees a
CONSISTENT prior-committed index, never a half-written / missing one.

This test PROVES the torn-read hazard the (deferred) VersionedVault targets is
already bounded on the single-host runtime path: the index is published by one
atomic ``os.replace`` of the whole DB file (commit_tail.rebuild_index_atomically),
so a reader holding a query either sees the entire prior generation or the entire
new one — never an intermediate state. It gates whether generation-layout surgery
is warranted (it is not, while readers read the atomically-swapped index).
"""

from __future__ import annotations

import threading
from pathlib import Path

from tessellum.indexer.build import build
from tessellum.retrieval.bm25 import bm25_search
from tessellum.runtime.commit_tail import rebuild_index_atomically
from tessellum.runtime.paths import RuntimePaths


def test_reader_sees_consistent_index_across_atomic_swap(tmp_path: Path) -> None:
    paths = RuntimePaths.discover(tmp_path)
    paths.ensure_runtime_dirs()
    (paths.vault).mkdir(parents=True, exist_ok=True)
    (paths.vault / "resources").mkdir(parents=True, exist_ok=True)
    (paths.vault / "resources" / "note_alpha.md").write_text(
        "---\ntitle: Alpha\ntags: [resource]\n---\n# Alpha\n"
        "reversal abuse scoring model recall\n",
        encoding="utf-8",
    )

    # Publish an initial index (BM25-only: no ML model needed).
    idx = paths.index_db
    build(paths.vault, idx, force=True, with_dense=False)
    assert idx.is_file()

    errors: list[str] = []
    stop = threading.Event()

    def reader() -> None:
        # Hammer the index while it is being rebuilt+swapped underneath us.
        while not stop.is_set():
            try:
                hits = bm25_search(idx, "reversal", k=5)
            except Exception as e:  # noqa: BLE001 — any torn/missing read is a failure
                errors.append(f"reader saw a broken index: {type(e).__name__}: {e}")
                return
            # A consistent index always answers this query (the note is present
            # in every committed generation) — an empty result would mean the
            # reader observed a half-published / missing index.
            if not hits:
                errors.append("reader saw an empty/partial index mid-swap")
                return

    t = threading.Thread(target=reader, daemon=True)
    t.start()
    try:
        # Repeatedly rebuild + atomically republish the index under the reader.
        for _ in range(8):
            rebuild_index_atomically(paths, with_dense=False)
    finally:
        stop.set()
        t.join(timeout=5.0)

    assert not errors, errors[:3]
    assert not t.is_alive()


def test_atomic_swap_never_leaves_a_missing_db(tmp_path: Path) -> None:
    # Narrower invariant: the index file exists + is queryable at EVERY moment
    # around a rebuild — the swap is atomic (os.replace), never unlink-then-write.
    paths = RuntimePaths.discover(tmp_path)
    paths.ensure_runtime_dirs()
    (paths.vault / "resources").mkdir(parents=True, exist_ok=True)
    (paths.vault / "resources" / "note_alpha.md").write_text(
        "---\ntitle: Alpha\ntags: [resource]\n---\n# Alpha\nreversal model\n",
        encoding="utf-8",
    )
    idx = paths.index_db
    build(paths.vault, idx, force=True, with_dense=False)

    seen_missing = []
    stop = threading.Event()

    def watcher() -> None:
        while not stop.is_set():
            if not idx.is_file():
                seen_missing.append(True)
                return

    w = threading.Thread(target=watcher, daemon=True)
    w.start()
    try:
        for _ in range(8):
            rebuild_index_atomically(paths, with_dense=False)
    finally:
        stop.set()
        w.join(timeout=5.0)

    assert not seen_missing, "index file was momentarily missing during a rebuild"
