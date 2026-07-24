"""Deterministic inbox reconciliation; filesystem events are optional hints."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tessellum.runtime.admission import AdmissionError, admit_path, is_eligible_source
from tessellum.runtime.models import Job
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.routing import LANE_HINTS
from tessellum.runtime.store import RuntimeStore


@dataclass(frozen=True)
class ScanResult:
    admitted: tuple[Job, ...]
    deduplicated: tuple[Job, ...]
    rejected: tuple[tuple[Path, str], ...]


class InboxScanner:
    def __init__(
        self,
        *,
        paths: RuntimePaths,
        store: RuntimeStore,
        settle_seconds: float = 1.0,
    ) -> None:
        self.paths = paths
        self.store = store
        self.settle_seconds = settle_seconds

    def scan_once(self) -> ScanResult:
        admitted: list[Job] = []
        deduplicated: list[Job] = []
        rejected: list[tuple[Path, str]] = []
        for lane in LANE_HINTS:
            lane_dir = self.paths.inbox / lane
            if not lane_dir.is_dir():
                continue
            for path in sorted(lane_dir.rglob("*")):
                if not is_eligible_source(path, self.paths.inbox):
                    continue
                try:
                    job, created = admit_path(
                        path,
                        paths=self.paths,
                        store=self.store,
                        settle_seconds=self.settle_seconds,
                    )
                except (AdmissionError, OSError) as exc:
                    rejected.append((path, str(exc)))
                    continue
                (admitted if created else deduplicated).append(job)
        return ScanResult(
            admitted=tuple(admitted),
            deduplicated=tuple(deduplicated),
            rejected=tuple(rejected),
        )
