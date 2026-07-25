"""tessellum.composer.publication — versioned publication + snapshot CAS.

P5 of the dynamic-digestion plan "Dynamic Digestion as a Snapshot-Pinned
Knowledge Transaction". This is the atomic reader-visible commit point the whole
transaction rests on — the plan's counter blocking-correction 3 replaced the
prior "one-visibility publication" *property* with a concrete protocol:

    PREPARED     immutable generation/{notes,index,capsule,evidence} fully
                 written + fsynced
    PUBLISHED    CAS-check the pinned base generation, then atomically replace
                 the CURRENT pointer
    ACKNOWLEDGED persist runtime completion and archive/acknowledge the source

Every reader pins ``CURRENT`` once and reads notes + index from that immutable
generation. Recovery treats the pointer switch as the authoritative commit
point: an unreferenced ``PREPARED`` generation is collectible; a ``PUBLISHED``-
but-unacknowledged generation completes idempotently. This replaces the shipped
NON-atomic publication (per-file ``os.replace`` edits + a separately swapped
index) whose intermediate states a raw reader could observe.

Snapshot CAS (A5.4) closes the shipped **lost-update** hazard: the base
generation the capsule planned against is re-checked immediately before the
pointer swap; a mismatch aborts the publish (the caller re-plans against the new
snapshot). Bounded retry with a terminal ``blocked`` outcome lives here.

Determinism: snapshot ids + generation ids are content hashes (no clock in the
hash). All writes are confined under the publication root; the CURRENT pointer
swap is a single atomic ``os.replace`` of a small pointer file.
"""

from __future__ import annotations

import contextlib
import hashlib
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Literal

try:  # POSIX advisory file lock for the publish critical section.
    import fcntl
except ImportError:  # pragma: no cover - non-POSIX
    fcntl = None  # type: ignore[assignment]

from tessellum.composer.materializer import (
    _atomic_write_bytes,
    _ensure_directory_durable,
    _fsync_dir,
)
from tessellum.composer.proposals import canonical_json_bytes
from tessellum.composer.write_closure import WriteClosure

ABSENT = "\0ABSENT\0"  # sentinel for a read-set path expected to NOT exist

# Control filenames the generation dir reserves at its ROOT — an agent write
# set may never occupy these (else its bytes would collide with a control
# marker and, worse, a stray root file named COMMITTED could mask an
# uncommitted orphan from recovery GC).
_RESERVED_ROOT_NAMES = frozenset({"COMMITTED", "ACKNOWLEDGED", "capsule.json"})


@dataclass(frozen=True)
class VaultSnapshot:
    """A pinned view of the base vault at planning time (A5.1).

    ``read_set`` maps each observed path → its content hash, or the ``ABSENT``
    sentinel for a path whose *absence* was relied on (phantom protection).
    ``candidate_query_hashes`` pin the dedup/candidate queries so a new
    near-duplicate appearing after planning trips the CAS."""

    base_generation: str
    index_hash: str
    read_set: dict[str, str] = field(default_factory=dict)
    candidate_query_hashes: tuple[str, ...] = ()

    @property
    def snapshot_id(self) -> str:
        payload = {
            "base_generation": self.base_generation,
            "index_hash": self.index_hash,
            "read_set": dict(sorted(self.read_set.items())),
            "candidate_query_hashes": sorted(self.candidate_query_hashes),
        }
        return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


@dataclass(frozen=True)
class KnowledgeCapsule:
    """A knowledge-specialized commit capsule (A5.2).

    Extends the P1 durable capsule identity with the transaction's provenance
    hashes and its exact write set. ``well_formed`` enforces the plan
    invariant ``staged_write_set == exact_write_closure(accepted_effects)`` —
    the capsule cannot promote a write set that is not its computed closure."""

    capsule_id: str
    source_bundle_hash: str
    vault_snapshot_id: str
    knowledge_plan_hash: str
    write_closure: WriteClosure
    preimage_hashes: dict[str, str] = field(default_factory=dict)
    postimage_hashes: dict[str, str] = field(default_factory=dict)

    def well_formed(self, expected_closure: WriteClosure) -> bool:
        """The staged write set must equal the exact computed closure."""
        return set(self.write_closure.writes) == set(expected_closure.writes)


class PublicationError(Exception):
    """Raised on a publication protocol violation (never a CAS conflict — that
    is a returned outcome, not an exception)."""


PublishOutcome = Literal["published", "cas_conflict", "blocked"]


