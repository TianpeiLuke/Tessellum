"""Composer v4, Phase 3 — gate engine + per-session close-gate.

Covers:
  - gates.py: Gate.run severity gating, GateSuite short-circuit vs full
    sweep, the format/grounding/dedup predicates, CompositeGateResult.
  - grounding fail-closed: no verdict / auth_blocked / ungrounded → FAIL;
    grounded → PASS.
  - run_pipeline_dynamic close-gate: a note that passes format+grounding
    closes done; one that fails closes blocked (errored result, manifest
    row blocked); the fix loop repairs and re-gates; gate-then-commit
    ordering; close_gate=None preserves parity (no gating).

All additive; run_pipeline (serial) untouched (IDENT-4).
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from tessellum.composer import (
    Gate,
    GateSuite,
    GroundingVerdict,
    Manifest,
    MockBackend,
    build_close_gate,
    build_wave_gate,
    compile_skill,
    run_pipeline_dynamic,
)
from tessellum.composer.gates import (
    duplicate_target_predicate,
    format_predicate,
    grounding_predicate,
)
from tessellum.format import Issue, Severity


# ── A minimal note that passes tessellum.format cleanly ─────────────────────


_GOOD_NOTE = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - concept
    keywords:
      - alpha term
      - beta term
      - gamma term
    topics:
      - Topic One
      - Topic Two
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: concept
    ---

    # Minimal Concept Note

    ## Purpose

    A minimal grounded note body.
    """
)


_BAD_NOTE = textwrap.dedent(
    """\
    ---
    tags:
      - resource
    ---

    # Broken note — missing required frontmatter fields.
    """
)


# ── gates.py unit behavior ──────────────────────────────────────────────────


def _issue(sev: Severity) -> Issue:
    return Issue(sev, "TEST-001", "x", "test issue")


def test_gate_blocks_on_error_not_warning() -> None:
    err_gate = Gate("g", "checkpoint", "session",
                    lambda t, **k: [_issue(Severity.ERROR)])
    warn_gate = Gate("g", "checkpoint", "session",
                     lambda t, **k: [_issue(Severity.WARNING)])
    assert not err_gate.run("x").passed
    assert warn_gate.run("x").passed  # WARNING < block_on=ERROR
    # But WARNING carried on the result for diagnostics.
    assert warn_gate.run("x").issues


def test_gate_block_on_warning_is_configurable() -> None:
    g = Gate("g", "checkpoint", "session",
             lambda t, **k: [_issue(Severity.WARNING)], block_on=Severity.WARNING)
    assert not g.run("x").passed


def test_gate_suite_short_circuits_at_first_failure() -> None:
    calls: list[str] = []

    def p1(t, **k):
        calls.append("p1")
        return [_issue(Severity.ERROR)]

    def p2(t, **k):
        calls.append("p2")
        return []

    suite = GateSuite(gates=(
        Gate("g1", "checkpoint", "session", p1),
        Gate("g2", "checkpoint", "session", p2),
    ))
    res = suite.evaluate("x")  # short_circuit=True default
    assert not res.passed
    assert res.first_failure_cause == "g1"
    assert calls == ["p1"]  # p2 never ran


def test_gate_suite_full_sweep_runs_all() -> None:
    calls: list[str] = []
    suite = GateSuite(gates=(
        Gate("g1", "checkpoint", "session",
             lambda t, **k: (calls.append("p1"), [_issue(Severity.ERROR)])[1]),
        Gate("g2", "checkpoint", "session",
             lambda t, **k: (calls.append("p2"), [_issue(Severity.ERROR)])[1]),
    ))
    res = suite.evaluate("x", short_circuit=False)
    assert not res.passed
    assert calls == ["p1", "p2"]
    assert len(res.blocking_issues) == 2


def test_format_predicate_passes_good_note(tmp_path: Path) -> None:
    p = tmp_path / "good.md"
    p.write_text(_GOOD_NOTE, encoding="utf-8")
    issues = format_predicate(p)
    errors = [i for i in issues if i.severity is Severity.ERROR]
    assert errors == []


