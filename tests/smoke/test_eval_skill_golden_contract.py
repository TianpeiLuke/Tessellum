"""Skill↔golden contract — the execute skill must instruct what the eval scores.

Tier-0 of the digestion hardening roadmap (the "eval-parity blockers"). The
golden reproduction eval scores a generated note against each slice's
``golden_facts.json``: it requires a set of frontmatter keys
(``frontmatter_required_keys``) and a set of body H2 sections (``required_h2``).
If the execute skill's OUTPUT FORMAT does not *instruct* those keys/sections, a
faithful run cannot reproduce them and the eval is capped below GREEN for a
reason that has nothing to do with digestion quality.

The golden-self-consistency check cannot catch this: the golden notes already
conform to themselves. Only a check that reads the *skill* against the *golden
facts* surfaces the drift. This test is that check.

Regression guard for:
- R1 — the skill instructed ``## References`` for graph edges while the golden
  requires ``## Related Notes``; and it never instructed the universal
  ``## Overview`` lead section the golden requires.
- R2 — the OUTPUT FORMAT omitted ``access_control_group`` (E10 incomplete).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
EXECUTE_SKILL = REPO / "vault" / "resources" / "skills" / "skill_tessellum_execute_digestion_plan.md"
EVAL_DIR = REPO / "eval" / "digestion_pipeline"


def _slice_golden_facts() -> list[tuple[str, dict]]:
    if not EVAL_DIR.is_dir():
        return []
    out: list[tuple[str, dict]] = []
    for facts in sorted(EVAL_DIR.glob("*/golden_facts.json")):
        out.append((facts.parent.name, json.loads(facts.read_text(encoding="utf-8"))))
    return out


def _skill_text() -> str:
    return EXECUTE_SKILL.read_text(encoding="utf-8")


def test_execute_skill_instructs_every_golden_frontmatter_key():
    """Every ``frontmatter_required_keys`` entry must be named in the skill.

    ``output_path`` is the coordination key (always instructed); the rest are the
    note's own frontmatter fields the writer must emit. If the golden requires a
    key the skill never mentions, a conforming note can't produce it → N1 < 1.0.
    """
    if not EXECUTE_SKILL.is_file():
        pytest.skip(f"execute skill not found at {EXECUTE_SKILL}")
    slices = _slice_golden_facts()
    if not slices:
        pytest.skip(f"no golden slices found under {EVAL_DIR}")
    text = _skill_text()
    for slice_name, facts in slices:
        req = facts["golden_output"]["frontmatter_required_keys"]
        missing = [k for k in req if k not in text]
        assert not missing, (
            f"[{slice_name}] execute skill OUTPUT FORMAT does not instruct "
            f"required frontmatter key(s) {missing}; a faithful run cannot "
            f"reproduce them and N1_frontmatter_schema is capped below 1.0"
        )


def test_execute_skill_instructs_every_golden_required_h2():
    """Every ``required_h2`` section must be instructed by the skill.

    The universal sections (``Overview``, ``Related Notes``) are instructed in
    the OUTPUT FORMAT BODY STRUCTURE block; type-specific sections come from the
    injected NOTE-TYPE CONTRACT at run time. This asserts the universal ones the
    golden requires on *every* note are present as literal ``## <name>`` (or a
    bare mention) in the skill text → otherwise N3_required_h2 is capped.
    """
    if not EXECUTE_SKILL.is_file():
        pytest.skip(f"execute skill not found at {EXECUTE_SKILL}")
    slices = _slice_golden_facts()
    if not slices:
        pytest.skip(f"no golden slices found under {EVAL_DIR}")
    text = _skill_text()
    for slice_name, facts in slices:
        required_h2 = facts["golden_output"].get("required_h2", [])
        missing = [h for h in required_h2 if f"## {h}" not in text and h not in text]
        assert not missing, (
            f"[{slice_name}] execute skill does not instruct required H2 "
            f"section(s) {missing}; a faithful run cannot reproduce them and "
            f"N3_required_h2 is capped below 1.0"
        )


def test_execute_skill_uses_related_notes_not_references_for_edges():
    """Graph edges must be instructed under ``## Related Notes`` (R1 guard).

    ``## References`` is external-URL-only; using it for internal graph edges
    diverges from the golden convention and zeroes N3. The skill may still
    *mention* ``## References`` to say "NOT ## References", so we assert the
    positive instruction (the RELATED NOTES → ## Related Notes line) exists.
    """
    if not EXECUTE_SKILL.is_file():
        pytest.skip(f"execute skill not found at {EXECUTE_SKILL}")
    text = _skill_text()
    assert "`## Related Notes`" in text or "## Related Notes" in text, (
        "execute skill must instruct graph edges under `## Related Notes`"
    )
    assert "RELATED NOTES → `## Related Notes`" in text, (
        "the RELATED NOTES instruction must point at `## Related Notes` "
        "(the vault graph-edge convention), not `## References`"
    )
