"""P6 smoke tests — the three-call protocol↔memory boundary.

One test per clause of the phase's acceptance line:

1. A locator-less record is REFUSED (both a claim and an edge).
2. A record from a NON-CLAIM-ELIGIBLE note is refused — plus the other two
   admission conditions, since the gate has four and the audit found none.
3. A protocol CANNOT READ ITS OWN UNCOMMITTED PROPOSAL as evidence: neither
   ``retrieve`` nor ``status`` sees a staged record, the pin survives the
   episode's own append, and only the speculative (non-citable) read shows it.
4. A REPLAYED batch is a no-op.
5. A MEMOIZED CLAIM is returned by ``retrieve``, and the cache-hit rate and
   latency are reported.
6. EDITING A CITED NOTE flags the dependent claim.

Plus the properties those clauses rest on: the Dependency Rule (this module
never imports ``runtime``), the content-id parity that makes a staged edge able
to name a staged claim, the Tier-A validity filter, the effect-kind vocabulary
validated at ingestion, and the reuse of ``base_snapshot_id`` as the one pin.

The final section covers the narrower materializer gap the phase owns: a vault
write inside an episode is recoverable but VISIBLE, so a vault-reading step can
observe uncommitted output. Those tests live here rather than beside the other
materializer tests because this phase owns this file and not that one.

The runtime side is deliberately exercised for real: ``ClaimLog`` already
satisfies :class:`ClaimLogReader`, and :class:`_ClaimLogAppender` below is the
small effect→draft adapter the runtime still owes this boundary (reported as a
follow-up, not smuggled into ``runtime/`` from here).

All local; no network, no model.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Callable, Sequence

import pytest

from tessellum.composer.materializer import MaterializedOutput, materialize
from tessellum.dks.capability import (
    EFFECT_KINDS,
    CapabilityEffect,
    CapabilityResult,
    EffectKindError,
    validate_effect_kind,
    validate_effects,
)
from tessellum.dks.entity_registry import AuthoredRelation
from tessellum.dks.memory_port import (
    REASON_BAD_PROVENANCE,
    REASON_ENDPOINT_REFUSED,
    REASON_NOT_CLAIM_ELIGIBLE,
    REASON_NO_LOCATOR,
    REASON_NO_OPERATOR,
    STATUS_UNKNOWN,
    AdmissionError,
    BuildingBlockEligibility,
    ClaimLogReader,
    ClaimProposal,
    EdgeProposal,
    EpisodeMemory,
    LogAppendPort,
    MappingNoteSearch,
    MemoryPort,
    MemoryPortError,
    NoteHit,
    claim_content_id,
    edge_content_id,
    edgeset_digest,
    effect_for_proposal,
    grounded_status_labeller,
)
from tessellum.runtime.claim_log import (
    ClaimDraft,
    ClaimLog,
    EdgeDraft,
    claim_identity,
    edge_identity,
    text_digest,
)
from tessellum.runtime.claim_log import edgeset_digest as log_edgeset_digest

MEMORY_PORT_SOURCE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "tessellum"
    / "dks"
    / "memory_port.py"
)

NOTE_A = "note-a"
NOTE_B = "note-b"
NOTE_INDEX = "note-index"

BLOCKS = {
    NOTE_A: "argument",
    NOTE_B: "empirical_observation",
    NOTE_INDEX: "navigation",
}


# ── the runtime-side adapter this phase does not own ────────────────────────


class _ClaimLogAppender:
    """Render claim/edge effects into the append-only log.

    The effect→draft translation belongs in ``runtime`` (the boundary hands over
    :class:`CapabilityEffect`s so "the kernel never writes" holds at this seam
    too). It is written here so the tests exercise the real log rather than a
    stand-in; a runtime module owning it is the reported follow-up.
    """

    def __init__(self, log: ClaimLog) -> None:
        self._log = log
        self.batches: list[tuple[str, int]] = []

    def append_effects(
        self, effects: Sequence[CapabilityEffect], *, base_snapshot_id: str
    ) -> int:
        drafts: list[ClaimDraft | EdgeDraft] = []
        for effect in validate_effects(effects):
            payload = effect.payload
            if effect.kind == "claim":
                drafts.append(
                    ClaimDraft(
                        derivation_id=payload["derivation_id"],
                        text=payload["text"],
                        note_id=payload["note_id"],
                        locator=payload["locator"],
                        provenance=payload["provenance"],
                        source_note_hash=payload["source_note_hash"],
                    )
                )
            elif effect.kind == "edge":
                drafts.append(
                    EdgeDraft(
                        op=payload["op"],
                        src=payload["src"],
                        dst=payload["dst"],
                        origin=payload["origin"],
                        evidence_locator=payload["evidence_locator"],
                    )
                )
            else:  # pragma: no cover - the boundary emits only these two
                raise AssertionError(f"unexpected effect kind: {effect.kind}")
        appended = self._log.append(drafts).appended if drafts else 0
        self.batches.append((base_snapshot_id, appended))
        return appended


class _SteppingClock:
    """A monotonic clock that advances by a fixed step per read.

    Injected so a reported latency is an exact number rather than a flake."""

    def __init__(self, step_seconds: float = 0.001) -> None:
        self.step = step_seconds
        self.now = 0.0

    def __call__(self) -> float:
        self.now += self.step
        return self.now


class _Relations:
    """Tier-A read port over a fixed row set, keyed by subject."""

    def __init__(self, rows: Sequence[AuthoredRelation]) -> None:
        self.rows = tuple(rows)

    def relations_for(
        self, subject_id: str, predicate: str | None = None
    ) -> tuple[AuthoredRelation, ...]:
        return tuple(
            row
            for row in self.rows
            if row.subject_id == subject_id
            and (predicate is None or row.predicate == predicate)
        )


# ── helpers ────────────────────────────────────────────────────────────────


def _log(tmp_path: Path) -> ClaimLog:
    return ClaimLog.open(tmp_path / "runtime.db")


def _episode(
    log: ClaimLog,
    *,
    appender: LogAppendPort | None = None,
    note_search: Callable[..., Sequence[NoteHit]] | None = None,
    relations: _Relations | None = None,
    eligibility: BuildingBlockEligibility | None = None,
    clock: Callable[[], float] | None = None,
) -> EpisodeMemory:
    return EpisodeMemory(
        log,
        appender=appender if appender is not None else _ClaimLogAppender(log),
        note_search=note_search,
        relations=relations,
        eligibility=(
            eligibility
            if eligibility is not None
            else BuildingBlockEligibility(blocks=BLOCKS)
        ),
        clock=clock or _SteppingClock(),
    )


def _claim(
    name: str,
    text: str,
    *,
    note_id: str = NOTE_A,
    locator: str = "h2:Claim",
    provenance: str = "constructed",
    operator: str = "support",
    source_note_hash: str | None = "note-hash-1",
) -> ClaimProposal:
    return ClaimProposal(
        derivation_id=f"derivation-{name}",
        text=text,
        note_id=note_id,
        locator=locator,
        provenance=provenance,
        source_note_hash=source_note_hash,
        operator=operator,
    )


def _seed_supported_claim(tmp_path: Path) -> tuple[ClaimLog, str, str]:
    """A warranted claim on ``NOTE_A``, supported by evidence on ``NOTE_B``."""
    log = _log(tmp_path)
    memory = _episode(log)
    evidence = _claim("evidence", "The measurement was taken twice.", note_id=NOTE_B)
    subject = _claim("subject", "The second run reproduced the first.")
    memory.stage(
        evidence,
        subject,
        EdgeProposal(
            op="support",
            src=evidence.claim_id,
            dst=subject.claim_id,
            origin="query",
            evidence_locator=f"{NOTE_B}#h2:Claim",
        ),
    )
    outcome = memory.append_batch()
    assert outcome.appended == 3
    return log, evidence.claim_id, subject.claim_id


# ── the Dependency Rule and the content-id parity ──────────────────────────


def test_the_boundary_module_never_imports_the_runtime() -> None:
    source = MEMORY_PORT_SOURCE.read_text(encoding="utf-8")
    code = "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith("#")
    )
    body = code.split('"""', 2)[-1]  # drop the module docstring, which names it
    assert "tessellum.runtime" not in body
    assert "import sqlite3" not in body


