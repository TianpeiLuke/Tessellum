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
from pathlib import Path

import pytest

from tessellum.composer import (
    MockBackend,
    RunBudget,
    SignOffPolicy,
    build_plan_gate,
    run_digestion_pipeline,
)
from tessellum.composer.signoff import AgentVerdict


# ── Synthetic phase skills (single-file), one no_op step each ────────────────


def _write_phase_skill(
    skills_dir: Path,
    phase_skill_name: str,
    *,
    output_key: str,
    required: list[str],
    materializer: str = "no_op",
    aggregation: str = "corpus_wide",
) -> None:
    """Write a minimal 1-step single-file skill the driver can compile + run.

    Each step is an H2 section carrying its ``section_id`` anchor, a leading
    ``​```yaml`` contract block (role/aggregation/…), and the prompt prose
    after it. No ``.pipeline.yaml`` sidecar, no ``pipeline_metadata``.
    """
    sid = "step_1"
    req_yaml = ", ".join(required)
    canonical = (
        "---\n"
        "tags:\n  - resource\n  - skill\n"
        "keywords:\n  - alpha\n  - beta\n  - gamma\n"
        "topics:\n  - Digestion\n"
        "language: markdown\n"
        "date of note: 2026-07-23\n"
        "status: active\n"
        "building_block: procedure\n"
        "access_control_group: [\"general\"]\n"
        "---\n\n"
        f"# {phase_skill_name}\n\n"
        f"## Do it <!-- :: section_id = {sid} :: -->\n\n"
        "```yaml\n"
        "role: CORE\n"
        f"aggregation: {aggregation}\n"
        "batchable: false\n"
        "depends_on: []\n"
        f"materializer: {materializer}\n"
        f"output_key: {output_key}\n"
        "expected_output_schema:\n"
        "  type: object\n"
        f"  required: [{req_yaml}]\n"
        "```\n\n"
        "phase\n"
    )
    (skills_dir / f"{phase_skill_name}.md").write_text(canonical, encoding="utf-8")


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


def test_invocation_budget_covers_linear_phases(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    backend = _mock()

    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf=dict(_SOURCE),
        backend=backend,
        vault_root=tmp_path / "vault",
        budget=RunBudget(max_invocations=1),
    )

    assert result.completed is False
    assert result.stopped_at == "augment"
    assert len(backend.calls) == 1
    assert result.phases[-1].run is not None
    assert "run budget exhausted" in (
        result.phases[-1].run.step_results[0].error or ""
    )


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


# ── P2b: opt-in NoteIntentGraph projection drives the execute fan-out ────────


def _note_intent_graph_blob() -> dict:
    """A note_intent_graph the review phase can emit into plan_doc; two intents
    → the execute wave must fan out to two per-intent leaves."""
    return {
        "objective_id": "obj",
        "intents": [
            {
                "note_id": "n1",
                "thesis": "first note",
                "building_block": "concept",
                "approx_words": 600,
                "target_path": "notes/n1.md",
                "provenance": [{"span_id": "s1", "source_ref": "src#1"}],
            },
            {
                "note_id": "n2",
                "thesis": "second note",
                "building_block": "procedure",
                "approx_words": 800,
                "target_path": "notes/n2.md",
                "provenance": [{"span_id": "s2", "source_ref": "src#2"}],
            },
        ],
    }


def test_note_intent_graph_projection_drives_execute(tmp_path: Path) -> None:
    """When plan_doc carries a valid note_intent_graph, the execute wave fans
    out one leaf per intent (P2b wiring) rather than the whole-plan fallback."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    vault = tmp_path / "vault"
    # The mock emits the graph as a phase's structured output → it threads into
    # plan_doc, engaging the opt-in projection branch. Each execute leaf carries
    # its own target_path.
    backend = _mock(note_intent_graph=_note_intent_graph_blob())
    result = run_digestion_pipeline(
        skills_dir=sd, source_leaf=dict(_SOURCE), backend=backend, vault_root=vault,
    )
    assert result.completed
    execute_phase = [p for p in result.phases if p.phase == "execute"][0]
    # Two intents → two per-leaf execute results (vs the single whole-plan leaf).
    assert len(execute_phase.run.leaves) == 2
    leaf_paths = {leaf.get("target_path") for leaf in execute_phase.run.leaves}
    assert leaf_paths == {"notes/n1.md", "notes/n2.md"}


def test_absent_note_intent_graph_is_shipped_single_leaf(tmp_path: Path) -> None:
    """Without a note_intent_graph, the shipped whole-plan fallback runs: a
    single execute leaf (byte-identical to pre-P2b behaviour)."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    result = run_digestion_pipeline(
        skills_dir=sd, source_leaf=dict(_SOURCE), backend=_mock(),
        vault_root=tmp_path / "vault",
    )
    assert result.completed
    execute_phase = [p for p in result.phases if p.phase == "execute"][0]
    assert len(execute_phase.run.leaves) == 1  # the whole-plan fallback leaf
    # FZ 20k9c1a1a1b7c2g: the plan declares 2 notes but the wave produced 1 leaf
    # → the under-production signal must be surfaced on the result so a headless
    # orchestrator (which never sees the RuntimeWarning) can branch on it.
    assert result.under_produced is True


