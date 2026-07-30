# `tessellum.mcp` — Reference

API, symbols, and signatures for the MCP server. For the mental model and how work flows through it, see [../mcp.md](../mcp.md).

## File → role

| File | Role |
|------|------|
| `mcp/__init__.py` | Public surface: re-exports `build_server` and `run_stdio` from `mcp.server`. `__all__ = ["build_server", "run_stdio"]`. |
| `mcp/server.py` | The whole server. Owns the static `tool_specs` descriptor list, the `list_tools` / `call_tool` SDK handlers, `_dispatch`, the twelve `_tool_*` implementations, the `_skills_dir` locator, and the `run_stdio` runner. |
| `cli/mcp.py` | The `tessellum mcp serve` command: `add_subparser` wires the `mcp` group + `serve` sub-subcommand; `run_mcp_serve` calls `run_stdio` (lazy import) and maps failures to exit code 2. |

## Public API — `tessellum.mcp`

- `build_server() -> Server` — construct the `"tessellum"` MCP `Server` with all twelve tools registered. Lazily imports `mcp.server.Server` and `mcp.types`; raises `ImportError` (with the `pip install tessellum[mcp]` hint) if the `[mcp]` extra is absent.
- `run_stdio() -> int` — build the server and run it over the stdio transport (`mcp.server.stdio.stdio_server`) inside `asyncio.run`. Blocks until the client closes the connection. Returns `0` on clean exit, `2` if the `[mcp]` extra import fails (prints the install hint).

## Internal symbols — `mcp/server.py`

- `tool_specs: list[dict]` — the static descriptor list (name, description, inputSchema) advertised by `list_tools`, built inside `build_server`.
- `list_tools() -> list[types.Tool]` — `@server.list_tools()` handler; maps each spec to a `types.Tool`.
- `call_tool(name, arguments) -> list[types.TextContent]` — `@server.call_tool()` handler; calls `_dispatch`, wraps any `Exception` into `{"error": "<Type>: <msg>"}`, and returns one `TextContent` holding `json.dumps(result, indent=2, default=str)`.
- `_dispatch(name: str, arguments: dict) -> dict` — routes to the matching `_tool_*` by name; raises `ValueError(f"unknown tool: {name}")` on an unknown name.
- `_skills_dir() -> Path | None` — locates the skills directory. Prefers the wheel path `tessellum/data/seed_vault/resources/skills/`, falls back to the repo-dev path `vault/resources/skills/` (repo root = `Path(__file__).resolve().parents[3]`). Returns `None` if neither exists.

### Tool implementations

Each returns a plain `dict` on success. Several implementations return `{"error": ...}` for an expected missing resource; other exceptions are converted to error content by the MCP call handler.

