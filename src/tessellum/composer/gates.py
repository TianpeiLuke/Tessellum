"""Gate engine — the one gate abstraction, at three scopes.

Composer v4, Phase 3. A **gate** is a named predicate over some target
that a session/plan/wave must pass to advance. Gates are the runtime
realization of the compile-before-dispatch → gate-before-close
discipline: a session is a transaction, and its *close-gate* is the
commit check.

Design invariants (from the v4 identity gates):

- **IDENT-3 (programs decide).** A gate predicate is a pure program — it
  never calls an LLM. The one semantic check (grounding/faithfulness)
  consumes a verifier's *already-produced* typed verdict; it does not
  itself invoke a model. So every :class:`Gate` here is program logic.
- **IDENT-5 (fail-closed).** A gate that cannot prove PASS is a FAIL.
  The grounding predicate treats an unverifiable source
  (``auth_blocked``) as a FAIL, never a plausibility-based pass.

One abstraction, three scopes (all :class:`Gate` instances of the same
engine — no second mechanism):

1. **plan** — augment/review checks over a whole plan, once, before the
   wave. "Is the plan sound?"
2. **session** — the *same* per-note predicates re-applied per note as
   its commit check. "Is THIS note sound?" (the per-session close-gate).
3. **wave** — cross-set checks a single session can't see (dedup,
   cross-reference integrity across notes). "Is the BATCH sound?"

The close-gate's pure predicates reuse :mod:`tessellum.format`
(``validate`` = format + links + BB edges, ``check_links``), so there is
no re-implementation of the note-format spec here — the gate engine is
the *composition + scope* layer over the existing format primitives.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal, Sequence

from tessellum.format import Issue, Severity, validate

GateKind = Literal["compile", "preflight", "checkpoint", "sweep"]
"""What a gate *is*, for grouping/telemetry:

