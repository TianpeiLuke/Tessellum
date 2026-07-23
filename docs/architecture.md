# Tessellum 1.0.0 — System Architecture

## 1. Purpose

Tessellum is a typed-atomic-note knowledge-construction system built on a CQRS split: a human/agent-authored markdown vault is the write model (System P), and a derived SQLite index plus a retrieval/composition layer is the read-and-compute model (System D). This document is the top-level map for contributors — it grounds the subsystem boundaries, the one-way P→D data flow, the memory model, and the load-bearing invariants in the actual source under `src/tessellum/`, and links out to the per-module docs.

## 2. Architecture / data flow

### 2.1 The CQRS split — System P and System D

- **System P (substrate, write side).** The `vault/` directory of typed markdown notes. Each note carries YAML frontmatter (`building_block:`, `folgezettel:`, `tags:`, `bb_schema_version:`, …) and a body with markdown `[text](path.md)` links. Notes are authored by humans and agents; the vault is the **single source of truth**. Nothing in the system writes vault-authoritative state from the DB.
- **System D (projection, read side).** One SQLite database (default `data/tessellum.db`) built from the vault, plus the retrieval, composer, and DKS compute layers that read it. Its schema is defined once in `src/tessellum/indexer/schema.sql`.
- **One-way P→D only.** The index is a pure projection of the vault. `indexer/build.py:build` is *idempotent — the DB is dropped + recreated each run* (module docstring), and `indexer/db.py:Database` is deliberately **read-oriented**: its docstring instructs *callers needing to mutate rows should rebuild via `tessellum.indexer.build`*. There is no D→P write path in the substrate. The DKS side names this rule explicitly — `dks/retrieval_client.py` operationalises **R-Cross**: *System P calls System D; System D never calls System P*, exposing only a read-through client with *no path back*.

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

Note the one feedback arrow that does *not* violate P→D: the composer and DKS **materialize new markdown into the vault** (System P), then the DB is rebuilt from that vault. They never mutate the DB as authority — they author notes, which are re-projected on the next `index build`.

### 2.2 Subsystem map

Data flows left-to-right from substrate primitives up to the agent-facing surfaces:

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

- **`bb`** — the Building Block ontology. `bb/types.py` is the *source of truth* for the 8 BB types and the schema graph of ~16 typed edges; `bb/graph.py` is the corpus (instance) view loaded from the DB.
- **`format`** — the P-side gatekeeper: parse markdown+frontmatter (`parser.py`), validate against the YAML spec + link rules + BB-edge rules (`validator.py`), check links (`link_checker.py`).
- **`indexer`** — the P→D projector: `build.py` walks the vault and writes all four tables in one transaction; `db.py` is the thin read wrapper.
- **`retrieval`** — five retrieval surfaces over System D plus a heuristic router.
- **`composer`** — the v4 pipeline that compiles a skill canonical into a typed DAG and executes it (compile → schedule → gate → fix → observe).
- **`dks`** — the Dialectic Knowledge System runtime: closed 7-component cycles that read the substrate and deposit Folgezettel subtrees back into the vault.
- **`cli`** — 11 subcommands dispatched by `cli/main.py`.
- **`mcp`** — a shipped MCP stdio server exposing 7 tools.
- **`composer-ts/`** — a zero-dependency TypeScript bridge (not a port) over the composer CLI.

### 2.3 The memory model (three projections, one truth)

| Store | Kind | Rebuildable from | Authority |
|---|---|---|---|
| `vault/` markdown | **source of truth** | — | authoritative |
| `data/tessellum.db` | derived projection | vault (`index build`, drop+recreate) | never authoritative |
| composer resume manifest | durable projection | vault (`Manifest.rebuild_from_vault`) | never authoritative |
| DKS `warrant_history.jsonl`, `schema_events.jsonl` | append-only logs (in `runs/`, outside vault + package) | — (log, not state) | event history |

The resume manifest is the subtle one: `composer/manifest.py` states **IDENT-2** directly — *the manifest is a rebuildable projection, never authoritative*; `Manifest.rebuild_from_vault` *reconstructs done-status purely from which target note files exist on disk, so a lost/corrupt manifest is always recoverable from the vault*. The DKS logs are event-sourced: `dks/persistence.py`'s `WarrantHistory` is *log, not state* — the current warrant set lives in the registry; the log records how it got there. Schema growth is likewise event-sourced (see §4).

### 2.4 Composer v4 pipeline at a glance

`tessellum composer compile <skill>` runs `composer/compiler.py:compile` — **zero LLM calls, pure logic** (docstring): load canonical+sidecar, validate contract integrity against `contracts.MATERIALIZER_CONTRACTS`, topo-sort by `depends_on`, detect cycles + forward references, extract each step's prompt text, and emit a `CompiledPipeline` (serialisable via `to_dag_json`). Then execution:

```
 compile ─► schedule ─► gate ─► fix ─► observe
 (compiler) (scheduler) (gates) (fix)  (manifest / eval / signoff)
```

- **compile** — `compiler.py`: skill → typed DAG, no dispatch.
- **schedule** — `scheduler.py`: `run_pipeline` (serial reference) or `run_pipeline_dynamic` (wave-parallel). Each unit is one `executor.py:execute_step` (resolve `{{leaf.X}}`/`{{upstream.Y}}`/`{{retry.X}}` placeholders → dispatch backend under a watchdog → validate response schema → hand to a materializer). Retry budgets (logic/crash split) live here.
- **gate** — `gates.py`: one `Gate` abstraction at three scopes (plan / session / wave). Gates are **pure programs** and *never call an LLM* (IDENT-3); the one semantic check consumes a verifier's already-produced verdict.
- **fix** — `fix.py`: informed, non-regressive close-gate repair — checkpoints the note's bytes before each fix and keeps the best-scoring snapshot; the fixer *callable* is where any LLM lives, injected by the caller.
- **observe** — durable bookkeeping and judgement: `manifest.py` (per-leaf resume), `eval.py` (structural assertions + a 6-dim LLMJudge rubric), `signoff.py` (cheapest-first plan→execute approval ladder), `credential_pool.py` (key rotation + run budgets).

