"""tessellum.dks.support_dependency — is a computed label actually *grounded*?

A companion to :mod:`tessellum.dks.status`, and deliberately **outside** the
labelling. The attack-only fixed point is correct and is not touched here; what
this module answers is the separate question the fixed point does not, and was
never meant to.

**Why a second check exists at all.** Two graphs the labelling reports as
``warranted``:

============================================  =====================  ============
Recorded graph                                Labelling says         Truth
============================================  =====================  ============
``source`` supports ``conclusion``;           ``source`` challenged  ``conclusion``
``counter`` defeats ``source``                ``conclusion``         rests on a
                                              **warranted**          defeated premise
``a`` supports ``b``; ``b`` supports ``a``;   **both warranted**     neither rests
no external anchor                                                   on anything
============================================  =====================  ============

Both follow *correctly* from the design: the fixed point runs over the ``attack``
relation only, and ``support`` is a post-classification — "has at least one
support edge", not "is entailed by a grounded premise set". So a computed label is
a **dialectical** verdict (did this claim survive criticism?) and not a
**grounded** one (does a chain of surviving evidence actually reach it?). The
answer gate needs both: ``warranted`` **and** :func:`is_grounded`.

**Three kinds of support, three propagation rules.** A support edge records that
one claim stands behind another, and the append-only schema says nothing about
*how*. That distinction is drawn here, at the validator's input boundary, through
the :class:`SupportKindResolver` port — never by adding a column to a log that is
append-only and already written:

``necessary``
    the conclusion cannot stand without it. **Conjunctive**: every necessary
    premise must itself be grounded, so defeat *propagates* — this is the rule
    the labelling structurally cannot express.
``evidential``
    the premise *is* evidence for the conclusion. **Disjunctive among
    themselves**: one grounded evidential premise is a basis, because two
    independent lines of evidence do not weaken each other and losing one does not
    unground what the other carries. The *group* is still required — a claim whose
    every declared line of evidence has fallen is not grounded, however else it is
    cited.
``contributory``
    corroboration. Adds weight, and is **neither necessary nor sufficient**: a
    defeated contributory premise ungrounds nothing, and a grounded one is not a
    basis on its own. Anything stronger read off a bare ``support`` edge would be
    an inference the log does not license.

:data:`CONSERVATIVE_SUPPORT_KINDS` — the default — reads **every** edge as
``necessary``. That is the fail-closed reading: an undeclared edge is one nobody
has classified, and treating it as conjunctive can only *withhold* an answer,
while treating it as contributory would answer from an unexamined premise set.

**The base case, and why cycles cannot supply one.** Grounding is a least fixed
point: start with nothing grounded and add a claim only once the premises it needs
are already in. A claim with no grounding-relevant premises is grounded when it is
**externally anchored** — it cites a source span (a locator), the span's version
still matches what was recorded, and it was ``constructed`` by reading rather than
located mechanically. Everything else is grounded through its premises. A support
cycle therefore never enters the set: neither member can be added before the
other, so mutual support grounds nothing however ``warranted`` both look. That is
the second fixture above, and it falls out of the iteration order rather than
needing a special case — the special case is only in the *diagnosis*
(:data:`REASON_CYCLIC_SUPPORT`), so a caller is told which cycle stopped it.

**Staleness invalidates.** A cached validation is keyed by a digest covering the
claim/edge set, the resolved support kinds and the cited source versions, so a
changed premise or a changed source version yields a new key and the previous
verdict is simply never read again — the same discipline the status memo uses,
and the reason neither needs an invalidation write. The staleness signal is the
recorded ``source_note_hash`` compared against what an index rebuild computed.

Pure: no clock, no randomness, no I/O, no model call, and no ``runtime`` import
(the Dependency Rule). Reads the log through the same :class:`EdgeSetSource` port
the status query uses.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Literal, Mapping, Protocol, Sequence

from tessellum.dks.status import (
    SUPPORT,
    ClaimView,
    EdgeSetSource,
    EdgeSetView,
    EdgeView,
    StatusTable,
    compute_statuses,
    edgeset_digest,
)

# ── the support vocabulary ──────────────────────────────────────────────────

SupportKind = Literal["evidential", "necessary", "contributory"]
"""How a ``support`` edge bears on its target — three different propagation
rules, not three synonyms. See the module docstring."""

EVIDENTIAL = "evidential"
NECESSARY = "necessary"
CONTRIBUTORY = "contributory"

SUPPORT_KINDS: frozenset[str] = frozenset({EVIDENTIAL, NECESSARY, CONTRIBUTORY})

_GROUNDING_KINDS: frozenset[str] = frozenset({EVIDENTIAL, NECESSARY})
"""The kinds that can carry grounding, and therefore the subgraph a cycle
matters in. A ``contributory`` cycle is harmless: it is not a grounding path."""

_DIGEST_HEX = 32


# ── reasons a claim is not grounded ─────────────────────────────────────────

REASON_UNKNOWN_CLAIM: str = "unknown_claim"
"""Asked about a claim the snapshot does not hold. Reported as a *reason* rather
than raised, because this is a fail-closed gate: an unanswerable question must
read as "not grounded", visibly."""

REASON_DEFEATED: str = "defeated_by_the_labelling"
REASON_SUPERSEDED: str = "superseded"
REASON_STALE_SOURCE: str = "cited_source_version_changed"
REASON_NECESSARY_PREMISE_NOT_GROUNDED: str = "necessary_premise_not_grounded"
REASON_NO_SURVIVING_EVIDENCE: str = "no_surviving_evidential_premise"
REASON_CYCLIC_SUPPORT: str = "cyclic_support_without_an_external_anchor"
REASON_NO_GROUNDING_BASIS: str = "no_grounding_basis"
REASON_STUB_ANCHOR: str = "anchor_claim_is_a_stub"
REASON_NO_ANCHOR_LOCATOR: str = "anchor_claim_has_no_locator"


# ── the input boundary: what a claim has to show to anchor ──────────────────


class GroundingClaimView(Protocol):
    """The claim fields grounding reads — identity, provenance and the anchor.

    Wider than :class:`~tessellum.dks.status.ClaimView` by exactly the anchor:
    the labelling never needs to know where a claim's evidence lives, and
    grounding is the question of whether that evidence exists and still says what
    was recorded. The runtime's claim record satisfies this structurally.

    All three anchor fields are read tolerantly (see :func:`_anchor_of`), so a
    narrower view still validates — it simply has no anchor, which is the
    fail-closed reading rather than a crash.
    """

    @property
    def claim_id(self) -> str: ...

    @property
    def provenance(self) -> str: ...

    @property
    def note_id(self) -> str: ...

    @property
    def locator(self) -> str | None: ...

    @property
    def source_note_hash(self) -> str | None: ...


class SupportKindResolver(Protocol):
    """Declares, per ``support`` edge, which of the three kinds it is.

    A port rather than a column: the claim/edge log is append-only and already
    written, so widening its schema to carry a distinction nobody recorded would
    mean back-filling a judgement. Resolving at the input boundary keeps the log
    honest and makes the reading an explicit, swappable decision.
    """

    def support_kind(self, edge: EdgeView) -> str: ...


@dataclass(frozen=True)
class ConservativeSupportKinds:
    """Every support edge reads as ``necessary`` — the fail-closed default.

    An undeclared edge is one nobody has classified. Reading it as conjunctive
    can only withhold an answer; reading it as ``contributory`` would answer from
    a premise set nobody examined, which is the failure the validator exists to
    catch.

    A record that *does* carry a ``support_kind`` attribute is believed, so a
    later schema that grows the column needs no change here. An unrecognised
    value falls back to ``default`` rather than raising: tolerating a value from
    a newer writer is right for a reader, and the tolerant direction is the
    conservative one.
    """

    default: str = NECESSARY

    def support_kind(self, edge: EdgeView) -> str:
        declared = getattr(edge, "support_kind", None)
        if isinstance(declared, str) and declared in SUPPORT_KINDS:
            return declared
        return self.default


CONSERVATIVE_SUPPORT_KINDS = ConservativeSupportKinds()
"""The default resolver — every support edge is ``necessary``."""


class SupportKindError(ValueError):
    """A declared support kind is not one of the three."""


@dataclass(frozen=True)
class DeclaredSupportKinds:
    """Kinds declared per ``(src, dst)`` pair, with a conservative fallback.

    Keyed on the endpoint pair rather than an edge id because that is the
    identity a caller reasoning about the argument has; the log's content address
    also covers the evidence locator, which is not part of *how* the premise
    bears on the conclusion. Values are validated once, at construction: a
    mistyped kind silently becoming ``necessary`` would be tolerable, but
    silently becoming ``contributory`` would not, so neither is allowed.
    """

    kinds: Mapping[tuple[str, str], str] = field(default_factory=dict)
    default: str = NECESSARY

    def __post_init__(self) -> None:
        unknown = sorted(
            f"{src}->{dst}={kind}"
            for (src, dst), kind in self.kinds.items()
            if kind not in SUPPORT_KINDS
        )
        if unknown:
            raise SupportKindError(
                "support kind must be one of "
                f"{sorted(SUPPORT_KINDS)}; got {', '.join(unknown)}"
            )
        if self.default not in SUPPORT_KINDS:
            raise SupportKindError(f"default support kind unknown: {self.default}")

    def support_kind(self, edge: EdgeView) -> str:
        return self.kinds.get((edge.src, edge.dst), self.default)


# ── the verdict ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class GroundingVerdict:
    """Whether one claim is grounded, with everything that decided it.

    ``status`` is carried from the labelling rather than recomputed, so a verdict
    and the label it disagrees with can be shown side by side — which is the whole
    point: ``status='warranted'`` with ``grounded=False`` is exactly the case the
    answer gate has to refuse.
    """

    claim_id: str
    grounded: bool
    status: str
    reasons: tuple[str, ...] = ()
    basis: tuple[str, ...] = ()
    anchored: bool = False
    failed_premises: tuple[str, ...] = ()
    cycle: tuple[str, ...] = ()
    provisional: bool = False

    @property
    def answerable(self) -> bool:
        """The full answer gate: ``warranted``, grounded, and not resting on a
        ``stub``. Any other combination surfaces a conflict or abstains."""
        return self.grounded and self.status == "warranted" and not self.provisional

    def render(self) -> str:
        """A deterministic plain-text rendering, refusal first."""
        lines = [self.claim_id]
        lines.append(f"  status: {self.status}")
        lines.append(f"  grounded: {self.grounded}")
        if self.anchored:
            lines.append("  anchor: its own cited source span")
        for premise in self.basis:
            lines.append(f"  grounded by: {premise}")
        for premise in self.failed_premises:
            lines.append(f"  ungrounded premise: {premise}")
        if self.cycle:
            lines.append(f"  support cycle: {' -> '.join(self.cycle)}")
        for reason in self.reasons:
            lines.append(f"  not grounded because: {reason}")
        return "\n".join(lines)


@dataclass(frozen=True)
class GroundingTable:
    """Every claim's grounding verdict at one snapshot.

    Keyed by :attr:`digest`, which covers the edge set, the resolved support kinds
    and the cited source versions — so a changed premise or a changed source
    version produces a different table and the previous one is never read again.
    """

    digest: str
    verdicts: Mapping[str, GroundingVerdict]

    def get(self, claim_id: str) -> GroundingVerdict | None:
        return self.verdicts.get(claim_id)

    def verdict(self, claim_id: str) -> GroundingVerdict:
        """The verdict, or the fail-closed one for an unknown claim."""
        found = self.verdicts.get(claim_id)
        if found is not None:
            return found
        return GroundingVerdict(
            claim_id=claim_id,
            grounded=False,
            status="unknown",
            reasons=(REASON_UNKNOWN_CLAIM,),
        )

    def is_grounded(self, claim_id: str) -> bool:
        return self.verdict(claim_id).grounded

    def grounded_ids(self) -> tuple[str, ...]:
        return tuple(
            sorted(cid for cid, verdict in self.verdicts.items() if verdict.grounded)
        )

    def ungrounded_ids(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                cid for cid, verdict in self.verdicts.items() if not verdict.grounded
            )
        )


# ── anchors and staleness ───────────────────────────────────────────────────


@dataclass(frozen=True)
class _Anchor:
    """Whether a claim's own cited source can ground it, and if not, why."""

    anchored: bool
    stale: bool = False
    reasons: tuple[str, ...] = ()


