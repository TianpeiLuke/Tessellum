from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from tessellum.runtime.admission import AdmissionError, admit_path
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.routing import LANE_HINTS, route_lane
from tessellum.runtime.store import RuntimeStore


def _paths(root: Path) -> RuntimePaths:
    paths = RuntimePaths.discover(root)
    paths.ensure_runtime_dirs()
    paths.inbox.mkdir(parents=True)
    return paths


def test_admission_spools_before_durable_job_and_deduplicates(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    source = paths.inbox / "papers" / "paper.md"
    source.parent.mkdir()
    source.write_text("evidence", encoding="utf-8")
    store = RuntimeStore.open(paths.db)
    first, created = admit_path(source, paths=paths, store=store)
    second, duplicate = admit_path(source, paths=paths, store=store)
    assert created is True
    assert duplicate is False
    assert second.job_id == first.job_id
    assert paths.spool_path(first.request.payload_ref).read_text() == "evidence"


def test_identical_replacement_is_a_new_source_event(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    source = paths.inbox / "papers" / "paper.md"
    source.parent.mkdir()
    source.write_text("same bytes", encoding="utf-8")
    store = RuntimeStore.open(paths.db)
    first, _ = admit_path(source, paths=paths, store=store)

    source.unlink()
    source.write_text("same bytes", encoding="utf-8")
    second, created = admit_path(source, paths=paths, store=store)

    assert created is True
    assert second.job_id != first.job_id
    assert second.request.payload_ref == first.request.payload_ref


def test_admission_rejects_path_outside_inbox(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    source = tmp_path / "outside.md"
    source.write_text("no", encoding="utf-8")
    with pytest.raises(AdmissionError):
        admit_path(source, paths=paths, store=RuntimeStore.open(paths.db))


def test_admission_rejects_corrupt_existing_spool_file(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    source = paths.inbox / "papers" / "paper.md"
    source.parent.mkdir()
    source.write_text("evidence", encoding="utf-8")
    digest = hashlib.sha256(b"evidence").hexdigest()
    spool = paths.spool_path(f"sha256:{digest}")
    spool.parent.mkdir(parents=True)
    spool.write_text("corrupt", encoding="utf-8")

    with pytest.raises(AdmissionError, match="spool digest mismatch"):
        admit_path(source, paths=paths, store=RuntimeStore.open(paths.db))


def test_admission_rejects_directory_at_spool_path(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    source = paths.inbox / "papers" / "paper.md"
    source.parent.mkdir()
    source.write_text("evidence", encoding="utf-8")
    digest = hashlib.sha256(b"evidence").hexdigest()
    spool = paths.spool_path(f"sha256:{digest}")
    spool.mkdir(parents=True)

    with pytest.raises(AdmissionError, match="spool object is not a regular file"):
        admit_path(source, paths=paths, store=RuntimeStore.open(paths.db))


def test_admission_rejects_symlink_at_spool_path(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    source = paths.inbox / "papers" / "paper.md"
    source.parent.mkdir()
    source.write_text("evidence", encoding="utf-8")
    digest = hashlib.sha256(b"evidence").hexdigest()
    spool = paths.spool_path(f"sha256:{digest}")
    spool.parent.mkdir(parents=True)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.write_text("evidence", encoding="utf-8")
    spool.symlink_to(elsewhere)

    with pytest.raises(AdmissionError, match="spool object is not a regular file"):
        admit_path(source, paths=paths, store=RuntimeStore.open(paths.db))


def test_admission_rejects_symlink_without_touching_target(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    lane = paths.inbox / "papers"
    lane.mkdir()
    target = lane / "target.md"
    target.write_text("keep", encoding="utf-8")
    source = lane / "linked.md"
    source.symlink_to(target)

    with pytest.raises(AdmissionError, match="ineligible inbox source"):
        admit_path(source, paths=paths, store=RuntimeStore.open(paths.db))

    assert target.read_text(encoding="utf-8") == "keep"
    assert source.is_symlink()


def test_all_existing_lanes_route_to_pinned_native_digestion(tmp_path: Path) -> None:
    skills = tmp_path / "skills"
    skills.mkdir()
    names = (
        "skill_tessellum_plan_digestion",
        "skill_tessellum_augment_digestion_plan",
        "skill_tessellum_review_digestion_plan",
        "skill_tessellum_execute_digestion_plan",
    )
    for name in names:
        (skills / f"{name}.md").write_text(name, encoding="utf-8")
    for lane in LANE_HINTS:
        route = route_lane(lane, skills_dir=skills)
        assert route.capability == "native_digestion"
        assert len(route.skill_digest) == 64


def test_scaffolded_direct_vault_contains_routable_runtime_skills(
    tmp_path: Path,
) -> None:
    from tessellum.init import scaffold

    scaffold(tmp_path)
    paths = RuntimePaths.discover(tmp_path)

    assert paths.vault == tmp_path.resolve()
    assert route_lane("papers", skills_dir=paths.skills).capability == "native_digestion"
