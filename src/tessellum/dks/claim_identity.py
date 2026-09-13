"""tessellum.dks.claim_identity — THREE identities for a derived claim.

P0 of the query-time-DKS plan: the prerequisite that blocks consolidation.
Consolidation counts *"recurrence >= 3 from >= 2 independent contexts"*, and a
count needs an identity — without one, a re-derivation forks into a second claim
and recurrence is uncountable by construction.

**Two earlier keys were both wrong, and the second one is the bug this module
exists to remove.** Keying on ``(note_id, span_locator, predicate_slot)`` puts a
domain predicate into identity, which makes identity model-dependent. Keying on
``(note_id, span_locator)`` *alone* is worse in a quieter way: **one span states
several independent propositions** — the same paragraph can give an owner *and* a
launch date — and **one multi-hop proposition can rest on several spans**. Under
the location-only key an owner claim, a launch-date claim, a negation of the
owner claim, and a rival owner claim all mint the SAME id; anything that keys
feedback on that id then hands a *changed* proposition the *replaced* one's
history. Span location is therefore neither necessary nor sufficient for
propositional identity.

So there are three identities, and every consumer must say which one it counts:

======================  ==========================================  ===========
Object                  Identity                                    Model?
======================  ==========================================  ===========
Evidence occurrence     ``(note_id, span_locator, source_note_hash)``  no
Proposition version     immutable; statement + declared polarity +
                        scope + qualifiers. Several may share one
                        evidence occurrence; one may cite several    yes, across
                                                                     spans only
Derivation event        a premise SET -> a proposition version, at
                        an episode                                   no
======================  ==========================================  ===========

- :func:`evidence_occurrence_id` — a *located string at a source version*. This
  is what the old ``derivation_id`` nearly was, and :func:`derivation_id` is
  retained as its legacy spelling. It identifies **evidence**, never a claim:
  do not key feedback, warrants or recurrence on it (see
  :func:`feedback_subject_id` and :data:`TRIAL_HISTORY_SUBJECT_RULE`).
- :func:`proposition_version_id` — the level feedback, warrants and recurrence
  **must** key on. It excludes the cited evidence on purpose, so citing a third
  span does not fork the proposition, and it excludes location on purpose, so an
  edit elsewhere in the note does not fork it either.
- :func:`derivation_event_id` — one episode's act of deriving a proposition from
  a premise set. Canonicalised over the premise *set*, so premise order and
  repetition cannot mint a second event.

**How a paraphrase can coalesce while a negation cannot, without a semantic
oracle.** Cross-span sameness is a judgement about meaning; it needs a model and
it is deliberately **not built** here. The default is therefore **fail-safe: do
not merge.** A distinct rendering is a distinct proposition version unless an
injected :class:`FactIdentityResolver` affirmatively says two are the same
(:func:`coalesce_propositions`). A negation consequently never coalesces on the
deterministic path, and a paraphrase coalesces only when a resolver says so —
which is exactly the rule that *neither same-span location nor similar wording
may merge incompatible claims*. No similarity metric, token-overlap rule or
embedding threshold ships behind that port: a lexical proxy would merge claims
that share vocabulary and split claims that paraphrase.

**The three-way relationship P0 owes its consumers, stated once.** An *unchanged
locator* plus a *changed rendering* (:func:`text_hash` moves) is a **new
proposition version over the same evidence occurrence** — never the old
proposition with a new wording. So *"A owns X"* becoming *"B owns X"* keeps the
citation and starts a fresh subject: no warrant, no feedback and no recurrence
count carries over, and whether the replaced version's incoming support carries
over is an explicit logged keep/drop decision on the ``revise`` operator, not an
implication of the locator having held. Conversely an *unchanged rendering* whose
*source note changed* is the same proposition over a **new** evidence occurrence
— which is what a staleness flag is computed from.

Even an over-eager resolver cannot merge across a **declared** disagreement:
:func:`coalesce_propositions` refuses a merge whose members declare a different
polarity, a different scope, or conflicting qualifier values. That check is a
comparison of what a caller *declared*, not an inference about meaning.

**The locator is content-anchored so it is insertion-stable.** An index
(``c0``, ``c1``, ...) or a raw character offset renumbers every later claim when
a sentence is inserted above it. :func:`anchor_locator` addresses a span by a
digest of its own normalised text, so an edit *elsewhere* cannot move it; the
source version enters the evidence key separately, which is what lets a changed
note flag its dependent claims as stale instead of silently re-pointing them.

Identity is content-hashed with the SAME construction as
``capability._replay_token`` (:func:`_content_id`), so claim identity and replay
identity agree: an append keyed on one of these ids is idempotent for the reason
a replayed result is.

Pure: no clock, no randomness, no I/O, no model call, and no import of the
runtime package (the Dependency Rule — storing these ids is a runtime concern).
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Literal, Protocol, runtime_checkable

# ── the content-id construction (shared with replay identity) ───────────────

# Hex characters kept from the digest — matches ``capability._replay_token``.
_ID_HEX = 32

# Reserved: the part terminator of :func:`_content_id`. A key or value carrying
# it could forge a different part boundary, so it is refused at the door.
_NUL = "\0"


def _content_id(prefix: str, *parts: str) -> str:
    """SHA-256 over NUL-terminated parts, truncated to :data:`_ID_HEX`.

    Byte-for-byte the construction ``capability._replay_token`` uses, so claim
    identity and replay identity agree. Duplicated rather than imported because
    that function's ``dks:`` prefix is part of ITS contract; the discipline (NUL
    termination so ``("ab", "c")`` and ``("a", "bc")`` differ, fixed truncation)
    is what has to match."""
    h = hashlib.sha256()
    for p in parts:
        h.update(p.encode("utf-8"))
        h.update(b"\0")
    return prefix + h.hexdigest()[:_ID_HEX]


# ── span text normalisation ─────────────────────────────────────────────────

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_span_text(text: str) -> str:
    """Reduce a span to what ADDRESSES it — NFC, whitespace collapsed, folded.

    A re-wrap, a trailing space or a case-only edit is therefore not a new span.
    Anything else is a *different* span, and honestly so: the anchor addresses
    content, and the content moved. Deterministic."""
    folded = unicodedata.normalize("NFC", text)
    return _WHITESPACE_RE.sub(" ", folded).strip().casefold()


def note_version_hash(body: str) -> str:
    """The source version a claim was read at — a digest of the WHOLE note body.

    Unlike :func:`normalize_span_text` this folds nothing but Unicode form: a
    case-only or whitespace-only edit *is* a new version of the note, because
    the point of this hash is to notice that the cited note changed at all. It
    is the third component of an evidence occurrence, and the input to the
    staleness flag a later phase raises when a cited note is edited."""
    return _content_id("nv:", unicodedata.normalize("NFC", body))


# ── level 1: the span locator ───────────────────────────────────────────────

LocatorKind = Literal["anchor", "char_range"]


@dataclass(frozen=True)
class SpanLocator:
    """A note-relative address for one span — one third of an evidence
    occurrence's key.

    Two kinds, and the difference is load-bearing:

    - ``"anchor"`` — a **content anchor**: a digest of the span's normalised
      text plus an ``occurrence`` ordinal that separates spans whose normalised
      text is *identical*. **Insertion-stable**: inserting a sentence above a
      span leaves the span's own content, and therefore its address, unchanged.
      This is the kind identity should use.
    - ``"char_range"`` — raw ``[start, end)`` character offsets. Provided
      because some callers only have offsets, and marked **not
      insertion-stable**: an edit above the span shifts it and mints a new
      address. Never key recurrence counting on it.

    ``section`` is an optional stable containing-section path; it scopes the
    occurrence ordinal and is part of the canonical form, so the same sentence
    under two headings is two spans."""

    kind: LocatorKind
    anchor: str = ""
    start: int = -1
    end: int = -1
    occurrence: int = 0
    section: str = ""

    def __post_init__(self) -> None:
        if self.occurrence < 0:
            raise ValueError(f"occurrence must be >= 0, got {self.occurrence}")
        if self.kind == "anchor":
            if not self.anchor:
                raise ValueError("an 'anchor' locator needs a non-empty anchor")
        elif self.kind == "char_range":
            if self.start < 0 or self.end < self.start:
                raise ValueError(
                    "a 'char_range' locator needs 0 <= start <= end, got "
                    f"[{self.start}, {self.end})"
                )
        else:
            raise ValueError(f"unknown locator kind {self.kind!r}")

    @property
    def insertion_stable(self) -> bool:
        """``True`` for a content anchor, ``False`` for raw offsets — the
        property a recurrence counter must check before trusting an address."""
        return self.kind == "anchor"

    def canonical(self) -> str:
        """The stable string form hashed into an evidence-occurrence id. Pure."""
        if self.kind == "anchor":
            return f"anchor|{self.section}|{self.anchor}|{self.occurrence}"
        return f"char_range|{self.section}|{self.start}|{self.end}|{self.occurrence}"


def anchor_locator(
    span_text: str, *, occurrence: int = 0, section: str = "",
) -> SpanLocator:
    """A content-anchored locator for ``span_text`` (the insertion-stable kind).

    Raises on an empty (or whitespace-only) span: an unaddressable span must not
    silently collapse onto a shared address."""
    normalized = normalize_span_text(span_text)
    if not normalized:
        raise ValueError("cannot anchor an empty span")
    return SpanLocator(
        kind="anchor",
        anchor=_content_id("", normalized),
        occurrence=occurrence,
        section=section,
    )


def char_range_locator(start: int, end: int, *, section: str = "") -> SpanLocator:
    """An offset locator for ``[start, end)``. **Not insertion-stable** — see
    :class:`SpanLocator`."""
    return SpanLocator(kind="char_range", start=start, end=end, section=section)


def locators_for_spans(
    spans: Sequence[str], *, section: str = "",
) -> list[SpanLocator]:
    """Content anchors for an ORDERED sequence of spans from one note.

    The ``occurrence`` ordinal counts only spans whose normalised text is
    identical, so inserting a *different* span above one never renumbers it —
    which is the whole point of replacing an index-based scheme. Two spans with
    byte-identical normalised text are indistinguishable by content, so an
    ordinal is the honest tie-break."""
    seen: dict[str, int] = {}
    out: list[SpanLocator] = []
    for span in spans:
        key = normalize_span_text(span)
        ordinal = seen.get(key, 0)
        seen[key] = ordinal + 1
        out.append(anchor_locator(span, occurrence=ordinal, section=section))
    return out


# ── identity 1: the evidence occurrence — a located string at a version ─────

UNPINNED_SOURCE_VERSION = ""
"""The ``source_note_hash`` of an occurrence whose source version is unknown.

