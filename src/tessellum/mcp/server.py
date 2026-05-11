"""Tessellum MCP server — 7 tools exposing the runtime + skill canonicals.

The server registers its tools via the MCP Python SDK's decorator API
(``@server.list_tools()``, ``@server.call_tool()``) and runs over the
standard stdio transport. Build the ``Server`` instance with
:func:`build_server`; run it via :func:`run_stdio` (called by
``tessellum mcp serve``).

Tool inventory:

1. ``tessellum_search`` — hybrid BM25 + dense + graph retrieval
2. ``tessellum_format_check`` — TESS-001..005 validators against a note
3. ``tessellum_bb_audit`` — corpus BBGraph telemetry (node + edge counts,
   untyped edges, unrealised schema edges)
4. ``tessellum_fz_traverse`` — walk a Folgezettel trail
   (ancestors / descendants / siblings)
5. ``tessellum_capture`` — create a new typed note from a template
6. ``tessellum_get_skill`` — return a skill canonical's body so the
   calling agent can apply the procedure itself
7. ``tessellum_list_skills`` — enumerate available skill canonicals

The runtime tools are deterministic Python-API wrappers; no LLM call
on the server side. The skill-canonical tools let the calling agent
execute the procedure in its own context — the canonical is the
prompt; the agent supplies the LLM.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_server():
    """Construct the Tessellum MCP server instance with all tools registered.

    Imports the ``mcp`` SDK lazily so the optional dependency is only
    required when the server is actually constructed (not when the
    package is imported). Raises ``ImportError`` if ``[mcp]`` extras
    aren't installed.
    """
    try:
        from mcp.server import Server
        from mcp import types
    except ImportError as e:
        raise ImportError(
            "tessellum.mcp requires the [mcp] extras: "
            "`pip install tessellum[mcp]`"
        ) from e

    server = Server("tessellum")

    # ── Tool descriptors ──────────────────────────────────────────────────
    tool_specs: list[dict[str, Any]] = [
        {
            "name": "tessellum_search",
            "description": (
                "Hybrid retrieval (BM25 + dense + graph) over the vault. "
                "Returns ranked note paths with snippets."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {"type": "string", "description": "Natural-language query"},
                    "k": {"type": "integer", "default": 10, "description": "Top-K hits"},
                    "db_path": {
                        "type": "string",
                        "default": "data/tessellum.db",
                        "description": "Index DB path (relative to cwd)",
                    },
                },
            },
        },
        {
            "name": "tessellum_format_check",
            "description": (
                "Validate one note (or a directory) against TESS-001..005 + "
                "YAML frontmatter + link rules. Returns the list of issues."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["path"],
                "properties": {
                    "path": {"type": "string", "description": "Note file or directory"},
                },
            },
        },
        {
            "name": "tessellum_bb_audit",
            "description": (
                "Corpus BBGraph telemetry: node counts by BB type, edge "
                "counts by epistemic-edge label, untyped corpus edges, "
                "unrealised schema edges. Pure read of the index DB."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "db_path": {
                        "type": "string",
                        "default": "data/tessellum.db",
                        "description": "Index DB path",
                    },
                },
            },
        },
        {
            "name": "tessellum_fz_traverse",
            "description": (
                "Walk a Folgezettel trail from a starting note. Returns "
                "ancestors / descendants / siblings as ordered FZ IDs."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["fz", "direction"],
                "properties": {
                    "fz": {"type": "string", "description": "Starting FZ ID (e.g., '2a1')"},
                    "direction": {
                        "type": "string",
                        "enum": ["ancestors", "descendants", "siblings"],
                        "description": "Traversal direction",
                    },
                    "db_path": {
                        "type": "string",
                        "default": "data/tessellum.db",
                        "description": "Index DB path",
                    },
                },
            },
        },
        {
            "name": "tessellum_capture",
            "description": (
                "Create a new typed note from a template. Returns the "
                "created file path. Optional --destination + --prefix "
                "overrides let the caller override the flavor's defaults."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["flavor", "slug"],
                "properties": {
                    "flavor": {
                        "type": "string",
                        "description": "Template flavor (concept / argument / model / procedure / ...)",
                    },
                    "slug": {
                        "type": "string",
                        "description": "Note identifier (lowercase letters/digits/underscores)",
                    },
                    "vault_root": {
                        "type": "string",
                        "default": "vault",
                        "description": "Vault root directory",
                    },
                    "destination": {
                        "type": ["string", "null"],
                        "description": "Override REGISTRY default destination (e.g., 'areas/tools')",
                    },
                    "filename_prefix": {
                        "type": ["string", "null"],
                        "description": "Override REGISTRY default filename prefix (e.g., 'tool_')",
                    },
                },
            },
        },
        {
            "name": "tessellum_list_skills",
            "description": (
                "Enumerate available skill canonicals from the seed vault. "
                "Returns each skill's name + 1-line description."
            ),
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "tessellum_get_skill",
            "description": (
                "Return a skill canonical's body as text. The calling "
                "agent applies the procedure in its own LLM context — "
                "the server does not invoke an LLM."
            ),
            "inputSchema": {
                "type": "object",
                "required": ["skill_name"],
                "properties": {
                    "skill_name": {
                        "type": "string",
                        "description": "Skill stem (e.g., 'tessellum_dks_cycle')",
                    },
                },
            },
        },
    ]

    @server.list_tools()
    async def list_tools():
        return [
            types.Tool(
                name=spec["name"],
                description=spec["description"],
                inputSchema=spec["inputSchema"],
            )
            for spec in tool_specs
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]):
        try:
            result = _dispatch(name, arguments)
        except Exception as e:  # noqa: BLE001 — surface error as MCP content
            result = {"error": f"{type(e).__name__}: {e}"}
        return [
            types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str),
            )
        ]

    return server


def _dispatch(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Route a tool call to its Python implementation."""
    if name == "tessellum_search":
        return _tool_search(**arguments)
    if name == "tessellum_format_check":
        return _tool_format_check(**arguments)
    if name == "tessellum_bb_audit":
        return _tool_bb_audit(**arguments)
    if name == "tessellum_fz_traverse":
        return _tool_fz_traverse(**arguments)
    if name == "tessellum_capture":
        return _tool_capture(**arguments)
    if name == "tessellum_list_skills":
        return _tool_list_skills(**arguments)
    if name == "tessellum_get_skill":
        return _tool_get_skill(**arguments)
    raise ValueError(f"unknown tool: {name}")


