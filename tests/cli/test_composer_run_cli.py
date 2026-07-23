"""Smoke tests for ``tessellum composer run``."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.cli.main import main


# Single-file skill: each pipeline step is an H2 section carrying a
# ``<!-- :: section_id = X :: -->`` anchor AND a leading ```yaml``` contract
# block (the typed step declaration), with the prompt prose after it. There
# is no ``.pipeline.yaml`` sidecar and no ``pipeline_metadata`` frontmatter.
_CANONICAL = textwrap.dedent(
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

    # Demo

    ## Step 1: produce <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: produced
    ```

    PRODUCE.

    ## Step 2: consume <!-- :: section_id = step_2 :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: [step_1]
    materializer: no_op
    ```

    CONSUME {{upstream.produced}}.
    """
)


@pytest.fixture
def demo_skill(tmp_path: Path) -> Path:
    skill = tmp_path / "skill_demo.md"
    skill.write_text(_CANONICAL, encoding="utf-8")
    return skill


def test_run_human_output(demo_skill, tmp_path, capsys):
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "ran skill_demo" in out
    assert "step_1" in out
    assert "step_2" in out


def test_run_json_output(demo_skill, tmp_path, capsys):
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
            "--format",
            "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["skill_name"] == "skill_demo"
    assert payload["step_invocation_count"] == 2
    assert payload["error_count"] == 0
    assert payload["trace_path"] is None


def test_run_with_mock_responses(demo_skill, tmp_path, capsys):
    responses = tmp_path / "mock.json"
    responses.write_text(
        json.dumps({"PRODUCE": '{"produced": [1, 2, 3]}'}),
        encoding="utf-8",
    )
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
            "--mock-responses",
            str(responses),
            "--format",
            "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["error_count"] == 0


def test_run_with_leaves(demo_skill, tmp_path, capsys):
    """Leaves file lets per_leaf steps run multiple times — even with corpus
    pipeline, the file must parse and load."""
    leaves = tmp_path / "leaves.json"
    leaves.write_text(json.dumps([{"id": "a"}, {"id": "b"}]), encoding="utf-8")
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
            "--leaves",
            str(leaves),
            "--format",
            "json",
        ]
    )
    assert code == 0


def test_run_writes_trace(demo_skill, tmp_path, capsys):
    runs_dir = tmp_path / "runs"
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--runs-dir",
            str(runs_dir),
        ]
    )
    assert code == 0
    traces = list(runs_dir.glob("*.json"))
    assert len(traces) == 1
    payload = json.loads(traces[0].read_text(encoding="utf-8"))
    assert payload["skill_name"] == "skill_demo"


def test_run_dry_run_no_files_written(demo_skill, tmp_path, capsys):
    vault = tmp_path / "vault"
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(vault),
            "--no-trace",
            "--dry-run",
        ]
    )
    assert code == 0
    # no_op materializer wouldn't write anyway, but the vault dir should not
    # have been populated by side effects.
    assert not vault.exists() or not any(vault.iterdir())


def test_run_missing_skill_returns_2(tmp_path, capsys):
    code = main(["composer", "run", str(tmp_path / "nope.md"), "--no-trace"])
    assert code == 2
    err = capsys.readouterr().err
    assert "does not exist" in err


def test_run_non_md_returns_2(tmp_path, capsys):
    p = tmp_path / "not_a_skill.txt"
    p.write_text("not a skill")
    code = main(["composer", "run", str(p), "--no-trace"])
    assert code == 2
    err = capsys.readouterr().err
    assert "not a markdown" in err


def test_run_invalid_leaves_json_returns_2(demo_skill, tmp_path, capsys):
    leaves = tmp_path / "bad-leaves.json"
    leaves.write_text("not valid json", encoding="utf-8")
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
            "--leaves",
            str(leaves),
        ]
    )
    assert code == 2


