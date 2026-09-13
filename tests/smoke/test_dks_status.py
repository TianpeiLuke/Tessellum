"""P5 smoke tests — the corpus-level computed status.

Covers each clause of the phase's acceptance line:

1. Appending ONE attack flips statuses downstream, **including reinstatement**
   (defeat the attacker and the claim it defeated comes back), with **zero
   status writes** — proved three ways: the ``status_cache`` table stays empty,
   the log's rows are byte-identical before and after a batch of queries, and
   the module's source contains no write statement at all.
2. Appending a ``support`` edge **never changes any Dung label** — only the
   post-classification (``proposed`` → ``warranted``).
3. A **superseded claim leaves the framework**: it is not labelled ``out``
   (being replaced is not being defeated), and its attacks stop counting — but
   only when the replacement itself computes as ``warranted``. The pre-filter's
   rule gets four fixtures of its own, three of them regressions against the
   rejected reading ("the replacement is merely not ``out``"): an **unsupported**
   replacement, a **mutually attacked** one and a **defeated** one all retire
   nothing, and an ungrounded later row loses the tie to a warranted earlier one.
4. The per-cycle frozen labelling is **marked historical** — in the cycle
   result's own docstring and on the public trace-JSON surface.

Plus the properties those clauses rest on: only the ``attack`` subset enters the
framework, ``undec`` reports as ``challenged``, the labelling is memoised by an
edge-set digest that an append invalidates, acceptance is a second axis on which
nothing is ``accepted`` yet, and a verdict whose chain touches a ``stub`` claim
is REFUSED rather than printed.

All pure/local-I/O; no network, no model.
"""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import pytest

from tessellum.cli.main import main
from tessellum.dks.ontology import INDEPENDENT_VALIDATION_AVAILABLE
from tessellum.dks.status import (
    EdgeSet,
    ProvisionalStatusError,
    StatusQuery,
    UnknownClaimError,
    attack_pairs,
    classify,
    compute_statuses,
    edgeset_digest,
    explain,
    status,
)
from tessellum.runtime.claim_log import (
    ClaimDraft,
    ClaimLog,
    EdgeDraft,
    ORIGIN_PROJECTED,
    ORIGIN_QUERY,
)

SRC = Path(__file__).resolve().parents[2] / "src" / "tessellum"
STATUS_SOURCE = SRC / "dks" / "status.py"
CORE_SOURCE = SRC / "dks" / "core.py"


# ── in-memory fixtures: the port is structural, so no storage is needed ──────


@dataclass(frozen=True)
class _C:
    """A :class:`ClaimView` with nothing but what the labelling reads."""

    claim_id: str
    provenance: str = "constructed"


@dataclass(frozen=True)
class _E:
    """An :class:`EdgeView`."""

    op: str
    src: str
    dst: str
    seq: int
    evidence_locator: str | None = "note#L1"
    origin: str = "query"


def _set(claims: tuple[_C, ...], edges: tuple[_E, ...]) -> EdgeSet:
    return EdgeSet(claims=claims, edges=edges)


# ── real-log fixtures ───────────────────────────────────────────────────────


def _log(tmp_path: Path) -> ClaimLog:
    return ClaimLog.open(tmp_path / "runtime.db")


def _claim(name: str, *, provenance: str = "constructed") -> ClaimDraft:
    return ClaimDraft(
        derivation_id=f"derivation-{name}",
        text=f"Claim {name} asserts something that can be true or false.",
        note_id=f"note-{name}",
        locator="h2:Claim",
        provenance=provenance,
        source_note_hash="0" * 64,
    )


def _rows(path: Path, table: str) -> list[tuple]:
    conn = sqlite3.connect(path)
    try:
        return list(conn.execute(f"SELECT * FROM {table} ORDER BY seq"))
    finally:
        conn.close()


def _status_cache_rows(path: Path) -> list[tuple]:
    conn = sqlite3.connect(path)
    try:
        return list(conn.execute("SELECT * FROM status_cache"))
    finally:
        conn.close()


