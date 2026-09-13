"""P5 smoke tests — the dependency validator, outside the labelling.

The attack-only fixed point is a *dialectical* check: it answers "did this claim
survive criticism?", not "does a chain of surviving evidence reach it?". These
tests are the two graphs where those answers differ, and they are written as
disagreements on purpose — each asserts the label the labelling computes AND the
opposite grounding verdict, so a change that quietly aligned them would fail
rather than pass.

The acceptance clauses:

1. ``source`` supports ``conclusion``; ``counter`` defeats ``source`` — the
   labelling says ``conclusion`` is **warranted**; the validator says it is **not
   grounded**, because defeat propagates across a necessary premise.
2. ``a`` supports ``b``; ``b`` supports ``a``; no external anchor — the labelling
   says **both warranted**; the validator says **neither is grounded**, because
   circular support grounds nothing. Both claims here cite their own spans, so the
   refusal is about the cycle rather than about missing evidence.
3. **Reinstatement still works** — defeat the attacker and the conclusion is
   grounded again, with nothing migrated; and **a defeated attacker does not
   defeat**.
4. A **cached validation is invalidated** when a required premise changes or a
   cited source version changes.

Plus the properties those rest on: three support kinds with three genuinely
different propagation rules, the conservative default, the external anchor as the
only base case, a ``stub`` anchoring nothing, and the Dependency Rule.

All pure; no storage, no network, no model.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from pathlib import Path

import pytest

from tessellum.dks.status import EdgeSet, compute_statuses
from tessellum.dks.support_dependency import (
    CONSERVATIVE_SUPPORT_KINDS,
    CONTRIBUTORY,
    EVIDENTIAL,
    NECESSARY,
    REASON_CYCLIC_SUPPORT,
    REASON_NECESSARY_PREMISE_NOT_GROUNDED,
    REASON_NO_ANCHOR_LOCATOR,
    REASON_NO_GROUNDING_BASIS,
    REASON_NO_SURVIVING_EVIDENCE,
    REASON_STALE_SOURCE,
    REASON_STUB_ANCHOR,
    REASON_SUPERSEDED,
    REASON_UNKNOWN_CLAIM,
    SUPPORT_KINDS,
    ConservativeSupportKinds,
    DeclaredSupportKinds,
    GroundingValidator,
    SupportKindError,
    grounding_digest,
    grounding_verdict,
    is_answerable,
    is_grounded,
    support_premises,
    validate_support_dependencies,
)

SOURCE_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "tessellum"
    / "dks"
    / "support_dependency.py"
)

NOTE = "note-observations"
HASH_V1 = "1" * 64
HASH_V2 = "2" * 64


# ── fixtures: the anchor fields the labelling's narrower view does not carry ──


@dataclass(frozen=True)
class _C:
    """A claim as the validator reads it — identity, provenance and the anchor."""

    claim_id: str
    provenance: str = "constructed"
    note_id: str = NOTE
    locator: str | None = "h2:Finding"
    source_note_hash: str | None = HASH_V1


@dataclass(frozen=True)
class _E:
    """An operator edge."""

    op: str
    src: str
    dst: str
    seq: int
    evidence_locator: str | None = "note-observations#L1"
    origin: str = "query"


@dataclass(frozen=True)
class _KindedE:
    """An edge from a writer that already records the support kind."""

    op: str
    src: str
    dst: str
    seq: int
    support_kind: str
    evidence_locator: str | None = "note-observations#L1"
    origin: str = "query"


class _MutableSource:
    """An :class:`~tessellum.dks.status.EdgeSetSource` whose fold can grow.

    Appending is the only change a log makes, so the source models exactly that:
    a test can add an edge between two reads and watch the memo miss."""

    def __init__(self, view: EdgeSet) -> None:
        self.view = view

    def append(self, *edges: _E) -> None:
        self.view = EdgeSet(
            claims=self.view.claims, edges=self.view.edges + tuple(edges)
        )

    def add_claims(self, *claims: _C) -> None:
        self.view = EdgeSet(
            claims=self.view.claims + tuple(claims), edges=self.view.edges
        )

    def fold(self) -> EdgeSet:
        return self.view


def _set(claims: tuple[_C, ...], edges: tuple[object, ...]) -> EdgeSet:
    return EdgeSet(claims=claims, edges=edges)  # type: ignore[arg-type]


# ── the Dependency Rule, and no write path ──────────────────────────────────


def test_the_validator_is_pure_and_has_no_write_path() -> None:
    """DKS stays pure, and validation stores nothing.

    A stored validation is a claim about the corpus that somebody has to keep
    true; keying the memo by a digest means nobody has to. Both properties are
    structural, so they are read off the source.
    """
    source = SOURCE_PATH.read_text(encoding="utf-8")
    assert "tessellum.runtime" not in source
    assert not re.search(r"^\s*(from|import)\s+.*\bruntime\b", source, re.MULTILINE)
    for statement in ("INSERT", "UPDATE ", "DELETE", "executescript", "commit("):
        assert statement not in source, f"must not {statement.strip()}"
    assert "sqlite3" not in source
    assert "open(" not in source


def test_the_validator_reads_the_labelling_rather_than_re_deriving_it() -> None:
    """One three-layer verdict in the codebase, and this module consumes it.

    The same defect shipped twice once because two modules each derived the
    labelling. So the validator holds no Dung framework of its own: it takes the
    status table, and a caller with one already passes it so the two verdicts
    cannot straddle different snapshots.
    """
    source = SOURCE_PATH.read_text(encoding="utf-8")
    assert "compute_statuses" in source
    assert "grounded_labelling" not in source
    assert "DungAF" not in source

    view = _set((_C("only"),), ())
    table = compute_statuses(view)
    assert validate_support_dependencies(view, statuses=table).verdicts.keys() == {
        "only"
    }


# ── ACCEPTANCE 1: defeat propagates across a necessary premise ──────────────


def test_a_conclusion_resting_on_a_defeated_premise_is_not_grounded() -> None:
    """The plan's first fixture, and the disagreement it exists to record.

    ``counter`` defeats ``source``; ``source`` is ``conclusion``'s only premise.
    The labelling calls ``conclusion`` **warranted** — correctly, since nothing
    attacks it and it carries a support edge — and that is precisely why
    ``warranted`` cannot be the answer gate on its own. Grounding propagates the
    defeat, names the premise that failed, and refuses.
    """
    view = _set(
        (_C("conclusion"), _C("source"), _C("counter")),
        (
            _E("support", "source", "conclusion", 1),
            _E("attack", "counter", "source", 2),
        ),
    )
    labels = compute_statuses(view)
    assert labels.statuses["conclusion"].status == "warranted"
    assert labels.statuses["source"].status == "challenged"

    table = validate_support_dependencies(view)
    verdict = table.verdict("conclusion")
    assert verdict.status == "warranted"  # the labels and the grounding disagree
    assert verdict.grounded is False
    assert verdict.answerable is False
    assert verdict.failed_premises == ("source",)
    assert REASON_NECESSARY_PREMISE_NOT_GROUNDED in verdict.reasons
    assert table.verdict("source").grounded is False
    assert not is_grounded(view, "conclusion")
    assert not is_answerable(view, "conclusion")
    assert "ungrounded premise: source" in verdict.render()


# ── ACCEPTANCE 2: circular support grounds nothing ──────────────────────────


def test_mutual_support_with_no_external_anchor_grounds_neither_claim() -> None:
    """The plan's second fixture: support *existence* is not support.

    ``a`` and ``b`` each support the other and nothing attacks either, so the
    labelling calls both **warranted**. Neither is grounded: the least fixed point
    starts empty, and neither claim can be the first one in. Both claims here
    carry their own locators, so the refusal is specifically about the cycle —
    an anchor does not license a claim whose declared premise chain is circular.
    """
    view = _set(
        (_C("a"), _C("b")),
        (
            _E("support", "a", "b", 1),
            _E("support", "b", "a", 2),
        ),
    )
    labels = compute_statuses(view)
    assert labels.statuses["a"].status == labels.statuses["b"].status == "warranted"

    table = validate_support_dependencies(view)
    for claim_id in ("a", "b"):
        verdict = table.verdict(claim_id)
        assert verdict.status == "warranted"
        assert verdict.anchored is True  # it cites a span; that is not enough
        assert verdict.grounded is False
        assert REASON_CYCLIC_SUPPORT in verdict.reasons
        assert verdict.cycle[0] == verdict.cycle[-1] == claim_id
    assert table.grounded_ids() == ()
    assert table.ungrounded_ids() == ("a", "b")


def test_a_longer_support_cycle_is_rejected_too() -> None:
    """Three hops round, and no anchor is reached — so nothing grounds.

    A cycle check that only knew the two-claim shape would be a check against the
    fixture rather than against circular justification.
    """
    view = _set(
        (_C("x"), _C("y"), _C("z")),
        (
            _E("support", "x", "y", 1),
            _E("support", "y", "z", 2),
            _E("support", "z", "x", 3),
        ),
    )
    table = validate_support_dependencies(view)
    assert table.grounded_ids() == ()
    assert len(table.verdict("y").cycle) == 4  # y -> x -> z -> y


def test_a_contributory_cycle_is_not_a_grounding_cycle() -> None:
    """Corroboration going round in a circle is harmless.

    ``contributory`` support is never a grounding path, so a cycle made of it is
    not one either: both claims stand on their own anchors, and the mutual
    corroboration adds exactly nothing — which is what ``contributory`` means.
    """
    kinds = DeclaredSupportKinds(
        {("a", "b"): CONTRIBUTORY, ("b", "a"): CONTRIBUTORY}
    )
    view = _set(
        (_C("a"), _C("b")),
        (
            _E("support", "a", "b", 1),
            _E("support", "b", "a", 2),
        ),
    )
    table = validate_support_dependencies(view, kinds=kinds)
    assert table.grounded_ids() == ("a", "b")
    assert table.verdict("a").cycle == ()


# ── ACCEPTANCE 3: reinstatement, and a defeated attacker does not defeat ────


def test_reinstatement_restores_grounding_and_a_defeated_attacker_does_not_defeat() -> None:
    """Defeat the attacker and the conclusion is grounded again.

    Nothing is migrated and no verdict is stored: grounding is recomputed over the
    same edge set the labelling reads, so the reinstatement the fixed point
    performs shows up here for free. The attacker's own verdict is the other half
    of the clause — a defeated attacker is not grounded and defeats nothing.
    """
    attacked = _set(
        (_C("conclusion"), _C("source"), _C("counter")),
        (
            _E("support", "source", "conclusion", 1),
            _E("attack", "counter", "source", 2),
        ),
    )
    assert not is_grounded(attacked, "conclusion")

    reinstated = _set(
        attacked.claims + (_C("defender"),),  # type: ignore[operator]
        attacked.edges + (_E("attack", "defender", "counter", 3),),
    )
    labels = compute_statuses(reinstated)
    assert labels.statuses["source"].label == "in"
    assert labels.statuses["counter"].label == "out"

    table = validate_support_dependencies(reinstated)
    conclusion = table.verdict("conclusion")
    assert conclusion.grounded is True
    assert conclusion.basis == ("source",)
    assert conclusion.answerable is True
    assert table.verdict("source").grounded is True
    # The defeated attacker: not grounded, and it defeats nothing.
    counter = table.verdict("counter")
    assert counter.status == "challenged"
    assert counter.grounded is False
    assert is_answerable(reinstated, "conclusion")


def test_a_superseded_claim_is_not_grounded() -> None:
    """Retired is not grounded either — and it is refused for the right reason.

    The replacement is supported, because only a ``warranted`` replacement retires
    anything; that is the pre-filter's rule, and this fixture depends on it.
    """
    view = _set(
        (_C("old"), _C("new"), _C("ground")),
        (
            _E("support", "ground", "new", 1),
            _E("supersede", "new", "old", 2),
        ),
    )
    assert compute_statuses(view).statuses["old"].status == "superseded"
    verdict = validate_support_dependencies(view).verdict("old")
    assert verdict.grounded is False
    assert REASON_SUPERSEDED in verdict.reasons


# ── the base case: an external anchor, and nothing else ─────────────────────


def test_an_anchored_claim_with_no_premises_is_grounded_but_not_answerable() -> None:
    """The only base case there is, and it stops short of an answer.

    A claim that cites a span nothing has changed is grounded in that span — that
    is what stops the regress. It is still ``proposed``, so it is not answerable:
    grounding and the dialectic are two conditions, and the gate needs both.
    """
    view = _set((_C("anchor"),), ())
    verdict = validate_support_dependencies(view).verdict("anchor")
    assert verdict.status == "proposed"
    assert verdict.anchored is True
    assert verdict.grounded is True
    assert verdict.answerable is False


def test_a_claim_with_no_locator_anchors_nothing() -> None:
    """No located span, no anchor — the fail-closed reading.

    A claim with nothing to point at cites nothing outside the claim graph, so
    there is nothing for it to stand on. Reading a missing locator as "fine"
    would make every un-located assertion self-grounding.
    """
    view = _set((_C("floating", locator=None),), ())
    verdict = validate_support_dependencies(view).verdict("floating")
    assert verdict.grounded is False
    assert verdict.reasons == (REASON_NO_GROUNDING_BASIS, REASON_NO_ANCHOR_LOCATOR)


def test_a_stub_anchors_nothing() -> None:
    """A located string is not a constructed claim, so it cannot anchor one.

    Most mechanically located claim strings are not truth-apt as written, and the
    conclusion resting on one inherits that — so the stub grounds nothing and the
    conclusion above it is refused with the premise named.
    """
    view = _set(
        (_C("conclusion"), _C("located", provenance="stub")),
        (_E("support", "located", "conclusion", 1),),
    )
    table = validate_support_dependencies(view)
    stub = table.verdict("located")
    assert stub.grounded is False
    assert REASON_STUB_ANCHOR in stub.reasons
    conclusion = table.verdict("conclusion")
    assert conclusion.grounded is False
    assert conclusion.failed_premises == ("located",)


def test_an_unknown_claim_fails_closed_and_says_so() -> None:
    """A question about a claim the snapshot lacks is answered "not grounded".

    Returned rather than raised, because this is a gate: a caller that asked about
    the wrong id must not get an answer. The reason is explicit so the mistake is
    visible rather than silent.
    """
    view = _set((_C("present"),), ())
    verdict = validate_support_dependencies(view).verdict("absent")
    assert verdict.grounded is False
    assert verdict.status == "unknown"
    assert verdict.reasons == (REASON_UNKNOWN_CLAIM,)
    assert not is_grounded(view, "absent")


# ── three kinds, three propagation rules ────────────────────────────────────


def test_the_default_resolver_reads_every_support_edge_as_necessary() -> None:
    """The conservative reading is the default, and it is the only safe one.

    An undeclared edge is one nobody classified. Conjunction can only withhold an
    answer; reading it as corroboration would answer from an unexamined premise
    set. A record that already records its kind is believed, so a schema that
    later grows the column needs no change here.
    """
    bare = _E("support", "s", "c", 1)
    assert CONSERVATIVE_SUPPORT_KINDS.support_kind(bare) == NECESSARY
    assert NECESSARY in SUPPORT_KINDS

    declared = _KindedE("support", "s", "c", 1, support_kind=EVIDENTIAL)
    assert CONSERVATIVE_SUPPORT_KINDS.support_kind(declared) == EVIDENTIAL
    # An unrecognised value from a newer writer falls back, never raises.
    assert (
        ConservativeSupportKinds().support_kind(
            _KindedE("support", "s", "c", 1, support_kind="probably")
        )
        == NECESSARY
    )


def test_a_declared_kind_outside_the_three_is_refused_at_construction() -> None:
    """A mistyped kind must not silently become the permissive one."""
    with pytest.raises(SupportKindError):
        DeclaredSupportKinds({("s", "c"): "corroborating"})
    with pytest.raises(SupportKindError):
        DeclaredSupportKinds({}, default="whatever")


def test_the_three_kinds_propagate_defeat_differently() -> None:
    """One graph, three readings, three answers — which is the whole point.

    ``source`` is defeated and supports ``conclusion``, which also cites its own
    span. As a **necessary** premise the defeat propagates and the conclusion
    falls. As the only **evidential** premise the conclusion's single declared line
    of evidence has fallen, so it falls too. As **contributory** the conclusion
    never rested on it and stands on its own anchor. A validator that treated all
    three alike would be a validator of one rule wearing three names.
    """
    claims = (_C("conclusion"), _C("source"), _C("counter"))
    edges = (
        _E("support", "source", "conclusion", 1),
        _E("attack", "counter", "source", 2),
    )
    view = _set(claims, edges)

    as_necessary = validate_support_dependencies(
        view, kinds=DeclaredSupportKinds({("source", "conclusion"): NECESSARY})
    ).verdict("conclusion")
    assert as_necessary.grounded is False
    assert REASON_NECESSARY_PREMISE_NOT_GROUNDED in as_necessary.reasons

    as_evidential = validate_support_dependencies(
        view, kinds=DeclaredSupportKinds({("source", "conclusion"): EVIDENTIAL})
    ).verdict("conclusion")
    assert as_evidential.grounded is False
    assert REASON_NO_SURVIVING_EVIDENCE in as_evidential.reasons

    as_contributory = validate_support_dependencies(
        view, kinds=DeclaredSupportKinds({("source", "conclusion"): CONTRIBUTORY})
    ).verdict("conclusion")
    assert as_contributory.grounded is True
    assert as_contributory.anchored is True
    assert as_contributory.basis == ()


def test_evidential_premises_are_disjunctive_among_themselves() -> None:
    """Two independent lines of evidence: losing one does not lose the claim.

    ``first`` is defeated and ``second`` is not, and the conclusion is grounded on
    what survives. Necessary premises could not behave this way, which is why the
    two kinds are not one kind with two names.
    """
    kinds = DeclaredSupportKinds(
        {
            ("first", "conclusion"): EVIDENTIAL,
            ("second", "conclusion"): EVIDENTIAL,
        }
    )
    view = _set(
        (_C("conclusion"), _C("first"), _C("second"), _C("counter")),
        (
            _E("support", "first", "conclusion", 1),
            _E("support", "second", "conclusion", 2),
            _E("attack", "counter", "first", 3),
        ),
    )
    verdict = validate_support_dependencies(view, kinds=kinds).verdict("conclusion")
    assert verdict.grounded is True
    assert verdict.basis == ("second",)

    # Defeat the survivor too and the group is gone, so the conclusion is gone.
    both_gone = _set(
        view.claims + (_C("second-counter"),),  # type: ignore[operator]
        view.edges + (_E("attack", "second-counter", "second", 4),),
    )
    fallen = validate_support_dependencies(both_gone, kinds=kinds).verdict(
        "conclusion"
    )
    assert fallen.grounded is False
    assert REASON_NO_SURVIVING_EVIDENCE in fallen.reasons
    assert fallen.failed_premises == ("first", "second")


def test_contributory_support_alone_is_not_a_grounding_basis() -> None:
    """Corroboration is not a foundation.

    The conclusion has no locator of its own and one perfectly healthy
    contributory premise. It is not grounded: ``contributory`` adds weight to
    something already standing, and there is nothing standing.
    """
    kinds = DeclaredSupportKinds({("corroboration", "conclusion"): CONTRIBUTORY})
    view = _set(
        (_C("conclusion", locator=None), _C("corroboration")),
        (_E("support", "corroboration", "conclusion", 1),),
    )
    table = validate_support_dependencies(view, kinds=kinds)
    assert table.verdict("corroboration").grounded is True
    conclusion = table.verdict("conclusion")
    assert conclusion.grounded is False
    assert REASON_NO_GROUNDING_BASIS in conclusion.reasons


def test_a_multi_hop_necessary_chain_grounds_end_to_end() -> None:
    """Conjunction is not just a one-hop rule.

    Three necessary hops back to an anchored premise: grounded. Defeat the deepest
    premise and the whole chain falls — which is what "the conclusion is not
    grounded, even though the labelling calls it warranted" means at depth.
    """
    claims = (_C("top"), _C("middle"), _C("bottom"))
    edges = (
        _E("support", "bottom", "middle", 1),
        _E("support", "middle", "top", 2),
    )
    grounded = validate_support_dependencies(_set(claims, edges))
    assert grounded.grounded_ids() == ("bottom", "middle", "top")

    broken = _set(
        claims + (_C("counter"),), edges + (_E("attack", "counter", "bottom", 3),)
    )
    labels = compute_statuses(broken)
    assert labels.statuses["top"].status == "warranted"
    table = validate_support_dependencies(broken)
    assert table.verdict("top").grounded is False
    assert table.verdict("middle").grounded is False


def test_premises_are_indexed_by_kind_and_self_support_is_dropped() -> None:
    """A claim cannot be its own premise, and the index says which kind is which."""
    kinds = DeclaredSupportKinds(
        {("e", "c"): EVIDENTIAL, ("k", "c"): CONTRIBUTORY}
    )
    edges = (
        _E("support", "n", "c", 1),
        _E("support", "e", "c", 2),
        _E("support", "k", "c", 3),
        _E("support", "c", "c", 4),  # self-support: a cycle of length one
        _E("attack", "x", "c", 5),
    )
    index = support_premises(edges, kinds)
    assert index["c"].necessary == ("n",)
    assert index["c"].evidential == ("e",)
    assert index["c"].contributory == ("k",)
    assert index["c"].grounding == ("e", "n")


# ── ACCEPTANCE 4: a cached validation is invalidated ────────────────────────


def test_a_changed_cited_source_version_invalidates_the_validation() -> None:
    """The staleness signal is an input, and it withdraws grounding.

    A claim is bound to its cited note's content hash at derivation time. When an
    index rebuild reports a different hash, the span the claim was read from is not
    the span that is there now, so the validation computed against the old version
    is not reused — the digest covers the source versions, so it cannot be.
    """
    view = _set((_C("anchor"),), ())
    fresh = GroundingValidator(_MutableSource(view), current_note_hashes={NOTE: HASH_V1})
    assert fresh.is_grounded("anchor")

    after_edit = fresh.with_note_hashes({NOTE: HASH_V2})
    verdict = after_edit.validate("anchor")
    assert verdict.grounded is False
    assert REASON_STALE_SOURCE in verdict.reasons
    assert grounding_digest(view.claims, view.edges, current_note_hashes={NOTE: HASH_V1}) != grounding_digest(
        view.claims, view.edges, current_note_hashes={NOTE: HASH_V2}
    )

    # A note absent from the rebuild's mapping is UNKNOWN, never asserted stale:
    # a partial rebuild must not unground the corpus.
    partial = fresh.with_note_hashes({"note-elsewhere": HASH_V2})
    assert partial.is_grounded("anchor")


def test_a_changed_premise_invalidates_the_validation() -> None:
    """Append the attack that defeats a premise and the verdict re-derives.

    Keyed by digest, like the status memo: the append yields a new key, the stale
    table is never read again, and no invalidation write is needed to say so —
    which is the only cache discipline an append-only log can support.
    """
    source = _MutableSource(
        _set(
            (_C("conclusion"), _C("source")),
            (_E("support", "source", "conclusion", 1),),
        )
    )
    validator = GroundingValidator(source)
    assert validator.is_grounded("conclusion")
    assert validator.is_grounded("conclusion")
    assert (validator.cache_misses, validator.cache_hits) == (1, 1)

    source.add_claims(_C("counter"))
    source.append(_E("attack", "counter", "source", 2))
    assert validator.is_grounded("conclusion") is False
    assert validator.cache_misses == 2
    assert validator.validate("conclusion").failed_premises == ("source",)


def test_reclassifying_one_support_edge_changes_the_digest() -> None:
    """The resolved kinds are part of the key, because they change the answer.

    A cache keyed on the graph alone would serve a verdict computed under a
    different reading of the same edge.
    """
    claims = (_C("conclusion"), _C("source"))
    edges = (_E("support", "source", "conclusion", 1),)
    conservative = grounding_digest(claims, edges)
    reclassified = grounding_digest(
        claims,
        edges,
        kinds=DeclaredSupportKinds({("source", "conclusion"): CONTRIBUTORY}),
    )
    assert conservative != reclassified
    # And it is stable: the same inputs digest the same way every time.
    assert conservative == grounding_digest(claims, edges)


def test_the_validator_is_a_pure_function_of_its_inputs() -> None:
    """Two readings of one snapshot agree, whatever order the rows arrive in."""
    claims = (_C("conclusion"), _C("source"), _C("counter"))
    edges = (
        _E("support", "source", "conclusion", 1),
        _E("attack", "counter", "source", 2),
    )
    once = validate_support_dependencies(_set(claims, edges))
    twice = validate_support_dependencies(
        _set(tuple(reversed(claims)), tuple(reversed(edges)))
    )
    assert once.digest == twice.digest
    assert dict(once.verdicts) == dict(twice.verdicts)


def test_the_one_shot_helpers_agree_with_the_table() -> None:
    """``grounding_verdict`` / ``is_grounded`` / ``is_answerable`` are the same
    computation with no memo — the shape the query path calls."""
    view = _set(
        (_C("conclusion"), _C("source")),
        (_E("support", "source", "conclusion", 1),),
    )
    table = validate_support_dependencies(view)
    assert grounding_verdict(view, "conclusion") == table.verdict("conclusion")
    assert is_grounded(view, "conclusion") is True
    assert is_answerable(view, "conclusion") is True

    # The gate is BOTH conditions: grounded but not warranted still abstains.
    assert is_grounded(view, "source") is True
    assert compute_statuses(view).statuses["source"].status == "proposed"
    assert is_answerable(view, "source") is False


def test_a_provisional_verdict_is_never_answerable() -> None:
    """A grounded, warranted claim whose chain touches a ``stub`` still abstains.

    The status query refuses such a verdict outright; the grounding table carries
    the flag instead of refusing, so a caller can see both halves — and
    :attr:`GroundingVerdict.answerable` is the half that must not say yes.
    """
    view = _set(
        (
            _C("conclusion"),
            _C("evidence"),
            _C("hearsay", provenance="stub"),
        ),
        (
            _E("support", "evidence", "conclusion", 1),
            _E("support", "hearsay", "evidence", 2),
        ),
    )
    kinds = DeclaredSupportKinds({("hearsay", "evidence"): CONTRIBUTORY})
    verdict = validate_support_dependencies(view, kinds=kinds).verdict("conclusion")
    assert verdict.status == "warranted"
    assert verdict.grounded is True
    assert verdict.provisional is True
    assert verdict.answerable is False


def test_the_memo_can_be_disabled_and_the_verdict_renders() -> None:
    """``cache_size=0`` recomputes every call — an escape hatch, not a mode."""
    source = _MutableSource(_set((_C("anchor"),), ()))
    validator = GroundingValidator(source, cache_size=0)
    validator.table()
    validator.table()
    assert (validator.cache_misses, validator.cache_hits) == (2, 0)
    assert validator.answerable("anchor") is False
    rendered = validator.validate("anchor").render()
    assert "grounded: True" in rendered
    assert "anchor: its own cited source span" in rendered


def test_a_narrower_claim_view_simply_has_no_anchor() -> None:
    """The labelling's view carries no locator, and that withholds grounding.

    Tolerated rather than rejected, so a caller holding the narrow view gets a
    conservative answer instead of an exception — but it is conservative in the
    direction that refuses, never the one that answers.
    """

    @dataclass(frozen=True)
    class _Narrow:
        claim_id: str
        provenance: str = "constructed"

    view = EdgeSet(claims=(_Narrow("bare"),), edges=())  # type: ignore[arg-type]
    verdict = validate_support_dependencies(view).verdict("bare")
    assert verdict.anchored is False
    assert verdict.grounded is False


def test_replacing_a_premise_text_yields_a_different_key() -> None:
    """Claim ids are content addresses, so "the premise changed" is "a new id".

    The digest therefore catches a premise edit without needing to hash claim
    texts: the edited premise is a different claim, and the edge naming it is a
    different edge.
    """
    original = (_C("conclusion"), _C("premise-v1"))
    edited = (_C("conclusion"), _C("premise-v2"))
    edges_v1 = (_E("support", "premise-v1", "conclusion", 1),)
    edges_v2 = (_E("support", "premise-v2", "conclusion", 1),)
    assert grounding_digest(original, edges_v1) != grounding_digest(edited, edges_v2)
    # And a locator move on the same claim is a different key too.
    moved = (replace(original[0], locator="h2:Elsewhere"), original[1])
    assert grounding_digest(original, edges_v1) != grounding_digest(moved, edges_v1)
