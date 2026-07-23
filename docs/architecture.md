# Tessellum 1.0.0 — System Architecture

## 1. What Tessellum is

Tessellum builds knowledge the way a mind does — by writing atomic, typed thoughts and then indexing them so they can be found again. It is a knowledge-construction system, and its shape is a CQRS split: one side is written, the other side is read and computed. The written side is a vault of markdown notes. The read side is a database projected from that vault, plus the machinery that searches and reasons over it. The two sides are named System P and System D, and the arrow between them points one way. Everything else in this document is a consequence of that arrow.

The essential idea is that authorship and computation live on opposite sides of a wall. Humans and agents write notes; nothing writes back over their heads. This is what makes the system trustworthy: there is exactly one source of truth, and it is human-legible.

## 2. The two systems

System P is the substrate. It is the `vault/` directory of typed markdown notes. Each note carries YAML frontmatter — its building block type, its Folgezettel position, its tags, the schema version it was born under — and a body woven with plain `[text](path.md)` links. Notes are authored by humans and by agents. The vault is the single source of truth. No part of the system writes vault-authoritative state from anywhere else.

System D is the projection. It is one SQLite database, built from the vault, together with the retrieval, composer, and DKS layers that read it. Its schema is defined once, in `indexer/schema.sql`. The database holds nothing the vault does not already imply; it is the vault made queryable.

The flow between them runs one way, P to D, and only one way. The index is a pure projection: the build step is idempotent and drops-and-recreates the database on every run, so the DB can never drift from the vault by accumulating edits. The database wrapper is deliberately read-oriented — its own docstring tells any caller who wants to change a row to rebuild instead of mutate. The DKS side states this law by name as **R-Cross**: System P calls System D, but System D never calls System P. The read-through client it exposes has no path back.

```
   authoring (humans + agents)
            │  writes .md
            ▼
   ┌──────────────────┐   build (drop+recreate)    ┌───────────────────────────┐
   │  System P: vault/ │ ─────────────────────────▶ │ System D: data/tessellum.db│
   │  typed markdown   │        one-way P→D          │ notes + note_links +      │
   │  (source of truth)│                             │ notes_fts + notes_vec     │
   └──────────────────┘ ◀───(read-through only)───── └───────────────────────────┘
            ▲                                                    │
            │  materialize new notes                            │ read
            │  (composer / DKS step-7)                          ▼
            └──────────────── retrieval · composer · dks ───────┘
```

There is one feedback arrow, and it does not break the law. The composer and DKS engines read System D, then write brand-new markdown into System P. They author notes; they never claim authority in the database. On the next build, the vault they wrote is re-projected. So the loop closes through the substrate, never around it.

## 3. The subsystem map

Read the system from the ground up, and it stacks in layers. At the bottom sit two primitives. Above them, projection. Above that, the ways of reading. At the top, the two engines and the two front doors.

```
   bb  ─────────┐  (BB ontology: types + corpus graph)
   format ──────┤  (parse / validate .md; the P-side gatekeeper)
                ▼
   indexer ─────►  build vault → SQLite (P→D)
                ▼
   retrieval ───►  5 surfaces over the DB (metadata/bfs/bm25/dense/hybrid)
                ▼
   composer ────►  compile skill → typed DAG → schedule → gate → fix → observe
   dks ─────────►  7-component dialectic cycles over bb + retrieval, deposit FZ subtrees
                ▼
   cli ─────────►  11 subcommands (the human front door)
   mcp ─────────►  7 stdio tools (the agent front door)
   composer-ts ─►  TypeScript control-flow bridge over the composer CLI
```

The `bb` subsystem is the ontology of Building Blocks. It fixes what kinds of thought exist and how they may connect. `bb/types.py` is the source of truth for the eight BB types and the roughly sixteen typed edges between them; `bb/graph.py` is the corpus view — the actual instances, streamed from the index. The `format` subsystem is the gatekeeper on the P side: it parses a note into frontmatter and body, validates it against the YAML spec and the link and edge rules, and checks its links. Nothing enters the vault well-formed by accident; `format` is where form is enforced.