# ── the Dependency Rule + "no writes" as source properties ──────────────────


def test_the_status_module_is_pure_and_has_no_write_path() -> None:
    """DKS stays pure (no ``runtime`` import) and stores no status anywhere.

    A stored status is a label somebody has to keep true; the point of computing
    it is that nobody does. Both properties are structural, so they are asserted
    against the source rather than inferred from behaviour.
    """
    source = STATUS_SOURCE.read_text(encoding="utf-8")
    assert "tessellum.runtime" not in source
    assert not re.search(r"^\s*(from|import)\s+.*\bruntime\b", source, re.MULTILINE)
    for statement in ("INSERT", "UPDATE ", "DELETE", "executescript", "commit("):
        assert statement not in source, f"status.py must not {statement.strip()}"
    # No file or DB handles either — the log is read through the port.
    assert "sqlite3" not in source
    assert "open(" not in source


# ── layer 2: only the attack relation enters the framework ──────────────────


def test_only_the_attack_subset_is_projected_into_the_framework() -> None:
    """``support`` / ``revise`` / ``supersede`` are not attacks.

    Every edge here points at ``a``. If the whole edge set were fed to the
    solver, ``a`` would be defeated three times over; because only ``attack`` is
    projected, ``a`` is unattacked and the least-fixed-point guarantee still
    belongs to Dung rather than owing a new proof.
    """
    view = _set(
        (_C("a"), _C("s"), _C("r"), _C("x")),
        (
            _E("support", "s", "a", 1),
            _E("revise", "r", "a", 2),
            _E("supersede", "x", "r", 3),
        ),
    )
    assert attack_pairs(view.edges) == ()
    table = compute_statuses(view)
    assert table.labels["a"] == "in"
    assert table.statuses["a"].status == "warranted"  # supported, unattacked


def test_the_four_statuses_are_a_function_of_the_edge_set() -> None:
    """One snapshot, all four statuses — and ``undec`` reports as ``challenged``.

    ``m1``/``m2`` attack each other with no defender, so the fixed point leaves
    both ``undec``. A live unresolved dispute answers a question the same way a
    defeated claim does, so exposing a third "undecided" verdict would only
    invite a caller to treat it as a weak yes.

    ``new`` carries its own support edge, which is what makes its supersession of
    ``old`` count at all: the pre-filter admits a supersession only from a claim
    that computes as ``warranted``. That support edge is therefore load-bearing
    for this fixture, not decoration — see the two counter-fixtures below for
    what happens without it.
    """
    view = _set(
        (_C("w"), _C("s"), _C("p"), _C("d"), _C("k"), _C("old"), _C("new"),
         _C("ns"), _C("m1"), _C("m2")),
        (
            _E("support", "s", "w", 1),
            _E("attack", "k", "d", 2),
            _E("support", "ns", "new", 3),
            _E("supersede", "new", "old", 4),
            _E("attack", "m1", "m2", 5),
            _E("attack", "m2", "m1", 6),
        ),
    )
    table = compute_statuses(view)
    got = {cid: verdict.status for cid, verdict in table.statuses.items()}
    assert got["w"] == "warranted"
    assert got["p"] == "proposed"
    assert got["d"] == "challenged"
    assert got["new"] == "warranted"  # the replacement earned the supersession
    assert got["old"] == "superseded"
    assert got["m1"] == got["m2"] == "challenged"
    assert table.labels["m1"] == table.labels["m2"] == "undec"
    assert classify("undec", superseded=False, supported=True) == "challenged"
    assert set(table.summary()) == {
        "warranted",
        "proposed",
        "challenged",
        "superseded",
    }


# ── clause 2: a support edge never moves a Dung label ───────────────────────