def test_the_boundary_shares_the_logs_content_id_construction() -> None:
    """A staged edge names a staged claim by id BEFORE the append, so the two
    constructions have to agree or the foreign key refuses the batch."""
    derivation, text = "derivation-x", "The claim as written."
    assert claim_content_id(derivation, text) == claim_identity(
        derivation, text_digest(text)
    )
    assert edge_content_id("attack", "a", "b", "loc") == edge_identity(
        "attack", "a", "b", "loc"
    )
    assert edge_content_id("attack", "a", "b") == edge_identity("attack", "a", "b")


def test_the_episode_memory_satisfies_the_three_call_port(tmp_path: Path) -> None:
    memory = _episode(_log(tmp_path))
    assert isinstance(memory, MemoryPort)
    assert isinstance(memory._log, ClaimLogReader)


# ── gate (i), condition (a): an evidence locator ───────────────────────────


def test_a_locator_less_claim_is_refused(tmp_path: Path) -> None:
    log = _log(tmp_path)
    memory = _episode(log)
    memory.stage(_claim("no-locator", "A claim with nowhere to point.", locator=""))

    outcome = memory.append_batch()

    assert outcome.appended == 0
    assert outcome.admitted == ()
    assert [reason for _p, verdict in outcome.refused for reason in verdict.reasons] == [
        REASON_NO_LOCATOR
    ]
    assert log.read_claims() == ()