def test_run_malformed_contract_block_returns_1(tmp_path, capsys):
    """Single-file equivalent of the old invalid-sidecar-YAML case: a step
    section whose inline ```yaml``` contract block is not valid YAML →
    PipelineValidationError at compile → exit 1 with a compile message."""
    canonical = textwrap.dedent(
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

        # Bad

        ## Step 1: produce <!-- :: section_id = step_1 :: -->

        ```yaml
        role: CORE
        aggregation: [unterminated
        ```

        PRODUCE.
        """
    )
    skill = tmp_path / "skill_bad.md"
    skill.write_text(canonical, encoding="utf-8")
    code = main(
        [
            "composer",
            "run",
            str(skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
        ]
    )
    assert code == 1
    err = capsys.readouterr().err
    assert "failed to compile" in err
    assert "not valid YAML" in err


def test_run_bad_role_enum_returns_1(tmp_path, capsys):
    """Single-file equivalent of the old schema-violation case: an inline
    contract block with a bad ``role`` enum → schema validation failure →
    exit 1 at compile."""
    canonical = _CANONICAL.replace("role: CORE", "role: INVENTED_ROLE", 1)
    skill = tmp_path / "skill_badrole.md"
    skill.write_text(canonical, encoding="utf-8")
    code = main(
        [
            "composer",
            "run",
            str(skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
        ]
    )
    assert code == 1
    err = capsys.readouterr().err
    assert "failed to compile" in err
    assert "schema validation" in err


def test_run_default_backend_is_mock(demo_skill, tmp_path, capsys):
    """No --backend flag → MockBackend."""
    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
            "--format",
            "json",
        ]
    )
    assert code == 0


def test_run_backend_anthropic_without_sdk_returns_2(
    demo_skill, tmp_path, capsys, monkeypatch
):
    """When the anthropic SDK isn't available, --backend=anthropic returns 2
    with a clear hint to install [agent] extras."""
    # Force the import to fail regardless of whether anthropic is actually
    # installed in the test environment.
    import builtins
    real_import = builtins.__import__

    def fail_anthropic_import(name, *args, **kwargs):
        if name == "anthropic":
            raise ImportError("anthropic not installed (test stub)")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fail_anthropic_import)

    code = main(
        [
            "composer",
            "run",
            str(demo_skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
            "--backend",
            "anthropic",
        ]
    )
    assert code == 2
    err = capsys.readouterr().err
    assert "[agent]" in err or "extras" in err


# ── v4 dynamic scheduler path (`--dynamic`, opt-in) ─────────────────────────


_PERLEAF_CANONICAL = textwrap.dedent(
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
    """
)


@pytest.fixture
def perleaf_skill(tmp_path: Path) -> Path:
    skill = tmp_path / "skill_pl.md"
    skill.write_text(_PERLEAF_CANONICAL, encoding="utf-8")
    return skill


def _leaves_file(tmp_path: Path, ids: list[str]) -> Path:
    p = tmp_path / "leaves.json"
    p.write_text(json.dumps([{"id": i} for i in ids]), encoding="utf-8")
    return p