The `indexer` is the projector — it walks the vault and writes every table in one transaction. `retrieval` offers five ways to find a note. The `composer` compiles a skill into a typed pipeline and runs it. `dks` runs dialectic reasoning cycles that grow the vault. And three surfaces expose all of this: `cli`, eleven subcommands for humans; `mcp`, seven stdio tools for agents; and `composer-ts`, a thin TypeScript bridge over the composer — a control-flow shell, not a reimplementation.

## 4. The memory model

The deepest idea in Tessellum is where authority lives. It lives in the vault, and nowhere else. Everything the system stores beyond the vault is either a projection that can be rebuilt from it, or a log that merely records how the present was reached.

| Store | Kind | Rebuildable from | Authority |
|---|---|---|---|
| `vault/` markdown | **source of truth** | — | authoritative |
| `data/tessellum.db` | derived projection | vault (`index build`, drop+recreate) | never authoritative |
| composer resume manifest | durable projection | vault (`Manifest.rebuild_from_vault`) | never authoritative |
| DKS `warrant_history.jsonl`, `schema_events.jsonl` | append-only logs (in `runs/`, outside vault + package) | — (log, not state) | event history |

The database is the obvious projection: drop it, rebuild it, lose nothing. The subtler one is the composer's resume manifest, which tracks how far a long pipeline got. It could have been treated as state, and then a crash could corrupt progress. It is not. It is a rebuildable projection — this is the invariant named **IDENT-2** — and its done-status is reconstructed purely from which target notes exist on disk. A lost or corrupt manifest is therefore always recoverable by looking at the vault. The DKS logs are the third kind: they are event-sourced. The current set of warrants lives in a registry; the history log only records how that set came to be. Schema growth works the same way. The lesson is uniform. Only the vault is authoritative, so only the vault must be protected; everything else can be thrown away and remade.

## 5. The Composer-v4 engine

The composer turns a skill — a written procedure — into a running pipeline that materializes notes. Its governing principle is that all structure is resolved before any money is spent. Compilation is pure logic, zero LLM calls: it loads the skill and its sidecar, validates the step contracts, topologically sorts the steps by their dependencies, catches cycles and forward references, and emits a typed DAG. If the pipeline is structurally broken, it fails here — deterministically, cheaply, before a single model is invoked.

Execution then flows through five stages.

```
 compile ─► schedule ─► gate ─► fix ─► observe
 (compiler) (scheduler) (gates) (fix)  (manifest / eval / signoff)
```

Compilation produces the DAG and dispatches nothing. Scheduling runs it — either serially, as the reference path, or wave-parallel, as the opt-in fast path. Each step resolves its placeholders, dispatches to a backend under a watchdog, validates the response against a schema, and hands the result to a materializer. Gating checks the work. Fixing repairs what fails a gate, without ever making it worse — it checkpoints the note's bytes before each attempt and keeps the best-scoring version. Observing records what happened: the manifest for resume, the evaluator for structural assertions and a judged rubric, the signoff ladder for approval, the credential pool for key rotation and run budgets.

Two lines are load-bearing here. The gates are pure programs and never call a model — when a gate needs a semantic judgment, it consumes a verdict a verifier already produced, rather than judging for itself. And the LLM lives only where it must: inside the fixer callable and inside the backends, injected by the caller, never buried in the control logic. The engine orchestrates; the model only produces content the engine then checks.

## 6. The DKS engine

DKS is the Dialectic Knowledge System — the part of Tessellum that thinks. Where the composer executes a written procedure, DKS runs a reasoning cycle and deposits its conclusions back into the vault as a Folgezettel subtree. One cycle is a closed seven-component loop: an observation, then several sibling arguments, then the disagreements between them as edges, then a counter, then a pattern, then one or more revised warrants. A runner threads many such cycles together, carrying warrant changes forward from one to the next. Each cycle leaves a small, typed argument-tree behind in System P.