def _anchor_of(
    claim: ClaimView, current_note_hashes: Mapping[str, str] | None
) -> _Anchor:
    """Read a claim's external anchor, tolerantly.

    Three conditions, and each failure is named rather than folded into one
    "ungrounded":

    * a **locator** — a claim with no located span cites nothing, so there is
      nothing outside the claim graph for it to stand on;
    * ``provenance='constructed'`` — a ``stub`` is a string located mechanically,
      and most such strings are not truth-apt as written, so one may anchor
      nothing;
    * a source version that still **matches**. ``current_note_hashes`` is what an
      index rebuild computed; a note absent from it is *unknown*, never asserted
      stale, so a partial rebuild cannot unground the corpus.

    The fields are read with :func:`getattr` because the labelling's narrower
    :class:`~tessellum.dks.status.ClaimView` does not carry them. Missing fields
    mean "no anchor", which withholds grounding rather than granting it.
    """
    locator = getattr(claim, "locator", None)
    reasons: list[str] = []
    if not isinstance(locator, str) or not locator.strip():
        reasons.append(REASON_NO_ANCHOR_LOCATOR)
    if getattr(claim, "provenance", "") == "stub":
        reasons.append(REASON_STUB_ANCHOR)
    stale = _is_stale(claim, current_note_hashes)
    if stale:
        reasons.append(REASON_STALE_SOURCE)
    return _Anchor(anchored=not reasons, stale=stale, reasons=tuple(reasons))


