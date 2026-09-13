"""Append-only claim/edge log — the of-record tier of the memory stack.

P3 of the query-time protocol plan. The log holds two kinds of immutable
record — a *claim* (a declarative sentence plus a locator) and an *operator
edge* (one of exactly four epistemic operators) — and nothing else. Three
properties are load-bearing:

* **Append is the only write.** There is no rewrite path and no removal path in
  this module: a correction is a further append. Every row, once written, is
  final.
* **The graph is exactly the fold of the log.** :func:`fold_log` is a pure
  function from records to an edge set, so no edge can exist that no record
  produced. The consequence is that an operator may never *infer* an edge:
  ``revise`` re-logs the supports it keeps and logs the attacks it carries,
  because auto-inheritance would fabricate epistemic acts that nobody
  performed.
* **Status is computed, never stored here.** The four statuses
  (proposed / challenged / warranted / superseded) are a pure function of the
  folded edge set. This module supplies the fold, the ``attack``-only
  projection, the ``supersede`` pre-filter and the edge-set digest that keys the
  cache; the labelling itself belongs to the status phase and is deliberately
  absent.

:func:`operator_for_legacy_relation` is the retirement adapter: the argument
relation labels and the warrant change kinds collapse onto the four operators
here rather than becoming further relation vocabularies at the log's edge.

Storage lives in ``runtime`` by the Dependency Rule — the reasoning kernel
proposes effects and never writes — so this module is where the claim/edge
tables are appended to, under the same ``BEGIN IMMEDIATE`` single-writer
transaction the job queue uses. It is purely additive: nothing on an existing
code path calls it, and the protocol port that will (with its admission gate on
locators, operator labels and claim-eligibility) is a later phase.
"""

from __future__ import annotations

import hashlib
import sqlite3
import time
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Iterable, Literal, Sequence

if TYPE_CHECKING:  # pragma: no cover - typing only, no runtime import cost
    from tessellum.runtime.store import RuntimeStore


class ClaimLogError(RuntimeError):
    pass


# ── the closed vocabularies ─────────────────────────────────────────────────

Operator = Literal["support", "attack", "revise", "supersede"]
"""The only fixed relation vocabulary in the system — four epistemic operators.

Domain relations ("X is owned by Y") are *claims*, never edges, so no domain
predicate ever appears here. Mirrored by a CHECK constraint on ``edges.op``.
"""

OPERATORS: frozenset[str] = frozenset({"support", "attack", "revise", "supersede"})

Provenance = Literal["stub", "constructed"]
"""How a claim arrived: mechanically located placeholder, or stated after reading.

A status computed over a ``stub`` is provisional, which is why ``stub`` is the
conservative default in both the draft and the column.
"""

PROVENANCES: frozenset[str] = frozenset({"stub", "constructed"})

ORIGIN_PROJECTED = "projected"
"""An act read off authored structure."""

ORIGIN_QUERY = "query"
"""An act derived and verified at read time."""

ORIGIN_REASSERTED = "reasserted"
"""A support KEPT across a revise — re-logged, never inherited."""

ORIGIN_CARRIED = "carried"
"""An attack carried onto a revision — logged, and still awaiting discharge."""


_LEGACY_RELATIONS: dict[str, Operator] = {
    # The argument-graph relation labels the four operators replace. `rebuts`
    # and `undercuts` are two ways of attacking, and the log's vocabulary is
    # exactly four, so both collapse onto `attack`; the distinction they carried
    # belongs in the attacking claim's TEXT and its evidence locator, not in a
    # fifth edge label.
    "supports": "support",
    "attacks": "attack",
    "rebuts": "attack",
    "undercuts": "attack",
    # The warrant-level change kinds. These stay valid FOR WARRANTS — a warrant
    # is a rule with its own lifecycle — but a change to a CLAIM is an operator
    # edge, and this is the mapping onto it. `added` has no operator: asserting
    # a claim is logging the claim, not an edge about it.
    "revised": "revise",
    "superseded": "supersede",
}


