"""``tessellum search <query>`` — query the indexed vault.

v0.0.13 ships BM25 only. Per ``plans/plan_retrieval_port.md``, Wave 3
(v0.0.15) flips the default to hybrid RRF; v0.0.13's bare
``tessellum search foo`` runs BM25 (the only strategy currently
implemented). The ``--bm25`` flag is accepted for forward-compat — once
``--dense`` and hybrid land, ``--bm25`` becomes a real selector.

Exit codes:
    0  search ran (results may be empty if no match)
    2  invocation error (DB missing, malformed query, etc.)
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from tessellum.retrieval import BM25Hit, bm25_search


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    search = subparsers.add_parser(
        "search",
        help="Query the indexed vault (BM25 in v0.0.13; dense + hybrid in v0.0.14+).",
    )
    search.add_argument("query", help="Search query (FTS5 MATCH syntax).")
    search.add_argument(
        "--bm25",
        action="store_true",
        help="Use BM25 lexical retrieval (currently the default; explicit flag "
        "for forward-compat with Wave 2-3 strategy selectors).",
    )
    search.add_argument(
        "--db",
        type=Path,
        default=Path("data") / "tessellum.db",
        help="Index DB path (default: ./data/tessellum.db).",
    )
    search.add_argument(
        "--k",
        type=int,
        default=20,
        help="Maximum number of results (default: 20).",
    )
    search.add_argument(
        "--no-snippet",
        action="store_true",
        help="Skip snippet generation (small speedup for batch queries).",
    )
    search.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    search.set_defaults(func=run_search)


def run_search(args: argparse.Namespace) -> int:
    db = args.db.expanduser().resolve()
    if not db.is_file():
        print(
            f"tessellum search: index DB not found at {db}. "
            f"Run `tessellum index build` first.",
            file=sys.stderr,
        )
        return 2

    snippet_length = None if args.no_snippet else 30

    try:
        hits = bm25_search(db, args.query, k=args.k, snippet_length=snippet_length)
    except FileNotFoundError as e:
        print(f"tessellum search: {e}", file=sys.stderr)
        return 2
    except sqlite3.OperationalError as e:
        print(f"tessellum search: query failed — {e}", file=sys.stderr)
        return 2

    if args.output_format == "json":
        return _emit_json(hits, args.query)
    return _emit_human(hits, args.query)


def _emit_human(hits: list[BM25Hit], query: str) -> int:
    if not hits:
        print(f"BM25 search: no matches for {query!r}")
        return 0
    print(f"BM25 matches for {query!r}  ({len(hits)} hit{'s' if len(hits) != 1 else ''})")
    print()
    for i, hit in enumerate(hits, 1):
        print(f"  {i:2d}. {hit.note_name}  ({hit.score:.3f})")
        print(f"      {hit.note_id}")
        if hit.snippet:
            # Indent multi-line snippets so they align under the note line.
            cleaned = hit.snippet.replace("\n", " ").strip()
            print(f"      {cleaned}")
        print()
    return 0


def _emit_json(hits: list[BM25Hit], query: str) -> int:
    payload = {
        "query": query,
        "strategy": "bm25",
        "hit_count": len(hits),
        "hits": [
            {
                "note_id": h.note_id,
                "note_name": h.note_name,
                "score": h.score,
                "snippet": h.snippet,
            }
            for h in hits
        ],
    }
    print(json.dumps(payload, indent=2))
    return 0
