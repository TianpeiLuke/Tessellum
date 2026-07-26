"""M3 smoke — corpus planning wave (CorpusPlan → N accepted sub-plans).

Multi-document corpus digestion (FZ 20k9c1a1a1b7b1). Proves the wave that turns
a decided CorpusPlan into one ACCEPTED plan per sub-objective by running the
shipped plan→augment→review→sign-off path (stop_after="review") over each
sub-objective's slice of the bundle — WITHOUT executing.

Covers:
  - all sub-objectives accepted → per-sub-plan accepted plan_docs captured;
  - a rejected sub-objective is marked blocked, others still accepted
    (a weak sub-plan blocks only itself — the partition policy);
  - each sub-plan sees ONLY its slice of members (slice correctness);
  - stop_after="review" writes NO note files (planning only);
  - bundle_id mismatch fails loud.
"""

from __future__ import annotations

import json
from pathlib import Path

from tessellum.composer import (
    CorpusPlan,
    MockBackend,
    SignOffPolicy,
    SubObjective,
    run_corpus_digestion,
    run_corpus_planning_wave,
    run_digestion_pipeline,
)
from tessellum.composer.knowledge_plan import BundleMember, SourceBundle


# ── synthetic phase skills (plan/augment/review reference {{leaf.members}}) ──


def _write_phase_skills(skills_dir: Path) -> None:
    def _skill(name: str, *, output_key: str, required: list[str],
               materializer: str = "no_op", aggregation: str = "corpus_wide",
               prompt: str = "phase") -> None:
        req = ", ".join(required)
        (skills_dir / f"{name}.md").write_text(
            "---\ntags:\n  - resource\n  - skill\n"
            "keywords:\n  - a\n  - b\n  - c\ntopics:\n  - X\n"
            "language: markdown\ndate of note: 2026-07-25\nstatus: active\n"
            "building_block: procedure\naccess_control_group: [\"general\"]\n---\n\n"
            f"# {name}\n\n## Do it <!-- :: section_id = step_1 :: -->\n\n"
            "```yaml\nrole: CORE\n"
            f"aggregation: {aggregation}\nbatchable: false\ndepends_on: []\n"
            f"materializer: {materializer}\noutput_key: {output_key}\n"
            "expected_output_schema:\n  type: object\n"
            f"  required: [{req}]\n```\n\n{prompt}\n",
            encoding="utf-8",
        )

    _skill("skill_tessellum_plan_digestion", output_key="plan_out",
           required=["plan_path"],
           prompt="Plan sub {{leaf.sub_id}} members:\n{{leaf.members}}")
    _skill("skill_tessellum_augment_digestion_plan", output_key="augment_out",
           required=["plan_text"])
    _skill("skill_tessellum_review_digestion_plan", output_key="verdict",
           required=["ready"], prompt="Review sub {{leaf.sub_id}}")
    _skill("skill_tessellum_execute_digestion_plan", output_key="exec_out",
           required=["output_path", "body_markdown"],
           materializer="body_markdown_to_file", aggregation="per_leaf",
           prompt="Execute sub {{leaf.sub_id}}")


def _mock(ready: bool = True) -> MockBackend:
    return MockBackend(default=json.dumps({
        "plan_path": "plans/p.md", "plan_text": "# Plan",
        "ready": ready, "failures": [] if ready else ["forced reject"],
        "output_path": "notes/n.md", "body_markdown": "# N",
        "total_notes": 2,
    }))


def _bundle(n: int) -> SourceBundle:
    return SourceBundle(
        bundle_id="corpus-bundle",
        objective="digest the corpus",
        members=tuple(
            BundleMember(source_id=f"j{i}", ordinal=i, ref=f"/inbox/d{i}.md",
                         parser_id="md", extracted_text_hash=f"h{i}")
            for i in range(n)
        ),
    )


