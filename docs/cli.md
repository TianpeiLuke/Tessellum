# Tessellum CLI (`src/tessellum/cli/`)

## 1. Purpose

The `tessellum` command is the operator surface over the whole system: it scaffolds and validates the markdown vault (System P), builds and queries the SQLite index (System D), and drives the Composer/DKS runtimes and the MCP server. Every subcommand is a thin CLI wrapper that parses `argparse` flags and delegates to a runtime package (`tessellum.init`, `tessellum.format`, `tessellum.indexer`, `tessellum.retrieval`, `tessellum.composer`, `tessellum.dks`, `tessellum.mcp`) — the CLI holds no business logic beyond I/O framing and exit codes.

## 2. Architecture / data flow

The console script `tessellum` resolves to `tessellum.cli:main` (`pyproject.toml` `[project.scripts]`), re-exported from `cli/__init__.py`, which forwards to `cli.main.main`. Dispatch is a two-stage `argparse` tree:

1. `main._build_parser()` builds the root `ArgumentParser(prog="tessellum")`, registers `--version` (`action="version"`, banner `f"tessellum {__version__}"` from `__about__.py`), then calls each module's `add_subparser(subparsers)` in a fixed order (init, format, capture, index, search, filter, fz, bb, composer, dks, mcp).
2. `main.main(argv)` calls `parser.parse_args(argv)`. Every leaf subparser binds a handler via `set_defaults(func=...)`. `main` runs `args.func(args)` if `func` is present and returns its int exit code; otherwise (bare `tessellum`) it calls `_print_banner()` and returns `0`.

The `func`-attribute convention is the entire dispatcher — there is no command registry or lookup table. Groups with sub-subcommands (`format`, `index`, `fz`, `bb`, `composer`, `mcp`) nest a second `add_subparsers`; the leaf sets `func`, and for optional-leaf groups (`fz`, `bb`, `mcp`) the *group* also sets `func` + a sentinel (`_fz_op=None` / `_bb_op=None` / `_mcp_op=None`) so bare `tessellum fz` reaches a handler that prints usage and exits `2`. `composer` and `index`/`format` use `required=True` on their sub-subparsers instead, so a missing sub-subcommand is an argparse error.

Data flow per family: **P → D** is `index build` (vault markdown → `tessellum.indexer.build` → SQLite). **D → answers** is `search`, `filter`, `fz`, `bb audit` (all read the DB via `tessellum.retrieval` / `tessellum.bb.BBGraph.from_db`). **P → P** is `init`, `capture`, `format check`, `bb migrate` (filesystem only, no DB). **Runtimes** are `composer` and `dks` (LLM-backed execution) and `mcp serve` (long-lived server).

## 3. Key modules + abstractions

| File | Role |
|------|------|
| `cli/__init__.py` | Re-exports `main` so the `tessellum` console script resolves. |
| `cli/main.py` | Dispatcher: `_build_parser` (registers all 11 groups), `main` (`args.func` dispatch), `_print_banner` (bare-command capability listing). |
| `cli/init.py` | `tessellum init <target>` → `tessellum.init.scaffold`. |
| `cli/format_check.py` | `tessellum format check <path>` → `tessellum.format.validate`; human/json emitters; non-note skip-list. |
| `cli/capture.py` | `tessellum capture <flavor> <slug>` → `tessellum.capture.capture`; flavors from `list_flavors()`. |
| `cli/index.py` | `tessellum index build` → `tessellum.indexer.build`. |
| `cli/search.py` | `tessellum search <query>` → `tessellum.retrieval` bm25/dense/hybrid/bfs. |
| `cli/filter.py` | `tessellum filter` → `tessellum.retrieval.metadata_search` (metadata-only). |
| `cli/fz.py` | `tessellum fz {list,show,ancestors,descendants,path,all}` — in-Python Folgezettel traversal over the `notes` table. |
| `cli/bb.py` | `tessellum bb {audit,migrate}` — corpus BB-graph telemetry + retroactive `bb_schema_version` classification. |
| `cli/composer.py` | `tessellum composer {validate,compile,run,batch,eval,scaffold-sidecar}` → `tessellum.composer`. |
| `cli/dks.py` | `tessellum dks <observations.jsonl>` — Dialectic Knowledge System multi-cycle runner (`--report`/`--calibrate`/`--meta` modes). |
| `cli/mcp.py` | `tessellum mcp serve` → `tessellum.mcp.run_stdio` (lazy import of the `[mcp]` SDK). |
| `tessellum/__about__.py` | Single source of `__version__` (`"1.0.0"`) + `__status__`; read by the version banner. |

