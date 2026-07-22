"""Resume manifest — durable, atomically-written, rebuildable projection.

Composer v4, Phase 1 (items 1.1 + 1.2 + 1.3). The manifest is the
per-leaf, per-attempt bookkeeping ledger that lets a multi-worker run
resume after a crash *at leaf granularity* — a strict superset of the
Wave-5a batch resume, which is all-or-nothing per *job* (see
``tessellum.composer.batch``).

Design invariants (from the v4 identity gates):

- **IDENT-2 (vault is source of truth).** The manifest is a *rebuildable
  projection*, never authoritative. :func:`Manifest.rebuild_from_vault`
  reconstructs done-status purely from which target note files exist on
  disk, so a lost/corrupt manifest is always recoverable from the vault.
- **IDENT-3 (programs decide).** All state transitions here are pure
  program logic. No LLM is consulted; the manifest only records what the
  executor/scheduler already decided.
- **IDENT-5 (fail-closed).** A corrupt manifest never silently loads
  garbage: :meth:`Manifest.load` integrity-checks the JSON shape and
  falls back to the newest good ``.bak``; if none is good it starts
  empty *with a logged warning* rather than pretending the file was fine.

Three mechanisms, one file:

1. **Delta-patch by id (1.1).** Callers mutate *one* entry at a time
   (:meth:`Manifest.upsert_entry`, :meth:`~Manifest.add_attempt`,
   :meth:`~Manifest.mark_done`, :meth:`~Manifest.mark_blocked`,
   :meth:`~Manifest.mark_in_progress`). Callers MUST NOT rebuild the
   whole ``entries`` dict wholesale — that races other workers' patches.

2. **Atomic write + rotation (1.2 / 1.3).** :meth:`Manifest.save`
   serializes to a temp file (``fsync`` + :func:`os.replace`, never an
   in-place write) and rotates the prior version through
   ``.bak`` → ``.bak.1`` → ``.bak.2`` (last three kept).
   :meth:`Manifest.load` sweeps orphaned ``.tmp`` files left by crashed
   writers.

3. **Owner-scoped reclaim + atomic claim (1.2).** ``in_progress`` rows
   carry the owning ``run_id`` (a uuid the caller passes in) plus a
   ``heartbeat`` float timestamp. :meth:`~Manifest.reclaim_stale`
   requeues only *foreign*, *stale* rows; :meth:`~Manifest.claim` is a
   compare-and-swap acquire that succeeds only when a leaf is
   pending/absent. Double-dispatch is prevented by the discipline that a
   worker :meth:`~Manifest.mark_done` (the durable-commit step) *before*
   releasing its claim — see :meth:`Manifest.mark_done`.

Timestamps are always passed in by the caller (``now: float``) rather
than read from the clock here, so the transition logic stays
deterministic and unit-testable.
"""

from __future__ import annotations

import dataclasses
import json
import logging
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping

logger = logging.getLogger(__name__)


MANIFEST_VERSION: str = "1.0"
"""On-disk schema version. Bumped only on a breaking payload change."""


VALID_STATUSES: frozenset[str] = frozenset(
    {"pending", "in_progress", "done", "blocked"}
)
"""The four leaf lifecycle states.

- ``pending`` — not yet claimed (the initial and reclaimed state).
- ``in_progress`` — claimed by ``run_id``; ``heartbeat`` proves liveness.
- ``done`` — durably completed (the target note exists). Terminal.
- ``blocked`` — cannot proceed until ``blocked_by`` leaves finish. Terminal
  for this run's purposes; a later run may unblock and re-mark it pending.
"""


class ManifestError(Exception):
    """Raised on invalid manifest mutations — e.g. an unknown status."""


@dataclass(frozen=True)
class AttemptRecord:
    """One execution attempt against a leaf.

    Attributes:
        attempt_n: 1-indexed attempt number, matching
            :attr:`tessellum.composer.executor.StepResult.attempts`.
        outcome: The attempt's terminal kind — mirrors the executor's
            ``retry_kind_history`` vocabulary (``"success"``, ``"logic"``,
            ``"crash"``, or ``"stall"``). Free-form so future kinds don't
            require a schema bump.
        cost: Best-effort cost signal for the attempt (tokens, dollars,
            or wall-seconds — the caller's choice). ``0.0`` when unknown.
        gates_failed: Names of the validation gates the attempt tripped
            (empty on success). Kept as a tuple so the record is hashable
            and cannot be mutated after the fact.
        at: Wall-clock timestamp (epoch seconds) the attempt finished.
            Passed in by the caller for determinism.
    """

    attempt_n: int
    outcome: str
    cost: float = 0.0
    gates_failed: tuple[str, ...] = ()
    at: float = 0.0


