"""tessellum.dks.elevation — self-driving elevation (decision b4a + the contract).

P7 of the DKS refactor plan — the maturity / certificate / ranker apparatus,
built LAST and only after everything below it is validated, because this is
where reward hacking and self-certification bite hardest.

Ships (pure structure):

- A7.1 **knowledge-maturity profile** + `DeepUnderstandingCertificate` — a
  9-capability profile (ABSENT → VALIDATED); the certificate is issued ONLY by
  validators that are NOT the reasoning backend (the mover-is-never-the-judge
  rule, P3), moving a sufficiently-mature inquiry into `UNDERSTOOD_WATCHING`
  with ranked future questions + invalidation triggers. It is REVOCABLE.
- A7.2 **hand-designed `V(q)` question value first** — a value-of-information
  score ranking candidate questions/moves; run + audited before any learning.
- A7.3 **the anti-hacking reward CONSTRUCTION (b4a)** — reward computed over a
  FROZEN published snapshot the policy cannot write to; confidence counted only
  after independent validation; seed-anchored TrustRank (self-links = 0,
  hub-discounted, reciprocal-capped) — NOT raw in-degree/PPR (ρ = 0.554 yet
  forgeable). The offline-RL policy FIT is the research prerequisite and is not
  bundled; what ships is the un-inflatable reward computation + the invariant
  that the ranker only ORDERS moves — never the commit authority, never the
  certificate.

All pure: no clock, no model, no vault write.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

# ── A7.1 knowledge-maturity profile ─────────────────────────────────────────

MaturityLevel = Literal["ABSENT", "CLAIMED", "SUPPORTED", "CHALLENGED", "VALIDATED"]
_MATURITY_ORDER: dict[str, int] = {
    "ABSENT": 0, "CLAIMED": 1, "SUPPORTED": 2, "CHALLENGED": 3, "VALIDATED": 4,
}

# The nine capabilities an inquiry cluster's maturity is profiled across.
CAPABILITIES: tuple[str, ...] = (
    "observation", "argument", "counter_argument", "pattern", "warrant",
    "provenance", "independent_validation", "coverage", "reproducibility",
)


@dataclass(frozen=True)
class MaturityProfile:
    """A per-capability maturity profile (A7.1). ``levels`` maps each capability
    to its attested level; capabilities absent from the map are ``ABSENT``."""

    levels: dict[str, MaturityLevel] = field(default_factory=dict)

    def level(self, capability: str) -> MaturityLevel:
        return self.levels.get(capability, "ABSENT")

    def is_mature_enough(self, *, min_level: MaturityLevel = "VALIDATED",
                         required: tuple[str, ...] | None = None) -> bool:
        """True iff every REQUIRED capability is at ≥ ``min_level``. Defaults to
        requiring the validation-bearing capabilities at VALIDATED."""
        req = required or ("independent_validation", "warrant", "provenance")
        floor = _MATURITY_ORDER[min_level]
        return all(_MATURITY_ORDER[self.level(c)] >= floor for c in req)


# ── A7.1 the deep-understanding certificate (validator-issued, revocable) ───


@dataclass(frozen=True)
class DeepUnderstandingCertificate:
    """A revocable attestation that an inquiry cluster is understood (A7.1).

    ``issuer`` must be an independent validator id — NOT the reasoning backend.
    ``ranked_future_questions`` + ``invalidation_triggers`` accompany the move
    into ``UNDERSTOOD_WATCHING`` (understood-but-watching, not final closure).
    """

    inquiry_id: str
    issuer: str
    profile: MaturityProfile
    ranked_future_questions: tuple[str, ...] = ()
    invalidation_triggers: tuple[str, ...] = ()
    revoked: bool = False


class CertificateError(Exception):
    pass


def issue_certificate(
    inquiry_id: str,
    profile: MaturityProfile,
    *,
    issuer: str,
    reasoning_backend_id: str,
    ranked_future_questions: tuple[str, ...] = (),
    invalidation_triggers: tuple[str, ...] = (),
) -> DeepUnderstandingCertificate:
    """Issue a certificate — ONLY when the issuer is an independent validator
    (not the reasoning backend) AND the profile is mature enough (A7.1, P3).

    Raises ``CertificateError`` if the reasoning backend tries to certify its
    own output (the mover-is-never-the-judge rule) or the profile is immature."""
    # Normalize both principals before comparison so an issuer differing only
    # by whitespace/case from the reasoning backend cannot self-certify.
    norm_issuer = (issuer or "").strip().casefold()
    norm_backend = (reasoning_backend_id or "").strip().casefold()
    if not norm_issuer or norm_issuer == norm_backend:
        raise CertificateError(
            "the reasoning backend may not issue its own certificate "
            "(the mover is never the judge)"
        )
    if not profile.is_mature_enough():
        raise CertificateError(
            "inquiry not mature enough for a deep-understanding certificate "
            "(independent_validation / warrant / provenance must be VALIDATED)"
        )
    return DeepUnderstandingCertificate(
        inquiry_id=inquiry_id, issuer=issuer, profile=profile,
        ranked_future_questions=ranked_future_questions,
        invalidation_triggers=invalidation_triggers,
    )


def revoke(cert: DeepUnderstandingCertificate) -> DeepUnderstandingCertificate:
    """Revoke a certificate (A7.1 — certificates are revocable when an
    invalidation trigger fires)."""
    return DeepUnderstandingCertificate(
        inquiry_id=cert.inquiry_id, issuer=cert.issuer, profile=cert.profile,
        ranked_future_questions=cert.ranked_future_questions,
        invalidation_triggers=cert.invalidation_triggers, revoked=True,
    )


# ── A7.2 hand-designed question value V(q) ──────────────────────────────────


@dataclass(frozen=True)
class QuestionValue:
    """A hand-designed value-of-information score for a candidate question/move
    (A7.2 — run + audited BEFORE any offline-RL ranker). Higher = more worth
    pursuing. Composed from expected precision gain, novelty, and cost."""

    expected_precision_gain: float
    novelty: float
    cost: float

    @property
    def value(self) -> float:
        # a transparent, auditable VOI: gain + novelty, discounted by cost.
        return self.expected_precision_gain + 0.5 * self.novelty - self.cost


def rank_questions(values: dict[str, QuestionValue]) -> list[str]:
    """Rank candidate question ids by hand-designed V(q) (A7.2), descending,
    ties broken by id for determinism."""
    return sorted(values, key=lambda q: (-values[q].value, q))


# ── A7.3 the anti-hacking reward CONSTRUCTION (b4a) ─────────────────────────


@dataclass(frozen=True)
class RewardInputs:
    """Inputs to the move reward, all read from a FROZEN published snapshot the
    policy cannot write to within the epoch (b4a). ``validated`` gates whether
    any confidence is counted at all."""

    node_id: str
    validated: bool                 # independent-validation passed (P4)?
    inbound_from: tuple[str, ...] = ()   # nodes linking TO this node (in the frozen snapshot)
    self_links: int = 0             # self-citations (always discounted to 0)
    reciprocal_pairs: int = 0       # reciprocal-link count (capped)
    hub_inbound: int = 0            # inbound from high-degree hubs (discounted)


def move_reward(inputs: RewardInputs, *, reciprocal_cap: int = 2) -> float:
    """Compute a move's reward over a FROZEN snapshot — un-inflatable by
    self-citation (b4a). Zero unless the node passed independent validation;
    self-links contribute nothing; reciprocal links are capped; hub inbound is
    discounted. This is seed-anchored-TrustRank-shaped, NOT raw in-degree/PPR
    (which correlate only at ρ = 0.554 yet remain forgeable).

    IMPORTANT: this reward only ever ORDERS candidate moves — it is never the
    commit authority and never the certificate (that stays validator-issued)."""
    if not inputs.validated:
        return 0.0  # no confidence counted before independent validation
    # Self-cites are discounted BY CONSTRUCTION, derived from the data (node_id
    # in inbound_from) — NOT trusted from a caller-supplied count — so a self-
    # link in inbound_from can never be counted as trust even if self_links is
    # understated (the FATAL self-citation attack the plan names). All discount
    # counts are clamped to >= 0 so an out-of-domain negative can never inflate.
    real_inbound = sum(1 for x in inputs.inbound_from if x != inputs.node_id)
    capped_reciprocal = min(max(0, inputs.reciprocal_pairs), max(0, reciprocal_cap))
    hub_discount = 0.25 * max(0, inputs.hub_inbound)
    return float(real_inbound + capped_reciprocal) - hub_discount


class RankerAuthorityError(Exception):
    """Raised if a move-ranker is asked to commit or certify — it may only
    ORDER moves (the b4a invariant)."""


@dataclass(frozen=True)
class MoveRanker:
    """Orders candidate moves by their frozen-snapshot reward (A7.3). It has NO
    ``commit`` / ``certify`` / ``promote`` method BY CONSTRUCTION — the offline-
    RL policy fit (BC → CQL-pessimistic) is the research prerequisite and is
    injected; what ships here is the ordering + the authority invariant."""

    reciprocal_cap: int = 2

    def order(self, candidates: dict[str, RewardInputs]) -> list[str]:
        """Return move ids ordered by descending reward (ties by id). Ordering
        ONLY — never a promotion or a certificate."""
        return sorted(
            candidates,
            key=lambda m: (-move_reward(candidates[m], reciprocal_cap=self.reciprocal_cap), m),
        )

    def commit(self, *_a, **_k):  # pragma: no cover - guard
        raise RankerAuthorityError(
            "a move-ranker orders moves only; it is never the commit authority"
        )

    def certify(self, *_a, **_k):  # pragma: no cover - guard
        raise RankerAuthorityError(
            "a move-ranker orders moves only; it never issues a certificate"
        )


__all__ = [
    "MaturityLevel",
    "CAPABILITIES",
    "MaturityProfile",
    "DeepUnderstandingCertificate",
    "CertificateError",
    "issue_certificate",
    "revoke",
    "QuestionValue",
    "rank_questions",
    "RewardInputs",
    "move_reward",
    "MoveRanker",
    "RankerAuthorityError",
]
