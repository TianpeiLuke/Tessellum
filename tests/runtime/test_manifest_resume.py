from __future__ import annotations

from pathlib import Path

from tessellum.composer.manifest import ArtifactRecord, Manifest


def test_owner_fenced_commit_and_artifact_verification(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    note = vault / "note.md"
    note.write_text("committed", encoding="utf-8")
    manifest = Manifest()
    assert manifest.claim("capture::a", "run-a", 10.0, generation=3)
    artifact = ArtifactRecord.from_path(note, vault_root=vault)
    assert not manifest.commit_success(
        "capture::a",
        run_id="stale",
        generation=3,
        plan_hash="plan",
        input_hash="input",
        capability_version="1",
        structured_output={"value": 1},
        artifacts=(artifact,),
        now=11.0,
    )
    assert manifest.commit_success(
        "capture::a",
        run_id="run-a",
        generation=3,
        plan_hash="plan",
        input_hash="input",
        capability_version="1",
        structured_output={"value": 1},
        artifacts=(artifact,),
        now=11.0,
    )
    assert manifest.verify_commit(
        "capture::a",
        vault_root=vault,
        generation=3,
        plan_hash="plan",
        input_hash="input",
        capability_version="1",
    )
    note.write_text("tampered", encoding="utf-8")
    assert not manifest.verify_commit(
        "capture::a",
        vault_root=vault,
        generation=3,
        plan_hash="plan",
        input_hash="input",
        capability_version="1",
    )
