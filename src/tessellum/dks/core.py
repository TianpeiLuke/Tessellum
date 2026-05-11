"""Dialectic Knowledge System (DKS) — core runtime implementation.

This module IS the implementation. Public-API consumers should import
from the package root: ``from tessellum.dks import DKSCycle, DKSRunner, ...``.
This file is re-exported by :mod:`tessellum.dks`'s ``__init__`` and is
not part of the documented public surface; lifting members here in a
patch release is allowed only via the ``__init__`` re-export list.

Phase 1 of ``plans/plan_dks_implementation.md`` (v0.0.40). Ships:

- Seven typed dataclasses (one per component output)
- A Folgezettel-ID allocator implementing the three multi-cycle modes
  per :doc:`thought_dks_fz_integration` (``fresh`` / ``extend`` / ``branch``)
- A :class:`DKSCycle` that drives the 7-component closed loop through an
  :class:`LLMBackend`

Each cycle deposits a 5-node Folgezettel subtree into the substrate
(observation → 2 sibling arguments → counter → pattern → revised
warrant). The 4th component (disagreement detection) produces an edge,
not a node, so it doesn't get an FZ ID of its own.

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

What Phase 1 does NOT ship (deferred to later phases per the plan):

- Composer skill machinery (skill canonical + sidecar) — Phase 2
- Multi-cycle orchestration / CLI — Phase 3
- P-side retrieval client + TESS-004 validator + 6th eval dim — Phase 4
- Confidence gating + warrant persistence — Phase 5
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from typing import ClassVar, Literal

from tessellum.bb.types import BBType
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


@dataclass(frozen=True)
class DKSObservation:
    """Step 1 — what happened.

    Becomes an ``empirical_observation`` note at the cycle root FZ.
    Per FZ 2a2, this dataclass is a typed view over a ``BBNode`` of
    type ``BBType.EMPIRICAL_OBSERVATION``.
    """

    bb_type: ClassVar[BBType] = BBType.EMPIRICAL_OBSERVATION

    folgezettel: str
    summary: str
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


@dataclass(frozen=True)
class DKSArgument:
    """Step 2 or 3 — a typed claim grounded in a warrant.

    Becomes an ``argument`` note at FZ ``<cycle_root>.a`` or
    ``<cycle_root>.b``. Typed view over a ``BBNode`` of type
    ``BBType.ARGUMENT``.
    """

    bb_type: ClassVar[BBType] = BBType.ARGUMENT

    folgezettel: str
    warrant: DKSWarrant
    evidence: str


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


@dataclass(frozen=True)
class DKSCounterArgument:
    """Step 5 — names which Toulmin component is broken.

    Becomes a ``counter_argument`` note at FZ ``<attacked_fz>.a``. The
    ``folgezettel_parent`` field of that note equals ``attacked_fz``,
    which is what TESS-004 (FZ-integrated) checks. Typed view over a
    ``BBNode`` of type ``BBType.COUNTER_ARGUMENT``.
    """

    bb_type: ClassVar[BBType] = BBType.COUNTER_ARGUMENT

    folgezettel: str
    attacked_fz: str
    broken_component: ToulminComponent
    counter_claim: str
    reason: str
    strength: CounterStrength


@dataclass(frozen=True)
class DKSPattern:
    """Step 6 — model aggregating contradictions into structural regularity.

    Becomes a ``model`` note at FZ ``<counter_fz>.a``. ``observed`` is the
    tuple of contradict FZs (or descriptions) that feed this pattern.
    Typed view over a ``BBNode`` of type ``BBType.MODEL``. The
    realised corpus edge ``COUNTER_ARGUMENT → MODEL`` instantiates the
    schema edge ``pattern_of_failure`` registered in
    ``BB_SCHEMA_DKS_EXTENSIONS`` (the Phase-4-class extension to the
    original 10-edge schema from FZ 1).
    """

    bb_type: ClassVar[BBType] = BBType.MODEL

    folgezettel: str
    description: str
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
       — observation + A only. The confidence model said existing warrants
       cover this observation; steps 2-7 short-circuited (per Phase 5 plan).
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

    @property
    def folgezettel_nodes(self) -> tuple[str, ...]:
        """FZ positions this cycle deposited (excluding the edge)."""
        nodes: list[str] = [
            self.observation.folgezettel,
            self.argument_a.folgezettel,
        ]
        if self.argument_b is not None:
            nodes.append(self.argument_b.folgezettel)
        if self.counter:
            nodes.append(self.counter.folgezettel)
        if self.pattern:
            nodes.append(self.pattern.folgezettel)
        if self.rule_revision:
            nodes.append(self.rule_revision.folgezettel)
        return tuple(nodes)

    @property
    def closed_loop(self) -> bool:
        """True iff step 7 fired (a revised warrant was produced)."""
        return self.rule_revision is not None

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

    Constructed with an observation + the current warrant set + a backend,
    plus an optional confidence model (Phase 5). ``run()`` decides which
    terminal shape applies:

    - **gated** (Phase 5): if a confidence model returns a score *above*
      the threshold, the cycle short-circuits to *observation + argument A*
      and does not run steps 3-7. ``escalation_decision="gated"``.
    - **short-circuited**: A and B agree → no contradicts, no steps 5-7.
      ``escalation_decision="full"``, ``closed_loop=False``.
    - **full closed loop**: A and B disagree → full 7-component cycle.
      ``escalation_decision="full"``, ``closed_loop=True``.

    Confidence gating is opt-in. Callers who don't pass
    ``confidence_model`` get the v0.0.40 behaviour: always full cycle.
    """

    def __init__(
        self,
        observation: DKSObservation,
        warrants: tuple[DKSWarrant, ...],
        backend: LLMBackend,
        *,
        confidence_model: object | None = None,
        confidence_threshold: float | None = None,
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
        # FZ allocator state — children of the cycle root
        self._cycle_fz_existing: list[str] = [observation.folgezettel]

    def run(self) -> DKSCycleResult:
        start = time.monotonic()
        cycle_id = self.observation.folgezettel
        backend_id = getattr(self.backend, "backend_id", "")

        # Phase 5 — confidence gating (opt-in). Compute the gate decision
        # before any LLM call; the gated path saves 6 of the 7 backend
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
        arg_a = self._step_argument(perspective="conservative", suffix_hint="a")

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
            )

        # Step 3: argument B from a different angle.
        arg_b = self._step_argument(perspective="exploratory", suffix_hint="b")

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
        )

    # ── Per-step methods ──────────────────────────────────────────────────

    def _step_argument(
        self, perspective: str, suffix_hint: str
    ) -> DKSArgument:
        """Step 2 / step 3 — produce one argument from the warrant set."""
        warrants_block = self._format_warrants()
        prompt = (
            f"Step: generate argument ({perspective}).\n"
            f"Observation: {self.observation.summary}\n\n"
            f"Available warrants:\n{warrants_block}\n\n"
            f"Produce one argument from a {perspective} angle. Return JSON:\n"
            f'{{"claim": "...", "data": "...", "warrant": "...", '
            f'"backing": "...", "qualifier": "...", "evidence": "..."}}'
        )
        response = self.backend.call(
            LLMRequest(system_prompt=_SYSTEM_PROMPT, user_prompt=prompt)
        )
        data = _parse_json(response.content)
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
        )

    def _step_disagreement(
        self, arg_a: DKSArgument, arg_b: DKSArgument
    ) -> DKSContradicts | None:
        """Step 4 — detect contradiction between A and B (local computation).

        Two arguments contradict when their claims differ AND they're
        about the same observation. Phase 1 uses simple string inequality;
        Phase 3+ can route this through an LLM call if subtle semantic
        contradictions matter.
        """
        if arg_a.warrant.claim.strip() == arg_b.warrant.claim.strip():
            return None
        # B attacks A by default (B is the "exploratory" angle challenging
        # A's "conservative" one). Phase 5 can make this more sophisticated.
        return DKSContradicts(
            attacker_fz=arg_b.folgezettel,
            attacked_fz=arg_a.folgezettel,
            reason=(
                f"Claim mismatch: A asserts {arg_a.warrant.claim!r}; "
                f"B asserts {arg_b.warrant.claim!r}"
            ),
        )

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
        data = _parse_json(response.content)
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
        data = _parse_json(response.content)
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

    def _step_rule_revision(self, pattern: DKSPattern) -> DKSRuleRevision:
        """Step 7 — revise the warrant the pattern indicts."""
        prompt = (
            f"Step: rule revision.\n"
            f"Pattern: {pattern.description}\n\n"
            f"Produce a revised warrant that prevents the same "
            f"contradiction in future cycles. Return JSON:\n"
            f'{{"claim": "...", "data": "...", "warrant": "...", '
            f'"backing": "...", "qualifier": "...", '
            f'"supersedes": "<FZ of replaced rule, or empty string>"}}'
        )
        response = self.backend.call(
            LLMRequest(system_prompt=_SYSTEM_PROMPT, user_prompt=prompt)
        )
        data = _parse_json(response.content)
        fz = _next_child_of(pattern.folgezettel, tuple(self._cycle_fz_existing))
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


