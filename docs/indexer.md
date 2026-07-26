# Indexer (`tessellum.indexer`)

## The mental model

Tessellum keeps its knowledge in a folder of markdown notes and answers queries out of a single SQLite database. The folder is the source of truth; the database is a derived projection of it. The indexer is the one-way bridge between them. It reads the vault and compiles it into that database, and nothing else writes the database. The arrow points from vault to DB, and only that way.

The core idea is *compile, don't sync*: the index is a reproducible projection of the vault, never a hand-patched mirror. The reference build throws the database away and rebuilds it from scratch — simple, and provably consistent with the vault at the moment it ran — and it stays the default for `tessellum index build` and the correctness oracle. But rebuilding the whole corpus on every one-note commit scales badly as the vault grows, so a second builder applies only the delta — the notes added, changed, or removed — and is proven equal, table for table, to a from-scratch rebuild. Incremental is an optimization of the same projection, never a departure from it: the output is identical, and the full rebuild is always there for a schema change or a repair. One build produces four correlated tables — a structured note table, a link-edge table, a full-text index, and a dense-vector index — so the retrieval layer can search the same corpus lexically, semantically, or as a graph without re-reading a single markdown file.

## The model — how the pieces relate

```
vault/*.md
  │  walk + filter        (drop README/CHANGELOG/… and Rank_* files)
  ▼
per-file metadata parse   (frontmatter → note row; assign surrogate id)
  │  (files with unparseable frontmatter → skipped, counted, not indexed)
  ▼
name index                (stem → note id, or a list when the stem is ambiguous)
  │
  ▼
link extraction           (mine body links, resolve paths, repair broken ones, dedupe)
  │
  ▼
one transaction:  apply schema  →  write notes / links / full-text / embeddings
  ▼
BuildResult               (db path, counts, skipped, duration, embeddings)
```

Three things flow through this pipeline, and the order is not incidental. The builder collects metadata for *every* note first. Each note needs a stable integer key, and the vector table joins back to notes through that key, so the whole key space has to exist before anything else can reference it. Only then can the builder build the name index — a map from a note's filename stem to its identity — because link resolution needs that map to be complete before it runs. And only after the name index exists can links be mined and resolved, because repairing a broken link path means looking a note up by name across the entire vault.

The four output tables split into two base tables and two search indexes. The note table holds one row per note, with its frontmatter fields flattened into columns. The link table holds one row per resolved internal link as a source-to-target edge. On top of those sit the two indexes: a full-text index that powers lexical search, and a dense-vector index that powers semantic search. The vector index is the subtle one. It cannot key on a note's path string, so it keys on the surrogate integer id and joins back through it. That surrogate is the seam that stitches a semantic hit back to a real note.

## The procedure — how a build runs

`build()` is the single public entry point, and one call does a full rebuild. It begins by checking the output path. If a database already exists there, the build refuses — unless the caller passed `force`, in which case it deletes the old file and starts clean. That refusal is the whole story of "no incremental path." There is no merge step, only overwrite.

The builder then walks the vault, recursively collecting every markdown file and dropping the handful that are not notes — top-level docs like the README and CHANGELOG, plus ranking scratch files. For each surviving file it parses the YAML frontmatter and flattens the fields it cares about into a row: name, location, category, status, dates, tags, keywords, topics, building block, and Folgezettel position. Two of these columns are *derived* rather than copied. The PARA category comes from the note's top-level folder. The second category comes from the note's second tag — the authoring rules make that tag the source of truth — and falls back to the parent directory name only when the tags are too short to supply it. If a note's frontmatter cannot be parsed, the builder does not fail. It skips that one note, counts it, and moves on. Surfacing the defect is the format checker's job, not the indexer's.

Once all notes are collected, the builder assigns each a sequential surrogate id and constructs the name index. Then it runs link extraction. For each note it first strips fenced code blocks out of the body, so a link written inside an example never becomes a real edge, then scans the remaining prose for markdown links that point at other notes, skipping anything external, a `mailto:`, or a bare anchor. Each surviving target is resolved relative to the linking note. If the target file exists, it becomes a clean edge. If the path is broken but its filename stem uniquely identifies a real note, the link is *repaired* — pointed at that note and tagged as a broken-path edge, so a consumer can still tell a repaired edge from a pristine one. If the stem is missing or ambiguous, the link is dropped silently; it will resurface as a diagnostic under format check, not as a database row. Every kept edge is deduplicated on its source-target pair.

