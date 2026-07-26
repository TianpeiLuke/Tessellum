# `tessellum.retrieval` — Reference

API, symbols, and signatures for the read layer. For the mental model and how work flows through it, see [../retrieval.md](../retrieval.md).

## File → role

| File | Role |
|------|------|
| `bm25.py` | Lexical retrieval over the `notes_fts` FTS5 table. `BM25Hit` + `bm25_search`. Negates SQLite's `bm25()` (lower-is-better) for the public score; generates snippets with `<<<term>>>` markers via `snippet()`. |
| `dense.py` | Semantic retrieval over the `notes_vec` sqlite-vec table. `DenseHit` + `dense_search`. Lazy process-level encoder singleton (`_get_encoder`); score is `1 - distance`. |
| `hybrid.py` | Reciprocal Rank Fusion of BM25 + dense. `HybridHit` + `hybrid_search`. Pure Python fusion — calls `bm25_search` and `dense_search`, sums `1/(k1+rank)`. Swallows a dense-side exception and falls back to BM25-only. |
| `graph.py` | Best-first BFS over the `note_links` graph. `GraphHit` + `best_first_bfs`. Builds a NetworkX `DiGraph` (`_load_graph`), traverses the undirected view, uses directed in-degree as the hub signal, hub-skips popular nodes. |
| `metadata.py` | Structured metadata filtering via direct SQL on `notes` columns. `MetadataHit` + `metadata_search`. AND-combines filters; JSON-array fields matched via `json_each`. |
| `router.py` | Heuristic query classifier + dispatcher. `Strategy`, `RouterDecision`, `classify_query`, `route`. First live caller: composer per-note related-notes enrichment (still no CLI command uses it). |
| `__init__.py` | Public surface: re-exports every hit type, search function, and the router symbols; its docstring records the deliberate no-PageRank decision. |

## Public API — `tessellum.retrieval`

### BM25 (`bm25.py`)

- `bm25_search(db_path: Path | str, query: str, *, k: int = 20, snippet_length: int | None = 30) -> list[BM25Hit]` — rank notes by FTS5 MATCH against `query`; ordered by descending relevance. `snippet_length=None` skips snippet generation. Returns `[]` for `k <= 0`.
- `BM25Hit` — `@dataclass(frozen=True)`: `note_id: str`, `note_name: str`, `score: float` (higher = better; internally the negated `bm25()`), `snippet: str | None = None`.

### Dense (`dense.py`)

- `dense_search(db_path: Path | str, query: str, *, k: int = 20) -> list[DenseHit]` — encode `query`, rank by cosine similarity over `notes_vec`; ordered by ascending distance. Returns `[]` for `k <= 0`.
- `DenseHit` — `@dataclass(frozen=True)`: `note_id: str`, `note_name: str`, `distance: float` (cosine distance, lower = closer), `score: float` (`1 - distance`, higher = better).

### Hybrid (`hybrid.py`)

