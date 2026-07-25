"""Explicit inbox-lane routing to the pinned native digestion capability."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from tessellum.composer.digestion import PHASE_SKILLS


LANE_HINTS: dict[str, tuple[str | None, str]] = {
    "papers": ("empirical_observation", "scholarly source"),
    "book": (None, "long-form source"),
    "podcast": (None, "transcript"),
    "sops": ("procedure", "policy or procedure"),
    "manual_retrieved": (None, "externally retrieved evidence"),
    "general": (None, "general source"),
    "latex": (None, "technical manuscript"),
    "flash": (None, "low-latency capture"),
}


class RoutingError(ValueError):
    pass


@dataclass(frozen=True)
class DigestionRoute:
    capability: str
    skill_digest: str
    building_block_hint: str | None
    source_kind: str


def route_lane(lane: str, *, skills_dir: Path | str) -> DigestionRoute:
    if lane not in LANE_HINTS:
        raise RoutingError(f"unsupported inbox lane: {lane!r}")
    root = Path(skills_dir)
    digest = hashlib.sha256()
    for phase in ("plan", "augment", "review", "execute"):
        path = root / f"{PHASE_SKILLS[phase]}.md"
        if not path.is_file():
            raise RoutingError(f"required digestion skill not found: {path}")
        digest.update(phase.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
    bb_hint, source_kind = LANE_HINTS[lane]
    return DigestionRoute(
        capability="native_digestion",
        skill_digest=digest.hexdigest(),
        building_block_hint=bb_hint,
        source_kind=source_kind,
    )


# ── P2 (b1a): capability registry keyed on the port ──────────────────────────
#
# The runtime routes ``native_digestion`` today (route_lane above, unchanged).
# P2 adds ``dks_inquiry`` as a SECOND capability so the supervisor can drive the
# DKS kernel through the SAME commit tail. The registry is keyed by capability
# name; a value is a zero-arg factory returning a
# :class:`tessellum.dks.capability.Capability` (the port). This stays additive:
# nothing selects ``dks_inquiry`` automatically — a caller opts in by name, and
# the shipped lane→native_digestion path is byte-identical.

NATIVE_DIGESTION = "native_digestion"
DKS_INQUIRY = "dks_inquiry"

_CAPABILITY_REGISTRY: dict[str, object] = {}


class CapabilityNotRegistered(RoutingError):
    pass


def register_capability(name: str, factory: object) -> None:
    """Register a capability factory under ``name`` (idempotent overwrite)."""
    _CAPABILITY_REGISTRY[name] = factory


def get_capability_factory(name: str) -> object:
    """Look up a registered capability factory, or raise if absent."""
    if name not in _CAPABILITY_REGISTRY:
        raise CapabilityNotRegistered(
            f"capability {name!r} is not registered; known: "
            f"{sorted(_CAPABILITY_REGISTRY)}"
        )
    return _CAPABILITY_REGISTRY[name]


def is_capability_registered(name: str) -> bool:
    return name in _CAPABILITY_REGISTRY