- ``compile`` — a static contract check before dispatch (P4.5 lives here).
- ``preflight`` — a pre-execution readiness check.
- ``checkpoint`` — a per-note quality check at write/commit time.
- ``sweep`` — a cross-set integrity check over many notes.
"""

GateScope = Literal["plan", "session", "wave"]
"""The breadth a gate applies to — see the module docstring."""


@dataclass(frozen=True)
class GateResult:
    """The outcome of running one :class:`Gate`.

    Attributes:
        gate_id: The gate that ran.
        passed: ``True`` iff the predicate returned no blocking issues.
        issues: Structured findings (empty on PASS). These feed the fix
            stage — a curated-diagnostics channel, not raw logs.
        cause: A short terminal-cause tag on FAIL (``"format"`` /
            ``"grounding"`` / ``"auth_blocked"`` / ``"ghost_ref"`` / …),
            or ``None`` on PASS. The manifest records this.
    """

    gate_id: str
    passed: bool
    issues: tuple[Issue, ...] = ()
    cause: str | None = None


# The predicate signature: takes a target (a note path, a note-path
# sequence, or an arbitrary context object) and returns the issues it
# found (empty = PASS). Pure — no LLM, no mutation of the target.
GatePredicate = Callable[..., Sequence[Issue]]


@dataclass(frozen=True)
class Gate:
    """A named, scoped predicate a target must pass.

    Attributes:
        gate_id: Stable identifier (e.g. ``"format"``, ``"ghost_ref"``).
        kind: One of :data:`GateKind`.
        scope: One of :data:`GateScope`.
        predicate: A pure callable returning the issues it found (empty =
            PASS). Blocking severity is decided by ``block_on``.
        cause: The terminal-cause tag stamped on a FAIL (defaults to
            ``gate_id``).
        block_on: The minimum :class:`~tessellum.format.Severity` that
            makes an issue blocking. Defaults to ERROR — WARNING/INFO
            issues are reported but don't fail the gate.
    """

    gate_id: str
    kind: GateKind
    scope: GateScope
    predicate: GatePredicate
    cause: str | None = None
    block_on: Severity = Severity.ERROR

    def run(self, target, /, **kwargs) -> GateResult:
        """Evaluate the predicate against ``target``; classify the result.

        The gate PASSES iff no issue meets or exceeds ``block_on``
        severity. Non-blocking issues (e.g. WARNINGs when ``block_on`` is
        ERROR) are still carried on the result for diagnostics.
        """
        issues = tuple(self.predicate(target, **kwargs))
        blocking = tuple(i for i in issues if _at_least(i.severity, self.block_on))
        passed = not blocking
        return GateResult(
            gate_id=self.gate_id,
            passed=passed,
            issues=issues,
            cause=None if passed else (self.cause or self.gate_id),
        )


_SEVERITY_ORDER = {Severity.INFO: 0, Severity.WARNING: 1, Severity.ERROR: 2}


def _at_least(sev: Severity, floor: Severity) -> bool:
    return _SEVERITY_ORDER[sev] >= _SEVERITY_ORDER[floor]


# ── Close-gate = a composite of scoped Gates ────────────────────────────────


@dataclass(frozen=True)
class CompositeGateResult:
    """The aggregate result of running an ordered list of gates.

    Attributes:
        passed: ``True`` iff *every* member gate passed.
        results: One :class:`GateResult` per member, in run order.
        first_failure_cause: The ``cause`` of the first failing gate (the
            terminal-cause tag), or ``None`` when all passed.
    """

    passed: bool
    results: tuple[GateResult, ...]
    first_failure_cause: str | None = None

    @property
    def blocking_issues(self) -> tuple[Issue, ...]:
        """All blocking issues across the member gates (fix-stage input)."""
        out: list[Issue] = []
        for r in self.results:
            if not r.passed:
                out.extend(r.issues)
        return tuple(out)


@dataclass(frozen=True)
class GateSuite:
    """An ordered set of gates evaluated as one commit check.

    Short-circuits by default (stop at the first failing gate — the
    cheapest structural pre-filter fails fast before the expensive
    semantic one runs), but can run all gates for a full diagnostic
    sweep.
    """

    gates: tuple[Gate, ...]

    def evaluate(
        self, target, /, *, short_circuit: bool = True, **kwargs
    ) -> CompositeGateResult:
        results: list[GateResult] = []
        first_cause: str | None = None
        all_passed = True
        for gate in self.gates:
            res = gate.run(target, **kwargs)
            results.append(res)
            if not res.passed:
                all_passed = False
                if first_cause is None:
                    first_cause = res.cause
                if short_circuit:
                    break
        return CompositeGateResult(
            passed=all_passed,
            results=tuple(results),
            first_failure_cause=first_cause,
        )


# ── Pure predicates for the close-gate ──────────────────────────────────────


def format_predicate(target: Path | str, /, **_) -> Sequence[Issue]:
    """The ``format`` close-gate predicate — reuses ``tessellum.format``.

    ``validate`` already runs frontmatter spec + wiki/markdown link checks
    (``check_links``) + BB-typed-edge checks in one pass, returning ERROR
    issues that block. This wraps it so the gate engine and the CLI share
    one format definition (no re-implementation).
    """
    return validate(Path(target))


def grounding_predicate(
    target: Path | str, /, *, verdict: "GroundingVerdict | None" = None, **_
) -> Sequence[Issue]:
    """The ``grounding`` close-gate predicate — consumes a typed verdict.

    This is the *only* semantic close-gate check, but it is still a pure
    program: it does **not** call an LLM. An independent read-only
    verifier (a cheap model that structurally cannot mutate the note it
    judges) produces a :class:`GroundingVerdict`; this predicate just
    reads it. IDENT-5 fail-closed: a ``None`` verdict (never ran) or an
    ``auth_blocked`` verdict (source unreadable / auth expired) is a FAIL
    — never a plausibility-based pass (the fail-closed rule).
    """
    if verdict is None:
        return [
            Issue(
                Severity.ERROR,
                "GROUND-000",
                "grounding",
                "no grounding verdict available — fail-closed (verifier did not run)",
            )
        ]
    if verdict.status == "grounded":
        # W2 (FZ 20k9c1a1a1b7c2k2a4): a grounded verdict may carry an
        # ADVISORY (the cross-contamination tier — tokens present in the
        # source but outside the note's owned slice). Non-blocking
        # (WARNING < block_on=ERROR), carried for diagnostics. `detail`
        # remains purely informational and produces no issue.
        if verdict.advisory:
            return [
                Issue(
                    Severity.WARNING,
                    "GROUND-003",
                    "grounding",
                    f"advisory: {verdict.advisory}",
                )
            ]
        return []
    if verdict.status == "auth_blocked":
        return [
            Issue(
                Severity.ERROR,
                "GROUND-002",
                "grounding",
                f"source unverifiable (auth_blocked): {verdict.detail or 'no detail'}",
            )
        ]
    # ungrounded
    return [
        Issue(
            Severity.ERROR,
            "GROUND-001",
            "grounding",
            f"note not grounded in source: {verdict.detail or 'fabrication risk'}",
        )
    ]


@dataclass(frozen=True)
class GroundingVerdict:
    """A read-only verifier's typed verdict on note↔source faithfulness.

    The verifier is an agent (a cheap model on a read-only tool
    allowlist); its verdict is the *evidence* this program checks — the
    Gate Engine boundary: the agent produces evidence, the program
    decides pass/fail.

    Attributes:
        status: ``"grounded"`` (faithful to source) | ``"ungrounded"``
            (fabrication/omission risk) | ``"auth_blocked"`` (source
            could not be read to verify — fail-closed).
        detail: Optional human-readable reason.
    """

    status: Literal["grounded", "ungrounded", "auth_blocked"]
    detail: str | None = None
    advisory: str | None = None
    """W2 (FZ 20k9c1a1a1b7c2k2a4): a non-blocking finding carried on a
    grounded verdict (the cross-contamination tier). ``detail`` stays the
    informational channel; only ``advisory`` produces a WARNING issue."""


# ── Wave-scope cross-set predicate ──────────────────────────────────────────


def duplicate_target_predicate(paths: Sequence[Path | str], /, **_) -> Sequence[Issue]:
    """A ``dedup`` wave-scope predicate — flags duplicate target paths.

    A per-session close-gate structurally cannot see its siblings, so two
    sessions writing the *same* note path (a dedup miss) escapes it. This
    wave-scope sweep catches it after the wave: any target path claimed by
    more than one session is a blocking issue. (Content-level dedup — near
    -duplicate notes — is a richer check deferred to a later phase; this
    is the exact-path guard.)
    """
    seen: dict[str, int] = {}
    for p in paths:
        key = str(Path(p))
        seen[key] = seen.get(key, 0) + 1
    return [
        Issue(
            Severity.ERROR,
            "WAVE-001",
            "dedup",
            f"target path written by {n} sessions (duplicate): {key}",
        )
        for key, n in sorted(seen.items())
        if n > 1
    ]


_MD_LINK_RE = __import__("re").compile(r"\[([^\]]+)\]\(([^)\s]+\.md)\)")
_FENCE_STRIP_RE = __import__("re").compile(r"(?ms)^```.*?^```\s*$")


def link_resolution_predicate(paths: Sequence[Path | str], /, **_) -> Sequence[Issue]:
    """W4 (FZ 20k9c1a1a1b7c2k2a4): the post-wave LINK sweep — the one check
    the per-note close gate structurally cannot time right (a link to a
    sibling written LATER in the wave is unresolvable at close and fine at
    wave end; one still unresolved after the whole wave is a real break).
    Replaces the LLM ``verify`` step's asserted link checking with computed
    evidence. ADVISORY (WARNING) per the report-first rule — findings reach
    the run events via the wave-gate composite."""
    issues: list[Issue] = []
    for p in paths:
        path = Path(p)
        try:
            body = _FENCE_STRIP_RE.sub("", path.read_text(encoding="utf-8"))
        except OSError:
            continue
        for m in _MD_LINK_RE.finditer(body):
            target = (path.parent / m.group(2)).resolve()
            if not target.exists():
                issues.append(
                    Issue(
                        Severity.WARNING,
                        "WAVE-003",
                        "link_resolution",
                        f"unresolved link after the wave: {m.group(2)} "
                        f"(in {path.name})",
                    )
                )
    return issues


# ── The DIGEST_GATES registry, parameterized by scope ───────────────────────


_CODE_FENCE_RE = __import__("re").compile(r"(?m)^```")
_GOLDEN_CODE_CAP = 6


def code_density_predicate(target: Path | str, /, **_) -> Sequence[Issue]:
    """k2a4a: the per-note CODE-DENSITY check, computed at close — N5's cap
    finally enforced by code instead of prose. ADVISORY (WARNING) per the
    report-first rule; the fix loop and the writer's numeric budget do the
    prevention, this check does the accounting."""
    try:
        text = Path(target).read_text(encoding="utf-8")
    except OSError:
        return []
    blocks = len(_CODE_FENCE_RE.findall(text)) // 2
    if blocks <= _GOLDEN_CODE_CAP:
        return []
    return [
        Issue(
            Severity.WARNING,
            "NOTE-005",
            "code_density",
            f"{blocks} fenced code blocks — over the {_GOLDEN_CODE_CAP}-block "
            f"cap (N5); select representative snippets",
        )
    ]


def build_close_gate() -> GateSuite:
    """The per-session close-gate: the format + grounding predicates.

    Ordered cheapest-first: the pure ``format`` structural check (a
    ``checkpoint`` gate) runs before the semantic ``grounding`` check (a
    ``checkpoint`` gate consuming the verifier verdict), so a
    format-broken note fails fast without spending the verifier. Both are
    session-scope. The remaining pure predicates (density, ≥8-terms,
    ghost, broken-link, discoverability) are folded into ``validate``'s
    link/BB-edge checks or run as wave-scope sweeps; this suite is the
    minimal always-on close gate that every note-creation session passes
    before it can close.

    A caller passes the grounding verdict through ``evaluate``'s kwargs::

        suite.evaluate(note_path, verdict=GroundingVerdict("grounded"))
    """
    return GateSuite(
        gates=(
            Gate(
                gate_id="format",
                kind="checkpoint",
                scope="session",
                predicate=format_predicate,
                cause="format",
            ),
            Gate(
                gate_id="grounding",
                kind="checkpoint",
                scope="session",
                predicate=grounding_predicate,
                cause="grounding",
            ),
            # k2a4a: advisory code-density accounting (WARNINGs only — the
            # gate always passes; findings ride the composite).
            Gate(
                gate_id="code_density",
                kind="checkpoint",
                scope="session",
                predicate=code_density_predicate,
                cause="code_density",
            ),
        )
    )


def build_wave_gate() -> GateSuite:
    """The per-wave post-batch gate: cross-set checks (dedup, …)."""
    return GateSuite(
        gates=(
            Gate(
                gate_id="dedup",
                kind="sweep",
                scope="wave",
                predicate=duplicate_target_predicate,
                cause="dedup",
            ),
        )
    )


# ── Plan-scope predicate (the pre-filter before the review-agent) ───────────


def plan_structure_predicate(plan_doc: "dict | None", /, **_) -> Sequence[Issue]:
    """A ``plan`` structural pre-filter over a ``plan_doc`` mapping.

    The cheapest rung of the ``review → ready`` sign-off ladder — a pure
    structural check that a plan is even *shaped* like a plan before an
    (expensive) reviewer agent judges its substance: it must carry a
    non-empty ``plan_path``/``plan_text`` and a positive ``total_notes``.
    A structurally-broken plan is rejected here without spending an agent.
    Missing/``None`` plan → a single blocking issue (fail-closed).
    """
    if not isinstance(plan_doc, dict):
        return [
            Issue(Severity.ERROR, "PLAN-000", "plan_doc",
                  "no plan_doc available — fail-closed")
        ]
    issues: list[Issue] = []
    if not str(plan_doc.get("plan_path") or "").strip():
        issues.append(
            Issue(Severity.ERROR, "PLAN-001", "plan_path", "plan has no plan_path")
        )
    if not str(plan_doc.get("plan_text") or "").strip():
        issues.append(
            Issue(Severity.ERROR, "PLAN-002", "plan_text", "plan body is empty")
        )
    total = plan_doc.get("total_notes")
    if not isinstance(total, int) or total <= 0:
        issues.append(
            Issue(Severity.ERROR, "PLAN-003", "total_notes",
                  f"plan declares no notes to produce (total_notes={total!r})")
        )
    return issues


# FZ 20k9d4 — the OBJECTIVE density ceiling. A planned note at/above this word
# count is not density-atomic and the plan must be re-planned (split OR the
# coverage map rearranged). Matches the plan skill's ~1800-word split threshold
# (skill_tessellum_plan_digestion.md). A number, not a judgement — so the hard
# gate never rejects on a subjective "is this atomic?" read.
PLAN_NOTE_MAX_WORDS: int = 1800

# PLAN-008 over-split floor (FZ 20k9c1a1a1b7c3). The symmetric complement to
# PLAN-004's over-dense CEILING: a plan that shreds a source into many thin
# notes fails the eval's note-count ratio just as an over-dense plan fails
# density. The threshold is the eval's OWN P1 tolerance boundary — the golden
# targets ~1,600 words/note and P1 accepts up to ratio 1.4, i.e. down to
# 1,600 / 1.4 ≈ 1,143 words/note — so the max acceptable note count is
# ceil(measured_total_words / 1143). Setting the floor to the eval boundary
# (not the skill's 1,500 aim) keeps the gate NO STRICTER than the metric it
# serves, so a golden-shaped plan never false-fails. Eval run 3 declared 13
# notes for a 12,813-word source (ceil(12813/1143)=12) → over-split by 1.
PLAN_OVERSPLIT_MIN_WORDS: int = 1143


def plan_atomicity_predicate(plan_doc: "dict | None", /, **_) -> Sequence[Issue]:
    """A ``plan`` gate over OBJECTIVE note-atomicity signals (FZ 20k9d4).

    Fails-closed on measurable, non-arguable facts only — never on a subjective
    "is this note truly BB-atomic?" judgement (that stays advisory, judged by
    the reviewer agent). On failure the issues surface into the review
    ``failures`` list and force the plan back through re-planning, where the
    planner may remedy by SPLITTING into new notes OR REARRANGING the coverage
    map (redistributing content) — the gate asserts "not acceptable, re-plan",
    it does not prescribe the fix.

    Objective triggers, read from either the typed ``note_intent_graph``
    (an OPT-IN P2b/corpus/DKS shape — NOT emitted by the current LLM phase
    skills, so on the live single-doc path the ``planned_notes`` fallback is
    what runs) or the skill's ``planned_notes`` + ``section_coverage_map``:

    - **PLAN-004** a note declares ``approx_words >= PLAN_NOTE_MAX_WORDS`` —
      the density ceiling (a number; word values are coerced from the int /
      numeric-string / float shapes raw LLM JSON delivers).
    - **PLAN-005** a note's ``building_block`` crams more than one block (a
      comma/`/`/`+`/`and`-joined value) — the objective single-BB smell, keyed
      on :data:`MULTI_BB_SEPARATORS`. (Neither a CONTENT mix within a
      single-token note NOR an invalid-vocabulary token is flagged here — the
      former is the reviewer's advisory call, the latter the G1 format
      validator's job.)
    - **PLAN-006** a source section is omitted from coverage — checked two
      ways: (a) a ``section_coverage_map`` row with an empty/`none`/`tbd`
      target, AND (b) set-difference of the authoritative source-section
      inventory (``plan_doc['pages'][*]['headings']``) MINUS the sections the
      coverage map actually names, so a section DROPPED from the map entirely
      is still caught. Fails-closed if the plan enumerates notes but the
      coverage map is not machine-checkable row-form (a shape drift must never
      silently pass).
    - **PLAN-007** the plan enumerates notes but NONE declares a positive
      ``approx_words`` — density is unverifiable, so the plan must be re-planned
      with real per-note word estimates (keeps IDENT-5 fail-closed; a count,
      not a judgement).
    - **PLAN-008** the plan is OVER-SPLIT — the enumerated note count exceeds
      ``ceil(measured_source_words / PLAN_OVERSPLIT_MIN_WORDS)`` (the symmetric
      complement to PLAN-004's over-dense ceiling). Only the ``planned_notes``
      shape, and only when ``pages[*].measured_words`` gives a real source total
      (fail-soft: no measurement → no judgement). The floor is the eval's own
      P1 ratio boundary, so a golden-shaped plan never false-fails; remedy by
      CONSOLIDATING thin notes or re-mapping coverage.

    A plan_doc with NEITHER a typed graph NOR planned_notes is not judged here
    (no atomicity signal to check) — ``plan_structure_predicate`` already
    fail-closes a shapeless plan; this predicate only adds objective checks
    when the plan actually enumerates notes."""
    if not isinstance(plan_doc, dict):
        return []  # plan_structure_predicate owns the fail-closed shapeless case
    issues: list[Issue] = []

    notes, notes_source = _plan_notes(plan_doc)
    any_words_declared = False
    for note in notes:
        name = str(note.get("note_id") or note.get("filename") or "?")
        words = _coerce_words(note.get("approx_words"))
        if words is not None and words > 0:
            any_words_declared = True
        if words is not None and words >= PLAN_NOTE_MAX_WORDS:
            issues.append(Issue(
                Severity.ERROR, "PLAN-004", name,
                f"note '{name}' is not density-atomic: approx_words={words} "
                f">= {PLAN_NOTE_MAX_WORDS} — re-plan (split or rearrange the "
                f"coverage map so no note carries >= {PLAN_NOTE_MAX_WORDS} words)",
            ))
        bb = note.get("building_block")
        if bb is not None and not is_single_bb(bb):
            issues.append(Issue(
                Severity.ERROR, "PLAN-005", name,
                f"note '{name}' is not BB-atomic: building_block={bb!r} crams "
                f"more than one building block — re-plan so each note declares "
                f"a single building block",
            ))

    # PLAN-007 — density unverifiable. ONLY for the LLM ``planned_notes`` shape,
    # where a word estimate is expected. A programmatically-compiled typed
    # ``note_intent_graph`` (e.g. the DKS compiler) legitimately carries no word
    # estimates, so it is exempt — density is not the LLM-planning concern there.
    if notes and notes_source == "planned_notes" and not any_words_declared:
        issues.append(Issue(
            Severity.ERROR, "PLAN-007", "planned_notes",
            f"no planned note declares a positive approx_words — density is "
            f"unverifiable; re-plan with a per-note word estimate so the "
            f"{PLAN_NOTE_MAX_WORDS}-word ceiling can be checked",
        ))

    # PLAN-008 — over-split floor (FZ 20k9c1a1a1b7c3), the complement to PLAN-004.
    # ONLY the LLM ``planned_notes`` shape (a typed graph plans its own fan-out),
    # and ONLY when the MEASURED source total is known (fail-soft: no measurement
    # → no over-split judgement, never a false fail). Over-split = the enumerated
    # count exceeds ceil(measured_total / PLAN_OVERSPLIT_MIN_WORDS) — the eval's
    # own P1 ratio boundary, so a golden-shaped plan passes. Remedy: consolidate
    # thin notes (or re-map coverage), the mirror of PLAN-004's split remedy.
    if notes and notes_source == "planned_notes":
        measured_total = _measured_source_words(plan_doc)
        if measured_total > 0:
            max_notes = math.ceil(measured_total / PLAN_OVERSPLIT_MIN_WORDS)
            if len(notes) > max_notes:
                issues.append(Issue(
                    Severity.ERROR, "PLAN-008", "planned_notes",
                    f"plan is over-split: {len(notes)} notes for a "
                    f"{measured_total}-word source exceeds the max "
                    f"{max_notes} (measured_total / {PLAN_OVERSPLIT_MIN_WORDS} "
                    f"words-per-note floor) — re-plan by CONSOLIDATING thin "
                    f"notes or redistributing the coverage map so each note "
                    f"carries closer to the ~1,600-word target",
                ))

    issues.extend(_coverage_issues(plan_doc, has_notes=bool(notes)))
    return issues


_UNMAPPED_MARKERS: frozenset[str] = frozenset(
    {"", "none", "null", "n/a", "na", "unmapped", "tbd", "todo", "-", "skip"}
)


def _coerce_words(value: object) -> int | None:
    """Coerce an ``approx_words`` value to a non-negative int, tolerating the
    int / numeric-string ("1800") / float (1800.0) shapes raw LLM JSON delivers.
    Excludes ``bool`` (an int subclass) and unparseable values → ``None``
    (unknown, not density-checkable)."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value >= 0 else None
    if isinstance(value, float):
        return int(value) if value >= 0 else None
    if isinstance(value, str):
        try:
            n = int(float(value.strip()))
        except (ValueError, TypeError):
            return None
        return n if n >= 0 else None
    return None


def _measured_source_words(plan_doc: dict) -> int:
    """Total MEASURED source words across ``pages[*].measured_words`` — the
    code-computed ground truth for the PLAN-008 over-split check (FZ
    20k9c1a1a1b7c3 / the b7c2k1a1b deterministic ledger). Reads the top-level
    ``pages`` (identify_source merges it in) or a nested ``source_assessment``.
    Returns ``0`` when no page carries a measured count — the caller then makes
    NO over-split judgement (fail-soft, never a false fail on an unmeasured
    plan). Only ``measured_words`` counts; an LLM ``approx_words``/``words``
    estimate is deliberately ignored (the whole point is a code-measured base)."""
    pages = plan_doc.get("pages")
    if not isinstance(pages, list) or not pages:
        src = plan_doc.get("source_assessment")
        pages = src.get("pages") if isinstance(src, dict) else None
    if not isinstance(pages, list):
        return 0
    total = 0
    for pg in pages:
        if isinstance(pg, dict):
            n = _coerce_words(pg.get("measured_words"))
            if n:
                total += n
    return total


def _coverage_issues(plan_doc: dict, *, has_notes: bool) -> list[Issue]:
    """PLAN-006 — every source section must be covered. Two checks:
    (a) empty/marker targets in the coverage-map rows, and (b) set-difference of
    the authoritative source-section inventory minus the covered sections (so a
    section dropped from the map entirely is caught). Fails-closed if notes are
    enumerated but the coverage map is present in a non-row-form shape (drift)."""
    issues: list[Issue] = []
    raw = plan_doc.get("section_coverage_map")
    covered: set[str] = set()

    if isinstance(raw, list):
        for row in raw:
            if not isinstance(row, dict):
                continue
            section = str(row.get("source_section") or "").strip()
            target = str(row.get("maps_to_note") or "").strip()
            if section and (not target or target.lower() in _UNMAPPED_MARKERS):
                issues.append(Issue(
                    Severity.ERROR, "PLAN-006", section,
                    f"source section '{section}' is not covered (maps_to_note="
                    f"{target!r}) — re-plan so every source section maps to a "
                    f"note (no content omitted)",
                ))
            elif section:
                covered.add(_norm_section(section))
    elif raw is not None and has_notes:
        # Shape drift (e.g. an ASCII-tree string) must NOT silently pass — the
        # coverage dimension is unverifiable, so fail closed.
        issues.append(Issue(
            Severity.ERROR, "PLAN-006", "section_coverage_map",
            "section_coverage_map is not a machine-checkable list of "
            "{source_section, maps_to_note} rows — coverage completeness "
            "cannot be verified; emit the coverage map in row form",
        ))
        return issues

    # (b) set-difference: authoritative source headings the map never names.
    for section in _source_sections(plan_doc):
        if _norm_section(section) not in covered:
            issues.append(Issue(
                Severity.ERROR, "PLAN-006", section,
                f"source section '{section}' is omitted from the coverage map "
                f"— re-plan so every source section maps to a note (no content "
                f"omitted)",
            ))
    return issues


def _norm_section(section: str) -> str:
    """Normalize a section heading for set membership (case/space-insensitive)."""
    return " ".join(section.split()).strip().lower()


def _source_sections(plan_doc: dict) -> list[str]:
    """The authoritative source-section inventory: the ``headings`` recorded
    per page in the plan's ``source_assessment`` (``plan_doc['pages']``). Empty
    when the plan carries no measured headings (then only the row-level empty-
    target check in PLAN-006 applies — no inventory to diff against)."""
    pages = plan_doc.get("pages")
    if not isinstance(pages, list):
        return []
    sections: list[str] = []
    for page in pages:
        if not isinstance(page, dict):
            continue
        headings = page.get("headings")
        if isinstance(headings, list):
            sections.extend(str(h).strip() for h in headings if str(h).strip())
    return sections


# Multi-BB separators — a building_block value containing any of these crams
# more than one block into one note. This is the SINGLE SOURCE OF TRUTH for the
# multi-BB smell: both the plan gate (PLAN-005) and the capsule gate
# (STRUCT-BB-ATOMIC, structural_gates.bb_atomicity_predicate) consume THIS
# constant, so the two never drift to different single-BB semantics.
MULTI_BB_SEPARATORS: tuple[str, ...] = (",", "/", "+", " and ")


def is_single_bb(building_block: object) -> bool:
    """True iff ``building_block`` is a single (non-multi-BB) value.

    Rejects a value that crams two blocks into the field
    (``"concept, procedure"``, ``"concept+procedure"``, ``"concept and
    procedure"``, ``"concept/procedure"``) — the OBJECTIVE half of single-BB,
    keyed on :data:`MULTI_BB_SEPARATORS`. A CONTENT mix within a validly-named
    note is the reviewer's advisory call, not gated here; and vocabulary
    validity (is the token a real BB?) is the G1 format validator's job."""
    if not isinstance(building_block, str):
        return False
    return not any(sep in building_block for sep in MULTI_BB_SEPARATORS)


def _plan_notes(plan_doc: dict) -> tuple[list[dict], str]:
    """The plan's per-note records + their SOURCE shape.

    Returns ``(notes, source)`` where ``source`` is ``"note_intent_graph"``
    (the typed shape), ``"planned_notes"`` (the LLM skill table), or ``"none"``.
    The source matters for PLAN-007: word estimates are expected on the LLM
    ``planned_notes`` shape but NOT on a programmatically-compiled typed graph
    (e.g. the DKS compiler), which is exempt.

    NOTE: the ``note_intent_graph`` branch is an OPT-IN P2b/corpus/DKS shape and
    is NOT emitted by the current LLM phase skills; on the live single-doc
    digestion path this always uses the ``planned_notes`` fallback. Both branches
    keep only dict rows — a graph whose intents are already typed ``NoteIntent``
    OBJECTS (not dicts) is skipped here, but at the live plan-gate call site
    plan_doc holds raw LLM JSON (dicts), so this is not hit in practice."""
    graph = plan_doc.get("note_intent_graph")
    if isinstance(graph, dict) and isinstance(graph.get("intents"), list):
        dict_intents = [n for n in graph["intents"] if isinstance(n, dict)]
        if dict_intents:
            return dict_intents, "note_intent_graph"
    planned = plan_doc.get("planned_notes")
    if isinstance(planned, list):
        return [n for n in planned if isinstance(n, dict)], "planned_notes"
    return [], "none"


def plan_sections_predicate(plan_doc: "dict | None", /, **_) -> Sequence[Issue]:
    """PLAN-009 (phase 3, FZ 20k9c1a1a1b7c2k2a3a): the mandatory-sections
    scan PROMOTED from exhibit-informed to gating — the deterministic check
    the eval's P7 runs, at the eval's own >=90% threshold (the goldens
    themselves land 13–14/14). The Bedrock leg's first-ever 14/14 proves the
    writers can; with F8 the revise loop now GRINDS plans there instead of
    P7 failing silently at scoring time. Deliberately threshold-based, never
    per-section: section NAMES legitimately vary (the E1.3 lesson)."""
    if not isinstance(plan_doc, dict):
        return []
    # Scope: the mandatory-section contract applies to FULL digestion plans,
    # and the marker of one is its section coverage map (the artifact the
    # mandatory sections document). A doc without one (unit fixtures, partial
    # folds) is not in scope — deliberate, not a loophole: every real plan
    # already carries the map because PLAN-006 requires it.
    cmap = plan_doc.get("section_coverage_map")
    if not (isinstance(cmap, list) and cmap):
        return []
    plan_text = plan_doc.get("plan_text")
    if not isinstance(plan_text, str) or not plan_text:
        return []
    from tessellum.composer.contracts import mandatory_section_stems

    stems = mandatory_section_stems()
    low = plan_text.lower()
    present = [s for s in stems if s.lower() in low]
    if len(present) >= 0.9 * len(stems):
        return []
    missing = [s for s in stems if s.lower() not in low]
    # Run 9 (F13's discovery run): ONE issue per missing stem, not one
    # aggregate line — the revise loop's convergence metric and P24's
    # revert-to-best both compare FAILURE COUNTS, so an aggregate hides
    # within-gate progress (10/14 → 9/14 read as "same one failure") and a
    # partially-improved round trips the same-failure short-circuit.
    # Per-stem issues make magnitude visible to both.
    return [
        Issue(
            Severity.ERROR,
            "PLAN-009",
            "plan_sections",
            f"mandatory section missing: '{s}' "
            f"({len(present)}/{len(stems)} present, threshold >=90%) — add it "
            f"as a section (an equivalent name under the same stem counts)",
        )
        for s in missing
    ]


def plan_balance_predicate(plan_doc: "dict | None", /, **_) -> Sequence[Issue]:
    """PLAN-010 (W1.3, FZ 20k9c1a1a1b7c2k2a4): per-note owned-span BALANCE —
    ADVISORY. The note-count band constrains the plan's TOTAL; nothing
    constrained the per-note allocation, and run 13's bimodal Tier-3 showed
    notes owning 11–17 sections diluting to ~1.7 completeness while notes
    owning 6–8 scored 4.5–5.0. A note whose owned slice measures more than
    2× the density ceiling cannot treat its sections deeply at cap — flagged
    as WARNING (never blocking until calibrated; the report-first rule)."""
    if not isinstance(plan_doc, dict):
        return []
    cmap = plan_doc.get("section_coverage_map")
    planned = plan_doc.get("planned_notes")
    source = plan_doc.get("source_excerpt")
    if not (isinstance(cmap, list) and cmap and isinstance(planned, list)
            and planned and isinstance(source, str) and source):
        return []
    from tessellum.composer.note_coverage import owned_span_words

    ceiling = 2 * PLAN_NOTE_MAX_WORDS
    return [
        Issue(
            Severity.WARNING,
            "PLAN-010",
            "plan_balance",
            f"note {name!r} owns {words} measured source words across "
            f"{nsec} sections — over {ceiling} (2× the {PLAN_NOTE_MAX_WORDS}"
            f"-word density ceiling); it cannot cover them deeply at cap — "
            f"consider re-allocating the coverage map",
        )
        for name, (words, nsec) in sorted(
            owned_span_words(planned, cmap, source).items()
        )
        if words > ceiling
    ]


def build_plan_gate() -> GateSuite:
    """The plan-scope structural pre-filter (the sign-off ladder's rung 1).

    Two objective gates: ``plan_structure`` (the plan is shaped like a plan) and
    ``plan_atomicity`` (FZ 20k9d4 — no note over the density ceiling, each note
    single-BB, every source section covered). Both are pure/deterministic; a
    failure loops the plan back to re-planning via the review verdict."""
    return GateSuite(
        gates=(
            Gate(
                gate_id="plan_structure",
                kind="preflight",
                scope="plan",
                predicate=plan_structure_predicate,
                cause="plan_structure",
            ),
            Gate(
                gate_id="plan_sections",
                kind="checkpoint",
                scope="session",
                predicate=plan_sections_predicate,
                cause="plan_sections",
            ),
            Gate(
                gate_id="plan_atomicity",
                kind="preflight",
                scope="plan",
                predicate=plan_atomicity_predicate,
                cause="plan_atomicity",
            ),
            # PLAN-010 emits only WARNINGs (< block_on=ERROR) — the gate
            # always passes; the findings ride the composite for exhibits
            # and diagnostics until the threshold is calibrated.
            Gate(
                gate_id="plan_balance",
                kind="preflight",
                scope="plan",
                predicate=plan_balance_predicate,
                cause="plan_balance",
            ),
        )
    )


# A scope → suite-builder registry so the driver can select gates by scope
# without a second mechanism. All three scopes are now populated: ``plan``
# (structural pre-filter, the sign-off ladder's cheap rung), ``session``
# (per-note close-gate), ``wave`` (cross-set post-batch sweep).
DIGEST_GATES: dict[GateScope, Callable[[], GateSuite]] = {
    "plan": build_plan_gate,
    "session": build_close_gate,
    "wave": build_wave_gate,
}


__all__ = [
    "GateKind",
    "GateScope",
    "GateResult",
    "GatePredicate",
    "Gate",
    "GateSuite",
    "CompositeGateResult",
    "GroundingVerdict",
    "format_predicate",
    "grounding_predicate",
    "duplicate_target_predicate",
    "build_close_gate",
    "build_wave_gate",
    "build_plan_gate",
    "plan_structure_predicate",
    "plan_atomicity_predicate",
    "PLAN_NOTE_MAX_WORDS",
    "DIGEST_GATES",
]