def test_a_locator_less_edge_is_refused(tmp_path: Path) -> None:
    log, evidence_id, subject_id = _seed_supported_claim(tmp_path)
    memory = _episode(log)
    memory.stage(
        EdgeProposal(
            op="attack",
            src=evidence_id,
            dst=subject_id,
            origin="query",
            evidence_locator=None,
        )
    )

    outcome = memory.append_batch()

    assert outcome.appended == 0
    assert outcome.refused[0][1].reasons == (REASON_NO_LOCATOR,)


def test_whitespace_is_not_a_locator(tmp_path: Path) -> None:
    memory = _episode(_log(tmp_path))
    verdict = memory.admit(_claim("blank", "A claim.", locator="   "))
    assert verdict.reasons == (REASON_NO_LOCATOR,)


# ── gate (i), condition (b): an operator label ─────────────────────────────


def test_a_claim_without_an_operator_label_is_refused(tmp_path: Path) -> None:
    log = _log(tmp_path)
    memory = _episode(log)
    memory.stage(_claim("unlabelled", "A claim nobody related to anything.", operator=""))

    outcome = memory.append_batch()

    assert outcome.appended == 0
    assert outcome.refused[0][1].reasons == (REASON_NO_OPERATOR,)
    assert log.read_claims() == ()


def test_an_operator_outside_the_closed_set_is_refused(tmp_path: Path) -> None:
    log, evidence_id, subject_id = _seed_supported_claim(tmp_path)
    memory = _episode(log)
    memory.stage(
        _claim("domain-op", "A claim.", operator="is_owned_by"),
        EdgeProposal(
            op="rebuts",
            src=evidence_id,
            dst=subject_id,
            origin="query",
            evidence_locator="loc",
        ),
    )

    outcome = memory.append_batch()

    assert outcome.appended == 0
    assert [verdict.reasons for _p, verdict in outcome.refused] == [
        (REASON_NO_OPERATOR,),
        (REASON_NO_OPERATOR,),
    ]


# ── gate (i), condition (c): provenance in the closed set ──────────────────


def test_a_provenance_outside_the_closed_set_is_refused(tmp_path: Path) -> None:
    log = _log(tmp_path)
    memory = _episode(log)
    memory.stage(_claim("guessed", "A claim.", provenance="inferred"))

    outcome = memory.append_batch()

    assert outcome.appended == 0
    assert outcome.refused[0][1].reasons == (REASON_BAD_PROVENANCE,)
    assert log.read_claims() == ()


def test_both_closed_provenances_are_admissible(tmp_path: Path) -> None:
    memory = _episode(_log(tmp_path))
    for provenance in ("stub", "constructed"):
        assert memory.admit(_claim("p", "A claim.", provenance=provenance)).admitted


# ── gate (i), condition (d): claim-eligibility of the source note ──────────


def test_a_record_from_a_non_claim_eligible_note_is_refused(tmp_path: Path) -> None:
    """An index note is EVIDENCE — a locator points into it, it is never a
    vertex — so a string located in one may not receive a corpus verdict."""
    log = _log(tmp_path)
    memory = _episode(log)
    memory.stage(_claim("from-index", "Index of everything.", note_id=NOTE_INDEX))

    outcome = memory.append_batch()

    assert outcome.appended == 0
    assert outcome.refused[0][1].reasons == (REASON_NOT_CLAIM_ELIGIBLE,)
    assert log.read_claims() == ()


def test_claim_eligibility_fails_closed_for_unknown_and_absent_sources(
    tmp_path: Path,
) -> None:
    eligibility = BuildingBlockEligibility(blocks=BLOCKS)
    assert eligibility.is_claim_eligible(NOTE_A)
    assert not eligibility.is_claim_eligible("note-nobody-classified")

    # No eligibility source at all must not read as "everything is admissible".
    blind = EpisodeMemory(_log(tmp_path), eligibility=None)
    assert blind.admit(_claim("x", "A claim.")).reasons == (REASON_NOT_CLAIM_ELIGIBLE,)


def test_an_authored_counter_promotes_an_evidence_only_note(tmp_path: Path) -> None:
    """The one authored exception, and it is opt-in: a contested note is a claim
    whether or not its building block says so."""
    memory = _episode(
        _log(tmp_path),
        eligibility=BuildingBlockEligibility(
            blocks=BLOCKS, promoted=frozenset({NOTE_INDEX})
        ),
    )
    assert memory.admit(_claim("promoted", "A claim.", note_id=NOTE_INDEX)).admitted


