"""Smoke tests for ``tessellum.capture``."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

from tessellum.capture import (
    REGISTRY,
    CaptureResult,
    TemplateSpec,
    capture,
    get_spec,
    list_flavors,
)
from tessellum.format import Severity, validate


def _make_vault(tmp_path: Path) -> Path:
    """Create a vault directory tree covering all destinations in REGISTRY."""
    vault = tmp_path / "vault"
    destinations = {spec.destination for spec in REGISTRY.values()}
    for dest in destinations:
        (vault / dest).mkdir(parents=True, exist_ok=True)
    return vault


@pytest.fixture
def vault_root(tmp_path: Path) -> Path:
    return _make_vault(tmp_path)


def test_list_flavors_returns_all_registered():
    flavors = list_flavors()
    assert len(flavors) == 12
    assert flavors == sorted(flavors)
    expected = {
        "concept", "procedure", "skill", "model",
        "argument", "counter_argument", "hypothesis",
        "empirical_observation", "experiment",
        "navigation", "entry_point", "acronym_glossary",
    }
    assert set(flavors) == expected


def test_get_spec_returns_correct_type():
    spec = get_spec("concept")
    assert isinstance(spec, TemplateSpec)
    assert spec.flavor == "concept"
    assert spec.template_filename == "template_concept.md"
    assert spec.destination == "resources/term_dictionary"
    assert spec.filename_prefix == "term_"


def test_get_spec_unknown_raises():
    with pytest.raises(ValueError, match="unknown template flavor"):
        get_spec("not_a_flavor")


def test_capture_concept_creates_file_at_expected_path(vault_root):
    result = capture("concept", "page_rank", vault_root=vault_root)
    expected = vault_root / "resources/term_dictionary/term_page_rank.md"
    assert result.path == expected
    assert result.path.is_file()


def test_capture_returns_capture_result(vault_root):
    result = capture("concept", "foo", vault_root=vault_root)
    assert isinstance(result, CaptureResult)
    assert result.flavor == "concept"
    assert result.slug == "foo"


def test_capture_strips_how_to_use_block(vault_root):
    result = capture("concept", "foo", vault_root=vault_root)
    text = result.path.read_text(encoding="utf-8")
    assert "HOW TO USE THIS TEMPLATE" not in text
    # The instructional text inside HOW TO USE references a literal
    # `<!-- HOW TO USE -->` snippet ("5. Remove this <!-- HOW TO USE -->
    # commentary block."). The regex must NOT stop at that inner mention;
    # it should only stop at the outer ``-->`` on its own line.
    assert "commentary block" not in text
    assert "EPISTEMIC FUNCTION" not in text  # also lives inside the block


def test_capture_sets_today_as_date_by_default(vault_root):
    result = capture("concept", "foo", vault_root=vault_root)
    text = result.path.read_text(encoding="utf-8")
    today = dt.date.today().isoformat()
    assert f"date of note: {today}" in text


def test_capture_sets_status_to_draft(vault_root):
    result = capture("concept", "foo", vault_root=vault_root)
    text = result.path.read_text(encoding="utf-8")
    assert "status: draft" in text
    assert "status: template" not in text


def test_capture_today_override_used(vault_root):
    fixed = dt.date(2025, 1, 15)
    result = capture("concept", "foo", vault_root=vault_root, today=fixed)
    text = result.path.read_text(encoding="utf-8")
    assert "date of note: 2025-01-15" in text


def test_capture_invalid_slug_uppercase_raises(vault_root):
    with pytest.raises(ValueError, match="slug"):
        capture("concept", "Bad", vault_root=vault_root)


def test_capture_invalid_slug_with_space_raises(vault_root):
    with pytest.raises(ValueError, match="slug"):
        capture("concept", "bad slug", vault_root=vault_root)


def test_capture_invalid_slug_with_hyphen_raises(vault_root):
    with pytest.raises(ValueError, match="slug"):
        capture("concept", "bad-slug", vault_root=vault_root)


def test_capture_invalid_flavor_raises(vault_root):
    with pytest.raises(ValueError, match="flavor"):
        capture("not_a_flavor", "foo", vault_root=vault_root)


def test_capture_missing_destination_raises(tmp_path):
    bare = tmp_path / "no_subdir"
    bare.mkdir()
    with pytest.raises(FileNotFoundError, match="destination directory"):
        capture("concept", "foo", vault_root=bare)


def test_capture_refuses_overwrite(vault_root):
    capture("concept", "foo", vault_root=vault_root)
    with pytest.raises(FileExistsError, match="already exists"):
        capture("concept", "foo", vault_root=vault_root)


def test_capture_force_overwrites_existing(vault_root):
    first = capture("concept", "foo", vault_root=vault_root)
    first.path.write_text("garbage\n", encoding="utf-8")
    capture("concept", "foo", vault_root=vault_root, force=True)
    text = first.path.read_text(encoding="utf-8")
    assert "garbage" not in text
    assert "---" in text  # frontmatter restored


@pytest.mark.parametrize("flavor", sorted(REGISTRY))
def test_each_flavor_produces_validator_clean_note(flavor, vault_root):
    """Every captured note must validate without ERRORs (warnings allowed)."""
    result = capture(flavor, "test_capture_smoke", vault_root=vault_root)
    issues = validate(result.path)
    errors = [i for i in issues if i.severity is Severity.ERROR]
    assert not errors, (
        f"capture('{flavor}') produced ERROR-level issues:\n"
        + "\n".join(f"  {e}" for e in errors)
    )


@pytest.mark.parametrize("flavor", sorted(REGISTRY))
def test_each_flavor_lands_at_registered_destination(flavor, vault_root):
    spec = get_spec(flavor)
    result = capture(flavor, "x_dest", vault_root=vault_root)
    assert result.path.parent == vault_root / spec.destination
    assert result.path.name == f"{spec.filename_prefix}x_dest.md"
