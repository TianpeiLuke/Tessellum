"""tessellum.composer.structural_gates — capsule-level structural gate suite.

P6 of the dynamic-digestion plan "Dynamic Digestion as a Snapshot-Pinned
Knowledge Transaction". After P5 gives an atomic commit point, P6 decides
whether a capsule is *allowed* to publish — using STRUCTURAL checks only (no
LLM). These run over the typed NoteIntentGraph + the P3 OverlayIndex + the P4
write closure — everything a pure program can verify:

- source-span coverage: every note intent cites ≥1 source span (provenance);
- claim provenance: each provenance row names a span + a source ref;
- BB-atomicity: exactly one building_block per note;
- disposition present + create-only (this phase);
- link-relevance threshold: outbound relevance links are bounded (a few
  justified edges, not a link-count-floor spray);
- navigation closure: every declared navigation entry point is a real write;
- reverse-inlink closure: every required reverse inlink is a real write;
- referential integrity: no dangling reference in the overlay (ghost_links
  empty) after the capsule's effects.

**The honest ceiling (A6.2, counter blocking-correction 6):** structural gates
give a *structurally-safe* capsule, NOT a *semantically-correct* one — a
program cannot judge claim entailment, decomposition completeness, or edge
usefulness. So P6 additionally REQUIRES a signed human-approval artifact on the
capsule before publication; without it the run is ``blocked``. The unattended,
semantically-gated path is P7 (the calibrated certificate). This module never
calls a model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from tessellum.composer.gates import Gate, GateSuite
from tessellum.composer.knowledge_plan import NoteIntent, NoteIntentGraph
from tessellum.composer.overlay_index import OverlayIndex
from tessellum.composer.write_closure import WriteClosure, write_closure
from tessellum.format import Issue, Severity

# A relevance-link budget: prefer a few justified edges over a count-floor
# spray. A note with more than this many outbound relevance links is flagged
# for review (WARNING) — it is not auto-blocked, but it is surfaced.
DEFAULT_RELEVANCE_LINK_CAP = 12


@dataclass(frozen=True)
class StructuralGateContext:
    """Everything the structural predicates read (all pure, no LLM)."""

    graph: NoteIntentGraph
    overlay: OverlayIndex | None = None
    write_closure: WriteClosure | None = None
    relevance_link_cap: int = DEFAULT_RELEVANCE_LINK_CAP


# ── structural predicates (pure; Sequence[Issue]) ───────────────────────────


def _intents(target: StructuralGateContext) -> tuple[NoteIntent, ...]:
    return target.graph.intents


def source_coverage_predicate(target: StructuralGateContext, /, **_) -> Sequence[Issue]:
    # Defense-in-depth: NoteIntent's model already enforces non-empty
    # provenance (min_length=1), so this cannot fire for a model-built intent —
    # it guards a capsule assembled from raw dicts that bypassed the model.
    issues: list[Issue] = []
    for intent in _intents(target):
        if not intent.provenance:
            issues.append(Issue(
                severity=Severity.ERROR, rule_id="STRUCT-COVERAGE",
                field=intent.note_id,
                message="note intent cites no source span (provenance empty)",
            ))
    return issues


def claim_provenance_predicate(target: StructuralGateContext, /, **_) -> Sequence[Issue]:
    issues: list[Issue] = []
    for intent in _intents(target):
        for p in intent.provenance:
            if not p.span_id or not p.source_ref:
                issues.append(Issue(
                    severity=Severity.ERROR, rule_id="STRUCT-PROVENANCE",
                    field=intent.note_id,
                    message="provenance row missing span_id or source_ref",
                ))
    return issues


def bb_atomicity_predicate(target: StructuralGateContext, /, **_) -> Sequence[Issue]:
    issues: list[Issue] = []
    for intent in _intents(target):
        # exactly one building block per note (the model enforces min_length=1;
        # here we reject a comma/space-joined multi-BB smell).
        if any(sep in intent.building_block for sep in (",", "/", "+", " and ")):
            issues.append(Issue(
                severity=Severity.ERROR, rule_id="STRUCT-BB-ATOMIC",
                field=intent.note_id,
                message=f"building_block not atomic: {intent.building_block!r}",
            ))
    return issues


_VALID_DISPOSITIONS = frozenset({"create", "update", "merge", "drop", "skip"})


def disposition_predicate(target: StructuralGateContext, /, **_) -> Sequence[Issue]:
    # P9 (A9.2): all effect classes are enabled. The preimage rule is enforced
    # by the NoteIntent model; here we only reject an unknown disposition (fail
    # closed on an unclassifiable effect class).
    issues: list[Issue] = []
    for intent in _intents(target):
        if intent.disposition not in _VALID_DISPOSITIONS:
            issues.append(Issue(
                severity=Severity.ERROR, rule_id="STRUCT-DISPOSITION",
                field=intent.note_id,
                message=f"unknown disposition {intent.disposition!r}",
            ))
    return issues


def link_relevance_predicate(target: StructuralGateContext, /, **_) -> Sequence[Issue]:
    issues: list[Issue] = []
    cap = target.relevance_link_cap
    for intent in _intents(target):
        if len(intent.relevance_links) > cap:
            issues.append(Issue(
                severity=Severity.WARNING, rule_id="STRUCT-LINK-RELEVANCE",
                field=intent.note_id,
                message=f"{len(intent.relevance_links)} relevance links > cap {cap} "
                        "(prefer a few justified edges over a count-floor spray)",
            ))
    return issues


def navigation_closure_predicate(target: StructuralGateContext, /, **_) -> Sequence[Issue]:
    """Every declared navigation entry point must be a mandatory write in the
    capsule's closure (else the note would be published undiscoverable)."""
    wc = target.write_closure or write_closure(target.graph)
    touched = wc.touched_note_ids
    issues: list[Issue] = []
    for intent in _intents(target):
        for ep in intent.navigation:
            if ep not in touched:
                issues.append(Issue(
                    severity=Severity.ERROR, rule_id="STRUCT-NAV-CLOSURE",
                    field=intent.note_id,
                    message=f"navigation entry point {ep!r} not in the write closure",
                ))
    return issues


