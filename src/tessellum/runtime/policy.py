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
    tools_enabled: bool = False
    max_attempts: int = 3
    lease_ttl: float = 120.0

    @classmethod
    def for_profile(cls, profile: str) -> "RuntimePolicy":
        if profile == "fast":
            return cls(max_workers=2, max_invocations=30, max_fix_rounds=0)
        if profile != "default":
            raise ValueError(f"unknown runtime policy profile: {profile!r}")
        return cls()
