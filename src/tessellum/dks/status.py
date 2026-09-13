"""tessellum.dks.status — the computed status of a claim, over the attack relation.

P5 of the query-time-DKS plan. This is where the *dynamic* half of the operator
system lives: no operator writes a status, because a status is a **pure function
of the edge set**, recomputed on demand. Appending one ``attack`` can therefore
flip verdicts arbitrarily far downstream — including flipping a claim BACK
(reinstatement) once its attacker is itself defeated — and nothing had to be
migrated for that to happen.

**Three layers, in this order, and the order is the whole design.** The fixed
point runs over the ``attack`` relation ONLY; ``supersede`` is applied before it
and ``support`` after it:

1. **Pre-filter — ``supersede``.** A superseded claim LEAVES the framework: it
   is not labelled ``out``, because being replaced is not being defeated. A
   ``supersede(b' → b)`` counts **only when ``b'`` itself computes as
   ``warranted``** in a first provisional pass — Dung ``in`` *and* carrying a
   support edge — so an unresolved replacement can never withdraw the current
   claim. The weaker rule ("``b'`` is merely not ``out`` in the provisional
   pass") is **rejected**, and both counter-fixtures say why: an *unsupported*
   ``b'`` is ``proposed``, and a *mutually attacked* ``b'`` is ``challenged``,
   yet either would silently retire ``b`` under the weak rule. A claim may only
   be replaced by one that has itself survived and is grounded.
2. **The fixed point — ``attack`` only.** The ``op='attack'`` subset is
   projected into a :class:`~tessellum.dks.dung.DungAF` and labelled by
   :func:`~tessellum.dks.dung.grounded_labelling`, which is correct, live and
   deliberately untouched. Feeding it the whole edge set would treat
   ``support`` / ``revise`` / ``supersede`` as attacks and forfeit the
   least-fixed-point guarantee this design inherits rather than re-proves.
3. **Post-classification — ``support``.** ``out`` → ``challenged``; ``undec``
   → ``challenged`` as well, because a live unresolved dispute and a defeated
   claim have the SAME consequence for answering, and exposing "undecided" as a
   third answer invites a caller to act on it; ``in`` **with** a support edge →
   ``warranted``; ``in`` **without** one → ``proposed``.

**A computed label is not a verified answer.** Layer 3 asks whether a support edge
*exists*, not whether the support *grounds* — so this labelling correctly reports
``warranted`` for a conclusion whose necessary premise has been defeated, and for
two claims that support only each other. Those are properties of the attack-only
semantics, not bugs in it, and the answer gate therefore needs a second, separate
check: :mod:`tessellum.dks.support_dependency`, which propagates defeat across
necessary premises and refuses circular support. Nothing in this module may be
read as "this claim is grounded".

``revise`` carries no force in the labelling. That is not an omission: the
asymmetric carry-over rule (kept supports are re-asserted as new edges, incoming
attacks are carried and must be explicitly discharged) is enforced where the
edges are *appended*, so inferring anything from a ``revise`` here would put
edges in the graph that appear in no log record.

**Two axes, not one.** The four statuses above are the edge-set-computed verdict.
:func:`~tessellum.dks.ontology.acceptance_from_labelling` is a SECOND axis over
the same Dung label, recording whether an *exogenous* check also passed
(``accepted``) or only the dialectic was survived (``dialectically_adequate``).
It is not a replacement status set — it cannot express ``proposed`` or
``superseded`` — and it is wired here with
:data:`~tessellum.dks.ontology.INDEPENDENT_VALIDATION_AVAILABLE`, hard-wired
``False`` until the verification phase lands, so nothing is ever ``accepted``
yet.

**No model, anywhere.** The verdict is what the system acts on and abstains on;
if a model decided "warranted" the judgement would not be replayable and could
not be audited. Models produce *evidence* (incompatibility, direction,
entailment) upstream; the verdict is graph arithmetic.

**Fail closed over stubs.** A ``stub`` claim is a string located mechanically
from a note rather than a proposition constructed by reading it. Measured on a
real corpus, 76% of such strings are not truth-apt as written (54% contain no
finite verb, 46% carry a document-type prefix), so printing ``warranted`` for
one would launder a document title into a verdict. :meth:`StatusQuery.status`
and :meth:`StatusQuery.explain` therefore REFUSE any verdict whose influencing
chain touches a stub, unless the caller passes ``allow_provisional=True`` — in
which case the answer comes back hard-labelled provisional, never quietly.

**Queries, and zero status writes.** Everything here is a read. The labelling is
memoised in :class:`StatusQuery` by a digest of the claim + edge set, so an
append yields a new key and the stale entry is simply never read again — no
invalidation write, which is what keeps a cache compatible with an append-only
log. Nothing in this module writes a status anywhere: a stored status would be a
label someone has to keep true, and the point of computing it is that nobody
does.

Pure: no clock, no randomness, no I/O, no model call, and no ``runtime`` import
(the Dependency Rule). The log is read through the :class:`EdgeSetSource` port,
which the runtime's append-only log satisfies structurally.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Literal, Mapping, Protocol, Sequence

from tessellum.dks.dung import DungAF, DungLabel, grounded_labelling
from tessellum.dks.ontology import (
    INDEPENDENT_VALIDATION_AVAILABLE,
    AcceptanceVerdict,
    acceptance_from_labelling,
)

# ── the computed vocabulary ─────────────────────────────────────────────────

Status = Literal["proposed", "challenged", "warranted", "superseded"]
"""The four computed statuses — the verdict a caller acts on.

