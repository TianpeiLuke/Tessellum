# `tessellum.indexer` — Building System D

## 1. Purpose

`tessellum.indexer` is the projection stage of the CQRS split: it reads the markdown vault (System P) and writes one self-contained SQLite database (System D) that the retrieval layer queries. It walks the vault, parses each typed atomic note, extracts internal markdown links (with broken-path repair), and materializes four tables — `notes`, `note_links`, `notes_fts` (BM25), `notes_vec` (dense) — in a single transaction.

## 2. Architecture / data flow

`indexer.build.build()` is the single entry point (`build.py:100`). One invocation does a full, from-scratch rebuild — there is **no incremental path yet** (`build.py:9`, `build.py:153`). The flow:

```
vault/*.md
  │  _walk_vault + _is_note_file        (drop README/CHANGELOG/… and Rank_* files)
  ▼
per-file _extract_note_metadata         (parse_note → frontmatter dict; assign note_int_id)
  │  (files with unparseable frontmatter → skipped, counted, not indexed)
  ▼
_build_note_name_index                  (stem → note_id, or [note_ids] if the stem is ambiguous)
  │
  ▼
_extract_all_links                      (regex over code-stripped body; resolve + broken-path repair; dedupe pairs)
  │
  ▼
_open_with_vec  →  one txn:  executescript(schema.sql)
                             _write_notes / _write_links / _write_fts / _write_embeddings
  ▼
BuildResult(db_path, notes_indexed, links_indexed, skipped_files, duration_seconds, embeddings_generated)
```

Ordering matters: metadata is collected for **all** notes first so `note_int_id` surrogate keys are assigned (`build.py:154`) and the name index is complete before link resolution runs. Schema creation and all four writes happen inside a single `with conn:` block (`build.py:162-169`), so the DB is either fully built or not written. The connection is opened with the `sqlite-vec` extension loaded up front (`_open_with_vec`, `build.py:79`) because `executescript` creates the `vec0` virtual table.

## 3. Key modules + abstractions

| File | Role |
|------|------|
| `indexer/__init__.py` | Public surface: re-exports `build`, `BuildResult`, `Database`, `NoteRow`, `LinkRow`. |
| `indexer/build.py` | The builder. Vault walk, metadata extraction, PARA/second-category derivation, link extraction + broken-path repair, all DB writes, dense-embedding generation. Defines `BuildResult`. |
| `indexer/schema.sql` | The four-table DDL, applied verbatim via `executescript`. Columns match the parent the source vault schema for portability. |
| `indexer/db.py` | Read-oriented `Database` wrapper + `NoteRow` / `LinkRow` dataclasses. Thin typed SQL adapter; no writes. |
| `cli/index.py` | `tessellum index build` argparse wiring; maps flags to `build(...)` and exit codes. |

Key functions in `build.py`:

- `build(vault_path, db_path, *, force=False, with_dense=True) -> BuildResult` (`build.py:100`) — the entry point.
- `_walk_vault` / `_is_note_file` (`build.py:186`, `:195`) — recursive `*.md` glob minus the non-note skip list.
- `_extract_note_metadata` (`build.py:218`) — one file → `notes`-row dict; returns `None` on `FrontmatterParseError`.
- `_determine_note_category` / `_determine_second_category` (`build.py:283`, `:290`) — PARA bucket from path[0]; `tags[1]` (source of truth) with parent-dir fallback.
- `_build_note_name_index` (`build.py:313`) — stem → note_id (or list when the stem collides).
- `_extract_all_links` / `_resolve_link` (`build.py:329`, `:400`) — link mining + relative-path resolution.
- `_write_notes` / `_write_links` / `_write_fts` / `_write_embeddings` (`build.py:450`, `:457`, `:466`, `:501`) — the four table writers.

## 4. Invariants / design decisions + WHY

**Rebuild-from-scratch each run; no incremental update.** If `db_path` exists, `build` raises `FileExistsError` unless `force=True`, in which case it `unlink()`s and recreates (`build.py:134-139`). WHY: `note_int_id` is a sequential surrogate assigned by enumeration order (`build.py:154`), stable only within one build; an incremental path would need stable surrogate management, which is deferred (`build.py:153`). Header comment states this explicitly (`build.py:9`).

