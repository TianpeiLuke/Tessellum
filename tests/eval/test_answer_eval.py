"""Reader-side answer eval: the scoring rules that each fixed a real defect,
the transport guard, and an end-to-end run through Tessellum's own retrieval
and ``MockBackend`` on a tiny fixture vault.

Every "bug case" below is a regression that once mis-scored a real run:

- hedged-but-correct answer scored as a refusal (substring refusal test);
- ``no`` found inside ``not`` (character-substring containment);
- ``Sam Bankman-Fried`` collapsed to one token (punctuation deletion);
- ``Insufficient balance …`` from the provider scored as deliberate abstention.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from tessellum.composer.llm import LLMResponse, MockBackend  # noqa: E402


def _load_harness():
    path = REPO / "eval" / "digestion_pipeline" / "answer_eval.py"
    spec = importlib.util.spec_from_file_location("answer_eval", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["answer_eval"] = module  # dataclasses resolve annotations via sys.modules
    spec.loader.exec_module(module)
    return module


ae = _load_harness()

SLICE = REPO / "eval" / "digestion_pipeline" / "claude_code_mcp"


# ─────────────────────────────────────────────────────────── scoring rules ────


class TestIsRefusal:
    def test_bare_token(self):
        assert ae.is_refusal("INSUFFICIENT")

    def test_token_with_trailing_explanation_is_still_refusal(self):
        assert ae.is_refusal("INSUFFICIENT — the context does not mention the port.")

    def test_answer_prefix_is_skipped(self):
        assert ae.is_refusal("Answer: INSUFFICIENT")

    def test_empty_is_refusal(self):
        assert ae.is_refusal("")
        assert ae.is_refusal("   \n")

    def test_hedged_but_correct_answer_is_NOT_a_refusal(self):
        # The substring test scored this as a refusal and reported 0.69
        # over-refusal on a run whose contains rate was 0.53.
        assert not ae.is_refusal("The context is insufficient, but the answer is Apple")

    def test_plain_answer(self):
        assert not ae.is_refusal("Apple")


class TestNormalise:
    def test_punctuation_becomes_space_not_nothing(self):
        assert ae.normalise("Sam Bankman-Fried") == "sam bankman fried"

    def test_hyphenated_gold_matches_spaced_answer(self):
        assert ae.tok_contains("Sam Bankman Fried", "Sam Bankman-Fried")
        assert ae.tok_contains("Sam Bankman-Fried", "Sam Bankman Fried")

    def test_articles_and_case_and_whitespace(self):
        assert ae.normalise("  The   Quick, brown FOX. ") == "quick brown fox"

    def test_underscored_identifier(self):
        assert ae.normalise("ENABLE_TOOL_SEARCH") == "enable tool search"


class TestTokContains:
    def test_no_is_not_inside_not(self):
        assert not ae.tok_contains("not", "no")
        assert not ae.tok_contains("It is not known", "no")
        assert not ae.tok_contains("north", "no")

    def test_exact_token(self):
        assert ae.tok_contains("No.", "no")
        assert ae.tok_contains("The answer is no", "no")

    def test_contiguous_subsequence(self):
        assert ae.tok_contains("Run `claude mcp add` in your shell", "claude mcp add")
        assert not ae.tok_contains("claude add mcp", "claude mcp add")

    def test_empty_gold_never_matches(self):
        assert not ae.tok_contains("anything", "")


class TestGoldClass:
    @pytest.mark.parametrize("gold", ["yes", "No", "TRUE", "false.", " Yes "])
    def test_polarity(self, gold):
        assert ae.gold_class(gold) == "polarity"

    @pytest.mark.parametrize("gold", ["claude mcp add", "2022", "Cupertino", "Nobody"])
    def test_entity(self, gold):
        assert ae.gold_class(gold) == "entity"


class TestCorrect:
    def test_polarity_with_justification_counts(self):
        assert ae.correct("Yes, because HTTP supports OAuth.", "yes") == 1.0
        assert ae.correct("No — stdio servers are local processes.", "false") == 1.0

    def test_polarity_wrong_verdict(self):
        assert ae.correct("No.", "yes") == 0.0

    def test_polarity_without_a_verdict_is_wrong(self):
        # "not" does not read as "no", and a non-committal lead scores zero.
        assert ae.correct("It is not stated", "no") == 0.0

    def test_entity_contains(self):
        assert ae.correct("The context is insufficient, but the answer is Apple", "Apple") == 1.0
        assert ae.correct("INSUFFICIENT", "Apple") == 0.0


# ───────────────────────────────────────────────────────── transport guard ────


class TestTransportGuard:
    def test_insufficient_balance_is_transport_not_refusal(self):
        text = "Insufficient balance. Your Cline Credits balance is $-0.04"
        assert ae.transport_reason(text) == "quota"

    def test_abstention_token_is_not_transport(self):
        assert ae.transport_reason("INSUFFICIENT") is None
        assert ae.transport_reason("INSUFFICIENT — the context does not say.") is None

    def test_hedged_answer_is_not_transport(self):
        assert ae.transport_reason("The context is insufficient, but the answer is Apple") is None

    def test_quota_envelope(self):
        env = '{"error":{"code":"INFERENCE_CAP_ERROR","message":"Error 429: Daily free limit reached"}}'
        assert ae.transport_reason(env) == "rate_limit"

    def test_timeout_relayed_as_text(self):
        assert ae.transport_reason("Request timed out") == "stall"

    def test_empty_body_is_a_dropped_call(self):
        assert ae.transport_reason("") == "empty"
        assert ae.transport_reason(None) == "empty"

    def test_legitimate_answer_spans_pass(self):
        for ans in ("MCP_TIMEOUT", "claude mcp add", "30 seconds", "Cupertino", "no"):
            assert ae.transport_reason(ans) is None, ans

    def test_long_body_mentioning_billing_is_content(self):
        body = ("The billing page explains the quota model in detail. " * 20).strip()
        assert len(body) > 600
        assert ae.transport_reason(body) is None

    def test_scored_record_excludes_transport_from_metrics(self):
        q = ae.Question(qid="q", question="Which var?", gold="MCP_TIMEOUT")
        resp = LLMResponse(
            content="Insufficient balance. Your Cline Credits balance is $-0.04",
            elapsed_ms=1.0, backend_id="x",
        )
        rec = ae.score_response(q, resp, ae.RetrievedContext("MCP_TIMEOUT raises it", ["n.md"], 5))
        assert rec.transport == "quota"
        assert rec.refused is False and rec.correct == 0.0
        summary = ae.summarise([rec])
        assert summary["n_scored"] == 0 and summary["n_transport"] == 1
        assert summary["transport_reasons"] == {"quota": 1}

    def test_raised_backend_error_is_transport(self):
        class Boom:
            backend_id = "boom"

            def call(self, request):
                raise RuntimeError("connection reset by peer")

        q = ae.Question(qid="q", question="Who?", gold="x")
        rec = ae.answer_one(Boom(), q, ae.RetrievedContext("", [], 0))
        assert rec.transport.startswith("raised: RuntimeError")


# ───────────────────────────────────────────────── budget + baselines + CI ────


class TestBudgetAndPool:
    def test_candidate_pool_scales_with_budget(self):
        assert ae.candidate_pool("tokens", k=10, budget=512) == 40
        assert ae.candidate_pool("tokens", k=10, budget=2048) == 85
        assert ae.candidate_pool("tokens", k=10, budget=8192) == 341
        assert ae.candidate_pool("slots", k=10, budget=8192) == 10

    def test_build_context_skips_overrunning_note_and_keeps_filling(self):
        arm = ae.VaultArm.__new__(ae.VaultArm)
        arm.strategy = "hybrid"
        arm.bodies = {"a": "A", "b": "B", "c": "C", "d": "D"}
        arm.tokens = {"a": 1000, "b": 1500, "c": 500, "d": 400}
        arm.rank = lambda question, want: ["a", "b", "c", "d"]
        ctx = arm.build_context("q", condition="tokens", budget=2048)
        assert ctx.note_ids == ["a", "c", "d"]
        assert ctx.tokens == 1900
        assert ctx.context == "A\n\n---\n\nC\n\n---\n\nD"

    def test_slots_condition_takes_top_k(self):
        arm = ae.VaultArm.__new__(ae.VaultArm)
        arm.strategy = "hybrid"
        arm.bodies = {"a": "A", "b": "B", "c": "C"}
        arm.tokens = {"a": 9000, "b": 9000, "c": 9000}
        arm.rank = lambda question, want: ["a", "b", "c"]
        ctx = arm.build_context("q", condition="slots", k=2, budget=10)
        assert ctx.note_ids == ["a", "b"]


class TestBaselinesAndBootstrap:
    def test_majority_is_per_stratum(self):
        qs = [
            ae.Question("1", "?", "Paris"), ae.Question("2", "?", "Paris"),
            ae.Question("3", "?", "Rome"),
            ae.Question("4", "?", "yes"), ae.Question("5", "?", "no"), ae.Question("6", "?", "no"),
            ae.Question("7", "?", null=True),
        ]
        recs, modes = ae.majority_baseline(qs)
        assert modes == {"entity": "paris", "polarity": "no"}
        s = ae.summarise(recs)
        # a single constant answer would have scored zero on one stratum
        assert s["entity"] == pytest.approx(2 / 3)
        assert s["polarity"] == pytest.approx(2 / 3)
        assert s["abstain_null"] == 0.0

    def test_paired_bootstrap_degenerate_and_mixed(self):
        assert ae.paired_bootstrap([1.0] * 8) == (1.0, 1.0)
        assert ae.paired_bootstrap([0.0] * 8) == (0.0, 0.0)
        assert ae.paired_bootstrap([]) == (0.0, 0.0)
        lo, hi = ae.paired_bootstrap([1, 0, 1, 0, 1, 1, 0, 0, 1, 1])
        assert lo < 0.6 < hi
        # deterministic under the fixed seed
        assert ae.paired_bootstrap([1, 0, 1, 0, 1, 1, 0, 0, 1, 1]) == (lo, hi)

    def test_compare_uses_shared_answerable_non_transport_questions(self):
        def rec(qid, cls, correct, transport=None, null=False):
            return ae.AnswerRecord(
                qid=qid, question="?", gold="g", null=null, cls=cls, answer="a",
                refused=False, correct=correct, transport=transport, stop_reason=None,
            )

        base = [rec("1", "entity", 0.0), rec("2", "entity", 0.0), rec("3", "polarity", 1.0),
                rec("4", "entity", 0.0, transport="quota"), rec("5", "null", 0.0, null=True)]
        other = [rec("1", "entity", 1.0), rec("2", "entity", 1.0), rec("3", "polarity", 0.0),
                 rec("4", "entity", 1.0), rec("5", "null", 0.0, null=True)]
        c = ae.compare(base, other)
        assert c["entity"]["n"] == 2 and c["entity"]["delta"] == 1.0 and c["entity"]["significant"]
        assert c["polarity"]["n"] == 1 and c["polarity"]["delta"] == -1.0
        assert c["both"]["n"] == 3


class TestQuestionsFormat:
    def test_load_object_and_bare_list(self, tmp_path):
        rows = [{"qid": "a", "question": "Q?", "gold": "x", "evidence_notes": ["n.md"]},
                {"question": "Null?", "null": True}]
        p1 = tmp_path / "obj.json"
        p1.write_text(json.dumps({"questions": rows}))
        p2 = tmp_path / "list.json"
        p2.write_text(json.dumps(rows))
        for p in (p1, p2):
            qs = ae.load_questions(p)
            assert [q.qid for q in qs] == ["a", "q002"]
            assert qs[0].evidence_notes == ("n.md",) and qs[0].cls == "entity"
            assert qs[1].null and qs[1].gold == "" and qs[1].cls == "null"

    def test_rejects_missing_gold_and_duplicate_qid(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text(json.dumps([{"qid": "a", "question": "Q?"}]))
        with pytest.raises(ValueError):
            ae.load_questions(p)
        p.write_text(json.dumps([{"qid": "a", "question": "Q?", "gold": "x"},
                                 {"qid": "a", "question": "R?", "gold": "y"}]))
        with pytest.raises(ValueError):
            ae.load_questions(p)

    def test_parse_arm_spec(self):
        assert ae._parse_arm_spec("notes=/v/notes:bm25") == ("notes", Path("/v/notes"), "bm25")
        assert ae._parse_arm_spec("notes=/v/notes") == ("notes", Path("/v/notes"), "hybrid")
        assert ae._parse_arm_spec("db=/v/index.db:router") == ("db", Path("/v/index.db"), "router")


# ───────────────────────────────────────────────────────────── end to end ────

_NOTE = """\
---
tags:
  - resource
  - terminology
