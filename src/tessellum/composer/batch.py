"""Multi-job batch runner — Wave 5a.

Runs many ``(skill, leaves)`` jobs through ``run_pipeline`` in
parallel, with resume support.

Why a batch runner: when you have 50 skills × 1000 leaves to evaluate
(e.g., for the eval framework, or to bulk-regenerate trail summaries
across an entire vault), invoking ``tessellum composer run`` 50 times
sequentially leaves the LLM API mostly idle. The batch runner uses a
``ThreadPoolExecutor`` because LLM calls are I/O-bound — ~95% of wall
time is waiting on the network.

Resume: each job produces a deterministically-named output file
(``<output_dir>/<job_id>.result.json``). If the file exists when the
runner starts, the job is skipped — restarting after a crash recovers
all completed work, costs the same API tokens twice for nothing.

What this module does NOT do (deferred):

  - Token-budget pacing — the parent project's ``BatchPolicy`` includes
    a tokens-per-minute throttle. Skip it for v0.1; the SDK handles
    rate-limits itself with retries.
  - Cross-job upstream dependencies — each job is independent here.
    A skill's internal pipeline still has dependencies (Wave 3); we
    just don't chain across jobs at the batch layer.
  - Streaming progress callbacks — the runner returns once everything
    finishes. Wave 5b's eval framework adds progress reporting.
"""

from __future__ import annotations

import dataclasses
import json
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tessellum.composer.compiler import compile_skill
from tessellum.composer.llm import LLMBackend
from tessellum.composer.scheduler import RunResult, run_pipeline


@dataclass(frozen=True)
class BatchJob:
    """One unit of work for the batch runner.

    Attributes:
        job_id: Stable identifier — used as the output filename and
            resume key. Must be filesystem-safe.
        skill_path: Path to the skill canonical (``skill_*.md``).
        leaves: Per-leaf data dicts. ``[]`` runs the synthetic
            ``{"_id": "corpus"}`` leaf for corpus-wide pipelines.
        vault_root: Materializer file-write root.
        runs_dir: Where the per-job run trace gets written. The result
            JSON also lands here as ``<job_id>.result.json``.
    """

    job_id: str
    skill_path: Path
    leaves: tuple[dict, ...] = ()
    vault_root: Path = Path("vault")
    runs_dir: Path | None = None


@dataclass(frozen=True)
class BatchJobResult:
    """One job's outcome — wraps a RunResult with batch-level state.

    Attributes:
        job_id: Echoes ``BatchJob.job_id``.
        status: ``"completed"`` | ``"skipped"`` | ``"failed"``.
            ``"skipped"`` means the result file already existed (resume).
        run_result: Populated when ``status == "completed"``. ``None``
            for ``"skipped"`` (loaded payload reflected via
            ``previous_payload`` instead) and ``"failed"`` (exception
            occurred — see ``error``).
        previous_payload: Loaded JSON from the existing result file when
            ``status == "skipped"``. Lets callers see prior outcomes
            without re-running.
        result_path: Where the result JSON was written / found.
        error: Exception string if compilation or execution raised.
    """

    job_id: str
    status: str
    run_result: RunResult | None = None
    previous_payload: dict | None = None
    result_path: Path | None = None
    error: str | None = None


@dataclass(frozen=True)
class BatchResult:
    """Aggregate of all job results.

    Attributes:
        jobs: Per-job results, in submission order.
        completed: Job IDs that ran fresh.
        skipped: Job IDs that resumed from cache.
        failed: Job IDs that raised.
    """

    jobs: tuple[BatchJobResult, ...]
    completed: tuple[str, ...] = field(default_factory=tuple)
    skipped: tuple[str, ...] = field(default_factory=tuple)
    failed: tuple[str, ...] = field(default_factory=tuple)


