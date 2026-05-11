"""Smoke tests for ``tessellum composer eval``."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.cli.main import main


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
    pipeline_metadata: ./skill_demo.pipeline.yaml
    ---

    # Demo

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
        prompt_template: "Run."
        output_key: out
    """
)


@pytest.fixture
def scenarios_dir(tmp_path: Path) -> Path:
    """Create a scenarios dir with one passing scenario."""
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    (tmp_path / "skill_demo.pipeline.yaml").write_text(_SIDECAR, encoding="utf-8")

    scenarios = tmp_path / "scenarios"
    scenarios.mkdir()
    (scenarios / "case_a.scenario.yaml").write_text(
        textwrap.dedent(
            """\
            name: "Case A"
            skill: ../skill_demo.md
            vault: ../vault
            expected_output_description: "A summary."
            assertions:
              - kind: no_errors
              - kind: step_count_eq
                expected: 1
            """
        ),
        encoding="utf-8",
    )
    return scenarios


def test_eval_human_output(scenarios_dir, capsys):
    code = main(["composer", "eval", str(scenarios_dir), "--judge-backend", "none"])
    assert code == 0
    out = capsys.readouterr().out
    assert "1 passed" in out
    assert "Case A" in out


def test_eval_json_output(scenarios_dir, capsys):
    code = main(
        [
            "composer",
            "eval",
            str(scenarios_dir),
            "--judge-backend",
            "none",
            "--format",
            "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["passed"] == 1
    assert payload["failed"] == 0
    assert len(payload["scenarios"]) == 1
    assert payload["scenarios"][0]["overall_passed"] is True


def test_eval_with_default_mock_judge(scenarios_dir, capsys):
    """Default --judge-backend=mock returns canned 4/5 scores for all dims."""
    code = main(
        [
            "composer",
            "eval",
            str(scenarios_dir),
            "--format",
            "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["scenarios"][0]["judge_scores"]
    assert all(j["score"] == 4 for j in payload["scenarios"][0]["judge_scores"])


def test_eval_failing_scenario_returns_1(tmp_path, capsys):
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    (tmp_path / "skill_demo.pipeline.yaml").write_text(_SIDECAR, encoding="utf-8")

    scenarios = tmp_path / "scenarios"
    scenarios.mkdir()
    (scenarios / "fail.scenario.yaml").write_text(
        textwrap.dedent(
            """\
            name: "Will fail"
            skill: ../skill_demo.md
            vault: ../vault
            assertions:
              - kind: step_count_eq
                expected: 99
            """
        ),
        encoding="utf-8",
    )
    code = main(["composer", "eval", str(scenarios), "--judge-backend", "none"])
    assert code == 1


def test_eval_missing_directory_returns_2(tmp_path, capsys):
    code = main(["composer", "eval", str(tmp_path / "nope")])
    assert code == 2
    err = capsys.readouterr().err
    assert "not a directory" in err


def test_eval_empty_dir_returns_0(tmp_path, capsys):
    empty = tmp_path / "empty"
    empty.mkdir()
    code = main(["composer", "eval", str(empty)])
    assert code == 0
    out = capsys.readouterr().out
    assert "no *.scenario.yaml" in out


def test_eval_invalid_scenario_yaml_returns_2(tmp_path, capsys):
    scenarios = tmp_path / "scenarios"
    scenarios.mkdir()
    (scenarios / "bad.scenario.yaml").write_text("name: x\n", encoding="utf-8")  # no skill
    code = main(["composer", "eval", str(scenarios)])
    assert code == 2
