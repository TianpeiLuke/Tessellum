"""``tessellum fz`` — Folgezettel trail explorer (list / show / ancestors / descendants / path).

Tessellum stores Folgezettel as two columns on the ``notes`` table:
``folgezettel`` and ``folgezettel_parent``. Unlike the AB parent
project, there is no pre-materialised ``folgezettel_trails`` view —
trail topology (path, depth, trail_id) is derived at query time by
walking the parent chain in Python. The vaults this targets are
small enough (typically <1000 FZ notes) that an in-memory traversal
is simpler and more portable than a recursive CTE.

```bash
tessellum fz list                  # trails with node counts + BB diversity
tessellum fz show 1a               # subtree rooted at FZ 1a
tessellum fz ancestors 1a1b1       # root → node chain
tessellum fz descendants 1         # node → leaves
tessellum fz path 1a1b             # full chain + siblings + trail metadata
tessellum fz all                   # every FZ node, grouped by trail
```

Exit codes:
    0  query ran (may return zero rows for unknown FZ)
    2  invocation error (DB missing, malformed args)
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path


# ── FZ string parsing ────────────────────────────────────────────────────────

_TOKEN_RE = re.compile(r"[a-z]+(?:-[a-z]+)*|[0-9]+")


def fz_sort_key(fz: str) -> tuple[tuple[int, int | str], ...]:
    """Numeric-aware FZ sort key.

    ``'5e1b10'`` → ``((0,5),(1,'e'),(0,1),(1,'b'),(0,10))`` so that
    ``5e1b2`` sorts before ``5e1b10``. Letters and numbers each have
    their own bucket so the lex order within a bucket makes sense.
    """
    parts = _TOKEN_RE.findall(fz)
    return tuple((0, int(p)) if p.isdigit() else (1, p) for p in parts)


def fz_trail_root(fz: str) -> str:
    """Leading numeric token = trail id. ``'1a1b'`` → ``'1'``."""
    m = re.match(r"\d+", fz)
    return m.group(0) if m else fz


# ── DB helpers ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class FZNote:
    """One FZ-bearing row materialised for traversal."""

    folgezettel: str
    folgezettel_parent: str | None
    note_name: str
    building_block: str | None
    note_second_category: str | None


def _load_fz_notes(conn: sqlite3.Connection) -> dict[str, FZNote]:
    """All FZ-bearing notes, keyed by folgezettel."""
    cur = conn.cursor()
    rows = cur.execute(
        """
        SELECT folgezettel, folgezettel_parent, note_name,
               building_block, note_second_category
        FROM notes
        WHERE folgezettel IS NOT NULL
        """
    ).fetchall()
    return {
        r[0]: FZNote(
            folgezettel=r[0],
            folgezettel_parent=r[1],
            note_name=r[2],
            building_block=r[3],
            note_second_category=r[4],
        )
        for r in rows
    }


def _children_index(notes: dict[str, FZNote]) -> dict[str, list[FZNote]]:
    """parent_fz → [child notes]."""
    by_parent: dict[str, list[FZNote]] = {}
    for n in notes.values():
        if n.folgezettel_parent is not None:
            by_parent.setdefault(n.folgezettel_parent, []).append(n)
    for kids in by_parent.values():
        kids.sort(key=lambda n: fz_sort_key(n.folgezettel))
    return by_parent


def _ancestor_chain(notes: dict[str, FZNote], fz: str) -> list[FZNote]:
    """Walk parent links from root to ``fz``. Returns empty list if FZ
    is not in the index. Cycle-safe."""
    if fz not in notes:
        return []
    chain: list[FZNote] = []
    seen: set[str] = set()
    current: str | None = fz
    while current and current not in seen:
        seen.add(current)
        n = notes.get(current)
        if n is None:
            break
        chain.append(n)
        current = n.folgezettel_parent
    chain.reverse()
    return chain


def _descendants(
    notes: dict[str, FZNote],
    children: dict[str, list[FZNote]],
    root_fz: str,
) -> list[tuple[FZNote, int]]:
    """DFS descendants in FZ order. Returns ``[(note, depth_from_root)]``,
    inclusive of the root itself at depth 0."""
    if root_fz not in notes:
        return []
    out: list[tuple[FZNote, int]] = []
    stack: list[tuple[FZNote, int]] = [(notes[root_fz], 0)]
    visited: set[str] = set()
    while stack:
        node, depth = stack.pop()
        if node.folgezettel in visited:
            continue
        visited.add(node.folgezettel)
        out.append((node, depth))
        kids = children.get(node.folgezettel, [])
        for k in reversed(kids):
            stack.append((k, depth + 1))
    return out


def _resolve(notes: dict[str, FZNote], query: str) -> FZNote | None:
    """Look up by exact FZ first; fall back to exact note_name match."""
    if query in notes:
        return notes[query]
    for n in notes.values():
        if n.note_name == query:
            return n
    return None


# ── Commands ─────────────────────────────────────────────────────────────────


def _cmd_list(notes: dict[str, FZNote]) -> int:
    """List trails with node counts + max depth + BB diversity."""
    by_trail: dict[str, list[FZNote]] = {}
    for n in notes.values():
        by_trail.setdefault(fz_trail_root(n.folgezettel), []).append(n)

    rows: list[tuple[str, int, int, str]] = []
    children = _children_index(notes)
    for trail_id, members in by_trail.items():
        max_depth = max(len(_ancestor_chain(notes, n.folgezettel)) - 1 for n in members)
        bbs = sorted({n.building_block for n in members if n.building_block})
        rows.append((trail_id, len(members), max_depth, ", ".join(bbs)))
    rows.sort(key=lambda r: (-r[1], fz_sort_key(r[0])))

    if not rows:
        print("No FZ trails found.")
        return 0

    print(f"{'Trail':<8} {'Nodes':>6} {'Depth':>6}  BB Types")
    print("-" * 70)
    for trail_id, n_nodes, max_d, bbs in rows:
        print(f"{trail_id:<8} {n_nodes:>6} {max_d:>6}  {bbs}")
    total = sum(r[1] for r in rows)
    print(f"\nTotal: {total} node{'s' if total != 1 else ''} across {len(rows)} trail{'s' if len(rows) != 1 else ''}")
    _ = children  # children unused here; kept for symmetry / future use
    return 0


def _cmd_show(notes: dict[str, FZNote], query: str) -> int:
    """Show the subtree rooted at the resolved note."""
    target = _resolve(notes, query)
    if target is None:
        print(f"No FZ note matching '{query}'.")
        return 0

    children = _children_index(notes)
    sub = _descendants(notes, children, target.folgezettel)
    print(f"Subtree of FZ {target.folgezettel} ({len(sub)} node{'s' if len(sub) != 1 else ''}):\n")
    for node, depth in sub:
        indent = "  " * depth
        bb_tag = f"[{node.building_block}]" if node.building_block else ""
        cat_tag = f"({node.note_second_category})" if node.note_second_category else ""
        print(f"{indent}{node.folgezettel:<20} {node.note_name:<55} {bb_tag:<25} {cat_tag}")
    return 0


def _cmd_ancestors(notes: dict[str, FZNote], query: str) -> int:
    """Display the ancestor chain from root to the resolved note."""
    target = _resolve(notes, query)
    if target is None:
        print(f"No FZ note matching '{query}'.")
        return 0

    chain = _ancestor_chain(notes, target.folgezettel)
    print(f"Ancestors of FZ {target.folgezettel} ({target.note_name}):\n")
    print(f"{'Depth':<6} {'FZ':<20} {'Note':<55} {'BB':<20}")
    print("-" * 105)
    for depth, node in enumerate(chain):
        marker = " *" if node.folgezettel == target.folgezettel else ""
        bb = node.building_block or ""
        print(f"{depth:<6} {node.folgezettel:<20} {node.note_name:<55} {bb:<20}{marker}")
    if chain:
        print(f"\nPath: {' -> '.join(n.folgezettel for n in chain)}")
    return 0


def _cmd_descendants(notes: dict[str, FZNote], query: str) -> int:
    """Display all descendants of the resolved note (excluding the root)."""
    target = _resolve(notes, query)
    if target is None:
        print(f"No FZ note matching '{query}'.")
        return 0

    children = _children_index(notes)
    sub = _descendants(notes, children, target.folgezettel)
    descendants_only = [(n, d) for n, d in sub if n.folgezettel != target.folgezettel]
    if not descendants_only:
        print(f"No descendants found for FZ {target.folgezettel}.")
        return 0

    print(f"Descendants of FZ {target.folgezettel} ({len(descendants_only)} node{'s' if len(descendants_only) != 1 else ''}):\n")
    for node, depth in descendants_only:
        indent = "  " * depth
        bb = node.building_block or ""
        print(f"{indent}{node.folgezettel:<20} {node.note_name:<55} [{bb}]")
    return 0


def _cmd_path(notes: dict[str, FZNote], query: str) -> int:
    """Full ancestor chain + same-parent siblings + trail metadata."""
    target = _resolve(notes, query)
    if target is None:
        print(f"No FZ note matching '{query}'.")
        return 0

    chain = _ancestor_chain(notes, target.folgezettel)
    trail_id = fz_trail_root(target.folgezettel)
    depth = len(chain) - 1

    print(f"Path to FZ {target.folgezettel} (trail {trail_id}, depth {depth}):\n")
    for i, node in enumerate(chain):
        connector = "-> " if i > 0 else "   "
        marker = " *" if node.folgezettel == target.folgezettel else ""
        bb = node.building_block or ""
        print(f"  {'  ' * i}{connector}{node.folgezettel} [{bb}] {node.note_name}{marker}")

    parent_fz = target.folgezettel_parent
    if parent_fz:
        children = _children_index(notes)
        siblings = [s for s in children.get(parent_fz, []) if s.folgezettel != target.folgezettel]
        if siblings:
            print(f"\nSiblings (same parent {parent_fz}):")
            for s in siblings:
                bb = s.building_block or ""
                print(f"  {s.folgezettel:<20} {s.note_name:<55} [{bb}]")
    return 0


def _cmd_all(notes: dict[str, FZNote]) -> int:
    """List every FZ node, grouped by trail, in numeric-aware order."""
    if not notes:
        print("No FZ notes in this vault.")
        return 0

    by_trail: dict[str, list[FZNote]] = {}
    for n in notes.values():
        by_trail.setdefault(fz_trail_root(n.folgezettel), []).append(n)

    for trail_id in sorted(by_trail.keys(), key=fz_sort_key):
        members = sorted(by_trail[trail_id], key=lambda n: fz_sort_key(n.folgezettel))
        print(f"--- Trail {trail_id} ---")
        for node in members:
            depth = len(_ancestor_chain(notes, node.folgezettel)) - 1
            indent = "  " * depth
            bb = node.building_block or ""
            cat = node.note_second_category or ""
            print(f"{indent}{node.folgezettel:<20} {node.note_name:<50} [{bb:^20}] {cat}")
        print()
    return 0


# ── argparse wiring ──────────────────────────────────────────────────────────


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    fz = subparsers.add_parser(
        "fz",
        help="Folgezettel trail explorer (list / show / ancestors / descendants / path).",
    )

    # Shared parent parser so every sub-subcommand accepts --db.
    # argparse subparsers do not inherit args from the parent group; the
    # ``parents=[]`` mechanism is the canonical workaround.
    db_parent = argparse.ArgumentParser(add_help=False)
    db_parent.add_argument(
        "--db",
        type=Path,
        default=Path("data") / "tessellum.db",
        help="Index DB path (default: ./data/tessellum.db).",
    )

    sub = fz.add_subparsers(dest="fz_command")

    p_list = sub.add_parser("list", parents=[db_parent], help="List all trails with node counts.")
    p_list.set_defaults(func=_run, _fz_op="list")

    p_show = sub.add_parser("show", parents=[db_parent], help="Show subtree rooted at a FZ.")
    p_show.add_argument("query", help="FZ number or exact note_name.")
    p_show.set_defaults(func=_run, _fz_op="show")

    p_anc = sub.add_parser("ancestors", parents=[db_parent], help="Root-to-node ancestor chain.")
    p_anc.add_argument("query", help="FZ number or exact note_name.")
    p_anc.set_defaults(func=_run, _fz_op="ancestors")

    p_desc = sub.add_parser(
        "descendants", parents=[db_parent], help="Node-to-leaves subtree (excluding root)."
    )
    p_desc.add_argument("query", help="FZ number or exact note_name.")
    p_desc.set_defaults(func=_run, _fz_op="descendants")

    p_path = sub.add_parser("path", parents=[db_parent], help="Full path + same-parent siblings.")
    p_path.add_argument("query", help="FZ number or exact note_name.")
    p_path.set_defaults(func=_run, _fz_op="path")

    p_all = sub.add_parser("all", parents=[db_parent], help="Every FZ node, grouped by trail.")
    p_all.set_defaults(func=_run, _fz_op="all")

    # Bare ``tessellum fz`` (no sub-subcommand) hits this dispatcher and
    # the missing-op branch in _run reports the available choices.
    fz.set_defaults(func=_run, _fz_op=None, db=Path("data") / "tessellum.db")


def _run(args: argparse.Namespace) -> int:
    op = getattr(args, "_fz_op", None)
    if op is None:
        print(
            "tessellum fz: missing sub-subcommand. "
            "Try `tessellum fz list`, `tessellum fz show <FZ>`, "
            "`tessellum fz ancestors <FZ>`, `tessellum fz descendants <FZ>`, "
            "`tessellum fz path <FZ>`, or `tessellum fz all`.",
            file=sys.stderr,
        )
        return 2

    db_path: Path = getattr(args, "db", Path("data") / "tessellum.db")
    db = db_path.expanduser().resolve()
    if not db.is_file():
        print(
            f"tessellum fz: index DB not found at {db}. "
            f"Run `tessellum index build` first.",
            file=sys.stderr,
        )
        return 2

    conn = sqlite3.connect(str(db))
    try:
        notes = _load_fz_notes(conn)
    finally:
        conn.close()

    if op == "list":
        return _cmd_list(notes)
    if op == "show":
        return _cmd_show(notes, args.query)
    if op == "ancestors":
        return _cmd_ancestors(notes, args.query)
    if op == "descendants":
        return _cmd_descendants(notes, args.query)
    if op == "path":
        return _cmd_path(notes, args.query)
    if op == "all":
        return _cmd_all(notes)
    print(f"tessellum fz: unknown operation {op!r}.", file=sys.stderr)
    return 2
