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
from typing import Literal

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
    """Dung grounded labelling over ``arguments``. Maps each
    argument's FZ to ``"in"`` / ``"out"`` / ``"undec"``. Empty for
    N=2 cycles (the existing single-edge logic still applies). For
    N>2, this is the basis of survival selection — surviving
    arguments are those labelled ``"in"``."""

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
    """Return the next letter-suffix child of ``parent_fz``.

    First child is ``<parent>a``; second is ``<parent>b``; etc. We use
    the alphanumeric form (parent ``"1"`` → child ``"1a"`` → grandchild
    ``"1a1"``) consistent with Tessellum's existing trail conventions —
    same shape as ``thought_cqrs_design_evolution`` (FZ 1a) descending
    from ``thought_building_block_ontology_relationships`` (FZ 1).
    """
    # Children of `parent_fz` have prefix `parent_fz` + single letter (and
    # possibly more after that). We're looking for direct children whose
    # next character is a letter.
    direct_letters: set[str] = set()
    parent_len = len(parent_fz)
    for fz in existing_trails:
        if not fz or not fz.startswith(parent_fz):
            continue
        if len(fz) <= parent_len:
            continue
        next_char = fz[parent_len]
        if next_char.isalpha() and next_char.islower():
            direct_letters.add(next_char)
    # Find the next available lowercase letter
    for letter_code in range(ord("a"), ord("z") + 1):
        letter = chr(letter_code)
        if letter not in direct_letters:
            return parent_fz + letter
    # Exhausted a-z; fall back to two-letter suffix
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
        perspectives: tuple[str, ...] = ("conservative", "exploratory"),
    ) -> None:
        self.observation = observation
        self.warrants = warrants
        self.backend = backend
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
                mode="fresh",
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
                mode="fresh",
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
            )

        # Step 5: counter-argument naming the broken Toulmin component
        counter = self._step_counter(contradicts, arg_a, arg_b)
        # Step 6: pattern discovery aggregating the contradiction
        pattern = self._step_pattern(counter)
        # Step 7: rule revision closing the loop
        revision = self._step_rule_revision(pattern)

        return DKSCycleResult(
            cycle_id=cycle_id,
            mode="fresh",
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
            grounded_labelling={
                arg_a.folgezettel: "out",
                arg_b.folgezettel: "in",
            },
            rule_revisions=(revision,),
            silent_failures=tuple(self._silent_failures),
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

        # Pairwise step 4: emit a contradicts edge for every (i, j)
        # pair with i < j where claims differ. B attacks A by
        # convention (the later perspective is the "attacker").
        contradicts_edges: list[DKSContradicts] = []
        for i in range(len(arguments)):
            for j in range(i + 1, len(arguments)):
                a_i = arguments[i]
                a_j = arguments[j]
                if a_i.warrant.claim.strip() == a_j.warrant.claim.strip():
                    continue
                contradicts_edges.append(
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
                mode="fresh",
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
            mode="fresh",
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

        Default: simple string-inequality on the claim text. With
        ``semantic_disagreement=True``, do one backend call asking
        "are these claims substantively different?"; fall back to
        string-compare on parse failure.
        """
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
        # B attacks A by default (B is the "exploratory" angle
        # challenging A's "conservative" one). N>2 cycles compute the
        # attack direction from the pairwise contradicts graph and
        # Dung labelling instead.
        return DKSContradicts(
            attacker_fz=arg_b.folgezettel,
            attacked_fz=arg_a.folgezettel,
            reason=(
                f"Claim mismatch: A asserts {arg_a.warrant.claim!r}; "
                f"B asserts {arg_b.warrant.claim!r}"
            ),
        )

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
        lines = ["Related material from the substrate (top-K hybrid hits):"]
        for h in hits:
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
        perspectives: tuple[str, ...] = ("conservative", "exploratory"),
    ) -> None:
        self.observations = observations
        self.backend = backend
        self.initial_warrants = initial_warrants
        self.confidence_model = confidence_model
        self.confidence_threshold = confidence_threshold
        # Retrieval + semantic-disagreement forwarded to each cycle.
        self.retrieval_client = retrieval_client
        self.semantic_disagreement = semantic_disagreement
        # Multi-perspective debate forwarded to each cycle.
        self.perspectives = perspectives

    def run(self) -> DKSRunResult:
        start = time.monotonic()
        warrants: list[DKSWarrant] = list(self.initial_warrants)
        cycles: list[DKSCycleResult] = []
        changes: list[WarrantChange] = []

        for obs in self.observations:
            cycle = DKSCycle(
                obs,
                tuple(warrants),
                self.backend,
                confidence_model=self.confidence_model,
                confidence_threshold=self.confidence_threshold,
                retrieval_client=self.retrieval_client,
                semantic_disagreement=self.semantic_disagreement,
                perspectives=self.perspectives,
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
                warrants.append(rev.revised_warrant)

        return DKSRunResult(
            cycles=tuple(cycles),
            warrant_changes=tuple(changes),
            final_warrants=tuple(warrants),
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
