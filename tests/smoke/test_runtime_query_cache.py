"""P9 smoke tests — Tier A's resolved rows, Tier B's cache, and the feedback signal.

Covers each clause of the phase's acceptance line:

1. A negative verdict LOWERS or EVICTS a cached mapping **before** any
   reinforcement path is enabled — and the reinforcement path is proved
   default-off, both in the policy and end to end through the store.
2. η = (n_pass + 1) / (n_trial + 2) is computable for a claim with a REAL trial
   history (episodes recorded, verdicts applied, the last verdict per episode
   winning), and the "open correction flag" half of the gate is real state with a
   raise/release lifecycle.
3. Target-note precision WITH vs. WITHOUT the cache is measured by a harness that
   returns the comparison, including the case where the cache lowers it.

Plus the properties those clauses rest on: both tables are evictable rebuildable
projections (dropping the cache leaves η intact), replaying a verdict stream does
not demote twice, re-deriving a demoted mapping cannot launder its standing back
up, and the ``origin='resolved'`` Tier-A layer neither writes through nor deletes
through the authored seed's door.

All local-I/O over a temporary SQLite file; no network, no model. The Tier-A
``relations`` table is created from the shipped runtime schema (this phase
deliberately does not define it), and one test builds the sidecar's stricter
shape by hand to prove the column projection handles both.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import replace
from importlib.resources import files
from pathlib import Path

import pytest

from tessellum.dks.memory_tiers import (
    DEFAULT_FEEDBACK_POLICY,
    INITIAL_FEEDBACK_SCORE,
    RELIABILITY_FLOOR,
    REPRESENTATIONS,
    SOURCE_EXPLICIT_THUMB,
    SOURCE_REVIEWED_QA,
    TIERS,
    CorrectionFlag,
    FeedbackEvent,
    FeedbackEventError,
    FeedbackPolicy,
    PrecisionProbe,
    ResolvedRelation,
    StaticVerdictSource,
    compare_target_note_precision,
    has_open_correction,
    is_rebuildable_projection,
    meets_reliability_gate,
    pack_embedding,
    precision,
    query_key_for,
    reliability,
    score_after,
    tally_trials,
    unpack_embedding,
)
from tessellum.runtime.query_cache import (
    QUERY_CACHE_SCHEMA,
    QueryCacheError,
    QueryCacheStore,
)

QUERY_CACHE_SOURCE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "tessellum"
    / "runtime"
    / "query_cache.py"
)

MEMORY_TIERS_SOURCE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "tessellum"
    / "dks"
    / "memory_tiers.py"
)


# ── helpers ─────────────────────────────────────────────────────────────────


def _store(tmp_path: Path, *, with_relations: bool = False) -> QueryCacheStore:
    """A store on its own file, optionally carrying the Tier-A table.

    The ``relations`` table comes from the shipped runtime schema rather than
    from this module: P9 writes the resolved layer, it does not own the table."""
    path = tmp_path / "memory.db"
    if with_relations:
        schema = (
            files("tessellum.runtime").joinpath("schema.sql").read_text(encoding="utf-8")
        )
        conn = sqlite3.connect(path)
        try:
            conn.executescript(schema)
        finally:
            conn.close()
    return QueryCacheStore.open(path)


def _seeded(tmp_path: Path) -> tuple[QueryCacheStore, str]:
    """A store holding one freshly derived mapping at full standing."""
    store = _store(tmp_path)
    key = query_key_for("Which note defines the retention window?")
    store.put_mapping(key, ("note-a", "note-b"), now=1_000.0)
    return store, key


# ── the two vocabularies, kept apart ───────────────────────────────────────


def test_tier_and_representation_vocabularies_are_distinct() -> None:
    assert set(TIERS) == {"A", "B", "C"}
    assert set(REPRESENTATIONS) == {"working", "log", "graph"}
    # Tier A and Tier B are rebuildable projections; Tier C is durable.
    assert is_rebuildable_projection("A") and is_rebuildable_projection("B")
    assert not is_rebuildable_projection("C")
    # Only Tier B is demotable by feedback — that is what this phase adds.
    assert TIERS["B"].demotable and not TIERS["A"].demotable
    # The log is the only of-record representation; working is discarded.
    assert REPRESENTATIONS["log"].of_record_for_epistemics
    assert not REPRESENTATIONS["working"].of_record_for_epistemics
    assert REPRESENTATIONS["working"].discarded_at_commit
    with pytest.raises(ValueError):
        is_rebuildable_projection("B2")


def test_query_key_is_deterministic_and_model_free() -> None:
    assert query_key_for("  Who Owns  the Index? ") == query_key_for("who owns the index?")
    assert query_key_for("a") != query_key_for("b")


def test_embeddings_round_trip_without_becoming_the_key() -> None:
    blob = pack_embedding([0.5, -0.25, 0.125])
    assert unpack_embedding(blob) == (0.5, -0.25, 0.125)
    assert unpack_embedding(None) == ()  # absent, not zeros


# ── clause 1: demotion first, reinforcement default-off ─────────────────────


def test_reinforcement_is_default_off_in_the_policy() -> None:
    """The switch itself: the shipped default cannot reinforce."""
    assert DEFAULT_FEEDBACK_POLICY.reinforcement_enabled is False
    assert FeedbackPolicy().reinforcement_enabled is False
    held = score_after(0.5, "correct")
    assert held.action == "hold"
    assert held.score == 0.5
    assert "default-off" in held.reason
    enabled = score_after(0.5, "correct", policy=FeedbackPolicy(reinforcement_enabled=True))
    assert enabled.action == "reinforce"
    assert enabled.score == 0.75


def test_negative_verdict_lowers_then_evicts_a_cached_mapping(tmp_path: Path) -> None:
    """Clause 1, end to end: demotion works while reinforcement is still off."""
    store, key = _seeded(tmp_path)
    assert store.cached_targets(key).feedback_score == INITIAL_FEEDBACK_SCORE

    first = store.apply_verdict(
        subject_id=key,
        subject_kind="cached_mapping",
        episode_id="episode-1",
        verdict="incorrect",
        at=1_001.0,
    )
    assert first.action == "demote"
    assert first.previous_score == 1.0 and first.score == 0.5
    assert first.evicted is False
    assert store.cached_targets(key).feedback_score == 0.5

    second = store.apply_verdict(
        subject_id=key,
        subject_kind="cached_mapping",
        episode_id="episode-2",
        verdict="incorrect",
        at=1_002.0,
    )
    assert second.action == "evict"
    assert second.evicted is True
    assert store.cached_targets(key) is None

    # and the reinforcement path never ran on the way there
    assert DEFAULT_FEEDBACK_POLICY.reinforcement_enabled is False


def test_a_single_negative_verdict_can_evict_outright(tmp_path: Path) -> None:
    """"Lower OR evict": a strict policy evicts on the first negative."""
    store, key = _seeded(tmp_path)
    outcome = store.apply_verdict(
        subject_id=key,
        subject_kind="cached_mapping",
        episode_id="episode-1",
        verdict="incorrect",
        at=1_001.0,
        policy=FeedbackPolicy(demotion_step=1.0),
    )
    assert outcome.action == "evict"
    assert store.mapping_count() == 0


def test_partial_verdict_demotes_less_than_incorrect(tmp_path: Path) -> None:
    store, key = _seeded(tmp_path)
    outcome = store.apply_verdict(
        subject_id=key,
        subject_kind="cached_mapping",
        episode_id="episode-1",
        verdict="partial",
        at=1_001.0,
    )
    assert outcome.action == "demote"
    assert outcome.score == 0.75


def test_positive_verdict_holds_the_score_by_default(tmp_path: Path) -> None:
    """A demoted mapping is not restored by praise while reinforcement is off."""
    store, key = _seeded(tmp_path)
    store.apply_verdict(
        subject_id=key,
        subject_kind="cached_mapping",
        episode_id="episode-1",
        verdict="incorrect",
        at=1_001.0,
    )
    outcome = store.apply_verdict(
        subject_id=key,
        subject_kind="cached_mapping",
        episode_id="episode-2",
        verdict="correct",
        at=1_002.0,
    )
    assert outcome.action == "hold"
    assert store.cached_targets(key).feedback_score == 0.5


def test_re_deriving_cannot_launder_away_a_demotion(tmp_path: Path) -> None:
    """A cache miss re-writing the mapping keeps the LOWER standing."""
    store, key = _seeded(tmp_path)
    store.apply_verdict(
        subject_id=key,
        subject_kind="cached_mapping",
        episode_id="episode-1",
        verdict="incorrect",
        at=1_001.0,
    )
    reput = store.put_mapping(key, ("note-a", "note-c"), now=1_010.0)
    assert reput.feedback_score == 0.5
    assert reput.target_note_ids == ("note-a", "note-c")
    assert reput.created_at == 1_000.0  # the original row's age survives
    # an explicit eviction is the only way back to full standing
    assert store.evict(key) is True
    fresh = store.put_mapping(key, ("note-a",), now=1_020.0)
    assert fresh.feedback_score == INITIAL_FEEDBACK_SCORE


def test_replaying_a_verdict_stream_does_not_demote_twice(tmp_path: Path) -> None:
    store, key = _seeded(tmp_path)
    source = StaticVerdictSource(
        (
            FeedbackEvent(
                kind="verdict",
                subject_id=key,
                subject_kind="cached_mapping",
                episode_id="episode-1",
                at=1_001.0,
                verdict="incorrect",
                source=SOURCE_EXPLICIT_THUMB,
            ),
        )
    )
    first = store.ingest_verdicts(source)
    assert [outcome.action for outcome in first] == ["demote"]
    second = store.ingest_verdicts(source)
    assert [outcome.action for outcome in second] == ["hold"]
    assert "no-op" in second[0].reason
    assert store.cached_targets(key).feedback_score == 0.5
    # the replay reports the flag the first pass raised rather than a fresh one
    assert second[0].correction_flag_id == first[0].correction_flag_id
    assert len(store.correction_flags(subject_id=key)) == 1


def test_the_verdict_source_is_an_injected_adapter(tmp_path: Path) -> None:
    """The feedback source is a port a deployment implements — no collector ships.

    Two source labels are shipped as generic constants (a reviewed
    question-and-answer stream and an explicit thumb); the stream itself comes
    from whatever the deployment already collects."""
    store, key = _seeded(tmp_path)

    class _DeploymentStream:
        """A deployment's own adapter — duck-typed against ``VerdictSource``."""

        def verdicts(self, *, since: float | None = None) -> tuple[FeedbackEvent, ...]:
            events = (
                FeedbackEvent(
                    kind="trial",
                    subject_id=key,
                    subject_kind="cached_mapping",
                    episode_id="episode-1",
                    at=1_001.0,
                ),
                FeedbackEvent(
                    kind="verdict",
                    subject_id=key,
                    subject_kind="cached_mapping",
                    episode_id="episode-1",
                    at=1_002.0,
                    verdict="incorrect",
                    source=SOURCE_REVIEWED_QA,
                ),
            )
            return tuple(e for e in events if since is None or e.at > since)

    outcomes = store.ingest_verdicts(_DeploymentStream())
    assert [outcome.action for outcome in outcomes] == ["demote"]
    assert {event.kind for event in store.events(subject_id=key)} == {
        "trial",
        "verdict",
        "correction_raise",
    }
    # the watermark is honoured, so a later pull re-reads nothing
    assert _DeploymentStream().verdicts(since=1_002.0) == ()


