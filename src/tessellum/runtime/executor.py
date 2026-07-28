"""Adapter from durable jobs to the native Composer digestion pipeline."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import threading
import uuid
from contextlib import nullcontext
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, ContextManager

from tessellum.composer import (
    AnthropicBackend,
    BedrockBackend,
    Manifest,
    MockBackend,
)
from tessellum.composer.context_assembler import get_assembler
from tessellum.composer.credential_pool import ErrorClassBreaker, RunBudget
from tessellum.composer.digestion import DigestionResult, run_digestion_pipeline
from tessellum.composer.fix import make_llm_fixer
from tessellum.composer.gates import GateSuite, build_close_gate, build_wave_gate
from tessellum.composer.llm import LLMBackend
from tessellum.runtime.models import Job, Lease
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.policy import RuntimePolicy
from tessellum.runtime.routing import DigestionRoute


class UnsupportedSourceError(ValueError):
    pass


class DigestionIncompleteError(RuntimeError):
    """Preserve Composer's typed terminal cause at the job boundary."""

    def __init__(self, message: str, *, error_class: str = "validation") -> None:
        super().__init__(message)
        self.error_class = error_class

    @classmethod
    def from_result(cls, result: DigestionResult) -> "DigestionIncompleteError":
        for phase in reversed(result.phases):
            if phase.run is None:
                continue
            failed = next(
                (
                    step
                    for step in phase.run.step_results
                    if step.error is not None
                ),
                None,
            )
            if failed is not None:
                return cls(
                    f"digestion {phase.phase} failed: {failed.error}",
                    error_class=failed.error_class or "validation",
                )
        stopped = result.stopped_at or "execute"
        decision = (
            result.sign_off.decision
            if result.sign_off is not None
            else "not completed"
        )
        return cls(f"digestion stopped at {stopped}: {decision}")


