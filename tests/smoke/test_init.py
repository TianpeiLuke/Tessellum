"""Smoke tests for tessellum.init.scaffold()."""

from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.capture import REGISTRY, capture
from tessellum.format import Severity, validate
from tessellum.init import ScaffoldResult, scaffold


def test_scaffold_creates_target_directory(tmp_path):
    target = tmp_path / "my-vault"
    result = scaffold(target)
    assert isinstance(result, ScaffoldResult)
    assert result.target == target.resolve()
    assert target.is_dir()


def test_scaffold_creates_para_top_level_dirs(tmp_path):
    target = tmp_path / "v"
    scaffold(target)
    for d in ("0_entry_points", "projects", "areas", "archives"):
        assert (target / d).is_dir(), f"missing top-level dir: {d}"


def test_scaffold_creates_automatic_runtime_inbox_lanes(tmp_path):
    target = tmp_path / "v"
    scaffold(target)
    for lane in (
        "manual_retrieved",
        "papers",
        "general",
        "latex",
        "flash",
        "book",
        "podcast",
        "sops",
    ):
        assert (target / "inbox" / lane).is_dir()


def test_scaffold_creates_destination_dir_for_every_flavor(tmp_path):
    target = tmp_path / "v"
    scaffold(target)
    for spec in REGISTRY.values():
        assert (target / spec.destination).is_dir(), (
            f"missing destination for flavor {spec.flavor}: {spec.destination}"
        )


def test_scaffold_copies_all_templates(tmp_path):
    target = tmp_path / "v"
    scaffold(target)
    templates = list((target / "resources/templates").glob("template_*.md"))
    assert len(templates) >= 13, f"expected ≥ 13 templates, got {len(templates)}"


def test_scaffold_copies_single_file_skill_template(tmp_path):
    """The scaffolded vault ships the single-file skill template, and that
    template carries its pipeline scaffolding inline: a step section with a
    ``section_id`` anchor + a leading ```yaml``` contract block. This is the
    single-file replacement for the old ``template_skill.pipeline.yaml``
    starter sidecar (which no longer exists)."""
    target = tmp_path / "v"
    scaffold(target)
    tmpl = target / "resources/templates/template_skill.md"
    assert tmpl.is_file()
    text = tmpl.read_text(encoding="utf-8")
    # A pipeline-step section carries a section_id anchor ...
    assert "<!-- :: section_id =" in text
    # ... followed by a leading ```yaml``` contract block whose required
    # fields (role / depends_on) declare the typed step contract inline.
    assert "role: CORE" in text
    assert "depends_on:" in text
    # No separate sidecar file is shipped any more.
    assert not (target / "resources/templates/template_skill.pipeline.yaml").exists()


def test_scaffold_copies_seed_term_building_block(tmp_path):
    target = tmp_path / "v"
    scaffold(target)
    seed = target / "resources/term_dictionary/term_building_block.md"
    assert seed.is_file()
    text = seed.read_text(encoding="utf-8")
    assert text.startswith("---\n")  # has YAML frontmatter
    assert "Building Block" in text


def test_scaffold_writes_master_toc(tmp_path):
    target = tmp_path / "my-cool-vault"
    scaffold(target)
    toc = target / "0_entry_points/entry_master_toc.md"
    assert toc.is_file()
    text = toc.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "my-cool-vault" in text
    assert "tessellum capture" in text  # quick-start guidance


def test_scaffold_writes_readme(tmp_path):
    target = tmp_path / "v"
    scaffold(target)
    readme = target / "README.md"
    assert readme.is_file()
    text = readme.read_text(encoding="utf-8")
    assert "Tessellum" in text


def test_scaffolded_vault_validates_with_no_errors(tmp_path):
    """Master TOC + seed term + templates should produce 0 ERROR-severity issues.
    Warnings are allowed (templates have placeholder links → LINK-003)."""
    target = tmp_path / "v"
    scaffold(target)

    # Validate every markdown file in the vault
    md_files = list(target.rglob("*.md"))
    error_files: list[Path] = []
    for f in md_files:
        # Skip non-note files (README, etc. — same convention as the CLI skip list)
        if f.name in {"README.md", "CHANGELOG.md", "CONTRIBUTING.md"}:
            continue
        issues = validate(f)
        errors = [i for i in issues if i.severity is Severity.ERROR]
        if errors:
            error_files.append(f)
    assert not error_files, (
        "scaffolded vault has files with ERROR-severity issues:\n"
        + "\n".join(f"  {f}" for f in error_files)
    )


def test_scaffold_into_empty_existing_dir_is_ok(tmp_path):
    target = tmp_path / "empty"
    target.mkdir()
    scaffold(target)
    assert (target / "0_entry_points").is_dir()


def test_scaffold_refuses_existing_non_empty_dir(tmp_path):
    target = tmp_path / "v"
    target.mkdir()
    (target / "stale.txt").write_text("x")
    with pytest.raises(FileExistsError, match="non-empty"):
        scaffold(target)


def test_scaffold_force_into_non_empty_dir(tmp_path):
    target = tmp_path / "v"
    target.mkdir()
    (target / "stale.txt").write_text("x")
    scaffold(target, force=True)
    # Pre-existing file is preserved.
    assert (target / "stale.txt").is_file()
    # Scaffold paths are populated.
    assert (target / "0_entry_points/entry_master_toc.md").is_file()


def test_scaffold_target_is_file_raises(tmp_path):
    target = tmp_path / "vfile"
    target.write_text("not a directory")
    with pytest.raises(FileExistsError, match="is a file"):
        scaffold(target)


def test_capture_works_against_scaffolded_vault(tmp_path):
    """End-to-end: scaffold, then capture into the new vault."""
    target = tmp_path / "v"
    scaffold(target)
    result = capture("concept", "test_topic", vault_root=target)
    assert result.path == target / "resources/term_dictionary/term_test_topic.md"
    assert result.path.is_file()


def test_capture_skill_works_against_scaffolded_vault(tmp_path):
    """Single-file skill emission works against a scaffolded vault: capture
    writes ONE canonical ``.md`` (no ``.pipeline.yaml`` sidecar) whose inline
    contract blocks compile to a valid pipeline."""
    from tessellum.composer import load_pipeline

    target = tmp_path / "v"
    scaffold(target)
    result = capture("skill", "test_skill", vault_root=target)
    canonical = target / "resources/skills/skill_test_skill.md"
    sidecar = target / "resources/skills/skill_test_skill.pipeline.yaml"
    assert canonical.is_file()
    assert result.path == canonical
    # Single-file format: no sidecar file, and sidecar_path stays None.
    assert not sidecar.exists()
    assert result.sidecar_path is None
    # The inline contract block(s) compile to a valid pipeline.
    pipeline = load_pipeline(canonical)
    assert pipeline is not None
    assert len(pipeline.pipeline) >= 1
    assert pipeline.pipeline[0].section_id == "step_1_first_action"
