"""Wave 3 smoke — pipeline scheduler.

Covers:
  - per_leaf: one invocation per leaf, outputs accumulate as a list.
  - corpus_wide: one invocation, output is a single dict.
  - INFRA: skipped entirely.
  - Upstream flow: step 2 reads step 1's output_key.
  - Synthetic single leaf when leaves=None.
  - Trace JSON written to runs_dir with expected fields.
  - error_count surfaces step failures.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.composer import (
    MockBackend,
    RunResult,
    compile_skill,
    run_pipeline,
)


_CANONICAL_CORPUS = textwrap.dedent(
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
    pipeline_metadata: ./skill_corpus.pipeline.yaml
    ---

    # Corpus

    ## Step 1: produce <!-- :: section_id = step_1 :: -->

    PRODUCE step.

    ## Step 2: consume <!-- :: section_id = step_2 :: -->

    CONSUME upstream {{upstream.produced}}.
    """
)


_SIDECAR_CORPUS = textwrap.dedent(
    """\
    version: "1.0"
    pipeline:
      - section_id: step_1
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        prompt_template: "PRODUCE."
        output_key: produced
      - section_id: step_2
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: [step_1]
        materializer: no_op
        prompt_template: "CONSUME."
    """
)


_CANONICAL_PER_LEAF = textwrap.dedent(
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
    pipeline_metadata: ./skill_perleaf.pipeline.yaml
    ---

    # Per-leaf

    ## Step 1: rate <!-- :: section_id = step_1 :: -->

    Rate leaf {{leaf.id}}.
    """
)


_SIDECAR_PER_LEAF = textwrap.dedent(
    """\
    version: "1.0"
    pipeline:
      - section_id: step_1
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: no_op
        prompt_template: "Rate."
        output_key: rating
    """
)


_CANONICAL_INFRA = textwrap.dedent(
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
    pipeline_metadata: ./skill_infra.pipeline.yaml
    ---

    # Mixed

    ## Step 1: setup <!-- :: section_id = step_1 :: -->

    INFRA setup.

    ## Step 2: real <!-- :: section_id = step_2 :: -->

    Real CORE work.
    """
)


_SIDECAR_INFRA = textwrap.dedent(
    """\
    version: "1.0"
    pipeline:
      - section_id: step_1
        role: INFRA
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        prompt_template: "Setup."
      - section_id: step_2
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        prompt_template: "Work."
    """
)


def _compile(tmp_path: Path, name: str, canonical: str, sidecar: str):
    skill = tmp_path / f"{name}.md"
    skill.write_text(canonical, encoding="utf-8")
    (tmp_path / f"{name}.pipeline.yaml").write_text(sidecar, encoding="utf-8")
    return compile_skill(skill)


def test_run_pipeline_corpus_wide(tmp_path: Path) -> None:
    compiled = _compile(tmp_path, "skill_corpus", _CANONICAL_CORPUS, _SIDECAR_CORPUS)
    backend = MockBackend(
        responses={
            "PRODUCE": '{"produced": [1, 2, 3]}',
            "CONSUME": '{"consumed": true}',
        }
    )
    run = run_pipeline(
        compiled,
        leaves=None,
        backend=backend,
        vault_root=tmp_path / "vault",
    )
    assert isinstance(run, RunResult)
    assert run.error_count == 0
    assert len(run.step_results) == 2
    assert all(r.error is None for r in run.step_results)


def test_run_pipeline_corpus_wide_upstream_flow(tmp_path: Path) -> None:
    compiled = _compile(tmp_path, "skill_corpus", _CANONICAL_CORPUS, _SIDECAR_CORPUS)
    backend = MockBackend(
        responses={
            "PRODUCE": '{"produced": [1, 2, 3]}',
            "CONSUME": '{"consumed": true}',
        }
    )
    run_pipeline(
        compiled,
        leaves=None,
        backend=backend,
        vault_root=tmp_path / "vault",
    )
    # Step 2's prompt should have seen step 1's output via {{upstream.produced}}.
    consume_call = next(c for c in backend.calls if "CONSUME" in c.user_prompt)
    # upstream stores the full structured dict; JSON pretty-prints it with newlines.
    assert "produced" in consume_call.user_prompt
    assert "1" in consume_call.user_prompt and "2" in consume_call.user_prompt


