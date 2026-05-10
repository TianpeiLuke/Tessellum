"""``tessellum init <dir>`` — scaffold a new Tessellum vault.

Thin CLI wrapper over :func:`tessellum.init.scaffold`.

Exit codes:
    0  scaffold succeeded
    1  target exists and is non-empty (without --force)
    2  invocation error (target is a file, package data missing, etc.)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tessellum.init import scaffold


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    init = subparsers.add_parser(
        "init",
        help="Scaffold a new Tessellum vault.",
    )
    init.add_argument(
        "target",
        type=Path,
        help="Directory to scaffold the vault in. May or may not exist.",
    )
    init.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Allow scaffolding into an existing non-empty directory "
        "(overwrites files at scaffolded paths; preserves other content).",
    )
    init.set_defaults(func=run_init)


def run_init(args: argparse.Namespace) -> int:
    try:
        result = scaffold(args.target, force=args.force)
    except FileExistsError as e:
        print(f"tessellum init: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"tessellum init: {e}", file=sys.stderr)
        return 2

    print(f"scaffolded vault at: {result.target}")
    print(f"  directories created: {len(result.dirs_created)}")
    print(f"  files copied:        {len(result.files_copied)}")
    print(f"  files written:       {len(result.files_written)}")
    print()
    print("Next steps:")
    print(f"  cd {result.target}")
    print("  tessellum capture concept my_topic --vault .")
    print("  tessellum format check .")
    return 0
