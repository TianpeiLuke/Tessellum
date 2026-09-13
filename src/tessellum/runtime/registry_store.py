"""SQLite-backed entity registry + Tier-A relations cache (P1 storage side).

The runtime half of the query-time DKS plan's step 1. ``dks.entity_registry``
defines the shapes and the two ports (``RegistrySource`` read /
``RegistrySink`` write) and stays pure; this module is the only place the
registry touches a disk, which is what keeps the Dependency Rule intact —
storage lives in ``runtime/``, the kernel reads and proposes.

**A rebuildable projection, not a source of truth.** Every table here is
derivable from authored notes: drop the database and the vault loses nothing but
latency. That is why the write API *replaces* a layer rather than appending to
it — ``replace_spine`` / ``replace_candidates`` /
``replace_authored_relations`` each rebuild one layer idempotently. The
append-only discipline the plan mandates belongs to the claim/edge log, a
different table with a different lifecycle; conflating the two would make a cache
un-rebuildable.

Two layering rules the write API enforces rather than documents:

- ``replace_authored_relations`` scopes its delete to ``origin='authored'``, so
  later query-derived (``origin='resolved'``) rows layer on TOP of the authored
  seed and a reseed never silently drops them.
- it refuses any row whose ``origin`` is not ``authored``; the authored seed is a
  projection of frontmatter and nothing else may ride in on it.

:data:`REGISTRY_SCHEMA` is applied to a SIDECAR database, separate from the job
queue, because the registry's lifetime is "rebuild whenever the vault changes"
and the queue's is "durable across restarts". The *DDL* is not separate, though:
the registry-only tables are declared below and the Tier-A ``relations`` table is
read from the ``tier_a_relations`` section of ``runtime/schema.sql``, which the
runtime database applies as well. It was written out twice until the two copies
drifted (different NOT NULLs, one extra column on one side), so the table now has
exactly one definition and two appliers.
"""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path
from typing import Sequence

from tessellum.dks.entity_registry import (
    AuthoredRelation,
    CandidateEntity,
    Entity,
    EntityAlias,
    EntityRegistry,
    registry_content_digest,
)
from tessellum.runtime.schema import WAL_PRAGMA, schema_section

_REGISTRY_TABLES = """

CREATE TABLE IF NOT EXISTS registry_schema (
    version INTEGER NOT NULL
);

INSERT INTO registry_schema(version)
SELECT 1 WHERE NOT EXISTS (SELECT 1 FROM registry_schema);

-- Build/version provenance. Timestamps live HERE and never in a content table,
-- so a determinism diff over the content tables stays clean.
CREATE TABLE IF NOT EXISTS registry_meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);

-- Canonical entities. The spine is one row per entity-DEFINING note, so
-- entity_id == note_id and the registry inherits the vault's identity rather
-- than minting a parallel one. source_layer separates the projected spine from
-- later promoted candidates.
CREATE TABLE IF NOT EXISTS entities (
    entity_id      TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    entity_type    TEXT NOT NULL,
    note_id        TEXT NOT NULL,
    file_path      TEXT NOT NULL,
    folgezettel    TEXT,
    source_layer   TEXT NOT NULL CHECK (source_layer IN ('spine', 'promoted')),
    scope          TEXT,
    content_hash   TEXT
);
CREATE INDEX IF NOT EXISTS entities_by_type ON entities(entity_type);

-- Surface forms, tagged with HOW each was obtained. alias_kind is load-bearing,
-- not descriptive: only 'canonical'/'acronym'/'variant' may drive resolution
-- (a frontmatter keyword dump names related terms as often as the note's own
-- entity, and folding it into exact resolution produced false links). 'keyword'
-- rows are retained for lexical/full-text use; 'exclusion' rows are a NEGATIVE
-- signal that blocks one (alias_norm, entity_id) pair.
CREATE TABLE IF NOT EXISTS entity_aliases (
    entity_id  TEXT NOT NULL REFERENCES entities(entity_id) ON DELETE CASCADE,
    alias      TEXT NOT NULL,
    alias_norm TEXT NOT NULL,
    alias_kind TEXT NOT NULL CHECK (
        alias_kind IN ('canonical', 'acronym', 'variant', 'keyword', 'exclusion')
    ),
    source     TEXT NOT NULL,
    PRIMARY KEY (entity_id, alias_norm, alias_kind)
);
CREATE INDEX IF NOT EXISTS entity_aliases_by_norm ON entity_aliases(alias_norm);

-- Surface forms observed in the corpus that are not (yet) canonical entities —
-- the promotion queue / ghost-note bridge. Demotable; authoritative only once a
-- defining note exists.
CREATE TABLE IF NOT EXISTS candidate_entities (
    candidate_id       TEXT PRIMARY KEY,
    surface_form       TEXT NOT NULL,
    surface_norm       TEXT NOT NULL,
    entity_type        TEXT,
    mention_count      INTEGER NOT NULL DEFAULT 0,
    distinct_notes     INTEGER NOT NULL DEFAULT 0,
    confidence         REAL,
    scope              TEXT,
    resolved_entity_id TEXT,
    status             TEXT NOT NULL DEFAULT 'candidate' CHECK (
        status IN ('candidate', 'linked', 'promoted', 'demoted')
    )
);
CREATE INDEX IF NOT EXISTS candidate_entities_by_norm ON candidate_entities(surface_norm);
"""
"""The registry-only tables: canonical entities, their aliases, the candidates."""