# ── clause 2: η over a real trial history, and the correction flag ──────────


def test_eta_is_the_laplace_smoothed_ratio() -> None:
    assert reliability(0, 0) == 0.5  # no history: fail-closed, under the floor
    assert reliability(1, 1) == pytest.approx(2 / 3)
    assert reliability(8, 8) == pytest.approx(0.9)
    assert reliability(8, 10) == 0.75
    assert reliability(0, 0) < RELIABILITY_FLOOR
    with pytest.raises(ValueError):
        reliability(2, 1)
    with pytest.raises(ValueError):
        reliability(-1, 3)


def test_eta_is_computable_for_a_claim_with_a_real_trial_history(tmp_path: Path) -> None:
    """Clause 2: a promoted claim, ten adjudicated episodes, η read off the log."""
    store = _store(tmp_path)
    claim = "derivation-3f1c"
    for index in range(10):
        episode = f"episode-{index}"
        store.record_trial(
            subject_id=claim,
            subject_kind="promoted_claim",
            episode_id=episode,
            at=2_000.0 + index,
        )
        store.apply_verdict(
            subject_id=claim,
            subject_kind="promoted_claim",
            episode_id=episode,
            verdict="correct" if index < 8 else "incorrect",
            at=2_100.0 + index,
        )
    # an eleventh episode used the claim and was never judged: coverage, not failure
    store.record_trial(
        subject_id=claim,
        subject_kind="promoted_claim",
        episode_id="episode-unjudged",
        at=2_200.0,
    )

    history = store.trial_history(claim)
    assert (history.n_trial, history.n_pass, history.n_fail) == (10, 8, 2)
    assert history.n_unadjudicated == 1
    assert history.coverage == pytest.approx(10 / 11)
    assert history.eta == pytest.approx(0.75)
    assert store.reliability(claim) == pytest.approx(0.75)
    # below the floor, and an open flag from each negative verdict
    assert not meets_reliability_gate(history)
    assert history.has_open_correction


