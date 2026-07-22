"""Pipeline scheduler — runs a :class:`CompiledPipeline` end-to-end.

Topologically iterates the pipeline (the compiler already topo-sorted),
running each step against each leaf (``per_leaf``) or once
(``corpus_wide`` / ``cross_leaf``). Accumulates upstream outputs by
``output_key`` so downstream ``{{upstream.X}}`` placeholders resolve.

Capabilities:

  - Topological dispatch via :func:`run_pipeline`.
  - Per-step retry budgets (logic + crash, separate) and same-error
    short-circuit via :func:`execute_step_with_retry`.
  - Optional per-step heartbeat to stderr via ``progress=True``.
  - Run trace written to
    ``runs/composer/<YYYY-MM-DDThh-mm-ss>_<skill>.json`` when
    ``runs_dir`` is set.
  - INFRA-role steps are skipped (informational glue, no LLM dispatch).

Out of scope:

  - Cross-leaf scoping is treated as corpus_wide for now.
  - APPLY-mode ``{{existing.Z}}`` pre-fetch — the materializer reads
    existing files at write time when needed.
  - Column-oriented batching (group N ``per_leaf`` instances into one
    LLM call) — defer until backend pricing motivates it.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import json
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Literal, Sequence

from tessellum.composer.compiler import CompiledPipeline, CompiledStep
from tessellum.composer.executor import (
    MAX_CRASH_RECOVERIES,
    MAX_LOGIC_RETRIES,
    StepResult,
    execute_step_with_retry,
)
from tessellum.composer.fix import FixContext, run_fix_loop
from tessellum.composer.gates import GateSuite, GroundingVerdict
from tessellum.composer.llm import LLMBackend
from tessellum.composer.manifest import AttemptRecord, Manifest
from tessellum.composer.materializer import MaterializedOutput


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
    max_logic_retries: int = MAX_LOGIC_RETRIES,
    max_crash_recoveries: int = MAX_CRASH_RECOVERIES,
    progress: bool = False,
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

    # Count non-INFRA steps for progress lines.
    runnable_steps = [s for s in pipeline.steps if s.role != "INFRA"]
    total_runnable = len(runnable_steps)
    runnable_index = 0

    for step in pipeline.steps:
        if step.role == "INFRA":
            continue

        runnable_index += 1
        per_leaf = step.aggregation == "per_leaf"
        scope_leaves = leaves if per_leaf else [{"_id": "corpus"}]
        step_started = time.monotonic()
        if progress:
            scope_n = len(scope_leaves)
            scope_kind = f"per_leaf × {scope_n}" if per_leaf else "corpus_wide"
            print(
                f"[composer] step {runnable_index}/{total_runnable} "
                f"{step.section_id} starting ({scope_kind})",
                file=__import__("sys").stderr,
                flush=True,
            )

        # Collect this step's outputs (per leaf or single corpus value)
        # to feed into ``upstream`` after the step completes. For
        # per_leaf steps, we expose a list of structured outputs under
        # the output_key (so downstream steps see all leaves at once
        # if they need to). For corpus_wide steps, expose the single dict.
        per_step_outputs: list[dict] = []

        for leaf in scope_leaves:
            # Use the retry-budgeted executor. Budgets default to
            # MAX_LOGIC_RETRIES + MAX_CRASH_RECOVERIES; callers that
            # explicitly want the no-retry behaviour can pass
            # max_logic_retries=0 + max_crash_recoveries=0.
            result = execute_step_with_retry(
                step,
                leaf=leaf,
                upstream=upstream,
                backend=backend,
                vault_root=vault_root,
                dry_run=dry_run,
                max_logic_retries=max_logic_retries,
                max_crash_recoveries=max_crash_recoveries,
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

        if progress:
            step_elapsed = time.monotonic() - step_started
            step_errors = sum(
                1
                for r in step_results
                if r.section_id == step.section_id and r.error is not None
            )
            print(
                f"[composer] step {runnable_index}/{total_runnable} "
                f"{step.section_id} done — {len(scope_leaves)} leaves, "
                f"{step_elapsed:.1f}s, {step_errors} errors",
                file=__import__("sys").stderr,
                flush=True,
            )

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


# ── Typed discriminated-union outcome ───────────────────────────────────────


StepOutcomeKind = Literal[
    "SUCCESS",
    "RETRY_EXHAUSTED",
    "WATCHDOG_KILLED",
    "SAME_ERROR_LOOP",
    "CONTRACT_VIOLATION",
    "BUDGET_EXHAUSTED",
]
"""The closed set of terminal outcomes for a single (step × leaf) run.

