"""Meta-DKS runtime — proposer/attacker strategies + :class:`MetaCycle` dispatcher + event log I/O.

The mechanics that turn telemetry into schema events. Two pluggable
strategy interfaces ship:

- :class:`Proposer` — generates :class:`SchemaEditProposal` from a
  :class:`MetaObservation`. Two implementations:
  :class:`HeuristicProposer` (lookup-table-driven) and
  :class:`LLMProposer` (LLM-backed; reasons about all four Toulmin
  components symmetrically, surfaces input-bias risk).
- :class:`Attacker` — generates :class:`MetaCounterArgument` against
  each proposal. :class:`NoOpAttacker` is the default (no attacks);
  :class:`LLMAttacker` runs the dialectical attack step.

:class:`MetaCycle` composes one proposer + one attacker + a survival
threshold (``strict`` / ``majority`` / ``permissive``) into the four
meta-FSM stages: build proposals → filter → survive → emit events.

Event log shape: JSONL at ``runs/dks/meta/schema_events.jsonl``.
Each line is one :class:`tessellum.bb.types.SchemaEditEvent`. The log
is append-only by convention; :func:`write_event_log`
truncates + rewrites only when explicitly requested (e.g. snapshot
compaction).
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol, Sequence

from tessellum.bb.types import (
    BB_SCHEMA,
    BB_SCHEMA_EPISTEMIC,
    BB_SCHEMA_USER_EXTENSIONS,
    BBType,
    EpistemicEdgeType,
    SchemaEditEvent,
)
from tessellum.composer.llm import LLMBackend, LLMRequest
from tessellum.dks.meta.types import (
    MetaCounterArgument,
    MetaObservation,
    SchemaEditProposal,
)


DEFAULT_MIN_CYCLES: int = 20
"""Cold-start guard: meta-DKS produces no proposals below this many cycles.

A Toulmin-failure distribution needs ≥ ~20 cycles to be statistically
meaningful. Configurable via ``--min-cycles`` on the CLI.
"""


_TOULMIN_FAILURE_DOMINANCE_THRESHOLD: float = 0.5
"""When one Toulmin failure mode exceeds 50% of counters, propose a
related schema edit. Heuristic threshold; calibrate against
production traces if the dominance signal proves noisy."""


# ── Proposer strategies ─────────────────────────────────────────────────────


class Proposer(Protocol):
    """Strategy interface for SchemaEditProposal generation.

    Two implementations ship:

    - :class:`HeuristicProposer` — lookup-table-driven; the default and
      the ``--proposer heuristic`` CLI mode.
    - :class:`LLMProposer` — LLM-backed; receives the full
      :class:`MetaObservation` (strength breakdown, sample quotes,
      source metadata) and emits well-formed proposals via an
      :class:`tessellum.composer.llm.LLMBackend`.
    """

    def generate(
        self, observation: MetaObservation, target_failure: str | None = None
    ) -> list[SchemaEditProposal]:  # pragma: no cover
        ...


@dataclass
class HeuristicProposer:
    """Heuristic proposer — lookup-table-driven.

    Two rules:

    1. **Toulmin-failure dominance**: when one ``broken_component``
       exceeds 50% of counters, propose adding the schema edge
       mapped in :data:`_TOULMIN_TO_PROPOSED_EDGE`.
    2. **Unrealised schema edge** (retraction, ≥50 cycles): if a
       declared edge has zero corpus instances, propose retract.

    This is the default proposer for :class:`MetaCycle`.
    :class:`LLMProposer` addresses the heuristic's blind spots by
    reasoning over the full :class:`MetaObservation`.
    """

    def generate(
        self, observation: MetaObservation, target_failure: str | None = None
    ) -> list[SchemaEditProposal]:
        out: list[SchemaEditProposal] = []

        # Heuristic 1: Toulmin failure dominance.
        total = sum(observation.toulmin_failure_counts.values())
        if total > 0:
            for component, count in observation.toulmin_failure_counts.items():
                if target_failure and component != target_failure:
                    continue
                if count / total < _TOULMIN_FAILURE_DOMINANCE_THRESHOLD:
                    continue
                proposal = _proposal_for_toulmin_dominance(component, count, total)
                if proposal is not None:
                    out.append(proposal)

        # Heuristic 2: unrealised schema edge (retract, ≥50 cycles).
        if observation.cycles_examined >= 50:
            for edge in observation.unrealised_schema_edges:
                if edge in BB_SCHEMA_EPISTEMIC:
                    continue
                out.append(
                    SchemaEditProposal(
                        kind="retract",
                        edge=edge,
                        motivating_observation=(
                            f"Edge {edge.source.value} → {edge.target.value} "
                            f"({edge.label!r}) has zero corpus instances after "
                            f"{observation.cycles_examined} cycles."
                        ),
                        expected_impact="Smaller schema; fewer untyped reports.",
                    )
                )

        return out


_LLM_PROPOSER_SYSTEM_PROMPT = """\
You are the meta-DKS proposer. You read aggregated telemetry from past \
cycle-level DKS runs (a MetaObservation) and emit zero or more \
SchemaEditProposals naming changes to BB_SCHEMA_USER_EXTENSIONS.

