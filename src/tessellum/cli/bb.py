"""``tessellum bb`` — BB ontology + corpus-graph operations.

Top-level subcommand group for everything related to the BB ontology
(types, schema, corpus graph). Phase 6 (v0.0.48) ships the first
operation:

- ``tessellum bb audit`` — vault-wide telemetry over ``BBGraph.from_db()``.
  Reports node counts by BB type, edge counts by epistemic-edge label,
  untyped corpus edges, orphan BB nodes (no inbound/outbound corpus
  edges), and unrealised schema edges (0 instances in the corpus).

Future phases (per `plans/plan_dks_expansion.md`):

- ``tessellum bb walk <fz>`` — visualise an FSM walk (Phase 8+)
- ``tessellum bb validate-schema`` — meta-DKS schema-edit validation (Phase 9)
- ``tessellum bb migrate`` — retroactive schema-version validation (Phase 9)

Exit codes:
    0  audit completed (warnings are not failure)
    2  invocation error (DB missing, etc.)
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from tessellum.bb import BB_SCHEMA, BBGraph, BBType
from tessellum.bb.graph import BBEdge, BBNode


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    bb = subparsers.add_parser(
        "bb",
        help="BB ontology + corpus-graph operations (audit, ...).",
    )

    sub = bb.add_subparsers(dest="bb_command")

    db_parent = argparse.ArgumentParser(add_help=False)
    db_parent.add_argument(
        "--db",
        type=Path,
        default=Path("data") / "tessellum.db",
        help="Index DB path (default: ./data/tessellum.db).",
    )

    audit = sub.add_parser(
        "audit",
        parents=[db_parent],
        help="Vault-wide BBGraph telemetry — counts, untyped edges, orphans.",
    )
    audit.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    audit.add_argument(
        "--show-untyped",
        action="store_true",
        help="Include the full list of untyped corpus edges in the output "
        "(by default only the count + first few examples are shown).",
    )
    audit.set_defaults(func=run_bb_audit, _bb_op="audit")

    bb.set_defaults(func=run_bb_audit, _bb_op=None, db=Path("data") / "tessellum.db")


def run_bb_audit(args: argparse.Namespace) -> int:
    op = getattr(args, "_bb_op", None)
    if op is None:
        print(
            "tessellum bb: missing sub-subcommand. Try `tessellum bb audit`.",
            file=sys.stderr,
        )
        return 2

    db_path: Path = getattr(args, "db", Path("data") / "tessellum.db")
    db = db_path.expanduser().resolve()
    if not db.is_file():
        print(
            f"tessellum bb audit: index DB not found at {db}. "
            f"Run `tessellum index build` first.",
            file=sys.stderr,
        )
        return 2

    graph = BBGraph.from_db(db)
    report = _build_audit_report(graph)

    if args.output_format == "json":
        _emit_json(report, show_untyped=args.show_untyped)
    else:
        _emit_human(report, show_untyped=args.show_untyped)
    return 0


# ── Report assembly ────────────────────────────────────────────────────────


def _build_audit_report(graph: BBGraph) -> dict:
    """Build the audit payload from a corpus BBGraph."""

    nodes_by_type: dict[BBType, list[BBNode]] = {bb: [] for bb in BBType}
    for node in graph:
        nodes_by_type[node.bb_type].append(node)

    edge_counts_by_label = graph.edges_by_type()
    typed_edges = [e for e in graph.edges() if e.edge_type is not None]
    untyped_edges = graph.untyped_edges()

    # Schema edges with 0 realisations in the corpus.
    realised_pairs: set[tuple[BBType, BBType]] = {
        (graph.node(e.source_note_id).bb_type, graph.node(e.target_note_id).bb_type)
        for e in typed_edges
        if graph.node(e.source_note_id) is not None
        and graph.node(e.target_note_id) is not None
    }
    unrealised_schema_edges = [
        {
            "source": edge.source.value,
            "target": edge.target.value,
            "label": edge.label,
        }
        for edge in BB_SCHEMA
        if (edge.source, edge.target) not in realised_pairs
    ]

    # Orphan BB nodes — present in the corpus but with no inbound or
    # outbound corpus edges. (A node only has fz-parent-root status if
    # it has no incoming fz-parent edge — that's a *trail root*, not an
    # orphan; we still flag for visibility.)
    orphan_nodes = [
        node
        for node in graph
        if not graph.out_edges(node.note_id) and not graph.in_edges(node.note_id)
    ]

    # Untyped-edge BB-pair counts for the human summary.
    untyped_pair_counts: dict[tuple[str, str], int] = defaultdict(int)
    for e in untyped_edges:
        src = graph.node(e.source_note_id)
        tgt = graph.node(e.target_note_id)
        if src is None or tgt is None:
            continue
        untyped_pair_counts[(src.bb_type.value, tgt.bb_type.value)] += 1

    return {
        "node_count": graph.node_count,
        "edge_count": graph.edge_count,
        "nodes_by_type": {
            bb.value: len(nodes_by_type[bb]) for bb in BBType
        },
        "edges_by_label": dict(edge_counts_by_label),
        "untyped_edge_count": len(untyped_edges),
        "untyped_edges_by_bb_pair": [
            {"source": s, "target": t, "count": c}
            for (s, t), c in sorted(
                untyped_pair_counts.items(), key=lambda kv: (-kv[1], kv[0])
            )
        ],
        "untyped_edges": [
            {
                "source_note_id": e.source_note_id,
                "target_note_id": e.target_note_id,
                "provenance": e.provenance,
            }
            for e in untyped_edges
        ],
        "orphan_node_count": len(orphan_nodes),
        "orphan_nodes": [
            {"note_id": n.note_id, "bb_type": n.bb_type.value}
            for n in orphan_nodes
        ],
        "unrealised_schema_edges": unrealised_schema_edges,
        "schema_edge_count": len(BB_SCHEMA),
        "realised_schema_edge_count": len(BB_SCHEMA) - len(unrealised_schema_edges),
    }


def _emit_human(report: dict, *, show_untyped: bool) -> None:
    print(
        f"bb audit  ({report['node_count']} BB nodes, "
        f"{report['edge_count']} BB edges)"
    )
    print()
    print("Nodes by BB type:")
    for bb_value, count in report["nodes_by_type"].items():
        if count == 0:
            continue
        print(f"  {count:>4}  {bb_value}")

    if report["edges_by_label"]:
        print()
        print("Edges by schema label:")
        for label, count in sorted(
            report["edges_by_label"].items(), key=lambda kv: (-kv[1], kv[0])
        ):
            print(f"  {count:>4}  {label}")

    if report["untyped_edge_count"]:
        print()
        print(
            f"Untyped corpus edges: {report['untyped_edge_count']} "
            f"(BB-pair not in BB_SCHEMA in either direction)"
        )
        for entry in report["untyped_edges_by_bb_pair"][:10]:
            print(
                f"  {entry['count']:>4}  {entry['source']} -> {entry['target']}"
            )
        if show_untyped:
            print()
            print("All untyped edges:")
            for e in report["untyped_edges"]:
                print(
                    f"  {e['source_note_id']} -> {e['target_note_id']}  "
                    f"[{e['provenance']}]"
                )

    if report["orphan_node_count"]:
        print()
        print(
            f"Orphan BB nodes: {report['orphan_node_count']} "
            f"(no inbound/outbound corpus edges)"
        )
        for n in report["orphan_nodes"][:10]:
            print(f"  {n['note_id']}  [{n['bb_type']}]")

    if report["unrealised_schema_edges"]:
        print()
        print(
            f"Unrealised schema edges: "
            f"{len(report['unrealised_schema_edges'])} of "
            f"{report['schema_edge_count']} "
            f"(BB_SCHEMA entries with 0 instances in the corpus)"
        )
        for edge in report["unrealised_schema_edges"]:
            print(
                f"  {edge['source']:<22} -> {edge['target']:<22}  [{edge['label']}]"
            )


def _emit_json(report: dict, *, show_untyped: bool) -> None:
    payload = dict(report)
    if not show_untyped:
        # By default the JSON output omits the verbose per-edge list,
        # keeping payload small. The aggregated `untyped_edges_by_bb_pair`
        # is preserved.
        payload.pop("untyped_edges", None)
    print(json.dumps(payload, indent=2))