Finally the builder writes everything in one transaction. It opens a connection with the vector extension already loaded — the schema declares a virtual vector table, so the extension must be present before the schema can be applied — applies the schema, and writes the four tables inside a single transactional block. Either the whole database is built or nothing is written; there is no half-populated intermediate state. The dense embeddings are the only optional table. For each note the builder concatenates its name, keywords, topics, tags, and body into one embedding text, encodes the batch with a sentence-transformers model, and stores each vector against its surrogate id. When embeddings are disabled, the step is skipped and the vector table is left empty. Encoding is also fail-soft: if the sentence-transformer dependency is missing or the encoder fails, the build degrades to a BM25-only index and flags `dense_degraded` on the result rather than aborting — so a dense-index problem never fails the whole build, nor, on the runtime path, a whole commit. The call returns a `BuildResult` summarizing the run.

Reading is a separate, deliberately thin surface. A small `Database` wrapper opens the finished DB and offers typed lookups — by id, by category, by building block, by Folgezettel root, and the links into or out of a note — but it never mutates. To change a row, you rebuild. That asymmetry is the CQRS split made concrete: the indexer is the write side, the wrapper is the read side, and they meet only at the file on disk.

## Design decisions and why

**Rebuild from scratch; no incremental update.** Each run drops and recreates the database rather than diffing the vault against it. The reason is the surrogate key. A note's integer id is assigned by enumeration order within a single build, and it is only stable *within* that build. An incremental path would have to keep those ids stable across runs so the vector index survived, and that stable-id bookkeeping is deliberately deferred. Rebuild-from-scratch trades a slower rebuild for a builder with no drift and no reconciliation logic.

**The surrogate id is the join key for semantic search.** The natural key for a note is its vault-relative path, but the vector index requires an integer rowid to join dense hits back to note rows — a path string cannot serve. So every note carries a surrogate integer id, and the vector table is keyed on it. This is precisely why metadata collection must finish for all notes before anything else runs: the surrogate space has to be fully assigned first.

**Broken links are repaired, not dropped, when the name is unambiguous.** A typo in a relative path should not sever a link that clearly means to reach a real note. When a broken path's filename uniquely identifies a note, the builder reconnects the edge and labels it as repaired. The label matters. A consumer that cares about link hygiene can still tell repaired edges from clean ones, so repair improves graph connectivity without hiding the underlying defect. Truly ambiguous or unresolvable links are left for the format checker to report.

**One malformed note never fails the whole index.** A note with unparseable frontmatter is skipped and counted, not fatal. A single bad note should not cost the entire build. The index stays useful over the healthy notes, and the defective one is caught by `tessellum format check`, which exists precisely to surface such problems.

**Fenced code is stripped before links are mined.** A link inside a code example documents syntax; it does not assert that two notes relate. Stripping fenced code before the link scan runs keeps illustrative links out of the real graph.

**The non-note skip list mirrors the format checker's.** The indexer and the format checker exclude the same files, so both commands operate over an identical set of real notes. Keeping the two lists in sync means the thing you index is exactly the thing you validate.

**Frontmatter is the source of truth.** Derived columns prefer explicit frontmatter over filesystem guesses. The second category comes from the note's tags before it falls back to the directory name, and the creation date comes from the YAML date before it falls back to file mtime. The one place the filesystem wins outright is the update date, which is always the file's modification time. A literal string `"null"` in YAML is also coerced to a real null, because templates author unset trail fields that way.

**Two search substrates, one corpus, uniform conventions.** The full-text index uses porter stemming with full Unicode normalization, so English queries match across word forms, and it reuses the note body already in memory rather than re-reading from disk. The dense index stores L2-normalized vectors and reports similarity as one-minus-distance, so that — like every other Tessellum search surface — higher means more similar. Both indexes are built from the same in-memory note data in the same transaction, so they can never disagree about what the corpus contains.

**No link-authority scoring in the index.** The graph is stored as raw edges only. There is deliberately no PageRank or in-degree authority column baked into the database. Link authority is a retrieval-time concern, not something the projection should precompute.

**Reference:** [reference/indexer.md](reference/indexer.md) — API, symbols, and signatures.