def test_under_produced_false_when_leaf_count_matches_declared(tmp_path: Path) -> None:
    """A plan declaring 1 note that produces 1 leaf is NOT under-produced —
    the flag keys on declared>1 (FZ 20k9c1a1a1b7c2g)."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    source = {"id": "demo", "plan_path": "plans/plan_demo.md",
              "plan_text": "# Plan", "total_notes": 1}
    result = run_digestion_pipeline(
        skills_dir=sd, source_leaf=source, backend=_mock(total_notes=1),
        vault_root=tmp_path / "vault",
    )
    assert result.completed
    assert result.under_produced is False


def test_under_produced_false_when_stopped_before_execute(tmp_path: Path) -> None:
    """stop_after='review' never executes, so under_produced stays False even
    for a multi-note plan (nothing was produced to compare)."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _synthetic_pipeline(sd)
    result = run_digestion_pipeline(
        skills_dir=sd, source_leaf=dict(_SOURCE), backend=_mock(),
        vault_root=tmp_path / "vault", stop_after="review",
    )
    assert result.stopped_at == "review_accepted"
    assert result.under_produced is False


# ── P15 (FZ 20k9c1a1a1b7c2h): the review-revise loop ─────────────────────────

def _write_marked_phase_skill(skills_dir: Path, name: str, *, output_key: str,
                              required: list[str], marker: str,
                              materializer: str = "no_op",
                              aggregation: str = "corpus_wide") -> None:
    """Like _write_phase_skill but with a distinct prompt `marker` (so a backend
    can tell which phase called it) and a `{{leaf.review_failures}}` echo in the
    augment prompt (so we can detect a revise round)."""
    canonical = (
        "---\ntags:\n  - resource\n  - skill\n"
        "keywords:\n  - alpha\n  - beta\n  - gamma\ntopics:\n  - Digestion\n"
        "language: markdown\ndate of note: 2026-07-27\nstatus: active\n"
        "building_block: procedure\naccess_control_group: [\"general\"]\n---\n\n"
        f"# {name}\n\n## Do it <!-- :: section_id = step_1 :: -->\n\n"
        "```yaml\nrole: CORE\n"
        f"aggregation: {aggregation}\nbatchable: false\ndepends_on: []\n"
        f"materializer: {materializer}\noutput_key: {output_key}\n"
        "expected_output_schema:\n  type: object\n"
        f"  required: [{', '.join(required)}]\n```\n\n"
        f"{marker}\nPRIOR REVIEW FAILURES: {{{{leaf.review_failures}}}}\n"
    )
    (skills_dir / f"{name}.md").write_text(canonical, encoding="utf-8")


def _marked_pipeline(skills_dir: Path) -> None:
    _write_marked_phase_skill(skills_dir, "skill_tessellum_plan_digestion",
                              output_key="plan_out", required=["plan_path"], marker="PLANMARK")
    _write_marked_phase_skill(skills_dir, "skill_tessellum_augment_digestion_plan",
                              output_key="augment_out", required=["plan_text"], marker="AUGMENTMARK")
    _write_marked_phase_skill(skills_dir, "skill_tessellum_review_digestion_plan",
                              output_key="verdict", required=["ready"], marker="REVIEWMARK")
    _write_marked_phase_skill(skills_dir, "skill_tessellum_execute_digestion_plan",
                              output_key="exec_out", required=["output_path", "body_markdown"],
                              marker="EXECMARK", materializer="body_markdown_to_file",
                              aggregation="per_leaf")


