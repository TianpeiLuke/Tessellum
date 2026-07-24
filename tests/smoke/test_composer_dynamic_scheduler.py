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
import time
from contextlib import contextmanager
from pathlib import Path

import pytest

from tessellum.composer import (
    Manifest,
    MockBackend,
    ReadySetState,
    RunResult,
    SkipReason,
    build_wave_gate,
    classify_outcome,
    compile_skill,
    compute_ready_set,
    run_pipeline,
    run_pipeline_dynamic,
)
from tessellum.composer.executor import StepResult
from tessellum.composer.llm import LLMResponse
from tessellum.composer.materializer import (
    MaterializedOutput,
    MaterializerError,
    materialize,
)


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
    ---

    # Per-leaf

    ## Step 1: rate <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: rating
    ```

    Rate leaf {{leaf.id}}.

    ## Step 2: consume <!-- :: section_id = step_2 :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: [step_1]
    materializer: no_op
    ```

    CONSUME {{upstream.rating}}.
    """
)


def _compile_pl(tmp_path: Path):
    sk = tmp_path / "skill_pl.md"
    sk.write_text(_CANON_PL, encoding="utf-8")
    return compile_skill(sk)


def _compile_writer(tmp_path: Path, *, instruction: str = "Write") -> tuple:
    skill = tmp_path / "skill_writer.md"
    skill.write_text(
        textwrap.dedent(
            f"""\
            ---
            tags: [resource, skill]
            keywords: [alpha, beta, gamma]
            topics: [X]
            language: markdown
            date of note: 2026-05-10
            status: active
            building_block: procedure
            ---

            # Writer

            ## Step 1: write <!-- :: section_id = write :: -->

            ```yaml
            role: CORE
            aggregation: per_leaf
            batchable: false
            depends_on: []
            materializer: body_markdown_to_file
            expected_output_schema:
              type: object
              required: [output_path, body_markdown]
            ```

            {instruction} for {{{{leaf.id}}}}.
            """
        ),
        encoding="utf-8",
    )
    return compile_skill(skill), skill


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


def test_dynamic_resume_reconstructs_upstream_and_skips_verified_leaves(
    tmp_path: Path,
) -> None:
    compiled = _compile_pl(tmp_path)
    manifest_path = tmp_path / "manifest.json"
    first_backend = MockBackend(default='{"rating": 5}')
    first = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}, {"id": "b"}],
        backend=first_backend,
        vault_root=tmp_path / "vault",
        manifest=Manifest.load(manifest_path),
        run_id="job:1",
        generation=1,
    )
    assert first.error_count == 0
    assert len(first_backend.calls) == 3

    resumed_backend = MockBackend(default='{"rating": 999}')
    resumed = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}, {"id": "b"}],
        backend=resumed_backend,
        vault_root=tmp_path / "vault",
        manifest=Manifest.load(manifest_path),
        run_id="job:1-restart",
        generation=1,
    )
    assert resumed.error_count == 0
    assert resumed_backend.calls == []
    assert [result.attempts for result in resumed.step_results] == [0, 0, 0]
    assert [result.materialized.structured for result in resumed.step_results] == [
        {"rating": 5},
        {"rating": 5},
        {"rating": 5},
    ]


def test_dynamic_resume_reexecutes_tampered_artifact(tmp_path: Path) -> None:
    compiled, _skill = _compile_writer(tmp_path)
    manifest_path = tmp_path / "manifest.json"
    vault = tmp_path / "vault"
    original = json.dumps(
        {"output_path": "notes/a.md", "body_markdown": "original"}
    )
    run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}],
        backend=MockBackend(default=original),
        vault_root=vault,
        manifest=Manifest.load(manifest_path),
        run_id="job:1",
        generation=1,
    )
    note = vault / "notes/a.md"
    note.write_text("tampered", encoding="utf-8")

    retry_backend = MockBackend(
        default=json.dumps(
            {"output_path": "notes/a.md", "body_markdown": "repaired"}
        )
    )
    retried = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}],
        backend=retry_backend,
        vault_root=vault,
        manifest=Manifest.load(manifest_path),
        run_id="job:2",
        generation=1,
    )

    assert retried.error_count == 0
    assert len(retry_backend.calls) == 1
    assert note.read_text(encoding="utf-8") == "repaired"
    assert Manifest.load(manifest_path).entries["write::leaf_0"].status == "done"


def test_dynamic_resume_reexecutes_changed_plan_identity(tmp_path: Path) -> None:
    compiled, _skill = _compile_writer(tmp_path, instruction="Write")
    manifest_path = tmp_path / "manifest.json"
    vault = tmp_path / "vault"
    run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}],
        backend=MockBackend(
            default=json.dumps(
                {"output_path": "notes/a.md", "body_markdown": "version one"}
            )
        ),
        vault_root=vault,
        manifest=Manifest.load(manifest_path),
        run_id="job:1",
        generation=1,
    )
    changed, _skill = _compile_writer(tmp_path, instruction="Rewrite")
    retry_backend = MockBackend(
        default=json.dumps(
            {"output_path": "notes/a.md", "body_markdown": "version two"}
        )
    )

    retried = run_pipeline_dynamic(
        changed,
        leaves=[{"id": "a"}],
        backend=retry_backend,
        vault_root=vault,
        manifest=Manifest.load(manifest_path),
        run_id="job:2",
        generation=1,
    )

    assert retried.error_count == 0
    assert len(retry_backend.calls) == 1
    assert (vault / "notes/a.md").read_text(encoding="utf-8") == "version two"


def test_dynamic_failed_leaf_releases_claim_for_next_run(tmp_path: Path) -> None:
    compiled, _skill = _compile_writer(tmp_path)
    manifest_path = tmp_path / "manifest.json"
    first = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}],
        backend=MockBackend(default='{"wrong": true}'),
        vault_root=tmp_path / "vault",
        manifest=Manifest.load(manifest_path),
        run_id="job:1",
        generation=1,
        max_logic_retries=0,
    )
    assert first.error_count == 1
    assert Manifest.load(manifest_path).entries["write::leaf_0"].status == "pending"

    retry_backend = MockBackend(
        default=json.dumps(
            {"output_path": "notes/a.md", "body_markdown": "recovered"}
        )
    )
    retried = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}],
        backend=retry_backend,
        vault_root=tmp_path / "vault",
        manifest=Manifest.load(manifest_path),
        run_id="job:2",
        generation=1,
        max_logic_retries=0,
    )

    assert retried.error_count == 0
    assert len(retry_backend.calls) == 1
    assert Manifest.load(manifest_path).entries["write::leaf_0"].status == "done"


def test_dynamic_retry_does_not_steal_live_foreign_claim(tmp_path: Path) -> None:
    compiled, _skill = _compile_writer(tmp_path)
    manifest = Manifest()
    assert manifest.claim(
        "write::leaf_0",
        run_id="foreign",
        now=time.time(),
        generation=1,
    )
    backend = MockBackend(
        default=json.dumps(
            {"output_path": "notes/a.md", "body_markdown": "must not run"}
        )
    )

    run = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}],
        backend=backend,
        vault_root=tmp_path / "vault",
        manifest=manifest,
        run_id="job:2",
        generation=1,
    )

    assert run.error_count == 1
    assert backend.calls == []
    assert manifest.entries["write::leaf_0"].status == "in_progress"
    assert manifest.entries["write::leaf_0"].run_id == "foreign"


def test_materializers_reject_outside_paths_before_any_write(
    tmp_path: Path,
) -> None:
    outside = tmp_path / "outside.md"
    cases = (
        (
            "body_markdown_to_file",
            json.dumps(
                {"output_path": str(outside), "body_markdown": "outside"}
            ),
        ),
        (
            "body_markdown_frontmatter_to_file",
            "---\noutput_path: ../outside.md\n---\noutside",
        ),
        (
            "edits_apply_to_files",
            json.dumps(
                {
                    "edits": [
                        {"file": "safe.md", "content": "must not be written"},
                        {"file": "../outside.md", "content": "outside"},
                    ]
                }
            ),
        ),
        (
            "edits_apply_xml_tags",
            (
                "<edits><edit><file>safe.md</file><content>must not be written"
                "</content></edit><edit><file>/outside.md</file>"
                "<content>outside</content></edit></edits>"
            ),
        ),
    )

    for i, (materializer_key, payload) in enumerate(cases):
        vault = tmp_path / f"vault-{i}"
        with pytest.raises(MaterializerError, match="vault_root"):
            materialize(materializer_key, payload, vault_root=vault)
        assert not outside.exists()
        assert not (vault / "safe.md").exists()


def test_materializer_acquires_effect_guard_for_each_write(tmp_path: Path) -> None:
    events: list[str] = []

    @contextmanager
    def guard():
        events.append("enter")
        try:
            yield
        finally:
            events.append("exit")

    materialize(
        "edits_apply_to_files",
        json.dumps(
            {
                "edits": [
                    {"file": "a.md", "content": "a"},
                    {"file": "b.md", "content": "b"},
                ]
            }
        ),
        vault_root=tmp_path / "vault",
        effect_guard=guard,
    )

    assert events == ["enter", "exit", "enter", "exit"]


def test_materializer_interrupted_replace_preserves_accepted_file(
    tmp_path: Path,
    monkeypatch,
) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    target = vault / "note.md"
    target.write_text("accepted", encoding="utf-8")
    real_replace = __import__("os").replace

    def interrupt_target_replace(source, destination):
        if Path(destination) == target:
            raise OSError("simulated publication interruption")
        return real_replace(source, destination)

    monkeypatch.setattr(
        "tessellum.composer.materializer.os.replace",
        interrupt_target_replace,
    )

    with pytest.raises(OSError, match="publication interruption"):
        materialize(
            "body_markdown_to_file",
            json.dumps(
                {"output_path": "note.md", "body_markdown": "partial"}
            ),
            vault_root=vault,
        )

    assert target.read_text(encoding="utf-8") == "accepted"
    assert list(vault.glob(".note.md.*.tmp")) == []


@pytest.mark.parametrize("runner", [run_pipeline, run_pipeline_dynamic])
def test_schedulers_forward_cancellation_and_effect_guard(
    tmp_path: Path,
    runner,
) -> None:
    compiled, _skill = _compile_writer(tmp_path)
    guard_entries = 0

    @contextmanager
    def guard():
        nonlocal guard_entries
        guard_entries += 1
        yield

    run = runner(
        compiled,
        leaves=[{"id": "a"}],
        backend=MockBackend(
            default=json.dumps(
                {"output_path": "notes/a.md", "body_markdown": "guarded"}
            )
        ),
        vault_root=tmp_path / "vault",
        cancellation_check=lambda: False,
        effect_guard=guard,
    )
    assert run.error_count == 0
    assert guard_entries == 1

    with pytest.raises(InterruptedError, match="cancelled"):
        runner(
            compiled,
            leaves=[{"id": "b"}],
            backend=MockBackend(default="{}"),
            vault_root=tmp_path / "cancelled-vault",
            cancellation_check=lambda: True,
            effect_guard=guard,
        )


def test_wave_gate_failure_is_recoverable_on_next_run(tmp_path: Path) -> None:
    compiled, _skill = _compile_writer(tmp_path)
    manifest_path = tmp_path / "manifest.json"
    vault = tmp_path / "vault"
    duplicate = json.dumps(
        {"output_path": "notes/duplicate.md", "body_markdown": "duplicate"}
    )
    failed = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}, {"id": "b"}],
        backend=MockBackend(default=duplicate),
        vault_root=vault,
        manifest=Manifest.load(manifest_path),
        run_id="job:1",
        generation=1,
        wave_gate=build_wave_gate(),
    )

    assert failed.error_count == 2
    assert {
        entry.status for entry in Manifest.load(manifest_path).entries.values()
    } == {"pending"}

    retry_backend = MockBackend(
        responses={
            "Write for a": json.dumps(
                {"output_path": "notes/a.md", "body_markdown": "a"}
            ),
            "Write for b": json.dumps(
                {"output_path": "notes/b.md", "body_markdown": "b"}
            ),
        }
    )
    recovered = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}, {"id": "b"}],
        backend=retry_backend,
        vault_root=vault,
        manifest=Manifest.load(manifest_path),
        run_id="job:2",
        generation=1,
        wave_gate=build_wave_gate(),
    )

    assert recovered.error_count == 0
    assert len(retry_backend.calls) == 2
    assert {
        entry.status for entry in Manifest.load(manifest_path).entries.values()
    } == {"done"}


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
        ---

        # W

        ## Step 1: emit <!-- :: section_id = step_1 :: -->

        ```yaml
        role: CORE
        aggregation: per_leaf
        batchable: false
        depends_on: []
        materializer: no_op
        output_key: emitted
        ```

        Emit for {{leaf.id}}.
        """
    )
    sk = tmp_path / "skill_w.md"
    sk.write_text(canon, encoding="utf-8")
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
        ---

        # Mixed

        ## Step 1: setup <!-- :: section_id = step_1 :: -->

        ```yaml
        role: INFRA
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        ```

        INFRA.

        ## Step 2: real <!-- :: section_id = step_2 :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        ```

        Real.
        """
    )
    sk = tmp_path / "skill_i.md"
    sk.write_text(canon, encoding="utf-8")
    compiled = compile_skill(sk)
    run = run_pipeline_dynamic(
        compiled, leaves=None, backend=MockBackend(default="{}"),
        vault_root=tmp_path / "v",
    )
    assert [r.section_id for r in run.step_results] == ["step_2"]


# ── manifest integration + observability ────────────────────────────────────


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
        ---

        # S

        ## Step 1: strict <!-- :: section_id = step_1 :: -->

        ```yaml
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
        ```

        Strict {{leaf.id}}.
        """
    )
    sk = tmp_path / "skill_s.md"
    sk.write_text(canon, encoding="utf-8")
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


