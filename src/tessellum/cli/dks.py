"""``tessellum dks`` — Dialectic Knowledge System multi-cycle CLI.

Phase 3 of ``plans/plan_dks_implementation.md``. Lifted to a top-level
subcommand in v0.0.43 to reflect DKS's status as a peer runtime to
``tessellum composer`` (the contract-pipeline executor), not a feature
inside it. DKS uses Composer's LLMBackend abstractions but is otherwise
independent.

```bash
tessellum dks <observations.jsonl>
    [--initial-warrants <warrants.json>]
    [--backend {mock,anthropic}] [--model <id>]
    [--mock-responses <responses.json>]
    [--runs-dir <dir>] [--no-trace]
    [--format {human,json}]
```

JSONL: one observation per non-blank line. Required string field
``summary``. Optional ``timestamp``, ``mode`` (``"fresh"|"extend"|"branch"``,
default ``"fresh"``), ``parent_fz`` (required for ``extend``/``branch``).

Writes per-cycle trace to ``<runs-dir>/<UTC-ts>_cycle_<FZ>.json`` and
an aggregate trace to ``<runs-dir>/<UTC-ts>_aggregate.json`` unless
``--no-trace`` is set.

Exit codes:
    0  run completed (zero cycles is allowed when JSONL is empty)
    2  invocation error (file missing, bad JSON, invalid mode, etc.)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from tessellum.composer import LLMBackend, MockBackend
from tessellum.dks import (
    DKSObservation,
    DKSRunner,
    DKSWarrant,
    aggregate_warrant_changes,
    allocate_cycle_fz,
)


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    dks = subparsers.add_parser(
        "dks",
        help="Run a multi-cycle DKS session over a JSONL of observations.",
    )
    dks.add_argument(
        "observations",
        type=Path,
        help="JSONL file — one observation object per line "
        '({"summary": "...", optional "timestamp", "mode", "parent_fz"}).',
    )
    dks.add_argument(
        "--initial-warrants",
        type=Path,
        help="Optional JSON file with a list of starting warrant objects "
        '(each: {"claim", "data", "warrant", "backing"?, "qualifier"?, "rebuttal"?}).',
    )
    dks.add_argument(
        "--backend",
        choices=["mock", "anthropic"],
        default="mock",
        help="LLM backend (default: mock — no network). `anthropic` requires "
        "the [agent] extras (`pip install tessellum[agent]`) and the "
        "ANTHROPIC_API_KEY environment variable.",
    )
    dks.add_argument(
        "--model",
        default="claude-sonnet-4-6",
        help="Anthropic model ID (only used when --backend=anthropic).",
    )
    dks.add_argument(
        "--mock-responses",
        type=Path,
        help="JSON file mapping prompt-substring patterns to canned response text "
        "(MockBackend only).",
    )
    dks.add_argument(
        "--runs-dir",
        type=Path,
        default=Path("runs") / "dks",
        help="Where to write per-cycle + aggregate trace JSON (default: ./runs/dks/). "
        "Pass --no-trace to skip writing.",
    )
    dks.add_argument(
        "--no-trace",
        action="store_true",
        help="Skip writing trace files to --runs-dir.",
    )
    dks.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    dks.set_defaults(func=run_dks_cli)


def run_dks_cli(args: argparse.Namespace) -> int:
    obs_path: Path = args.observations.expanduser().resolve()
    if not obs_path.is_file():
        print(
            f"tessellum dks: {obs_path} does not exist or is not a file",
            file=sys.stderr,
        )
        return 2

    try:
        raw = obs_path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"tessellum dks: failed to read {obs_path}: {e}", file=sys.stderr)
        return 2

    observation_specs: list[dict] = []
    for lineno, line in enumerate(raw.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            entry = json.loads(stripped)
        except json.JSONDecodeError as e:
            print(
                f"tessellum dks: {obs_path}:{lineno} invalid JSON: {e}",
                file=sys.stderr,
            )
            return 2
        if not isinstance(entry, dict):
            print(
                f"tessellum dks: {obs_path}:{lineno} must be a JSON object, "
                f"got {type(entry).__name__}",
                file=sys.stderr,
            )
            return 2
        if "summary" not in entry or not isinstance(entry["summary"], str):
            print(
                f"tessellum dks: {obs_path}:{lineno} missing required string field 'summary'",
                file=sys.stderr,
            )
            return 2
        observation_specs.append(entry)

    if not observation_specs:
        if args.output_format == "json":
            print(
                json.dumps(
                    {
                        "cycles": [],
                        "warrant_changes": [],
                        "summary": {
                            "cycle_count": 0,
                            "closed_loop_count": 0,
                            "added": 0,
                            "revised": 0,
                            "superseded": 0,
                        },
                    },
                    indent=2,
                )
            )
        else:
            print(f"tessellum dks: {obs_path} has no observations — nothing to run.")
        return 0

    existing_trails: list[str] = []
    observations: list[DKSObservation] = []
    for i, spec in enumerate(observation_specs):
        mode = spec.get("mode", "fresh")
        if mode not in ("fresh", "extend", "branch"):
            print(
                f"tessellum dks: observation #{i + 1} has invalid mode={mode!r}; "
                f"expected one of fresh|extend|branch",
                file=sys.stderr,
            )
            return 2
        parent_fz = spec.get("parent_fz")
        try:
            fz = allocate_cycle_fz(
                tuple(existing_trails), mode=mode, parent_fz=parent_fz
            )
        except ValueError as e:
            print(
                f"tessellum dks: observation #{i + 1} FZ allocation failed: {e}",
                file=sys.stderr,
            )
            return 2
        existing_trails.append(fz)
        observations.append(
            DKSObservation(
                folgezettel=fz,
                summary=spec["summary"],
                timestamp=spec.get("timestamp"),
            )
        )

    initial_warrants: tuple = ()
    if args.initial_warrants is not None:
        wpath = args.initial_warrants.expanduser().resolve()
        if not wpath.is_file():
            print(
                f"tessellum dks: --initial-warrants {wpath} not found",
                file=sys.stderr,
            )
            return 2
        try:
            w_data = json.loads(wpath.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(
                f"tessellum dks: --initial-warrants unreadable: {e}",
                file=sys.stderr,
            )
            return 2
        if not isinstance(w_data, list):
            print(
                "tessellum dks: --initial-warrants must be a JSON list",
                file=sys.stderr,
            )
            return 2
        try:
            initial_warrants = tuple(
                DKSWarrant(
                    claim=str(w.get("claim", "")),
                    data=str(w.get("data", "")),
                    warrant=str(w.get("warrant", "")),
                    backing=str(w.get("backing", "")),
                    qualifier=str(w.get("qualifier", "")),
                    rebuttal=str(w.get("rebuttal", "")),
                )
                for w in w_data
            )
        except (TypeError, AttributeError) as e:
            print(
                f"tessellum dks: --initial-warrants malformed entries: {e}",
                file=sys.stderr,
            )
            return 2

    backend: LLMBackend
    if args.backend == "anthropic":
        try:
            from tessellum.composer import AnthropicBackend

            backend = AnthropicBackend(model=args.model)
        except ImportError as e:
            print(
                "tessellum dks: --backend=anthropic requires the "
                "[agent] extras: pip install tessellum[agent]",
                file=sys.stderr,
            )
            print(f"  ({e})", file=sys.stderr)
            return 2
    else:
        responses: dict[str, str] = {}
        if args.mock_responses is not None:
            try:
                responses = json.loads(
                    args.mock_responses.expanduser().resolve().read_text(
                        encoding="utf-8"
                    )
                )
            except (OSError, json.JSONDecodeError) as e:
                print(
                    f"tessellum dks: --mock-responses unreadable: {e}",
                    file=sys.stderr,
                )
                return 2
            if not isinstance(responses, dict):
                print(
                    "tessellum dks: --mock-responses must be a JSON object",
                    file=sys.stderr,
                )
                return 2
        backend = MockBackend(responses=responses)

    runner = DKSRunner(
        observations=tuple(observations),
        backend=backend,
        initial_warrants=initial_warrants,
    )
    result = runner.run()

    trace_paths: list[Path] = []
    aggregate_path: Path | None = None
    if not args.no_trace:
        runs_dir = args.runs_dir.expanduser().resolve()
        runs_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        for cycle in result.cycles:
            tp = runs_dir / f"{ts}_cycle_{cycle.cycle_id}.json"
            tp.write_text(
                json.dumps(_serialize_cycle(cycle), indent=2) + "\n",
                encoding="utf-8",
            )
            trace_paths.append(tp)

        aggregate_path = runs_dir / f"{ts}_aggregate.json"
        aggregate_path.write_text(
            json.dumps(
                _serialize_run(result, trace_paths, observation_specs, ts),
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    counts = aggregate_warrant_changes(result.warrant_changes)
    if args.output_format == "json":
        payload = {
            "cycle_count": result.cycle_count,
            "closed_loop_count": result.closed_loop_count,
            "duration_seconds": result.elapsed_ms / 1000.0,
            "summary": counts,
            "cycles": [_serialize_cycle(c) for c in result.cycles],
            "warrant_changes": [
                _serialize_change(c) for c in result.warrant_changes
            ],
            "trace_paths": [str(p) for p in trace_paths],
            "aggregate_path": str(aggregate_path) if aggregate_path else None,
        }
        print(json.dumps(payload, indent=2))
    else:
        print(
            f"dks: {result.cycle_count} cycle(s); "
            f"{result.closed_loop_count} closed loop; "
            f"{counts['added']} added, {counts['revised']} revised, "
            f"{counts['superseded']} superseded; "
            f"{result.elapsed_ms:.1f}ms"
        )
        for c in result.cycles:
            tag = "CLOSED" if c.closed_loop else " SHORT"
            print(
                f"  {tag}  FZ {c.cycle_id}  "
                f"nodes={len(c.folgezettel_nodes)}  "
                f"{c.elapsed_ms:.1f}ms"
            )
        if trace_paths:
            print()
            print(f"  traces: {len(trace_paths)} cycle file(s) + aggregate")
            print(f"  aggregate: {aggregate_path}")

    return 0


def _serialize_cycle(cycle) -> dict:
    """Flatten a DKSCycleResult to a JSON-safe dict for trace files."""

    def _w(w):
        if w is None:
            return None
        return {
            "claim": w.claim,
            "data": w.data,
            "warrant": w.warrant,
            "backing": w.backing,
            "qualifier": w.qualifier,
            "rebuttal": w.rebuttal,
        }

    def _arg(a):
        return {
            "folgezettel": a.folgezettel,
            "warrant": _w(a.warrant),
            "evidence": a.evidence,
        }

    return {
        "cycle_id": cycle.cycle_id,
        "mode": cycle.mode,
        "closed_loop": cycle.closed_loop,
        "elapsed_ms": cycle.elapsed_ms,
        "backend_id": cycle.backend_id,
        "folgezettel_nodes": list(cycle.folgezettel_nodes),
        "observation": {
            "folgezettel": cycle.observation.folgezettel,
            "summary": cycle.observation.summary,
            "timestamp": cycle.observation.timestamp,
        },
        "argument_a": _arg(cycle.argument_a),
        "argument_b": _arg(cycle.argument_b),
        "contradicts": (
            None
            if cycle.contradicts is None
            else {
                "attacker_fz": cycle.contradicts.attacker_fz,
                "attacked_fz": cycle.contradicts.attacked_fz,
                "reason": cycle.contradicts.reason,
            }
        ),
        "counter": (
            None
            if cycle.counter is None
            else {
                "folgezettel": cycle.counter.folgezettel,
                "attacked_fz": cycle.counter.attacked_fz,
                "broken_component": cycle.counter.broken_component,
                "counter_claim": cycle.counter.counter_claim,
                "reason": cycle.counter.reason,
                "strength": cycle.counter.strength,
            }
        ),
        "pattern": (
            None
            if cycle.pattern is None
            else {
                "folgezettel": cycle.pattern.folgezettel,
                "description": cycle.pattern.description,
                "observed": list(cycle.pattern.observed),
            }
        ),
        "rule_revision": (
            None
            if cycle.rule_revision is None
            else {
                "folgezettel": cycle.rule_revision.folgezettel,
                "revised_warrant": _w(cycle.rule_revision.revised_warrant),
                "supersedes": cycle.rule_revision.supersedes,
            }
        ),
    }


def _serialize_change(change) -> dict:
    return {
        "cycle_id": change.cycle_id,
        "kind": change.kind,
        "revision_fz": change.revision_fz,
        "superseded_fz": change.superseded_fz,
        "warrant": (
            None
            if change.warrant is None
            else {
                "claim": change.warrant.claim,
                "data": change.warrant.data,
                "warrant": change.warrant.warrant,
                "backing": change.warrant.backing,
                "qualifier": change.warrant.qualifier,
                "rebuttal": change.warrant.rebuttal,
            }
        ),
    }


def _serialize_run(
    result,
    trace_paths: list[Path],
    observation_specs: list[dict],
    timestamp: str,
) -> dict:
    counts = aggregate_warrant_changes(result.warrant_changes)
    return {
        "timestamp": timestamp,
        "cycle_count": result.cycle_count,
        "closed_loop_count": result.closed_loop_count,
        "duration_seconds": result.elapsed_ms / 1000.0,
        "backend_id": result.backend_id,
        "summary": counts,
        "observation_specs": observation_specs,
        "cycle_traces": [str(p) for p in trace_paths],
        "warrant_changes": [_serialize_change(c) for c in result.warrant_changes],
        "final_warrants": [
            {
                "claim": w.claim,
                "data": w.data,
                "warrant": w.warrant,
                "backing": w.backing,
                "qualifier": w.qualifier,
                "rebuttal": w.rebuttal,
            }
            for w in result.final_warrants
        ],
    }
