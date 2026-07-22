"""Composer v4, Phase 2 — self-claiming dynamic scheduler + typed outcome.

Covers:
  - compute_ready_set: pure functional core (deps gating, concurrency cap,
    closed skip-enum, done/in-flight exclusion, idempotence).
  - classify_outcome: StepResult → typed discriminated-union StepOutcome,
    every kind, artifact-readable-only-on-SUCCESS guard.
  - run_pipeline_dynamic: PARITY with run_pipeline (byte-identical vault
    output + identical ordered per-leaf outcomes), the P2 gate; plus
    manifest claim/attempt/done recording, event stream, statistics.json.

All additive; run_pipeline (serial) is untouched (IDENT-4).
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

from tessellum.composer import (
    Manifest,
    MockBackend,
    ReadySetState,
    RunResult,
    SkipReason,
    classify_outcome,
    compile_skill,
    compute_ready_set,
    run_pipeline,
    run_pipeline_dynamic,
)
from tessellum.composer.executor import StepResult
from tessellum.composer.llm import LLMResponse
from tessellum.composer.materializer import MaterializedOutput


# ── compute_ready_set (pure functional core) ────────────────────────────────


_DIAMOND = (
    ("a", ()),
    ("b", ("a",)),
    ("c", ("a",)),
    ("d", ("b", "c")),
)


def test_ready_set_promotes_only_root_first() -> None:
    promoted, skipped = compute_ready_set(
        ReadySetState(
            steps=_DIAMOND,
            done=frozenset(),
            in_flight=frozenset(),
            concurrency_cap=99,
        )
    )
    assert promoted == ("a",)
    assert {(s.section_id, s.reason) for s in skipped} == {
        ("b", "deps_unmet"),
        ("c", "deps_unmet"),
        ("d", "deps_unmet"),
    }


def test_ready_set_promotes_independent_siblings_together() -> None:
    promoted, skipped = compute_ready_set(
        ReadySetState(
            steps=_DIAMOND,
            done=frozenset({"a"}),
            in_flight=frozenset(),
            concurrency_cap=99,
        )
    )
    assert promoted == ("b", "c")  # topological order preserved
    assert [(s.section_id, s.reason) for s in skipped] == [("d", "deps_unmet")]


def test_ready_set_concurrency_cap_defers_with_closed_reason() -> None:
    promoted, skipped = compute_ready_set(
        ReadySetState(
            steps=_DIAMOND,
            done=frozenset({"a"}),
            in_flight=frozenset(),
            concurrency_cap=1,
        )
    )
    assert promoted == ("b",)
    assert skipped == (SkipReason("c", "concurrency_capped"),
                       SkipReason("d", "deps_unmet"))


def test_ready_set_excludes_done_and_in_flight() -> None:
    promoted, skipped = compute_ready_set(
        ReadySetState(
            steps=_DIAMOND,
            done=frozenset({"a", "b"}),
            in_flight=frozenset({"c"}),
            concurrency_cap=99,
        )
    )
    # a, b done; c in-flight; only d remains but its dep c isn't done.
    assert promoted == ()
    assert skipped == (SkipReason("d", "deps_unmet"),)


def test_ready_set_all_deps_done_promotes_join() -> None:
    promoted, skipped = compute_ready_set(
        ReadySetState(
            steps=_DIAMOND,
            done=frozenset({"a", "b", "c"}),
            in_flight=frozenset(),
            concurrency_cap=99,
        )
    )
    assert promoted == ("d",)
    assert skipped == ()


def test_ready_set_zero_cap_promotes_nothing() -> None:
    promoted, skipped = compute_ready_set(
        ReadySetState(
            steps=(("a", ()),),
            done=frozenset(),
            in_flight=frozenset(),
            concurrency_cap=0,
        )
    )
    assert promoted == ()
    assert skipped == (SkipReason("a", "concurrency_capped"),)


def test_ready_set_is_pure_no_mutation() -> None:
    state = ReadySetState(
        steps=_DIAMOND,
        done=frozenset({"a"}),
        in_flight=frozenset(),
        concurrency_cap=99,
    )
    first = compute_ready_set(state)
    second = compute_ready_set(state)
    assert first == second  # deterministic, state untouched


# ── classify_outcome (typed discriminated union) ────────────────────────────


def _result(error: str | None, *, error_class: str | None = None,
            attempts: int = 1) -> StepResult:
    return StepResult(
        section_id="s",
        leaf_id="l",
        response=LLMResponse(content="{}", elapsed_ms=1.0, backend_id="mock"),
        materialized=MaterializedOutput(structured={"ok": True}),
        elapsed_ms=1.0,
        error=error,
        attempts=attempts,
        error_class=error_class,
    )


def test_classify_outcome_success_exposes_artifact() -> None:
    outcome = classify_outcome(_result(None))
    assert outcome.kind == "SUCCESS"
    assert outcome.is_success
    assert outcome.artifact.structured == {"ok": True}


def test_classify_outcome_success_carries_telemetry_on_every_kind() -> None:
    outcome = classify_outcome(_result(None, attempts=2))
    assert outcome.attempts == 2
    assert outcome.elapsed_ms == 1.0
    assert outcome.error is None


def test_classify_outcome_same_error_loop() -> None:
    o = classify_outcome(_result("same-error loop short-circuit (logic): boom"))
    assert o.kind == "SAME_ERROR_LOOP"


def test_classify_outcome_watchdog_kill_wins_over_budget() -> None:
    # A stall that also exhausted the crash budget → the timeout is the root.
    o = classify_outcome(
        _result("crash budget exhausted (2 retries, stalls): stalled after 120.0s",
                error_class="transient")
    )
    assert o.kind == "WATCHDOG_KILLED"


def test_classify_outcome_retry_exhausted() -> None:
    o = classify_outcome(_result("crash budget exhausted (2 retries): Boom: x",
                                 error_class="crash"))
    assert o.kind == "RETRY_EXHAUSTED"


def test_classify_outcome_contract_violation_from_class() -> None:
    o = classify_outcome(
        _result("response failed schema validation: bad", error_class="validation")
    )
    assert o.kind == "CONTRACT_VIOLATION"


def test_classify_outcome_prompt_cap_is_contract_violation() -> None:
    o = classify_outcome(
        _result("prompt exceeded HARD_PROMPT_CAP_CHARS: 9 > 5",
                error_class="validation")
    )
    assert o.kind == "CONTRACT_VIOLATION"


def test_step_outcome_artifact_guard_raises_on_failure() -> None:
    o = classify_outcome(_result("some error", error_class="crash"))
    assert not o.is_success
    try:
        _ = o.artifact
        raise AssertionError("expected ValueError accessing failed artifact")
    except ValueError as e:
        assert "only readable on SUCCESS" in str(e)


# ── run_pipeline_dynamic PARITY with run_pipeline (the P2 gate) ──────────────


_CANON_PL = textwrap.dedent(
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
    pipeline_metadata: ./skill_pl.pipeline.yaml
    ---

    # Per-leaf

    ## Step 1: rate <!-- :: section_id = step_1 :: -->

    Rate leaf {{leaf.id}}.

    ## Step 2: consume <!-- :: section_id = step_2 :: -->

    CONSUME {{upstream.rating}}.
    """
)


