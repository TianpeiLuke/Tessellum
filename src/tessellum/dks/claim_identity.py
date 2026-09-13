"""tessellum.dks.claim_identity — two-level identity for a derived claim.

P0 of the query-time-DKS plan: the prerequisite that blocks consolidation.
Consolidation counts *"recurrence ≥ 3 from ≥ 2 independent contexts"*, and a
count needs an identity — without one, a re-worded derivation of the same fact
forks into a second claim and recurrence is uncountable by construction.

**Two levels, and every consumer must say which one it counts.**

- **``derivation_id`` = hash(``note_id``, ``span_locator``)** — deterministic,
  **no model**. Two things are deliberately absent from the key:

  * the claim's **text**, because text is a *rendering* of the span. So a
    paraphrase does not fork the claim, and a revision preserves
    ``derivation_id`` while :func:`text_hash` moves.
  * any **domain predicate**, because naming a predicate is a model act; a
    predicate in the key would make identity model-dependent (and re-introduce
    the typed-relation vocabulary the design keeps out of identity).

- **``fact_id``** — the cross-span layer: two *different* spans stating the
  same fact. That judgement is genuinely semantic, needs a model, and is
  **specified here and deliberately not built** — see
  :class:`FactIdentityResolver` and :data:`FACT_ID_DEVIATION`.

**The locator has to be insertion-stable, and that is why it is content-
anchored.** An index (``c0``, ``c1``, …) or a raw character offset renumbers
every later claim when a sentence is inserted above it, which is exactly the
defect this module replaces. :func:`anchor_locator` addresses a span by a digest
of its own normalised text, so an edit *elsewhere* in the note cannot move it.

Identity is content-hashed with the SAME construction as
``capability._replay_token`` (:func:`_content_id`), so claim identity and replay
identity agree: an append keyed on a ``derivation_id`` is idempotent for the
same reason a replayed result is.

Pure: no clock, no randomness, no I/O, no model call, and no ``runtime`` import
(the Dependency Rule — storage of these ids is a runtime concern).
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass, replace
from typing import Literal, Mapping, Protocol, Sequence, runtime_checkable

# ── the content-id construction (shared with replay identity) ───────────────

# Hex characters kept from the digest — matches ``capability._replay_token``.
_ID_HEX = 32


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


# ── level 1: the span locator ───────────────────────────────────────────────

LocatorKind = Literal["anchor", "char_range"]


@dataclass(frozen=True)
class SpanLocator:
    """A note-relative address for one span — the second half of a
    ``derivation_id``.

    Two kinds, and the difference is load-bearing:

    - ``"anchor"`` — a **content anchor**: a digest of the span's normalised
      text plus an ``occurrence`` ordinal that separates spans whose normalised
      text is *identical*. **Insertion-stable**: inserting a sentence above a
      span leaves the span's own content, and therefore its id, unchanged. This
      is the kind identity should use.
    - ``"char_range"`` — raw ``[start, end)`` character offsets. Provided
      because some callers only have offsets, and marked **not
      insertion-stable**: an edit above the span shifts it and mints a new id.
      Never key recurrence counting on it.

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
        property a recurrence counter must check before trusting an id."""
        return self.kind == "anchor"

    def canonical(self) -> str:
        """The stable string form hashed into a ``derivation_id``. Pure."""
        if self.kind == "anchor":
            return f"anchor|{self.section}|{self.anchor}|{self.occurrence}"
        return f"char_range|{self.section}|{self.start}|{self.end}|{self.occurrence}"


def anchor_locator(
    span_text: str, *, occurrence: int = 0, section: str = "",
) -> SpanLocator:
    """A content-anchored locator for ``span_text`` (the insertion-stable kind).

    Raises on an empty (or whitespace-only) span: an unaddressable span must not
    silently collapse onto a shared id."""
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
    ordinal is the honest tie-break; inserting a further copy of THAT text above
    them does renumber, and that residual needs the cross-span layer to fix."""
    seen: dict[str, int] = {}
    out: list[SpanLocator] = []
    for span in spans:
        key = normalize_span_text(span)
        ordinal = seen.get(key, 0)
        seen[key] = ordinal + 1
        out.append(anchor_locator(span, occurrence=ordinal, section=section))
    return out


# ── level 1: the ids ────────────────────────────────────────────────────────


def derivation_id(note_id: str, locator: SpanLocator) -> str:
    """The claim's identity: a content hash over ``(note_id, span_locator)``.

    No model, no claim text, no domain predicate. Deterministic across
    processes (SHA-256, not ``hash()``)."""
    if not note_id:
        raise ValueError("derivation_id needs a non-empty note_id")
    return _content_id("claim:", note_id, locator.canonical())