def test_appending_a_support_edge_never_changes_a_dung_label(tmp_path: Path) -> None:
    """Only the post-classification moves: ``proposed`` → ``warranted``.

    The labelling is computed over the ``attack`` projection, which a support
    append does not touch. The digest DOES change (the edge set changed), so the
    memo is bypassed and the identical labels are a recomputation, not a stale
    read.
    """
    log = _log(tmp_path)
    a = log.append_claim(_claim("a"))
    s = log.append_claim(_claim("s"))
    query = StatusQuery(log)

    before = query.table()
    assert before.statuses[a.claim_id].status == "proposed"
    assert before.statuses[a.claim_id].supporters == ()

    log.append_edge(
        EdgeDraft("support", s.claim_id, a.claim_id, ORIGIN_QUERY, "note-s#L4")
    )
    after = query.table()

    assert after.digest != before.digest
    assert dict(after.labels) == dict(before.labels)
    assert after.statuses[a.claim_id].status == "warranted"
    assert after.statuses[a.claim_id].supporters == (s.claim_id,)
    # And the second axis did not move either: acceptance reads the Dung label.
    assert (
        after.statuses[a.claim_id].acceptance
        == before.statuses[a.claim_id].acceptance
    )


# ── clause 1: one attack flips statuses downstream, incl. reinstatement ─────


def test_appending_one_attack_flips_statuses_downstream_with_reinstatement(
    tmp_path: Path,
) -> None:
    """``a`` warranted → challenged by ``b`` → warranted again once ``b`` falls.

    Nothing was migrated between the three readings and no status was rewritten:
    each verdict is a fresh function of the edge set at that moment, which is the
    property a frozen per-cycle labelling cannot have.
    """
    log = _log(tmp_path)
    a = log.append_claim(_claim("a"))
    s = log.append_claim(_claim("s"))
    b = log.append_claim(_claim("b"))
    c = log.append_claim(_claim("c"))
    log.append_edge(
        EdgeDraft("support", s.claim_id, a.claim_id, ORIGIN_PROJECTED, "note-s#L2")
    )
    query = StatusQuery(log)
    assert query.status(a.claim_id).status == "warranted"

    log.append_edge(
        EdgeDraft("attack", b.claim_id, a.claim_id, ORIGIN_QUERY, "note-b#L7")
    )
    challenged = query.status(a.claim_id)
    assert challenged.status == "challenged"
    assert challenged.label == "out"
    assert challenged.attackers == (b.claim_id,)

    # Defeat the attacker: `a` is reinstated by the fixed point, not by an edit.
    log.append_edge(
        EdgeDraft("attack", c.claim_id, b.claim_id, ORIGIN_QUERY, "note-c#L3")
    )
    reinstated = query.status(a.claim_id)
    assert reinstated.status == "warranted"
    assert reinstated.label == "in"
    assert query.status(b.claim_id).status == "challenged"
    assert query.status(c.claim_id).status == "proposed"


def test_status_queries_write_nothing(tmp_path: Path) -> None:
    """Zero status writes: the cache table stays empty and the log is untouched.

    The runtime schema ships a ``status_cache`` table, and this is the test that
    the query surface does not use it: the memo lives in the query object, keyed
    by the edge-set digest, so an append invalidates it without any write.
    """
    log = _log(tmp_path)
    a = log.append_claim(_claim("a"))
    b = log.append_claim(_claim("b"))
    log.append_edge(EdgeDraft("attack", b.claim_id, a.claim_id, ORIGIN_QUERY))
    claims_before = _rows(log.path, "claims")
    edges_before = _rows(log.path, "edges")

    query = StatusQuery(log)
    query.table()
    query.status(a.claim_id)
    query.explain(a.claim_id)
    query.summary()
    status(log, b.claim_id)
    explain(log, b.claim_id)

    assert _status_cache_rows(log.path) == []
    assert _rows(log.path, "claims") == claims_before
    assert _rows(log.path, "edges") == edges_before


