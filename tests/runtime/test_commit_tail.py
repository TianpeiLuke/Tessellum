from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from tessellum.indexer.build import BuildResult
from tessellum.runtime.admission import AdmissionError, admit_path, archive_source
from tessellum.runtime.commit_tail import rebuild_index_atomically
from tessellum.runtime.locking import vault_write_lock
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.store import RuntimeStore
from tessellum.runtime.executor import VaultEffectJournal


def _paths(root: Path) -> RuntimePaths:
    paths = RuntimePaths.discover(root)
    paths.ensure_runtime_dirs()
    paths.inbox.mkdir(parents=True)
    (paths.inbox / "papers").mkdir()
    paths.vault.mkdir()
    return paths


def _fake_build_result(target: Path, *, dense_degraded: bool = False) -> BuildResult:
    """Minimal BuildResult for build() fakes (commit_tail now reads
    result.dense_degraded off the return value)."""
    return BuildResult(
        db_path=Path(target),
        notes_indexed=0,
        links_indexed=0,
        skipped_files=0,
        duration_seconds=0.0,
        dense_degraded=dense_degraded,
    )


def test_archive_uses_spool_and_preserves_replaced_source(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    source = paths.inbox / "papers" / "paper.md"
    source.write_text("admitted", encoding="utf-8")
    job, _ = admit_path(source, paths=paths, store=RuntimeStore.open(paths.db))

    source.write_text("new submission", encoding="utf-8")
    archived = archive_source(job, paths=paths)

    assert archived.read_text(encoding="utf-8") == "admitted"
    assert source.read_text(encoding="utf-8") == "new submission"
    assert hashlib.sha256(archived.read_bytes()).hexdigest() in job.request.payload_ref


def test_archive_rejects_corrupt_spool_before_source_acknowledgement(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    source = paths.inbox / "papers" / "paper.md"
    source.write_text("admitted", encoding="utf-8")
    job, _ = admit_path(source, paths=paths, store=RuntimeStore.open(paths.db))
    paths.spool_path(job.request.payload_ref).write_text(
        "corrupt",
        encoding="utf-8",
    )

    with pytest.raises(AdmissionError, match="spool digest mismatch"):
        archive_source(job, paths=paths)

    assert source.read_text(encoding="utf-8") == "admitted"


def test_archive_verifies_temporary_copy_before_publication(
    tmp_path: Path,
    monkeypatch,
) -> None:
    paths = _paths(tmp_path)
    source = paths.inbox / "papers" / "paper.md"
    source.write_text("admitted", encoding="utf-8")
    job, _ = admit_path(source, paths=paths, store=RuntimeStore.open(paths.db))

    def corrupt_copy(_source, target):
        Path(target).write_text("corrupt", encoding="utf-8")

    monkeypatch.setattr("tessellum.runtime.admission.shutil.copy2", corrupt_copy)
    with pytest.raises(AdmissionError, match="spool digest mismatch"):
        archive_source(job, paths=paths)

    target = paths.archive / job.job_id / "source" / source.name
    assert not target.exists()
    assert source.read_text(encoding="utf-8") == "admitted"


def test_index_rebuilds_are_serialized(
    tmp_path: Path,
    monkeypatch,
) -> None:
    paths = _paths(tmp_path)
    active = 0
    max_active = 0
    state_lock = threading.Lock()

    def fake_build(_vault, target, *, with_dense):
        nonlocal active, max_active
        with state_lock:
            active += 1
            max_active = max(max_active, active)
        time.sleep(0.03)
        Path(target).write_text(str(threading.get_ident()), encoding="utf-8")
        with state_lock:
            active -= 1
        return _fake_build_result(target)

    monkeypatch.setattr("tessellum.runtime.commit_tail.build", fake_build)
    # incremental=False: this test exercises the publication LOCK/serialization
    # with a full-build fake, not the incremental copy+update path.
    threads = [
        threading.Thread(
            target=rebuild_index_atomically, args=(paths,),
            kwargs={"incremental": False},
        )
        for _ in range(2)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert max_active == 1
    assert paths.index_db.is_file()


def test_standalone_and_supervised_index_rebuilds_do_not_deadlock(
    tmp_path: Path,
    monkeypatch,
) -> None:
    paths = _paths(tmp_path)

    def fake_build(_vault, target, *, with_dense):
        time.sleep(0.02)
        Path(target).write_text("index", encoding="utf-8")
        return _fake_build_result(target)

    monkeypatch.setattr("tessellum.runtime.commit_tail.build", fake_build)

    def supervised_rebuild() -> None:
        with vault_write_lock(paths):
            rebuild_index_atomically(paths, lock_vault=False, incremental=False)

    threads = [
        threading.Thread(
            target=rebuild_index_atomically, args=(paths,),
            kwargs={"incremental": False},
        ),
        threading.Thread(target=supervised_rebuild),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=2.0)

    assert all(not thread.is_alive() for thread in threads)
    assert paths.index_db.read_text(encoding="utf-8") == "index"


def test_rebuild_index_atomically_threads_dense_degraded(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """R1 review-fix: rebuild_index_atomically returns (path, dense_degraded)
    off the BuildResult so a degraded (BM25-only) live index is not silent."""
    paths = _paths(tmp_path)

    def fake_build(_vault, target, *, with_dense):
        Path(target).write_text("index", encoding="utf-8")
        return _fake_build_result(target, dense_degraded=True)

    monkeypatch.setattr("tessellum.runtime.commit_tail.build", fake_build)
    index_path, dense_degraded = rebuild_index_atomically(paths)
    assert index_path == paths.index_db
    assert dense_degraded is True


def test_commit_job_surfaces_dense_degraded(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """R1 review-fix: commit_job carries dense_degraded up to CommitResult so
    the supervisor can record it in the job's completion detail."""
    from tessellum.runtime.commit_tail import commit_job

    paths = _paths(tmp_path)

    def fake_build(_vault, target, *, with_dense):
        Path(target).write_text("index", encoding="utf-8")
        return _fake_build_result(target, dense_degraded=True)

    monkeypatch.setattr("tessellum.runtime.commit_tail.build", fake_build)
    # No real job/archive needed — stub archive_source to a no-op path.
    monkeypatch.setattr(
        "tessellum.runtime.commit_tail.archive_source",
        lambda job, *, paths, effect_guard=None: paths.artifacts,
    )
    result = commit_job(object(), paths=paths, rebuild_index=True)
    assert result.dense_degraded is True

    # When the index is NOT rebuilt, dense_degraded stays None (not applicable).
    result2 = commit_job(object(), paths=paths, rebuild_index=False)
    assert result2.dense_degraded is None


def test_stale_temp_index_copies_are_swept(tmp_path: Path, monkeypatch) -> None:
    """I3 review-fix: a .tmp index copy left by a killed process (finally never
    ran) is swept on the next rebuild, under the publication lock."""
    paths = _paths(tmp_path)

    def fake_build(_vault, target, *, with_dense):
        Path(target).write_text("index", encoding="utf-8")
        return _fake_build_result(target)

    monkeypatch.setattr("tessellum.runtime.commit_tail.build", fake_build)
    # simulate a leaked temp from a prior killed build
    leaked = paths.index_db.with_name(f".{paths.index_db.name}.deadbeef.tmp")
    leaked.parent.mkdir(parents=True, exist_ok=True)
    leaked.write_text("orphan", encoding="utf-8")
    assert leaked.exists()

    rebuild_index_atomically(paths, incremental=False)
    assert not leaked.exists(), "stale .tmp copy should be swept"
    assert paths.index_db.is_file()


def test_wal_index_is_rejected_by_copy_path(tmp_path: Path) -> None:
    """I3 review-fix: the incremental copy path fails closed on a WAL index
    (shutil.copy2 would drop the -wal sidecar → a silently stale copy)."""
    import sqlite3

    import pytest

    from tessellum.runtime.commit_tail import _assert_not_wal

    paths = _paths(tmp_path)
    db = paths.index_db
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("CREATE TABLE t (x)")
    conn.close()
    with pytest.raises(RuntimeError, match="WAL"):
        _assert_not_wal(db)


def test_non_wal_index_passes_guard(tmp_path: Path) -> None:
    import sqlite3

    from tessellum.runtime.commit_tail import _assert_not_wal

    paths = _paths(tmp_path)
    db = paths.index_db
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db))  # default rollback journal
    conn.execute("CREATE TABLE t (x)")
    conn.close()
    _assert_not_wal(db)  # must not raise


def test_vault_effect_journal_restores_overwrites_and_creations(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    existing = paths.vault / "existing.md"
    created = paths.vault / "created.md"
    existing.write_text("before", encoding="utf-8")
    journal = VaultEffectJournal(paths.vault, effect_guard=None)

    journal.record(existing)
    journal.record_postimage(existing, b"after")
    existing.write_text("after", encoding="utf-8")
    journal.record(created)
    journal.record_postimage(created, b"new")
    created.write_text("new", encoding="utf-8")
    journal.rollback()

    assert existing.read_text(encoding="utf-8") == "before"
    assert not created.exists()


def test_vault_effect_journal_rejects_directory_targets(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    directory = paths.vault / "existing"
    directory.mkdir()
    journal = VaultEffectJournal(paths.vault, effect_guard=None)

    with pytest.raises(ValueError, match="not a regular file"):
        journal.record(directory)


def test_durable_vault_effect_journal_recovers_after_process_loss(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    existing = paths.vault / "existing.md"
    created = paths.vault / "created.md"
    existing.write_text("before", encoding="utf-8")
    journal_dir = paths.artifacts / "job-1" / "vault-effects" / "1"
    journal = VaultEffectJournal(
        paths.vault,
        effect_guard=None,
        journal_dir=journal_dir,
    )

    journal.record(existing)
    journal.record_postimage(existing, b"after")
    existing.write_text("after", encoding="utf-8")
    journal.record(created)
    journal.record_postimage(created, b"new")
    created.write_text("new", encoding="utf-8")

    recovered = VaultEffectJournal.recover_pending(
        paths.vault,
        paths.artifacts,
    )

    assert recovered == 1
    assert existing.read_text(encoding="utf-8") == "before"
    assert not created.exists()
    assert not journal_dir.exists()


def test_durable_vault_effect_journal_accept_survives_cleanup_interruption(
    tmp_path: Path,
    monkeypatch,
) -> None:
    paths = _paths(tmp_path)
    existing = paths.vault / "existing.md"
    existing.write_text("before", encoding="utf-8")
    journal_dir = paths.artifacts / "job-1" / "vault-effects" / "1"
    journal = VaultEffectJournal(
        paths.vault,
        effect_guard=None,
        journal_dir=journal_dir,
    )
    journal.record(existing)
    journal.record_postimage(existing, b"accepted")
    existing.write_text("accepted", encoding="utf-8")
    monkeypatch.setattr(journal, "_cleanup", lambda: None)

    journal.accept()
    recovered = VaultEffectJournal.recover_pending(
        paths.vault,
        paths.artifacts,
    )

    assert recovered == 0
    assert existing.read_text(encoding="utf-8") == "accepted"
    assert not journal_dir.exists()


def test_durable_vault_effect_journal_survives_hard_process_exit(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    existing = paths.vault / "existing.md"
    existing.write_text("before", encoding="utf-8")
    journal_dir = paths.artifacts / "job-1" / "vault-effects" / "1"
    script = """
import os
import sys
from pathlib import Path
from tessellum.runtime.executor import VaultEffectJournal

root = Path(sys.argv[1])
journal_dir = Path(sys.argv[2])
target = root / "existing.md"
journal = VaultEffectJournal(
    root,
    effect_guard=None,
    journal_dir=journal_dir,
)
journal.record(target)
journal.record_postimage(target, b"partial")
target.write_text("partial", encoding="utf-8")
os._exit(23)
"""

    completed = subprocess.run(
        [sys.executable, "-c", script, str(paths.vault), str(journal_dir)],
        check=False,
    )
    assert completed.returncode == 23
    assert existing.read_text(encoding="utf-8") == "partial"

    assert VaultEffectJournal.recover_pending(paths.vault, paths.artifacts) == 1
    assert existing.read_text(encoding="utf-8") == "before"


def test_vault_effect_recovery_preserves_unknown_manual_edit(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    existing = paths.vault / "existing.md"
    existing.write_text("before", encoding="utf-8")
    journal_dir = paths.artifacts / "job-1" / "vault-effects" / "1"
    journal = VaultEffectJournal(
        paths.vault,
        effect_guard=None,
        journal_dir=journal_dir,
    )
    journal.record(existing)
    journal.record_postimage(existing, b"runtime output")
    existing.write_text("manual edit", encoding="utf-8")

    with pytest.raises(RuntimeError, match="current bytes are not journaled"):
        VaultEffectJournal.recover_pending(paths.vault, paths.artifacts)

    assert existing.read_text(encoding="utf-8") == "manual edit"
    assert journal_dir.is_dir()


def test_archive_replays_source_acknowledgement_quarantine(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    source = paths.inbox / "papers" / "paper.md"
    source.write_text("admitted", encoding="utf-8")
    job, _ = admit_path(source, paths=paths, store=RuntimeStore.open(paths.db))
    quarantine = source.with_name(
        f".{source.name}.{job.job_id}.ack-interrupted"
    )
    os.replace(source, quarantine)

    archived = archive_source(job, paths=paths)

    assert archived.read_text(encoding="utf-8") == "admitted"
    assert not source.exists()
    assert not quarantine.exists()


def test_archive_fsyncs_parent_after_quarantine_replay(
    tmp_path: Path,
    monkeypatch,
) -> None:
    paths = _paths(tmp_path)
    source = paths.inbox / "papers" / "paper.md"
    source.write_text("admitted", encoding="utf-8")
    job, _ = admit_path(source, paths=paths, store=RuntimeStore.open(paths.db))
    quarantine = source.with_name(
        f".{source.name}.{job.job_id}.ack-interrupted"
    )
    os.replace(source, quarantine)
    synced: list[Path] = []
    monkeypatch.setattr(
        "tessellum.runtime.admission._fsync_dir",
        lambda path: synced.append(path),
    )

    archive_source(job, paths=paths)

    assert source.parent in synced
    assert not quarantine.exists()
