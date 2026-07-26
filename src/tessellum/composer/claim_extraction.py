"""tessellum.composer.claim_extraction — note body → checkable Claims.

The calibrated certificate (``semantic_certificate.certify``) scores a
``list[Claim]``; something must turn a WRITTEN note (its markdown body + the
provenance rows that back it) into those claims. This module is that pure,
deterministic extractor — the C2 piece of the "make the certificate runnable"
increment.

Design (honest + fail-closed):

- **Claims are prose sentences.** The extractor keeps only body prose: it
  drops the YAML frontmatter, ATX/`##` headers, fenced code blocks, table rows,
  list markers, and lines that are purely a link/URL — none of those are
  checkable factual assertions. What remains is split into sentences on
  ``.!?`` boundaries; sentences below a small content-token floor (e.g. a bare
  "Yes.") are dropped as non-checkable.
- **A sentence is grounded if ANY cited source supports it.** A note may carry
  several provenance rows; the correct semantics is disjunctive over sources.
  So each claim's ``source_ref`` is a STABLE JOIN of all the note's distinct
  provenance refs (:data:`MULTI_SOURCE_SEP`-separated, sorted); the injected
  span resolver (C3) splits on that separator and concatenates the spans, so
  :func:`~tessellum.composer.lexical_scorer.claim_support_score` measures
  support against the union of cited sources — not one arbitrary source.
- **No provenance → no claims.** A note with no cited sources yields an empty
  claim list, which ``certify`` treats fail-closed (empty → abstain): an
  unsourced note is never auto-grounded.

Pure: no clock, no randomness, no I/O.
"""

from __future__ import annotations

import re

from tessellum.composer.knowledge_plan import ClaimProvenance
from tessellum.composer.lexical_scorer import _content_tokens
from tessellum.composer.semantic_certificate import Claim, FailureClass

# Separator joining a note's distinct source refs into one Claim.source_ref.
# The C3 span resolver splits on this to resolve + concatenate the cited spans.
# Chosen to not occur in a normal ref (path/URL/span-id).
MULTI_SOURCE_SEP = "\x1f"  # ASCII unit separator

# A claim sentence must carry at least this many content tokens to be checkable
# (a bare "Yes." / "See above." is not a groundable factual assertion).
_MIN_CLAIM_CONTENT_TOKENS = 3

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_FENCE_RE = re.compile(r"^\s*(?:```|~~~)")  # both backtick AND tilde fences
_INDENTED_CODE_RE = re.compile(r"^(?: {4,}|\t)")  # 4-space / tab indented code
_HEADER_RE = re.compile(r"^\s{0,3}#{1,6}\s")
_TABLE_ROW_RE = re.compile(r"^\s*\|")
_LIST_MARKER_RE = re.compile(r"^\s*([-*+]|\d+\.)\s+")
# A line that is ONLY a markdown link / bare URL (no surrounding prose).
_LINK_ONLY_RE = re.compile(
    r"^\s*(?:[-*+]\s+)?(?:\[[^\]]*\]\([^)]*\)|<?https?://\S+>?|\[\[[^\]]*\]\])\s*$"
)


def _strip_frontmatter(body: str) -> str:
    """Drop a leading ``---`` … ``---`` YAML frontmatter block, if present."""
    if body.startswith("---"):
        end = body.find("\n---", 3)
        if end != -1:
            nl = body.find("\n", end + 1)
            return body[nl + 1:] if nl != -1 else ""
    return body


def _prose_lines(body: str) -> list[str]:
    """Body lines that are checkable prose — frontmatter / code fences / headers
    / tables / list markers / link-only lines removed. List CONTENT (the text
    after a ``- `` marker) is kept; a bare link bullet is dropped."""
    out: list[str] = []
    in_fence = False
    for raw in _strip_frontmatter(body).splitlines():
        if _FENCE_RE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not raw.strip():
            continue
        # Indented code block (4+ spaces / tab) — but NOT a list-item continuation
        # (a list marker line is handled below); a bare indented code line is dropped.
        if _INDENTED_CODE_RE.match(raw) and not _LIST_MARKER_RE.match(raw.strip()):
            continue
        if _HEADER_RE.match(raw) or _TABLE_ROW_RE.match(raw):
            continue
        if _LINK_ONLY_RE.match(raw):
            continue
        # keep list-item CONTENT but drop the marker so it reads as prose.
        line = _LIST_MARKER_RE.sub("", raw).strip()
        if line:
            out.append(line)
    return out