def test_the_memo_is_keyed_by_the_digest_and_an_append_invalidates_it(
    tmp_path: Path,
) -> None:
    """One recomputation per distinct edge set — and exactly one per append."""
    log = _log(tmp_path)
    a = log.append_claim(_claim("a"))
    b = log.append_claim(_claim("b"))
    query = StatusQuery(log)

    first = query.status(a.claim_id)
    assert (query.cache_misses, query.cache_hits) == (1, 0)
    query.status(a.claim_id)
    query.status(b.claim_id)
    assert (query.cache_misses, query.cache_hits) == (1, 2)

    log.append_edge(EdgeDraft("attack", b.claim_id, a.claim_id, ORIGIN_QUERY))
    flipped = query.status(a.claim_id)
    assert (query.cache_misses, query.cache_hits) == (2, 2)
    assert first.status == "proposed" and flipped.status == "challenged"

    # A claim appended with no edges is a real change too: the digest covers the
    # claim set, so the new claim cannot be missed by an edge-only key.
    digest_before = query.table().digest
    log.append_claim(_claim("lonely"))
    assert query.table().digest != digest_before
    assert query.status(_claim("lonely").claim_id).status == "proposed"


# ── clause 3: a superseded claim leaves the framework ───────────────────────


def test_a_superseded_claim_leaves_the_framework(tmp_path: Path) -> None:
    """It is not labelled ``out`` — and its attacks stop counting.

    ``b`` attacks ``a``; retiring ``b`` reinstates ``a`` without anyone having to
    discharge the attack, because a retired claim neither attacks nor is
    labelled. Being replaced is not being defeated, so ``b``'s Dung label is
    absent rather than ``out``.

    The successor is supported first, and that is a precondition rather than
    set-dressing: only a ``warranted`` replacement retires anything.
    """
    log = _log(tmp_path)
    a = log.append_claim(_claim("a"))
    b = log.append_claim(_claim("b"))
    successor = log.append_claim(_claim("successor"))
    ground = log.append_claim(_claim("ground"))
    log.append_edge(EdgeDraft("attack", b.claim_id, a.claim_id, ORIGIN_QUERY))
    log.append_edge(
        EdgeDraft(
            "support", ground.claim_id, successor.claim_id, ORIGIN_QUERY, "note-g#L1"
        )
    )
    query = StatusQuery(log)
    assert query.status(a.claim_id).status == "challenged"
    assert query.status(successor.claim_id).status == "warranted"

    log.supersede(
        superseding_claim_id=successor.claim_id,
        superseded_claim_id=b.claim_id,
        origin=ORIGIN_QUERY,
        evidence_locator="note-successor#L1",
    )
    table = query.table()
    retired = table.statuses[b.claim_id]
    assert retired.status == "superseded"
    assert retired.label is None
    assert retired.superseded_by == successor.claim_id
    assert b.claim_id not in table.live
    assert b.claim_id not in table.labels
    assert table.statuses[a.claim_id].status == "proposed"  # reinstated, unsupported


# ── the pre-filter's rule: only a WARRANTED replacement retires anything ─────


def test_an_unsupported_supersede_does_not_retire_the_current_claim() -> None:
    """A2's first counter-fixture, and the rule it establishes.

    ``new`` supersedes ``old`` and nothing supports ``new``, so ``new`` computes
    as ``proposed`` — surviving, but ungrounded. The rejected pre-filter asked
    only whether the replacement was *not* ``out``, which ``proposed`` satisfies,
    so ``old`` came back ``superseded``: an unsupported assertion silently
    withdrew the current answer. The rule is ``warranted``, so nothing is
    retired here and both claims stay in the framework.
    """
    view = _set(
        (_C("old"), _C("new")),
        (_E("supersede", "new", "old", 1),),
    )
    table = compute_statuses(view)
    assert table.statuses["new"].status == "proposed"  # survives, but ungrounded
    assert table.statuses["old"].status != "superseded"
    assert table.statuses["old"].status == "proposed"
    assert table.statuses["old"].superseded_by is None
    assert "old" in table.live
    assert table.labels["old"] == "in"  # still labelled: it never left