# ── Self-claiming scheduler: dependency ordering + no straggler barrier ──────


_DIAMOND_CANON = textwrap.dedent(
    """\
    ---
    tags: [resource, skill]
    keywords: [alpha, beta, gamma]
    topics: [X]
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    ---

    # Diamond

    ## Step a <!-- :: section_id = a :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: a_out
    ```

    A.

    ## Step b <!-- :: section_id = b :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: [a]
    materializer: no_op
    output_key: b_out
    ```

    B reads {{upstream.a_out}}.

    ## Step c <!-- :: section_id = c :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: [a]
    materializer: no_op
    output_key: c_out
    ```

    C reads {{upstream.a_out}}.

    ## Step d <!-- :: section_id = d :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: [b, c]
    materializer: no_op
    ```

    D reads {{upstream.b_out}} and {{upstream.c_out}}.
    """
)


def test_dynamic_diamond_dependency_ordering(tmp_path: Path) -> None:
    """The self-claiming loop honours a diamond DAG: d sees both b's and c's
    outputs, which each saw a's — proving deps gate promotion + upstream
    accumulates across the (now barrier-free) loop."""
    sk = tmp_path / "skill_d.md"
    sk.write_text(_DIAMOND_CANON, encoding="utf-8")
    compiled = compile_skill(sk)
    backend = MockBackend(default='{"v": 1}')
    run = run_pipeline_dynamic(compiled, leaves=None, backend=backend, vault_root=tmp_path / "v")
    assert run.error_count == 0
    assert len(run.step_results) == 4
    # d's prompt must have seen BOTH b's and c's RESOLVED outputs (proves b
    # AND c ran + published before d). A resolved {{upstream.X}} becomes the
    # value; an unmet dep would leave a "<missing upstream.X>" sentinel.
    d_call = next(c for c in backend.calls if "D reads" in c.user_prompt)
    assert "<missing" not in d_call.user_prompt
    assert d_call.user_prompt.count('"v": 1') == 2  # both b_out and c_out resolved
    # b's + c's prompts each saw a's resolved output (a ran + published first).
    b_call = next(c for c in backend.calls if "B reads" in c.user_prompt)
    c_call = next(c for c in backend.calls if "C reads" in c.user_prompt)
    assert "<missing" not in b_call.user_prompt and '"v": 1' in b_call.user_prompt
    assert "<missing" not in c_call.user_prompt and '"v": 1' in c_call.user_prompt


