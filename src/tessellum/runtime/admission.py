"""Filesystem admission: confinement, stable bytes, spool, then DB commit."""

from __future__ import annotations

import hashlib
import os
import shutil
import stat
import time
import uuid
from contextlib import nullcontext
from pathlib import Path
from typing import Callable, ContextManager

from tessellum.runtime.models import Job, WorkRequest
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.store import RuntimeStore


class AdmissionError(ValueError):
    pass


IGNORED_SUFFIXES = frozenset({".tmp", ".part", ".swp", ".crdownload"})


def _fsync_dir(path: Path) -> None:
    """Persist directory-entry changes where the platform supports it."""
    try:
        descriptor = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    except OSError:
        pass
    finally:
        os.close(descriptor)


def _ensure_directory_durable(path: Path) -> None:
    missing: list[Path] = []
    current = path
    while not current.exists():
        missing.append(current)
        current = current.parent
    for directory in reversed(missing):
        directory.mkdir(exist_ok=True)
        _fsync_dir(directory.parent)


def _confined(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _entry_exists(path: Path) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    return True


def _verify_spool_object(path: Path, expected_digest: str) -> None:
    """Verify one immutable content-addressed object without following links."""
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise AdmissionError(f"durable spool object is missing: {path}") from exc
    if not stat.S_ISREG(metadata.st_mode):
        raise AdmissionError(f"durable spool object is not a regular file: {path}")

    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise AdmissionError(f"cannot open durable spool object: {path}") from exc
    digest = hashlib.sha256()
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            raise AdmissionError(
                f"durable spool object is not a regular file: {path}"
            )
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    finally:
        os.close(descriptor)
    actual_digest = digest.hexdigest()
    if actual_digest != expected_digest:
        raise AdmissionError(
            f"durable spool digest mismatch: {actual_digest} != {expected_digest}"
        )


def is_eligible_source(path: Path, inbox_root: Path) -> bool:
    candidate = path.expanduser()
    try:
        if candidate.is_symlink():
            return False
        resolved = candidate.resolve(strict=True)
        root = inbox_root.expanduser().resolve(strict=True)
    except OSError:
        return False
    return (
        _confined(resolved, root)
        and resolved.is_file()
        and not resolved.name.startswith(".")
        and resolved.name != ".gitkeep"
        and resolved.suffix.lower() not in IGNORED_SUFFIXES
    )


def is_stable_file(path: Path, *, settle_seconds: float = 1.0) -> bool:
    before = path.stat()
    if settle_seconds > 0:
        time.sleep(settle_seconds)
    after = path.stat()
    return before.st_size == after.st_size and before.st_mtime_ns == after.st_mtime_ns


def admit_path(
    source_path: Path | str,
    *,
    paths: RuntimePaths,
    store: RuntimeStore,
    settle_seconds: float = 0.0,
    policy_profile: str | None = None,
    now: float | None = None,
) -> tuple[Job, bool]:
    candidate = Path(source_path).expanduser()
    if not is_eligible_source(candidate, paths.inbox):
        raise AdmissionError(f"ineligible inbox source: {candidate}")
    source = candidate.resolve(strict=True)
    before = source.stat()
    if settle_seconds > 0:
        time.sleep(settle_seconds)
    data = source.read_bytes()
    after = source.stat()
    before_identity = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )
    after_identity = (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    )
    if before_identity != after_identity or len(data) != after.st_size:
        raise AdmissionError(f"source is still changing: {source}")

    relative = source.relative_to(paths.inbox)
    if len(relative.parts) < 2:
        raise AdmissionError("source must be inside a named inbox lane")
    lane = relative.parts[0]
    digest = hashlib.sha256(data).hexdigest()
    payload_ref = f"sha256:{digest}"
    spool_path = paths.spool_path(payload_ref)
    _ensure_directory_durable(spool_path.parent)
    if _entry_exists(spool_path):
        _verify_spool_object(spool_path, digest)
    else:
        tmp = spool_path.with_name(
            f"{spool_path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
        )
        try:
            with tmp.open("xb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            _verify_spool_object(tmp, digest)
            os.replace(tmp, spool_path)
            _fsync_dir(spool_path.parent)
        finally:
            tmp.unlink(missing_ok=True)
        _verify_spool_object(spool_path, digest)

    request = WorkRequest(
        source="inbox",
        source_event_id=str(relative),
        intent="digest",
        payload_ref=payload_ref,
        original_path=str(source),
        lane=lane,
        source_device=after.st_dev,
        source_inode=after.st_ino,
        source_size=after.st_size,
        source_mtime_ns=after.st_mtime_ns,
        policy_profile=policy_profile or ("fast" if lane == "flash" else "default"),
    )
    job, created = store.admit(request, now=now)
    return job, created


def archive_source(
    job: Job,
    *,
    paths: RuntimePaths,
    effect_guard: Callable[[], ContextManager[None]] | None = None,
) -> Path:
    """Archive the admitted bytes and acknowledge only the same source.

    The content-addressed spool is authoritative for this job. A newer
    file that appears at ``original_path`` is never moved into the old
    job's archive and is left in the inbox for independent admission.
    """
    source = Path(job.request.original_path)
    spool = paths.spool_path(job.request.payload_ref)
    expected_digest = job.request.payload_ref.removeprefix("sha256:")
    _verify_spool_object(spool, expected_digest)
    target_dir = paths.archive / job.job_id / "source"
    _ensure_directory_durable(target_dir)
    target = target_dir / source.name
    guard = effect_guard or nullcontext

    target_matches = (
        target.is_file()
        and hashlib.sha256(target.read_bytes()).hexdigest() == expected_digest
    )
    temporary: Path | None = None
    if not target_matches:
        temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
        shutil.copy2(spool, temporary)
        with temporary.open("rb") as handle:
            os.fsync(handle.fileno())
        _verify_spool_object(temporary, expected_digest)

    expected_identity = None
    if all(
        value is not None
        for value in (
            job.request.source_device,
            job.request.source_inode,
            job.request.source_size,
            job.request.source_mtime_ns,
        )
    ):
        expected_identity = (
            job.request.source_device,
            job.request.source_inode,
            job.request.source_size,
            job.request.source_mtime_ns,
        )

    def acknowledge(quarantine: Path) -> None:
        stat = quarantine.stat()
        identity = (
            stat.st_dev,
            stat.st_ino,
            stat.st_size,
            stat.st_mtime_ns,
        )
        digest = hashlib.sha256(quarantine.read_bytes()).hexdigest()
        if digest == expected_digest and (
            expected_identity is None or identity == expected_identity
        ):
            quarantine.unlink()
            _fsync_dir(source.parent)
        elif not source.exists():
            os.replace(quarantine, source)
            _fsync_dir(source.parent)
        else:
            recovered = source.with_name(
                f"{source.stem}.recovered-{uuid.uuid4().hex}{source.suffix}"
            )
            os.replace(quarantine, recovered)
            _fsync_dir(source.parent)

    try:
        with guard():
            if temporary is not None:
                os.replace(temporary, target)
                temporary = None
                _fsync_dir(target.parent)

            # Replay a prior process that died after hiding this job's source.
            quarantine_prefix = f".{source.name}.{job.job_id}.ack-"
            for pending in sorted(source.parent.iterdir()):
                if not pending.name.startswith(quarantine_prefix):
                    continue
                if not pending.is_file() or pending.is_symlink():
                    raise AdmissionError(
                        f"invalid source acknowledgement quarantine: {pending}"
                    )
                acknowledge(pending)

            # Rename first so acknowledgement verifies the exact directory
            # entry it will remove, not a pathname that can be replaced
            # between stat() and unlink().
            quarantine = source.with_name(
                f".{source.name}.{job.job_id}.ack-{uuid.uuid4().hex}"
            )
            try:
                if source.is_file() and not source.is_symlink():
                    os.replace(source, quarantine)
                else:
                    quarantine = None
            except FileNotFoundError:
                quarantine = None

            if quarantine is not None:
                acknowledge(quarantine)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return target
