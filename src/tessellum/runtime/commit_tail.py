"""Idempotent completion tail: verify, index atomically, archive source."""

from __future__ import annotations

import os
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

from tessellum.indexer import build
from tessellum.runtime.admission import archive_source
from tessellum.runtime.locking import vault_write_lock
from tessellum.runtime.models import Job
from tessellum.runtime.paths import RuntimePaths


@dataclass(frozen=True)
class CommitResult:
    archive_path: Path
    index_path: Path


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


def rebuild_index_atomically(
    paths: RuntimePaths,
    *,
    with_dense: bool = False,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    lock_vault: bool = True,
) -> Path:
    target = paths.index_db
    target.parent.mkdir(parents=True, exist_ok=True)
    guard = effect_guard or nullcontext
    vault_guard = vault_write_lock(paths) if lock_vault else nullcontext()
    with vault_guard:
        with _index_publication_lock(target):
            temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
            try:
                build(paths.vault, temporary, with_dense=with_dense)
                with temporary.open("rb") as handle:
                    os.fsync(handle.fileno())
                with guard():
                    os.replace(temporary, target)
                    _fsync_dir(target.parent)
            finally:
                temporary.unlink(missing_ok=True)
    return target


def commit_job(
    job: Job,
    *,
    paths: RuntimePaths,
    rebuild_index: bool = True,
    with_dense: bool = False,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
    lock_vault: bool = True,
) -> CommitResult:
    index_path = paths.index_db
    if rebuild_index:
        index_path = rebuild_index_atomically(
            paths,
            with_dense=with_dense,
            effect_guard=effect_guard,
            lock_vault=lock_vault,
        )
    archive_path = archive_source(job, paths=paths, effect_guard=effect_guard)
    return CommitResult(archive_path=archive_path, index_path=index_path)