def operator_for_legacy_relation(relation: str) -> Operator | None:
    """Map a retired relation label onto one of the four operators.

    The retirement adapter: rather than letting the argument-graph relation
    labels and the warrant change kinds become a fifth and sixth relation
    vocabulary at the log's edge, every legacy label collapses here onto the
    single closed set. Returns ``None`` for a label with no operator reading
    (``added``, and anything unrecognised), so a caller must decide explicitly
    rather than receiving a silently plausible default.
    """
    return _LEGACY_RELATIONS.get(relation)


# ── content identity ────────────────────────────────────────────────────────


def _content_id(*parts: str | None) -> str:
    """``sha256`` over NUL-joined parts — the store's 64-hex convention."""
    raw = "\0".join("" if part is None else part for part in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def text_digest(text: str) -> str:
    """``text_hash`` for a claim: a change here is a MATERIAL change."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def claim_identity(derivation_id: str, text_hash: str) -> str:
    """The log's content address for a claim.

    ``derivation_id`` is the deterministic identity of the derivation itself
    (``hash(note_id, span_locator)``, supplied by the caller — the identity
    phase owns its construction), and it is PRESERVED across a revision.
    Folding ``text_hash`` in gives the revision its own row while keeping the
    two rows joinable on one derivation, which is what makes recurrence
    countable. Identical inputs therefore replay onto the same row.
    """
    return _content_id(derivation_id, text_hash)


def edge_identity(
    op: str, src: str, dst: str, evidence_locator: str | None = None
) -> str:
    """The log's content address for an operator edge — so replays dedup."""
    return _content_id(op, src, dst, evidence_locator)


def edgeset_digest(edges: Iterable["EdgeRecord"]) -> str:
    """Digest of an edge SET, order-independent — the status cache's key.

    Every append yields a new digest, so a cached labelling is keyed to the
    exact edge set it was computed over and a stale entry is simply never read
    again (no invalidation write is needed, which is what keeps the cache
    compatible with an append-only log).
    """
    return _content_id(*sorted(edge.edge_id for edge in edges))


# ── records ─────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ClaimRecord:
    """One immutable ``claims`` row.

    ``seq`` is the record's position in the single log order shared with
    :class:`EdgeRecord`; ``created_at`` is epoch seconds, matching the rest of
    the runtime tables.
    """

    claim_id: str
    derivation_id: str
    text: str
    note_id: str
    locator: str | None
    provenance: str
    source_note_hash: str | None
    text_hash: str
    seq: int
    created_at: float


@dataclass(frozen=True)
class EdgeRecord:
    """One immutable ``edges`` row — a single epistemic act."""

    edge_id: str
    op: str
    src: str
    dst: str
    evidence_locator: str | None
    origin: str
    seq: int
    created_at: float


@dataclass(frozen=True)
class ClaimDraft:
    """A claim to append. Its ``claim_id`` is content-derived, so it is known
    before the write and a replay is a no-op rather than a duplicate."""

    derivation_id: str
    text: str
    note_id: str
    locator: str | None = None
    provenance: str = "stub"
    source_note_hash: str | None = None

    @property
    def text_hash(self) -> str:
        return text_digest(self.text)

    @property
    def claim_id(self) -> str:
        return claim_identity(self.derivation_id, self.text_hash)


@dataclass(frozen=True)
class EdgeDraft:
    """An operator edge to append. ``origin`` is required: an act whose
    provenance is unrecorded cannot later be audited for self-confirmation."""

    op: str
    src: str
    dst: str
    origin: str
    evidence_locator: str | None = None

    @property
    def edge_id(self) -> str:
        return edge_identity(self.op, self.src, self.dst, self.evidence_locator)


Draft = ClaimDraft | EdgeDraft


@dataclass(frozen=True)
class AppendResult:
    """The outcome of one append transaction.

    ``claims`` / ``edges`` are the records now in the log for the submitted
    drafts — the ALREADY-LOGGED record (with its original ``seq``) for anything
    replayed. ``appended`` counts rows actually written, so a replayed batch
    reports ``0``.
    """

    claims: tuple[ClaimRecord, ...]
    edges: tuple[EdgeRecord, ...]
    appended: int


@dataclass(frozen=True)
class ReviseResult:
    """The full record set one ``revise`` produced.

    ``reasserted_supports`` and ``carried_attacks`` are real logged edges, not
    a description of inheritance: the fold sees exactly these and nothing more.
    ``dropped_supports`` names the supports the caller explicitly declined to
    re-assert, and is reported rather than logged — a support that was not
    re-asserted simply has no edge on the revision.
    """

    revision: ClaimRecord
    revise_edge: EdgeRecord
    reasserted_supports: tuple[EdgeRecord, ...]
    carried_attacks: tuple[EdgeRecord, ...]
    dropped_supports: tuple[str, ...]
    appended: int


# ── the fold: records → graph ───────────────────────────────────────────────


@dataclass(frozen=True)
class FoldedGraph:
    """The argument graph, which is *exactly* the fold of the log.

    Constructed only from records, so an edge that no record produced cannot
    appear. The three projections the labelling needs are separated the way the
    design requires — ``supersede`` as a pre-filter, ``attack`` as the sole
    input to the fixed point, ``support`` as a post-classification — because
    feeding the whole edge set to a Dung solver would treat support and
    supersession as attacks and forfeit its least-fixed-point guarantee.
    """

    claims: tuple[ClaimRecord, ...]
    edges: tuple[EdgeRecord, ...]

    def claim(self, claim_id: str) -> ClaimRecord | None:
        for record in self.claims:
            if record.claim_id == claim_id:
                return record
        return None

    def incoming(self, claim_id: str, op: str | None = None) -> tuple[EdgeRecord, ...]:
        return tuple(
            edge
            for edge in self.edges
            if edge.dst == claim_id and (op is None or edge.op == op)
        )

    def outgoing(self, claim_id: str, op: str | None = None) -> tuple[EdgeRecord, ...]:
        return tuple(
            edge
            for edge in self.edges
            if edge.src == claim_id and (op is None or edge.op == op)
        )

    def supporters_of(self, claim_id: str) -> tuple[str, ...]:
        return tuple(sorted({edge.src for edge in self.incoming(claim_id, "support")}))

    def attackers_of(self, claim_id: str) -> tuple[str, ...]:
        return tuple(sorted({edge.src for edge in self.incoming(claim_id, "attack")}))

    def attack_pairs(self) -> tuple[tuple[str, str], ...]:
        """The ``attack`` subset as ``(attacker, attacked)`` pairs — the ONLY
        projection a Dung framework may be built over."""
        return tuple(
            (edge.src, edge.dst) for edge in self.edges if edge.op == "attack"
        )

    def dangling_edges(self) -> tuple[EdgeRecord, ...]:
        """Edges naming a claim the fold does not hold. Always empty for a log
        read whole (the foreign key forbids it); non-empty only for a partial
        snapshot, which is worth surfacing rather than silently traversing."""
        known = {record.claim_id for record in self.claims}
        return tuple(
            edge for edge in self.edges if edge.src not in known or edge.dst not in known
        )

    def superseding_claim(
        self,
        claim_id: str,
        *,
        is_warranted: Callable[[str], bool] | None = None,
    ) -> str | None:
        """The claim that supersedes ``claim_id``, or ``None``.

        A ``supersede`` edge only *counts* when the superseding claim is itself
        warranted, so the warrant test is an INJECTED predicate rather than a
        second labelling implementation here. Omitting it gives the purely
        structural reading (every logged supersession counts), which is what a
        first provisional pass needs. Ties are broken by log position: the
        latest supersession wins.
        """
        candidates = [
            edge
            for edge in self.incoming(claim_id, "supersede")
            if is_warranted is None or is_warranted(edge.src)
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda edge: edge.seq).src

    def is_superseded(
        self, claim_id: str, *, is_warranted: Callable[[str], bool] | None = None
    ) -> bool:
        return self.superseding_claim(claim_id, is_warranted=is_warranted) is not None

    def chain_head(
        self, claim_id: str, *, is_warranted: Callable[[str], bool] | None = None
    ) -> str:
        """Follow the supersession chain to its head — the CURRENT claim.

        "Current" is never the newest row nor a mutable flag; it is the end of
        the chain. A cycle (which the append path refuses to create) terminates
        the walk rather than hanging.
        """
        current = claim_id
        seen = {current}
        while True:
            following = self.superseding_claim(current, is_warranted=is_warranted)
            if following is None or following in seen:
                return current
            seen.add(following)
            current = following

    def live_claim_ids(
        self, *, is_warranted: Callable[[str], bool] | None = None
    ) -> tuple[str, ...]:
        """The supersede PRE-FILTER: claim ids still in the framework.

        A superseded claim leaves the framework entirely; it is not labelled
        ``out``, because being replaced is not being defeated."""
        return tuple(
            sorted(
                record.claim_id
                for record in self.claims
                if not self.is_superseded(record.claim_id, is_warranted=is_warranted)
            )
        )


def fold_log(
    claims: Iterable[ClaimRecord], edges: Iterable[EdgeRecord]
) -> FoldedGraph:
    """Fold log records into the graph — pure, no I/O, no clock.

    Records are ordered by their shared log position, so the fold of a prefix
    of the log is the graph as of that point.
    """
    return FoldedGraph(
        claims=tuple(sorted(claims, key=lambda record: record.seq)),
        edges=tuple(sorted(edges, key=lambda record: record.seq)),
    )


# ── the append path ─────────────────────────────────────────────────────────

_CLAIM_COLUMNS = (
    "claim_id",
    "derivation_id",
    "text",
    "note_id",
    "locator",
    "provenance",
    "source_note_hash",
    "text_hash",
    "seq",
    "created_at",
)

_EDGE_COLUMNS = (
    "edge_id",
    "op",
    "src",
    "dst",
    "evidence_locator",
    "origin",
    "seq",
    "created_at",
)


class ClaimLog:
    """The append-only claim/edge log over the runtime database.

    Opened on the same file as the job queue and created by the same schema
    script, so an existing runtime DB gains the tables on its next open. Every
    method that writes does so inside one ``BEGIN IMMEDIATE`` transaction — the
    single-writer discipline the rest of the runtime store uses — and every
    write is an INSERT.
    """

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path).expanduser().resolve()

    @classmethod
    def open(cls, path: Path | str) -> "ClaimLog":
        log = cls(path)
        log.path.parent.mkdir(parents=True, exist_ok=True)
        schema = files("tessellum.runtime").joinpath("schema.sql").read_text(
            encoding="utf-8"
        )
        with log._connect() as conn:
            conn.executescript(schema)
        return log

    @classmethod
    def for_store(cls, store: "RuntimeStore") -> "ClaimLog":
        """Open the log on an existing store's database.

        A separate object rather than extra store methods: the log has its own
        append-only contract, and the job queue has no reason to grow a claim
        API to expose it.
        """
        return cls.open(store.path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=2.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 2000")
        return conn

    # ── reads ───────────────────────────────────────────────────────────────

    def read_claims(self) -> tuple[ClaimRecord, ...]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM claims ORDER BY seq").fetchall()
        return tuple(_row_to_claim(row) for row in rows)

    def read_edges(self) -> tuple[EdgeRecord, ...]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM edges ORDER BY seq").fetchall()
        return tuple(_row_to_edge(row) for row in rows)

    def fold(self) -> FoldedGraph:
        """The whole log, folded — the graph the labelling runs over."""
        return fold_log(self.read_claims(), self.read_edges())

    def claims_for_derivation(self, derivation_id: str) -> tuple[ClaimRecord, ...]:
        """Every logged claim sharing one derivation identity, in log order —
        the original plus each revision of it."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM claims WHERE derivation_id = ? ORDER BY seq",
                (derivation_id,),
            ).fetchall()
        return tuple(_row_to_claim(row) for row in rows)

    # ── appends ─────────────────────────────────────────────────────────────

    def append(
        self, drafts: Sequence[Draft], *, now: float | None = None
    ) -> AppendResult:
        """Append a batch of claims and edges in one transaction.

        Order within the batch is preserved and claims must precede the edges
        that name them (the foreign key enforces it). Anything already logged
        under its content id is left exactly as it is and returned unchanged,
        so replaying an episode is a no-op.
        """
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            return self._write(conn, drafts, timestamp)

    def append_claim(self, draft: ClaimDraft, *, now: float | None = None) -> ClaimRecord:
        return self.append((draft,), now=now).claims[0]

    def append_edge(self, draft: EdgeDraft, *, now: float | None = None) -> EdgeRecord:
        return self.append((draft,), now=now).edges[0]

    def revise(
        self,
        target_claim_id: str,
        revision: ClaimDraft,
        *,
        keep_supports: Iterable[str],
        drop_supports: Iterable[str],
        origin: str,
        evidence_locator: str | None = None,
        now: float | None = None,
    ) -> ReviseResult:
        """Append ``revise(revision → target)`` and its two consequences.

        A revise appends one claim and one ``revise`` edge. Beyond that it
        obeys two rules, and both exist because the graph is exactly the fold of
        the log — an inherited edge would be an epistemic act nobody performed:

        * **The target's incoming supports are an explicit keep/drop
          decision.** ``keep_supports`` and ``drop_supports`` must together
          cover every incoming ``support`` of the target, exactly once. Each
          keep becomes a NEW logged ``support`` edge on the revision (origin
          ``reasserted``, carrying the original evidence locator). Each drop is
          reported and simply has no edge. An incomplete decision is refused,
          because silence is how supports get inherited by accident.
        * **Incoming attacks are carried.** Every incoming ``attack`` on the
          target is re-logged onto the revision (origin ``carried``) and stays
          live until a *further* append discharges it — see
          :meth:`discharge_attack`. There is deliberately no opt-out: an
          opt-out would make revision an escape hatch from criticism.

        A revise is not a supersession. The target stays in the framework with
        its own edges intact until :meth:`supersede` says otherwise.
        """
        timestamp = time.time() if now is None else now
        keep = frozenset(keep_supports)
        drop = frozenset(drop_supports)
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            if _claim_row(conn, target_claim_id) is None:
                raise ClaimLogError(f"revise target is not in the log: {target_claim_id}")
            incoming = _incoming_edges(conn, target_claim_id)
            supports = {edge.src: edge for edge in incoming if edge.op == "support"}
            _check_keep_drop_decision(target_claim_id, set(supports), keep, drop)

            drafts: list[Draft] = [
                revision,
                EdgeDraft(
                    op="revise",
                    src=revision.claim_id,
                    dst=target_claim_id,
                    origin=origin,
                    evidence_locator=evidence_locator,
                ),
            ]
            reasserted_ids: list[str] = []
            for supporter in sorted(keep):
                draft = EdgeDraft(
                    op="support",
                    src=supporter,
                    dst=revision.claim_id,
                    origin=ORIGIN_REASSERTED,
                    evidence_locator=supports[supporter].evidence_locator,
                )
                reasserted_ids.append(draft.edge_id)
                drafts.append(draft)
            carried_ids: list[str] = []
            for attack in sorted(
                (edge for edge in incoming if edge.op == "attack"),
                key=lambda edge: edge.seq,
            ):
                draft = EdgeDraft(
                    op="attack",
                    src=attack.src,
                    dst=revision.claim_id,
                    origin=ORIGIN_CARRIED,
                    evidence_locator=attack.evidence_locator,
                )
                carried_ids.append(draft.edge_id)
                drafts.append(draft)

            written = self._write(conn, drafts, timestamp)

        by_id = {edge.edge_id: edge for edge in written.edges}
        revise_edge = next(edge for edge in written.edges if edge.op == "revise")
        return ReviseResult(
            revision=written.claims[0],
            revise_edge=revise_edge,
            reasserted_supports=tuple(by_id[edge_id] for edge_id in reasserted_ids),
            carried_attacks=tuple(by_id[edge_id] for edge_id in carried_ids),
            dropped_supports=tuple(sorted(drop)),
            appended=written.appended,
        )

    def supersede(
        self,
        *,
        superseding_claim_id: str,
        superseded_claim_id: str,
        origin: str,
        evidence_locator: str | None = None,
        now: float | None = None,
    ) -> EdgeRecord:
        """Append ``supersede(superseding → superseded)``.

        The superseded claim leaves the framework — once the superseding claim
        is warranted, which the reader decides by passing its warrant predicate
        to :meth:`FoldedGraph.superseding_claim`. Nothing is marked here: the
        current claim is the CHAIN HEAD of the supersession chain, computed on
        read. Self-supersession and a cycle are refused, since either would
        leave "current" undefined.
        """
        timestamp = time.time() if now is None else now
        if superseding_claim_id == superseded_claim_id:
            raise ClaimLogError(
                f"a claim cannot supersede itself: {superseded_claim_id}"
            )
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            for claim_id in (superseding_claim_id, superseded_claim_id):
                if _claim_row(conn, claim_id) is None:
                    raise ClaimLogError(f"supersede names an unlogged claim: {claim_id}")
            graph = fold_log(_all_claims(conn), _all_edges(conn))
            if superseding_claim_id in _supersession_reach(
                graph, superseded_claim_id
            ):
                raise ClaimLogError(
                    "supersede would close a cycle: "
                    f"{superseding_claim_id} -> {superseded_claim_id}"
                )
            written = self._write(
                conn,
                (
                    EdgeDraft(
                        op="supersede",
                        src=superseding_claim_id,
                        dst=superseded_claim_id,
                        origin=origin,
                        evidence_locator=evidence_locator,
                    ),
                ),
                timestamp,
            )
        return written.edges[0]

    def discharge_attack(
        self,
        *,
        attacking_claim_id: str,
        rebuttal: ClaimDraft | str,
        origin: str,
        evidence_locator: str | None = None,
        now: float | None = None,
    ) -> AppendResult:
        """Discharge an attack by appending an attack ON THE ATTACKER.

        The explicit further append a carried attack demands. Nothing is
        retracted and nothing is rewritten: the rebuttal attacks the attacking
        claim, and the fixed point reinstates whatever that attacker was
        defeating. ``rebuttal`` is a draft to log, or the id of a claim already
        logged. Superseding the attacker via :meth:`supersede` is the other
        available discharge.
        """
        timestamp = time.time() if now is None else now
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            if _claim_row(conn, attacking_claim_id) is None:
                raise ClaimLogError(
                    f"discharge names an unlogged claim: {attacking_claim_id}"
                )
            drafts: list[Draft] = []
            if isinstance(rebuttal, ClaimDraft):
                drafts.append(rebuttal)
                rebuttal_id = rebuttal.claim_id
            else:
                if _claim_row(conn, rebuttal) is None:
                    raise ClaimLogError(f"discharge names an unlogged claim: {rebuttal}")
                rebuttal_id = rebuttal
            drafts.append(
                EdgeDraft(
                    op="attack",
                    src=rebuttal_id,
                    dst=attacking_claim_id,
                    origin=origin,
                    evidence_locator=evidence_locator,
                )
            )
            return self._write(conn, drafts, timestamp)

    # ── the single write primitive ──────────────────────────────────────────

    def _write(
        self, conn: sqlite3.Connection, drafts: Sequence[Draft], timestamp: float
    ) -> AppendResult:
        """Insert drafts at consecutive log positions. INSERT only.

        A draft whose content id is already present consumes no log position
        and its stored record is returned instead, which is what makes replay a
        no-op. Vocabularies are validated here as well as by the column CHECKs,
        so a bad operator raises before it can reach the database.
        """
        claims: list[ClaimRecord] = []
        edges: list[EdgeRecord] = []
        appended = 0
        seq = _next_seq(conn)
        for draft in drafts:
            if isinstance(draft, ClaimDraft):
                if draft.provenance not in PROVENANCES:
                    raise ClaimLogError(f"unknown provenance: {draft.provenance!r}")
                existing = _claim_row(conn, draft.claim_id)
                if existing is not None:
                    claims.append(_row_to_claim(existing))
                    continue
                record = ClaimRecord(
                    claim_id=draft.claim_id,
                    derivation_id=draft.derivation_id,
                    text=draft.text,
                    note_id=draft.note_id,
                    locator=draft.locator,
                    provenance=draft.provenance,
                    source_note_hash=draft.source_note_hash,
                    text_hash=draft.text_hash,
                    seq=seq,
                    created_at=timestamp,
                )
                conn.execute(
                    f"INSERT INTO claims({', '.join(_CLAIM_COLUMNS)}) "
                    f"VALUES ({', '.join('?' * len(_CLAIM_COLUMNS))})",
                    (
                        record.claim_id,
                        record.derivation_id,
                        record.text,
                        record.note_id,
                        record.locator,
                        record.provenance,
                        record.source_note_hash,
                        record.text_hash,
                        record.seq,
                        record.created_at,
                    ),
                )
                claims.append(record)
            elif isinstance(draft, EdgeDraft):
                if draft.op not in OPERATORS:
                    raise ClaimLogError(f"unknown operator: {draft.op!r}")
                existing = _edge_row(conn, draft.edge_id)
                if existing is not None:
                    edges.append(_row_to_edge(existing))
                    continue
                edge = EdgeRecord(
                    edge_id=draft.edge_id,
                    op=draft.op,
                    src=draft.src,
                    dst=draft.dst,
                    evidence_locator=draft.evidence_locator,
                    origin=draft.origin,
                    seq=seq,
                    created_at=timestamp,
                )
                conn.execute(
                    f"INSERT INTO edges({', '.join(_EDGE_COLUMNS)}) "
                    f"VALUES ({', '.join('?' * len(_EDGE_COLUMNS))})",
                    (
                        edge.edge_id,
                        edge.op,
                        edge.src,
                        edge.dst,
                        edge.evidence_locator,
                        edge.origin,
                        edge.seq,
                        edge.created_at,
                    ),
                )
                edges.append(edge)
            else:  # pragma: no cover - defensive: the union is closed
                raise ClaimLogError(f"not a log draft: {draft!r}")
            appended += 1
            seq += 1
        return AppendResult(
            claims=tuple(claims), edges=tuple(edges), appended=appended
        )


# ── row helpers ─────────────────────────────────────────────────────────────


def _row_to_claim(row: sqlite3.Row) -> ClaimRecord:
    return ClaimRecord(
        claim_id=row["claim_id"],
        derivation_id=row["derivation_id"],
        text=row["text"],
        note_id=row["note_id"],
        locator=row["locator"],
        provenance=row["provenance"],
        source_note_hash=row["source_note_hash"],
        text_hash=row["text_hash"],
        seq=row["seq"],
        created_at=row["created_at"],
    )


def _row_to_edge(row: sqlite3.Row) -> EdgeRecord:
    return EdgeRecord(
        edge_id=row["edge_id"],
        op=row["op"],
        src=row["src"],
        dst=row["dst"],
        evidence_locator=row["evidence_locator"],
        origin=row["origin"],
        seq=row["seq"],
        created_at=row["created_at"],
    )


def _claim_row(conn: sqlite3.Connection, claim_id: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM claims WHERE claim_id = ?", (claim_id,)
    ).fetchone()


def _edge_row(conn: sqlite3.Connection, edge_id: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM edges WHERE edge_id = ?", (edge_id,)).fetchone()


def _incoming_edges(conn: sqlite3.Connection, claim_id: str) -> tuple[EdgeRecord, ...]:
    rows = conn.execute(
        "SELECT * FROM edges WHERE dst = ? ORDER BY seq", (claim_id,)
    ).fetchall()
    return tuple(_row_to_edge(row) for row in rows)


def _all_claims(conn: sqlite3.Connection) -> tuple[ClaimRecord, ...]:
    rows = conn.execute("SELECT * FROM claims ORDER BY seq").fetchall()
    return tuple(_row_to_claim(row) for row in rows)


def _all_edges(conn: sqlite3.Connection) -> tuple[EdgeRecord, ...]:
    rows = conn.execute("SELECT * FROM edges ORDER BY seq").fetchall()
    return tuple(_row_to_edge(row) for row in rows)


def _next_seq(conn: sqlite3.Connection) -> int:
    """The next position in the ONE log order shared by claims and edges."""
    row = conn.execute(
        "SELECT COALESCE(MAX(seq), 0) FROM "
        "(SELECT seq FROM claims UNION ALL SELECT seq FROM edges)"
    ).fetchone()
    return int(row[0]) + 1


def _supersession_reach(graph: FoldedGraph, claim_id: str) -> frozenset[str]:
    """Everything ``claim_id`` already supersedes, transitively.

    A new ``supersede(x → y)`` closes a cycle exactly when ``x`` is already in
    ``y``'s reach, which would leave the chain head — and therefore "current" —
    undefined."""
    seen: set[str] = set()
    frontier = [claim_id]
    while frontier:
        current = frontier.pop()
        for edge in graph.outgoing(current, "supersede"):
            if edge.dst not in seen:
                seen.add(edge.dst)
                frontier.append(edge.dst)
    return frozenset(seen)


def _check_keep_drop_decision(
    target_claim_id: str,
    incoming_supports: set[str],
    keep: frozenset[str],
    drop: frozenset[str],
) -> None:
    """Refuse anything short of a complete, unambiguous keep/drop decision."""
    both = keep & drop
    if both:
        raise ClaimLogError(
            "a support cannot be both kept and dropped: " + ", ".join(sorted(both))
        )
    undecided = incoming_supports - (keep | drop)
    if undecided:
        raise ClaimLogError(
            f"every incoming support of {target_claim_id} needs an explicit "
            "keep/drop decision; undecided: " + ", ".join(sorted(undecided))
        )
    unknown = (keep | drop) - incoming_supports
    if unknown:
        raise ClaimLogError(
            f"not an incoming support of {target_claim_id}: "
            + ", ".join(sorted(unknown))
        )


__all__ = [
    "AppendResult",
    "ClaimDraft",
    "ClaimLog",
    "ClaimLogError",
    "ClaimRecord",
    "Draft",
    "EdgeDraft",
    "EdgeRecord",
    "FoldedGraph",
    "OPERATORS",
    "ORIGIN_CARRIED",
    "ORIGIN_PROJECTED",
    "ORIGIN_QUERY",
    "ORIGIN_REASSERTED",
    "Operator",
    "PROVENANCES",
    "Provenance",
    "ReviseResult",
    "claim_identity",
    "edge_identity",
    "edgeset_digest",
    "fold_log",
    "operator_for_legacy_relation",
    "text_digest",
]