## 4. Invariants / design decisions + WHY

- **`args.func` is the whole dispatcher (`main.main`).** No command registry — each module owns its wiring via `add_subparser` + `set_defaults(func=...)`. Adding a command = write a module with `add_subparser`, import it, add one call in `_build_parser`. WHY: keeps command definition co-located with its handler and keeps `main.py` a flat list.
- **Thin CLI over fat runtime.** Every handler translates flags → a runtime call and maps exceptions → exit codes; it never reimplements logic. WHY: the same runtime is reused by MCP tools and tests, so behavior can't diverge between surfaces.
- **Consistent exit-code contract.** `0` success, `1` domain failure (e.g. validation error, target exists, a skill fails to compile/run), `2` invocation error (missing path/DB, missing extras, bad args). Codified per-module (e.g. `format_check._exit_code`, `init` docstring, `composer` docstring). WHY: scriptability — callers branch on `1` (fix the content) vs `2` (fix the invocation).
- **`--format {human,json}` on every read/telemetry command** (`format check`, `search`, `filter`, `bb audit`, `bb migrate`, `dks`, and the `composer` verbs validate/compile/run/batch/eval — not scaffold-sidecar, which has only `--output`/`--force`/`--stdout`). WHY: the same command serves human operators and machine consumers (agents, CI, the MCP layer).
- **The serial Composer path is the default and byte-identical; `--dynamic` is strictly opt-in (`composer.run_composer_run_cli`, IDENT-4).** `if getattr(args, "dynamic", False)` selects `run_pipeline_dynamic` (L860); the `else` branch calls `run_pipeline` (L884). Every `--dynamic`-family flag (`--workers`, `--manifest`, `--close-gate`, `--fix-with-backend`, `--max-invocations`/`--max-cost`, `--wave-gate`, `--context-strategy`, `--skip-unchanged`, `--stats`) is documented as "Ignored without `--dynamic`." WHY: the wave-parallel runtime must never silently change the reference execution semantics.
- **DKS is a peer runtime, not a Composer subcommand (`dks.py` docstring).** It reuses Composer's `LLMBackend`/`MockBackend` but lives at top-level `tessellum dks`. WHY: independent lifecycle and mode surface (`--report`/`--calibrate`/`--meta`) that doesn't belong under the pipeline executor.
- **`fz` derives trail topology at query time in Python, not via a materialized view (`fz.py` docstring, `_ancestor_chain`/`_descendants`).** It loads all FZ-bearing rows (`folgezettel`, `folgezettel_parent`) and walks the parent chain in memory; traversals are cycle-safe (`seen`/`visited` guards). WHY: target vaults are small (<~1000 FZ notes), so in-memory traversal is simpler and more portable than a recursive CTE and needs no extra DB schema.
- **`filter` is metadata-only; content search lives under `search` (`filter.py` docstring).** Filters AND-combine; no filters lists everything up to `--k`. WHY: a clean split between "what kind of note" (SQL on `notes` columns) and "what content" (retrieval).
- **Optional dependencies are lazy-imported at the call site, not at module import.** `mcp serve` imports `tessellum.mcp.run_stdio` inside `run_mcp_serve` and returns `2` with an install hint on `ImportError`; `composer run --backend=anthropic|bedrock` and `dks --backend=anthropic` / `--proposer llm` / `--attacker llm` guard the `[agent]` extras the same way. WHY: users without extras must still be able to load and use the rest of the CLI.
- **`bb migrate` never auto-rewrites would-fail notes.** `--apply` bumps `bb_schema_version` only on notes that would pass `TESS-005`; would-fail notes are reported for manual review (`run_bb_migrate`). WHY: passive migration must not silently rewrite content that doesn't actually conform.
- **Retrieval has no PageRank/PPR.** `search` exposes exactly `--bm25`, `--dense`, `--hybrid` (default, RRF fusion), `--bfs` (graph, seed-note argument) — a single mutually-exclusive group with `strategy="hybrid"` default. No ranking-by-centrality path exists in the CLI.

## 5. Public API / CLI

