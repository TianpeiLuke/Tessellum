"""Per-note related-notes enrichment — the retrieval home for graph edges.

The composer's write wave dispatches one sub-agent per planned note. For the
knowledge graph to grow, each written note must carry, in its ``## References``
section, relevance-selected markdown links to EXISTING vault notes — the
indexer turns those links into ``note_links`` edges (``build.py``).

FZ 20k9d2 established that the ``ContextAssembler`` seam is the WRONG home for
this: it is a single instance shared concurrently across all note-writer
threads, it only sees the rendered (boilerplate-headed) prompt, and it does not
know the note's target path — so it can compute neither a good per-note query
nor a resolvable relative link. The RIGHT home is HERE: a pure, per-note
enrichment keyed on the planned :class:`~tessellum.composer.knowledge_plan.NoteIntent`'s
OWN ``thesis`` + ``coverage`` (its most discriminating signal), computing links
relative to its ``target_path``, run once per leaf BEFORE the wave.

Design invariants:

- **Per-note relevance.** The query is built from the note's own thesis +
  coverage tokens, sanitized to a safe FTS5 bag — never a shared job-level query.
- **Router-dispatched (wires the heuristic router).** Primary retrieval goes
  through :func:`tessellum.retrieval.router.route`, giving that previously
  orphaned decision-tree its first live caller; the seed set is then expanded
  over the link graph via :func:`best_first_bfs` for structural neighbors.
- **Resolvable links → real edges.** Each hit's vault-relative ``note_id`` is
  rebased to a path RELATIVE to the new note's ``target_path`` directory via
  ``os.path.relpath``, so the emitted ``[title](rel/path.md)`` yields a direct
  ``link_type="markdown"`` edge — never leaning on the indexer's fragile
  duplicate-name fallback.
- **Self- and dependency-exclusion.** The note never links itself; planned
  siblings it already ``depends_on`` are also excluded (that edge is expressed
  structurally, not as a "related" reference).
- **Pure + fail-soft + thread-safe.** No shared mutable state; a missing index,
  empty query, or any retrieval error yields an EMPTY result (the note is
  written without a References block), never a crash. Safe to call concurrently.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from tessellum.composer.context_assembler import _fts5_safe_query

# Retrieval sizing defaults for per-note enrichment.
DEFAULT_SEEDS: int = 10  # router top-K used as the relevance core + BFS seeds
DEFAULT_NEIGHBORS: int = 8  # best-first BFS neighbors expanded per seed
# Cap on links written into ## References. Sized above the digestion skill's
# per-note cross-reference floor (≥8 relevant term-dictionary notes +
# non-entry/service/etc. notes — plan/augment skills) so the suggested block can
# actually MEET that floor rather than undershoot it; the writer trims to the
# genuinely relevant subset.
DEFAULT_MAX_RELATED: int = 14
# Minimum term_dictionary (term_*) notes the enrichment tries to surface, so the
# References block can satisfy the skill's ≥8-term floor even when free
# relevance ranking is dominated by non-term notes. Best-effort: filled only if
# retrieval found that many term notes.
DEFAULT_MIN_TERM_NOTES: int = 8

# The section header the writer's ## References block is rendered under. Matches
# the vault note templates (template_*.md) so the enrichment slots into the
# canonical note shape rather than inventing a new header.
REFERENCES_HEADER = "## References"


@dataclass(frozen=True)
class RelatedNote:
    """One relevance-selected related note, ready to render as a graph edge.

    Attributes:
        note_id: Vault-relative path of the related note (``notes.note_id``).
        note_name: Filename stem (used as the link title default).
        rel_path: Path to ``note_id`` RELATIVE to the new note's target
            directory — the exact target the writer puts in ``[title](rel_path)``
            so the indexer resolves it to a ``markdown`` edge.
        score: Relevance score (router/BFS score; higher = more relevant).
        source: Which surface surfaced it — ``"seed"`` (router primary) or
            ``"neighbor"`` (BFS expansion). Diagnostic only.
    """

    note_id: str
    note_name: str
    rel_path: str
    score: float
    source: str


@dataclass(frozen=True)
class RelatedNotesResult:
    """Enrichment output for one note. Empty (``related == ()``) on any
    fail-soft degradation, with the reason captured in ``warning``."""

    related: tuple[RelatedNote, ...] = ()
    references_markdown: str = ""
    warning: str | None = None

    @property
    def is_empty(self) -> bool:
        return not self.related


def _query_for_note(thesis: str, coverage: tuple[str, ...] | list[str] | None) -> str:
    """Build the per-note FTS5-safe retrieval query from the note's OWN signal.

    Thesis first (the single human-readable claim — the highest-signal
    discriminator), then coverage/topic tokens. Sanitized to an ``OR``-joined
    alphanumeric bag so it can never be an FTS5 syntax error and so a term that
    appears in no single note still contributes a hit (implicit-AND would
    zero-out). Returns ``""`` when nothing usable remains."""
    parts: list[str] = []
    if isinstance(thesis, str) and thesis.strip():
        parts.append(thesis)
    if coverage:
        parts.append(" ".join(str(c) for c in coverage))
    return _fts5_safe_query(" ".join(parts))


def _dense_query_for_note(
    thesis: str, coverage: tuple[str, ...] | list[str] | None
) -> str:
    """The RAW natural-language query for the dense (embedding) arm.

    Unlike :func:`_query_for_note`, this is NOT FTS5-sanitized — the embedding
    model ranks best on the original prose (thesis sentence + coverage terms),
    whereas an ``OR``-joined keyword bag embeds poorly. Only whitespace is
    normalized. Returns ``""`` when nothing usable remains."""
    parts: list[str] = []
    if isinstance(thesis, str) and thesis.strip():
        parts.append(thesis.strip())
    if coverage:
        cov = " ".join(str(c) for c in coverage).strip()
        if cov:
            parts.append(cov)
    return " ".join(parts).strip()


def _rebase(note_id: str, target_dir: str) -> str:
    """Path to ``note_id`` relative to the new note's target directory.

    Both are vault-relative POSIX paths; ``os.path.relpath`` computes the
    ``../…`` hops the writer needs so the indexer (which resolves link targets
    relative to the AUTHORING note's own dir) records a direct edge. Falls back
    to the bare ``note_id`` if relpath fails (defensive; never raises)."""
    try:
        rel = os.path.relpath(note_id, target_dir or ".")
    except (ValueError, TypeError):
        return note_id
    # Normalize to POSIX separators — vault paths are POSIX, and a Windows
    # backslash would break the markdown link on any platform.
    return rel.replace(os.sep, "/")


def enrich_related_notes(
    *,
    thesis: str,
    target_path: str,
    db_path: Path | str | None,
    coverage: tuple[str, ...] | list[str] | None = (),
    exclude_ids: tuple[str, ...] | list[str] | None = (),
    seeds: int = DEFAULT_SEEDS,
    neighbors: int = DEFAULT_NEIGHBORS,
    max_related: int = DEFAULT_MAX_RELATED,
    min_term_notes: int = DEFAULT_MIN_TERM_NOTES,
) -> RelatedNotesResult:
    """Retrieve relevance-ranked related notes for ONE planned note. Pure,
    fail-soft, thread-safe.

    Args:
        thesis: The note's single human-readable claim (primary query signal).
        target_path: The note's vault-relative ``.md`` target — its directory
            anchors the computed relative links, and the note excludes itself.
        db_path: The live index DB. ``None`` / missing → empty result (the note
            is written without a References block).
        coverage: Optional topic/section tokens appended to the query.
        exclude_ids: Additional vault-relative note_ids to exclude (e.g. the
            note's ``depends_on`` — that relationship is structural, not a
            "related" reference). ``target_path`` is always excluded.
        seeds: Router primary top-K (also the BFS seed set).
        neighbors: Best-first BFS neighbors expanded per seed.
        max_related: Hard cap on the number of links returned/rendered.

    Returns:
        A :class:`RelatedNotesResult`. ``related`` is relevance-ordered (router
        seeds first, then BFS neighbors), deduped, self/dep-excluded, capped,
        and each carries a ``rel_path`` resolvable from ``target_path``.
    """
    if db_path is None:
        return RelatedNotesResult(warning="no index configured; no related notes")
    db = Path(db_path)
    if not db.exists():
        return RelatedNotesResult(
            warning=f"index {db} does not exist; no related notes"
        )

    query = _query_for_note(thesis, coverage)
    if not query:
        return RelatedNotesResult(
            warning="note thesis/coverage yielded an empty query; no related notes"
        )
    # The dense (embedding) arm ranks natural-language prose far better than the
    # FTS5 ``OR``-bag (the literal ``OR`` tokens + bag structure embed poorly).
    # Give it the RAW thesis + coverage; BM25 keeps the FTS5-safe bag (``query``).
    dense_query = _dense_query_for_note(thesis, coverage) or None

    # Lazy import: retrieval pulls sqlite_vec / networkx — keep them off the
    # import path of composer callers that never enrich.
    from tessellum.retrieval.graph import best_first_bfs
    from tessellum.retrieval.router import route

    # Exclusions: never link self; drop caller-supplied structural deps.
    excluded: set[str] = {target_path}
    if exclude_ids:
        excluded.update(exclude_ids)

    target_dir = str(Path(target_path).parent)

    # Primary retrieval THROUGH the router (wires the previously-orphaned
    # decision tree). route() classifies the query and dispatches to the right
    # surface; for a thesis-shaped multi-word query it lands on hybrid, where the
    # BM25 arm sees the FTS5 bag and the dense arm sees the raw prose.
    try:
        _decision, hits = route(db, query, dense_query=dense_query, k=max(1, seeds))
    except Exception as e:  # noqa: BLE001 — retrieval failure degrades, not kills
        return RelatedNotesResult(
            warning=f"router retrieval failed ({type(e).__name__}); no related notes"
        )

    ordered: list[RelatedNote] = []
    seen: set[str] = set(excluded)

    def _add(nid: str, name: str, score: float, source: str) -> None:
        if nid in seen:
            return
        seen.add(nid)
        ordered.append(
            RelatedNote(
                note_id=nid,
                note_name=name,
                rel_path=_rebase(nid, target_dir),
                score=float(score),
                source=source,
            )
        )

    # score/note_id read defensively (getattr) even though the only reachable
    # surfaces (bm25/hybrid/bfs) all carry them — a future router change that
    # dispatched to a score-less MetadataHit must degrade, not raise and kill
    # the whole wave. note_id is required; a hit without one is skipped.
    for h in hits:
        nid = getattr(h, "note_id", None)
        if not nid:
            continue
        _add(
            nid,
            getattr(h, "note_name", None) or Path(nid).stem,
            getattr(h, "score", 0.0),
            "seed",
        )

    # Structural expansion: best-first BFS from each seed over the link graph,
    # so the writer also sees graph-adjacent notes, not only lexical/semantic
    # top hits. A bad seed never sinks the whole enrichment.
    if neighbors:
        seed_ids = [r.note_id for r in ordered]
        for sid in seed_ids:
            try:
                neigh = best_first_bfs(db, sid, k=neighbors)
            except Exception:  # noqa: BLE001 — one bad seed is not fatal
                continue
            for g in neigh:
                gid = getattr(g, "note_id", None)
                if not gid:
                    continue
                _add(
                    gid,
                    getattr(g, "note_name", None) or Path(gid).stem,
                    getattr(g, "score", 0.0),
                    "neighbor",
                )

    if not ordered:
        return RelatedNotesResult(
            warning="retrieval returned no related notes for this note"
        )

    capped = _cap_with_term_quota(ordered, max_related, min_term_notes)
    return RelatedNotesResult(
        related=capped,
        references_markdown=render_references(capped),
        warning=None,
    )


def _is_term_note(note_id: str) -> bool:
    """True iff ``note_id`` is a term_dictionary note (``…/term_*.md``)."""
    return Path(note_id).name.startswith("term_")


def _cap_with_term_quota(
    ordered: list[RelatedNote], max_related: int, min_term_notes: int
) -> tuple[RelatedNote, ...]:
    """Cap to ``max_related`` while reserving room for up to ``min_term_notes``
    term_dictionary notes.

    The digestion skills mandate a per-note floor of ≥8 relevant term notes, but
    free relevance ranking can be dominated by non-term notes and push the term
    notes past a flat top-N cut. So take the top relevance-ordered notes, then —
    if fewer than ``min_term_notes`` term notes made the cut — swap in the
    next-best term notes from the tail (displacing the lowest-ranked non-term
    notes), preserving overall relevance order. Best-effort: never invents term
    notes retrieval did not find, never exceeds ``max_related``."""
    cap = max(1, max_related)
    if len(ordered) <= cap:
        return tuple(ordered)
    head = ordered[:cap]
    if min_term_notes <= 0:
        return tuple(head)
    terms_in_head = sum(1 for r in head if _is_term_note(r.note_id))
    needed = min(min_term_notes, DEFAULT_MIN_TERM_NOTES) - terms_in_head
    if needed <= 0:
        return tuple(head)
    # Term notes ranked below the cut, best-first.
    tail_terms = [r for r in ordered[cap:] if _is_term_note(r.note_id)]
    if not tail_terms:
        return tuple(head)
    # Displace the lowest-ranked NON-term notes in the head with the best tail
    # terms, keeping the selected set and then re-sorting to relevance order.
    keep = list(head)
    non_term_positions = [
        i for i, r in enumerate(keep) if not _is_term_note(r.note_id)
    ]
    swaps = min(needed, len(tail_terms), len(non_term_positions))
    if swaps <= 0:
        return tuple(head)
    # Replace from the END of the head's non-term notes (lowest relevance).
    for j in range(swaps):
        keep[non_term_positions[-1 - j]] = tail_terms[j]
    keep.sort(key=lambda r: -r.score)
    return tuple(keep[:cap])


# Note-name slug prefixes stripped when de-slugging a link title. These are the
# vault's building-block / category filename conventions (term_x, model_y, …);
# the prefix is noise in a human-readable reference title.
_SLUG_TITLE_PREFIXES: tuple[str, ...] = (
    "term_", "model_", "entry_", "thought_", "argument_", "counter_",
    "hypothesis_", "analysis_", "proposal_", "coe_", "note_", "table_",
    "etl_", "data_source_", "intent_", "area_", "dashboard_", "repo_",
    "snippet_", "builderhub_", "acronym_glossary_", "tracker_", "shepherd_",
)


def _deslug_title(note_name: str) -> str:
    """Best-effort human-readable link title from a filename slug.

    The index exposes no note title/H1 (the ``notes`` table has no title
    column — ``note_name`` is ``md_file.stem``), so a rendered reference would
    otherwise read ``[term_zettelkasten](…)``. Strip a known building-block
    prefix and turn underscores into spaces so it reads ``[zettelkasten](…)``.
    Purely cosmetic for the LINK TEXT; the link TARGET (rel_path) — the part the
    indexer resolves into an edge — is untouched. Falls back to the raw stem if
    stripping would empty it."""
    if not note_name:
        return note_name
    body = note_name
    for prefix in _SLUG_TITLE_PREFIXES:
        if body.startswith(prefix) and len(body) > len(prefix):
            body = body[len(prefix):]
            break
    title = body.replace("_", " ").strip()
    return title or note_name


def render_references(related: tuple[RelatedNote, ...] | list[RelatedNote]) -> str:
    """Render related notes as a ``## References`` markdown block.

    One bullet per note as a relative markdown link — the exact
    ``[title](rel/path.md)`` shape the indexer extracts as a ``note_links``
    edge (``build.py`` ``_MARKDOWN_LINK_RE``). The link TEXT is a de-slugged
    human-readable title (:func:`_deslug_title`); the link TARGET is the
    resolvable ``rel_path`` (never altered). Returns ``""`` for an empty list
    (no header emitted). This is a suggested-and-resolved block the writer folds
    into the note; the writer may drop a truly irrelevant suggestion — relevance
    is a floor, not a mandate to link noise."""
    if not related:
        return ""
    lines = [
        f"- [{_deslug_title(r.note_name)}]({r.rel_path})"
        for r in related
    ]
    return f"{REFERENCES_HEADER}\n" + "\n".join(lines) + "\n"
