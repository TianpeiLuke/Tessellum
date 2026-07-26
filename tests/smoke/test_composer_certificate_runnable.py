"""Semantic certificate — runnable pieces (C1-C4).

Makes the calibrated certificate (semantic_certificate.py, P7/DKS P4) runnable
end-to-end with a deterministic reference scorer, so the certify→verdict→gate
loop and the A7.5 go/no-go gate can be exercised NOW — the real NLI model + a
human-labelled corpus remain the injected/external research prerequisite.

Covers:
  - C1 make_lexical_scorer / claim_support_score: directional token containment,
    fail-closed abstain on missing span.
  - C2 extract_claims / split_sentences: prose-only, provenance-gated, union-of-
    sources ref.
  - C3 make_certificate_verifier: end-to-end (well-supported note → grounded;
    fabricated note → ungrounded) through the grounding_verifier seam signature.
  - C4 run_calibration_gate: GO on a separable corpus, fail-closed NO-GO when a
    wrong-but-high-score example leaks or the held-out split is too small.
"""

from __future__ import annotations

from tessellum.composer import (
    CalibrationCorpus,
    ClaimProvenance,
    CorpusExample,
    calibrate,
    claim_support_score,
    extract_claims,
    make_certificate_verifier,
    make_lexical_scorer,
    run_calibration_gate,
    split_sentences,
)


# ── C1: lexical scorer ───────────────────────────────────────────────────────


def test_claim_support_full_when_span_contains_claim_words() -> None:
    # every content word of the claim is in the span → 1.0.
    span = "The RnR BSM BERT model scores the reversal domain at 1% FPR."
    assert claim_support_score("The BSM BERT model scores reversal", span) == 1.0


def test_claim_support_partial_and_zero() -> None:
    span = "Lambda functions run in an execution environment."
    s = claim_support_score("Lambda functions support provisioned concurrency", span)
    assert 0.0 < s < 1.0  # "functions"+"lambda" present, "provisioned/concurrency" not
    assert claim_support_score("Kinesis streams shard aggregation", span) == 0.0


def test_claim_support_empty_claim_is_zero() -> None:
    assert claim_support_score("the of and", "anything here") == 0.0  # all stopwords


def test_lexical_scorer_abstains_on_missing_span() -> None:
    scorer = make_lexical_scorer(span_text_of=lambda ref: None)
    from tessellum.composer import Claim

    [score] = scorer([Claim("c1", "some claim", "ref://missing")])
    assert score.abstained and score.score == 0.0


def test_lexical_scorer_scores_present_span() -> None:
    spans = {"s://1": "alpha beta gamma delta content words here"}
    scorer = make_lexical_scorer(span_text_of=lambda ref: spans.get(ref))
    from tessellum.composer import Claim

    [score] = scorer([Claim("c1", "alpha beta gamma", "s://1")])
    assert not score.abstained and score.score == 1.0


# ── C2: claim extraction ─────────────────────────────────────────────────────


def _prov(*refs: str) -> tuple[ClaimProvenance, ...]:
    return tuple(ClaimProvenance(span_id=f"sp{i}", source_ref=r) for i, r in enumerate(refs))


def test_split_sentences_drops_non_prose() -> None:
    body = (
        "---\ntitle: x\n---\n\n"
        "## Heading\n\n"
        "The model computes recall at a fixed false positive rate.\n"
        "```python\ncode = 1\n```\n"
        "| a | b |\n"
        "- [link](http://x)\n"
        "It also aggregates good and abusive orders per marketplace.\n"
    )
    sents = split_sentences(body)
    assert any("recall" in s for s in sents)
    assert any("marketplace" in s for s in sents)
    assert not any("code" in s or "Heading" in s or "title" in s for s in sents)


def test_split_sentences_drops_tilde_and_indented_code() -> None:
    # Review: ~~~ fences and 4-space/tab indented code must NOT leak as claims.
    body = (
        "The model computes recall at a fixed rate here.\n"
        "~~~python\nleaked = should_not_appear\n~~~\n"
        "    indented_code_line = also_hidden\n"
        "It aggregates good and abusive orders per marketplace.\n"
    )
    sents = split_sentences(body)
    assert not any("should_not_appear" in s or "also_hidden" in s for s in sents)
    assert any("recall" in s for s in sents)
    assert any("marketplace" in s for s in sents)


def test_split_sentences_merges_subfloor_fragment_not_drop() -> None:
    # Review: an abbreviation/decimal split fragment below the floor is MERGED
    # back (fail-closed), not silently dropped.
    sents = split_sentences("The onboarding task takes about 1.5w to complete fully.")
    # "1.5w to complete fully" must remain scored somewhere, not vanish.
    joined = " ".join(sents)
    assert "complete" in joined and "onboarding" in joined


def test_extract_claims_no_provenance_is_empty() -> None:
    assert extract_claims("A real sentence with content.", ()) == []


