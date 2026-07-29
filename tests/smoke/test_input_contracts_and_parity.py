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


# ── R1.2: the acquisition-verb lint ──────────────────────────────────────────

from tessellum.composer.compiler import audit_acquisition_prose  # noqa: E402


@pytest.mark.skipif(not _skills_present(), reason="real skills not present")
@pytest.mark.parametrize("name", PHASE_SKILL_NAMES)
def test_shipped_skills_have_no_role_play_bait(name: str) -> None:
    """R1.2: every acquisition-verbed step renders a content-bearing binding —
    the F1/F2 substrate (read/fetch prose with nothing bound on a tool-free
    backend) is a lint failure now."""
    pipeline = compile_skill(SKILLS / f"{name}.md")
    assert audit_acquisition_prose(pipeline) == []


def test_acquisition_lint_flags_ungrounded_read_prose(tmp_path: Path) -> None:
    skill = tmp_path / "skill_bait.md"
    skill.write_text(
        "# Bait\n\n"
        "## Step <!-- :: section_id = s1 :: -->\n\n"
        "```yaml\n"
        "role: CORE\naggregation: corpus_wide\nbatchable: false\ndepends_on: []\n"
        "materializer: no_op\noutput_key: o\n"
        "```\n\n"
        "Read the source file end to end and measure it. Uses {{leaf.source_url}}.\n",
        encoding="utf-8",
    )
    findings = audit_acquisition_prose(compile_skill(skill))
    assert findings and "role-play bait" in findings[0]


# ── R1.3: dispatch-time required-input validation ────────────────────────────

def test_required_input_missing_refuses_dispatch(tmp_path: Path) -> None:
    from tessellum.composer import MockBackend
    from tessellum.composer.executor import execute_step

    skill = tmp_path / "skill_req.md"
    skill.write_text(
        "# Req\n\n"
        "## Step <!-- :: section_id = s1 :: -->\n\n"
        "```yaml\n"
        "role: CORE\naggregation: corpus_wide\nbatchable: false\ndepends_on: []\n"
        "materializer: no_op\noutput_key: o\n"
        "inputs:\n- name: leaf.pages\n  required: true\n"
        "```\n\n"
        "Ledger: {{leaf.pages}}\n",
        encoding="utf-8",
    )
    step = compile_skill(skill).steps[0]
    backend = MockBackend()
    result = execute_step(
        step, leaf={"_id": "x"}, upstream={}, backend=backend,
        vault_root=tmp_path, dry_run=False,
    )
    assert result.error_class == "validation"
    assert "required input leaf.pages" in (result.error or "")
    assert backend.calls == []  # refused BEFORE the backend call

    ok = execute_step(
        step, leaf={"_id": "x", "pages": [{"measured_words": 5}]},
        upstream={}, backend=backend, vault_root=tmp_path, dry_run=False,
    )
    assert ok.error is None


# ── R1.4: the feedback edge reaches the writer (contract-level pin) ──────────

@pytest.mark.skipif(not _skills_present(), reason="real skills not present")
def test_feedback_edge_declared_at_the_effector_step() -> None:
    """R1.4: `leaf.review_failures` is a DECLARED input of BOTH the revise
    round's reader (read_draft) and the step that rewrites the artifact under
    review (write_augmented_plan) — the F4 schema bottleneck cannot silently
    reopen while this pin holds."""
    pipeline = compile_skill(SKILLS / "skill_tessellum_augment_digestion_plan.md")
    by_id = {s.section_id: dict(s.declared_inputs) for s in pipeline.steps}
    assert "leaf.review_failures" in by_id["read_draft"]
    assert "leaf.review_failures" in by_id["write_augmented_plan"]
    # and the effector also receives the artifact under revision + the ledger
    assert "artifact.plan_text" in by_id["write_augmented_plan"]
    assert "artifact.pages" in by_id["write_augmented_plan"]
