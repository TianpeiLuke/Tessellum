"""A0 (FZ 20k9c1a1a1b7c2k1a) — run identity plumbing.

Pins the three A0 seams:

- :func:`tessellum.runtime.paths.new_run_id` — the canonical mint (shape,
  uniqueness, reserved-prefix safety);
- :meth:`RuntimePaths.run_dir` — the per-run root addressing + its id
  validation (no escape, no reserved-subdir collision);
- :func:`run_digestion_pipeline`'s ``run_id`` named param — hoisted identity
  surfaced on :class:`DigestionResult`, no-clobber vs the pre-A0
  ``execute_kwargs["run_id"]`` calling convention, and byte-identical
  ``None`` default.

The corpus isolation of ``run_id`` itself is pinned where it lives
(``_RUN_SCOPED_EXECUTE_KWARGS`` — re-asserted here so a refactor dropping the
key from the allowlist fails a named A0 test, not just a corpus test).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tessellum.composer import MockBackend, run_digestion_pipeline
from tessellum.composer.corpus_digestion import _RUN_SCOPED_EXECUTE_KWARGS
from tessellum.runtime.paths import RuntimePaths, new_run_id


# ── new_run_id ───────────────────────────────────────────────────────────────


def test_new_run_id_shape_and_uniqueness() -> None:
    a, b = new_run_id(), new_run_id()
    for rid in (a, b):
        assert re.fullmatch(r"run-\d{8}-\d{6}-[0-9a-f]{8}", rid), rid
    assert a != b


# ── RuntimePaths.run_dir ─────────────────────────────────────────────────────


def _paths(tmp_path: Path) -> RuntimePaths:
    return RuntimePaths.discover(tmp_path, env={})


def test_run_dir_addresses_under_runs(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    rid = new_run_id()
    assert paths.run_dir(rid) == paths.runs / rid


@pytest.mark.parametrize(
    "bad", ["", ".", "..", "a/b", "a\\b", "runtime", "composer", "dks", "eval"]
)
def test_run_dir_rejects_invalid_and_reserved_ids(tmp_path: Path, bad: str) -> None:
    with pytest.raises(ValueError):
        _paths(tmp_path).run_dir(bad)


# ── run_digestion_pipeline run_id hoist ──────────────────────────────────────
# Minimal synthetic 4-phase pipeline (the test_composer_digestion pattern,
# reduced): one no_op step per linear phase + a file-writing execute step.


def _write_phase_skill(
    skills_dir: Path,
    name: str,
    *,
    output_key: str,
    required: list[str],
    materializer: str = "no_op",
    aggregation: str = "corpus_wide",
) -> None:
    canonical = (
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
        f"# {name}\n\n"
        "## Do it <!-- :: section_id = step_1 :: -->\n\n"
        "```yaml\n"
        "role: CORE\n"
        f"aggregation: {aggregation}\n"
        "batchable: false\n"
        "depends_on: []\n"
        f"materializer: {materializer}\n"
        f"output_key: {output_key}\n"
        "expected_output_schema:\n"
        "  type: object\n"
        f"  required: [{', '.join(required)}]\n"
        "```\n\n"
        "phase\n"
    )
    (skills_dir / f"{name}.md").write_text(canonical, encoding="utf-8")


def _synthetic_pipeline(skills_dir: Path) -> None:
    _write_phase_skill(skills_dir, "skill_tessellum_plan_digestion",
                       output_key="plan_out", required=["plan_path"])
    _write_phase_skill(skills_dir, "skill_tessellum_augment_digestion_plan",
                       output_key="augment_out", required=["plan_text"])
    _write_phase_skill(skills_dir, "skill_tessellum_review_digestion_plan",
                       output_key="verdict", required=["ready"])
    _write_phase_skill(skills_dir, "skill_tessellum_execute_digestion_plan",
                       output_key="exec_out", required=["output_path", "body_markdown"],
                       materializer="body_markdown_to_file", aggregation="per_leaf")


def _mock() -> MockBackend:
    return MockBackend(default=json.dumps({
        "plan_path": "plans/plan_demo.md",
        "plan_text": "# Plan\n\nbody",
        "ready": True, "failures": [],
        "output_path": "notes/n.md", "body_markdown": "# Note\n\nbody",
        "total_notes": 1,
    }))


_SOURCE = {"id": "demo", "plan_path": "plans/plan_demo.md",
           "plan_text": "# Plan", "total_notes": 1}


def _run(tmp_path: Path, **kwargs):
    sd = tmp_path / "skills"
    sd.mkdir(exist_ok=True)
    _synthetic_pipeline(sd)
    return run_digestion_pipeline(
        skills_dir=sd,
        source_leaf=dict(_SOURCE),
        backend=_mock(),
        vault_root=tmp_path / "vault",
        **kwargs,
    )


def test_run_id_param_surfaces_on_result(tmp_path: Path) -> None:
    result = _run(tmp_path, run_id="run-20260728-000000-deadbeef")
    assert result.completed
    assert result.run_id == "run-20260728-000000-deadbeef"


def test_run_id_defaults_to_none(tmp_path: Path) -> None:
    # Byte-identical pre-A0 behaviour: no identity supplied → none surfaced.
    result = _run(tmp_path)
    assert result.completed
    assert result.run_id is None


def test_execute_kwargs_run_id_surfaces_via_legacy_convention(tmp_path: Path) -> None:
    # The pre-A0 calling convention (run_id via **execute_kwargs) still works
    # and the SURFACED identity is what the wave actually uses.
    result = _run(tmp_path, **{"run_id": "run-kwargs-wins"})
    assert result.completed
    assert result.run_id == "run-kwargs-wins"


def test_run_id_surfaced_on_early_halt(tmp_path: Path) -> None:
    # A phase error still returns a result carrying the identity.
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    bad_backend = MockBackend(default="not json at all {{{")
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf=dict(_SOURCE),
        backend=bad_backend,
        vault_root=tmp_path / "vault",
        run_id="run-early-halt",
    )
    assert not result.completed
    assert result.run_id == "run-early-halt"


# ── corpus isolation allowlist ───────────────────────────────────────────────


def test_run_id_stays_in_corpus_isolation_allowlist() -> None:
    assert "run_id" in _RUN_SCOPED_EXECUTE_KWARGS
