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

import re

from tessellum.bb import BB_SCHEMA, BBGraph, BBType
from tessellum.bb.graph import BBNode


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

    # ── migrate ────────────────────────────────────────────────────────────
    migrate = sub.add_parser(
        "migrate",
        help="Retroactive bb_schema_version validation (Phase B.5). "
        "Scan a vault for notes whose recorded version is below the "
        "current BB_SCHEMA_VERSION; report which would pass TESS-005 "
        "today and which would fail.",
    )
    migrate.add_argument(
        "--vault",
        type=Path,
        default=Path("vault"),
        help="Vault root to scan (default: ./vault/).",
    )
    migrate.add_argument(
        "--target-version",
        default="current",
        help="Target version. 'current' (default) uses the live "
        "BB_SCHEMA_VERSION. Pass an integer to target a specific version.",
    )
    migrate.add_argument(
        "--apply",
        action="store_true",
        help="Bump the recorded bb_schema_version on notes that would "
        "pass TESS-005 under the target version (passive migration). "
        "Notes that would fail are reported but never auto-rewritten — "
        "manual review required.",
    )
    migrate.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    migrate.set_defaults(func=run_bb_migrate, _bb_op="migrate")

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


# ── tessellum bb migrate (Phase B.5) ────────────────────────────────────────


_BB_SCHEMA_VERSION_LINE_RE = re.compile(
    r"^bb_schema_version:\s*(\d+)\s*$", re.MULTILINE
)


def run_bb_migrate(args: argparse.Namespace) -> int:
    """Retroactive bb_schema_version validation + passive migration."""
    from tessellum.bb.types import BB_SCHEMA_VERSION
    from tessellum.format import parse_note, validate
    from tessellum.format.issue import Severity

    vault_root: Path = args.vault.expanduser().resolve()
    if not vault_root.is_dir():
        print(
            f"tessellum bb migrate: vault root not found at {vault_root}.",
            file=sys.stderr,
        )
        return 2

    if args.target_version == "current":
        target = BB_SCHEMA_VERSION
    else:
        try:
            target = int(args.target_version)
        except (TypeError, ValueError):
            print(
                f"tessellum bb migrate: --target-version must be 'current' "
                f"or an integer; got {args.target_version!r}.",
                file=sys.stderr,
            )
            return 2

    # Walk the vault for .md files
    md_files = sorted(p for p in vault_root.rglob("*.md") if p.is_file())

    behind: list[dict] = []  # notes with recorded_version < target
    would_pass: list[dict] = []
    would_fail: list[dict] = []
    skipped: list[dict] = []  # parse errors or unparseable notes

    for path in md_files:
        try:
            note = parse_note(path)
        except Exception as e:  # noqa: BLE001 — defensive, surface in skipped
            skipped.append({"path": str(path.relative_to(vault_root)), "reason": str(e)})
            continue

        recorded_raw = note.frontmatter.get("bb_schema_version")
        try:
            recorded = (
                int(recorded_raw) if recorded_raw is not None else 1
            )  # default 1 for v0.0.52-era notes
        except (TypeError, ValueError):
            skipped.append(
                {
                    "path": str(path.relative_to(vault_root)),
                    "reason": f"bb_schema_version not an integer: {recorded_raw!r}",
                }
            )
            continue

        if recorded >= target:
            continue  # already at-or-above target

        # Run validation against the live schema (which reflects target_version
        # only when target == current; for past targets the live schema is a
        # superset, but reporting errors against current is the conservative
        # behavior — would_fail under current implies would_fail under target).
        issues = validate(path)
        tess005_errors = [
            i for i in issues if i.rule_id == "TESS-005" and i.severity == Severity.ERROR
        ]
        # TESS-005 is only WARNING today, so passing means: no ERRORs surface.
        # We classify by whether TESS-005 *warnings* exist (informational).
        tess005_warnings = [
            i for i in issues if i.rule_id == "TESS-005"
        ]

        entry = {
            "path": str(path.relative_to(vault_root)),
            "recorded_version": recorded,
            "target_version": target,
            "tess005_warnings": len(tess005_warnings),
        }
        behind.append(entry)
        if not tess005_errors:
            would_pass.append(entry)
        else:
            entry["sample_error"] = tess005_errors[0].message[:200]
            would_fail.append(entry)

    # Apply: bump versions on would_pass entries
    bumped: list[str] = []
    if args.apply:
        for entry in would_pass:
            full_path = vault_root / entry["path"]
            try:
                text = full_path.read_text(encoding="utf-8")
            except OSError:
                continue
            new_text, changed = _bump_bb_schema_version(text, target)
            if changed:
                full_path.write_text(new_text, encoding="utf-8")
                bumped.append(entry["path"])

    report = {
        "vault_root": str(vault_root),
        "target_version": target,
        "current_version": BB_SCHEMA_VERSION,
        "total_md_files": len(md_files),
        "behind_count": len(behind),
        "would_pass_count": len(would_pass),
        "would_fail_count": len(would_fail),
        "skipped_count": len(skipped),
        "bumped_count": len(bumped),
        "apply_mode": args.apply,
        "behind": behind,
        "would_pass": would_pass,
        "would_fail": would_fail,
        "skipped": skipped,
        "bumped": bumped,
    }

    if args.output_format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(f"tessellum bb migrate  (vault: {vault_root})")
        print(f"  target version:  {target}")
        print(f"  current version: {BB_SCHEMA_VERSION}")
        print(f"  total .md files: {len(md_files)}")
        print(f"  notes behind target: {len(behind)}")
        print(f"    would pass under target: {len(would_pass)}")
        print(f"    would fail under target: {len(would_fail)}")
        if skipped:
            print(f"  skipped (parse errors): {len(skipped)}")
        if args.apply:
            print(f"  versions bumped: {len(bumped)}")
        elif would_pass:
            print(
                f"  (dry run) pass --apply to bump versions on the "
                f"{len(would_pass)} would-pass notes."
            )
        if would_fail:
            print(
                "  would-fail notes need manual review — never auto-rewritten."
            )
            for entry in would_fail[:5]:
                print(f"    {entry['path']}: {entry.get('sample_error', '')[:120]}")

    return 0


def _bump_bb_schema_version(text: str, target: int) -> tuple[str, bool]:
    """Replace the ``bb_schema_version:`` line in YAML frontmatter.

    Returns ``(new_text, changed)``. When the field is absent, append it
    after the first ``building_block:`` line. When present, replace its
    value with ``target``. Returns ``changed=False`` if the field already
    equals ``target`` (idempotent).
    """
    match = _BB_SCHEMA_VERSION_LINE_RE.search(text)
    if match:
        try:
            current = int(match.group(1))
        except ValueError:
            current = -1
        if current == target:
            return text, False
        new_text = (
            text[: match.start()]
            + f"bb_schema_version: {target}"
            + text[match.end():]
        )
        return new_text, True

    # Field absent — inject after building_block: line
    bb_line = re.search(r"^(building_block:\s*[a-z_]+)\s*$", text, re.MULTILINE)
    if not bb_line:
        return text, False
    new_text = (
        text[: bb_line.end()]
        + f"\nbb_schema_version: {target}"
        + text[bb_line.end():]
    )
    return new_text, True
