"""FZ 20k9d1b1a P3 — the registry ⟺ template ⟺ contract consistency gate.

BB_SPECS[bb].required_sections is the authoritative per-building-block section
contract. These tests assert (1) the consistency check is GREEN for the shipped
templates (every primary-type template declares its BB's required sections;
section-divergent flavors are documented + exempt), and (2) the validator's
TESS-010 surfaces a missing required section on a real note (advisory INFO).
"""

from __future__ import annotations

from pathlib import Path

from tessellum.capture import (
    REGISTRY,
    SECTION_DIVERGENT_FLAVORS,
    check_template_registry_consistency,
)
from tessellum.format import validate
from tessellum.format.building_blocks import BB_SPECS, BuildingBlock
from tessellum.format.issue import Severity


def test_registry_template_consistency_is_green() -> None:
    # Every registered template's building_block matches its bb_type, and every
    # primary-type template declares its BB's required_sections. Any drift here
    # is a real regression to fix (or an intentional divergence to exempt).
    findings = check_template_registry_consistency()
    assert findings == [], "template/registry drift:\n" + "\n".join(findings)


def test_divergent_flavors_are_a_subset_of_registry() -> None:
    # The exemption set must name only real flavors (no stale entries).
    assert SECTION_DIVERGENT_FLAVORS <= set(REGISTRY)


def test_every_bb_type_in_registry_resolves_in_bb_specs() -> None:
    for spec in REGISTRY.values():
        assert BuildingBlock(spec.bb_type) in BB_SPECS


def test_new_flavors_registered() -> None:
    for flavor in ("faq", "sop", "coe", "thought"):
        assert flavor in REGISTRY


def _infos(issues) -> list[str]:
    return [i.rule_id for i in issues if i.severity == Severity.INFO]


def test_tess010_flags_missing_required_section(tmp_path: Path) -> None:
    # A concept note (required: Definition, Examples, References) missing Examples
    # gets a TESS-010 INFO issue — advisory, not an ERROR.
    note = tmp_path / "term_x.md"
    note.write_text(
        "---\n"
        "tags:\n  - resource\n  - terminology\n"
        "keywords:\n  - a\n  - b\n  - c\n"
        "topics:\n  - X\n  - Y\n"
        "language: markdown\n"
        "date of note: 2026-07-26\n"
        "status: active\n"
        "building_block: concept\n"
        "---\n\n# X\n\n## Definition\nd\n\n## References\n- r\n",
        encoding="utf-8",
    )
    issues = validate(note)
    tess010 = [i for i in issues if i.rule_id == "TESS-010"]
    assert any("Examples" in i.message for i in tess010)
    # advisory only — no ERROR from the missing section
    assert all(i.severity != Severity.ERROR for i in tess010)


def test_tess010_silent_when_all_sections_present(tmp_path: Path) -> None:
    note = tmp_path / "term_y.md"
    note.write_text(
        "---\n"
        "tags:\n  - resource\n  - terminology\n"
        "keywords:\n  - a\n  - b\n  - c\n"
        "topics:\n  - X\n  - Y\n"
        "language: markdown\n"
        "date of note: 2026-07-26\n"
        "status: active\n"
        "building_block: concept\n"
        "---\n\n# Y\n\n## Definition\nd\n\n## Examples\ne\n\n## References\n- r\n",
        encoding="utf-8",
    )
    assert "TESS-010" not in _infos(validate(note))


def test_tess010_exempts_template_status(tmp_path: Path) -> None:
    # A status: template scaffold legitimately omits filled sections.
    note = tmp_path / "template_z.md"
    note.write_text(
        "---\n"
        "tags:\n  - resource\n  - template\n"
        "keywords:\n  - a\n  - b\n  - c\n"
        "topics:\n  - X\n  - Y\n"
        "language: markdown\n"
        "date of note: 2026-07-26\n"
        "status: template\n"
        "building_block: concept\n"
        "---\n\n# Z\n\n## Definition\nd\n",
        encoding="utf-8",
    )
    assert "TESS-010" not in _infos(validate(note))
