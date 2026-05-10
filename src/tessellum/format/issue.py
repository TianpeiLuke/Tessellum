"""Shared issue + severity types.

Lives in its own module so ``validator`` and ``link_checker`` can both depend
on it without forming a cycle.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class Issue:
    """A single format-check finding.

    Attributes:
        severity: ERROR / WARNING / INFO.
        rule_id:  Stable identifier (e.g. ``YAML-014``, ``LINK-003``,
                  ``TESS-001``). Useful for grep + JSON pipelines.
        field:    Frontmatter field name or sub-locator (e.g. ``tags[0]``,
                  ``links``). ``None`` for whole-note issues.
        message:  Human-readable description.
    """

    severity: Severity
    rule_id: str
    field: str | None
    message: str

    def __str__(self) -> str:
        loc = f"[{self.field}]" if self.field else ""
        return f"{self.severity.value.upper()}{loc} {self.rule_id}: {self.message}"