def test_a_promoted_claim_has_no_mapping_to_score(tmp_path: Path) -> None:
    """Demoting a promoted claim is the re-derivation gate's act, not the cache's."""
    store = _store(tmp_path)
    outcome = store.apply_verdict(
        subject_id="derivation-9a",
        subject_kind="promoted_claim",
        episode_id="episode-1",
        verdict="incorrect",
        at=3_000.0,
    )
    assert outcome.action == "hold"
    assert "no cached mapping" in outcome.reason
    assert outcome.score is None
    assert outcome.correction_flag_id is not None
    assert store.reliability("derivation-9a") == pytest.approx(1 / 3)


def test_the_last_verdict_per_episode_wins(tmp_path: Path) -> None:
    """A correction supersedes an earlier judgement; counts never inflate."""
    store = _store(tmp_path)
    claim = "derivation-7b"
    store.apply_verdict(
        subject_id=claim,
        subject_kind="promoted_claim",
        episode_id="episode-1",
        verdict="correct",
        at=4_000.0,
    )
    store.apply_verdict(
        subject_id=claim,
        subject_kind="promoted_claim",
        episode_id="episode-1",
        verdict="incorrect",
        at=4_050.0,
        detail="reviewer corrected the earlier pass",
    )
    history = store.trial_history(claim)
    assert history.n_trial == 1
    assert (history.n_pass, history.n_fail) == (0, 1)


