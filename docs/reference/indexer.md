# `tessellum.indexer` — Reference

API, symbols, and signatures for the vault indexer. For the mental model and how work flows through it, see [../indexer.md](../indexer.md).

## File → role

| File | Role |
|------|------|
| `build.py` | The compiler. `build()` entry point + `BuildResult`, the vault walk, per-file metadata extraction, link mining/resolution/repair, and the four DB writers (notes, links, FTS, embeddings). Owns the link regex, the non-note skip list, and the embedding model constants. |
| `db.py` | The read side. `Database` wrapper + `NoteRow` / `LinkRow` dataclasses and their row converters. Read-only, typed query helpers; no mutation. |
| `schema.sql` | The DDL. `notes` + `note_links` base tables (with indexes + FKs), the `notes_vec` sqlite-vec virtual table, and the `notes_fts` FTS5 virtual table. Applied verbatim via `executescript` at build time. |
| `__init__.py` | Public surface: re-exports `build`, `BuildResult`, `Database`, `NoteRow`, `LinkRow`. |
| `cli/index.py` | The `tessellum index build` command: wires `build()` into the CLI, resolves paths, maps exceptions to exit codes, prints the summary. |

## Public API — `tessellum.indexer`

### Builder (`build.py`)

- `build(vault_path: Path | str, db_path: Path | str, *, force: bool = False, with_dense: bool = True) -> BuildResult` — full from-scratch scan and write. Creates `db_path` parent dirs as needed. Raises `FileNotFoundError` if `vault_path` is not a directory; raises `FileExistsError` if `db_path` exists and `force=False` (with `force=True`, deletes and recreates). `with_dense=False` skips embedding generation.
- `BuildResult` — `@dataclass(frozen=True)`: `db_path: Path`, `notes_indexed: int`, `links_indexed: int`, `skipped_files: int`, `duration_seconds: float`, `embeddings_generated: int = 0` (0 when `with_dense=False`).

### Reader (`db.py`)

- `Database(db_path: Path | str)` — opens the indexed DB with `sqlite3.Row` factory. Raises `FileNotFoundError` if the DB is missing. Usable as a context manager or via `close()`.

| Method | Returns | Query |
|--------|---------|-------|
| `all_notes()` | `list[NoteRow]` | all notes, ordered by `note_id` |
| `note_by_id(note_id)` | `NoteRow \| None` | single note by vault-relative path |
| `notes_by_building_block(bb)` | `list[NoteRow]` | `WHERE building_block = ?` |
| `notes_by_category(cat)` | `list[NoteRow]` | `WHERE note_category = ?` (PARA bucket, from the top-level folder via `_CATEGORY_MAP` — never from tags) |
| `notes_by_second_category(cat)` | `list[NoteRow]` | `WHERE note_second_category = ?` (`tags[1]`) |
| `notes_by_folgezettel_root(root)` | `list[NoteRow]` | `WHERE folgezettel LIKE 'root%'` (trail subset, prefix match) |
| `all_links()` | `list[LinkRow]` | all links, ordered by source then target |
| `links_from(note_id)` | `list[LinkRow]` | outbound edges (`source_note_id = ?`) |
| `links_to(note_id)` | `list[LinkRow]` | inbound edges (`target_note_id = ?`) |
| `note_count()` | `int` | `COUNT(*)` of notes |
| `link_count()` | `int` | `COUNT(*)` of links |

- `NoteRow` — `@dataclass(frozen=True)`: one `notes` row with JSON columns (`tags`, `keywords`, `topics`) parsed to `tuple[str, ...]`. Fields mirror the `notes` table below, plus `indexed_at` and `last_indexed_mtime`.
- `LinkRow` — `@dataclass(frozen=True)`: `link_id: int`, `source_note_id: str`, `target_note_id: str`, `link_context: str | None`, `link_type: str | None`, `created_at: str | None`.

## Schema (`schema.sql`)

### `notes` — one row per note

| Column | Type | Source |
|--------|------|--------|
| `note_id` | TEXT PK | vault-relative path |
| `note_name` | TEXT | file stem |
| `note_location` | TEXT | parent dir (relative) |
| `note_category` | TEXT | top-level folder → PARA bucket (`_CATEGORY_MAP`) |
| `note_second_category` | TEXT | `tags[1]`, else parent dir name |
| `note_status` | TEXT | frontmatter `status` |
| `note_creation_date` | DATE | frontmatter `date of note`, else file mtime date |
| `note_update_date` | DATE | file mtime date (always) |
| `file_path` | TEXT | alias of `note_id` (parity with parent project) |
| `file_size_bytes` | INTEGER | `stat().st_size` |
| `tags` / `keywords` / `topics` | TEXT | JSON array |
| `language` | TEXT | frontmatter `language` |
| `building_block` | TEXT | frontmatter `building_block` |
| `folgezettel` | TEXT | frontmatter `folgezettel` |
| `folgezettel_parent` | TEXT | frontmatter `folgezettel_parent`, else `fz_parent` |
| `indexed_at` | TIMESTAMP | `DEFAULT CURRENT_TIMESTAMP` |
| `last_indexed_mtime` | REAL | file mtime (epoch float) |
| `note_int_id` | INTEGER UNIQUE | surrogate key for the `notes_vec` join |

Indexes: `note_int_id`, `note_category`, `note_second_category`, `note_status`, `building_block`, `folgezettel`, `folgezettel_parent`.

### `note_links` — one row per resolved internal link