# ── Multi-cycle orchestration (Phase 3) ──────────────────────────────────


WarrantChangeKind = Literal["added", "revised", "superseded"]
"""How a rule revision affects the active warrant set.

- ``added``: the revision introduces a wholly new warrant (``supersedes`` is None)
- ``revised``: the revision replaces an existing warrant (``supersedes`` set);
  this entry records the new warrant
- ``superseded``: companion entry for ``revised`` — records the FZ of the
  warrant that got displaced. Has no warrant body since Phase 3 does not
  track FZ→warrant association on the input set.
"""


@dataclass(frozen=True)
class WarrantChange:
    """One entry in the per-run warrant-revision diff.

    ``added`` and ``revised`` carry the new warrant in ``warrant``. The
    paired ``superseded`` entry carries only the FZ in ``superseded_fz``
    and leaves ``warrant`` as ``None`` — Phase 3 does not track FZ→warrant
    association on the input warrant set, only the revision-side FZ.
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
        """How many cycles short-circuited via confidence gating (Phase 5)."""
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
        confidence_model: Optional Phase 5 confidence gate. When passed,
            each cycle scores the observation against the current
            warrants before running; high-confidence observations
            short-circuit to observation + argument A only.
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
    ) -> None:
        self.observations = observations
        self.backend = backend
        self.initial_warrants = initial_warrants
        self.confidence_model = confidence_model
        self.confidence_threshold = confidence_threshold

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
            ).run()
            cycles.append(cycle)
            if cycle.rule_revision is None:
                continue

            rev = cycle.rule_revision
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