- ``"warranted"`` — survives the attack relation AND has a support edge.
  Answerable, citing the support chain.
- ``"challenged"`` — a live attack survives (Dung ``out`` *or* ``undec``). Both
  chains are worth surfacing; neither is an answer.
- ``"proposed"`` — unattacked but ungrounded: nothing supports it yet.
- ``"superseded"`` — replaced by a later claim that is itself ``warranted``, so
  it left the framework. The current claim is the head of the supersession
  chain; a replacement that is not warranted retires nothing.
"""

STATUSES: frozenset[str] = frozenset(
    {"proposed", "challenged", "warranted", "superseded"}
)

ATTACK = "attack"
SUPPORT = "support"
SUPERSEDE = "supersede"
REVISE = "revise"

_INFLUENCING_OPS: frozenset[str] = frozenset({SUPPORT, ATTACK, SUPERSEDE})
"""The ops whose incoming edges can change a verdict — so the ops a stub-chain
walk has to follow. ``revise`` is excluded because it carries no force in the
labelling."""

_DIGEST_HEX = 32


# ── errors ──────────────────────────────────────────────────────────────────


class StatusError(RuntimeError):
    """Base for the two refusals this module makes."""


class UnknownClaimError(StatusError):
    """The queried claim is not in the log — distinct from having no status."""


class ProvisionalStatusError(StatusError):
    """The verdict's influencing chain touches a ``stub`` claim.

    Raised instead of returning a status, because a status computed over a
    string that cannot be true or false is not a status. Carries the stub ids so
    a caller can report *which* claims need constructing (the fix is a reading
    pass, never a better regex), and ``allow_provisional=True`` is the explicit
    opt-out.
    """

    def __init__(self, claim_id: str, stub_chain: Sequence[str]) -> None:
        self.claim_id = claim_id
        self.stub_chain: tuple[str, ...] = tuple(stub_chain)
        super().__init__(
            f"refusing a status for {claim_id}: its chain touches "
            f"{len(self.stub_chain)} claim(s) with provenance='stub' "
            f"({', '.join(self.stub_chain[:3])}"
            f"{', …' if len(self.stub_chain) > 3 else ''}). A stub is a located "
            "string, not a constructed claim, and most are not truth-apt; "
            "construct them by reading the source, or pass allow_provisional "
            "to compute anyway."
        )


# ── the read port ───────────────────────────────────────────────────────────


class ClaimView(Protocol):
    """The claim fields the labelling reads — an identity and a provenance.

    Deliberately narrow: the verdict never depends on a claim's text, note or
    locator, so those are not in the port. The runtime's claim record satisfies
    this structurally.
    """

    @property
    def claim_id(self) -> str: ...

    @property
    def provenance(self) -> str: ...


class EdgeView(Protocol):
    """The edge fields the labelling reads.

    ``seq`` is the log position, and it is here for one reason: when two
    supersessions target the same claim, the LATEST one names the successor.
    ``evidence_locator`` and ``origin`` are read only by :func:`explain`.
    """

    @property
    def op(self) -> str: ...

    @property
    def src(self) -> str: ...

    @property
    def dst(self) -> str: ...

    @property
    def seq(self) -> int: ...

    @property
    def evidence_locator(self) -> str | None: ...

    @property
    def origin(self) -> str: ...


class EdgeSetView(Protocol):
    """One SNAPSHOT of the folded log — the input the labelling is a function of."""

    @property
    def claims(self) -> Sequence[ClaimView]: ...

    @property
    def edges(self) -> Sequence[EdgeView]: ...


class EdgeSetSource(Protocol):
    """The port :class:`StatusQuery` reads through — a re-readable fold.

    Re-readable rather than a single snapshot because the point of a computed
    status is that an append changes it: each query folds again, and the digest
    decides whether the previous labelling still applies. Storage lives in the
    runtime by the Dependency Rule, and the runtime's append-only log satisfies
    this port structurally (its ``fold()`` returns a folded graph).
    """

    def fold(self) -> EdgeSetView: ...


@dataclass(frozen=True)
class EdgeSet:
    """An in-memory :class:`EdgeSetView` that is also its own
    :class:`EdgeSetSource`.

    The deterministic reference implementation of the port: it makes the
    labelling exercisable with no database and no storage dependency at all,
    which is what keeps this module's tests pure. ``claims`` / ``edges`` may hold
    any objects satisfying the two views — the runtime's log records do.
    """

    claims: tuple[ClaimView, ...] = ()
    edges: tuple[EdgeView, ...] = ()

    def fold(self) -> "EdgeSet":
        return self


# ── the digest that keys the cache ──────────────────────────────────────────


def edgeset_digest(
    claims: Iterable[ClaimView], edges: Iterable[EdgeView]
) -> str:
    """Order-independent digest of everything the labelling depends on.

    Two deliberate divergences from the reference implementation this ports,
    recorded here so neither is rediscovered by debugging a stale answer:

    * **The claim set is in the key, not only the edges.** A claim appended with
      no edges is a real change — it is ``proposed`` and must appear — and an
      edge-only key would miss it.
    * **``provenance`` is in the key**, because it decides whether a verdict is
      refused; constructing a stub does not change any label but must change the
      answer.

    An edge's locator and origin are NOT in the key: they are evidence for a
    reader, and re-citing the same act does not move a label.
    """
    h = hashlib.sha256()
    for part in sorted(f"claim|{c.claim_id}|{c.provenance}" for c in claims):
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    for part in sorted(f"edge|{e.op}|{e.src}|{e.dst}" for e in edges):
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:_DIGEST_HEX]


# ── the verdict ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ClaimStatus:
    """One claim's computed verdict, with everything it was computed from.

    ``label`` is the Dung label from layer 2, and it is ``None`` for a
    superseded claim — which is the honest reading: that claim was not labelled,
    it left the framework before the fixed point ran.

    ``acceptance`` is the second axis (see the module docstring): it reports the
    same Dung label under the ``accepted`` / ``dialectically_adequate``
    distinction, and while independent validation is unavailable a surviving
    claim is ``dialectically_adequate`` — surviving the dialectic is necessary
    but not sufficient for truth.
    """

    claim_id: str
    status: Status
    label: DungLabel | None
    acceptance: AcceptanceVerdict
    supporters: tuple[str, ...] = ()
    attackers: tuple[str, ...] = ()
    superseded_by: str | None = None
    stub_chain: tuple[str, ...] = ()

    @property
    def provisional(self) -> bool:
        """``True`` when a ``stub`` claim influenced this verdict, so the verdict
        is not trustworthy however confident it looks."""
        return bool(self.stub_chain)

    @property
    def answerable(self) -> bool:
        """``True`` only for a non-provisional ``warranted`` claim — the single
        status a caller may answer from. ``challenged`` surfaces the conflict;
        ``proposed`` and ``superseded`` abstain.

        **Necessary, not sufficient.** This is the *dialectical* half of the answer
        gate. The attack-only labelling checks that a claim survived criticism and
        that something supports it; it cannot check that the support actually
        grounds it, so it admits a conclusion whose necessary premise is defeated
        and admits circular support. The other half is
        :func:`tessellum.dks.support_dependency.is_grounded`, and the full gate is
        :func:`tessellum.dks.support_dependency.is_answerable`.
        """
        return self.status == "warranted" and not self.provisional


@dataclass(frozen=True)
class StatusTable:
    """The whole corpus labelled at one edge-set digest.

    Keyed by the digest it was computed over, which is what makes it cacheable
    without an invalidation write: a later append produces a different digest and
    this table is simply never read again.
    """

    digest: str
    statuses: Mapping[str, ClaimStatus]
    labels: Mapping[str, DungLabel]
    live: tuple[str, ...]

    def get(self, claim_id: str) -> ClaimStatus | None:
        return self.statuses.get(claim_id)

    def summary(self) -> dict[str, int]:
        """Count by status — the corpus-level view, in the four-status
        vocabulary. Missing statuses are omitted rather than reported as zero."""
        return dict(Counter(v.status for v in self.statuses.values()))

    def with_status(self, status: str) -> tuple[str, ...]:
        return tuple(
            sorted(cid for cid, v in self.statuses.items() if v.status == status)
        )


# ── the three layers ────────────────────────────────────────────────────────


def attack_pairs(edges: Iterable[EdgeView]) -> tuple[tuple[str, str], ...]:
    """The ``attack`` subset as ``(attacker, attacked)`` — the ONLY projection a
    Dung framework may be built over."""
    return tuple((e.src, e.dst) for e in edges if e.op == ATTACK)


def supported_claims(edges: Iterable[EdgeView]) -> frozenset[str]:
    """The claims carrying at least one incoming ``support`` edge.

    Layer 3 reads this to tell ``warranted`` from ``proposed``, and layer 1 reads
    it because "``b'`` is warranted" is a *status*, not a Dung label — a
    surviving-but-ungrounded replacement is ``proposed`` and may not retire
    anything.
    """
    return frozenset(edge.dst for edge in edges if edge.op == SUPPORT)


def provisionally_warranted(
    edges: Iterable[EdgeView], provisional_labels: Mapping[str, DungLabel]
) -> frozenset[str]:
    """Layer 1's input: the claims that compute as ``warranted`` in the FIRST
    pass — before any supersession has been applied.

    ``warranted`` is Dung ``in`` **and** supported, which is exactly layer 3's
    rule (:func:`classify`) minus the supersession it is about to decide. The
    provisional pass is unavoidable and deliberately shallow: the pre-filter's
    input cannot be the final labelling, because the final labelling is what the
    pre-filter produces. One pass is enough for the rule the design states —
    "``b`` is superseded when ``b'`` is warranted" — since a replacement whose
    own warrant depends on a supersession it is itself performing is precisely
    the circularity this refuses to resolve in its favour.
    """
    supported = supported_claims(edges)
    return frozenset(
        claim_id
        for claim_id, label in provisional_labels.items()
        if label == "in" and claim_id in supported
    )


def superseded_claims(
    edges: Iterable[EdgeView], warranted_claims: Iterable[str]
) -> dict[str, str]:
    """Layer 1, the pre-filter: ``claim_id -> the claim that retired it``.

    A ``supersede`` counts **only when its source is in ``warranted_claims``** —
    the provisionally warranted set from :func:`provisionally_warranted`. So a
    replacement that is defeated (``challenged``), still disputed (also
    ``challenged``, via ``undec``) or ungrounded (``proposed``) retires nothing.
    Ties go to the later log position: the most recent *counting* supersession
    names the successor.

    A supersession whose source is not in the snapshot at all therefore does NOT
    count — it cannot be shown warranted. That inverts the earlier reading, and
    the inversion is the point: an absent replacement is an *unverifiable* one,
    and withdrawing the current claim on an unverifiable replacement is how a
    partial fold silently deletes an answer. Such a fold is only reachable by
    reading around the log's own foreign key.
    """
    warranted = frozenset(warranted_claims)
    retired: dict[str, tuple[int, str]] = {}
    for edge in edges:
        if edge.op != SUPERSEDE:
            continue
        if edge.src not in warranted:
            continue
        current = retired.get(edge.dst)
        if current is None or edge.seq > current[0]:
            retired[edge.dst] = (edge.seq, edge.src)
    return {dst: src for dst, (_, src) in retired.items()}


def classify(
    label: DungLabel | None, *, superseded: bool, supported: bool
) -> Status:
    """Layer 3, the post-classification: a Dung label + two facts → a status.

    ``undec`` maps to ``challenged`` deliberately. A live unresolved dispute and
    a defeated claim have the same consequence for answering, so exposing a
    third "undecided" answer would only invite a caller to treat it as a weak
    yes.
    """
    if superseded:
        return "superseded"
    if label != "in":
        return "challenged"
    return "warranted" if supported else "proposed"


def compute_statuses(view: EdgeSetView) -> StatusTable:
    """Run the three layers over one snapshot. Pure, model-free, no writes.

    Provisionality is *marked* here (``ClaimStatus.stub_chain``) and *refused*
    at the query surface — :meth:`StatusQuery.status` and
    :meth:`StatusQuery.explain` are what callers use and they fail closed. That
    split keeps the arithmetic inspectable without making the default path
    launder a stub.
    """
    claims = tuple(view.claims)
    edges = tuple(view.edges)
    claim_ids = tuple(sorted(c.claim_id for c in claims))
    attacks = attack_pairs(edges)

    # Layer 1 — the pre-filter needs a provisional pass first: a supersession
    # only counts when the superseding claim itself computes as `warranted`
    # there (Dung `in` AND supported), never merely "not defeated".
    provisional = grounded_labelling(DungAF(arguments=claim_ids, attacks=attacks))
    retired = superseded_claims(edges, provisionally_warranted(edges, provisional))

    # Layer 2 — the fixed point, over the attack relation ONLY, with the
    # superseded claims absent. `grounded_labelling` silently ignores attacks
    # naming an argument it was not given, which is exactly what "leaves the
    # framework" means: a retired claim neither attacks nor is labelled.
    live = tuple(cid for cid in claim_ids if cid not in retired)
    labels = grounded_labelling(DungAF(arguments=live, attacks=attacks))

    supporters: dict[str, set[str]] = {}
    attackers: dict[str, set[str]] = {}
    for edge in edges:
        if edge.op == SUPPORT:
            supporters.setdefault(edge.dst, set()).add(edge.src)
        elif edge.op == ATTACK:
            attackers.setdefault(edge.dst, set()).add(edge.src)

    chains = _stub_chains(claims, edges)

    statuses: dict[str, ClaimStatus] = {}
    for claim_id in claim_ids:
        label = labels.get(claim_id)
        status = classify(
            label,
            superseded=claim_id in retired,
            supported=bool(supporters.get(claim_id)),
        )
        statuses[claim_id] = ClaimStatus(
            claim_id=claim_id,
            status=status,
            label=label,
            # The second axis, over the SAME label. Hard-wired unvalidated:
            # until the verification phase wires an independent check, a
            # surviving claim is `dialectically_adequate`, never `accepted`.
            acceptance=acceptance_from_labelling(
                claim_id,
                dict(labels),
                independently_validated=INDEPENDENT_VALIDATION_AVAILABLE,
            ),
            supporters=tuple(sorted(supporters.get(claim_id, ()))),
            attackers=tuple(sorted(attackers.get(claim_id, ()))),
            superseded_by=retired.get(claim_id),
            stub_chain=chains.get(claim_id, ()),
        )
    return StatusTable(
        digest=edgeset_digest(claims, edges),
        statuses=statuses,
        labels=dict(labels),
        live=live,
    )


def _stub_chains(
    claims: Sequence[ClaimView], edges: Sequence[EdgeView]
) -> dict[str, tuple[str, ...]]:
    """Per claim, the ``stub`` claims that could have influenced its verdict.

    The influence set is the transitive closure over INCOMING ``support`` /
    ``attack`` / ``supersede`` edges: a claim's verdict depends on its
    supporters, its attackers, its attackers' attackers (that is what
    reinstatement is), and on whatever retired it. ``revise`` is not followed —
    it carries no force in the labelling.

    Returns ``{}`` outright when the snapshot holds no stub at all, which is the
    common case once claims are constructed, so the walk costs nothing when it
    would find nothing. Otherwise it is one closure per claim — O(N·E) worst
    case, paid only while stubs remain, and the cure for a stub is to construct
    it rather than to optimise this.
    """
    stubs = {c.claim_id for c in claims if c.provenance == "stub"}
    if not stubs:
        return {}
    incoming: dict[str, set[str]] = {}
    for edge in edges:
        if edge.op in _INFLUENCING_OPS:
            incoming.setdefault(edge.dst, set()).add(edge.src)
    out: dict[str, tuple[str, ...]] = {}
    for claim in claims:
        seen: set[str] = set()
        frontier = [claim.claim_id]
        while frontier:
            current = frontier.pop()
            if current in seen:
                continue
            seen.add(current)
            frontier.extend(incoming.get(current, ()))
        touched = seen & stubs
        if touched:
            out[claim.claim_id] = tuple(sorted(touched))
    return out


# ── explanation ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class EdgeExplanation:
    """One incoming edge, with the status of the claim it comes from."""

    op: str
    src: str
    src_status: str
    evidence_locator: str | None
    origin: str


@dataclass(frozen=True)
class Explanation:
    """Why a claim has the status it has — the verdict plus its incoming edges.

    Rendered from the same table the verdict came from, so an explanation can
    never disagree with the status it explains. ``revisions`` is reported for the
    reader even though ``revise`` takes no part in the labelling: knowing a claim
    was revised is exactly what a reader looking at a ``challenged`` verdict
    wants next.
    """

    verdict: ClaimStatus
    digest: str
    supports: tuple[EdgeExplanation, ...] = ()
    attacks: tuple[EdgeExplanation, ...] = ()
    supersessions: tuple[EdgeExplanation, ...] = ()
    revisions: tuple[EdgeExplanation, ...] = ()

    @property
    def provisional(self) -> bool:
        return self.verdict.provisional

    def render(self) -> str:
        """A plain-text rendering — deterministic, and it leads with the
        provisional warning when there is one, because a warning after the
        verdict is a warning nobody reads."""
        lines: list[str] = []
        if self.provisional:
            lines.append(
                f"PROVISIONAL: {len(self.verdict.stub_chain)} claim(s) in this "
                "chain have provenance='stub' (located mechanically, not "
                "constructed by reading). This verdict is not trustworthy."
            )
        lines.append(self.verdict.claim_id)
        lines.append(f"  status: {self.verdict.status}")
        lines.append(f"  dung label: {self.verdict.label or '-'}")
        lines.append(f"  acceptance: {self.verdict.acceptance.status}")
        for title, entries in (
            ("supported by", self.supports),
            ("attacked by", self.attacks),
            ("superseded by", self.supersessions),
            ("revised by", self.revisions),
        ):
            for entry in entries:
                lines.append(
                    f"  {title}: {entry.src} [{entry.src_status}] "
                    f"@ {entry.evidence_locator or '-'} ({entry.origin})"
                )
        lines.append(f"  edge-set digest: {self.digest}")
        return "\n".join(lines)


# ── the query surface ───────────────────────────────────────────────────────


class StatusQuery:
    """``status`` / ``explain`` as QUERIES over the log, memoised by digest.

    Reads only. There is no write path in this class and no status is stored
    anywhere: the labelling is recomputed whenever the claim/edge set changes,
    and the memo is keyed by :func:`edgeset_digest` so an append yields a new key
    rather than needing an invalidation write.

    The refusal lives here. Both queries fail closed when the verdict's chain
    touches a ``stub`` claim; ``allow_provisional=True`` returns the verdict
    hard-labelled instead (:attr:`ClaimStatus.provisional`, and a leading warning
    in :meth:`Explanation.render`).

    Args:
        source: anything satisfying :class:`EdgeSetSource` — the runtime's
            append-only log, or an in-memory :class:`EdgeSet`.
        cache_size: how many digests to keep. The current digest is the only one
            a query can hit; keeping a few makes an A/B that alternates between
            two snapshots cheap. ``0`` disables the memo.
    """

    def __init__(self, source: EdgeSetSource, *, cache_size: int = 4) -> None:
        self.source = source
        self.cache_size = max(0, cache_size)
        self._cache: dict[str, StatusTable] = {}
        self._hits = 0
        self._misses = 0

    # ── cache telemetry (the plan's Increment-1 metric) ─────────────────────

    @property
    def cache_hits(self) -> int:
        return self._hits

    @property
    def cache_misses(self) -> int:
        """Recomputations. One per distinct claim/edge set the query has seen."""
        return self._misses

    def table(self) -> StatusTable:
        """The whole corpus labelled at the CURRENT snapshot.

        Folds the log, digests it, and returns the memoised labelling when the
        digest is unchanged. No refusal here — a table is a corpus view, and the
        stub marking travels on every row.
        """
        return self._table_for(self.source.fold())

    def _table_for(self, view: EdgeSetView) -> StatusTable:
        """Label ONE already-folded snapshot, hitting the memo when it applies.

        Separate from :meth:`table` so a caller that also needs the snapshot's
        edges (:meth:`explain`) folds once: two folds could straddle an append,
        and an explanation drawn from a different edge set than its verdict would
        be an explanation of a different verdict.
        """
        digest = edgeset_digest(view.claims, view.edges)
        cached = self._cache.get(digest)
        if cached is not None:
            self._hits += 1
            return cached
        self._misses += 1
        table = compute_statuses(view)
        if self.cache_size:
            if len(self._cache) >= self.cache_size:
                # Drop the oldest entry: insertion order is the arrival order of
                # the digests, and the current one is always the useful one.
                self._cache.pop(next(iter(self._cache)))
            self._cache[digest] = table
        return table

    def status(self, claim_id: str, *, allow_provisional: bool = False) -> ClaimStatus:
        """The computed verdict for one claim.

        Raises:
            UnknownClaimError: the log holds no such claim.
            ProvisionalStatusError: the verdict's chain touches a ``stub`` claim
                and ``allow_provisional`` is ``False``.
        """
        verdict = self.table().get(claim_id)
        if verdict is None:
            raise UnknownClaimError(f"no such claim in the log: {claim_id}")
        if verdict.provisional and not allow_provisional:
            raise ProvisionalStatusError(claim_id, verdict.stub_chain)
        return verdict

    def explain(self, claim_id: str, *, allow_provisional: bool = False) -> Explanation:
        """The verdict plus the incoming edges that produced it.

        Same refusal as :meth:`status`, for the same reason: an explanation of a
        laundered verdict is a more persuasive laundered verdict.
        """
        view = self.source.fold()
        table = self._table_for(view)
        verdict = table.get(claim_id)
        if verdict is None:
            raise UnknownClaimError(f"no such claim in the log: {claim_id}")
        if verdict.provisional and not allow_provisional:
            raise ProvisionalStatusError(claim_id, verdict.stub_chain)
        grouped: dict[str, list[EdgeExplanation]] = {
            SUPPORT: [],
            ATTACK: [],
            SUPERSEDE: [],
            REVISE: [],
        }
        for edge in sorted(view.edges, key=lambda e: e.seq):
            if edge.dst != claim_id or edge.op not in grouped:
                continue
            source_verdict = table.get(edge.src)
            grouped[edge.op].append(
                EdgeExplanation(
                    op=edge.op,
                    src=edge.src,
                    src_status=source_verdict.status if source_verdict else "unknown",
                    evidence_locator=edge.evidence_locator,
                    origin=edge.origin,
                )
            )
        return Explanation(
            verdict=verdict,
            digest=table.digest,
            supports=tuple(grouped[SUPPORT]),
            attacks=tuple(grouped[ATTACK]),
            supersessions=tuple(grouped[SUPERSEDE]),
            revisions=tuple(grouped[REVISE]),
        )

    def summary(self) -> dict[str, int]:
        """Corpus counts by status, at the current snapshot."""
        return self.table().summary()


def status(
    source: EdgeSetSource, claim_id: str, *, allow_provisional: bool = False
) -> ClaimStatus:
    """One-shot :meth:`StatusQuery.status` — no memo survives the call."""
    return StatusQuery(source, cache_size=0).status(
        claim_id, allow_provisional=allow_provisional
    )


def explain(
    source: EdgeSetSource, claim_id: str, *, allow_provisional: bool = False
) -> Explanation:
    """One-shot :meth:`StatusQuery.explain` — no memo survives the call."""
    return StatusQuery(source, cache_size=0).explain(
        claim_id, allow_provisional=allow_provisional
    )


__all__ = [
    "ATTACK",
    "ClaimStatus",
    "ClaimView",
    "EdgeExplanation",
    "EdgeSet",
    "EdgeSetSource",
    "EdgeSetView",
    "EdgeView",
    "Explanation",
    "ProvisionalStatusError",
    "REVISE",
    "STATUSES",
    "SUPERSEDE",
    "SUPPORT",
    "Status",
    "StatusError",
    "StatusQuery",
    "StatusTable",
    "UnknownClaimError",
    "attack_pairs",
    "classify",
    "compute_statuses",
    "edgeset_digest",
    "explain",
    "provisionally_warranted",
    "status",
    "superseded_claims",
    "supported_claims",
]
