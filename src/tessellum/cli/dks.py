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
        "without --include-bb-graph. v0.0.53: also consumed by "
        "--meta when present and readable, to populate "
        "MetaObservation.unrealised_schema_edges from BBGraph.",
    )
    # Phase 7 — learned confidence + retrieval-grounded warrants
    dks.add_argument(
        "--confidence-model",
        choices=["constant", "calibrated"],
        default="constant",
        help="Confidence model for the gate (Phase 5 + Phase 7). "
        "`constant` uses ConstantConfidence(--gate-confidence). "
        "`calibrated` uses CalibratedConfidence reading "
        "warrant_history.jsonl under --runs-dir for an attack-rate signal.",
    )
    dks.add_argument(
        "--calibrate",
        action="store_true",
        help="Calibration mode (Phase 7): scan past per-cycle traces "
        "under --runs-dir, report the achieved false-gate rate at "
        "--gate-threshold, and suggest a threshold that hits "
        "--target-false-gate-rate. Skips the observations run.",
    )
    dks.add_argument(
        "--target-false-gate-rate",
        type=float,
        default=None,
        help="With --calibrate: target false-gate rate (default 0.10). "
        "Per D2 in plan_dks_expansion: configurable + observable. "
        "Ignored without --calibrate.",
    )
    dks.add_argument(
        "--retrieval-db",
        type=Path,
        default=None,
        help="With a normal run: build a RetrievalClient against this "
        "index DB and pass it to each cycle. Argument-generation prompts "
        "gain a 'Related material from the substrate' block populated by "
        "hybrid-search hits against the observation summary. Off by default.",
    )
    dks.add_argument(
        "--perspectives",
        type=str,
        default="conservative,exploratory",
        help="Phase 10: comma-separated list of perspectives the cycle "
        "should generate arguments from. Default 'conservative,exploratory' "
        "preserves the v0.0.40-era A/B behaviour. N>2 activates pairwise "
        "contradicts + Dung grounded labelling. Perspectives must be unique.",
    )
    dks.add_argument(
        "--semantic-disagreement",
        action="store_true",
        help="Use one LLM call at step 4 to check whether claims "
        "substantively disagree, instead of string-compare. Falls back "
        "to string-compare on parse failure. Off by default.",
    )
    # Phase 9 — meta-DKS (schema-mutation runtime)
    dks.add_argument(
        "--meta",
        action="store_true",
        help="Meta-DKS mode (Phase 9): scan past per-cycle traces "
        "under --runs-dir, build a MetaObservation (top-K attacked "
        "warrants + Toulmin failure distribution + unrealised schema "
        "edges), run MetaCycle, propose 0-N schema edits. Default "
        "--dry-run; pass --apply to actually write the edits.",
    )
    dks.add_argument(
        "--apply",
        action="store_true",
        help="With --meta: actually write the surviving SchemaEditEvents "
        "to runs/dks/meta/schema_events.jsonl + emit a migration note. "
        "Without this, --meta runs in dry-run mode (proposals only).",
    )
    dks.add_argument(
        "--min-cycles",
        type=int,
        default=None,
        help="With --meta: minimum cycles required before any proposals "
        "fire (cold-start guard). Default per DEFAULT_MIN_CYCLES=20.",
    )
    dks.add_argument(
        "--target-failure",
        choices=["premise", "warrant", "counter-example", "undercutting"],
        default=None,
        help="With --meta: only propose edits for cycles whose Toulmin "
        "failure mode is the given component. Default: all components.",
    )
    dks.add_argument(
        "--proposer",
        choices=["heuristic", "llm"],
        default="heuristic",
        help="With --meta: proposal strategy. 'heuristic' (default) "
        "uses the v0.0.52 lookup-table-driven HeuristicProposer; "
        "'llm' uses the Phase B.2 LLMProposer backed by --backend. "
        "llm requires --backend anthropic (or mock for testing).",
    )
    dks.add_argument(
        "--attacker",
        choices=["none", "llm"],
        default="none",
        help="With --meta: attack stage. 'none' (default) preserves "
        "v0.0.52 survive=pass-through behaviour. 'llm' enables the "
        "Phase B.3 LLMAttacker (dialectical attack on each proposal). "
        "llm requires --backend anthropic (or mock for testing).",
    )
    dks.add_argument(
        "--survive-threshold",
        choices=["strict", "majority", "permissive"],
        default="majority",
        help="With --meta --attacker llm: aggregation policy for "
        "deciding survival. 'strict': zero attacks. 'majority' "
        "(default): <=1 strong AND <=2 moderate. 'permissive': no "
        "strong attacks. Ignored when --attacker=none (all proposals survive).",
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

    # Phase 7 — --calibrate short-circuits to calibration replay.
    if args.calibrate:
        return _run_dks_calibrate(args)

    # Phase 9 — --meta short-circuits to schema-mutation runtime.
    if args.meta:
        return _run_dks_meta(args)

    if args.observations is None:
        print(
            "tessellum dks: missing observations file (or pass --report / --calibrate / --meta).",
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

    # Phase 5 — confidence gating (opt-in via --gate-confidence
    # ConstantConfidence). Phase 7 adds --confidence-model=calibrated
    # to use CalibratedConfidence (reads warrant_history.jsonl under
    # --runs-dir for an attack-rate signal).
    confidence_model = None
    if args.confidence_model == "calibrated":
        # CalibratedConfidence lives in tessellum.dks; WarrantHistory is
        # already imported at module level (line 45). Import only the
        # name not already in module scope to avoid shadowing the
        # module-level WarrantHistory as a local (Python rebinds the
        # symbol throughout the function once any inner import binds it).
        from tessellum.dks import CalibratedConfidence

        calibration_history_path = (
            args.runs_dir.expanduser().resolve() / "warrant_history.jsonl"
        )
        confidence_model = CalibratedConfidence(
            warrant_history=WarrantHistory(calibration_history_path)
        )
    elif args.gate_confidence is not None:
        if not 0.0 <= args.gate_confidence <= 1.0:
            print(
                f"tessellum dks: --gate-confidence must be in [0.0, 1.0]; "
                f"got {args.gate_confidence}",
                file=sys.stderr,
            )
            return 2
        confidence_model = ConstantConfidence(args.gate_confidence)

    # Phase 7 — retrieval-grounded warrants (opt-in via --retrieval-db).
    retrieval_client = None
    if args.retrieval_db is not None:
        from tessellum.dks import RetrievalClient

        try:
            retrieval_client = RetrievalClient(
                args.retrieval_db.expanduser().resolve()
            )
        except FileNotFoundError as e:
            print(
                f"tessellum dks: --retrieval-db unreadable: {e}",
                file=sys.stderr,
            )
            return 2

    perspectives_tuple: tuple[str, ...] = tuple(
        p.strip() for p in args.perspectives.split(",") if p.strip()
    )
    if len(perspectives_tuple) < 2:
        print(
            f"tessellum dks: --perspectives must list at least 2 unique "
            f"perspectives; got {args.perspectives!r}",
            file=sys.stderr,
        )
        return 2
    if len(set(perspectives_tuple)) != len(perspectives_tuple):
        print(
            f"tessellum dks: --perspectives entries must be unique; "
            f"got {args.perspectives!r}",
            file=sys.stderr,
        )
        return 2

    runner = DKSRunner(
        observations=tuple(observations),
        backend=backend,
        initial_warrants=initial_warrants,
        confidence_model=confidence_model,
        confidence_threshold=args.gate_threshold,
        retrieval_client=retrieval_client,
        semantic_disagreement=args.semantic_disagreement,
        perspectives=perspectives_tuple,
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
        # Phase 10 — multi-perspective fields. Always serialised, even
        # in N=2 cycles, so downstream tools (meta-DKS observation
        # builder, audit) can read them uniformly.
        "arguments": [_arg(a) for a in cycle.arguments],
        "contradicts_edges": [
            {
                "attacker_fz": e.attacker_fz,
                "attacked_fz": e.attacked_fz,
                "reason": e.reason,
            }
            for e in cycle.contradicts_edges
        ],
        "grounded_labelling": dict(cycle.grounded_labelling),
        "surviving_argument_fzs": list(cycle.surviving_argument_fzs),
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


# ── --meta mode (Phase 9) ──────────────────────────────────────────────────


def _run_dks_meta(args: argparse.Namespace) -> int:
    """Meta-DKS replay over past per-cycle traces.

    Builds a MetaObservation from the telemetry under --runs-dir
    (top-K attacked warrants, Toulmin failure distribution,
    unrealised schema edges from the current BB_SCHEMA), runs a
    MetaCycle, prints the proposals + optionally writes the
    surviving events to the schema_events.jsonl log.

    Default ``--dry-run`` (no writes); ``--apply`` activates writes.
    """
    from collections import Counter

    from tessellum.bb.types import BB_SCHEMA, BB_SCHEMA_EPISTEMIC
    from tessellum.dks.meta import (
        Attacker,
        DEFAULT_MIN_CYCLES,
        HeuristicProposer,
        LLMAttacker,
        LLMProposer,
        MetaCycle,
        MetaObservation,
        NoOpAttacker,
        Proposer,
        load_event_log,
        write_event_log,
    )

    runs_dir = args.runs_dir.expanduser().resolve()
    min_cycles = args.min_cycles if args.min_cycles is not None else DEFAULT_MIN_CYCLES

    # Build MetaObservation from per-cycle traces.
    if not runs_dir.is_dir():
        observation = MetaObservation(
            timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            cycles_examined=0,
        )
    else:
        cycle_traces: list[dict] = []
        for cycle_path in sorted(runs_dir.glob("*_cycle_*.json")):
            try:
                cycle_traces.append(json.loads(cycle_path.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError):
                continue

        # Top attacked warrants: read per-aggregate warrant_changes
        attacked: Counter[str] = Counter()
        for agg_path in sorted(runs_dir.glob("*_aggregate.json")):
            try:
                agg = json.loads(agg_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for change in agg.get("warrant_changes", []) or []:
                if change.get("kind") in ("revised", "superseded"):
                    fz = change.get("superseded_fz")
                    if fz:
                        attacked[fz] += 1

        # Toulmin failure distribution: read per-cycle traces' counter.broken_component
        toulmin: Counter[str] = Counter()
        for ct in cycle_traces:
            counter = ct.get("counter")
            if isinstance(counter, dict):
                comp = counter.get("broken_component")
                if comp:
                    toulmin[comp] += 1

        # Unrealised schema edges: BB_SCHEMA entries with 0 corpus
        # instances. v0.0.53 (Phase B.6) — when --bb-db points at a
        # readable index DB, query BBGraph.from_db and call
        # ``unrealised_schema_edges()`` to populate the field. Activates
        # Heuristic-2 (retract-unused-edge) in HeuristicProposer.
        # When the DB is absent or unreadable, fall back to empty tuple
        # (v0.0.52 behaviour).
        unrealised: tuple = ()
        bb_db_path: Path | None = getattr(args, "bb_db", None)
        if bb_db_path is not None:
            resolved_db = bb_db_path.expanduser().resolve()
            if resolved_db.is_file():
                try:
                    from tessellum.bb import BBGraph

                    bb_graph = BBGraph.from_db(resolved_db)
                    unrealised = bb_graph.unrealised_schema_edges()
                except Exception:  # noqa: BLE001 — defensive
                    unrealised = ()

        observation = MetaObservation(
            timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            cycles_examined=len(cycle_traces),
            top_attacked_warrants=tuple(attacked.most_common(10)),
            toulmin_failure_counts=dict(toulmin),
            unrealised_schema_edges=unrealised,
        )

    # Build backend lazily — both proposer and attacker may need it
    meta_backend = None
    if args.proposer == "llm" or args.attacker == "llm":
        if args.backend == "anthropic":
            try:
                from tessellum.composer import AnthropicBackend

                meta_backend = AnthropicBackend(model=args.model)
            except ImportError as e:
                print(
                    "tessellum dks --meta with --proposer llm / --attacker llm: "
                    "--backend=anthropic requires the [agent] extras: "
                    "pip install tessellum[agent]",
                    file=sys.stderr,
                )
                print(f"  ({e})", file=sys.stderr)
                return 2
        else:
            mock_responses: dict[str, str] = {}
            if args.mock_responses is not None:
                try:
                    mock_responses = json.loads(
                        args.mock_responses.expanduser().resolve().read_text(
                            encoding="utf-8"
                        )
                    )
                except (OSError, json.JSONDecodeError) as e:
                    print(
                        f"tessellum dks --meta: --mock-responses "
                        f"unreadable: {e}",
                        file=sys.stderr,
                    )
                    return 2
                if not isinstance(mock_responses, dict):
                    print(
                        "tessellum dks --meta: --mock-responses must be "
                        "a JSON object",
                        file=sys.stderr,
                    )
                    return 2
            meta_backend = MockBackend(responses=mock_responses)

    proposer: Proposer
    if args.proposer == "llm":
        proposer = LLMProposer(backend=meta_backend)
    else:
        proposer = HeuristicProposer()

    attacker: Attacker
    if args.attacker == "llm":
        attacker = LLMAttacker(backend=meta_backend)
    else:
        attacker = NoOpAttacker()

    cycle = MetaCycle(
        observation=observation,
        min_cycles=min_cycles,
        target_failure=args.target_failure,
        dry_run=not args.apply,
        proposer=proposer,
        attacker=attacker,
        survive_threshold=args.survive_threshold,
    )
    result = cycle.run()

    # Write events if --apply
    events_path: Path | None = None
    migration_note_path: Path | None = None
    if args.apply and result.events_landed:
        events_path = runs_dir / "meta" / "schema_events.jsonl"
        write_event_log(events_path, result.events_landed, append=True)
        # Emit a migration note for each event
        migration_note_path = _write_migration_note(
            runs_dir / "meta", result.events_landed
        )

    payload = {
        "runs_dir": str(runs_dir),
        "cycles_examined": result.observation.cycles_examined,
        "min_cycles": min_cycles,
        "dry_run": result.dry_run,
        "target_failure": args.target_failure,
        "observation": {
            "top_attacked_warrants": [
                {"fz": fz, "attacks": n}
                for fz, n in result.observation.top_attacked_warrants
            ],
            "toulmin_failure_counts": result.observation.toulmin_failure_counts,
            "unrealised_schema_edges_count": len(
                result.observation.unrealised_schema_edges
            ),
        },
        "proposals": [
            {
                "kind": p.kind,
                "edge": {
                    "source": p.edge.source.value,
                    "target": p.edge.target.value,
                    "label": p.edge.label,
                },
                "motivating_observation": p.motivating_observation,
                "expected_impact": p.expected_impact,
            }
            for p in result.proposals
        ],
        "surviving_count": len(result.surviving),
        "events_landed_count": len(result.events_landed),
        "events_path": str(events_path) if events_path else None,
        "migration_note_path": str(migration_note_path) if migration_note_path else None,
        "elapsed_ms": result.elapsed_ms,
        "attacker": args.attacker,
        "proposer": args.proposer,
        "survive_threshold": result.survive_threshold,
        "attacks": [
            {
                "attacked_proposal_index": a.attacked_proposal_index,
                "attack_kind": a.attack_kind,
                "reason": a.reason,
                "strength": a.strength,
            }
            for a in result.attacks
        ],
    }

    if args.output_format == "json":
        print(json.dumps(payload, indent=2))
    else:
        mode_tag = "DRY RUN" if result.dry_run else "APPLIED"
        print(
            f"dks --meta  ({result.observation.cycles_examined} cycles examined; {mode_tag})"
        )
        if result.observation.cycles_examined < min_cycles:
            print(
                f"  cold-start guard active (--min-cycles={min_cycles}); "
                f"no proposals will fire below this threshold."
            )
        if not result.proposals:
            print("  no proposals generated from the available telemetry.")
        else:
            print(f"  {len(result.proposals)} proposals, {len(result.surviving)} surviving:")
            for p in result.surviving:
                print(
                    f"    {p.kind:>9}  {p.edge.source.value} -> {p.edge.target.value}  "
                    f"({p.edge.label})"
                )
                print(f"               {p.motivating_observation}")
        if events_path:
            print(f"  events appended to: {events_path}")
        if migration_note_path:
            print(f"  migration note:     {migration_note_path}")

    return 0


def _write_migration_note(meta_dir: Path, events) -> Path:
    """Author a brief migration note documenting the landed events."""
    meta_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    note_path = meta_dir / f"migration_{ts}.md"
    lines = [
        "# Schema Edit Migration Note",
        "",
        f"**Timestamp:** {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"**Events landed:** {len(events)}",
        "",
        "## Events",
        "",
    ]
    for e in events:
        lines.append(
            f"- **{e.kind}** `{e.edge.source.value} -> {e.edge.target.value}` "
            f"({e.edge.label!r})"
        )
        if e.motivating_failure:
            lines.append(f"  - Motivation: {e.motivating_failure}")
    note_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return note_path


# ── --calibrate mode (Phase 7) ─────────────────────────────────────────────


def _run_dks_calibrate(args: argparse.Namespace) -> int:
    """Calibration replay over past per-cycle traces.

    Reads every ``*_cycle_*.json`` under ``--runs-dir``, examines the
    recorded ``confidence_score`` + ``closed_loop`` fields, and reports
    how the current ``--gate-threshold`` (or default 0.85) would have
    behaved. Suggests a threshold that achieves
    ``--target-false-gate-rate`` (default 0.10 per D2).

    Skips the observations run (no cycles fire during calibration).
    """
    from tessellum.dks import (
        DEFAULT_CONFIDENCE_THRESHOLD,
        DEFAULT_TARGET_FALSE_GATE_RATE,
        calibrate_from_traces,
    )

    runs_dir = args.runs_dir.expanduser().resolve()
    threshold = (
        args.gate_threshold
        if args.gate_threshold is not None
        else DEFAULT_CONFIDENCE_THRESHOLD
    )
    target_rate = (
        args.target_false_gate_rate
        if args.target_false_gate_rate is not None
        else DEFAULT_TARGET_FALSE_GATE_RATE
    )

    result = calibrate_from_traces(
        runs_dir,
        current_threshold=threshold,
        target_false_gate_rate=target_rate,
    )

    payload = {
        "runs_dir": str(runs_dir),
        "cycles_examined": result.cycles_examined,
        "current_threshold": result.current_threshold,
        "target_false_gate_rate": result.target_false_gate_rate,
        "would_gate_count": result.would_gate_count,
        "false_gate_count": result.false_gate_count,
        "false_gate_rate": result.false_gate_rate,
        "suggested_threshold": result.suggested_threshold,
    }

    if args.output_format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"dks --calibrate  ({result.cycles_examined} cycles examined under {runs_dir})")
        if result.cycles_examined == 0:
            print(
                "  No per-cycle traces with confidence_score found. "
                "Run `tessellum dks <obs.jsonl>` with a confidence model "
                "(e.g. --confidence-model calibrated) first."
            )
        else:
            print(
                f"  threshold={result.current_threshold}: "
                f"{result.would_gate_count} would-gate, "
                f"{result.false_gate_count} false-gate "
                f"({result.false_gate_rate * 100:.1f}% — "
                f"target {result.target_false_gate_rate * 100:.1f}%)"
            )
            if result.suggested_threshold is not None:
                print(
                    f"  suggested threshold to hit target: "
                    f"{result.suggested_threshold:.4f}"
                )
            else:
                print(
                    "  No threshold in [0, 1] hits the target with positive "
                    "would-gate count. Try lowering --target-false-gate-rate "
                    "or accumulating more diverse confidence-score data."
                )

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
