"""R1.1 + R3.2 (FZ 20k9c1a1a1b7c2k2a1a/c) — input-manifest closure + parity.

The static/dynamic twins over the step input contract: the closure audit
verifies every prompt hole is declared (and every declaration referenced) in
the four shipped skills; the parity diff verifies the eval-driver leaf and
the runtime M0 leaf feed the compiled skills identically — the F1/F2 class
becomes a deterministic finding with no model call.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tessellum.composer.compiler import audit_input_closure, compile_skill
from tessellum.composer.parity import PHASE_SKILL_NAMES, diff_leaf_shapes

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "vault" / "resources" / "skills"

_CORPUS = "# Demo\n\n## Overview\n\n" + ("real source words here. " * 400)


def _skills_present() -> bool:
    return all((SKILLS / f"{n}.md").is_file() for n in PHASE_SKILL_NAMES)


@pytest.mark.skipif(not _skills_present(), reason="real skills not present")
@pytest.mark.parametrize("name", PHASE_SKILL_NAMES)
def test_shipped_skills_have_closed_input_manifests(name: str) -> None:
    """R1.1: zero findings — every hole declared, every declaration used.
    A new placeholder without a manifest entry (the next A3.2-style migration
    gap) fails THIS test the day it is written."""
    pipeline = compile_skill(SKILLS / f"{name}.md")
    assert audit_input_closure(pipeline) == []


def test_audit_reports_missing_manifest_and_undeclared_hole(tmp_path: Path) -> None:
    skill = tmp_path / "skill_demo.md"
    skill.write_text(
        "# Demo Skill\n\n"
        "## Step One <!-- :: section_id = s1 :: -->\n\n"
        "```yaml\n"
        "role: CORE\naggregation: corpus_wide\nbatchable: false\ndepends_on: []\n"
        "materializer: no_op\noutput_key: out1\n"
        "```\n\n"
        "Uses {{leaf.alpha}} with no manifest.\n\n"
        "## Step Two <!-- :: section_id = s2 :: -->\n\n"
        "```yaml\n"
        "role: CORE\naggregation: corpus_wide\nbatchable: false\ndepends_on: [s1]\n"
        "materializer: no_op\noutput_key: out2\n"
        "inputs:\n- name: leaf.beta\n  required: true\n- name: leaf.gamma\n"
        "```\n\n"
        "Uses {{leaf.beta}} and the UNDECLARED {{upstream.out1}}.\n",
        encoding="utf-8",
    )
    findings = audit_input_closure(compile_skill(skill))
    joined = "\n".join(findings)
    assert "s1" in joined and "no input manifest" in joined
    assert "undeclared input {{upstream.out1}}" in joined
    assert "'leaf.gamma' declared but never referenced" in joined


def _eval_driver_leaf() -> dict:
    return {
        "id": "demo", "source_url": "https://example.com/docs",
        "source_name": "Demo", "member_count": 1,
        "members": [{"source_id": "p1", "excerpt": _CORPUS,
                     "source_url": "https://example.com/p1"}],
    }


def _runtime_m0_leaf() -> dict:
    return {
        "_id": "job1", "source_path": "/tmp/demo.md",
        "source_url": "file:///tmp/demo.md", "source_name": "demo.md",
        "source_type": "local_file", "source_content": _CORPUS,
        "source_hash": "x", "inbox_lane": "general",
        "building_block_hint": None, "member_count": 1, "members": [],
    }


@pytest.mark.skipif(not _skills_present(), reason="real skills not present")
def test_leaf_constructor_parity_holds_post_j3() -> None:
    """R3.2: the eval-driver shape and the runtime M0 shape resolve the SAME
    informational bindings across all four skills — the certificate the five
    pre-J3 green evals never actually held."""
    findings = diff_leaf_shapes(
        SKILLS, _eval_driver_leaf(), _runtime_m0_leaf(),
        label_a="eval_driver", label_b="runtime_m0",
    )
    assert findings == []


@pytest.mark.skipif(not _skills_present(), reason="real skills not present")
def test_parity_catches_an_ungrounded_shape() -> None:
    """Strip the M0 leaf's source_content (the pre-F1 world): parity must
    report the source bindings resolving under the eval shape only."""
    broken = _runtime_m0_leaf()
    del broken["source_content"]
    findings = diff_leaf_shapes(
        SKILLS, _eval_driver_leaf(), broken,
        label_a="eval_driver", label_b="runtime_m0",
    )
    assert any("source_excerpt" in f or "pages" in f for f in findings)
