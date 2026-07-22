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


# ── The DIGEST_GATES registry, parameterized by scope ───────────────────────


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


# A scope → suite-builder registry so the driver can select gates by scope
# without a second mechanism. ``plan`` scope is a placeholder for the
# augment/review plan-time gates (Phase 6 wires the sign-off approver).
DIGEST_GATES: dict[GateScope, Callable[[], GateSuite]] = {
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
    "DIGEST_GATES",
]