def _is_stale(
    claim: ClaimView, current_note_hashes: Mapping[str, str] | None
) -> bool:
    """``True`` only when a recorded source version is known to have changed."""
    if not current_note_hashes:
        return False
    recorded = getattr(claim, "source_note_hash", None)
    note_id = getattr(claim, "note_id", None)
    if not recorded or not note_id:
        return False
    current = current_note_hashes.get(note_id)
    return current is not None and current != recorded


# ── the premise index ───────────────────────────────────────────────────────


@dataclass(frozen=True)
class _Premises:
    """One claim's incoming support, split by kind."""

    necessary: tuple[str, ...] = ()
    evidential: tuple[str, ...] = ()
    contributory: tuple[str, ...] = ()

    @property
    def grounding(self) -> tuple[str, ...]:
        """The premises that can carry grounding — ``contributory`` excluded."""
        return tuple(sorted(set(self.necessary) | set(self.evidential)))


def support_premises(
    edges: Iterable[EdgeView], kinds: SupportKindResolver
) -> dict[str, _Premises]:
    """``claim_id -> its incoming support premises, by kind``.

    Self-support is dropped outright: an edge from a claim to itself is a cycle of
    length one and can ground nothing, so it is not worth carrying into the
    iteration to be rejected there.
    """
    buckets: dict[str, dict[str, set[str]]] = {}
    for edge in edges:
        if edge.op != SUPPORT or edge.src == edge.dst:
            continue
        kind = kinds.support_kind(edge)
        if kind not in SUPPORT_KINDS:
            kind = NECESSARY
        buckets.setdefault(
            edge.dst, {NECESSARY: set(), EVIDENTIAL: set(), CONTRIBUTORY: set()}
        )[kind].add(edge.src)
    return {
        claim_id: _Premises(
            necessary=tuple(sorted(by_kind[NECESSARY])),
            evidential=tuple(sorted(by_kind[EVIDENTIAL])),
            contributory=tuple(sorted(by_kind[CONTRIBUTORY])),
        )
        for claim_id, by_kind in buckets.items()
    }