def test_run_pipeline_per_leaf_runs_per_leaf(tmp_path: Path) -> None:
    compiled = _compile(
        tmp_path, "skill_perleaf", _CANONICAL_PER_LEAF, _SIDECAR_PER_LEAF
    )
    backend = MockBackend(default='{"rating": 5}')
    run = run_pipeline(
        compiled,
        leaves=[{"id": "a"}, {"id": "b"}, {"id": "c"}],
        backend=backend,
        vault_root=tmp_path / "vault",
    )
    # 3 leaves × 1 step = 3 invocations.
    assert len(run.step_results) == 3
    assert run.error_count == 0
    # Each leaf saw a distinct prompt.
    prompts = [c.user_prompt for c in backend.calls]
    assert any("a" in p for p in prompts)
    assert any("b" in p for p in prompts)
    assert any("c" in p for p in prompts)


def test_run_pipeline_synthetic_leaf_when_none(tmp_path: Path) -> None:
    compiled = _compile(tmp_path, "skill_corpus", _CANONICAL_CORPUS, _SIDECAR_CORPUS)
    backend = MockBackend(default='{"x": 1}')
    run = run_pipeline(
        compiled,
        leaves=None,
        backend=backend,
        vault_root=tmp_path / "vault",
    )
    assert len(run.leaves) == 1
    assert run.leaves[0]["_id"] == "corpus"


def test_run_pipeline_skips_infra(tmp_path: Path) -> None:
    compiled = _compile(tmp_path, "skill_infra", _CANONICAL_INFRA, _SIDECAR_INFRA)
    backend = MockBackend(default="{}")
    run = run_pipeline(
        compiled,
        leaves=None,
        backend=backend,
        vault_root=tmp_path / "vault",
    )
    # Only step_2 (CORE) ran; step_1 (INFRA) skipped.
    section_ids = [r.section_id for r in run.step_results]
    assert section_ids == ["step_2"]
    # Backend was called exactly once.
    assert len(backend.calls) == 1


def test_run_pipeline_writes_trace(tmp_path: Path) -> None:
    compiled = _compile(tmp_path, "skill_corpus", _CANONICAL_CORPUS, _SIDECAR_CORPUS)
    backend = MockBackend(default='{"produced": []}')
    runs_dir = tmp_path / "runs"
    run = run_pipeline(
        compiled,
        leaves=None,
        backend=backend,
        vault_root=tmp_path / "vault",
        runs_dir=runs_dir,
    )
    assert run.trace_path is not None
    assert run.trace_path.exists()
    payload = json.loads(run.trace_path.read_text(encoding="utf-8"))
    assert payload["skill_name"] == "skill_corpus"
    assert payload["error_count"] == 0
    assert payload["step_invocation_count"] == 2
    assert "step_results" in payload
    # Trace path is filesystem-safe (no colons).
    assert ":" not in run.trace_path.name


def test_run_pipeline_no_trace_when_runs_dir_none(tmp_path: Path) -> None:
    compiled = _compile(tmp_path, "skill_corpus", _CANONICAL_CORPUS, _SIDECAR_CORPUS)
    backend = MockBackend(default='{"produced": []}')
    run = run_pipeline(
        compiled,
        leaves=None,
        backend=backend,
        vault_root=tmp_path / "vault",
        runs_dir=None,
    )
    assert run.trace_path is None


def test_run_pipeline_dry_run_no_files_written(tmp_path: Path) -> None:
    compiled = _compile(tmp_path, "skill_corpus", _CANONICAL_CORPUS, _SIDECAR_CORPUS)
    backend = MockBackend(default='{"produced": []}')
    run = run_pipeline(
        compiled,
        leaves=None,
        backend=backend,
        vault_root=tmp_path / "vault",
        dry_run=True,
    )
    assert run.error_count == 0
    for r in run.step_results:
        assert r.materialized.files_written == ()
        assert r.materialized.files_applied == ()