- ``SUCCESS`` — clean result; the materialized artifact is readable.
- ``RETRY_EXHAUSTED`` — the executor burned its logic/crash retry budget.
- ``WATCHDOG_KILLED`` — the per-step watchdog timeout fired (stall).
- ``SAME_ERROR_LOOP`` — the same-error short-circuit tripped.
- ``CONTRACT_VIOLATION`` — schema / materializer / prompt-cap failure
  (a logic/contract defect, distinct from an infra flake).
- ``BUDGET_EXHAUSTED`` — a *global* run-level invocation/token budget
  halted the run. Never produced by :func:`classify_outcome` (a single
  ``StepResult`` can't see the global budget); emitted by the Phase 5
  budget layer. Present here so the union is closed up-front.
"""


@dataclass(frozen=True)
class StepOutcome:
    """A typed, discriminated outcome derived from a :class:`StepResult`.

    The artifact is *readable only on* ``SUCCESS`` — accessing
    :attr:`artifact` on any failure kind raises, so a caller can't
    accidentally consume a note that never validated (CC's
    discriminated-union discipline). Cost/duration/attempts are recorded
    on **every** outcome, success or failure, for the ``statistics.json``
    rollup.

    Attributes:
        kind: One of :data:`StepOutcomeKind`.
        section_id: The step that ran.
        leaf_id: The leaf id (``None`` for corpus/cross-leaf steps).
        attempts: How many attempts ran (mirrors ``StepResult.attempts``).
        elapsed_ms: Wall-clock for the (final) attempt.
        error_class: The fine-grained :func:`classify_error` class, or
            ``None`` on success.
        error: The raw error string, or ``None`` on success.
    """

    kind: StepOutcomeKind
    section_id: str
    leaf_id: str | None
    attempts: int
    elapsed_ms: float
    error_class: str | None = None
    error: str | None = None
    _artifact: MaterializedOutput | None = None

    @property
    def is_success(self) -> bool:
        return self.kind == "SUCCESS"

    @property
    def artifact(self) -> MaterializedOutput:
        """The materialized output — readable only on ``SUCCESS``.

        Raises:
            ValueError: If the outcome is not ``SUCCESS`` (the artifact
                of a failed step is meaningless and must not be consumed).
        """
        if self.kind != "SUCCESS" or self._artifact is None:
            raise ValueError(
                f"artifact is only readable on SUCCESS; this outcome is {self.kind}"
            )
        return self._artifact


def classify_outcome(result: StepResult) -> StepOutcome:
    """Map a :class:`StepResult` onto a typed :class:`StepOutcome`.

    Pure and deterministic — a program decision (IDENT-3), no LLM. The
    mapping reads the executor's terminal ``error`` string (the same
    markers :func:`~tessellum.composer.executor.execute_step_with_retry`
    emits) with a precedence that surfaces the *proximate* cause:

    1. ``same-error loop`` marker → ``SAME_ERROR_LOOP``.
    2. ``stalled after`` marker → ``WATCHDOG_KILLED`` (even when the
       stall also exhausted the crash budget — the timeout is the root).
    3. validation / contract markers (or ``error_class == "validation"``)
       → ``CONTRACT_VIOLATION``. Checked *before* the budget marker so a
       schema/contract defect that exhausted its retry budget still
       surfaces as the actionable contract violation (route to fix), not
       a generic budget exhaustion.
    4. ``budget exhausted`` marker → ``RETRY_EXHAUSTED``.
    5. anything else with an error → ``RETRY_EXHAUSTED`` (generic).

    ``BUDGET_EXHAUSTED`` is intentionally never produced here — a single
    step can't observe the global budget; the Phase 5 budget layer emits
    it directly.
    """
    if result.error is None:
        return StepOutcome(
            kind="SUCCESS",
            section_id=result.section_id,
            leaf_id=result.leaf_id,
            attempts=result.attempts,
            elapsed_ms=result.elapsed_ms,
            error_class=None,
            error=None,
            _artifact=result.materialized,
        )

    e = result.error.lower()
    if "same-error loop" in e:
        kind: StepOutcomeKind = "SAME_ERROR_LOOP"
    elif "stalled after" in e:
        kind = "WATCHDOG_KILLED"
    elif (
        result.error_class == "validation"
        or "prompt exceeded" in e
        or "schema" in e
        or "materializer" in e
        or "contract" in e
    ):
        # Checked before the budget marker: a contract defect that
        # burned its retry budget is still a contract violation (the
        # actionable, fix-routable cause), not a generic exhaustion.
        kind = "CONTRACT_VIOLATION"
    elif "budget exhausted" in e:
        kind = "RETRY_EXHAUSTED"
    else:
        kind = "RETRY_EXHAUSTED"

    return StepOutcome(
        kind=kind,
        section_id=result.section_id,
        leaf_id=result.leaf_id,
        attempts=result.attempts,
        elapsed_ms=result.elapsed_ms,
        error_class=result.error_class,
        error=result.error,
    )


# ── Pure ready-set computation ──────────────────────────────────────────────


SkipReasonKind = Literal[
    "deps_unmet",
    "concurrency_capped",
    "contract_gate_failed",
    "no_input",
]
"""The closed enum of reasons a step is *not* promoted this round.