# ── the digest that keys a cached validation ────────────────────────────────


def grounding_digest(
    claims: Sequence[ClaimView],
    edges: Sequence[EdgeView],
    *,
    kinds: SupportKindResolver = CONSERVATIVE_SUPPORT_KINDS,
    current_note_hashes: Mapping[str, str] | None = None,
) -> str:
    """Order-independent digest of everything a grounding verdict depends on.

    Three parts, and each one is a way a cached validation goes wrong:

    * the **claim/edge set** — reused from
      :func:`~tessellum.dks.status.edgeset_digest`, so the two caches agree about
      what "the same graph" means. A changed premise is a new content-addressed
      claim id, so "a required premise changed" is covered by construction;
    * the **resolved support kinds** — reclassifying one edge from contributory to
      necessary changes every verdict downstream of it;
    * the **cited source versions**, recorded and current — the staleness signal.
      A claim whose note is absent from the current-hash mapping contributes its
      recorded hash only, so a partial rebuild does not churn the key.
    """
    h = hashlib.sha256()
    h.update(edgeset_digest(claims, edges).encode("utf-8"))
    h.update(b"\0")
    for part in sorted(
        "src|{}|{}|{}|{}".format(
            claim.claim_id,
            getattr(claim, "locator", None) or "",
            getattr(claim, "source_note_hash", None) or "",
            (current_note_hashes or {}).get(getattr(claim, "note_id", "") or "", ""),
        )
        for claim in claims
    ):
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    for part in sorted(
        f"kind|{edge.src}|{edge.dst}|{kinds.support_kind(edge)}"
        for edge in edges
        if edge.op == SUPPORT
    ):
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:_DIGEST_HEX]


