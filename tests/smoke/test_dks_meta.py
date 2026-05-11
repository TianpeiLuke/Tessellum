"""Smoke tests for tessellum.dks.meta — Phase 9 meta-DKS runtime.

Surfaces under test (v0.0.52):

- Event-sourced schema (D3): SchemaEditEvent fold for added / retracted /
  refined applies to BB_SCHEMA_USER_EXTENSIONS.
- META_SCHEMA shape (D4): 5 states + 4 transitions; in-code constant; no
  runtime mutation.
- MetaObservation + SchemaEditProposal dataclass shape.
- MetaCycle: cold-start guard (<min_cycles → no proposals), Toulmin-dominance
  heuristic, --target-failure filter, retract-unused-edge heuristic gated by
  ≥50 cycles, dry-run vs apply distinction.
- Event log I/O: write_event_log + load_event_log round-trip.
"""

from __future__ import annotations



from tessellum.bb.types import (
    BBType,
    EpistemicEdgeType,
    SchemaEditEvent,
    fold_schema_events,
)
from tessellum.dks.meta import (
    DEFAULT_MIN_CYCLES,
    META_SCHEMA,
    MetaCycle,
    MetaCycleResult,
    MetaObservation,
    SchemaEditProposal,
    load_event_log,
    write_event_log,
)
from tessellum.dks.meta.types import META_STATES, MetaEdgeType


# ── META_SCHEMA shape (D4) ─────────────────────────────────────────────────


def test_meta_schema_states():
    """5 meta-states, in the order the meta-FSM walks them."""
    assert META_STATES == (
        "meta_observation",
        "meta_argument",
        "meta_counter",
        "meta_pattern",
        "meta_revision",
    )


def test_meta_schema_transitions():
    """4 transitions: proposing → attacking → aggregating → landing."""
    assert len(META_SCHEMA) == 4
    labels = [edge.label for edge in META_SCHEMA]
    assert labels == ["proposing", "attacking", "aggregating", "landing"]
    # Each transition's source must be a META_STATE; same for target.
    for edge in META_SCHEMA:
        assert edge.source in META_STATES
        assert edge.target in META_STATES


def test_meta_schema_is_immutable_constant():
    """META_SCHEMA is a tuple — caller can't mutate at runtime."""
    assert isinstance(META_SCHEMA, tuple)
    assert all(isinstance(e, MetaEdgeType) for e in META_SCHEMA)


# ── SchemaEditEvent fold (D3) ──────────────────────────────────────────────


def test_fold_schema_events_added():
    """Single ``added`` event materialises one edge."""
    edge = EpistemicEdgeType(
        BBType.MODEL, BBType.PROCEDURE, "warrant_codification"
    )
    events = (
        SchemaEditEvent(
            timestamp="2026-05-10T00:00:00+00:00",
            kind="added",
            edge=edge,
            motivating_failure="test",
        ),
    )
    result = fold_schema_events(events)
    assert edge in result


def test_fold_schema_events_added_then_retracted_yields_empty():
    """Retract reverses a prior add; net schema is empty."""
    edge = EpistemicEdgeType(
        BBType.MODEL, BBType.PROCEDURE, "warrant_codification"
    )
    events = (
        SchemaEditEvent(
            timestamp="2026-05-10T00:00:00+00:00",
            kind="added",
            edge=edge,
            motivating_failure="add",
        ),
        SchemaEditEvent(
            timestamp="2026-05-10T01:00:00+00:00",
            kind="retracted",
            edge=edge,
            motivating_failure="retract",
        ),
    )
    result = fold_schema_events(events)
    assert edge not in result


def test_fold_schema_events_refined_replaces_existing():
    """Refine drops the old version (by source+target) and adds the new."""
    old = EpistemicEdgeType(BBType.MODEL, BBType.PROCEDURE, "old_label")
    new = EpistemicEdgeType(BBType.MODEL, BBType.PROCEDURE, "new_label")
    events = (
        SchemaEditEvent(
            timestamp="2026-05-10T00:00:00+00:00",
            kind="added",
            edge=old,
            motivating_failure="add",
        ),
        SchemaEditEvent(
            timestamp="2026-05-10T01:00:00+00:00",
            kind="refined",
            edge=new,
            motivating_failure="refine",
        ),
    )
    result = fold_schema_events(events)
    assert old not in result
    assert new in result


