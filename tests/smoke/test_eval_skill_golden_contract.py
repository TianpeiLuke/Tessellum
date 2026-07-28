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


# ── P19 (FZ 20k9c1a1a1b7c2g): golden facts derive from the ONE vault contract ──
# frontmatter_spec is the single source of truth (authoritative: DEVELOPING.md).
# These bind the eval golden facts to it so the scorer and the shipped validator
# can never again return opposite verdicts on the same note (the pre-P19 state:
# the golden wrongly forbade `folgezettel`/`last_updated`/`author`/`related_wiki`,
# all legitimate vault fields, and the validator permitted them).

from tessellum.format.frontmatter_spec import (  # noqa: E402
    FORBIDDEN_FIELDS,
    OPTIONAL_COMMON_FIELDS,
    REQUIRED_FIELDS,
    required_fields_for,
)


def test_golden_forbidden_matches_single_source():
    """Each slice's golden forbidden set must equal the vault contract's
    FORBIDDEN_FIELDS — not a hand-drifted superset. This is the test that would
    have caught the `folgezettel` contradiction (golden forbade it; the validator
    + DEVELOPING.md permit it as a legitimate trail field)."""
    slices = _slice_golden_facts()
    if not slices:
        pytest.skip(f"no golden slices found under {EVAL_DIR}")
    for slice_name, facts in slices:
        golden_forbidden = set(facts["golden_output"]["frontmatter_forbidden_keys"])
        assert golden_forbidden == set(FORBIDDEN_FIELDS), (
            f"[{slice_name}] golden forbidden set drifted from the single-source "
            f"frontmatter_spec.FORBIDDEN_FIELDS. "
            f"extra={sorted(golden_forbidden - set(FORBIDDEN_FIELDS))} "
            f"missing={sorted(set(FORBIDDEN_FIELDS) - golden_forbidden)}"
        )


def test_golden_never_forbids_a_legitimate_optional_field():
    """The golden must never forbid a field the vault contract permits — a
    forbidden ∩ (required ∪ optional-common) intersection means the scorer would
    reject a note the validator accepts (the pre-P19 opposite-verdict hazard)."""
    slices = _slice_golden_facts()
    if not slices:
        pytest.skip("no golden slices")
    legit = set(REQUIRED_FIELDS) | set(OPTIONAL_COMMON_FIELDS) | {"folgezettel", "folgezettel_parent"}
    for slice_name, facts in slices:
        forbidden = set(facts["golden_output"]["frontmatter_forbidden_keys"])
        clash = forbidden & legit
        assert not clash, (
            f"[{slice_name}] golden forbids legitimate vault field(s) {sorted(clash)} "
            f"— the scorer would reject a note the validator accepts"
        )


def test_golden_required_is_contract_required_for_its_note_type():
    """A slice's golden required keys = the vault contract's required set for that
    slice's note type (universal 7 + type-specific). The doc slices are
    `documentation`, so they legitimately add `source_url`; `access_control_group`
    is the recommended access tag. Guards that the required set stays derived, not
    a hand-typed list that can drift from `required_fields_for`."""
    slices = _slice_golden_facts()
    if not slices:
        pytest.skip("no golden slices")
    for slice_name, facts in slices:
        golden_req = set(facts["golden_output"]["frontmatter_required_keys"])
        # doc slices → documentation second-category
        expected = set(required_fields_for("documentation")) | {"access_control_group"}
        assert golden_req == expected, (
            f"[{slice_name}] golden required {sorted(golden_req)} != "
            f"contract-derived {sorted(expected)} for a documentation note"
        )