# ── Tool implementations ────────────────────────────────────────────────────


def _tool_search(query: str, k: int = 10, db_path: str = "data/tessellum.db") -> dict:
    from tessellum.retrieval import hybrid_search

    db = Path(db_path).expanduser().resolve()
    if not db.is_file():
        return {"error": f"Index DB not found at {db}. Run `tessellum index build` first."}
    hits = hybrid_search(db, query, k=k)
    return {
        "query": query,
        "k": k,
        "hits": [
            {
                "note_id": h.note_id,
                "note_name": h.note_name,
                "score": h.score,
                "bm25_rank": h.bm25_rank,
                "dense_rank": h.dense_rank,
            }
            for h in hits
        ],
    }


def _tool_format_check(path: str) -> dict:
    from tessellum.format import validate

    p = Path(path).expanduser().resolve()
    if p.is_dir():
        files = sorted(p.rglob("*.md"))
    elif p.is_file():
        files = [p]
    else:
        return {"error": f"path not found: {path}"}
    out = []
    for f in files:
        issues = validate(f)
        if issues:
            out.append(
                {
                    "path": str(f),
                    "issues": [
                        {
                            "severity": i.severity.value,
                            "rule_id": i.rule_id,
                            "field": i.field,
                            "message": i.message,
                        }
                        for i in issues
                    ],
                }
            )
    return {
        "files_checked": len(files),
        "files_with_issues": len(out),
        "issues": out,
    }


def _tool_bb_audit(db_path: str = "data/tessellum.db") -> dict:
    from tessellum.bb import BBGraph

    db = Path(db_path).expanduser().resolve()
    if not db.is_file():
        return {"error": f"Index DB not found at {db}."}
    graph = BBGraph.from_db(db)
    return {
        "db_path": str(db),
        "node_count": len(graph),
        "edges_by_label": graph.edges_by_type(),
        "untyped_edge_count": len(graph.untyped_edges()),
        "unrealised_schema_edges": [
            {
                "source": e.source.value,
                "target": e.target.value,
                "label": e.label,
            }
            for e in graph.unrealised_schema_edges()
        ],
    }