@dataclass(frozen=True)
class ManifestEntry:
    """The durable state of a single leaf.

    Frozen: every mutation goes through :class:`Manifest`'s delta-patch
    methods, which replace *this one entry* under its ``leaf_id`` key.
    That keeps concurrent patches from clobbering unrelated rows.

    Attributes:
        leaf_id: Stable identifier for the leaf (the scheduler's ``_id``).
        status: One of :data:`VALID_STATUSES`.
        attempts: Per-attempt history, oldest first.
        blocked_by: Leaf ids this entry is waiting on (only meaningful
            when ``status == "blocked"``).
        run_id: The uuid of the run that currently owns an ``in_progress``
            entry (or last owned a terminal one). ``None`` when pending.
        heartbeat: Epoch-seconds timestamp of the owner's last liveness
            beat while ``in_progress``. ``None`` when not owned. Used by
            :meth:`Manifest.reclaim_stale` to detect abandoned rows.
    """

    leaf_id: str
    status: str = "pending"
    attempts: tuple[AttemptRecord, ...] = ()
    blocked_by: tuple[str, ...] = ()
    run_id: str | None = None
    heartbeat: float | None = None


@dataclass
class Manifest:
    """A ``{leaf_id: ManifestEntry}`` ledger with durable persistence.

    Not frozen — this is the live, mutable registry that workers
    delta-patch. The *entries themselves* are frozen; mutation replaces a
    single value under its key. ``path`` is where :meth:`save` / :meth:`load`
    persist; it may be ``None`` for an in-memory-only manifest.
    """

    path: Path | None = None
    entries: dict[str, ManifestEntry] = field(default_factory=dict)

    # ── Delta-patch by id (1.1) ──────────────────────────────────────────

    def upsert_entry(self, entry: ManifestEntry) -> ManifestEntry:
        """Add or replace exactly one entry, keyed by ``entry.leaf_id``.

        This is the only sanctioned way to introduce a fully-formed entry.
        Callers MUST NOT reassign ``self.entries`` wholesale — doing so
        would drop concurrent workers' patches.

        Raises:
            ManifestError: If ``entry.status`` is not a known status.
        """
        if entry.status not in VALID_STATUSES:
            raise ManifestError(
                f"invalid status {entry.status!r} for leaf {entry.leaf_id!r}"
            )
        self.entries[entry.leaf_id] = entry
        return entry

    def _patch(self, leaf_id: str, **changes) -> ManifestEntry:
        """Replace one entry with a delta-applied copy (create if absent)."""
        entry = self.entries.get(leaf_id) or ManifestEntry(leaf_id=leaf_id)
        patched = dataclasses.replace(entry, **changes)
        self.entries[leaf_id] = patched
        return patched

    def add_attempt(self, leaf_id: str, attempt: AttemptRecord) -> ManifestEntry:
        """Append one :class:`AttemptRecord` to a leaf's history.

        Creates a ``pending`` entry first if the leaf is unknown, so an
        attempt can never be silently dropped.
        """
        entry = self.entries.get(leaf_id) or ManifestEntry(leaf_id=leaf_id)
        return self._patch(leaf_id, attempts=entry.attempts + (attempt,))

    def mark_in_progress(
        self, leaf_id: str, run_id: str, now: float
    ) -> ManifestEntry:
        """Stamp a leaf as owned by ``run_id`` with a fresh heartbeat.

        Unconditional (unlike :meth:`claim`, which is a guarded acquire).
        Use :meth:`claim` when you need contention safety.
        """
        return self._patch(
            leaf_id, status="in_progress", run_id=run_id, heartbeat=now
        )

    def mark_done(self, leaf_id: str) -> ManifestEntry:
        """Mark a leaf durably complete (the durable-commit step).

        **Double-dispatch safety.** A worker MUST call ``mark_done`` and
        then :meth:`save` (persisting the ``done`` state) *before* it
        releases its in-flight claim. If it instead released the claim
        first, a second worker could :meth:`claim` the still-``pending``
        leaf and redo the (already-finished) work. Committing ``done``
        first closes that window: the leaf leaves the claimable set the
        moment the write lands on disk.

        Clears ``heartbeat`` (the leaf is no longer running) but retains
        ``run_id`` for provenance.
        """
        return self._patch(leaf_id, status="done", heartbeat=None)

    def mark_blocked(
        self, leaf_id: str, blocked_by: Iterable[str]
    ) -> ManifestEntry:
        """Mark a leaf blocked on the given upstream leaf ids."""
        return self._patch(
            leaf_id,
            status="blocked",
            blocked_by=tuple(blocked_by),
            heartbeat=None,
        )

    # ── Atomic claim + owner-scoped reclaim (1.2) ────────────────────────

    def claim(self, leaf_id: str, run_id: str, now: float) -> bool:
        """Atomically acquire a leaf for ``run_id`` (compare-and-swap).

        Succeeds *only* when the leaf is absent or ``pending``. Returns
        ``False`` when the leaf is already ``in_progress`` (owned by any
        run — including this one), ``done``, or ``blocked``, leaving the
        existing entry untouched. This is the single choke point that
        prevents two workers from both believing they own a leaf.

        On success the entry becomes ``in_progress`` stamped with
        ``run_id`` and ``heartbeat = now``.

        Args:
            leaf_id: The leaf to acquire.
            run_id: The acquiring run's uuid.
            now: Epoch-seconds timestamp used as the initial heartbeat.

        Returns:
            ``True`` if the claim was acquired, ``False`` otherwise.
        """
        entry = self.entries.get(leaf_id)
        if entry is None or entry.status == "pending":
            self.mark_in_progress(leaf_id, run_id=run_id, now=now)
            return True
        return False

    def touch(self, leaf_id: str, run_id: str, now: float) -> bool:
        """Refresh the heartbeat of a leaf this run owns.

        A no-op returning ``False`` unless the leaf is ``in_progress`` and
        owned by ``run_id``. Live workers call this periodically so their
        rows stay out of :meth:`reclaim_stale`'s reach.
        """
        entry = self.entries.get(leaf_id)
        if entry is None or entry.status != "in_progress" or entry.run_id != run_id:
            return False
        self._patch(leaf_id, heartbeat=now)
        return True

    def reclaim_stale(
        self, current_run_id: str, now: float, stale_secs: float
    ) -> list[str]:
        """Requeue abandoned ``in_progress`` rows owned by *other* runs.

        A row is reclaimed (re-marked ``pending``, ``run_id`` and
        ``heartbeat`` cleared) iff **all** hold:

        - ``status == "in_progress"`` (``done`` / ``blocked`` / ``pending``
          are never touched), and
        - ``run_id != current_run_id`` (this run's own rows are never
          touched — the caller is the authority on its own liveness), and
        - the heartbeat is older than ``stale_secs`` (``now - heartbeat >
          stale_secs``). A ``None`` heartbeat on a foreign ``in_progress``
          row cannot prove liveness, so it is treated as stale.

        Args:
            current_run_id: The reclaiming run's uuid — its rows are spared.
            now: Current epoch-seconds timestamp.
            stale_secs: Age threshold; foreign rows quieter than this are
                left alone.

        Returns:
            The leaf ids reclaimed, in iteration order.
        """
        reclaimed: list[str] = []
        for leaf_id, entry in list(self.entries.items()):
            if entry.status != "in_progress":
                continue
            if entry.run_id == current_run_id:
                continue
            if entry.heartbeat is not None and (now - entry.heartbeat) <= stale_secs:
                continue
            self._patch(
                leaf_id, status="pending", run_id=None, heartbeat=None
            )
            reclaimed.append(leaf_id)
        return reclaimed

    # ── Rebuildable projection (IDENT-2) ─────────────────────────────────

    @classmethod
    def rebuild_from_vault(
        cls,
        vault_root: Path,
        expected_leaf_paths: Mapping[str, Path],
        *,
        path: Path | None = None,
    ) -> "Manifest":
        """Rebuild done-status from the vault — proving it's a projection.

        For each ``leaf_id -> target_path`` mapping, the leaf is ``done``
        iff its target note file exists on disk (relative paths resolve
        under ``vault_root``; absolute paths are used as-is). Everything
        else is ``pending``. Because this derives state solely from the
        vault (the source of truth per IDENT-2), a lost manifest can
        always be regenerated.

        Args:
            vault_root: Root the relative target paths resolve against.
            expected_leaf_paths: ``{leaf_id: target_note_path}``.
            path: Optional persistence path for the rebuilt manifest.

        Returns:
            A fresh :class:`Manifest`.
        """
        vault_root = Path(vault_root)
        entries: dict[str, ManifestEntry] = {}
        for leaf_id, target in expected_leaf_paths.items():
            target_path = Path(target)
            if not target_path.is_absolute():
                target_path = vault_root / target_path
            status = "done" if target_path.is_file() else "pending"
            entries[leaf_id] = ManifestEntry(leaf_id=leaf_id, status=status)
        return cls(path=path, entries=entries)

    # ── Durable persistence: atomic write + rotation (1.2 / 1.3) ─────────

    def save(self) -> Path:
        """Persist atomically, rotating the prior version to a backup.

        Sequence:

        1. Serialize the current entries to JSON (sorted keys → stable
           bytes across saves).
        2. Rotate backups: ``.bak.1`` → ``.bak.2`` (oldest dropped),
           ``.bak`` → ``.bak.1``, and snapshot the *current* main file to
           ``.bak`` — keeping the last three versions. The main file stays
           in place throughout (snapshot is a copy, not a move).
        3. Write the new payload to a uniquely-named ``.tmp`` sibling,
           ``fsync`` it, then :func:`os.replace` it over the main file.
           ``os.replace`` is atomic on POSIX and Windows, so a reader
           never observes a half-written manifest.

        Returns:
            The main manifest path.

        Raises:
            ManifestError: If this manifest has no ``path``.
        """
        if self.path is None:
            raise ManifestError("cannot save a manifest with path=None")
        path = self.path
        path.parent.mkdir(parents=True, exist_ok=True)

        data = json.dumps(self._to_payload(), indent=2, sort_keys=True) + "\n"

        if path.exists():
            self._rotate_backups(path)

        _atomic_write_text(path, data)
        return path

    @classmethod
    def load(cls, path: Path, *, sweep_tmps: bool = True) -> "Manifest":
        """Load with integrity checks and backup fallback (fail-closed).

        Order of operations:

        1. Sweep orphaned ``.tmp`` files (crashed-writer leftovers).
        2. Try the main file, then ``.bak``, ``.bak.1``, ``.bak.2`` in
           turn. The first file that parses as JSON *and* passes the shape
           check wins.
        3. If none is good (or none exists), return an empty manifest and
           log a warning — never load partial/garbage state (IDENT-5).

        Args:
            path: The main manifest path.
            sweep_tmps: Set ``False`` to skip the orphan-``.tmp`` sweep
                (useful when another writer may be mid-save).

        Returns:
            A :class:`Manifest` bound to ``path``.
        """
        path = Path(path)
        if sweep_tmps:
            _sweep_orphan_tmps(path)

        candidates = [path, *(_bak_path(path, n) for n in range(3))]
        for candidate in candidates:
            if not candidate.exists():
                continue
            payload = _read_good_payload(candidate)
            if payload is None:
                logger.warning(
                    "manifest candidate %s is corrupt/invalid; trying next backup",
                    candidate,
                )
                continue
            if candidate != path:
                logger.warning(
                    "manifest %s unreadable; recovered from backup %s",
                    path,
                    candidate,
                )
            return cls._from_payload(payload, path=path)

        logger.warning(
            "no readable manifest at %s (or any backup); starting empty", path
        )
        return cls(path=path, entries={})

    def _rotate_backups(self, path: Path) -> None:
        """Shift ``.bak`` → ``.bak.1`` → ``.bak.2`` and snapshot main to ``.bak``."""
        bak, bak1, bak2 = (_bak_path(path, n) for n in range(3))
        if bak1.exists():
            os.replace(bak1, bak2)  # drops any prior .bak.2
        if bak.exists():
            os.replace(bak, bak1)
        shutil.copy2(path, bak)

    # ── Serialization ────────────────────────────────────────────────────

    def _to_payload(self) -> dict:
        return {
            "version": MANIFEST_VERSION,
            "entries": {
                leaf_id: {
                    "leaf_id": e.leaf_id,
                    "status": e.status,
                    "run_id": e.run_id,
                    "heartbeat": e.heartbeat,
                    "blocked_by": list(e.blocked_by),
                    "attempts": [
                        {
                            "attempt_n": a.attempt_n,
                            "outcome": a.outcome,
                            "cost": a.cost,
                            "gates_failed": list(a.gates_failed),
                            "at": a.at,
                        }
                        for a in e.attempts
                    ],
                }
                for leaf_id, e in self.entries.items()
            },
        }

    @classmethod
    def _from_payload(cls, payload: dict, *, path: Path | None) -> "Manifest":
        entries: dict[str, ManifestEntry] = {}
        for leaf_id, ed in payload["entries"].items():
            attempts = tuple(
                AttemptRecord(
                    attempt_n=a["attempt_n"],
                    outcome=a["outcome"],
                    cost=a.get("cost", 0.0),
                    gates_failed=tuple(a.get("gates_failed", ())),
                    at=a.get("at", 0.0),
                )
                for a in ed.get("attempts", [])
            )
            entries[leaf_id] = ManifestEntry(
                leaf_id=ed["leaf_id"],
                status=ed["status"],
                attempts=attempts,
                blocked_by=tuple(ed.get("blocked_by", ())),
                run_id=ed.get("run_id"),
                heartbeat=ed.get("heartbeat"),
            )
        return cls(path=path, entries=entries)