class _RevisingBackend:
    """Review returns `ready:false` (shrinking failure set) for the first
    `reject_rounds` reviews, then `ready:true` — so P15 must re-augment and
    converge. Records review calls + whether each augment saw injected failures."""

    backend_id = "revising"

    def __init__(self, *, reject_rounds: int, shrink: bool = True) -> None:
        self.reject_rounds = reject_rounds
        self.shrink = shrink
        self.review_calls = 0
        self.augment_calls = 0
        self.augment_saw_failures: list[bool] = []

    def call(self, request):  # noqa: ANN001
        import json as _json
        from tessellum.composer import LLMResponse
        p = request.user_prompt
        blob = {
            "plan_path": "plans/plan_demo.md", "plan_text": "# Plan\n\nbody",
            "output_path": "notes/n.md", "body_markdown": "# Note\n\nbody",
            "total_notes": 2, "ready": True, "failures": [],
        }
        if "AUGMENTMARK" in p:
            self.augment_calls += 1
            tail = p.split("PRIOR REVIEW FAILURES:", 1)[1] if "PRIOR REVIEW FAILURES:" in p else ""
            self.augment_saw_failures.append("CP" in tail)
        if "REVIEWMARK" in p:
            self.review_calls += 1
            if self.review_calls <= self.reject_rounds:
                n = (self.reject_rounds - self.review_calls + 2) if self.shrink else 2
                blob = {**blob, "ready": False,
                        "failures": [f"CP{i} FAIL – gap {i}" for i in range(n)]}
        return LLMResponse(content=_json.dumps(blob), elapsed_ms=1.0, backend_id=self.backend_id)


def test_review_revise_loop_converges(tmp_path: Path) -> None:
    """P15: review rejects round 1 (with failures), the loop re-augments with
    those failures injected, review accepts round 2 → converged + executed."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _marked_pipeline(sd)
    be = _RevisingBackend(reject_rounds=1)
    result = run_digestion_pipeline(
        skills_dir=sd, source_leaf=dict(_SOURCE), backend=be,
        vault_root=tmp_path / "vault", max_review_rounds=2, stop_after="review",
    )
    assert result.stopped_at == "review_accepted", "loop should converge to accepted"
    assert result.review_rounds == 1, "exactly one extra revise round"
    assert be.review_calls == 2, "review ran twice (reject then accept)"
    assert be.augment_calls == 2, "augment ran twice (initial + revise)"
    # the SECOND augment must have seen the injected review failures
    assert be.augment_saw_failures == [False, True]


def test_review_revise_loop_default_is_single_pass(tmp_path: Path) -> None:
    """max_review_rounds=0 (default) → the original single pass; a rejection
    halts at review with review_rounds=0 (byte-identical prior behaviour)."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _marked_pipeline(sd)
    be = _RevisingBackend(reject_rounds=1)  # rejects round 1
    result = run_digestion_pipeline(
        skills_dir=sd, source_leaf=dict(_SOURCE), backend=be,
        vault_root=tmp_path / "vault",  # max_review_rounds defaults to 0
    )
    assert result.stopped_at == "review"
    assert result.review_rounds == 0
    assert be.review_calls == 1 and be.augment_calls == 1, "no revise round"


def test_review_revise_loop_escalates_when_not_converging(tmp_path: Path) -> None:
    """A review that keeps rejecting with a non-shrinking failure set stops after
    the budget (or the same-failure short-circuit) and escalates the residual —
    it does NOT loop forever or force-execute."""
    sd = tmp_path / "skills"
    sd.mkdir()
    _marked_pipeline(sd)
    be = _RevisingBackend(reject_rounds=99, shrink=False)  # never converges, flat 2 failures
    result = run_digestion_pipeline(
        skills_dir=sd, source_leaf=dict(_SOURCE), backend=be,
        vault_root=tmp_path / "vault", max_review_rounds=3,
    )
    assert result.stopped_at == "review", "non-converging → escalate, not execute"
    # same-failure short-circuit fires after round 1 (round-2 failures not smaller)
    assert result.review_rounds <= 3
    assert be.review_calls <= 4  # bounded, never unbounded
