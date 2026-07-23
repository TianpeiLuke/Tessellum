# Tessellum MCP Server

## 1. Purpose

`src/tessellum/mcp/` ships a stdio Model Context Protocol (MCP) server that exposes Tessellum's deterministic runtime APIs (System D retrieval/format/graph + System P capture) as callable tools for MCP hosts such as Claude Desktop and MCP-aware IDEs. It also acts as a **skills-as-tools front door**: two tools return the raw canonical body of a shipped skill so the *calling* agent — not the server — supplies the LLM and executes the procedure.

Status note: this component is **SHIPPED, not deferred**. The old "MCP is a stub / future work" framing is stale. `build_server()` registers seven working tools and `run_stdio()` serves them over a real stdio transport; the only gate is the optional `[mcp]` extra.

## 2. Architecture / data flow

```
MCP host (Claude Desktop / IDE)
        │  JSON-RPC over stdio
        ▼
run_stdio()  ──►  build_server()  ──►  mcp.server.Server("tessellum")
        │                                    │
        │              @server.list_tools()  │  advertises 7 Tool descriptors
        │              @server.call_tool()   │  receives (name, arguments)
        ▼                                    ▼
   stdio_server()                       _dispatch(name, arguments)
                                             │
                    ┌────────────────────────┼───────────────────────────┐
                    ▼                         ▼                           ▼
          Runtime tools (no LLM)      Capture (System P write)   Skill tools (prompt fetch)
          _tool_search      ──► tessellum.retrieval.hybrid_search
          _tool_format_check──► tessellum.format.validate
          _tool_bb_audit    ──► tessellum.bb.BBGraph.from_db
          _tool_fz_traverse ──► tessellum.bb.BBGraph.from_db
          _tool_capture     ──► tessellum.capture.capture
          _tool_list_skills ──► seed_vault/resources/skills/*.md (read)
          _tool_get_skill   ──► seed_vault/resources/skills/*.md (read)
```

Every tool result is serialized to a single `types.TextContent` block via `json.dumps(result, indent=2, default=str)` (`server.py`, `call_tool`). Errors are not raised across the wire — `call_tool` wraps `_dispatch` in a `try/except` and returns `{"error": "<ExceptionType>: <msg>"}` as content, so a bad argument or missing DB degrades to a readable payload rather than an MCP protocol fault.

Key data-flow property: **the server side is LLM-free for all runtime tools.** The five runtime tools are thin wrappers over deterministic Python APIs; the two skill tools return canonical text. The LLM lives entirely in the connected agent.

## 3. Key modules + abstractions

| File | Role |
|------|------|
| `src/tessellum/mcp/__init__.py` | Public package surface. Re-exports `build_server` and `run_stdio`; module docstring documents the two tool classes (runtime vs prompt) and the `tessellum mcp serve` entry point. |
| `src/tessellum/mcp/server.py` | The whole server. `build_server()` (registers 7 tool descriptors + `list_tools`/`call_tool` handlers), `_dispatch()` (name→impl router), the 7 `_tool_*` implementations, `_skills_dir()` locator, and `run_stdio()` (asyncio stdio runner). |
| `src/tessellum/cli/mcp.py` | CLI wiring for the `mcp` subcommand. `add_subparser()` adds `mcp serve`; `run_mcp_serve()` lazy-imports `run_stdio` and maps missing extras / bad invocation to exit code 2. |
| `src/tessellum/cli/main.py` | Dispatcher that registers `add_mcp_subparser` (line 48), making `mcp` one of the 11 top-level CLI commands. |
| `pyproject.toml` `[project.optional-dependencies].mcp` | Declares the `mcp` extra (`mcp>=1.0`, plus `fastapi`/`uvicorn`). Not installed by default; gates server construction. |

### The 7 registered tools

Advertised by `list_tools` from the `tool_specs` list in `build_server()`:

| Tool name | Impl | Backing API | Class |
|-----------|------|-------------|-------|
| `tessellum_search` | `_tool_search` | `tessellum.retrieval.hybrid_search(db, query, k)` → BM25 + dense + graph | runtime |
| `tessellum_format_check` | `_tool_format_check` | `tessellum.format.validate(file)` → TESS-001..005 + YAML/link `Issue`s | runtime |
| `tessellum_bb_audit` | `_tool_bb_audit` | `tessellum.bb.BBGraph.from_db(db)` → node/edge counts, untyped + unrealised schema edges | runtime |
| `tessellum_fz_traverse` | `_tool_fz_traverse` | `BBGraph.from_db(db)` + folgezettel prefix walk | runtime |
| `tessellum_capture` | `_tool_capture` | `tessellum.capture.capture(flavor, slug, vault_root, …)` → new note file | runtime (System P write) |
| `tessellum_list_skills` | `_tool_list_skills` | reads `resources/skills/skill_tessellum_*.md` | prompt |
| `tessellum_get_skill` | `_tool_get_skill` | reads one skill canonical (+ optional `.pipeline.yaml` sidecar) | prompt |

