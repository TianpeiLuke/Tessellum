"""DKS refactor P7 — self-driving elevation (decision b4a + the contract).

Gate deliverables:
 - the DeepUnderstandingCertificate is validator-issued (never the reasoning
   backend) and revocable;
 - a hand-designed V(q) ranks questions (audited before any learning);
 - the reward is computed on a FROZEN snapshot, zero before independent
   validation, and un-inflatable by self-citation;
 - the ranker ORDERS moves only — never commits, never certifies.
"""

from __future__ import annotations

from tessellum.dks import (
    CertificateError,
    MaturityProfile,
    MoveRanker,
    QuestionValue,
    RankerAuthorityError,
    RewardInputs,
    issue_certificate,
    move_reward,
    rank_questions,
    revoke,
)


def _validated_profile() -> MaturityProfile:
    return MaturityProfile(levels={
        "independent_validation": "VALIDATED",
        "warrant": "VALIDATED",
        "provenance": "VALIDATED",
    })


# ── A7.1 maturity profile + validator-issued certificate ────────────────────


def test_certificate_issued_by_independent_validator() -> None:
    cert = issue_certificate(
        "inq1", _validated_profile(),
        issuer="validator-x", reasoning_backend_id="claude",
    )
    assert cert.issuer == "validator-x"
    assert not cert.revoked


def test_reasoning_backend_cannot_certify_itself() -> None:
    # the mover is never the judge (P3).
    try:
        issue_certificate("inq1", _validated_profile(),
                          issuer="claude", reasoning_backend_id="claude")
        raise AssertionError("self-certification should raise")
    except CertificateError:
        pass


def test_self_certify_guard_normalizes_ids() -> None:
    # Review nit (low): an issuer differing only by whitespace/case cannot
    # self-certify (the ids are normalized before comparison).
    for near in ("claude", " claude", "CLAUDE", "Claude ", "  claude\t"):
        try:
            issue_certificate("inq1", _validated_profile(),
                              issuer=near, reasoning_backend_id="claude")
            raise AssertionError(f"issuer {near!r} should be treated as the backend")
        except CertificateError:
            pass


def test_certificate_requires_mature_profile() -> None:
    immature = MaturityProfile(levels={"warrant": "CLAIMED"})
    try:
        issue_certificate("inq1", immature,
                          issuer="validator-x", reasoning_backend_id="claude")
        raise AssertionError("immature profile should raise")
    except CertificateError:
        pass


def test_certificate_is_revocable() -> None:
    cert = issue_certificate("inq1", _validated_profile(),
                             issuer="v", reasoning_backend_id="claude")
    assert revoke(cert).revoked is True


def test_maturity_profile_defaults_absent() -> None:
    p = MaturityProfile()
    assert p.level("warrant") == "ABSENT"
    assert not p.is_mature_enough()


# ── A7.2 hand-designed V(q) ─────────────────────────────────────────────────


def test_rank_questions_by_value_of_information() -> None:
    values = {
        "q_low": QuestionValue(expected_precision_gain=0.1, novelty=0.1, cost=0.5),
        "q_high": QuestionValue(expected_precision_gain=0.9, novelty=0.8, cost=0.1),
        "q_mid": QuestionValue(expected_precision_gain=0.5, novelty=0.2, cost=0.2),
    }
    assert rank_questions(values)[0] == "q_high"
    assert rank_questions(values)[-1] == "q_low"


# ── A7.3 anti-hacking reward (frozen snapshot, validated-only, no self-cite) ─


def test_reward_zero_before_independent_validation() -> None:
    r = move_reward(RewardInputs("n", validated=False, inbound_from=("a", "b", "c")))
    assert r == 0.0  # no confidence counted before validation


def test_reward_discounts_self_links() -> None:
    # 3 inbound, 2 of them self-links → only 1 real inbound counts.
    r = move_reward(RewardInputs(
        "n", validated=True, inbound_from=("n", "n", "a"), self_links=2))
    assert r == 1.0


def test_reward_caps_reciprocal_and_discounts_hubs() -> None:
    r = move_reward(RewardInputs(
        "n", validated=True, inbound_from=("a", "b"),
        reciprocal_pairs=10, hub_inbound=4), reciprocal_cap=2)
    # 2 real inbound + capped reciprocal(2) - hub_discount(0.25*4=1.0) = 3.0
    assert r == 3.0


def test_reward_not_inflatable_by_self_citation() -> None:
    # a node that self-cites 100 times gains nothing over its real inbound.
    honest = move_reward(RewardInputs("n", validated=True, inbound_from=("a",)))
    gamed = move_reward(RewardInputs(
        "n", validated=True, inbound_from=("a",) + ("n",) * 100, self_links=100))
    assert honest == gamed == 1.0


def test_reward_self_cite_discounted_by_construction_not_caller_count() -> None:
    # Review nit (medium): self-cites are derived from node_id in inbound_from,
    # NOT the caller's self_links. A self-link present in inbound_from but with
    # self_links understated to 0 must STILL be discounted.
    r = move_reward(RewardInputs(
        "n", validated=True, inbound_from=("a", "n", "b"), self_links=0))
    assert r == 2.0  # only 'a' and 'b' count; the self-link 'n' is discounted


def test_reward_negative_counts_cannot_inflate() -> None:
    # Review nit (medium): out-of-domain negative counts are clamped to >=0.
    r = move_reward(RewardInputs(
        "n", validated=True, inbound_from=("a", "b"),
        self_links=-5, reciprocal_pairs=-3, hub_inbound=-100))
    assert r == 2.0  # 2 real inbound; negatives clamped, no inflation


# ── the ranker orders moves only — never commits, never certifies ───────────


def test_move_ranker_orders_by_reward() -> None:
    ranker = MoveRanker()
    candidates = {
        "m1": RewardInputs("m1", validated=True, inbound_from=("a",)),
        "m2": RewardInputs("m2", validated=True, inbound_from=("a", "b", "c")),
        "m3": RewardInputs("m3", validated=False, inbound_from=("a", "b")),  # 0
    }
    assert ranker.order(candidates) == ["m2", "m1", "m3"]  # by descending reward


def test_ranker_cannot_commit_or_certify() -> None:
    ranker = MoveRanker()
    for method in ("commit", "certify"):
        try:
            getattr(ranker, method)()
            raise AssertionError(f"ranker.{method} should raise")
        except RankerAuthorityError:
            pass
    assert not hasattr(ranker, "promote")