# ── the validator ───────────────────────────────────────────────────────────


def validate_support_dependencies(
    view: EdgeSetView,
    *,
    kinds: SupportKindResolver = CONSERVATIVE_SUPPORT_KINDS,
    current_note_hashes: Mapping[str, str] | None = None,
    statuses: StatusTable | None = None,
) -> GroundingTable:
    """Grounding for every claim in one snapshot. Pure, model-free, no writes.

    The labelling is **read, never re-derived**: ``statuses`` defaults to
    :func:`~tessellum.dks.status.compute_statuses` over the same view, and a
    caller that already has the table passes it so the two verdicts cannot be
    computed over different snapshots.

    The iteration is a least fixed point over the grounding-relevant support
    subgraph. Each round adds the eligible claims whose premise obligations are
    already met; when a round adds nothing, whatever is left is ungrounded — and
    a support cycle is exactly the shape that never gets a first member in.
    Terminates in at most one round per claim.
    """
    claims = tuple(view.claims)
    edges = tuple(view.edges)
    table = statuses if statuses is not None else compute_statuses(view)
    premises = support_premises(edges, kinds)
    anchors = {
        claim.claim_id: _anchor_of(claim, current_note_hashes) for claim in claims
    }

    eligible: dict[str, tuple[str, ...]] = {}
    for claim in claims:
        verdict = table.get(claim.claim_id)
        status = verdict.status if verdict is not None else "unknown"
        blockers: list[str] = []
        if status == "challenged":
            blockers.append(REASON_DEFEATED)
        elif status == "superseded":
            blockers.append(REASON_SUPERSEDED)
        elif status == "unknown":  # pragma: no cover - defensive
            blockers.append(REASON_UNKNOWN_CLAIM)
        if anchors[claim.claim_id].stale:
            blockers.append(REASON_STALE_SOURCE)
        eligible[claim.claim_id] = tuple(blockers)

    grounded: set[str] = set()
    basis: dict[str, tuple[str, ...]] = {}
    changed = True
    while changed:
        changed = False
        for claim in claims:
            claim_id = claim.claim_id
            if claim_id in grounded or eligible[claim_id]:
                continue
            found = _basis_for(
                claim_id,
                premises.get(claim_id, _Premises()),
                anchored=anchors[claim_id].anchored,
                grounded=grounded,
            )
            if found is None:
                continue
            grounded.add(claim_id)
            basis[claim_id] = found
            changed = True

    verdicts: dict[str, GroundingVerdict] = {}
    for claim in claims:
        claim_id = claim.claim_id
        verdict = table.get(claim_id)
        verdicts[claim_id] = _verdict_for(
            claim_id,
            status=verdict.status if verdict is not None else "unknown",
            provisional=bool(verdict.provisional) if verdict is not None else False,
            blockers=eligible[claim_id],
            premises=premises.get(claim_id, _Premises()),
            anchor=anchors[claim_id],
            grounded=grounded,
            basis=basis.get(claim_id, ()),
            all_premises=premises,
        )
    return GroundingTable(
        digest=grounding_digest(
            claims, edges, kinds=kinds, current_note_hashes=current_note_hashes
        ),
        verdicts=verdicts,
    )


