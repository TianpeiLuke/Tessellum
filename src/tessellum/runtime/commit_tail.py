"""Idempotent completion tail: verify, index atomically, archive source."""

from __future__ import annotations

import os
import shutil
import sqlite3
import threading
import uuid
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, ContextManager, Iterator

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback is thread-local
    fcntl = None  # type: ignore[assignment]

from tessellum.indexer import build, build_incremental
from tessellum.runtime.admission import archive_source
from tessellum.runtime.locking import vault_write_lock
from tessellum.runtime.models import Job
from tessellum.runtime.paths import RuntimePaths


@dataclass(frozen=True)
class CommitResult:
    archive_path: Path
    index_path: Path
    # True iff the index was rebuilt with_dense=True but dense embedding
    # generation failed, so the published index is BM25-only. Surfaced up to
    # the supervisor's completion detail so a degraded live index is visible
    # in job state, not silent. None when the index was not rebuilt.
    dense_degraded: bool | None = None


_INDEX_THREAD_LOCK = threading.Lock()


def _fsync_dir(path: Path) -> None:
    try:
        descriptor = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


@contextmanager
def _index_publication_lock(target: Path) -> Iterator[None]:
    """Serialize snapshot construction and publication across workers."""
    lock_path = target.with_name(f".{target.name}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with _INDEX_THREAD_LOCK:
        with lock_path.open("a+b") as handle:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                if fcntl is not None:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _sweep_stale_index_temps(target: Path) -> None:
    """Remove leftover ``.{target.name}.<hex>.tmp`` index copies from a prior
    build whose process was killed before its ``finally`` cleanup ran. Called
    under the publication lock (serializes builds), so no live temp is swept."""
    for stale in target.parent.glob(f".{target.name}.*.tmp"):
        try:
            stale.unlink()
        except OSError:  # pragma: no cover - best-effort GC, never fatal
            pass


def _assert_not_wal(db: Path) -> None:
    """Fail closed if the index DB is in WAL mode — ``shutil.copy2`` copies only
    the main file, so a WAL index's committed-but-not-checkpointed pages (in an
    uncopied ``-wal``) would yield a silently stale copy. The index is
    rollback-journal today; this guards a future regression."""
    try:
        with sqlite3.connect(str(db)) as probe:
            mode = probe.execute("PRAGMA journal_mode").fetchone()[0]
    except sqlite3.Error:  # pragma: no cover - a broken DB fails later anyway
        return
    if str(mode).lower() == "wal":
        raise RuntimeError(
            f"index DB {db} is WAL-mode; shutil.copy2 would drop its -wal "
            "sidecar and publish a stale copy. Use conn.backup() or "
            "checkpoint + copy all sidecars for a WAL index."
        )


def rebuild_index_atomically(
    paths: RuntimePaths,
    *,
    with_dense: bool = True,
    incremental: bool = True,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    lock_vault: bool = True,
) -> tuple[Path, bool]:
    """(Re)build + atomically publish the index.

    Builds into a private temp DB and publishes it with a single atomic
    ``os.replace`` onto the live ``index_db`` — the live index is never mutated
    in place, so a reader always sees a complete prior/next generation and a
    failed build leaves the live index untouched (FZ 20k9d3 P0).

    ``incremental`` (default True, FZ 20k9d3 P1): when a live index already
    exists, COPY it to the temp path and run :func:`build_incremental` on the
    copy — re-indexing only changed notes instead of the O(vault) full rebuild.
    The atomic-swap publish is identical either way. Falls back to a full
    :func:`build` when no live index exists (first commit) or ``incremental``
    is False (e.g. a schema change / corruption repair).

    Returns ``(index_path, dense_degraded)`` — ``dense_degraded`` is True iff
    ``with_dense=True`` was requested but embedding generation failed (BM25-only,
    fail-soft), surfaced so a degraded live index is visible, not silent.
    """
    target = paths.index_db
    target.parent.mkdir(parents=True, exist_ok=True)
    guard = effect_guard or nullcontext
    vault_guard = vault_write_lock(paths) if lock_vault else nullcontext()
    dense_degraded = False
    with vault_guard:
        with _index_publication_lock(target):
            # Sweep any stale temp copies left by a prior process killed
            # mid-build (the finally-unlink below cannot run on SIGKILL). Safe
            # under the publication lock, which serializes all builds — no
            # concurrent build holds an in-flight temp for this target.
            _sweep_stale_index_temps(target)
            temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
            try:
                if incremental and target.exists():
                    # Copy the live index into the temp, update the COPY
                    # incrementally, then atomically swap it in. The live index
                    # is never touched until the pointer-equivalent os.replace.
                    # copy2 copies ONLY the main DB file (no -wal/-shm); this is
                    # correct because the index is rollback-journal mode (build /
                    # build_incremental commit + close their conn before return,
                    # so a published index has no outstanding sidecar). Guard the
                    # invariant fail-closed — a future WAL switch would leave
                    # committed pages in an uncopied -wal → a silently stale copy.
                    _assert_not_wal(target)
                    shutil.copy2(target, temporary)
                    result = build_incremental(
                        paths.vault, temporary, with_dense=with_dense
                    )
                else:
                    result = build(paths.vault, temporary, with_dense=with_dense)
                dense_degraded = result.dense_degraded
                with temporary.open("rb") as handle:
                    os.fsync(handle.fileno())
                with guard():
                    os.replace(temporary, target)
                    _fsync_dir(target.parent)
            finally:
                temporary.unlink(missing_ok=True)
    return target, dense_degraded


def commit_job(
    job: Job,
    *,
    paths: RuntimePaths,
    rebuild_index: bool = True,
    with_dense: bool = True,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    lock_vault: bool = True,
) -> CommitResult:
    index_path = paths.index_db
    dense_degraded: bool | None = None
    if rebuild_index:
        index_path, dense_degraded = rebuild_index_atomically(
            paths,
            with_dense=with_dense,
            effect_guard=effect_guard,
            lock_vault=lock_vault,
        )
    archive_path = archive_source(job, paths=paths, effect_guard=effect_guard)
    return CommitResult(
        archive_path=archive_path,
        index_path=index_path,
        dense_degraded=dense_degraded,
    )