def reverse_inlink_closure_predicate(target: StructuralGateContext, /, **_) -> Sequence[Issue]:
    wc = target.write_closure or write_closure(target.graph)
    touched = wc.touched_note_ids
    issues: list[Issue] = []
    for intent in _intents(target):
        for src in intent.required_inlinks:
            if src not in touched:
                issues.append(Issue(
                    severity=Severity.ERROR, rule_id="STRUCT-INLINK-CLOSURE",
                    field=intent.note_id,
                    message=f"required reverse inlink source {src!r} not in the write closure",
                ))
    return issues


def referential_integrity_predicate(target: StructuralGateContext, /, **_) -> Sequence[Issue]:
    """No dangling reference in the effective overlay after the capsule's
    effects (the promotion must not publish a fresh broken link)."""
    if target.overlay is None:
        return []
    issues: list[Issue] = []
    for ghost in target.overlay.ghost_links():
        issues.append(Issue(
            severity=Severity.ERROR, rule_id="STRUCT-REF-INTEGRITY",
            field=ghost.source_note_id,
            message=f"dangling reference to {ghost.target_note_id!r} after capsule effects",
        ))
    return issues


def build_structural_gate_suite() -> GateSuite:
    """The capsule-level structural gate suite (P6, A6.1). All ERROR-blocking
    except the relevance-link cap (WARNING/advisory)."""
    def _g(gate_id: str, predicate, block_on=Severity.ERROR) -> Gate:
        return Gate(gate_id=gate_id, kind="checkpoint", scope="wave",
                    predicate=predicate, cause=gate_id, block_on=block_on)
    return GateSuite(gates=(
        _g("struct_coverage", source_coverage_predicate),
        _g("struct_provenance", claim_provenance_predicate),
        _g("struct_bb_atomic", bb_atomicity_predicate),
        _g("struct_disposition", disposition_predicate),
        _g("struct_nav_closure", navigation_closure_predicate),
        _g("struct_inlink_closure", reverse_inlink_closure_predicate),
        _g("struct_ref_integrity", referential_integrity_predicate),
        _g("struct_link_relevance", link_relevance_predicate, block_on=Severity.ERROR),
    ))


# ── human approval (A6.2) — the honest supervised ceiling ────────────────────


@dataclass(frozen=True)
class HumanApproval:
    """A signed human-approval artifact carried on a capsule (A6.2).

    Structural gates cannot establish semantic correctness, so a human sign-off
    is REQUIRED before a P6 capsule publishes. ``capsule_id`` binds the approval
    to exactly one capsule (an approval for a different capsule id is invalid,
    so it cannot be replayed onto a mutated capsule)."""

    capsule_id: str
    approver: str
    signature: str
    reason: str = ""


ConstructorDecision = str  # "approved" | "blocked_structural" | "blocked_needs_human"


@dataclass(frozen=True)
class SupervisedResult:
    decision: ConstructorDecision
    structural_passed: bool
    first_failure_cause: str | None = None
    detail: str = ""
    blocking_rules: tuple[str, ...] = field(default_factory=tuple)


def supervised_admit(
    context: StructuralGateContext,
    *,
    capsule_id: str,
    approval: HumanApproval | None = None,
    suite: GateSuite | None = None,
) -> SupervisedResult:
    """The P6 admission decision (the structurally-safe, human-SUPERVISED
    ceiling). A capsule may publish iff (1) the structural gate suite passes AND
    (2) a valid human-approval artifact bound to THIS capsule id is present.

    - structural gate fails  → ``blocked_structural`` (fail closed);
    - structural ok, no/invalid approval → ``blocked_needs_human``;
    - structural ok + valid approval → ``approved``.

    This is NOT "automatic/unattended" — unattended admission requires the P7
    calibrated semantic certificate."""
    suite = suite or build_structural_gate_suite()
    composite = suite.evaluate(context, short_circuit=False)
    blocking = tuple(
        i.rule_id
        for r in composite.results if not r.passed
        for i in r.issues if i.severity == Severity.ERROR
    )
    if not composite.passed:
        return SupervisedResult(
            decision="blocked_structural",
            structural_passed=False,
            first_failure_cause=composite.first_failure_cause,
            detail="structural gate failed",
            blocking_rules=blocking,
        )
    # structurally safe — but a human must sign before publication.
    if approval is None or approval.capsule_id != capsule_id or not approval.signature:
        return SupervisedResult(
            decision="blocked_needs_human",
            structural_passed=True,
            detail="structurally safe; awaiting a valid human-approval artifact",
        )
    return SupervisedResult(
        decision="approved",
        structural_passed=True,
        detail=f"structurally safe + approved by {approval.approver}",
    )


__all__ = [
    "DEFAULT_RELEVANCE_LINK_CAP",
    "StructuralGateContext",
    "build_structural_gate_suite",
    "source_coverage_predicate",
    "claim_provenance_predicate",
    "bb_atomicity_predicate",
    "disposition_predicate",
    "link_relevance_predicate",
    "navigation_closure_predicate",
    "reverse_inlink_closure_predicate",
    "referential_integrity_predicate",
    "HumanApproval",
    "SupervisedResult",
    "supervised_admit",
]
