---
tags:
  - resource
  - terminology
  - sqlite
  - full_text_search
  - inverted_index
  - bm25
  - sparse_retrieval
  - storage_layer
keywords:
  - FTS5
  - Full-Text Search version 5
  - SQLite full-text search
  - inverted index
  - BM25 ranking
  - virtual table
  - unicode61 tokenizer
  - porter tokenizer
  - snippet function
  - MATCH operator
topics:
  - retrieval substrate
  - sparse retrieval
  - SQL-embedded search
  - knowledge base indexing
language: markdown
date of note: 2026-04-29
status: active
building_block: concept
related_wiki: https://www.sqlite.org/fts5.html
---

# FTS5 - Full-Text Search version 5

## Definition

**FTS5** (Full-Text Search version 5) is the fifth-generation full-text search extension built into SQLite since version 3.9 (2015). It implements an inverted-index-backed virtual table type that supports keyword, phrase, prefix, and boolean queries with native BM25 relevance ranking, configurable Unicode-aware tokenizers, and snippet/highlight auxiliary functions — all transactional, atomic with row writes, and stored inside the same `.db` file as the relational data.

In the slipbox vault context, FTS5 is the leading candidate to replace the standalone `bm25_index.pkl` artifact (built by `rank_bm25.BM25Okapi`) per [FZ 5e1c3a1's unified-index proposal](../analysis_thoughts/proposal_unified_index_engine_sqlite_vec_fts5_design.md): collapsing four independent index artifacts (SQLite metadata, `bm25_index.pkl`, `note_embeddings.npy`, `note_ids_order.json`) into one file would close the COE-2026-04-29 sync-script Bug A surface area and give us atomic cross-index updates "for free".

## Context

FTS5 ships with the SQLite Amalgamation that the slipbox vault's databases (`abuse_slipbox_notes.db`, `slipbot_qa.db`, `slipbot_experiments.db`) already use — no additional dependencies, no separate process. Within Amazon, FTS5 powers MeshClaw's session-memory retrieval (see `snippet_meshclaw_memory_fts5`) and is a peer to enterprise search engines like [Elasticsearch](term_elasticsearch.md) and [OpenSearch](term_opensearch.md), but at vastly smaller operational scope: a single embedded virtual table rather than a distributed cluster.

Outside the vault, FTS5 is widely used in personal-knowledge tools (Obsidian's omnisearch plugin, DEVONthink, Notable, Logseq), CLIs that need offline search (ripgrep wrappers, sqlite-utils), and embedded full-text search inside mobile apps (it backs Signal's message search, among others). Its design point is "good-enough BM25 in a file you can `cp`", which matches the slipbox vault's "single backup file" goal exactly.

## Key Characteristics

- **Inverted index**: tokenizes each row's text into normalized terms, stores per-term posting lists `(rowid, position(s))` so queries that intersect multiple terms run in time proportional to the rarest term's posting list, not the total corpus size.
- **BM25 ranking**: built-in `bm25(table)` SQL function returns Okapi BM25 scores (default `k1=1.2`, `b=0.75`) — the same algorithm family `rank_bm25` uses, but with FTS5's own tokenizer rules.
- **Configurable tokenizers**: `unicode61` (default, Unicode-aware case-folding + diacritic removal), `porter` (English stemmer on top of unicode61), `ascii` (legacy/byte), or pluggable custom tokenizers in C.
- **Virtual-table interface**: `CREATE VIRTUAL TABLE notes_fts USING fts5(...)`; behaves like a regular table for INSERT/UPDATE/DELETE so participates in the same transactions as relational rows. No separate "rebuild the pickle" step.
- **`MATCH` operator**: `WHERE notes_fts MATCH 'sqlite AND vec'` for boolean queries; `'"hybrid retrieval"'` for phrases; `'body : graph'` for column-scoped search; `'sqlite NOT pickle'` for exclusion.
- **Auxiliary functions**: `snippet(table, col, openTag, closeTag, ellipsis, maxTokens)` returns a `…matching context…` excerpt; `highlight(table, col, openTag, closeTag)` wraps matched terms with markup. Useful for SlipBot answer attribution.
- **Storage modes**: default "internal-content" stores a copy of the indexed text inside FTS5's auxiliary tables (so snippet/highlight work); "external-content" mode points at another table to avoid duplication but loses snippet support.
- **Incremental + ACID**: every row insert/update/delete updates the index inside the SQL transaction. A crash mid-update leaves a coherent state; no half-rebuilt pickle.
- **Single-file storage**: the FTS5 index lives in shadow tables (`<name>_data`, `<name>_idx`, `<name>_docsize`, `<name>_config`) inside the same `.db` file. `cp file.db backup.db` is a complete backup including the index.
- **Trigram extension** (FTS5 + trigram tokenizer, SQLite ≥ 3.34): supports substring-LIKE queries with index acceleration — useful when users search for partial identifiers or code symbols.

## Performance / Metrics

At slipbox scale (9,336 notes, ~600 MB raw markdown), FTS5 on a typical laptop SSD:

| Operation | Expected latency | Notes |
|---|---:|---|
| Single-row `INSERT INTO notes_fts` | < 1 ms | per-row tokenize + posting-list update |
| `MATCH` query, single term | 1–5 ms | scales with rarest-term posting list |
| `MATCH` query + `bm25()` ORDER BY + LIMIT 50 | 5–20 ms | full scan over MATCH-qualified rows |
| Snippet generation, top-10 results | 1–3 ms | reads stored body from FTS5 internal tables |
| Full rebuild (`INSERT INTO notes_fts SELECT ... FROM notes`) | ~10–30 s | tokenizes the entire vault body |

These are project predictions for FZ 5e1c3a1 Phase 0; not yet measured. **Phase 1 of the migration plan benchmarks FTS5 BM25 against `rank_bm25.BM25Okapi` on the n=80 SlipBot QA set** to verify ranking parity (Hit@5 within 1 SE).

## Related Terms

- **[Information Retrieval](term_information_retrieval.md)**: the parent field; FTS5 is one concrete realization of sparse-retrieval IR primitives (inverted index + BM25) embedded in a SQL engine.
- **[Elasticsearch](term_elasticsearch.md)**: distributed search engine on Apache Lucene; same algorithmic family as FTS5 (Lucene also uses inverted index + BM25) but at distributed/web-scale rather than embedded/personal-scale.
- **[OpenSearch](term_opensearch.md)**: AWS-managed fork of Elasticsearch; same peer relationship — same algorithm family, opposite end of the operational-scale spectrum from FTS5.
- **[Vector Database](term_vector_database.md)**: the dense-retrieval counterpart that FTS5 complements in hybrid retrieval; in the unified-index proposal `notes_vec` (sqlite-vec) sits next to `notes_fts` (FTS5) in the same SQLite file.
- **[Dense Retrieval](term_dense_retrieval.md)**: the embedding-cosine retrieval modality; FTS5 is the *sparse* counterpart, and modern hybrid pipelines (RRF) fuse the two.
- **[Embedding](term_embedding.md)**: what dense retrieval indexes — FTS5 is the sparse alternative that does not require an encoder model.
- **[ANN Search](term_ann_search.md)**: approximate-nearest-neighbor search for high-dimensional vectors; orthogonal retrieval modality to FTS5's inverted-index search.
- **[Tokenization](term_tokenization.md)**: FTS5's first preprocessing step; choice of tokenizer (`unicode61` vs `porter` vs custom) determines what the inverted index actually stores.
- **[PageRank](term_pagerank.md)**: graph-based ranking algorithm; conceptual peer to BM25 in the "how do you rank a result set" design space, used in the slipbox vault for `static_ppr_score` over `note_links`.
- **[RAG](term_rag.md)**: retrieval-augmented generation; FTS5 is one of the legitimate retrieval backends for a RAG pipeline (sparse arm), often combined with a dense arm via RRF.
- **[Cosine Similarity](term_cosine_similarity.md)**: scoring function used by dense retrieval; FTS5's BM25 is the sparse-side analog (different math, same role).
- **[KG Embeddings](term_kg_embeddings.md)**: graph-aware embeddings; another retrieval modality that complements FTS5's lexical matching when query terms don't match document vocabulary.
- **[sqlite-vec](term_sqlite_vec.md)**: sister SQLite extension for vector storage and KNN search; paired with FTS5 in FZ 5e1c3a1's unified-index proposal — sqlite-vec for the dense arm, FTS5 for the sparse arm, both inside the same `.db` file.

## References

- [SQLite FTS5 documentation](https://www.sqlite.org/fts5.html) — the authoritative spec; covers virtual table interface, MATCH grammar, BM25 function, all tokenizers, auxiliary functions, internal vs external content modes, and shadow-table layout.
- [SQLite version 3.9 release notes (Oct 2015)](https://www.sqlite.org/releaselog/3_9_0.html) — initial FTS5 release with rationale vs FTS3/4.
- [Cormack, Clarke, Büttcher (2009) — Reciprocal Rank Fusion](https://plg.uwaterloo.ca/~gvcormack/cormacksigir09-rrf.pdf) — the canonical RRF reference; FTS5 + dense retrieval fusion in the unified-index proposal uses RRF (k=60 default).
- [Robertson & Zaragoza (2009) — The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) — definitive BM25 mathematical foundation; FTS5's `bm25()` implements this directly with `k1=1.2`, `b=0.75` defaults.
- [Alex Garcia, sqlite-vec + FTS5 hybrid search (2024)](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html) — leading blog-grade benchmark of the exact stack the unified-index proposal targets; demonstrates RRF over FTS5 + sqlite-vec at ~14k docs.