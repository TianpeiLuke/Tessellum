"""``tessellum filter`` — query the indexed vault by structured metadata.

The simplest retrieval surface — direct SQL filtering on the YAML fields
extracted into ``notes`` columns. Use this when you know *what kind* of
note you want, not *what content*. The four content-search strategies
(``--bm25``, ``--dense``, ``--hybrid``, ``--bfs``) live under
``tessellum search``; this command is metadata-only.

```bash
tessellum filter --building-block concept --status active
tessellum filter --tag cqrs --date-after 2026-01-01
tessellum filter --building-block argument --topic "Knowledge Management"
tessellum filter --has-folgezettel       # all FZ-trail notes
tessellum filter --folgezettel-prefix 7  # all notes in trail 7 (7, 7a, 7a1, ...)
```

All filters AND-combine. Pass no filters to list every note (up to ``--k``).

Exit codes:
    0  filter ran (results may be empty)
    2  invocation error (DB missing, etc.)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tessellum.retrieval import MetadataHit, metadata_search


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    flt = subparsers.add_parser(
        "filter",
        help="Filter notes by structured metadata (tags, status, BB, dates, ...).",
    )

    flt.add_argument(
        "--db",
        type=Path,
        default=Path("data") / "tessellum.db",
        help="Index DB path (default: ./data/tessellum.db).",
    )
    flt.add_argument(
        "--k",
        type=int,
        default=100,
        help="Maximum number of results (default: 100).",
    )
    flt.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )

    # Closed-enum fields
    flt.add_argument(
        "--building-block",
        help="Exact match on building_block (concept, procedure, model, ...).",
    )
    flt.add_argument(
        "--status",
        help="Exact match on status (active, draft, archived, template, ...).",
    )
    flt.add_argument(
        "--category",
        help="Exact match on tags[0] / PARA bucket (resource, area, project, archive, entry_point).",
    )
    flt.add_argument(
        "--second-category",
        help="Exact match on tags[1] (terminology, skill, how_to, analysis, ...).",
    )

    # Open-vocabulary JSON-array fields (any-of match)
    flt.add_argument(
        "--tag",
        help="Note's tags[] contains this value (any-of match).",
    )
    flt.add_argument(
        "--keyword",
        help="Note's keywords[] contains this value (any-of match).",
    )
    flt.add_argument(
        "--topic",
        help="Note's topics[] contains this value (any-of match).",
    )

    # Date filters
    flt.add_argument(
        "--date-after",
        help="YYYY-MM-DD; notes whose 'date of note' is on or after this date.",
    )
    flt.add_argument(
        "--date-before",
        help="YYYY-MM-DD; notes whose 'date of note' is on or before this date.",
    )

    # Folgezettel filters
    flt.add_argument(
        "--folgezettel-prefix",
        help="String-prefix match on folgezettel (e.g. '7' matches 7, 7a, 7a1, 7a1a).",
    )
    folge_group = flt.add_mutually_exclusive_group()
    folge_group.add_argument(
        "--has-folgezettel",
        dest="has_folgezettel",
        action="store_const",
        const=True,
        help="Only return notes with a folgezettel (trail nodes).",
    )
    folge_group.add_argument(
        "--no-folgezettel",
        dest="has_folgezettel",
        action="store_const",
        const=False,
        help="Only return notes WITHOUT a folgezettel (non-trail nodes).",
    )

    flt.set_defaults(func=run_filter, has_folgezettel=None)


def run_filter(args: argparse.Namespace) -> int:
    db = args.db.expanduser().resolve()
    if not db.is_file():
        print(
            f"tessellum filter: index DB not found at {db}. "
            f"Run `tessellum index build` first.",
            file=sys.stderr,
        )
        return 2

    try:
        hits = metadata_search(
            db,
            building_block=args.building_block,
            status=args.status,
            category=args.category,
            second_category=args.second_category,
            tag=args.tag,
            keyword=args.keyword,
            topic=args.topic,
            date_after=args.date_after,
            date_before=args.date_before,
            folgezettel_prefix=args.folgezettel_prefix,
            has_folgezettel=args.has_folgezettel,
            k=args.k,
        )
    except FileNotFoundError as e:
        print(f"tessellum filter: {e}", file=sys.stderr)
        return 2

    if args.output_format == "json":
        return _emit_json(hits, args)
    return _emit_human(hits, args)


def _summarize_filters(args: argparse.Namespace) -> str:
    parts: list[str] = []
    for label, value in [
        ("building_block", args.building_block),
        ("status", args.status),
        ("category", args.category),
        ("second_category", args.second_category),
        ("tag", args.tag),
        ("keyword", args.keyword),
        ("topic", args.topic),
        ("date_after", args.date_after),
        ("date_before", args.date_before),
        ("folgezettel_prefix", args.folgezettel_prefix),
    ]:
        if value is not None:
            parts.append(f"{label}={value!r}")
    if args.has_folgezettel is True:
        parts.append("has_folgezettel=True")
    elif args.has_folgezettel is False:
        parts.append("has_folgezettel=False")
    return ", ".join(parts) if parts else "(no filters)"


def _emit_human(hits: list[MetadataHit], args: argparse.Namespace) -> int:
    summary = _summarize_filters(args)
    if not hits:
        print(f"FILTER: no notes match {summary}")
        return 0
    print(f"FILTER {summary}  ({len(hits)} hit{'s' if len(hits) != 1 else ''})")
    print()
    for i, hit in enumerate(hits, 1):
        print(f"  {i:2d}. {hit.note_name}")
        print(f"      {hit.note_id}")
        bits = [
            f"BB={hit.building_block or '?'}",
            f"status={hit.note_status or '?'}",
        ]
        if hit.note_second_category:
            bits.append(f"sub={hit.note_second_category}")
        if hit.folgezettel:
            bits.append(f"FZ={hit.folgezettel}")
        if hit.note_creation_date:
            bits.append(f"date={hit.note_creation_date}")
        print(f"      [{'  '.join(bits)}]")
        print()
    return 0


def _emit_json(hits: list[MetadataHit], args: argparse.Namespace) -> int:
    payload = {
        "filters": {
            "building_block": args.building_block,
            "status": args.status,
            "category": args.category,
            "second_category": args.second_category,
            "tag": args.tag,
            "keyword": args.keyword,
            "topic": args.topic,
            "date_after": args.date_after,
            "date_before": args.date_before,
            "folgezettel_prefix": args.folgezettel_prefix,
            "has_folgezettel": args.has_folgezettel,
        },
        "hit_count": len(hits),
        "hits": [
            {
                "note_id": h.note_id,
                "note_name": h.note_name,
                "note_category": h.note_category,
                "note_second_category": h.note_second_category,
                "note_status": h.note_status,
                "building_block": h.building_block,
                "note_creation_date": h.note_creation_date,
                "folgezettel": h.folgezettel,
            }
            for h in hits
        ],
    }
    print(json.dumps(payload, indent=2))
    return 0
