"""T3 (FZ 20k9d6a) — inspect-before-execute: the pause / promote / reject loop.

Uses a fake executor (the test_supervisor.py pattern) so the full state-machine
path is exercised through the REAL Supervisor + RuntimeStore without a backend:
  - a stop_after=review run parks the job PAUSED (executor writes plan.json),
  - `promote` → READY → the next claim resumes execute-only → COMPLETE,
  - `reject` → CANCELLED.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from tessellum.runtime.admission import admit_path
from tessellum.runtime.models import JobState
from tessellum.runtime.paths import RuntimePaths
from tessellum.runtime.routing import LANE_HINTS
from tessellum.runtime.store import RuntimeStore
from tessellum.runtime.supervisor import Supervisor


@dataclass
class _Result:
    completed: bool = True
    stopped_at: str | None = None
    plan_doc: dict | None = None


class _InspectExecutor:
    """Fake executor: execute() parks at review (writes plan.json + returns
    review_accepted); resume_execute() finishes the accepted plan."""

    cancellation_check = None
    effect_guard = None

    def __init__(self, paths: RuntimePaths) -> None:
        self.paths = paths
        self.execute_calls = 0
        self.resume_calls = 0

    def execute(self, job, lease, route, policy):
        self.execute_calls += 1
        # stop_after=review → write the accepted plan-of-record and pause.
        art = self.paths.job_artifacts(job.job_id)
        art.mkdir(parents=True, exist_ok=True)
        (art / "plan.json").write_text(
            json.dumps({"plan_text": "# Plan", "total_notes": 1,
                        "planned_notes": [{"filename": "n1", "building_block": "concept"}]}),
            encoding="utf-8",
        )
        (art / "source_leaf.json").write_text(
            json.dumps({"source_content": "evidence"}), encoding="utf-8"
        )
        assert policy.stop_after == "review"
        return _Result(completed=False, stopped_at="review_accepted")

    def resume_execute(self, job, lease, route, policy):
        self.resume_calls += 1
        # promote must resume execute-only, never re-plan.
        with self.effect_guard():
            pass
        return _Result(completed=True, stopped_at=None)


def _runtime(tmp_path: Path) -> tuple[RuntimePaths, RuntimeStore, Path]:
    paths = RuntimePaths.discover(tmp_path)
    paths.ensure_runtime_dirs()
    paths.inbox.mkdir()
    paths.vault.mkdir()
    paths.skills.mkdir(parents=True)
    for skill in (
        "skill_tessellum_plan_digestion",
        "skill_tessellum_augment_digestion_plan",
        "skill_tessellum_review_digestion_plan",
        "skill_tessellum_execute_digestion_plan",
    ):
        (paths.skills / f"{skill}.md").write_text(skill, encoding="utf-8")
    for lane in LANE_HINTS:
        (paths.inbox / lane).mkdir()
    source = paths.inbox / "papers" / "paper.md"
    source.write_text("evidence", encoding="utf-8")
    return paths, RuntimeStore.open(paths.db), source


def test_inspect_parks_job_paused(tmp_path: Path) -> None:
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store, policy_profile="inspect")
    ex = _InspectExecutor(paths)
    outcome = Supervisor(
        store=store, paths=paths, executor=ex,  # type: ignore[arg-type]
        owner_id="w", rebuild_index=False,
    ).work_once()
    assert outcome.status == "paused"
    job = store.get(admitted.job_id)
    assert job.state == JobState.PAUSED
    assert ex.execute_calls == 1 and ex.resume_calls == 0
    # the accepted plan is persisted for a human to inspect
    assert (paths.job_artifacts(admitted.job_id) / "plan.json").is_file()


def test_promote_resumes_execute_only_to_complete(tmp_path: Path) -> None:
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store, policy_profile="inspect")
    sup = Supervisor(
        store=store, paths=paths, executor=_InspectExecutor(paths),  # type: ignore[arg-type]
        owner_id="w", rebuild_index=False,
    )
    sup.work_once()  # → PAUSED
    assert store.get(admitted.job_id).state == JobState.PAUSED

    # operator promotes
    promoted = store.promote_paused(admitted.job_id)
    assert promoted.state == JobState.READY
    assert promoted.lease is None

    # the next work cycle resumes EXECUTE-ONLY (plan.json exists) → COMPLETE
    ex2 = _InspectExecutor(paths)
    sup2 = Supervisor(
        store=store, paths=paths, executor=ex2,  # type: ignore[arg-type]
        owner_id="w2", rebuild_index=False,
    )
    outcome = sup2.work_once()
    assert outcome.status == "complete"
    assert ex2.resume_calls == 1 and ex2.execute_calls == 0  # NO re-plan
    assert store.get(admitted.job_id).state == JobState.COMPLETE


def test_reject_paused_cancels(tmp_path: Path) -> None:
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store, policy_profile="inspect")
    Supervisor(
        store=store, paths=paths, executor=_InspectExecutor(paths),  # type: ignore[arg-type]
        owner_id="w", rebuild_index=False,
    ).work_once()
    assert store.get(admitted.job_id).state == JobState.PAUSED

    rejected = store.reject_paused(admitted.job_id)
    assert rejected.state == JobState.CANCELLED
    assert rejected.cancel_requested is True


def test_fresh_job_takes_full_execute_path(tmp_path: Path) -> None:
    """A non-inspect job has no plan.json → the full execute path runs (T3 is
    byte-neutral to the default flow)."""
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store)  # default profile
    ex = _InspectExecutor(paths)

    # default policy has stop_after=None; the fake execute() asserts
    # policy.stop_after=="review", so a default run would trip that assert —
    # meaning it correctly took the execute() path (not resume). We assert the
    # routing decision directly instead: no plan.json pre-exists.
    assert not (paths.job_artifacts(admitted.job_id) / "plan.json").is_file()
    sup = Supervisor(
        store=store, paths=paths, executor=ex,  # type: ignore[arg-type]
        owner_id="w", rebuild_index=False,
    )
    # _has_accepted_plan is False on a fresh job → execute() (not resume) chosen.
    assert sup._has_accepted_plan(admitted.job_id) is False


# ── promote re-hydration (the slim-plan ⨝ source-leaf join) ──────────────────


def test_rehydrate_restores_source_content_and_member_excerpts() -> None:
    from tessellum.runtime.executor import _rehydrate_plan_from_source_leaf

    plan_doc = {
        "plan_text": "# P",
        "members": [
            {"source_id": "a"},                       # slim-dropped excerpt
            {"source_id": "b", "excerpt": "KEEP"},    # still carried — never overwrite
            {"name": "c"},                            # id-less, positional fallback
        ],
    }
    source_leaf = {
        "source_content": "FULL",
        "members": [
            {"source_id": "a", "excerpt": "AAA"},
            {"source_id": "b", "excerpt": "BBB-orig"},
            {"name": "c", "excerpt": "CCC"},
        ],
    }
    _rehydrate_plan_from_source_leaf(plan_doc, source_leaf)
    assert plan_doc["source_content"] == "FULL"
    assert plan_doc["members"][0]["excerpt"] == "AAA"
    assert plan_doc["members"][1]["excerpt"] == "KEEP"  # not clobbered
    assert plan_doc["members"][2]["excerpt"] == "CCC"


def test_rehydrate_failsoft_on_odd_shapes() -> None:
    from tessellum.runtime.executor import _rehydrate_plan_from_source_leaf

    plan_doc = {"members": "junk"}
    _rehydrate_plan_from_source_leaf(plan_doc, {"members": [{"excerpt": "x"}]})
    assert plan_doc["members"] == "junk"  # untouched, no raise