@dataclass(frozen=True)
class PublishResult:
    outcome: PublishOutcome
    generation: str | None
    detail: str = ""


class VersionedVault:
    """A generation-versioned publication root with an atomic CURRENT pointer.

    Layout under ``root``::

        root/
          CURRENT                 -> a pointer file holding the live generation id
          generations/<gen>/      -> immutable published generation dir
          staging/<gen>/          -> a PREPARED (not-yet-published) generation

    Readers call :meth:`current_generation` ONCE and read from
    ``generations/<gen>/``. A publish writes the whole generation into staging,
    fsyncs it, CAS-checks the base, then atomically ``os.replace``s a temp
    pointer onto ``CURRENT`` — the single linearization point.
    """

    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self._current = self.root / "CURRENT"
        self._generations = self.root / "generations"
        self._staging = self.root / "staging"

    # ── layout / readers ────────────────────────────────────────────────────

    def initialize(self, genesis: str = "gen0") -> str:
        """Create the root with an empty genesis generation as CURRENT."""
        gdir = self._generations / genesis
        _ensure_directory_durable(gdir)
        _ensure_directory_durable(self._staging)
        _atomic_write_bytes(gdir / "COMMITTED", b"1")  # genesis is committed
        self._write_pointer(genesis)
        return genesis

    def current_generation(self) -> str | None:
        """The live generation id (read the pointer ONCE per reader). None if
        uninitialized."""
        if not self._current.is_file():
            return None
        return self._current.read_text(encoding="utf-8").strip()

    def generation_dir(self, generation: str) -> Path:
        return self._generations / generation

    def _write_pointer(self, generation: str) -> None:
        # atomic pointer swap: write temp then os.replace onto CURRENT.
        _ensure_directory_durable(self.root)
        _atomic_write_bytes(self._current, generation.encode("utf-8"))

    @contextlib.contextmanager
    def _publish_lock(self):
        """Exclusive advisory lock making compare + promote + pointer-swap a
        single critical section (so the CAS is a real atomic test-and-set, not a
        racy check-then-act). Best-effort on non-POSIX (no fcntl) — the shipped
        runtime publishes single-writer, but concurrent publishers are now
        mutually excluded on POSIX."""
        _ensure_directory_durable(self.root)
        lock_path = self.root / ".publish.lock"
        fh = open(lock_path, "w")
        try:
            if fcntl is not None:
                fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
            fh.close()

    # ── PREPARE → PUBLISH → ACKNOWLEDGE ──────────────────────────────────────

    def prepare(self, capsule: KnowledgeCapsule, files: dict[str, bytes]) -> str:
        """PREPARED: write the whole generation into staging + fsync it.

        The generation id is content-addressed over the capsule + its files, so
        re-preparing identical content is idempotent. Returns the generation id;
        no reader can see it yet (CURRENT is untouched)."""
        gen = self._generation_id(capsule, files)
        gdir = self._staging / gen
        _ensure_directory_durable(gdir)
        gdir_resolved = gdir.resolve()
        for rel, content in sorted(files.items()):
            target = (gdir / rel).resolve()
            # A file target must be strictly BELOW the generation dir — it may
            # never escape it AND may never resolve to the dir itself ('.', '',
            # 'a/..'), which would try to os.replace a file onto a directory.
            if not str(target).startswith(str(gdir_resolved) + os.sep):
                raise PublicationError(f"staged path escapes generation dir: {rel!r}")
            # reserve the control-marker namespace at the gen-dir root.
            if target.parent == gdir_resolved and target.name in _RESERVED_ROOT_NAMES:
                raise PublicationError(
                    f"staged path uses a reserved control filename: {rel!r}"
                )
            _ensure_directory_durable(target.parent)
            _atomic_write_bytes(target, content)
        # capsule record + evidence, so the generation is self-describing.
        _atomic_write_bytes(
            gdir / "capsule.json",
            canonical_json_bytes(self._capsule_payload(capsule)),
        )
        _fsync_dir(gdir)
        return gen

    def publish(
        self,
        generation: str,
        *,
        expected_current: str,
        cas_check: Callable[[], bool] | None = None,
    ) -> PublishResult:
        """PUBLISHED: CAS-check the base generation, then atomically swap CURRENT.

        ``expected_current`` is the generation the capsule planned against. If
        CURRENT has moved (another transaction published first), OR the optional
        ``cas_check()`` (a read-set re-validation) returns False, the publish
        aborts as ``cas_conflict`` WITHOUT touching CURRENT — the caller
        re-plans against the new snapshot. On success the staged generation is
        promoted into ``generations/`` and CURRENT is swapped in one
        ``os.replace``."""
        with self._publish_lock():
            live = self.current_generation()
            if live != expected_current:
                return PublishResult("cas_conflict", None,
                                     f"CURRENT moved {expected_current!r}->{live!r}")
            if cas_check is not None and not cas_check():
                return PublishResult("cas_conflict", None, "read-set CAS re-check failed")

            staged = self._staging / generation
            published = self._generations / generation
            if not staged.is_dir() and not published.exists():
                raise PublicationError(
                    f"cannot publish unprepared generation: {generation}"
                )
            if not published.exists():
                # promote staging -> generations (atomic dir rename on same fs).
                _ensure_directory_durable(self._generations)
                os.replace(staged, published)
                _fsync_dir(self._generations)
            elif staged.is_dir():
                # a redundant staging copy (crash-recovered re-prepare, or a
                # promote whose pointer swap did not land): drop it so it never
                # leaks. The published generation is the durable copy.
                _rmtree(staged)
                _fsync_dir(self._staging)
            # Mark the generation COMMITTED *before* the pointer swap: a crash
            # after the marker but before the swap leaves a committed-marked but
            # not-CURRENT generation — recover() will keep it (harmless), while
            # an unmarked promoted dir (crash before the marker) is GC'd as an
            # orphan. Either way no committed generation is ever collected.
            _atomic_write_bytes(published / "COMMITTED", b"1")
            # THE linearization point: atomically move CURRENT to the new gen.
            self._write_pointer(generation)
            return PublishResult("published", generation)

    def acknowledge(self, generation: str) -> None:
        """ACKNOWLEDGED: mark the generation's transaction complete (idempotent).

        A PUBLISHED-but-unacknowledged generation is completed idempotently on
        recovery: acknowledging an already-acknowledged generation is a no-op."""
        gdir = self._generations / generation
        if not gdir.is_dir():
            raise PublicationError(f"cannot acknowledge unpublished generation: {generation}")
        ack = gdir / "ACKNOWLEDGED"
        if not ack.is_file():
            _atomic_write_bytes(ack, b"1")

    def is_acknowledged(self, generation: str) -> bool:
        return (self._generations / generation / "ACKNOWLEDGED").is_file()

    # ── recovery / GC ────────────────────────────────────────────────────────

    def recover(self, *, genesis_keep: set[str] | None = None) -> str | None:
        """Recovery = the pointer switch is the commit point.

        - A PUBLISHED generation (== CURRENT) that is not yet ACKNOWLEDGED is
          completed idempotently (its transaction finished at the pointer swap).
        - Unreferenced PREPARED generations in staging are collectible (they
          never reached the commit point).
        - An ORPHAN generation in ``generations/`` — one that is neither CURRENT
          nor an ancestor of it and carries no ACKNOWLEDGED marker — is a
          promote that crashed before its pointer swap; it never committed, so
          it is collected (closing the crash-between-promote-and-swap leak).
        ``genesis_keep`` protects generations that legitimately precede CURRENT
        (e.g. the genesis) from orphan GC. Returns the live generation.

        Runs under the publish lock so recovery cannot race a concurrent
        publisher's promote-before-marker window (where orphan GC would otherwise
        reclaim a generation mid-commit). Recovery is still a restart-time
        single-actor operation by design; the lock is defence in depth."""
        with self._publish_lock():
            live = self.current_generation()
            if live is not None and (self._generations / live).is_dir():
                self.acknowledge(live)
            self.collect_staging()
            self.collect_orphan_generations(keep=genesis_keep)
            return live

    def collect_orphan_generations(self, keep: set[str] | None = None) -> list[str]:
        """Delete uncommitted orphan generations in ``generations/`` — a
        promoted dir that never became CURRENT and was never acknowledged (its
        pointer swap crashed). NEVER deletes CURRENT or an acknowledged/kept
        generation. Returns the collected ids."""
        keep = set(keep or set())
        live = self.current_generation()
        if live is not None:
            keep.add(live)
        collected: list[str] = []
        if not self._generations.is_dir():
            return collected
        for child in sorted(self._generations.iterdir()):
            if not child.is_dir() or child.name in keep:
                continue
            # A COMMITTED marker means the generation reached (or passed) the
            # commit point — keep it (superseded-but-committed generations may
            # still be read). Only an UNMARKED promoted dir is a crashed-promote
            # orphan that never committed.
            if (child / "COMMITTED").is_file():
                continue
            _rmtree(child)
            collected.append(child.name)
        _fsync_dir(self._generations)
        return collected

    def collect_staging(self, keep: set[str] | None = None) -> list[str]:
        """Delete unreferenced PREPARED (staged) generations. Never touches a
        published generation or CURRENT. Returns the collected ids."""
        keep = keep or set()
        live = self.current_generation()
        collected: list[str] = []
        if not self._staging.is_dir():
            return collected
        for child in sorted(self._staging.iterdir()):
            if not child.is_dir():
                continue
            if child.name == live or child.name in keep:
                continue
            # only collect if it was never promoted to generations/.
            if (self._generations / child.name).exists():
                continue
            _rmtree(child)
            collected.append(child.name)
        _fsync_dir(self._staging)
        return collected

    # ── ids / payloads ───────────────────────────────────────────────────────

    def _generation_id(self, capsule: KnowledgeCapsule, files: dict[str, bytes]) -> str:
        file_hashes = {
            rel: hashlib.sha256(content).hexdigest()
            for rel, content in files.items()
        }
        payload = {
            "capsule": self._capsule_payload(capsule),
            "files": dict(sorted(file_hashes.items())),
        }
        return "gen_" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()[:32]

    @staticmethod
    def _capsule_payload(capsule: KnowledgeCapsule) -> dict:
        return {
            "capsule_id": capsule.capsule_id,
            "source_bundle_hash": capsule.source_bundle_hash,
            "vault_snapshot_id": capsule.vault_snapshot_id,
            "knowledge_plan_hash": capsule.knowledge_plan_hash,
            "writes": sorted(
                (w.note_id, w.kind, w.origin) for w in capsule.write_closure.writes
            ),
            "preimage_hashes": dict(sorted(capsule.preimage_hashes.items())),
            "postimage_hashes": dict(sorted(capsule.postimage_hashes.items())),
        }


