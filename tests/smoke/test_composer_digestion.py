"""Digestion phase driver — plan → augment → review →[sign-off]→ execute.

Tests the DRIVER's orchestration logic (phase sequencing, plan_doc
threading, the review→ready sign-off gate, stop-before-execute on
rejection/error) using synthetic phase skills whose schemas the test
controls — so it exercises the driver, not the real skills' strict
value-constraints (real-skill compilation is proven in
test_composer_skill_tool + the digestion-skilltools authoring).

Note: this test WRITES synthetic skill_tessellum_{plan,augment,review,
execute}_digestion.* into a tmp dir and points the driver there via
skills_dir — it never touches the shipped vault skills.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.composer import (
    MockBackend,
    SignOffPolicy,
    build_plan_gate,
    run_digestion_pipeline,
)
from tessellum.composer.signoff import AgentVerdict


# ── Synthetic phase skills (canonical + sidecar), one no_op step each ────────


def _write_phase_skill(
    skills_dir: Path,
    phase_skill_name: str,
    *,
    output_key: str,
    required: list[str],
    materializer: str = "no_op",
    aggregation: str = "corpus_wide",
) -> None:
    """Write a minimal 1-step skill the driver can compile + run."""
    sid = "step_1"
    canonical = (
        "---\n"
        "tags:\n  - resource\n  - skill\n"
        "keywords:\n  - alpha\n  - beta\n  - gamma\n"
        "topics:\n  - Digestion\n"
        "language: markdown\n"
        "date of note: 2026-07-23\n"
        "status: active\n"
        "building_block: procedure\n"
        f"pipeline_metadata: ./{phase_skill_name}.pipeline.yaml\n"
        "access_control_group: [\"general\"]\n"
        "---\n\n"
        f"# {phase_skill_name}\n\n"
        f"## Do it <!-- :: section_id = {sid} :: -->\n\n"
        "Run this phase. Return the JSON per the schema.\n"
    )
    req_yaml = ", ".join(required)
    sidecar = textwrap.dedent(
        f"""\
        pipeline:
          - section_id: {sid}
            role: CORE
            aggregation: {aggregation}
            batchable: false
            depends_on: []
            materializer: {materializer}
            output_key: {output_key}
            expected_output_schema:
              type: object
              required: [{req_yaml}]
            prompt_template: "phase"
        """
    )
    (skills_dir / f"{phase_skill_name}.md").write_text(canonical, encoding="utf-8")
    (skills_dir / f"{phase_skill_name}.pipeline.yaml").write_text(sidecar, encoding="utf-8")


def _synthetic_pipeline(skills_dir: Path) -> None:
    """The 4 phase skills the driver expects, minimal but real (compilable)."""
    _write_phase_skill(skills_dir, "skill_tessellum_plan_digestion",
                        output_key="plan_out", required=["plan_path"])
    _write_phase_skill(skills_dir, "skill_tessellum_augment_digestion_plan",
                        output_key="augment_out", required=["plan_text"])
    _write_phase_skill(skills_dir, "skill_tessellum_review_digestion_plan",
                        output_key="verdict", required=["ready"])
    # execute is per_leaf + writes a file
    _write_phase_skill(skills_dir, "skill_tessellum_execute_digestion_plan",
                        output_key="exec_out", required=["output_path", "body_markdown"],
                        materializer="body_markdown_to_file", aggregation="per_leaf")


def _mock(**overrides) -> MockBackend:
    """A backend whose default JSON satisfies every synthetic phase schema."""
    blob = {
        "plan_path": "plans/plan_demo.md",
        "plan_text": "# Plan\n\nbody",
        "ready": True, "failures": [],
        "output_path": "notes/n.md", "body_markdown": "# Note\n\nbody",
        "total_notes": 2,
    }
    blob.update(overrides)
    return MockBackend(default=json.dumps(blob))


_SOURCE = {"id": "demo", "plan_path": "plans/plan_demo.md",
           "plan_text": "# Plan", "total_notes": 2}


# ── The happy path: all 4 phases + approve + complete ───────────────────────


def test_full_pipeline_runs_all_four_phases(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf=dict(_SOURCE),
        backend=_mock(),
        vault_root=tmp_path / "vault",
    )
    ran = [p.phase for p in result.phases if p.ran]
    assert ran == ["plan", "augment", "review", "execute"]
    assert result.sign_off is not None and result.sign_off.decision == "approved"
    assert result.completed
    assert result.stopped_at is None


def test_plan_doc_threads_through_phases(tmp_path: Path) -> None:
    """The plan_doc accumulates each phase's structured output."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    result = run_digestion_pipeline(
        skills_dir=sd, source_leaf=dict(_SOURCE),
        backend=_mock(), vault_root=tmp_path / "vault",
    )
    # The review verdict landed in plan_doc (proves review's output threaded in).
    assert result.plan_doc.get("ready") is True
    assert result.plan_doc.get("plan_path") == "plans/plan_demo.md"


