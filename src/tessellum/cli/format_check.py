"""``tessellum format check`` — validate notes against the YAML frontmatter spec.

Wires ``tessellum.format.validator`` into a CLI subcommand. Accepts a file or
directory; directories recurse over ``*.md``. Exit code:

  0 — no errors (warnings allowed unless --strict)
  1 — at least one ERROR (or any WARNING under --strict)
  2 — invocation error (path doesn't exist, etc.)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tessellum.format import Severity, validate


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    fmt = subparsers.add_parser(
        "format",
        help="Note format operations (check, ...).",
    )
    fmt_sub = fmt.add_subparsers(dest="format_command", required=True)

    check = fmt_sub.add_parser(
        "check",
        help="Validate notes against the YAML frontmatter spec.",
    )
    check.add_argument(
        "path",
        type=Path,
        help="Markdown file or directory. Directories recurse over *.md.",
    )
    check.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors (exit 1 if any warnings).",
    )
    check.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Print only files with issues; suppress the summary if clean.",
    )
    check.set_defaults(func=run_format_check)


def run_format_check(args: argparse.Namespace) -> int:
    target: Path = args.path.expanduser().resolve()

    if not target.exists():
        print(f"tessellum format check: {target} does not exist", file=sys.stderr)
        return 2

    if target.is_dir():
        files = sorted(target.rglob("*.md"))
        base = target
    elif target.is_file() and target.suffix == ".md":
        files = [target]
        base = target.parent
    else:
        print(
            f"tessellum format check: {target} is neither a markdown file nor a directory",
            file=sys.stderr,
        )
        return 2

    if not files:
        print(f"tessellum format check: no markdown files under {target}", file=sys.stderr)
        return 0

    total_errors = 0
    total_warnings = 0
    files_with_issues = 0

    for f in files:
        issues = validate(f)
        if not issues:
            continue
        files_with_issues += 1
        try:
            rel = f.relative_to(base)
        except ValueError:
            rel = f
        print(f"{rel}:")
        for issue in issues:
            print(f"  {issue}")
            if issue.severity is Severity.ERROR:
                total_errors += 1
            else:
                total_warnings += 1

    if not args.quiet or files_with_issues:
        print()
        print(
            f"validated {len(files)} file(s); "
            f"{files_with_issues} with issues; "
            f"{total_errors} error(s), {total_warnings} warning(s)"
        )

    if total_errors > 0:
        return 1
    if args.strict and total_warnings > 0:
        return 1
    return 0