keywords:
  - {kw}
topics:
  - fixture
language: markdown
date of note: 2026-09-01
status: active
building_block: concept
---

# {title}

## Overview

{body}

## Related Notes

- [Scaffolding link](term_noise.md) — SCAFFOLDING_MARKER must not reach the reader.
"""


@pytest.fixture
def fixture_arm(tmp_path):
    v = tmp_path / "v" / "resources" / "term_dictionary"
    v.mkdir(parents=True)
    notes = {
        "term_ftx": ("FTX", "ftx", "FTX was founded by Sam Bankman-Fried. The exchange collapsed in November 2022."),
        "term_apple": ("Apple", "apple", "Apple Inc. was founded by Steve Jobs and Steve Wozniak. Its headquarters are in Cupertino."),
        "term_mcp_timeout": ("MCP timeout", "timeout", "The MCP_TIMEOUT environment variable raises the server startup timeout, whose default is 30 seconds."),
        "term_stdio": ("Stdio servers", "stdio", "Stdio servers are local processes and are not reconnected automatically. HTTP servers reconnect with exponential backoff."),
        "term_noise": ("Gardening", "gardening", "Tomatoes prefer full sun and well-drained soil; water deeply but infrequently."),
    }
    for name, (title, kw, body) in notes.items():
        (v / f"{name}.md").write_text(_NOTE.format(title=title, kw=kw, body=body))
    db = tmp_path / "v.db"
    return ae.VaultArm.from_vault(
        "notes", tmp_path / "v", db, with_dense=False, count=lambda s: len(s.split())
    )


FIXTURE_QUESTIONS = [
    ae.Question("e1", "Who founded FTX?", "Sam Bankman-Fried", evidence_notes=("resources/term_dictionary/term_ftx.md",)),
    ae.Question("e2", "Where is Apple headquartered?", "Cupertino", evidence_notes=("resources/term_dictionary/term_apple.md",)),
    ae.Question("e3", "Which environment variable raises the MCP startup timeout?", "MCP_TIMEOUT", evidence_notes=("resources/term_dictionary/term_mcp_timeout.md",)),
    ae.Question("e4", "In what year did FTX collapse?", "2022", evidence_notes=("resources/term_dictionary/term_ftx.md",)),
    ae.Question("p1", "Are stdio servers reconnected automatically?", "no", evidence_notes=("resources/term_dictionary/term_stdio.md",)),
    ae.Question("p2", "Do HTTP servers reconnect with exponential backoff?", "yes", evidence_notes=("resources/term_dictionary/term_stdio.md",)),
    ae.Question("n1", "Who is the CEO of Apple?", null=True),
    ae.Question("n2", "What is Apple's stock ticker?", null=True),
]

FIXTURE_REPLIES = {
    "Question: Who founded FTX?": "Sam Bankman Fried",                                   # hyphenated gold, spaced answer
    "Question: Where is Apple headquartered?": "The context is insufficient, but the answer is Cupertino",  # hedged-but-correct
    "Question: Which environment variable raises": "Insufficient balance. Your Cline Credits balance is $-0.04",  # provider stopped
    "Question: In what year did FTX collapse?": "INSUFFICIENT — the context does not say.",  # refusal with answer present
    "Question: Are stdio servers reconnected": "No, stdio servers are local processes.",   # verdict + justification
    "Question: Do HTTP servers reconnect": "Not stated in the context.",                   # 'not' is not 'no'; no verdict
    "Question: What is Apple's stock ticker?": "AAPL",                                     # hallucinated on a null
}


def test_end_to_end_mock_backend(fixture_arm):
    assert fixture_arm.dense_available is False
    assert fixture_arm.describe().startswith("hybrid (bm25-only")
    # evidence-only bodies: the Related Notes block never reaches the reader
    assert all("SCAFFOLDING_MARKER" not in b for b in fixture_arm.bodies.values())

    backend = MockBackend(FIXTURE_REPLIES, default=ae.REFUSAL_TOKEN)
    report = ae.run(FIXTURE_QUESTIONS, {"notes": fixture_arm}, backend, budget=2048)

    assert set(report["arms"]) == {"notes", "_majority", "_closed_book"}
    a = report["arms"]["notes"]
    assert a["n"] == 8 and a["n_scored"] == 7
    assert a["n_transport"] == 1 and a["transport_reasons"] == {"quota": 1}
    assert a["n_entity"] == 3 and a["entity"] == pytest.approx(2 / 3)
    assert a["n_polarity"] == 2 and a["polarity"] == pytest.approx(0.5)
    assert a["macro"] == pytest.approx((2 / 3 + 0.5) / 2)
    assert a["refused"] == pytest.approx(1 / 5)
    assert a["n_null"] == 2 and a["abstain_null"] == pytest.approx(0.5)
    assert a["evidence_recall"] == 1.0
    assert a["truncated"] == 0

    d = a["refusal_diagnosis"]
    assert d["n_present"] == 3 and d["wasted_refusals"] == 1
    assert d["p_refuse_answer_present"] == pytest.approx(1 / 3)
    assert d["n_absent"] == 0

    per_q = {r["qid"]: r for r in a["per_question"]}
    assert per_q["e1"]["correct"] == 1.0 and per_q["e1"]["refused"] is False
    assert per_q["e2"]["correct"] == 1.0 and per_q["e2"]["refused"] is False
    assert per_q["e3"]["transport"] == "quota" and per_q["e3"]["correct"] == 0.0
    assert per_q["e4"]["refused"] is True and per_q["e4"]["answer_in_context"] is True
    assert per_q["p1"]["correct"] == 1.0 and per_q["p1"]["answer_in_context"] is None
    assert per_q["p2"]["correct"] == 0.0
    assert per_q["n1"]["refused"] is True and per_q["n2"]["refused"] is False
    assert per_q["e1"]["stop_reason"] is None  # mock carries none; recorded, not invented
    assert "resources/term_dictionary/term_ftx.md" in per_q["e1"]["note_ids"]

    # baselines
    assert report["settings"]["majority_answers"] == {"entity": "sam bankman fried", "polarity": "no"}
    m = report["arms"]["_majority"]
    assert m["n_transport"] == 0 and m["entity"] == pytest.approx(1 / 4)
    cb = report["arms"]["_closed_book"]
    assert cb["refusal_diagnosis"]["n_present"] == 0
    assert cb["mean_context_tokens"] == 0.0
    assert {"_majority:notes", "_closed_book:notes"} <= set(report["comparisons"])
    assert report["comparisons"]["_majority:notes"]["entity"]["n"] == 3

    # the reader contract: fixed prompt, abstention token offered, temperature 0
    assert backend.calls, "no reader calls recorded"
    for req in backend.calls:
        assert req.temperature == 0.0
        assert req.max_tokens == 128
        assert ae.REFUSAL_TOKEN in req.system_prompt
        assert req.system_prompt == ae.SYSTEM_PROMPT
    e1_calls = [r for r in backend.calls if "Question: Who founded FTX?" in r.user_prompt]
    assert len(e1_calls) == 2  # vault arm + closed book
    assert any("Sam Bankman-Fried" in r.user_prompt for r in e1_calls)
    assert any("Context:\n\n\nQuestion" in r.user_prompt for r in e1_calls)

    # the report round-trips through JSON and the console formatter
    json.dumps(report)
    text = ae.format_report(report)
    assert "P(ref|present)" in text and "_closed_book" in text


def test_transport_fraction_flags_degraded_arm(fixture_arm):
    backend = MockBackend(default="Insufficient balance. Your Cline Credits balance is $-0.04")
    report = ae.run(FIXTURE_QUESTIONS, {"notes": fixture_arm}, backend, closed_book=False)
    a = report["arms"]["notes"]
    assert a["n_transport"] == 8 and a["transport_fraction"] == 1.0
    assert a["n_scored"] == 0
    assert "NOT comparable" in ae.format_report(report)


# ─────────────────────────────────────────────────── the curated dev slice ────


@pytest.mark.skipif(not (SLICE / "questions.json").exists(), reason="slice questions missing")
def test_claude_code_mcp_questions_are_answerable_from_their_evidence(tmp_path):
    qs = ae.load_questions(SLICE / "questions.json")
    arm = ae.VaultArm.from_vault("golden", SLICE / "golden_notes", tmp_path / "g.db", with_dense=False)
    assert len(arm.bodies) == 8
    strata = {q.cls for q in qs}
    assert strata == {"entity", "polarity", "null"}
    for q in qs:
        if q.null:
            continue
        assert q.evidence_notes, q.qid
        for n in q.evidence_notes:
            assert n in arm.bodies, (q.qid, n)
        if q.cls == "entity":
            assert any(ae.tok_contains(arm.bodies[n], q.gold) for n in q.evidence_notes), q.qid
        # a gold must never look like a provider error to the transport guard
        assert ae.transport_reason(q.gold) is None, q.qid

    # retrieval through Tessellum finds the cited notes at a generous budget
    hits = [any(n in arm.build_context(q.question, budget=8192).note_ids for n in q.evidence_notes)
            for q in qs if not q.null]
    assert sum(hits) / len(hits) >= 0.9


@pytest.mark.skipif(not (SLICE / "questions.json").exists(), reason="slice questions missing")
def test_cli_dry_run_on_slice(tmp_path, capsys):
    out = tmp_path / "report.json"
    rc = ae.main([
        str(SLICE), "--arms", f"golden={SLICE / 'golden_notes'}:bm25",
        "--db-dir", str(tmp_path), "--no-dense", "--backend", "mock",
        "--budget", "2048", "--json", str(out),
    ])
    assert rc == 0
    report = json.loads(out.read_text())
    assert report["slice"] == "claude_code_mcp"
    assert set(report["arms"]) == {"golden", "_majority", "_closed_book"}
    g = report["arms"]["golden"]
    assert g["retrieval"] == "bm25"
    assert g["refused"] == 1.0 and g["abstain_null"] == 1.0  # mock refuses everything
    assert g["n_transport"] == 0
    assert (tmp_path / "golden.db").exists()
    assert "majority baseline answers" in capsys.readouterr().out


def test_cli_missing_questions_exits_2(tmp_path, capsys):
    assert ae.main([str(tmp_path)]) == 2
    assert "not found" in capsys.readouterr().err