| Column | Type | Notes |
|--------|------|-------|
| `link_id` | INTEGER PK AUTOINCREMENT | |
| `source_note_id` | TEXT NOT NULL | FK → `notes(note_id)` ON DELETE CASCADE |
| `target_note_id` | TEXT NOT NULL | FK → `notes(note_id)` ON DELETE CASCADE |
| `link_context` | TEXT | ±50 chars around the link, newlines collapsed |
| `link_type` | TEXT | `'markdown'` or `'markdown_broken_path'` |
| `created_at` | TIMESTAMP | `DEFAULT CURRENT_TIMESTAMP` |

`UNIQUE(source_note_id, target_note_id)` — the dedupe constraint. Indexes: `source_note_id`, `target_note_id`, `link_type`.

### `notes_vec` — dense (cosine) index (sqlite-vec `vec0`)

`note_int_id INTEGER PRIMARY KEY`, `embedding FLOAT[384] distance_metric=cosine`. Populated unless `with_dense=False`. Query via `MATCH` + `k`, join `notes` on `note_int_id`; distance is cosine (lower = more similar), and `dense_search()` reports `score = 1 - distance`.

### `notes_fts` — lexical (BM25) index (FTS5)

`note_id UNINDEXED`, `note_name`, `body`, `tokenize='porter unicode61'`. Query via `MATCH` + `bm25()`; FTS5 ranks lower-is-better, so user-visible scores negate it.

## Constants (`build.py`)

| Symbol | Value | Purpose |
|--------|-------|---------|
| `EMBEDDING_DIM` | `384` | vector dimensionality |
| `EMBEDDING_MODEL_NAME` | `"sentence-transformers/all-MiniLM-L6-v2"` | dense encoder (lazy-loaded singleton, ~1.5s first call) |
| `_NON_NOTE_NAMES` | `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `DEVELOPING.md`, `LICENSE.md`, `MEMORY.md` | skipped by the walk; mirrors the format-check skip list |
| `_NON_NOTE_PREFIXES` | `("Rank_",)` | filename prefixes skipped by the walk |
| `_PARA_FOLDERS` | `0_entry_points`, `areas`, `projects`, `resources`, `archives` | recognized top-level folders (second-category fallback excludes these) |
| `_CATEGORY_MAP` | folder → `entry_point` / `area` / `project` / `resource` / `archive` | derives `note_category` |
| `_MARKDOWN_LINK_RE` | `[text](path.md#anchor?)` | link miner (requires `.md`; allows nested `[..]` in text) |
| `_FENCED_CODE_RE` | ``` ```…``` ``` (DOTALL) | stripped from body before link mining |
| `_EXTERNAL_RE` | `^https?://` | external links skipped |

## Internal helpers (`build.py`)

| Symbol | Role |
|--------|------|
| `_walk_vault(vault)` / `_is_note_file(p)` | recursive `*.md` collection with skip-list filter |
| `_extract_note_metadata(md_file, vault_path)` | one file → metadata dict; `None` on `FrontmatterParseError` |
| `_str_or_none(value)` | YAML → `str \| None`; coerces `None`, `""`, and literal `"null"` to `None` |
| `_determine_note_category(rel_path)` | top-level folder → PARA bucket via `_CATEGORY_MAP` |
| `_determine_second_category(tags, rel_path)` | `tags[1]` if present, else parent dir name (unless a PARA folder) |
| `_build_note_name_index(notes)` | stem → `note_id`, or `list[note_id]` when the stem is duplicated |
| `_extract_all_links(notes, vault_path, name_index)` | mine + resolve + repair + dedupe → link records |
| `_resolve_link(target, vault_path, source_path)` | `(note_id, None)` exists / `(None, ghost)` missing-in-vault / `(None, None)` outside vault |
| `_open_with_vec(db_path)` | open a connection with the sqlite-vec extension loaded |
| `_get_encoder()` | lazy-load the sentence-transformers model (module singleton) |
| `_vec_blob(vector)` | pack a float list as a little-endian float32 blob for sqlite-vec |
| `_build_embedding_text(note)` | concatenate name + keywords + topics + tags + body |
| `_write_notes` / `_write_links` / `_write_fts` / `_write_embeddings` | the four table writers (each `executemany`) |

## Link resolution / repair

- **Kept as `markdown`** — target `.md` resolves to an existing file inside the vault.
- **Kept as `markdown_broken_path`** — target path is broken, but the target's stem *uniquely* names an existing note (`name_index` hit is a single `str`); the edge is repaired to that note.
- **Dropped silently** — target is external (`https?://`), a `mailto:`/anchor, resolves outside the vault, or its stem is missing/ambiguous. Surfaces as `LINK-003` under `tessellum format check`, not as a DB row.
- **Deduped** — each `(source_note_id, target_note_id)` pair is written at most once (matches the `UNIQUE` constraint).

## CLI — `tessellum index build`

Registered in `cli/main.py` alongside `bb`, `capture`, `composer`, `dks`, `mcp`, `filter`, `format`, `fz`, `init`, `search`.

```
tessellum index build [--vault PATH] [--db PATH] [--force|-f] [--no-dense]
```

| Flag | Default | Effect |
|------|---------|--------|
| `--vault` | `./vault` | Vault root directory. |
| `--db` | `./data/tessellum.db` | Output SQLite DB path (parent dirs created as needed). |
| `--force` / `-f` | off | Overwrite an existing DB at the output path. |
| `--no-dense` | off | Skip dense-embedding generation (faster; disables `tessellum search --dense`; sets `with_dense=False`). |

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | Index built successfully. |
| `1` | Output DB exists and `--force` not passed (`FileExistsError`). |
| `2` | Invocation error — vault doesn't exist, etc. (`FileNotFoundError`). |