def _basis_for(
    claim_id: str,
    premises: _Premises,
    *,
    anchored: bool,
    grounded: set[str],
) -> tuple[str, ...] | None:
    """The premises grounding ``claim_id``, or ``None`` if it is not yet grounded.

    Three obligations, and all of them have to hold:

    1. **conjunction over ``necessary``** — every necessary premise is already
       grounded, which is how defeat propagates;
    2. **survival of the ``evidential`` group** — if any evidential premise is
       declared, at least one of them is grounded. Disjunctive within the group,
       required as a group: a claim every one of whose declared lines of evidence
       has fallen is not grounded by the fact that it also cites a span;
    3. **a basis** — the claim's own anchor, or a grounded ``evidential`` premise,
       or a non-empty fully-grounded ``necessary`` set. ``contributory`` premises
       are never a basis, so a claim standing only on corroboration is not
       grounded.

    Returning ``None`` is "not yet, or not ever" — the caller's fixed point
    distinguishes them by whether a later round adds it.
    """
    if any(premise not in grounded for premise in premises.necessary):
        return None
    supporting = [
        premise for premise in premises.evidential if premise in grounded
    ]
    if premises.evidential and not supporting:
        return None
    if not anchored and not supporting and not premises.necessary:
        return None
    return tuple(sorted(set(premises.necessary) | set(supporting)))


def _verdict_for(
    claim_id: str,
    *,
    status: str,
    provisional: bool,
    blockers: tuple[str, ...],
    premises: _Premises,
    anchor: _Anchor,
    grounded: set[str],
    basis: tuple[str, ...],
    all_premises: Mapping[str, _Premises],
) -> GroundingVerdict:
    """Assemble one verdict, naming every reason a refusal has."""
    if claim_id in grounded:
        return GroundingVerdict(
            claim_id=claim_id,
            grounded=True,
            status=status,
            basis=basis,
            anchored=anchor.anchored,
            provisional=provisional,
        )
    reasons: list[str] = list(blockers)
    failed_necessary = tuple(
        premise for premise in premises.necessary if premise not in grounded
    )
    if failed_necessary:
        reasons.append(REASON_NECESSARY_PREMISE_NOT_GROUNDED)
    evidence_fell = bool(premises.evidential) and not any(
        premise in grounded for premise in premises.evidential
    )
    if evidence_fell:
        reasons.append(REASON_NO_SURVIVING_EVIDENCE)
    cycle = _grounding_cycle(claim_id, all_premises)
    if cycle:
        reasons.append(REASON_CYCLIC_SUPPORT)
    if not reasons:
        reasons.append(REASON_NO_GROUNDING_BASIS)
        reasons.extend(anchor.reasons)
    failed = tuple(
        sorted(
            set(failed_necessary)
            | (set(premises.evidential) if evidence_fell else set())
        )
    )
    return GroundingVerdict(
        claim_id=claim_id,
        grounded=False,
        status=status,
        reasons=tuple(dict.fromkeys(reasons)),
        anchored=anchor.anchored,
        failed_premises=failed,
        cycle=cycle,
        provisional=provisional,
    )


