"""``tessellum format check`` — validate notes against the YAML frontmatter spec.

Wires ``tessellum.format.validator`` into a CLI subcommand. Accepts a file or
directory; directories recurse over ``*.md`` and skip non-note files
(``README.md``, ``CHANGELOG.md``, ``CONTRIBUTING.md``, ``DEVELOPING.md``,
``LICENSE.md``, ``MEMORY.md``, ``Rank_*.md``).

Output formats:
    --format human   Default. Per-file issue list + trailing summary.
    --format json    Machine-readable; structure documented below.

Exit code:
    0  no errors (warnings/infos allowed unless --strict)
    1  at least one ERROR (or any WARNING under --strict)
    2  invocation error (path doesn't exist, etc.)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tessellum.format import Issue, Severity, validate

_NON_NOTE_NAMES: frozenset[str] = frozenset(
    {
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "DEVELOPING.md",
        "LICENSE.md",
        "MEMORY.md",
    }
)

_NON_NOTE_PREFIXES: tuple[str, ...] = ("Rank_",)


def _is_note_file(p: Path) -> bool:
    if p.name in _NON_NOTE_NAMES:
        return False
    if any(p.name.startswith(prefix) for prefix in _NON_NOTE_PREFIXES):
        return False
    return True


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
    check.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    check.set_defaults(func=run_format_check)


def run_format_check(args: argparse.Namespace) -> int:
    target: Path = args.path.expanduser().resolve()

    if not target.exists():
        print(
            f"tessellum format check: {target} does not exist",
            file=sys.stderr,
        )
        return 2

    if target.is_dir():
        files = [f for f in sorted(target.rglob("*.md")) if _is_note_file(f)]
        base = target
    elif target.is_file() and target.suffix == ".md":
        files = [target]
        base = target.parent
    else:
        print(
            f"tessellum format check: {target} is neither a markdown file "
            f"nor a directory",
            file=sys.stderr,
        )
        return 2

    if not files:
        if args.output_format == "json":
            print(json.dumps({"files": [], "summary": _empty_summary()}, indent=2))
        else:
            print(
                f"tessellum format check: no markdown files under {target}",
                file=sys.stderr,
            )
        return 0

    file_results: list[tuple[Path, list[Issue]]] = [(f, validate(f)) for f in files]

    if args.output_format == "json":
        return _emit_json(file_results, base, args.strict)
    return _emit_human(file_results, base, args.strict, args.quiet)


def _empty_summary() -> dict:
    return {
        "files_checked": 0,
        "files_with_issues": 0,
        "errors": 0,
        "warnings": 0,
        "infos": 0,
    }


def _emit_human(
    file_results: list[tuple[Path, list[Issue]]],
    base: Path,
    strict: bool,
    quiet: bool,
) -> int:
    total_errors = 0
    total_warnings = 0
    total_infos = 0
    files_with_issues = 0

    for f, issues in file_results:
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
            elif issue.severity is Severity.WARNING:
                total_warnings += 1
            else:
                total_infos += 1

    if not quiet or files_with_issues:
        print()
        print(
            f"validated {len(file_results)} file(s); "
            f"{files_with_issues} with issues; "
            f"{total_errors} error(s), {total_warnings} warning(s), "
            f"{total_infos} info(s)"
        )

    return _exit_code(total_errors, total_warnings, strict)


def _emit_json(
    file_results: list[tuple[Path, list[Issue]]],
    base: Path,
    strict: bool,
) -> int:
    total_errors = 0
    total_warnings = 0
    total_infos = 0
    files_with_issues = 0

    files_payload: list[dict] = []
    for f, issues in file_results:
        if issues:
            files_with_issues += 1
        try:
            rel_str = str(f.relative_to(base))
        except ValueError:
            rel_str = str(f)
        files_payload.append(
            {
                "path": rel_str,
                "issues": [
                    {
                        "rule_id": i.rule_id,
                        "severity": i.severity.value,
                        "field": i.field,
                        "message": i.message,
                    }
                    for i in issues
                ],
            }
        )
        for i in issues:
            if i.severity is Severity.ERROR:
                total_errors += 1
            elif i.severity is Severity.WARNING:
                total_warnings += 1
            else:
                total_infos += 1

    payload = {
        "files": files_payload,
        "summary": {
            "files_checked": len(file_results),
            "files_with_issues": files_with_issues,
            "errors": total_errors,
            "warnings": total_warnings,
            "infos": total_infos,
        },
    }
    print(json.dumps(payload, indent=2))
    return _exit_code(total_errors, total_warnings, strict)


def _exit_code(errors: int, warnings: int, strict: bool) -> int:
    if errors > 0:
        return 1
    if strict and warnings > 0:
        return 1
    return 0
