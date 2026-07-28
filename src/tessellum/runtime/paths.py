"""Absolute runtime path resolution independent of process cwd."""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

# Subdirectory names under runs/ that belong to subsystem-owned trees, not
# per-run roots (runs/runtime/, runs/composer/, runs/dks/, runs/eval/). A run
# id minted by :func:`new_run_id` can never collide with these (the ``run-``
# prefix), but ``RuntimePaths.run_dir`` validates caller-supplied ids too.
_RESERVED_RUNS_SUBDIRS: frozenset[str] = frozenset({"runtime", "composer", "dks", "eval"})


def new_run_id() -> str:
    """Mint a collision-safe composer run identity (A0, FZ 20k9c1a1a1b7c2k1a).

    Shape: ``run-<UTC yyyymmdd-hhmmss>-<8 hex>`` — sortable by mint time,
    unique via the uuid tail, and prefixed so it can never collide with the
    reserved subsystem subdirectories under ``runs/``.
    """
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"run-{stamp}-{uuid.uuid4().hex[:8]}"


@dataclass(frozen=True)
class RuntimePaths:
    root: Path
    vault: Path
    inbox: Path
    skills: Path
    runs: Path
    db: Path
    spool: Path
    artifacts: Path
    archive: Path
    events: Path
    index_db: Path

    @classmethod
    def discover(
        cls,
        root: Path | str | None = None,
        *,
        env: Mapping[str, str] | None = None,
    ) -> "RuntimePaths":
        values = os.environ if env is None else env
        resolved_root = Path(
            values.get("TESSELLUM_ROOT") or root or Path.cwd()
        ).expanduser().resolve()
        runs = Path(values.get("TESSELLUM_RUNS") or resolved_root / "runs").expanduser().resolve()
        runtime_dir = runs / "runtime"
        configured_vault = values.get("TESSELLUM_VAULT")
        if configured_vault:
            vault = Path(configured_vault).expanduser().resolve()
        else:
            nested_vault = resolved_root / "vault"
            direct_vault = resolved_root / "resources" / "skills"
            vault = resolved_root if direct_vault.is_dir() else nested_vault
        inbox = Path(values.get("TESSELLUM_INBOX") or resolved_root / "inbox").expanduser().resolve()
        return cls(
            root=resolved_root,
            vault=vault,
            inbox=inbox,
            skills=Path(
                values.get("TESSELLUM_SKILLS") or vault / "resources" / "skills"
            ).expanduser().resolve(),
            runs=runs,
            db=Path(
                values.get("TESSELLUM_RUNTIME_DB") or runtime_dir / "runtime.db"
            ).expanduser().resolve(),
            spool=runtime_dir / "spool",
            artifacts=runtime_dir / "artifacts",
            archive=runtime_dir / "archive",
            events=runtime_dir / "events",
            index_db=Path(
                values.get("TESSELLUM_INDEX_DB")
                or resolved_root / "data" / "tessellum.db"
            ).expanduser().resolve(),
        )

    def ensure_runtime_dirs(self) -> None:
        for path in (
            self.db.parent,
            self.spool,
            self.artifacts,
            self.archive,
            self.events,
        ):
            path.mkdir(parents=True, exist_ok=True)

    def spool_path(self, payload_ref: str) -> Path:
        algorithm, separator, digest = payload_ref.partition(":")
        if separator != ":" or algorithm != "sha256" or len(digest) != 64:
            raise ValueError(f"invalid payload ref: {payload_ref!r}")
        return self.spool / digest[:2] / digest

    def job_artifacts(self, job_id: str) -> Path:
        return self.artifacts / job_id

    def run_dir(self, run_id: str) -> Path:
        """The per-run root ``runs/<run_id>/`` (A0, FZ 20k9c1a1a1b7c2k1a).

        The future home of run-scoped working artifacts
        (``runs/<run_id>/artifacts/<key>``) — A0 only establishes the
        addressing; nothing writes here yet. Validates the id so a
        caller-supplied value can neither escape ``runs/`` nor collide with
        the reserved subsystem subdirectories.
        """
        if (
            not run_id
            or "/" in run_id
            or "\\" in run_id
            or run_id in (".", "..")
            or run_id in _RESERVED_RUNS_SUBDIRS
        ):
            raise ValueError(f"invalid run id: {run_id!r}")
        return self.runs / run_id
