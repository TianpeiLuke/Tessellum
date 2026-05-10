"""``tessellum composer validate <skill>`` — validate a skill's pipeline sidecar.

Mirrors the ``tessellum format check`` pattern: accepts a single file or a
directory (recurses over ``skill_*.md``), supports ``--format json`` for CI.
Each skill is validated via :func:`tessellum.composer.load_pipeline`, which
runs three-stage validation:

    1. JSON Schema (structural)
    2. Pydantic V2 model construction (typed access + immutability)
    3. Cross-file consistency (every sidebar section_id has a canonical anchor)

Exit codes:
    0  every skill validates clean (or declares ``pipeline_metadata: none``)
    1  at least one skill fails validation
    2  invocation error (path doesn't exist, etc.)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tessellum.composer import PipelineValidationError, load_pipeline


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    composer = subparsers.add_parser(
        "composer",
        help="Composer pipeline operations (validate, ...).",
    )
    composer_sub = composer.add_subparsers(dest="composer_command", required=True)

    validate = composer_sub.add_parser(
        "validate",
        help="Validate a skill canonical's pipeline sidecar against the spec.",
    )
    validate.add_argument(
        "skill",
        type=Path,
        help="Skill canonical (markdown file) or directory to recurse over.",
    )
    validate.add_argument(
        "--format",
        dest="output_format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human).",
    )
    validate.set_defaults(func=run_composer_validate)


def run_composer_validate(args: argparse.Namespace) -> int:
    target: Path = args.skill.expanduser().resolve()

    if not target.exists():
        print(
            f"tessellum composer validate: {target} does not exist",
            file=sys.stderr,
        )
        return 2

    if target.is_dir():
        skills = sorted(p for p in target.glob("skill_*.md"))
    elif target.is_file() and target.suffix == ".md":
        skills = [target]
    else:
        print(
            f"tessellum composer validate: {target} is neither a markdown "
            f"file nor a directory",
            file=sys.stderr,
        )
        return 2

    if not skills:
        if args.output_format == "json":
            print(json.dumps({"skills": [], "summary": _empty_summary()}, indent=2))
        else:
            print(
                f"tessellum composer validate: no skill_*.md files under {target}",
                file=sys.stderr,
            )
        return 0

    if args.output_format == "json":
        return _emit_json(skills, target)
    return _emit_human(skills, target)


def _empty_summary() -> dict:
    return {"total": 0, "passed": 0, "failed": 0}


def _relative(path: Path, base: Path) -> str:
    try:
        if base.is_dir():
            return str(path.relative_to(base))
        return str(path.relative_to(base.parent))
    except ValueError:
        return str(path)


def _emit_human(skills: list[Path], base: Path) -> int:
    failed = 0
    for skill in skills:
        rel = _relative(skill, base)
        try:
            pipeline = load_pipeline(skill)
        except PipelineValidationError as e:
            print(f"FAIL {rel}")
            for line in str(e).splitlines():
                print(f"     {line}")
            failed += 1
            continue

        if pipeline is None:
            print(f"OK   {rel} (pipeline_metadata: none)")
        else:
            steps = len(pipeline.pipeline)
            print(f"OK   {rel} ({steps} step{'s' if steps != 1 else ''})")

    print()
    print(
        f"validated {len(skills)} skill(s); "
        f"{len(skills) - failed} passed, {failed} failed"
    )
    return 1 if failed else 0


def _emit_json(skills: list[Path], base: Path) -> int:
    results: list[dict] = []
    failed = 0
    for skill in skills:
        rel = _relative(skill, base)
        try:
            pipeline = load_pipeline(skill)
        except PipelineValidationError as e:
            failed += 1
            results.append(
                {
                    "skill": rel,
                    "status": "fail",
                    "has_pipeline": None,
                    "step_count": None,
                    "error": str(e),
                }
            )
            continue

        results.append(
            {
                "skill": rel,
                "status": "ok",
                "has_pipeline": pipeline is not None,
                "step_count": len(pipeline.pipeline) if pipeline else 0,
                "error": None,
            }
        )

    payload = {
        "skills": results,
        "summary": {
            "total": len(skills),
            "passed": len(skills) - failed,
            "failed": failed,
        },
    }
    print(json.dumps(payload, indent=2))
    return 1 if failed else 0