def test_run_dynamic_basic(perleaf_skill, tmp_path, capsys):
    """`--dynamic` routes to run_pipeline_dynamic and runs every leaf."""
    leaves = _leaves_file(tmp_path, ["a", "b", "c"])
    code = main(
        [
            "composer", "run", str(perleaf_skill),
            "--vault", str(tmp_path / "vault"),
            "--no-trace", "--leaves", str(leaves),
            "--dynamic", "--workers", "3",
            "--format", "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["step_invocation_count"] == 3
    assert payload["error_count"] == 0


def test_run_dynamic_matches_serial(perleaf_skill, tmp_path, capsys):
    """Same skill/leaves through serial and --dynamic → same invocation count
    + error count (parity at the CLI level)."""
    leaves = _leaves_file(tmp_path, ["a", "b", "c"])
    args = [
        "composer", "run", str(perleaf_skill),
        "--no-trace", "--leaves", str(leaves), "--format", "json",
    ]
    assert main(args + ["--vault", str(tmp_path / "v_serial")]) == 0
    serial = json.loads(capsys.readouterr().out)
    assert main(args + ["--vault", str(tmp_path / "v_dyn"), "--dynamic"]) == 0
    dynamic = json.loads(capsys.readouterr().out)
    assert serial["step_invocation_count"] == dynamic["step_invocation_count"]
    assert serial["error_count"] == dynamic["error_count"] == 0
    assert (
        sorted(r["leaf_id"] for r in serial["step_results"])
        == sorted(r["leaf_id"] for r in dynamic["step_results"])
    )


def test_run_dynamic_writes_manifest(perleaf_skill, tmp_path, capsys):
    leaves = _leaves_file(tmp_path, ["a", "b"])
    manifest = tmp_path / "manifest.json"
    code = main(
        [
            "composer", "run", str(perleaf_skill),
            "--vault", str(tmp_path / "vault"),
            "--no-trace", "--leaves", str(leaves),
            "--dynamic", "--manifest", str(manifest),
        ]
    )
    assert code == 0
    assert manifest.exists()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["entries"]
    assert all(e["status"] == "done" for e in data["entries"].values())


def test_run_dynamic_writes_statistics(perleaf_skill, tmp_path, capsys):
    leaves = _leaves_file(tmp_path, ["a", "b", "c"])
    stats = tmp_path / "statistics.json"
    code = main(
        [
            "composer", "run", str(perleaf_skill),
            "--vault", str(tmp_path / "vault"),
            "--no-trace", "--leaves", str(leaves),
            "--dynamic", "--stats", str(stats),
        ]
    )
    assert code == 0
    payload = json.loads(stats.read_text(encoding="utf-8"))
    assert payload["invocation_count"] == 3
    assert payload["error_count"] == 0
    assert payload["per_stage"]["step_1"]["succeeded"] == 3


def test_run_dynamic_budget_halts_runaway(perleaf_skill, tmp_path, capsys):
    """--max-invocations below the leaf count → some leaves halt with a typed
    BUDGET_EXHAUSTED outcome, surfacing as errors + a non-zero exit."""
    leaves = _leaves_file(tmp_path, ["a", "b", "c", "d"])
    code = main(
        [
            "composer", "run", str(perleaf_skill),
            "--vault", str(tmp_path / "vault"),
            "--no-trace", "--leaves", str(leaves),
            "--dynamic", "--workers", "1", "--max-invocations", "2",
            "--format", "json",
        ]
    )
    assert code == 1  # some leaves errored (budget-exhausted)
    payload = json.loads(capsys.readouterr().out)
    assert payload["error_count"] == 2  # 4 leaves, budget 2 → 2 halted
    budget_errs = [
        r for r in payload["step_results"]
        if r["error"] and "budget exhausted" in r["error"]
    ]
    assert len(budget_errs) == 2


def test_run_dynamic_close_gate_blocks_ungrounded(tmp_path, capsys):
    """--close-gate without a grounding verifier → grounding fails closed →
    a format-clean written note still can't close (session blocked → error)."""
    # A writer skill whose materializer actually writes a note file.
    canonical = textwrap.dedent(
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

        ## Step 1: write <!-- :: section_id = step_1 :: -->

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

        Write for {{leaf.id}}.
        """
    )
    skill = tmp_path / "skill_w.md"
    skill.write_text(canonical, encoding="utf-8")

    note_body = textwrap.dedent(
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

        # Written Note

        ## Purpose

        A grounded body.
        """
    )
    # The rendered prompt is "Write for leaf_0." — key on the "Write" substring.
    responses = tmp_path / "resp.json"
    responses.write_text(
        json.dumps({"Write": json.dumps({"output_path": "notes/out.md", "body_markdown": note_body})}),
        encoding="utf-8",
    )
    leaves = _leaves_file(tmp_path, ["a"])
    code = main(
        [
            "composer", "run", str(skill),
            "--vault", str(tmp_path / "vault"),
            "--no-trace", "--leaves", str(leaves),
            "--mock-responses", str(responses),
            "--dynamic", "--close-gate",
            "--format", "json",
        ]
    )
    # Format passes but grounding fails closed (no verifier) → session blocked
    # → the otherwise-clean capture is rewritten to an errored result.
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error_count"] == 1
    assert "close-gate blocked (grounding)" in payload["step_results"][0]["error"]


def _writer_skill_for_wave(tmp_path: Path) -> Path:
    """A per-leaf writer skill for the --wave-gate test."""
    canonical = textwrap.dedent(
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

        # WW

        ## Step 1: write <!-- :: section_id = step_1 :: -->

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

        Write for {{leaf.id}}.
        """
    )
    skill = tmp_path / "skill_ww.md"
    skill.write_text(canonical, encoding="utf-8")
    return skill


def test_run_dynamic_wave_gate_flags_duplicate_paths(tmp_path, capsys):
    """--wave-gate: two sessions writing the SAME output_path is a cross-set
    dedup violation a per-session gate can't see → both flagged errored."""
    skill = _writer_skill_for_wave(tmp_path)
    # Both leaves get the SAME output_path via the default mock response.
    responses = tmp_path / "resp.json"
    responses.write_text(
        json.dumps(
            {"Write": json.dumps({"output_path": "notes/dup.md", "body_markdown": "# X\n"})}
        ),
        encoding="utf-8",
    )
    leaves = _leaves_file(tmp_path, ["a", "b"])
    code = main(
        [
            "composer", "run", str(skill),
            "--vault", str(tmp_path / "vault"),
            "--no-trace", "--leaves", str(leaves),
            "--mock-responses", str(responses),
            "--dynamic", "--wave-gate",
            "--format", "json",
        ]
    )
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error_count"] == 2
    assert all(
        "wave-gate blocked (dedup)" in r["error"] for r in payload["step_results"]
    )


def test_run_dynamic_wave_gate_clean_when_paths_distinct(tmp_path, capsys):
    """--wave-gate passes when sessions write distinct paths (no false positive)."""
    skill = _writer_skill_for_wave(tmp_path)
    # Per-leaf distinct paths: the rendered prompt is "Write for <id>." where
    # <id> is the leaf's `id` field (a / b) — key each response on that.
    responses = tmp_path / "resp.json"
    responses.write_text(
        json.dumps(
            {
                "Write for a": json.dumps({"output_path": "notes/a.md", "body_markdown": "# A\n"}),
                "Write for b": json.dumps({"output_path": "notes/b.md", "body_markdown": "# B\n"}),
            }
        ),
        encoding="utf-8",
    )
    leaves = _leaves_file(tmp_path, ["a", "b"])
    code = main(
        [
            "composer", "run", str(skill),
            "--vault", str(tmp_path / "vault"),
            "--no-trace", "--leaves", str(leaves),
            "--mock-responses", str(responses),
            "--dynamic", "--wave-gate",
            "--format", "json",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["error_count"] == 0


def test_run_dynamic_context_strategy_bounds_fail_soft(tmp_path, capsys):
    """--context-strategy makes an oversized prompt degrade (truncate + warn)
    instead of erroring — the run stays clean where the hard cap would fail."""
    skill = _writer_skill_for_wave(tmp_path)
    # Distinct paths so the (uninvolved) wave logic can't confound this;
    # the leaf ids carry a large body via the prompt {{leaf.id}}.
    responses = tmp_path / "resp.json"
    responses.write_text(
        json.dumps({"Write": json.dumps({"output_path": "notes/a.md", "body_markdown": "# A\n"})}),
        encoding="utf-8",
    )
    leaves = tmp_path / "leaves.json"
    leaves.write_text(json.dumps([{"id": "Z" * 5000}]), encoding="utf-8")
    code = main(
        [
            "composer", "run", str(skill),
            "--vault", str(tmp_path / "vault"),
            "--no-trace", "--leaves", str(leaves),
            "--mock-responses", str(responses),
            "--dynamic", "--context-strategy", "full_source",
            "--context-max-chars", "300",
            "--format", "json",
        ]
    )
    assert code == 0  # bounded fail-soft, not a hard-cap error
    payload = json.loads(capsys.readouterr().out)
    assert payload["error_count"] == 0


def test_run_dynamic_skip_unchanged_pre_gate(perleaf_skill, tmp_path, capsys):
    """--skip-unchanged: first run executes all leaves + writes the store;
    an identical second run skips them all (0 invocations); changing a leaf
    re-runs just that one."""
    fps = tmp_path / "fp.json"

    def _run(leaves_list):
        leaves = tmp_path / "leaves.json"
        leaves.write_text(json.dumps(leaves_list), encoding="utf-8")
        code = main(
            [
                "composer", "run", str(perleaf_skill),
                "--vault", str(tmp_path / "vault"),
                "--no-trace", "--leaves", str(leaves),
                "--dynamic", "--skip-unchanged", str(fps),
                "--format", "json",
            ]
        )
        return code, json.loads(capsys.readouterr().out)

    # Run 1: fresh store → both leaves run.
    code1, p1 = _run([{"_id": "a", "id": "a", "body": "X"}, {"_id": "b", "id": "b", "body": "Y"}])
    assert code1 == 0
    assert p1["step_invocation_count"] == 2
    assert fps.is_file()

    # Run 2: identical leaves → all skipped → 0 invocations (no corpus fallback).
    code2, p2 = _run([{"_id": "a", "id": "a", "body": "X"}, {"_id": "b", "id": "b", "body": "Y"}])
    assert code2 == 0
    assert p2["step_invocation_count"] == 0
    assert p2["step_results"] == []

    # Run 3: leaf b changed → only b runs.
    code3, p3 = _run([{"_id": "a", "id": "a", "body": "X"}, {"_id": "b", "id": "b", "body": "CHANGED"}])
    assert code3 == 0
    assert p3["step_invocation_count"] == 1


def test_run_fix_with_backend_requires_close_gate(tmp_path, capsys):
    """--fix-with-backend without --close-gate is an invocation error (2)."""
    skill = _writer_skill_for_wave(tmp_path)
    leaves = _leaves_file(tmp_path, ["a"])
    code = main(
        [
            "composer", "run", str(skill),
            "--vault", str(tmp_path / "vault"),
            "--no-trace", "--leaves", str(leaves),
            "--dynamic", "--fix-with-backend",
        ]
    )
    assert code == 2
    assert "requires --close-gate" in capsys.readouterr().err


def test_run_fix_with_backend_repairs_failing_note(tmp_path, capsys):
    """--fix-with-backend repairs a format-failing captured note via the
    LLM fixer (same --backend) so the session closes clean."""
    skill = _writer_skill_for_wave(tmp_path)
    good_note = textwrap.dedent(
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

        # Fixed

        ## Purpose

        Repaired.
        """
    )
    bad_note = "---\ntags:\n  - resource\n---\n\n# Broken\n"
    # The mock backend serves BOTH capture (a "Write" prompt → the bad note
    # JSON envelope) AND the fixer (a repair prompt → the good note text).
    responses = tmp_path / "resp.json"
    responses.write_text(
        json.dumps(
            {
                "Write": json.dumps({"output_path": "notes/out.md", "body_markdown": bad_note}),
                "note-repair": good_note,  # the fixer's system prompt won't match; use body key
                "Current note text": good_note,  # matches the fixer's user prompt section
            }
        ),
        encoding="utf-8",
    )
    leaves = _leaves_file(tmp_path, ["a"])
    code = main(
        [
            "composer", "run", str(skill),
            "--vault", str(tmp_path / "vault"),
            "--no-trace", "--leaves", str(leaves),
            "--mock-responses", str(responses),
            "--dynamic", "--close-gate", "--fix-with-backend", "--max-fix-rounds", "2",
            "--format", "json",
        ]
    )
    # Grounding fails closed without a verifier, but the format repair path is
    # exercised; the note on disk is the repaired version regardless.
    written = (tmp_path / "vault" / "notes" / "out.md").read_text(encoding="utf-8")
    assert "# Fixed" in written  # the fixer rewrote the note in place
    _ = code  # exit code depends on grounding; the repair-in-place is the assertion


def test_run_pipeline_none_returns_0(tmp_path, capsys):
    """Single-file equivalent of the old ``pipeline_metadata: none``: a skill
    whose sections carry NO ```yaml``` contract block compiles to an empty
    pipeline (0 steps) → the CLI reports nothing to run and exits 0."""
    canonical = textwrap.dedent(
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

        # Demo

        ## Setup

        Prose only — no contract block, so this is not a pipeline step.

        ## Step 1: produce <!-- :: section_id = step_1 :: -->

        PRODUCE (prose only, no contract block → not a dispatchable step).
        """
    )
    skill = tmp_path / "skill_demo.md"
    skill.write_text(canonical, encoding="utf-8")
    code = main(
        [
            "composer",
            "run",
            str(skill),
            "--vault",
            str(tmp_path / "vault"),
            "--no-trace",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "nothing to run" in out