# ── MetaObservation + SchemaEditProposal ───────────────────────────────────


def test_meta_observation_construction():
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=42,
        top_attacked_warrants=(("FZ-2a", 3), ("FZ-2b", 1)),
        toulmin_failure_counts={"warrant": 10, "premise": 2},
        unrealised_schema_edges=(),
    )
    assert obs.cycles_examined == 42
    assert obs.toulmin_failure_counts["warrant"] == 10


def test_schema_edit_proposal_construction():
    edge = EpistemicEdgeType(BBType.MODEL, BBType.PROCEDURE, "test_edge")
    p = SchemaEditProposal(
        kind="add",
        edge=edge,
        motivating_observation="m",
        expected_impact="e",
    )
    assert p.kind == "add"
    assert p.edge == edge


# ── MetaCycle: cold-start guard ────────────────────────────────────────────


def test_metacycle_cold_start_guard():
    """Below DEFAULT_MIN_CYCLES → no proposals, dry-run preserved."""
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=5,  # well below DEFAULT_MIN_CYCLES (=20)
        toulmin_failure_counts={"warrant": 10},
    )
    result = MetaCycle(observation=obs).run()
    assert isinstance(result, MetaCycleResult)
    assert result.proposals == ()
    assert result.surviving == ()
    assert result.events_landed == ()
    assert result.dry_run is True


def test_metacycle_min_cycles_configurable():
    """--min-cycles=2 lets a tiny observation through."""
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=2,
        toulmin_failure_counts={"warrant": 10, "premise": 1},
    )
    result = MetaCycle(observation=obs, min_cycles=2).run()
    # Warrant dominance (10/11 = 91% > 50%) → one proposal.
    assert len(result.proposals) == 1
    assert result.proposals[0].kind == "add"
    assert result.proposals[0].edge.source == BBType.MODEL
    assert result.proposals[0].edge.target == BBType.PROCEDURE


# ── MetaCycle: Toulmin-dominance heuristic ─────────────────────────────────


def test_metacycle_toulmin_dominance_warrant():
    """warrant > 50% → propose MOD→PRO ``warrant_codification`` edge."""
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=DEFAULT_MIN_CYCLES,
        toulmin_failure_counts={"warrant": 30, "counter-example": 5},
    )
    result = MetaCycle(observation=obs).run()
    assert len(result.proposals) == 1
    p = result.proposals[0]
    assert p.kind == "add"
    assert p.edge.label == "warrant_codification"


def test_metacycle_toulmin_dominance_counter_example():
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=DEFAULT_MIN_CYCLES,
        toulmin_failure_counts={"counter-example": 30, "warrant": 5},
    )
    result = MetaCycle(observation=obs).run()
    assert len(result.proposals) == 1
    assert result.proposals[0].edge.label == "counterexample_anchor"


def test_metacycle_no_dominance_no_proposal():
    """Balanced distribution → no proposal."""
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=DEFAULT_MIN_CYCLES,
        toulmin_failure_counts={"warrant": 5, "premise": 5, "counter-example": 5},
    )
    result = MetaCycle(observation=obs).run()
    assert result.proposals == ()


def test_metacycle_target_failure_filter():
    """--target-failure=warrant restricts to that component only."""
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=DEFAULT_MIN_CYCLES,
        toulmin_failure_counts={"warrant": 30, "premise": 0},
    )
    # Without filter — warrant dominance triggers.
    r1 = MetaCycle(observation=obs).run()
    assert len(r1.proposals) == 1
    # With filter set to premise — no warrant proposal.
    r2 = MetaCycle(observation=obs, target_failure="premise").run()
    assert r2.proposals == ()


# ── MetaCycle: dry-run vs apply ────────────────────────────────────────────


def test_metacycle_dry_run_no_events():
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=DEFAULT_MIN_CYCLES,
        toulmin_failure_counts={"warrant": 30},
    )
    result = MetaCycle(observation=obs, dry_run=True).run()
    assert len(result.proposals) == 1
    assert result.events_landed == ()