def test_the_correction_flag_is_real_state_with_a_lifecycle(tmp_path: Path) -> None:
    """Clause 2's second half: the gate's "no open correction flag" condition."""
    store, key = _seeded(tmp_path)
    assert store.has_open_correction(key) is False

    outcome = store.apply_verdict(
        subject_id=key,
        subject_kind="cached_mapping",
        episode_id="episode-1",
        verdict="incorrect",
        at=5_000.0,
    )
    flag_id = outcome.correction_flag_id
    assert flag_id is not None
    assert store.has_open_correction(key) is True
    assert has_open_correction(store.events(subject_id=key), subject_id=key)

    store.release_correction(flag_id, detail="mapping re-derived and reviewed", at=5_100.0)
    assert store.has_open_correction(key) is False
    flags = store.correction_flags(subject_id=key)
    assert len(flags) == 1  # released, not erased
    assert flags[0].is_open is False
    assert flags[0].released_at == 5_100.0
    with pytest.raises(QueryCacheError):
        store.release_correction("not-a-flag")


def test_an_open_flag_alone_fails_the_gate() -> None:
    """The two conditions are ANDed: high η does not outvote a reported error."""
    history = tally_trials(
        [
            FeedbackEvent(
                kind="verdict",
                subject_id="s",
                subject_kind="promoted_claim",
                episode_id=f"episode-{index}",
                at=float(index),
                verdict="correct",
            )
            for index in range(20)
        ],
        subject_id="s",
    )
    assert history.eta > RELIABILITY_FLOOR
    assert meets_reliability_gate(history)
    flagged = replace(
        history,
        open_corrections=(
            CorrectionFlag(
                flag_id="flag-1",
                subject_id="s",
                subject_kind="promoted_claim",
                episode_id="episode-1",
                raised_at=1.0,
                reason="reported wrong",
            ),
        ),
    )
    assert flagged.eta > RELIABILITY_FLOOR
    assert not meets_reliability_gate(flagged)