def test_format_predicate_flags_bad_note(tmp_path: Path) -> None:
    p = tmp_path / "bad.md"
    p.write_text(_BAD_NOTE, encoding="utf-8")
    issues = format_predicate(p)
    assert any(i.severity is Severity.ERROR for i in issues)


def test_grounding_predicate_fail_closed_without_verdict(tmp_path: Path) -> None:
    p = tmp_path / "n.md"
    p.write_text(_GOOD_NOTE, encoding="utf-8")
    issues = grounding_predicate(p, verdict=None)
    assert issues and issues[0].rule_id == "GROUND-000"


def test_grounding_predicate_auth_blocked_fails(tmp_path: Path) -> None:
    p = tmp_path / "n.md"
    p.write_text(_GOOD_NOTE, encoding="utf-8")
    issues = grounding_predicate(p, verdict=GroundingVerdict("auth_blocked", "auth expired"))
    assert issues and issues[0].rule_id == "GROUND-002"


def test_grounding_predicate_ungrounded_fails(tmp_path: Path) -> None:
    p = tmp_path / "n.md"
    p.write_text(_GOOD_NOTE, encoding="utf-8")
    issues = grounding_predicate(p, verdict=GroundingVerdict("ungrounded", "fabricated"))
    assert issues and issues[0].rule_id == "GROUND-001"


def test_grounding_predicate_grounded_passes(tmp_path: Path) -> None:
    p = tmp_path / "n.md"
    p.write_text(_GOOD_NOTE, encoding="utf-8")
    assert grounding_predicate(p, verdict=GroundingVerdict("grounded")) == []


def test_close_gate_passes_grounded_good_note(tmp_path: Path) -> None:
    p = tmp_path / "good.md"
    p.write_text(_GOOD_NOTE, encoding="utf-8")
    res = build_close_gate().evaluate(p, verdict=GroundingVerdict("grounded"))
    assert res.passed
    assert res.first_failure_cause is None


def test_close_gate_fails_format_before_grounding(tmp_path: Path) -> None:
    p = tmp_path / "bad.md"
    p.write_text(_BAD_NOTE, encoding="utf-8")
    # Even with a grounded verdict, the format gate fails first (short-circuit).
    res = build_close_gate().evaluate(p, verdict=GroundingVerdict("grounded"))
    assert not res.passed
    assert res.first_failure_cause == "format"


def test_dedup_predicate_flags_duplicate_paths() -> None:
    issues = duplicate_target_predicate(["a/n.md", "b/m.md", "a/n.md"])
    assert len(issues) == 1
    assert issues[0].rule_id == "WAVE-001"
    assert "a/n.md" in issues[0].message


def test_dedup_predicate_clean_when_unique() -> None:
    assert duplicate_target_predicate(["a.md", "b.md", "c.md"]) == []


def test_wave_gate_uses_dedup() -> None:
    suite = build_wave_gate()
    assert not suite.evaluate(["x.md", "x.md"]).passed
    assert suite.evaluate(["x.md", "y.md"]).passed


# ── run_pipeline_dynamic close-gate integration ─────────────────────────────


