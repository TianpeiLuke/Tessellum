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
    SubObjective,
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
           materializer="body_markdown_to_file", aggregation="per_leaf")


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
    run_corpus_planning_wave(plan, b, contents, skills_dir=sd, backend=_mock(),
                             vault_root=vault)
    # stop_after="review" → planning only; no note files materialized.
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
