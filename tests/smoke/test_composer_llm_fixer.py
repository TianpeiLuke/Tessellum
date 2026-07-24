"""make_llm_fixer — a real LLM-backed informed fixer for the close-gate loop.

Covers: the fixer reads the note + gate issues + prior-attempt history into
its prompt, writes the backend's corrected text back in place, and is
fail-soft (empty note / empty response = no-op). Plus the end-to-end path:
a format-failing captured note is repaired by the fixer, re-gated, and the
session closes clean; and revert-to-BEST still protects against a
regressing repair.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

from tessellum.composer import (
    FixContext,
    GroundingVerdict,
    MockBackend,
    RunBudget,
    build_close_gate,
    compile_skill,
    make_llm_fixer,
    run_fix_loop,
    run_pipeline_dynamic,
)
from tessellum.composer.fix import AttemptOutcome
from tessellum.composer.llm import LLMRequest, LLMResponse


class _RecordingBackend:
    """Backend that returns a fixed body and records the prompts it saw."""

    backend_id = "rec"

    def __init__(self, body: str) -> None:
        self.body = body
        self.prompts: list[LLMRequest] = []

    def call(self, request: LLMRequest) -> LLMResponse:
        self.prompts.append(request)
        return LLMResponse(content=self.body, elapsed_ms=1.0, backend_id="rec")


def test_llm_fixer_writes_corrected_note(tmp_path: Path) -> None:
    note = tmp_path / "n.md"
    note.write_text("BROKEN original", encoding="utf-8")
    backend = _RecordingBackend("CORRECTED note text")
    fixer = make_llm_fixer(backend)
    fixer(FixContext(note_path=note, issues=(), prior_attempts=()))
    assert note.read_text(encoding="utf-8") == "CORRECTED note text"


def test_llm_fixer_prompt_includes_issues_and_current(tmp_path: Path) -> None:
    from tessellum.format import Issue, Severity

    note = tmp_path / "n.md"
    note.write_text("current body here", encoding="utf-8")
    backend = _RecordingBackend("fixed")
    fixer = make_llm_fixer(backend)
    issues = (Issue(Severity.ERROR, "YAML-050", "date of note", "required field missing"),)
    fixer(FixContext(note_path=note, issues=issues, prior_attempts=()))
    prompt = backend.prompts[0].user_prompt
    assert "current body here" in prompt          # the note text is included
    assert "YAML-050" in prompt                    # the issue rule id is included
    assert "required field missing" in prompt      # the issue message is included


def test_llm_fixer_prompt_includes_prior_attempts(tmp_path: Path) -> None:
    note = tmp_path / "n.md"
    note.write_text("body", encoding="utf-8")
    backend = _RecordingBackend("fixed")
    fixer = make_llm_fixer(backend)
    prior = (AttemptOutcome(round_n=1, score=2, causes=("format",)),)
    fixer(FixContext(note_path=note, issues=(), prior_attempts=prior))
    prompt = backend.prompts[0].user_prompt
    assert "round 1" in prompt
    assert "different fix" in prompt  # the nudge to try something else


def test_llm_fixer_empty_response_is_noop(tmp_path: Path) -> None:
    note = tmp_path / "n.md"
    note.write_text("keep me", encoding="utf-8")
    fixer = make_llm_fixer(MockBackend(default=""))  # empty backend response
    fixer(FixContext(note_path=note, issues=(), prior_attempts=()))
    assert note.read_text(encoding="utf-8") == "keep me"  # unchanged (no-op)


def test_llm_fixer_missing_note_is_noop(tmp_path: Path) -> None:
    note = tmp_path / "does_not_exist.md"
    backend = _RecordingBackend("would-be fix")
    fixer = make_llm_fixer(backend)
    fixer(FixContext(note_path=note, issues=(), prior_attempts=()))
    assert not note.exists()          # not created
    assert backend.prompts == []      # backend never called (nothing to repair)


def test_llm_fixer_respects_shared_run_budget(tmp_path: Path) -> None:
    note = tmp_path / "n.md"
    note.write_text("keep me", encoding="utf-8")
    backend = _RecordingBackend("would-be fix")
    fixer = make_llm_fixer(
        backend,
        budget=RunBudget(max_invocations=0),
    )

    fixer(FixContext(note_path=note, issues=(), prior_attempts=()))

    assert backend.prompts == []
    assert note.read_text(encoding="utf-8") == "keep me"


def test_llm_fixer_in_run_fix_loop_repairs_and_passes(tmp_path: Path) -> None:
    """The fix loop drives the LLM fixer; a repair that clears the gate ends
    the loop passing."""
    note = tmp_path / "n.md"
    note.write_text("bad", encoding="utf-8")
    backend = _RecordingBackend("good")

    # Evaluate: fails until the note text is "good".
    def evaluate():
        txt = note.read_text(encoding="utf-8")
        if txt == "good":
            return True, None, []
        return False, "format", [1]

    result = run_fix_loop(
        note_path=note,
        evaluate=evaluate,
        fixer=make_llm_fixer(backend),
        max_rounds=2,
    )
    assert result.passed
    assert note.read_text(encoding="utf-8") == "good"


def test_llm_fixer_revert_to_best_protects_regression(tmp_path: Path) -> None:
    """A regressing LLM repair never overwrites a better earlier note — the
    loop restores the BEST-scoring snapshot."""
    note = tmp_path / "n.md"
    note.write_text("v0", encoding="utf-8")
    # The fixer writes progressively; scores are keyed off the text.
    bodies = iter(["v1", "v2"])

    class _SeqBackend:
        backend_id = "seq"

        def call(self, request: LLMRequest) -> LLMResponse:
            return LLMResponse(content=next(bodies), elapsed_ms=1.0, backend_id="seq")

    scores = {"v0": 2, "v1": 1, "v2": 3}  # v1 best, v2 regresses

    def evaluate():
        txt = note.read_text(encoding="utf-8")
        s = scores.get(txt, 9)
        return (s == 0), "format", list(range(s))

    result = run_fix_loop(
        note_path=note,
        evaluate=evaluate,
        fixer=make_llm_fixer(_SeqBackend()),
        max_rounds=2,
    )
    assert not result.passed
    assert result.final_score == 1        # best achieved (v1)
    assert result.reverted
    assert note.read_text(encoding="utf-8") == "v1"  # NOT the regressed v2


# ── End-to-end: LLM fixer wired into run_pipeline_dynamic ───────────────────


# Single-file skill: the step's contract block lives under the anchored H2,
# with the prompt prose after it (no .pipeline.yaml sidecar).
_CANON = textwrap.dedent(
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

    Write.
    """
)

