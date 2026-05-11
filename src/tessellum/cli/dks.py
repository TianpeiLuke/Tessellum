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
    ConstantConfidence,
    DKSObservation,
    DKSRunner,
    DKSWarrant,
    WarrantHistory,
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
        nargs="?",
        help="JSONL file — one observation object per line "
        '({"summary": "...", optional "timestamp", "mode", "parent_fz"}). '
        "Optional when --report is passed.",
    )
    dks.add_argument(
        "--report",
        action="store_true",
        help="Inter-cycle telemetry mode (Phase 5): aggregate stats across "
        "every *_aggregate.json under --runs-dir and exit 0. Skips the "
        "observation run.",
    )
    dks.add_argument(
        "--report-last",
        type=int,
        default=None,
        help="With --report: aggregate only the most recent N runs (by "
        "aggregate-trace mtime). Default: all runs.",
    )
    dks.add_argument(
        "--include-bb-graph",
        action="store_true",
        help="With --report: join the per-run aggregate stats with "
        "`BBGraph.from_db()` corpus telemetry (node counts by BB type, "
        "edge counts by schema label, untyped-edge BB-pair tallies). "
        "Requires --bb-db or default index DB path.",
    )
    dks.add_argument(
        "--bb-db",
        type=Path,
        default=Path("data") / "tessellum.db",
        help="With --report --include-bb-graph: index DB to load the "
        "corpus BBGraph from. Default: ./data/tessellum.db. Ignored "
        "without --include-bb-graph.",
    )
    dks.add_argument(
        "--gate-confidence",
        type=float,
        default=None,
        help="Phase 5 confidence gate: force a constant confidence score "
        "(0.0-1.0) for every observation. When > --gate-threshold the "
        "cycle short-circuits to observation + argument A only. Useful "
        "for testing gating end-to-end without a learned model.",
    )
    dks.add_argument(
        "--gate-threshold",
        type=float,
        default=None,
        help="Override the default confidence gate threshold "
        "(tessellum.dks.DEFAULT_CONFIDENCE_THRESHOLD = 0.85). "
        "Ignored without --gate-confidence.",
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
    # Phase 5 — --report short-circuits to inter-cycle telemetry.
    if args.report:
        return _run_dks_report(args)

    if args.observations is None:
        print(
            "tessellum dks: missing observations file (or pass --report).",
            file=sys.stderr,
        )
        return 2

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

    # Phase 5 — confidence gating (opt-in). The `--gate-confidence` flag
    # wires a ConstantConfidence model that returns the same score for
    # every observation; useful for testing gating end-to-end without a
    # learned model. The threshold defaults to
    # DEFAULT_CONFIDENCE_THRESHOLD when --gate-threshold is omitted.
    confidence_model = None
    if args.gate_confidence is not None:
        if not 0.0 <= args.gate_confidence <= 1.0:
            print(
                f"tessellum dks: --gate-confidence must be in [0.0, 1.0]; "
                f"got {args.gate_confidence}",
                file=sys.stderr,
            )
            return 2
        confidence_model = ConstantConfidence(args.gate_confidence)

    runner = DKSRunner(
        observations=tuple(observations),
        backend=backend,
        initial_warrants=initial_warrants,
        confidence_model=confidence_model,
        confidence_threshold=args.gate_threshold,
    )
    result = runner.run()

    trace_paths: list[Path] = []
    aggregate_path: Path | None = None
    history_path: Path | None = None
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

        # Phase 5 — append warrant revisions to the persistent history log.
        if result.warrant_changes:
            history_path = runs_dir / "warrant_history.jsonl"
            WarrantHistory(history_path).record_changes(result.warrant_changes)

    counts = aggregate_warrant_changes(result.warrant_changes)
    gated_count = sum(1 for c in result.cycles if c.gated)
    if args.output_format == "json":
        payload = {
            "cycle_count": result.cycle_count,
            "gated_count": gated_count,
            "warrant_history_path": str(history_path) if history_path else None,
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
            f"{result.closed_loop_count} closed loop, "
            f"{gated_count} gated; "
            f"{counts['added']} added, {counts['revised']} revised, "
            f"{counts['superseded']} superseded; "
            f"{result.elapsed_ms:.1f}ms"
        )
        for c in result.cycles:
            if c.gated:
                tag = " GATED"
            elif c.closed_loop:
                tag = "CLOSED"
            else:
                tag = " SHORT"
            print(
                f"  {tag}  FZ {c.cycle_id}  "
                f"nodes={len(c.folgezettel_nodes)}  "
                f"{c.elapsed_ms:.1f}ms"
            )
        if trace_paths:
            print()
            print(f"  traces: {len(trace_paths)} cycle file(s) + aggregate")
            print(f"  aggregate: {aggregate_path}")
            if history_path is not None:
                print(f"  warrant history: {history_path}")

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
        "escalation_decision": cycle.escalation_decision,
        "confidence_score": cycle.confidence_score,
        "gated": cycle.gated,
        "elapsed_ms": cycle.elapsed_ms,
        "backend_id": cycle.backend_id,
        "folgezettel_nodes": list(cycle.folgezettel_nodes),
        "observation": {
            "folgezettel": cycle.observation.folgezettel,
            "summary": cycle.observation.summary,
            "timestamp": cycle.observation.timestamp,
        },
        "argument_a": _arg(cycle.argument_a),
        "argument_b": _arg(cycle.argument_b) if cycle.argument_b is not None else None,
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


# ── --report mode (Phase 5) ─────────────────────────────────────────────────


def _run_dks_report(args: argparse.Namespace) -> int:
    """Inter-cycle telemetry across past DKS runs.

    Scans ``--runs-dir`` for ``*_aggregate.json`` files (written by
    prior ``tessellum dks`` invocations) and aggregates: total cycles
    across all runs, closed-loop rate, gated-vs-full ratio, total
    warrant changes by kind, top-K most-attacked warrant FZs. Exits
    0 on success (empty runs-dir is treated as zero stats, not error).
    """
    runs_dir = args.runs_dir.expanduser().resolve()
    if not runs_dir.is_dir():
        if args.output_format == "json":
            print(json.dumps(_empty_report(runs_dir), indent=2))
        else:
            print(
                f"tessellum dks --report: no runs directory at {runs_dir} "
                f"(no prior dks runs to aggregate)."
            )
        return 0

    aggregates = sorted(
        runs_dir.glob("*_aggregate.json"),
        key=lambda p: p.stat().st_mtime,
    )
    if args.report_last is not None and args.report_last > 0:
        aggregates = aggregates[-args.report_last :]

    if not aggregates:
        if args.output_format == "json":
            print(json.dumps(_empty_report(runs_dir), indent=2))
        else:
            print(
                f"tessellum dks --report: {runs_dir} contains no "
                f"*_aggregate.json files (no prior dks runs to aggregate)."
            )
        return 0

    run_summaries: list[dict] = []
    total_cycles = 0
    total_closed = 0
    total_gated = 0
    total_added = 0
    total_revised = 0
    total_superseded = 0
    attacked_fz_counts: dict[str, int] = {}

    for path in aggregates:
        try:
            agg = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        cycle_count = int(agg.get("cycle_count", 0))
        closed = int(agg.get("closed_loop_count", 0))
        summary = agg.get("summary", {}) or {}
        added = int(summary.get("added", 0))
        revised = int(summary.get("revised", 0))
        superseded = int(summary.get("superseded", 0))

        # Phase 5 fields (only present for v0.0.45+ runs). Tolerant
        # of older trace files that don't have `gated_count` set.
        gated = 0
        for cycle_trace_path in agg.get("cycle_traces", []) or []:
            try:
                ct = json.loads(Path(cycle_trace_path).read_text(encoding="utf-8"))
                if ct.get("gated") or ct.get("escalation_decision") == "gated":
                    gated += 1
            except (OSError, json.JSONDecodeError):
                continue

        for change in agg.get("warrant_changes", []) or []:
            if change.get("kind") in ("revised", "superseded"):
                old_fz = change.get("superseded_fz")
                if old_fz:
                    attacked_fz_counts[old_fz] = attacked_fz_counts.get(old_fz, 0) + 1

        total_cycles += cycle_count
        total_closed += closed
        total_gated += gated
        total_added += added
        total_revised += revised
        total_superseded += superseded

        run_summaries.append(
            {
                "aggregate_path": str(path),
                "timestamp": agg.get("timestamp"),
                "cycle_count": cycle_count,
                "closed_loop_count": closed,
                "gated_count": gated,
                "added": added,
                "revised": revised,
                "superseded": superseded,
            }
        )

    top_attacked = sorted(
        attacked_fz_counts.items(), key=lambda kv: (-kv[1], kv[0])
    )[:10]
    closed_rate = total_closed / total_cycles if total_cycles else 0.0
    gated_rate = total_gated / total_cycles if total_cycles else 0.0

    report = {
        "runs_dir": str(runs_dir),
        "run_count": len(run_summaries),
        "total_cycles": total_cycles,
        "closed_loop_count": total_closed,
        "closed_loop_rate": round(closed_rate, 4),
        "gated_count": total_gated,
        "gated_rate": round(gated_rate, 4),
        "warrant_changes": {
            "added": total_added,
            "revised": total_revised,
            "superseded": total_superseded,
        },
        "top_attacked_warrant_fz": [
            {"fz": fz, "attacks": n} for fz, n in top_attacked
        ],
        "runs": run_summaries,
    }

    if getattr(args, "include_bb_graph", False):
        report["bb_graph"] = _build_bb_graph_section(args.bb_db)

    if args.output_format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(f"dks --report  ({len(run_summaries)} run(s) under {runs_dir})")
        print(
            f"  cycles: {total_cycles}  "
            f"({total_closed} closed = {closed_rate * 100:.1f}%, "
            f"{total_gated} gated = {gated_rate * 100:.1f}%)"
        )
        print(
            f"  warrant changes: "
            f"{total_added} added, {total_revised} revised, "
            f"{total_superseded} superseded"
        )
        if top_attacked:
            print()
            print("  top attacked warrant FZs:")
            for fz, n in top_attacked:
                print(f"    {n:>3}×  FZ {fz}")
        if run_summaries:
            print()
            print("  per-run breakdown:")
            for rs in run_summaries:
                print(
                    f"    {rs['timestamp'] or '(no ts)'}  "
                    f"cycles={rs['cycle_count']}  "
                    f"closed={rs['closed_loop_count']}  "
                    f"gated={rs['gated_count']}  "
                    f"+{rs['added']}/Δ{rs['revised']}/-{rs['superseded']}"
                )
        bb_graph = report.get("bb_graph")
        if isinstance(bb_graph, dict) and "error" not in bb_graph:
            print()
            print(
                f"  bb graph: {bb_graph['node_count']} nodes, "
                f"{bb_graph['edge_count']} edges, "
                f"{bb_graph['untyped_edge_count']} untyped"
            )
            top_pairs = bb_graph.get("untyped_edges_by_bb_pair", [])[:5]
            for pair in top_pairs:
                print(
                    f"    {pair['count']:>3}×  {pair['source']} -> {pair['target']}"
                )
        elif isinstance(bb_graph, dict) and bb_graph.get("error"):
            print()
            print(f"  bb graph: error — {bb_graph['error']}")

    return 0


def _build_bb_graph_section(db_path: Path) -> dict:
    """Phase 6 — corpus-graph telemetry joined into `dks --report`.

    Loads ``BBGraph.from_db()`` and returns a JSON-safe summary:
    node counts by BB type, edge counts by schema label, untyped-edge
    BB-pair tallies. Best-effort: if the index DB can't be read, we
    return a sentinel ``{"error": ...}`` payload rather than crashing
    the report.
    """
    from collections import defaultdict

    db = db_path.expanduser().resolve()
    if not db.is_file():
        return {"error": f"index DB not found at {db}"}

    from tessellum.bb import BB_SCHEMA, BBGraph, BBType

    try:
        graph = BBGraph.from_db(db)
    except Exception as e:  # noqa: BLE001 — best-effort; surface as data
        return {"error": f"failed to load BBGraph from {db}: {e}"}

    untyped_pair_counts: dict[tuple[str, str], int] = defaultdict(int)
    for e in graph.untyped_edges():
        src = graph.node(e.source_note_id)
        tgt = graph.node(e.target_note_id)
        if src is None or tgt is None:
            continue
        untyped_pair_counts[(src.bb_type.value, tgt.bb_type.value)] += 1

    return {
        "db_path": str(db),
        "node_count": graph.node_count,
        "edge_count": graph.edge_count,
        "nodes_by_type": {
            bb.value: len(graph.nodes_of_type(bb)) for bb in BBType
        },
        "edges_by_label": graph.edges_by_type(),
        "untyped_edge_count": len(graph.untyped_edges()),
        "untyped_edges_by_bb_pair": [
            {"source": s, "target": t, "count": c}
            for (s, t), c in sorted(
                untyped_pair_counts.items(), key=lambda kv: (-kv[1], kv[0])
            )
        ],
        "schema_edge_count": len(BB_SCHEMA),
    }


def _empty_report(runs_dir: Path) -> dict:
    return {
        "runs_dir": str(runs_dir),
        "run_count": 0,
        "total_cycles": 0,
        "closed_loop_count": 0,
        "closed_loop_rate": 0.0,
        "gated_count": 0,
        "gated_rate": 0.0,
        "warrant_changes": {"added": 0, "revised": 0, "superseded": 0},
        "top_attacked_warrant_fz": [],
        "runs": [],
    }
