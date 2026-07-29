"""R2.3 (FZ 20k9c1a1a1b7c2k2a1b): the timing assertion table.

Every ordering between two racing timers, machine-asserted in ONE place —
the panel's inventory found the system's liveness constants free-floating
across five modules with their relationships stated only in comments that
disagreed with each other and with the code (the F5→F6→F7 chain manufactured
one defect per locally-sound change). Two timer families, per the
timing-algebra design: DETECTOR constants (how fast death is declared) and
WORKLOAD bounds (how long legitimate work may take); they never borrow each
other's numbers, and every cross-family relationship is asserted here.

Report-style: :func:`timing_violations` returns finding strings; the CI test
asserts every shipped profile is clean, and a deployment can call it at
startup. Raising is the caller's policy decision.
"""
from __future__ import annotations

from tessellum.composer.executor import DEFAULT_TIMEOUT_SECONDS
from tessellum.composer.llm import CONNECT_TIMEOUT_S, READ_TIMEOUT_S
from tessellum.runtime.policy import RuntimePolicy

WATCHDOG_SLACK_S: float = 60.0
"""The step watchdog must dominate the transport read timeout by at least
this much — equality means the two bounded waits race to fire first."""

PROFILES: tuple[str, ...] = ("default", "fast", "inspect", "converge")


def timing_violations(profile: str = "default") -> list[str]:
    """The assertion table for one profile. Empty = every invariant holds."""
    findings: list[str] = []
    policy = RuntimePolicy.for_profile(profile)
    default_ttl = RuntimePolicy().lease_ttl

    # INV-1: at least two renewal beats fit inside the profile TTL — a single
    # missed beat must never be fatal by arithmetic alone.
    cadence = policy.lease_ttl / 3.0
    if not cadence * 2 <= policy.lease_ttl:
        findings.append(
            f"{profile}: renewal cadence {cadence}s does not fit two beats "
            f"inside lease_ttl {policy.lease_ttl}s"
        )

    # INV-2 (the F7 class): the profile's renewal cadence must be shorter than
    # the DEFAULT claim TTL, OR the entry re-lease mechanism must be in place
    # (it is — supervisor._heartbeat re-leases synchronously on entry). We
    # assert the ARITHMETIC half so removing the mechanism without fixing the
    # numbers fails loudly here.
    if cadence >= default_ttl:
        findings.append(
            f"{profile}: renewal cadence {cadence}s >= default claim TTL "
            f"{default_ttl}s — safe ONLY via the entry re-lease "
            f"(supervisor._heartbeat); do not remove that without fixing this"
        )

    # INV-3 (the F5/F6 seam): the step watchdog dominates the transport read
    # timeout with real slack — zero slack means two bounded waits racing.
    if not DEFAULT_TIMEOUT_SECONDS >= READ_TIMEOUT_S + WATCHDOG_SLACK_S:
        findings.append(
            f"step watchdog {DEFAULT_TIMEOUT_SECONDS}s < transport read "
            f"{READ_TIMEOUT_S}s + slack {WATCHDOG_SLACK_S}s"
        )

    # INV-4: connect timeout is a small detector-family constant.
    if not CONNECT_TIMEOUT_S <= default_ttl:
        findings.append(
            f"connect timeout {CONNECT_TIMEOUT_S}s exceeds the default "
            f"lease TTL {default_ttl}s"
        )

    return findings


def all_profile_violations() -> dict[str, list[str]]:
    """Every shipped profile's findings — the CI enforcement surface."""
    return {p: timing_violations(p) for p in PROFILES}