Entry point: `console_scripts` `tessellum = "tessellum.cli:main"`. Bare `tessellum` prints the version + capability banner (`main._print_banner`) and exits `0`. `tessellum --version` prints `tessellum 1.0.0` (from `__about__.__version__`).

The eleven top-level commands and their real flags:

1. **`init <target>`** — scaffold a new vault via `tessellum.init.scaffold`. Flags: `--force/-f` (scaffold into a non-empty dir). Exit `1` if target exists non-empty, `2` if target is a file / package data missing.
2. **`format check <path>`** — validate notes against the YAML spec (`tessellum.format.validate`). Dir args recurse `*.md`, skipping non-note names (`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `DEVELOPING.md`, `LICENSE.md`, `MEMORY.md`) and `Rank_*` prefixes. Flags: `--strict` (warnings → exit 1), `--quiet/-q`, `--format {human,json}`. (`format` is a group; `check` is its only leaf, `required=True`.)
3. **`capture <FLAVOR> <SLUG>`** — create a note from a template (`tessellum.capture.capture`). `FLAVOR` is enum-constrained to `list_flavors()`. Flags: `--vault` (default `./vault`), `--force/-f`, `--destination` (override REGISTRY dir), `--prefix` (override filename prefix, `dest=filename_prefix`).
4. **`index build`** — build the unified SQLite index (`tessellum.indexer.build`). Flags: `--vault` (default `./vault`), `--db` (default `./data/tessellum.db`), `--force/-f`, `--no-dense` (skip embeddings; disables `search --dense`).
5. **`search <query>`** — content retrieval (`tessellum.retrieval`). Strategy (mutually exclusive, default `--hybrid`): `--bm25` (FTS5), `--dense` (sqlite-vec), `--hybrid` (BM25+dense via RRF), `--bfs` (best-first BFS; the `query` arg is a vault-relative seed note_id). Flags: `--db`, `--k` (default 20), `--depth` (BFS, default 3), `--hub-threshold` (BFS, default 50), `--no-snippet` (BM25), `--format {human,json}`. Exit `2` if the DB is missing.
6. **`filter`** — metadata query (`tessellum.retrieval.metadata_search`), all filters AND-combined. Flags: `--db`, `--k` (default 100), `--format`; enum fields `--building-block`, `--status`, `--category`, `--second-category`; any-of array fields `--tag`, `--keyword`, `--topic`; dates `--date-after`, `--date-before`; Folgezettel `--folgezettel-prefix` and the mutually-exclusive `--has-folgezettel`/`--no-folgezettel`.
7. **`fz {list|show|ancestors|descendants|path|all}`** — Folgezettel trail explorer. `list`/`all` take no positional; `show`/`ancestors`/`descendants`/`path` take a `query` (FZ number or exact note_name). Every leaf accepts `--db` (via a shared `parents=[db_parent]`). Bare `tessellum fz` exits `2` with usage.
8. **`bb {audit|migrate}`** — BB ontology / corpus-graph ops. `audit` (`BBGraph.from_db`): `--db`, `--format`, `--show-untyped`; reports node counts by BB type, edges by epistemic-edge label, untyped corpus edges, orphan nodes, unrealised schema edges. `migrate`: `--vault` (default `./vault`), `--target-version` (`current`|int), `--apply` (bump `bb_schema_version` on would-pass notes only), `--format`. Bare `tessellum bb` exits `2` with usage.
9. **`composer {validate|compile|run|batch|eval|scaffold-sidecar}`** — pipeline ops (`tessellum.composer`; `composer_command` is `required=True`).
   - `validate <skill>` — sidecar schema + cross-file checks; `--format`.
   - `compile <skill>` — compile to a typed DAG (zero LLM calls); `--output/-o`, `--format`, `--no-prompts`.
   - `run <skill>` — execute against leaves. Serial default; `--dynamic` opts into the v4 wave-parallel scheduler. Base flags: `--leaves`, `--vault`, `--mock-responses`, `--backend {mock,anthropic,bedrock}` (default `mock`; `anthropic`/`bedrock` need `[agent]` extras), `--region`, `--aws-profile`, `--model`, `--dry-run`, `--no-trace`, `--runs-dir`, `--format`, `--progress`. `--dynamic` family (else ignored): `--workers` (4), `--manifest`, `--fix-with-backend` + `--max-fix-rounds`, `--close-gate`, `--max-invocations`, `--max-cost`, `--stats`, `--wave-gate`, `--context-strategy {full_source,windowed}` + `--context-max-chars`, `--skip-unchanged` + `--skip-unchanged-key`.
   - `batch <jobs.json>` — many jobs in parallel with resume; `--parallelism` (4), `--no-resume`, `--dry-run`, `--mock-responses`, `--backend {mock,anthropic}`, `--model`, `--format`.
   - `eval <scenarios_dir>` — scenario assertions + `LLMJudge` rubric; `--backend {mock,anthropic}`, `--judge-backend {none,mock,anthropic}`, `--mock-responses`, `--judge-mock-responses`, `--model`, `--dry-run`, `--format`.
   - `scaffold-sidecar <skill>` — starter `.pipeline.yaml` from `<!-- :: section_id = X :: -->` anchors; `--output/-o`, `--force`, `--stdout`.
   Note the CLI's `run` backends are Mock/Anthropic/Bedrock; the fourth backend (Pooled/`PooledBackend`) is a Python-level credential-pool wiring, not a `--backend` choice.
10. **`dks <observations.jsonl>`** — Dialectic Knowledge System multi-cycle runner. Baseline flags: `--initial-warrants`, `--backend {mock,anthropic}`, `--model`, `--mock-responses`, `--runs-dir`, `--no-trace`, `--format`, plus gating (`--gate-confidence`/`--gate-threshold`, `--confidence-model`, `--retrieval-db`, `--perspectives`, `--semantic-disagreement`). Three short-circuit modes (skip the observations run): `--report` (aggregate `*_aggregate.json` under `--runs-dir`; `--report-last N`, `--include-bb-graph`+`--bb-db`), `--calibrate` (replay to hit `--target-false-gate-rate`, default 0.10), `--meta` (build a `MetaObservation` and propose schema edits — dry-run unless `--apply`; `--min-cycles`, `--target-failure`, `--proposer {heuristic,llm}`, `--attacker {none,llm}`, `--survive-threshold`).
11. **`mcp serve`** — run the MCP stdio server (`tessellum.mcp.run_stdio`). MCP is shipped, not deferred. Bare `tessellum mcp` exits `2` with usage; missing `[mcp]` extras exit `2` with an install hint.

**Optional-dependency extras** (`pyproject.toml [project.optional-dependencies]`): `[mcp]` (`mcp>=1.0`, `fastapi`, `uvicorn`) for `mcp serve`; `[agent]` (`anthropic>=0.40`) for the `anthropic`/`bedrock` LLM backends; `[papers]` (`pyzotero`, `requests`); `[ingest]` (`watchdog`, `beautifulsoup4`, `html2text`, `pdfplumber`, `PyPDF2`, `python-docx`, `python-pptx`); `[dev]` (`pytest`, `pytest-asyncio`, `pytest-cov`, `ruff`, `mypy`, `build`, `twine`). All are opt-in; the base CLI loads without any of them.

## 6. Extension points

- **New top-level command.** Add `cli/<name>.py` exposing `add_subparser(subparsers)`; register a leaf handler with `set_defaults(func=...)`; import it in `cli/main.py` and append one `add_<name>_subparser(subparsers)` call in `_build_parser`. Nothing else wires it — `main` finds it via `args.func`. Update `_print_banner` if it should appear in the bare-command listing.
- **New sub-subcommand** in a group (`composer`/`bb`/`fz`/`index`/`format`/`mcp`): add a parser to the group's inner `add_subparsers` with its own `set_defaults(func=...)`. Reuse the `db_parent = ArgumentParser(add_help=False)` + `parents=[db_parent]` idiom (see `fz.py`/`bb.py`) to inherit `--db`, since argparse subparsers don't inherit parent-group args.
- **New search strategy:** add a `store_const` option to `search`'s mutually-exclusive `strategy` group and a branch in `run_search`, backed by a new `tessellum.retrieval` entry point.
- **New Composer backend:** add a choice to `run_cmd`'s `--backend` (and/or `batch`/`eval`) and a construction branch in the corresponding `run_composer_*_cli`, guarding any new optional dependency with a lazy import + exit-2 install hint (mirror the `[agent]` pattern).
- **New optional feature set:** add an extra under `[project.optional-dependencies]` and gate its imports at the call site so the base CLI stays importable without it.