def test_a_mutually_attacked_supersede_does_not_retire_the_current_claim() -> None:
    """A2's second counter-fixture: an unresolved dispute retires nothing.

    ``new`` and ``old`` attack each other with no defender, so the fixed point
    leaves both ``undec`` and ``new`` computes as ``challenged``. ``new`` IS
    supported here, which isolates the variable: the supersession fails on the
    live dispute alone, not on missing support. Under the rejected rule ``undec``
    was "not ``out``" and ``old`` was retired by a claim the corpus had not
    settled — the replacement would have won its own dispute by removing the
    other side.
    """
    view = _set(
        (_C("old"), _C("new"), _C("ns")),
        (
            _E("support", "ns", "new", 1),
            _E("attack", "new", "old", 2),
            _E("attack", "old", "new", 3),
            _E("supersede", "new", "old", 4),
        ),
    )
    table = compute_statuses(view)
    assert table.labels["new"] == table.labels["old"] == "undec"
    assert table.statuses["new"].status == "challenged"
    assert table.statuses["old"].status != "superseded"
    assert table.statuses["old"].status == "challenged"
    assert table.statuses["old"].superseded_by is None
    assert "old" in table.live


def test_a_supersede_from_a_defeated_claim_does_not_count() -> None:
    """A defeated claim retires nothing either — ``r`` is ``out``.

    The weakest case of the same rule, and the only one the rejected pre-filter
    also got right.
    """
    view = _set(
        (_C("b"), _C("r"), _C("x")),
        (
            _E("attack", "x", "r", 1),
            _E("supersede", "r", "b", 2),
        ),
    )
    table = compute_statuses(view)
    assert table.labels["r"] == "out"
    assert table.statuses["b"].status == "proposed"  # still in the framework
    assert table.statuses["b"].superseded_by is None
    assert "b" in table.live


def test_the_latest_supersession_names_the_successor() -> None:
    """Two COUNTING supersessions of one claim: the later log position wins, so
    "current" is well defined rather than dependent on read order.

    Both replacements are supported, because a supersession that does not count
    cannot break a tie: with the pre-filter's rule in force, "latest" is the
    latest *warranted* replacement.
    """
    view = _set(
        (_C("b"), _C("first"), _C("second"), _C("g1"), _C("g2")),
        (
            _E("support", "g1", "first", 1),
            _E("support", "g2", "second", 2),
            _E("supersede", "first", "b", 3),
            _E("supersede", "second", "b", 4),
        ),
    )
    table = compute_statuses(view)
    assert table.statuses["first"].status == table.statuses["second"].status
    assert table.statuses["second"].status == "warranted"
    assert table.statuses["b"].superseded_by == "second"


def test_an_ungrounded_replacement_loses_the_tie_to_a_warranted_one() -> None:
    """Log position only orders the supersessions that count.

    ``late`` is appended after ``early`` and is unsupported, so it never enters
    the pre-filter; ``early`` is warranted, so it names the successor even though
    a later row also claims to replace ``b``. Under the rejected rule the answer
    was ``late`` — the newest row won regardless of whether anything stood
    behind it.
    """
    view = _set(
        (_C("b"), _C("early"), _C("late"), _C("g")),
        (
            _E("support", "g", "early", 1),
            _E("supersede", "early", "b", 2),
            _E("supersede", "late", "b", 3),
        ),
    )
    table = compute_statuses(view)
    assert table.statuses["late"].status == "proposed"
    assert table.statuses["b"].status == "superseded"
    assert table.statuses["b"].superseded_by == "early"


# ── the stub refusal ────────────────────────────────────────────────────────