**`note_int_id` is the join key for the dense index.** `notes.note_int_id INTEGER UNIQUE` (`schema.sql:32`) is the primary key of the `vec0` virtual table `notes_vec` (`schema.sql:75`). WHY: `vec0` requires an integer rowid to join dense hits back to note rows; the natural key `note_id` (a path string) can't serve. `notes_vec` embeddings and `notes` rows are correlated only through this surrogate.

**Two link types, with unique-pair dedup and broken-path repair.** `_extract_all_links` strips fenced code (`_FENCED_CODE_RE`, `build.py:352`) before matching, skips external/`mailto:`/anchor targets, and dedupes on `(source, target)` to satisfy the `UNIQUE(source_note_id, target_note_id)` constraint (`schema.sql:53`, `build.py:347`,`:380`). Resolution rules (`build.py:362-378`):
- target file exists in-vault → `link_type='markdown'`.
- target path is broken **but** its stem uniquely names an existing note → repaired to that note with `link_type='markdown_broken_path'` (`build.py:369-371`).
- stem missing or ambiguous (name index returns a list) → link silently dropped (`build.py:372`); it will surface as a format-check diagnostic, not a DB row.

WHY: broken-path repair keeps a typo'd relative path from severing a real graph edge, while the distinct `link_type` label (and index `idx_note_links_type`, `schema.sql:58`) lets consumers tell repaired edges from clean ones. The regex requires a `.md` extension (`build.py:33-35`) because links to other formats aren't note relationships.

**FK cascade on `note_links`.** Both endpoints are `REFERENCES notes(note_id) ON DELETE CASCADE` (`schema.sql:51-52`). WHY parity/correctness — deleting a note row cleans up its edges — though note that cascade requires `PRAGMA foreign_keys=ON` at connection time to enforce, and in the current full-rebuild model tables are dropped-and-recreated wholesale rather than row-deleted.

**Frontmatter is the source of truth; second-category from `tags[1]`.** `note_second_category` prefers `tags[1]` per the DEVELOPING.md rule, falling back to the parent directory name only when tags are too short (`build.py:290-307`). `note_creation_date` reads the YAML `date of note`, falling back to file-mtime date (`build.py:248`); `note_update_date` is always the mtime date. `_str_or_none` coerces the literal YAML string `"null"` to `None` (`build.py:267-280`) because templates author `folgezettel: null` as a string.

**Unparseable notes are skipped, not fatal.** `_extract_note_metadata` returns `None` on `FrontmatterParseError` (`build.py:224-227`); the file is counted in `skipped_files` and excluded from every table. WHY: one malformed note shouldn't fail the whole index; `tessellum format check` is the place that surfaces the defect.

**Non-note files are filtered.** `_NON_NOTE_NAMES` (README, CHANGELOG, CONTRIBUTING, DEVELOPING, LICENSE, MEMORY) and the `Rank_` prefix are excluded (`build.py:42-52`), deliberately mirroring the `format check` skip list so both commands see the same "real" notes.

**Dense embedding contract.** `sentence-transformers/all-MiniLM-L6-v2`, 384-dim, L2-normalized, cosine (`build.py:56-57`, `:511`; `schema.sql:63,76`). The embedding text concatenates name + keywords + topics + tags + body (`_build_embedding_text`, `build.py:480`) so both short metadata queries and long prose queries match. The encoder is a lazily-loaded module singleton (`_get_encoder`, `build.py:62`) — ~1.5s on first call, cached thereafter. Vectors are stored as packed little-endian float32 blobs (`_vec_blob`, `build.py:74`). `dense_search` returns `score = 1 - distance` so users see higher-is-better (`schema.sql:73`).

**`--no-dense` / `with_dense=False` fast build.** Skips `_write_embeddings` entirely (`build.py:167-169`); `embeddings_generated` stays 0. WHY: a BM25-only build needs no ML dependency and no model load — for CI or environments without the `sentence-transformers` stack cached (`build.py:117-119`). The `notes_vec` table still exists (schema always applied) but is empty, so `search --dense` returns nothing.