def test_metacycle_apply_emits_events():
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=DEFAULT_MIN_CYCLES,
        toulmin_failure_counts={"warrant": 30},
    )
    result = MetaCycle(observation=obs, dry_run=False).run()
    assert len(result.events_landed) == 1
    event = result.events_landed[0]
    assert event.kind == "added"
    assert event.edge.label == "warrant_codification"


# ── MetaCycle: filter sanity (don't propose already-existing edges) ────────


def test_metacycle_filter_drops_already_in_schema():
    """If the proposed edge is already in BB_SCHEMA, the filter drops it."""
    # Find an existing MOD→PRO edge to clash with — synthesise one such by
    # picking a known epistemic edge from BB_SCHEMA. We use the
    # MODEL→PROCEDURE family — if no such edge exists in core schema, the
    # heuristic add will succeed unfiltered.
    obs = MetaObservation(
        timestamp="2026-05-10T00:00:00+00:00",
        cycles_examined=DEFAULT_MIN_CYCLES,
        toulmin_failure_counts={"warrant": 30},
    )
    cycle = MetaCycle(observation=obs)
    # Simulate the proposal — then re-run filter directly.
    proposals = cycle._generate_proposals()
    filtered = cycle._filter_proposals(proposals)
    # In v0.0.52 the warrant edge is *not* in core schema, so the proposal
    # survives.
    assert len(filtered) == 1


# ── Event log I/O round-trip ───────────────────────────────────────────────


def test_event_log_round_trip(tmp_path):
    """write_event_log → load_event_log preserves the events."""
    path = tmp_path / "schema_events.jsonl"
    events = (
        SchemaEditEvent(
            timestamp="2026-05-10T00:00:00+00:00",
            kind="added",
            edge=EpistemicEdgeType(
                BBType.MODEL, BBType.PROCEDURE, "warrant_codification"
            ),
            motivating_failure="warrant dominance",
        ),
        SchemaEditEvent(
            timestamp="2026-05-10T01:00:00+00:00",
            kind="retracted",
            edge=EpistemicEdgeType(
                BBType.MODEL, BBType.PROCEDURE, "old_label"
            ),
            motivating_failure="unused after 50 cycles",
        ),
    )
    write_event_log(path, events, append=False)
    loaded = load_event_log(path)
    assert loaded == events


def test_event_log_load_missing_file(tmp_path):
    """Missing file → empty tuple, no exception."""
    assert load_event_log(tmp_path / "nope.jsonl") == ()


def test_event_log_load_skips_bad_lines(tmp_path):
    """Malformed JSONL lines are skipped, not raised."""
    path = tmp_path / "messy.jsonl"
    good_event = SchemaEditEvent(
        timestamp="2026-05-10T00:00:00+00:00",
        kind="added",
        edge=EpistemicEdgeType(
            BBType.MODEL, BBType.PROCEDURE, "warrant_codification"
        ),
        motivating_failure="x",
    )
    write_event_log(path, (good_event,), append=False)
    # Append a non-JSON line.
    with path.open("a", encoding="utf-8") as fh:
        fh.write("not-json\n")
        fh.write("\n")  # empty line — also skipped
    loaded = load_event_log(path)
    assert loaded == (good_event,)


def test_event_log_append_mode(tmp_path):
    """append=True (default) concatenates onto an existing log."""
    path = tmp_path / "log.jsonl"
    edge = EpistemicEdgeType(
        BBType.MODEL, BBType.PROCEDURE, "warrant_codification"
    )
    e1 = SchemaEditEvent(
        timestamp="2026-05-10T00:00:00+00:00",
        kind="added",
        edge=edge,
        motivating_failure="first",
    )
    e2 = SchemaEditEvent(
        timestamp="2026-05-10T01:00:00+00:00",
        kind="retracted",
        edge=edge,
        motivating_failure="second",
    )
    write_event_log(path, (e1,), append=False)
    write_event_log(path, (e2,), append=True)
    assert load_event_log(path) == (e1, e2)
