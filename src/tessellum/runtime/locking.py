"""Cross-process serialization for live-vault write transactions."""

from __future__ import annotations

import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback is process-local
    fcntl = None  # type: ignore[assignment]

from tessellum.runtime.paths import RuntimePaths


_THREAD_LOCK = threading.RLock()


@contextmanager
def vault_write_lock(paths: RuntimePaths) -> Iterator[None]:
    """Exclude other runtime jobs and index snapshots from the live vault."""
    lock_path = Path(paths.db).parent / ".vault-write.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with _THREAD_LOCK:
        with lock_path.open("a+b") as handle:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                if fcntl is not None:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
