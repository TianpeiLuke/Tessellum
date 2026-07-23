# Retrieval (`tessellum.retrieval`)

## Purpose

`tessellum.retrieval` is **System D's read surface**: a set of stateless functions that take a DB path plus a query and return ranked hits, reading only the SQLite index built by `tessellum.indexer.build` (`src/tessellum/retrieval/__init__.py`). It never touches the markdown vault (System P) and holds no state between calls beyond one process-level embedding-model singleton.

## Architecture / data flow

The vault (System P) is compiled by the indexer into a single SQLite DB with two base tables (`notes`, `note_links`) and two virtual tables (`notes_fts` for FTS5 lexical search, `notes_vec` for sqlite-vec dense search) — see `src/tessellum/indexer/schema.sql`. Retrieval is a thin, read-only layer over those tables:

```
query ──▶ [ bm25 | dense | hybrid | bfs | metadata ] ──▶ list[*Hit]
              │       │        │        │        │
          notes_fts notes_vec  ├─(fuses bm25+dense via RRF)
                               note_links (NetworkX DiGraph)
                                          notes (SQL AND filters)
```

Every surface is `db_path in → hits out`. Each opens its own short-lived `sqlite3` connection, runs one query (BFS loads the whole graph once), closes it in a `finally`, and returns a list of frozen dataclass hits. All hits carry a `score` field with the uniform convention **higher = better**, even though the underlying SQLite primitives use lower-is-better conventions that the code deliberately flips (see Invariants).

Two entry points into this layer exist at the CLI level: `tessellum search` (the four content strategies) and `tessellum filter` (metadata). The heuristic `router` module reproduces the strategy-selection logic as a Python function but is **not wired into either CLI command** (see Public API / CLI).

## Key modules + abstractions

| File | Role |
| --- | --- |
| `retrieval/__init__.py` | Public re-exports of the five search functions, their `*Hit` dataclasses, and the router symbols (`classify_query`, `route`, `RouterDecision`, `Strategy`). |
| `retrieval/bm25.py` | `bm25_search` — FTS5 lexical retrieval over `notes_fts`; returns `BM25Hit`. Negates SQLite `bm25()` so `score` is higher-is-better; optional `snippet()` highlighting with `<<<term>>>` markers. |
| `retrieval/dense.py` | `dense_search` — semantic retrieval over `notes_vec` (sqlite-vec `vec0`). Encodes the query with a module-level `all-MiniLM-L6-v2` singleton; `DenseHit.score = 1 - distance`. |
| `retrieval/hybrid.py` | `hybrid_search` — Reciprocal Rank Fusion of `bm25_search` + `dense_search`. `DEFAULT_RRF_K1 = 60`. **Production default.** Falls back to BM25-only if dense is unavailable. |
| `retrieval/graph.py` | `best_first_bfs` — best-first BFS over a NetworkX `DiGraph` loaded from `note_links`. Undirected traversal, directed in-degree as a hub signal, `DEFAULT_HUB_THRESHOLD = 50`. **No PageRank.** |
| `retrieval/metadata.py` | `metadata_search` — pure-SQL AND-combined filters on the structured YAML columns of `notes`. JSON-array fields matched via `json_each`. |
| `retrieval/router.py` | Heuristic `classify_query` / `route` — regex/structural cues → one of five strategies. **Not wired into the CLI.** |

### The five surfaces in detail

**`bm25_search(db_path, query, *, k=20, snippet_length=30)` (`bm25.py:54`)** — Runs `WHERE notes_fts MATCH ? ORDER BY bm25(notes_fts) LIMIT ?`. The `query` string is passed straight to FTS5's `MATCH` operator, so prefix (`foo*`), phrase (`"exact phrase"`), boolean (`AND`/`OR`/`NOT`), and column filters (`note_name:term`) all work; malformed syntax surfaces as `sqlite3.OperationalError`. The SQL `ORDER BY bm25(...)` (un-negated) does the ranking; the SELECT projects `-bm25(notes_fts) AS score` purely to flip the displayed sign. `snippet_length=None` skips `snippet()` generation entirely.

**`dense_search(db_path, query, *, k=20)` (`dense.py:69`)** — Lazily loads the sentence-transformers encoder via the module-level `_ENCODER` singleton (`_get_encoder`, `dense.py:35`), encodes the query with `normalize_embeddings=True`, packs it to a float32 blob (`_vec_blob`, `dense.py:46`), and runs sqlite-vec's KNN: `WHERE v.embedding MATCH ? AND k = ? ORDER BY v.distance`, joining `notes_vec` to `notes` on the `note_int_id` surrogate key. `EMBEDDING_DIM = 384`, `EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"`. `DenseHit` exposes both raw `distance` (lower = closer) and `score = 1 - distance`.

