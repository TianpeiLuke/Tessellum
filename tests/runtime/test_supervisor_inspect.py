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
                        "planned_notes": [{"filename": "n1", "building_block": "concept"}],
                        # F14: the real executor stamps acceptance on the dump;
                        # the routing check requires it (presence != approval).
                        "_sign_off": {"accepted": True, "decision": "approved",
                                      "stopped_at": "review_accepted",
                                      "completed": True}}),
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


# ── J1+J2 (FZ 20k9c1a1a1b7c2k2): one episodic surface + one plan-of-record ───


def test_execute_wires_episodic_surface_and_artifact_refs(tmp_path, monkeypatch) -> None:
    """The REAL DigestionExecutor passes the job-dir episodic seams (runs/,
    artifacts/) to the pipeline (J1) and persists a refs-bearing plan.json
    whose digests match the durable of-record bytes (J2)."""
    import hashlib

    from tessellum.composer.digestion import DigestionResult
    from tessellum.runtime import executor as executor_mod
    from tessellum.runtime.executor import DigestionExecutor

    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store)
    captured: dict = {}

    def _stub_pipeline(**kwargs):
        captured.update(kwargs)
        return DigestionResult(
            completed=True, stopped_at=None, sign_off=None, phases=(),
            plan_doc={
                "plan_text": "# Accepted", "total_notes": 1,
                "planned_notes": [{"filename": "n1"}],
                "source_content": "evidence",
            },
        )

    monkeypatch.setattr(executor_mod, "run_digestion_pipeline", _stub_pipeline)
    ex = DigestionExecutor(paths=paths, backend=None)  # type: ignore[arg-type]  # never called — pipeline stubbed
    outcome = Supervisor(
        store=store, paths=paths, executor=ex,  # type: ignore[arg-type]
        owner_id="w", rebuild_index=False,
    ).work_once()
    assert outcome.status == "complete"
    art = paths.job_artifacts(admitted.job_id)
    # J1: the composer's episodic tier lands under the job's own dir.
    assert captured["runs_dir"] == art / "runs"
    assert captured["durable_artifact_dir"] == art / "artifacts"
    # J3: the revise loop is policy-gated (default 0 = single-pass).
    assert captured["max_review_rounds"] == 0
    # J2: plan.json carries digests of the of-record bytes the store paged.
    plan = json.loads((art / "plan.json").read_text(encoding="utf-8"))
    refs = plan["_artifact_refs"]
    expected = hashlib.sha256("# Accepted".encode("utf-8")).hexdigest()
    assert refs["plan_text"]["sha256"] == expected
    assert "source_content" not in plan  # the projection stays slim
    # A4.2: the COMMIT swept the fleeting working store (the Zettelkasten
    # discard) — the refs' digests remain in plan.json as provenance.
    assert not (art / "artifacts").exists()
    assert (art / "plan.json").is_file()  # the episodic record is retained


def _persisted_plan(tmp_path):
    """Build the REAL persist artifact set: a plan_doc paged via
    _slim_plan_with_refs, round-tripped through the exact plan.json
    serialization (sort_keys=True — dict key order changes vs the store's
    insertion-ordered bytes, which is what the parse-compare must absorb)."""
    from tessellum.runtime.executor import _slim_plan_with_refs

    art = tmp_path / "job-art"
    plan_doc = {
        "plan_text": "# Plan\nbody",
        "planned_notes": [{"zeta": 1, "alpha": 2, "filename": "n1"}],
        "pages": [{"page": "p1", "words": 10}],
        "total_notes": 1,
        "source_content": "SRC",
    }
    slim = _slim_plan_with_refs(plan_doc, art / "artifacts")
    reloaded = json.loads(json.dumps(slim, indent=2, sort_keys=True, default=str))
    return plan_doc, reloaded, art


def test_verify_roundtrip_passes_and_pops_refs(tmp_path) -> None:
    from tessellum.runtime.executor import _verify_plan_artifacts

    plan_doc, reloaded, art = _persisted_plan(tmp_path)
    _verify_plan_artifacts(reloaded, art)
    assert "_artifact_refs" not in reloaded  # never leaks into prompts
    assert reloaded["plan_text"] == plan_doc["plan_text"]
    assert reloaded["planned_notes"] == plan_doc["planned_notes"]


def test_verify_store_tamper_fails_closed(tmp_path) -> None:
    import pytest

    from tessellum.runtime.executor import DigestionIncompleteError, _verify_plan_artifacts

    _plan_doc, reloaded, art = _persisted_plan(tmp_path)
    (art / "artifacts" / "plan_text").write_text("TAMPERED", encoding="utf-8")
    with pytest.raises(DigestionIncompleteError, match="hash mismatch"):
        _verify_plan_artifacts(reloaded, art)


def test_verify_missing_artifact_fails_closed(tmp_path) -> None:
    import pytest

    from tessellum.runtime.executor import DigestionIncompleteError, _verify_plan_artifacts

    _plan_doc, reloaded, art = _persisted_plan(tmp_path)
    (art / "artifacts" / "plan_text").unlink()
    with pytest.raises(DigestionIncompleteError, match="unreadable"):
        _verify_plan_artifacts(reloaded, art)


def test_verify_projection_drift_fails_closed(tmp_path) -> None:
    import pytest

    from tessellum.runtime.executor import DigestionIncompleteError, _verify_plan_artifacts

    _plan_doc, reloaded, art = _persisted_plan(tmp_path)
    reloaded["plan_text"] = "# EDITED after approval"
    with pytest.raises(DigestionIncompleteError, match="drifted"):
        _verify_plan_artifacts(reloaded, art)


