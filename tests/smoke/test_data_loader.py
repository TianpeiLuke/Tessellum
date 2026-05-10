"""Smoke tests for ``tessellum.data.templates_dir`` — exercises the dev-mode
fallback (editable install) since pytest runs against the source checkout.

Wheel-install mode is verified out-of-band by `python -m build` plus a
clean-venv install + smoke check (documented in CHANGELOG and the v0.1
plan's validation section).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.data import templates_dir

# Templates that must always exist in the templates directory. Reflects the 13
# files currently in vault/resources/templates/ (12 BB-type + 1 YAML reference).
EXPECTED_TEMPLATES: tuple[str, ...] = (
    "template_yaml_header.md",
    "template_concept.md",
    "template_procedure.md",
    "template_skill.md",
    "template_model.md",
    "template_argument.md",
    "template_counter_argument.md",
    "template_hypothesis.md",
    "template_empirical_observation.md",
    "template_experiment.md",
    "template_navigation.md",
    "template_entry_point.md",
    "template_acronym_glossary.md",
)


def test_templates_dir_returns_existing_directory():
    p = templates_dir()
    assert isinstance(p, Path)
    assert p.is_dir(), f"templates_dir() returned non-dir path: {p}"


def test_templates_dir_contains_template_files():
    p = templates_dir()
    found = sorted(f.name for f in p.glob("template_*.md"))
    assert len(found) >= len(EXPECTED_TEMPLATES), (
        f"expected ≥{len(EXPECTED_TEMPLATES)} templates, found {len(found)}: {found}"
    )


@pytest.mark.parametrize("template_name", EXPECTED_TEMPLATES)
def test_each_expected_template_present(template_name):
    p = templates_dir() / template_name
    assert p.is_file(), f"missing template: {p}"


def test_templates_have_yaml_frontmatter():
    """Sanity check: every template is a Tessellum-formatted note."""
    for template_name in EXPECTED_TEMPLATES:
        path = templates_dir() / template_name
        content = path.read_text(encoding="utf-8")
        assert content.startswith("---\n"), (
            f"{template_name} does not start with YAML frontmatter"
        )
