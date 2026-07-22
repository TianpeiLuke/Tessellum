"""Planner economics — selective depth + a ``$0`` change-detection pre-gate.

Composer v4, Phase 4 (planner half). Two pure, deterministic economies
that concentrate the expensive passes where they pay:

1. **Selective planning depth.** Not every leaf deserves the full plan →
   augment → review → compile treatment. A cheap complexity/novelty
   classifier (:func:`classify_planning_depth`) routes a trivial/templated
   leaf to a lightweight ``fast`` path (skip the deep passes) and a
   novel/multi-note leaf to the ``full`` path (all passes + a stricter
   gate). The classifier is a string/size heuristic — no LLM, no I/O.

2. **``$0`` change-detection pre-gate.** Re-digesting an unchanged source
   is wasted spend. :func:`content_fingerprint` hashes a source's bytes
   (or mtime+size when given a path), and :func:`should_skip_unchanged`
   compares it against the last-recorded fingerprint so an unchanged
   source is skipped *before* the expensive capture call — a
   generalization of content-addressed resume.

Both are program logic (IDENT-3); they inform the scheduler/driver, they
don't themselves dispatch anything.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Mapping

PlanningDepth = Literal["fast", "full"]
"""Routing decision for a leaf:

- ``fast`` — trivial/templated; skip the deep enrich/route passes.
- ``full`` — novel/multi-note; run the full P1–P4 + a stricter gate.
"""


@dataclass(frozen=True)
class LeafComplexity:
    """The signals the depth classifier reads off a leaf (all cheap).

    Attributes:
        source_chars: Size of the source payload in characters. Large
            sources tend to need the full treatment.
        note_count: How many notes this leaf is expected to produce
            (``> 1`` ⇒ multi-note ⇒ full).
        is_templated: ``True`` when the leaf follows a known template
            (e.g. a launch-announcement / ticket digest) — a strong
            fast-path signal.
        novelty: Optional 0..1 novelty score (fraction of unseen terms /
            distance from prior notes). ``None`` when not computed.
    """

    source_chars: int = 0
    note_count: int = 1
    is_templated: bool = False
    novelty: float | None = None


# Thresholds — deliberately conservative: default to ``full`` when in
# doubt (a mis-routed novel leaf is far costlier than an over-planned
# trivial one). Tunable without touching the logic.
FAST_PATH_MAX_CHARS: int = 4000
"""A source above this size is never fast-pathed (too much to summarize)."""

NOVELTY_FULL_THRESHOLD: float = 0.3
"""Novelty at or above this forces the full path even for a small source."""


def classify_planning_depth(complexity: LeafComplexity) -> PlanningDepth:
    """Route a leaf to ``fast`` or ``full`` — pure, conservative.

    A leaf is fast-pathed **only** when every cheap signal says trivial:
    single-note, small source, and either explicitly templated or
    low-novelty. Any signal of size/multiplicity/novelty forces ``full``.
    Defaults to ``full`` when signals are missing (fail-safe: never skip
    depth on an unknown).

    Rules (all must hold for ``fast``):

    - ``note_count <= 1`` (multi-note ⇒ full), and
    - ``source_chars <= FAST_PATH_MAX_CHARS`` (big source ⇒ full), and
    - ``is_templated`` **or** a known novelty below
      :data:`NOVELTY_FULL_THRESHOLD` (unknown novelty on a non-templated
      leaf ⇒ full).
    """
    if complexity.note_count > 1:
        return "full"
    if complexity.source_chars > FAST_PATH_MAX_CHARS:
        return "full"
    if complexity.novelty is not None and complexity.novelty >= NOVELTY_FULL_THRESHOLD:
        return "full"
    if complexity.is_templated:
        return "fast"
    if complexity.novelty is not None and complexity.novelty < NOVELTY_FULL_THRESHOLD:
        return "fast"
    # Non-templated, unknown novelty → be safe, plan fully.
    return "full"


def content_fingerprint(source: str | bytes | Path) -> str:
    """A stable content fingerprint for the ``$0`` change-detection gate.

    - ``str`` / ``bytes`` → a SHA-256 of the content (exact-content
      addressing; two identical payloads share a fingerprint).
    - ``Path`` → SHA-256 of the file bytes when readable; falls back to
      ``"mtime:<mtime>:size:<size>"`` if the file can't be read (cheap
      stat-based addressing). A missing path → ``"absent"``.

    Deterministic and side-effect-free.
    """
    if isinstance(source, Path):
        p = source
        if not p.exists():
            return "absent"
        try:
            return _sha256(p.read_bytes())
        except OSError:
            st = p.stat()
            return f"mtime:{st.st_mtime}:size:{st.st_size}"
    if isinstance(source, str):
        return _sha256(source.encode("utf-8"))
    return _sha256(source)


def should_skip_unchanged(
    leaf_id: str,
    source: str | bytes | Path,
    prior_fingerprints: Mapping[str, str],
) -> tuple[bool, str]:
    """Decide whether a leaf can be skipped because its source is unchanged.

    Compares the source's current :func:`content_fingerprint` against the
    fingerprint last recorded for ``leaf_id``. Skips (returns ``True``)
    only on an exact match — a changed, new, or absent source is never
    skipped (fail-open toward doing the work).

    Args:
        leaf_id: The leaf's stable id.
        source: The source payload / path to fingerprint.
        prior_fingerprints: ``{leaf_id: fingerprint}`` from a prior run
            (e.g. persisted in the manifest).

    Returns:
        ``(skip, fingerprint)`` — ``skip`` is ``True`` iff the current
        fingerprint equals the recorded one; ``fingerprint`` is the
        freshly-computed value (record it for next time).
    """
    fp = content_fingerprint(source)
    prior = prior_fingerprints.get(leaf_id)
    return (prior is not None and prior == fp), fp


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


__all__ = [
    "PlanningDepth",
    "LeafComplexity",
    "FAST_PATH_MAX_CHARS",
    "NOVELTY_FULL_THRESHOLD",
    "classify_planning_depth",
    "content_fingerprint",
    "should_skip_unchanged",
]