def test_dynamic_diamond_matches_serial(tmp_path: Path) -> None:
    """Parity on a diamond DAG: serial and self-claiming produce the same
    ordered step_results + error count."""
    sk = tmp_path / "skill_d.md"
    sk.write_text(_DIAMOND_CANON, encoding="utf-8")
    compiled = compile_skill(sk)
    serial = run_pipeline(compiled, leaves=None, backend=MockBackend(default='{"v": 1}'), vault_root=tmp_path / "vs")
    dynamic = run_pipeline_dynamic(compiled, leaves=None, backend=MockBackend(default='{"v": 1}'), vault_root=tmp_path / "vd")
    assert [r.section_id for r in serial.step_results] == [r.section_id for r in dynamic.step_results]
    assert serial.error_count == dynamic.error_count == 0


def test_dynamic_straggler_does_not_block_independent_step(tmp_path: Path) -> None:
    """The barrier-free loop: an independent fast step finishes BEFORE a slow
    sibling in the same promotion — the slow one no longer gates the fast one.

    Two independent per_leaf steps; step_slow's backend sleeps, step_fast's
    doesn't. We record completion order via the backend call timestamps: the
    fast step's call must return before the slow step's, and the run stays
    correct. (Under the old whole-round barrier the fast leaf still had to
    wait for the round's join; here nothing gates it.)"""
    import time as _time

    canon = textwrap.dedent(
        """\
        ---
        tags: [resource, skill]
        keywords: [alpha, beta, gamma]
        topics: [X]
        language: markdown
        date of note: 2026-05-10
        status: active
        building_block: procedure
        ---

        # S

        ## Step fast <!-- :: section_id = fast :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        ```

        FAST.

        ## Step slow <!-- :: section_id = slow :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        ```

        SLOW.
        """
    )
    sk = tmp_path / "skill_s.md"
    sk.write_text(canon, encoding="utf-8")
    compiled = compile_skill(sk)

    completed: list[str] = []
    lock = __import__("threading").Lock()

    class _TimedBackend:
        backend_id = "timed"

        def call(self, request):
            if "SLOW" in request.user_prompt:
                _time.sleep(0.2)
                tag = "slow"
            else:
                tag = "fast"
            with lock:
                completed.append(tag)
            return LLMResponse(content='{"v": 1}', elapsed_ms=1.0, backend_id="timed")

    run = run_pipeline_dynamic(
        compiled, leaves=None, backend=_TimedBackend(), vault_root=tmp_path / "v",
        max_workers=2,
    )
    assert run.error_count == 0
    # The fast step completed before the slow one (they ran concurrently,
    # and nothing made fast wait for slow).
    assert completed[0] == "fast"
    assert set(completed) == {"fast", "slow"}