def test_a_malformed_feedback_event_is_refused_at_construction() -> None:
    with pytest.raises(FeedbackEventError):
        FeedbackEvent(
            kind="verdict",
            subject_id="s",
            subject_kind="promoted_claim",
            episode_id="e",
            at=0.0,
        )
    with pytest.raises(FeedbackEventError):
        FeedbackEvent(
            kind="trial",
            subject_id="s",
            subject_kind="promoted_claim",
            episode_id="e",
            at=0.0,
            verdict="correct",
        )
    with pytest.raises(FeedbackEventError):
        FeedbackEvent(
            kind="correction_release",
            subject_id="s",
            subject_kind="promoted_claim",
            episode_id="e",
            at=0.0,
        )
    with pytest.raises(FeedbackEventError):
        FeedbackEvent(
            kind="trial",
            subject_id="s",
            subject_kind="note",  # type: ignore[arg-type]
            episode_id="e",
            at=0.0,
        )


def test_the_feedback_table_mirrors_the_event_validation(tmp_path: Path) -> None:
    """The CHECK constraints are the same rule, enforced one layer down."""
    store = _store(tmp_path)
    conn = sqlite3.connect(store.path)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO feedback(feedback_id, kind, subject_id, subject_kind, "
                "episode_id, verdict, source, detail, releases, at, seq) "
                "VALUES ('x', 'verdict', 's', 'cached_mapping', 'e', NULL, 'r', '', NULL, 0, 1)"
            )
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO feedback(feedback_id, kind, subject_id, subject_kind, "
                "episode_id, verdict, source, detail, releases, at, seq) "
                "VALUES ('y', 'trial', 's', 'note', 'e', NULL, 'r', '', NULL, 0, 2)"
            )
    finally:
        conn.close()


# ── clause 3: the precision harness ────────────────────────────────────────


def test_precision_scores_an_empty_retrieval_as_zero() -> None:
    assert precision((), ("note-a",)) == 0.0
    assert precision(("note-a", "note-b"), ("note-a",)) == 0.5
    assert precision(("note-a",), ("note-a", "note-b")) == 1.0


def test_target_note_precision_is_measured_with_and_without_the_cache(
    tmp_path: Path,
) -> None:
    """Clause 3: the harness returns the comparison, over live cache rows."""
    store = _store(tmp_path)
    hit = query_key_for("which note holds the retention window?")
    miss = query_key_for("which note holds the escalation path?")
    store.put_mapping(hit, ("note-a",), query_embedding=pack_embedding([0.1, 0.2]), now=1.0)

    probes = (
        PrecisionProbe(
            query_key=hit,
            relevant_note_ids=("note-a",),
            uncached_note_ids=("note-x", "note-a", "note-y"),
        ),
        PrecisionProbe(
            query_key=miss,
            relevant_note_ids=("note-b",),
            uncached_note_ids=("note-b", "note-z"),
        ),
    )
    comparison = store.measure_target_note_precision(probes)
    assert comparison.episodes == 2
    assert comparison.cache_hits == 1
    assert comparison.cache_hit_rate == 0.5
    # cached arm: 1.0 (exact) and 0.5 (miss falls through to retrieval)
    assert comparison.precision_with_cache == pytest.approx(0.75)
    assert comparison.precision_without_cache == pytest.approx((1 / 3 + 0.5) / 2)
    assert comparison.delta > 0