def _corpus_plan(n_members: int) -> CorpusPlan:
    # two sub-objectives partitioning the bundle: s1 owns [0..half), s2 the rest.
    half = n_members // 2
    return CorpusPlan(
        bundle_id="corpus-bundle",
        objective="digest the corpus",
        sub_objectives=(
            SubObjective(sub_id="s1", topic="foundations", priority="P1",
                         member_ordinals=tuple(range(half)), est_note_count=4),
            SubObjective(sub_id="s2", topic="advanced", priority="P2",
                         member_ordinals=tuple(range(half, n_members)),
                         est_note_count=4, depends_on=("s1",)),
        ),
        bundle_member_count=n_members,
    )


# ── the wave ────────────────────────────────────────────────────────────────


def test_all_sub_objectives_accepted(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    plan = _corpus_plan(4)
    contents = {i: f"content of doc {i}" for i in range(4)}
    res = run_corpus_planning_wave(
        plan, b, contents, skills_dir=sd, backend=_mock(ready=True),
        vault_root=tmp_path / "vault",
    )
    assert res.all_accepted
    assert res.accepted_count == 2 and res.blocked_count == 0
    assert [o.sub_id for o in res.sub_plans] == ["s1", "s2"]
    assert all(o.status == "accepted" and o.plan_doc for o in res.sub_plans)


def test_each_sub_plan_sees_only_its_slice(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    plan = _corpus_plan(4)  # s1 → ordinals 0,1 ; s2 → 2,3
    contents = {i: f"UNIQUE_DOC_{i}" for i in range(4)}
    backend = _mock(ready=True)
    run_corpus_planning_wave(plan, b, contents, skills_dir=sd, backend=backend,
                             vault_root=tmp_path / "vault")
    # Collect the plan-phase prompts (one per sub-objective, in order). Each
    # sub-plan's prompt must contain ONLY its own members' refs/content.
    plan_prompts = [c.user_prompt for c in backend.calls if "Plan sub" in c.user_prompt]
    assert len(plan_prompts) == 2
    s1_prompt, s2_prompt = plan_prompts
    assert "/inbox/d0.md" in s1_prompt and "/inbox/d1.md" in s1_prompt
    assert "/inbox/d2.md" not in s1_prompt and "/inbox/d3.md" not in s1_prompt
    assert "/inbox/d2.md" in s2_prompt and "/inbox/d3.md" in s2_prompt
    assert "/inbox/d0.md" not in s2_prompt and "/inbox/d1.md" not in s2_prompt


def test_rejected_sub_objective_blocks_only_itself(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    plan = _corpus_plan(4)

    # Reject s2 only: the review skill's prompt renders "Review sub {{leaf.sub_id}}",
    # so a prompt-pattern MockBackend returns a NOT-ready verdict for the
    # "Review sub s2" prompt and the default ready verdict for everything else.
    backend = MockBackend(
        default=json.dumps({
            "plan_path": "plans/p.md", "plan_text": "# Plan",
            "ready": True, "failures": [],
            "output_path": "notes/n.md", "body_markdown": "# N", "total_notes": 2,
        }),
        responses={
            "Review sub s2": json.dumps({
                "plan_path": "plans/p.md", "plan_text": "# Plan",
                "ready": False, "failures": ["s2 rejected"],
                "output_path": "notes/n.md", "body_markdown": "# N", "total_notes": 2,
            }),
        },
    )
    contents = {i: f"doc {i}" for i in range(4)}
    res = run_corpus_planning_wave(plan, b, contents, skills_dir=sd,
                                   backend=backend, vault_root=tmp_path / "vault")
    by_id = {o.sub_id: o for o in res.sub_plans}
    assert by_id["s1"].accepted and by_id["s1"].status == "accepted"
    assert not by_id["s2"].accepted and by_id["s2"].status == "blocked"
    assert res.accepted_count == 1 and res.blocked_count == 1
    assert not res.all_accepted
    assert by_id["s2"].reason and "sign-off" in by_id["s2"].reason


def test_planning_wave_writes_no_note_files(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    vault = tmp_path / "vault"
    b = _bundle(4)
    plan = _corpus_plan(4)
    contents = {i: f"doc {i}" for i in range(4)}
    res = run_corpus_planning_wave(plan, b, contents, skills_dir=sd,
                                   backend=_mock(), vault_root=vault)
    # (a) execute-SKIPPED contract (not just file-absence): every accepted
    # sub-plan stopped at review_accepted and NO execute phase ran.
    for o in res.sub_plans:
        assert o.result is not None
        assert o.result.stopped_at == "review_accepted"
        assert not any(p.phase == "execute" for p in o.result.phases if p.ran)
    # (b) and, consequently, no note files materialized.
    written = list(vault.rglob("*.md")) if vault.exists() else []
    assert written == [], f"planning wave should write no notes, found {written}"


def test_slice_time_failure_blocks_only_that_sub_objective(tmp_path: Path) -> None:
    # Review (medium): slice/leaf construction is INSIDE the try, so a
    # slice-time failure of ONE sub-objective (here: a member with content so
    # large that build_corpus_leaf cannot fit even its scaffolding under the
    # per-sub budget is NOT the trigger; instead force an out-of-content
    # member) blocks only that sub-objective — the others still plan.
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    plan = _corpus_plan(4)  # s1 → 0,1 ; s2 → 2,3
    # Omit content for a member s2 owns → _slice_contents raises for s2 only.
    contents = {0: "doc0", 1: "doc1", 2: "doc2"}  # missing ordinal 3 (s2's)
    res = run_corpus_planning_wave(plan, b, contents, skills_dir=sd,
                                   backend=_mock(), vault_root=tmp_path / "vault")
    by_id = {o.sub_id: o for o in res.sub_plans}
    assert by_id["s1"].accepted, "s1 has all its content → should plan fine"
    assert not by_id["s2"].accepted and by_id["s2"].status == "blocked"
    assert by_id["s2"].result is None  # blocked before a result was produced
    assert by_id["s2"].reason and "planning raised" in by_id["s2"].reason
    assert res.accepted_count == 1 and res.blocked_count == 1


def test_shared_cross_refs_threaded_to_each_sub_plan(tmp_path: Path) -> None:
    # The corpus's shared cross-references (M7) must reach EVERY sub-plan's
    # planning leaf with the correct shape ({target, relationship}). The plan
    # skill reads {{leaf.shared_cross_refs}}; assert both members' targets +
    # relationships render into each sub-plan's plan prompt.
    from tessellum.composer import SharedCrossRef

    sd = tmp_path / "skills"
    sd.mkdir()
    # a plan skill that echoes the shared cross-refs so we can observe them.
    _write_phase_skills(sd)
    (sd / "skill_tessellum_plan_digestion.md").write_text(
        (sd / "skill_tessellum_plan_digestion.md").read_text(encoding="utf-8").replace(
            "Plan sub {{leaf.sub_id}} members:\n{{leaf.members}}",
            "Plan sub {{leaf.sub_id}} xrefs:\n{{leaf.shared_cross_refs}}",
        ),
        encoding="utf-8",
    )
    b = _bundle(4)
    plan = _corpus_plan(4).model_copy(update={
        "shared_cross_refs": (
            SharedCrossRef(target="term_dag", relationship="uses"),
            SharedCrossRef(target="term_cqrs", relationship="separates"),
        ),
    })
    backend = _mock()
    run_corpus_planning_wave(plan, b, {i: f"doc {i}" for i in range(4)},
                             skills_dir=sd, backend=backend,
                             vault_root=tmp_path / "vault")
    plan_prompts = [c.user_prompt for c in backend.calls if "xrefs" in c.user_prompt]
    assert len(plan_prompts) == 2  # one per sub-objective
    for p in plan_prompts:
        # correct shape reaches the sub-planner (guards against a shape/omission
        # regression the mutation probe exposed).
        assert "term_dag" in p and "uses" in p
        assert "term_cqrs" in p and "separates" in p
        assert "target" in p and "relationship" in p
        assert "<missing" not in p


def test_bundle_id_mismatch_fails_loud(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    plan = _corpus_plan(4).model_copy(update={"bundle_id": "different-bundle"})
    try:
        run_corpus_planning_wave(plan, b, {i: "x" for i in range(4)},
                                 skills_dir=sd, backend=_mock(),
                                 vault_root=tmp_path / "vault")
        raise AssertionError("expected ValueError on bundle_id mismatch")
    except ValueError as exc:
        assert "does not match" in str(exc)


def test_stop_after_review_returns_accepted(tmp_path: Path) -> None:
    # Directly exercise the new stop_after="review" contract on the single-plan
    # pipeline: an approved plan returns completed=True, stopped_at=review_accepted,
    # and does not execute.
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    result = run_digestion_pipeline(
        skills_dir=sd,
        source_leaf={"_id": "x", "plan_path": "plans/p.md", "total_notes": 2},
        backend=_mock(), vault_root=tmp_path / "vault", stop_after="review",
    )
    assert result.completed
    assert result.stopped_at == "review_accepted"
    assert not any(p.phase == "execute" for p in result.phases if p.ran)


# ── M4: corpus execute wave (per-sub-plan transactions) ─────────────────────


def test_corpus_digestion_all_promoted(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    vault = tmp_path / "vault"
    b = _bundle(4)
    plan = _corpus_plan(4)
    contents = {i: f"doc {i}" for i in range(4)}
    res = run_corpus_digestion(plan, b, contents, skills_dir=sd, backend=_mock(),
                               vault_root=vault)
    assert res.bundle_status == "complete"
    assert res.planning.all_accepted
    assert len(res.executions) == 2
    assert all(e.promoted and e.status == "promoted" for e in res.executions)
    # execute actually ran now (unlike the planning-only wave) → notes written.
    assert list(vault.rglob("*.md")), "execute wave should materialize notes"


def test_corpus_digestion_partial_when_one_sub_blocked_at_planning(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    plan = _corpus_plan(4)
    # reject s2 at planning (review not-ready) → only s1 promotes.
    backend = MockBackend(
        default=json.dumps({
            "plan_path": "plans/p.md", "plan_text": "# Plan", "ready": True,
            "failures": [], "output_path": "notes/n.md", "body_markdown": "# N",
            "total_notes": 2,
        }),
        responses={
            "Review sub s2": json.dumps({
                "plan_path": "plans/p.md", "plan_text": "# Plan", "ready": False,
                "failures": ["s2 rejected"], "output_path": "notes/n.md",
                "body_markdown": "# N", "total_notes": 2,
            }),
        },
    )
    res = run_corpus_digestion(plan, b, {i: f"doc {i}" for i in range(4)},
                               skills_dir=sd, backend=backend, vault_root=tmp_path / "vault")
    assert res.bundle_status == "partially_promoted"
    # only the accepted sub-plan (s1) is executed; s2 (blocked at planning) is not.
    assert [e.sub_id for e in res.executions] == ["s1"]
    assert res.executions[0].promoted


def test_corpus_digestion_executes_in_wave_order(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    # s2 is P1, s1 is P2 → wave order must put s2 (foundational) FIRST despite id.
    plan = CorpusPlan(
        bundle_id="corpus-bundle", objective="digest the corpus",
        sub_objectives=(
            SubObjective(sub_id="s1", topic="ops", priority="P2",
                         member_ordinals=(0, 1), est_note_count=2),
            SubObjective(sub_id="s2", topic="foundations", priority="P1",
                         member_ordinals=(2, 3), est_note_count=2),
        ),
        bundle_member_count=4,
    )
    res = run_corpus_digestion(plan, b, {i: f"doc {i}" for i in range(4)},
                               skills_dir=sd, backend=_mock(), vault_root=tmp_path / "vault")
    assert res.bundle_status == "complete"
    assert [e.sub_id for e in res.executions] == ["s2", "s1"]  # P1 before P2


def test_corpus_gate_human_rejection_promotes_nothing(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    vault = tmp_path / "vault"
    b = _bundle(4)
    plan = _corpus_plan(4)  # 2 sub-plans × total_notes 2 = 4 blast
    # threshold below total blast + human rejects → nothing promoted.
    policy = SignOffPolicy(use_human=True, blast_radius_threshold=1)
    res = run_corpus_digestion(
        plan, b, {i: f"doc {i}" for i in range(4)}, skills_dir=sd,
        backend=_mock(), vault_root=vault,
        corpus_sign_off_policy=policy, human_prompt=lambda: False,
    )
    assert res.bundle_status == "blocked"
    assert res.corpus_sign_off is not None
    assert res.corpus_sign_off.decision == "rejected"
    assert res.executions == ()
    assert not list(vault.rglob("*.md")), "rejected corpus must promote nothing"


def test_corpus_gate_human_approval_promotes(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    vault = tmp_path / "vault"
    b = _bundle(4)
    plan = _corpus_plan(4)
    policy = SignOffPolicy(use_human=True, blast_radius_threshold=1)
    res = run_corpus_digestion(
        plan, b, {i: f"doc {i}" for i in range(4)}, skills_dir=sd,
        backend=_mock(), vault_root=vault,
        corpus_sign_off_policy=policy, human_prompt=lambda: True,
    )
    assert res.corpus_sign_off is not None
    assert res.corpus_sign_off.decision == "approved"
    assert res.corpus_sign_off.deciding_rung == "human"
    assert res.bundle_status == "complete"
    assert list(vault.rglob("*.md")), "approved corpus must promote (write notes)"


def test_corpus_high_blast_needs_human_without_prompt_blocks(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    vault = tmp_path / "vault"
    b = _bundle(4)
    plan = _corpus_plan(4)
    # human rung requested for high blast but NO prompt wired → needs_human, blocked.
    policy = SignOffPolicy(use_human=True, blast_radius_threshold=1)
    res = run_corpus_digestion(
        plan, b, {i: f"doc {i}" for i in range(4)}, skills_dir=sd,
        backend=_mock(), vault_root=vault,
        corpus_sign_off_policy=policy, human_prompt=None,
    )
    assert res.corpus_sign_off is not None
    assert res.corpus_sign_off.decision == "needs_human"
    assert res.bundle_status == "blocked"
    assert res.executions == ()
    assert not list(vault.rglob("*.md")), "needs_human corpus must promote nothing"


def test_corpus_gate_low_blast_use_human_auto_approves(tmp_path: Path) -> None:
    # Low total blast + use_human → the else-branch auto-approves at the program
    # rung WITHOUT prompting the human (no needless escalation).
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    plan = _corpus_plan(4)  # total blast = 4
    prompted = {"called": False}

    def _human() -> bool:
        prompted["called"] = True
        return True

    policy = SignOffPolicy(use_human=True, blast_radius_threshold=100)  # above 4
    res = run_corpus_digestion(
        plan, b, {i: f"doc {i}" for i in range(4)}, skills_dir=sd,
        backend=_mock(), vault_root=tmp_path / "vault",
        corpus_sign_off_policy=policy, human_prompt=_human,
    )
    assert res.corpus_sign_off is not None
    assert res.corpus_sign_off.decision == "approved"
    assert res.corpus_sign_off.deciding_rung == "program"
    assert not prompted["called"], "low-blast corpus must NOT prompt the human"
    assert res.bundle_status == "complete"


def test_corpus_term_ownership_gate_blocks_on_unowned_term(tmp_path: Path) -> None:
    # M6: an introduced term with no owner sub-objective blocks the WHOLE corpus
    # before any promotion (fail-closed) — nothing written.
    from tessellum.composer import TermOwnerRow

    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    vault = tmp_path / "vault"
    b = _bundle(4)
    # s1 owns term_x; term_y is introduced but owned by nobody.
    plan = _corpus_plan(4).model_copy(update={
        "term_ownership": (TermOwnerRow(term="term_x", owner_sub_id="s1"),),
    })
    backend = _mock()
    res = run_corpus_digestion(
        plan, b, {i: f"doc {i}" for i in range(4)}, skills_dir=sd,
        backend=backend, vault_root=vault,
        introduced_terms=("term_x", "term_y"),
    )
    assert res.bundle_status == "blocked"
    assert res.term_ownership is not None
    assert not res.term_ownership.passed
    assert res.term_ownership.unowned == ("term_y",)
    assert res.executions == ()
    assert not list(vault.rglob("*.md")), "term-gate failure must promote nothing"
    # M6 review (low): the gate runs BEFORE the planning wave, so a blocked
    # corpus pays ZERO planning-wave LLM cost (no backend calls) and the
    # planning result is empty.
    assert backend.calls == [], "term gate must fail fast before any LLM call"
    assert res.planning.sub_plans == ()


def test_corpus_term_ownership_gate_passes_and_promotes(tmp_path: Path) -> None:
    from tessellum.composer import TermOwnerRow

    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    plan = _corpus_plan(4).model_copy(update={
        "term_ownership": (
            TermOwnerRow(term="term_x", owner_sub_id="s1"),
            TermOwnerRow(term="term_y", owner_sub_id="s2"),
        ),
    })
    res = run_corpus_digestion(
        plan, b, {i: f"doc {i}" for i in range(4)}, skills_dir=sd,
        backend=_mock(), vault_root=tmp_path / "vault",
        introduced_terms=("term_x", "term_y"),
    )
    assert res.term_ownership is not None and res.term_ownership.passed
    assert res.bundle_status == "complete"


def test_corpus_shared_cross_refs_resolved_once_and_threaded(tmp_path: Path) -> None:
    # M7: shared cross-refs are resolved ONCE at corpus scope (existence-filtered
    # + deduped) and the RESOLVED set is threaded into every sub-plan — a missing
    # ref is dropped, not re-linked in N sub-plans.
    from tessellum.composer import SharedCrossRef

    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    # plan skill echoes the threaded shared_cross_refs so we can observe them.
    (sd / "skill_tessellum_plan_digestion.md").write_text(
        (sd / "skill_tessellum_plan_digestion.md").read_text(encoding="utf-8").replace(
            "Plan sub {{leaf.sub_id}} members:\n{{leaf.members}}",
            "Plan sub {{leaf.sub_id}} xrefs:\n{{leaf.shared_cross_refs}}",
        ),
        encoding="utf-8",
    )
    b = _bundle(4)
    plan = _corpus_plan(4).model_copy(update={
        "shared_cross_refs": (
            SharedCrossRef(target="term_real", relationship="uses"),
            SharedCrossRef(target="term_ghost", relationship="x"),
            SharedCrossRef(target="term_real", relationship="dup"),
        ),
    })
    backend = _mock()
    res = run_corpus_digestion(
        plan, b, {i: f"doc {i}" for i in range(4)}, skills_dir=sd,
        backend=backend, vault_root=tmp_path / "vault",
        shared_cross_ref_exists=lambda t: t == "term_real",
    )
    # resolution report on the result: ghost dropped, dup collapsed.
    assert res.shared_cross_refs is not None
    assert [r.target for r in res.shared_cross_refs.resolved] == ["term_real"]
    assert res.shared_cross_refs.dropped_missing == ("term_ghost",)
    assert res.shared_cross_refs.dropped_duplicate == ("term_real",)
    # every sub-plan's plan prompt carries ONLY the resolved ref (no ghost).
    plan_prompts = [c.user_prompt for c in backend.calls if "xrefs" in c.user_prompt]
    assert len(plan_prompts) == 2
    for p in plan_prompts:
        assert "term_real" in p
        assert "term_ghost" not in p


def test_corpus_no_term_gate_when_introduced_terms_omitted(tmp_path: Path) -> None:
    # M6 is opt-in: without introduced_terms the gate does not run (term_ownership
    # is None) and the corpus digests as in M4/M5.
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    plan = _corpus_plan(4)
    res = run_corpus_digestion(plan, b, {i: f"doc {i}" for i in range(4)},
                               skills_dir=sd, backend=_mock(),
                               vault_root=tmp_path / "vault")
    assert res.term_ownership is None
    assert res.bundle_status == "complete"


def test_write_closure_overlap_detects_shared_note() -> None:
    # unit: two sub-plan outcomes whose note_intent_graphs write the SAME note
    # are both reported as overlapping (the M5 disjointness gate input).
    from tessellum.composer.corpus_digestion import (
        SubPlanOutcome,
        _write_closure_overlaps,
    )

    def _graph(note_id: str) -> dict:
        return {
            "objective_id": "obj",
            "intents": [{
                "note_id": note_id, "thesis": "t", "building_block": "concept",
                "target_path": f"areas/{note_id}.md",
                "provenance": [{"span_id": "s", "source_ref": "r"}],
            }],
        }

    # s1 and s2 both write note "shared"; s3 writes "unique".
    s1 = SubPlanOutcome(sub_id="s1", priority="P1", accepted=True,
                        status="accepted", plan_doc={"note_intent_graph": _graph("shared")})
    s2 = SubPlanOutcome(sub_id="s2", priority="P1", accepted=True,
                        status="accepted", plan_doc={"note_intent_graph": _graph("shared")})
    s3 = SubPlanOutcome(sub_id="s3", priority="P1", accepted=True,
                        status="accepted", plan_doc={"note_intent_graph": _graph("unique")})
    overlaps = _write_closure_overlaps([s1, s2, s3])
    assert set(overlaps) == {"s1", "s2"}  # s3 disjoint → not flagged
    assert "shared" in overlaps["s1"] and "shared" in overlaps["s2"]


def test_write_closure_overlap_abstains_on_prose_fallback() -> None:
    # a sub-plan with no typed note_intent_graph (prose fallback) can't be proven
    # to conflict → the gate abstains (does not block it).
    from tessellum.composer.corpus_digestion import (
        SubPlanOutcome,
        _write_closure_overlaps,
    )
    a = SubPlanOutcome(sub_id="a", priority="P1", accepted=True, status="accepted",
                       plan_doc={"plan_path": "plans/a.md"})  # no graph
    b = SubPlanOutcome(sub_id="b", priority="P1", accepted=True, status="accepted",
                       plan_doc={"plan_path": "plans/b.md"})
    assert _write_closure_overlaps([a, b]) == {}


def test_corpus_isolates_run_scoped_execute_kwargs_per_sub_plan(tmp_path: Path) -> None:
    # M4 review (high): run-scoped execute kwargs (manifest / run_id /
    # events_path / stats_path) forwarded verbatim would collide across sibling
    # sub-plan waves. They must be uniquified per sub_id so each sub-plan is its
    # own transaction. Assert two sub-plans produce SEPARATE per-sub sidecars.
    from tessellum.composer import Manifest

    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    plan = _corpus_plan(4)  # s1, s2 both accepted
    manifest_path = tmp_path / "run.manifest.json"
    events_path = tmp_path / "run.events.jsonl"
    res = run_corpus_digestion(
        plan, b, {i: f"doc {i}" for i in range(4)}, skills_dir=sd,
        backend=_mock(), vault_root=tmp_path / "vault",
        manifest=Manifest(path=manifest_path), events_path=events_path,
        run_id="corpus-run",
    )
    assert res.bundle_status == "complete"
    # per-sub-plan manifests + event streams were written (not one clobbered file).
    assert (tmp_path / "run.manifest.s1.json").exists()
    assert (tmp_path / "run.manifest.s2.json").exists()
    assert (tmp_path / "run.events.s1.jsonl").exists()
    assert (tmp_path / "run.events.s2.jsonl").exists()


def test_isolate_execute_kwargs_uniquifies_by_sub_id() -> None:
    # unit: the helper rewrites run-scoped keys and passes others through.
    from tessellum.composer import Manifest
    from tessellum.composer.corpus_digestion import _isolate_execute_kwargs

    kw = {
        "run_id": "R",
        "events_path": Path("/tmp/x/run.events.jsonl"),
        "stats_path": Path("/tmp/x/run.stats.json"),
        "manifest": Manifest(path=Path("/tmp/x/run.manifest.json")),
        "max_fix_rounds": 3,  # passthrough
    }
    out = _isolate_execute_kwargs(kw, "sA")
    assert out["run_id"] == "R:sA"
    assert out["events_path"].name == "run.events.sA.jsonl"
    assert out["stats_path"].name == "run.stats.sA.json"
    assert Path(out["manifest"].path).name == "run.manifest.sA.json"
    assert out["max_fix_rounds"] == 3
    # input not mutated
    assert kw["run_id"] == "R"
    # empty kwargs → same object (fast path)
    assert _isolate_execute_kwargs({}, "sA") == {}


def test_corpus_concurrent_within_layer_preserves_order_and_promotes(tmp_path: Path) -> None:
    # M5: two dependency-INDEPENDENT sub-objectives (same first layer) run
    # concurrently (max_sub_plan_workers>1); the execution result list stays in
    # the layer's deterministic order and both promote.
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    # s1 and s2 both P1, no deps → one layer {s1, s2}.
    plan = CorpusPlan(
        bundle_id="corpus-bundle", objective="digest the corpus",
        sub_objectives=(
            SubObjective(sub_id="s1", topic="a", priority="P1",
                         member_ordinals=(0, 1), est_note_count=2),
            SubObjective(sub_id="s2", topic="b", priority="P1",
                         member_ordinals=(2, 3), est_note_count=2),
        ),
        bundle_member_count=4,
    )
    res = run_corpus_digestion(plan, b, {i: f"doc {i}" for i in range(4)},
                               skills_dir=sd, backend=_mock(),
                               vault_root=tmp_path / "vault",
                               max_sub_plan_workers=4)
    assert res.bundle_status == "complete"
    # deterministic order preserved despite concurrency (P1 s1 before P1 s2).
    assert [e.sub_id for e in res.executions] == ["s1", "s2"]
    assert all(e.promoted for e in res.executions)


def test_corpus_dependent_layer_runs_after_dependency(tmp_path: Path) -> None:
    # M5: a chain s1 -> s2 -> s3 executes strictly in dependency order across
    # layers, even with concurrency enabled (each layer is a singleton).
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(3)
    plan = CorpusPlan(
        bundle_id="corpus-bundle", objective="digest the corpus",
        sub_objectives=(
            SubObjective(sub_id="s1", topic="a", priority="P1",
                         member_ordinals=(0,), est_note_count=1),
            SubObjective(sub_id="s2", topic="b", priority="P1",
                         member_ordinals=(1,), est_note_count=1, depends_on=("s1",)),
            SubObjective(sub_id="s3", topic="c", priority="P1",
                         member_ordinals=(2,), est_note_count=1, depends_on=("s2",)),
        ),
        bundle_member_count=3,
    )
    res = run_corpus_digestion(plan, b, {i: f"doc {i}" for i in range(3)},
                               skills_dir=sd, backend=_mock(),
                               vault_root=tmp_path / "vault",
                               max_sub_plan_workers=4)
    assert res.bundle_status == "complete"
    assert [e.sub_id for e in res.executions] == ["s1", "s2", "s3"]


def test_corpus_execute_error_blocks_only_that_sub_plan(tmp_path: Path) -> None:
    # M4 headline invariant: an accepted sub-plan whose EXECUTE wave errors is
    # blocked while the others still promote. Drive s1's execute step to emit
    # invalid output (missing required body_markdown) via a prompt-pattern mock.
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_phase_skills(sd)
    b = _bundle(4)
    plan = _corpus_plan(4)
    backend = MockBackend(
        default=json.dumps({
            "plan_path": "plans/p.md", "plan_text": "# Plan", "ready": True,
            "failures": [], "output_path": "notes/n.md", "body_markdown": "# N",
            "total_notes": 2,
        }),
        responses={
            # s1's execute step: missing required body_markdown → materializer/schema error.
            "Execute sub s1": json.dumps({"output_path": "notes/n.md"}),
        },
    )
    res = run_corpus_digestion(plan, b, {i: f"doc {i}" for i in range(4)},
                               skills_dir=sd, backend=backend,
                               vault_root=tmp_path / "vault")
    by_id = {e.sub_id: e for e in res.executions}
    assert set(by_id) == {"s1", "s2"}  # both accepted at planning, both attempted
    assert not by_id["s1"].promoted and by_id["s1"].status == "blocked"
    assert by_id["s2"].promoted and by_id["s2"].status == "promoted"
    assert res.bundle_status == "partially_promoted"