def _grounding_cycle(
    claim_id: str, premises: Mapping[str, _Premises]
) -> tuple[str, ...]:
    """A support path from ``claim_id`` back to itself, or ``()``.

    Diagnosis only — the fixed point already refuses a cycle by never admitting a
    first member — so this runs solely for claims that came out ungrounded. The
    walk follows ``necessary`` and ``evidential`` premises; a ``contributory``
    cycle is not a grounding path and is therefore not reported as one. The first
    path found is returned, which is deterministic because the premise lists are
    sorted.
    """
    stack: list[tuple[str, tuple[str, ...]]] = [(claim_id, (claim_id,))]
    seen: set[str] = set()
    while stack:
        current, path = stack.pop(0)
        for premise in premises.get(current, _Premises()).grounding:
            if premise == claim_id:
                return path + (claim_id,)
            if premise in seen:
                continue
            seen.add(premise)
            stack.append((premise, path + (premise,)))
    return ()


class GroundingValidator:
    """:func:`validate_support_dependencies` as a query, memoised by digest.

    Reads only, writes nothing, and caches the way the status query does: the memo
    is keyed by :func:`grounding_digest`, so a changed premise, a reclassified
    support edge or a changed cited source version yields a new key and the stale
    entry is simply never read again. There is no invalidation write, which is what
    keeps a cache compatible with an append-only log.

    Args:
        source: anything satisfying :class:`~tessellum.dks.status.EdgeSetSource`.
        kinds: the :class:`SupportKindResolver`; conservative by default.
        current_note_hashes: what an index rebuild computed, for the staleness
            check. Rebind with :meth:`with_note_hashes` when a rebuild reports
            new hashes — a new mapping is a new digest, and therefore a
            revalidation.
        cache_size: how many digests to keep; ``0`` disables the memo.
    """

    def __init__(
        self,
        source: EdgeSetSource,
        *,
        kinds: SupportKindResolver = CONSERVATIVE_SUPPORT_KINDS,
        current_note_hashes: Mapping[str, str] | None = None,
        cache_size: int = 4,
    ) -> None:
        self.source = source
        self.kinds = kinds
        self.current_note_hashes = (
            dict(current_note_hashes) if current_note_hashes else None
        )
        self.cache_size = max(0, cache_size)
        self._cache: dict[str, GroundingTable] = {}
        self._hits = 0
        self._misses = 0

    @property
    def cache_hits(self) -> int:
        return self._hits

    @property
    def cache_misses(self) -> int:
        """Revalidations. One per distinct graph + kinds + source-version state."""
        return self._misses

    def with_note_hashes(
        self, current_note_hashes: Mapping[str, str] | None
    ) -> "GroundingValidator":
        """A validator over the same source at a new source-version state.

        A new object rather than a mutation, so a cached table can never be read
        against hashes it was not computed under.
        """
        return GroundingValidator(
            self.source,
            kinds=self.kinds,
            current_note_hashes=current_note_hashes,
            cache_size=self.cache_size,
        )

    def table(self) -> GroundingTable:
        view = self.source.fold()
        digest = grounding_digest(
            tuple(view.claims),
            tuple(view.edges),
            kinds=self.kinds,
            current_note_hashes=self.current_note_hashes,
        )
        cached = self._cache.get(digest)
        if cached is not None:
            self._hits += 1
            return cached
        self._misses += 1
        table = validate_support_dependencies(
            view,
            kinds=self.kinds,
            current_note_hashes=self.current_note_hashes,
        )
        if self.cache_size:
            if len(self._cache) >= self.cache_size:
                self._cache.pop(next(iter(self._cache)))
            self._cache[digest] = table
        return table

    def validate(self, claim_id: str) -> GroundingVerdict:
        """One claim's grounding verdict — fail-closed for an unknown claim."""
        return self.table().verdict(claim_id)

    def is_grounded(self, claim_id: str) -> bool:
        return self.validate(claim_id).grounded

    def answerable(self, claim_id: str) -> bool:
        """The full answer gate: ``warranted``, grounded, and not provisional."""
        return self.validate(claim_id).answerable