# ── Module internals ─────────────────────────────────────────────────────


def _bak_path(path: Path, level: int) -> Path:
    """Backup sibling path: level 0 → ``.bak``, level N → ``.bak.N``."""
    if level == 0:
        return path.with_name(path.name + ".bak")
    return path.with_name(f"{path.name}.bak.{level}")


def _atomic_write_text(path: Path, data: str) -> None:
    """Write ``data`` to ``path`` via a temp file + ``os.replace``.

    The temp file is named ``<name>.<pid>.<uuid>.tmp`` so a crashed writer
    leaves a recognizable orphan that :func:`_sweep_orphan_tmps` cleans up,
    and so concurrent writers never collide on the temp name.
    """
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{os.urandom(8).hex()}.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    # Best-effort directory fsync so the rename is itself durable.
    try:
        dir_fd = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except (OSError, AttributeError):  # pragma: no cover — platform-dependent
        pass


def _sweep_orphan_tmps(path: Path) -> None:
    """Delete leftover ``<name>.*.tmp`` files from crashed writers."""
    parent = path.parent
    if not parent.is_dir():
        return
    for orphan in parent.glob(f"{path.name}.*.tmp"):
        try:
            orphan.unlink()
        except OSError:  # pragma: no cover — best-effort cleanup
            logger.warning("could not sweep orphan tmp %s", orphan)


