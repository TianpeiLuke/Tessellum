"""R2.3 (FZ 20k9c1a1a1b7c2k2a1b) — the timing assertion table + R3.4's
transport-timeout classification fixture."""
from __future__ import annotations

from tessellum.composer.executor import classify_error
from tessellum.runtime.timing import all_profile_violations, timing_violations


def test_every_shipped_profile_satisfies_the_timing_invariants() -> None:
    v = all_profile_violations()
    assert v["default"] == []
    assert v["fast"] == []
    assert v["inspect"] == []


def test_converge_inv2_names_the_discharging_mechanism() -> None:
    """converge (TTL 900 → cadence 300 > default claim 120) trips INV-2's
    arithmetic half — the finding must NAME the entry re-lease so removing
    that mechanism without fixing the numbers is loud. R2.4's detector
    rollback deletes this exception."""
    findings = timing_violations("converge")
    assert findings and all("entry re-lease" in f for f in findings)


def test_transport_timeout_is_transient_not_crash() -> None:
    """R3.4 fixture (a): run 6 recorded its ReadTimeout as `crash`, burning
    crash-recovery budget on the one class where waiting-and-retrying is the
    whole cure. Transport timeouts ride the stall/transient rung now."""
    assert classify_error("ReadTimeout: The read operation timed out") == "transient"
    assert classify_error("httpx.ConnectTimeout: timed out") == "transient"
    assert classify_error("stalled after 360s") == "transient"
