"""Runtime safety defaults for unattended digestion."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimePolicy:
    max_workers: int = 4
    max_invocations: int = 100
    max_cost: float | None = None
    max_fix_rounds: int = 1
    context_strategy: str = "windowed"
    context_max_chars: int = 120_000
    close_gate: bool = True
    wave_gate: bool = True
    # P8/F6 (FZ 20k9c1a1a1b7c2e): run the note-level GROUNDING check at close, not
    # just the format check. Default OFF: the shipped grounding certificate is
    # fail-closed until it is calibrated on a real model + labelled corpus (the
    # semantic-certificate A7.5 prereq) — an uncalibrated certificate abstains on
    # EVERY note (blocks the whole pipeline). A deployment with a calibrated
    # certificate sets this True to close the F6 gap (a source-unfaithful note
    # passing the format-only close gate). When True + no calibration, the gate
    # correctly fails closed (blocks) rather than silently admitting.
    grounding_gate: bool = False
    tools_enabled: bool = False
    max_attempts: int = 3
    lease_ttl: float = 120.0
    # P17 — run-level error-class circuit breaker. The execute wave aborts once
    # this proportion of its dispatched leaves have failed with the same
    # systemic class (auth / rate_limit), instead of burning the whole
    # invocation budget against the same wall. ``None`` disables the breaker
    # (a healthy wave with scattered transient failures never trips regardless).
    breaker_proportion: float | None = 0.8
    breaker_min_dispatched: int = 3
    # Absolute backstop: abort after this many terminal systemic (auth /
    # rate_limit) failures REGARDLESS of proportion. The proportional rule alone
    # is defeated by a mid-wave credential-pool death — early successes inflate
    # the denominator so the ratio may never reach ``breaker_proportion`` (a
    # 100-leaf wave that succeeds 40× then dies never trips at 0.8). A healthy
    # wave has ~0 TERMINAL systemic failures (auth/rate_limit that survived the
    # retry ladder are a real wall, not per-leaf flakiness), so a modest
    # absolute count is safe. ``None`` disables the backstop.
    breaker_error_threshold: int | None = 10
    # T3 (FZ 20k9d6a) — inspect-before-execute. When ``"review"``, the digestion
    # runs plan→augment→review and STOPS at an accepted plan WITHOUT dispatching
    # the execute wave (the supervisor parks the job in PAUSED). A human then
    # inspects the plan and `promote`s (resume into the execute wave) or
    # `reject`s. ``None`` (default) → the full plan→…→execute path, byte-identical
    # to pre-T3. The ``inspect`` profile sets it.
    stop_after: str | None = None
    # J3 (FZ 20k9c1a1a1b7c2k2) — the P15 review-revise loop on the service
    # path. Before this, the runtime executor never passed the parameter, so
    # the loop that demonstrably converges an over-split plan toward the
    # golden count (the API runs' 17→16→8) was unreachable under the
    # supervisor. ``0`` (default) → single-pass, byte-identical to pre-J3.
    max_review_rounds: int = 0

    @classmethod
    def for_profile(cls, profile: str) -> "RuntimePolicy":
        if profile == "fast":
            return cls(max_workers=2, max_invocations=30, max_fix_rounds=0)
        if profile == "inspect":
            return cls(stop_after="review")
        if profile == "converge":
            # J3 (FZ 20k9c1a1a1b7c2k2): the convergence posture — the P15
            # revise loop ON so an over-split round-0 plan is driven toward
            # the gates' note-count band before sign-off (the API runs'
            # demonstrated 17→16→8 cure).
            #
            # lease_ttl CORRECTED RECORD (R5.2, FZ 20k9c1a1a1b7c2k2a1e): the
            # original comment claimed "no heartbeat can renew INSIDE a
            # blocked call" — false: the supervisor's daemon renewal thread
            # (shipped v1.2.0) renews every ttl/3 independent of the blocked
            # main thread. Run 6's lease death mechanism is a labeled
            # HYPOTHESIS (the renewal thread stopped renewing — one-shot-fatal
            # exit or repeated busy-skips; undiagnosable because no renewal
            # journal existed — the discriminating instrumentation is R2.1's
            # heartbeats journal). A large TTL is therefore a MITIGATION that
            # widens the survivable dead-renewal window, not a workload bound;
            # per the timing-algebra design (FZ b7c2k2a1b) it rolls back to a
            # detector constant once the renewal actor is hardened (R2.4).
            return cls(max_review_rounds=2, lease_ttl=900.0)
        if profile != "default":
            raise ValueError(f"unknown runtime policy profile: {profile!r}")
        return cls()