The engine has two additive refinements, both designed to change nothing they touch. Confidence gating lets a cycle short-circuit: when confidence is high, it emits just an observation and a single argument, skipping most of the loop and saving most of the backend round-trips; when confidence is low, the full dialectic runs. Dung argumentation handles genuine multi-perspective conflict: when more than two views produce a graph of contradiction edges, grounded labelling decides which arguments survive, using Dung's grounded semantics. For the two-perspective case it collapses back to the original single-edge outcome — a strict extension, never a replacement. A generic FSM walker over the schema offers an alternative dispatcher for the same components, again leaving the core cycle untouched.

## 7. The invariants and why they hold

The composer names its load-bearing invariants IDENT-2 through IDENT-5 in its own docstrings, but they are the spine of the whole system, not just one subsystem. Each one is a rule about how to fail, because a knowledge system is only as trustworthy as its behavior under stress.

The first is that the vault is the source of truth — **IDENT-2**. The database and the resume manifest are rebuildable projections and nothing more. This holds because a lost or corrupt projection is always recoverable by re-reading the vault, and because there is no second authority that could ever need reconciling.

The second is that gates are pure programs — **IDENT-3**. Every gate is deterministic code, and the one gate that needs a semantic verdict consumes one a verifier already produced rather than invoking a model itself. The same discipline runs through the fixer, the planner, the credential pool, and the signoff ladder: the program orchestrates, the agent or human produces the verdict. The reason is stark. A gate is a commit-check. A gate that could hallucinate a PASS would be worthless, and worse than worthless if it silently corrupted the substrate.

The third is that the serial path is byte-identical — **IDENT-4**. The serial scheduler is the reference, and it stays the default. The dynamic wave scheduler is opt-in, reached only through an explicit flag, and it is defined to produce the same vault output, the same per-leaf outcomes, and the same ordered result. Parallelism is a throughput optimization, and an optimization must never change answers. The serial path stays the ground truth to diff against.

The fourth is fail-closed — **IDENT-5**. A gate that cannot prove PASS is a FAIL. An unverifiable source is a FAIL, never a plausibility pass. A corrupt manifest falls back to the newest good backup or starts empty with a logged warning. An empty backend outcome is treated as a crash. The principle is that silent success on unproven state corrupts the substrate, and refusing is always safe.

And underneath the reasoning ontology, one more invariant makes growth possible without erasing history: the schema is closed, finite, versioned, and event-sourced. The full schema is the epistemic edges, plus navigation edges, plus DKS extensions, plus whatever the user has added — around sixteen typed edges over eight BB types. User additions are the fold over an append-only event log; retractions are first-class events, and the log is never rewritten. The schema version bumps on each landed event, and the schema can be reconstructed as of any past version, so a note always validates against the schema it was frozen under at creation. The reason is that an ontology must be able to grow under discipline without invalidating what was typed before it. Old edges stay interpretable forever.

## 8. Key modules and abstractions