def run_batch(
    jobs: list[BatchJob],
    *,
    backend: LLMBackend,
    parallelism: int = 4,
    dry_run: bool = False,
    resume: bool = True,
) -> BatchResult:
    """Run a list of BatchJobs in parallel with optional resume.

    Args:
        jobs: Jobs to run. Order is preserved in the returned result list.
        backend: LLM backend to dispatch through. The same backend is
            shared across all jobs — most SDKs are thread-safe.
        parallelism: Maximum concurrent jobs. Defaults to 4 — enough to
            saturate typical LLM API rate limits without overwhelming
            them. Pass ``1`` for sequential execution (debugging).
        dry_run: Pass-through to the underlying ``run_pipeline``.
        resume: If True (default), jobs whose result file already exists
            are skipped (status ``"skipped"``). Pass False to force
            re-run regardless of cached results.

    Returns:
        BatchResult.
    """
    job_ids_in_order = [job.job_id for job in jobs]
    results_by_id: dict[str, BatchJobResult] = {}

    if parallelism <= 1:
        # Sequential path — easier to debug, identical observable result.
        for job in jobs:
            results_by_id[job.job_id] = _run_one_job(
                job, backend=backend, dry_run=dry_run, resume=resume
            )
    else:
        with ThreadPoolExecutor(max_workers=parallelism) as pool:
            futures: dict[Future, str] = {}
            for job in jobs:
                fut = pool.submit(
                    _run_one_job,
                    job,
                    backend=backend,
                    dry_run=dry_run,
                    resume=resume,
                )
                futures[fut] = job.job_id
            for fut in as_completed(futures):
                job_id = futures[fut]
                try:
                    results_by_id[job_id] = fut.result()
                except Exception as e:  # pragma: no cover — _run_one_job catches
                    results_by_id[job_id] = BatchJobResult(
                        job_id=job_id,
                        status="failed",
                        error=f"{type(e).__name__}: {e}",
                    )

    ordered = tuple(results_by_id[jid] for jid in job_ids_in_order)
    return BatchResult(
        jobs=ordered,
        completed=tuple(r.job_id for r in ordered if r.status == "completed"),
        skipped=tuple(r.job_id for r in ordered if r.status == "skipped"),
        failed=tuple(r.job_id for r in ordered if r.status == "failed"),
    )


def _run_one_job(
    job: BatchJob,
    *,
    backend: LLMBackend,
    dry_run: bool,
    resume: bool,
) -> BatchJobResult:
    """Run one job. Catches all exceptions → ``status="failed"``."""
    result_path = _result_path(job)

    if resume and result_path.exists():
        try:
            payload = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            return BatchJobResult(
                job_id=job.job_id,
                status="failed",
                result_path=result_path,
                error=f"existing result file unreadable: {e}",
            )
        return BatchJobResult(
            job_id=job.job_id,
            status="skipped",
            previous_payload=payload,
            result_path=result_path,
        )

    try:
        compiled = compile_skill(job.skill_path)
    except Exception as e:
        return BatchJobResult(
            job_id=job.job_id,
            status="failed",
            error=f"compile failed: {type(e).__name__}: {e}",
        )

    try:
        run = run_pipeline(
            compiled,
            leaves=list(job.leaves) if job.leaves else None,
            backend=backend,
            vault_root=job.vault_root,
            dry_run=dry_run,
            runs_dir=job.runs_dir,
        )
    except Exception as e:
        return BatchJobResult(
            job_id=job.job_id,
            status="failed",
            error=f"run failed: {type(e).__name__}: {e}",
        )

    _write_result(result_path, job=job, run=run)
    return BatchJobResult(
        job_id=job.job_id,
        status="completed",
        run_result=run,
        result_path=result_path,
    )


def _result_path(job: BatchJob) -> Path:
    """Where ``job_id``'s result JSON lives — under the job's runs_dir."""
    base = job.runs_dir if job.runs_dir is not None else Path("runs") / "composer"
    return base / f"{job.job_id}.result.json"


def _write_result(path: Path, *, job: BatchJob, run: RunResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "job_id": job.job_id,
        "skill_name": run.skill_name,
        "skill_path": str(run.skill_path),
        "pipeline_version": run.pipeline_version,
        "started_at": run.started_at,
        "duration_seconds": run.duration_seconds,
        "leaf_count": len(run.leaves),
        "step_invocation_count": len(run.step_results),
        "error_count": run.error_count,
        "trace_path": str(run.trace_path) if run.trace_path else None,
        "step_results": [
            {
                "section_id": r.section_id,
                "leaf_id": r.leaf_id,
                "elapsed_ms": r.elapsed_ms,
                "error": r.error,
                "files_written": [str(p) for p in r.materialized.files_written],
                "files_applied": [str(p) for p in r.materialized.files_applied],
            }
            for r in run.step_results
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


__all__ = ["BatchJob", "BatchJobResult", "BatchResult", "run_batch"]
