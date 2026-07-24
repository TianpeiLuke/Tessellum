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