def derivation_ids_for_spans(
    note_id: str, spans: Sequence[str], *, section: str = "",
) -> list[str]:
    """:func:`derivation_id` over :func:`locators_for_spans` — the helper a
    per-note extractor wants."""
    return [
        derivation_id(note_id, loc)
        for loc in locators_for_spans(spans, section=section)
    ]


def text_hash(text: str) -> str:
    """The hash of a claim's RENDERING — explicitly NOT its identity.

    This is what changes when a claim is re-worded or revised while its
    ``derivation_id`` holds. Normalised the same way as a span, so a re-wrap is
    not a revision."""
    return _content_id("text:", normalize_span_text(text))


@dataclass(frozen=True)
class DerivedClaimIdentity:
    """One claim's identity at both levels, with its rendering hash beside it.

    ``fact_id`` is empty until a model-backed :class:`FactIdentityResolver`
    exists. An empty ``fact_id`` means **unresolved**, never "a distinct fact" —
    a consumer that reads it as distinctness re-introduces the over-counting
    :data:`FACT_ID_DEVIATION` warns about."""

    derivation_id: str
    note_id: str
    locator: SpanLocator
    text_hash: str
    fact_id: str = ""

    def revised(self, text: str) -> DerivedClaimIdentity:
        """The same claim, re-rendered: ``derivation_id``, the locator and any
        resolved ``fact_id`` all survive; only ``text_hash`` moves."""
        return replace(self, text_hash=text_hash(text))


def identify(
    note_id: str, locator: SpanLocator, text: str, *, fact_id: str = "",
) -> DerivedClaimIdentity:
    """Mint a :class:`DerivedClaimIdentity` for one derivation. Pure."""
    return DerivedClaimIdentity(
        derivation_id=derivation_id(note_id, locator),
        note_id=note_id,
        locator=locator,
        text_hash=text_hash(text),
        fact_id=fact_id,
    )


# ── level 2: the cross-span fact layer — SPECIFIED, NOT BUILT ──────────────

FACT_ID_DEVIATION = (
    "Until fact_id lands, a claim has exactly one source span by construction, "
    "so a consolidation gate's 'independent contexts' term must be read over "
    "EPISODES (distinct query episodes that independently derived the same "
    "derivation_id), not over distinct sources. That is a weaker reading than "
    "the promotion criteria intend: in a single-author corpus, counting "
    "episodes counts habits of description alongside evidence. Stated here so "
    "that no consumer adopts the weaker reading silently."
)
"""The recorded deviation P0 owes its consumers. Consolidation must cite this
rather than quietly reading ``derivation_id`` recurrence as source diversity."""


@dataclass(frozen=True)
class ClaimRendering:
    """A claim as a fact resolver sees it — its identity plus the prose a model
    would have to read to decide whether two spans state the same fact."""

    identity: DerivedClaimIdentity
    text: str


@runtime_checkable
class FactIdentityResolver(Protocol):
    """The port for the cross-span layer. **Deliberately not implemented here.**

    Deciding that two *different* spans state the same fact is a judgement about
    meaning, so it needs a model — it is one of the few genuinely semantic steps
    in this pipeline. No regex, token-overlap rule or embedding threshold is
    shipped behind this port on purpose: a lexical proxy would merge claims that
    merely share vocabulary and split claims that paraphrase, and consolidation's
    independence term would then count an author's habits of description as
    independent evidence. An honest hole beats a confident wrong answer.

    An implementation returns ``derivation_id -> fact_id`` covering only the
    claims it is confident about. An absent key means **unresolved**, and a
    consumer must treat unresolved as "no cross-span merge", never as "distinct
    fact"."""

    def resolve(self, claims: Sequence[ClaimRendering]) -> Mapping[str, str]: ...


@dataclass(frozen=True)
class UnresolvedFactIdentity:
    """The deferral made explicit and callable: a :class:`FactIdentityResolver`
    that resolves NOTHING.

    It exists so downstream code can be written against the port before a
    model-backed resolver exists, and so "no fact layer yet" is a named object
    in the call graph instead of a ``None`` someone forgets to check. It is not
    a heuristic — it merges no claims at all, which is the fail-closed reading
    (every derivation stays its own fact) and the reason
    :data:`FACT_ID_DEVIATION` has to be recorded."""

    def resolve(self, claims: Sequence[ClaimRendering]) -> Mapping[str, str]:
        return {}


__all__ = [
    "LocatorKind",
    "SpanLocator",
    "normalize_span_text",
    "anchor_locator",
    "char_range_locator",
    "locators_for_spans",
    "derivation_id",
    "derivation_ids_for_spans",
    "text_hash",
    "DerivedClaimIdentity",
    "identify",
    "FACT_ID_DEVIATION",
    "ClaimRendering",
    "FactIdentityResolver",
    "UnresolvedFactIdentity",
]
