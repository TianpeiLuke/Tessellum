"""``tessellum mcp serve`` — run the Tessellum MCP server (stdio transport).

Phase V of ``plans/plan_v01_completion_roadmap.md`` (v0.0.59). Exposes
Tessellum's runtime APIs as MCP tools so MCP-compatible agents
(Claude Desktop, IDEs, etc.) can invoke them.

The server is built lazily — the ``mcp`` SDK is only imported when
``serve`` is invoked, so users without the ``[mcp]`` extras can still
load the CLI without errors.

Exit codes:
    0   server ran cleanly (client closed the connection)
    2   missing [mcp] extras, invocation error
"""

from __future__ import annotations

import argparse
import sys


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    mcp = subparsers.add_parser(
        "mcp",
        help="MCP server — expose Tessellum runtime APIs as MCP tools.",
    )

    sub = mcp.add_subparsers(dest="mcp_command")

    serve = sub.add_parser(
        "serve",
        help="Run the MCP stdio server (for Claude Desktop and similar hosts).",
    )
    serve.set_defaults(func=run_mcp_serve, _mcp_op="serve")

    mcp.set_defaults(func=run_mcp_serve, _mcp_op=None)


def run_mcp_serve(args: argparse.Namespace) -> int:
    op = getattr(args, "_mcp_op", None)
    if op is None:
        print(
            "tessellum mcp: missing sub-subcommand. Try `tessellum mcp serve`.",
            file=sys.stderr,
        )
        return 2

    try:
        from tessellum.mcp import run_stdio
    except ImportError as e:
        print(
            "tessellum mcp: missing the [mcp] extras. "
            "Install with: pip install tessellum[mcp]",
            file=sys.stderr,
        )
        print(f"  ({e})", file=sys.stderr)
        return 2

    return run_stdio()
