# Reference — `tessellum` CLI (`src/tessellum/cli/`)

Lookup surface for the `tessellum` command. For the mental model and the reasons behind these shapes, read [../cli.md](../cli.md).

## Entry point

- Console script: `tessellum = "tessellum.cli:main"` (`pyproject.toml` `[project.scripts]`).
- `cli/__init__.py` re-exports `main` from `cli.main`.
- `tessellum` (no subcommand) → `main._print_banner()`, exit `0`.
- `tessellum --version` → `tessellum 1.2.0` (from `tessellum.__about__.__version__`).

## File → role

| File | Role |
|------|------|
| `cli/__init__.py` | Re-exports `main` so the console script resolves. |
| `cli/main.py` | Dispatcher: `_build_parser`, `main`, `_print_banner`. |
| `cli/init.py` | `tessellum init <target>` → `tessellum.init.scaffold`. |
| `cli/format_check.py` | `tessellum format check <path>` → `tessellum.format.validate`; human/json emitters; non-note skip-list. |
| `cli/capture.py` | `tessellum capture <flavor> <slug>` → `tessellum.capture.capture`; flavors from `list_flavors()`. |
| `cli/index.py` | `tessellum index build` → `tessellum.indexer.build`. |
| `cli/search.py` | `tessellum search <query>` → `tessellum.retrieval` bm25/dense/hybrid/bfs. |
| `cli/filter.py` | `tessellum filter` → `tessellum.retrieval.metadata_search`. |
| `cli/fz.py` | `tessellum fz {list,show,ancestors,descendants,path,all}`; in-Python Folgezettel traversal over `notes`. |
| `cli/bb.py` | `tessellum bb {audit,migrate}` over `tessellum.bb`. |
| `cli/composer.py` | `tessellum composer {validate,compile,run,batch,eval,scaffold-sidecar,digest}` → `tessellum.composer`. |
| `cli/dks.py` | `tessellum dks <observations.jsonl>` → `tessellum.dks`. |
| `cli/mcp.py` | `tessellum mcp serve` → `tessellum.mcp.run_stdio` (lazy `[mcp]` import). |
| `cli/runtime.py` | `tessellum runtime {init,submit,work,serve,get,list,cancel,retry,doctor}` → `tessellum.runtime`. |
| `tessellum/__about__.py` | `__version__` (`"1.2.0"`) + `__status__`; read by the version banner. |

## Dispatcher (`cli/main.py`)

| Symbol | Signature | Role |
|--------|-----------|------|
| `main` | `main(argv: list[str] \| None = None) -> int` | Parse args; run `args.func(args)` if present, else print banner and return `0`. |
| `_build_parser` | `_build_parser() -> argparse.ArgumentParser` | Root parser; registers `--version`; registers 12 top-level groups in order: init, format, capture, index, search, filter, fz, bb, composer, dks, mcp, runtime. |
| `_print_banner` | `_print_banner() -> None` | Bare-command capability listing (Python API + CLI). |

Every subcommand module exposes `add_subparser(subparsers)` and binds a handler via `set_defaults(func=...)`. There is no command registry; `args.func` is the whole dispatch. Optional-leaf groups (`fz`, `bb`, `mcp`) set `func` + a `None` sentinel (`_fz_op` / `_bb_op` / `_mcp_op`) on the group so the bare group prints usage and exits `2`. Groups with `required=True` sub-subparsers (`format`, `index`, `composer`, `runtime`) raise an argparse error on a missing sub-subcommand.

## Exit-code contract

These are the common handler-level meanings. Exceptions a command does not
explicitly map may propagate and terminate the process nonzero.

| Code | Meaning |
|------|---------|
| `0` | Success (results may be empty). |
| `1` | Domain failure — validation error, target exists non-empty, a skill fails to compile/run, a note ERROR. |
| `2` | Invocation error — missing path/DB, supported missing-extra case, bad args, missing sub-subcommand. |

## Commands and flags

### `init <target>`
Handler `run_init`. Flags: `--force/-f`. Exit `1` if target exists non-empty; `2` if target is a file / package data missing.