- ``deps_unmet`` — one or more ``depends_on`` steps are not yet ``done``.
- ``concurrency_capped`` — ready, but no promotion slot remains this call.
- ``contract_gate_failed`` — a compile/preflight gate rejected the step
  (emitted by the driver / Gate Engine, not by :func:`compute_ready_set`).
- ``no_input`` — a ``per_leaf`` step with an empty leaf scope (emitted by
  the driver).
"""


@dataclass(frozen=True)
class SkipReason:
    """Why a step was skipped in a given :func:`compute_ready_set` call."""

    section_id: str
    reason: SkipReasonKind


@dataclass(frozen=True)
class ReadySetState:
    """The pure input to :func:`compute_ready_set`.

    Attributes:
        steps: ``(section_id, depends_on)`` pairs in topological order.
        done: section_ids that have fully completed.
        in_flight: section_ids currently executing.
        concurrency_cap: max steps that may be promoted *this call*
            (remaining slots). ``0`` promotes nothing.
    """

    steps: tuple[tuple[str, tuple[str, ...]], ...]
    done: frozenset[str]
    in_flight: frozenset[str]
    concurrency_cap: int


def compute_ready_set(
    state: ReadySetState,
) -> tuple[tuple[str, ...], tuple[SkipReason, ...]]:
    """Decide which steps are ready to run — a pure functional core.

    A candidate is any step not already ``done`` or ``in_flight``. It is
    **promoted** iff all its ``depends_on`` are ``done`` *and* a promotion
    slot remains; otherwise it is **skipped** with a closed
    :class:`SkipReason` (``deps_unmet`` or ``concurrency_capped``). No
    I/O, no clock, no LLM — reproducible and unit-testable (a
    functional-core discipline). The effectful driver applies the result.

    Returns:
        ``(promoted, skipped)`` — ``promoted`` in topological order,
        ``skipped`` with one reason each. Steps already done/in-flight
        appear in neither list.
    """
    promoted: list[str] = []
    skipped: list[SkipReason] = []
    slots = state.concurrency_cap
    for sid, deps in state.steps:
        if sid in state.done or sid in state.in_flight:
            continue
        if any(d not in state.done for d in deps):
            skipped.append(SkipReason(sid, "deps_unmet"))
            continue
        if slots <= 0:
            skipped.append(SkipReason(sid, "concurrency_capped"))
            continue
        promoted.append(sid)
        slots -= 1
    return tuple(promoted), tuple(skipped)


# ── Self-claiming dynamic scheduler ─────────────────────────────────────────


def run_pipeline_dynamic(
    pipeline: CompiledPipeline,
    *,
    leaves: list[dict] | None = None,
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool = False,
    runs_dir: Path | None = None,
    max_logic_retries: int = MAX_LOGIC_RETRIES,
    max_crash_recoveries: int = MAX_CRASH_RECOVERIES,
    max_workers: int = 4,
    manifest: Manifest | None = None,
    run_id: str | None = None,
    events_path: Path | None = None,
    stats_path: Path | None = None,
    close_gate: GateSuite | None = None,
    grounding_verifier: "Callable[[CompiledStep, dict, StepResult], GroundingVerdict] | None" = None,
    max_fix_rounds: int = 0,
    fixer: "Callable[[CompiledStep, dict, tuple], StepResult] | None" = None,
) -> RunResult:
    """Wave-parallel, self-claiming variant of :func:`run_pipeline`.

    Semantically byte-identical to :func:`run_pipeline` — same vault
    output, same per-leaf outcomes, same ordered ``RunResult`` — but the
    per-leaf executions of every ready step run **concurrently** through a
    shared worker pool instead of one-leaf-at-a-time. This removes the
    intra-step straggler stall (a slow leaf no longer serializes its
    siblings) while preserving the step-level ``upstream`` accumulation
    barrier that data dependencies require.

    Mechanics:

    - **Ready-set driven.** Each round, :func:`compute_ready_set` promotes
      every step whose ``depends_on`` are ``done`` (independent steps run
      together); the round's ``(step × leaf)`` tasks are submitted to one
      :class:`~concurrent.futures.ThreadPoolExecutor`. Its internal work
      queue *is* the self-claiming queue — an idle worker pulls the next
      task. ``upstream`` is published (on the main thread, between rounds)
      only after a step's whole leaf scope completes, exactly as the
      serial path accumulates it, so downstream steps read an identical
      context.
    - **Manifest claim (optional).** When a ``manifest`` is supplied, each
      task ``claim``s its ``"{section_id}::{leaf_id}"`` key (compare-and-
      swap, double-dispatch safe) and, on success, records an
      :class:`~tessellum.composer.manifest.AttemptRecord` + ``mark_done``
      *before* releasing — the durable-commit-before-release ordering. The
      manifest is a crash-safety projection here; output-reconstruction on
      resume (skip-a-done-leaf) is deferred to a later phase, so a fresh
      run always executes every task (identical to serial).
    - **Observability.** When ``events_path`` is set, a
      machine-readable per-leaf lifecycle event is appended per task; when
      ``stats_path`` is set, a final ``statistics.json`` rollup is written.
    - **Per-session close-gate (opt-in).** When a ``close_gate``
      is supplied, each task that materialized a note is a *session*:
      after capture it runs the close-gate against the written note
      (``format`` + ``grounding`` via the ``grounding_verifier``); the
      session closes ``done`` **only on gate PASS**. On FAIL it routes to
      the ``fixer`` up to ``max_fix_rounds`` times, then closes
      ``blocked`` (never silently ``done`` — the lifecycle-terminator
      invariant). Gate-then-commit: the note file is written during
      capture, but the manifest row flips ``done`` and the ``StepResult``
      is treated as clean **only after** the gate passes; a gate FAIL
      turns an otherwise-clean capture into an errored result. When
      ``close_gate`` is ``None`` (the default) this whole path is skipped
      — parity with the pre-Phase-3 behaviour is preserved.

    Determinism: ``step_results`` are sorted by ``(topological step index,
    leaf index)`` before the :class:`RunResult` is built, so the tuple
    order matches the serial path regardless of completion order.

    Args:
        max_workers: Worker-pool size (leaf-level concurrency ceiling).
        manifest: Optional resume manifest for claim/attempt recording.
        run_id: This run's uuid (for owner-scoped manifest ops). A fresh
            uuid is generated when ``None``.
        events_path: Optional sidecar for the lifecycle event stream.
        stats_path: Optional path for the final ``statistics.json``.
        close_gate: Optional per-session close :class:`GateSuite`. When
            set, every session that wrote a note file must pass it to
            close ``done`` (else ``blocked``). ``None`` = no gating.
        grounding_verifier: Callable ``(step, leaf, result) ->
            GroundingVerdict`` — the read-only semantic verifier the
            ``grounding`` predicate consumes. Required only if the
            ``close_gate`` includes a ``grounding`` gate; a ``None``
            verifier makes grounding fail-closed.
        max_fix_rounds: Max close-gate fix retries per session (0 = no
            fix loop; a first FAIL closes ``blocked``).
        fixer: Callable ``(step, leaf, issues) -> StepResult`` invoked on
            a close-gate FAIL to repair the note in place. ``None`` skips
            the fix loop.

    Returns:
        RunResult — byte-comparable to :func:`run_pipeline`'s (modulo the
        wall-clock ``started_at`` / ``duration_seconds`` / ``trace_path``).
    """
    started = time.monotonic()
    started_iso = dt.datetime.now(dt.UTC).isoformat()
    run_id = run_id or uuid.uuid4().hex

    if leaves is None or not leaves:
        leaves = [{"_id": "corpus"}]
    else:
        for i, leaf in enumerate(leaves):
            if "_id" not in leaf:
                leaf["_id"] = f"leaf_{i}"

    # Topological index for every runnable (non-INFRA) step — the sort key
    # that reproduces the serial step_results ordering.
    runnable = [s for s in pipeline.steps if s.role != "INFRA"]
    topo_index = {s.section_id: i for i, s in enumerate(runnable)}
    by_id = {s.section_id: s for s in runnable}

    upstream: dict[str, Any] = {}
    # results keyed by (topo_step_index, leaf_index) → StepResult
    results: dict[tuple[int, int], StepResult] = {}
    events: list[dict] = []
    lock = threading.Lock()

    def _scope_leaves(step: CompiledStep) -> list[dict]:
        return leaves if step.aggregation == "per_leaf" else [{"_id": "corpus"}]

    def _run_task(step: CompiledStep, leaf: dict, leaf_index: int) -> None:
        key = f"{step.section_id}::{leaf.get('_id')}"
        if manifest is not None:
            with lock:
                manifest.claim(key, run_id=run_id, now=started)
        result = execute_step_with_retry(
            step,
            leaf=leaf,
            upstream=upstream,
            backend=backend,
            vault_root=vault_root,
            dry_run=dry_run,
            max_logic_retries=max_logic_retries,
            max_crash_recoveries=max_crash_recoveries,
        )

        # Per-session close-gate. Only when a close_gate is
        # supplied AND the capture produced a clean, materialized note —
        # a capture that already errored stays errored (gate can't repair
        # a note that wasn't written). Gate-then-commit: the note file
        # exists (written during capture), but this determines whether the
        # session closes ``done`` or ``blocked``.
        gate_cause: str | None = None
        if close_gate is not None and result.error is None:
            result, gate_cause = _run_close_gate(
                step=step,
                leaf=leaf,
                result=result,
                close_gate=close_gate,
                grounding_verifier=grounding_verifier,
                fixer=fixer,
                max_fix_rounds=max_fix_rounds,
                backend=backend,
                vault_root=vault_root,
                dry_run=dry_run,
            )

        outcome = classify_outcome(result)
        with lock:
            results[(topo_index[step.section_id], leaf_index)] = result
            if manifest is not None:
                manifest.add_attempt(
                    key,
                    AttemptRecord(
                        attempt_n=result.attempts,
                        outcome=(
                            "success"
                            if result.error is None
                            else (gate_cause or result.error_class or "crash")
                        ),
                        at=started,
                    ),
                )
                # Gate-then-commit: mark done only on a clean (gate-passed)
                # result; a gate FAIL closes the session ``blocked``, never
                # silently ``done`` (lifecycle-terminator invariant).
                if result.error is None:
                    manifest.mark_done(key)
                elif gate_cause is not None:
                    manifest.mark_blocked(key, blocked_by=())
                if manifest.path is not None:
                    manifest.save()
            if events_path is not None:
                events.append(
                    {
                        "section_id": step.section_id,
                        "leaf_id": leaf.get("_id"),
                        "outcome": outcome.kind,
                        "attempts": outcome.attempts,
                        "elapsed_ms": outcome.elapsed_ms,
                        "error_class": outcome.error_class,
                    }
                )

    # Ready-set loop over STEPS. Within a round every ready step's leaves
    # are dispatched together; upstream is published after the round.
    step_topo = tuple((s.section_id, s.depends_on) for s in runnable)
    done_steps: set[str] = set()
    with ThreadPoolExecutor(
        max_workers=max_workers, thread_name_prefix="composer-leaf"
    ) as pool:
        while len(done_steps) < len(runnable):
            promoted, _skipped = compute_ready_set(
                ReadySetState(
                    steps=step_topo,
                    done=frozenset(done_steps),
                    in_flight=frozenset(),
                    concurrency_cap=len(runnable),  # leaf pool bounds real parallelism
                )
            )
            if not promoted:  # pragma: no cover — compiler guarantees a DAG
                break
            futures = []
            for sid in promoted:
                step = by_id[sid]
                for leaf_index, leaf in enumerate(_scope_leaves(step)):
                    futures.append(pool.submit(_run_task, step, leaf, leaf_index))
            for fut in as_completed(futures):
                fut.result()  # propagate unexpected framework errors

            # Publish upstream for each step just completed (topo order).
            for sid in promoted:
                step = by_id[sid]
                if step.output_key:
                    scope = _scope_leaves(step)
                    per_leaf = step.aggregation == "per_leaf"
                    outs = [
                        results[(topo_index[sid], i)].materialized.structured
                        for i in range(len(scope))
                        if results[(topo_index[sid], i)].error is None
                    ]
                    if outs:
                        upstream[step.output_key] = outs if per_leaf else outs[0]
                done_steps.add(sid)

    # Rebuild ordered step_results to match the serial path exactly.
    step_results = [results[k] for k in sorted(results.keys())]
    error_count = sum(1 for r in step_results if r.error is not None)
    duration = time.monotonic() - started

    if events_path is not None:
        events_path.parent.mkdir(parents=True, exist_ok=True)
        events_path.write_text(
            "".join(json.dumps(ev) + "\n" for ev in events), encoding="utf-8"
        )
    if stats_path is not None:
        _write_statistics(
            stats_path=stats_path,
            pipeline=pipeline,
            step_results=step_results,
            duration=duration,
        )

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


def _run_close_gate(
    *,
    step: CompiledStep,
    leaf: dict,
    result: StepResult,
    close_gate: GateSuite,
    grounding_verifier: "Callable[[CompiledStep, dict, StepResult], GroundingVerdict] | None",
    fixer: "Callable[[CompiledStep, dict, tuple], StepResult] | None",
    max_fix_rounds: int,
    backend: LLMBackend,
    vault_root: Path,
    dry_run: bool,
) -> tuple[StepResult, str | None]:
    """Gate a materialized note; fix-loop on FAIL; return (result, cause).

    A session closes on a close-gate PASS. The gate runs against the
    note file the capture wrote (``files_written`` / ``files_applied``);
    a session that wrote no file (a corpus/no-op step) has nothing to
    gate and passes through untouched. On FAIL, the ``fixer`` (if any) is
    invoked up to ``max_fix_rounds`` times, re-gating after each; if it
    still fails, the clean ``StepResult`` is rewritten into an errored one
    whose ``error`` names the terminal gate cause, so ``error_count`` and
    ``classify_outcome`` reflect the blocked session.

    Returns:
        ``(result, gate_cause)`` — ``gate_cause`` is ``None`` on PASS (or
        when there was no note to gate), else the first failing gate's
        cause tag (the session is ``blocked``).
    """
    note_paths = list(result.materialized.files_written) + list(
        result.materialized.files_applied
    )
    if not note_paths:
        return result, None  # nothing to gate (corpus/no-op step)
    note_path = note_paths[0]

    def _evaluate() -> tuple[bool, str | None, tuple]:
        verdict = (
            grounding_verifier(step, leaf, result)
            if grounding_verifier is not None
            else None
        )
        composite = close_gate.evaluate(note_path, verdict=verdict)
        return composite.passed, composite.first_failure_cause, composite.blocking_issues

    # The scheduler's fixer contract is (step, leaf, issues) -> anything;
    # adapt it to the informed-fix contract (FixContext) the fix loop uses.
    # The fix loop owns the checkpoint-before-fix + revert-to-BEST safety;
    # the fixer only repairs the note in place. Prior-attempt outcomes ride
    # inside the FixContext so the fixer is informed, not blind.
    informed_fixer = None
    if fixer is not None:

        def informed_fixer(ctx: FixContext) -> object:  # noqa: F811 — local closure
            return fixer(step, leaf, ctx.issues)

    loop = run_fix_loop(
        note_path=Path(note_path),
        evaluate=_evaluate,
        fixer=informed_fixer,
        max_rounds=max_fix_rounds,
    )

    if loop.passed:
        return result, None

    # Blocked: rewrite the clean result into an errored one so the run's
    # error_count + typed outcome reflect the failed session. The fix loop
    # has already restored the BEST-scoring snapshot to disk if a later
    # attempt regressed, so the note left behind is the best version seen.
    blocked = dataclasses.replace(
        result,
        error=(
            f"close-gate blocked ({loop.cause}): "
            f"{loop.final_score} blocking issue(s)"
            + (" [reverted to best]" if loop.reverted else "")
        ),
        error_class="validation",
    )
    return blocked, loop.cause


def _write_statistics(
    *,
    stats_path: Path,
    pipeline: CompiledPipeline,
    step_results: Sequence[StepResult],
    duration: float,
) -> Path:
    """Write the final ``statistics.json`` rollup.

    Per-stage processed/succeeded/failed counts + a total-duration line,
    keyed by ``section_id``. A machine-readable summary distinct from the
    per-leaf event stream and the human trace.
    """
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    per_stage: dict[str, dict[str, int]] = {}
    for r in step_results:
        bucket = per_stage.setdefault(
            r.section_id, {"processed": 0, "succeeded": 0, "failed": 0}
        )
        bucket["processed"] += 1
        if r.error is None:
            bucket["succeeded"] += 1
        else:
            bucket["failed"] += 1
    payload = {
        "skill_name": pipeline.skill_name,
        "duration_seconds": duration,
        "invocation_count": len(step_results),
        "error_count": sum(1 for r in step_results if r.error is not None),
        "per_stage": per_stage,
    }
    stats_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return stats_path


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
                # Retry telemetry
                "attempts": r.attempts,
                "retry_kind_history": list(r.retry_kind_history),
            }
            for r in step_results
        ],
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return target


__all__ = [
    "RunResult",
    "run_pipeline",
    "run_pipeline_dynamic",
    "compute_ready_set",
    "ReadySetState",
    "SkipReason",
    "SkipReasonKind",
    "StepOutcome",
    "StepOutcomeKind",
    "classify_outcome",
]