def test_status_refuses_a_verdict_whose_chain_touches_a_stub(tmp_path: Path) -> None:
    """A located string is not a claim, so a verdict resting on one is refused.

    Most mechanically-located claim strings are not truth-apt as written;
    printing ``warranted`` for a document heading would launder a title into a
    verdict. The refusal is the default for both queries.
    """
    log = _log(tmp_path)
    a = log.append_claim(_claim("a"))
    stub = log.append_claim(_claim("stub", provenance="stub"))
    log.append_edge(
        EdgeDraft("support", stub.claim_id, a.claim_id, ORIGIN_PROJECTED, "note#L1")
    )
    query = StatusQuery(log)

    with pytest.raises(ProvisionalStatusError) as refused:
        query.status(a.claim_id)
    assert stub.claim_id in refused.value.stub_chain
    with pytest.raises(ProvisionalStatusError):
        query.explain(a.claim_id)


def test_allow_provisional_hard_labels_instead_of_refusing(tmp_path: Path) -> None:
    """The opt-out returns the verdict marked PROVISIONAL, never quietly."""
    log = _log(tmp_path)
    a = log.append_claim(_claim("a"))
    stub = log.append_claim(_claim("stub", provenance="stub"))
    log.append_edge(
        EdgeDraft("attack", stub.claim_id, a.claim_id, ORIGIN_PROJECTED, "note#L9")
    )
    query = StatusQuery(log)

    verdict = query.status(a.claim_id, allow_provisional=True)
    assert verdict.status == "challenged"
    assert verdict.provisional is True
    assert verdict.answerable is False
    assert verdict.stub_chain == (stub.claim_id,)

    rendered = query.explain(a.claim_id, allow_provisional=True).render()
    assert rendered.splitlines()[0].startswith("PROVISIONAL:")
    assert "provenance='stub'" in rendered
    assert "attacked by" in rendered


def test_the_refusal_is_chain_scoped_not_corpus_wide(tmp_path: Path) -> None:
    """A stub elsewhere in the log does not block an unrelated verdict.

    A deliberate divergence from the reference implementation, which refuses for
    the whole corpus when any claim is a stub. Scoping to the influencing chain
    keeps the refusal exactly as wide as the reason for it — and a warranted
    claim whose own chain is clean is answerable even while the corpus is being
    migrated off stubs.
    """
    log = _log(tmp_path)
    clean = log.append_claim(_claim("clean"))
    support = log.append_claim(_claim("support-of-clean"))
    log.append_edge(
        EdgeDraft("support", support.claim_id, clean.claim_id, ORIGIN_QUERY, "n#L1")
    )
    stub = log.append_claim(_claim("elsewhere", provenance="stub"))
    query = StatusQuery(log)

    verdict = query.status(clean.claim_id)
    assert verdict.status == "warranted"
    assert verdict.provisional is False
    assert verdict.answerable is True
    # The stub itself is still provisional — it IS its own chain.
    with pytest.raises(ProvisionalStatusError):
        query.status(stub.claim_id)


def test_an_unknown_claim_is_an_error_not_a_status(tmp_path: Path) -> None:
    log = _log(tmp_path)
    log.append_claim(_claim("a"))
    with pytest.raises(UnknownClaimError):
        StatusQuery(log).status("no-such-claim")
    with pytest.raises(UnknownClaimError):
        StatusQuery(log).explain("no-such-claim")


# ── the second axis ─────────────────────────────────────────────────────────


