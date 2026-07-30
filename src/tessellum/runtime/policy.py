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
    # Phase 4 (FZ 20k9c1a1a1b7c2k2a3a) — checkpoint-resume at claim. The job
    # dir is the run scope on the service path (only generations of the SAME
    # job share it), so a re-claimed retry finds its predecessor's A1.2
    # checkpoints in place and skips the already-paid linear phases; the
    # composer additionally refuses a resume whose code-measured ledger does
    # not match the claimed source (fail-soft fresh start). ON by default —
    # the two external kills and the credit wall each re-paid ~15 min of
    # linear work the checkpoints already contained.
    resume_from_checkpoint: bool = True
    # W2 (FZ 20k9c1a1a1b7c2k2a4) — the FREE deterministic identifier layer,
    # ON by default: no calibration artifact, no scorer calls, precision-
    # allowlisted, two-tier (absent-from-source blocks; outside-owned-slice
    # is advisory). The calibrated certificate stays opt-in behind
    # `grounding_gate` + its artifact. Before this, the fabrication defense
    # was deployed but never enabled live (runs 9–13 all ran without it).
    identifier_grounding: bool = True

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
            # lease_ttl: R2.4 (FZ 20k9c1a1a1b7c2k2a1b) rolled the interim 900s
            # back to the detector default — a TTL is "how fast do we declare
            # a worker dead", never a workload bound. The interim 900 was a
            # mitigation for a dead renewal actor (run 6, hypothesis-labeled);
            # with R2.1 the actor retries transients, escalates loudly on
            # staleness, and journals every beat, and the schedule test
            # proves a blocked call 2.5x the TTL survives under it. History
            # of the wrong turn: R5.2's corrected record in the CHANGELOG.
            return cls(max_review_rounds=2)
        if profile != "default":
            raise ValueError(f"unknown runtime policy profile: {profile!r}")
        return cls()
