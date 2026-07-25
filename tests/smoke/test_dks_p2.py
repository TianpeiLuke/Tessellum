"""DKS refactor P2 — the seam: CapabilityResult port + DKSExecutor + dks_inquiry.

Gate-to-P3 deliverables:
 - a Capability produces an equivalent DKSCycleResult through the port that the
   CLI would produce directly (same fixed request);
 - the DKSExecutor returns a CANDIDATE (it cannot commit / does not write);
 - dks_inquiry registers on the runtime capability registry keyed on the port;
 - the warrant-bearing envelope carries the Toulmin warrant + qualifier +
   replay token without changing the kernel's internal shape.
"""

from __future__ import annotations

import json

from tessellum.composer import MockBackend
from tessellum.dks import (
    Capability,
    CapabilityResult,
    DKSCandidate,
    DKSCycle,
    DKSExecutor,
    DKSObservation,
    DKSRunner,
    adapt_cycle_result,
    adapt_run_result,
)
from tessellum.runtime.routing import (
    DKS_INQUIRY,
    NATIVE_DIGESTION,
    get_capability_factory,
    is_capability_registered,
    register_capability,
    route_lane,
)


def _arg(claim: str, warrant: str) -> str:
    return json.dumps({
        "claim": claim, "data": "D", "warrant": warrant,
        "backing": "B", "qualifier": "usually", "rebuttal": "r", "evidence": "E",
    })


def _full_backend() -> MockBackend:
    return MockBackend(responses={
        "conservative": _arg("claim-A", "W-A"),
        "exploratory": _arg("claim-B", "W-B"),
        "counter-argument": json.dumps({
            "attacked_fz": "5a", "broken_component": "warrant",
            "counter_claim": "cc", "reason": "r", "strength": "moderate"}),
        "pattern discovery": json.dumps({"description": "p", "observed": ["5a"]}),
        "rule revision": json.dumps({
            "claim": "Revised", "data": "D", "warrant": "W'",
            "qualifier": "in most cases", "supersedes": ""}),
    })


# ── a concrete Capability wrapping the kernel (the adapter) ─────────────────


class _DKSInquiryCapability:
    """A minimal Capability: run one DKS cycle for a fixed request and wrap it.
    Mirrors what the runtime adapter will do; used to prove the port shape."""

    def __init__(self, backend) -> None:
        self._backend = backend

    def invoke(self, request) -> CapabilityResult:
        obs = DKSObservation(folgezettel=request["fz"], summary=request["summary"])
        cycle = DKSCycle(obs, (), self._backend, mode=request.get("mode", "fresh")).run()
        return adapt_cycle_result(cycle)


# ── port conformance + equivalence ──────────────────────────────────────────


def test_capability_satisfies_the_port_protocol() -> None:
    cap = _DKSInquiryCapability(_full_backend())
    assert isinstance(cap, Capability)  # runtime-checkable Protocol


def test_port_result_equivalent_to_direct_cli_run() -> None:
    req = {"fz": "5", "summary": "something happened", "mode": "fresh"}
    # direct (what the CLI does)
    direct = DKSCycle(
        DKSObservation(folgezettel="5", summary="something happened"),
        (), _full_backend(),
    ).run()
    # through the port
    env = _DKSInquiryCapability(_full_backend()).invoke(req)
    assert env.status == "ok"
    assert env.payload.cycle_id == direct.cycle_id
    assert env.payload.closed_loop == direct.closed_loop
    assert env.payload.grounded_labelling == direct.grounded_labelling


# ── warrant-bearing envelope (no shape change) ──────────────────────────────


def test_envelope_carries_warrant_qualifier_and_replay_token() -> None:
    env = _DKSInquiryCapability(_full_backend()).invoke(
        {"fz": "5", "summary": "x"})
    assert env.warrant is not None
    assert env.warrant.warrant == "W'"        # the revised warrant licenses it
    assert env.qualifier == "in most cases"   # calibrated qualifier surfaced
    assert env.replay_token.startswith("dks:")
    # effects were derived (observation + args + counter + pattern + revision)
    roles = {e.bb_role for e in env.effects}
    assert "empirical_observation" in roles and "argument" in roles


def test_replay_token_is_deterministic() -> None:
    a = _DKSInquiryCapability(_full_backend()).invoke({"fz": "5", "summary": "x"})
    b = _DKSInquiryCapability(_full_backend()).invoke({"fz": "5", "summary": "x"})
    assert a.replay_token == b.replay_token  # same request → same token


def test_adapt_run_result_aggregates_cycles() -> None:
    obs = (
        DKSObservation(folgezettel="5", summary="a"),
        DKSObservation(folgezettel="6", summary="b"),
    )
    run = DKSRunner(obs, _full_backend()).run()
    env = adapt_run_result(run)
    assert env.status == "ok"
    assert env.payload is run
    # effects aggregate across both cycles
    assert len({e.folgezettel for e in env.effects}) >= 2


def test_gated_cycle_envelope_is_empty() -> None:
    gated_backend = MockBackend(responses={"conservative": _arg("A", "W-A")})
    obs = DKSObservation(folgezettel="5", summary="x")
    cycle = DKSCycle(
        obs, (), gated_backend,
        confidence_model=lambda o, w: 0.99, confidence_threshold=0.85,
    ).run()
    env = adapt_cycle_result(cycle)
    assert env.status == "empty"  # nothing was disputed


# ── DKSExecutor returns a candidate; never writes ───────────────────────────


def test_executor_returns_candidate_not_commit() -> None:
    cap = _DKSInquiryCapability(_full_backend())
    ex = DKSExecutor(cap)
    candidate = ex.execute(
        {"fz": "5", "summary": "x"}, base_snapshot_id="snap-1", parent_fz=None,
    )
    assert isinstance(candidate, DKSCandidate)
    assert candidate.base_snapshot_id == "snap-1"
    assert isinstance(candidate.result, CapabilityResult)
    # the executor exposes no write/commit/promote surface.
    assert not hasattr(ex, "commit")
    assert not hasattr(ex, "promote")
    assert not hasattr(ex, "write")


# ── dks_inquiry registers on the runtime registry (additive) ────────────────


def test_dks_inquiry_registers_on_capability_registry() -> None:
    register_capability(DKS_INQUIRY, lambda: _DKSInquiryCapability(_full_backend()))
    assert is_capability_registered(DKS_INQUIRY)
    factory = get_capability_factory(DKS_INQUIRY)
    cap = factory()
    assert isinstance(cap, Capability)


def test_native_digestion_lane_routing_unchanged(tmp_path) -> None:
    # the shipped lane→native_digestion path is byte-identical (P2 is additive).
    # build the four phase skills so route_lane's digest succeeds.
    from tessellum.composer.digestion import PHASE_SKILLS
    sd = tmp_path / "skills"
    sd.mkdir()
    for phase in ("plan", "augment", "review", "execute"):
        (sd / f"{PHASE_SKILLS[phase]}.md").write_text("# skill\n", encoding="utf-8")
    route = route_lane("papers", skills_dir=sd)
    assert route.capability == NATIVE_DIGESTION