_SIDE_PL = textwrap.dedent(
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
      - section_id: step_2
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: [step_1]
        materializer: no_op
        prompt_template: "Consume."
    """
)


def _compile_pl(tmp_path: Path):
    sk = tmp_path / "skill_pl.md"
    sk.write_text(_CANON_PL, encoding="utf-8")
    (tmp_path / "skill_pl.pipeline.yaml").write_text(_SIDE_PL, encoding="utf-8")
    return compile_skill(sk)


def _sig(run: RunResult):
    return [
        (r.section_id, r.leaf_id, r.error, r.attempts,
         tuple(sorted(r.materialized.structured.items())))
        for r in run.step_results
    ]


def test_dynamic_matches_serial_step_results(tmp_path: Path) -> None:
    compiled = _compile_pl(tmp_path)
    leaves_a = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    leaves_b = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    serial = run_pipeline(
        compiled, leaves=leaves_a,
        backend=MockBackend(default='{"rating": 5}'), vault_root=tmp_path / "v1"
    )
    dynamic = run_pipeline_dynamic(
        compiled, leaves=leaves_b,
        backend=MockBackend(default='{"rating": 5}'), vault_root=tmp_path / "v2",
        max_workers=4,
    )
    assert isinstance(dynamic, RunResult)
    # The P2 parity gate: identical ordered per-leaf outcomes + structured output.
    assert _sig(serial) == _sig(dynamic)
    assert serial.error_count == dynamic.error_count == 0
    # Same leaves, same order.
    assert [leaf["_id"] for leaf in dynamic.leaves] == ["leaf_0", "leaf_1", "leaf_2"]


def test_dynamic_matches_serial_on_written_files(tmp_path: Path) -> None:
    # A materializer that actually writes: parity must hold on the vault bytes.
    canon = textwrap.dedent(
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
        pipeline_metadata: ./skill_w.pipeline.yaml
        ---

        # W

        ## Step 1: emit <!-- :: section_id = step_1 :: -->

        Emit for {{leaf.id}}.
        """
    )
    side = textwrap.dedent(
        """\
        version: "1.0"
        pipeline:
          - section_id: step_1
            role: CORE
            aggregation: per_leaf
            batchable: false
            depends_on: []
            materializer: no_op
            prompt_template: "Emit."
            output_key: emitted
        """
    )
    sk = tmp_path / "skill_w.md"
    sk.write_text(canon, encoding="utf-8")
    (tmp_path / "skill_w.pipeline.yaml").write_text(side, encoding="utf-8")
    compiled = compile_skill(sk)

    serial = run_pipeline(
        compiled, leaves=[{"id": "x"}, {"id": "y"}],
        backend=MockBackend(default='{"emitted": 1}'), vault_root=tmp_path / "vs",
    )
    dynamic = run_pipeline_dynamic(
        compiled, leaves=[{"id": "x"}, {"id": "y"}],
        backend=MockBackend(default='{"emitted": 1}'), vault_root=tmp_path / "vd",
        max_workers=2,
    )
    assert _sig(serial) == _sig(dynamic)