def test_extract_claims_unions_sources() -> None:
    from tessellum.composer import MULTI_SOURCE_SEP

    claims = extract_claims(
        "The model scores the reversal domain accurately.",
        _prov("src://b", "src://a", "src://a"),  # dup + unsorted
        note_id="n1",
    )
    assert len(claims) == 1
    # union of DISTINCT sources, sorted, joined by the separator.
    assert claims[0].source_ref == f"src://a{MULTI_SOURCE_SEP}src://b"
    assert claims[0].claim_id == "n1:c0"


# ── C3: end-to-end verifier through the seam ─────────────────────────────────


class _Result:
    def __init__(self, structured: dict) -> None:
        self.materialized = type("M", (), {"structured": structured})()


def _thresholds(alpha: float = 0.1):
    # calibrate so grounding accepts at a high bar (>=0.75 support), in domain
    # "demo" — certify() fail-closes outside the calibrated domain set.
    from tessellum.composer import LabeledExample

    examples = [
        LabeledExample("grounding", 0.9, True), LabeledExample("grounding", 0.8, True),
        LabeledExample("grounding", 0.5, False), LabeledExample("grounding", 0.3, False),
    ]
    return calibrate(examples, alpha=alpha, domains=("demo",))


def _demo_domain(step, leaf, result):
    return "demo"


def test_verifier_grounds_well_supported_note() -> None:
    span = ("The RnR BSM BERT model scores the reversal domain and aggregates "
            "good and abusive orders per marketplace at fixed false positive rates.")
    verifier = make_certificate_verifier(
        scorer=make_lexical_scorer(span_text_of=lambda ref: span),
        thresholds=_thresholds(), note_domain_of=_demo_domain,
    )
    leaf = {"_id": "n1"}
    result = _Result({
        "body_markdown": "The BSM BERT model scores the reversal domain.",
        "provenance": [{"span_id": "s1", "source_ref": "src://1"}],
    })
    verdict = verifier(None, leaf, result)
    assert verdict.status == "grounded"


def test_verifier_abstains_outside_calibrated_domain() -> None:
    # a well-supported note in an UNCALIBRATED domain must abstain (fail-closed
    # domain gate — empty/mismatched domain never auto-accepts).
    span = "The model scores the reversal domain accurately here."
    verifier = make_certificate_verifier(
        scorer=make_lexical_scorer(span_text_of=lambda ref: span),
        thresholds=_thresholds(), note_domain_of=lambda *a: "other_domain",
    )
    result = _Result({
        "body_markdown": "The model scores the reversal domain.",
        "provenance": [{"span_id": "s1", "source_ref": "src://1"}],
    })
    assert verifier(None, {"_id": "n1b"}, result).status == "ungrounded"


def test_verifier_abstains_when_no_domain_supplied() -> None:
    # default note_domain_of=None → note_domain None → outside any calibrated
    # domain → fail-closed abstain (wiring the verifier does NOT auto-promote).
    span = "The model scores the reversal domain accurately here."
    verifier = make_certificate_verifier(
        scorer=make_lexical_scorer(span_text_of=lambda ref: span),
        thresholds=_thresholds(),  # no note_domain_of
    )
    result = _Result({
        "body_markdown": "The model scores the reversal domain.",
        "provenance": [{"span_id": "s1", "source_ref": "src://1"}],
    })
    assert verifier(None, {"_id": "n1c"}, result).status == "ungrounded"


def test_verifier_flags_fabricated_note() -> None:
    span = "The document describes an unrelated caching subsystem."
    verifier = make_certificate_verifier(
        scorer=make_lexical_scorer(span_text_of=lambda ref: span),
        thresholds=_thresholds(), note_domain_of=_demo_domain,
    )
    leaf = {"_id": "n2"}
    result = _Result({
        "body_markdown": "The model achieves ninety nine percent precision on fraud.",
        "provenance": [{"span_id": "s1", "source_ref": "src://1"}],
    })
    verdict = verifier(None, leaf, result)
    assert verdict.status == "ungrounded"  # claim words absent from span → abstain


def test_verifier_skips_malformed_provenance_row_without_crashing() -> None:
    # Review (high): a truthy-but-non-string provenance field (span_id=1) must be
    # SKIPPED, not passed to ClaimProvenance's str validator (which would raise
    # and crash the whole step). Here the only row is malformed → no valid
    # provenance → no claims → fail-closed abstain (ungrounded), not an exception.
    verifier = make_certificate_verifier(
        scorer=make_lexical_scorer(span_text_of=lambda ref: "some span text"),
        thresholds=_thresholds(),
    )
    result = _Result({
        "body_markdown": "A sentence with content words here.",
        "provenance": [{"span_id": 1, "source_ref": "src://1"}],  # span_id not a str
    })
    verdict = verifier(None, {"_id": "n4"}, result)  # must NOT raise
    assert verdict.status == "ungrounded"


