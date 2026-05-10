-- Tessellum unified-index schema, v0.0.12 (Wave 1 — minimal).
--
-- Two tables: notes + note_links. FTS5 (lexical) and sqlite-vec (dense)
-- are deferred to v0.0.13 / v0.0.14. Ghost-note + broken-link diagnostic
-- tables are deferred to v0.0.13.
--
-- Schema is portable to and from the parent project: column names match
-- AbuseSlipBox's `notes` and `note_links` tables verbatim, modulo columns
-- that depend on subsystems Tessellum hasn't shipped yet
-- (static_ppr_score, in_degree, note_int_id).

CREATE TABLE IF NOT EXISTS notes (
    note_id              TEXT PRIMARY KEY,             -- vault-relative path
    note_name            TEXT NOT NULL,                -- file stem
    note_location        TEXT NOT NULL,                -- parent dir (relative)
    note_category        TEXT,                         -- tags[0] / PARA bucket
    note_second_category TEXT,                         -- tags[1]
    note_status          TEXT,
    note_creation_date   DATE,                         -- YAML "date of note"
    note_update_date     DATE,                         -- file mtime date
    file_path            TEXT NOT NULL,                -- alias of note_id; kept for parity
    file_size_bytes      INTEGER,
    tags                 TEXT,                         -- JSON array
    keywords             TEXT,                         -- JSON array
    topics               TEXT,                         -- JSON array
    language             TEXT,
    building_block       TEXT,
    folgezettel          TEXT,
    folgezettel_parent   TEXT,
    indexed_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_indexed_mtime   REAL                          -- file mtime as epoch float
);

CREATE INDEX IF NOT EXISTS idx_notes_category           ON notes(note_category);
CREATE INDEX IF NOT EXISTS idx_notes_second_category    ON notes(note_second_category);
CREATE INDEX IF NOT EXISTS idx_notes_status             ON notes(note_status);
CREATE INDEX IF NOT EXISTS idx_notes_building_block     ON notes(building_block);
CREATE INDEX IF NOT EXISTS idx_notes_folgezettel        ON notes(folgezettel);
CREATE INDEX IF NOT EXISTS idx_notes_folgezettel_parent ON notes(folgezettel_parent);


CREATE TABLE IF NOT EXISTS note_links (
    link_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    source_note_id  TEXT    NOT NULL,
    target_note_id  TEXT    NOT NULL,
    link_context    TEXT,                                -- ±50 chars around the link
    link_type       TEXT,                                -- 'markdown' | 'markdown_broken_path'
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_note_id) REFERENCES notes(note_id) ON DELETE CASCADE,
    FOREIGN KEY (target_note_id) REFERENCES notes(note_id) ON DELETE CASCADE,
    UNIQUE(source_note_id, target_note_id)
);

CREATE INDEX IF NOT EXISTS idx_note_links_source ON note_links(source_note_id);
CREATE INDEX IF NOT EXISTS idx_note_links_target ON note_links(target_note_id);
CREATE INDEX IF NOT EXISTS idx_note_links_type   ON note_links(link_type);


-- Lexical (BM25) full-text index. Populated alongside `notes` by the builder.
-- Uses the porter stemmer + unicode61 tokenizer — the SQLite default for
-- English with full Unicode normalization. `note_id` is UNINDEXED because
-- we only need it for joins, not for token matching.
--
-- Query via the bm25() ranking function:
--     SELECT note_id, -bm25(notes_fts) AS score
--     FROM notes_fts
--     WHERE notes_fts MATCH ?
--     ORDER BY bm25(notes_fts)
--     LIMIT ?
--
-- (The negation is because FTS5 returns lower-is-better; we want
-- higher-is-better in user-visible output.)
CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
    note_id UNINDEXED,
    note_name,
    body,
    tokenize='porter unicode61'
);