**FTS5 tokenizer.** `notes_fts` uses `porter unicode61` (`schema.sql:98`) — porter stemming + full Unicode normalization — with `note_id UNINDEXED` (join-only, not token-matched). It reuses the body already in memory from metadata extraction, so no extra disk read (`_write_fts` docstring, `build.py:466`).

Retrieval detail worth stating plainly: there is **no PageRank / link-authority scoring** in the index. `schema.sql:8-10` notes `static_ppr_score` and `in_degree` are among the parent-project columns Tessellum has **not** shipped; the graph is stored as raw edges only.

## 5. Public API / CLI

**Python API** (`from tessellum.indexer import ...`):

```python
build(vault_path, db_path, *, force=False, with_dense=True) -> BuildResult
```
- Raises `FileNotFoundError` if the vault doesn't exist; `FileExistsError` if the DB exists and `force=False`.
- `BuildResult` (frozen dataclass, `build.py:88`): `db_path`, `notes_indexed`, `links_indexed`, `skipped_files`, `duration_seconds`, `embeddings_generated`.

```python
Database(db_path)   # read-oriented wrapper; context manager or explicit close()
```
Raises `FileNotFoundError` if the DB is absent, pointing the user at `tessellum index build` (`db.py:71`). Query helpers (`db.py`):
- Notes: `all_notes()`, `note_by_id(id)`, `notes_by_building_block(bb)`, `notes_by_category(cat)`, `notes_by_second_category(cat)`, `notes_by_folgezettel_root(root)` (string-prefix trail match).
- Links: `all_links()`, `links_from(id)`, `links_to(id)`.
- Aggregates: `note_count()`, `link_count()`.
- Results are `NoteRow` / `LinkRow` frozen dataclasses; JSON columns (`tags`/`keywords`/`topics`) are parsed to tuples (`_parse_json_list`, `db.py:179`).

**CLI** (`cli/index.py`):

```
tessellum index build [--vault PATH] [--db PATH] [--force/-f] [--no-dense]
```
- `--vault` default `./vault`, `--db` default `./data/tessellum.db` (`index.py:33-44`).
- `--no-dense` maps to `with_dense=False` (`index.py:66`).
- Exit codes (`index.py:7-11`): `0` success, `1` DB exists without `--force`, `2` invocation error (e.g. missing vault).
- On success prints db path, notes/links counts, embeddings (if any), skipped count, and duration (`index.py:74-82`).

## 6. Extension points

- **Incremental indexing.** The stated deferral (`build.py:9`, `:153`). Adding it requires stable `note_int_id` management across builds so `notes_vec` rows survive — the current enumeration-order assignment is the blocker to design around.
- **New note metadata columns.** Add a column to `schema.sql`, populate it in `_extract_note_metadata`, list it in `_NOTES_INSERT_COLUMNS` (`build.py:427`), and add the field to `NoteRow` + `_row_to_note` (`db.py:191`). The parent-schema-parity comment (`schema.sql:7-10`) is the guide for column naming.
- **New link types.** `_extract_all_links` returns a `link_type` string written straight into `note_links.link_type`; a new resolver branch can emit a new label without a schema change (the column is untyped TEXT, indexed by `idx_note_links_type`).
- **Alternative embedding model.** Change `EMBEDDING_MODEL_NAME` / `EMBEDDING_DIM` (`build.py:56-57`) and the `FLOAT[384]` width in `schema.sql:76` in lockstep. `_build_embedding_text` is the single place to change what gets embedded.
- **New read queries.** Add methods to `Database`; keep it a thin SQL adapter — the module docstring (`db.py:1-8`) directs specialized traversals (FZ trails, orphan detection) to dedicated modules rather than accreting here.
- **Non-note filtering.** Extend `_NON_NOTE_NAMES` / `_NON_NOTE_PREFIXES` (`build.py:42-52`) — but keep it in sync with the `format check` skip list, which is the stated reason the two lists mirror each other.