def _tool_fz_traverse(
    fz: str,
    direction: str,
    db_path: str = "data/tessellum.db",
) -> dict:
    from tessellum.bb import BBGraph

    db = Path(db_path).expanduser().resolve()
    if not db.is_file():
        return {"error": f"Index DB not found at {db}."}
    graph = BBGraph.from_db(db)
    # Find the node at this FZ
    start = next(
        (n for n in graph if getattr(n, "folgezettel", "") == fz),
        None,
    )
    if start is None:
        return {"error": f"No note found at FZ {fz!r}."}
    # Naive traversal: walk parent / children via folgezettel prefix
    results: list[dict] = []
    for n in graph:
        n_fz = getattr(n, "folgezettel", "") or ""
        if not n_fz or n_fz == fz:
            continue
        if direction == "ancestors":
            if fz.startswith(n_fz) and fz != n_fz:
                results.append({"fz": n_fz, "note_id": n.note_id})
        elif direction == "descendants":
            if n_fz.startswith(fz) and n_fz != fz:
                results.append({"fz": n_fz, "note_id": n.note_id})
        elif direction == "siblings":
            parent_fz = getattr(start, "folgezettel_parent", "") or ""
            sibling_parent = getattr(n, "folgezettel_parent", "") or ""
            if parent_fz and sibling_parent == parent_fz:
                results.append({"fz": n_fz, "note_id": n.note_id})
    results.sort(key=lambda r: r["fz"])
    return {
        "starting_fz": fz,
        "direction": direction,
        "results": results,
    }


def _tool_capture(
    flavor: str,
    slug: str,
    vault_root: str = "vault",
    destination: str | None = None,
    filename_prefix: str | None = None,
) -> dict:
    from tessellum.capture import capture

    root = Path(vault_root).expanduser().resolve()
    if not root.is_dir():
        return {"error": f"Vault root not found at {root}."}
    result = capture(
        flavor=flavor,
        slug=slug,
        vault_root=root,
        destination=destination,
        filename_prefix=filename_prefix,
    )
    return {
        "path": str(result.path),
        "flavor": result.flavor,
        "slug": result.slug,
        "sidecar_path": str(result.sidecar_path) if result.sidecar_path else None,
    }


def _skills_dir() -> Path | None:
    """Locate the skills directory in the wheel-shipped vault.

    Mirrors :func:`tessellum.data.templates_dir` but for skills.
    Returns ``None`` if no skills directory is found.
    """
    # Wheel-installed: under tessellum/data/seed_vault/resources/skills/
    from tessellum import data as data_pkg

    pkg_root = Path(data_pkg.__file__).parent
    candidate = pkg_root / "seed_vault" / "resources" / "skills"
    if candidate.is_dir():
        return candidate
    # Editable install / repo dev: vault/resources/skills/ relative to repo root
    repo_root = Path(__file__).resolve().parents[3]
    candidate = repo_root / "vault" / "resources" / "skills"
    if candidate.is_dir():
        return candidate
    return None


def _tool_list_skills() -> dict:
    skills_dir = _skills_dir()
    if skills_dir is None:
        return {"error": "skills directory not found"}
    skills = []
    for p in sorted(skills_dir.glob("skill_tessellum_*.md")):
        # Read frontmatter for description
        text = p.read_text(encoding="utf-8")
        # Extract H1 line as the short description
        title = ""
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        skills.append(
            {
                "name": p.stem,
                "title": title,
                "has_sidecar": (p.parent / f"{p.stem}.pipeline.yaml").is_file(),
            }
        )
    return {"skills_dir": str(skills_dir), "skills": skills, "count": len(skills)}


def _tool_get_skill(skill_name: str) -> dict:
    skills_dir = _skills_dir()
    if skills_dir is None:
        return {"error": "skills directory not found"}
    # Accept both 'tessellum_dks_cycle' and 'skill_tessellum_dks_cycle' forms
    stem = skill_name if skill_name.startswith("skill_") else f"skill_{skill_name}"
    path = skills_dir / f"{stem}.md"
    if not path.is_file():
        return {"error": f"skill not found: {skill_name} (looked for {path.name})"}
    sidecar_path = skills_dir / f"{stem}.pipeline.yaml"
    return {
        "skill_name": skill_name,
        "canonical_path": str(path),
        "canonical_body": path.read_text(encoding="utf-8"),
        "sidecar_path": str(sidecar_path) if sidecar_path.is_file() else None,
        "sidecar_body": (
            sidecar_path.read_text(encoding="utf-8")
            if sidecar_path.is_file()
            else None
        ),
    }


# ── Stdio runner ────────────────────────────────────────────────────────────


def run_stdio() -> int:
    """Run the Tessellum MCP server over stdio transport.

    Called by ``tessellum mcp serve``. Blocks until the client closes
    the connection (typical lifecycle for Claude Desktop and similar
    MCP hosts).
    """
    import asyncio

    try:
        from mcp.server.stdio import stdio_server
    except ImportError as e:
        print(
            "tessellum mcp: missing the [mcp] extras. "
            "Install with: pip install tessellum[mcp]"
        )
        print(f"  ({e})")
        return 2

    server = build_server()

    async def _main() -> None:
        async with stdio_server() as (read, write):
            await server.run(
                read,
                write,
                server.create_initialization_options(),
            )

    asyncio.run(_main())
    return 0
