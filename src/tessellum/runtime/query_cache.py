"""Tier-B query cache + feedback log, and the Tier-A resolved rows (P9 storage).

The runtime half of the query-time DKS plan's memory tiers. ``dks.memory_tiers``
defines the tier vocabulary, the reliability arithmetic and the ports
(:class:`~tessellum.dks.memory_tiers.QueryCacheSource` read /
:class:`~tessellum.dks.memory_tiers.FeedbackSink` write /
:class:`~tessellum.dks.memory_tiers.VerdictSource` adapter) and stays pure; this
module is the only place those tiers touch a disk, which is what keeps the
Dependency Rule intact.

**Both tables here are REBUILDABLE PROJECTIONS, and both are evictable.**

* ``query_cache`` is a projection of derivations that already happened. Drop it
  and the next query re-derives: the cost is latency and target-note precision,
  never knowledge.
* ``feedback`` is a projection of a deployment's own review stream, re-ingestible
  through :meth:`QueryCacheStore.ingest_verdicts` because every event is content
  addressed. Drop it and η falls back to its fail-closed prior.

That is why this module contains ``DELETE`` and ``UPDATE`` statements while
``runtime.claim_log`` contains none, and the difference is not a relaxation of
the append-only rule: it is the rule applied to the right object. The claim/edge
log is of-record, so a correction there is a further append. A cache that could
not be evicted would be a second source of truth nobody can rebuild.

**Demotion first — the guard this phase exists for.** A negative verdict lowers a
mapping's standing and, at the floor, evicts it; that path is unconditional.
Reinforcement is gated by
:attr:`~tessellum.dks.memory_tiers.FeedbackPolicy.reinforcement_enabled`, which is
``False`` by default, so the reinforcement path ships second. The asymmetry is
the point: a memory that can only be reinforced entrenches a wrong mapping,
because every episode that used it reads as evidence for it.

Two further layering rules the write API enforces rather than documents:

- :meth:`QueryCacheStore.put_mapping` never RAISES an existing mapping's score
  (it keeps the lower of the two), so re-deriving is not a way to launder away a
  demotion. Restoring full standing takes an explicit :meth:`evict`.
- :meth:`QueryCacheStore.record_resolved_relation` refuses any row whose origin
  is not ``resolved``, and :meth:`evict_resolved_relations` scopes its delete the
  same way — so the ``origin='authored'`` seed the registry projects is neither
  written through this door nor deleted through it. It is the mirror image of the
  registry store's refusal, and together they keep the two Tier-A layers honest.

The ``relations`` table is **not defined here**: it is the Tier-A cache the
runtime schema owns, and this module writes only its ``origin='resolved'`` layer.
:data:`QUERY_CACHE_SCHEMA` still covers the two Tier-B tables only, but it is now
*read out of* ``runtime/schema.sql`` (the ``tier_b_query_cache`` section) rather
than restated here — one home for the DDL, applied narrowly by the consumer that
may be opened on either database. Tier A likewise has a single definition now, so
:meth:`_relations_columns` has stopped being a shape-discovery probe and is only
a presence check.

Purely additive: nothing on an existing code path calls this module, and no
behaviour it adds is on by default.
"""

from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import replace
from pathlib import Path
from typing import Sequence

from tessellum.dks.memory_tiers import (
    DEFAULT_FEEDBACK_POLICY,
    INITIAL_FEEDBACK_SCORE,
    RESOLVED_ORIGIN,
    SOURCE_REVIEWED_QA,
    CachedMapping,
    CachePrecisionComparison,
    CorrectionFlag,
    FeedbackEvent,
    FeedbackPolicy,
    PrecisionProbe,
    ResolvedRelation,
    SubjectKind,
    TrialHistory,
    Verdict,
    VerdictOutcome,
    VerdictSource,
    compare_target_note_precision,
)
from tessellum.dks.memory_tiers import correction_flags as _correction_flags
from tessellum.dks.memory_tiers import open_correction_flags as _open_correction_flags
from tessellum.dks.memory_tiers import score_after, tally_trials
from tessellum.runtime.schema import schema_section

QUERY_CACHE_SCHEMA: str = schema_section("tier_b_query_cache", with_pragma=True)
"""The Tier-B DDL, read from the ``tier_b_query_cache`` section of ``schema.sql``.

Applied on whichever database this store is opened against, which is why it is a
section rather than the whole file: a sidecar registry database has no business
growing a job queue, and this store has no business defining Tier A."""

