"""R3.5 (FZ 20k9c1a1a1b7c2k2a1c) — failing-then-passing regressions for the
J3 prose-only fixes (F1/F2/F4), retiring their "patched, not fixed" status.

Each test renders the REAL step's prompt exactly as the executor does and
asserts the grounding the fix added is actually present in the rendered text
— on the runtime M0 shape (F1) and the revise-round shape (F2/F4). Before
the fixes these prompts carried acquisition prose with nothing bound; the
model role-played (F1/F2) or revised blind (F4).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.composer.compiler import compile_skill
from tessellum.composer.executor import _resolve_placeholders
from tessellum.composer.parity import _normalize

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "vault" / "resources" / "skills"

_CORPUS = "# Demo\n\n## Overview\n\n" + ("distinctive source words here. " * 300)


def _skills_present() -> bool:
    return (SKILLS / "skill_tessellum_plan_digestion.md").is_file()


def _m0_leaf() -> dict:
    return _normalize({
        "_id": "job1", "source_url": "file:///tmp/demo.md",
        "source_name": "demo.md", "source_type": "local_file",
        "source_content": _CORPUS, "member_count": 1, "members": [],
    })


def _render(skill: str, section_id: str, leaf: dict, *, artifacts=None) -> str:
    pipeline = compile_skill(SKILLS / f"{skill}.md")
    step = next(s for s in pipeline.steps if s.section_id == section_id)
    return _resolve_placeholders(
        step.prompt_section_text, leaf=leaf, upstream={}, artifacts=artifacts or {},
    )


@pytest.mark.skipif(not _skills_present(), reason="real skills not present")
def test_f1_identify_source_prompt_carries_ledger_and_source() -> None:
    """F1: on the M0 shape, identify_source receives the code ledger AND the
    inline source — the pre-fix prompt had only a file:// URI and 'read the
    source' prose (the model role-played a fake tool session)."""
    leaf = _m0_leaf()
    prompt = _render("skill_tessellum_plan_digestion", "identify_source", leaf)
    assert "measured_words" in prompt                      # the ledger rendered
    assert "distinctive source words here." in prompt      # the source rendered
    assert "<missing leaf.pages>" not in prompt
    assert "<missing leaf.source_excerpt>" not in prompt
    assert "NEVER emit" in prompt                          # the no-tools mandate


@pytest.mark.skipif(not _skills_present(), reason="real skills not present")
def test_f2_read_draft_prompt_carries_the_draft() -> None:
    """F2: read_draft receives the of-record draft by reference — the pre-fix
    prompt said 'read the draft plan file at $PLANS_DIR/…' with nothing
    bound (round 1 fabricated a plausible assessment; round 2 role-played)."""
    leaf = dict(_m0_leaf(), review_failures="")
    prompt = _render(
        "skill_tessellum_augment_digestion_plan", "read_draft", leaf,
        artifacts={"plan_text": "# THE DRAFT PLAN BODY\n\n## Objective\n"},
    )
    assert "THE DRAFT PLAN BODY" in prompt
    assert "NEVER emit" in prompt


@pytest.mark.skipif(not _skills_present(), reason="real skills not present")
def test_f4_writer_prompt_carries_failures_draft_and_ledger() -> None:
    """F4: the revise directives reach the step that rewrites the plan — with
    the draft and the ledger — instead of dying in read_draft's schema."""
    leaf = dict(
        _m0_leaf(),
        review_failures="- CP7 FAIL: record the exact measured figure 12813",
    )
    prompt = _render(
        "skill_tessellum_augment_digestion_plan", "write_augmented_plan", leaf,
        artifacts={
            "plan_text": "# THE DRAFT PLAN BODY\n",
            "pages": [{"measured_words": 12813, "headings": ["Demo"]}],
        },
    )
    assert "record the exact measured figure 12813" in prompt  # failures arrive
    assert "THE DRAFT PLAN BODY" in prompt                     # the draft arrives
    assert "12813" in prompt                                   # the ledger arrives
    assert "concrete edit instructions" in prompt              # the revise mandate