def test_the_harness_reports_a_cache_that_lowers_precision() -> None:
    """A signed delta: a harmful cache must be visible as a negative number."""
    comparison = compare_target_note_precision(
        (
            PrecisionProbe(
                query_key="k",
                relevant_note_ids=("note-a",),
                uncached_note_ids=("note-a",),
                cached_note_ids=("note-a", "note-wrong"),
            ),
        )
    )
    assert comparison.precision_with_cache == 0.5
    assert comparison.precision_without_cache == 1.0
    assert comparison.delta == -0.5


def test_the_harness_is_defined_on_an_empty_probe_set() -> None:
    comparison = compare_target_note_precision(())
    assert comparison.episodes == 0
    assert comparison.cache_hit_rate == 0.0
    assert comparison.delta == 0.0


# ── both tables are evictable rebuildable projections ──────────────────────


def test_hits_are_counted_and_a_miss_reports_itself(tmp_path: Path) -> None:
    store, key = _seeded(tmp_path)
    used = store.record_hit(key, episode_id="episode-1", now=6_000.0)
    assert used is not None
    assert (used.hits, used.last_used) == (1, 6_000.0)
    assert store.record_hit("no-such-key") is None
    history = store.trial_history(key)
    assert (history.n_trial, history.n_unadjudicated) == (0, 1)


def test_dropping_the_cache_costs_latency_not_knowledge(tmp_path: Path) -> None:
    """The evictability proof: η and the flags survive a full cache drop."""
    store, key = _seeded(tmp_path)
    store.record_hit(key, episode_id="episode-1", now=7_000.0)
    store.apply_verdict(
        subject_id=key,
        subject_kind="cached_mapping",
        episode_id="episode-1",
        verdict="correct",
        at=7_001.0,
    )
    before = store.trial_history(key)

    assert store.drop_cache() == 1
    assert store.cached_targets(key) is None
    after = store.trial_history(key)
    assert after == before
    assert after.eta == pytest.approx(2 / 3)


