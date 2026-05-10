# Changelog

All notable changes to Tessellum are documented here. The format is loosely [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v0.1.0 — Public Beta

- Engine port from parent project (composer + retrieval primitives)
- 20 essential skills (capture / search / answer / trail management / maintenance)
- 8 BB-type example notes (one per Building Block)
- Conceptual primer term notes (Z + PARA + BB + Epistemic Function + DKS + CQRS)
- Public-facing how-to library (getting-started, note-format, agent-integration, growing a trail)
- MCP server exposing v0.1 skills as tools
- CI workflow (ruff + pytest + format/link validators)
- `tessellum init` / `capture` / `format check` / `search` CLI subcommands
- Hatch `force-include` wiring so `vault/resources/templates/` ships in the wheel

## [0.0.14] — 2026-05-10

### Added — Retrieval Wave 2: Dense + sqlite-vec

`tessellum search --dense <query>` ships. Per `plans/plan_retrieval_port.md` Wave 2. Both lexical (BM25) and semantic (dense) retrieval are now available; Wave 3 (v0.0.15) will combine them via Reciprocal Rank Fusion as the production default.

```bash
tessellum search "knowledge graph" --bm25
# BM25 matches by lexical overlap — finds "knowledge" + "graph" tokens.

tessellum search "knowledge graph" --dense
# DENSE matches by semantic similarity — finds notes about knowledge
# organization, building-block ontologies, dialectic systems.
```

The two strategies retrieve different ranked sets — exactly the diversity that hybrid RRF in Wave 3 will exploit (parent project: +12pp Hit@5 lift over best single strategy, per FZ 5e1c3a1a1).

#### Schema extension — `notes_vec` virtual table + `note_int_id`

`src/tessellum/indexer/schema.sql`:

```sql
-- notes table gains a surrogate key for the join:
note_int_id INTEGER UNIQUE
CREATE INDEX idx_notes_int_id ON notes(note_int_id);

-- New virtual table:
CREATE VIRTUAL TABLE notes_vec USING vec0(
    note_int_id INTEGER PRIMARY KEY,
    embedding   FLOAT[384] distance_metric=cosine
);
```

**`distance_metric=cosine`** is critical. sqlite-vec defaults to L2 (Euclidean), which gives correct ranking for normalized embeddings but yields scores in `[0, 2]` that don't map cleanly to "1 = identical, 0 = orthogonal". Cosine distance gives `[0, 2]` too but for normalized vectors `score = 1 - distance` IS exactly cosine similarity ∈ `[-1, 1]`. Users see meaningful scores like `0.487` (moderate semantic match) instead of `-0.013` (which was actually `1 - L2_distance` for distance ≈ 1).

**Schema migration**: existing v0.0.13 DBs lack `notes_vec` and the `note_int_id` column. Users re-run `tessellum index build --force` to rebuild.

#### Build pipeline — embedding generation

`src/tessellum/indexer/build.py`:

- Allocates sequential `note_int_id` (1, 2, 3, ...) per note as the join key for `notes_vec`.
- Lazy-loads `sentence-transformers/all-MiniLM-L6-v2` via a module-level singleton — `~1.5s` first-call cost; in-process re-builds are fast.
- Encodes each note's text (`note_name + keywords + topics + tags + body`, joined by `\n`) with `normalize_embeddings=True` so cosine distance behaves predictably.
- Writes embeddings to `notes_vec` as packed little-endian float32 blobs.
- New `with_dense: bool = True` parameter on `build()`. Pass `False` to skip embedding generation entirely (faster builds when only BM25 is needed).
- New `--no-dense` CLI flag on `tessellum index build`.
- `BuildResult.embeddings_generated` reports the count.

End-to-end on the real Tessellum vault: 5.8s build (71 notes, 71 embeddings, 547 links) on a warm sentence-transformers cache; ~20s on a cold cache.

#### `tessellum.retrieval.dense_search`

`src/tessellum/retrieval/dense.py`:

```python
from tessellum.retrieval import dense_search, DenseHit

hits = dense_search("data/tessellum.db", "knowledge graph", k=5)
# [DenseHit(note_id=..., note_name=..., distance=0.513, score=0.487), ...]
```

`DenseHit` has both `score` (cosine similarity, `1 - distance`, "higher = more similar") and `distance` (raw cosine distance, "lower = closer"). Both fields are useful: `score` mirrors `BM25Hit.score`'s convention; `distance` is what the SQL actually returns.

Lazy-loads the encoder via the same module-level singleton pattern as `build`. First query in a process loads the model; subsequent queries are fast.

#### `tessellum search` CLI gains `--dense`

```bash
tessellum search <query>           # BM25 (Wave 1 default; Wave 3 flips to hybrid)
tessellum search --bm25 <query>    # explicit BM25
tessellum search --dense <query>   # dense semantic
```

`--bm25` and `--dense` are mutually exclusive (argparse `add_mutually_exclusive_group`). JSON output for dense includes both `score` and `distance` fields.

#### Tests

17 new tests, all passing. **265 total** (248 prior + 17 new).

- `tests/smoke/test_retrieval_dense.py` (14 tests): typed return, semantic ranking (graph query → graph note ranks higher than cooking note; cooking query inverts), score in `[-1, 1]`, distance in `[0, 2]`, scores descend / distance ascends, `k` flag, `k=0` → empty, missing DB → FileNotFoundError, `--no-dense` build → empty dense results (not error), `with_dense=True/False` toggles correctly, integration test against real vault.
- `tests/cli/test_search_cli.py` (3 new): `--dense` flag uses dense strategy + DENSE-labeled output; `--dense --format json` includes `distance` field; `--bm25 --dense` is mutually exclusive (raises SystemExit).

Per-test runtime is dominated by the embedding model load (~1.5s once); module-scoped fixture builds the test DB once.

#### End-to-end smoke on real vault

```
$ tessellum search "knowledge graph" --bm25 --k 3
BM25 matches for 'knowledge graph'  (3 hits)
  1. term_slipbox  (0.056)
      ...<<<Knowledge>>> <<<Graph>>>...
  2. term_zettelkasten  (0.055)
  3. term_information_retrieval  (0.053)

$ tessellum search "knowledge graph" --dense --k 3
DENSE matches for 'knowledge graph'  (3 hits)
  1. thought_building_block_ontology_relationships  (0.487)
  2. term_dialectic_knowledge_system  (0.383)
  3. term_para_method  (0.371)
```

The two strategies return DIFFERENT ranked sets — BM25 finds tokens; dense finds concepts. Wave 3's hybrid RRF will exploit this diversity for the +12pp lift.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.14"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.14"`.
- 265/265 tests pass (248 prior + 17 new).

### What's NOT in this release (Waves 3-5)

- **Wave 3 (v0.0.15)** — Hybrid RRF (the production winner). One SQL `UNION ALL` of BM25 + dense top-K, ranked by `1/(rank + k1)` summed across both. Becomes the default `tessellum search <query>`.
- **Wave 4 (v0.0.16)** — Best-first BFS graph traversal. **No PPR** per FZ 5e2b1c.
- **Wave 5 (v0.0.17)** — Skill orchestration: `skill_tessellum_search_notes` + `skill_tessellum_answer_query` canonicals.

## [0.0.13] — 2026-05-10

### Added — Retrieval Wave 1: BM25 + FTS5

`tessellum search <query>` ships. **The first user-facing query capability** — System D is no longer empty. Per `plans/plan_retrieval_port.md` Wave 1.

```bash
tessellum index build  # populates notes_fts alongside notes + note_links
tessellum search composer
# BM25 matches for 'composer'  (5 hits)
#   1. term_dspy  (2.931)
#       resources/term_dictionary/term_dspy.md
#       ...modules <<<compose>>> (via a Python program)...
#   2. term_atomic_skill  (2.895)
#       ...
```

#### Schema extension — `notes_fts` virtual table

`src/tessellum/indexer/schema.sql` adds:

```sql
CREATE VIRTUAL TABLE notes_fts USING fts5(
    note_id UNINDEXED,
    note_name,
    body,
    tokenize='porter unicode61'
);
```

`UNINDEXED` on `note_id` because we use it for joins, not match. The `porter` stemmer + `unicode61` tokenizer is SQLite's standard for English text with full Unicode normalization.

`src/tessellum/indexer/build.py` populates `notes_fts` from each note's body — no extra disk read since `parse_note` already returned the body in memory.

**Schema migration**: existing `data/tessellum.db` files don't have `notes_fts`. Users re-run `tessellum index build --force` to rebuild. Per the plan: "schema migrations are destructive within v0.x."

#### `tessellum.retrieval.bm25_search`

`src/tessellum/retrieval/__init__.py` + `bm25.py`:

```python
from tessellum.retrieval import bm25_search, BM25Hit

hits = bm25_search("data/tessellum.db", "composer", k=5, snippet_length=30)
# [BM25Hit(note_id=..., note_name=..., score=2.93, snippet="...<<<compose>>>...")]
```

Three details worth knowing:

1. **Score sign**: SQLite's `bm25()` returns lower-is-better. Tessellum's API negates it so `BM25Hit.score` is "higher = more relevant" — matches how users naturally read scores. The internal `ORDER BY bm25(notes_fts)` is unchanged (still ranks correctly).
2. **Snippet generation**: SQLite's `snippet()` wraps matched terms in `<<<...>>>` markers (terminal-friendly, easy to grep). Set `snippet_length=None` to skip generation for batch queries.
3. **Query syntax**: Passed straight to FTS5's `MATCH`. Supports prefix (`foo*`), phrase (`"x y"`), boolean (`AND`/`OR`/`NOT`), and column filters (`note_name:term`). Malformed queries raise `sqlite3.OperationalError`.

#### `tessellum search <query>` CLI

`src/tessellum/cli/search.py` wired into the dispatcher.

| Flag | Default | Purpose |
|---|---|---|
| `<query>` (positional) | required | FTS5 MATCH query |
| `--bm25` | (implicit default) | Forward-compat selector for Waves 2-3 |
| `--db PATH` | `./data/tessellum.db` | Index DB path |
| `--k N` | 20 | Max results |
| `--no-snippet` | off | Skip snippet generation |
| `--format {human,json}` | human | Output format |

Exit codes: 0 success (results may be empty), 2 invocation error (DB missing, malformed query).

In v0.0.13, `tessellum search foo` and `tessellum search --bm25 foo` are equivalent — `--bm25` is reserved for Waves 2-3 when `--dense` and `--hybrid` join. Per the plan: "Wave 3 flips the default to hybrid; document in CHANGELOG."

#### CLI banner

Banner now lists 6 subcommands in usage order:

```
tessellum init <dir>                — scaffold a new vault
tessellum format check <path>       — validate notes against the YAML spec
tessellum capture <flavor> <slug>   — create a new note from a template
tessellum index build               — build the unified SQLite index
tessellum search <query>            — BM25 lexical retrieval (v0.0.13)
tessellum composer validate <skill> — validate a skill's pipeline sidecar
```

#### Tests

25 new tests, all passing. **248 total** (223 prior + 25 new).

- `tests/smoke/test_retrieval_bm25.py` (16 tests):
  - bm25_search returns typed BM25Hit list
  - Ranking: relevant terms rank higher; unique-term lookup; specific-term filter
  - Empty result for unknown query
  - Score sign: positive (negation of FTS5 convention)
  - Scores descend
  - `k` flag limits; `k=0` returns empty
  - Snippet present by default; `snippet_length=None` omits
  - Missing DB raises FileNotFoundError
  - Malformed FTS5 query raises OperationalError
  - Phrase query (`"foundational layer"`)
  - Prefix query (`supersym*`)
  - note_id + note_name shape verified
  - Integration: against the real Tessellum vault.
- `tests/cli/test_search_cli.py` (9 tests):
  - basic search → 0
  - no-match → 0 with "no matches" message
  - missing DB → 2 with stderr message
  - malformed query → 2
  - `--k` limits (verified via `--format json`)
  - JSON output structure (query, strategy, hit_count, hits[*])
  - `--no-snippet` flag omits snippets
  - `--bm25` flag accepted (forward-compat)
  - banner mentions search.

#### End-to-end smoke

```bash
$ tessellum index build --vault vault --db /tmp/test.db
built index at: /tmp/test.db
  notes indexed:  71
  links indexed:  547
  duration:       0.12s

$ tessellum search composer --db /tmp/test.db --k 5
BM25 matches for 'composer'  (5 hits)
  1. term_dspy  (2.931)
  2. term_atomic_skill  (2.895)
  3. term_intermediate_packets  (2.886)
  4. term_dialectic_knowledge_system  (2.621)
  5. template_model  (2.271)
```

All five hits make sense — DSPy is the LM-composition framework that inspired Tessellum's typed-contract approach, atomic_skill describes composable skills, etc. BM25 ranking is doing real work.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.13"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.13"`.
- Removed obsolete `src/tessellum/retrieval/.gitkeep` (replaced by real content).
- 248/248 tests pass (223 prior + 25 new).

### What's NOT in this release (Waves 2-5)

- **Wave 2 (v0.0.14)** — Dense retrieval via sqlite-vec + sentence-transformers. `tessellum search --dense`. Adds `notes_vec` virtual table.
- **Wave 3 (v0.0.15)** — Hybrid RRF (the production winner per FZ 5e1c3a1a1's +12pp finding). `tessellum search` becomes hybrid-by-default; `--bm25` and `--dense` become explicit overrides.
- **Wave 4 (v0.0.16)** — Best-first BFS graph traversal. `tessellum search --bfs <seed>`. **No PPR** per FZ 5e2b1c (Hit@K↔answer-quality disconnect).
- **Wave 5 (v0.0.17)** — Skill orchestration. `skill_tessellum_search_notes.md` (decision-tree router) + `skill_tessellum_answer_query.md` (5-stage QA pipeline).

## [0.0.12] — 2026-05-10

### Added — Indexer Wave 1 (System D substrate)

`tessellum index build` ships the SQLite-backed unified index. **Step 5 of `plans/plan_v01_src_tessellum_layout.md` partially complete** — the substrate-level structure is in place. FTS5 + sqlite-vec + retrieval CLI layer on top in v0.0.13+.

```bash
tessellum index build
# built index at: data/tessellum.db
#   notes indexed:  71
#   links indexed:  547
#   duration:       0.11s
```

#### `src/tessellum/indexer/schema.sql`

Two-table schema, ported verbatim from the parent project's column conventions:

- **`notes`** (18 columns): `note_id`, `note_name`, `note_location`, PARA bucket (`note_category`), second-category (`note_second_category`), `note_status`, dates, file metadata, JSON-encoded `tags`/`keywords`/`topics`, `language`, `building_block`, `folgezettel` + `folgezettel_parent`, indexing timestamps. Six indexes for common access patterns.
- **`note_links`** (6 columns): `link_id`, `source_note_id`, `target_note_id`, `link_context` (±50 chars around the link), `link_type` (`'markdown'` or `'markdown_broken_path'`), `created_at`. UNIQUE constraint on (source, target). Three indexes.

Deliberately **deferred to v0.0.13**: `ghost_notes`, `broken_links`, `folgezettel_trails` (diagnostic tables); FTS5 virtual table; sqlite-vec virtual table; `static_ppr_score`, `in_degree`, `note_int_id` columns (need supporting subsystems first).

#### `src/tessellum/indexer/build.py`

`build(vault_path, db_path, *, force=False) -> BuildResult` — single transactional entry point.

- Walks the vault via `vault.rglob("*.md")` with the same non-note skip list as the format-check CLI (`README.md`, `CHANGELOG.md`, `Rank_*.md`, etc.).
- Parses each note via `tessellum.format.parse_note` (no duplicate parser code).
- Determines `note_category` from the first path segment (PARA bucket); `note_second_category` from `tags[1]` (with parent-folder fallback).
- Extracts internal markdown links with **broken-path detection**: if the relative path doesn't resolve but the target's stem uniquely names an existing note, the link is recorded as `link_type='markdown_broken_path'` with `target_note_id` pointing at the unique match. Useful for retrieval — the link is still a real relationship even if the path is wrong.
- Skips: external `http(s)://`/`mailto:` links, anchor-only `#fragment` links, links inside fenced code blocks, ambiguous broken paths.
- Idempotent: `force=True` deletes + recreates the DB; row counts match across re-runs.

#### `src/tessellum/indexer/db.py`

`Database(db_path)` — read-oriented wrapper around the SQLite connection.

Public methods (typed `NoteRow` / `LinkRow` dataclasses with JSON columns parsed):

| Method | Purpose |
|---|---|
| `all_notes()` | Every row in `notes` |
| `note_by_id(note_id)` | Single lookup |
| `notes_by_building_block(bb)` | Filter by BB enum |
| `notes_by_category(cat)` | Filter by PARA bucket |
| `notes_by_second_category(sub)` | Filter by `tags[1]` |
| `notes_by_folgezettel_root(root)` | All notes whose FZ starts with `root` (string-prefix; full topological sort in v0.0.13+) |
| `links_from(note_id)` | Outbound links |
| `links_to(note_id)` | Inbound links |
| `note_count()` / `link_count()` | Aggregate counts |

Use as a context manager (recommended) or call `close()` explicitly.

#### `src/tessellum/cli/index.py`

`tessellum index build [--vault PATH] [--db PATH] [--force]`

Defaults: `--vault ./vault`, `--db ./data/tessellum.db`. Creates the DB's parent directory as needed. Refuses to overwrite an existing DB without `--force`.

Exit codes: 0 success, 1 DB exists without `--force`, 2 vault doesn't exist.

#### CLI banner reorganized

The bare `tessellum` banner now lists 5 subcommands in the natural usage order:

1. `tessellum init <dir>` — scaffold a vault
2. `tessellum format check <path>` — validate format
3. `tessellum capture <flavor> <slug>` — create a typed note
4. `tessellum index build` — build the unified index
5. `tessellum composer validate <skill>` — validate a skill's pipeline sidecar

#### Tests

29 new tests, all passing. 223 total (194 prior + 29 new).

- `tests/smoke/test_indexer.py` (24 tests):
  - build creates DB with correct row counts
  - build refuses overwrite without `--force`; `--force` works
  - build is idempotent (consecutive runs → same counts)
  - build creates parent dirs as needed
  - missing vault → FileNotFoundError
  - Database queries: `all_notes`, `note_by_id`, `notes_by_building_block`, `notes_by_category`, `notes_by_second_category`, `notes_by_folgezettel_root`, `links_from`, `links_to`, `link_count`, `note_count`
  - JSON columns (tags/keywords/topics) parsed back to tuples
  - external links not indexed; code-block links not indexed; broken-path link uses `markdown_broken_path` type
  - non-note files (README, CHANGELOG, Rank_*) skipped
  - integration test against the real Tessellum vault
- `tests/cli/test_index_cli.py` (5 tests): basic build, refuses overwrite, `--force` works, missing vault → 2, banner mentions index build.

#### End-to-end smoke against the real Tessellum vault

```bash
$ tessellum index build --vault vault --db /tmp/test.db
built index at: /tmp/test.db
  notes indexed:  71
  links indexed:  547
  duration:       0.11s
```

71 notes (matches `tessellum format check vault/`'s file count); 547 internal markdown links resolved (skipping external/anchor/code-block links and ambiguous-broken paths). Indexing runs in ~110ms — fast enough for sub-second CI integration.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.12"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.12"`.
- Removed obsolete `src/tessellum/indexer/.gitkeep` (replaced by real content).
- 223/223 tests pass (194 prior + 29 new).

### What's NOT in this release (deferred)

- **FTS5 lexical retrieval** (v0.0.13/14) — `notes_fts` virtual table + `tessellum search --bm25 <query>` CLI.
- **sqlite-vec dense retrieval** (v0.0.14/15) — `notes_vec` virtual table + sentence-transformers integration + `tessellum search --dense <query>`.
- **Hybrid retrieval** (v0.1.0) — RRF fusion of BM25 + dense + PPR.
- **Diagnostic tables** (v0.0.13) — `ghost_notes`, `broken_links`, `folgezettel_trails`.
- **Incremental update** (v0.0.13) — `tessellum index update` (mtime-based).
- **Composer applies_to_files_query resolution** (Composer Wave 2) — uses the indexer's Database queries to resolve the schema's `term_backlink_candidates`, `related_term_notes`, `related_notes_by_keywords` query kinds.

## [0.0.11] — 2026-05-10

### Added — `tessellum init <dir>` CLI subcommand

Completes step 4c of `plans/plan_v01_src_tessellum_layout.md` and **closes the v0.1 minimum** (format library + the four core CLI subcommands: `init`, `format check`, `capture`, `composer validate`). Users can now scaffold a new vault from scratch:

```bash
tessellum init my-vault
# → 11 dirs created, 16 files copied (templates + seed term), 2 files written (master TOC + README)
cd my-vault
tessellum capture concept zettelkasten --vault .
tessellum format check .
```

#### What `tessellum init` scaffolds

- **All PARA top-level dirs**: `0_entry_points/`, `projects/`, `areas/`, `archives/` (incl. `archives/experiments/`).
- **All capture-flavor destination dirs**: derived from `tessellum.capture.REGISTRY` so every flavor's destination exists out of the box. `tessellum capture skill foo --vault .` works immediately after init.
- **All 13 templates + starter sidecar**: copied from `tessellum.data.templates_dir()` into `resources/templates/`.
- **One seed term note**: `term_building_block.md` (the load-bearing concept), copied from `tessellum.data.seed_vault_dir()`.
- **Generic master TOC**: written inline at `0_entry_points/entry_master_toc.md`, parameterized with the target dir's name. Validates clean (zero ERROR-severity issues).
- **README.md**: top-level vault overview with quick-start commands.

The full set of pillar terms (Z, PARA, BB, EF, DKS, CQRS) is **deferred** to a future `--with-pillars` flag. v0.0.11 ships only `term_building_block.md` to keep the seed minimal; users add the rest via `tessellum capture concept zettelkasten` etc.

#### `tessellum.init.scaffold(target, *, force=False) -> ScaffoldResult`

Library API for programmatic scaffolding. Returns a `ScaffoldResult` with `target`, `dirs_created`, `files_copied`, `files_written`. Raises `FileExistsError` if the target exists and is non-empty (without `--force`); raises `FileNotFoundError` if package data is missing.

#### `tessellum.data.seed_vault_dir()` accessor

Mirrors the existing `templates_dir()` pattern. Resolves the seed-vault root via `Path(__file__).parent / "seed_vault"` in installed mode; falls back to the source-tree `vault/` directly in editable mode (since seed-vault content is force-included from there). Same dual-mode resolution; same import works in dev and production.

#### Force-include — per-file mapping verified

Added a per-file entry to `pyproject.toml`'s `[tool.hatch.build.targets.wheel.force-include]`:

```toml
"vault/resources/term_dictionary/term_building_block.md" = "src/tessellum/data/seed_vault/resources/term_dictionary/term_building_block.md"
```

Hatch supports per-file mapping (not just whole-directory grafting) — verified by `python -m build && unzip -l dist/*.whl | grep seed_vault`. This pattern can be reused to add more seed terms incrementally without grafting the entire `term_dictionary/`.

#### Tests

21 new tests, all passing. 194 total (173 prior + 21 new).

- `tests/smoke/test_init.py` (15 tests) — directory structure, every flavor has a destination, all templates copied, starter sidecar copied, seed term copied + has frontmatter, master TOC has vault name + quick-start, README mentions Tessellum, **scaffolded vault validates with 0 ERROR-severity issues** (templates have placeholder LINK-003 warnings — by design), empty existing dir OK, non-empty dir refused without `--force`, `--force` preserves existing files, target-is-file → error, capture works against scaffolded vault, capture-skill paired emission works against scaffolded vault.
- `tests/cli/test_init_cli.py` (6 tests) — basic scaffold, existing non-empty → 1, `--force` → 0, target-is-file → 1, banner mentions init, help has `--force`.

#### End-to-end smoke

```bash
$ tessellum init /tmp/my-vault
scaffolded vault at: /tmp/my-vault
  directories created: 11
  files copied:        16
  files written:       2

Next steps:
  cd /tmp/my-vault
  tessellum capture concept my_topic --vault .
  tessellum format check .

$ tessellum format check /tmp/my-vault
validated 15 file(s); 0 error(s), 81 warning(s), 0 info(s)

$ tessellum capture concept hello_world --vault /tmp/my-vault
created: /tmp/my-vault/resources/term_dictionary/term_hello_world.md

$ tessellum format check /tmp/my-vault
validated 16 file(s); 0 error(s), 83 warning(s), 0 info(s)
```

Zero errors. Warnings are template placeholder broken-links (LINK-003) and orphan notes (LINK-006) — expected, by design.

### CLI banner reorganized

The bare `tessellum` banner now lists four "Available now (CLI)" entries in the natural usage order:

1. `tessellum init <dir>` — scaffold a vault
2. `tessellum format check <path>` — validate format
3. `tessellum capture <flavor> <slug>` — create a typed note
4. `tessellum composer validate <skill>` — validate a skill's pipeline sidecar

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.11"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.11"`; new `force-include` entry for `term_building_block.md`.

### v0.1 minimum status

The v0.1 plan's minimum (`plans/plan_v01_src_tessellum_layout.md` step 1-4 + Composer Wave 1) is now complete:

| Item | Version |
|---|---|
| Format library | v0.0.2 + v0.0.4 |
| `tessellum format check` | v0.0.3 |
| `tessellum capture` | v0.0.8 (+ paired-sidecar in v0.0.10) |
| Templates `force-include` | v0.0.7 |
| **`tessellum init`** | **v0.0.11 (this release)** |
| Composer Wave 1 (foundation library) | v0.0.9 |
| Composer Wave 1b (validate CLI) | v0.0.10 |

Pending for v0.1+: indexer (step 5), retrieval (step 6), Composer Waves 2-4 (compiler/executor/LLM bridge).

## [0.0.10] — 2026-05-10

### Added — Composer Wave 1b (user-facing surface)

Completes Composer Wave 1 per `plans/plan_composer_port.md`. The skill canonical ↔ pipeline.yaml pairing is now operationalized end-to-end at the CLI level — the user's load-bearing hint about "convert skill canonical note into sidebar yaml" is delivered.

#### `tessellum composer validate <skill>` CLI subcommand

```bash
tessellum composer validate vault/resources/skills/skill_foo.md
# → OK skill_foo.md (3 steps)        if pipeline_metadata points at a valid sidecar
# → OK skill_foo.md (pipeline_metadata: none)  if the skill has no Composer dispatch
# → FAIL skill_foo.md                 if any of the 3 validation stages fails

tessellum composer validate vault/resources/skills/
# Recurses over skill_*.md and reports per-file pass/fail
```

Mirrors the `tessellum format check` pattern: single file or directory, `--format json` for CI integration. Exit codes:

- **0** — every skill validates clean (or declares `pipeline_metadata: none`)
- **1** — at least one skill fails validation
- **2** — invocation error (path doesn't exist, etc.)

#### Paired sidecar emission via `tessellum capture skill <slug>`

`tessellum.capture.capture()` now does extra work for `flavor="skill"`: it emits BOTH `skill_<slug>.md` AND `skill_<slug>.pipeline.yaml` from the paired templates, and rewrites the canonical's `pipeline_metadata: none` to point at the new sidecar.

```bash
tessellum capture skill my_skill --vault vault
# → vault/resources/skills/skill_my_skill.md
# → vault/resources/skills/skill_my_skill.pipeline.yaml

tessellum composer validate vault/resources/skills/skill_my_skill.md
# → OK skill_my_skill.md (1 step)
```

The user's hint operationalized: capture-time conversion, not a one-off migration script. Authors who don't want Composer dispatch can delete the sidecar and revert `pipeline_metadata: ./...` to `none`.

`CaptureResult` gained a `sidecar_path: Path | None` attribute. `None` for non-skill flavors (and as a defensive fallback if the sidecar template is missing — but it ships with the package, so this case shouldn't fire in practice).

#### Starter sidecar template

New `vault/resources/templates/template_skill.pipeline.yaml` — schema-compliant skeleton with one CORE step (`step_1_first_action`) matching the canonical's first anchor. Includes detailed comments for every key (`role`, `aggregation`, `batchable`, `materializer`, `output_key`, `expected_output_schema`, `prompt_template`).

Ships in the wheel automatically — the existing `[tool.hatch.build.targets.wheel.force-include]` rule for `vault/resources/templates/` grafts ALL files in the directory.

#### CLI banner updated

The bare `tessellum` command now lists three subcommands under "Available now (CLI)":

- `tessellum format check <path>`
- `tessellum capture <flavor> <slug>`
- `tessellum composer validate <skill>`

#### Tests

16 new tests, all passing. 173 total (157 prior + 16 new).

- `tests/cli/test_composer_cli.py` (10 tests) — clean skill, `pipeline_metadata: none`, orphan section_id, missing sidecar, directory recursion, missing path, JSON output (clean + dirty), real-skill canonical (the shipped `skill_tessellum_format_check.md`), banner mentions composer.
- `tests/smoke/test_capture.py` (6 new tests on top of the existing 40) — paired sidecar emission for skill flavor, canonical's `pipeline_metadata` pointer, sidecar validates clean via `load_pipeline`, non-skill flavors have `sidecar_path=None`, `--force` overwrites both files, refuses overwrite when sidecar exists.

#### End-to-end smoke against a fresh vault

```bash
$ rm -rf /tmp/tessellum-paired-test-vault
$ mkdir -p /tmp/tessellum-paired-test-vault/resources/skills
$ tessellum capture skill foo --vault /tmp/tessellum-paired-test-vault
created: …/skill_foo.md
$ ls /tmp/tessellum-paired-test-vault/resources/skills/
skill_foo.md  skill_foo.pipeline.yaml
$ tessellum composer validate /tmp/…/skill_foo.md
OK   skill_foo.md (1 step)

validated 1 skill(s); 1 passed, 0 failed
```

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.10"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.10"`.

### What's NOT in this release (deferred to Wave 2+)

- **Compiler** (Wave 2) — DAG build, contract validation, zero LLM calls. `tessellum composer compile <plan_doc>`.
- **Executor + materializers** (Wave 3) — runtime placeholder resolution, agent dispatch, filesystem effect routing. `tessellum composer run <plan_doc>`.
- **LLM bridge** (Wave 4) — Anthropic SDK + optional MCP dispatcher. Behind `[agent]` / `[mcp]` extras.
- **Scale + eval** (Wave 5+) — batch runner, LLMJudge eval framework. Defer to v0.2+.

## [0.0.9] — 2026-05-10

### Added — Composer Wave 1 Foundation (library only)

Per `plans/plan_composer_port.md`. **Pure data + library.** No CLI yet, no LLM dispatch, no compiler. The library lets you load and validate skill pipeline sidecars in Python:

```python
from tessellum.composer import load_pipeline, Pipeline, ContractViolation
pipeline = load_pipeline("vault/resources/skills/skill_foo.md")
```

CLI subcommand (`tessellum composer validate`) and `tessellum capture skill` paired-sidecar emission ship in v0.0.10 (Wave 1 user-facing surface).

#### `src/tessellum/composer/schemas/pipeline.schema.json`

JSON Schema (draft-07) for the pipeline sidebar YAML format. Ported from the parent project with parent-internal references scrubbed:

- `$id` rewrites to `https://tessellum/composer/...`
- `MCPDependency.name` enum → open `pattern: ^[a-z][a-z0-9_-]*$` (Tessellum has no built-in MCPs; users register their own)
- FZ-trail-specific descriptions replaced with neutral language

The schema declares the structure: `version`, `pipeline` array of `Step` items, with required `section_id`/`role`/`aggregation`/`batchable`/`depends_on` per step. Materializer enum (5 values) covers the universal materializers; `applies_to_files_query` is documented as indexer-dependent (not yet shipped).

#### `src/tessellum/composer/contracts.py`

Three contract families as Pydantic V2 frozen models:

- **MaterializerContract** + 5 concrete subclasses (`BodyMarkdownToFileContract`, `BodyMarkdownFrontmatterToFileContract`, `EditsApplyToFilesContract`, `EditsApplyXmlTagsContract`, `NoOpContract`). Module-level registry `MATERIALIZER_CONTRACTS` keyed by materializer name.
- **LLMBackendContract** — declares backend capabilities (allowed_tools, max_user_message_chars, batching support). Default registry ships only `mock` for testing; real backends (Anthropic, OpenAI) ship with the LLM bridge in Wave 4.
- **MCPContract** — declares MCP server capabilities (available_tools, auth_required, rate_limit_qps, fallback_strategy). **Empty registry by default** — Tessellum is generic; users register their own MCPs.

`ContractViolation` exception with 10 violation kinds — defined here so library users can catch it the same way they import the contract types. The compiler (Wave 2) raises this on declaration drift.

#### `src/tessellum/composer/skill_extractor.py`

Three functions for working with skill canonicals:

- `load_skill_section(skill_path, section_id) -> str` — extracts the body text of a section identified by `<!-- :: section_id = X :: -->` anchor. Excludes the heading line; stops at the next H2 (anchored or not).
- `load_pipeline_metadata(skill_path) -> Path | None` — resolves the canonical's frontmatter `pipeline_metadata:` field. Returns `None` for the `"none"` sentinel or absent field; otherwise returns the absolute path to the sidecar (relative paths resolve against the skill's parent directory).
- `list_section_ids(skill_path) -> list[str]` — all section_ids in document order. Used by the loader for cross-file consistency checks.

#### `src/tessellum/composer/loader.py`

`load_pipeline(skill_path) -> Pipeline | None` — three-stage validation:

1. **JSON Schema** validation against `pipeline.schema.json` (structural — required keys, enum membership, pattern match)
2. **Pydantic V2** model construction (`Pipeline` and `PipelineStep` with typed access)
3. **Cross-file consistency** — every step's `section_id` must have a matching anchor in the canonical; orphan section_ids raise `PipelineValidationError`

Returns `None` if the canonical declares `pipeline_metadata: none` (skill has no Composer dispatch — e.g. `skill_tessellum_format_check.md` which is a CLI wrapper, not LLM-dispatched).

`Pipeline`, `PipelineStep`, `MCPDependency`, `Query` are Pydantic V2 frozen models mirroring the JSON schema's shape.

#### Tests

40 new tests across three files, all passing:

- `tests/smoke/test_composer_contracts.py` (18) — registry contents, contract immutability, extra-fields-forbidden, ContractViolation message format, parametrized round-trip serialization for all 5 materializer concrete classes.
- `tests/smoke/test_composer_skill_extractor.py` (11) — section extraction, body-text isolation (stops at next H2 with or without anchor), unknown section_id → error, no-anchors skill → error, document-order listing, pipeline_metadata resolution (relative path / `none` sentinel / absent field). Plus an integration test against the shipped `skill_tessellum_format_check.md` verifying its 10 anchored H2s yield non-empty bodies.
- `tests/smoke/test_composer_loader.py` (11) — happy path returns typed `Pipeline`, dependencies preserved, MCP dependencies typed, `pipeline_metadata: none` → `None`, missing sidecar → error, invalid YAML → error, schema violation (bad enum / missing required field) → error, orphan section_id → error, top-level non-mapping → error.

Total tests now 157/157 passing (117 prior + 40 new).

#### Wheel-build verification

```bash
$ python -m build --wheel
$ unzip -l dist/tessellum-0.0.9-py3-none-any.whl | grep composer
  tessellum/composer/__init__.py
  tessellum/composer/contracts.py
  tessellum/composer/loader.py
  tessellum/composer/skill_extractor.py
  tessellum/composer/schemas/pipeline.schema.json
```

Schema ships automatically because `src/tessellum/composer/schemas/` is inside `src/tessellum/` — no `force-include` needed (correctly noted in the revised plan after the post-research adjustments).

#### What's NOT in this release

Per the plan, the following ship in subsequent versions:

- v0.0.10 (Wave 1 user-facing): `tessellum composer validate` CLI; `template_skill.pipeline.yaml` starter; `tessellum capture skill` paired-sidecar emission.
- Wave 2: compiler (DAG build, contract validation, zero LLM calls).
- Wave 3: executor + materializer implementations.
- Wave 4: LLM backends (Anthropic SDK, optional MCP dispatcher).

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.9"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.9"`.

## [0.0.8] — 2026-05-10

### Added — `tessellum capture <flavor> <slug>` CLI subcommand

Step 4 of `plans/plan_v01_src_tessellum_layout.md` (capture half). Users can now create a new typed note from a template in one command:

```bash
tessellum capture concept page_rank
# → vault/resources/term_dictionary/term_page_rank.md (status: draft, date: today)

tessellum capture skill detect_atomicity_drift
# → vault/resources/skills/skill_detect_atomicity_drift.md

tessellum capture argument cqrs_thesis
# → vault/resources/analysis_thoughts/thought_cqrs_thesis.md
```

#### `tessellum.capture` library module

New `src/tessellum/capture.py` exposes:

- `REGISTRY: dict[str, TemplateSpec]` — 12 registered flavors (one per template under `vault/resources/templates/`, excluding `template_yaml_header` which is a spec reference, not a copy-and-fill skeleton).
- `TemplateSpec` — dataclass with `flavor`, `template_filename`, `destination`, `filename_prefix`, `bb_type`, `second_category`, `description`.
- `list_flavors()`, `get_spec(flavor)` — registry accessors.
- `capture(flavor, slug, vault_root, *, force=False, today=None) -> CaptureResult` — the load-bearing API.

The 12 flavors and their destinations:

| Flavor | Destination | Filename pattern |
|---|---|---|
| `concept` | `resources/term_dictionary/` | `term_<slug>.md` |
| `procedure` | `resources/how_to/` | `howto_<slug>.md` |
| `skill` | `resources/skills/` | `skill_<slug>.md` |
| `model` | `resources/term_dictionary/` | `term_<slug>.md` |
| `argument` | `resources/analysis_thoughts/` | `thought_<slug>.md` |
| `counter_argument` | `resources/analysis_thoughts/` | `thought_counter_<slug>.md` |
| `hypothesis` | `resources/analysis_thoughts/` | `thought_hypothesis_<slug>.md` |
| `empirical_observation` | `resources/analysis_thoughts/` | `thought_observation_<slug>.md` |
| `experiment` | `archives/experiments/` | `experiment_<slug>.md` |
| `navigation` | `0_entry_points/` | `<slug>.md` |
| `entry_point` | `0_entry_points/` | `entry_<slug>.md` |
| `acronym_glossary` | `0_entry_points/` | `acronym_glossary_<slug>.md` |

#### Capture transform — three-step

The capture function applies three transformations to the template content:

1. **Strip the `<!-- HOW TO USE THIS TEMPLATE: ... -->` HTML comment block.** Regex pattern is intentionally specific: requires `\n-->` (closing on its own line), since the instructional text inside the block contains a literal `<!-- HOW TO USE -->` mention ("5. Remove this `<!-- HOW TO USE -->` commentary block.") that would short-circuit a naive non-greedy match.
2. **Replace `date of note: <whatever>` with today's date** (or the explicit `today=` override).
3. **Replace `status: template` with `status: draft`** so the captured note is a real draft, not flagged as a template by search filters.

Other placeholder content (keywords, topics, body sections like `<Concept Name>`) is left for the user to fill — capture is a scaffold, not a content generator.

#### CLI

`src/tessellum/cli/capture.py` is a thin argparse wrapper. Wired into the dispatcher in `cli/main.py`:

- Positional args: `flavor` (one of 12 choices), `slug` (lowercase letters/digits/underscores only).
- Flags: `--vault PATH` (default `./vault`), `--force` / `-f` (overwrite existing).
- Exit codes: `0` success, `1` target file exists (without `--force`), `2` invalid flavor/slug or missing destination directory.

The bare `tessellum` banner now lists `tessellum capture <flavor> <slug>` under "Available now (CLI)".

#### Tests

48 new tests, all passing:

- `tests/smoke/test_capture.py` (40) — registry contents, accessors, slug validation (uppercase / space / hyphen rejected), date/status transforms, HOW TO USE strip (verifies "commentary block" and "EPISTEMIC FUNCTION" leak-text doesn't survive), refuse/force overwrite, parametrized "every flavor produces a validator-clean note" + "every flavor lands at registered destination".
- `tests/cli/test_capture_cli.py` (8) — basic create, invalid slug → 2, existing file → 1, `--force` → 0, missing vault → 2, banner mentions capture, help lists all 12 flavors.

`tests/cli/test_capture.py` was renamed to `test_capture_cli.py` to avoid a pytest module-name collision with `tests/smoke/test_capture.py`.

#### Real-vault smoke test

```bash
$ tessellum capture concept smoke_test_capture --vault vault
created: vault/resources/term_dictionary/term_smoke_test_capture.md
  flavor:  concept
  next:    fill placeholders, then `tessellum format check ...`

$ tessellum format check vault/resources/term_dictionary/term_smoke_test_capture.md
  WARNING[links] LINK-003: link target 'term_related_a.md' does not exist
  WARNING[links] LINK-003: link target 'term_related_b.md' does not exist
validated 1 file(s); 0 errors, 2 warning(s)
```

Two LINK-003 warnings are expected — they're placeholder targets in the template's See Also section that the user replaces when filling in the note.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.8"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.8"`.
- 117/117 tests pass (69 prior + 48 new).

## [0.0.7] — 2026-05-10

### Added — Templates ship in the wheel via `force-include`

Step 3 of `plans/plan_v01_src_tessellum_layout.md`. `pip install tessellum` users now get the 13 canonical BB-type templates without cloning the repo. Prerequisite for upcoming `tessellum init` and `tessellum capture <bb>` CLI subcommands.

#### `pyproject.toml` — `[tool.hatch.build.targets.wheel.force-include]`

```toml
[tool.hatch.build.targets.wheel.force-include]
"vault/resources/templates" = "src/tessellum/data/templates"
```

Hatch grafts files from `vault/resources/templates/` into the wheel at `tessellum/data/templates/` at build time. **Single source of truth in the dogfooded vault**; automatic inclusion in the wheel; no two-copy drift.

#### `tessellum.data.templates_dir()`

New module at `src/tessellum/data/__init__.py` exposing one helper:

```python
from tessellum.data import templates_dir
path = templates_dir()  # -> Path to the templates directory
```

The helper handles **both install modes**:

- **Wheel install**: returns `<site-packages>/tessellum/data/templates/` (where `force-include` grafted them).
- **Editable install** (`pip install -e .`): `force-include` doesn't run for editable installs, so the helper falls back to `<repo>/vault/resources/templates/` via `Path(__file__).resolve().parents[3]`. Same import works in both modes; no caller-side branching.

Raises `FileNotFoundError` if neither location exists (broken install or misconfigured `force-include`).

#### Tests

`tests/smoke/test_data_loader.py` (new, 16 tests):

- `templates_dir()` returns an existing directory
- The directory contains ≥ 13 `template_*.md` files
- Each of the 13 expected templates is present (parametrized)
- Every template starts with YAML frontmatter

All 16 pass in editable mode (the test environment).

#### Wheel-install verification

Build + clean-venv install + import smoke check:

```bash
$ python -m build --wheel
$ unzip -l dist/tessellum-0.0.7-py3-none-any.whl | grep templates
  tessellum/data/templates/README.md
  tessellum/data/templates/template_yaml_header.md
  tessellum/data/templates/template_concept.md
  ...  (13 templates total + README + __init__.py)

$ pip install dist/tessellum-0.0.7-py3-none-any.whl
$ python -c "from tessellum.data import templates_dir; print(templates_dir())"
  /tmp/.../site-packages/tessellum/data/templates
```

#### Out of scope (deferred to future commits)

- **Seed vault** for `tessellum init` (full directory skeleton, not just templates) — bigger scope, ships when `init` does.
- **Skills `force-include`** (so `vault/resources/skills/` is grafted too) — only needed when a CLI subcommand reads skill canonicals at runtime.
- **JSON schemas** under `tessellum.data.schemas/` — when the composer ships and needs schema-validated pipeline configs.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.7"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.7"`.
- All 69 tests pass (53 prior + 16 new in `test_data_loader.py`).

## [0.0.6] — 2026-05-10

### Changed — `scripts/` role clarified (docs-only)

Refined the convention for the top-level `scripts/` directory: **reserved for one-off operational utilities** (vault migrations, repo maintenance, contributor helpers) — *not* core capabilities. Recurring capabilities belong as CLI subcommands under `src/tessellum/cli/`, where they ship in the wheel and are invoked via `tessellum <subcommand>`.

Surfaced when reviewing what to port from the parent project's 60+ scripts: most are now-or-soon CLI subcommands (format check, indexer, retrieval, capture), library modules (config, parser), or already-ported skill canonicals. Only true one-offs (one-time migrations, contributor convenience) belong in `scripts/`.

The decision rule:

| Question | Destination |
|---|---|
| Recurring capability users run via the `tessellum` command? | `src/tessellum/cli/<subcommand>.py` |
| Re-usable library function? | `src/tessellum/<module>/` |
| One-off migration / repo maintenance / contributor helper? | top-level `scripts/` |

**Files updated**:

- `scripts/README.md` (new) — documents the convention with examples in both directions and the decision rule.
- `DEVELOPING.md § Layout Convention` — refined the `scripts/` row from "build / update / format utilities" to "one-off operational utilities, not shipped"; expanded the decision rule into 6 explicit cases.
- `plans/plan_cqrs_repo_layout.md` — refined the `scripts/` row in the System × lifecycle matrix; added a new subsection "scripts/ vs src/tessellum/cli/" calling out the subtlety.

This is a docs-only release. No code changes; library + CLI behavior unchanged. 53/53 tests still pass.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.6"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.6"`.

## [0.0.5] — 2026-05-10

### Changed — Repository layout (CQRS workflow → folder mapping)

Promoted `plans/` to a top-level directory and added `runs/` for runtime traces. Each top-level folder now maps to a defined CQRS role: System P (capture), System D (retrieval), governance (meta to both), or runtime forensics. See [`plans/plan_cqrs_repo_layout.md`](plans/plan_cqrs_repo_layout.md) for the full framing.

**New top-level folders**:

- `plans/` — project-management plan notes (committed). Status tracked via YAML `status:` field, not folder layout. Includes `plan_v01_src_tessellum_layout.md` and `plan_cqrs_repo_layout.md` (moved from `inbox/plans/`) plus a README explaining the convention.
- `runs/` — session-scoped runtime traces (gitignored except for `README.md` and `.gitkeep` files). Three subdirectories: `capture/`, `retrieval/`, `composer/`. Filename convention: `<YYYY-MM-DDThh-mm-ss>_<task>.<ext>`.

**Other layout changes**:

- `inbox/plans/` removed — plans no longer claim to be System P input.
- `.gitignore` — `runs/**` ignored except `runs/`, `runs/README.md`, `runs/*/`, `runs/*/.gitkeep`.
- `pyproject.toml` `[tool.hatch.build.targets.sdist]` — `plans` added to `include`; `runs` added to `exclude`.
- `README.md § Project Structure` — rewritten directory tree with the new top-level folders.
- `DEVELOPING.md § Layout Convention` — table now has a System role column; added rows for `plans/` and `runs/`; CQRS framing paragraph; updated decision rule.
- `vault/0_entry_points/entry_master_toc.md` — new "Project State (Outside the Vault)" section listing active plans and pointing at `runs/`.

### Fixed — link_checker config-extension skip list

`tessellum.format.link_checker._NON_MD_EXTS` now exempts common config-file formats: `.toml`, `.cfg`, `.ini`, `.lock`, `.env`. Surfaced during the layout migration when `[pyproject.toml](../pyproject.toml)` in `plan_v01_src_tessellum_layout.md` tripped LINK-001 — `.toml` is a legitimate link target, not a missing-extension defect. Added a parametrized test case covering all five new extensions.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.5"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.5"`.

### Validation

- `tessellum format check plans/`: 2 files, 0 errors, **0 warnings** (was 1 warning pre-fix).
- `tessellum format check vault/`: 71 files, 0 errors, 613 warnings (no regression).
- `pytest tests/`: **53/53 passing** (52 pre-fix + 1 new test for config extensions).

## [0.0.4] — 2026-05-10

### Added — Tier-1 parity with the parent project's format checker

Studied the parent project's `scripts/check_note_format.py` + `skill_slipbox_check_note_format.md` and ported the high-leverage features. Brings Tessellum's checker close to feature-parity for the YAML-frontmatter + body-link surface; H1/H2 section rules and the vault summary report are deferred to a later release.

#### Stable rule IDs on every issue

`Issue` now carries a `rule_id: str` field. IDs follow three families:

- `YAML-NNN` — frontmatter rules (010–099 for presence/type/value, 100–199 for linkage).
- `LINK-NNN` — body markdown link rules.
- `TESS-NNN` — Tessellum-specific rules (folgezettel pair, forbidden fields).

Existing rules are mapped to the parent's IDs where the parent has one (`YAML-010`, `YAML-014`, etc.), so logs and grep patterns are portable. Output format updated to `SEVERITY[field] RULE-ID: message`.

#### `Severity.INFO` (third tier)

Added `Severity.INFO` alongside `ERROR` and `WARNING`. No rule emits INFO yet, but the type is now available for downstream rules that want a "soft suggestion" tier (the parent uses INFO for H1/H2 hints and for orphan-related findings).

#### YAML-100/101 — forbid links inside YAML field values

Wiki links (`[[...]]`) and markdown links (`[text](path.md)`) inside YAML field values silently break the parent project's indexer. Now flagged as ERROR with the line number where they appear. Detection uses the raw frontmatter text (preserved on `Note.raw_frontmatter`), not the parsed dict.

#### LINK-001/002/003/006 — body markdown link checks

New module `tessellum.format.link_checker`:

- **LINK-001** (WARNING) — internal link missing `.md` extension
- **LINK-002** (WARNING) — internal link uses an absolute path (prefer relative)
- **LINK-003** (WARNING) — internal link target does not exist on disk
- **LINK-006** (WARNING) — note has no internal links to other notes (orphan)

Skipped (not flagged): external `http(s)://` and `mailto:` links, anchor-only `#section` links, non-markdown extensions (images, PDFs, code, archives), placeholder targets (`<placeholder>`, `link`, `...`, `-`, etc.), directory links, and any link inside a fenced code block.

`Note.raw_frontmatter: str = ""` is the new required field on the dataclass — populated by `parse_text` / `parse_note` from the regex match.

#### `Note.raw_frontmatter` + parser refactor

Dropped runtime use of `python-frontmatter`; the parser now uses PyYAML directly with a regex to capture both the parsed dict and the raw YAML text. `python-frontmatter>=1.1` removed from runtime dependencies.

#### `--format json` output

`tessellum format check --format json` emits a machine-readable report:

```json
{
  "files": [
    {
      "path": "vault/resources/term_dictionary/term_zettelkasten.md",
      "issues": [
        {"rule_id": "LINK-006", "severity": "warning", "field": "links",
         "message": "note has no internal links to other notes (orphan)"}
      ]
    }
  ],
  "summary": {
    "files_checked": 70, "files_with_issues": 64,
    "errors": 0, "warnings": 613, "infos": 0
  }
}
```

Designed so a CI step can pipe it into `jq` and gate on `summary.errors`.

#### Non-note skip list

The CLI's directory recursion now skips `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `DEVELOPING.md`, `LICENSE.md`, `MEMORY.md`, and any `Rank_*.md`. The parent project skips these because they're not vault notes (no required frontmatter). Library-level `validate(path)` is unchanged — the skip list only applies to CLI directory mode.

#### Tests

20 new tests across 2 files:

- `tests/smoke/test_link_checker.py` (13 tests) — every LINK-* rule, plus negative tests for external/anchor/non-md/placeholder/directory targets and code-block-fenced links.
- `tests/smoke/test_format_validator.py` (7 new tests on top of the existing 16) — rule IDs are well-formed, `Severity.INFO` exists, YAML-100/101 fire on link-in-YAML, plus updated `test_issue_str_*` for the new ctor signature.
- `tests/cli/test_format_check.py` (3 new tests on top of the existing 9) — `--format json` clean + dirty paths, non-note skip list.

All 52 tests pass.

#### Dogfood (separate from this commit)

Running v0.0.4 over `vault/` surfaces **0 errors and 613 warnings**: many LINK-003 (links to planned-but-not-yet-authored notes like `term_folgezettel.md`) and LINK-006 (orphan term notes). These are real findings — the vault is in early build-out — and will be addressed in follow-up data work, not by silencing the checker.

#### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.4"`; status line updated.
- `pyproject.toml`: `project.version` → `"0.0.4"`; `python-frontmatter` removed from runtime deps.

#### Breaking change

`Issue` ctor signature is now `Issue(severity, rule_id, field, message)` (4 positional args). v0.0.2/v0.0.3 used 3 positional args. Library callers constructing `Issue` directly need to add a `rule_id` argument; `validate()` consumers are unaffected.

## [0.0.3] — 2026-05-10

### Added — `tessellum format check` CLI subcommand

The validator shipped in 0.0.2 is now reachable from the shell:

```bash
tessellum format check path/to/note.md     # single file
tessellum format check vault/              # recurse over *.md
tessellum format check vault/ --strict     # treat warnings as errors
tessellum format check vault/ --quiet      # suppress summary when clean
```

Exit codes:

- **0** — no errors (warnings allowed unless `--strict`)
- **1** — at least one ERROR-severity issue (or any WARNING under `--strict`)
- **2** — invocation error (path doesn't exist, not a `.md` file or directory)

Per-file output prints the relative path (anchored at the directory if recursing, otherwise at the file's parent), then one line per issue with severity + field locator + message. A trailing summary reports total files validated, files with issues, and error/warning counts.

The dispatcher in `tessellum.cli.main` now uses argparse subparsers; sibling subcommand modules (`tessellum.cli.format_check`) expose `add_subparser(subparsers)` for wiring. Bare `tessellum` still prints the version + capability banner and now lists `format check` under "Available now (CLI)".

9 smoke tests under `tests/cli/test_format_check.py`: clean file → 0, dirty file → 1, directory recursion, warnings-only → 0, `--strict` promotes warnings to failure, missing path → 2, `--quiet` suppresses summary, bare command prints banner, `--version` exits cleanly.

Bumped:
- `src/tessellum/__about__.py`: `__version__` → `"0.0.3"`; `__status__` updated
- `pyproject.toml`: `project.version` → `"0.0.3"`

Smoke-tested end-to-end in .venv: `tessellum format check vault/` validates all 71 vault notes clean (0 errors, 0 warnings).

## [0.0.2] — 2026-05-10

### Added — Format Library (parser + validator + closed-enum spec)

The typed substrate is now usable as a library: pip users can `from tessellum import validate` to lint their own notes against the spec.

- `tessellum.format.frontmatter_spec` — closed enums as Python data: `VALID_PARA_BUCKETS` (5), `VALID_BUILDING_BLOCKS` (8), `VALID_STATUSES` (21), `REQUIRED_FIELDS` (7), soft minima for tags/keywords/topics, `FORBIDDEN_FIELDS` (`note_second_category`)
- `tessellum.format.parser` — `Note` dataclass with convenience accessors (`tags`, `para_bucket`, `second_category`, `building_block`, `status`, `folgezettel`, `folgezettel_parent`); `parse_note(path)` and `parse_text(str)` entry points; `FrontmatterParseError` for unparseable frontmatter
- `tessellum.format.validator` — `validate(target) -> list[Issue]` and `is_valid(target) -> bool`; checks all 7 required fields, the 3 closed enums, the `YYYY-MM-DD` date format, lowercase-underscore tag format, the both-or-neither rule for `folgezettel:` / `folgezettel_parent:` (incl. legacy `fz_parent` alias), and the `note_second_category` forbidden-field rule
- `tessellum.Issue` and `tessellum.Severity` re-exported at top level for ergonomics
- 23 smoke tests under `tests/smoke/test_format_validator.py` cover every error path + warning path + the 8 BB enum values
- `__about__.py` bumped to `0.0.2`; the CLI banner now points users at `validate` / `parse_note` / `is_valid`

### Caught in dogfooding (separate commit)

The new validator immediately caught 2 real spec violations + 1 corrupted file in this repo's own `vault/`. Those are fixed in a follow-up data commit, demonstrating the library works on real content.

## [0.0.1] — 2026-05-09

### Added — Namespace Reservation

- Repository skeleton with target layout (no `src/` dumping ground; clean separation of code / vault / inbox / data / experiments / scripts / tests)
- `pyproject.toml` declaring the `tessellum` PyPI package with dependencies for the v0.1 engine port
- Top-level `src/tessellum/__init__.py` documenting the six-pillar thesis
- `src/tessellum/format/building_blocks.py` — typed Python registry of the 8 BB types, 4 epistemic layers, and 10 directed edges; the load-bearing primitive of the typed substrate
- `vault/0_entry_points/entry_master_toc.md` — Master TOC entry for the dogfooded vault
- `vault/resources/term_dictionary/term_building_block.md` — first conceptual primer term note
- README + LICENSE (MIT) + CONTRIBUTING + DEVELOPING + this CHANGELOG
- `.gitignore` for derived artifacts (`data/`, `experiments/`, build outputs)

### Architecture decision

Tessellum dogfoods itself: the project's public documentation lives in `vault/` as typed atomic notes, not in a separate `docs/` directory. See [DEVELOPING.md § Layout Convention](DEVELOPING.md#layout-convention).

[Unreleased]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.14...HEAD
[0.0.14]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.13...v0.0.14
[0.0.13]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.12...v0.0.13
[0.0.12]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.11...v0.0.12
[0.0.11]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.10...v0.0.11
[0.0.10]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.9...v0.0.10
[0.0.9]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.8...v0.0.9
[0.0.8]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/TianpeiLuke/Tessellum/releases/tag/v0.0.1