### 2.5 DKS engine at a glance

`dks/core.py:DKSCycle.run` drives a closed 7-component loop through an `LLMBackend`, each cycle depositing a Folgezettel subtree into the substrate: **observation → N sibling arguments → disagreement (edges) → counter → pattern → revised warrant(s)**. `DKSRunner` orchestrates multi-cycle sessions, threading warrant changes between cycles. Two additive extensions:

- **Confidence gating** (`dks/confidence.py`): above threshold the cycle short-circuits to *observation + one argument* (skips steps 3–7, saving 6 of 7 backend round-trips); at or below, the full closed loop runs.
- **Dung argumentation** (`dks/dung.py`): when N>2 perspectives produce a graph of `contradicts` edges, `grounded_labelling` decides survivors via Dung's grounded semantics. For N=2 it *collapses to the existing single-edge outcome* — additive, not a replacement.

`dks/fsm.py` is a generic walker over `BB_SCHEMA` (the FSM ⟨Q,Σ,δ,q₀,F⟩ from the design trail) — an alternative dispatcher that leaves `DKSCycle.run` unchanged.

## 3. Key modules + abstractions

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
| `retrieval/{metadata,graph,bm25,dense,hybrid}.py` | The five retrieval surfaces (see §5). `router.py` = heuristic query→surface classifier. |
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
| `mcp/server.py` | `build_server` / `run_stdio` — 7 tools over stdio (see §5). |
| `composer-ts/src/{bridge,dag}.ts` | TS control-flow bridge: shells the composer CLI (`bridge.ts`) + pure DAG-walk helpers (`dag.ts`). Zero contract logic. |

## 4. Invariants / design decisions + WHY

The composer names its load-bearing invariants **IDENT-2..5** in module docstrings (IDENT-2 vault-is-truth manifest rebuild, IDENT-3 gates-are-pure-programs, IDENT-4 serial-default-byte-identical, IDENT-5 fail-closed manifest load). They are the spine of the whole system, not just the composer.

- **Compile-before-dispatch.** The compiler is *pure logic, zero LLM calls* (`compiler.py`); the DAG, contracts, and cycle/forward-reference checks are all resolved *before* any model is invoked. **Why:** a structurally-broken pipeline must fail deterministically and cheaply, not halfway through a paid wave. `signoff.py` extends this — a program gate rejects a structurally-broken plan outright before spending an agent.
- **Serial default is byte-identical (IDENT-4); v4 dynamic is opt-in.** `run_pipeline` is the reference path. `run_pipeline_dynamic` is *semantically byte-identical — same vault output, same per-leaf outcomes, same ordered `RunResult`* — but runs ready steps concurrently. It is reached only via `tessellum composer run --dynamic` (`cli/composer.py`): *the serial `run_pipeline` stays the default and is byte-identical*. The additive concurrency wrapper in `executor.py` likewise *keeps the serial path byte-identical (IDENT-4)* when its flag is off. **Why:** parallelism is a throughput optimisation that must never change results; the serial path stays the ground truth to diff against.
- **Gates are pure programs, never call an LLM (IDENT-3).** Every `Gate` in `gates.py` is program logic; the sole semantic check *consumes a verifier's already-produced typed verdict — it does not itself invoke a model*. The same rule is asserted across `fix.py`, `planning.py`, `credential_pool.py`, `context_assembler.py`, and `signoff.py` (*the program orchestrates; the agent/human produce the verdicts*). **Why:** gates are the transaction commit-check; a gate that could hallucinate PASS is worthless. Keeping decisions in deterministic code makes them auditable and testable.
- **Vault is source of truth (IDENT-2).** The DB and the resume manifest are rebuildable projections. **Why:** a lost/corrupt DB or manifest is always recoverable by re-reading the vault; there is no second authority to reconcile.
- **Fail-closed (IDENT-5).** A gate that cannot *prove* PASS is a FAIL — an unverifiable source (`auth_blocked`) is a FAIL, never a plausibility pass (`gates.py`); a corrupt manifest falls back to the newest good `.bak` or starts empty *with a logged warning* (`manifest.py`); an empty/None backend outcome is treated as a crash (`executor.py`). **Why:** silent success on unproven state corrupts the substrate; refusing is always safe.
- **Schema is closed, finite, versioned, and event-sourced.** `BB_SCHEMA` = `BB_SCHEMA_EPISTEMIC` (8) + `BB_SCHEMA_NAVIGATION` (7) + `BB_SCHEMA_DKS_EXTENSIONS` (1) + `BB_SCHEMA_USER_EXTENSIONS` (0+) — ~16 typed edges over 8 BB types. User extensions are the fold over an **append-only** `SchemaEditEvent` log; retractions are first-class events and the log is never rewritten. `BB_SCHEMA_VERSION` bumps on each landed `added`/`retracted` event, and `BB_SCHEMA_AT_VERSION(n)` reconstructs the schema as of any version so a note validates against its own recorded `bb_schema_version` (frozen-at-creation). **Why:** the ontology must be able to grow under discipline without invalidating history — corpus edges typed under an old schema stay interpretable.

## 5. Public API / CLI

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

## 6. Extension points

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