def test_stale_and_low_standing_mappings_are_evictable(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.put_mapping("old", ("note-a",), now=1.0)
    store.put_mapping("fresh", ("note-b",), now=9_000.0)
    store.put_mapping("weak", ("note-c",), feedback_score=0.0, now=9_000.0)
    assert store.evict_stale() == ()  # no bound given: evicts nothing
    assert store.evict_stale(unused_since=100.0) == ("old",)
    assert store.evict_stale(at_or_below_score=0.0) == ("weak",)
    assert store.mapping_count() == 1


def test_the_feedback_log_is_evictable_and_re_ingestible(tmp_path: Path) -> None:
    """A projection of the deployment's stream: drop it, re-pull it, same state."""
    store = _store(tmp_path)
    claim = "derivation-2c"
    source = StaticVerdictSource(
        tuple(
            FeedbackEvent(
                kind="verdict",
                subject_id=claim,
                subject_kind="promoted_claim",
                episode_id=f"episode-{index}",
                at=8_000.0 + index,
                verdict="correct",
            )
            for index in range(4)
        )
    )
    store.ingest_verdicts(source)
    seeded = store.trial_history(claim)
    assert seeded.n_trial == 4

    assert store.evict_feedback_before(9_000.0) == 4
    assert store.trial_history(claim).n_trial == 0
    assert store.reliability(claim) == 0.5  # back to the fail-closed prior

    store.ingest_verdicts(source)
    assert store.trial_history(claim) == seeded


# ── Tier A: the resolved layer on top of the authored seed ──────────────────


def _authored_row(path: Path, subject_id: str) -> None:
    """One ``origin='authored'`` row, written the way the registry projects it.

    Every column the reconciled Tier-A definition requires is supplied, including
    ``object_kind`` — there is one ``relations`` shape now, so a fixture that
    omitted a required column would be asserting against a schema that no longer
    exists."""
    conn = sqlite3.connect(path)
    try:
        conn.execute(
            "INSERT INTO relations(relation_id, subject_id, predicate, object_ref, "
            "object_kind, evidence_note, evidence_locator, origin) "
            "VALUES ('authored-1', ?, 'documented_in', 'note-seed', 'entity', ?, "
            "'frontmatter:documented_in', 'authored')",
            (subject_id, subject_id),
        )
        conn.commit()
    finally:
        conn.close()


def test_resolved_rows_layer_on_the_authored_seed(tmp_path: Path) -> None:
    """Tier A completion: rows written on a cache miss, ``origin='resolved'``."""
    store = _store(tmp_path, with_relations=True)
    _authored_row(store.path, "note-subject")

    derived = ResolvedRelation(
        subject_id="note-subject",
        predicate="documented_in",
        object_ref="note-target",
        evidence_note="note-subject",
        evidence_locator="span:120-190",
        valid_from="2020-01-01",
    )
    relation_id = store.record_resolved_relation(derived)
    assert store.record_resolved_relation(derived) == relation_id  # idempotent

    resolved = store.resolved_relations_for("note-subject")
    assert len(resolved) == 1
    assert resolved[0].object_ref == "note-target"
    assert resolved[0].valid_from == "2020-01-01"  # the interval is not optional
    assert resolved[0].origin == "resolved"
    assert store.resolved_relations_for("note-subject", "no-such-predicate") == ()

    # the authored seed is untouched by both the write and the eviction
    assert store.evict_resolved_relations() == 1
    assert store.resolved_relations_for("note-subject") == ()
    conn = sqlite3.connect(store.path)
    try:
        remaining = conn.execute("SELECT origin FROM relations").fetchall()
    finally:
        conn.close()
    assert [origin for (origin,) in remaining] == ["authored"]


def test_a_superseded_resolved_row_is_not_returned(tmp_path: Path) -> None:
    """Recency: a role-style relation must not return a former holder."""
    store = _store(tmp_path, with_relations=True)
    former = ResolvedRelation(
        subject_id="note-subject",
        predicate="maintained_by",
        object_ref="entity-old",
        evidence_locator="span:1-40",
        valid_to="2021-06-30",
    )
    current = ResolvedRelation(
        subject_id="note-subject",
        predicate="maintained_by",
        object_ref="entity-new",
        evidence_locator="span:41-80",
        valid_from="2021-07-01",
    )
    store.record_resolved_relation(former)
    store.record_resolved_relation(current)
    assert len(store.resolved_relations_for("note-subject", "maintained_by")) == 2
    assert store.supersede_resolved_relation(
        former.relation_id, superseded_by=current.relation_id
    )
    live = store.resolved_relations_for("note-subject", "maintained_by")
    assert [relation.object_ref for relation in live] == ["entity-new"]
    # an authored row is not supersedable through this door
    _authored_row(store.path, "note-other")
    assert store.supersede_resolved_relation(
        "authored-1", superseded_by=current.relation_id
    ) is False


def test_the_authored_origin_cannot_ride_in_through_this_door(tmp_path: Path) -> None:
    store = _store(tmp_path, with_relations=True)
    smuggled = replace(
        ResolvedRelation(
            subject_id="note-subject",
            predicate="documented_in",
            object_ref="note-target",
            evidence_locator="span:1-2",
        ),
        origin="authored",  # type: ignore[arg-type]
    )
    with pytest.raises(QueryCacheError, match="resolved"):
        store.record_resolved_relation(smuggled)


def test_a_missing_tier_a_table_is_reported_not_guessed(tmp_path: Path) -> None:
    store = _store(tmp_path)  # no relations table on this file
    with pytest.raises(QueryCacheError, match="relations"):
        store.record_resolved_relation(
            ResolvedRelation(
                subject_id="s", predicate="p", object_ref="o", evidence_locator="l"
            )
        )


def test_the_resolved_write_projects_onto_the_stricter_relations_shape(
    tmp_path: Path,
) -> None:
    """Two ``relations`` shapes are in the tree; the write handles both.

    The sidecar registry's table additionally carries ``object_kind`` and NOT
    NULL evidence columns. Built by hand here rather than imported, so this test
    does not depend on another phase's module."""
    path = tmp_path / "sidecar.db"
    conn = sqlite3.connect(path)
    try:
        conn.executescript(
            """
            CREATE TABLE relations (
                relation_id      TEXT PRIMARY KEY,
                subject_id       TEXT NOT NULL,
                predicate        TEXT NOT NULL,
                object_ref       TEXT NOT NULL,
                object_kind      TEXT NOT NULL CHECK (object_kind IN ('entity', 'literal')),
                valid_from       TEXT,
                valid_to         TEXT,
                evidence_note    TEXT NOT NULL,
                evidence_locator TEXT NOT NULL,
                epistemic_status TEXT,
                origin           TEXT NOT NULL CHECK (
                    origin IN ('authored', 'extracted', 'resolved')
                ),
                superseded_by    TEXT,
                content_hash     TEXT
            );
            """
        )
        conn.commit()
    finally:
        conn.close()
    store = QueryCacheStore.open(path)
    store.record_resolved_relation(
        ResolvedRelation(
            subject_id="note-subject",
            predicate="documented_in",
            object_ref="entity-1",
            object_kind="entity",
            evidence_note="note-subject",
            evidence_locator="span:5-9",
        )
    )
    resolved = store.resolved_relations_for("note-subject")
    assert len(resolved) == 1
    assert resolved[0].object_kind == "entity"


def test_a_relations_table_needing_unknown_columns_is_reported(tmp_path: Path) -> None:
    """Schema drift surfaces here, not as an integrity error three frames down."""
    path = tmp_path / "drifted.db"
    conn = sqlite3.connect(path)
    try:
        conn.executescript(
            """
            CREATE TABLE relations (
                relation_id TEXT PRIMARY KEY,
                subject_id  TEXT NOT NULL,
                predicate   TEXT NOT NULL,
                object_ref  TEXT NOT NULL,
                origin      TEXT NOT NULL,
                tenant_id   TEXT NOT NULL
            );
            """
        )
        conn.commit()
    finally:
        conn.close()
    store = QueryCacheStore.open(path)
    with pytest.raises(QueryCacheError, match="tenant_id"):
        store.record_resolved_relation(
            ResolvedRelation(
                subject_id="s", predicate="p", object_ref="o", evidence_locator="l"
            )
        )


# ── the module's own discipline ─────────────────────────────────────────────


def test_the_pure_tier_module_does_not_import_the_runtime() -> None:
    """The Dependency Rule, checked on the source rather than asserted."""
    source = MEMORY_TIERS_SOURCE.read_text(encoding="utf-8")
    assert "tessellum.runtime" not in source
    assert "sqlite3" not in source


def test_the_store_never_writes_the_append_only_log() -> None:
    """Eviction is legal for a projection and illegal for the claim/edge log."""
    source = QUERY_CACHE_SOURCE.read_text(encoding="utf-8")
    written = set(
        re.findall(
            r"\b(?:INSERT(?:\s+OR\s+\w+)?\s+INTO|UPDATE|DELETE\s+FROM)\s+(\w+)", source
        )
    )
    assert written  # this module does write — to its own projections
    assert written == {"query_cache", "feedback", "relations"}
    assert not written & {"claims", "edges", "status_cache", "jobs", "job_events"}


def test_the_schema_defines_only_the_two_new_tables() -> None:
    """P9 writes the Tier-A table; it deliberately does not define it."""
    created = {
        line.split("IF NOT EXISTS")[1].strip().rstrip("(").strip()
        for line in QUERY_CACHE_SCHEMA.splitlines()
        if line.startswith("CREATE TABLE")
    }
    assert created == {"query_cache", "feedback"}
    assert "CREATE TABLE IF NOT EXISTS relations" not in QUERY_CACHE_SCHEMA


def test_opening_the_store_twice_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / "memory.db"
    QueryCacheStore.open(path).put_mapping("k", ("note-a",), now=1.0)
    reopened = QueryCacheStore.open(path)
    assert reopened.cached_targets("k").target_note_ids == ("note-a",)