_RELATION_PAYLOAD_ORDER = (
    "relation_id",
    "subject_id",
    "predicate",
    "object_ref",
    "object_kind",
    "valid_from",
    "valid_to",
    "evidence_note",
    "evidence_locator",
    "epistemic_status",
    "origin",
    "superseded_by",
    "content_hash",
)


class QueryCacheError(RuntimeError):
    """A Tier-A/Tier-B write that would corrupt a projection's layering."""


class QueryCacheStore:
    """Durable home for the Tier-B cache, its feedback log, and Tier-A's
    ``origin='resolved'`` rows.

    Implements ``dks.memory_tiers.QueryCacheSource`` (read) and ``FeedbackSink``
    (write). Constructed against a database path; :meth:`open` applies
    :data:`QUERY_CACHE_SCHEMA` idempotently. Resolved-relation writes need the
    Tier-A ``relations`` table on that SAME file, so a deployment opens this
    store on whichever database owns it."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path).expanduser().resolve()

    @classmethod
    def open(cls, path: Path | str) -> "QueryCacheStore":
        """Create (or attach to) the database and apply the two new tables."""
        store = cls(path)
        store.path.parent.mkdir(parents=True, exist_ok=True)
        with store._connect() as conn:
            conn.executescript(QUERY_CACHE_SCHEMA)
        return store

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=2.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 2000")
        return conn

    # ── Tier B: the cache (QueryCacheSource) ────────────────────────────────

    def put_mapping(
        self,
        query_key: str,
        target_note_ids: Sequence[str],
        *,
        query_embedding: bytes | None = None,
        feedback_score: float = INITIAL_FEEDBACK_SCORE,
        now: float | None = None,
    ) -> CachedMapping:
        """Write the mapping a cache MISS just derived.

        A re-put keeps the existing row's ``hits`` and ``created_at``, and takes
        the LOWER of the two feedback scores. That second rule is the demotion
        guard: re-deriving the same mapping must not be a way to launder away a
        demotion, or a wrong mapping recovers full standing on its next miss.
        Restoring standing takes an explicit :meth:`evict` first.
        """
        timestamp = time.time() if now is None else now
        targets = tuple(target_note_ids)
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            existing = _mapping_row(conn, query_key)
            if existing is None:
                record = CachedMapping(
                    query_key=query_key,
                    target_note_ids=targets,
                    feedback_score=feedback_score,
                    hits=0,
                    last_used=None,
                    query_embedding=query_embedding,
                    created_at=timestamp,
                )
                conn.execute(
                    """
                    INSERT INTO query_cache(
                        query_key, query_embedding, target_note_ids,
                        feedback_score, hits, last_used, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.query_key,
                        record.query_embedding,
                        json.dumps(list(record.target_note_ids)),
                        record.feedback_score,
                        record.hits,
                        record.last_used,
                        record.created_at,
                    ),
                )
                return record
            record = CachedMapping(
                query_key=query_key,
                target_note_ids=targets,
                feedback_score=min(float(existing["feedback_score"]), feedback_score),
                hits=int(existing["hits"]),
                last_used=existing["last_used"],
                query_embedding=(
                    existing["query_embedding"]
                    if query_embedding is None
                    else query_embedding
                ),
                created_at=float(existing["created_at"]),
            )
            conn.execute(
                """
                UPDATE query_cache
                   SET query_embedding = ?, target_note_ids = ?, feedback_score = ?
                 WHERE query_key = ?
                """,
                (
                    record.query_embedding,
                    json.dumps(list(record.target_note_ids)),
                    record.feedback_score,
                    query_key,
                ),
            )
            return record

    def cached_targets(self, query_key: str) -> CachedMapping | None:
        """The read port: the cached mapping for ``query_key``, or ``None``."""
        with self._connect() as conn:
            row = _mapping_row(conn, query_key)
        return None if row is None else _row_to_mapping(row)

    def record_hit(
        self,
        query_key: str,
        *,
        episode_id: str | None = None,
        now: float | None = None,
    ) -> CachedMapping | None:
        """Count one use of a cached mapping. ``None`` means it was a miss.

        Passing ``episode_id`` also appends a ``trial`` event, which is what
        makes the use countable later: without it the episode is invisible to
        the coverage figure, and a verdict arriving afterwards would be the only
        trace that the mapping was ever consulted."""
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = _mapping_row(conn, query_key)
            if row is None:
                return None
            conn.execute(
                "UPDATE query_cache SET hits = hits + 1, last_used = ? WHERE query_key = ?",
                (timestamp, query_key),
            )
            if episode_id is not None:
                self._append(
                    conn,
                    FeedbackEvent(
                        kind="trial",
                        subject_id=query_key,
                        subject_kind="cached_mapping",
                        episode_id=episode_id,
                        at=timestamp,
                        source=SOURCE_REVIEWED_QA,
                    ),
                )
            updated = _mapping_row(conn, query_key)
            assert updated is not None
            return _row_to_mapping(updated)

    def mapping_count(self) -> int:
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) FROM query_cache").fetchone()
        return int(row[0])

    # ── Tier B: eviction (both tables are evictable) ────────────────────────

    def evict(self, query_key: str) -> bool:
        """Drop one cached mapping. Its feedback history deliberately survives.

        Returns whether a row was there to drop. The evidence outliving the row
        is what lets an eviction be audited — and what lets η stay computable for
        a subject whose mapping is gone."""
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            cursor = conn.execute(
                "DELETE FROM query_cache WHERE query_key = ?", (query_key,)
            )
            return cursor.rowcount > 0

    def evict_stale(
        self,
        *,
        unused_since: float | None = None,
        at_or_below_score: float | None = None,
    ) -> tuple[str, ...]:
        """Evict by age and/or standing. Returns the keys evicted, sorted.

        With neither bound this evicts nothing rather than everything: a
        no-argument call that emptied the cache is the kind of accident an
        eviction API should refuse to make easy. :meth:`drop_cache` is the
        explicit way to ask for that."""
        clauses: list[str] = []
        params: list[float] = []
        if unused_since is not None:
            clauses.append("(last_used IS NULL OR last_used < ?) AND created_at < ?")
            params.extend([unused_since, unused_since])
        if at_or_below_score is not None:
            clauses.append("feedback_score <= ?")
            params.append(at_or_below_score)
        if not clauses:
            return ()
        where = " OR ".join(f"({clause})" for clause in clauses)
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            rows = conn.execute(
                f"SELECT query_key FROM query_cache WHERE {where} ORDER BY query_key",
                tuple(params),
            ).fetchall()
            keys = tuple(row["query_key"] for row in rows)
            conn.execute(f"DELETE FROM query_cache WHERE {where}", tuple(params))
            return keys

    def drop_cache(self) -> int:
        """Drop the whole Tier-B cache. Returns the row count removed.

        The evictability proof, and a legitimate operation: this is a projection.
        What survives is the feedback log, so reliability and correction state are
        unchanged by it — the cost is latency and target-note precision only."""
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT COUNT(*) FROM query_cache").fetchone()
            conn.execute("DELETE FROM query_cache")
            return int(row[0])

    def evict_feedback_before(self, cutoff: float) -> int:
        """Drop feedback events older than ``cutoff``. Returns rows removed.

        The feedback table is a projection too — of the deployment's review
        stream — so it is evictable and re-ingestible. Evicting it narrows the
        evidence η is computed from, which widens η back toward its fail-closed
        prior rather than inventing confidence."""
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            cursor = conn.execute("DELETE FROM feedback WHERE at < ?", (cutoff,))
            return cursor.rowcount

    # ── Tier B: the feedback log (FeedbackSink) ─────────────────────────────

    def record_trial(
        self,
        *,
        subject_id: str,
        subject_kind: SubjectKind,
        episode_id: str,
        at: float | None = None,
    ) -> FeedbackEvent:
        """Record that one episode used ``subject_id`` — a trial, not a verdict."""
        timestamp = time.time() if at is None else at
        event = FeedbackEvent(
            kind="trial",
            subject_id=subject_id,
            subject_kind=subject_kind,
            episode_id=episode_id,
            at=timestamp,
        )
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            return self._append(conn, event)

    def apply_verdict(
        self,
        *,
        subject_id: str,
        subject_kind: SubjectKind,
        episode_id: str,
        verdict: Verdict,
        source: str = SOURCE_REVIEWED_QA,
        detail: str = "",
        at: float | None = None,
        policy: FeedbackPolicy | None = None,
    ) -> VerdictOutcome:
        """Record one verdict and act on it — the demotion path.

        A negative verdict lowers the mapping's score and, at the floor, evicts
        it; a positive one reinforces only when the policy says so, and holds
        otherwise (the default). A negative verdict also raises a correction
        flag, so the gate condition "no open correction flag" is driven by the
        same signal that demotes rather than by a separate, forgettable step.

        Replay is a no-op: an already-recorded event returns ``action='hold'``
        without touching the score, because ingesting the same verdict stream
        twice must not demote twice.
        """
        rules = DEFAULT_FEEDBACK_POLICY if policy is None else policy
        timestamp = time.time() if at is None else at
        event = FeedbackEvent(
            kind="verdict",
            subject_id=subject_id,
            subject_kind=subject_kind,
            episode_id=episode_id,
            at=timestamp,
            verdict=verdict,
            source=source,
            detail=detail,
        )
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            flag = FeedbackEvent(
                kind="correction_raise",
                subject_id=subject_id,
                subject_kind=subject_kind,
                episode_id=episode_id,
                at=timestamp,
                source=source,
                detail=f"negative verdict {verdict!r}: {detail}".strip(),
            )
            # A cached mapping is the only thing this call can score. A promoted
            # claim's subject id lives in another namespace, so it is never
            # looked up here even by coincidence.
            mapping = (
                _mapping_row(conn, subject_id)
                if subject_kind == "cached_mapping"
                else None
            )
            recorded = _event_row(conn, event.event_id)
            if recorded is not None:
                raised = _event_row(conn, flag.event_id)
                return VerdictOutcome(
                    event=_row_to_event(recorded),
                    action="hold",
                    reason="already recorded — replaying a verdict stream is a no-op",
                    previous_score=(
                        None if mapping is None else float(mapping["feedback_score"])
                    ),
                    score=None if mapping is None else float(mapping["feedback_score"]),
                    correction_flag_id=None if raised is None else flag.event_id,
                )
            stored = self._append(conn, event)
            flag_id: str | None = None
            if stored.is_negative and rules.raise_correction_on_negative:
                flag_id = self._append(conn, flag).event_id
            if mapping is None:
                # Nothing to score. For a promoted claim that is the normal case:
                # demotion there is the re-derivation gate's act (a retraction
                # appended to the claim log), and what this call contributes is
                # the trial count and the correction flag.
                return VerdictOutcome(
                    event=stored,
                    action="hold",
                    reason=f"no cached mapping to score for a {subject_kind!r} subject",
                    correction_flag_id=flag_id,
                )
            decision = score_after(
                float(mapping["feedback_score"]), verdict, policy=rules
            )
            evicted = False
            if decision.action == "evict":
                conn.execute(
                    "DELETE FROM query_cache WHERE query_key = ?", (subject_id,)
                )
                evicted = True
            elif decision.action in ("demote", "reinforce"):
                conn.execute(
                    "UPDATE query_cache SET feedback_score = ? WHERE query_key = ?",
                    (decision.score, subject_id),
                )
            return VerdictOutcome(
                event=stored,
                action=decision.action,
                reason=decision.reason,
                previous_score=decision.previous_score,
                score=decision.score,
                evicted=evicted,
                correction_flag_id=flag_id,
            )

    def ingest_verdicts(
        self,
        source: VerdictSource,
        *,
        since: float | None = None,
        policy: FeedbackPolicy | None = None,
    ) -> tuple[VerdictOutcome, ...]:
        """Pull a deployment's review stream through the adapter port.

        The stream is whatever a deployment already collects — reviewed
        question-and-answer verdicts, explicit thumbs — and this package ships no
        collector for it, only :class:`VerdictSource`. Verdict events are applied
        (and so can demote); trial and correction events are appended as they
        stand. Idempotent by content id, so re-pulling an overlapping window
        changes nothing."""
        outcomes: list[VerdictOutcome] = []
        for event in source.verdicts(since=since):
            if event.kind == "verdict":
                assert event.verdict is not None  # FeedbackEvent guarantees it
                outcomes.append(
                    self.apply_verdict(
                        subject_id=event.subject_id,
                        subject_kind=event.subject_kind,
                        episode_id=event.episode_id,
                        verdict=event.verdict,
                        source=event.source,
                        detail=event.detail,
                        at=event.at,
                        policy=policy,
                    )
                )
                continue
            with self._connect() as conn:
                conn.execute("BEGIN IMMEDIATE")
                self._append(conn, event)
        return tuple(outcomes)

    def raise_correction(
        self,
        *,
        subject_id: str,
        subject_kind: SubjectKind,
        episode_id: str,
        reason: str = "",
        source: str = SOURCE_REVIEWED_QA,
        at: float | None = None,
    ) -> CorrectionFlag:
        """Flag a subject as reported-wrong, without waiting for a verdict."""
        timestamp = time.time() if at is None else at
        event = FeedbackEvent(
            kind="correction_raise",
            subject_id=subject_id,
            subject_kind=subject_kind,
            episode_id=episode_id,
            at=timestamp,
            source=source,
            detail=reason,
        )
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            stored = self._append(conn, event)
        return CorrectionFlag(
            flag_id=stored.event_id,
            subject_id=stored.subject_id,
            subject_kind=stored.subject_kind,
            episode_id=stored.episode_id,
            raised_at=stored.at,
            reason=stored.detail,
        )

    def release_correction(
        self, flag_id: str, *, detail: str = "", at: float | None = None
    ) -> FeedbackEvent:
        """Close one raised flag by appending the event that releases it.

        The flag is never overwritten: an open flag and a released one are two
        rows, so "this was reported wrong and then cleared" stays readable."""
        timestamp = time.time() if at is None else at
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            raised = _event_row(conn, flag_id)
            if raised is None or raised["kind"] != "correction_raise":
                raise QueryCacheError(f"not a raised correction flag: {flag_id!r}")
            return self._append(
                conn,
                FeedbackEvent(
                    kind="correction_release",
                    subject_id=raised["subject_id"],
                    subject_kind=raised["subject_kind"],
                    episode_id=raised["episode_id"],
                    at=timestamp,
                    source=raised["source"],
                    detail=detail,
                    releases=flag_id,
                ),
            )

    # ── Tier B: reads over the feedback log ─────────────────────────────────

    def events(self, *, subject_id: str | None = None) -> tuple[FeedbackEvent, ...]:
        """Every recorded event, in append order — the input to every tally."""
        sql = "SELECT * FROM feedback"
        params: tuple[str, ...] = ()
        if subject_id is not None:
            sql += " WHERE subject_id = ?"
            params = (subject_id,)
        sql += " ORDER BY seq"
        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return tuple(_row_to_event(row) for row in rows)

    def trial_history(
        self, subject_id: str, *, subject_kind: str | None = None
    ) -> TrialHistory:
        """The counts η needs, tallied by the pure kernel function."""
        return tally_trials(
            self.events(subject_id=subject_id),
            subject_id=subject_id,
            subject_kind=subject_kind,
        )

    def reliability(self, subject_id: str, *, subject_kind: str | None = None) -> float:
        """η = (n_pass + 1) / (n_trial + 2) for one subject's real history."""
        return self.trial_history(subject_id, subject_kind=subject_kind).eta

    def correction_flags(
        self, *, subject_id: str | None = None
    ) -> tuple[CorrectionFlag, ...]:
        """Every flag, open or released — the audit trail behind a demotion."""
        return _correction_flags(
            self.events(subject_id=subject_id), subject_id=subject_id
        )

    def has_open_correction(self, subject_id: str) -> bool:
        """The gate's second condition, read from real state."""
        return bool(
            _open_correction_flags(
                self.events(subject_id=subject_id), subject_id=subject_id
            )
        )

    # ── Tier A: the resolved rows, layered on the authored seed ─────────────

    def record_resolved_relation(self, row: ResolvedRelation) -> str:
        """Write one ``origin='resolved'`` Tier-A row on a cache miss.

        Idempotent by content id, so a replayed derivation lands on the same
        row. Column-projected onto whatever ``relations`` shape the opened
        database has (see :meth:`_relations_columns`).

        Raises:
            QueryCacheError: when the row's origin is not ``resolved`` (the
                authored seed is a projection of frontmatter and must not be
                written through this door), or when the Tier-A table is absent.
        """
        if row.origin != RESOLVED_ORIGIN:
            raise QueryCacheError(
                f"record_resolved_relation accepts origin={RESOLVED_ORIGIN!r} only; "
                f"refused {row.relation_id!r} with origin={row.origin!r}"
            )
        payload = {
            "relation_id": row.relation_id,
            "subject_id": row.subject_id,
            "predicate": row.predicate,
            "object_ref": row.object_ref,
            "object_kind": row.object_kind,
            "valid_from": row.valid_from,
            "valid_to": row.valid_to,
            "evidence_note": row.evidence_note,
            "evidence_locator": row.evidence_locator,
            "epistemic_status": row.epistemic_status,
            "origin": row.origin,
            "superseded_by": row.superseded_by,
            "content_hash": row.content_hash,
        }
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            columns = self._relations_columns(conn)
            written = tuple(
                name for name in _RELATION_PAYLOAD_ORDER if name in columns
            )
            conn.execute(
                f"INSERT OR REPLACE INTO relations({', '.join(written)}) "
                f"VALUES ({', '.join('?' * len(written))})",
                tuple(payload[name] for name in written),
            )
        return row.relation_id

    def resolved_relations_for(
        self, subject_id: str, predicate: str | None = None
    ) -> tuple[ResolvedRelation, ...]:
        """Read the CURRENT resolved relations for one subject.

        Reads BY SUBJECT — the access pattern the Tier-A cache exists for, and
        the one the scaling bound permits — and filters superseded rows out so a
        role-style query cannot return a former holder. Never enumerates across
        subjects."""
        sql = (
            "SELECT * FROM relations WHERE subject_id = ? AND origin = ? "
            "AND superseded_by IS NULL"
        )
        params: list[str] = [subject_id, RESOLVED_ORIGIN]
        if predicate is not None:
            sql += " AND predicate = ?"
            params.append(predicate)
        sql += " ORDER BY relation_id"
        with self._connect() as conn:
            columns = self._relations_columns(conn)
            rows = conn.execute(sql, tuple(params)).fetchall()
        return tuple(_row_to_resolved(row, columns) for row in rows)

    def supersede_resolved_relation(
        self, relation_id: str, *, superseded_by: str
    ) -> bool:
        """Point one resolved row at the row that replaced it.

        The recency half of Tier A: a newer derivation does not delete the older
        row, it supersedes it, and :meth:`resolved_relations_for` then stops
        returning the former value. Scoped to ``origin='resolved'``, so an
        authored row cannot be superseded through this door — the authored layer
        is rebuilt from frontmatter, never patched from query traffic. Returns
        whether a resolved row was there to update."""
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            self._relations_columns(conn)
            cursor = conn.execute(
                "UPDATE relations SET superseded_by = ? "
                "WHERE relation_id = ? AND origin = ?",
                (superseded_by, relation_id, RESOLVED_ORIGIN),
            )
            return cursor.rowcount > 0

    def evict_resolved_relations(self, *, subject_id: str | None = None) -> int:
        """Evict resolved Tier-A rows. Scoped to ``origin='resolved'``.

        The mirror image of the registry store's authored-scoped rebuild: the
        authored seed survives this, exactly as resolved rows survive a reseed.
        Returns rows removed."""
        sql = "DELETE FROM relations WHERE origin = ?"
        params: list[str] = [RESOLVED_ORIGIN]
        if subject_id is not None:
            sql += " AND subject_id = ?"
            params.append(subject_id)
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            self._relations_columns(conn)
            cursor = conn.execute(sql, tuple(params))
            return cursor.rowcount

    def _relations_columns(self, conn: sqlite3.Connection) -> frozenset[str]:
        """The Tier-A table's actual columns — and the check that it exists.

        There is now ONE ``relations`` definition (the ``tier_a_relations``
        section of ``runtime/schema.sql``, applied to both the runtime database
        and the registry sidecar), so this is a presence-and-drift check rather
        than the shape discovery it began as: the payload is still projected onto
        the columns actually found, so an older file opened after a schema change
        is reported here as drift instead of surfacing as an integrity error from
        three frames down."""
        rows = conn.execute("PRAGMA table_info(relations)").fetchall()
        if not rows:
            raise QueryCacheError(
                f"the Tier-A 'relations' table is not present on {self.path}: apply the "
                "runtime schema (or the registry sidecar schema) on this database "
                "first — this module deliberately does not define that table"
            )
        columns = frozenset(row["name"] for row in rows)
        required = {
            row["name"]
            for row in rows
            if row["notnull"] and row["dflt_value"] is None and not row["pk"]
        }
        missing = required - set(_RELATION_PAYLOAD_ORDER)
        if missing:
            raise QueryCacheError(
                "the Tier-A 'relations' table requires column(s) this module does not "
                f"supply: {', '.join(sorted(missing))}"
            )
        return columns

    # ── the measurement harness ────────────────────────────────────────────

    def measure_target_note_precision(
        self, probes: Sequence[PrecisionProbe]
    ) -> CachePrecisionComparison:
        """Target-note precision with vs. without the cache, over live rows.

        Fills each probe's cached arm from this store (``None`` for a miss, which
        the comparison resolves by falling through to the uncached arm, as a real
        miss does) and delegates the arithmetic to the pure comparator. The
        returned ``delta`` is signed, so a cache that *lowers* precision shows up
        as a negative number rather than as an unstated regression."""
        return compare_target_note_precision(
            tuple(
                probe.with_cached(
                    None
                    if (mapping := self.cached_targets(probe.query_key)) is None
                    else mapping.target_note_ids
                )
                for probe in probes
            )
        )

    # ── the single append primitive ─────────────────────────────────────────

    def _append(
        self, conn: sqlite3.Connection, event: FeedbackEvent
    ) -> FeedbackEvent:
        """Insert one feedback event at the next log position. INSERT only.

        An event whose content id is already present consumes no position and
        its stored record is returned instead, which is what makes re-ingesting a
        verdict stream a no-op."""
        existing = _event_row(conn, event.event_id)
        if existing is not None:
            return _row_to_event(existing)
        seq = _next_seq(conn)
        conn.execute(
            """
            INSERT INTO feedback(
                feedback_id, kind, subject_id, subject_kind, episode_id,
                verdict, source, detail, releases, at, seq
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.event_id,
                event.kind,
                event.subject_id,
                event.subject_kind,
                event.episode_id,
                event.verdict,
                event.source,
                event.detail,
                event.releases,
                event.at,
                seq,
            ),
        )
        return replace(event, seq=seq)


# ── row helpers ─────────────────────────────────────────────────────────────


def _mapping_row(conn: sqlite3.Connection, query_key: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM query_cache WHERE query_key = ?", (query_key,)
    ).fetchone()


def _event_row(conn: sqlite3.Connection, feedback_id: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM feedback WHERE feedback_id = ?", (feedback_id,)
    ).fetchone()


def _next_seq(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COALESCE(MAX(seq), 0) FROM feedback").fetchone()
    return int(row[0]) + 1


def _row_to_mapping(row: sqlite3.Row) -> CachedMapping:
    return CachedMapping(
        query_key=row["query_key"],
        target_note_ids=tuple(json.loads(row["target_note_ids"])),
        feedback_score=float(row["feedback_score"]),
        hits=int(row["hits"]),
        last_used=row["last_used"],
        query_embedding=row["query_embedding"],
        created_at=float(row["created_at"]),
    )


def _row_to_event(row: sqlite3.Row) -> FeedbackEvent:
    return FeedbackEvent(
        kind=row["kind"],
        subject_id=row["subject_id"],
        subject_kind=row["subject_kind"],
        episode_id=row["episode_id"],
        at=float(row["at"]),
        verdict=row["verdict"],
        source=row["source"],
        detail=row["detail"],
        releases=row["releases"],
        seq=int(row["seq"]),
    )


def _row_to_resolved(row: sqlite3.Row, columns: frozenset[str]) -> ResolvedRelation:
    """Read one resolved row back, tolerating either ``relations`` shape."""

    def text(name: str) -> str | None:
        return row[name] if name in columns else None

    return ResolvedRelation(
        subject_id=row["subject_id"],
        predicate=row["predicate"],
        object_ref=row["object_ref"],
        object_kind="entity" if text("object_kind") == "entity" else "literal",
        evidence_note=text("evidence_note") or "",
        evidence_locator=text("evidence_locator") or "",
        valid_from=text("valid_from"),
        valid_to=text("valid_to"),
        epistemic_status=text("epistemic_status") or "",
        superseded_by=text("superseded_by"),
        content_hash=text("content_hash"),
    )


__all__ = [
    "QUERY_CACHE_SCHEMA",
    "QueryCacheError",
    "QueryCacheStore",
]