Authoring rules:

- All four Toulmin components are first-class — do not privilege one
  over the others.
- Counter strengths weight the signal: one `strong` outweighs two `weak`.
- Quote sample counter-arguments when justifying proposals; aggregates
  alone are not sufficient.
- Self-report `input_bias_risk` ("low" / "medium" / "high") on every
  proposal. If the observation source has structural skew that would
  mechanically induce one failure shape (e.g., open-architectural
  questions invite warrant attacks), set "high".
- When ``silent_failure_count > 0``, factor degraded-backend likelihood
  into your reasoning — a backend that's silently failing every other
  call may be producing misleading Toulmin distributions. Bias
  ``input_bias_risk`` upward when silent_failure_count >= 10% of
  cycles_examined.

Return ONLY a JSON object of the shape:

{
  "proposals": [
    {
      "kind": "add" | "retract" | "refine",
      "edge": {"source": <BBType>, "target": <BBType>, "label": "<snake_case>"},
      "motivating_observation": "...",
      "expected_impact": "...",
      "input_bias_risk": "low" | "medium" | "high"
    }
  ]
}

The 8 valid BBType values are: empirical_observation, concept, model, \
hypothesis, argument, counter_argument, procedure, navigation.

No code fences. No prose. If no actionable schema gap is surfaced,
return {"proposals": []}.
"""


@dataclass
class LLMProposer:
    """Phase V-driven LLM-backed proposer.

    Constructs an :class:`LLMRequest` from the :class:`MetaObservation`,
    invokes the supplied :class:`LLMBackend`, parses the JSON response,
    and returns the resulting :class:`SchemaEditProposal` list. The
    ``input_bias_risk`` field on each proposal is captured into
    ``motivating_observation`` as a one-line prefix (the dataclass
    itself does not yet have a dedicated field — that ships in B.3
    along with :class:`MetaCounterArgument`).

    Failure modes:

    - LLM returns malformed JSON → empty list (caller may fall back).
    - LLM returns proposals with unknown BBType strings → those
      proposals are skipped silently; valid ones still pass through.
    """

    backend: LLMBackend
    max_tokens: int = 2000

    def generate(
        self, observation: MetaObservation, target_failure: str | None = None
    ) -> list[SchemaEditProposal]:
        prompt = self._render_user_prompt(observation, target_failure)
        request = LLMRequest(
            system_prompt=_LLM_PROPOSER_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=self.max_tokens,
        )
        response = self.backend.call(request)
        try:
            payload = json.loads(response.content)
        except json.JSONDecodeError:
            return []

        if not isinstance(payload, dict):
            return []
        items = payload.get("proposals") or []
        if not isinstance(items, list):
            return []

        out: list[SchemaEditProposal] = []
        for item in items:
            proposal = self._parse_proposal(item, target_failure)
            if proposal is not None:
                out.append(proposal)
        return out

    @staticmethod
    def _render_user_prompt(
        observation: MetaObservation, target_failure: str | None
    ) -> str:
        target_clause = (
            f"\nFILTER: only propose edits whose motivating component is "
            f"{target_failure!r}.\n"
            if target_failure
            else ""
        )
        return (
            f"META-OBSERVATION\n"
            f"  cycles_examined: {observation.cycles_examined}\n"
            f"  toulmin_failure_counts: "
            f"{json.dumps(observation.toulmin_failure_counts)}\n"
            f"  counter_strength_breakdown: "
            f"{json.dumps(observation.counter_strength_breakdown)}\n"
            f"  per_perspective_breakdown: "
            f"{json.dumps(observation.per_perspective_breakdown)}\n"
            f"  silent_failure_count: "
            f"{observation.silent_failure_count}\n"
            f"  top_attacked_warrants: "
            f"{json.dumps(list(observation.top_attacked_warrants))}\n"
            f"  unrealised_schema_edges: "
            f"{json.dumps([_edge_to_dict(e) for e in observation.unrealised_schema_edges])}\n"
            f"  sample_counter_quotes: "
            f"{json.dumps({k: list(v) for k, v in observation.sample_counter_quotes.items()})}\n"
            f"  observation_source_metadata: "
            f"{observation.observation_source_metadata!r}\n"
            f"{target_clause}\n"
            f"Apply the meta-DKS proposer rules. Emit zero or more "
            f"proposals as JSON."
        )

    @staticmethod
    def _parse_proposal(
        item: object, target_failure: str | None
    ) -> SchemaEditProposal | None:
        if not isinstance(item, dict):
            return None
        kind = item.get("kind")
        if kind not in ("add", "retract", "refine"):
            return None
        edge_dict = item.get("edge")
        if not isinstance(edge_dict, dict):
            return None
        try:
            source = BBType(edge_dict.get("source"))
            target = BBType(edge_dict.get("target"))
        except ValueError:
            return None
        label = edge_dict.get("label")
        if not isinstance(label, str) or not label:
            return None
        motivating = str(item.get("motivating_observation", ""))
        impact = str(item.get("expected_impact", ""))
        risk = item.get("input_bias_risk")
        if isinstance(risk, str) and risk in ("low", "medium", "high"):
            motivating = f"[input_bias_risk={risk}] {motivating}"
        return SchemaEditProposal(
            kind=kind,  # type: ignore[arg-type]
            edge=EpistemicEdgeType(source=source, target=target, label=label),
            motivating_observation=motivating,
            expected_impact=impact,
        )


def _edge_to_dict(edge: EpistemicEdgeType) -> dict:
    return {
        "source": edge.source.value,
        "target": edge.target.value,
        "label": edge.label,
    }


# ── Attacker strategies ─────────────────────────────────────────────────────


class Attacker(Protocol):
    """Strategy interface for :class:`MetaCounterArgument` generation.

    Two implementations ship:

    - :class:`NoOpAttacker` — default. Returns ``[]`` for every
      proposal. Effectively a pass-through survival policy when
      meta-DKS is run with ``--attacker none``.
    - :class:`LLMAttacker` — LLM-backed dialectical attacker. Reads
      the proposal list + the :class:`MetaObservation` and emits
      typed counter-arguments per the meta-cycle skill canonical's
      step 2.
    """

    def attack(
        self,
        proposals: Sequence[SchemaEditProposal],
        observation: MetaObservation,
    ) -> list[MetaCounterArgument]:  # pragma: no cover
        ...


@dataclass
class NoOpAttacker:
    """Default attacker — emits zero counter-arguments.

    Equivalent to a ``survive = filter(generate)`` policy when the
    user has not opted into ``--attacker llm``.
    """

    def attack(
        self,
        proposals: Sequence[SchemaEditProposal],
        observation: MetaObservation,
    ) -> list[MetaCounterArgument]:
        return []


_LLM_ATTACKER_SYSTEM_PROMPT = """\
You are the meta-DKS attacker. You read a list of SchemaEditProposals \
(produced by step 1, the proposer) and the originating MetaObservation, \
and emit zero or more MetaCounterArguments naming weaknesses in those \
proposals.