| File | Role |
|---|---|
| `bb/types.py` | Source of truth for the 8 `BBType` values, `EpistemicEdgeType`, the composed `BB_SCHEMA` (~16 edges), `BB_SCHEMA_VERSION`, and event-sourced schema growth (`SchemaEditEvent`, `fold_schema_events`, `BB_SCHEMA_AT_VERSION`). |
| `bb/graph.py` | Corpus (instance) BB graph. `BBGraph.schema` = the 8-node type graph; `BBGraph.from_db` streams the vault's BB-typed notes + edges from the index (read-only). |
| `format/parser.py` | Parse a `.md` note into frontmatter + body (`parse_note`, `Note`). |
| `format/validator.py` | `validate` / `is_valid` — YAML-0xx, LINK-00x, TESS-00x rules. The vault-side gatekeeper. |
| `format/frontmatter_spec.py` | The YAML spec data (valid PARA buckets, statuses, `VALID_BUILDING_BLOCKS` derived from `BBType`, forbidden fields). |
| `indexer/schema.sql` | The one DDL: `notes`, `note_links`, `notes_vec` (vec0, 384-dim cosine), `notes_fts` (FTS5, porter+unicode61). |
| `indexer/build.py` | `build` — walk vault, parse notes, extract links w/ broken-path detection, write all four tables in one transaction. Drop+recreate (idempotent). |
| `indexer/db.py` | `Database` — read-oriented typed query wrapper (`NoteRow`, `LinkRow`). |
| `retrieval/{metadata,graph,bm25,dense,hybrid}.py` | The five retrieval surfaces (see §9). `router.py` = heuristic query→surface classifier. |
| `composer/compiler.py` | Skill canonical+sidecar → typed `CompiledPipeline` DAG. Zero LLM. |
| `composer/contracts.py` | Typed registries: `MATERIALIZER_CONTRACTS`, `BACKEND_CONTRACTS`, `MCP_CONTRACTS`; `ContractViolation`. |
| `composer/scheduler.py` | `run_pipeline` (serial reference) + `run_pipeline_dynamic` (wave-parallel, self-claiming). |
| `composer/executor.py` | `execute_step` unit op: placeholder resolve → dispatch → schema-validate → materialize; retry ladders. |
| `composer/materializer.py` | Five materializers (no_op, body_markdown_to_file, body_markdown_frontmatter_to_file, edits_apply_to_files, edits_apply_xml_tags) — the D→P authoring seam. |
| `composer/gates.py` | One `Gate` abstraction at plan/session/wave scope. Pure predicates; never call an LLM. |
| `composer/fix.py` | Non-regressive close-gate repair (checkpoint bytes, keep best snapshot). |
| `composer/manifest.py` | Per-leaf/per-attempt resume ledger; rebuildable from the vault. |
| `composer/llm.py` | `LLMBackend` protocol + 4 backends: `MockBackend`, `AnthropicBackend`, `BedrockBackend`, `PooledBackend`. |
| `composer/credential_pool.py` | Same-provider key pool (leasing, error-class rotation, cooldowns) + `RunBudget` (invocation/token caps). |
| `composer/{planning,signoff,eval}.py` | Selective planning depth + $0 change-detection pre-gate; plan→execute approval ladder; scenario assertions + LLMJudge rubric. |
| `dks/core.py` | `DKSCycle` (7-component loop) + `DKSRunner` (multi-cycle) + the 7 typed component dataclasses + FZ allocator. |
| `dks/dung.py` | `DungAF` + `grounded_labelling` — multi-perspective survivorship. |
| `dks/fsm.py` | Generic FSM walker over `BB_SCHEMA` (additive dispatcher). |
| `dks/confidence.py` | Confidence gate (`ConstantConfidence`, `CalibratedConfidence`). |
| `dks/persistence.py` | `WarrantRegistry` (current set) + `WarrantHistory` (append-only JSONL log). |
| `dks/retrieval_client.py` | R-Cross read-through client wrapping `hybrid_search`; no path back to P. |
| `cli/main.py` | Dispatcher wiring the 11 subparsers; bare `tessellum` prints the capability banner. |
| `mcp/server.py` | `build_server` / `run_stdio` — 7 tools over stdio (see §9). |
| `composer-ts/src/{bridge,dag}.ts` | TS control-flow bridge: shells the composer CLI (`bridge.ts`) + pure DAG-walk helpers (`dag.ts`). Zero contract logic. |

## 9. Public surfaces

**CLI — 11 subcommands** (wired in `cli/main.py`):

`init` · `format` · `capture` · `index` · `search` · `filter` · `fz` · `bb` · `composer` · `dks` · `mcp`.

Selected surfaces:

- `tessellum index build` — build the unified SQLite index (P→D).
- `tessellum search <query> [--bm25|--dense|--hybrid|--bfs]` — the five retrieval surfaces: **metadata** (structured filter), **bfs** (best-first BFS over `note_links`), **bm25** (FTS5 lexical), **dense** (sqlite-vec cosine over 384-dim MiniLM embeddings), **hybrid** (RRF fusion, the default). There is **no PageRank** in retrieval — the schema notes `static_ppr_score` is an *unshipped* parity column.
- `tessellum filter --tag <t> [--bb …]` — metadata-only filtering.
- `tessellum fz {list|show|ancestors|descendants|path|all}` — Folgezettel trail explorer.
- `tessellum bb audit` — corpus BB-graph telemetry (counts, untyped edges, unrealised schema edges).
- `tessellum composer {validate|compile|run|batch|eval}` — the composer subcommands; `run --backend={mock|anthropic|bedrock}`, `run --dynamic [--workers N --manifest PATH]` opts into the v4 wave scheduler.
- `tessellum dks <observations.jsonl>` — run a multi-cycle DKS session.
- `tessellum mcp serve` — start the stdio MCP server.

**Python API** (banner in `cli/main.py`): `from tessellum import BB_SPECS, validate, parse_note, Note, Issue`; `from tessellum.composer import load_pipeline, Pipeline, ContractViolation`; `from tessellum.indexer import build, Database`; `from tessellum.retrieval import bm25_search, dense_search, hybrid_search, best_first_bfs, metadata_search`.

**MCP — 7 tools over stdio** (`mcp/server.py`, requires `[mcp]` extras): `tessellum_search`, `tessellum_format_check`, `tessellum_bb_audit`, `tessellum_fz_traverse`, `tessellum_capture`, `tessellum_get_skill`, `tessellum_list_skills`. The runtime tools are deterministic Python-API wrappers (no server-side LLM); the skill-canonical tools hand the procedure back for the calling agent to execute. **MCP is shipped, not deferred.**

**composer-ts bridge** (`@tessellum/composer-ts`): `compile`, `run`, `columns`, `readyFrontier`. Runs under Node's native type-stripping with zero npm dependencies.

## 10. Extension points

- **New BB edge / schema growth** — append a `SchemaEditEvent` to `runs/dks/meta/schema_events.jsonl` via `tessellum dks meta --apply` (folded into `BB_SCHEMA_USER_EXTENSIONS`); or commit a project-team edge into `BB_SCHEMA_DKS_EXTENSIONS` in `bb/types.py`. The version and per-version reconstruction follow automatically.
- **New LLM backend** — implement the `LLMBackend` protocol in `composer/llm.py` and register a `LLMBackendContract` in `composer/contracts.py:BACKEND_CONTRACTS`.
- **New materializer** — add a concrete materializer in `composer/materializer.py` and its `MaterializerContract` to `MATERIALIZER_CONTRACTS`; the compiler validates every step's `expected_output_schema` against it.
- **New gate / validator rule** — add a `Gate` predicate (`composer/gates.py`) or a new `TESS-0xx`/`YAML-0xx`/`LINK-00x` rule in `format/validator.py`. Keep it a pure program (IDENT-3).
- **New retrieval surface** — add a primitive under `retrieval/` and route to it in `retrieval/router.py`.
- **New DKS transition handler** — inject a handler for one BB edge via the `dks/fsm.py` transition-handler registry without touching cycle-level code.
- **New MCP tool** — add a descriptor to `tool_specs` in `mcp/server.py`.
- **New CLI subcommand** — add a `cli/<name>.py` exposing `add_subparser` and wire it in `cli/main.py`.

---

**Per-module docs.** This is the map; deeper docs (when present) live alongside each subsystem — `bb`, `format`, `indexer`, `retrieval`, `composer` (compiler/scheduler/gates/fix/manifest/llm), `dks`, `cli`, `mcp`, and the `composer-ts/README.md` bridge doctrine. Grounding files: `src/tessellum/{bb/types.py, indexer/schema.sql, indexer/build.py, indexer/db.py, retrieval/router.py, composer/{compiler,scheduler,gates,fix,manifest,llm,materializer,credential_pool,planning,signoff,eval}.py, dks/{core,dung,fsm,confidence,persistence,retrieval_client}.py, mcp/server.py, cli/main.py, cli/composer.py}` and `composer-ts/README.md`.