def test_acceptance_is_a_second_axis_and_nothing_is_accepted_yet() -> None:
    """The four statuses are the verdict; acceptance records an exogenous check.

    ``independently_validated`` is hard-wired ``False`` until the verification
    phase wires an independent validator, so a surviving claim is
    ``dialectically_adequate`` and never ``accepted`` — surviving the dialectic
    is necessary but not sufficient for truth. Both axes read the SAME Dung
    label, so they cannot disagree about survival.
    """
    assert INDEPENDENT_VALIDATION_AVAILABLE is False
    view = _set(
        (_C("w"), _C("s"), _C("p"), _C("d"), _C("k"), _C("old"), _C("new"),
         _C("ns")),
        (
            _E("support", "s", "w", 1),
            _E("attack", "k", "d", 2),
            _E("support", "ns", "new", 3),  # only a warranted claim supersedes
            _E("supersede", "new", "old", 4),
        ),
    )
    table = compute_statuses(view)
    assert table.statuses["w"].status == "warranted"
    assert table.statuses["w"].acceptance.status == "dialectically_adequate"
    assert table.statuses["p"].status == "proposed"
    assert table.statuses["p"].acceptance.status == "dialectically_adequate"
    assert table.statuses["d"].acceptance.status == "defeated"
    # The acceptance vocabulary cannot express `superseded`: a retired claim was
    # never labelled, so that axis reads `undecided` while the status axis
    # carries the temporal fact.
    assert table.statuses["old"].status == "superseded"
    assert table.statuses["old"].acceptance.status == "undecided"
    assert {v.acceptance.status for v in table.statuses.values()} != {"accepted"}
    assert all(
        v.acceptance.status != "accepted" for v in table.statuses.values()
    )


def test_the_digest_covers_provenance_so_constructing_a_stub_re_answers() -> None:
    """Constructing a stub moves no label but must move the ANSWER, so the digest
    covers provenance as well as the edge set."""
    claims = (_C("a"), _C("s", provenance="stub"))
    edges = (_E("support", "s", "a", 1),)
    stubby = edgeset_digest(claims, edges)
    constructed = edgeset_digest((_C("a"), _C("s")), edges)
    assert stubby != constructed


# ── clause 4: the frozen per-cycle field is marked historical ───────────────


def test_the_per_cycle_frozen_labelling_is_marked_historical() -> None:
    """The field survives (its trace shape is a public surface) but says so.

    Deleting ``DKSCycleResult.grounded_labelling`` would break every trace reader
    and the cycle's own survival selection, so the phase's "gone or marked
    historical" is discharged by marking: the docstring says the value is a
    frozen snapshot, says why that cannot be a status, and names the computed
    query that is one.
    """
    source = CORE_SOURCE.read_text(encoding="utf-8")
    field_at = source.index("grounded_labelling: dict[str, str] = field(")
    docstring = source[field_at : field_at + 1400]
    assert "**HISTORICAL**" in docstring
    assert "FROZEN SNAPSHOT" in docstring
    assert "tessellum.dks.status" in docstring
    assert "reinstate" in docstring


def test_the_trace_json_marks_the_frozen_labelling_historical(tmp_path: Path) -> None:
    """The public trace surface keeps the key and adds the marker beside it.

    Removing ``grounded_labelling`` from the trace would be a breaking change for
    every reader (the report and meta modes included), so the deprecation is
    additive: same key, plus a flag that says not to read it as a status.
    """
    obs = tmp_path / "obs.jsonl"
    obs.write_text(json.dumps({"summary": "an observation", "mode": "fresh"}) + "\n")
    responses = tmp_path / "responses.json"
    responses.write_text(
        json.dumps(
            {
                "conservative": json.dumps(
                    {
                        "claim": "A-claim",
                        "data": "D",
                        "warrant": "W",
                        "backing": "",
                        "qualifier": "",
                        "evidence": "E",
                    }
                ),
                "exploratory": json.dumps(
                    {
                        "claim": "B-claim",
                        "data": "D",
                        "warrant": "W",
                        "backing": "",
                        "qualifier": "",
                        "evidence": "E",
                    }
                ),
                "counter-argument": json.dumps(
                    {
                        "broken_component": "warrant",
                        "counter_claim": "fails here",
                        "reason": "scope mismatch",
                        "strength": "moderate",
                    }
                ),
                "pattern discovery": json.dumps(
                    {"description": "pattern", "observed": ["t1"]}
                ),
                "rule revision": json.dumps(
                    {
                        "claim": "Revised",
                        "data": "D",
                        "warrant": "Revised warrant",
                        "supersedes": "",
                    }
                ),
            }
        )
    )
    runs = tmp_path / "runs"
    code = main(
        [
            "dks",
            str(obs),
            "--mock-responses",
            str(responses),
            "--runs-dir",
            str(runs),
        ]
    )
    assert code == 0
    traces = sorted(runs.glob("*_cycle_*.json"))
    assert traces
    trace = json.loads(traces[0].read_text(encoding="utf-8"))
    assert "grounded_labelling" in trace  # kept: the shape is a public surface
    assert trace["grounded_labelling_is_historical"] is True