Each attack must:

- Reference a proposal by its index in the input array
  (`attacked_proposal_index`).
- Name a single `attack_kind` from this closed vocabulary:
  - `insufficient_evidence` — telemetry doesn't actually support the
    proposed edge
  - `input_bias` — the dominance is input-induced, not a real schema
    gap (use this when proposal's input_bias_risk is medium / high)
  - `overgeneralisation` — proposed edge is too broad / would over-fire
  - `collides_with_existing` — duplicates or contradicts an active edge
  - `weak_signal` — counts cross threshold but strength is too soft
- Cite specific telemetry counts, sample quotes, or schema state in
  `reason`. Attack the proposal's logic, never the proposer's competence.
- Assign a `strength`: "weak" / "moderate" / "strong".

Multiple attacks against the same proposal are allowed only when each
names a distinct `attack_kind`. Empty `attacks` array is valid — if a
proposal has no defensible attack, return [] for it.

Return ONLY a JSON object of the shape:

{
  "attacks": [
    {
      "attacked_proposal_index": <integer>,
      "attack_kind": "insufficient_evidence" | "input_bias" | "overgeneralisation" | "collides_with_existing" | "weak_signal",
      "reason": "<specific evidence-grounded prose>",
      "strength": "weak" | "moderate" | "strong"
    }
  ]
}

No code fences. No prose.
"""


@dataclass
class LLMAttacker:
    """LLM-backed dialectical attacker (Phase B.3).

    Renders proposals + MetaObservation into an :class:`LLMRequest`,
    invokes the supplied :class:`LLMBackend`, parses the JSON response
    into :class:`MetaCounterArgument` instances.
    """

    backend: LLMBackend
    max_tokens: int = 2000

    def attack(
        self,
        proposals: Sequence[SchemaEditProposal],
        observation: MetaObservation,
    ) -> list[MetaCounterArgument]:
        if not proposals:
            return []
        prompt = self._render_user_prompt(proposals, observation)
        request = LLMRequest(
            system_prompt=_LLM_ATTACKER_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=self.max_tokens,
        )
        response = self.backend.call(request)
        try:
            payload = json.loads(response.content)
        except json.JSONDecodeError:
            return []
        if not isinstance(payload, dict):
            return []
        items = payload.get("attacks") or []
        if not isinstance(items, list):
            return []

        out: list[MetaCounterArgument] = []
        seen: set[tuple[int, str]] = set()
        for item in items:
            attack = self._parse_attack(item, len(proposals))
            if attack is None:
                continue
            # Dedup: same (proposal_index, kind) pair filtered
            key = (attack.attacked_proposal_index, attack.attack_kind)
            if key in seen:
                continue
            seen.add(key)
            out.append(attack)
        return out

    @staticmethod
    def _render_user_prompt(
        proposals: Sequence[SchemaEditProposal], observation: MetaObservation
    ) -> str:
        proposals_json = [
            {
                "index": i,
                "kind": p.kind,
                "edge": _edge_to_dict(p.edge),
                "motivating_observation": p.motivating_observation,
                "expected_impact": p.expected_impact,
            }
            for i, p in enumerate(proposals)
        ]
        return (
            f"PROPOSALS (from step 1)\n"
            f"{json.dumps(proposals_json, indent=2)}\n\n"
            f"META-OBSERVATION\n"
            f"  cycles_examined: {observation.cycles_examined}\n"
            f"  toulmin_failure_counts: "
            f"{json.dumps(observation.toulmin_failure_counts)}\n"
            f"  counter_strength_breakdown: "
            f"{json.dumps(observation.counter_strength_breakdown)}\n"
            f"  sample_counter_quotes: "
            f"{json.dumps({k: list(v) for k, v in observation.sample_counter_quotes.items()})}\n"
            f"  observation_source_metadata: "
            f"{observation.observation_source_metadata!r}\n\n"
            f"Apply the meta-DKS attacker rules. Emit zero or more "
            f"attacks as JSON."
        )

    @staticmethod
    def _parse_attack(
        item: object, num_proposals: int
    ) -> MetaCounterArgument | None:
        if not isinstance(item, dict):
            return None
        idx = item.get("attacked_proposal_index")
        if not isinstance(idx, int) or idx < 0 or idx >= num_proposals:
            return None
        kind = item.get("attack_kind")
        valid_kinds = (
            "insufficient_evidence",
            "input_bias",
            "overgeneralisation",
            "collides_with_existing",
            "weak_signal",
        )
        if kind not in valid_kinds:
            return None
        reason = item.get("reason")
        if not isinstance(reason, str) or not reason:
            return None
        strength = item.get("strength", "moderate")
        if strength not in ("weak", "moderate", "strong"):
            strength = "moderate"
        return MetaCounterArgument(
            attacked_proposal_index=idx,
            attack_kind=kind,  # type: ignore[arg-type]
            reason=reason,
            strength=strength,  # type: ignore[arg-type]
        )


# ── Aggregation (Phase B.3) ─────────────────────────────────────────────────


def _proposal_survives(
    attacks: Sequence[MetaCounterArgument], threshold: str
) -> bool:
    """Decide survival per the configured threshold.

    See :data:`tessellum.dks.meta.types.SURVIVE_THRESHOLD` for the
    three policies.
    """
    if threshold == "strict":
        return len(attacks) == 0
    if threshold == "permissive":
        return all(a.strength != "strong" for a in attacks)
    # default: majority
    strong = sum(1 for a in attacks if a.strength == "strong")
    moderate = sum(1 for a in attacks if a.strength == "moderate")
    return strong <= 1 and moderate <= 2


# ── MetaCycleResult ─────────────────────────────────────────────────────────


@dataclass(frozen=True)
class MetaCycleResult:
    """Output of one meta-DKS cycle.

    Carries the input observation, the (≥0) proposals the cycle
    generated, surviving proposals after dialectic, the events
    written (if --apply was used), and the elapsed time.

    Two telemetry fields surface the dialectic outcome:

    - ``attacks``: the :class:`MetaCounterArgument`s emitted by the
      configured attacker (default :class:`NoOpAttacker` → empty).
    - ``survive_threshold``: which aggregation policy was applied.
    """

    observation: MetaObservation
    proposals: tuple[SchemaEditProposal, ...]
    surviving: tuple[SchemaEditProposal, ...]
    events_landed: tuple[SchemaEditEvent, ...]
    elapsed_ms: float = 0.0
    dry_run: bool = True
    # Attack telemetry — populated by the configured attacker.
    attacks: tuple[MetaCounterArgument, ...] = ()
    survive_threshold: str = "majority"


# ── MetaCycle ───────────────────────────────────────────────────────────────


@dataclass
class MetaCycle:
    """One meta-DKS cycle — walks the meta-FSM end-to-end.

    Stages:

    1. **Build proposals** from the :class:`MetaObservation` via the
       configured :class:`Proposer` (heuristic by default; LLM-backed
       under ``--proposer llm``). Each proposal is a
       :class:`SchemaEditProposal`.
    2. **Filter** by basic sanity (no duplicate edges; no edge that
       already exists in ``BB_SCHEMA``; no proposal naming a BB type
       not in :class:`BBType`).
    3. **Survive**: dispatch to the configured :class:`Attacker`. The
       default :class:`NoOpAttacker` makes every well-formed proposal
       survive; :class:`LLMAttacker` runs the dialectical attack step
       and the ``survive_threshold`` decides per-proposal survival.
    4. **Emit events**: when ``dry_run=False``, turn surviving
       proposals into :class:`SchemaEditEvent` instances + return
       them. The caller (CLI) writes them to disk.

    All four stages run synchronously.
    """

    observation: MetaObservation
    min_cycles: int = DEFAULT_MIN_CYCLES
    target_failure: str | None = None  # filter to a specific Toulmin component
    dry_run: bool = True
    proposer: Proposer = field(default_factory=lambda: HeuristicProposer())
    attacker: Attacker = field(default_factory=lambda: NoOpAttacker())
    survive_threshold: str = "majority"

    def run(self) -> MetaCycleResult:
        start = time.monotonic()

        if self.observation.cycles_examined < self.min_cycles:
            return MetaCycleResult(
                observation=self.observation,
                proposals=(),
                surviving=(),
                events_landed=(),
                elapsed_ms=(time.monotonic() - start) * 1000.0,
                dry_run=self.dry_run,
                attacks=(),
                survive_threshold=self.survive_threshold,
            )

        proposals = tuple(self._generate_proposals())
        filtered = tuple(self._filter_proposals(proposals))
        attacks = tuple(self.attacker.attack(filtered, self.observation))
        surviving = tuple(self._aggregate_survival(filtered, attacks))
        events: tuple[SchemaEditEvent, ...] = ()
        if not self.dry_run:
            events = tuple(self._proposals_to_events(surviving))

        return MetaCycleResult(
            observation=self.observation,
            proposals=proposals,
            surviving=surviving,
            events_landed=events,
            elapsed_ms=(time.monotonic() - start) * 1000.0,
            dry_run=self.dry_run,
            attacks=attacks,
            survive_threshold=self.survive_threshold,
        )

    def _aggregate_survival(
        self,
        filtered_proposals: Sequence[SchemaEditProposal],
        attacks: Sequence[MetaCounterArgument],
    ) -> list[SchemaEditProposal]:
        """Per-proposal survival decision using the configured threshold."""
        if not attacks:
            # NoOpAttacker path — pass-through survival policy.
            return list(filtered_proposals)
        attacks_by_index: dict[int, list[MetaCounterArgument]] = {}
        for a in attacks:
            attacks_by_index.setdefault(a.attacked_proposal_index, []).append(a)
        surviving: list[SchemaEditProposal] = []
        for i, proposal in enumerate(filtered_proposals):
            proposal_attacks = attacks_by_index.get(i, [])
            if _proposal_survives(proposal_attacks, self.survive_threshold):
                surviving.append(proposal)
        return surviving

    # ── proposal generation ──

    def _generate_proposals(self) -> list[SchemaEditProposal]:
        """Delegate to the configured :class:`Proposer` strategy.

        Default proposer is :class:`HeuristicProposer`. Pass
        ``proposer=LLMProposer(backend=...)`` for the LLM-driven
        proposer.
        """
        return self.proposer.generate(
            self.observation, target_failure=self.target_failure
        )

    def _filter_proposals(
        self, proposals: Sequence[SchemaEditProposal]
    ) -> list[SchemaEditProposal]:
        """Drop ill-formed or duplicate proposals."""
        seen: set[tuple] = set()
        out: list[SchemaEditProposal] = []
        for p in proposals:
            key = (p.kind, p.edge.source, p.edge.target, p.edge.label)
            if key in seen:
                continue
            seen.add(key)

            # Sanity: every BB type must be valid (caller can't pass
            # garbage)
            if not isinstance(p.edge.source, BBType):
                continue
            if not isinstance(p.edge.target, BBType):
                continue

            # Don't propose adding an edge that already exists
            if p.kind == "add" and p.edge in BB_SCHEMA:
                continue
            # Don't propose retracting an edge that's not in the user
            # extensions (we can't retract core schema edges via this
            # path).
            if p.kind == "retract" and p.edge not in BB_SCHEMA_USER_EXTENSIONS:
                # Allow retracting if it's in the corpus-realisable
                # set (DKS_EXTENSIONS). Otherwise skip.
                if p.edge not in BB_SCHEMA:
                    continue

            out.append(p)
        return out

    def _proposals_to_events(
        self, proposals: Sequence[SchemaEditProposal]
    ) -> list[SchemaEditEvent]:
        """Materialise surviving proposals as SchemaEditEvents."""
        out: list[SchemaEditEvent] = []
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for p in proposals:
            kind = "added" if p.kind == "add" else (
                "retracted" if p.kind == "retract" else "refined"
            )
            out.append(
                SchemaEditEvent(
                    timestamp=ts,
                    kind=kind,  # type: ignore[arg-type]
                    edge=p.edge,
                    motivating_failure=p.motivating_observation,
                    superseded_by=None,
                )
            )
        return out


# ── Heuristic helpers ───────────────────────────────────────────────────────


_TOULMIN_TO_PROPOSED_EDGE: dict[str, tuple[BBType, BBType, str]] = {
    # When counters keep firing with ``broken_component=warrant``,
    # propose adding an explicit MOD→PRO "warrant_codification" edge
    # so warrants can be located + queried.
    "warrant": (BBType.MODEL, BBType.PROCEDURE, "warrant_codification"),
    # When ``broken_component=counter-example``, propose adding a
    # CTR→OBS "counterexample_anchor" edge — counters citing
    # specific observations should type-check.
    "counter-example": (
        BBType.COUNTER_ARGUMENT,
        BBType.EMPIRICAL_OBSERVATION,
        "counterexample_anchor",
    ),
    # When ``broken_component=premise``, propose adding an ARG→OBS
    # "premise_grounding" edge for the data field of warrants.
    "premise": (
        BBType.ARGUMENT,
        BBType.EMPIRICAL_OBSERVATION,
        "premise_grounding",
    ),
    # ``undercutting`` doesn't map cleanly to a single edge — emit
    # no proposal for it. The :class:`LLMProposer` can reason about it
    # directly via the full :class:`MetaObservation`.
}


def _proposal_for_toulmin_dominance(
    component: str, count: int, total: int
) -> SchemaEditProposal | None:
    """Resolve a Toulmin-dominance signal to a proposed schema edge."""
    mapping = _TOULMIN_TO_PROPOSED_EDGE.get(component)
    if mapping is None:
        return None
    source, target, label = mapping
    edge = EpistemicEdgeType(source, target, label)
    pct = 100.0 * count / total if total else 0.0
    return SchemaEditProposal(
        kind="add",
        edge=edge,
        motivating_observation=(
            f"Toulmin failure mode {component!r} dominates the "
            f"counter-argument distribution ({count}/{total} = {pct:.1f}%). "
            f"Propose adding the related typed edge so the schema can "
            f"declare the missing relationship."
        ),
        expected_impact=(
            f"Reduce {component!r}-class counter-argument firings; "
            f"give meta-DKS a structural way to track this failure "
            f"mode beyond the warrant-attack-rate signal."
        ),
    )


# ── Event log I/O ───────────────────────────────────────────────────────────


def load_event_log(path: Path | str) -> tuple[SchemaEditEvent, ...]:
    """Read SchemaEditEvents from a JSONL log. Empty list if missing."""
    p = Path(path)
    if not p.is_file():
        return ()
    out: list[SchemaEditEvent] = []
    with p.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            try:
                event = _parse_event(obj)
            except (KeyError, TypeError, ValueError):
                continue
            out.append(event)
    return tuple(out)


def write_event_log(
    path: Path | str,
    events: Sequence[SchemaEditEvent],
    *,
    append: bool = True,
) -> None:
    """Write events to the JSONL log. Default append-only."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with p.open(mode, encoding="utf-8") as fh:
        for e in events:
            fh.write(json.dumps(_serialise_event(e)) + "\n")


def _serialise_event(event: SchemaEditEvent) -> dict:
    return {
        "timestamp": event.timestamp,
        "kind": event.kind,
        "edge": {
            "source": event.edge.source.value,
            "target": event.edge.target.value,
            "label": event.edge.label,
        },
        "motivating_failure": event.motivating_failure,
        "superseded_by": event.superseded_by,
    }


def _parse_event(payload: dict) -> SchemaEditEvent:
    edge_dict = payload["edge"]
    return SchemaEditEvent(
        timestamp=str(payload["timestamp"]),
        kind=payload["kind"],
        edge=EpistemicEdgeType(
            source=BBType(edge_dict["source"]),
            target=BBType(edge_dict["target"]),
            label=str(edge_dict["label"]),
        ),
        motivating_failure=str(payload.get("motivating_failure", "")),
        superseded_by=payload.get("superseded_by"),
    )


__all__ = [
    "DEFAULT_MIN_CYCLES",
    "MetaCycle",
    "MetaCycleResult",
    "Proposer",
    "HeuristicProposer",
    "LLMProposer",
    "Attacker",
    "NoOpAttacker",
    "LLMAttacker",
    "load_event_log",
    "write_event_log",
]
