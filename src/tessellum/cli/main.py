"""Tessellum CLI dispatcher. ``tessellum`` resolves to ``main()`` here.

Subcommand wiring lives in sibling modules (e.g. ``format_check``); each
exposes ``add_subparser(subparsers)``. Bare ``tessellum`` (no subcommand)
prints the version + capability banner.
"""

from __future__ import annotations

import argparse
import sys

from tessellum.__about__ import __status__, __version__
from tessellum.cli.capture import add_subparser as add_capture_subparser
from tessellum.cli.composer import add_subparser as add_composer_subparser
from tessellum.cli.format_check import add_subparser as add_format_subparser
from tessellum.cli.init import add_subparser as add_init_subparser


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tessellum",
        description="Tessellum — typed atomic notes in a graph.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"tessellum {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")
    add_init_subparser(subparsers)
    add_format_subparser(subparsers)
    add_capture_subparser(subparsers)
    add_composer_subparser(subparsers)
    return parser


def _print_banner() -> None:
    print(f"tessellum {__version__}")
    print(__status__)
    print()
    print("Available now (Python API):")
    print("  from tessellum import BuildingBlock, BB_SPECS, EPISTEMIC_EDGES")
    print("  from tessellum import validate, is_valid, parse_note, Note, Issue")
    print("  from tessellum.capture import capture, REGISTRY")
    print("  from tessellum.composer import load_pipeline, Pipeline, ContractViolation")
    print("  from tessellum.init import scaffold")
    print("  from tessellum.data import templates_dir, seed_vault_dir")
    print()
    print("Available now (CLI):")
    print("  tessellum init <dir>                — scaffold a new vault")
    print("  tessellum format check <path>       — validate notes against the YAML spec")
    print("  tessellum capture <flavor> <slug>   — create a new note from a template")
    print("  tessellum composer validate <skill> — validate a skill's pipeline sidecar")
    print()
    print("Roadmap:")
    print("  tessellum search <q>     — hybrid retrieval (BM25 + dense + RRF)")
    print("  tessellum composer compile/run  — Composer Wave 2-3")
    print()
    print("See https://github.com/TianpeiLuke/Tessellum for the v0.1 plan.")


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        return args.func(args)
    _print_banner()
    return 0


if __name__ == "__main__":
    sys.exit(main())