# ── The gate: a NOT-READY review stops before execute ───────────────────────


def test_not_ready_verdict_blocks_execute(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    # review returns ready=False → sign-off program gate rejects.
    result = run_digestion_pipeline(
        skills_dir=sd, source_leaf=dict(_SOURCE),
        backend=_mock(ready=False, failures=["CP2 failed"]),
        vault_root=tmp_path / "vault",
    )
    ran = [p.phase for p in result.phases if p.ran]
    assert ran == ["plan", "augment", "review"]  # execute NOT run
    assert result.sign_off.decision == "rejected"
    assert result.stopped_at == "review"
    assert not result.completed


def test_structurally_broken_plan_blocks_execute(tmp_path: Path) -> None:
    """A plan_doc failing the plan-structure pre-filter is rejected before
    the reviewer even runs (rung 1 of the sign-off ladder)."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    # total_notes 0 → plan_structure predicate PLAN-003 fails.
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf={"id": "x", "plan_path": "plans/p.md", "plan_text": "x", "total_notes": 0},
        backend=_mock(ready=True, total_notes=0),
        vault_root=tmp_path / "vault",
    )
    assert result.sign_off.decision == "rejected"
    assert result.stopped_at == "review"
    assert [p.phase for p in result.phases if p.ran] == ["plan", "augment", "review"]


# ── The sign-off ladder: agent + human rungs ────────────────────────────────


def test_agent_rung_can_reject_ready_plan(tmp_path: Path) -> None:
    """Even a ready plan is rejected if the reviewer-agent rung says no."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    result = run_digestion_pipeline(
        skills_dir=sd, source_leaf=dict(_SOURCE), backend=_mock(),
        vault_root=tmp_path / "vault",
        sign_off_policy=SignOffPolicy(use_agent=True, min_agent_confidence=0.7),
        agent_judge=lambda: AgentVerdict(approved=False, confidence=0.9, reason="weak"),
    )
    assert result.sign_off.decision == "rejected"
    assert result.sign_off.deciding_rung == "agent"
    assert result.stopped_at == "review"


def test_agent_rung_approves_then_executes(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    result = run_digestion_pipeline(
        skills_dir=sd, source_leaf=dict(_SOURCE), backend=_mock(),
        vault_root=tmp_path / "vault",
        sign_off_policy=SignOffPolicy(use_agent=True, min_agent_confidence=0.7,
                                      blast_radius_threshold=100),
        agent_judge=lambda: AgentVerdict(approved=True, confidence=0.95),
    )
    assert result.sign_off.decision == "approved"
    assert result.sign_off.deciding_rung == "agent"
    assert result.completed
    assert [p.phase for p in result.phases if p.ran][-1] == "execute"


def test_high_blast_escalates_to_human(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf={"id": "x", "plan_path": "plans/p.md", "plan_text": "x", "total_notes": 500},
        backend=_mock(total_notes=500),
        vault_root=tmp_path / "vault",
        sign_off_policy=SignOffPolicy(use_agent=True, use_human=True,
                                      blast_radius_threshold=50),
        agent_judge=lambda: AgentVerdict(approved=True, confidence=0.99),
        human_prompt=lambda: True,  # human approves the big change
    )
    assert result.sign_off.decision == "approved"
    assert result.sign_off.deciding_rung == "human"
    assert result.completed


# ── Registered plan-scope gate ──────────────────────────────────────────────


def test_plan_gate_registered_in_digest_gates() -> None:
    from tessellum.composer.gates import DIGEST_GATES

    assert set(DIGEST_GATES) == {"plan", "session", "wave"}
    suite = DIGEST_GATES["plan"]()
    # A well-formed plan_doc passes; a broken one fails.
    assert suite.evaluate({"plan_path": "p.md", "plan_text": "x", "total_notes": 3}).passed
    assert not suite.evaluate({"plan_path": "", "plan_text": "", "total_notes": 0}).passed


def test_build_plan_gate_predicate_causes() -> None:
    suite = build_plan_gate()
    res = suite.evaluate({"plan_path": "p.md", "plan_text": "x", "total_notes": 0},
                         short_circuit=False)
    assert not res.passed
    # total_notes=0 → PLAN-003 among the blocking issues.
    assert any(i.rule_id == "PLAN-003" for i in res.blocking_issues)


@pytest.mark.parametrize("bad", [None, {}, "not a dict"])
def test_plan_gate_fail_closed_on_missing_plan(bad) -> None:
    res = build_plan_gate().evaluate(bad)
    assert not res.passed