def read_set_matches(snapshot: VaultSnapshot, current: dict[str, str | None]) -> bool:
    """A5.4 CAS predicate: True iff every read-set expectation still holds.

    ``current`` maps a path → its current content hash (or None if absent). A
    path pinned to a hash must still hash the same; a path pinned ABSENT must
    still be absent (phantom protection)."""
    for path, expected in snapshot.read_set.items():
        actual = current.get(path)
        if expected == ABSENT:
            if actual is not None:
                return False  # a phantom appeared
        elif actual != expected:
            return False  # a concurrent mutation (lost-update hazard)
    return True


@dataclass
class RetryPolicy:
    max_attempts: int = 3


def publish_with_cas(
    vault: VersionedVault,
    generation: str,
    *,
    expected_current: str,
    snapshot: VaultSnapshot,
    read_current: Callable[[], dict],
    replan: Callable[[], tuple | None],
    policy: RetryPolicy | None = None,
) -> PublishResult:
    """Bounded CAS-retry publish (A5.4). On a CAS conflict, ``replan()`` must
    return a fresh ``(generation, expected_current, snapshot)`` or None to give
    up; after ``max_attempts`` conflicts the outcome is terminal ``blocked``
    (never a livelock)."""
    policy = policy or RetryPolicy()
    gen, exp, snap = generation, expected_current, snapshot
    for _attempt in range(policy.max_attempts):
        result = vault.publish(
            gen,
            expected_current=exp,
            cas_check=lambda: read_set_matches(snap, read_current()),
        )
        if result.outcome != "cas_conflict":
            return result
        nxt = replan()
        if nxt is None:
            return PublishResult("blocked", None, "re-plan declined after CAS conflict")
        gen, exp, snap = nxt
    return PublishResult("blocked", None, "max CAS attempts exhausted")


def _rmtree(path: Path) -> None:
    for child in sorted(path.iterdir()):
        if child.is_dir():
            _rmtree(child)
        else:
            child.unlink(missing_ok=True)
    path.rmdir()


__all__ = [
    "ABSENT",
    "VaultSnapshot",
    "KnowledgeCapsule",
    "VersionedVault",
    "PublicationError",
    "PublishResult",
    "PublishOutcome",
    "RetryPolicy",
    "read_set_matches",
    "publish_with_cas",
]
