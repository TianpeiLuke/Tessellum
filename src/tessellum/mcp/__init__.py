"""Tessellum MCP server — expose runtime APIs as MCP tools.

Phase V of ``plans/plan_v01_completion_roadmap.md`` (v0.0.59). The
server lets MCP-compatible agents (Claude Desktop, IDEs, etc.) invoke
Tessellum's deterministic runtime APIs as tools, and fetch any of the
13 skill canonicals as prompts to execute themselves.

Two classes of tool:

- **Runtime tools** (deterministic Python-API wrappers): search,
  format-check, bb-audit, fz-traverse, capture. Pure code; no LLM
  involved on the server side.
- **Prompt tools** (skill canonical retrievers): get-skill returns
  the canonical body of a named skill so the calling agent can apply
  the procedure step-by-step in its own context.

Entry point: ``tessellum mcp serve`` (stdio transport — the default
for Claude Desktop integration).

Requires the ``[mcp]`` extras::

    pip install tessellum[mcp]
"""

from tessellum.mcp.server import build_server, run_stdio

__all__ = ["build_server", "run_stdio"]