def _writer_skill(tmp_path: Path):
    """A skill whose single per-leaf step writes a note via the frontmatter
    materializer, so the close-gate has a real file to check."""
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
        pipeline_metadata: ./skill_writer.pipeline.yaml
        ---

        # Writer

        ## Step 1: write <!-- :: section_id = step_1 :: -->

        Write for {{leaf.id}}.
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
            materializer: body_markdown_to_file
            expected_output_schema:
              type: object
              required: [output_path, body_markdown]
            prompt_template: "Write."
        """
    )
    sk = tmp_path / "skill_writer.md"
    sk.write_text(canon, encoding="utf-8")
    (tmp_path / "skill_writer.pipeline.yaml").write_text(side, encoding="utf-8")
    return compile_skill(sk)


def _good_response(path: str) -> str:
    # JSON envelope for body_markdown_to_file: output_path + the full note
    # text (frontmatter + body) as body_markdown. The written file is a
    # format-clean note the close-gate can pass.
    import json as _json

    return _json.dumps({"output_path": path, "body_markdown": _GOOD_NOTE})


def test_dynamic_close_gate_passes_and_closes_done(tmp_path: Path) -> None:
    compiled = _writer_skill(tmp_path)
    backend = MockBackend(default=_good_response("notes/out.md"))
    manifest = Manifest(path=tmp_path / "manifest.json")
    run = run_pipeline_dynamic(
        compiled, leaves=[{"id": "a"}],
        backend=backend, vault_root=tmp_path / "vault",
        manifest=manifest, run_id="r1",
        close_gate=build_close_gate(),
        grounding_verifier=lambda step, leaf, result: GroundingVerdict("grounded"),
    )
    assert run.error_count == 0
    assert all(e.status == "done" for e in manifest.entries.values())


def test_dynamic_close_gate_blocks_ungrounded(tmp_path: Path) -> None:
    compiled = _writer_skill(tmp_path)
    backend = MockBackend(default=_good_response("notes/out.md"))
    manifest = Manifest(path=tmp_path / "manifest.json")
    run = run_pipeline_dynamic(
        compiled, leaves=[{"id": "a"}],
        backend=backend, vault_root=tmp_path / "vault",
        manifest=manifest, run_id="r1",
        close_gate=build_close_gate(),
        # Verifier says the note is NOT grounded → session must block.
        grounding_verifier=lambda step, leaf, result: GroundingVerdict("ungrounded", "made up"),
    )
    # A format-clean but ungrounded note fails the close-gate → errored result.
    assert run.error_count == 1
    assert "close-gate blocked (grounding)" in run.step_results[0].error
    # Manifest session is blocked, not done (lifecycle-terminator invariant).
    statuses = {e.status for e in manifest.entries.values()}
    assert statuses == {"blocked"}


def test_dynamic_close_gate_fail_closed_without_verifier(tmp_path: Path) -> None:
    compiled = _writer_skill(tmp_path)
    backend = MockBackend(default=_good_response("notes/out.md"))
    run = run_pipeline_dynamic(
        compiled, leaves=[{"id": "a"}],
        backend=backend, vault_root=tmp_path / "vault",
        close_gate=build_close_gate(),
        grounding_verifier=None,  # grounding fails closed
    )
    assert run.error_count == 1
    assert "grounding" in run.step_results[0].error


def test_dynamic_close_gate_fix_loop_repairs(tmp_path: Path) -> None:
    compiled = _writer_skill(tmp_path)
    backend = MockBackend(default=_good_response("notes/out.md"))
    # Verifier flips to grounded after the fixer runs once.
    state = {"grounded": False}

    def verifier(step, leaf, result):
        return GroundingVerdict("grounded" if state["grounded"] else "ungrounded")

    # The fixer just flips the verifier state; it repairs in place and
    # doesn't need to return anything meaningful.
    def fixer(step, leaf, issues):
        state["grounded"] = True

    run = run_pipeline_dynamic(
        compiled, leaves=[{"id": "a"}],
        backend=backend, vault_root=tmp_path / "vault",
        close_gate=build_close_gate(),
        grounding_verifier=verifier,
        max_fix_rounds=1,
        fixer=fixer,
    )
    # After one fix round the re-gate passes → session closes done.
    assert run.error_count == 0


def test_dynamic_close_gate_none_preserves_parity(tmp_path: Path) -> None:
    # With close_gate=None (default) an ungrounded verifier is irrelevant —
    # the write succeeds and closes done, exactly as pre-Phase-3.
    compiled = _writer_skill(tmp_path)
    backend = MockBackend(default=_good_response("notes/out.md"))
    run = run_pipeline_dynamic(
        compiled, leaves=[{"id": "a"}],
        backend=backend, vault_root=tmp_path / "vault",
        close_gate=None,
    )
    assert run.error_count == 0