### `format check <path>` (group `format`, leaf `check`, `required=True`)
Handler `run_format_check`. Dir args recurse `*.md`, skipping `_NON_NOTE_NAMES` (`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `DEVELOPING.md`, `LICENSE.md`, `MEMORY.md`) and `_NON_NOTE_PREFIXES` (`Rank_`). Flags: `--strict`, `--quiet/-q`, `--format {human,json}`. Exit via `_exit_code`: `1` on any ERROR, or any WARNING under `--strict`.

### `capture <FLAVOR> <SLUG>`
Handler `run_capture`. `FLAVOR` enum-constrained to `list_flavors()`. Flags: `--vault` (default `./vault`), `--force/-f`, `--destination` (override REGISTRY dir), `--prefix` (`dest=filename_prefix`).

### `index build` (group `index`, leaf `build`, `required=True`)
Handler `run_index_build`. Flags: `--vault` (default `./vault`), `--db` (default `./data/tessellum.db`), `--force/-f`, `--no-dense` (skip embeddings; disables `search --dense`). Exit `1` if DB exists without `--force`.

### `search <query>`
Handler `run_search`. Strategy — mutually exclusive `store_const` group, default `--hybrid`:

| Flag | Strategy | Backend |
|------|----------|---------|
| `--hybrid` | BM25 + dense via RRF (default) | `hybrid_search` |
| `--bm25` | FTS5 lexical | `bm25_search` |
| `--dense` | sqlite-vec semantic | `dense_search` |
| `--bfs` | best-first BFS; `query` is a vault-relative seed `note_id` | `best_first_bfs` |

Flags: `--db`, `--k` (20), `--depth` (BFS, 3), `--hub-threshold` (BFS, 50), `--no-snippet` (BM25; snippet_length 30→None), `--format {human,json}`. Exit `2` if DB missing.

### `filter`
Handler `run_filter` → `metadata_search`; all filters AND-combine; no filters lists everything up to `--k`. Flags: `--db`, `--k` (100), `--format`. Enum fields: `--building-block`, `--status`, `--category` (`tags[0]`), `--second-category` (`tags[1]`). Any-of array fields: `--tag`, `--keyword`, `--topic`. Dates: `--date-after`, `--date-before` (`YYYY-MM-DD`). Folgezettel: `--folgezettel-prefix`, and mutually-exclusive `--has-folgezettel` / `--no-folgezettel` (`dest=has_folgezettel`, default `None`). Exit `2` if DB missing.

### `fz {list,show,ancestors,descendants,path,all}`
Handler `_run` (dispatches on `_fz_op`). `list`/`all` take no positional; `show`/`ancestors`/`descendants`/`path` take `query` (FZ number or exact `note_name`). Every leaf inherits `--db` via `parents=[db_parent]`. Bare `tessellum fz` exits `2` with usage. Command functions: `_cmd_list`, `_cmd_show`, `_cmd_ancestors`, `_cmd_descendants`, `_cmd_path`, `_cmd_all`. Traversal helpers: `_load_fz_notes`, `_children_index`, `_ancestor_chain`, `_descendants`, `_resolve`; sort key `fz_sort_key`; trail-root `fz_trail_root`; row dataclass `FZNote`.

### `bb {audit,migrate}`
Group handler defaults to `run_bb_audit`; bare `tessellum bb` exits `2` with usage.

- `audit` (`run_bb_audit`, `_bb_op="audit"`): `BBGraph.from_db(db)` → `_build_audit_report`. Flags: `--db`, `--format`, `--show-untyped`. Reports node counts by BB type, edges by schema label, untyped corpus edges, orphan nodes, unrealised schema edges.
- `migrate` (`run_bb_migrate`, `_bb_op="migrate"`): retroactive `bb_schema_version` stamp classification. Flags: `--vault` (default `./vault`), `--target-version` (`current` | int), `--apply`, `--format`. The current warning-only check classifies every parseable lagging note as would-pass; `--apply` bumps those stamps but does not validate against the target schema.

### `composer {validate,compile,run,batch,eval,scaffold-sidecar,digest}` (`composer_command` `required=True`)

| Sub | Handler | Positional | Notable flags |
|-----|---------|-----------|---------------|
| `validate` | `run_composer_validate` | `skill` (file or dir of `skill_*.md`) | `--format` |
| `compile` | `run_composer_compile` | `skill` (`.md`) | `--output/-o`, `--format`, `--no-prompts` |
| `run` | `run_composer_run_cli` | `skill` (`.md`) | see below |
| `batch` | `run_composer_batch_cli` | `jobs` (JSON list) | `--parallelism` (4), `--no-resume`, `--dry-run`, `--mock-responses`, `--backend {mock,anthropic}`, `--model`, `--format` |
| `eval` | `run_composer_eval_cli` | `scenarios_dir` | `--backend {mock,anthropic}`, `--judge-backend {none,mock,anthropic}`, `--mock-responses`, `--judge-mock-responses`, `--model`, `--dry-run`, `--format` |
| `scaffold-sidecar` | `run_composer_scaffold_cli` | `skill` (`.md`) | `--stdout` |
| `digest` | `run_composer_digest_cli` | `--source` (JSON object file) | `--skills-dir`, `--vault`, `--backend {mock,anthropic,bedrock}`, `--model`, `--region`, `--aws-profile`, `--mock-responses`, `--require-agent-signoff`, `--dry-run`, `--format` |

`composer run` base flags: `--leaves`, `--vault` (default `vault`), `--mock-responses`, `--backend {mock,anthropic,bedrock}` (default `mock`), `--region` (default `us-east-1`), `--aws-profile`, `--model`, `--dry-run`, `--no-trace`, `--runs-dir` (default `./runs/composer`), `--format`, `--progress`.

`composer run --dynamic` family (selects `run_pipeline_dynamic`; each flag ignored without `--dynamic`): `--workers` (4), `--manifest`, `--fix-with-backend` (requires `--close-gate`) + `--max-fix-rounds` (1), `--close-gate`, `--max-invocations`, `--max-cost`, `--stats`, `--wave-gate`, `--context-strategy {full_source,windowed}` + `--context-max-chars`, `--skip-unchanged` + `--skip-unchanged-key`. Without `--dynamic`, `run` calls `run_pipeline` (serial reference path).

Default models: `run --backend=anthropic` → `claude-sonnet-4-6`; `run --backend=bedrock` → `us.anthropic.claude-sonnet-4-6` (cross-region inference profile). `batch`/`eval` default `--model` `claude-sonnet-4-6`.

Composer imports from `tessellum.composer`: `compile_skill`, `load_pipeline`, `run_pipeline`, `run_pipeline_dynamic`, `run_batch`, `run_eval`, `run_digestion_pipeline`, `load_scenarios`, `to_dag_json`, `LLMBackend`, `MockBackend`, `LLMJudge`, `Manifest`, `RunBudget`, `BatchJob`, `SignOffPolicy`, `AgentVerdict`, `build_close_gate`, `build_wave_gate`, `make_llm_fixer`, `partition_unchanged_leaves`, `get_assembler`; errors `PipelineValidationError`, `ContractViolation`, `CompilerError`, `EvalError` (`DEFAULT_RUBRIC_DIMENSIONS` is lazy-imported at eval time). `AnthropicBackend` / `BedrockBackend` are lazy-imported at the `--backend` call site. `scaffold-sidecar` uses `tessellum.composer.skill_extractor.list_section_ids` over `<!-- :: section_id = X :: -->` anchors.

The CLI `run` backends are Mock / Anthropic / Bedrock. The fourth backend, `PooledBackend` (credential pool), is Python-level wiring, not a `--backend` choice.

### `dks <observations.jsonl>`
Handler `run_dks_cli`. Positional `observations` optional (`nargs="?"`) — required only for a normal run. JSONL: one observation object per non-blank line; required string `summary`; optional `timestamp`, `mode` (`fresh`|`extend`|`branch`, default `fresh`), `parent_fz` (required for `extend`/`branch`). Writes `<runs-dir>/<UTC-ts>_cycle_<FZ>.json` per cycle + `<UTC-ts>_aggregate.json` unless `--no-trace`.

Baseline flags: `--initial-warrants`, `--backend {mock,anthropic}`, `--model` (`claude-sonnet-4-6`), `--mock-responses`, `--runs-dir` (default `./runs/dks`), `--no-trace`, `--format`.

Gating / grounding flags: `--gate-confidence`, `--gate-threshold` (default `DEFAULT_CONFIDENCE_THRESHOLD` = 0.85; ignored without `--gate-confidence`), `--confidence-model {constant,calibrated}`, `--retrieval-db`, `--perspectives` (default `conservative,exploratory`; N>2 activates pairwise contradicts + Dung grounded labelling; must be unique), `--semantic-disagreement`.

Three short-circuit modes (skip the observations run):

| Mode | Flag | Extra flags |
|------|------|-------------|
| Report | `--report` | `--report-last N`, `--include-bb-graph` + `--bb-db` |
| Calibrate | `--calibrate` | `--target-false-gate-rate` (default 0.10) |
| Meta | `--meta` | `--apply`, `--min-cycles` (default `DEFAULT_MIN_CYCLES` = 20), `--target-failure {premise,warrant,counter-example,undercutting}`, `--proposer {heuristic,llm}`, `--attacker {none,llm}`, `--survive-threshold {strict,majority,permissive}` (default `majority`) |

### `runtime {init,submit,work,serve,get,list,cancel,retry,doctor}` (`runtime_command` `required=True`)

Durable automatic inbox ingestion and job control. Every non-service successful leaf prints JSON to stdout; `serve` runs silently. A bare `tessellum runtime` is an argparse invocation error and exits `2`. Every parser also has argparse's standard `-h/--help`; parse failures exit `2`. Exceptions not explicitly mapped below propagate from `main` (and terminate the console process nonzero).

#### Paths and environment

Every runtime leaf accepts:

| Flag | Default | Resolution |
|------|---------|------------|
| `--root PATH` | current working directory | Passed to `RuntimePaths.discover`; `TESSELLUM_ROOT` takes precedence when set. Paths are expanded and made absolute. |
| `--db PATH` | `<root>/runs/runtime/runtime.db` | Explicit CLI override for the runtime SQLite DB after discovery; otherwise `TESSELLUM_RUNTIME_DB` can override the default. |

Other discovery overrides are `TESSELLUM_RUNS` (default `<root>/runs`), `TESSELLUM_VAULT`, `TESSELLUM_INBOX` (`<root>/inbox`), `TESSELLUM_SKILLS` (`<vault>/resources/skills`), and `TESSELLUM_INDEX_DB` (`<root>/data/tessellum.db`). Without `TESSELLUM_VAULT`, discovery uses `<root>` when `<root>/resources/skills` identifies a directly scaffolded vault, otherwise `<root>/vault`. Opening any command creates the runtime DB parent plus the spool, artifact, archive, and event directories and initializes/migrates the DB schema. It does not create the vault, skills, inbox, or index parent unless the specific command says so.

`work` and `serve` also accept the execution/backend family:

| Flag | Default | Behavior |
|------|---------|----------|
| `--backend {mock,anthropic,bedrock}` | `mock` | Composer backend used by native digestion. |
| `--model MODEL` | backend default | Mock: no model; Anthropic: `claude-sonnet-4-6`; Bedrock: `us.anthropic.claude-sonnet-4-6`. |
| `--region REGION` | `us-east-1` | Bedrock region; parsed but unused by other backends. |
| `--aws-profile PROFILE` | unset | Bedrock AWS profile; parsed but unused by other backends. |
| `--mock-responses PATH` | unset | UTF-8 JSON file loaded and passed to `MockBackend`; parsed for every backend. |
| `--no-index` | false | Skip the commit-tail index rebuild. By default the index is replaced atomically without dense embeddings. |

#### Runtime leaves

| Subcommand | Arguments and flags | Behavior and output | Exit |
|------------|---------------------|---------------------|------|
| `init` | common paths only | Opens the DB, creates the resolved inbox directory, and creates lanes `papers`, `book`, `podcast`, `sops`, `manual_retrieved`, `general`, `latex`, `flash`. Prints `{db, inbox}`. Idempotent. | `0`; filesystem/SQLite errors propagate. |
| `submit PATH` | `--settle-seconds FLOAT` (`0.0`), common paths | Resolves an existing stable regular file, requires the resolved target below a named inbox lane, and rejects hidden names and temporary suffixes `.tmp`, `.part`, `.swp`, `.crdownload`. Spools bytes by SHA-256 before idempotent admission. Prints the job payload plus `created` (`false` returns the existing job). | `0`; `2` for an admission or filesystem error. Argparse errors also exit `2`. |
| `work` | backend family, common paths | Promotes due retries, claims at most one admitted/ready job for digestion or one committing job for commit-only resume, and runs under a heartbeat lease. Prints `{job_id, status, detail}`. Status is `idle`, `complete`, `cancelled`, `retry_wait`, `dead_letter`, or `lease_lost`. | `1` only for `dead_letter` or `lease_lost`; otherwise `0`, including `idle`, `cancelled`, and scheduled retry. Setup/backend errors propagate. |
| `serve` | `--scan-seconds FLOAT` (`2.0`), `--settle-seconds FLOAT` (`1.0`), backend family, common paths | Foreground loop: recursively reconcile the eight known lanes, run one supervisor claim, and wait `scan-seconds` only when idle. Stable-file checks wait `settle-seconds`. SIGINT/SIGTERM requests a graceful stop. No normal JSON output. | `0` after graceful stop; setup/backend/service errors propagate. |
| `get JOB_ID` | `--events` (false), common paths | Prints one job. With `--events`, adds its ordered event history (up to the store default of 500 events). | `0`; `1` and `job not found` on stderr if absent. |
| `list` | repeatable `--state STATE`, `--limit INT` (`100`), common paths | Prints a newest-first JSON array. Repeated states OR together; no state selects all. State choices: `received`, `admitted`, `routed`, `planning`, `ready`, `running`, `validating`, `committing`, `retry_wait`, `paused`, `complete`, `cancelled`, `dead_letter`. | `0`; invalid state/flag exits `2` via argparse. |
| `cancel JOB_ID` | common paths | Requests cancellation and prints the resulting job. An unleased cancellable job moves immediately to `cancelled`; an owned job sets `cancel_requested` for cooperative cancellation; a terminal job is returned unchanged. | `0`; `1` and `job not found` on stderr if absent. |
| `retry JOB_ID` | common paths | Creates and prints a new admitted job whose `supersedes_job_id` points to the prior job. Only `cancelled` and `dead_letter` jobs are retryable; the source event gets a unique retry suffix, so the new generation does not deduplicate to the old job. | `0`; `1` for a missing job or an ineligible state. |
| `doctor` | common paths | Prints all resolved paths and booleans for runtime DB, vault dir, inbox dir, skills dir, index-parent writability, and a jobs read. Note that opening the store makes the runtime DB/read check true; this is a readiness check, not a non-mutating probe. | `0` only when every check is true; otherwise `1`. |

CLI job payloads contain `job_id`, `state`, `lane`, `source_event_id`, `payload_ref`, `capability`, `attempts`, `commit_attempts`, `cancel_requested`, `last_error`, `result_path`, `supersedes_job_id`, and either `lease: null` or `{owner_id, generation, expires_at}`.

Lane execution is explicitly pinned to `native_digestion`; it requires the four digestion skill canonicals under the resolved skills directory. Text sources support `.md`, `.txt`, `.tex`, `.json`, `.jsonl`, and `.csv`; PDF requires `[ingest]`. Other suffixes fail the job. `serve` scans only the eight initialized lanes; manual `submit` can admit another named lane, but routing that job will fail closed as unsupported.

### `mcp serve` (group `mcp`, leaf `serve`)
Handler `run_mcp_serve` (`_mcp_op="serve"`) → `tessellum.mcp.run_stdio` (lazy `[mcp]` import). Bare `tessellum mcp` exits `2` with usage; missing `[mcp]` extras exit `2` with an install hint.

## Optional-dependency extras (`pyproject.toml [project.optional-dependencies]`)

| Extra | Packages | Gates |
|-------|----------|-------|
| `[mcp]` | `mcp>=1.0`, `fastapi`, `uvicorn` | `mcp serve` |
| `[agent]` | `anthropic>=0.40` | `--backend anthropic` / `bedrock`; DKS `--backend anthropic`, `--proposer llm`, `--attacker llm` |
| `[papers]` | `pyzotero`, `requests` | — |
| `[ingest]` | `watchdog`, `beautifulsoup4`, `html2text`, `pdfplumber`, `PyPDF2`, `python-docx`, `python-pptx` | Automatic-runtime PDF source extraction (`pdfplumber`); other packages are ingest headroom. |
| `[dev]` | `pytest`, `pytest-asyncio`, `pytest-cov`, `ruff`, `mypy`, `build`, `twine` | — |

All extras are opt-in; the base CLI imports and runs without any of them. Handlers that explicitly catch `ImportError` return exit `2` with an install hint. Runtime `work`/`serve` backend setup errors currently propagate.

## Extension points

- **New top-level command.** Add `cli/<name>.py` with `add_subparser(subparsers)` that binds `set_defaults(func=...)`; import it in `cli/main.py` and append one call in `_build_parser`. Update `_print_banner` if it should appear in the bare listing.
- **New sub-subcommand.** Add a parser to the group's inner `add_subparsers` with its own `set_defaults(func=...)`. Reuse the `db_parent = ArgumentParser(add_help=False)` + `parents=[db_parent]` idiom (`fz.py` / `bb.py`) to inherit `--db`.
- **New search strategy.** Add a `store_const` option to `search`'s `strategy` group and a branch in `run_search`, backed by a new `tessellum.retrieval` entry point.
- **New Composer backend.** Add a choice to the relevant `--backend` and a construction branch in the corresponding `run_composer_*_cli`, guarding any new dependency with a lazy import + exit-`2` hint (mirror the `[agent]` pattern).
- **New optional feature set.** Add an extra under `[project.optional-dependencies]` and gate its imports at the call site.
