"""Dialectic Knowledge System (DKS) — core runtime implementation.

This module IS the implementation. Public-API consumers should import
from the package root: ``from tessellum.dks import DKSCycle, DKSRunner, ...``.
This file is re-exported by :mod:`tessellum.dks`'s ``__init__`` and is
not part of the documented public surface; lifting members here in a
patch release is allowed only via the ``__init__`` re-export list.

Provides:

- Seven typed dataclasses (one per component output).
- A Folgezettel-ID allocator implementing the three multi-cycle modes
  (``fresh`` / ``extend`` / ``branch``) per
  :doc:`thought_dks_fz_integration`.
- :class:`DKSCycle` — drives the 7-component closed loop through an
  :class:`LLMBackend`. Supports N-perspective debate via the
  ``perspectives`` kwarg + multi-revision authoring when grounded
  labelling produces multiple ``in`` survivors.
- :class:`DKSRunner` — multi-cycle orchestration over a sequence of
  observations, threading warrant changes between cycles.

Each cycle deposits a Folgezettel subtree into the substrate
(observation → N sibling arguments → counter → pattern → revised
warrant(s)). Disagreement detection produces edges, not nodes, so they
don't get FZ IDs of their own.

The seven components map onto BB-to-BB epistemic edges as documented in
:doc:`thought_dks_design_synthesis`:

============  ===================  =======================
Step          BB type produced     FZ position
============  ===================  =======================
1. Observation  empirical_observation  cycle root (FZ N)
2. Argument A   argument               FZ N.a
3. Argument B   argument               FZ N.b
4. Contradicts  (edge — no FZ)         (link from B to A or vice versa)
5. Counter      counter_argument       FZ <attacked>.a
6. Pattern      model                  FZ <counter>.a
7. Revision     procedure/concept      FZ <pattern>.a (leaf)
============  ===================  =======================
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from typing import Literal, Mapping, Protocol, Sequence

from tessellum.bb.graph import (
    ArgumentNode,
    CounterArgumentNode,
    EmpiricalObservationNode,
    ModelNode,
)
from tessellum.composer.llm import LLMBackend, LLMRequest

# ── Type aliases ──────────────────────────────────────────────────────────

ToulminComponent = Literal[
    "premise", "warrant", "counter-example", "undercutting"
]
"""Which Toulmin component an attack targets. Per FZ 2a step 5, every
counter-argument names exactly one component, which classifies the
failure mode and constrains what kind of repair is appropriate.

- ``premise``: the data is wrong / unsupported
- ``warrant``: the rule licensing data → claim is wrong
- ``counter-example``: the warrant has an exception this case hits
- ``undercutting``: the qualifier shouldn't apply here
"""

CycleMode = Literal["fresh", "extend", "branch"]
"""Where the new cycle lives in the FZ graph. Per FZ 2a1:

- ``fresh``: new top-level FZ root (observation is unconnected)
- ``extend``: descend from a prior cycle's leaf (new observation refutes
  / extends a prior warrant)
- ``branch``: insert sibling counter at an attacked argument's position
  (new observation attacks the same argument from a different angle)