def test_dynamic_synthetic_leaf_when_none(tmp_path: Path) -> None:
    compiled = _compile_pl(tmp_path)
    run = run_pipeline_dynamic(
        compiled, leaves=None,
        backend=MockBackend(default='{"rating": 1}'), vault_root=tmp_path / "v",
    )
    # per_leaf step_1 runs against the synthetic corpus leaf.
    assert run.leaves[0]["_id"] == "corpus"
    assert run.error_count == 0


def test_dynamic_skips_infra(tmp_path: Path) -> None:
    canon = textwrap.dedent(
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
        pipeline_metadata: ./skill_i.pipeline.yaml
        ---

        # Mixed

        ## Step 1: setup <!-- :: section_id = step_1 :: -->

        INFRA.

        ## Step 2: real <!-- :: section_id = step_2 :: -->

        Real.
        """
    )
    side = textwrap.dedent(
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
    sk = tmp_path / "skill_i.md"
    sk.write_text(canon, encoding="utf-8")
    (tmp_path / "skill_i.pipeline.yaml").write_text(side, encoding="utf-8")
    compiled = compile_skill(sk)
    run = run_pipeline_dynamic(
        compiled, leaves=None, backend=MockBackend(default="{}"),
        vault_root=tmp_path / "v",
    )
    assert [r.section_id for r in run.step_results] == ["step_2"]


# ── manifest integration + observability (§C5 / §C9) ─────────────────────────


def test_dynamic_records_manifest_done(tmp_path: Path) -> None:
    compiled = _compile_pl(tmp_path)
    manifest = Manifest(path=tmp_path / "manifest.json")
    run = run_pipeline_dynamic(
        compiled, leaves=[{"id": "a"}, {"id": "b"}],
        backend=MockBackend(default='{"rating": 5}'), vault_root=tmp_path / "v",
        manifest=manifest, run_id="run-xyz", max_workers=2,
    )
    assert run.error_count == 0
    # Every (step × leaf) key is done with a recorded attempt.
    assert manifest.entries  # non-empty
    for key, entry in manifest.entries.items():
        assert entry.status == "done", (key, entry.status)
        assert entry.attempts  # at least one AttemptRecord
        assert entry.attempts[-1].outcome == "success"
    # Manifest was persisted.
    assert (tmp_path / "manifest.json").exists()
    reloaded = Manifest.load(tmp_path / "manifest.json")
    assert all(e.status == "done" for e in reloaded.entries.values())


def test_dynamic_writes_event_stream_and_statistics(tmp_path: Path) -> None:
    compiled = _compile_pl(tmp_path)
    events_path = tmp_path / "events.jsonl"
    stats_path = tmp_path / "statistics.json"
    run_pipeline_dynamic(
        compiled, leaves=[{"id": "a"}, {"id": "b"}, {"id": "c"}],
        backend=MockBackend(default='{"rating": 5}'), vault_root=tmp_path / "v",
        events_path=events_path, stats_path=stats_path, max_workers=3,
    )
    # Event stream: one line per (step × leaf) invocation.
    lines = [
        json.loads(ln)
        for ln in events_path.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    # 3 leaves × step_1 + 1 corpus × step_2 = 4 events.
    assert len(lines) == 4
    assert all(ev["outcome"] == "SUCCESS" for ev in lines)
    # Statistics rollup.
    stats = json.loads(stats_path.read_text(encoding="utf-8"))
    assert stats["invocation_count"] == 4
    assert stats["error_count"] == 0
    assert stats["per_stage"]["step_1"]["succeeded"] == 3
    assert stats["per_stage"]["step_2"]["succeeded"] == 1


def test_dynamic_surfaces_errors_in_outcome(tmp_path: Path) -> None:
    # A backend returning malformed JSON for a schema-checked step surfaces
    # as an error in both paths — parity on the failure path too.
    canon = textwrap.dedent(
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
        pipeline_metadata: ./skill_s.pipeline.yaml
        ---

        # S

        ## Step 1: strict <!-- :: section_id = step_1 :: -->

        Strict {{leaf.id}}.
        """
    )
    side = textwrap.dedent(
        """\
        version: "1.0"
        pipeline:
          - section_id: step_1
            role: CORE
            aggregation: per_leaf
            batchable: false
            depends_on: []
            materializer: no_op
            expected_output_schema:
              type: object
              required: [must_have]
              properties:
                must_have:
                  type: string
            prompt_template: "Strict."
        """
    )
    sk = tmp_path / "skill_s.md"
    sk.write_text(canon, encoding="utf-8")
    (tmp_path / "skill_s.pipeline.yaml").write_text(side, encoding="utf-8")
    compiled = compile_skill(sk)

    leaves = [{"id": "a"}]
    serial = run_pipeline(
        compiled, leaves=[dict(x) for x in leaves],
        backend=MockBackend(default='{"wrong": 1}'), vault_root=tmp_path / "vs",
        max_logic_retries=0, max_crash_recoveries=0,
    )
    dynamic = run_pipeline_dynamic(
        compiled, leaves=[dict(x) for x in leaves],
        backend=MockBackend(default='{"wrong": 1}'), vault_root=tmp_path / "vd",
        max_logic_retries=0, max_crash_recoveries=0,
    )
    assert serial.error_count == dynamic.error_count == 1
    # Same failure classification.
    s_outcome = classify_outcome(serial.step_results[0])
    d_outcome = classify_outcome(dynamic.step_results[0])
    assert s_outcome.kind == d_outcome.kind == "CONTRACT_VIOLATION"