Result shapes are grounded in the impls:
- `tessellum_search` returns per-hit `note_id`, `note_name`, `score`, `bm25_rank`, `dense_rank` (fields off `hybrid.py`'s `HybridHit` dataclass).
- `tessellum_bb_audit` returns `node_count`, `edges_by_label` (`graph.edges_by_type()`, keyed by `edge_type.label` or `"(untyped)"`), `untyped_edge_count`, and `unrealised_schema_edges` (BB-schema pairs with no corpus instance — `graph.unrealised_schema_edges()`).
- `tessellum_capture` returns `path`, `flavor`, `slug`, and `sidecar_path` (non-null only for the `skill` flavor, which emits a paired `.pipeline.yaml`).

### The skills-as-tools front door

`tessellum_list_skills` enumerates `skill_tessellum_*.md` canonicals (name + H1 title + whether a `.pipeline.yaml` sidecar exists). `tessellum_get_skill` returns `canonical_body` (the full markdown text) plus, if present, `sidecar_body`. The docstring is explicit: *"The calling agent applies the procedure in its own LLM context — the server does not invoke an LLM."* The canonical **is** the prompt; the agent supplies the model. `_tool_get_skill` accepts both `tessellum_dks_cycle` and `skill_tessellum_dks_cycle` forms (it prepends `skill_` when missing).

`_skills_dir()` resolves the skills directory in two layouts: wheel install (`tessellum/data/seed_vault/resources/skills/`) first, then editable/repo dev (`<repo_root>/vault/resources/skills/`, via `Path(__file__).resolve().parents[3]`). Returns `None` (surfaced as `{"error": "skills directory not found"}`) if neither exists.

## 4. Invariants / design decisions + WHY

- **Server side is deterministic; no LLM call in-process.** Runtime tools wrap pure Python APIs and skill tools return text. WHY: keeps the server a trustworthy, reproducible substrate — the host agent owns model choice, cost, and non-determinism. This is the CQRS split extended to the tool boundary (System D reads + System P capture on one side, agent cognition on the other).
- **Lazy SDK import.** `build_server()` imports `mcp.server.Server`/`mcp.types` inside the function; `run_stdio()` imports `mcp.server.stdio.stdio_server` inside the function; `cli/mcp.py` imports `tessellum.mcp.run_stdio` inside `run_mcp_serve`. WHY: users without the `[mcp]` extra must still load the CLI and every other subcommand. The `mcp` dependency is genuinely optional and only materializes when `serve` runs.
- **Missing `[mcp]` extra → exit code 2, never a traceback.** Both `run_stdio()` (catches `ImportError` from `stdio_server`) and `run_mcp_serve()` (catches `ImportError` from `run_stdio`) print an actionable `pip install tessellum[mcp]` message and return 2. WHY: a missing optional dep is a user-config problem, not a crash.
- **Bad invocation → exit code 2.** `tessellum mcp` with no sub-subcommand (`_mcp_op is None`) prints guidance and returns 2. WHY: `mcp` is a subcommand group; only `serve` does work.
- **Errors are content, not protocol faults.** `call_tool` returns `{"error": ...}` text instead of letting exceptions escape. WHY: an agent reading a JSON error can recover/retry; a broken JSON-RPC frame cannot be reasoned about.
- **`_tool_fz_traverse` is deliberately naive.** It loads the whole `BBGraph` and does an O(N) scan per call, matching ancestors/descendants by folgezettel string prefix and siblings by shared `folgezettel_parent` (the impl comment calls it "Naive traversal"). WHY: correctness-first over an already in-memory graph; no separate FZ index is required on the MCP path. Sibling matching depends on the `folgezettel_parent` field being populated on nodes.
- **Capture destination/prefix are overridable, not fixed.** `tessellum_capture` forwards optional `destination` and `filename_prefix` to `capture()`, which treats the `REGISTRY` value as a *default*, not a constraint. WHY: the calling agent often knows the note's true sub-category (a `model`-flavored repo note belongs in `areas/code_repos/`, an algorithm note in `areas/tools/`) better than a static registry can.

## 5. Public API / CLI

**Python API** (`from tessellum.mcp import build_server, run_stdio`):
- `build_server()` → an `mcp.server.Server` with all 7 tools registered. Raises `ImportError` (with the `[mcp]` install hint) if the extra is absent.
- `run_stdio() -> int` → builds the server and runs it over stdio until the client disconnects. Returns `0` on clean exit, `2` if the SDK is missing.

**CLI:**
```
tessellum mcp serve      # run the stdio MCP server (for Claude Desktop / IDE hosts)
tessellum mcp            # no sub-subcommand → guidance + exit 2
```
`mcp serve` blocks until the host closes the connection (the normal MCP host lifecycle) and exits 0; without the `[mcp]` extra it exits 2 with an install hint.

**Tool arguments** (from each tool's `inputSchema`): `tessellum_search` requires `query` (+ `k`=10, `db_path`); `tessellum_format_check` requires `path` (file or dir — a dir is `rglob("*.md")`-expanded); `tessellum_bb_audit` takes optional `db_path`; `tessellum_fz_traverse` requires `fz` + `direction` (`ancestors`/`descendants`/`siblings`); `tessellum_capture` requires `flavor` + `slug` (+ `vault_root`, optional `destination`, `filename_prefix`); `tessellum_get_skill` requires `skill_name`; `tessellum_list_skills` takes no arguments. Default `db_path` is `data/tessellum.db`; a missing index DB returns a `{"error": ...}` payload advising `tessellum index build`.

## 6. Extension points

- **Add a runtime tool.** Append a descriptor to `tool_specs` in `build_server()` (name, description, `inputSchema`), add a `_tool_<x>` impl that wraps a deterministic Tessellum API, and add a routing branch in `_dispatch()`. Keep it LLM-free to preserve the server invariant.
- **Add a skill to the front door.** Drop a `skill_tessellum_<name>.md` (optionally a `skill_tessellum_<name>.pipeline.yaml` sidecar) into `resources/skills/`; `list_skills`/`get_skill` pick it up by glob with no code change.
- **Alternate transport.** Only stdio is wired today (`run_stdio()` / `stdio_server()`). The `[mcp]` extra also pulls `fastapi`/`uvicorn`, but **no HTTP/SSE transport is implemented** — that is unwired headroom, not a shipped feature.
- **CLI surface.** `cli/mcp.py` exposes only `serve`. Additional `mcp <op>` operations would be added as parsers under the existing `sub` sub-subparsers in `add_subparser()`.
