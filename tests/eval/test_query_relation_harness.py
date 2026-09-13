"""The role/relation A/B harness: the question-set contract, the three metrics
that did not exist before it, and the admission rule.

The three acceptance clauses of the phases this harness serves are tested by
name below:

- the harness runs end to end on the example question set with stub arms and
  produces a verdict object (``TestEndToEnd``);
- the admission rule REFUSES arm 3 when its gain over arm 2 sits inside the
  uncertainty THIS harness estimates for it
  (``TestAdmissionRule.test_refuses_a_gain_inside_the_harnesss_own_uncertainty``);
- the ordering control detects an order-dependent gain — a fixture whose gain
  exists under one ordering and vanishes under the other is rejected
  (``TestAdmissionRule.test_rejects_a_gain_that_only_holds_under_one_ordering``);
- the historical build-noise interval is asymmetric, reference-only, never a
  default threshold, and never rendered as ± (``TestHistoricalInterval``);
- the paired estimate is deterministic for a fixed seed
  (``TestPairedUncertainty``).

Everything here is deterministic and calls no model.
"""
from __future__ import annotations

import importlib.util
import inspect
import json
import statistics
import sys
from dataclasses import asdict
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def _load_harness():
    """Load ``arms.py``; it loads ``metrics.py`` itself and exposes the module.

    ``eval/`` is not a package, so the harness is loaded by path — the same way
    ``test_answer_eval.py`` loads its own. Reaching the metrics through
    ``arms.metrics`` rather than loading the file a second time matters: a second
    load would define a second ``Locator`` class and frozen-dataclass equality is
    class-based, so nothing would ever match."""
    path = REPO / "eval" / "query_relation" / "arms.py"
    spec = importlib.util.spec_from_file_location("query_relation_arms", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["query_relation_arms"] = module
    spec.loader.exec_module(module)
    return module


A = _load_harness()
M = A.metrics

EXAMPLE = REPO / "eval" / "query_relation" / "question_set.example.json"
SCHEMA = REPO / "eval" / "query_relation" / "question_set.schema.json"


# ─────────────────────────────────────────────────────────────── fixtures ────


def _question(
    qid: str,
    *,
    answer: str = "Team Aurora",
    note: str = "catalog/a.md",
    field: str = "maintainer",
    line: int = 6,
    abstain: bool = False,
    reason: str | None = None,
    hops: tuple = (),
    traps: tuple = (),
):
    """One question, built directly rather than through JSON."""
    expected = (
        None
        if abstain
        else M.ExpectedAnswer(
            answer=answer, locator=M.Locator(note_id=note, field=field, line=line)
        )
    )
    if not abstain and not hops:
        hops = (M.Hop(locator=M.Locator(note_id=note, field=field, line=line)),)
    return M.Question(
        qid=qid,
        question=f"Which team maintains {qid}?",
        relation="maintainer",
        target=M.Target(surface=qid, entity_id=None if abstain and reason else f"c:{qid}"),
        abstain=abstain,
        abstain_reason=reason,
        expected=expected,
        hops=hops,
        conflation_traps=traps,
    )


def _set(questions, *, name: str = "rule_under_test", labelling: str = "human"):
    """A question set for a rule test.

    Labelled ``human`` on purpose: the fixture guard would otherwise refuse every
    verdict for the wrong reason and the rule under test would never be
    exercised. The guard itself is tested separately."""
    return M.QuestionSet(question_set=name, labelling=labelling, questions=tuple(questions))


def _scripted_arm(correct: set[str], *, budget=None, conflate: dict | None = None):
    """An arm that answers a fixed set of questions and abstains on the rest."""
    conflate = conflate or {}

    def factory():
        def answer(question, *, suppressed: tuple = ()):
            if question.qid in conflate:
                return M.AnswerAttempt(
                    qid=question.qid,
                    outcome="answered",
                    answer=conflate[question.qid],
                    locators=(M.Locator(note_id="catalog/a.md", field="author"),),
                    budget=budget or M.ModelBudget(),
                )
            if question.qid in correct and question.expected is not None:
                return M.AnswerAttempt(
                    qid=question.qid,
                    outcome="answered",
                    answer=question.expected.answer,
                    locators=tuple(h.locator for h in question.required_hops)
                    or (question.expected.locator,),
                    budget=budget or M.ModelBudget(),
                )
            return M.AnswerAttempt(
                qid=question.qid, outcome="abstained", budget=budget or M.ModelBudget()
            )

        return answer

    return factory


def _curriculum_arm(base: set[str], *, unlocked_by: dict[str, str]):
    """An arm whose extra answers depend on WHAT IT SAW EARLIER in the run.

    This is the order artifact the control exists to catch: a question in
    ``unlocked_by`` is answered only when its unlocking question came first, so
    the same arm scores differently under two orderings of the same set."""

    def factory():
        seen: set[str] = set()

        def answer(question, *, suppressed: tuple = ()):
            seen.add(question.qid)
            unlocked = unlocked_by.get(question.qid)
            answerable = question.qid in base or (unlocked is not None and unlocked in seen)
            if answerable and question.expected is not None:
                return M.AnswerAttempt(
                    qid=question.qid,
                    outcome="answered",
                    answer=question.expected.answer,
                    locators=(question.expected.locator,),
                )
            return M.AnswerAttempt(qid=question.qid, outcome="abstained")

        return answer

    return factory


# ────────────────────────────────────────────── the question-set contract ────


class TestQuestionSetFormat:
    def test_example_loads_and_is_declared_a_fixture(self):
        qs = M.load_question_set(EXAMPLE)
        assert qs.version == "1.0"
        assert qs.labelling == "synthetic_fixture" and qs.is_fixture
        assert len(qs.questions) == 8
        assert len(qs.answerable) == 4 and len(qs.should_abstain) == 4

    def test_abstention_questions_are_first_class_and_cover_every_reason(self):
        qs = M.load_question_set(EXAMPLE)
        reasons = {q.abstain_reason for q in qs.should_abstain}
        assert reasons == {
            "field_absent",
            "entity_unresolvable",
            "ambiguous_entity",
            "superseded_only",
        }
        assert all(q.expected is None for q in qs.should_abstain)

    def test_example_has_multi_hop_questions_with_a_bridge_and_a_conflation_trap(self):
        qs = M.load_question_set(EXAMPLE)
        assert len(qs.multi_hop) == 2
        assert all(q.bridge_hops for q in qs.multi_hop)
        trapped = [q for q in qs.questions if q.conflation_traps]
        assert len(trapped) == 1
        assert trapped[0].conflation_traps[0].relation == "author"

    @pytest.mark.skipif(
        importlib.util.find_spec("jsonschema") is None, reason="jsonschema not installed"
    )
    def test_example_validates_against_the_schema(self):
        import jsonschema

        jsonschema.validate(
            instance=json.loads(EXAMPLE.read_text(encoding="utf-8")),
            schema=json.loads(SCHEMA.read_text(encoding="utf-8")),
        )

    def test_rejects_an_abstain_question_carrying_an_expected_answer(self, tmp_path):
        raw = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        raw["questions"][2]["expected"] = {
            "answer": "Team Basalt",
            "locator": {"note_id": "catalog/signal_router.md"},
        }
        with pytest.raises(M.QuestionSetError):
            M.parse_question_set(raw, structural=False)

    def test_rejects_an_answerable_question_without_an_expected_answer(self):
        raw = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        raw["questions"][0].pop("expected")
        with pytest.raises(M.QuestionSetError):
            M.parse_question_set(raw, structural=False)

    def test_rejects_an_expected_answer_without_a_locator(self):
        raw = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        raw["questions"][0]["expected"].pop("locator")
        with pytest.raises(M.QuestionSetError, match="locator"):
            M.parse_question_set(raw, structural=False)

    def test_rejects_a_bridge_hop_that_is_not_required(self):
        # A bridge that may be skipped is not a bridge, and the shortcut control
        # would pass vacuously on it.
        raw = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        raw["questions"][5]["hops"][0]["required"] = False
        with pytest.raises(M.QuestionSetError, match="bridge"):
            M.parse_question_set(raw, structural=False)

    def test_rejects_a_duplicate_qid_and_an_unknown_abstain_reason(self):
        raw = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        raw["questions"][1]["qid"] = raw["questions"][0]["qid"]
        with pytest.raises(M.QuestionSetError, match="duplicate"):
            M.parse_question_set(raw, structural=False)
        raw = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        raw["questions"][2]["abstain_reason"] = "because_i_said_so"
        with pytest.raises(M.QuestionSetError, match="abstain_reason"):
            M.parse_question_set(raw, structural=False)

    def test_rejects_an_unknown_labelling(self):
        raw = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        raw["labelling"] = "vibes"
        with pytest.raises(M.QuestionSetError, match="labelling"):
            M.parse_question_set(raw, structural=False)

    def test_malformed_json_is_reported_not_raised_as_a_decode_error(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("{not json", encoding="utf-8")
        with pytest.raises(M.QuestionSetError):
            M.load_question_set(p)


# ───────────────────────────────────────────────────── scoring conventions ────


class TestScoringConventions:
    def test_punctuation_becomes_space_and_articles_go(self):
        assert M.normalise("Sam Bankman-Fried") == "sam bankman fried"
        assert M.normalise("  The   Quick, brown FOX. ") == "quick brown fox"

    def test_token_containment_not_character_substring(self):
        assert not M.tok_contains("It is not known", "no")
        assert M.tok_contains("The answer is no", "no")
        assert not M.tok_contains("claude add mcp", "claude mcp add")

    def test_aliases_count_as_the_expected_answer(self):
        exp = M.ExpectedAnswer(
            answer="Team Aurora", aliases=("Aurora",), locator=M.Locator(note_id="a.md")
        )
        assert M.answer_matches("Aurora", exp)
        assert M.answer_matches("the maintainer is Team Aurora", exp)
        assert not M.answer_matches("Team Basalt", exp)

    def test_agrees_with_the_reader_evals_rules(self):
        """The two scoring rules copied from ``answer_eval`` must not drift.

        Skipped rather than failed when ``answer_eval`` cannot import: it pulls
        the indexer, retrieval and the LLM bridge at module scope, and this
        harness deliberately does not."""
        path = REPO / "eval" / "digestion_pipeline" / "answer_eval.py"
        spec = importlib.util.spec_from_file_location("answer_eval_agreement", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["answer_eval_agreement"] = module
        try:
            spec.loader.exec_module(module)
        except Exception as e:  # noqa: BLE001 — its own imports, not ours
            pytest.skip(f"answer_eval not importable here: {type(e).__name__}: {e}")
        cases = [
            "Sam Bankman-Fried",
            "  The   Quick, brown FOX. ",
            "ENABLE_TOOL_SEARCH",
            "Team Aurora",
            "no",
        ]
        for s in cases:
            assert M.normalise(s) == module.normalise(s), s
        pairs = [
            ("It is not known", "no"),
            ("The answer is no", "no"),
            ("Run `claude mcp add` now", "claude mcp add"),
            ("claude add mcp", "claude mcp add"),
            ("Sam Bankman Fried", "Sam Bankman-Fried"),
            ("anything", ""),
        ]
        for ans, gold in pairs:
            assert M.tok_contains(ans, gold) == module.tok_contains(ans, gold), (ans, gold)


# ───────────────────────────────────────────────────────────────── locators ────


class TestLocator:
    def test_note_must_match(self):
        assert not M.Locator("a.md", field="x").satisfies(M.Locator("b.md", field="x"))

    def test_any_named_component_of_the_expectation_matches(self):
        expected = M.Locator("a.md", field="maintainer", line=6)
        assert M.Locator("a.md", field="maintainer").satisfies(expected)
        assert M.Locator("a.md", line=6).satisfies(expected)
        assert not M.Locator("a.md", field="author", line=4).satisfies(expected)

    def test_note_level_expectation_is_satisfied_by_the_note(self):
        assert M.Locator("a.md", field="anything").satisfies(M.Locator("a.md"))

    def test_a_citation_with_no_component_does_not_ground_a_field_expectation(self):
        # "the right name appears somewhere in this note" is the failure the
        # grounding rate exists to separate from an answer.
        assert not M.Locator("a.md").satisfies(M.Locator("a.md", field="maintainer"))


# ────────────────────────────────────────────────────────────── the metrics ────


class TestGroundingRate:
    def test_denominator_is_the_fixed_answerable_set_not_the_answers_given(self):
        """An arm that abstains on all but one easy question must not score 1.0."""
        qs = _set([_question(f"q{i}") for i in range(4)])
        attempts = {
            "q0": M.AnswerAttempt(
                qid="q0",
                outcome="answered",
                answer="Team Aurora",
                locators=(M.Locator("catalog/a.md", field="maintainer"),),
            ),
            **{f"q{i}": M.AnswerAttempt(qid=f"q{i}", outcome="abstained") for i in (1, 2, 3)},
        }
        met = M.score_arm("timid", qs, attempts)
        assert met.grounding_rate == pytest.approx(0.25)
        assert met.grounded_precision == pytest.approx(1.0)
        assert met.abstention.n_wasted == 3

    def test_a_right_answer_without_a_locator_is_not_grounded(self):
        qs = _set([_question("q0")])
        met = M.score_arm(
            "unlocated",
            qs,
            {"q0": M.AnswerAttempt(qid="q0", outcome="answered", answer="Team Aurora")},
        )
        assert met.n_grounded == 0
        assert met.grounding_rate == 0.0
        assert met.ungrounded_answer_rate == pytest.approx(1.0)
        assert met.graded[0].answer_correct is True and met.graded[0].locator_grounded is False

    def test_a_mislocated_citation_is_not_grounded(self):
        qs = _set([_question("q0")])
        met = M.score_arm(
            "elsewhere",
            qs,
            {
                "q0": M.AnswerAttempt(
                    qid="q0",
                    outcome="answered",
                    answer="Team Aurora",
                    locators=(M.Locator("catalog/other.md", field="maintainer"),),
                )
            },
        )
        assert met.grounding_rate == 0.0

    def test_answering_a_deserving_abstention_counts_as_ungrounded(self):
        qs = _set([_question("q0", abstain=True, reason="field_absent")])
        met = M.score_arm(
            "guesser",
            qs,
            {"q0": M.AnswerAttempt(qid="q0", outcome="answered", answer="Team Aurora")},
        )
        assert met.n_grounded == 0
        assert met.ungrounded_answer_rate == pytest.approx(1.0)
        assert met.abstention.abstained_on_deserving == 0.0

    def test_conflated_answer_is_graded_apart_from_a_plain_miss(self):
        trap = (M.ConflationTrap(relation="author", value="Team Cinder"),)
        qs = _set([_question("q0", answer="Team Basalt", traps=trap), _question("q1")])
        arm = _scripted_arm({"q1"}, conflate={"q0": "Team Cinder"})()
        attempts = {q.qid: arm(q) for q in qs.questions}
        met = M.score_arm("conflater", qs, attempts)
        assert met.n_conflated == 1
        assert met.conflation_rate == pytest.approx(1.0)  # one trapped question, hit
        assert met.grounding_rate == pytest.approx(0.5)

    def test_empty_stratum_is_nan_not_zero(self):
        qs = _set([_question("q0", abstain=True, reason="field_absent")])
        met = M.score_arm("x", qs, {"q0": M.AnswerAttempt(qid="q0", outcome="abstained")})
        assert met.grounding_rate != met.grounding_rate  # NaN: no answerable questions


class TestAbstentionCalibration:
    def test_both_halves_are_reported(self):
        qs = _set(
            [
                _question("a0"),
                _question("a1"),
                _question("n0", abstain=True, reason="field_absent"),
                _question("n1", abstain=True, reason="entity_unresolvable"),
            ]
        )
        attempts = {
            "a0": M.AnswerAttempt(
                qid="a0",
                outcome="answered",
                answer="Team Aurora",
                locators=(M.Locator("catalog/a.md", field="maintainer"),),
            ),
            "a1": M.AnswerAttempt(qid="a1", outcome="abstained"),
            "n0": M.AnswerAttempt(qid="n0", outcome="abstained"),
            "n1": M.AnswerAttempt(qid="n1", outcome="answered", answer="Team Basalt"),
        }
        cal = M.score_arm("half", qs, attempts).abstention
        assert cal.abstained_on_deserving == pytest.approx(0.5)
        assert cal.abstained_on_answerable == pytest.approx(0.5)
        assert cal.precision == pytest.approx(0.5)
        assert cal.n_wasted == 1
        assert cal.calibration_gap == pytest.approx(0.0)

    def test_a_surfaced_conflict_is_neither_an_answer_nor_an_abstention(self):
        qs = _set([_question("n0", abstain=True, reason="field_absent")])
        cal = M.score_arm(
            "three_way", qs, {"n0": M.AnswerAttempt(qid="n0", outcome="conflict")}
        ).abstention
        assert cal.n_conflict_on_deserving == 1
        assert cal.abstained_on_deserving == 0.0
        assert cal.n_abstentions == 0


class TestConnectedReasoning:
    def _two_hop_set(self):
        hops = (
            M.Hop(locator=M.Locator("catalog/a.md", line=12), bridge=True),
            M.Hop(locator=M.Locator("catalog/b.md", field="maintainer", line=6)),
        )
        return _set(
            [
                _question("m0", answer="Team Cinder", note="catalog/b.md", hops=hops),
                _question("s0"),
            ]
        )

    def _full_chain_attempt(self, qid="m0"):
        return M.AnswerAttempt(
            qid=qid,
            outcome="answered",
            answer="Team Cinder",
            locators=(
                M.Locator("catalog/a.md", line=12),
                M.Locator("catalog/b.md", field="maintainer"),
            ),
        )

    def test_full_chain_with_a_load_bearing_bridge_is_connected(self):
        qs = self._two_hop_set()
        met = M.score_arm(
            "chain",
            qs,
            {"m0": self._full_chain_attempt()},
            ablated_attempts={"m0": M.AnswerAttempt(qid="m0", outcome="abstained")},
        )
        assert met.connected.n_multi_hop == 1
        assert met.connected.n_connected == 1 and met.connected.rate == 1.0
        assert met.connected.shortcut_controlled is True

    def test_answering_with_the_bridge_suppressed_is_a_shortcut_not_connected(self):
        qs = self._two_hop_set()
        met = M.score_arm(
            "shortcut",
            qs,
            {"m0": self._full_chain_attempt()},
            ablated_attempts={"m0": self._full_chain_attempt()},  # still right without it
        )
        assert met.connected.n_chain_complete == 1
        assert met.connected.n_shortcut == 1
        assert met.connected.n_connected == 0 and met.connected.rate == 0.0

    def test_a_missing_hop_citation_is_not_connected(self):
        qs = self._two_hop_set()
        partial = M.AnswerAttempt(
            qid="m0",
            outcome="answered",
            answer="Team Cinder",
            locators=(M.Locator("catalog/b.md", field="maintainer"),),
        )
        met = M.score_arm(
            "partial",
            qs,
            {"m0": partial},
            ablated_attempts={"m0": M.AnswerAttempt(qid="m0", outcome="abstained")},
        )
        assert met.connected.n_chain_complete == 0 and met.connected.n_connected == 0
        assert met.graded[0].hops_cited == 1 and met.graded[0].hops_required == 2

    def test_without_the_ablated_reask_the_rate_is_not_shortcut_controlled(self):
        qs = self._two_hop_set()
        met = M.score_arm("uncontrolled", qs, {"m0": self._full_chain_attempt()})
        assert met.connected.rate == 1.0
        assert met.connected.shortcut_controlled is False

    def test_single_hop_questions_are_outside_the_denominator(self):
        qs = _set([_question("s0"), _question("s1")])
        met = M.score_arm("single", qs, {"s0": M.AnswerAttempt("s0", "abstained")})
        assert met.connected.n_multi_hop == 0
        assert met.connected.rate != met.connected.rate  # NaN, not 0.0


class TestModelBudget:
    def test_the_invariant_is_one_naming_k_reads_and_a_bounded_refutation(self):
        pol = M.BudgetPolicy()
        assert (pol.max_relation_naming, pol.max_refutations) == (1, M.REFUTATION_CAP)
        ok = M.ModelBudget(relation_naming=1, claim_reads=4, refutations=2, stop_checks=1)
        assert ok.total == 8 and pol.violations(ok) == ()

    def test_an_unbounded_refutation_is_a_reported_violation(self):
        pol = M.BudgetPolicy()
        bad = M.ModelBudget(relation_naming=2, claim_reads=99, refutations=40)
        v = pol.violations(bad)
        assert any("refutations" in x for x in v)
        assert any("claim_reads" in x for x in v)
        assert any("relation_naming" in x for x in v)

    def test_per_query_budget_is_counted_and_breaches_surface_on_the_arm(self):
        qs = _set([_question("q0"), _question("q1")])
        attempts = {
            "q0": M.AnswerAttempt(
                qid="q0",
                outcome="answered",
                answer="Team Aurora",
                locators=(M.Locator("catalog/a.md", field="maintainer"),),
                budget=M.ModelBudget(relation_naming=1, claim_reads=1, refutations=1),
            ),
            "q1": M.AnswerAttempt(
                qid="q1", outcome="abstained", budget=M.ModelBudget(refutations=9)
            ),
        }
        met = M.score_arm("spendy", qs, attempts)
        assert met.model_calls_per_query == pytest.approx((3 + 9) / 2)
        assert met.model_calls_max == 9
        assert any("q1" in v and "refutations" in v for v in met.budget_violations)

    def test_plus_returns_a_new_frozen_budget(self):
        b = M.ModelBudget()
        b2 = b.plus(claim_reads=2).plus(refutations=1)
        assert (b.total, b2.total) == (0, 3)


class TestHistoricalInterval:
    """The imported figure is kept as the asymmetric interval it is, and is
    reference-only: it is the default threshold of nothing."""

    def test_it_is_an_asymmetric_interval_not_a_plus_minus_figure(self):
        iv = M.HISTORICAL_BUILD_NOISE_INTERVAL
        assert (iv.low, iv.high) == (-0.047, 0.018)
        assert iv.symmetric is False  # there is no "±0.047" form of this
        assert iv.render() == "[-0.047, +0.018]"
        assert not hasattr(iv, "plus_minus")

    def test_its_provenance_records_why_it_does_not_transfer(self):
        prov = M.HISTORICAL_BUILD_NOISE_INTERVAL.provenance.lower()
        for token in ("proxy", "mismatch", "37-document", "not a significance threshold"):
            assert token in prov, token
        # measured on a build-noise probe, so it does not transfer to this harness
        assert M.HISTORICAL_BUILD_NOISE_INTERVAL.transfers_to("fixed-vault lookup") is False

    def test_the_old_scalar_constant_is_gone(self):
        # `BUILD_NOISE_FLOOR = 0.047` was the shape that invited the misuse: a
        # single number, importable as a threshold, with the asymmetry discarded.
        assert not hasattr(M, "BUILD_NOISE_FLOOR")
        assert not hasattr(A, "BUILD_NOISE_FLOOR")

    def test_it_is_not_the_default_threshold_of_the_admission_rule(self):
        defaults = {
            p.name: p.default
            for p in inspect.signature(A.admission_verdict).parameters.values()
        }
        assert defaults["min_gain"] is None
        assert 0.047 not in [d for d in defaults.values() if isinstance(d, float)]
        # and no verdict field carries it either
        base = {f"q{i:02d}" for i in range(40)}
        v = A.p11_verdict(_ab_report(base, base | {f"q{i:02d}" for i in range(40, 45)}))
        assert v.min_gain is None
        assert "0.047" not in v.render()

    def test_no_verdict_or_report_renders_a_plus_minus(self):
        base = {f"q{i:02d}" for i in range(40)}
        report = _ab_report(base, base | {f"q{i:02d}" for i in range(40, 45)})
        assert "±" not in A.p11_verdict(report).render()
        assert "±" not in A.render_report(report)
        assert "±" not in A.p2_verdict(report, target=0.5).render()

    def test_a_caller_may_impose_an_extra_floor_explicitly(self):
        """If a caller wants an absolute floor — even this one — they pass it."""
        base = {f"q{i:02d}" for i in range(40)}
        report = _ab_report(base, base | {f"q{i:02d}" for i in range(40, 45)})  # +0.10
        assert A.p11_verdict(report).admitted is True  # the paired bar alone
        floor = abs(M.HISTORICAL_BUILD_NOISE_INTERVAL.low)  # 0.047, passed explicitly
        assert A.p11_verdict(report, min_gain=floor).admitted is True
        strict = A.p11_verdict(report, min_gain=0.20)
        assert strict.admitted is False
        assert strict.min_gain == 0.20
        assert all(g.clears_uncertainty for g in strict.per_ordering)
        assert all(g.clears_min_gain is False for g in strict.per_ordering)
        assert any("caller-supplied floor" in r for r in strict.reasons)


class TestPairedUncertainty:
    """The harness's own uncertainty: paired per question, seeded, replayable."""

    def _diffs(self, metric="grounding_rate", *, n=50, extra=5):
        base = {f"q{i:02d}" for i in range(20)}
        cand = base | {f"q{i:02d}" for i in range(20, 20 + extra)}
        qs = _set([_question(f"q{i:02d}") for i in range(n)])
        b = A.run_arm(A.ARM_NODE_FIRST, _scripted_arm(base), qs, "as_given").metrics
        c = A.run_arm(A.ARM_DERIVATION, _scripted_arm(cand), qs, "as_given").metrics
        return M.paired_differences(metric, [b], [c])

    def test_pairs_per_question_and_the_difference_is_the_gain(self):
        d = self._diffs()
        assert d.n == 50 and d.unpaired_qids == ()
        assert sum(1 for x in d.differences if x > 0) == 5
        assert d.mean == pytest.approx(0.10)

    def test_the_per_question_decomposition_reproduces_the_aggregate_rate(self):
        qs = M.load_question_set(EXAMPLE)
        met = A.run_arm(
            A.ARM_NODE_FIRST,
            A.node_first_arm(A.oracle_resolver(qs), A.oracle_field_reader(qs)),
            qs,
            "as_given",
        ).metrics
        for name in M.PAIRABLE_METRICS:
            scores = M.per_question_scores(met, name)
            if not scores:
                continue
            assert statistics.fmean(scores.values()) == pytest.approx(
                M.metric_value(met, name)
            ), name

    def test_a_metric_with_an_arm_chosen_denominator_is_refused_not_mispaired(self):
        d = self._diffs()
        assert "grounded_precision" in M.UNPAIRABLE_METRICS
        with pytest.raises(M.NotPairable):
            M.paired_differences("grounded_precision", [], [])
        with pytest.raises(KeyError):
            M.paired_differences("no_such_metric", [], [])
        assert d.metric == "grounding_rate"

    def test_the_bootstrap_is_deterministic_for_a_fixed_seed(self):
        d = self._diffs()
        one = M.paired_uncertainty(d, seed=4242)
        two = M.paired_uncertainty(d, seed=4242)
        assert (one.ci_low, one.ci_high) == (two.ci_low, two.ci_high)
        assert one == two
        assert one.seed == 4242 and one.resamples == M.DEFAULT_BOOTSTRAP_RESAMPLES
        # the point estimate and the standard error do not depend on the seed at all
        other = M.paired_uncertainty(d, seed=99)
        assert other.mean_difference == pytest.approx(one.mean_difference)
        assert other.standard_error == pytest.approx(one.standard_error)

    def test_the_standard_error_method_agrees_in_sign_and_ignores_the_seed(self):
        d = self._diffs()
        se = M.paired_uncertainty(d, method=M.PAIRED_STANDARD_ERROR, seed=1)
        assert se == M.paired_uncertainty(d, method=M.PAIRED_STANDARD_ERROR, seed=2)
        assert se.resamples == 0 and se.seed == 0
        assert se.excludes_zero is True  # +0.10 over 50 questions
        assert se.standard_error == pytest.approx(
            se.stdev_difference / len(d.differences) ** 0.5
        )

    def test_a_gain_of_one_question_does_not_exclude_zero(self):
        d = self._diffs(extra=1)  # +0.02 over 50 questions
        unc = M.paired_uncertainty(d)
        assert unc.mean_difference == pytest.approx(0.02)
        assert unc.ci_low <= 0.0 and unc.excludes_zero is False

    def test_the_interval_is_reported_as_two_bounds_never_as_a_margin(self):
        unc = M.paired_uncertainty(self._diffs())
        assert "±" not in unc.render()
        assert unc.render().startswith("95% CI [")
        assert unc.ci_low < unc.mean_difference < unc.ci_high

    def test_an_unknown_method_or_confidence_is_rejected(self):
        d = self._diffs()
        with pytest.raises(ValueError, match="unknown method"):
            M.paired_uncertainty(d, method="vibes")
        with pytest.raises(ValueError, match="confidence"):
            M.paired_uncertainty(d, confidence=1.5)


class TestSummaryStatistics:
    def test_mean_and_sample_spread_are_both_reported(self):
        s = M.summarise("grounding_rate", [0.4, 0.6, 0.5])
        assert s.mean == pytest.approx(0.5) and s.stdev == pytest.approx(0.1)
        assert s.n == 3 and s.n_missing == 0

    def test_a_single_run_has_no_measured_spread(self):
        s = M.summarise("grounding_rate", [0.4])
        assert s.stdev == 0.0 and s.n == 1

    def test_nan_runs_are_dropped_and_counted(self):
        s = M.summarise("grounding_rate", [float("nan"), 0.5])
        assert s.n == 1 and s.n_missing == 1 and s.mean == pytest.approx(0.5)

    def test_all_nan_is_not_measured(self):
        s = M.summarise("grounding_rate", [float("nan")])
        assert s.measured is False


# ─────────────────────────────────────────────────────────────────── the arms ────


class TestNodeFirstArm:
    def _arm(self, qs):
        return A.node_first_arm(A.oracle_resolver(qs), A.oracle_field_reader(qs))()

    def test_answers_from_the_authored_field_with_its_locator_and_no_model_call(self):
        qs = M.load_question_set(EXAMPLE)
        attempt = self._arm(qs)(qs.by_id("q001"))
        assert attempt.outcome == "answered" and attempt.answer == "Team Aurora"
        assert attempt.locators[0].field == "maintainer"
        assert attempt.budget.total == 0

    def test_abstains_when_the_field_is_absent(self):
        qs = M.load_question_set(EXAMPLE)
        a = self._arm(qs)(qs.by_id("q003"))
        assert a.outcome == "abstained" and a.reason == "field_absent"

    def test_abstains_on_an_ambiguous_surface_rather_than_picking(self):
        qs = M.load_question_set(EXAMPLE)
        a = self._arm(qs)(qs.by_id("q004"))
        assert a.outcome == "abstained" and a.reason == "ambiguous_entity"
        assert len(a.diagnostics) == 2

    def test_abstains_on_an_unresolvable_surface(self):
        qs = M.load_question_set(EXAMPLE)
        a = self._arm(qs)(qs.by_id("q005"))
        assert a.outcome == "abstained" and a.reason == "entity_unresolvable"

    def test_a_closed_validity_interval_is_not_a_current_answer(self):
        qs = M.load_question_set(EXAMPLE)
        a = self._arm(qs)(qs.by_id("q007"))
        assert a.outcome == "abstained" and a.reason == "superseded_only"

    def test_cannot_reach_a_multi_hop_answer(self):
        qs = M.load_question_set(EXAMPLE)
        assert self._arm(qs)(qs.by_id("q006")).outcome == "abstained"

    def test_a_suppressed_span_is_not_read(self):
        qs = M.load_question_set(EXAMPLE)
        q = qs.by_id("q001")
        a = self._arm(qs)(q, suppressed=(q.expected.locator,))
        assert a.outcome == "abstained"


class TestDerivationArm:
    def _arm(self, qs, **kw):
        return A.derivation_arm(
            A.oracle_resolver(qs), A.oracle_field_reader(qs), A.oracle_derivation(qs, **kw)
        )()

    def test_consults_the_cheap_read_first_and_spends_nothing_on_a_hit(self):
        qs = M.load_question_set(EXAMPLE)
        a = self._arm(qs)(qs.by_id("q001"))
        assert a.outcome == "answered" and a.budget.total == 0
        assert any("memory_hit" in d for d in a.diagnostics)

    def test_derives_the_multi_hop_answer_with_the_whole_chain(self):
        qs = M.load_question_set(EXAMPLE)
        a = self._arm(qs)(qs.by_id("q006"))
        assert a.outcome == "answered" and a.answer == "Team Cinder"
        assert len(a.locators) == 2
        assert (a.budget.relation_naming, a.budget.claim_reads, a.budget.refutations) == (1, 2, 1)

    def test_abstains_when_the_bridge_hop_is_suppressed(self):
        qs = M.load_question_set(EXAMPLE)
        q = qs.by_id("q006")
        a = self._arm(qs)(q, suppressed=tuple(h.locator for h in q.bridge_hops))
        assert a.outcome == "abstained" and a.reason == "bridge_hop_suppressed"

    def test_an_answer_with_no_locator_is_withheld_not_reported(self):
        qs = _set([_question("q0")])

        def ungrounded(_request):
            return A.DerivationResult(outcome="answered", answer="Team Aurora")

        arm = A.derivation_arm(
            A.oracle_resolver(qs), lambda *_: None, ungrounded
        )()
        a = arm(qs.questions[0])
        assert a.outcome == "abstained" and a.answer == ""
        assert any("ungrounded answer withheld" in d for d in a.diagnostics)

    def test_a_budget_breach_is_recorded_on_the_attempt(self):
        qs = M.load_question_set(EXAMPLE)
        a = self._arm(qs, refutations=9)(qs.by_id("q006"))
        assert a.budget.refutations == 9  # not clipped
        assert any("refutations" in d for d in a.diagnostics)


class TestStatusQuoArm:
    def test_it_cannot_run_here_and_is_reported_not_scored(self):
        qs = M.load_question_set(EXAMPLE)
        run = A.run_arm(A.ARM_STATUS_QUO, A.status_quo_arm(), qs, "as_given")
        assert run.metrics is None
        assert run.unavailable and "outside this repository" in run.unavailable

    def test_the_factory_raises_rather_than_answering(self):
        with pytest.raises(A.ArmUnavailable):
            A.external_arm("x", "elsewhere")()


# ────────────────────────────────────────────────────────── ordering control ────


class TestOrderings:
    def test_named_orderings_are_deterministic_and_permutations(self):
        qs = _set([_question(f"q{i}") for i in range(8)])
        a = A.order_questions(qs.questions, "shuffle:ordering_a")
        b = A.order_questions(qs.questions, "shuffle:ordering_b")
        assert {q.qid for q in a} == {q.qid for q in qs.questions}
        assert a == A.order_questions(qs.questions, "shuffle:ordering_a")
        assert [q.qid for q in a] != [q.qid for q in b]
        assert [q.qid for q in A.order_questions(qs.questions, "reversed")] == [
            f"q{i}" for i in reversed(range(8))
        ]

    def test_an_unknown_ordering_is_rejected(self):
        with pytest.raises(ValueError, match="unknown ordering"):
            A.order_questions((), "alphabetical")

    def test_each_run_gets_a_fresh_arm_so_state_cannot_leak(self):
        qs = _set([_question("seed"), _question("dep")])
        factory = _curriculum_arm({"seed"}, unlocked_by={"dep": "seed"})
        report = A.run_ab(qs, {A.ARM_NODE_FIRST: factory}, runs=2, orderings=("reversed",))
        # Under "reversed" the unlocking question comes second, so `dep` must be
        # unanswered in EVERY run — a leaked cache would answer it in run 2.
        rates = [r.metrics.grounding_rate for r in report.runs]
        assert rates == [0.5, 0.5]


# ─────────────────────────────────────────────────────── the admission rule ────


def _ab_report(baseline_correct, candidate_correct, *, n=50, **kw):
    """A report over ``n`` answerable questions with two scripted arms."""
    qs = _set([_question(f"q{i:02d}") for i in range(n)])
    return A.run_ab(
        qs,
        {
            A.ARM_NODE_FIRST: _scripted_arm(baseline_correct),
            A.ARM_DERIVATION: _scripted_arm(candidate_correct, **kw),
        },
        runs=3,
        orderings=("as_given", "reversed"),
    )


class TestAdmissionRule:
    def test_refuses_a_gain_inside_the_harnesss_own_uncertainty(self):
        """40/50 vs 41/50 is a +0.02 gain: ONE question of fifty flipped.

        The paired interval on the mean difference includes zero, so the gain has
        not been separated from this harness's own uncertainty — which is the bar,
        rather than any figure imported from another experiment."""
        base = {f"q{i:02d}" for i in range(40)}
        cand = {f"q{i:02d}" for i in range(41)}
        v = A.p11_verdict(_ab_report(base, cand))
        assert v.admitted is False
        assert v.baseline_arm == A.ARM_NODE_FIRST
        gains = {g.ordering: g for g in v.per_ordering}
        assert all(g.gain == pytest.approx(0.02) for g in gains.values())
        assert all(not g.clears_uncertainty for g in gains.values())
        for g in gains.values():
            assert g.n_pairs == 50
            assert g.uncertainty.ci_low <= 0.0 <= g.uncertainty.ci_high
            assert g.uncertainty.mean_difference == pytest.approx(g.gain)
        assert any("lies inside this harness's paired" in r for r in v.reasons)
        assert "REFUSED" in v.render()

    def test_admits_a_gain_outside_the_uncertainty_under_every_ordering(self):
        base = {f"q{i:02d}" for i in range(40)}
        cand = {f"q{i:02d}" for i in range(45)}
        v = A.p11_verdict(_ab_report(base, cand))
        assert v.admitted is True and v.reasons == ()
        assert all(g.gain == pytest.approx(0.10) for g in v.per_ordering)
        assert all(g.uncertainty.ci_low > 0.0 for g in v.per_ordering)
        assert v.method == A.PAIRED_BOOTSTRAP and v.confidence == 0.95
        assert "ADMITTED" in v.render()

    def test_a_verdict_is_reproducible_from_its_recorded_seed(self):
        base = {f"q{i:02d}" for i in range(40)}
        report = _ab_report(base, {f"q{i:02d}" for i in range(45)})
        first = A.p11_verdict(report)
        again = A.p11_verdict(report, seed=first.seed)
        assert [g.uncertainty.ci_low for g in first.per_ordering] == [
            g.uncertainty.ci_low for g in again.per_ordering
        ]
        assert first.render() == again.render()

    def test_rejects_a_gain_that_only_holds_under_one_ordering(self):
        """The order-artifact fixture: a gain under one ordering, none under the other.

        The candidate answers four extra questions only when an unlocking
        question was asked earlier in the same run. Under ``as_given`` the
        unlocker comes first (+0.20); under ``reversed`` it comes last (+0.00).
        The gain must hold under BOTH, so the harness rejects it."""
        n = 20
        base_correct = {f"q{i:02d}" for i in range(10)}
        unlocked_by = {f"q{i:02d}": "q00" for i in (10, 11, 12, 13)}
        qs = _set([_question(f"q{i:02d}") for i in range(n)])
        report = A.run_ab(
            qs,
            {
                A.ARM_NODE_FIRST: _scripted_arm(base_correct),
                A.ARM_DERIVATION: _curriculum_arm(base_correct, unlocked_by=unlocked_by),
            },
            runs=3,
            orderings=("as_given", "reversed"),
        )
        gains = {g.ordering: g for g in A.p11_verdict(report).per_ordering}
        assert gains["as_given"].gain == pytest.approx(0.20)
        assert gains["as_given"].clears_uncertainty is True
        assert gains["reversed"].gain == pytest.approx(0.0)
        assert gains["reversed"].clears_uncertainty is False

        v = A.p11_verdict(report)
        assert v.admitted is False
        assert any("reversed" in r and "lies inside" in r for r in v.reasons)
        # and the same arms with the ordering control switched off would have
        # passed — which is the point of running more than one ordering.
        one_ordering = A.run_ab(
            qs,
            {
                A.ARM_NODE_FIRST: _scripted_arm(base_correct),
                A.ARM_DERIVATION: _curriculum_arm(base_correct, unlocked_by=unlocked_by),
            },
            runs=3,
            orderings=("as_given",),
        )
        lax = A.p11_verdict(one_ordering, min_orderings=1)
        assert lax.admitted is True

    def test_refuses_when_fewer_than_two_orderings_were_run(self):
        base = {f"q{i:02d}" for i in range(40)}
        cand = {f"q{i:02d}" for i in range(45)}
        qs = _set([_question(f"q{i:02d}") for i in range(50)])
        report = A.run_ab(
            qs,
            {
                A.ARM_NODE_FIRST: _scripted_arm(base),
                A.ARM_DERIVATION: _scripted_arm(cand),
            },
            runs=3,
            orderings=("as_given",),
        )
        v = A.p11_verdict(report)
        assert v.admitted is False
        assert any("at least 2" in r for r in v.reasons)

    def test_refuses_on_too_few_runs_to_report_a_spread(self):
        base = {f"q{i:02d}" for i in range(40)}
        cand = {f"q{i:02d}" for i in range(45)}
        qs = _set([_question(f"q{i:02d}") for i in range(50)])
        report = A.run_ab(
            qs,
            {
                A.ARM_NODE_FIRST: _scripted_arm(base),
                A.ARM_DERIVATION: _scripted_arm(cand),
            },
            runs=1,
            orderings=("as_given", "reversed"),
        )
        v = A.p11_verdict(report)
        assert v.admitted is False
        assert any("scored run" in r for r in v.reasons)

    def test_run_spread_is_reported_and_not_subtracted_from_the_gain(self):
        """The run-to-run spread is a REPORTED quantity, not an interval.

        Subtracting it from the gain was an invented margin — the code that did it
        said so itself ("not a confidence interval") — and it is gone. The spread
        is still carried on every ordering, because the plan requires repeated runs
        with their variance reported; the DECISION is made by the paired estimate."""
        base = {f"q{i:02d}" for i in range(40)}
        v = A.p11_verdict(_ab_report(base, {f"q{i:02d}" for i in range(45)}))
        g = v.per_ordering[0]
        assert not hasattr(g, "variance_margin")
        assert not hasattr(g, "clears_floor")
        assert (g.baseline_stdev, g.candidate_stdev) == (0.0, 0.0)  # deterministic arms
        assert g.n_runs == 3
        assert g.uncertainty is not None and g.uncertainty.n_pairs == 50
        assert "run sd" in v.render()

    def test_refuses_an_unjustified_rise_in_abstention(self):
        # The candidate answers MORE questions correctly and also withholds more
        # of the answerable ones: the gain is outside the paired uncertainty and
        # the abstention guard still refuses, because the plan requires both
        # halves to hold. The rise is judged against ITS OWN paired standard
        # error, not against a threshold from elsewhere.
        qs = _set(
            [_question(f"q{i:02d}") for i in range(40)]
            + [_question(f"n{i}", abstain=True, reason="field_absent") for i in range(4)]
        )
        wrong_answer = M.AnswerAttempt(
            qid="", outcome="answered", answer="Team Basalt", locators=()
        )

        def loose_factory():
            def answer(question, *, suppressed=()):
                if question.abstain:
                    return M.AnswerAttempt(qid=question.qid, outcome="abstained")
                if question.qid in {f"q{i:02d}" for i in range(24)}:
                    return M.AnswerAttempt(
                        qid=question.qid,
                        outcome="answered",
                        answer=question.expected.answer,
                        locators=(question.expected.locator,),
                    )
                # answers anyway, wrongly and with no locator: never abstains
                return M.AnswerAttempt(
                    qid=question.qid, outcome="answered", answer=wrong_answer.answer
                )

            return answer

        report = A.run_ab(
            qs,
            {
                A.ARM_NODE_FIRST: loose_factory,
                A.ARM_DERIVATION: _scripted_arm({f"q{i:02d}" for i in range(32)}),
            },
            runs=3,
            orderings=("as_given", "reversed"),
        )
        v = A.p11_verdict(report)
        # 24/40 -> 32/40: a +0.20 gain, and it does clear the paired uncertainty
        assert all(g.gain == pytest.approx(0.20) for g in v.per_ordering)
        assert all(g.clears_uncertainty for g in v.per_ordering)
        # ... and the verdict still refuses, on the abstention half alone
        assert v.admitted is False
        assert any("abstention on answerable" in r for r in v.reasons)
        assert any("paired standard error" in r for r in v.reasons)

    def test_refuses_a_candidate_that_broke_its_model_budget(self):
        base = {f"q{i:02d}" for i in range(40)}
        cand = {f"q{i:02d}" for i in range(48)}
        report = _ab_report(base, cand, budget=M.ModelBudget(refutations=20))
        v = A.p11_verdict(report)
        assert v.admitted is False
        assert any("matched cost" in r for r in v.reasons)
        # ... and passes once the guard is explicitly disabled, so the refusal is
        # attributable to the budget and nothing else.
        assert A.p11_verdict(report, budget_guard=False).admitted is True

    def test_refuses_a_fixture_labelled_question_set(self):
        qs = M.load_question_set(EXAMPLE)
        report = A.run_ab(
            qs,
            {
                A.ARM_NODE_FIRST: A.node_first_arm(
                    A.oracle_resolver(qs), A.oracle_field_reader(qs)
                ),
                A.ARM_DERIVATION: A.derivation_arm(
                    A.oracle_resolver(qs), A.oracle_field_reader(qs), A.oracle_derivation(qs)
                ),
            },
            runs=3,
        )
        v = A.p11_verdict(report)
        assert all(g.gain == pytest.approx(0.5) for g in v.per_ordering)  # oracle wins big
        assert v.admitted is False
        assert any("synthetic_fixture" in r for r in v.reasons)
        # the example set is also too small to support a paired estimate at all,
        # which is a second, independent reason it cannot decide a phase
        assert any("paired question(s)" in r for r in v.reasons)

    def test_p11_cannot_be_pointed_at_the_flattering_baseline(self):
        report = _ab_report({"q00"}, {"q00", "q01"})
        with pytest.raises(ValueError, match="arm2_node_first"):
            A.admission_verdict(
                report, phase="P11", candidate=A.ARM_DERIVATION, baseline=A.ARM_STATUS_QUO
            )
        with pytest.raises(ValueError, match="unknown phase"):
            A.admission_verdict(report, phase="P7")

    def test_refuses_when_an_arm_did_not_run(self):
        qs = _set([_question(f"q{i}") for i in range(4)])
        report = A.run_ab(
            qs,
            {
                A.ARM_NODE_FIRST: A.external_arm(A.ARM_NODE_FIRST, "no resolver supplied"),
                A.ARM_DERIVATION: _scripted_arm({"q0", "q1"}),
            },
            runs=3,
            orderings=("as_given", "reversed"),
        )
        v = A.p11_verdict(report)
        assert v.admitted is False
        assert any("did not run" in r for r in v.reasons)
        assert v.per_ordering == ()


class TestP2Verdict:
    def _report(self, node_first_correct, *, n=10, with_baseline=None):
        qs = _set([_question(f"q{i:02d}") for i in range(n)])
        arms = {
            A.ARM_STATUS_QUO: with_baseline or A.status_quo_arm(),
            A.ARM_NODE_FIRST: _scripted_arm(node_first_correct),
        }
        return A.run_ab(qs, arms, runs=3, orderings=("as_given", "reversed"))

    def test_inconclusive_when_the_external_baseline_did_not_run(self):
        v = A.p2_verdict(self._report({f"q{i:02d}" for i in range(9)}), target=0.8)
        assert v.expensive_phases_admitted is None
        assert any("cannot be settled here" in r for r in v.reasons)
        assert "INCONCLUSIVE" in v.render()

    def test_inconclusive_without_a_preregistered_target(self):
        report = self._report(
            {f"q{i:02d}" for i in range(9)}, with_baseline=_scripted_arm({"q00"})
        )
        v = A.p2_verdict(report)
        assert v.expensive_phases_admitted is None
        assert any("preregistered" in r for r in v.reasons)

    def test_a_cheap_path_that_clears_the_target_stops_the_plan(self):
        report = self._report(
            {f"q{i:02d}" for i in range(9)}, with_baseline=_scripted_arm({"q00"})
        )
        v = A.p2_verdict(report, target=0.8)
        assert v.node_first_clears_target is True
        assert v.expensive_phases_admitted is False
        assert v.comparison.admitted is True  # 0.90 vs 0.10 clears the floor
        assert any("not admitted" in r for r in v.reasons)

    def test_a_cheap_path_below_the_target_admits_the_expensive_phases(self):
        report = self._report(
            {f"q{i:02d}" for i in range(4)}, with_baseline=_scripted_arm({"q00"})
        )
        v = A.p2_verdict(report, target=0.8)
        assert v.node_first_clears_target is False
        assert v.expensive_phases_admitted is True

    def test_the_worst_ordering_decides_not_the_best(self):
        qs = _set([_question(f"q{i:02d}") for i in range(10)])
        report = A.run_ab(
            qs,
            {
                A.ARM_STATUS_QUO: _scripted_arm({"q00"}),
                A.ARM_NODE_FIRST: _curriculum_arm(
                    {f"q{i:02d}" for i in range(8)},
                    unlocked_by={"q08": "q00", "q09": "q00"},
                ),
            },
            runs=3,
            orderings=("as_given", "reversed"),
        )
        v = A.p2_verdict(report, target=0.95)
        # as_given reaches 1.0, reversed only 0.8; the target is judged on 0.8.
        assert v.node_first_worst_ordering.mean == pytest.approx(0.8)
        assert v.node_first_clears_target is False


# ────────────────────────────────────────────────────────────── end to end ────


class TestEndToEnd:
    def test_runs_on_the_example_set_with_stub_arms_and_produces_a_verdict(self):
        qs = M.load_question_set(EXAMPLE)
        report = A.run_ab(
            qs,
            {
                A.ARM_STATUS_QUO: A.status_quo_arm(),
                A.ARM_NODE_FIRST: A.node_first_arm(
                    A.oracle_resolver(qs), A.oracle_field_reader(qs)
                ),
                A.ARM_DERIVATION: A.derivation_arm(
                    A.oracle_resolver(qs), A.oracle_field_reader(qs), A.oracle_derivation(qs)
                ),
            },
            runs=3,
        )
        assert report.arms == (A.ARM_STATUS_QUO, A.ARM_NODE_FIRST, A.ARM_DERIVATION)
        assert len(report.orderings) == 3
        assert report.unavailable and A.ARM_STATUS_QUO in report.unavailable
        assert report.settings["n_should_abstain"] == 4
        # the report carries NO threshold: the bar is estimated at admission time
        assert "noise_floor" not in report.settings
        assert report.settings["uncertainty"] == "paired per question at admission time"

        node = report.aggregate(A.ARM_NODE_FIRST, "as_given")
        deriv = report.aggregate(A.ARM_DERIVATION, "as_given")
        # node-first reaches the two single-hop questions and abstains on the
        # two multi-hop ones; derivation reaches all four.
        assert node.summary("grounding_rate").mean == pytest.approx(0.5)
        assert deriv.summary("grounding_rate").mean == pytest.approx(1.0)
        assert node.summary("model_calls_per_query").mean == 0.0
        assert deriv.summary("model_calls_per_query").mean == pytest.approx(1.75)
        assert deriv.summary("connected_reasoning_rate").mean == pytest.approx(1.0)
        assert node.summary("abstained_on_answerable").mean == pytest.approx(0.5)
        assert deriv.summary("abstained_on_answerable").mean == 0.0

        p2 = A.p2_verdict(report, target=0.9)
        p11 = A.p11_verdict(report)
        assert isinstance(p2, A.P2Verdict) and isinstance(p11, A.AdmissionVerdict)
        assert p2.expensive_phases_admitted is None  # arm 1 absent + fixture set
        assert p11.admitted is False  # fixture set
        assert p2.render() and p11.render()

        # the verdicts and the report are JSON-serialisable for a run record
        json.dumps({"report": asdict(report), "p2": asdict(p2), "p11": asdict(p11)}, default=str)

    def test_the_report_table_carries_every_metric_the_phase_must_report(self):
        qs = M.load_question_set(EXAMPLE)
        report = A.run_ab(
            qs,
            {
                A.ARM_STATUS_QUO: A.status_quo_arm(),
                A.ARM_NODE_FIRST: A.node_first_arm(
                    A.oracle_resolver(qs), A.oracle_field_reader(qs)
                ),
            },
            runs=3,
            orderings=("as_given", "reversed"),
        )
        text = A.render_report(report)
        for _, label in A.REPORTED_METRICS:
            assert label in text
        assert {"grounding_rate", "connected_reasoning_rate", "model_calls_per_query"} <= {
            name for name, _ in A.REPORTED_METRICS
        }
        assert "NOT RUN" in text  # the absent arm is a line, not a row of zeros
        assert "0.000" not in text.split("NOT RUN")[1].splitlines()[0]

    def test_an_uncontrolled_connected_rate_is_flagged_in_the_table(self):
        qs = M.load_question_set(EXAMPLE)
        report = A.run_ab(
            qs,
            {
                A.ARM_DERIVATION: A.derivation_arm(
                    A.oracle_resolver(qs), A.oracle_field_reader(qs), A.oracle_derivation(qs)
                )
            },
            runs=1,
            orderings=("as_given",),
            ablate=False,
        )
        assert "not shortcut-controlled" in A.render_report(report)

    def test_cli_describes_the_set_without_producing_a_number(self, capsys):
        assert A.main([str(EXAMPLE)]) == 0
        out = capsys.readouterr().out
        assert "No measurement has been produced" in out
        assert "NOT RUN — external answer path" in out
        assert "fixture: cannot decide a phase" in out
        # describing a set must not emit anything that reads as a measurement
        assert "grounded" not in out and "±" not in out

    def test_cli_self_check_is_labelled_tautological(self, tmp_path, capsys):
        out_path = tmp_path / "self_check.json"
        argv = [str(EXAMPLE), "--self-check", "--target", "0.9", "--json", str(out_path)]
        assert A.main(argv) == 0
        out = capsys.readouterr().out
        assert "ORACLE doubles (tautological)" in out
        assert "REFUSED" in out and "INCONCLUSIVE" in out
        written = json.loads(out_path.read_text(encoding="utf-8"))
        assert written["self_check"] is True
        assert "No measurement has been produced" in written["disclaimer"]

    def test_cli_exits_2_on_a_malformed_question_set(self, tmp_path, capsys):
        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({"version": "1.0"}), encoding="utf-8")
        assert A.main([str(bad)]) == 2
        assert "error:" in capsys.readouterr().err


# ────────────────────────────────── clauses that need a later phase to test ────


@pytest.mark.skip(
    reason="blocked on the harness adapters, not on the phases: dks.resolve_entity "
    "(P1) and dks.query_protocol (P8) both exist now, but nothing adapts their "
    "resolver to this harness's `Resolver`, reads a resolved note's authored field "
    "off an indexed vault for `node_first_arm`, or drives `derivation_arm` through "
    "the registered dks_query capability — and no indexed-vault fixture exists to "
    "run them against"
)
def test_arms_run_against_the_real_query_path():
    raise AssertionError("placeholder for the wired arms")


@pytest.mark.skip(
    reason="blocked on the external baseline: arm 1 (the status-quo answer path) "
    "lives outside this repository, so P2's arm2-vs-arm1 comparison and its stop "
    "rule cannot be settled here"
)
def test_p2_decides_whether_the_expensive_phases_are_admitted():
    raise AssertionError("placeholder for the P2 decision")
