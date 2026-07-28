"""A2 (FZ 20k9c1a1a1b7c2k1a) — the durable working store + ArtifactRef deref.

Pins the pivot's contract:

- :class:`ArtifactRef` round-trip + LOUD integrity failure;
- :func:`_build_artifact_store` durable mode — files written atomically,
  refs returned, **prompt text byte-identical** to the in-RAM store (the
  store serializes with the executor's own stringifier);
- fail-soft durable WRITE (unwritable dir → in-RAM values, run correctness
  preserved) vs fail-loud corrupted READ;
- the end-to-end seam: ``run_digestion_pipeline(durable_artifact_dir=…)``
  completes with artifacts paged to disk, result equal to the in-RAM run;
- A2.4-lite: the compiler surfaces unmodeled large runtime payloads.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.composer import run_digestion_pipeline
from tessellum.composer.contracts import ArtifactIntegrityError, ArtifactRef
from tessellum.composer.digestion import _build_artifact_store
from tessellum.composer.executor import _resolve_placeholders

from test_composer_episodic_hardening import _SOURCE, _mock, _synthetic_pipeline


# ── ArtifactRef ──────────────────────────────────────────────────────────────


def test_artifact_ref_roundtrip_and_integrity(tmp_path: Path) -> None:
    store = _build_artifact_store({"plan_text": "# Plan body"}, tmp_path / "arts")
    ref = store["plan_text"]
    assert isinstance(ref, ArtifactRef)
    assert ref.read_text() == "# Plan body"
    assert ref.size == len(b"# Plan body")
    # Corrupt the durable bytes → the deref fails LOUD, never silently.
    ref.path.write_text("tampered", encoding="utf-8")
    with pytest.raises(ArtifactIntegrityError):
        ref.read_text()


def test_durable_store_prompt_text_byte_identical(tmp_path: Path) -> None:
    doc = {
        "plan_text": "# Plan\n\nbody",
        "planned_notes": [{"filename": "a.md"}, {"filename": "b.md"}],
    }
    ram = _build_artifact_store(doc)
    durable = _build_artifact_store(doc, tmp_path / "arts")
    template = "PLAN: {{artifact.plan_text}} NOTES: {{artifact.planned_notes}}"
    ram_prompt = _resolve_placeholders(template, leaf={}, upstream={}, artifacts=ram)
    dur_prompt = _resolve_placeholders(template, leaf={}, upstream={}, artifacts=durable)
    assert ram_prompt == dur_prompt


def test_durable_write_fails_soft_to_values() -> None:
    doc = {"plan_text": "# P"}
    store = _build_artifact_store(doc, Path("/nonexistent-root/arts"))
    # Correctness preserved: the in-RAM value is kept, not a broken ref.
    assert store["plan_text"] == "# P"


# ── end-to-end seam ──────────────────────────────────────────────────────────


def test_pipeline_with_durable_artifacts(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    arts = tmp_path / "run" / "artifacts"
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf=dict(_SOURCE),
        backend=_mock(),
        vault_root=tmp_path / "vault",
        durable_artifact_dir=arts,
    )
    assert result.completed
    # The of-record plan body was paged to the durable working store.
    assert (arts / "plan_text").read_text().startswith("# Plan")
    assert not list(arts.glob("*.tmp"))


def test_pipeline_without_flag_stays_in_ram(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf=dict(_SOURCE),
        backend=_mock(),
        vault_root=tmp_path / "vault",
    )
    assert result.completed
    assert not list(tmp_path.rglob("artifacts"))


# ── A2.4-lite compiler warning ───────────────────────────────────────────────


def test_compiler_warns_on_unmodeled_large_payload(tmp_path: Path) -> None:
    from tessellum.composer import compile_skill

    skill = tmp_path / "skill_payload.md"
    skill.write_text(
        "---\n"
        "tags:\n  - resource\n  - skill\n"
        "keywords:\n  - alpha\n  - beta\n  - gamma\n"
        "topics:\n  - Digestion\n"
        "language: markdown\n"
        "date of note: 2026-07-28\n"
        "status: active\n"
        "building_block: procedure\n"
        "access_control_group: [\"general\"]\n"
        "---\n\n"
        "# skill_payload\n\n"
        "## Do it <!-- :: section_id = step_1 :: -->\n\n"
        "```yaml\n"
        "role: CORE\n"
        "aggregation: corpus_wide\n"
        "batchable: false\n"
        "depends_on: []\n"
        "materializer: no_op\n"
        "output_key: out\n"
        "expected_output_schema:\n"
        "  type: object\n"
        "  required: [ok]\n"
        "```\n\n"
        "Read {{artifact.plan_text}} and the source {{leaf.members}}.\n",
        encoding="utf-8",
    )
    # OPT-IN (review finding 3): default compiles stay byte-identical — the
    # shipped review skill's {{artifact.plan_text}} reads are the PRESCRIBED
    # by-reference pattern and must not warn by default.
    assert not [
        w for w in compile_skill(skill).budget_warnings if "not modeled" in w
    ]
    compiled = compile_skill(skill, warn_unmodeled_payloads=True)
    hits = [w for w in compiled.budget_warnings if "not modeled" in w]
    assert hits and "{{artifact.plan_text}}" in hits[0] and "{{leaf.members}}" in hits[0]


def test_compiler_payload_scan_ignores_non_artifact_keys(tmp_path: Path) -> None:
    from tessellum.composer.compiler import _warn_unmodeled_payloads, compile_skill

    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    compiled = compile_skill(
        sd / "skill_tessellum_plan_digestion.md", warn_unmodeled_payloads=True
    )
    # The synthetic plan skill has no large-payload placeholders → no hits.
    assert not [w for w in compiled.budget_warnings if "not modeled" in w]
    assert _warn_unmodeled_payloads is not None


def test_shipped_skills_compile_byte_identical_by_default() -> None:
    # Review finding 3: the four REAL vault skills must emit no NEW budget
    # warnings on a default compile (the pre-A2 zero-warning state).
    from tessellum.composer import compile_skill

    skills = Path(__file__).resolve().parents[2] / "vault" / "resources" / "skills"
    for name in (
        "skill_tessellum_plan_digestion.md",
        "skill_tessellum_review_digestion_plan.md",
    ):
        compiled = compile_skill(skills / name)
        assert not [w for w in compiled.budget_warnings if "not modeled" in w], name


# ── review findings 1+2: terminal, non-tripping integrity failure ───────────


def test_integrity_failure_is_terminal_and_non_tripping(tmp_path: Path) -> None:
    """A corrupted durable artifact fails the step ONCE (no crash retries) with
    error_class='validation' — never the auth/rate_limit classes that would
    trip the P17 breaker as a fake credential wall."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    arts = tmp_path / "arts"
    store = _build_artifact_store({"plan_text": "# P"}, arts)
    (arts / "plan_text").write_text("tampered", encoding="utf-8")

    from tessellum.composer import compile_skill
    from tessellum.composer.executor import execute_step_with_retry

    compiled = compile_skill(sd / "skill_tessellum_augment_digestion_plan.md")
    step = compiled.steps[0]
    # Give the step a prompt that derefs the corrupted artifact.
    import dataclasses as _dc

    step = _dc.replace(step, prompt_section_text="Read {{artifact.plan_text}}")
    result = execute_step_with_retry(
        step,
        leaf={"_id": "corpus"},
        upstream={},
        backend=_mock(),
        vault_root=tmp_path / "vault",
        dry_run=True,
        artifacts=store,
    )
    assert result.error and "integrity" in result.error
    assert result.error_class == "validation"
    assert result.attempts == 1  # terminal on first sight — no burned retries