- `hybrid_search(db_path: Path | str, query: str, *, dense_query: str | None = None, k: int = 20, k1: int = 60, per_strategy_k: int | None = None) -> list[HybridHit]` — RRF fusion of BM25 + dense; ordered by descending RRF score, ties broken by `note_id`. `per_strategy_k` defaults to `max(2*k, 20)`. Falls back to BM25-only if dense raises. `dense_query` (default `query`) lets the embedding arm receive a natural-language query while the BM25 arm keeps an FTS5-safe token bag.
- `HybridHit` — `@dataclass(frozen=True)`: `note_id: str`, `note_name: str`, `score: float` (RRF sum, higher = better), `bm25_rank: int | None`, `dense_rank: int | None` (1-indexed ranks per ranker; `None` if absent from that ranker's top-K).

### Graph / BFS (`graph.py`)

- `best_first_bfs(db_path: Path | str, seed: str, *, k: int = 20, max_depth: int = 3, hub_threshold: int = 50) -> list[GraphHit]` — best-first traversal from `seed` (a `note_id`). Undirected walk; directed in-degree as hub signal; nodes with in-degree > `hub_threshold` are returned but not expanded; the seed always expands and is excluded from results. Returns `[]` for `k <= 0`, `max_depth <= 0`, or a `seed` not in the graph.
- `GraphHit` — `@dataclass(frozen=True)`: `note_id: str`, `note_name: str`, `score: float` (`1/(1+depth)`, higher = closer), `depth: int` (hops from seed), `path: tuple[str, ...]` (seed → hit inclusive; `len(path) == depth + 1`).

### Metadata (`metadata.py`)

- `metadata_search(db_path: Path | str, *, building_block=None, status=None, category=None, second_category=None, tag=None, keyword=None, topic=None, date_after=None, date_before=None, folgezettel_prefix=None, has_folgezettel=None, k=100) -> list[MetadataHit]` — filter `notes` by structured fields; all filters AND-combine; ordered by `note_id`. No filters lists every note up to `k`. Returns `[]` for `k <= 0`.
- `MetadataHit` — `@dataclass(frozen=True)`: `note_id`, `note_name`, `note_category`, `note_second_category`, `note_status`, `building_block`, `note_creation_date`, `folgezettel` (all `str | None` except the ids).

### Router (`router.py`)

- `classify_query(query: str) -> RouterDecision` — pure function, no DB access; maps a query to a strategy + reason.
- `route(db_path: Path | str, query: str, *, k: int = 20, dense_query: str | None = None) -> tuple[RouterDecision, list[...]]` — classify then dispatch to the chosen surface; returns `(decision, hits)`. `dense_query` is forwarded to the dense/hybrid arms.
- `RouterDecision` — `@dataclass(frozen=True)`: `strategy: Strategy`, `reason: str`.
- `Strategy` — `Literal["metadata", "bfs", "bm25", "dense", "hybrid"]`.

## Metadata filter fields

| Arg | Column / source | Match |
|-----|-----------------|-------|
| `building_block` | `building_block` | exact (closed BB enum) |
| `status` | `note_status` | exact (closed status enum) |
| `category` | `note_category` (`tags[0]`, PARA bucket) | exact |
| `second_category` | `note_second_category` (`tags[1]`) | exact |
| `tag` | `tags[]` JSON array | any-of (`json_each`, exact value) |
| `keyword` | `keywords[]` JSON array | any-of (`json_each`, exact value) |
| `topic` | `topics[]` JSON array | any-of (`json_each`, exact value) |
| `date_after` | `note_creation_date` | `>=` (`YYYY-MM-DD`) |
| `date_before` | `note_creation_date` | `<=` (`YYYY-MM-DD`) |
| `folgezettel_prefix` | `folgezettel` | `LIKE 'prefix%'` string-prefix |
| `has_folgezettel` | `folgezettel` | `True` → not null; `False` → null; `None` → ignore |

## Router decision rules (`classify_query`)

| Order | Cue | Strategy |
|-------|-----|----------|
| 1 | empty query | `hybrid` |
| 2 | matches `^[a-z0-9_/\-]+\.md$` and contains `/` | `bfs` |
| 3 | matches `^[a-z0-9_\-]{1,30}$` (single token) | `bm25` |
| 4 | ends with `?` or ≥ 4 words | `hybrid` |
| 5 | otherwise | `hybrid` |

`route` dispatches on this decision. It never returns `dense` (no cue selects it) and never picks `metadata` for free text (the branch exists only so the return-type union documents all five surfaces).

## Constants / defaults

| Symbol | Module | Value |
|--------|--------|-------|
| `EMBEDDING_DIM` | `dense.py` | `384` |
| `EMBEDDING_MODEL_NAME` | `dense.py` | `sentence-transformers/all-MiniLM-L6-v2` |
| `DEFAULT_RRF_K1` | `hybrid.py` | `60` |
| `DEFAULT_HUB_THRESHOLD` | `graph.py` | `50` |
| default `k` | bm25 / dense / hybrid / bfs | `20` |
| default `k` | metadata | `100` |
| default `max_depth` | bfs | `3` |
| default `snippet_length` | bm25 | `30` |

## Errors

- `FileNotFoundError` — `db_path` does not exist. Raised by every surface.
- `sqlite3.OperationalError` — required table missing (`notes_fts`, `notes_vec`, `notes`, `note_links`), or malformed FTS5 query syntax (bm25 / hybrid). `hybrid_search` catches the dense-side error and continues BM25-only.

## CLI

Two commands split along the content / metadata seam, registered in `cli/main.py`.

### `tessellum search <query>` — content retrieval (`cli/search.py`)

```
tessellum search <query> [--hybrid|--bm25|--dense|--bfs] [--db PATH] [--k N]
                         [--depth N] [--hub-threshold N] [--no-snippet]
                         [--format human|json]
```

| Flag | Effect |
|------|--------|
| `<query>` | FTS5 MATCH for `--bm25`; natural language for hybrid / `--dense`; vault-relative `note_id` seed for `--bfs`. |
| `--hybrid` / `--bm25` / `--dense` / `--bfs` | Mutually exclusive strategy select. Default `--hybrid`. |
| `--db PATH` | Index DB (default `./data/tessellum.db`). |
| `--k N` | Max results (default 20). |
| `--depth N` | BFS only — max hops from seed (default 3). |
| `--hub-threshold N` | BFS only — in-degree above which a node is not expanded (default 50). |
| `--no-snippet` | BM25 only — skip snippet generation. |
| `--format human\|json` | Output format (default human). |

Exit codes: `0` ran (results may be empty); `2` invocation error (DB missing, `FileNotFoundError`, or malformed-query `sqlite3.OperationalError`).

### `tessellum filter` — metadata retrieval (`cli/filter.py`)

```
tessellum filter [--building-block X] [--status X] [--category X] [--second-category X]
                 [--tag X] [--keyword X] [--topic X]
                 [--date-after YYYY-MM-DD] [--date-before YYYY-MM-DD]
                 [--folgezettel-prefix X] [--has-folgezettel|--no-folgezettel]
                 [--db PATH] [--k N] [--format human|json]
```

Each flag maps to the matching `metadata_search` argument. `--has-folgezettel` / `--no-folgezettel` are mutually exclusive (`True` / `False`; default `None`). All filters AND-combine; no filters lists every note up to `--k` (default 100). Exit codes: `0` ran; `2` invocation error (DB missing).
