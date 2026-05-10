"""``tessellum capture <flavor> <slug>`` — create a new vault note from a template.

Thin CLI wrapper over :func:`tessellum.capture.capture`. See that module for
the canonical capture logic and the template registry.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tessellum.capture import capture, list_flavors


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    cap = subparsers.add_parser(
        "capture",
        help="Create a new vault note from a typed template.",
    )
    cap.add_argument(
        "flavor",
        choices=list_flavors(),
        metavar="FLAVOR",
        help="Template flavor: " + ", ".join(list_flavors()),
    )
    cap.add_argument(
        "slug",
        metavar="SLUG",
        help="New note's identifier (lowercase letters/digits/underscores).",
    )
    cap.add_argument(
        "--vault",
        type=Path,
        default=Path("vault"),
        help="Vault root directory (default: ./vault).",
    )
    cap.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite an existing target file.",
    )
    cap.set_defaults(func=run_capture)


def run_capture(args: argparse.Namespace) -> int:
    vault_root = args.vault.expanduser().resolve()
    try:
        result = capture(
            flavor=args.flavor,
            slug=args.slug,
            vault_root=vault_root,
            force=args.force,
        )
    except ValueError as e:
        print(f"tessellum capture: {e}", file=sys.stderr)
        return 2
    except FileExistsError as e:
        print(f"tessellum capture: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"tessellum capture: {e}", file=sys.stderr)
        return 2

    print(f"created: {result.path}")
    print(f"  flavor:  {result.flavor}")
    print(f"  next:    fill placeholders, then `tessellum format check {result.path}`")
    return 0
