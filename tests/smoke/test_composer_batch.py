"""Wave 5a smoke — multi-job batch runner.

Covers:
  - Sequential + parallel execution paths.
  - Resume via existing result file.
  - Failure capture (compile error → status="failed").
  - Result file format.
  - Empty jobs list / single job edge cases.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path


from tessellum.composer import (
    BatchJob,
    BatchResult,
    MockBackend,
    run_batch,
)


_CANONICAL = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - skill
    keywords:
      - alpha
      - beta
      - gamma
    topics:
      - X
      - Y
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    pipeline_metadata: ./{name}.pipeline.yaml
    ---

    # {name}

    ## Step 1 <!-- :: section_id = step_1 :: -->

    Body.
    """
)


_SIDECAR = textwrap.dedent(
    """\
    version: "1.0"
    pipeline:
      - section_id: step_1
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        prompt_template: "Hi."
        output_key: out
    """
)


def _make_skill(tmp_path: Path, name: str) -> Path:
    skill = tmp_path / f"{name}.md"
    skill.write_text(_CANONICAL.format(name=name), encoding="utf-8")
    (tmp_path / f"{name}.pipeline.yaml").write_text(_SIDECAR, encoding="utf-8")
    return skill


def test_run_batch_sequential(tmp_path: Path) -> None:
    s1 = _make_skill(tmp_path, "skill_a")
    s2 = _make_skill(tmp_path, "skill_b")
    runs_dir = tmp_path / "runs"
    backend = MockBackend(default='{"out": 1}')
    jobs = [
        BatchJob(job_id="job_a", skill_path=s1, vault_root=tmp_path, runs_dir=runs_dir),
        BatchJob(job_id="job_b", skill_path=s2, vault_root=tmp_path, runs_dir=runs_dir),
    ]
    result = run_batch(jobs, backend=backend, parallelism=1)
    assert isinstance(result, BatchResult)
    assert len(result.completed) == 2
    assert len(result.failed) == 0
    assert {j.job_id for j in result.jobs} == {"job_a", "job_b"}


def test_run_batch_parallel(tmp_path: Path) -> None:
    skills = [_make_skill(tmp_path, f"skill_{i}") for i in range(5)]
    runs_dir = tmp_path / "runs"
    backend = MockBackend(default='{"out": 1}')
    jobs = [
        BatchJob(
            job_id=f"job_{i}",
            skill_path=s,
            vault_root=tmp_path,
            runs_dir=runs_dir,
        )
        for i, s in enumerate(skills)
    ]
    result = run_batch(jobs, backend=backend, parallelism=4)
    assert len(result.completed) == 5
    # Order is preserved in the returned list.
    assert [j.job_id for j in result.jobs] == [f"job_{i}" for i in range(5)]


def test_run_batch_writes_result_file(tmp_path: Path) -> None:
    s = _make_skill(tmp_path, "skill_a")
    runs_dir = tmp_path / "runs"
    backend = MockBackend(default='{"out": 1}')
    jobs = [
        BatchJob(job_id="job_x", skill_path=s, vault_root=tmp_path, runs_dir=runs_dir),
    ]
    result = run_batch(jobs, backend=backend, parallelism=1)
    job_result = result.jobs[0]
    assert job_result.status == "completed"
    assert job_result.result_path is not None
    payload = json.loads(job_result.result_path.read_text(encoding="utf-8"))
    assert payload["job_id"] == "job_x"
    assert payload["skill_name"] == "skill_a"
    assert payload["error_count"] == 0


def test_run_batch_resume_skips_existing(tmp_path: Path) -> None:
    s = _make_skill(tmp_path, "skill_a")
    runs_dir = tmp_path / "runs"
    backend = MockBackend(default='{"out": 1}')
    job = BatchJob(
        job_id="job_x", skill_path=s, vault_root=tmp_path, runs_dir=runs_dir
    )
    # First run.
    result1 = run_batch([job], backend=backend, parallelism=1)
    assert result1.jobs[0].status == "completed"
    # Mock backend's call count should now be 1.
    assert len(backend.calls) == 1

    # Second run with resume (default) — should skip without dispatching.
    result2 = run_batch([job], backend=backend, parallelism=1)
    assert result2.jobs[0].status == "skipped"
    assert result2.jobs[0].previous_payload is not None
    assert result2.jobs[0].previous_payload["job_id"] == "job_x"
    # Backend was NOT called again.
    assert len(backend.calls) == 1


def test_run_batch_no_resume_forces_rerun(tmp_path: Path) -> None:
    s = _make_skill(tmp_path, "skill_a")
    runs_dir = tmp_path / "runs"
    backend = MockBackend(default='{"out": 1}')
    job = BatchJob(
        job_id="job_x", skill_path=s, vault_root=tmp_path, runs_dir=runs_dir
    )
    run_batch([job], backend=backend, parallelism=1)
    assert len(backend.calls) == 1
    # resume=False → re-runs.
    result = run_batch([job], backend=backend, parallelism=1, resume=False)
    assert result.jobs[0].status == "completed"
    assert len(backend.calls) == 2


def test_run_batch_compile_failure_captured(tmp_path: Path) -> None:
    """A non-existent skill path → compile fails → status=failed (not raised)."""
    runs_dir = tmp_path / "runs"
    backend = MockBackend(default="{}")
    jobs = [
        BatchJob(
            job_id="bad_job",
            skill_path=tmp_path / "nope.md",
            vault_root=tmp_path,
            runs_dir=runs_dir,
        )
    ]
    result = run_batch(jobs, backend=backend, parallelism=1)
    assert result.jobs[0].status == "failed"
    assert result.jobs[0].error is not None
    assert len(result.failed) == 1


def test_run_batch_empty_jobs(tmp_path: Path) -> None:
    backend = MockBackend()
    result = run_batch([], backend=backend, parallelism=1)
    assert result.jobs == ()
    assert result.completed == ()
    assert result.failed == ()


def test_run_batch_dry_run_passthrough(tmp_path: Path) -> None:
    s = _make_skill(tmp_path, "skill_a")
    runs_dir = tmp_path / "runs"
    backend = MockBackend(default='{"out": 1}')
    jobs = [
        BatchJob(job_id="j", skill_path=s, vault_root=tmp_path, runs_dir=runs_dir),
    ]
    result = run_batch(jobs, backend=backend, parallelism=1, dry_run=True)
    assert result.jobs[0].status == "completed"
    for r in result.jobs[0].run_result.step_results:
        assert r.materialized.files_written == ()


def test_run_batch_corrupt_result_file_marked_failed(tmp_path: Path) -> None:
    s = _make_skill(tmp_path, "skill_a")
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    # Pre-seed a corrupt result file.
    (runs_dir / "job_x.result.json").write_text("not valid json", encoding="utf-8")
    backend = MockBackend(default='{"out": 1}')
    jobs = [
        BatchJob(job_id="job_x", skill_path=s, vault_root=tmp_path, runs_dir=runs_dir),
    ]
    result = run_batch(jobs, backend=backend, parallelism=1)
    assert result.jobs[0].status == "failed"
    assert result.jobs[0].error is not None
    assert "unreadable" in result.jobs[0].error.lower()