def test_every_failed_condition_is_reported_not_just_the_first(
    tmp_path: Path,
) -> None:
    memory = _episode(_log(tmp_path))
    verdict = memory.admit(
        _claim(
            "hopeless",
            "A claim.",
            note_id=NOTE_INDEX,
            locator="",
            provenance="inferred",
            operator="",
        )
    )
    assert set(verdict.reasons) == {
        REASON_NO_LOCATOR,
        REASON_NO_OPERATOR,
        REASON_BAD_PROVENANCE,
        REASON_NOT_CLAIM_ELIGIBLE,
    }


def test_an_edge_whose_endpoint_was_refused_is_refused_too(tmp_path: Path) -> None:
    """Not a fifth condition — the integrity consequence of one. Sending the
    edge on would fail at the foreign key instead of at the gate."""
    log = _log(tmp_path)
    memory = _episode(log)
    good = _claim("good", "An admissible claim.")
    bad = _claim("bad", "From an index.", note_id=NOTE_INDEX)
    memory.stage(
        good,
        bad,
        EdgeProposal(
            op="support",
            src=bad.claim_id,
            dst=good.claim_id,
            origin="query",
            evidence_locator="loc",
        ),
    )

    outcome = memory.append_batch()

    assert outcome.appended == 1
    assert outcome.admitted == (good,)
    assert [verdict.reasons for _p, verdict in outcome.refused] == [
        (REASON_NOT_CLAIM_ELIGIBLE,),
        (REASON_ENDPOINT_REFUSED,),
    ]