def _read_good_payload(candidate: Path) -> dict | None:
    """Return the parsed payload if valid JSON *and* well-shaped, else ``None``."""
    try:
        raw = candidate.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not _payload_shape_ok(payload):
        return None
    return payload


def _payload_shape_ok(payload: object) -> bool:
    """Fail-closed integrity check on a decoded manifest payload."""
    if not isinstance(payload, dict):
        return False
    entries = payload.get("entries")
    if not isinstance(entries, dict):
        return False
    for leaf_id, ed in entries.items():
        if not isinstance(leaf_id, str) or not isinstance(ed, dict):
            return False
        if ed.get("leaf_id") != leaf_id:
            return False
        if ed.get("status") not in VALID_STATUSES:
            return False
        if not isinstance(ed.get("blocked_by", []), list):
            return False
        attempts = ed.get("attempts", [])
        if not isinstance(attempts, list):
            return False
        for a in attempts:
            if not isinstance(a, dict) or "attempt_n" not in a or "outcome" not in a:
                return False
        run_id = ed.get("run_id")
        if run_id is not None and not isinstance(run_id, str):
            return False
        heartbeat = ed.get("heartbeat")
        if heartbeat is not None and not isinstance(heartbeat, (int, float)):
            return False
    return True


__all__ = [
    "MANIFEST_VERSION",
    "VALID_STATUSES",
    "ManifestError",
    "AttemptRecord",
    "ManifestEntry",
    "Manifest",
]
