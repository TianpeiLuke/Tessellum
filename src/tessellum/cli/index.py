"""``tessellum index build`` — build the unified SQLite index from a vault.

Mirrors the established CLI pattern (``format check``, ``capture``,
``composer validate``, ``init``): single subcommand, sensible defaults,
clear exit codes.

Exit codes:
    0  index built successfully
    1  output DB exists and ``--force`` not passed
    2  invocation error (vault doesn't exist, etc.)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tessellum.indexer import build


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    index = subparsers.add_parser(
        "index",
        help="Vault index operations (build, ...).",
    )
    index_sub = index.add_subparsers(dest="index_command", required=True)

    build_cmd = index_sub.add_parser(
        "build",
        help="Build the unified SQLite index from a vault.",
    )
    build_cmd.add_argument(
        "--vault",
        type=Path,
        default=Path("vault"),
        help="Vault root directory (default: ./vault).",
    )
    build_cmd.add_argument(
        "--db",
        type=Path,
        default=Path("data") / "tessellum.db",
        help="Output SQLite DB path (default: ./data/tessellum.db).",
    )
    build_cmd.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite an existing DB at the output path.",
    )
    build_cmd.set_defaults(func=run_index_build)


def run_index_build(args: argparse.Namespace) -> int:
    vault = args.vault.expanduser().resolve()
    db = args.db.expanduser().resolve()

    try:
        result = build(vault, db, force=args.force)
    except FileNotFoundError as e:
        print(f"tessellum index build: {e}", file=sys.stderr)
        return 2
    except FileExistsError as e:
        print(f"tessellum index build: {e}", file=sys.stderr)
        return 1

    print(f"built index at: {result.db_path}")
    print(f"  notes indexed:  {result.notes_indexed}")
    print(f"  links indexed:  {result.links_indexed}")
    if result.skipped_files:
        print(f"  files skipped:  {result.skipped_files} (unparseable frontmatter)")
    print(f"  duration:       {result.duration_seconds:.2f}s")
    return 0