"""

CounterStrength = Literal["weak", "moderate", "strong"]


# ── Component-output dataclasses ──────────────────────────────────────────


@dataclass(frozen=True, kw_only=True)
class DKSObservation(EmpiricalObservationNode):
    """Step 1 — what happened.

    Per D1 (`plan_dks_expansion`) + FZ 2a2: subclass of
    :class:`EmpiricalObservationNode`, so ``bb_type`` is fixed at
    ``BBType.EMPIRICAL_OBSERVATION`` via the parent's
    ``field(default=..., init=False)``.

    The cycle-specific fields (``summary``, ``timestamp``) layer on
    top of the BBNode-base fields (``note_id``, ``note_name``,
    ``folgezettel``, ``folgezettel_parent``, ``note_status``).
    """

    summary: str = ""
    timestamp: str | None = None
    # P1 A1.2 — tri-temporal stamping. Separating WHEN the claim was made
    # (t_claim), WHEN its evidence was known (t_evidence), and WHEN the outcome
    # it predicts is observable (t_outcome) is what lets the P4 prequential
    # validator run a leakage-free temporal holdout: a predictive warrant is
    # un-scorable unless its outcome falls strictly AFTER its full information
    # set (see ``temporal_holdout_valid``). ISO-8601 strings; ``None`` when the
    # dimension does not apply (e.g. a non-predictive observation).
    t_claim: str | None = None
    t_evidence: str | None = None
    t_outcome: str | None = None


@dataclass(frozen=True)
class DKSWarrant:
    """A Toulmin-typed standing reason.

    Attached to each argument (the rule that licenses the move from
    data to claim). Revised by step 7's rule revision.
    """

    claim: str
    data: str
    warrant: str
    backing: str = ""
    qualifier: str = ""
    rebuttal: str = ""
    # P1 A1.2 — tri-temporal stamps carried onto the warrant so the P4
    # validator can holdout-score a predictive/causal warrant without leakage.
    t_claim: str | None = None
    t_evidence: str | None = None
    t_outcome: str | None = None


def temporal_holdout_valid(
    t_claim: str | None,
    t_evidence: str | None,
    t_outcome: str | None,
) -> bool:
    """P1 A1.2 — is a predictive warrant leakage-free-scorable?

    A temporal holdout is only valid when the predicted OUTCOME is observable
    strictly AFTER the claim's full information set — i.e. ``t_outcome`` is
    strictly greater than both ``t_claim`` and ``t_evidence``. If the outcome
    falls at or before any part of the information the claim was made from, the
    "prediction" saw its own answer and the result is un-scorable (fail-closed).

    Requires ``t_outcome`` plus at least one of ``t_claim``/``t_evidence`` — a
    predictive warrant with no anchoring information time cannot be validated.
    ISO-8601 strings compare lexicographically iff same-length/zone; callers
    should pass normalized UTC ISO timestamps.
    """
    if t_outcome is None:
        return False
    info_times = [t for t in (t_claim, t_evidence) if t is not None]
    if not info_times:
        return False
    return all(t_outcome > t for t in info_times)


@dataclass(frozen=True, kw_only=True)
class DKSArgument(ArgumentNode):
    """Step 2 or 3 — a typed claim grounded in a warrant.

    Per D1 + FZ 2a2: subclass of :class:`ArgumentNode`; ``bb_type``
    fixed at ``BBType.ARGUMENT``. Cycle-specific fields:
    ``warrant`` (the Toulmin-typed standing reason), ``evidence``
    (citation back to the observation), and ``perspective``
    (the conservative vs exploratory vs skeptical angle the argument
    took). Default empty perspective for cycles that don't run
    multi-perspective debate.
    """

    warrant: DKSWarrant = field(default_factory=lambda: DKSWarrant(claim="", data="", warrant=""))
    evidence: str = ""
    perspective: str = ""


@dataclass(frozen=True)
class DKSContradicts:
    """Step 4 — disagreement edge.

    Materialized in the substrate as a link between the two argument
    notes; does NOT get its own FZ ID (it's a relation, not a node).
    ``attacker_fz`` and ``attacked_fz`` are the FZ IDs of the two
    arguments involved.
    """

    attacker_fz: str
    attacked_fz: str
    reason: str


@dataclass(frozen=True, kw_only=True)
class DKSCounterArgument(CounterArgumentNode):
    """Step 5 — names which Toulmin component is broken.

    Per D1 + FZ 2a2: subclass of :class:`CounterArgumentNode`;
    ``bb_type`` fixed at ``BBType.COUNTER_ARGUMENT``. Cycle-specific
    fields target the attacked argument's FZ + the broken Toulmin
    component + the strength of the attack. TESS-004 enforces the
    ``folgezettel_parent → argument`` link at the static layer; this
    dataclass captures the structured Toulmin failure mode.
    """

    attacked_fz: str = ""
    broken_component: ToulminComponent = "warrant"
    counter_claim: str = ""
    reason: str = ""
    strength: CounterStrength = "moderate"


@dataclass(frozen=True, kw_only=True)
class DKSPattern(ModelNode):
    """Step 6 — model aggregating contradictions into structural regularity.

    Per D1 + FZ 2a2: subclass of :class:`ModelNode`; ``bb_type``
    fixed at ``BBType.MODEL``. The realised corpus edge
    ``COUNTER_ARGUMENT → MODEL`` instantiates the schema edge
    ``pattern_of_failure`` (registered in ``BB_SCHEMA_DKS_EXTENSIONS``).
    """

    description: str = ""
    observed: tuple[str, ...] = ()


@dataclass(frozen=True)
class DKSRuleRevision:
    """Step 7 — revised warrant.

    Becomes a ``procedure`` or ``concept`` note at FZ ``<pattern_fz>.a``
    (the leaf of the cycle's 5-node subtree). ``supersedes`` is the FZ
    of the warrant this replaces; ``None`` if it's a wholly new rule.
    """

    folgezettel: str
    revised_warrant: DKSWarrant
    supersedes: str | None = None


# ── Cycle result ──────────────────────────────────────────────────────────


@dataclass(frozen=True)
class DKSCycleResult:
    """Output of one DKS cycle (full closed loop, short-circuited, or gated).

    Three terminal shapes:

    1. **Full closed loop** (``closed_loop=True``, ``escalation_decision="full"``)
       — observation + A + B + contradicts + counter + pattern + revision.
       6 FZ nodes deposited.
    2. **Short-circuited** (``closed_loop=False``, ``escalation_decision="full"``)
       — observation + A + B; arguments agreed so no contradiction, no
       counter, no pattern, no revision. 3 FZ nodes deposited.
    3. **Gated** (``closed_loop=False``, ``escalation_decision="gated"``)
       — observation + A only. The confidence model said existing
       warrants cover this observation; steps 2-7 short-circuited.
       2 FZ nodes deposited; ``argument_b`` is None.

    ``argument_b`` is therefore the load-bearing way to tell gated cycles
    apart from full ones: gated → ``None``; full or short-circuit →
    populated.
    """

    cycle_id: str
    mode: CycleMode
    observation: DKSObservation
    argument_a: DKSArgument
    argument_b: DKSArgument | None = None
    contradicts: DKSContradicts | None = None
    counter: DKSCounterArgument | None = None
    pattern: DKSPattern | None = None
    rule_revision: DKSRuleRevision | None = None
    elapsed_ms: float = 0.0
    backend_id: str = ""
    escalation_decision: str = "full"
    confidence_score: float | None = None
    # ── Multi-perspective debate ──────────────────────────────────────────
    arguments: tuple[DKSArgument, ...] = ()
    """All arguments produced by this cycle, in perspective order.
    For N=2 (default): ``(argument_a, argument_b)`` or ``(argument_a,)``
    when gated. For N>2: one entry per ``DKSCycle.perspectives`` value.
    Empty tuple when the caller did not provide a ``perspectives`` list."""

    contradicts_edges: tuple[DKSContradicts, ...] = ()
    """All pairwise contradicts edges between arguments. For N=2:
    either ``(contradicts,)`` when arguments disagree, or ``()`` when
    they agree. For N>2: every (i, j) pair where ``i < j`` and claims
    differ. Empty for gated cycles."""

    grounded_labelling: dict[str, str] = field(default_factory=dict)
    """**HISTORICAL** — the Dung grounded labelling as it stood at the end of
    THIS cycle, over this cycle's ``arguments`` only. Maps each argument's FZ to
    ``"in"`` / ``"out"`` / ``"undec"``.

    Retained because it is a public trace-JSON surface and because survival
    selection inside a cycle (which warrants to carry forward) is a decision
    about this cycle's arguments. But it is a FROZEN SNAPSHOT of a value that is
    not stable: an attack appended later can defeat one of these arguments, or
    defeat its attacker and reinstate it, and this dict will never say so. So it
    must not be read as a claim's status.

    The corpus-level verdict is COMPUTED, never frozen:
    :class:`tessellum.dks.status.StatusQuery` labels the whole claim/edge set on
    demand — over the ``attack`` relation only, with ``supersede`` as a
    pre-filter and ``support`` as a post-classification — and reports the four
    statuses (``proposed`` / ``challenged`` / ``warranted`` / ``superseded``).
    Ask that, not this, for "is this claim warranted now?"."""

    rule_revisions: tuple[DKSRuleRevision, ...] = ()
    """All :class:`DKSRuleRevision`s emitted by this cycle.

    For N=2 cycles + N>2 cycles with a single ``in`` survivor, this
    tuple has exactly one entry that mirrors the legacy
    ``rule_revision`` field. For N>2 cycles where Dung grounded
    labelling identifies multiple ``in`` survivors, the cycle emits
    one revision per survivor. Empty when the cycle did not reach
    step 7 (gated, short-circuited, or all-undec).

    The legacy ``rule_revision`` field is preserved + populated as
    ``rule_revisions[0] if rule_revisions else None``."""

    silent_failures: tuple[str, ...] = ()
    """Telemetry for backend calls inside the cycle that raised an
    exception but were silently fallen-back to preserve graceful
    degradation.

    Each entry is a one-line description of the form
    ``"<site_name>: <ExceptionType>: <message>"``. The cycle's
    semantics are unchanged — the silent fallback still happens — but
    callers (and meta-DKS via :class:`MetaObservation`) can now
    observe the rate at which it happens.

    The three known swallow sites in :class:`DKSCycle` are:

    - ``_llm_check_disagreement`` — backend raises during the
      semantic-disagreement step → falls back to string-compare.
    - ``_format_retrieval_context`` — retrieval client raises → falls
      back to empty context block.
    - ``_step_argument`` JSON parse — LLM returns unparseable JSON →
      ``_parse_json`` returns ``{}``, the step proceeds with empty
      data."""

    disagreement_diagnostics: tuple[str, ...] = ()
    """Why step 4 declined to emit an attack edge for a candidate pair.

    One line per candidate pair the evidence-based path (P4) did *not*
    turn into an edge: the incompatibility judge was unavailable, the
    two claims were adjudicated compatible, or they were incompatible
    but the evidence determined no direction. Also records when the
    per-cycle refutation budget truncated the candidate list.

    Empty on the legacy string-compare path — which never declines, and
    so never has anything to explain."""

    @property
    def folgezettel_nodes(self) -> tuple[str, ...]:
        """FZ positions this cycle deposited (excluding the edge).

        Covers all ``arguments`` (not just A/B) and all
        ``rule_revisions`` (not just the legacy ``rule_revision``
        field).
        """
        nodes: list[str] = [self.observation.folgezettel]
        if self.arguments:
            nodes.extend(a.folgezettel for a in self.arguments)
        else:
            # Legacy path for cycles constructed without `arguments`.
            nodes.append(self.argument_a.folgezettel)
            if self.argument_b is not None:
                nodes.append(self.argument_b.folgezettel)
        if self.counter:
            nodes.append(self.counter.folgezettel)
        if self.pattern:
            nodes.append(self.pattern.folgezettel)
        if self.rule_revisions:
            nodes.extend(r.folgezettel for r in self.rule_revisions)
        elif self.rule_revision:
            nodes.append(self.rule_revision.folgezettel)
        return tuple(nodes)

    @property
    def closed_loop(self) -> bool:
        """True iff step 7 fired (a revised warrant was produced)."""
        return self.rule_revision is not None

    @property
    def surviving_argument_fzs(self) -> tuple[str, ...]:
        """Folgezettel IDs of arguments labelled ``"in"`` under Dung
        grounded semantics.

        For N=2 cycles, this collapses to:

        - ``(argument_a.folgezettel, argument_b.folgezettel)`` when A
          and B agree (no contradicts edge); both arguments survive.
        - ``(argument_b.folgezettel,)`` when B attacks A (today's
          single-edge attack outcome).
        - Empty tuple when ``argument_b`` is ``None`` (gated path).

        For N>2 cycles, derived directly from
        :attr:`grounded_labelling`. Lex-sorted for stable iteration.

        Callers (e.g. ``DKSRunner`` warrant threading) use this to
        decide which warrants to carry forward when multiple
        arguments survive the dialectic — the multi-survivor case
        produced by the pairwise contradicts graph in N>2 cycles.

        Historical in the same sense as :attr:`grounded_labelling`: it
        answers "which of THIS cycle's arguments survived THIS cycle",
        not "which claims are warranted now". The latter is computed
        from the claim/edge log by :mod:`tessellum.dks.status`.
        """
        if self.grounded_labelling:
            return tuple(
                sorted(fz for fz, lbl in self.grounded_labelling.items() if lbl == "in")
            )
        # Pre-Phase-10 fallback for cycles constructed without the
        # additive fields. Mirrors the N=2 logic above.
        if self.argument_b is None:
            return ()
        if self.contradicts is None:
            return (self.argument_a.folgezettel, self.argument_b.folgezettel)
        return (self.argument_b.folgezettel,)

    @property
    def gated(self) -> bool:
        """True iff confidence gating skipped steps 2-7."""
        return self.escalation_decision == "gated"


# ── Folgezettel allocator ─────────────────────────────────────────────────


_TRAIL_ID_RE = re.compile(r"^(\d+)([a-z][a-z0-9]*)?$")


def allocate_cycle_fz(
    existing_trails: tuple[str, ...],
    mode: CycleMode = "fresh",
    parent_fz: str | None = None,
) -> str:
    """Allocate the cycle root FZ for a new DKS cycle.

    Per FZ 2a1, each cycle's root sits at one of three positions:

    - ``fresh``: the next unused top-level integer FZ.
    - ``extend``: descends from ``parent_fz`` (allocated as the next
      letter-suffix child of ``parent_fz``: ``a``, then ``b``, etc.).
    - ``branch``: same as ``extend`` but the caller's intent is to
      branch (insert a sibling counter at ``parent_fz``'s position).
      Mechanically identical to ``extend`` at the allocator layer; the
      distinction matters at the cycle-semantics layer.

    Args:
        existing_trails: All FZ IDs currently in the vault. Used to find
            the next unused position. Empty strings are ignored.
        mode: Allocation mode (see :data:`CycleMode`).
        parent_fz: Required for ``extend`` and ``branch``. The FZ of the
            node the new cycle descends from / branches off.

    Returns:
        The allocated FZ root ID for the new cycle.

    Raises:
        ValueError: if ``mode`` is ``extend``/``branch`` and ``parent_fz``
            is missing or empty.
    """
    if mode == "fresh":
        return _next_fresh_root(existing_trails)
    if parent_fz is None or not parent_fz:
        raise ValueError(
            f"mode={mode!r} requires parent_fz; got {parent_fz!r}"
        )
    return _next_child_of(parent_fz, existing_trails)


def _next_fresh_root(existing_trails: tuple[str, ...]) -> str:
    """Return the smallest unused integer (as string) at the top level."""
    used: set[int] = set()
    for fz in existing_trails:
        if not fz:
            continue
        m = _TRAIL_ID_RE.match(fz)
        if m:
            used.add(int(m.group(1)))
    n = 1
    while n in used:
        n += 1
    return str(n)


def _next_child_of(parent_fz: str, existing_trails: tuple[str, ...]) -> str:
    """Return the next child of ``parent_fz``, ALTERNATING digit/letter by depth.

    Tessellum's FZ convention alternates the component class at each level: a
    parent ending in a DIGIT gets a LETTER child (``1`` → ``1a``), and a parent
    ending in a LETTER gets a DIGIT child (``1a`` → ``1a1`` → ``1a1a`` …). The
    prior implementation always appended a letter (``1a`` → ``1aa``), which
    broke alternation and collided with sibling trails (release-blocker #1).

    A digit child counts from ``1`` (``…a`` → ``…a1``, ``…a2`` …); a letter
    child counts ``a``, ``b`` …, with a two-letter fallback after ``z``.
    Direct children are the existing trails whose next component (the maximal
    run of same-class chars immediately after ``parent_fz``) is of the expected
    class; we return the smallest unused value of that class.
    """
    parent_len = len(parent_fz)
    last_char = parent_fz[-1]
    want_digit = last_char.isalpha()  # letter parent → digit child; else letter

    if want_digit:
        used_digits: set[int] = set()
        for fz in existing_trails:
            if not fz or not fz.startswith(parent_fz) or len(fz) <= parent_len:
                continue
            # the child's leading digit run immediately after the parent
            rest = fz[parent_len:]
            if not rest[0].isdigit():
                continue
            run = ""
            for ch in rest:
                if ch.isdigit():
                    run += ch
                else:
                    break
            used_digits.add(int(run))
        n = 1
        while n in used_digits:
            n += 1
        return parent_fz + str(n)

    # want a letter child: collect the leading single-letter component of each
    # direct child (letters are single-char components in this convention).
    direct_letters: set[str] = set()
    for fz in existing_trails:
        if not fz or not fz.startswith(parent_fz) or len(fz) <= parent_len:
            continue
        next_char = fz[parent_len]
        if next_char.isalpha() and next_char.islower():
            direct_letters.add(next_char)
    for letter_code in range(ord("a"), ord("z") + 1):
        letter = chr(letter_code)
        if letter not in direct_letters:
            return parent_fz + letter
    # Exhausted a-z; fall back to a two-letter suffix.
    for letter_code1 in range(ord("a"), ord("z") + 1):
        for letter_code2 in range(ord("a"), ord("z") + 1):
            suffix = chr(letter_code1) + chr(letter_code2)
            if suffix not in direct_letters:
                return parent_fz + suffix
    raise RuntimeError(
        f"cannot allocate child FZ under {parent_fz!r}: 702 children exhausted"
    )


# ── Cycle dispatcher ──────────────────────────────────────────────────────


_SYSTEM_PROMPT = (
    "You are an analyst running one cycle of the Dialectic Knowledge "
    "System. Each step produces a single JSON object matching its "
    "schema. Return only the JSON; no prose, no code fences."
)


# ── Evidence-based incompatibility and direction ──────────────────────────
#
# Step 4 historically decided that two arguments disagreed by comparing
# their claim STRINGS, and decided which of them attacked which from the
# order the perspectives were generated in. Both inputs to the Dung
# solver were therefore manufactured: two differently worded claims about
# compatible facts always produced an attack edge, and the perspective
# generated second always won it, so the outcome was fixed before the
# solver ran.
#
# This section replaces both inputs with an INJECTED judgement over the
# arguments' evidence. Deciding whether two claims are incompatible, and
# which one the evidence defeats, is a judgement about meaning and so
# needs a model — but the seam is a Protocol, and a deterministic
# reference implementation (:class:`TableIncompatibilityJudge`) ships
# alongside the model-backed one for tests and for callers with no model.
# Three properties are load-bearing:
#
# 1. FAIL CLOSED. There is no string-compare fallback. When the judge is
#    unavailable, raises, or answers unparseably, NO attack edge is
#    emitted and the reason lands on
#    ``DKSCycleResult.disagreement_diagnostics``. Absence of adjudicated
#    evidence is not evidence of disagreement.
# 2. POSITION-FREE. Candidates are ranked by content, each pair is
#    canonicalised by content before the judge sees it, and the pairs are
#    adjudicated in content order — so the edge set does not depend on
#    the order the perspectives were listed in.
# 3. BOUNDED MODEL COST. The judge runs against candidate attackers
#    surfaced for the derived claim, capped per claim
#    (``max_attack_candidates``) and per cycle (``refutation_budget``) —
#    never once per pair in the reached set.
#
# The section is deliberately free of cycle state so it can be lifted
# into its own module when ``dks/core.py`` is broken up.


DEFAULT_MAX_ATTACK_CANDIDATES: int = 4
"""Candidate attackers surfaced per derived claim before adjudication.

The ranker returns at most this many candidates for one claim, so the
judge is asked about plausible refutations rather than about every other
argument in the reached set."""

DEFAULT_REFUTATION_BUDGET: int = 8
"""Hard cap on incompatibility judgements per cycle.

The per-claim cap alone still grows with the number of arguments; this is
the cap that makes the per-cycle model budget a constant. Candidate pairs
beyond the budget are left unadjudicated (and therefore edge-less), with
the truncation recorded in
:attr:`DKSCycleResult.disagreement_diagnostics`."""


AttackDirection = Literal["a_attacks_b", "b_attacks_a", "undetermined"]
"""Which way the evidence points in an adjudicated incompatibility.

``a_attacks_b`` / ``b_attacks_a`` name the two arguments in the order
they were handed to the judge. ``undetermined`` means the evidence
establishes that the two claims cannot both hold but does *not* establish
which one it defeats — in which case the cycle emits no edge rather than
inventing a direction.
"""


@dataclass(frozen=True)
class IncompatibilityVerdict:
    """One adjudicated candidate disagreement.

    ``incompatible=False`` is the fail-closed answer, and the one the
    old string comparison could never give: differently worded claims
    about compatible facts are not a disagreement.

    ``rationale`` and ``evidence_locator`` are what make the resulting
    edge auditable — they carry the *reason* the pair was adjudicated
    this way into :attr:`DKSContradicts.reason`, where a bare "claim
    mismatch" used to sit.
    """

    incompatible: bool
    direction: AttackDirection = "undetermined"
    rationale: str = ""
    evidence_locator: str = ""


def _flipped(verdict: IncompatibilityVerdict) -> IncompatibilityVerdict:
    """The same verdict with its two sides swapped."""
    if verdict.direction == "a_attacks_b":
        direction: AttackDirection = "b_attacks_a"
    elif verdict.direction == "b_attacks_a":
        direction = "a_attacks_b"
    else:
        direction = "undetermined"
    return IncompatibilityVerdict(
        incompatible=verdict.incompatible,
        direction=direction,
        rationale=verdict.rationale,
        evidence_locator=verdict.evidence_locator,
    )


class IncompatibilityJudge(Protocol):
    """Decide whether two arguments' claims are incompatible, and which
    way the evidence points.

    Called with the two whole :class:`DKSArgument`s rather than their
    claim strings, because the judgement is over the *evidence*: the
    Toulmin warrant licensing each claim and the quoted source span each
    cites.

    Returns ``None`` for "no judgement available" — a backend error, an
    unparseable answer, a pair outside the judge's competence. The caller
    treats ``None`` as *no attack edge* and records why; it must never
    fall back to comparing claim strings, since that fallback is what
    made every pair disagree.
    """

    def __call__(
        self, a: DKSArgument, b: DKSArgument
    ) -> IncompatibilityVerdict | None:
        ...


@dataclass(frozen=True)
class TableIncompatibilityJudge:
    """Deterministic reference judge — an explicit table of adjudications.

    Keyed by the ordered pair of claim texts. A lookup that matches only
    the reversed pair returns the stored verdict with its two sides
    swapped, so the judge is symmetric by construction. Pairs absent from
    the table are reported COMPATIBLE: the reference implementation holds
    the same fail-closed bias as the model-backed one and can never
    manufacture a disagreement nobody wrote down.

    This is what tests inject, and what a caller runs when no model is
    available.
    """

    verdicts: Mapping[tuple[str, str], IncompatibilityVerdict] = field(
        default_factory=dict
    )

    def __call__(
        self, a: DKSArgument, b: DKSArgument
    ) -> IncompatibilityVerdict | None:
        claim_a = a.warrant.claim.strip()
        claim_b = b.warrant.claim.strip()
        direct = self.verdicts.get((claim_a, claim_b))
        if direct is not None:
            return direct
        reverse = self.verdicts.get((claim_b, claim_a))
        if reverse is not None:
            return _flipped(reverse)
        return IncompatibilityVerdict(
            incompatible=False,
            rationale=(
                "no adjudicated evidence for this claim pair; "
                "reported compatible"
            ),
        )


_INCOMPATIBILITY_PROMPT = (
    "Step: evidence-based incompatibility check.\n"
    "Decide (1) whether the two claims below can both hold at once and "
    "(2) if they cannot, which one the cited evidence defeats. Claims that "
    "are merely worded differently are NOT a disagreement. Judge the "
    "evidence, not the phrasing, and answer 'undetermined' rather than "
    "guessing a direction the evidence does not establish.\n\n"
    "Claim A: {claim_a}\n"
    "A's warrant: {warrant_a}\n"
    "A's evidence: {evidence_a}\n\n"
    "Claim B: {claim_b}\n"
    "B's warrant: {warrant_b}\n"
    "B's evidence: {evidence_b}\n\n"
    'Return JSON:\n{{"incompatible": true|false, "direction": '
    '"a_attacks_b|b_attacks_a|undetermined", "rationale": "...", '
    '"evidence_locator": "<the span that settles it, or empty>"}}'
)


@dataclass(frozen=True)
class LLMIncompatibilityJudge:
    """Model-backed judge — one backend call per candidate pair.

    The model *produces the evidence* for the judgement; what to do with
    it stays with the cycle. On a backend exception, an unparseable
    response, or a missing ``incompatible`` field this returns ``None``
    and the caller emits no edge. An out-of-vocabulary ``direction``
    degrades to ``undetermined``, which also emits no edge — a
    hallucinated direction must not become an attack.
    """

    backend: LLMBackend
    system_prompt: str = _SYSTEM_PROMPT

    def __call__(
        self, a: DKSArgument, b: DKSArgument
    ) -> IncompatibilityVerdict | None:
        prompt = _INCOMPATIBILITY_PROMPT.format(
            claim_a=a.warrant.claim,
            warrant_a=a.warrant.warrant,
            evidence_a=a.evidence,
            claim_b=b.warrant.claim,
            warrant_b=b.warrant.warrant,
            evidence_b=b.evidence,
        )
        try:
            response = self.backend.call(
                LLMRequest(
                    system_prompt=self.system_prompt, user_prompt=prompt
                )
            )
        except Exception:  # noqa: BLE001 — an unavailable judge fails closed, it does not raise into the cycle
            return None
        data = _parse_json(response.content)
        if "incompatible" not in data:
            return None
        incompatible = _coerce_bool(data["incompatible"])
        if incompatible is None:
            return None
        raw_direction = str(data.get("direction", "undetermined")).strip().lower()
        direction: AttackDirection = (
            raw_direction  # type: ignore[assignment]
            if raw_direction in ("a_attacks_b", "b_attacks_a", "undetermined")
            else "undetermined"
        )
        return IncompatibilityVerdict(
            incompatible=incompatible,
            direction=direction,
            rationale=_get_str(data, "rationale"),
            evidence_locator=_get_str(data, "evidence_locator", ""),
        )


class CandidateAttackerRanker(Protocol):
    """Surface the candidate attackers of one derived claim.

    This is what bounds the model budget: the incompatibility judge runs
    against the candidates this returns, never against every pair in the
    reached set. Implementations must rank by CONTENT, so the candidate
    set does not depend on the order the arguments were generated in.
    """

    def __call__(
        self, claim: str, candidates: Sequence[DKSArgument], *, k: int
    ) -> tuple[DKSArgument, ...]:
        ...


@dataclass(frozen=True)
class LexicalOverlapRanker:
    """Deterministic, model-free candidate surfacing — token overlap.

    Scores each candidate by Jaccard overlap between its claim's token
    set and the derived claim's, descending, with the candidate's content
    key as tiebreak. Nothing is dropped for a low score: the caps are the
    only thing that drops a candidate, so the recall loss is explicit and
    budgeted rather than hidden in a threshold.

    This stands in for the retrieval ranker later phases wire in (dense +
    lexical against the derived claim). The interface is the same, so
    swapping it does not touch the cycle.
    """

    def __call__(
        self, claim: str, candidates: Sequence[DKSArgument], *, k: int
    ) -> tuple[DKSArgument, ...]:
        if k <= 0:
            return ()
        target = _claim_tokens(claim)
        ranked = sorted(
            candidates,
            key=lambda c: (
                -_jaccard(target, _claim_tokens(c.warrant.claim)),
                _argument_content_key(c),
            ),
        )
        return tuple(ranked[:k])


def _claim_tokens(text: str) -> frozenset[str]:
    """Lowercased alphanumeric token set of a claim."""
    return frozenset(t for t in re.split(r"[^0-9a-z]+", text.lower()) if t)


def _jaccard(left: frozenset[str], right: frozenset[str]) -> float:
    """Jaccard overlap; 0.0 when either side is empty."""
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _argument_content_key(arg: DKSArgument) -> tuple[str, str, str, str]:
    """A stable identity for an argument that does not use its position.

    Content first, then the perspective label as a tiebreak — the
    perspective is unique per cycle (the constructor enforces it) and
    independent of where in the list it was declared, so this key is
    invariant under permutation of ``perspectives`` while still telling
    two same-content arguments apart.
    """
    return (
        arg.warrant.claim.strip(),
        arg.warrant.warrant.strip(),
        arg.evidence.strip(),
        arg.perspective,
    )


def _canonical_pair(
    x: DKSArgument, y: DKSArgument
) -> tuple[DKSArgument, DKSArgument]:
    """Order two arguments by content so the judge sees one fixed
    presentation of the pair regardless of generation order."""
    return (
        (x, y) if _argument_content_key(x) <= _argument_content_key(y) else (y, x)
    )


class DKSCycle:
    """One DKS cycle (full closed loop, short-circuited, or confidence-gated).

    Constructed with an observation + the current warrant set + a
    backend, plus an optional confidence model. ``run()`` decides
    which terminal shape applies:

    - **gated**: if a confidence model returns a score *above* the
      threshold, the cycle short-circuits to *observation + argument
      A* and does not run steps 3-7. ``escalation_decision="gated"``.
    - **short-circuited**: A and B agree → no contradicts, no steps
      5-7. ``escalation_decision="full"``, ``closed_loop=False``.
    - **full closed loop**: A and B disagree → full 7-component
      cycle. ``escalation_decision="full"``, ``closed_loop=True``.

    Confidence gating is opt-in. Callers who don't pass
    ``confidence_model`` always run the full cycle.

    Step 4's *inputs* are opt-in too. By default "A and B disagree" means
    their claim strings differ and the attacker is whichever argument was
    generated second. Pass ``evidence_based_disagreement=True`` (or an
    explicit ``incompatibility_judge``) to decide both questions from the
    arguments' evidence instead, under an explicit per-cycle cap on
    judgements — see the "Evidence-based incompatibility and direction"
    section above.
    """

    def __init__(
        self,
        observation: DKSObservation,
        warrants: tuple[DKSWarrant, ...],
        backend: LLMBackend,
        *,
        confidence_model: object | None = None,
        confidence_threshold: float | None = None,
        retrieval_client: object | None = None,
        semantic_disagreement: bool = False,
        evidence_based_disagreement: bool = False,
        incompatibility_judge: IncompatibilityJudge | None = None,
        candidate_ranker: CandidateAttackerRanker | None = None,
        max_attack_candidates: int = DEFAULT_MAX_ATTACK_CANDIDATES,
        refutation_budget: int = DEFAULT_REFUTATION_BUDGET,
        perspectives: tuple[str, ...] = ("conservative", "exploratory"),
        mode: CycleMode = "fresh",
    ) -> None:
        self.observation = observation
        self.warrants = warrants
        self.backend = backend
        # A0.1 — the requested allocation mode (fresh/extend/branch) must
        # round-trip into DKSCycleResult.mode + the trace. Previously every
        # return site hard-coded "fresh", so extend/branch were lost
        # (release-blocker #2).
        self.mode: CycleMode = mode
        self.confidence_model = confidence_model
        # The default threshold lives in tessellum.dks.confidence; we
        # import lazily here to avoid a circular import at module load
        # (confidence.py depends on DKSObservation/DKSWarrant from this
        # module). The default is materialised on first call to .run().
        self.confidence_threshold = confidence_threshold
        # Retrieval-grounded argument step. When supplied, the
        # argument-generation prompts get a "Related material from the
        # substrate" block populated by
        # retrieval_client.search(observation.summary).
        self.retrieval_client = retrieval_client
        # Optional LLM-based disagreement detection at step 4. Off by
        # default falls back to local string-compare on claim text.
        self.semantic_disagreement = semantic_disagreement
        # Evidence-based incompatibility + direction at step 4. DEFAULT
        # OFF: with neither the flag nor a judge, step 4 runs the legacy
        # string-compare path and the N>2 builder keeps its
        # attacker-is-the-later-perspective convention, so existing
        # callers and traces are unchanged. Supplying a judge implies the
        # flag (a judge that silently did nothing would be a trap);
        # setting the flag alone builds an LLMIncompatibilityJudge over
        # this cycle's backend. When on, it takes precedence over
        # ``semantic_disagreement`` — the two answer the same question,
        # and only one of them weighs evidence.
        if max_attack_candidates < 0:
            raise ValueError(
                f"max_attack_candidates must be >= 0; got {max_attack_candidates}"
            )
        if refutation_budget < 0:
            raise ValueError(
                f"refutation_budget must be >= 0; got {refutation_budget}"
            )
        self.evidence_based_disagreement: bool = bool(
            evidence_based_disagreement
        ) or (incompatibility_judge is not None)
        self.max_attack_candidates = max_attack_candidates
        self.refutation_budget = refutation_budget
        self.candidate_ranker: CandidateAttackerRanker = (
            candidate_ranker if candidate_ranker is not None else LexicalOverlapRanker()
        )
        self.incompatibility_judge: IncompatibilityJudge | None = None
        if self.evidence_based_disagreement:
            self.incompatibility_judge = (
                incompatibility_judge
                if incompatibility_judge is not None
                else LLMIncompatibilityJudge(backend=backend)
            )
        # Why step 4 declined a candidate pair. Surfaced on
        # DKSCycleResult.disagreement_diagnostics.
        self._disagreement_diagnostics: list[str] = []
        # Multi-perspective debate. The default ("conservative",
        # "exploratory") matches the canonical 2-argument cycle. N>2
        # activates pairwise contradicts + Dung grounded labelling.
        if len(perspectives) < 2:
            raise ValueError(
                f"perspectives must have at least 2 entries; got {perspectives!r}"
            )
        if len(set(perspectives)) != len(perspectives):
            raise ValueError(
                f"perspectives must be unique; got {perspectives!r}"
            )
        self.perspectives: tuple[str, ...] = perspectives
        # FZ allocator state — children of the cycle root
        self._cycle_fz_existing: list[str] = [observation.folgezettel]
        # Silent-failure telemetry. Each swallow site appends a
        # one-line description before falling back. Surfaced on
        # DKSCycleResult.silent_failures.
        self._silent_failures: list[str] = []

    def _parse_json_or_record(self, content: str, site_name: str) -> dict:
        """Wrapper around :func:`_parse_json` that records a silent
        failure when content is non-empty but parses to ``{}``.
        Preserves the historical swallow semantics —
        the empty-dict fallback still happens — but makes the
        silence observable via ``DKSCycleResult.silent_failures``.
        """
        result = _parse_json(content)
        if not result and content.strip():
            self._silent_failures.append(
                f"{site_name}: JSONDecodeError: content not parseable to dict "
                f"(first 80 chars: {content[:80]!r})"
            )
        return result

    def run(self) -> DKSCycleResult:
        start = time.monotonic()
        cycle_id = self.observation.folgezettel
        backend_id = getattr(self.backend, "backend_id", "")

        # Confidence gating (opt-in). Compute the gate decision before
        # any LLM call; the gated path saves 6 of the 7 backend
        # round-trips when it fires.
        confidence_score: float | None = None
        gated = False
        if self.confidence_model is not None:
            from tessellum.dks.confidence import (
                DEFAULT_CONFIDENCE_THRESHOLD,
                decide_escalation,
            )

            threshold = (
                self.confidence_threshold
                if self.confidence_threshold is not None
                else DEFAULT_CONFIDENCE_THRESHOLD
            )
            confidence_score = float(
                self.confidence_model(self.observation, self.warrants)
            )
            gated = decide_escalation(confidence_score, threshold) == "gated"

        # Step 2: argument A (always runs — every cycle deposits at
        # least observation + A, whether gated or full).
        arg_a = self._step_argument(
            perspective=self.perspectives[0], suffix_hint="a"
        )

        if gated:
            # Skip steps 3-7. Cycle deposits 2 FZ nodes (observation + A).
            return DKSCycleResult(
                cycle_id=cycle_id,
                mode=self.mode,
                observation=self.observation,
                argument_a=arg_a,
                argument_b=None,
                contradicts=None,
                counter=None,
                pattern=None,
                rule_revision=None,
                elapsed_ms=(time.monotonic() - start) * 1000.0,
                backend_id=backend_id,
                escalation_decision="gated",
                confidence_score=confidence_score,
                arguments=(arg_a,),
                contradicts_edges=(),
                grounded_labelling={},
                silent_failures=tuple(self._silent_failures),
            )

        # Step 3: argument B from a different angle.
        arg_b = self._step_argument(
            perspective=self.perspectives[1], suffix_hint="b"
        )

        # N>2 dispatch. When the cycle was constructed with more than
        # two perspectives, generate the additional arguments, compute
        # pairwise contradicts + grounded labelling, and identify the
        # attacked argument(s). For N=2 the existing path runs.
        if len(self.perspectives) > 2:
            return self._run_n_perspective(
                cycle_id=cycle_id,
                start=start,
                backend_id=backend_id,
                confidence_score=confidence_score,
                arg_a=arg_a,
                arg_b=arg_b,
            )

        # Step 4: disagreement detection (local, not an LLM call)
        contradicts = self._step_disagreement(arg_a, arg_b)

        # Short-circuit if A and B agree
        if contradicts is None:
            return DKSCycleResult(
                cycle_id=cycle_id,
                mode=self.mode,
                observation=self.observation,
                argument_a=arg_a,
                argument_b=arg_b,
                contradicts=None,
                counter=None,
                pattern=None,
                rule_revision=None,
                elapsed_ms=(time.monotonic() - start) * 1000.0,
                backend_id=backend_id,
                escalation_decision="full",
                confidence_score=confidence_score,
                arguments=(arg_a, arg_b),
                contradicts_edges=(),
                grounded_labelling={},
                silent_failures=tuple(self._silent_failures),
                disagreement_diagnostics=tuple(self._disagreement_diagnostics),
            )

        # A0.4 — Dung-IN must be COMPUTED by the solver, not asserted. Build a
        # DungAF over the two arguments with the attack edge derived from the
        # contradicts relation (attacker_fz attacks attacked_fz) and let the
        # grounded labelling decide which argument is `in`/`out`/`undec`. This
        # is the same solver the N>2 path uses; the hard-coded {A:out, B:in}
        # made P4's validation meaningless (release-blocker #5, mechanics half).
        from tessellum.dks.dung import DungAF, grounded_labelling

        n2_af = DungAF(
            arguments=(arg_a.folgezettel, arg_b.folgezettel),
            attacks=((contradicts.attacker_fz, contradicts.attacked_fz),),
        )
        n2_labels = grounded_labelling(n2_af)

        # Step 5: counter-argument naming the broken Toulmin component
        counter = self._step_counter(contradicts, arg_a, arg_b)
        # Step 6: pattern discovery aggregating the contradiction
        pattern = self._step_pattern(counter)
        # Step 7: rule revision closing the loop
        revision = self._step_rule_revision(pattern)

        return DKSCycleResult(
            cycle_id=cycle_id,
            mode=self.mode,
            observation=self.observation,
            argument_a=arg_a,
            argument_b=arg_b,
            contradicts=contradicts,
            counter=counter,
            pattern=pattern,
            rule_revision=revision,
            elapsed_ms=(time.monotonic() - start) * 1000.0,
            backend_id=backend_id,
            escalation_decision="full",
            confidence_score=confidence_score,
            arguments=(arg_a, arg_b),
            contradicts_edges=(contradicts,),
            grounded_labelling=dict(n2_labels),
            rule_revisions=(revision,),
            silent_failures=tuple(self._silent_failures),
            disagreement_diagnostics=tuple(self._disagreement_diagnostics),
        )

    # ── N>2 perspective dispatch ────────────────────────────────────────

    _SUFFIX_ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    def _run_n_perspective(
        self,
        *,
        cycle_id: str,
        start: float,
        backend_id: str,
        confidence_score: float | None,
        arg_a: DKSArgument,
        arg_b: DKSArgument,
    ) -> DKSCycleResult:
        """N>2 path: generate remaining arguments, compute pairwise
        contradicts edges, derive Dung grounded labelling, then route
        steps 5-7 through the attacked argument (if any survives the
        grounded labelling as ``out``).
        """
        from tessellum.dks.dung import DungAF, grounded_labelling

        arguments: list[DKSArgument] = [arg_a, arg_b]
        for i, persp in enumerate(self.perspectives[2:], start=2):
            if i >= len(self._SUFFIX_ALPHABET):
                # Defensive — alphabet runs out at 26 perspectives. Bail.
                break
            arg = self._step_argument(
                perspective=persp, suffix_hint=self._SUFFIX_ALPHABET[i]
            )
            arguments.append(arg)

        # Pairwise step 4. Evidence-based when opted in (the same builder
        # the N=2 path uses, so the two cannot drift apart again);
        # otherwise the legacy index-order convention.
        contradicts_edges: list[DKSContradicts] = list(
            self._build_attack_edges(arguments)
            if self.evidence_based_disagreement
            else self._build_attack_edges_by_order(arguments)
        )

        # Build Dung AF + compute grounded labelling.
        af = DungAF(
            arguments=tuple(a.folgezettel for a in arguments),
            attacks=tuple(
                (e.attacker_fz, e.attacked_fz) for e in contradicts_edges
            ),
        )
        labels = grounded_labelling(af)

        # Find the attacked argument: the (lex-smallest) one labelled "out".
        # When no labels are "out" (all agree or all undec), short-circuit
        # without steps 5-7.
        out_fzs = sorted(fz for fz, lbl in labels.items() if lbl == "out")
        if not out_fzs:
            return DKSCycleResult(
                cycle_id=cycle_id,
                mode=self.mode,
                observation=self.observation,
                argument_a=arg_a,
                argument_b=arg_b,
                contradicts=None,
                counter=None,
                pattern=None,
                rule_revision=None,
                elapsed_ms=(time.monotonic() - start) * 1000.0,
                backend_id=backend_id,
                escalation_decision="full",
                confidence_score=confidence_score,
                arguments=tuple(arguments),
                contradicts_edges=tuple(contradicts_edges),
                grounded_labelling=dict(labels),
                silent_failures=tuple(self._silent_failures),
                disagreement_diagnostics=tuple(self._disagreement_diagnostics),
            )

        attacked_fz = out_fzs[0]
        attacked = next(a for a in arguments if a.folgezettel == attacked_fz)
        # Pick the (lex-smallest) attacker on that proposal.
        attacker_fz = sorted(
            e.attacker_fz
            for e in contradicts_edges
            if e.attacked_fz == attacked_fz
        )[0]
        attacker = next(a for a in arguments if a.folgezettel == attacker_fz)
        primary_contradicts = next(
            e
            for e in contradicts_edges
            if e.attacked_fz == attacked_fz and e.attacker_fz == attacker_fz
        )

        counter = self._step_counter(primary_contradicts, attacked, attacker)
        pattern = self._step_pattern(counter)

        # Multi-revision authoring. When grounded labelling identifies
        # multiple ``in`` survivors, emit one DKSRuleRevision per
        # survivor. Each revision uses an independent LLM call so the
        # revised warrants can differ (the surviving warrants are
        # themselves distinct; revisions building from each should be
        # distinct too).
        in_fzs = sorted(fz for fz, lbl in labels.items() if lbl == "in")
        revisions: list[DKSRuleRevision] = []
        if len(in_fzs) <= 1:
            # Single survivor (or none) — preserve N=2 semantics:
            # one revision, derived from the pattern alone.
            revisions.append(self._step_rule_revision(pattern))
        else:
            # Multi-survivor: one revision per surviving argument.
            # The pattern is shared; the surviving warrant's claim
            # threads into each prompt as additional context.
            survivors = [
                next(a for a in arguments if a.folgezettel == fz)
                for fz in in_fzs
            ]
            for survivor in survivors:
                revisions.append(
                    self._step_rule_revision(
                        pattern, surviving_argument=survivor
                    )
                )

        return DKSCycleResult(
            cycle_id=cycle_id,
            mode=self.mode,
            observation=self.observation,
            argument_a=arg_a,
            argument_b=arg_b,
            contradicts=primary_contradicts,
            counter=counter,
            pattern=pattern,
            rule_revision=revisions[0],
            elapsed_ms=(time.monotonic() - start) * 1000.0,
            backend_id=backend_id,
            escalation_decision="full",
            confidence_score=confidence_score,
            arguments=tuple(arguments),
            contradicts_edges=tuple(contradicts_edges),
            grounded_labelling=dict(labels),
            rule_revisions=tuple(revisions),
            silent_failures=tuple(self._silent_failures),
            disagreement_diagnostics=tuple(self._disagreement_diagnostics),
        )

    # ── Per-step methods ──────────────────────────────────────────────────

    def _step_argument(
        self, perspective: str, suffix_hint: str
    ) -> DKSArgument:
        """Step 2 / step 3 — produce one argument from the warrant set.

        Retrieval enrichment: when a ``retrieval_client`` is wired
        into the cycle, the prompt gains a "Related material from the
        substrate" block populated by hybrid-search hits against the
        observation summary. The warrant set still flows through
        unchanged — retrieval *augments* the prompt's substrate
        awareness; it does not replace warrants.
        """
        warrants_block = self._format_warrants()
        retrieval_block = self._format_retrieval_context()
        prompt = (
            f"Step: generate argument ({perspective}).\n"
            f"Observation: {self.observation.summary}\n\n"
            f"Available warrants:\n{warrants_block}\n\n"
            f"{retrieval_block}"
            f"Produce one argument from a {perspective} angle. Return JSON:\n"
            f'{{"claim": "...", "data": "...", "warrant": "...", '
            f'"backing": "...", "qualifier": "...", "evidence": "..."}}'
        )
        response = self.backend.call(
            LLMRequest(system_prompt=_SYSTEM_PROMPT, user_prompt=prompt)
        )
        data = self._parse_json_or_record(response.content, "_step_argument")
        fz = self.observation.folgezettel + suffix_hint
        self._cycle_fz_existing.append(fz)
        return DKSArgument(
            folgezettel=fz,
            warrant=DKSWarrant(
                claim=_get_str(data, "claim"),
                data=_get_str(data, "data"),
                warrant=_get_str(data, "warrant"),
                backing=_get_str(data, "backing", ""),
                qualifier=_get_str(data, "qualifier", ""),
            ),
            evidence=_get_str(data, "evidence"),
            # Record the perspective string on every DKSArgument.
            # Surfaces in cycle traces and MetaObservation
            # per-perspective stratification.
            perspective=perspective,
        )

    def _step_disagreement(
        self, arg_a: DKSArgument, arg_b: DKSArgument
    ) -> DKSContradicts | None:
        """Step 4 — detect contradiction between A and B.

        Two paths:

        - **Evidence-based** (opt-in via ``evidence_based_disagreement``
          or an explicit ``incompatibility_judge``): the pair is
          adjudicated by :meth:`_build_attack_edges` — the same builder
          the N>2 path uses — so an edge appears only when the judge
          finds the claims incompatible *and* the evidence names a
          direction.
        - **Legacy** (default): string-inequality on the claim text, or,
          with ``semantic_disagreement=True``, one backend call that
          falls back to string-compare on parse failure. The direction is
          then fixed by prompt-slot order: B attacks A because B was
          generated second. Retained unchanged so existing callers and
          traces keep working; it treats any difference in wording as a
          disagreement, which is what the evidence-based path exists to
          replace.
        """
        if self.evidence_based_disagreement:
            edges = self._build_attack_edges((arg_a, arg_b))
            return edges[0] if edges else None

        a_claim = arg_a.warrant.claim.strip()
        b_claim = arg_b.warrant.claim.strip()

        if self.semantic_disagreement:
            disagree = self._llm_check_disagreement(a_claim, b_claim)
            if disagree is None:
                # Fall back to string compare on parse failure
                disagree = a_claim != b_claim
        else:
            disagree = a_claim != b_claim

        if not disagree:
            return None
        # Legacy direction: B attacks A because B is the second prompt
        # slot, not because the evidence says so.
        return DKSContradicts(
            attacker_fz=arg_b.folgezettel,
            attacked_fz=arg_a.folgezettel,
            reason=(
                f"Claim mismatch: A asserts {arg_a.warrant.claim!r}; "
                f"B asserts {arg_b.warrant.claim!r}"
            ),
        )

    # ── Step 4, evidence-based (P4) ───────────────────────────────────────

    def _build_attack_edges(
        self, arguments: Sequence[DKSArgument]
    ) -> tuple[DKSContradicts, ...]:
        """Derive step 4's attack edges from evidence, for any N.

        One implementation behind both the N=2 and the N>2 path, so the
        two cannot diverge again. Four stages, none of which consults an
        argument's position:

        1. **Surface** candidate attackers for each derived claim through
           :attr:`candidate_ranker`, capped at
           :attr:`max_attack_candidates`. The judge is never asked about
           every pair in the reached set.
        2. **Canonicalise** each candidate pair by content and
           de-duplicate it, then adjudicate the pairs in content order,
           truncated to :attr:`refutation_budget` — the per-cycle cap on
           model calls.
        3. **Adjudicate.** An unavailable judge, a compatible pair, and an
           incompatible pair whose direction the evidence leaves open all
           yield no edge, each with a recorded reason.
        4. **Emit** one edge per adjudicated, directed incompatibility,
           in the same content order.

        Returns an empty tuple when no judge is configured — the caller
        only reaches this method with the feature opted in, so that case
        is a defensive fail-closed, not a fallback.
        """
        judge = self.incompatibility_judge
        if judge is None:
            return ()

        # Stage 1 + 2: content-keyed candidate pairs, de-duplicated.
        pairs: dict[
            tuple[tuple[str, ...], tuple[str, ...]],
            tuple[DKSArgument, DKSArgument],
        ] = {}
        for arg in arguments:
            others = [other for other in arguments if other is not arg]
            candidates = self.candidate_ranker(
                arg.warrant.claim, others, k=self.max_attack_candidates
            )
            for candidate in candidates:
                first, second = _canonical_pair(arg, candidate)
                key = (
                    _argument_content_key(first),
                    _argument_content_key(second),
                )
                pairs[key] = (first, second)

        ordered = [pairs[key] for key in sorted(pairs)]
        if len(ordered) > self.refutation_budget:
            self._disagreement_diagnostics.append(
                f"refutation budget {self.refutation_budget} reached: "
                f"{len(ordered) - self.refutation_budget} candidate pair(s) "
                f"left unadjudicated"
            )
            ordered = ordered[: self.refutation_budget]

        # Stage 3 + 4.
        edges: list[DKSContradicts] = []
        for first, second in ordered:
            edge = self._adjudicate_pair(judge, first, second)
            if edge is not None:
                edges.append(edge)
        return tuple(edges)

    def _adjudicate_pair(
        self,
        judge: IncompatibilityJudge,
        first: DKSArgument,
        second: DKSArgument,
    ) -> DKSContradicts | None:
        """Ask the judge about one canonically-ordered pair.

        Returns the attack edge the evidence licenses, or ``None`` —
        recording why on :attr:`_disagreement_diagnostics` in every
        ``None`` case, so "no disagreement" is auditable rather than
        silent. There is no string-compare fallback on any branch.
        """
        label = f"{first.folgezettel} vs {second.folgezettel}"
        try:
            verdict = judge(first, second)
        except Exception as e:  # noqa: BLE001 — a raising judge fails closed, like an absent one
            self._silent_failures.append(
                f"_adjudicate_pair: {type(e).__name__}: {e}"
            )
            self._disagreement_diagnostics.append(
                f"{label}: judge raised {type(e).__name__} — no attack edge"
            )
            return None
        if verdict is None:
            self._disagreement_diagnostics.append(
                f"{label}: no judgement available — no attack edge"
            )
            return None
        why = verdict.rationale or "no rationale given"
        if not verdict.incompatible:
            self._disagreement_diagnostics.append(
                f"{label}: claims are compatible — no attack edge ({why})"
            )
            return None
        if verdict.direction == "undetermined":
            self._disagreement_diagnostics.append(
                f"{label}: incompatible, but the evidence determines no "
                f"direction — no attack edge ({why})"
            )
            return None
        if verdict.direction == "a_attacks_b":
            attacker, attacked = first, second
        else:
            attacker, attacked = second, first
        locator = (
            f" [locator: {verdict.evidence_locator}]"
            if verdict.evidence_locator
            else ""
        )
        return DKSContradicts(
            attacker_fz=attacker.folgezettel,
            attacked_fz=attacked.folgezettel,
            reason=(
                f"Evidence-based incompatibility: {attacker.folgezettel} "
                f"asserts {attacker.warrant.claim!r} against "
                f"{attacked.folgezettel}'s {attacked.warrant.claim!r}; "
                f"{why}{locator}"
            ),
        )

    def _build_attack_edges_by_order(
        self, arguments: Sequence[DKSArgument]
    ) -> tuple[DKSContradicts, ...]:
        """Legacy N>2 step 4 — one edge per (i, j), i < j, whose claim
        strings differ, with the later perspective named the attacker.

        Kept as the default so existing callers and traces are unchanged.
        It weighs no evidence: the trigger is claim-string identity and
        the direction is list position, so permuting ``perspectives``
        permutes the verdict. :meth:`_build_attack_edges` is the
        evidence-based replacement.
        """
        edges: list[DKSContradicts] = []
        for i in range(len(arguments)):
            for j in range(i + 1, len(arguments)):
                a_i = arguments[i]
                a_j = arguments[j]
                if a_i.warrant.claim.strip() == a_j.warrant.claim.strip():
                    continue
                edges.append(
                    DKSContradicts(
                        attacker_fz=a_j.folgezettel,
                        attacked_fz=a_i.folgezettel,
                        reason=(
                            f"Claim mismatch: {a_i.folgezettel} asserts "
                            f"{a_i.warrant.claim!r}; "
                            f"{a_j.folgezettel} asserts {a_j.warrant.claim!r}"
                        ),
                    )
                )
        return tuple(edges)

    def _llm_check_disagreement(self, claim_a: str, claim_b: str) -> bool | None:
        """LLM-based disagreement check.

        Returns True if the claims substantively disagree, False if
        they're equivalent, None on parse failure (caller falls back
        to string-compare).
        """
        prompt = (
            "Step: semantic disagreement check.\n"
            f"Claim A: {claim_a}\n"
            f"Claim B: {claim_b}\n\n"
            'Are these claims substantively different? Return JSON: '
            '{"disagree": true|false}'
        )
        try:
            response = self.backend.call(
                LLMRequest(system_prompt=_SYSTEM_PROMPT, user_prompt=prompt)
            )
            data = self._parse_json_or_record(
                response.content, "_llm_check_disagreement"
            )
        except Exception as e:  # noqa: BLE001 — silent fallback preserves graceful degradation
            self._silent_failures.append(
                f"_llm_check_disagreement: {type(e).__name__}: {e}"
            )
            return None
        if not isinstance(data, dict) or "disagree" not in data:
            return None
        value = data["disagree"]
        if isinstance(value, bool):
            return value
        # Some LLMs return strings; coerce.
        if isinstance(value, str):
            return value.strip().lower() in ("true", "yes", "y", "1")
        return None

    def _step_counter(
        self,
        contradicts: DKSContradicts,
        arg_a: DKSArgument,
        arg_b: DKSArgument,
    ) -> DKSCounterArgument:
        """Step 5 — counter-argument naming the broken Toulmin component."""
        attacked = arg_a if contradicts.attacked_fz == arg_a.folgezettel else arg_b
        attacker = arg_b if attacked is arg_a else arg_a
        prompt = (
            f"Step: counter-argument.\n"
            f"Attacked argument warrant: {attacked.warrant.warrant}\n"
            f"Attacker's claim: {attacker.warrant.claim}\n\n"
            f"Identify which Toulmin component of the attacked argument "
            f"is broken. Return JSON:\n"
            f'{{"broken_component": "premise|warrant|counter-example|undercutting", '
            f'"counter_claim": "...", "reason": "...", '
            f'"strength": "weak|moderate|strong"}}'
        )
        response = self.backend.call(
            LLMRequest(system_prompt=_SYSTEM_PROMPT, user_prompt=prompt)
        )
        data = self._parse_json_or_record(response.content, "_step_counter")
        broken = _get_str(data, "broken_component", "warrant")
        if broken not in ("premise", "warrant", "counter-example", "undercutting"):
            broken = "warrant"
        strength = _get_str(data, "strength", "moderate")
        if strength not in ("weak", "moderate", "strong"):
            strength = "moderate"
        fz = _next_child_of(contradicts.attacked_fz, tuple(self._cycle_fz_existing))
        self._cycle_fz_existing.append(fz)
        return DKSCounterArgument(
            folgezettel=fz,
            attacked_fz=contradicts.attacked_fz,
            broken_component=broken,  # type: ignore[arg-type]
            counter_claim=_get_str(data, "counter_claim"),
            reason=_get_str(data, "reason"),
            strength=strength,  # type: ignore[arg-type]
        )

    def _step_pattern(self, counter: DKSCounterArgument) -> DKSPattern:
        """Step 6 — pattern discovery aggregating contradictions."""
        prompt = (
            f"Step: pattern discovery.\n"
            f"Counter-argument: {counter.counter_claim}\n"
            f"Broken component: {counter.broken_component}\n\n"
            f"Describe the structural regularity this contradiction "
            f"reveals. Return JSON:\n"
            f'{{"description": "...", "observed": ["short tag", ...]}}'
        )
        response = self.backend.call(
            LLMRequest(system_prompt=_SYSTEM_PROMPT, user_prompt=prompt)
        )
        data = self._parse_json_or_record(response.content, "_step_pattern")
        observed = data.get("observed") if isinstance(data, dict) else None
        if not isinstance(observed, list):
            observed = []
        fz = _next_child_of(counter.folgezettel, tuple(self._cycle_fz_existing))
        self._cycle_fz_existing.append(fz)
        return DKSPattern(
            folgezettel=fz,
            description=_get_str(data, "description"),
            observed=tuple(str(x) for x in observed),
        )

    def _step_rule_revision(
        self,
        pattern: DKSPattern,
        surviving_argument: DKSArgument | None = None,
    ) -> DKSRuleRevision:
        """Step 7 — revise the warrant the pattern indicts.

        When ``surviving_argument`` is supplied (multi-revision N>2
        cycles), the prompt names the surviving warrant so the revised
        rule can build from it rather than from the pattern alone.
        The revision's ``folgezettel`` is a child of the survivor's
        FZ (so each revision is anchored to the
        survivor it elaborates), not of the pattern's FZ.
        """
        if surviving_argument is not None:
            prompt = (
                f"Step: rule revision (multi-survivor, anchored to "
                f"{surviving_argument.folgezettel}).\n"
                f"Pattern: {pattern.description}\n"
                f"Surviving warrant — claim: "
                f"{surviving_argument.warrant.claim!r}\n"
                f"Surviving warrant — rule: "
                f"{surviving_argument.warrant.warrant!r}\n\n"
                f"Produce a revised warrant that elaborates the surviving "
                f"warrant + addresses the pattern. Return JSON:\n"
                f'{{"claim": "...", "data": "...", "warrant": "...", '
                f'"backing": "...", "qualifier": "...", '
                f'"supersedes": "<FZ of replaced rule, or empty string>"}}'
            )
            parent_fz = surviving_argument.folgezettel
        else:
            prompt = (
                f"Step: rule revision.\n"
                f"Pattern: {pattern.description}\n\n"
                f"Produce a revised warrant that prevents the same "
                f"contradiction in future cycles. Return JSON:\n"
                f'{{"claim": "...", "data": "...", "warrant": "...", '
                f'"backing": "...", "qualifier": "...", '
                f'"supersedes": "<FZ of replaced rule, or empty string>"}}'
            )
            parent_fz = pattern.folgezettel
        response = self.backend.call(
            LLMRequest(system_prompt=_SYSTEM_PROMPT, user_prompt=prompt)
        )
        data = self._parse_json_or_record(response.content, "_step_rule_revision")
        fz = _next_child_of(parent_fz, tuple(self._cycle_fz_existing))
        self._cycle_fz_existing.append(fz)
        supersedes_raw = _get_str(data, "supersedes", "")
        return DKSRuleRevision(
            folgezettel=fz,
            revised_warrant=DKSWarrant(
                claim=_get_str(data, "claim"),
                data=_get_str(data, "data"),
                warrant=_get_str(data, "warrant"),
                backing=_get_str(data, "backing", ""),
                qualifier=_get_str(data, "qualifier", ""),
            ),
            supersedes=supersedes_raw if supersedes_raw else None,
        )

    # ── Helpers ───────────────────────────────────────────────────────────

    def _format_warrants(self) -> str:
        if not self.warrants:
            return "(none)"
        return "\n".join(
            f"  - claim={w.claim!r} warrant={w.warrant!r}" for w in self.warrants
        )

    def _format_retrieval_context(self, k: int = 5) -> str:
        """Produce a "Related material from the substrate" block.

        Returns the empty string when no retrieval_client is configured
        or the search returns no hits. The block appends to the argument
        prompt (between warrants and the instruction). Errors are
        swallowed — retrieval grounding is best-effort context, not a
        hard prerequisite.
        """
        if self.retrieval_client is None:
            return ""
        try:
            hits = self.retrieval_client.search(self.observation.summary, k=k)
        except Exception as e:  # noqa: BLE001 — silent fallback preserves graceful degradation
            self._silent_failures.append(
                f"_format_retrieval_context: {type(e).__name__}: {e}"
            )
            return ""
        if not hits:
            return ""
        # P1 A1.1 — inject the quoted source SPAN (the BM25 snippet) so an
        # argument's `evidence` can cite a real span rather than free-form
        # model text. The snippet was generated by BM25 then dropped at the
        # fusion + client layers; it now flows through to here.
        lines = ["Related material from the substrate (top-K hybrid hits):"]
        for h in hits:
            snippet = getattr(h, "snippet", None)
            if snippet:
                # collapse whitespace so the span sits on one prompt line
                span = " ".join(snippet.split())
                lines.append(
                    f"  - {h.note_name} (score={h.score:.4f}) [span: {span}]"
                )
            else:
                lines.append(f"  - {h.note_name} (score={h.score:.4f})")
        lines.append("")  # trailing blank for prompt readability
        return "\n".join(lines) + "\n"


# ── Module-level helpers ─────────────────────────────────────────────────


def _parse_json(text: str) -> dict:
    """Tolerant JSON extraction — strict first, then first ``{...}`` block."""
    text = text.strip()
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            parsed = json.loads(m.group(0))
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


def _get_str(data: dict, key: str, default: str = "") -> str:
    """Get a string field with default; coerce non-strings."""
    v = data.get(key, default) if isinstance(data, dict) else default
    return str(v) if v is not None else default


def _coerce_bool(value: object) -> bool | None:
    """Read a boolean out of an LLM's JSON; ``None`` when it isn't one.

    Some backends answer ``"true"`` rather than ``true``, so strings are
    coerced from a closed vocabulary. Anything else returns ``None``,
    which callers must treat as "no answer" rather than as ``False`` —
    the two mean different things to a fail-closed gate.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        text = value.strip().lower()
        if text in ("true", "yes", "y", "1"):
            return True
        if text in ("false", "no", "n", "0"):
            return False
    return None


# ── Multi-cycle orchestration ────────────────────────────────────────────


WarrantChangeKind = Literal["added", "revised", "superseded"]
"""How a rule revision affects the active warrant set.

- ``added``: the revision introduces a wholly new warrant (``supersedes`` is None)
- ``revised``: the revision replaces an existing warrant (``supersedes`` set);
  this entry records the new warrant
- ``superseded``: companion entry for ``revised`` — records the FZ of
  the warrant that got displaced. Has no warrant body since the
  multi-cycle runner does not track FZ→warrant association on the
  input set.
"""


@dataclass(frozen=True)
class WarrantChange:
    """One entry in the per-run warrant-revision diff.

    ``added`` and ``revised`` carry the new warrant in ``warrant``.
    The paired ``superseded`` entry carries only the FZ in
    ``superseded_fz`` and leaves ``warrant`` as ``None`` — the
    multi-cycle runner does not track FZ→warrant association on the
    input warrant set, only the revision-side FZ.
    """

    cycle_id: str
    kind: WarrantChangeKind
    warrant: DKSWarrant | None = None
    revision_fz: str | None = None
    superseded_fz: str | None = None


@dataclass(frozen=True)
class DKSRunResult:
    """Output of an N-cycle DKS run.

    Aggregates per-cycle results plus a flat list of warrant changes
    classified by kind. ``final_warrants`` is the active warrant set
    after the last cycle — the union of ``initial_warrants`` and every
    cycle's revised warrant, in chronological order.
    """

    cycles: tuple[DKSCycleResult, ...]
    warrant_changes: tuple[WarrantChange, ...]
    final_warrants: tuple[DKSWarrant, ...]
    elapsed_ms: float = 0.0
    backend_id: str = ""

    @property
    def cycle_count(self) -> int:
        return len(self.cycles)

    @property
    def closed_loop_count(self) -> int:
        """How many cycles closed all 7 components."""
        return sum(1 for c in self.cycles if c.closed_loop)

    @property
    def gated_count(self) -> int:
        """How many cycles short-circuited via confidence gating."""
        return sum(1 for c in self.cycles if c.gated)


class DKSRunner:
    """Drive N sequential DKS cycles, threading warrants across them.

    Each cycle reads the *current* warrant set (initial + every prior
    cycle's revision) and may emit a new warrant via step 7. The
    ``DKSRunResult`` collects the per-cycle outputs plus a chronological
    diff of warrant changes so callers can audit the trajectory of the
    rule set across a multi-cycle session.

    Args:
        observations: Sequence of DKSObservations to drive cycles from.
            One cycle per observation. Each observation's ``folgezettel``
            is the cycle root.
        backend: LLM backend (MockBackend or AnthropicBackend) shared
            across all cycles.
        initial_warrants: Warrant set the first cycle sees. Empty tuple
            means cycle 1 authors warrants from the observation alone.
        confidence_model: Optional confidence gate. When passed, each
            cycle scores the observation against the current warrants
            before running; high-confidence observations short-circuit
            to observation + argument A only.
        confidence_threshold: Override the default
            (:data:`tessellum.dks.confidence.DEFAULT_CONFIDENCE_THRESHOLD`,
            0.85). Ignored when ``confidence_model`` is ``None``.
    """

    def __init__(
        self,
        observations: tuple[DKSObservation, ...],
        backend: LLMBackend,
        *,
        initial_warrants: tuple[DKSWarrant, ...] = (),
        confidence_model: object | None = None,
        confidence_threshold: float | None = None,
        retrieval_client: object | None = None,
        semantic_disagreement: bool = False,
        evidence_based_disagreement: bool = False,
        incompatibility_judge: IncompatibilityJudge | None = None,
        candidate_ranker: CandidateAttackerRanker | None = None,
        max_attack_candidates: int = DEFAULT_MAX_ATTACK_CANDIDATES,
        refutation_budget: int = DEFAULT_REFUTATION_BUDGET,
        perspectives: tuple[str, ...] = ("conservative", "exploratory"),
        modes: tuple[CycleMode, ...] = (),
    ) -> None:
        self.observations = observations
        self.backend = backend
        self.initial_warrants = initial_warrants
        self.confidence_model = confidence_model
        self.confidence_threshold = confidence_threshold
        # Retrieval + semantic-disagreement forwarded to each cycle.
        self.retrieval_client = retrieval_client
        self.semantic_disagreement = semantic_disagreement
        # P4 step-4 configuration, forwarded to each cycle. Default off:
        # every cycle runs the legacy string-compare path unless the
        # caller opts in here.
        self.evidence_based_disagreement = evidence_based_disagreement
        self.incompatibility_judge = incompatibility_judge
        self.candidate_ranker = candidate_ranker
        self.max_attack_candidates = max_attack_candidates
        self.refutation_budget = refutation_budget
        # Multi-perspective debate forwarded to each cycle.
        self.perspectives = perspectives
        # A0.1 — per-observation allocation mode, aligned positionally to
        # ``observations``. Empty (the default) means every cycle is "fresh",
        # preserving prior behavior; a NON-empty tuple must match the
        # observation count exactly (a partial tuple is a caller error).
        if modes and len(modes) != len(observations):
            raise ValueError(
                f"modes must align to observations: got {len(modes)} modes "
                f"for {len(observations)} observations"
            )
        self.modes: tuple[CycleMode, ...] = modes

    def run(self) -> DKSRunResult:
        from tessellum.dks.persistence import WarrantRegistry

        start = time.monotonic()
        # A0.3 — active-warrant supersession (release-blocker #3). Previously a
        # flat list appended every revision, so a superseded warrant stayed in
        # the active set AND leaked into the next cycle + final_warrants. Use a
        # WarrantRegistry keyed by FZ so supersede() REMOVES the old warrant
        # from the active set (WarrantHistory / the change log keep the audit
        # trail). Initial warrants carry no FZ, so key them synthetically.
        registry = WarrantRegistry()
        for j, w in enumerate(self.initial_warrants):
            registry.add(f"init:{j}", w)
        cycles: list[DKSCycleResult] = []
        changes: list[WarrantChange] = []

        for i, obs in enumerate(self.observations):
            obs_mode: CycleMode = self.modes[i] if self.modes else "fresh"
            cycle = DKSCycle(
                obs,
                registry.snapshot(),
                self.backend,
                confidence_model=self.confidence_model,
                confidence_threshold=self.confidence_threshold,
                retrieval_client=self.retrieval_client,
                semantic_disagreement=self.semantic_disagreement,
                evidence_based_disagreement=self.evidence_based_disagreement,
                incompatibility_judge=self.incompatibility_judge,
                candidate_ranker=self.candidate_ranker,
                max_attack_candidates=self.max_attack_candidates,
                refutation_budget=self.refutation_budget,
                perspectives=self.perspectives,
                mode=obs_mode,
            ).run()
            cycles.append(cycle)
            # Iterate every emitted revision. For N=2 cycles + N>2
            # single-survivor cycles, rule_revisions has 0 or 1 entry.
            # For N>2 multi-survivor cycles, this loop threads each
            # revision into the warrant change log.
            for rev in cycle.rule_revisions:
                if rev.supersedes:
                    changes.append(
                        WarrantChange(
                            cycle_id=cycle.cycle_id,
                            kind="revised",
                            warrant=rev.revised_warrant,
                            revision_fz=rev.folgezettel,
                            superseded_fz=rev.supersedes,
                        )
                    )
                    changes.append(
                        WarrantChange(
                            cycle_id=cycle.cycle_id,
                            kind="superseded",
                            warrant=None,
                            revision_fz=rev.folgezettel,
                            superseded_fz=rev.supersedes,
                        )
                    )
                else:
                    changes.append(
                        WarrantChange(
                            cycle_id=cycle.cycle_id,
                            kind="added",
                            warrant=rev.revised_warrant,
                            revision_fz=rev.folgezettel,
                            superseded_fz=None,
                        )
                    )
                # Update the ACTIVE set: a supersede removes the old warrant;
                # a plain add registers the new one. Guarded so
                # WarrantRegistry.add() never raises mid-run on a revision FZ
                # that is already active (only reachable on pathological
                # duplicate-root input, where the new revision FZ collides with
                # one already in the set — we then leave the active set as-is
                # rather than raising).
                new_fz = rev.folgezettel
                if new_fz in registry:
                    continue  # replacement key already active; skip (no raise)
                if rev.supersedes and rev.supersedes in registry:
                    registry.supersede(rev.supersedes, new_fz, rev.revised_warrant)
                else:
                    registry.add(new_fz, rev.revised_warrant)

        return DKSRunResult(
            cycles=tuple(cycles),
            warrant_changes=tuple(changes),
            final_warrants=registry.snapshot(),
            elapsed_ms=(time.monotonic() - start) * 1000.0,
            backend_id=getattr(self.backend, "backend_id", ""),
        )


def aggregate_warrant_changes(
    changes: tuple[WarrantChange, ...],
) -> dict[str, int]:
    """Count warrant changes by kind. Used in CLI aggregate traces."""
    counts: dict[str, int] = {"added": 0, "revised": 0, "superseded": 0}
    for c in changes:
        counts[c.kind] = counts.get(c.kind, 0) + 1
    return counts


__all__ = [
    # Types
    "ToulminComponent",
    "CycleMode",
    "CounterStrength",
    "WarrantChangeKind",
    "AttackDirection",
    # Evidence-based step 4 (P4)
    "DEFAULT_MAX_ATTACK_CANDIDATES",
    "DEFAULT_REFUTATION_BUDGET",
    "IncompatibilityVerdict",
    "IncompatibilityJudge",
    "TableIncompatibilityJudge",
    "LLMIncompatibilityJudge",
    "CandidateAttackerRanker",
    "LexicalOverlapRanker",
    # Dataclasses
    "DKSObservation",
    "DKSWarrant",
    "DKSArgument",
    "DKSContradicts",
    "DKSCounterArgument",
    "DKSPattern",
    "DKSRuleRevision",
    "DKSCycleResult",
    "WarrantChange",
    "DKSRunResult",
    # Allocator
    "allocate_cycle_fz",
    # Runtime
    "DKSCycle",
    "DKSRunner",
    "aggregate_warrant_changes",
]