class VaultEffectJournal:
    """Capture pre-write vault bytes so uncommitted work can be rolled back.

    When ``journal_dir`` is supplied, every original is persisted before the
    corresponding vault write. A later worker can therefore replay an open
    journal after a hard process crash. Marking a journal accepted is itself
    durable, so recovery never rolls back output that already passed digestion.
    """

    def __init__(
        self,
        root: Path,
        *,
        effect_guard: Callable[[], ContextManager[None]] | None,
        journal_dir: Path | None = None,
    ) -> None:
        self.root = root.resolve()
        self.effect_guard = effect_guard
        self.journal_dir = (
            journal_dir.expanduser().resolve() if journal_dir is not None else None
        )
        self._originals: dict[Path, bytes | None] = {}
        self._entries: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        if self.journal_dir is not None:
            self._ensure_directory_durable(self.journal_dir)
            manifest = self.journal_dir / "journal.json"
            if manifest.is_file():
                payload = self._read_manifest(self.journal_dir)
                if payload["state"] != "open":
                    raise RuntimeError(
                        f"effect journal is not open: {self.journal_dir}"
                    )
                self._entries = list(payload["entries"])
            else:
                self._persist("open")

    def record(self, path: Path) -> None:
        resolved = path.resolve()
        try:
            relative = resolved.relative_to(self.root)
        except ValueError as exc:
            raise ValueError(f"journal path escapes vault: {resolved}") from exc
        with self._lock:
            if self.journal_dir is None:
                if resolved.exists() and not resolved.is_file():
                    raise ValueError(
                        f"journal target is not a regular file: {resolved}"
                    )
                if resolved not in self._originals:
                    self._originals[resolved] = (
                        resolved.read_bytes() if resolved.is_file() else None
                    )
                return
            relative_text = relative.as_posix()
            if any(entry["path"] == relative_text for entry in self._entries):
                return
            if resolved.exists() and not resolved.is_file():
                raise ValueError(
                    f"journal target is not a regular file: {resolved}"
                )
            existed = resolved.is_file()
            backup = None
            if existed:
                backup = f"{len(self._entries):08d}.original"
                self._atomic_write_bytes(
                    self.journal_dir / backup,
                    resolved.read_bytes(),
                )
            self._entries.append(
                {
                    "path": relative_text,
                    "existed": existed,
                    "backup": backup,
                    "postimages": [],
                }
            )
            # This commit precedes the caller's vault mutation.
            self._persist("open")

    __call__ = record

    def record_postimage(self, path: Path, content: bytes) -> None:
        """Durably allow one exact runtime-authored state during recovery."""
        if self.journal_dir is None:
            return
        if not isinstance(content, bytes):
            raise TypeError("journal postimage content must be bytes")
        resolved = path.resolve()
        try:
            relative_text = resolved.relative_to(self.root).as_posix()
        except ValueError as exc:
            raise ValueError(f"journal path escapes vault: {resolved}") from exc
        digest = hashlib.sha256(content).hexdigest()
        with self._lock:
            entry = next(
                (
                    candidate
                    for candidate in self._entries
                    if candidate["path"] == relative_text
                ),
                None,
            )
            if entry is None:
                raise RuntimeError(
                    f"journal postimage has no preimage: {resolved}"
                )
            postimages = entry["postimages"]
            if digest not in postimages:
                postimages.append(digest)
                # This commit precedes publication of the matching bytes.
                self._persist("open")

    def rollback(self) -> None:
        if self.journal_dir is not None:
            with self._lock:
                entries = list(self._entries)
            self._restore_entries(
                root=self.root,
                journal_dir=self.journal_dir,
                entries=entries,
                effect_guard=self.effect_guard,
            )
            with self._lock:
                self._persist("rolled_back")
                self._entries.clear()
            self._cleanup()
            return
        guard = self.effect_guard or nullcontext
        with self._lock:
            entries = list(reversed(self._originals.items()))
            self._originals.clear()
        for path, original in entries:
            with guard():
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(original)

    def accept(self) -> None:
        if self.journal_dir is not None:
            with self._lock:
                self._persist("accepted")
                self._entries.clear()
            self._cleanup()
            return
        with self._lock:
            self._originals.clear()

    @classmethod
    def recover_pending(
        cls,
        root: Path,
        artifacts_dir: Path,
        *,
        is_accepted_job: Callable[[str], bool] | None = None,
    ) -> int:
        """Roll back every open durable journal beneath ``artifacts_dir``.

        The caller must hold the cross-process vault write lock. Accepted and
        already-rolled-back journals are cleanup leftovers. An open journal
        whose job durably reached ``COMMITTING`` is also accepted: the state
        transition is the commit decision and may precede journal cleanup.
        """
        resolved_root = root.resolve()
        recovered = 0
        for journal_dir in sorted(artifacts_dir.glob("*/vault-effects/*")):
            if not journal_dir.is_dir():
                continue
            manifest = journal_dir / "journal.json"
            if not manifest.is_file():
                cls._remove_tree(journal_dir)
                continue
            payload = cls._read_manifest(journal_dir)
            recorded_root = Path(payload["root"]).resolve()
            if recorded_root != resolved_root:
                raise RuntimeError(
                    "effect journal vault root mismatch: "
                    f"{recorded_root} != {resolved_root}"
                )
            if payload["state"] == "open":
                job_id = journal_dir.parent.parent.name
                if is_accepted_job is not None and is_accepted_job(job_id):
                    cls._write_manifest(
                        journal_dir,
                        root=resolved_root,
                        state="accepted",
                        entries=payload["entries"],
                    )
                else:
                    cls._restore_entries(
                        root=resolved_root,
                        journal_dir=journal_dir,
                        entries=payload["entries"],
                        effect_guard=None,
                    )
                    cls._write_manifest(
                        journal_dir,
                        root=resolved_root,
                        state="rolled_back",
                        entries=payload["entries"],
                    )
                    recovered += 1
            cls._remove_tree(journal_dir)
        return recovered

    def _persist(self, state: str) -> None:
        assert self.journal_dir is not None
        self._write_manifest(
            self.journal_dir,
            root=self.root,
            state=state,
            entries=self._entries,
        )

    def _cleanup(self) -> None:
        assert self.journal_dir is not None
        self._remove_tree(self.journal_dir)

    @classmethod
    def _restore_entries(
        cls,
        *,
        root: Path,
        journal_dir: Path,
        entries: list[dict[str, Any]],
        effect_guard: Callable[[], ContextManager[None]] | None,
    ) -> None:
        guard = effect_guard or nullcontext
        prepared: list[tuple[dict[str, Any], Path, bytes | None]] = []
        for entry in entries:
            target = (root / entry["path"]).resolve()
            try:
                target.relative_to(root)
            except ValueError as exc:
                raise RuntimeError(
                    f"effect journal path escapes vault: {target}"
                ) from exc
            original: bytes | None = None
            allowed_hashes = set(entry["postimages"])
            if entry["existed"]:
                backup_name = entry["backup"]
                if not isinstance(backup_name, str):
                    raise RuntimeError(
                        f"effect journal backup missing for {target}"
                    )
                backup = (journal_dir / backup_name).resolve()
                try:
                    backup.relative_to(journal_dir.resolve())
                except ValueError as exc:
                    raise RuntimeError(
                        f"effect journal backup escapes journal: {backup}"
                    ) from exc
                if not backup.is_file():
                    raise RuntimeError(
                        f"effect journal backup missing: {backup}"
                    )
                original = backup.read_bytes()
                allowed_hashes.add(hashlib.sha256(original).hexdigest())

            if target.exists() and not target.is_file():
                raise RuntimeError(
                    f"effect journal recovery conflict at {target}: "
                    "target is not a regular file"
                )
            if target.is_file():
                current_hash = hashlib.sha256(target.read_bytes()).hexdigest()
                if current_hash not in allowed_hashes:
                    raise RuntimeError(
                        f"effect journal recovery conflict at {target}: "
                        "current bytes are not journaled"
                    )
            elif entry["existed"]:
                raise RuntimeError(
                    f"effect journal recovery conflict at {target}: "
                    "original file is missing"
                )
            prepared.append((entry, target, original))

        for entry, target, original in reversed(prepared):
            with guard():
                if entry["existed"]:
                    assert original is not None
                    cls._atomic_write_bytes(target, original)
                elif target.exists():
                    target.unlink()
                    cls._fsync_dir(target.parent)

    @classmethod
    def _read_manifest(cls, journal_dir: Path) -> dict[str, Any]:
        try:
            payload = json.loads(
                (journal_dir / "journal.json").read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                f"invalid effect journal: {journal_dir}"
            ) from exc
        if (
            not isinstance(payload, dict)
            or payload.get("version") != 1
            or payload.get("state") not in {"open", "accepted", "rolled_back"}
            or not isinstance(payload.get("root"), str)
            or not isinstance(payload.get("entries"), list)
        ):
            raise RuntimeError(f"invalid effect journal shape: {journal_dir}")
        for entry in payload["entries"]:
            if (
                not isinstance(entry, dict)
                or not isinstance(entry.get("path"), str)
                or not isinstance(entry.get("existed"), bool)
                or not isinstance(entry.get("postimages"), list)
                or any(
                    not isinstance(digest, str)
                    or len(digest) != 64
                    or any(
                        character not in "0123456789abcdef"
                        for character in digest
                    )
                    for digest in entry.get("postimages", ())
                )
                or (
                    entry["existed"]
                    and not isinstance(entry.get("backup"), str)
                )
            ):
                raise RuntimeError(f"invalid effect journal entry: {journal_dir}")
        return payload

    @classmethod
    def _write_manifest(
        cls,
        journal_dir: Path,
        *,
        root: Path,
        state: str,
        entries: list[dict[str, Any]],
    ) -> None:
        payload = {
            "version": 1,
            "root": str(root),
            "state": state,
            "entries": entries,
        }
        cls._atomic_write_bytes(
            journal_dir / "journal.json",
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )

    @staticmethod
    def _atomic_write_bytes(path: Path, content: bytes) -> None:
        VaultEffectJournal._ensure_directory_durable(path.parent)
        temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
        try:
            with temporary.open("wb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
            VaultEffectJournal._fsync_dir(path.parent)
        finally:
            temporary.unlink(missing_ok=True)

    @staticmethod
    def _ensure_directory_durable(path: Path) -> None:
        missing: list[Path] = []
        current = path
        while not current.exists():
            missing.append(current)
            current = current.parent
        if not current.is_dir():
            raise RuntimeError(f"journal parent is not a directory: {current}")
        for directory in reversed(missing):
            directory.mkdir()
            VaultEffectJournal._fsync_dir(directory.parent)

    @staticmethod
    def _fsync_dir(path: Path) -> None:
        try:
            descriptor = os.open(path, os.O_RDONLY)
        except OSError:
            return
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    @staticmethod
    def _remove_tree(path: Path) -> None:
        parent = path.parent
        shutil.rmtree(path, ignore_errors=False)
        VaultEffectJournal._fsync_dir(parent)


@dataclass(frozen=True)
class BackendConfig:
    kind: str = "mock"
    model: str | None = None
    region: str = "us-east-1"
    aws_profile: str | None = None
    mock_responses: dict[str, str] | None = None


def build_backend(config: BackendConfig) -> LLMBackend:
    if config.kind == "anthropic":
        return AnthropicBackend(model=config.model or "claude-sonnet-4-6")
    if config.kind == "bedrock":
        return BedrockBackend(
            model=config.model or "us.anthropic.claude-sonnet-4-6",
            region=config.region,
            aws_profile=config.aws_profile,
        )
    if config.kind == "mock":
        return MockBackend(responses=config.mock_responses)
    raise ValueError(f"unknown backend: {config.kind!r}")


def _read_source(path: Path, *, source_suffix: str) -> str:
    suffix = source_suffix.lower()
    if suffix in {".md", ".txt", ".tex", ".json", ".jsonl", ".csv"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        try:
            import pdfplumber  # type: ignore[import-not-found]
        except ImportError as exc:
            raise UnsupportedSourceError(
                "PDF ingestion requires `pip install tessellum[ingest]`"
            ) from exc
        with pdfplumber.open(path) as pdf:
            return "\n\n".join((page.extract_text() or "") for page in pdf.pages)
    raise UnsupportedSourceError(f"unsupported inbox source type: {suffix or '(none)'}")


def _format_only_gate() -> GateSuite:
    suite = build_close_gate()
    return GateSuite(gates=(suite.gates[0],))


@dataclass
class DigestionExecutor:
    paths: RuntimePaths
    backend: LLMBackend
    cancellation_check: Callable[[], bool] | None = None
    effect_guard: Callable[[], ContextManager[None]] | None = None
    _journal: VaultEffectJournal | None = field(default=None, init=False)

    def rollback_uncommitted(self) -> None:
        if self._journal is not None:
            self._journal.rollback()
            self._journal = None

    def accept_uncommitted(self) -> None:
        if self._journal is not None:
            self._journal.accept()
            self._journal = None

    def execute(
        self,
        job: Job,
        lease: Lease,
        route: DigestionRoute,
        policy: RuntimePolicy,
    ) -> DigestionResult:
        if self.cancellation_check is not None and self.cancellation_check():
            raise InterruptedError("job cancelled before planning")
        spool = self.paths.spool_path(job.request.payload_ref)
        source_content = _read_source(
            spool,
            source_suffix=Path(job.request.original_path).suffix,
        )
        source_hash = hashlib.sha256(source_content.encode("utf-8")).hexdigest()
        # P2b (A2.2): the plan skill prompt references ``{{leaf.source_url}}``
        # (skill_tessellum_plan_digestion.md), but the leaf previously carried
        # only ``source_path`` — so the placeholder rendered a
        # ``<missing leaf.source_url>`` sentinel and the planner was under-fed.
        # Provide a bounded reference (a file:// URI for absolute paths, else
        # the raw path) — NOT the content. ``source_content`` stays on the leaf
        # for a context_assembler to window; it is never force-injected into
        # the prompt (that would breach HARD_PROMPT_CAP_CHARS).
        original_path = job.request.original_path
        source_url = (
            Path(original_path).as_uri()
            if Path(original_path).is_absolute()
            else original_path
        )
        source_leaf = {
            "_id": job.job_id,
            "source_path": original_path,
            "source_url": source_url,
            "source_name": Path(original_path).name,
            "source_type": route.source_kind,
            "source_content": source_content,
            "source_hash": source_hash,
            "inbox_lane": job.request.lane,
            "building_block_hint": route.building_block_hint,
            # M0: a single source is a corpus of one — expose the same
            # member_count / members keys the multi-doc fan-in leaf carries, so
            # the plan skill's {{leaf.member_count}} / {{leaf.members}} resolve
            # (never a <missing> sentinel) whether the source is one doc or a
            # bundle. member_count == 1 tells the planner this is the single-doc
            # path; the members list is empty (the single source is already
            # described by source_url / source_name, not re-windowed here).
            "member_count": 1,
            "members": [],
        }
        artifact_dir = self.paths.job_artifacts(job.job_id)
        artifact_dir.mkdir(parents=True, exist_ok=True)
        (artifact_dir / "source_leaf.json").write_text(
            json.dumps(source_leaf, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        manifest = Manifest.load(artifact_dir / "manifest.json")
        budget = RunBudget(
            max_invocations=policy.max_invocations,
            max_cost=policy.max_cost,
        )
        # P17: the run-level error-class breaker. Disabled only when BOTH the
        # proportional rule and the absolute backstop are off (parity with
        # pre-P17); otherwise the two rules together catch both a wave that is
        # mostly-failing (proportion) and a mid-wave credential death that
        # dilutes the ratio (absolute backstop).
        breaker = (
            ErrorClassBreaker(
                proportion=policy.breaker_proportion,
                error_threshold=policy.breaker_error_threshold,
                min_dispatched=policy.breaker_min_dispatched,
            )
            if (
                policy.breaker_proportion is not None
                or policy.breaker_error_threshold is not None
            )
            else None
        )
        close_gate = _format_only_gate() if policy.close_gate else None
        journal = VaultEffectJournal(
            self.paths.vault,
            effect_guard=self.effect_guard,
            journal_dir=artifact_dir / "vault-effects" / str(lease.generation),
        )
        self._journal = journal
        try:
            result = run_digestion_pipeline(
                skills_dir=self.paths.skills,
                source_leaf=source_leaf,
                backend=self.backend,
                vault_root=self.paths.vault,
                execute_max_workers=policy.max_workers,
                cancellation_check=self.cancellation_check,
                effect_guard=self.effect_guard,
                effect_recorder=journal,
                manifest=manifest,
                run_id=f"{job.job_id}:{lease.generation}",
                generation=job.execution_generation,
                manifest_stale_secs=0.0,
                close_gate=close_gate,
                informed_fixer=(
                    make_llm_fixer(
                        self.backend,
                        budget=budget,
                        cancellation_check=self.cancellation_check,
                        effect_guard=self.effect_guard,
                        effect_recorder=journal,
                    )
                    if policy.close_gate and policy.max_fix_rounds > 0
                    else None
                ),
                max_fix_rounds=policy.max_fix_rounds,
                budget=budget,
                breaker=breaker,
                wave_gate=build_wave_gate() if policy.wave_gate else None,
                context_assembler=get_assembler(
                    policy.context_strategy,
                    max_chars=policy.context_max_chars,
                    # db_path/query are consumed only by the "retrieval" strategy
                    # (RetrievalAugmentedAssembler) — the default "windowed"
                    # strategy ignores them, so this is byte-identical unless a
                    # deployment opts into policy.context_strategy="retrieval".
                    # The index exists only once a prior commit built it; the
                    # assembler is fail-soft when it is absent.
                    db_path=self.paths.index_db if self.paths.index_db.exists() else None,
                    query=source_content[:512],
                ),
                # FZ 20k9d2: the live index feeds per-note related-notes
                # enrichment (each written note gets relevance-ranked
                # ## References links → note_links graph edges). None when the
                # index does not yet exist (first-ever digestion) → fail-soft
                # pass-through, byte-identical to pre-fix.
                related_notes_db=(
                    self.paths.index_db if self.paths.index_db.exists() else None
                ),
                events_path=artifact_dir / "composer-events.jsonl",
                stats_path=artifact_dir / "statistics.json",
            )
        except BaseException:
            self.rollback_uncommitted()
            raise
        if not result.completed:
            self.rollback_uncommitted()
        (artifact_dir / "plan.json").write_text(
            json.dumps(result.plan_doc, indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf-8",
        )
        return result
