"""Scenario-based evaluation framework — structural assertions + LLM judge.

Two complementary kinds of checks:

  1. **Structural assertions** — deterministic, no LLM:

     - ``file_written``: did the pipeline produce the expected vault file?
     - ``response_contains``: does a step's response contain a substring?
     - ``step_count_eq``: did exactly N step invocations occur?
     - ``error_count_eq``: did exactly N steps surface an error?
     - ``no_errors``: shorthand for ``error_count_eq=0``.

     Structural assertions catch the load-bearing wiring issues — the
     pipeline ran, the right number of steps fired, files landed where
     expected. They don't say anything about content quality.

  2. **LLMJudge 6-dim rubric** — content-quality scoring:

     - ``relevance``: does the output address the input?
     - ``completeness``: are all required facets covered?
     - ``accuracy``: are the claims supported by the source?
     - ``clarity``: is the writing clear and well-structured?
     - ``structural_integrity``: does the output respect the format
       contract (frontmatter, sections, etc.)?
     - ``epistemic_congruence``: does the output honour the BB-type
       expectations the question implies?

     Each dimension is rated 1-5 by an LLM judge. The default judge is
     ``MockBackend`` (returns canned high scores — useful for testing the
     framework). Pass an ``AnthropicBackend`` for real evaluation.

YAML scenario format::

    name: "Skill X handles edge-case Y"
    skill: vault/resources/skills/skill_x.md
    expected_output_description: "A summary note with three facets..."
    leaves:
      - {id: "case_1", input: "..."}
    vault: ./eval-vault
    assertions:
      - kind: no_errors
      - kind: file_written
        target: notes/expected.md
      - kind: response_contains
        target: step_2
        expected: "facet_a"
    rubric_dimensions: [relevance, completeness]  # optional; full set by default

What this module does NOT do (deferred):

  - Bootstrapped confidence intervals on judge scores. v0.2+ if needed.
  - Multi-judge ensembles. v0.2+ if needed.
  - Pairwise/preference judging. The 6-dim rubric is what users want first.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from tessellum.composer.compiler import compile_skill
from tessellum.composer.llm import LLMBackend, LLMRequest
from tessellum.composer.scheduler import RunResult, StepResult, run_pipeline


DEFAULT_RUBRIC_DIMENSIONS: tuple[str, ...] = (
    "relevance",
    "completeness",
    "accuracy",
    "clarity",
    "structural_integrity",
    # Asks the judge whether the response honours the BB-type
    # expectations the question implies. DKS cycles produce typed notes
    # (empirical_observation / argument / counter_argument / model /
    # procedure / concept), and an epistemically-congruent response
    # must respect those types.
    "epistemic_congruence",
)


# ── Public dataclasses ─────────────────────────────────────────────────────


@dataclass(frozen=True)
class Assertion:
    """One structural assertion against a pipeline run.

    Attributes:
        kind: ``"file_written"`` | ``"response_contains"`` |
            ``"step_count_eq"`` | ``"error_count_eq"`` | ``"no_errors"``.
        target: Path / section_id / unused, depending on kind.
        expected: Expected value (substring, count). Optional for
            ``no_errors`` and ``file_written``.
    """

    kind: str
    target: str = ""
    expected: Any = None


@dataclass(frozen=True)
class AssertionResult:
    """Outcome of one assertion."""

    assertion: Assertion
    passed: bool
    actual: Any = None
    message: str = ""


@dataclass(frozen=True)
class JudgeScore:
    """One rubric-dimension score from the LLM judge."""

    dimension: str
    score: int
    justification: str = ""


@dataclass(frozen=True)
class EvalScenario:
    """One eval scenario — pairs a skill+inputs with expected behavior."""

    name: str
    skill_path: Path
    leaves: tuple[dict, ...] = ()
    vault_root: Path = Path("vault")
    assertions: tuple[Assertion, ...] = ()
    rubric_dimensions: tuple[str, ...] = DEFAULT_RUBRIC_DIMENSIONS
    expected_output_description: str = ""


@dataclass(frozen=True)
class ScenarioResult:
    """One scenario's evaluation outcome."""

    scenario_name: str
    run_result: RunResult | None = None
    assertions: tuple[AssertionResult, ...] = ()
    judge_scores: tuple[JudgeScore, ...] = ()
    overall_passed: bool = False
    error: str | None = None


