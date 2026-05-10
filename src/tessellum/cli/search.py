"""``tessellum search <query>`` — query the indexed vault.

v0.0.15 ships **hybrid as the default** — `tessellum search foo` runs
BM25 + dense fused via Reciprocal Rank Fusion (RRF). Pass ``--bm25``,
``--dense``, or ``--hybrid`` to select an explicit strategy.

The default flip is per ``plans/plan_retrieval_port.md`` Wave 3: the
parent project's experiments measured +12pp Hit@5 lift for hybrid over
the best single strategy on real queries (FZ 5e1c3a1a1).

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

from tessellum.retrieval import (
    BM25Hit,
    DenseHit,
    HybridHit,
    bm25_search,
    dense_search,
    hybrid_search,
)


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    search = subparsers.add_parser(
        "search",
        help="Query the indexed vault (hybrid by default; --bm25 / --dense for ablation).",
    )
    search.add_argument(
        "query",
        help="Search query. FTS5 MATCH syntax for --bm25; natural language otherwise.",
    )

    strategy = search.add_mutually_exclusive_group()
    strategy.add_argument(
        "--hybrid",
        dest="strategy",
        action="store_const",
        const="hybrid",
        help="Use hybrid retrieval — BM25 + dense fused via RRF (default).",
    )
    strategy.add_argument(
        "--bm25",
        dest="strategy",
        action="store_const",
        const="bm25",
        help="Use BM25 lexical retrieval only.",
    )
    strategy.add_argument(
        "--dense",
        dest="strategy",
        action="store_const",
        const="dense",
        help="Use dense semantic retrieval only.",
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
        help="(BM25 only) Skip snippet generation.",
    )
    search.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    search.set_defaults(func=run_search, strategy="hybrid")


def run_search(args: argparse.Namespace) -> int:
    db = args.db.expanduser().resolve()
    if not db.is_file():
        print(
            f"tessellum search: index DB not found at {db}. "
            f"Run `tessellum index build` first.",
            file=sys.stderr,
        )
        return 2

    strategy = getattr(args, "strategy", "hybrid") or "hybrid"

    try:
        if strategy == "dense":
            hits = dense_search(db, args.query, k=args.k)
        elif strategy == "bm25":
            snippet_length = None if args.no_snippet else 30
            hits = bm25_search(
                db, args.query, k=args.k, snippet_length=snippet_length
            )
        else:  # hybrid
            hits = hybrid_search(db, args.query, k=args.k)
    except FileNotFoundError as e:
        print(f"tessellum search: {e}", file=sys.stderr)
        return 2
    except sqlite3.OperationalError as e:
        print(f"tessellum search: query failed — {e}", file=sys.stderr)
        return 2

    if args.output_format == "json":
        return _emit_json(hits, args.query, strategy)
    return _emit_human(hits, args.query, strategy)


def _emit_human(hits: list, query: str, strategy: str) -> int:
    label = strategy.upper()
    if not hits:
        print(f"{label} search: no matches for {query!r}")
        return 0
    print(
        f"{label} matches for {query!r}  "
        f"({len(hits)} hit{'s' if len(hits) != 1 else ''})"
    )
    print()
    for i, hit in enumerate(hits, 1):
        print(f"  {i:2d}. {hit.note_name}  ({hit.score:.4f})")
        print(f"      {hit.note_id}")
        if isinstance(hit, HybridHit):
            ranks = []
            if hit.bm25_rank is not None:
                ranks.append(f"bm25=#{hit.bm25_rank}")
            if hit.dense_rank is not None:
                ranks.append(f"dense=#{hit.dense_rank}")
            if ranks:
                print(f"      [{' '.join(ranks)}]")
        snippet = getattr(hit, "snippet", None)
        if snippet:
            cleaned = snippet.replace("\n", " ").strip()
            print(f"      {cleaned}")
        print()
    return 0


def _emit_json(hits: list, query: str, strategy: str) -> int:
    payload_hits: list[dict] = []
    for h in hits:
        record: dict = {
            "note_id": h.note_id,
            "note_name": h.note_name,
            "score": h.score,
        }
        if isinstance(h, BM25Hit):
            record["snippet"] = h.snippet
        elif isinstance(h, DenseHit):
            record["distance"] = h.distance
        elif isinstance(h, HybridHit):
            record["bm25_rank"] = h.bm25_rank
            record["dense_rank"] = h.dense_rank
        payload_hits.append(record)

    payload = {
        "query": query,
        "strategy": strategy,
        "hit_count": len(hits),
        "hits": payload_hits,
    }
    print(json.dumps(payload, indent=2))
    return 0