def test_verify_restores_missing_inline_from_store(tmp_path) -> None:
    from tessellum.runtime.executor import _verify_plan_artifacts

    plan_doc, reloaded, art = _persisted_plan(tmp_path)
    del reloaded["plan_text"]  # the projection lost the field
    _verify_plan_artifacts(reloaded, art)
    assert reloaded["plan_text"] == plan_doc["plan_text"]  # store is of-record


def test_converge_profile_enables_revise_loop() -> None:
    from tessellum.runtime.policy import RuntimePolicy

    policy = RuntimePolicy.for_profile("converge")
    assert policy.max_review_rounds == 2
    assert policy.stop_after is None
    # R2.4: detector constant — the renewal actor owns liveness, not the TTL
    assert policy.lease_ttl == RuntimePolicy().lease_ttl
    assert RuntimePolicy.for_profile("default").max_review_rounds == 0


def test_verify_noop_without_refs(tmp_path) -> None:
    from tessellum.runtime.executor import _verify_plan_artifacts

    plan_doc = {"plan_text": "# pre-J2 plan"}
    _verify_plan_artifacts(plan_doc, tmp_path)  # no _artifact_refs → no-op
    assert plan_doc == {"plan_text": "# pre-J2 plan"}


def test_heartbeat_context_releases_with_profile_ttl_immediately(tmp_path) -> None:
    """J3 finding 7: the claim lease uses the DEFAULT TTL; the heartbeat
    context must re-lease with the PROFILE TTL on entry, else a long-profile
    cadence (ttl/3) first fires after the short claim lease expired."""
    import time as _time

    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store, policy_profile="converge")
    job = store.claim_next("w", lease_ttl=120.0, max_attempts=3)
    assert job is not None and job.lease is not None
    sup = Supervisor(
        store=store, paths=paths, executor=_InspectExecutor(paths),  # type: ignore[arg-type]
        owner_id="w", rebuild_index=False,
    )
    with sup._heartbeat(job.job_id, job.lease, 900.0):
        row = store.get(job.job_id)
        assert row.lease is not None
        # extended to ~now+900 immediately, not left at the 120s claim window
        assert row.lease.expires_at - _time.time() > 600.0


# ── F14 (FZ 20k9c1a1a1b7c2k2a3a — run 10's resume): presence != approval ────


def test_halted_plan_dump_does_not_route_to_resume_execute(tmp_path: Path) -> None:
    """F14 regression: a crashed attempt's forensic plan.json (no acceptance
    stamp / accepted=false) must NOT satisfy the routing check — the re-claim
    takes the FULL pipeline, where review + sign-off actually run. Run 10's
    resume executed an unreviewed plan through the old existence check."""
    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store, policy_profile="inspect")
    art = paths.job_artifacts(admitted.job_id)
    art.mkdir(parents=True, exist_ok=True)
    sup = Supervisor(
        store=store, paths=paths, executor=_InspectExecutor(paths),  # type: ignore[arg-type]
        owner_id="w", rebuild_index=False,
    )
    # the halted-run dump: full plan content, negative stamp
    (art / "plan.json").write_text(
        json.dumps({"plan_text": "# Plan", "total_notes": 1,
                    "_sign_off": {"accepted": False, "decision": None,
                                  "stopped_at": "augment", "completed": False}}),
        encoding="utf-8",
    )
    assert sup._has_accepted_plan(admitted.job_id) is False
    # legacy unstamped dump → also refused (fail-closed)
    (art / "plan.json").write_text(
        json.dumps({"plan_text": "# Plan", "total_notes": 1}), encoding="utf-8"
    )
    assert sup._has_accepted_plan(admitted.job_id) is False
    # corrupt dump → refused, never an exception
    (art / "plan.json").write_text("{corrupt", encoding="utf-8")
    assert sup._has_accepted_plan(admitted.job_id) is False
    # the stamped accepted dump is the ONLY thing that routes to resume
    (art / "plan.json").write_text(
        json.dumps({"plan_text": "# Plan", "total_notes": 1,
                    "_sign_off": {"accepted": True, "decision": "approved",
                                  "stopped_at": "review_accepted",
                                  "completed": True}}),
        encoding="utf-8",
    )
    assert sup._has_accepted_plan(admitted.job_id) is True


def test_resume_execute_refuses_unaccepted_plan(tmp_path: Path) -> None:
    """F14 defense-in-depth: even if routing mis-fires, resume_execute itself
    refuses a plan.json without a positive acceptance stamp."""
    import pytest

    from tessellum.runtime.executor import DigestionExecutor, DigestionIncompleteError
    from tessellum.runtime.policy import RuntimePolicy

    paths, store, source = _runtime(tmp_path)
    admitted, _ = admit_path(source, paths=paths, store=store, policy_profile="inspect")
    art = paths.job_artifacts(admitted.job_id)
    art.mkdir(parents=True, exist_ok=True)
    (art / "plan.json").write_text(
        json.dumps({"plan_text": "# Plan", "total_notes": 1,
                    "_sign_off": {"accepted": False, "decision": None,
                                  "stopped_at": "augment", "completed": False}}),
        encoding="utf-8",
    )
    (art / "source_leaf.json").write_text(
        json.dumps({"source_content": "evidence"}), encoding="utf-8"
    )
    executor = DigestionExecutor(paths=paths, backend=None)  # type: ignore[arg-type]
    job = store.get(admitted.job_id)
    with pytest.raises(DigestionIncompleteError, match="not an ACCEPTED plan"):
        executor.resume_execute(job, lease=None, route=None,  # type: ignore[arg-type]
                                policy=RuntimePolicy.for_profile("inspect"))