REGISTRY_SCHEMA: str = (
    WAL_PRAGMA + _REGISTRY_TABLES + "\n" + schema_section("tier_a_relations")
)
"""What :meth:`RegistryStore.open` applies — the registry tables plus Tier A.

The ``relations`` half is read from ``runtime/schema.sql`` rather than restated
here, so the sidecar and the runtime database cannot drift into two shapes of one
table again. The registry tables stay local because they exist only on the
sidecar; sharing a *file* is not the same as sharing a *lifetime*."""

AUTHORED_ORIGIN: str = "authored"
"""The only origin :meth:`RegistryStore.replace_authored_relations` will accept."""


class RegistryStoreError(RuntimeError):
    """A registry write that would corrupt the projection's layering."""


class RegistryStore:
    """Durable home for the entity registry and the Tier-A relations cache.

    Implements ``dks.entity_registry.RegistrySource`` (read) and
    ``RegistrySink`` (write). Constructed against a sidecar database path;
    :meth:`open` applies :data:`REGISTRY_SCHEMA` idempotently."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path).expanduser().resolve()

    @classmethod
    def open(cls, path: Path | str) -> "RegistryStore":
        """Create (or attach to) the sidecar registry DB and apply the schema."""
        store = cls(path)
        store.path.parent.mkdir(parents=True, exist_ok=True)
        with store._connect() as conn:
            conn.executescript(REGISTRY_SCHEMA)
        return store

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=2.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 2000")
        return conn

    # ── write side (RegistrySink) ───────────────────────────────────────────

    def replace_spine(
        self,
        entities: Sequence[Entity],
        aliases: Sequence[EntityAlias],
    ) -> int:
        """Rebuild the spine layer (and its aliases) idempotently.

        Scoped to ``source_layer='spine'`` so a promoted entity survives a
        reseed. Returns the number of entities written."""
        spine = [e for e in entities if e.source_layer == "spine"]
        spine_ids = {e.entity_id for e in spine}
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute(
                "DELETE FROM entity_aliases WHERE entity_id IN "
                "(SELECT entity_id FROM entities WHERE source_layer = 'spine')"
            )
            conn.execute("DELETE FROM entities WHERE source_layer = 'spine'")
            conn.executemany(
                """
                INSERT OR REPLACE INTO entities(
                    entity_id, canonical_name, entity_type, note_id, file_path,
                    folgezettel, source_layer, scope, content_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        e.entity_id, e.canonical_name, e.entity_type, e.note_id,
                        e.file_path, e.folgezettel, e.source_layer, e.scope,
                        e.content_hash,
                    )
                    for e in sorted(spine, key=lambda e: e.entity_id)
                ],
            )
            conn.executemany(
                """
                INSERT OR IGNORE INTO entity_aliases(
                    entity_id, alias, alias_norm, alias_kind, source
                ) VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (a.entity_id, a.alias, a.alias_norm, a.alias_kind, a.source)
                    for a in sorted(aliases, key=lambda a: (a.entity_id, a.alias_norm))
                    if a.entity_id in spine_ids
                ],
            )
        return len(spine)

    def replace_candidates(self, candidates: Sequence[CandidateEntity]) -> int:
        """Rebuild the candidate/promotion-queue layer. Returns rows written."""
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute("DELETE FROM candidate_entities")
            conn.executemany(
                """
                INSERT OR REPLACE INTO candidate_entities(
                    candidate_id, surface_form, surface_norm, entity_type,
                    mention_count, distinct_notes, confidence, scope,
                    resolved_entity_id, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        c.candidate_id, c.surface_form, c.surface_norm, c.entity_type,
                        c.mention_count, c.distinct_notes, c.confidence, c.scope,
                        c.resolved_entity_id, c.status,
                    )
                    for c in sorted(candidates, key=lambda c: c.candidate_id)
                ],
            )
        return len(candidates)

    def replace_authored_relations(self, rows: Sequence[AuthoredRelation]) -> int:
        """Rebuild ONLY the ``origin='authored'`` layer of the relations cache.

        Raises:
            RegistryStoreError: when a row carries a non-authored origin. The
                authored seed is a projection of frontmatter; letting a resolved
                row in through this door would make the seed un-rebuildable and
                the origin column a lie.
        """
        foreign = [r.relation_id for r in rows if r.origin != AUTHORED_ORIGIN]
        if foreign:
            raise RegistryStoreError(
                f"replace_authored_relations accepts origin={AUTHORED_ORIGIN!r} only; "
                f"refused {len(foreign)} row(s), first={foreign[0]!r}"
            )
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            # scoped delete: query-derived rows layer on top of the seed and
            # must survive a reseed.
            conn.execute("DELETE FROM relations WHERE origin = ?", (AUTHORED_ORIGIN,))
            conn.executemany(
                """
                INSERT OR REPLACE INTO relations(
                    relation_id, subject_id, predicate, object_ref, object_kind,
                    valid_from, valid_to, evidence_note, evidence_locator,
                    epistemic_status, origin, superseded_by, content_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        r.relation_id, r.subject_id, r.predicate, r.object_ref,
                        r.object_kind, r.valid_from, r.valid_to, r.evidence_note,
                        r.evidence_locator, r.epistemic_status, r.origin,
                        r.superseded_by, r.content_hash,
                    )
                    for r in sorted(rows, key=lambda r: r.relation_id)
                ],
            )
        return len(rows)

    def put_meta(self, key: str, value: str) -> None:
        """Record one build-provenance fact (never a content fact)."""
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute(
                "INSERT OR REPLACE INTO registry_meta(key, value) VALUES (?, ?)",
                (key, value),
            )

    # ── read side (RegistrySource) ──────────────────────────────────────────

    def load_registry(self) -> EntityRegistry:
        """Load the whole registry — every alias kind included.

        Retain broadly, resolve narrowly: the keyword aliases come back here for
        lexical use, and
        :meth:`~tessellum.dks.entity_registry.EntityRegistry.resolution_index`
        is what filters them out of resolution."""
        with self._connect() as conn:
            entity_rows = conn.execute(
                "SELECT * FROM entities ORDER BY entity_id"
            ).fetchall()
            alias_rows = conn.execute(
                "SELECT * FROM entity_aliases ORDER BY entity_id, alias_norm, alias_kind"
            ).fetchall()
            candidate_rows = conn.execute(
                "SELECT * FROM candidate_entities ORDER BY candidate_id"
            ).fetchall()
        return EntityRegistry(
            entities=tuple(
                Entity(
                    entity_id=row["entity_id"],
                    canonical_name=row["canonical_name"],
                    entity_type=row["entity_type"],
                    note_id=row["note_id"],
                    file_path=row["file_path"],
                    folgezettel=row["folgezettel"],
                    source_layer=row["source_layer"],
                    scope=row["scope"] or "",
                    content_hash=row["content_hash"],
                )
                for row in entity_rows
            ),
            aliases=tuple(
                EntityAlias(
                    entity_id=row["entity_id"],
                    alias=row["alias"],
                    alias_kind=row["alias_kind"],
                    source=row["source"],
                )
                for row in alias_rows
            ),
            candidates=tuple(
                CandidateEntity(
                    candidate_id=row["candidate_id"],
                    surface_form=row["surface_form"],
                    surface_norm=row["surface_norm"],
                    entity_type=row["entity_type"] or "",
                    mention_count=row["mention_count"],
                    distinct_notes=row["distinct_notes"],
                    confidence=row["confidence"] or 0.0,
                    scope=row["scope"] or "",
                    resolved_entity_id=row["resolved_entity_id"],
                    status=row["status"],
                )
                for row in candidate_rows
            ),
        )

    def relations_for(
        self,
        subject_id: str,
        predicate: str | None = None,
    ) -> tuple[AuthoredRelation, ...]:
        """Read the CURRENT authored relations for one subject.

        Reads BY SUBJECT — the access pattern the Tier-A cache exists for — and
        filters out superseded rows so a role query cannot return a former
        holder. Never enumerates across subjects."""
        sql = (
            "SELECT * FROM relations WHERE subject_id = ? AND origin = ? "
            "AND superseded_by IS NULL"
        )
        params: list[str] = [subject_id, AUTHORED_ORIGIN]
        if predicate is not None:
            sql += " AND predicate = ?"
            params.append(predicate)
        sql += " ORDER BY relation_id"
        with self._connect() as conn:
            rows = conn.execute(sql, tuple(params)).fetchall()
        return tuple(
            AuthoredRelation(
                relation_id=row["relation_id"],
                subject_id=row["subject_id"],
                predicate=row["predicate"],
                object_ref=row["object_ref"],
                object_kind=row["object_kind"],
                evidence_note=row["evidence_note"],
                evidence_locator=row["evidence_locator"],
                valid_from=row["valid_from"],
                valid_to=row["valid_to"],
                epistemic_status=row["epistemic_status"] or "",
                superseded_by=row["superseded_by"],
                content_hash=row["content_hash"],
            )
            for row in rows
        )

    def meta(self) -> dict[str, str]:
        """Every recorded build-provenance fact."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT key, value FROM registry_meta ORDER BY key"
            ).fetchall()
        return {row["key"]: row["value"] for row in rows}

    def content_digest(self) -> str:
        """Order-invariant digest of registry + relations content (no meta).

        The determinism contract: the same notes, projected and stored twice,
        yield the same digest. Build timestamps live in ``registry_meta`` and are
        deliberately excluded."""
        with self._connect() as conn:
            relations = conn.execute(
                """
                SELECT relation_id, subject_id, predicate, object_ref, object_kind,
                       COALESCE(valid_from, ''), COALESCE(valid_to, ''),
                       evidence_note, evidence_locator, origin
                FROM relations ORDER BY relation_id
                """
            ).fetchall()
        digest = hashlib.sha256()
        digest.update(registry_content_digest(self.load_registry()).encode("utf-8"))
        digest.update(repr([tuple(row) for row in relations]).encode("utf-8"))
        return digest.hexdigest()


__all__ = [
    "AUTHORED_ORIGIN",
    "REGISTRY_SCHEMA",
    "RegistryStore",
    "RegistryStoreError",
]
