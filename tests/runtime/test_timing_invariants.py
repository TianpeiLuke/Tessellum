"""R2.3 (FZ 20k9c1a1a1b7c2k2a1b) — the timing assertion table + R3.4's
transport-timeout classification fixture."""
from __future__ import annotations

from tessellum.composer.executor import classify_error
from tessellum.runtime.timing import all_profile_violations, timing_violations


def test_every_shipped_profile_satisfies_the_timing_invariants() -> None:
    """Post-R2.4: EVERY shipped profile is clean — converge's INV-2 exception
    (TTL 900 → cadence > default claim TTL, safe only via the entry re-lease)
    was deleted by the detector rollback."""
    assert all(v == [] for v in all_profile_violations().values())


def test_inv2_still_fires_for_a_hypothetical_long_ttl_profile(monkeypatch) -> None:
    """The INV-2 arithmetic guard remains armed: a profile with cadence >=
    the default claim TTL must produce the entry-re-lease-naming finding."""
    from tessellum.runtime.policy import RuntimePolicy

    real = RuntimePolicy.for_profile

    def fake(profile):
        if profile == "converge":
            return RuntimePolicy(max_review_rounds=2, lease_ttl=900.0)
        return real(profile)

    monkeypatch.setattr(RuntimePolicy, "for_profile", staticmethod(fake))
    findings = timing_violations("converge")
    assert findings and all("entry re-lease" in f for f in findings)


def test_transport_timeout_is_transient_not_crash() -> None:
    """R3.4 fixture (a): run 6 recorded its ReadTimeout as `crash`, burning
    crash-recovery budget on the one class where waiting-and-retrying is the
    whole cure. Transport timeouts ride the stall/transient rung now."""
    assert classify_error("ReadTimeout: The read operation timed out") == "transient"
    assert classify_error("httpx.ConnectTimeout: timed out") == "transient"
    assert classify_error("stalled after 360s") == "transient"