def test_verifier_abstains_on_unsourced_note() -> None:
    verifier = make_certificate_verifier(
        scorer=make_lexical_scorer(span_text_of=lambda ref: "x"),
        thresholds=_thresholds(),
    )
    result = _Result({"body_markdown": "A confident but unsourced claim here.",
                      "provenance": []})
    verdict = verifier(None, {"_id": "n3"}, result)
    assert verdict.status == "ungrounded"  # no provenance → no claims → fail-closed


# ── C4: A7.5 go/no-go gate ───────────────────────────────────────────────────


def _separable_corpus(n: int = 24) -> CalibrationCorpus:
    # cleanly separable: correct claims score high, incorrect score low.
    exs = []
    for i in range(n):
        correct = i % 2 == 0
        exs.append(CorpusExample(
            example_id=f"e{i}", failure_class="grounding",
            score=0.95 if correct else 0.2, correct=correct, domain="demo",
        ))
    return CalibrationCorpus(examples=tuple(exs), domains=("demo",))


def test_calibration_gate_go_on_separable_corpus() -> None:
    res = run_calibration_gate(_separable_corpus(), alpha=0.1)
    assert res.unattended_ok
    assert res.reasons == ()
    assert res.n_held_out >= 8
    assert res.held_out_far["grounding"] <= 0.1


def test_calibration_gate_nogo_when_wrong_but_high_score_leaks() -> None:
    # inject wrong-but-well-formed examples that score HIGH → FAR breaches α.
    exs = list(_separable_corpus().examples)
    for i in range(10):
        exs.append(CorpusExample(
            example_id=f"leak{i}", failure_class="grounding",
            score=0.97, correct=False, domain="demo",  # high score, WRONG
        ))
    corpus = CalibrationCorpus(examples=tuple(exs), domains=("demo",))
    res = run_calibration_gate(corpus, alpha=0.1)
    assert not res.unattended_ok
    # wrong-but-high leaks force a fail-closed NO-GO — either a FAR breach or an
    # unreachable-threshold always-abstain; never a silent promote.
    assert any("grounding" in r for r in res.reasons)


def test_calibration_gate_nogo_on_indistinguishable_scores() -> None:
    # correct and incorrect claims INDISTINGUISHABLE by score (both high) → no
    # threshold can meet α → always-abstain / FAR breach → fail-closed NO-GO.
    exs = [
        CorpusExample(example_id=f"e{i}", failure_class="grounding",
                      score=0.9, correct=(i < 12), domain="demo")
        for i in range(24)
    ]
    res = run_calibration_gate(CalibrationCorpus(tuple(exs), ("demo",)), alpha=0.1)
    assert not res.unattended_ok
    assert any("grounding" in r for r in res.reasons)


def test_calibration_gate_nogo_when_held_out_too_small() -> None:
    tiny = CalibrationCorpus(examples=tuple(
        CorpusExample(f"e{i}", "grounding", 0.9, True, "demo") for i in range(6)
    ), domains=("demo",))
    res = run_calibration_gate(tiny, alpha=0.1)
    assert not res.unattended_ok
    assert any("too small" in r for r in res.reasons)


def test_calibration_gate_nogo_when_class_present_only_in_train() -> None:
    # Review (critical): a class with too few / one-sided held-out examples must
    # be a fail-closed NO-GO — its FAR/recall are unmeasurable, so it cannot be
    # certified unattended even though grounding is separable.
    exs = [CorpusExample(f"g{i}", "grounding", 0.95 if i % 2 == 0 else 0.2,
                         (i % 2 == 0), "demo") for i in range(24)]
    exs.append(CorpusExample("cov1", "coverage", 0.9, True, "demo"))  # lone coverage
    res = run_calibration_gate(CalibrationCorpus(tuple(exs), ("demo",)), alpha=0.1)
    assert not res.unattended_ok
    assert any("coverage" in r and "held-out evidence" in r for r in res.reasons)


def test_calibration_gate_nogo_when_class_held_out_one_sided() -> None:
    # a class with held-out examples but only CORRECT ones (no incorrect) → FAR
    # unmeasurable → NO-GO (can't prove it won't false-accept).
    exs = [CorpusExample(f"g{i}", "grounding", 0.95 if i % 2 == 0 else 0.2,
                         (i % 2 == 0), "demo") for i in range(24)]
    # coverage: 8 examples, ALL correct → held-out has 0 incorrect.
    exs += [CorpusExample(f"cov{i}", "coverage", 0.9, True, "demo") for i in range(8)]
    res = run_calibration_gate(CalibrationCorpus(tuple(exs), ("demo",)), alpha=0.1)
    assert not res.unattended_ok
    assert any("coverage" in r and "incorrect" in r for r in res.reasons)


def test_calibration_gate_is_deterministic() -> None:
    c = _separable_corpus()
    a = run_calibration_gate(c, alpha=0.1)
    b = run_calibration_gate(c, alpha=0.1)
    assert a.unattended_ok == b.unattended_ok
    assert a.held_out_far == b.held_out_far