@dataclass(frozen=True)
class EvalResult:
    """Aggregate across an evaluation suite."""

    scenarios: tuple[ScenarioResult, ...]
    passed_count: int = 0
    failed_count: int = 0
    error_count: int = 0
    mean_score_by_dim: dict[str, float] = field(default_factory=dict)


class EvalError(Exception):
    """Raised on hard eval-framework failures (malformed scenario, etc.)."""


# ── Loading scenarios ──────────────────────────────────────────────────────


def load_scenario(path: Path) -> EvalScenario:
    """Parse one ``*.scenario.yaml`` file into an :class:`EvalScenario`.

    Raises:
        EvalError: missing required fields, bad assertion shape.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        raise EvalError(f"cannot read scenario {path}: {e}") from e
    try:
        data = yaml.safe_load(raw) or {}
    except yaml.YAMLError as e:
        raise EvalError(f"scenario {path} YAML parse error: {e}") from e
    if not isinstance(data, dict):
        raise EvalError(f"scenario {path} must be a YAML mapping")

    name = data.get("name") or path.stem
    skill = data.get("skill")
    if not skill:
        raise EvalError(f"scenario {path} missing required `skill` field")
    skill_path = (path.parent / str(skill)).resolve()

    vault_field = data.get("vault") or "vault"
    vault_root = (path.parent / str(vault_field)).resolve()

    leaves_field = data.get("leaves") or []
    if not isinstance(leaves_field, list):
        raise EvalError(f"scenario {path}: `leaves` must be a list")

    assertions_field = data.get("assertions") or []
    if not isinstance(assertions_field, list):
        raise EvalError(f"scenario {path}: `assertions` must be a list")
    assertions: list[Assertion] = []
    for i, a in enumerate(assertions_field):
        if not isinstance(a, dict):
            raise EvalError(f"scenario {path}: assertions[{i}] must be a mapping")
        kind = a.get("kind")
        if not kind:
            raise EvalError(
                f"scenario {path}: assertions[{i}] missing `kind`"
            )
        assertions.append(
            Assertion(
                kind=str(kind),
                target=str(a.get("target", "")),
                expected=a.get("expected"),
            )
        )

    rubric_dims = data.get("rubric_dimensions")
    if rubric_dims is None:
        dims = DEFAULT_RUBRIC_DIMENSIONS
    elif isinstance(rubric_dims, list) and all(isinstance(d, str) for d in rubric_dims):
        dims = tuple(rubric_dims)
    else:
        raise EvalError(
            f"scenario {path}: `rubric_dimensions` must be a list of strings"
        )

    return EvalScenario(
        name=str(name),
        skill_path=skill_path,
        leaves=tuple(leaves_field),
        vault_root=vault_root,
        assertions=tuple(assertions),
        rubric_dimensions=dims,
        expected_output_description=str(data.get("expected_output_description") or ""),
    )


def load_scenarios(directory: Path) -> list[EvalScenario]:
    """Load every ``*.scenario.yaml`` file in ``directory`` (sorted)."""
    if not directory.is_dir():
        raise EvalError(f"scenarios directory does not exist: {directory}")
    scenarios: list[EvalScenario] = []
    for path in sorted(directory.glob("*.scenario.yaml")):
        scenarios.append(load_scenario(path))
    return scenarios


# ── Structural assertions ──────────────────────────────────────────────────


def _check_assertion(
    assertion: Assertion,
    *,
    run_result: RunResult,
    vault_root: Path,
) -> AssertionResult:
    kind = assertion.kind
    if kind == "no_errors":
        passed = run_result.error_count == 0
        return AssertionResult(
            assertion=assertion,
            passed=passed,
            actual=run_result.error_count,
            message="" if passed else f"{run_result.error_count} step(s) errored",
        )

    if kind == "error_count_eq":
        expected = int(assertion.expected or 0)
        actual = run_result.error_count
        return AssertionResult(
            assertion=assertion,
            passed=actual == expected,
            actual=actual,
            message=("" if actual == expected else f"expected {expected}, got {actual}"),
        )

    if kind == "step_count_eq":
        expected = int(assertion.expected or 0)
        actual = len(run_result.step_results)
        return AssertionResult(
            assertion=assertion,
            passed=actual == expected,
            actual=actual,
            message=("" if actual == expected else f"expected {expected}, got {actual}"),
        )

    if kind == "file_written":
        target = (vault_root / assertion.target).resolve()
        passed = target.exists()
        return AssertionResult(
            assertion=assertion,
            passed=passed,
            actual=str(target),
            message="" if passed else f"file not written: {target}",
        )

    if kind == "response_contains":
        section_id = assertion.target
        substring = str(assertion.expected or "")
        matches = [
            r for r in run_result.step_results if r.section_id == section_id
        ]
        if not matches:
            return AssertionResult(
                assertion=assertion,
                passed=False,
                message=f"no step result found for section_id={section_id!r}",
            )
        # If any invocation of this step contains the substring, pass.
        contained = any(substring in r.response.content for r in matches)
        return AssertionResult(
            assertion=assertion,
            passed=contained,
            actual=substring,
            message=(
                ""
                if contained
                else f"substring {substring!r} not found in any "
                f"{section_id!r} response"
            ),
        )

    return AssertionResult(
        assertion=assertion,
        passed=False,
        message=f"unknown assertion kind: {kind!r}",
    )


# ── LLMJudge ───────────────────────────────────────────────────────────────


JUDGE_SYSTEM_PROMPT = """You are a strict, fair evaluator of LLM pipeline output.
You score each requested rubric dimension on an integer scale of 1-5,
where 1 = unacceptable, 3 = acceptable, 5 = excellent. Always return
strict JSON matching the requested schema. Do not include any text
outside the JSON object."""


def _build_judge_prompt(
    *,
    expected_description: str,
    actual_output: str,
    dimensions: tuple[str, ...],
) -> str:
    dim_lines = "\n".join(f"- {d}" for d in dimensions)
    schema_props = ",\n".join(
        f'    "{d}": {{ "score": <int 1-5>, "justification": "<brief>" }}'
        for d in dimensions
    )
    return (
        f"Expected output description:\n{expected_description or '(none provided)'}\n\n"
        f"Actual output:\n{actual_output}\n\n"
        f"Rubric dimensions to score:\n{dim_lines}\n\n"
        f"Return a JSON object of the form:\n"
        f"{{\n{schema_props}\n}}"
    )


class LLMJudge:
    """Wraps any LLMBackend to produce 6-dim rubric scores.

    Attributes:
        backend: The judge LLM. Use ``MockBackend`` for tests, real
            backend for production. The backend used for the judge is
            independent of the backend used to run the scenario.
    """

    def __init__(self, backend: LLMBackend) -> None:
        self.backend = backend

    def score(
        self,
        *,
        expected_description: str,
        actual_output: str,
        dimensions: tuple[str, ...],
    ) -> tuple[JudgeScore, ...]:
        """Score one output against the rubric. Returns one score per dim.

        Soft-fails on parse errors: every dim gets ``score=0`` and the
        parse error in the justification. Pipeline tests can still
        continue.
        """
        prompt = _build_judge_prompt(
            expected_description=expected_description,
            actual_output=actual_output,
            dimensions=dimensions,
        )
        response = self.backend.call(
            LLMRequest(
                system_prompt=JUDGE_SYSTEM_PROMPT,
                user_prompt=prompt,
            )
        )
        return _parse_judge_response(response.content, dimensions)


def _parse_judge_response(
    text: str, dimensions: tuple[str, ...]
) -> tuple[JudgeScore, ...]:
    # Be tolerant — judges sometimes wrap JSON in prose. Try strict first.
    parsed: dict | None = None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # Fallback: extract the first {...} block.
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                parsed = json.loads(m.group(0))
            except json.JSONDecodeError:
                parsed = None

    if not isinstance(parsed, dict):
        return tuple(
            JudgeScore(dimension=d, score=0, justification="judge response unparseable")
            for d in dimensions
        )

    scores: list[JudgeScore] = []
    for d in dimensions:
        entry = parsed.get(d)
        if isinstance(entry, dict):
            raw_score = entry.get("score", 0)
            justification = str(entry.get("justification") or "")
        elif isinstance(entry, (int, float)):
            raw_score = entry
            justification = ""
        else:
            raw_score = 0
            justification = f"missing dimension {d!r} in judge response"
        try:
            score = max(0, min(5, int(raw_score)))
        except (TypeError, ValueError):
            score = 0
        scores.append(
            JudgeScore(dimension=d, score=score, justification=justification)
        )
    return tuple(scores)


# ── Running the eval suite ─────────────────────────────────────────────────


def run_eval(
    scenarios: list[EvalScenario],
    *,
    backend: LLMBackend,
    judge: LLMJudge | None = None,
    dry_run: bool = False,
) -> EvalResult:
    """Run a list of scenarios and aggregate results.

    Args:
        scenarios: Scenarios to evaluate.
        backend: LLM backend for the pipeline runs.
        judge: Optional :class:`LLMJudge`. If ``None``, no rubric
            scoring is performed (structural assertions still run).
            For tests, pass ``LLMJudge(MockBackend(...))``; for
            production pass ``LLMJudge(AnthropicBackend(model="..."))``.
        dry_run: Pass-through to ``run_pipeline``.

    Returns:
        EvalResult.
    """
    results: list[ScenarioResult] = []
    error_count = 0
    for scenario in scenarios:
        result = _run_one_scenario(
            scenario, backend=backend, judge=judge, dry_run=dry_run
        )
        if result.error is not None:
            error_count += 1
        results.append(result)

    passed_count = sum(1 for r in results if r.overall_passed)
    failed_count = len(results) - passed_count - error_count

    # Aggregate mean scores per dimension.
    sums: dict[str, float] = {}
    counts: dict[str, int] = {}
    for r in results:
        for s in r.judge_scores:
            sums[s.dimension] = sums.get(s.dimension, 0.0) + s.score
            counts[s.dimension] = counts.get(s.dimension, 0) + 1
    mean_score_by_dim = {
        d: (sums[d] / counts[d]) for d in sums if counts[d] > 0
    }

    return EvalResult(
        scenarios=tuple(results),
        passed_count=passed_count,
        failed_count=failed_count,
        error_count=error_count,
        mean_score_by_dim=mean_score_by_dim,
    )


def _run_one_scenario(
    scenario: EvalScenario,
    *,
    backend: LLMBackend,
    judge: LLMJudge | None,
    dry_run: bool,
) -> ScenarioResult:
    try:
        compiled = compile_skill(scenario.skill_path)
    except Exception as e:
        return ScenarioResult(
            scenario_name=scenario.name,
            error=f"compile failed: {type(e).__name__}: {e}",
            overall_passed=False,
        )

    try:
        run = run_pipeline(
            compiled,
            leaves=list(scenario.leaves) if scenario.leaves else None,
            backend=backend,
            vault_root=scenario.vault_root,
            dry_run=dry_run,
        )
    except Exception as e:
        return ScenarioResult(
            scenario_name=scenario.name,
            error=f"run failed: {type(e).__name__}: {e}",
            overall_passed=False,
        )

    assertion_results = tuple(
        _check_assertion(a, run_result=run, vault_root=scenario.vault_root)
        for a in scenario.assertions
    )

    judge_scores: tuple[JudgeScore, ...] = ()
    if judge is not None and run.step_results:
        # Judge the most-recent CORE step's response — pragmatic default.
        last_core: StepResult | None = None
        for r in run.step_results:
            if r.error is None:
                last_core = r
        if last_core is not None:
            judge_scores = judge.score(
                expected_description=scenario.expected_output_description,
                actual_output=last_core.response.content,
                dimensions=scenario.rubric_dimensions,
            )

    structural_passed = all(a.passed for a in assertion_results)
    return ScenarioResult(
        scenario_name=scenario.name,
        run_result=run,
        assertions=assertion_results,
        judge_scores=judge_scores,
        overall_passed=structural_passed,
    )


__all__ = [
    "DEFAULT_RUBRIC_DIMENSIONS",
    "Assertion",
    "AssertionResult",
    "EvalError",
    "EvalResult",
    "EvalScenario",
    "JudgeScore",
    "LLMJudge",
    "ScenarioResult",
    "load_scenario",
    "load_scenarios",
    "run_eval",
]
