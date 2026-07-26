"""tessellum.composer.lexical_scorer — a deterministic reference ClaimScorer.

The calibrated semantic certificate (``semantic_certificate.py``, P7 / DKS P4)
runs its conformal calibration + fail-closed abstain over a PLUGGABLE
:data:`~tessellum.composer.semantic_certificate.ClaimScorer` — the real
NLI/SummaC/FEVER model is an injected dependency it never bundles. But with no
scorer at all the certify→verdict→gate loop cannot run end-to-end, so nothing
can be exercised, wired, or A7.5-gated.

This module ships the ONE scorer a pure code phase can honestly deliver: a
deterministic, model-free **lexical-entailment proxy** — the exact analog of the
deterministic temporal-holdout scorer DKS ships in ``dks/validation.py``. It
scores how much of a claim's content is lexically supported by its cited source
span (directional token containment over content words), which cheaply separates
"the claim's words are present in the span" from "the claim asserts words the
span never mentions" (the crudest fabrication signal). It is a BASELINE, not the
real entailment model — and its ceiling is sharp and MUST be understood:

- **It is bag-of-content-words and does NOT understand negation, reordering, or
  paraphrase.** ``not`` / ``no`` / ``does`` are stopwords, so "the model does
  NOT support X" and "the model does support X" have IDENTICAL content-token
  bags and both score 1.0; "A causes B" and "B causes A" both score 1.0. A
  negation- or reordering-fabrication therefore scores HIGH and is emitted as
  ``grounded`` — this proxy CANNOT catch it. That is exactly why it is a
  runnable baseline for wiring + calibration, NOT a safety-bearing verifier: the
  A7.5 gate is what protects unattended promotion (it will not return GO unless a
  scorer's held-out false-accept rate — which INCLUDES such fabrications when the
  corpus contains them — is ≤ α), and until a REAL entailment model passes that
  gate on a REAL corpus, promotion stays human-supervised. Do not read a
  ``grounded`` verdict from THIS scorer as semantic entailment.
- it ABSTAINS (fail-closed) only on the coarsest signal it CAN see — the span
  text being unavailable / empty (an unreadable source) or the claim having no
  content tokens — NOT on paraphrase/negation, which it silently cannot judge;
- it makes the loop runnable and the A7.5 gate measurable NOW, and drops out the
  moment a real model is injected into the same seam.

Pure: no clock, no randomness, no I/O. The span text is resolved through an
injected ``span_text_of`` callable (composer stays vault-I/O-free).
"""

from __future__ import annotations

import re
from typing import Callable

from tessellum.composer.semantic_certificate import Claim, ClaimScore

# Content-word tokenization: lowercase alphanumeric runs, minus a small closed
# stoplist. Deliberately tiny + frozen (determinism > coverage) — the real
# model replaces this whole scorer, so the stoplist need not be exhaustive.
_TOKEN_RE = re.compile(r"[a-z0-9]+")
_STOPWORDS: frozenset[str] = frozenset(
    """a an the of to in on at for and or but is are was were be been being
    this that these those it its as by with from into over under then than
    so such not no nor can will would should could may might must do does did
    have has had he she they we you i""".split()
)


def _content_tokens(text: str) -> list[str]:
    """Lowercased content-word tokens (stopwords + pure-punctuation dropped).
    Deterministic; preserves multiplicity for a stable overlap denominator."""
    return [t for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS]


def claim_support_score(claim_text: str, span_text: str) -> float:
    """Directional token-containment of ``claim_text`` in ``span_text`` in
    ``[0, 1]`` — the fraction of the claim's DISTINCT content tokens present in
    the span. Pure.

    Directional on purpose: entailment cares whether the SOURCE supports the
    CLAIM (every content word the claim asserts should be in the span), not the
    reverse — a long span that happens to contain the claim's words still
    supports it. A claim with no content tokens (all stopwords/empty) scores
    0.0 (nothing checkable → the certificate treats it fail-closed)."""
    claim_tokens = set(_content_tokens(claim_text))
    if not claim_tokens:
        return 0.0
    span_tokens = set(_content_tokens(span_text))
    supported = claim_tokens & span_tokens
    return len(supported) / len(claim_tokens)


def make_lexical_scorer(
    span_text_of: Callable[[str], str | None],
) -> Callable[[list[Claim]], list[ClaimScore]]:
    """Build a reference :data:`ClaimScorer` from an injected span resolver.

    ``span_text_of(source_ref) -> str | None`` returns the text of the cited
    span (``None`` / empty ⇒ unresolvable). For each claim: resolve its span,
    and if the span is unavailable ABSTAIN (fail-closed — an unreadable source
    is never auto-grounded), else score by :func:`claim_support_score`.

    The returned callable matches the
    :data:`~tessellum.composer.semantic_certificate.ClaimScorer` seam, so it
    drops straight into ``certify(...)`` / the DKS router in place of the real
    model. Pure given a pure ``span_text_of``."""

    def _scorer(claims: list[Claim]) -> list[ClaimScore]:
        out: list[ClaimScore] = []
        for c in claims:
            span = span_text_of(c.source_ref)
            if not span:
                out.append(ClaimScore(c.claim_id, 0.0, abstained=True))
                continue
            out.append(ClaimScore(c.claim_id, claim_support_score(c.text, span)))
        return out

    return _scorer


__all__ = [
    "claim_support_score",
    "make_lexical_scorer",
]
