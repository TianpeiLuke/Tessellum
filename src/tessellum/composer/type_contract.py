"""Per-note NOTE-TYPE contract resolution — the type home for the writer.

The composer's write wave dispatches one sub-agent per planned note. Each note
belongs to a note TYPE (a capture ``flavor`` — ``concept``, ``procedure``,
``sop``, ``code_snippet``, …) that carries a section contract: the ``## H2``
sections the finished note should contain. FZ 20k9d1b1a1a established WHY this
is keyed on the flavor and NOT on ``building_block``:

- ``building_block`` and ``note_second_category`` are ORTHOGONAL over the vault
  (many-to-many both ways): one BB spans many second_categories (``procedure``
  → code_snippet / sop / how_to / tutorial / skills / aws_docs) and one
  second_category spans many BBs (``aws_docs`` = 6 BBs). So the note's
  file-shape / template is a function of the flavor, not the building block.
- ``building_block`` is a SEPARATE per-note field the template CARRIES — a
  per-flavor default the per-note :class:`~tessellum.composer.knowledge_plan.NoteIntent.building_block`
  can override. Resolution therefore keys on ``target_path`` (which encodes the
  flavor via its destination + filename prefix), never on ``building_block`` —
  or a per-note BB override would fight the resolver.

This module is the pure, fail-soft twin of :mod:`tessellum.composer.related_notes`
(distinct from :mod:`tessellum.composer.contracts`, which is the producer/consumer
WIRE contract). It reverse-resolves a leaf's ``target_path`` to its flavor via
``capture.REGISTRY`` and renders a compact per-type contract block the writer
folds in next to the ``## References`` block.

Design invariants (mirroring the related-notes precedent):

- **Flavor-keyed, target_path-driven.** ``resolve_flavor`` matches the longest
  ``(destination, filename_prefix)`` prefix so ``thought_observation_x.md`` →
  ``empirical_observation`` (not the bare ``thought_`` → ``argument``). Flavor is
  FINER than second_category (six flavors share ``second_category=analysis`` but
  have distinct ``required_sections``).
- **Section source per flavor.** Primary flavors get ``BB_SPECS[bb].required_sections``
  (the epistemic contract). The four ``SECTION_DIVERGENT_FLAVORS`` (code_snippet,
  skill, experiment, code_repo) legitimately do NOT follow their BB's section
  triple, so their sections come from the flavor's OWN template H2 headers —
  never the wrong ``BB_SPECS[procedure]`` Setup/Steps/Validation.
- **Pure + fail-soft + thread-safe.** No mutable shared state; the reverse index
  and template parse are ``lru_cache`` read-only after first build. An
  unresolvable path, an unreadable template, or any error yields ``None`` / an
  empty section list — never a raise, never a crash of the wave-parallel run.
- **Advisory only.** This DELIVERS a per-FLAVOR section list to the writer up
  front; it adds no hard gate (``required_sections`` is intentionally advisory
  today). NOTE: for a PRIMARY flavor the delivered list is exactly
  ``BB_SPECS[bb].required_sections``, so a conforming note also satisfies the
  ``TESS-010`` INFO advisory (which is BB-keyed). For the four
  ``SECTION_DIVERGENT_FLAVORS`` (and any note whose per-note ``building_block``
  differs from the flavor's default) the delivered flavor sections DIFFER from
  the note's BB sections, so a note that follows this contract may STILL raise
  TESS-010 INFOs — that divergence is expected and acceptable precisely because
  TESS-010 is advisory, not a gate. A future flavor-keyed ``TESS-011`` would
  reconcile the two, and is deliberately deferred.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import PurePosixPath

from tessellum import capture
from tessellum.format.building_blocks import BB_SPECS, BuildingBlock


@dataclass(frozen=True)
class NoteTypeContract:
    """The resolved note-type contract for one planned note.

    Attributes:
        flavor: The resolved ``capture.REGISTRY`` flavor (e.g. ``"concept"``).
        second_category: The flavor's ``second_category`` (``tags[1]``); coarser
            than ``flavor`` (many flavors share one, e.g. ``analysis``).
        building_block: The flavor's DEFAULT ``bb_type`` (diagnostic only — the
            per-note ``NoteIntent.building_block`` may legitimately differ; this
            is not enforced here).
        required_sections: The ``## H2`` sections the finished note should carry.
            Sourced from ``BB_SPECS`` for primary flavors, or the flavor's own
            template H2 headers for a ``SECTION_DIVERGENT`` flavor. ``()`` when a
            divergent flavor's template is unreadable (fail-soft).
        section_source: ``"BB_SPECS"`` | ``"template"`` | ``"divergent-unreadable"``.
        contract_md: The compact rendered block the writer folds in.
    """

    flavor: str
    second_category: str
    building_block: str
    required_sections: tuple[str, ...]
    section_source: str
    contract_md: str


# Domain-specific filename-prefix ALIASES for the ``capture()`` ``filename_prefix=``
# override convention: a note may be written with a subject prefix other than its
# flavor's default while keeping the flavor's shape. These are the documented
# vault conventions (``skill_tessellum_append_to_trail.md`` / ``skill_tessellum_dks_cycle.md``):
# a ``model``-flavored note may be named ``pattern_<slug>`` (DKS pattern discovery,
# ``areas/models/pattern_*.md``, ``building_block: model``) or ``tool_<slug>`` (an
# algorithm/tool model note). Keyed as ``(destination, alias_prefix) -> flavor`` so
# the alias applies only under that flavor's destination subtree, never globally.
_PREFIX_ALIASES: dict[str, list[tuple[str, str]]] = {
    "areas": [("pattern_", "model"), ("tool_", "model")],
}


@lru_cache(maxsize=1)
def _reverse_index() -> dict[str, list[tuple[str, str]]]:
    """Build ``destination -> [(filename_prefix, flavor), ...]`` from the
    registry (plus :data:`_PREFIX_ALIASES`), sorted so the LONGEST prefix wins.

    Read-only after the one-time build (``lru_cache`` size 1). The sort key
    ``(-len(prefix), prefix)`` puts longer prefixes first — load-bearing so that
    under ``resources/analysis_thoughts`` the specific ``thought_observation_`` /
    ``thought_hypothesis_`` / ``thought_counter_`` prefixes are matched BEFORE
    the bare ``thought_``; and under ``0_entry_points`` the empty prefix ``""``
    (the ``navigation`` flavor) sorts LAST, acting as that directory's default
    only after ``entry_`` / ``acronym_glossary_`` are tried.
    """
    index: dict[str, list[tuple[str, str]]] = {}
    for flavor, spec in capture.REGISTRY.items():
        index.setdefault(spec.destination, []).append((spec.filename_prefix, flavor))
    for dest, aliases in _PREFIX_ALIASES.items():
        index.setdefault(dest, []).extend(aliases)
    for dest in index:
        index[dest].sort(key=lambda t: (-len(t[0]), t[0]))
    return index


def resolve_flavor(target_path: str) -> str | None:
    """Reverse-resolve a vault-relative ``target_path`` to its capture flavor.

    Walks the note's ancestor directories DEEPEST-first: at each ancestor that
    is a registered destination it tries that destination's prefixes (longest
    first) and returns the first flavor whose prefix matches the filename. This
    resolves notes NESTED under a registered destination — the ``model`` flavor's
    destination is ``areas`` but the vault writes model notes to ``areas/models/``
    (the DKS cycle's ``areas/models/pattern_*.md`` / ``model_*.md``), so an
    exact-directory lookup would miss them. A deeper ancestor with a matching
    prefix wins over a shallower one (more specific location); the longest-prefix
    order is the tiebreak WITHIN one destination (see :func:`_reverse_index`).

    Returns ``None`` (fail-soft) when no ancestor destination has a matching
    prefix — a ``capture()`` ``destination=`` override dir whose filename prefix
    is unregistered (``areas/tools/tool_x.md``, ``resources/teams/team_x.md``), a
    bare filename, or an unknown prefix. The caller stamps an empty contract for
    such leaves so the writer degrades gracefully.

    The benign ``thought_`` collision (``argument`` and ``thought`` share the
    destination, prefix, ``bb_type`` and ``second_category``) resolves
    deterministically to the alphabetically-first flavor, but the resulting
    contract is identical either way, so callers must not depend on which wins.
    """
    if not isinstance(target_path, str) or not target_path:
        return None
    p = PurePosixPath(target_path)
    name = p.name
    index = _reverse_index()
    note_dir = p.parent
    for ancestor in (note_dir, *note_dir.parents):
        candidates = index.get(str(ancestor))
        if not candidates:
            continue
        for prefix, flavor in candidates:
            if name.startswith(prefix):
                return flavor
        # A registered ancestor with no matching prefix does not block a
        # shallower ancestor — keep walking up.
    return None


@lru_cache(maxsize=None)
def _template_h2_sections(flavor: str) -> tuple[str, ...]:
    """The ``## H2`` headers declared in a flavor's template file.

    Used for the ``SECTION_DIVERGENT_FLAVORS`` (code_snippet / skill /
    experiment / code_repo), whose file-shape legitimately diverges from their
    building block's ``BB_SPECS`` section triple — so their contract must come
    from the template, not ``BB_SPECS[procedure]``. Reuses the exact parse
    :func:`capture.check_template_registry_consistency` uses
    (``capture._TMPL_H2_RE`` + ``tessellum.data.templates_dir``).

    Placeholder headers (containing an ``<…>`` fill token — e.g. the ``skill``
    template's ``## Step 1: <First action>``) are DROPPED: they are authoring
    scaffolds, not literal section names, and delivering them verbatim would tell
    the writer to emit a section named ``## Step 1: <First action>``. Fail-soft:
    returns ``()`` on ANY read/parse error — never raises. Memoized (the
    templates are static per process)."""
    from tessellum.data import templates_dir

    try:
        spec = capture.get_spec(flavor)
        text = (templates_dir() / spec.template_filename).read_text(encoding="utf-8")
        headers = (
            h.split("<!--")[0].strip() for h in capture._TMPL_H2_RE.findall(text)
        )
        # Drop placeholder-bearing headers (``<…>`` fill tokens) — scaffolds, not
        # real section names — while keeping concrete ones.
        return tuple(h for h in headers if h and "<" not in h and ">" not in h)
    except Exception:  # noqa: BLE001 — an unreadable template degrades, never kills
        return ()


def render_type_contract(
    flavor: str,
    second_category: str,
    required_sections: tuple[str, ...],
) -> str:
    """Render the COMPACT per-type contract block for the writer.

    Deliberately compact — it shares the writer prompt's ``WindowedAssembler``
    budget with the ``## References`` block (``related_references_md``), so it
    names the flavor + second_category + the required-section checklist + one
    reference-rule line, NOT a full template dump. When ``required_sections`` is
    empty (a divergent flavor whose template couldn't be read) it tells the
    writer to follow the plan's per-flavor format instead of a fixed list.
    """
    if required_sections:
        sections = ", ".join(f"`## {s}`" for s in required_sections)
        return (
            f"Type: `{flavor}` (second_category: {second_category}). "
            f"Your written note MUST include these H2 sections: {sections}. "
            f"End with a `## References` section of relative markdown links."
        )
    return (
        f"Type: `{flavor}` (second_category: {second_category}). "
        f"This type uses its own per-flavor template shape — follow the plan's "
        f"format definition and the pilot worked example, not a fixed section "
        f"list. End with a `## References` section of relative markdown links."
    )


def build_type_contract(flavor: str) -> NoteTypeContract:
    """Build the :class:`NoteTypeContract` for a resolved flavor. Keyed on the
    FLAVOR (finer than second_category): ``argument`` / ``counter_argument`` /
    ``hypothesis`` all share ``second_category=analysis`` but have distinct
    ``required_sections``.

    Primary flavors get ``BB_SPECS[BuildingBlock(bb_type)].required_sections``.
    A ``SECTION_DIVERGENT`` flavor gets its OWN template's H2 headers (fail-soft
    to ``()`` → ``section_source="divergent-unreadable"``)."""
    spec = capture.get_spec(flavor)
    if flavor in capture.SECTION_DIVERGENT_FLAVORS:
        sections = _template_h2_sections(flavor)
        section_source = "template" if sections else "divergent-unreadable"
    else:
        try:
            sections = BB_SPECS[BuildingBlock(spec.bb_type)].required_sections
            section_source = "BB_SPECS"
        except (ValueError, KeyError):
            sections = ()
            section_source = "divergent-unreadable"
    return NoteTypeContract(
        flavor=flavor,
        second_category=spec.second_category,
        building_block=spec.bb_type,
        required_sections=tuple(sections),
        section_source=section_source,
        contract_md=render_type_contract(flavor, spec.second_category, tuple(sections)),
    )


def resolve_note_contract(target_path: str) -> NoteTypeContract | None:
    """The single-leaf public entry point (mirrors ``enrich_related_notes``'s
    call style). Resolves ``target_path`` → flavor → contract, or ``None`` when
    the path resolves to no registered flavor. Wrapped fail-soft: any error
    (a malformed path, a registry lookup miss) yields ``None`` rather than
    raising into the wave."""
    try:
        flavor = resolve_flavor(target_path)
        if flavor is None:
            return None
        return build_type_contract(flavor)
    except Exception:  # noqa: BLE001 — resolution degrades to no contract, never kills
        return None


__all__ = [
    "NoteTypeContract",
    "resolve_flavor",
    "build_type_contract",
    "render_type_contract",
    "resolve_note_contract",
]
