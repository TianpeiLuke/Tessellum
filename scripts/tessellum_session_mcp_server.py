#!/usr/bin/env python3
"""tessellum-session-mcp — stdio MCP server.

Thin protocol wrapper around the pure handlers in
:mod:`tessellum.composer.session_mcp`. Exposes the 4 session tools
over stdio JSON-RPC so Claude Code (or any MCP-compatible host) can
invoke them.

Registration in ``~/.claude/settings.json`` (or per-project
``.claude/settings.json``)::

    {
      "mcpServers": {
        "tessellum-session-mcp": {
          "command": "python3",
          "args": ["/absolute/path/to/scripts/tessellum_session_mcp_server.py"]
        }
      }
    }

Transcript path resolution mirrors the handler's documented order:

    1. ``--transcript-path PATH`` CLI arg
    2. ``SESSION_TRANSCRIPT_PATH`` env var
    3. Auto-detect: most recent ``~/.claude/projects/<encoded-cwd>/*.jsonl``

Requires the ``mcp`` Python SDK (``pip install tessellum[mcp]``).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from tessellum.composer.session_mcp import (
    get_session_metadata,
    get_tool_uses,
    read_recent_messages,
    resolve_transcript_path,
    search_transcript,
)

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool
except ImportError as e:
    sys.stderr.write(
        "tessellum-session-mcp requires the `mcp` Python SDK.\n"
        "Install via:  pip install tessellum[mcp]\n"
        f"(import error: {e})\n"
    )
    sys.exit(1)


def _build_server(transcript_path_override: Path | None) -> Server:
    """Construct the MCP server with the 4 session tools registered."""
    server = Server("tessellum-session-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="get_session_metadata",
                description=(
                    "Static snapshot of the active Claude Code session — "
                    "session_id, cwd, git_branch, model, user/assistant turn "
                    "counts, transcript size + mtime."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
            ),
            Tool(
                name="read_recent_messages",
                description=(
                    "Last N user/assistant messages with role + flattened text. "
                    "By default strips assistant `thinking` blocks (verbose); "
                    "set include_thinking=true to keep them."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "n": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 200,
                            "default": 20,
                        },
                        "include_thinking": {
                            "type": "boolean",
                            "default": False,
                        },
                    },
                    "additionalProperties": False,
                },
            ),
            Tool(
                name="search_transcript",
                description=(
                    "Search messages for `query` (keyword by default; regex if "
                    "regex=true). Returns matching messages with role + 200-char "
                    "snippet around each match."
                ),
                inputSchema={
                    "type": "object",
                    "required": ["query"],
                    "properties": {
                        "query": {"type": "string"},
                        "regex": {"type": "boolean", "default": False},
                        "max_matches": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 500,
                            "default": 50,
                        },
                    },
                    "additionalProperties": False,
                },
            ),
            Tool(
                name="get_tool_uses",
                description=(
                    "Extract tool_use blocks from assistant messages. "
                    "Optionally filter by `tool_name_pattern` (regex)."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tool_name_pattern": {"type": "string"},
                        "max_results": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 500,
                            "default": 100,
                        },
                    },
                    "additionalProperties": False,
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        transcript_path = resolve_transcript_path(transcript_path_override)
        if transcript_path is None:
            payload = {
                "error": "no_active_session",
                "detail": (
                    "No transcript could be located. Pass --transcript-path, "
                    "set SESSION_TRANSCRIPT_PATH, or invoke from inside an "
                    "active Claude Code session whose project directory has "
                    "a transcript at ~/.claude/projects/<encoded-cwd>/."
                ),
            }
            return [TextContent(type="text", text=json.dumps(payload))]

        if name == "get_session_metadata":
            result = get_session_metadata(transcript_path)
        elif name == "read_recent_messages":
            result = read_recent_messages(
                transcript_path,
                n=arguments.get("n", 20),
                include_thinking=arguments.get("include_thinking", False),
            )
        elif name == "search_transcript":
            result = search_transcript(
                transcript_path,
                query=arguments["query"],
                regex=arguments.get("regex", False),
                max_matches=arguments.get("max_matches", 50),
            )
        elif name == "get_tool_uses":
            result = get_tool_uses(
                transcript_path,
                tool_name_pattern=arguments.get("tool_name_pattern"),
                max_results=arguments.get("max_results", 100),
            )
        else:
            result = {"error": f"unknown_tool: {name}"}

        return [TextContent(type="text", text=json.dumps(result))]

    return server


async def _amain(transcript_path_override: Path | None) -> None:
    server = _build_server(transcript_path_override)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="tessellum-session-mcp stdio server",
    )
    parser.add_argument(
        "--transcript-path",
        type=Path,
        default=None,
        help=(
            "Override transcript path; otherwise uses SESSION_TRANSCRIPT_PATH "
            "env var or auto-detects from ~/.claude/projects/."
        ),
    )
    args = parser.parse_args()
    asyncio.run(_amain(args.transcript_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