# ── the predicates the query path calls ─────────────────────────────────────


def grounding_verdict(
    view: EdgeSetView,
    claim_id: str,
    *,
    kinds: SupportKindResolver = CONSERVATIVE_SUPPORT_KINDS,
    current_note_hashes: Mapping[str, str] | None = None,
    statuses: StatusTable | None = None,
) -> GroundingVerdict:
    """One-shot verdict over one snapshot — no memo survives the call."""
    return validate_support_dependencies(
        view,
        kinds=kinds,
        current_note_hashes=current_note_hashes,
        statuses=statuses,
    ).verdict(claim_id)


def is_grounded(
    view: EdgeSetView,
    claim_id: str,
    *,
    kinds: SupportKindResolver = CONSERVATIVE_SUPPORT_KINDS,
    current_note_hashes: Mapping[str, str] | None = None,
    statuses: StatusTable | None = None,
) -> bool:
    """Is ``claim_id`` grounded in surviving evidence, not merely undefeated?

    **The predicate the answer gate calls.** ``warranted`` is necessary and not
    sufficient: the labelling admits a conclusion resting on a defeated necessary
    premise and admits circular support. So the gate is
    ``status == 'warranted' and is_grounded(...)`` — or, in one call,
    :func:`is_answerable`.
    """
    return grounding_verdict(
        view,
        claim_id,
        kinds=kinds,
        current_note_hashes=current_note_hashes,
        statuses=statuses,
    ).grounded


def is_answerable(
    view: EdgeSetView,
    claim_id: str,
    *,
    kinds: SupportKindResolver = CONSERVATIVE_SUPPORT_KINDS,
    current_note_hashes: Mapping[str, str] | None = None,
    statuses: StatusTable | None = None,
) -> bool:
    """The whole gate in one call: ``warranted``, grounded, not provisional.

    ``challenged`` surfaces the conflict, ``proposed`` and ``superseded`` abstain,
    and a ``warranted`` claim that fails grounding also abstains — it is not an
    answer, and it is not a conflict to surface either.
    """
    return grounding_verdict(
        view,
        claim_id,
        kinds=kinds,
        current_note_hashes=current_note_hashes,
        statuses=statuses,
    ).answerable


__all__ = [
    "CONSERVATIVE_SUPPORT_KINDS",
    "CONTRIBUTORY",
    "EVIDENTIAL",
    "NECESSARY",
    "REASON_CYCLIC_SUPPORT",
    "REASON_DEFEATED",
    "REASON_NECESSARY_PREMISE_NOT_GROUNDED",
    "REASON_NO_ANCHOR_LOCATOR",
    "REASON_NO_GROUNDING_BASIS",
    "REASON_NO_SURVIVING_EVIDENCE",
    "REASON_STALE_SOURCE",
    "REASON_STUB_ANCHOR",
    "REASON_SUPERSEDED",
    "REASON_UNKNOWN_CLAIM",
    "SUPPORT_KINDS",
    "ConservativeSupportKinds",
    "DeclaredSupportKinds",
    "GroundingClaimView",
    "GroundingTable",
    "GroundingValidator",
    "GroundingVerdict",
    "SupportKind",
    "SupportKindError",
    "SupportKindResolver",
    "grounding_digest",
    "grounding_verdict",
    "is_answerable",
    "is_grounded",
    "support_premises",
    "validate_support_dependencies",
]