def split_sentences(body: str) -> list[str]:
    """Split a note body into candidate claim sentences (pure, deterministic).

    Prose lines only (see :func:`_prose_lines`), joined then split on sentence
    punctuation. A below-floor fragment is NOT silently dropped (that would
    fail-OPEN — a fabricated clause carved off by an abbreviation/decimal split,
    e.g. "1.5w" or "e.g.", would escape scoring); instead it is MERGED back into
    the previous fragment so its tokens stay inside a scored claim. A leading
    below-floor fragment merges into the next. Only a fragment whose ENTIRE
    content is below the floor with no neighbour to attach to is dropped."""
    prose = " ".join(_prose_lines(body))
    if not prose.strip():
        return []
    raw = [s.strip() for s in _SENTENCE_SPLIT_RE.split(prose) if s.strip()]
    merged: list[str] = []
    for frag in raw:
        if len(_content_tokens(frag)) >= _MIN_CLAIM_CONTENT_TOKENS or not merged:
            merged.append(frag)
        else:
            # below-floor + a previous fragment exists → re-attach (don't drop).
            merged[-1] = f"{merged[-1]} {frag}"
    # a lone leading below-floor fragment with no successor to absorb it: fold
    # forward if a next fragment exists, else keep it (it may still carry a
    # checkable token; the scorer treats an all-stopword claim as 0.0 anyway).
    if len(merged) >= 2 and len(_content_tokens(merged[0])) < _MIN_CLAIM_CONTENT_TOKENS:
        merged[1] = f"{merged[0]} {merged[1]}"
        merged = merged[1:]
    return [s for s in merged if _content_tokens(s)]


def _joined_source_ref(provenance: tuple[ClaimProvenance, ...]) -> str:
    """The stable, sorted, distinct join of a note's provenance source refs
    (the C3 resolver splits this on :data:`MULTI_SOURCE_SEP`).

    Fails loud if a source_ref itself contains the separator byte (0x1f) — that
    would make the downstream split ambiguous. 0x1f is a control char that never
    occurs in a real path/URL/span-id, so this only fires on corrupt input; a
    fail-closed error beats a silently mis-split source ref."""
    refs = sorted({p.source_ref for p in provenance})
    for r in refs:
        if MULTI_SOURCE_SEP in r:
            raise ValueError(
                f"source_ref {r!r} contains the reserved MULTI_SOURCE_SEP byte "
                "(0x1f) — cannot join/split unambiguously"
            )
    return MULTI_SOURCE_SEP.join(refs)


def extract_claims(
    body: str,
    provenance: tuple[ClaimProvenance, ...],
    *,
    failure_class: FailureClass = "grounding",
    note_id: str = "note",
) -> list[Claim]:
    """Extract checkable :class:`Claim` s from a written note (C2) — pure.

    Each prose sentence becomes one grounding-class claim cited against the
    UNION of the note's provenance refs (:func:`_joined_source_ref`), so it is
    scored as grounded iff any cited source supports it. A note with no
    provenance yields ``[]`` (``certify`` → fail-closed abstain). ``claim_id`` s
    are stable + deterministic (``{note_id}:c{index}``).

    ``failure_class`` defaults to ``"grounding"`` (the class this lexical proxy
    checks); coverage/duplicate/edge-relevance claims are produced by their own
    extractors when those scorers exist."""
    if not provenance:
        return []
    src = _joined_source_ref(provenance)
    return [
        Claim(claim_id=f"{note_id}:c{i}", text=sentence, source_ref=src,
              failure_class=failure_class)
        for i, sentence in enumerate(split_sentences(body))
    ]


__all__ = [
    "MULTI_SOURCE_SEP",
    "split_sentences",
    "extract_claims",
]
