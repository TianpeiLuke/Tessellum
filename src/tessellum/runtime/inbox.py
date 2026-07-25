"""Deterministic inbox reconciliation; filesystem events are optional hints."""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from dataclasses import dataclass
from pathlib import Path

from tessellum.composer.knowledge_plan import (
    BundleMember,
    SourceBundle,
    bundle_content_hash,
)
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


@dataclass(frozen=True)
class BundleAdmission:
    """The result of admitting a :class:`SourceBundle` as ONE objective.

    ``bundle`` is the typed, ordinal-normalized bundle; ``jobs`` are the
    per-member admitted Jobs (in bundle-member order); ``manifest_path`` is the
    durable manifest written under ``runs/runtime/bundles``; ``created`` is
    False on an idempotent re-admission of an already-recorded bundle.
    """

    bundle: SourceBundle
    jobs: tuple[Job, ...]
    manifest_path: Path
    created: bool


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

    def _bundles_dir(self) -> Path:
        # Durable bundle manifests live alongside the runtime dirs (sibling of
        # spool/artifacts under runs/runtime), so they survive restarts.
        return self.paths.artifacts.parent / "bundles"

    def admit_bundle(
        self,
        members: list[Path | str],
        *,
        objective: str,
        settle_seconds: float | None = None,
    ) -> BundleAdmission:
        """Admit a set of sources as ONE coordinated objective (P2b, A2.1).

        Unlike :meth:`scan_once` (which admits each eligible inbox file as an
        independent per-file job and never infers a grouping), this admits an
        explicitly-supplied, ordered list of member paths as a single
        objective. Each member is admitted via :func:`admit_path`, so member
        idempotency (sha256 ``payload_ref`` dedup) is inherited. The members +
        objective are captured in a typed :class:`SourceBundle` whose
        content-addressed ``bundle_id`` (see :func:`bundle_content_hash`) keys
        a durable JSON manifest written atomically under
        ``runs/runtime/bundles``. Re-admitting the same members + objective is
        idempotent: same ``bundle_id``, no duplicate jobs, ``created=False``.

        ``scan_once`` is deliberately untouched — this is a separate, opt-in
        entry point.
        """
        settle = self.settle_seconds if settle_seconds is None else settle_seconds
        jobs: list[Job] = []
        bundle_members: list[BundleMember] = []
        for ordinal, raw in enumerate(members):
            path = Path(raw)
            job, _created = admit_path(
                path,
                paths=self.paths,
                store=self.store,
                settle_seconds=settle,
            )
            jobs.append(job)
            # payload_ref is a content hash (sha256:...) — pins the parsed bytes.
            payload_ref = job.request.payload_ref
            extracted_hash = payload_ref.split(":", 1)[-1]
            bundle_members.append(
                BundleMember(
                    source_id=job.job_id,
                    ordinal=ordinal,
                    ref=job.request.original_path,
                    parser_id=Path(job.request.original_path).suffix.lstrip(".")
                    or "raw",
                    extracted_text_hash=extracted_hash,
                )
            )

        # bundle_id is content-addressed over (objective, ordered members),
        # so it is stable across re-admission and independent of a caller id.
        provisional = SourceBundle(
            bundle_id="pending",
            objective=objective,
            members=tuple(bundle_members),
        )
        digest = hashlib.sha256(
            (objective + "\0" + bundle_content_hash(provisional)).encode("utf-8")
        ).hexdigest()
        bundle = SourceBundle(
            bundle_id=digest,
            objective=objective,
            members=tuple(bundle_members),
        )

        bundles_dir = self._bundles_dir()
        bundles_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = bundles_dir / f"{bundle.bundle_id}.json"
        created = not manifest_path.exists()
        if created:
            payload = {
                "bundle_id": bundle.bundle_id,
                "objective": bundle.objective,
                "content_hash": bundle_content_hash(bundle),
                "members": [
                    {
                        "ordinal": m.ordinal,
                        "source_id": m.source_id,
                        "ref": m.ref,
                        "payload_ref": j.request.payload_ref,
                        "parser_id": m.parser_id,
                        "extracted_text_hash": m.extracted_text_hash,
                    }
                    for m, j in zip(bundle.members, jobs)
                ],
            }
            tmp = bundles_dir / f".{bundle.bundle_id}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
            try:
                with tmp.open("w", encoding="utf-8") as handle:
                    json.dump(payload, handle, sort_keys=True, indent=2)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(tmp, manifest_path)
            finally:
                tmp.unlink(missing_ok=True)

        return BundleAdmission(
            bundle=bundle,
            jobs=tuple(jobs),
            manifest_path=manifest_path,
            created=created,
        )
