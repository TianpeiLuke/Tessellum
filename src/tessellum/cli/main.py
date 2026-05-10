"""v0.0.1 CLI: report version + roadmap. No vault-touching subcommands yet."""

from __future__ import annotations

import argparse
import sys

from tessellum.__about__ import __status__, __version__


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
    return parser


def main(argv: list[str] | None = None) -> int:
    _build_parser().parse_args(argv)
    print(f"tessellum {__version__}")
    print(__status__)
    print()
    print("Available now (Python API):")
    print("  from tessellum import BuildingBlock, BB_SPECS, EPISTEMIC_EDGES")
    print("  from tessellum import validate, is_valid, parse_note, Note, Issue")
    print()
    print("Roadmap:")
    print("  tessellum format check   — validate notes against the YAML spec")
    print("  tessellum init           — scaffold a new vault")
    print("  tessellum capture <bb>   — copy a BB-typed template")
    print("  tessellum search <q>     — hybrid retrieval (BM25 + dense + RRF)")
    print()
    print("See https://github.com/TianpeiLuke/Tessellum for the v0.1 plan.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