def test_strict_mode_turns_the_gate_into_a_batch_level_refusal(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    memory = _episode(log)
    memory.stage(_claim("ok", "An admissible claim."), _claim("bad", "x", locator=""))
    with pytest.raises(AdmissionError):
        memory.append_batch(strict=True)
    assert log.read_claims() == ()


def test_append_batch_refuses_a_read_only_episode(tmp_path: Path) -> None:
    memory = EpisodeMemory(_log(tmp_path), appender=None)
    with pytest.raises(MemoryPortError):
        memory.append_batch()


def test_the_gated_batch_can_be_rendered_as_effects_without_an_append_port(
    tmp_path: Path,
) -> None:
    """The effects ARE the append: a caller routing them through the commit
    tail needs no append port, and the gate still runs."""
    log = _log(tmp_path)
    memory = EpisodeMemory(
        log, eligibility=BuildingBlockEligibility(blocks=BLOCKS), appender=None
    )
    good = _claim("good", "An admissible claim.")
    memory.stage(good, _claim("bad", "From an index.", note_id=NOTE_INDEX))

    effects = memory.pending_effects()

    assert [effect.payload["claim_id"] for effect in effects] == [good.claim_id]
    assert validate_effects(effects) == effects
    admitted, refused = memory.gate_batch()
    assert admitted == (good,)
    assert refused[0][1].reasons == (REASON_NOT_CLAIM_ELIGIBLE,)
    assert log.read_claims() == ()  # rendering is not writing


# ── rule 4: read at a snapshot, append at the end ──────────────────────────


def test_a_protocol_cannot_read_its_own_uncommitted_proposal_as_evidence(
    tmp_path: Path,
) -> None:
    log, _evidence_id, subject_id = _seed_supported_claim(tmp_path)
    search = MappingNoteSearch({"the query": (NoteHit(NOTE_A, "note_a", 0.9),)})
    memory = _episode(log, note_search=search)

    proposal = _claim("proposed", "A claim this episode has merely proposed.")
    memory.stage(
        proposal,
        EdgeProposal(
            op="support",
            src=subject_id,
            dst=proposal.claim_id,
            origin="query",
            evidence_locator=f"{NOTE_A}#h2:Claim",
        ),
    )

    # Neither read call can see it: no candidate, and no status to trust.
    retrieved = memory.retrieve("the query")
    assert proposal.claim_id not in {c.claim_id for c in retrieved.claims}
    assert memory.status(proposal.claim_id) == STATUS_UNKNOWN
    assert memory.explain(proposal.claim_id).links == ()

    # The consequence IS available — under a name no read path uses, and
    # explicitly non-citable.
    assert memory.speculative_statuses()[proposal.claim_id] == "warranted"

    # Even the episode's OWN append does not retroactively become readable:
    # the pin holds for the whole episode.
    outcome = memory.append_batch()
    assert outcome.appended == 2
    assert memory.status(proposal.claim_id) == STATUS_UNKNOWN

    # The next episode reads it, which is the intra-episode-only ceiling.
    assert _episode(log).status(proposal.claim_id) == "warranted"


def test_every_read_in_an_episode_resolves_against_one_digest(
    tmp_path: Path,
) -> None:
    log, evidence_id, subject_id = _seed_supported_claim(tmp_path)
    memory = _episode(log)
    pinned = memory.base_snapshot_id
    assert pinned == log_edgeset_digest(log.read_edges())
    assert pinned == edgeset_digest(log.read_edges())

    # A concurrent episode appends; the pinned reads do not move.
    other = _episode(log)
    other.stage(
        EdgeProposal(
            op="attack",
            src=evidence_id,
            dst=subject_id,
            origin="query",
            evidence_locator=f"{NOTE_B}#h2:Claim",
        )
    )
    assert other.append_batch().appended == 1

    assert memory.retrieve("q").base_snapshot_id == pinned
    assert memory.base_snapshot_id == pinned
    assert _episode(log).base_snapshot_id != pinned


def test_the_pin_rides_out_on_the_existing_candidate_field(tmp_path: Path) -> None:
    """``base_snapshot_id`` already exists on the candidate transaction; the
    boundary fills it in rather than inventing a second pin."""
    memory = _episode(_log(tmp_path))
    result = CapabilityResult(
        status="ok",
        effects=(),
        diagnostics=(),
        promotion_eligibility="needs_validation",
        warrant=None,
        qualifier="",
        replay_token="dks:test",
    )
    candidate = memory.pinned_candidate(result, parent_fz="1a")
    assert candidate.base_snapshot_id == memory.base_snapshot_id
    assert candidate.parent_fz == "1a"
    assert candidate.result is result


# ── replay ─────────────────────────────────────────────────────────────────


def test_a_replayed_batch_is_a_no_op(tmp_path: Path) -> None:
    log = _log(tmp_path)
    first = _episode(log)
    evidence = _claim("evidence", "The measurement was taken twice.", note_id=NOTE_B)
    subject = _claim("subject", "The second run reproduced the first.")
    batch = (
        evidence,
        subject,
        EdgeProposal(
            op="support",
            src=evidence.claim_id,
            dst=subject.claim_id,
            origin="query",
            evidence_locator=f"{NOTE_B}#h2:Claim",
        ),
    )
    first.stage(*batch)
    assert first.append_batch().appended == 3
    before = (log.read_claims(), log.read_edges())

    # A retried episode re-submits the identical batch.
    retry = _episode(log)
    retry.stage(*batch)
    outcome = retry.append_batch()

    assert outcome.appended == 0
    assert len(outcome.admitted) == 3  # admitted, and already present
    assert (log.read_claims(), log.read_edges()) == before


def test_a_reworded_claim_keeps_its_derivation_and_appends_a_row(
    tmp_path: Path,
) -> None:
    log = _log(tmp_path)
    memory = _episode(log)
    original = _claim("subject", "The second run reproduced the first.")
    memory.stage(original)
    memory.append_batch()

    reworded = replace(original, text="The first run was reproduced by the second.")
    again = _episode(log)
    again.stage(reworded)
    assert again.append_batch().appended == 1

    rows = log.claims_for_derivation(original.derivation_id)
    assert len(rows) == 2
    assert {row.text_hash for row in rows} == {original.text_hash, reworded.text_hash}


# ── the cache-read path and its metrics ────────────────────────────────────


def test_a_memoized_claim_is_returned_by_retrieve_with_its_status(
    tmp_path: Path,
) -> None:
    log, _evidence_id, subject_id = _seed_supported_claim(tmp_path)
    search = MappingNoteSearch(
        {"did the run reproduce": (NoteHit(NOTE_A, "note_a", 0.8),)}
    )
    memory = _episode(log, note_search=search)

    result = memory.retrieve("did the run reproduce")

    assert [candidate.claim_id for candidate in result.claims] == [subject_id]
    memoized = result.claims[0]
    assert memoized.status == "warranted"
    assert memoized.locator == "h2:Claim"
    assert memoized.provenance == "constructed"
    assert memoized.score == pytest.approx(0.8)
    assert memoized.source == "log"
    assert result.notes == (NoteHit(NOTE_A, "note_a", 0.8),)
    assert result.cache_hit is True


def test_retrieve_reports_the_cache_hit_rate_and_the_latency(
    tmp_path: Path,
) -> None:
    log, _evidence_id, _subject_id = _seed_supported_claim(tmp_path)
    search = MappingNoteSearch({"hit": (NoteHit(NOTE_A, "note_a", 0.8),)})
    clock = _SteppingClock(step_seconds=0.001)
    memory = _episode(log, note_search=search, clock=clock)

    hit = memory.retrieve("hit")
    miss = memory.retrieve("miss")

    assert hit.cache_hit is True and miss.cache_hit is False
    assert hit.latency_ms == pytest.approx(1.0)
    metrics = memory.metrics()
    assert (metrics.calls, metrics.hits) == (2, 1)
    assert metrics.hit_rate == pytest.approx(0.5)
    assert metrics.claim_hits == 1
    assert metrics.mean_latency_ms == pytest.approx(1.0)
    assert metrics.latency_ms_total == pytest.approx(2.0)


def test_an_unmeasured_cache_reports_a_zero_hit_rate(tmp_path: Path) -> None:
    metrics = _episode(_log(tmp_path)).metrics()
    assert (metrics.calls, metrics.hit_rate, metrics.mean_latency_ms) == (0, 0.0, 0.0)


def test_retrieve_answers_from_the_log_without_a_search_seam(
    tmp_path: Path,
) -> None:
    """A caller that resolved the authoritative note itself still gets the
    memoized claims — the cache read does not depend on similarity ranking."""
    log, _evidence_id, subject_id = _seed_supported_claim(tmp_path)
    memory = _episode(log)
    result = memory.retrieve("anything", note_ids=(NOTE_A,))
    assert [candidate.claim_id for candidate in result.claims] == [subject_id]
    assert result.notes == ()


def test_retrieve_returns_current_tier_a_relations_and_hides_stale_ones(
    tmp_path: Path,
) -> None:
    current = AuthoredRelation(
        relation_id="r-current",
        subject_id="entity-1",
        predicate="held_by",
        object_ref="entity-2",
        object_kind="entity",
        evidence_note=NOTE_A,
        evidence_locator=f"{NOTE_A}#frontmatter:held_by",
    )
    expired = replace(current, relation_id="r-expired", valid_to="2020-01-01")
    superseded = replace(current, relation_id="r-old", superseded_by="r-current")
    memory = _episode(
        _log(tmp_path), relations=_Relations((current, expired, superseded))
    )

    result = memory.retrieve("who holds it", subject_ids=("entity-1",))

    assert [row.relation_id for row in result.relations] == ["r-current"]
    assert result.relations[0].evidence_locator == f"{NOTE_A}#frontmatter:held_by"
    assert result.cache_hit is True
    assert [
        row.relation_id
        for row in memory.retrieve(
            "history", subject_ids=("entity-1",), include_expired=True
        ).relations
    ] == ["r-current", "r-expired", "r-old"]


# ── status / explain ───────────────────────────────────────────────────────


def test_explain_walks_the_chain_with_its_locators(tmp_path: Path) -> None:
    log, evidence_id, subject_id = _seed_supported_claim(tmp_path)
    explanation = _episode(log).explain(subject_id)

    assert explanation.status == "warranted"
    assert len(explanation.links) == 1
    link = explanation.links[0]
    assert (link.op, link.claim_id, link.direction) == ("support", evidence_id, "incoming")
    assert link.evidence_locator == f"{NOTE_B}#h2:Claim"
    assert explanation.provisional is False


def test_explain_flags_a_chain_that_touches_a_stub(tmp_path: Path) -> None:
    """A stub is a located string, not a constructed claim. Reporting a verdict
    over one launders a document title into a verdict, so the explanation says
    so; the refusal POLICY belongs to the status phase."""
    log = _log(tmp_path)
    memory = _episode(log)
    stub = _claim("stub", "Design: Something", note_id=NOTE_B, provenance="stub")
    subject = _claim("subject", "The design holds under load.")
    memory.stage(
        stub,
        subject,
        EdgeProposal(
            op="support",
            src=stub.claim_id,
            dst=subject.claim_id,
            origin="projected",
            evidence_locator=f"{NOTE_B}#h1",
        ),
    )
    memory.append_batch()

    assert _episode(log).explain(subject.claim_id).provisional is True


def test_the_reference_labeller_is_attack_only_with_a_supersede_prefilter(
    tmp_path: Path,
) -> None:
    log, evidence_id, subject_id = _seed_supported_claim(tmp_path)

    # A support edge changes the CLASSIFICATION, never a Dung label.
    assert _episode(log).status(subject_id) == "warranted"
    assert _episode(log).status(evidence_id) == "proposed"

    attacker = _claim("attacker", "The second run used different inputs.", note_id=NOTE_B)
    memory = _episode(log)
    memory.stage(
        attacker,
        EdgeProposal(
            op="attack",
            src=attacker.claim_id,
            dst=subject_id,
            origin="query",
            evidence_locator=f"{NOTE_B}#h2:Claim",
        ),
    )
    memory.append_batch()
    assert _episode(log).status(subject_id) == "challenged"

    # Superseding the attacker takes it OUT OF THE FRAMEWORK — being replaced is
    # not being defeated — and the claim it attacked is reinstated.
    replacement = _claim("replacement", "The inputs were identical after all.", note_id=NOTE_B)
    third = _episode(log)
    third.stage(replacement)
    third.append_batch()
    log.supersede(
        superseding_claim_id=replacement.claim_id,
        superseded_claim_id=attacker.claim_id,
        origin="query",
        evidence_locator=f"{NOTE_B}#h2:Claim",
    )

    final = _episode(log)
    assert final.status(attacker.claim_id) == "superseded"
    assert final.status(subject_id) == "warranted"


def test_the_labeller_is_a_pure_function_of_the_edge_set(tmp_path: Path) -> None:
    log, _evidence_id, subject_id = _seed_supported_claim(tmp_path)
    claims, edges = log.read_claims(), log.read_edges()
    once = grounded_status_labeller(claims, edges)
    twice = grounded_status_labeller(tuple(reversed(claims)), tuple(reversed(edges)))
    assert once == twice
    assert once[subject_id] == "warranted"


# ── locator staleness (detection only) ─────────────────────────────────────


def test_editing_a_cited_note_flags_the_dependent_claim(tmp_path: Path) -> None:
    log, _evidence_id, subject_id = _seed_supported_claim(tmp_path)
    memory = _episode(log)
    assert memory.status(subject_id) == "warranted"

    # An index rebuild reports a new content hash for the cited note.
    stale = memory.detect_stale_claims({NOTE_A: "note-hash-2", NOTE_B: "note-hash-1"})
    assert [finding.claim_id for finding in stale] == [subject_id]
    assert stale[0].recorded_note_hash == "note-hash-1"
    assert stale[0].current_note_hash == "note-hash-2"

    staged = memory.stage_staleness_flags(stale)
    assert len(staged) == 2
    outcome = memory.append_batch()
    assert outcome.appended == 2
    assert outcome.refused == ()

    # The dependent claim is now CHALLENGED — the computed way of saying it
    # needs re-derivation — and the flag is visible in its chain.
    after = _episode(log)
    assert after.status(subject_id) == "challenged"
    flags = [
        link
        for link in after.explain(subject_id).links
        if link.op == "attack" and link.direction == "incoming"
    ]
    assert len(flags) == 1
    flag_claim = after.snapshot.claim(flags[0].claim_id)
    assert flag_claim is not None
    assert flag_claim.provenance == "constructed"
    assert flag_claim.source_note_hash == "note-hash-2"
    assert "needs re-derivation" in flag_claim.text


def test_re_running_staleness_detection_appends_nothing_new(tmp_path: Path) -> None:
    log, _evidence_id, _subject_id = _seed_supported_claim(tmp_path)
    hashes = {NOTE_A: "note-hash-2", NOTE_B: "note-hash-1"}
    first = _episode(log)
    first.stage_staleness_flags(first.detect_stale_claims(hashes))
    assert first.append_batch().appended == 2

    second = _episode(log)
    second.stage_staleness_flags(second.detect_stale_claims(hashes))
    assert second.append_batch().appended == 0


def test_staleness_detection_is_silent_where_it_cannot_know(tmp_path: Path) -> None:
    """Two deliberate silences: a claim with no recorded hash cannot be checked,
    and a note absent from a partial rebuild is unknown, never stale."""
    log = _log(tmp_path)
    memory = _episode(log)
    memory.stage(_claim("unbound", "A claim with no recorded source hash.",
                        source_note_hash=None))
    memory.append_batch()

    checked = _episode(log)
    assert checked.detect_stale_claims({NOTE_A: "note-hash-9"}) == ()
    assert checked.detect_stale_claims({}) == ()


# ── the effect vocabulary, validated at ingestion ──────────────────────────


def test_the_boundary_emits_effects_not_writes(tmp_path: Path) -> None:
    proposal = _claim("subject", "The second run reproduced the first.")
    effect = effect_for_proposal(proposal)
    assert effect.kind == "claim"
    assert effect.folgezettel == NOTE_A
    assert effect.payload["claim_id"] == proposal.claim_id
    assert effect.payload["operator"] == "support"

    edge = EdgeProposal(
        op="attack", src="a", dst="b", origin="query", evidence_locator="loc"
    )
    edge_effect = effect_for_proposal(edge)
    assert (edge_effect.kind, edge_effect.bb_role) == ("edge", "attack")
    assert edge_effect.payload["edge_id"] == edge.edge_id


def test_the_effect_kind_vocabulary_is_validated_at_ingestion() -> None:
    for kind in ("note", "edge", "warrant", "claim", "relation"):
        assert validate_effect_kind(kind) == kind
    assert EFFECT_KINDS == {"note", "edge", "warrant", "claim", "relation"}
    with pytest.raises(EffectKindError):
        validate_effect_kind("proposition")
    with pytest.raises(EffectKindError):
        validate_effects(
            (
                CapabilityEffect(kind="claim", folgezettel="1a"),
                CapabilityEffect(kind="proposition", folgezettel="1b"),
            )
        )


def test_validation_is_at_ingestion_not_in_the_constructor() -> None:
    """The kind stays a free-form ``str`` on a published contract, so an
    existing construction site is unaffected — the check is where effects are
    INGESTED."""
    assert CapabilityEffect(kind="anything", folgezettel="1a").kind == "anything"


def test_the_appender_receives_the_pin_with_the_batch(tmp_path: Path) -> None:
    log = _log(tmp_path)
    appender = _ClaimLogAppender(log)
    memory = _episode(log, appender=appender)
    memory.stage(_claim("subject", "The second run reproduced the first."))
    outcome = memory.append_batch()
    assert appender.batches == [(memory.base_snapshot_id, 1)]
    assert outcome.base_snapshot_id == memory.base_snapshot_id


# ── the narrower materializer gap: recoverable, but VISIBLE ────────────────

_FRONTMATTER_NOTE = """---
output_path: notes/derived.md
tags: [alpha]
---
# Derived

A body.
"""


def _vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    (vault / "notes").mkdir(parents=True)
    return vault


def test_materialize_writes_to_the_live_vault_by_default(tmp_path: Path) -> None:
    """The default is unchanged: no new behaviour becomes the default here."""
    vault = _vault(tmp_path)
    out = materialize(
        "body_markdown_frontmatter_to_file", _FRONTMATTER_NOTE, vault_root=vault
    )
    assert (vault / "notes" / "derived.md").is_file()
    assert out.files_written == (vault / "notes" / "derived.md",)
    assert out.pending_targets == ()
    assert out.notes.startswith("wrote ")


def test_an_overlay_write_is_invisible_to_a_vault_reading_step(
    tmp_path: Path,
) -> None:
    """The gap this phase owns. Every write already runs inside
    ``effect_guard()`` and is rollback-able, so a mid-episode write is
    RECOVERABLE — but a vault-reading step later in the same episode can still
    OBSERVE it. Routing through the overlay closes that read channel."""
    vault = _vault(tmp_path)
    overlay = tmp_path / "overlay"

    out = materialize(
        "body_markdown_frontmatter_to_file",
        _FRONTMATTER_NOTE,
        vault_root=vault,
        overlay_root=overlay,
    )

    live = vault / "notes" / "derived.md"
    staged = overlay / "notes" / "derived.md"
    assert not live.exists()          # the reading path cannot observe it
    assert staged.is_file()
    assert "# Derived" in staged.read_text(encoding="utf-8")
    assert out.files_written == (staged,)
    assert out.pending_targets == (live,)
    assert out.notes.startswith("staged ")


def test_an_overlay_apply_leaves_the_live_note_untouched(tmp_path: Path) -> None:
    vault = _vault(tmp_path)
    overlay = tmp_path / "overlay"
    live = vault / "notes" / "existing.md"
    live.write_text("original\n", encoding="utf-8")

    out = materialize(
        "edits_apply_xml_tags",
        "<edits><edit><file>notes/existing.md</file>"
        "<content>revised</content></edit></edits>",
        vault_root=vault,
        overlay_root=overlay,
    )

    assert live.read_text(encoding="utf-8") == "original\n"
    assert (overlay / "notes" / "existing.md").read_text(encoding="utf-8") == "revised"
    assert out.files_applied == (overlay / "notes" / "existing.md",)
    assert out.pending_targets == (live,)


def test_overlay_staging_still_confines_the_agent_supplied_path(
    tmp_path: Path,
) -> None:
    vault = _vault(tmp_path)
    overlay = tmp_path / "overlay"
    escaping = _FRONTMATTER_NOTE.replace(
        "output_path: notes/derived.md", "output_path: ../escaped.md"
    )
    with pytest.raises(Exception) as excinfo:
        materialize(
            "body_markdown_frontmatter_to_file",
            escaping,
            vault_root=vault,
            overlay_root=overlay,
        )
    assert "escapes vault_root" in str(excinfo.value)
    assert not (overlay / "escaped.md").exists()
    assert not (tmp_path / "escaped.md").exists()


def test_a_dry_run_stages_nothing(tmp_path: Path) -> None:
    vault = _vault(tmp_path)
    overlay = tmp_path / "overlay"
    out = materialize(
        "body_markdown_frontmatter_to_file",
        _FRONTMATTER_NOTE,
        vault_root=vault,
        overlay_root=overlay,
        dry_run=True,
    )
    assert isinstance(out, MaterializedOutput)
    assert out.files_written == () and out.pending_targets == ()
    assert not overlay.exists()
    assert not (vault / "notes" / "derived.md").exists()