| Function | Signature | Backing API | Returns |
|----------|-----------|-------------|---------|
| `_tool_search` | `(query, k=10, db_path="data/tessellum.db")` | `tessellum.retrieval.hybrid_search` | `{query, k, hits:[{note_id, note_name, score, bm25_rank, dense_rank}]}`; error if DB file missing. |
| `_tool_format_check` | `(path)` | `tessellum.format.validate` | `{files_checked, files_with_issues, issues:[{path, issues:[{severity, rule_id, field, message}]}]}`. Directory → `rglob("*.md")` sorted; only notes with issues listed; error if path not found. |
| `_tool_bb_audit` | `(db_path="data/tessellum.db")` | `tessellum.bb.BBGraph.from_db` | `{db_path, node_count, edges_by_label, untyped_edge_count, unrealised_schema_edges:[{source, target, label}]}`; error if DB file missing. |
| `_tool_fz_traverse` | `(fz, direction, db_path="data/tessellum.db")` | `tessellum.bb.BBGraph.from_db` | `{starting_fz, direction, results:[{fz, note_id}]}` sorted by `fz`; error if DB missing or no note at `fz`. |
| `_tool_capture` | `(flavor, slug, vault_root="vault", destination=None, filename_prefix=None)` | `tessellum.capture.capture` | `{path, flavor, slug, sidecar_path}`; error if vault root missing. The write is journaled (A5.2): the server opens a `VaultEffectJournal` under `<vault>/runs/mcp-effects/<uuid12>/`, passes `journal.record` as `capture()`'s `effect_recorder`, accepts the journal on success and rolls back on failure; a crash between record and accept leaves an open journal the runtime's `recover_pending` rolls back. Return shape unchanged. |
| `_tool_list_skills` | `()` | `_skills_dir` + file read/`compile_skill` | `{skills_dir, skills:[{name, title, pipeline_step_count}], count}`; error if skills dir not found. |
| `_tool_get_skill` | `(skill_name)` | `_skills_dir` + `compile_skill` | `{skill_name, canonical_path, canonical_body, pipeline_step_count}`; the single-file canonical carries its per-step contract blocks inline, so there is no separate sidecar body; `pipeline_step_count` is `None` if the skill does not compile. Error if skills dir or skill file not found. |
| `_tool_submit_job` | `(path, root=".")` | `RuntimePaths.discover` + `RuntimeStore.open` + `admit_path` | Job fields plus `created`; spools and idempotently admits an eligible inbox file. |
| `_tool_get_job` | `(job_id, root=".")` | `RuntimeStore.get/events` | Job fields plus ordered `events`; direct error payload if the job is absent. |
| `_tool_list_jobs` | `(root=".", state=None, limit=100)` | `RuntimeStore.list` | `{jobs:[...]}` newest first; optional exact `JobState` filter. |
| `_tool_cancel_job` | `(job_id, root=".")` | `RuntimeStore.request_cancel` | Resulting job fields; immediate or cooperative cancellation depending on lease ownership. |
| `_tool_retry_job` | `(job_id, root=".")` | `RuntimeStore.retry_terminal` | New linked job fields; accepts only `cancelled` or `dead_letter` source jobs. |

`_tool_fz_traverse` matching (linear scan over the in-memory graph, excluding the start node): `ancestors` = nodes whose `folgezettel` is a strict prefix of `fz`; `descendants` = nodes whose `folgezettel` is strictly prefixed by `fz`; `siblings` = nodes sharing the start's non-empty `folgezettel_parent`.

`_tool_list_skills` globs `skill_tessellum_*.md`; `title` = the first `# ` H1 line; `pipeline_step_count` is the compiled number of inline contract steps, or `0` when compilation fails.

`_tool_get_skill` accepts `skill_name` with or without the `skill_` prefix (normalizes to `skill_<name>.md`); it returns the whole single-file canonical body (per-step contract blocks included) plus the compiled `pipeline_step_count` (`null` if the skill does not compile).

### Durable-job implementation details

`_runtime(root)` resolves `RuntimePaths`, creates the runtime DB/spool/artifact/archive/event directories, and opens or initializes the SQLite store. `root` is expanded and resolved; `TESSELLUM_ROOT` takes precedence when set. The tools do not expose a runtime DB override, so the DB is `TESSELLUM_RUNTIME_DB` or `<root>/runs/runtime/runtime.db`.

`_job_dict` returns `job_id`, `state`, `lane`, `source_event_id`, `capability`, `attempts`, `commit_attempts`, `cancel_requested`, `last_error`, `result_path`, and `supersedes_job_id`. Unlike the CLI job payload, it omits `payload_ref` and lease details. `_tool_get_job` adds events shaped as `{sequence, event_type, at, detail}`.

`_tool_submit_job` resolves `path` from the server process working directory, not relative to `root`; after resolution it must be a stable eligible file below the resolved inbox and inside a named lane. The MCP tool uses `admit_path`'s `settle_seconds=0.0` default. Admission is idempotent for the same source event and bytes, reported by `created`.