**`hybrid_search(db_path, query, *, k=20, k1=60, per_strategy_k=None)` (`hybrid.py:69`)** — Calls `bm25_search` and `dense_search` **sequentially in Python** (fetching `per_strategy_k`, default `max(2*k, 20)`, from each), then fuses by summing `1 / (k1 + rank)` per note across rankers (Cormack–Clarke–Buettcher 2009 RRF). `DEFAULT_RRF_K1 = 60`. It captures per-ranker ranks (`bm25_rank`, `dense_rank`) as diagnostics on `HybridHit`, sorts by descending score with `note_id` as a deterministic tiebreaker, and returns the top `k`. If dense raises (e.g. an index built `--no-dense`), it catches the exception and **falls back to BM25-only fusion** rather than failing the query (`hybrid.py:114`). The module docstring notes a single-SQL fusion was deliberately avoided in favor of reuse/readability.

**`best_first_bfs(db_path, seed, *, k=20, max_depth=3, hub_threshold=50)` (`graph.py:62`)** — `_load_graph` (`graph.py:161`) builds a NetworkX `DiGraph` from `SELECT note_id, note_name FROM notes` (nodes) and `SELECT source_note_id, target_note_id FROM note_links` (edges). Traversal walks the **undirected** view (`to_undirected(as_view=True)`) because a link conceptually relates both endpoints, but uses the **directed** in-degree as the hub signal. The priority queue is keyed `(depth * 1000) + in_degree` — depth-major so each depth ring is exhausted before going deeper, in-degree-minor so less-popular (more-specific) notes surface first among ties. Nodes whose directed in-degree exceeds `hub_threshold` (default 50) are returned as hits but **not expanded** (hub-skip), preventing "everything connects to everything" blowup; the seed always expands. `GraphHit.score = 1 / (1 + depth)` and each hit carries its full `path` from the seed. The `seed` argument is a `note_id`, not free text; a seed absent from the graph returns `[]`.

**`metadata_search(db_path, *, building_block, status, category, second_category, tag, keyword, topic, date_after, date_before, folgezettel_prefix, has_folgezettel, k=100)` (`metadata.py:54`)** — The simplest surface: builds a parameterized `WHERE` clause from whichever filters are non-`None`, **all AND-combined**, and orders by `note_id` for deterministic output. Closed-enum/scalar fields (`building_block`, `note_status`, `note_category`, `note_second_category`, `note_creation_date` range) use `= ?` / `>=` / `<=`; `folgezettel_prefix` uses `LIKE '<prefix>%'`; `has_folgezettel` maps to `folgezettel IS [NOT] NULL`. The three JSON-array fields (`tags`, `keywords`, `topics`) are matched with `EXISTS (SELECT 1 FROM json_each(notes.<col>) WHERE value = ?)` to get exact-value semantics and avoid `LIKE` false positives (e.g. `cqr` matching `cqrs`) — `metadata.py:146`.

## Invariants / design decisions + WHY

- **Uniform `score` convention: higher = better, everywhere.** SQLite primitives disagree (`bm25()` is lower-is-better; sqlite-vec returns lower-is-better `distance`). `bm25_search` negates the score in the SELECT projection while still `ORDER BY bm25()` un-negated for correct ranking (`bm25.py:100–104`); `dense_search` returns `1 - distance` (`dense.py:130`); `hybrid`/`graph` scores are naturally higher-is-better. WHY: callers and CLI output can compare and sort hits from any strategy without knowing the underlying sign.
- **Stateless, DB-path-in / hits-out.** Each function opens and closes its own connection; the only cross-call state is the `_ENCODER` singleton, which is a pure process-level cache (`dense.py:32`). WHY: functions compose freely (hybrid literally calls two of them), are trivially testable, and the layer holds no locks or long-lived handles.
- **Frozen dataclass hits.** `BM25Hit`, `DenseHit`, `HybridHit`, `GraphHit`, `MetadataHit` are all `@dataclass(frozen=True)`. WHY: results are immutable value objects safe to pass around and cache.
- **RRF over score-normalization for fusion.** Hybrid fuses on *ranks*, not raw scores. WHY: BM25 and cosine scores live on incomparable scales; ranks are scale-free, and RRF (`k1=60`) is the standard robust default. Absolute RRF magnitudes are tiny (~0.01–0.03) — only the ordering is meaningful (`hybrid.py:48`).
- **Hybrid degrades, never fails.** A dense failure is swallowed and the query returns BM25-only results (`hybrid.py:114`). WHY: a `--no-dense` index or a missing embedding extension should still answer queries.
- **BFS: undirected traversal, directed hub signal.** Deliberate asymmetry — reachability is bidirectional (conceptual relatedness) but "popularity" is inbound-link count (`graph.py:110–114`). WHY: hubs are defined by how many notes point *at* them; skipping their expansion keeps results focused and bounded.
- **`json_each` for array fields, not `LIKE`.** WHY: exact-value membership without substring false positives. Relies on SQLite's JSON1 (bundled/enabled since 3.38; Python's SQLite is new enough — `metadata.py:23`).
- **NO PageRank / Personalized PageRank anywhere in this layer.** This is a load-bearing design decision, stated explicitly: the empirical Hit@K↔answer-quality correlation measured ρ=0.37, so PPR's expensive multi-hop walks optimize a retrieval metric that does not translate into better answers; best-first BFS is chosen as simpler, faster, and Pareto-optimal (`graph.py:1–7`, `__init__.py:24–28`). **Ground-truth caveat on the schema:** in the shipped 1.0 `notes` schema, `static_ppr_score` is *not even a column* — it is *not even a shipped column* (the `schema.sql:7–10` header notes the parent-project columns dropped, incl. `static_ppr_score`), so there is neither a PPR column nor an index on one, and no strategy references it. (By contrast `note_int_id` IS a real, shipped surrogate-key column — the join key `dense_search` uses.) (Note: the top-level `tessellum.__init__` module docstring lists "ppr" in a strategy enumeration; that is stale doc text — there is no `ppr` function, CLI flag, or column.)

