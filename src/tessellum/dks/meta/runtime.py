"""Meta-DKS runtime — observation builder + MetaCycle dispatcher + event log I/O.

The mechanics that turn telemetry into schema events. v0.0.52 ships
heuristic-based proposal generation; Phase 11+ will swap in an
LLM-driven proposer that uses the Composer skill canonical for the
meta-cycle.

Event log shape: JSONL at ``runs/dks/meta/schema_events.jsonl``.
Each line is one :class:`tessellum.bb.types.SchemaEditEvent`. The log
is append-only by convention; ``write_event_log`` truncates+rewrites
only when explicitly requested (e.g. snapshot compaction).
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from tessellum.bb.types import (
    BB_SCHEMA,
    BB_SCHEMA_EPISTEMIC,
    BB_SCHEMA_USER_EXTENSIONS,
    BBType,
    EpistemicEdgeType,
    SchemaEditEvent,
)
from tessellum.dks.meta.types import (
    MetaObservation,
    SchemaEditProposal,
)


DEFAULT_MIN_CYCLES: int = 20
"""Cold-start guard: meta-DKS produces no proposals below this many cycles.

Per `plan_dks_expansion` open-question lean: a Toulmin-failure
distribution needs ≥ ~20 cycles to be statistically meaningful.
Configurable via ``--min-cycles`` on the CLI.
"""


_TOULMIN_FAILURE_DOMINANCE_THRESHOLD: float = 0.5
"""When one Toulmin failure mode exceeds 50% of counters, propose a
related schema edit. Heuristic; replace with learned thresholds in
Phase 11+."""


# ── MetaCycleResult ─────────────────────────────────────────────────────────


@dataclass(frozen=True)
class MetaCycleResult:
    """Output of one meta-DKS cycle.

    Carries the input observation, the (≥0) proposals the cycle
    generated, surviving proposals after dialectic, the events
    written (if --apply was used), and the elapsed time.
    """

    observation: MetaObservation
    proposals: tuple[SchemaEditProposal, ...]
    surviving: tuple[SchemaEditProposal, ...]
    events_landed: tuple[SchemaEditEvent, ...]
    elapsed_ms: float = 0.0
    dry_run: bool = True


# ── MetaCycle ───────────────────────────────────────────────────────────────


@dataclass
class MetaCycle:
    """One meta-DKS cycle — walks the meta-FSM end-to-end.

    Stages:

    1. **Build proposals** from the :class:`MetaObservation`. v0.0.52
       uses heuristics (Toulmin-failure dominance, attacked-warrant
       concentration). Each proposal is a :class:`SchemaEditProposal`.
    2. **Filter** by basic sanity (no duplicate edges; no edge that
       already exists in ``BB_SCHEMA``; no proposal naming a BB type
       not in :class:`BBType`).
    3. **Survive**: in v0.0.52 every well-formed proposal survives
       (the meta-cycle's *attack* step is a stub for Phase 11+'s
       LLM-driven dialectic).
    4. **Emit events**: when ``dry_run=False``, turn surviving
       proposals into :class:`SchemaEditEvent` instances + return
       them. The caller (CLI) writes them to disk.

    All four stages run synchronously; no LLM calls in v0.0.52.
    """

    observation: MetaObservation
    min_cycles: int = DEFAULT_MIN_CYCLES
    target_failure: str | None = None  # filter to a specific Toulmin component
    dry_run: bool = True

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
            )

        proposals = tuple(self._generate_proposals())
        surviving = tuple(self._filter_proposals(proposals))
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
        )

    # ── proposal generation ──

    def _generate_proposals(self) -> list[SchemaEditProposal]:
        """v0.0.52 heuristics. Phase 11+ swaps in LLM-driven generation."""
        out: list[SchemaEditProposal] = []
        obs = self.observation

        # Heuristic 1: Toulmin failure dominance.
        # If one ``broken_component`` exceeds the threshold of all
        # counters, propose adding a schema edge that would type-check
        # the failure mode.
        total = sum(obs.toulmin_failure_counts.values())
        if total > 0:
            for component, count in obs.toulmin_failure_counts.items():
                if self.target_failure and component != self.target_failure:
                    continue
                if count / total < _TOULMIN_FAILURE_DOMINANCE_THRESHOLD:
                    continue
                proposal = _proposal_for_toulmin_dominance(component, count, total)
                if proposal is not None:
                    out.append(proposal)

        # Heuristic 2: unrealised schema edge.
        # If a declared edge has zero corpus instances, propose
        # retracting it. Conservative — only retract when ≥ 50 cycles
        # have run (the corpus has had enough chance to populate).
        if obs.cycles_examined >= 50:
            for edge in obs.unrealised_schema_edges:
                # Don't retract core epistemic edges (FZ 1's 10);
                # they're load-bearing for the BB cycle.
                if edge in BB_SCHEMA_EPISTEMIC:
                    continue
                out.append(
                    SchemaEditProposal(
                        kind="retract",
                        edge=edge,
                        motivating_observation=(
                            f"Edge {edge.source.value} → {edge.target.value} "
                            f"({edge.label!r}) has zero corpus instances after "
                            f"{obs.cycles_examined} cycles."
                        ),
                        expected_impact="Smaller schema; fewer untyped reports.",
                    )
                )

        return out

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
    # no proposal for it in v0.0.52. Phase 11+ may add a learned mapping.
}


def _proposal_for_toulmin_dominance(
    component: str, count: int, total: int
) -> SchemaEditProposal | None:
    """v0.0.52's lookup-based heuristic proposer."""
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
    "load_event_log",
    "write_event_log",
]
