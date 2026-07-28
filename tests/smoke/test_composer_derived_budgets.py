"""P12 (FZ 20k9c1a1a1b7c2e) — per-step budgets DERIVED from declared work.

The E14/E17 fix hand-set ``max_tokens: 32000`` + ``timeout_seconds: 900`` on the
big-output writers — which closes the symptom per step but not the class: a plan
declaring 200 notes still inherits a constant tuned for a small plan and
truncates. P12 lets a step declare a per-note coefficient
(``max_tokens_per_note`` / ``timeout_seconds_per_note``); the driver
(``_derive_step_budgets``) rewrites the effective budget at runtime from
``total_notes`` — the hand-set value a FLOOR the derivation can only raise,
clamped to the P16-shared ceiling. Inert (byte-identical) until a step opts in.

Covers: the loader→compiler coefficient passthrough; the derivation formula +
identity guards (no coeff / 0 notes → unchanged) + floor + ceiling + timeout;
and that the shipped augment skill scales on a large plan but stays at the floor
on a small one.

Pure — no LLM, no network. Safe alongside a live run.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from tessellum.composer.compiler import CompiledPipeline, CompiledStep, compile_skill
from tessellum.composer.digestion import (
    DERIVED_MAX_TOKENS_CEILING,
    DERIVED_TIMEOUT_CEILING_SECONDS,
    _derive_step_budgets,
)


def _step(**kw) -> CompiledStep:
    base = dict(
        section_id="s", role="CORE", aggregation="corpus_wide", batchable=False,
        depends_on=(), materializer_key="no_op", materializer_contract=None,
        expected_output_schema=None, prompt_section_text="p", output_key="k",
    )
    base.update(kw)
    return CompiledStep(**base)


def _pipe(*steps: CompiledStep) -> CompiledPipeline:
    return CompiledPipeline(
        skill_path=Path("x"), skill_name="x", pipeline_version="1.0", steps=tuple(steps)
    )


# ── loader→compiler coefficient passthrough ──────────────────────────────────

_CANON = textwrap.dedent(
    """\
    ---
    tags: [resource, skill]
    keywords: [a, b, c]
    topics: [X, Y]
    language: markdown
    date of note: 2026-07-28
    status: active
    building_block: procedure
    ---

    # Demo

    ## Step scaler <!-- :: section_id = scaler :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: out
    max_tokens: 32000
    max_tokens_per_note: 400
    timeout_seconds: 900
    timeout_seconds_per_note: 5
    ```

    Write scaled.

    ## Step plain <!-- :: section_id = plain :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: out2
    ```

    Plain.
    """
)


def test_compiled_step_carries_per_note_coefficients(tmp_path: Path):
    sk = tmp_path / "skill_scaler.md"
    sk.write_text(_CANON, encoding="utf-8")
    by_id = {s.section_id: s for s in compile_skill(sk).steps}
    assert by_id["scaler"].max_tokens_per_note == 400
    assert by_id["scaler"].timeout_seconds_per_note == 5
    # A step omitting them stays None (no scaling).
    assert by_id["plain"].max_tokens_per_note is None
    assert by_id["plain"].timeout_seconds_per_note is None


# ── _derive_step_budgets — formula + guards ──────────────────────────────────

def test_derive_scales_max_tokens_by_note_count():
    s = _step(max_tokens=32000, max_tokens_per_note=500)
    out = _derive_step_budgets(_pipe(s), declared_notes=200)
    # min(64000, max(32000, 32000 + 500*200=132000)) = 64000
    assert out.steps[0].max_tokens == 64000


def test_derive_hand_set_is_a_floor_not_lowered():
    """A small plan on a hand-set 32000 step stays at least 32000 — the
    derivation only RAISES."""
    s = _step(max_tokens=32000, max_tokens_per_note=100)
    out = _derive_step_budgets(_pipe(s), declared_notes=8)
    assert out.steps[0].max_tokens == 32800  # 32000 + 100*8, above the floor
    assert out.steps[0].max_tokens >= 32000


def test_derive_clamps_to_ceiling():
    s = _step(max_tokens=32000, max_tokens_per_note=10000)
    out = _derive_step_budgets(_pipe(s), declared_notes=100)
    assert out.steps[0].max_tokens == DERIVED_MAX_TOKENS_CEILING


def test_derive_zero_notes_is_noop():
    """No declared-work signal → the pipeline is returned UNCHANGED (the plan
    phase, whose leaf has no total_notes yet, always hits this)."""
    s = _step(max_tokens=32000, max_tokens_per_note=500)
    out = _derive_step_budgets(_pipe(s), declared_notes=0)
    assert out.steps[0] is s  # identity — same object


def test_derive_no_coefficient_is_noop():
    s = _step(max_tokens=32000)  # no coefficient
    out = _derive_step_budgets(_pipe(s), declared_notes=500)
    assert out.steps[0] is s
    assert out.steps[0].max_tokens == 32000


def test_derive_scales_timeout():
    s = _step(timeout_seconds=900, timeout_seconds_per_note=5.0)
    out = _derive_step_budgets(_pipe(s), declared_notes=100)
    assert out.steps[0].timeout_seconds == 1400.0  # 900 + 5*100


def test_derive_timeout_ceiling():
    s = _step(timeout_seconds=900, timeout_seconds_per_note=100.0)
    out = _derive_step_budgets(_pipe(s), declared_notes=1000)
    assert out.steps[0].timeout_seconds == DERIVED_TIMEOUT_CEILING_SECONDS


def test_derive_default_base_when_no_static_max_tokens():
    """A coefficient-bearing step with NO static max_tokens uses the executor
    default (16000) as the base floor."""
    s = _step(max_tokens=None, max_tokens_per_note=1000)
    out = _derive_step_budgets(_pipe(s), declared_notes=10)
    assert out.steps[0].max_tokens == 26000  # 16000 + 1000*10


def test_derive_mixed_pipeline_only_touches_coefficient_steps():
    plain = _step(section_id="plain", max_tokens=32000)
    scaler = _step(section_id="scaler", max_tokens=32000, max_tokens_per_note=500)
    out = _derive_step_budgets(_pipe(plain, scaler), declared_notes=200)
    by_id = {s.section_id: s for s in out.steps}
    assert by_id["plain"] is plain  # untouched
    assert by_id["scaler"].max_tokens == 64000


def test_derive_preserves_pipeline_metadata():
    """Rewriting steps preserves budget_warnings / re_emission_warnings / version."""
    s = _step(max_tokens=32000, max_tokens_per_note=500)
    p = CompiledPipeline(
        skill_path=Path("x"), skill_name="x", pipeline_version="9.9",
        steps=(s,), budget_warnings=("bw",), re_emission_warnings=("rw",),
    )
    out = _derive_step_budgets(p, declared_notes=200)
    assert out.pipeline_version == "9.9"
    assert out.budget_warnings == ("bw",)
    assert out.re_emission_warnings == ("rw",)


# ── shipped-skill adoption: scales on a large plan, floored on a small one ────

def test_augment_skill_scales_on_large_plan_floored_on_small():
    skill = Path(__file__).resolve().parents[2] / "vault" / "resources" / "skills" / \
        "skill_tessellum_augment_digestion_plan.md"
    if not skill.is_file():
        return  # real skill not present
    compiled = compile_skill(skill)
    coeff_ids = {s.section_id for s in compiled.steps if s.max_tokens_per_note}
    assert coeff_ids, "the augment skill should declare per-note coefficients (P12)"
    small = _derive_step_budgets(compiled, declared_notes=8)
    large = _derive_step_budgets(compiled, declared_notes=80)
    for s_small, s_large in zip(small.steps, large.steps, strict=True):
        if s_small.max_tokens_per_note:
            assert s_small.max_tokens >= 32000  # floor holds on a small plan
            assert s_large.max_tokens > s_small.max_tokens  # scales up on a large one
            assert s_large.max_tokens <= DERIVED_MAX_TOKENS_CEILING