## Public API / CLI

**Python API** (re-exported from `tessellum.retrieval`, `__init__.py:34–56`):

```python
from tessellum.retrieval import (
    bm25_search, BM25Hit,
    dense_search, DenseHit,
    hybrid_search, HybridHit,
    best_first_bfs, GraphHit,
    metadata_search, MetadataHit,
    classify_query, route, RouterDecision, Strategy,
)
```

**CLI split** — the content strategies and metadata filtering are two separate top-level commands (registered in `cli/main.py:42–43`):

- **`tessellum search <query>`** (`cli/search.py`) — mutually-exclusive strategy flags `--bm25` / `--dense` / `--hybrid` / `--bfs`, defaulting to `--hybrid` (`search.py:118`). Shared options: `--db` (default `./data/tessellum.db`), `--k` (default 20), `--format {human,json}`. `--depth` and `--hub-threshold` apply to `--bfs` only; `--no-snippet` applies to `--bm25` only. For `--bfs` the positional `query` is interpreted as a **seed note_id**, not free text. Exit code `0` on a run that produced (possibly empty) results, `2` on invocation error (missing DB, `sqlite3.OperationalError`).
- **`tessellum filter [...]`** (`cli/filter.py`) — metadata-only, wrapping `metadata_search`. Flags: `--building-block`, `--status`, `--category`, `--second-category`, `--tag`, `--keyword`, `--topic`, `--date-after`, `--date-before`, `--folgezettel-prefix`, and mutually-exclusive `--has-folgezettel` / `--no-folgezettel`; plus `--db`, `--k` (default 100), `--format`. All filters AND-combine; no filters lists every note up to `--k`.

Both commands support `--format json` for machine consumption; the JSON payload includes strategy/filter provenance and per-hit diagnostics (BM25 `snippet`, dense `distance`, hybrid `bm25_rank`/`dense_rank`, BFS `depth`/`path`).

**The router is NOT wired into the CLI.** `classify_query` / `route` (`router.py`) provide the same five-way strategy selection as a pure Python function (regex for `.md` seed paths → BFS, single-token identifiers → BM25, question-shaped/multi-word → hybrid, else hybrid). It exists for non-agent programmatic callers (CI scripts, ablation tests, "the agent runtime once Composer ships", per `router.py:1–8`) and mirrors the `skill_tessellum_search_notes` decision tree. No CLI command imports it — `main.py` wires `search` and `filter` directly to the primitives, and grepping the source confirms `classify_query`/`route` are imported nowhere outside `retrieval/__init__.py`. Note also that `route` never selects `metadata` for free-text input; `metadata` is kept in the return-type union for completeness but is invoked only when a caller already holds structured filters (`router.py:130–135`).

## Extension points

- **Add a strategy.** Write `retrieval/<name>.py` exposing `<name>_search(db_path, query, *, k=...) -> list[<Name>Hit]` with a frozen `*Hit` dataclass carrying a higher-is-better `score`; re-export it from `__init__.py`; add a `--<name>` const to the mutually-exclusive group and a branch in `run_search` (`cli/search.py:50–79`, `133–150`). Follow the existing DB-path-in / connect-in-`try` / close-in-`finally` contract.
- **Tune RRF.** `hybrid_search` accepts `k1` (default `DEFAULT_RRF_K1 = 60`) and `per_strategy_k`; add more rankers to the fusion by extending the two `for rank, hit in enumerate(...)` accumulation loops (`hybrid.py:130–138`).
- **Swap the embedding model.** Change `EMBEDDING_MODEL_NAME` / `EMBEDDING_DIM` in `dense.py` (must match the model used at index time by `tessellum.indexer.build`); the `_ENCODER` singleton loads whatever is named.
- **Extend metadata filters.** Add a keyword-only arg to `metadata_search`, append a `WHERE` clause + param (scalar `= ?` or `json_each` `EXISTS` for array fields), and surface a matching `--flag` in `cli/filter.py`.
- **Tune graph traversal.** `best_first_bfs` exposes `max_depth` and `hub_threshold` (`DEFAULT_HUB_THRESHOLD = 50`); the priority function (`(depth * 1000) + in_degree`) is the seam for alternative orderings (`graph.py:116–156`).
- **Wire the router (deferred).** `route` is ready to back an agent runtime or a "smart" default CLI mode; it is currently unreferenced by any command and would need an explicit `add_subparser` / dispatch to become user-facing.
