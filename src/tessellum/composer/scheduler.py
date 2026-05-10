"""Pipeline scheduler — runs a CompiledPipeline end-to-end.

Topologically iterates the pipeline (the compiler already topo-sorted),
running each step against each leaf (``per_leaf``) or once
(``corpus_wide`` / ``cross_leaf``). Accumulates upstream outputs by
``output_key`` so downstream ``{{upstream.X}}`` placeholders resolve.

What this Wave 3 implementation covers:

  - Topological dispatch (no batching yet — column-oriented batching
    surfaces in Wave 5+ if profiling shows the per-leaf calls dominate).
  - Run trace written to ``runs/composer/<YYYY-MM-DDThh-mm-ss>_<skill>.json``
    when ``runs_dir`` is set.
  - INFRA-role steps are skipped (they're informational glue, no
    LLM dispatch).

Deferred:

  - Cross-leaf scoping (treated as corpus_wide for now).
  - APPLY-mode ``{{existing.Z}}`` pre-fetch — the materializer reads
    existing files at write time when needed; Wave 5+ adds compile-time
    pre-fetch for prompt context.
  - Column-oriented batching — group N ``per_leaf`` instances into one
    LLM call. Per FZ 5e1c3a1a5, ~4× cost reduction; defer until backend
    pricing motivates it.
"""

from __future__ import annotations

import datetime as dt
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tessellum.composer.compiler import CompiledPipeline, CompiledStep
from tessellum.composer.executor import StepResult, execute_step
from tessellum.composer.llm import LLMBackend


@dataclass(frozen=True)
class RunResult:
    """One end-to-end pipeline run.

    Attributes:
        skill_name: From the compiled pipeline.
        skill_path: Source canonical path.
        pipeline_version: Sidecar's ``version`` field.
        started_at: ISO-8601 UTC timestamp.
        duration_seconds: Wall-clock total.
        leaves: The leaves the pipeline ran against (with ``_id`` keys).
        step_results: One ``StepResult`` per (step × leaf-or-corpus)
            invocation, in execution order.
        error_count: How many step_results had ``error != None``.
        trace_path: Where the trace JSON was written, or ``None`` if
            tracing was disabled.
    """

    skill_name: str
    skill_path: Path
    pipeline_version: str
    started_at: str
    duration_seconds: float
    leaves: tuple[dict, ...]
    step_results: tuple[StepResult, ...]
    error_count: int
    trace_path: Path | None = None


def run_pipeline(
    pipeline: CompiledPipeline,
    *,
    leaves: list[dict] | None = None,
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool = False,
    runs_dir: Path | None = None,
) -> RunResult:
    """Execute a compiled pipeline against ``leaves``.

    Args:
        pipeline: The compiled pipeline (output of
            :func:`tessellum.composer.compile_skill`).
        leaves: List of per-leaf data dicts. ``None`` or empty → a
            single synthetic ``{"_id": "corpus"}`` leaf so corpus_wide
            steps still run. Each leaf is augmented in-place with an
            ``_id`` key if absent.
        backend: LLM backend to dispatch through.
        vault_root: Root for materializer file paths.
        dry_run: Pass through to materializers; skips filesystem writes.
        runs_dir: If set, write a JSON trace to
            ``runs_dir/<timestamp>_<skill>.json``. Convention is the
            project's ``runs/composer/`` directory.

    Returns:
        RunResult.
    """
    started = time.monotonic()
    started_iso = dt.datetime.now(dt.UTC).isoformat()

    if leaves is None or not leaves:
        leaves = [{"_id": "corpus"}]
    else:
        for i, leaf in enumerate(leaves):
            if "_id" not in leaf:
                leaf["_id"] = f"leaf_{i}"

    upstream: dict[str, Any] = {}
    step_results: list[StepResult] = []
    error_count = 0

    for step in pipeline.steps:
        if step.role == "INFRA":
            continue

        per_leaf = step.aggregation == "per_leaf"
        scope_leaves = leaves if per_leaf else [{"_id": "corpus"}]

        # Collect this step's outputs (per leaf or single corpus value)
        # to feed into ``upstream`` after the step completes. For
        # per_leaf steps, we expose a list of structured outputs under
        # the output_key (so downstream steps see all leaves at once
        # if they need to). For corpus_wide steps, expose the single dict.
        per_step_outputs: list[dict] = []

        for leaf in scope_leaves:
            result = execute_step(
                step,
                leaf=leaf,
                upstream=upstream,
                backend=backend,
                vault_root=vault_root,
                dry_run=dry_run,
            )
            step_results.append(result)
            if result.error is not None:
                error_count += 1
            else:
                per_step_outputs.append(result.materialized.structured)

        if step.output_key and per_step_outputs:
            if per_leaf:
                upstream[step.output_key] = per_step_outputs
            else:
                upstream[step.output_key] = per_step_outputs[0]

    duration = time.monotonic() - started

    trace_path: Path | None = None
    if runs_dir is not None:
        trace_path = _write_trace(
            runs_dir=runs_dir,
            pipeline=pipeline,
            started_iso=started_iso,
            duration=duration,
            leaves=leaves,
            step_results=step_results,
            error_count=error_count,
        )

    return RunResult(
        skill_name=pipeline.skill_name,
        skill_path=pipeline.skill_path,
        pipeline_version=pipeline.pipeline_version,
        started_at=started_iso,
        duration_seconds=duration,
        leaves=tuple(leaves),
        step_results=tuple(step_results),
        error_count=error_count,
        trace_path=trace_path,
    )


# ── Run trace ──────────────────────────────────────────────────────────────


def _filesystem_safe_timestamp(iso: str) -> str:
    """Convert an ISO-8601 timestamp to a filesystem-safe string.

    ``2026-05-10T20:00:42.346528+00:00`` → ``2026-05-10T20-00-42``
    """
    base = iso.split(".")[0].split("+")[0]  # drop microseconds + tz
    return base.replace(":", "-")


def _write_trace(
    *,
    runs_dir: Path,
    pipeline: CompiledPipeline,
    started_iso: str,
    duration: float,
    leaves: list[dict],
    step_results: list[StepResult],
    error_count: int,
) -> Path:
    runs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = _filesystem_safe_timestamp(started_iso)
    target = runs_dir / f"{timestamp}_{pipeline.skill_name}.json"

    payload = {
        "skill_name": pipeline.skill_name,
        "skill_path": str(pipeline.skill_path),
        "pipeline_version": pipeline.pipeline_version,
        "started_at": started_iso,
        "duration_seconds": duration,
        "leaf_count": len(leaves),
        "step_invocation_count": len(step_results),
        "error_count": error_count,
        "leaves": [{"_id": leaf.get("_id"), **{k: v for k, v in leaf.items() if k != "_id"}} for leaf in leaves],
        "step_results": [
            {
                "section_id": r.section_id,
                "leaf_id": r.leaf_id,
                "elapsed_ms": r.elapsed_ms,
                "error": r.error,
                "response_chars": len(r.response.content),
                "backend_id": r.response.backend_id,
                "files_written": [str(p) for p in r.materialized.files_written],
                "files_applied": [str(p) for p in r.materialized.files_applied],
                "notes": r.materialized.notes,
            }
            for r in step_results
        ],
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return target


__all__ = ["RunResult", "run_pipeline"]