# ── the CLI query surface ───────────────────────────────────────────────────


def test_cli_claim_status_and_explain_read_the_log(tmp_path: Path, capsys) -> None:
    log = _log(tmp_path)
    a = log.append_claim(_claim("a"))
    s = log.append_claim(_claim("s"))
    log.append_edge(
        EdgeDraft("support", s.claim_id, a.claim_id, ORIGIN_QUERY, "note-s#L2")
    )

    code = main(
        ["dks", "--claim-log", str(log.path), "--claim-status", a.claim_id]
    )
    assert code == 0
    assert capsys.readouterr().out.strip() == "warranted"

    code = main(
        ["dks", "--claim-log", str(log.path), "--claim-explain", a.claim_id]
    )
    assert code == 0
    rendered = capsys.readouterr().out
    assert "status: warranted" in rendered
    assert f"supported by: {s.claim_id}" in rendered
    assert "note-s#L2" in rendered

    code = main(
        [
            "dks",
            "--claim-log",
            str(log.path),
            "--claim-summary",
            "--format",
            "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["claims"] == 2
    assert payload["by_status"] == {"warranted": 1, "proposed": 1}
    assert payload["provisional_claims"] == []

    # The query wrote nothing, the CLI included.
    assert _status_cache_rows(log.path) == []


def test_cli_refuses_a_stub_verdict_unless_provisional(tmp_path: Path, capsys) -> None:
    log = _log(tmp_path)
    a = log.append_claim(_claim("a"))
    stub = log.append_claim(_claim("stub", provenance="stub"))
    log.append_edge(
        EdgeDraft("support", stub.claim_id, a.claim_id, ORIGIN_PROJECTED, "n#L1")
    )

    code = main(["dks", "--claim-log", str(log.path), "--claim-status", a.claim_id])
    assert code == 2
    assert "REFUSED" in capsys.readouterr().err

    code = main(
        [
            "dks",
            "--claim-log",
            str(log.path),
            "--claim-status",
            a.claim_id,
            "--provisional",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert out.startswith("PROVISIONAL:")
    assert "warranted" in out


def test_cli_query_modes_need_a_log_and_report_a_bad_one(tmp_path: Path, capsys) -> None:
    code = main(["dks", "--claim-status", "whatever"])
    assert code == 2
    assert "--claim-log" in capsys.readouterr().err

    missing = tmp_path / "nope.db"
    code = main(["dks", "--claim-log", str(missing), "--claim-summary"])
    assert code == 2
    assert "does not exist" in capsys.readouterr().err

    # A database without the log tables is reported, never migrated into one.
    plain = tmp_path / "plain.db"
    conn = sqlite3.connect(plain)
    conn.execute("CREATE TABLE unrelated (x INTEGER)")
    conn.commit()
    conn.close()
    code = main(["dks", "--claim-log", str(plain), "--claim-summary"])
    assert code == 2
    assert "claim/edge log" in capsys.readouterr().err
    conn = sqlite3.connect(plain)
    try:
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
    finally:
        conn.close()
    assert "claims" not in tables


def test_cli_unknown_claim_exits_two(tmp_path: Path, capsys) -> None:
    log = _log(tmp_path)
    log.append_claim(_claim("a"))
    code = main(["dks", "--claim-log", str(log.path), "--claim-status", "ghost"])
    assert code == 2
    assert "no such claim" in capsys.readouterr().err
