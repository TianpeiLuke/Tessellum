# `tessellum.mcp` — Reference

API, symbols, and signatures for the MCP server. For the mental model and how work flows through it, see [../mcp.md](../mcp.md).

## File → role

| File | Role |
|------|------|
| `mcp/__init__.py` | Public surface: re-exports `build_server` and `run_stdio` from `mcp.server`. `__all__ = ["build_server", "run_stdio"]`. |
| `mcp/server.py` | The whole server. Owns the static `tool_specs` descriptor list, the `list_tools` / `call_tool` SDK handlers, `_dispatch`, the seven `_tool_*` implementations, the `_skills_dir` locator, and the `run_stdio` runner. |
| `cli/mcp.py` | The `tessellum mcp serve` command: `add_subparser` wires the `mcp` group + `serve` sub-subcommand; `run_mcp_serve` calls `run_stdio` (lazy import) and maps failures to exit code 2. |

## Public API — `tessellum.mcp`

- `build_server() -> Server` — construct the `"tessellum"` MCP `Server` with all seven tools registered. Lazily imports `mcp.server.Server` and `mcp.types`; raises `ImportError` (with the `pip install tessellum[mcp]` hint) if the `[mcp]` extra is absent.
- `run_stdio() -> int` — build the server and run it over the stdio transport (`mcp.server.stdio.stdio_server`) inside `asyncio.run`. Blocks until the client closes the connection. Returns `0` on clean exit, `2` if the `[mcp]` extra import fails (prints the install hint).

## Internal symbols — `mcp/server.py`

- `tool_specs: list[dict]` — the static descriptor list (name, description, inputSchema) advertised by `list_tools`, built inside `build_server`.
- `list_tools() -> list[types.Tool]` — `@server.list_tools()` handler; maps each spec to a `types.Tool`.
- `call_tool(name, arguments) -> list[types.TextContent]` — `@server.call_tool()` handler; calls `_dispatch`, wraps any `Exception` into `{"error": "<Type>: <msg>"}`, and returns one `TextContent` holding `json.dumps(result, indent=2, default=str)`.
- `_dispatch(name: str, arguments: dict) -> dict` — routes to the matching `_tool_*` by name; raises `ValueError(f"unknown tool: {name}")` on an unknown name.
- `_skills_dir() -> Path | None` — locates the skills directory. Prefers the wheel path `tessellum/data/seed_vault/resources/skills/`, falls back to the repo-dev path `vault/resources/skills/` (repo root = `Path(__file__).resolve().parents[3]`). Returns `None` if neither exists.

### Tool implementations

Each returns a plain `dict`. On a missing resource each returns `{"error": ...}` rather than raising.

| Function | Signature | Backing API | Returns |
|----------|-----------|-------------|---------|
| `_tool_search` | `(query, k=10, db_path="data/tessellum.db")` | `tessellum.retrieval.hybrid_search` | `{query, k, hits:[{note_id, note_name, score, bm25_rank, dense_rank}]}`; error if DB file missing. |
| `_tool_format_check` | `(path)` | `tessellum.format.validate` | `{files_checked, files_with_issues, issues:[{path, issues:[{severity, rule_id, field, message}]}]}`. Directory → `rglob("*.md")` sorted; only notes with issues listed; error if path not found. |
| `_tool_bb_audit` | `(db_path="data/tessellum.db")` | `tessellum.bb.BBGraph.from_db` | `{db_path, node_count, edges_by_label, untyped_edge_count, unrealised_schema_edges:[{source, target, label}]}`; error if DB file missing. |
| `_tool_fz_traverse` | `(fz, direction, db_path="data/tessellum.db")` | `tessellum.bb.BBGraph.from_db` | `{starting_fz, direction, results:[{fz, note_id}]}` sorted by `fz`; error if DB missing or no note at `fz`. |
| `_tool_capture` | `(flavor, slug, vault_root="vault", destination=None, filename_prefix=None)` | `tessellum.capture.capture` | `{path, flavor, slug, sidecar_path}`; error if vault root missing. |
| `_tool_list_skills` | `()` | `_skills_dir` + file read | `{skills_dir, skills:[{name, title, has_sidecar}], count}`; error if skills dir not found. |
| `_tool_get_skill` | `(skill_name)` | `_skills_dir` + file read | `{skill_name, canonical_path, canonical_body, sidecar_path, sidecar_body}`; error if skills dir or skill file not found. |

`_tool_fz_traverse` matching (linear scan over the in-memory graph, excluding the start node): `ancestors` = nodes whose `folgezettel` is a strict prefix of `fz`; `descendants` = nodes whose `folgezettel` is strictly prefixed by `fz`; `siblings` = nodes sharing the start's non-empty `folgezettel_parent`.

`_tool_list_skills` globs `skill_tessellum_*.md`; `title` = the first `# ` H1 line; `has_sidecar` = a `<stem>.pipeline.yaml` exists beside it.

`_tool_get_skill` accepts `skill_name` with or without the `skill_` prefix (normalizes to `skill_<name>.md`); sidecar fields are `null` when no `<stem>.pipeline.yaml` exists.

## Tool inventory

Seven tools, advertised as `types.Tool` descriptors.

| Tool | Required args | Optional args (default) | Purpose |
|------|---------------|-------------------------|---------|
| `tessellum_search` | `query` | `k` (10), `db_path` (`data/tessellum.db`) | Hybrid BM25 + dense + graph retrieval; ranked paths + snippets. |
| `tessellum_format_check` | `path` | — | Validate a note or directory against TESS-001..005 + YAML frontmatter + link rules. |
| `tessellum_bb_audit` | — | `db_path` (`data/tessellum.db`) | Corpus BBGraph telemetry: node/edge counts, untyped edges, unrealised schema edges. |
| `tessellum_fz_traverse` | `fz`, `direction` | `db_path` (`data/tessellum.db`) | Walk a Folgezettel trail; `direction` ∈ `ancestors` / `descendants` / `siblings`. |
| `tessellum_capture` | `flavor`, `slug` | `vault_root` (`vault`), `destination`, `filename_prefix` | Create a new typed note from a template; overrides steer the write. |
| `tessellum_list_skills` | — | — | Enumerate shipped skill canonicals (name + 1-line title). |
| `tessellum_get_skill` | `skill_name` | — | Return one skill canonical's body (+ sidecar) as text. |

## CLI — `tessellum mcp`

Registered in `cli/main.py` alongside `bb`, `capture`, `composer`, `dks`, `filter`, `format`, `fz`, `index`, `init`, `search`.

```
tessellum mcp serve
```

| Invocation | Behavior |
|------------|----------|
| `tessellum mcp serve` | Runs the stdio server via `run_stdio()` (blocks until the client disconnects). |
| `tessellum mcp` (no sub-subcommand) | Prints `missing sub-subcommand` to stderr; exit 2. |

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | Server ran cleanly (client closed the connection). |
| `2` | Missing `[mcp]` extras, or invocation error (no sub-subcommand). |

## Dependencies — `[mcp]` extra

| Package | Constraint | Used for |
|---------|-----------|----------|
| `mcp` | `>=1.0` | MCP stdio server SDK (`Server`, `types`, `stdio_server`). |
| `fastapi` | `>=0.115` | Pulled in by the extra; no HTTP/SSE transport wired yet. |
| `uvicorn` | `>=0.32` | Pulled in by the extra; no HTTP/SSE transport wired yet. |