Honest rather than convenient: an unpinned occurrence addresses a span in
*whatever* version of the note is on disk, so it cannot be checked for
staleness. A derivation that will be counted, warranted or promoted must pin
:func:`note_version_hash`; the unpinned form exists for write-time extractors
that have the body but not yet a committed version."""


def evidence_occurrence_id(
    note_id: str,
    locator: SpanLocator,
    source_note_hash: str = UNPINNED_SOURCE_VERSION,
) -> str:
    """Identity of ONE located string at ONE source version — no model.

    Deliberately absent from the key: the proposition read out of the span
    (several may be read from one span), and any domain predicate (naming one is
    a model act). Deterministic across processes (SHA-256, not ``hash()``)."""
    if not note_id:
        raise ValueError("an evidence occurrence needs a non-empty note_id")
    return _content_id("evidence:", note_id, locator.canonical(), source_note_hash)


def derivation_id(
    note_id: str,
    locator: SpanLocator,
    source_note_hash: str = UNPINNED_SOURCE_VERSION,
) -> str:
    """LEGACY SPELLING of :func:`evidence_occurrence_id`, retained for callers.

    It names **evidence**, not a claim. Keying feedback, a warrant or a
    recurrence count on it is the defect this module was rewritten to remove —
    use :func:`feedback_subject_id` over a :class:`PropositionVersion`."""
    return evidence_occurrence_id(note_id, locator, source_note_hash)


@dataclass(frozen=True)
class EvidenceOccurrence:
    """A located string at a source version, as a value.

    ``occurrence_id`` is computed rather than stored, so an occurrence's id can
    never disagree with the fields it is supposed to be a digest of."""

    note_id: str
    locator: SpanLocator
    source_note_hash: str = UNPINNED_SOURCE_VERSION

    def __post_init__(self) -> None:
        if not self.note_id:
            raise ValueError("an evidence occurrence needs a non-empty note_id")

    @property
    def occurrence_id(self) -> str:
        return evidence_occurrence_id(
            self.note_id, self.locator, self.source_note_hash
        )

    @property
    def version_pinned(self) -> bool:
        """``False`` for :data:`UNPINNED_SOURCE_VERSION` — an occurrence whose
        staleness cannot be detected."""
        return self.source_note_hash != UNPINNED_SOURCE_VERSION

    def at_version(self, source_note_hash: str) -> EvidenceOccurrence:
        """The same located string at a DIFFERENT source version — a different
        occurrence, and its id says so."""
        return replace(self, source_note_hash=source_note_hash)


def evidence_occurrence(
    note_id: str,
    span_text: str,
    *,
    occurrence: int = 0,
    section: str = "",
    source_note_hash: str = UNPINNED_SOURCE_VERSION,
) -> EvidenceOccurrence:
    """An :class:`EvidenceOccurrence` from raw span text (content-anchored)."""
    return EvidenceOccurrence(
        note_id=note_id,
        locator=anchor_locator(span_text, occurrence=occurrence, section=section),
        source_note_hash=source_note_hash,
    )


def evidence_occurrence_ids_for_spans(
    note_id: str,
    spans: Sequence[str],
    *,
    section: str = "",
    source_note_hash: str = UNPINNED_SOURCE_VERSION,
) -> list[str]:
    """One occurrence id per span, in order — the helper a per-note extractor
    wants. Insertion above a span never renumbers it (content anchors)."""
    return [
        evidence_occurrence_id(note_id, loc, source_note_hash)
        for loc in locators_for_spans(spans, section=section)
    ]


def derivation_ids_for_spans(
    note_id: str,
    spans: Sequence[str],
    *,
    section: str = "",
    source_note_hash: str = UNPINNED_SOURCE_VERSION,
) -> list[str]:
    """LEGACY SPELLING of :func:`evidence_occurrence_ids_for_spans`."""
    return evidence_occurrence_ids_for_spans(
        note_id, spans, section=section, source_note_hash=source_note_hash
    )


def text_hash(text: str) -> str:
    """The hash of a RENDERING — a claim's wording, not any of the three ids.

    Normalised the same way as a span, so a re-wrap is not a re-wording."""
    return _content_id("text:", normalize_span_text(text))


# ── identity 2: the proposition version — what feedback keys on ─────────────

Polarity = Literal["affirm", "deny"]
"""Whether a proposition ASSERTS or DENIES its statement, **as declared by the
reader that produced it**. Nothing in this module infers polarity from text;
declaring it is what lets a merge across a negation be refused deterministically
without a semantic oracle."""

PairsInput = Mapping[str, str] | Sequence[tuple[str, str]] | None


def _pairs(raw: PairsInput, *, label: str) -> tuple[tuple[str, str], ...]:
    """Canonical, sorted, de-duplicated key/value pairs — order-insensitive.

    Fails loud on a conflicting duplicate key (the caller declared two values
    for one dimension) and on a NUL byte (it would forge a part boundary in
    :func:`_content_id`)."""
    if raw is None:
        return ()
    items: Iterable[tuple[str, str]]
    if hasattr(raw, "items"):
        items = tuple(raw.items())  # type: ignore[union-attr]
    else:
        items = tuple(tuple(p) for p in raw)  # type: ignore[misc]
    seen: dict[str, str] = {}
    for pair in items:
        key, value = pair
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError(f"{label} keys and values must be str, got {pair!r}")
        if not key:
            raise ValueError(f"a {label} key must be non-empty")
        if _NUL in key or _NUL in value:
            raise ValueError(f"a {label} key/value may not contain NUL")
        if key in seen and seen[key] != value:
            raise ValueError(
                f"conflicting {label} values for {key!r}: "
                f"{seen[key]!r} vs {value!r}"
            )
        seen[key] = value
    return tuple(sorted(seen.items()))


def proposition_version_id(
    statement: str,
    *,
    polarity: Polarity = "affirm",
    scope: PairsInput = None,
    qualifiers: PairsInput = None,
) -> str:
    """Identity of ONE immutable proposition version — deterministic, no model.

    In the key: the normalised statement, the declared polarity, the declared
    scope and the declared qualifiers. **Not** in the key:

    - the **cited evidence**, so one proposition citing three spans is one
      proposition, and adding a fourth citation does not fork it;
    - the **location**, so an edit elsewhere in the note does not fork it;
    - any **domain predicate slot**, so identity stays model-free.

    A different rendering therefore mints a different version — the fail-safe
    default. Merging two renderings is :func:`coalesce_propositions`' job, and
    only under an injected :class:`FactIdentityResolver`."""
    normalized = normalize_span_text(statement)
    if not normalized:
        raise ValueError("a proposition needs a non-empty statement")
    if polarity not in ("affirm", "deny"):
        raise ValueError(f"unknown polarity {polarity!r}")
    parts = [normalized, polarity, "scope"]
    for key, value in _pairs(scope, label="scope"):
        parts += [key, value]
    parts.append("qualifiers")
    for key, value in _pairs(qualifiers, label="qualifier"):
        parts += [key, value]
    return _content_id("prop:", *parts)


@dataclass(frozen=True)
class PropositionVersion:
    """One immutable proposition version: the level feedback keys on.

    ``evidence`` is the set of evidence-occurrence ids this version cites — one
    or several — and it is **outside** the identity, so:

    - several propositions may share one evidence occurrence (an owner and a
      launch date read from the same paragraph stay two propositions), and
    - one proposition may cite several occurrences (a multi-hop claim stays one
      proposition however many spans support it).

    ``supersedes`` records that this version replaced another. That is
    **lineage, not identity**: the replacement gets its own id, and it inherits
    no warrant and no feedback history. Whether the replaced version's incoming
    support carries over is an explicit logged decision elsewhere (the ``revise``
    operator's keep/drop), never an implicit consequence of a stable locator."""

    statement: str
    polarity: Polarity = "affirm"
    scope: tuple[tuple[str, str], ...] = ()
    qualifiers: tuple[tuple[str, str], ...] = ()
    evidence: tuple[str, ...] = ()
    supersedes: str = ""

    def __post_init__(self) -> None:
        if not normalize_span_text(self.statement):
            raise ValueError("a proposition needs a non-empty statement")
        if self.polarity not in ("affirm", "deny"):
            raise ValueError(f"unknown polarity {self.polarity!r}")
        object.__setattr__(self, "scope", _pairs(self.scope, label="scope"))
        object.__setattr__(
            self, "qualifiers", _pairs(self.qualifiers, label="qualifier")
        )
        object.__setattr__(self, "evidence", tuple(sorted(set(self.evidence))))

    @property
    def proposition_id(self) -> str:
        """Computed, never stored: an id cannot drift from its own fields."""
        return proposition_version_id(
            self.statement,
            polarity=self.polarity,
            scope=self.scope,
            qualifiers=self.qualifiers,
        )

    @property
    def text_hash(self) -> str:
        """The rendering hash of the statement (a convenience, not an id)."""
        return text_hash(self.statement)

    def citing(self, *evidence_ids: str) -> PropositionVersion:
        """The SAME proposition, citing more evidence — ``proposition_id``
        unchanged, because evidence is outside identity."""
        return replace(
            self, evidence=tuple(sorted(set(self.evidence) | set(evidence_ids)))
        )

    def restated(
        self,
        statement: str,
        *,
        polarity: Polarity | None = None,
        scope: PairsInput = None,
        qualifiers: PairsInput = None,
        evidence: Sequence[str] | None = None,
    ) -> PropositionVersion:
        """A NEW version replacing this one — new id, ``supersedes`` set.

        Used for every change of the asserted content, including the one that
        looks most like a re-wording: *"A owns X"* to *"B owns X"* holds the
        locator and changes the proposition, so it must not reuse A's warrant or
        feedback. Nothing is carried but the citation set (the same spans are
        still what was read) and, unless overridden, the declared scope and
        qualifiers."""
        return PropositionVersion(
            statement=statement,
            polarity=self.polarity if polarity is None else polarity,
            scope=self.scope if scope is None else _pairs(scope, label="scope"),
            qualifiers=(
                self.qualifiers
                if qualifiers is None
                else _pairs(qualifiers, label="qualifier")
            ),
            evidence=self.evidence if evidence is None else tuple(evidence),
            supersedes=self.proposition_id,
        )

    def same_proposition_as(self, other: PropositionVersion) -> bool:
        """Deterministic sameness only: identical declared content. Two
        renderings of one fact are NOT the same by this test — that is
        :func:`coalesce_propositions` under a resolver."""
        return self.proposition_id == other.proposition_id


def proposition_version(
    statement: str,
    *,
    polarity: Polarity = "affirm",
    scope: PairsInput = None,
    qualifiers: PairsInput = None,
    evidence: Sequence[str] = (),
    supersedes: str = "",
) -> PropositionVersion:
    """Build a :class:`PropositionVersion`, normalising scope/qualifier input
    from a mapping or a pair sequence."""
    return PropositionVersion(
        statement=statement,
        polarity=polarity,
        scope=_pairs(scope, label="scope"),
        qualifiers=_pairs(qualifiers, label="qualifier"),
        evidence=tuple(evidence),
        supersedes=supersedes,
    )


TRIAL_HISTORY_SUBJECT_RULE = (
    "Feedback, warrants, trial history (n_pass/n_trial, eta) and recurrence "
    "counts key on the PROPOSITION VERSION id — feedback_subject_id(proposition) "
    "— never on an evidence-occurrence id. An evidence occurrence is a located "
    "string; several propositions can share one, so a store keyed on it hands a "
    "changed proposition the replaced one's history. A replacement version "
    "(PropositionVersion.restated) records `supersedes` for lineage and starts "
    "with NO history of its own; carrying anything forward is an explicit logged "
    "decision, not a consequence of a stable locator."
)
"""The rule every consumer of these ids has to obey, stated once so a consumer
can cite it instead of re-deriving it."""


def feedback_subject_id(proposition: PropositionVersion) -> str:
    """The ONLY id a warrant, a feedback row or a recurrence count may key on.

    See :data:`TRIAL_HISTORY_SUBJECT_RULE` for why an evidence-occurrence id is
    the wrong subject."""
    return proposition.proposition_id


# ── identity 3: the derivation event — premises -> proposition, at an episode ─


def derivation_event_id(
    *, episode_id: str, proposition_id: str, premises: Sequence[str] = ()
) -> str:
    """Identity of one derivation ACT — deterministic, no model.

    Canonicalised over the premise **set**: reordering or repeating a premise
    describes the same act, so it must not mint a second event."""
    if not episode_id:
        raise ValueError("a derivation event needs a non-empty episode_id")
    if not proposition_id:
        raise ValueError("a derivation event needs a proposition_id")
    canonical = sorted(set(premises))
    return _content_id(
        "derivation:", episode_id, proposition_id, str(len(canonical)), *canonical
    )


@dataclass(frozen=True)
class DerivationEvent:
    """One episode connecting a premise set to a proposition version.

    Kept distinct from both other identities because it is the thing that
    *recurs*: the same proposition derived in two episodes is two derivation
    events and one proposition — which is what a recurrence counter has to see
    to count anything at all."""

    episode_id: str
    proposition_id: str
    premises: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.episode_id:
            raise ValueError("a derivation event needs a non-empty episode_id")
        if not self.proposition_id:
            raise ValueError("a derivation event needs a proposition_id")

    @property
    def event_id(self) -> str:
        return derivation_event_id(
            episode_id=self.episode_id,
            proposition_id=self.proposition_id,
            premises=self.premises,
        )

    @property
    def premise_set(self) -> frozenset[str]:
        return frozenset(self.premises)


def derivation_event(
    episode_id: str, proposition: PropositionVersion | str, premises: Sequence[str] = (),
) -> DerivationEvent:
    """A :class:`DerivationEvent` from a proposition version (or its id)."""
    proposition_id = (
        proposition
        if isinstance(proposition, str)
        else proposition.proposition_id
    )
    return DerivationEvent(
        episode_id=episode_id,
        proposition_id=proposition_id,
        premises=tuple(premises),
    )


# ── the bundle: all three ids for one located derivation ────────────────────


@dataclass(frozen=True)
class DerivedClaimIdentity:
    """One derivation's three identities in one value.

    ``fact_id`` is empty until a model-backed :class:`FactIdentityResolver`
    resolves this proposition against another span's. An empty ``fact_id`` means
    **unresolved**, never "a distinct fact" — a consumer that reads it as
    distinctness re-introduces the over-counting :data:`FACT_ID_DEVIATION`
    warns about."""

    note_id: str
    locator: SpanLocator
    proposition: PropositionVersion
    source_note_hash: str = UNPINNED_SOURCE_VERSION
    fact_id: str = ""

    @property
    def evidence_id(self) -> str:
        """The located string at its source version."""
        return evidence_occurrence_id(
            self.note_id, self.locator, self.source_note_hash
        )

    @property
    def derivation_id(self) -> str:
        """LEGACY SPELLING of :attr:`evidence_id` — evidence, not a claim."""
        return self.evidence_id

    @property
    def proposition_id(self) -> str:
        return self.proposition.proposition_id

    @property
    def text_hash(self) -> str:
        return self.proposition.text_hash

    @property
    def occurrence(self) -> EvidenceOccurrence:
        return EvidenceOccurrence(
            note_id=self.note_id,
            locator=self.locator,
            source_note_hash=self.source_note_hash,
        )

    def revised(
        self,
        text: str,
        *,
        polarity: Polarity | None = None,
        scope: PairsInput = None,
        qualifiers: PairsInput = None,
    ) -> DerivedClaimIdentity:
        """The claim re-asserted with different content: the SAME evidence
        occurrence, a NEW proposition version, and **no** ``fact_id``.

        The evidence is unchanged because the cited span is unchanged. The
        proposition is new because what is asserted changed — so nothing keyed on
        the proposition (warrant, feedback, recurrence) carries over. The
        ``fact_id`` is dropped because a resolved sameness judgement was about
        the *previous* rendering and is not evidence about this one."""
        return DerivedClaimIdentity(
            note_id=self.note_id,
            locator=self.locator,
            proposition=self.proposition.restated(
                text, polarity=polarity, scope=scope, qualifiers=qualifiers
            ),
            source_note_hash=self.source_note_hash,
            fact_id="",
        )

    def resolved_as(self, fact_id: str) -> DerivedClaimIdentity:
        """Record a resolver's cross-span sameness verdict on this claim."""
        return replace(self, fact_id=fact_id)


def identify(
    note_id: str,
    locator: SpanLocator,
    text: str,
    *,
    source_note_hash: str = UNPINNED_SOURCE_VERSION,
    polarity: Polarity = "affirm",
    scope: PairsInput = None,
    qualifiers: PairsInput = None,
    fact_id: str = "",
) -> DerivedClaimIdentity:
    """Mint all three ids for one derivation of ``text`` from one span. Pure.

    ``text`` is the proposition read out of the span, so it *is* part of the
    proposition id and is *not* part of the evidence id — which is the whole
    correction: two readings of one span are two propositions over one piece of
    evidence."""
    if not note_id:
        raise ValueError("an evidence occurrence needs a non-empty note_id")
    proposition = PropositionVersion(
        statement=text,
        polarity=polarity,
        scope=_pairs(scope, label="scope"),
        qualifiers=_pairs(qualifiers, label="qualifier"),
        evidence=(evidence_occurrence_id(note_id, locator, source_note_hash),),
    )
    return DerivedClaimIdentity(
        note_id=note_id,
        locator=locator,
        proposition=proposition,
        source_note_hash=source_note_hash,
        fact_id=fact_id,
    )


# ── the cross-span fact layer — a PORT, SPECIFIED and NOT BUILT ─────────────

FAIL_SAFE_MERGE_RULE = (
    "Cross-span sameness needs a model, so the default is FAIL-SAFE: do not "
    "merge. A distinct rendering is a distinct proposition version unless an "
    "injected FactIdentityResolver affirmatively says two are the same. A "
    "negation therefore never coalesces deterministically, and a paraphrase "
    "coalesces only under a resolver — neither same-span location nor similar "
    "wording may merge incompatible claims. Refusing to merge over-counts "
    "recurrence's denominator; merging wrongly fabricates agreement, so the "
    "safe direction is the one taken here."
)
"""The merge policy, stated once so a consumer can cite it."""

FACT_ID_DEVIATION = (
    "Until a model-backed FactIdentityResolver lands, cross-span sameness is "
    "UNRESOLVED and this module merges nothing, so a consolidation gate's "
    "'independent contexts' term cannot mean distinct sources. It has to be read "
    "over EPISODES — distinct derivation events that reached the same proposition "
    "version — which is weaker than the promotion criteria intend, and weaker "
    "still because episode distinctness alone is not independence: repeated "
    "derivations tracing to one origin never corroborate, however many episode "
    "ids they carry. In a single-author corpus, counting episodes counts habits "
    "of description alongside evidence. Stated here so that no consumer adopts "
    "the weaker reading silently."
)
"""The recorded deviation P0 owes its consumers. Consolidation must cite this
rather than quietly reading recurrence as source diversity."""


@dataclass(frozen=True)
class ClaimRendering:
    """A proposition version as a fact resolver sees it.

    ``context`` is optional surrounding prose a resolver may read (the span, the
    paragraph, the note title). It is *evidence for the resolver's judgement*,
    never part of any id."""

    proposition: PropositionVersion
    context: str = ""

    @property
    def key(self) -> str:
        """The id a resolver's returned mapping is keyed on."""
        return self.proposition.proposition_id

    @property
    def text(self) -> str:
        return self.proposition.statement


@runtime_checkable
class FactIdentityResolver(Protocol):
    """The port for the cross-span layer. **No semantic implementation here.**

    Deciding that two *different* renderings state the same fact is a judgement
    about meaning, so it needs a model — one of the few genuinely semantic steps
    in this pipeline. No similarity metric, token-overlap rule or embedding
    threshold ships behind this port on purpose: a lexical proxy would merge
    claims that merely share vocabulary and split claims that paraphrase, and a
    consolidation gate's independence term would then count an author's habits
    of description as independent evidence. An honest hole beats a confident
    wrong answer.

    An implementation returns ``proposition_id -> fact key`` covering only the
    propositions it is confident about. An absent key means **unresolved**, and a
    consumer must treat unresolved as "no cross-span merge", never as "distinct
    fact". Two propositions sharing a fact key are a *proposal* to merge, which
    :func:`coalesce_propositions` still refuses across a declared disagreement."""

    def resolve(self, claims: Sequence[ClaimRendering]) -> Mapping[str, str]: ...


@dataclass(frozen=True)
class UnresolvedFactIdentity:
    """The deferral made explicit and callable: a :class:`FactIdentityResolver`
    that resolves NOTHING.

    It exists so downstream code can be written against the port before a
    model-backed resolver exists, and so "no fact layer yet" is a named object
    in the call graph instead of a ``None`` someone forgets to check. It is not a
    heuristic — it merges no proposition at all, which is the fail-safe reading
    (:data:`FAIL_SAFE_MERGE_RULE`) and the reason :data:`FACT_ID_DEVIATION` has
    to be recorded."""

    resolver_id: str = "unresolved-fact-identity"

    def resolve(self, claims: Sequence[ClaimRendering]) -> Mapping[str, str]:
        return {}


@dataclass(frozen=True)
class ScriptedFactIdentity:
    """A deterministic reference resolver: it merges EXACTLY what it is told.

    Not a model and not a heuristic — there is no inference in it. ``groups``
    maps a fact key to the proposition ids a caller (a test, or a human review)
    has declared to state the same fact, so downstream code and the merge
    refusals can be exercised without a model and without a similarity rule. Any
    proposition absent from every group stays unresolved."""

    groups: Mapping[str, Sequence[str]]
    resolver_id: str = "scripted-fact-identity"

    def resolve(self, claims: Sequence[ClaimRendering]) -> Mapping[str, str]:
        present = {c.key for c in claims}
        out: dict[str, str] = {}
        for fact_key, members in self.groups.items():
            for member in members:
                if member in present:
                    out[member] = fact_key
        return out


@dataclass(frozen=True)
class RefusedMerge:
    """A resolver-proposed merge this module would not perform."""

    member: str
    canonical: str
    reason: str


@dataclass(frozen=True)
class PropositionCoalescence:
    """The outcome of asking a resolver which propositions are one fact.

    ``canonical`` maps EVERY input proposition id to the id it counts as — its
    own, unless an affirmed and non-refused merge moved it. ``merges`` and
    ``refused`` are the audit trail: a merge is a claim about the world, so it is
    recorded with the resolver that made it."""

    resolver_id: str
    canonical: Mapping[str, str]
    merges: tuple[tuple[str, str], ...] = ()
    refused: tuple[RefusedMerge, ...] = ()

    def canonical_id(self, proposition_id: str) -> str:
        """The counting id for ``proposition_id`` (itself when unresolved)."""
        return self.canonical.get(proposition_id, proposition_id)

    @property
    def merged_any(self) -> bool:
        return bool(self.merges)

    @property
    def groups(self) -> dict[str, tuple[str, ...]]:
        """Canonical id -> the ids counted under it, each group sorted."""
        out: dict[str, list[str]] = {}
        for member, canonical in self.canonical.items():
            out.setdefault(canonical, []).append(member)
        return {k: tuple(sorted(v)) for k, v in out.items()}


def _declared_conflict(a: PropositionVersion, b: PropositionVersion) -> str:
    """Why ``a`` and ``b`` may not be merged, from what they DECLARE — never
    from what they might mean. Empty string when nothing declared conflicts."""
    if a.polarity != b.polarity:
        return (
            "declared polarity differs "
            f"({a.polarity} vs {b.polarity}) — a negation is not a paraphrase"
        )
    if a.scope != b.scope:
        return f"declared scope differs ({dict(a.scope)} vs {dict(b.scope)})"
    b_qualifiers = dict(b.qualifiers)
    for key, value in a.qualifiers:
        other = b_qualifiers.get(key)
        if other is not None and other != value:
            return (
                f"conflicting {key} qualifier ({value!r} vs {other!r}) — "
                "a qualifier difference is a different claim"
            )
    return ""


def coalesce_propositions(
    renderings: Sequence[ClaimRendering],
    *,
    resolver: FactIdentityResolver | None = None,
) -> PropositionCoalescence:
    """Ask a resolver which propositions are one fact — FAIL-SAFE by default.

    With no resolver (or the :class:`UnresolvedFactIdentity` one) every
    proposition is its own canonical id: distinct renderings stay distinct, so a
    negation cannot coalesce with what it negates and a paraphrase coalesces only
    when a resolver affirms it (:data:`FAIL_SAFE_MERGE_RULE`).

    An affirmed merge is still refused across a **declared** disagreement — a
    different polarity or scope, or conflicting qualifier values — and the
    refusal is recorded rather than silently dropped. A resolver that returns a
    proposition it was not given is a bug, and raises."""
    active: FactIdentityResolver = (
        UnresolvedFactIdentity() if resolver is None else resolver
    )
    resolver_id = str(getattr(active, "resolver_id", type(active).__name__))
    by_id: dict[str, PropositionVersion] = {
        r.key: r.proposition for r in renderings
    }
    canonical: dict[str, str] = {pid: pid for pid in by_id}

    verdict = active.resolve(tuple(renderings))
    unknown = sorted(set(verdict) - set(by_id))
    if unknown:
        raise ValueError(
            f"resolver {resolver_id!r} returned propositions it was not given: "
            f"{unknown}"
        )

    grouped: dict[str, list[str]] = {}
    for pid, fact_key in verdict.items():
        if not fact_key:
            raise ValueError(
                f"resolver {resolver_id!r} returned an empty fact key for {pid!r}"
            )
        grouped.setdefault(fact_key, []).append(pid)

    merges: list[tuple[str, str]] = []
    refused: list[RefusedMerge] = []
    for _fact_key, members in sorted(grouped.items()):
        if len(set(members)) < 2:
            continue  # a fact key on its own is not a merge
        ordered = sorted(set(members))
        head = ordered[0]
        for member in ordered[1:]:
            reason = _declared_conflict(by_id[head], by_id[member])
            if reason:
                refused.append(RefusedMerge(member=member, canonical=head, reason=reason))
                continue
            canonical[member] = head
            merges.append((member, head))

    return PropositionCoalescence(
        resolver_id=resolver_id,
        canonical=canonical,
        merges=tuple(merges),
        refused=tuple(refused),
    )


__all__ = [
    # locators
    "LocatorKind",
    "SpanLocator",
    "normalize_span_text",
    "note_version_hash",
    "anchor_locator",
    "char_range_locator",
    "locators_for_spans",
    # identity 1 — evidence occurrence
    "UNPINNED_SOURCE_VERSION",
    "EvidenceOccurrence",
    "evidence_occurrence",
    "evidence_occurrence_id",
    "evidence_occurrence_ids_for_spans",
    "derivation_id",  # legacy spelling of evidence_occurrence_id
    "derivation_ids_for_spans",  # legacy spelling
    "text_hash",
    # identity 2 — proposition version
    "Polarity",
    "PairsInput",
    "PropositionVersion",
    "proposition_version",
    "proposition_version_id",
    "feedback_subject_id",
    "TRIAL_HISTORY_SUBJECT_RULE",
    # identity 3 — derivation event
    "DerivationEvent",
    "derivation_event",
    "derivation_event_id",
    # the bundle
    "DerivedClaimIdentity",
    "identify",
    # the cross-span fact layer (a port)
    "FAIL_SAFE_MERGE_RULE",
    "FACT_ID_DEVIATION",
    "ClaimRendering",
    "FactIdentityResolver",
    "UnresolvedFactIdentity",
    "ScriptedFactIdentity",
    "RefusedMerge",
    "PropositionCoalescence",
    "coalesce_propositions",
]