`_tool_list_jobs.state`, when non-null, is converted with `JobState(state)`. Valid values are `received`, `admitted`, `routed`, `planning`, `ready`, `running`, `validating`, `committing`, `retry_wait`, `paused`, `complete`, `cancelled`, and `dead_letter`. Unlike CLI `--state`, MCP accepts one state rather than an OR-list.

These five tools control the queue only. They do not expose `work`/`serve`, choose an LLM backend, rebuild the index, or wait for a job. A separate automatic-runtime process must execute admitted work.

## Tool inventory

Twelve tools, advertised as `types.Tool` descriptors.

| Tool | Required args | Optional args (default) | Purpose |
|------|---------------|-------------------------|---------|
| `tessellum_search` | `query` | `k` (10), `db_path` (`data/tessellum.db`) | Hybrid retrieval; note ids/names, fused score, and BM25/dense ranks. |
| `tessellum_format_check` | `path` | — | Validate a note or directory against TESS-001..005 + YAML frontmatter + link rules. |
| `tessellum_bb_audit` | — | `db_path` (`data/tessellum.db`) | Corpus BBGraph telemetry: node/edge counts, untyped edges, unrealised schema edges. |
| `tessellum_fz_traverse` | `fz`, `direction` | `db_path` (`data/tessellum.db`) | Walk a Folgezettel trail; `direction` ∈ `ancestors` / `descendants` / `siblings`. |
| `tessellum_capture` | `flavor`, `slug` | `vault_root` (`vault`), `destination`, `filename_prefix` | Create a new typed note from a template; overrides steer the write. |
| `tessellum_list_skills` | — | — | Enumerate shipped skill canonicals (name + 1-line title). |
| `tessellum_get_skill` | `skill_name` | — | Return one skill canonical's body (per-step contract blocks inline) as text, plus its compiled pipeline step count. |
| `tessellum_submit_job` | `path` | `root` (`"."`) | Spool and durably admit one existing file inside a named inbox lane; returns job fields plus `created`. |
| `tessellum_get_job` | `job_id` | `root` (`"."`) | Return current job fields and up to 500 ordered events; returns an error payload when absent. |
| `tessellum_list_jobs` | — | `root` (`"."`), `state` (`null`), `limit` (`100`) | Return newest-first durable jobs, optionally filtered to one exact state. |
| `tessellum_cancel_job` | `job_id` | `root` (`"."`) | Request cooperative cancellation, or immediately cancel an unleased job; terminal jobs are unchanged. |
| `tessellum_retry_job` | `job_id` | `root` (`"."`) | Create a new admitted job linked to a cancelled or dead-letter job through `supersedes_job_id`. |

## Dispatch and errors

`_dispatch` matches the twelve exact names above and forwards the argument object with `**arguments`; an unknown name raises `ValueError("unknown tool: ...")`. The MCP `call_tool` handler catches every `Exception` and returns one JSON `TextContent` with `{"error": "<ExceptionType>: <message>"}`. Consequently schema omissions, extra arguments, invalid job states, ineligible submit paths, missing jobs in cancel/retry, and invalid retry states are tool-result content rather than protocol failures.

Implementations that explicitly test a resource may return their own `{"error": ...}` without raising. For durable jobs, `get` does this for an unknown ID; `cancel` and `retry` let the store exception reach the handler and therefore include the exception type. All successful and failed results are serialized with two-space indentation and `default=str`.

## CLI — `tessellum mcp`

Registered in `cli/main.py` alongside `bb`, `capture`, `composer`, `dks`, `filter`, `format`, `fz`, `index`, `init`, `runtime`, and `search`.

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
| `mcp` | `>=1.0,<2` | MCP stdio server SDK (`Server`, `types`, `stdio_server`). 2.0 removed the `Server.list_tools` decorator API this server uses; bounded until a deliberate 2.x port. |
| `fastapi` | `>=0.115` | Pulled in by the extra; no HTTP/SSE transport wired yet. |
| `uvicorn` | `>=0.32` | Pulled in by the extra; no HTTP/SSE transport wired yet. |