_BAD_NOTE = "---\ntags:\n  - resource\n---\n\n# Broken\n"

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

    # Fixed Note

    ## Purpose

    Repaired.
    """
)


def test_dynamic_llm_fixer_repairs_failing_note(tmp_path: Path) -> None:
    sk = tmp_path / "s.md"
    sk.write_text(_CANON, encoding="utf-8")
    compiled = compile_skill(sk)

    # Capture writes the format-FAILING note.
    capture_backend = MockBackend(
        default=json.dumps({"output_path": "notes/out.md", "body_markdown": _BAD_NOTE})
    )
    # The fixer backend returns the GOOD note text.
    fixer = make_llm_fixer(MockBackend(default=_GOOD_NOTE))

    run = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}],
        backend=capture_backend,
        vault_root=tmp_path / "v",
        close_gate=build_close_gate(),
        grounding_verifier=lambda s, leaf, r: GroundingVerdict("grounded"),
        informed_fixer=fixer,
        max_fix_rounds=2,
    )
    assert run.error_count == 0  # repaired → close-gate passed → session done
    written = (tmp_path / "v" / "notes" / "out.md").read_text(encoding="utf-8")
    assert "Fixed Note" in written
    assert "building_block: concept" in written


def test_dynamic_llm_fixer_blocks_when_repair_fails(tmp_path: Path) -> None:
    """If the fixer can't produce a passing note, the session still blocks
    (never silently closes done)."""
    sk = tmp_path / "s.md"
    sk.write_text(_CANON, encoding="utf-8")
    compiled = compile_skill(sk)

    capture_backend = MockBackend(
        default=json.dumps({"output_path": "notes/out.md", "body_markdown": _BAD_NOTE})
    )
    # The fixer returns STILL-broken text → never passes.
    fixer = make_llm_fixer(MockBackend(default=_BAD_NOTE))

    run = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}],
        backend=capture_backend,
        vault_root=tmp_path / "v",
        close_gate=build_close_gate(),
        grounding_verifier=lambda s, leaf, r: GroundingVerdict("grounded"),
        informed_fixer=fixer,
        max_fix_rounds=2,
    )
    assert run.error_count == 1
    assert "close-gate blocked" in run.step_results[0].error
