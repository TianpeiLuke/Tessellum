"""Wave 5b smoke — eval framework (assertions + LLMJudge rubric)."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.composer import (
    Assertion,
    AssertionResult,
    DEFAULT_RUBRIC_DIMENSIONS,
    EvalError,
    EvalScenario,
    JudgeScore,
    LLMJudge,
    MockBackend,
    ScenarioResult,
    load_scenario,
    load_scenarios,
    run_eval,
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
    pipeline_metadata: ./skill_demo.pipeline.yaml
    ---

    # Demo

    ## Step 1 <!-- :: section_id = step_1 :: -->

    Step 1 body.
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
def skill(tmp_path: Path) -> Path:
    p = tmp_path / "skill_demo.md"
    p.write_text(_CANONICAL, encoding="utf-8")
    (tmp_path / "skill_demo.pipeline.yaml").write_text(_SIDECAR, encoding="utf-8")
    return p


# ── Scenario YAML loading ─────────────────────────────────────────────────


def test_load_scenario_basic(tmp_path: Path, skill: Path) -> None:
    scenario_yaml = tmp_path / "case_a.scenario.yaml"
    scenario_yaml.write_text(
        textwrap.dedent(
            """\
            name: "Case A"
            skill: ./skill_demo.md
            expected_output_description: "A summary."
            leaves:
              - {id: "x"}
            assertions:
              - kind: no_errors
              - kind: step_count_eq
                expected: 1
            """
        ),
        encoding="utf-8",
    )
    scenario = load_scenario(scenario_yaml)
    assert isinstance(scenario, EvalScenario)
    assert scenario.name == "Case A"
    assert scenario.skill_path == skill
    assert len(scenario.assertions) == 2
    assert scenario.assertions[0].kind == "no_errors"
    assert scenario.assertions[1].kind == "step_count_eq"
    assert scenario.assertions[1].expected == 1


def test_load_scenario_missing_skill_raises(tmp_path: Path) -> None:
    p = tmp_path / "bad.scenario.yaml"
    p.write_text("name: x\n", encoding="utf-8")
    with pytest.raises(EvalError, match="missing required `skill`"):
        load_scenario(p)


def test_load_scenario_assertions_must_be_list(tmp_path: Path, skill: Path) -> None:
    p = tmp_path / "bad.scenario.yaml"
    p.write_text(
        f"name: x\nskill: ./skill_demo.md\nassertions: 'not a list'\n",
        encoding="utf-8",
    )
    with pytest.raises(EvalError, match="assertions"):
        load_scenario(p)


def test_load_scenario_default_rubric_dimensions(tmp_path: Path, skill: Path) -> None:
    p = tmp_path / "default.scenario.yaml"
    p.write_text(
        f"name: x\nskill: ./skill_demo.md\n",
        encoding="utf-8",
    )
    scenario = load_scenario(p)
    assert scenario.rubric_dimensions == DEFAULT_RUBRIC_DIMENSIONS


def test_load_scenario_custom_rubric_dimensions(tmp_path: Path, skill: Path) -> None:
    p = tmp_path / "custom.scenario.yaml"
    p.write_text(
        f"name: x\nskill: ./skill_demo.md\nrubric_dimensions: [relevance, clarity]\n",
        encoding="utf-8",
    )
    scenario = load_scenario(p)
    assert scenario.rubric_dimensions == ("relevance", "clarity")


def test_load_scenarios_from_directory(tmp_path: Path, skill: Path) -> None:
    for name in ["a", "b", "c"]:
        (tmp_path / f"case_{name}.scenario.yaml").write_text(
            f"name: case_{name}\nskill: ./skill_demo.md\n", encoding="utf-8"
        )
    # Non-scenario file should be ignored.
    (tmp_path / "not_a_scenario.yaml").write_text("ignored: true\n", encoding="utf-8")
    scenarios = load_scenarios(tmp_path)
    assert len(scenarios) == 3
    assert [s.name for s in scenarios] == ["case_a", "case_b", "case_c"]


# ── Structural assertions ────────────────────────────────────────────────


def test_assertion_no_errors_passes(tmp_path: Path, skill: Path) -> None:
    scenario = EvalScenario(
        name="t",
        skill_path=skill,
        vault_root=tmp_path / "vault",
        assertions=(Assertion(kind="no_errors"),),
    )
    backend = MockBackend(default='{"out": 1}')
    result = run_eval([scenario], backend=backend, judge=None)
    assert result.passed_count == 1
    assert result.failed_count == 0
    assert result.scenarios[0].assertions[0].passed is True


def test_assertion_step_count_eq(tmp_path: Path, skill: Path) -> None:
    scenario = EvalScenario(
        name="t",
        skill_path=skill,
        vault_root=tmp_path / "vault",
        assertions=(Assertion(kind="step_count_eq", expected=1),),
    )
    result = run_eval([scenario], backend=MockBackend(default="{}"), judge=None)
    assert result.scenarios[0].assertions[0].passed is True


def test_assertion_step_count_eq_fails_with_message(tmp_path: Path, skill: Path) -> None:
    scenario = EvalScenario(
        name="t",
        skill_path=skill,
        vault_root=tmp_path / "vault",
        assertions=(Assertion(kind="step_count_eq", expected=99),),
    )
    result = run_eval([scenario], backend=MockBackend(default="{}"), judge=None)
    assert result.scenarios[0].overall_passed is False
    assert "99" in result.scenarios[0].assertions[0].message


def test_assertion_response_contains(tmp_path: Path, skill: Path) -> None:
    scenario = EvalScenario(
        name="t",
        skill_path=skill,
        vault_root=tmp_path / "vault",
        assertions=(
            Assertion(kind="response_contains", target="step_1", expected="hello"),
        ),
    )
    backend = MockBackend(default='hello world')
    result = run_eval([scenario], backend=backend, judge=None)
    assert result.scenarios[0].assertions[0].passed is True


def test_assertion_response_contains_unknown_section(tmp_path: Path, skill: Path) -> None:
    scenario = EvalScenario(
        name="t",
        skill_path=skill,
        vault_root=tmp_path / "vault",
        assertions=(
            Assertion(kind="response_contains", target="not_a_step", expected="x"),
        ),
    )
    result = run_eval([scenario], backend=MockBackend(default="x"), judge=None)
    assert result.scenarios[0].assertions[0].passed is False
    assert "not_a_step" in result.scenarios[0].assertions[0].message


def test_assertion_unknown_kind(tmp_path: Path, skill: Path) -> None:
    scenario = EvalScenario(
        name="t",
        skill_path=skill,
        vault_root=tmp_path / "vault",
        assertions=(Assertion(kind="never_heard_of_it"),),
    )
    result = run_eval([scenario], backend=MockBackend(default="{}"), judge=None)
    assert result.scenarios[0].assertions[0].passed is False
    assert "unknown assertion kind" in result.scenarios[0].assertions[0].message


# ── LLMJudge ──────────────────────────────────────────────────────────────


def test_llmjudge_parses_full_rubric() -> None:
    canned = json.dumps(
        {
            d: {"score": 4, "justification": "ok"}
            for d in DEFAULT_RUBRIC_DIMENSIONS
        }
    )
    judge = LLMJudge(MockBackend(default=canned))
    scores = judge.score(
        expected_description="A summary.",
        actual_output="The summary.",
        dimensions=DEFAULT_RUBRIC_DIMENSIONS,
    )
    assert len(scores) == 5
    assert all(isinstance(s, JudgeScore) for s in scores)
    assert all(s.score == 4 for s in scores)


def test_llmjudge_clamps_out_of_range() -> None:
    canned = json.dumps(
        {d: {"score": 99, "justification": ""} for d in ("relevance",)}
    )
    judge = LLMJudge(MockBackend(default=canned))
    scores = judge.score(
        expected_description="x",
        actual_output="y",
        dimensions=("relevance",),
    )
    assert scores[0].score == 5  # clamped


def test_llmjudge_handles_unparseable_response() -> None:
    judge = LLMJudge(MockBackend(default="totally not json"))
    scores = judge.score(
        expected_description="x",
        actual_output="y",
        dimensions=("relevance", "clarity"),
    )
    assert all(s.score == 0 for s in scores)
    assert all("unparseable" in s.justification for s in scores)


def test_llmjudge_missing_dimension_gets_zero() -> None:
    canned = json.dumps({"relevance": {"score": 5}})  # no clarity
    judge = LLMJudge(MockBackend(default=canned))
    scores = judge.score(
        expected_description="x",
        actual_output="y",
        dimensions=("relevance", "clarity"),
    )
    by_dim = {s.dimension: s for s in scores}
    assert by_dim["relevance"].score == 5
    assert by_dim["clarity"].score == 0
    assert "missing" in by_dim["clarity"].justification.lower()


def test_llmjudge_extracts_json_from_prose() -> None:
    """Tolerant of prose-wrapped JSON."""
    canned = (
        'Here is my evaluation: {"relevance": {"score": 3, "justification": "meh"}} '
        'I hope this helps.'
    )
    judge = LLMJudge(MockBackend(default=canned))
    scores = judge.score(
        expected_description="x",
        actual_output="y",
        dimensions=("relevance",),
    )
    assert scores[0].score == 3
    assert scores[0].justification == "meh"


# ── End-to-end run_eval ───────────────────────────────────────────────────


def test_run_eval_with_judge_aggregates_mean_scores(
    tmp_path: Path, skill: Path
) -> None:
    canned = json.dumps(
        {d: {"score": 4, "justification": "ok"} for d in DEFAULT_RUBRIC_DIMENSIONS}
    )
    scenario = EvalScenario(
        name="t",
        skill_path=skill,
        vault_root=tmp_path / "vault",
        assertions=(Assertion(kind="no_errors"),),
        expected_output_description="A summary.",
    )
    result = run_eval(
        [scenario],
        backend=MockBackend(default='{"out": 1}'),
        judge=LLMJudge(MockBackend(default=canned)),
    )
    assert result.passed_count == 1
    assert len(result.mean_score_by_dim) == 5
    for mean in result.mean_score_by_dim.values():
        assert mean == 4.0


def test_run_eval_compile_failure_marks_error(tmp_path: Path) -> None:
    scenario = EvalScenario(
        name="bad",
        skill_path=tmp_path / "nope.md",
        vault_root=tmp_path / "vault",
    )
    result = run_eval([scenario], backend=MockBackend(default="{}"), judge=None)
    assert result.error_count == 1
    assert result.scenarios[0].error is not None
    assert "compile failed" in result.scenarios[0].error


def test_run_eval_failed_assertion_does_not_pass(tmp_path: Path, skill: Path) -> None:
    scenario = EvalScenario(
        name="t",
        skill_path=skill,
        vault_root=tmp_path / "vault",
        assertions=(Assertion(kind="step_count_eq", expected=99),),
    )
    result = run_eval([scenario], backend=MockBackend(default="{}"), judge=None)
    assert result.passed_count == 0
    assert result.failed_count == 1


def test_run_eval_no_judge_skips_rubric(tmp_path: Path, skill: Path) -> None:
    scenario = EvalScenario(
        name="t",
        skill_path=skill,
        vault_root=tmp_path / "vault",
        assertions=(Assertion(kind="no_errors"),),
    )
    result = run_eval([scenario], backend=MockBackend(default="{}"), judge=None)
    assert result.scenarios[0].judge_scores == ()
    assert result.mean_score_by_dim == {}
