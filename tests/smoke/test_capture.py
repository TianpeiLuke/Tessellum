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
    assert len(flavors) == 14
    assert flavors == sorted(flavors)
    expected = {
        "concept", "procedure", "skill", "model",
        "argument", "counter_argument", "hypothesis",
        "empirical_observation", "experiment",
        "navigation", "entry_point", "acronym_glossary",
        "code_snippet", "code_repo",
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


# ── Paired sidecar emission for skill flavor (Wave 1b) ────────────────────


def test_capture_skill_emits_paired_sidecar(vault_root):
    result = capture("skill", "my_skill", vault_root=vault_root)
    canonical = vault_root / "resources/skills/skill_my_skill.md"
    sidecar = vault_root / "resources/skills/skill_my_skill.pipeline.yaml"
    assert result.path == canonical
    assert result.sidecar_path == sidecar
    assert canonical.is_file()
    assert sidecar.is_file()


def test_capture_skill_canonical_has_pipeline_metadata_pointing_at_sidecar(
    vault_root,
):
    result = capture("skill", "my_skill", vault_root=vault_root)
    text = result.path.read_text(encoding="utf-8")
    assert "pipeline_metadata: ./skill_my_skill.pipeline.yaml" in text
    assert "pipeline_metadata: none" not in text


def test_capture_skill_sidecar_is_schema_valid_pipeline(vault_root):
    """The auto-emitted sidecar must validate clean against load_pipeline."""
    from tessellum.composer import load_pipeline

    result = capture("skill", "my_skill", vault_root=vault_root)
    pipeline = load_pipeline(result.path)
    assert pipeline is not None
    assert len(pipeline.pipeline) >= 1
    # The starter declares step_1_first_action which matches template_skill.md's
    # first anchored step.
    assert pipeline.pipeline[0].section_id == "step_1_first_action"
    assert pipeline.pipeline[0].role == "CORE"


def test_capture_non_skill_flavor_has_no_sidecar(vault_root):
    result = capture("concept", "foo", vault_root=vault_root)
    assert result.sidecar_path is None


def test_capture_skill_force_overwrites_both_files(vault_root):
    first = capture("skill", "my_skill", vault_root=vault_root)
    first.path.write_text("garbage\n", encoding="utf-8")
    first.sidecar_path.write_text("garbage\n", encoding="utf-8")  # type: ignore[union-attr]
    capture("skill", "my_skill", vault_root=vault_root, force=True)
    assert "garbage" not in first.path.read_text(encoding="utf-8")
    assert "garbage" not in first.sidecar_path.read_text(encoding="utf-8")  # type: ignore[union-attr]


def test_capture_skill_refuses_overwrite_when_sidecar_exists(vault_root):
    capture("skill", "my_skill", vault_root=vault_root)
    with pytest.raises(FileExistsError, match="already exists"):
        capture("skill", "my_skill", vault_root=vault_root)


# ── bb_schema_version auto-population (Phase B.4) ──────────────────────────


def test_capture_writes_bb_schema_version_frontmatter(vault_root):
    """New captures must record `bb_schema_version` per D8 frozen-at-creation."""
    from tessellum.bb.types import BB_SCHEMA_VERSION

    result = capture("argument", "my_argument", vault_root=vault_root)
    text = result.path.read_text(encoding="utf-8")
    assert f"bb_schema_version: {BB_SCHEMA_VERSION}" in text


def test_capture_bb_schema_version_appears_after_building_block(vault_root):
    """Field is placed right after `building_block:` for visual grouping."""
    result = capture("concept", "my_concept", vault_root=vault_root)
    text = result.path.read_text(encoding="utf-8")
    lines = text.splitlines()
    # Find indices
    bb_idx = next(i for i, ln in enumerate(lines) if ln.startswith("building_block:"))
    ver_idx = next(i for i, ln in enumerate(lines) if ln.startswith("bb_schema_version:"))
    assert ver_idx == bb_idx + 1


def test_capture_bb_schema_version_across_all_flavors(vault_root):
    """Every flavor records bb_schema_version (sanity over all templates)."""
    from tessellum.bb.types import BB_SCHEMA_VERSION

    flavors_with_bb = [
        f for f in list_flavors() if get_spec(f).bb_type
    ]
    for flavor in flavors_with_bb:
        result = capture(flavor, f"check_{flavor}", vault_root=vault_root)
        text = result.path.read_text(encoding="utf-8")
        assert (
            f"bb_schema_version: {BB_SCHEMA_VERSION}" in text
        ), f"{flavor} did not record bb_schema_version"


def test_capture_does_not_overwrite_explicit_bb_schema_version(vault_root, tmp_path, monkeypatch):
    """If the template already declares bb_schema_version, capture leaves it alone."""
    # Build a fake template with an explicit version.
    fake_templates = tmp_path / "fake_templates"
    fake_templates.mkdir()
    # Use the real argument template as a base but inject bb_schema_version explicitly
    from tessellum.data import templates_dir

    base_text = (templates_dir() / "template_argument.md").read_text(encoding="utf-8")
    base_text_with_pinned = base_text.replace(
        "building_block: argument",
        "building_block: argument\nbb_schema_version: 999",
    )
    (fake_templates / "template_argument.md").write_text(base_text_with_pinned)

    # Monkey-patch templates_dir to point at our fake dir
    import tessellum.capture as capture_mod

    monkeypatch.setattr(capture_mod, "templates_dir", lambda: fake_templates)

    result = capture("argument", "pinned_arg", vault_root=vault_root)
    text = result.path.read_text(encoding="utf-8")
    assert "bb_schema_version: 999" in text
    # The current BB_SCHEMA_VERSION should NOT appear (since the template
    # already had one, we did not inject)
    from tessellum.bb.types import BB_SCHEMA_VERSION

    if BB_SCHEMA_VERSION != 999:
        # Count occurrences — there should be exactly 1 (the pinned one)
        assert text.count("bb_schema_version:") == 1
