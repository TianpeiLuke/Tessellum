"""M0 smoke — bundle → joint-planner fan-in (build_corpus_leaf + delivery).

Multi-document corpus digestion (FZ 20k9c1a1a1b7b1). Proves the fan-in the
shipped single-doc path lacks: a multi-member SourceBundle becomes ONE planning
leaf whose ``{{leaf.members}}`` reaches the planner prompt with every member's
identity + bounded excerpt — not N independent one-at-a-time jobs.

Covers:
  - build_corpus_leaf: shape, even per-member budget, HEAD/TAIL windowing,
    fail-loud on a member missing content, ascending-ordinal member order.
  - delivery: feeding the corpus leaf into run_digestion_pipeline renders every
    member's ref into the plan-phase prompt (asserted via MockBackend.calls),
    and the single-doc path is unaffected.
"""

from __future__ import annotations

import json
from pathlib import Path

from tessellum.composer import (
    DEFAULT_CORPUS_LEAF_MAX_CHARS,
    MockBackend,
    build_corpus_leaf,
    compile_skill,
    run_digestion_pipeline,
    run_pipeline,
    run_pipeline_dynamic,
)
from tessellum.composer.knowledge_plan import BundleMember, SourceBundle

_SHIPPED_PLAN_SKILL = (
    Path(__file__).resolve().parents[2]
    / "vault/resources/skills/skill_tessellum_plan_digestion.md"
)


def _bundle(n: int) -> SourceBundle:
    return SourceBundle(
        bundle_id="bundle-xyz",
        objective="digest the whole corpus jointly",
        members=tuple(
            BundleMember(
                source_id=f"job{i}", ordinal=i, ref=f"/inbox/doc_{i}.md",
                parser_id="md", extracted_text_hash=f"hash{i}",
            )
            for i in range(n)
        ),
    )


# ── build_corpus_leaf ───────────────────────────────────────────────────────


def test_leaf_carries_every_member_in_order() -> None:
    b = _bundle(3)
    leaf = build_corpus_leaf(b, {0: "a", 1: "b", 2: "c"})
    assert leaf["member_count"] == 3
    assert [m["ordinal"] for m in leaf["members"]] == [0, 1, 2]
    assert [m["ref"] for m in leaf["members"]] == [
        "/inbox/doc_0.md", "/inbox/doc_1.md", "/inbox/doc_2.md",
    ]
    assert leaf["bundle_id"] == "bundle-xyz"
    assert leaf["_id"] == "bundle-xyz"


def test_leaf_budget_split_evenly_stays_bounded() -> None:
    from tessellum.composer.corpus_plan import _render_members

    b = _bundle(4)
    big = {i: "X" * 100_000 for i in range(4)}
    max_chars = 40_000
    leaf = build_corpus_leaf(b, big, max_chars=max_chars)
    # The RENDERED members block (what {{leaf.members}} substitutes) stays under
    # the budget — the invariant that actually protects the hard prompt cap.
    assert len(_render_members(leaf["members"])) <= max_chars
    assert all(m["truncated"] for m in leaf["members"])


def test_leaf_windowing_keeps_head_and_tail() -> None:
    b = _bundle(1)
    content = "HEAD" + "m" * 100_000 + "TAIL"
    leaf = build_corpus_leaf(b, {0: content}, max_chars=5_000)
    exc = leaf["members"][0]["excerpt"]
    assert exc.startswith("HEAD")
    assert exc.endswith("TAIL")
    assert "[… excerpt elided …]" in exc
    assert leaf["members"][0]["full_char_count"] == len(content)


def test_leaf_no_truncation_when_small() -> None:
    b = _bundle(2)
    leaf = build_corpus_leaf(b, {0: "short", 1: "also short"})
    assert not any(m["truncated"] for m in leaf["members"])
    assert leaf["members"][0]["excerpt"] == "short"


def test_leaf_fails_loud_on_missing_member_content() -> None:
    b = _bundle(3)
    try:
        build_corpus_leaf(b, {0: "a", 2: "c"})  # ordinal 1 missing
        raise AssertionError("expected ValueError for missing member content")
    except ValueError as exc:
        assert "missing content" in str(exc)
        assert "1" in str(exc)


def test_leaf_ignores_extra_content() -> None:
    b = _bundle(1)
    leaf = build_corpus_leaf(b, {0: "a", 99: "ignored"})
    assert leaf["member_count"] == 1


def test_default_budget_under_hard_cap() -> None:
    # sanity: the default aggregate budget leaves headroom under the 150k cap.
    assert DEFAULT_CORPUS_LEAF_MAX_CHARS < 150_000


# ── delivery: members reach the planner prompt ──────────────────────────────


def _write_corpus_plan_skill(skills_dir: Path) -> None:
    """A synthetic plan skill whose step-1 prompt references {{leaf.members}},
    so the rendered prompt (captured by MockBackend) proves delivery."""
    def _skill(name: str, *, output_key: str, required: list[str],
               materializer: str = "no_op", aggregation: str = "corpus_wide",
               prompt: str = "phase") -> None:
        req = ", ".join(required)
        (skills_dir / f"{name}.md").write_text(
            "---\n"
            "tags:\n  - resource\n  - skill\n"
            "keywords:\n  - alpha\n  - beta\n  - gamma\n"
            "topics:\n  - Digestion\n"
            "language: markdown\ndate of note: 2026-07-25\nstatus: active\n"
            "building_block: procedure\naccess_control_group: [\"general\"]\n---\n\n"
            f"# {name}\n\n"
            "## Do it <!-- :: section_id = step_1 :: -->\n\n"
            "```yaml\n"
            "role: CORE\n"
            f"aggregation: {aggregation}\n"
            "batchable: false\ndepends_on: []\n"
            f"materializer: {materializer}\n"
            f"output_key: {output_key}\n"
            "expected_output_schema:\n  type: object\n"
            f"  required: [{req}]\n"
            "```\n\n"
            f"{prompt}\n",
            encoding="utf-8",
        )

    _skill("skill_tessellum_plan_digestion", output_key="plan_out",
           required=["plan_path"],
           prompt="Plan this corpus (count {{leaf.member_count}}):\n{{leaf.members}}")
    _skill("skill_tessellum_augment_digestion_plan", output_key="augment_out",
           required=["plan_text"])
    _skill("skill_tessellum_review_digestion_plan", output_key="verdict",
           required=["ready"])
    _skill("skill_tessellum_execute_digestion_plan", output_key="exec_out",
           required=["output_path", "body_markdown"],
           materializer="body_markdown_to_file", aggregation="per_leaf")


def _mock() -> MockBackend:
    return MockBackend(default=json.dumps({
        "plan_path": "plans/plan_corpus.md",
        "plan_text": "# Plan",
        "ready": True, "failures": [],
        "output_path": "notes/n.md", "body_markdown": "# Note\n\nbody",
        "total_notes": 2,
    }))


def test_corpus_leaf_delivers_all_members_to_planner_prompt(tmp_path: Path) -> None:
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_corpus_plan_skill(sd)
    backend = _mock()
    b = _bundle(3)
    leaf = build_corpus_leaf(b, {0: "alpha doc", 1: "beta doc", 2: "gamma doc"})
    run_digestion_pipeline(
        skills_dir=sd, source_leaf=leaf, backend=backend,
        vault_root=tmp_path / "vault",
    )
    # The FIRST call is the plan phase; its rendered prompt must carry every
    # member's ref + its excerpt (delivery proof, not just leaf construction).
    plan_prompt = backend.calls[0].user_prompt
    for ref in ("/inbox/doc_0.md", "/inbox/doc_1.md", "/inbox/doc_2.md"):
        assert ref in plan_prompt, f"member {ref} not delivered to planner prompt"
    for excerpt in ("alpha doc", "beta doc", "gamma doc"):
        assert excerpt in plan_prompt


def test_single_doc_leaf_renders_no_missing_sentinel(tmp_path: Path) -> None:
    # Regression: adding {{leaf.member_count}}/{{leaf.members}} to the shipped
    # plan skill must NOT pollute the single-doc plan prompt with <missing …>
    # sentinels. A single-source leaf carries member_count:1 + members:[] so
    # both placeholders resolve cleanly.
    sd = tmp_path / "skills"
    sd.mkdir()
    _write_corpus_plan_skill(sd)
    backend = _mock()
    single_leaf = {
        "_id": "job-single",
        "source_url": "file:///inbox/one.md",
        "source_name": "one.md",
        "source_content": "the single source",
        "member_count": 1,
        "members": [],
    }
    run_digestion_pipeline(
        skills_dir=sd, source_leaf=single_leaf, backend=backend,
        vault_root=tmp_path / "vault",
    )
    plan_prompt = backend.calls[0].user_prompt
    assert "<missing leaf.members>" not in plan_prompt
    assert "<missing leaf.member_count>" not in plan_prompt


def test_shipped_plan_skill_references_member_placeholders() -> None:
    # Bind the SHIPPED vault skill to the delivery contract: if someone drops or
    # renames the CORPUS MEMBERS block, member delivery silently breaks in
    # production while the synthetic-stub tests stay green. This fails loud.
    text = _SHIPPED_PLAN_SKILL.read_text(encoding="utf-8")
    assert "{{leaf.member_count}}" in text
    assert "{{leaf.members}}" in text


def test_rendered_members_block_bounded_at_high_member_count() -> None:
    # The high-severity review finding: budget the RENDERED JSON, not just the
    # excerpt bodies. Even with many members (each carrying ~275 chars of fixed
    # JSON scaffolding), the rendered members block must stay <= max_chars.
    from tessellum.composer.corpus_plan import _render_members

    n = 25
    b = _bundle(n)
    contents = {i: "Z" * 100_000 for i in range(n)}
    max_chars = 60_000
    leaf = build_corpus_leaf(b, contents, max_chars=max_chars)
    rendered = _render_members(leaf["members"])
    assert len(rendered) <= max_chars, (
        f"rendered members block {len(rendered)} exceeds max_chars {max_chars}"
    )


def test_more_members_than_budget_fails_loud_not_overcap() -> None:
    # Degenerate case (member_count > max_chars): the scaffolding alone can't
    # fit, so the builder must RAISE rather than emit an over-cap leaf that
    # trips the hard prompt cap downstream.
    b = _bundle(50)
    contents = {i: "x" for i in range(50)}
    try:
        build_corpus_leaf(b, contents, max_chars=100)  # 100 < 50 members' scaffolding
        raise AssertionError("expected ValueError for over-budget scaffolding")
    except ValueError as exc:
        assert "exceeds max_chars" in str(exc)


# ── scheduler parity: corpus_wide {{leaf.X}} resolves in BOTH schedulers ─────


def _corpus_wide_leaf_skill(tmp_path: Path):
    """A 1-step corpus_wide skill whose prompt reads a SHARED leaf key, compiled.

    The M0 scheduler review (critical) found the _corpus_leaf fix reached serial
    run_pipeline but NOT run_pipeline_dynamic, so a corpus_wide {{leaf.X}} was
    starved (<missing leaf.X>) in the dynamic/execute-wave path only. The
    existing dynamic-parity gate (_sig) never compares the rendered prompt, so
    the divergence was invisible. This binds both schedulers to the fix.
    """
    sk = tmp_path / "skill_cw.md"
    sk.write_text(
        "---\ntags:\n  - resource\n  - skill\n"
        "keywords:\n  - a\n  - b\n  - c\ntopics:\n  - X\n"
        "language: markdown\ndate of note: 2026-07-25\nstatus: active\n"
        "building_block: procedure\naccess_control_group: [\"general\"]\n---\n\n"
        "# skill_cw\n\n## Do it <!-- :: section_id = step_1 :: -->\n\n"
        "```yaml\nrole: CORE\naggregation: corpus_wide\nbatchable: false\n"
        "depends_on: []\nmaterializer: no_op\noutput_key: out\n"
        "expected_output_schema:\n  type: object\n  required: [ok]\n```\n\n"
        "CONSUME src={{leaf.src}}\n",
        encoding="utf-8",
    )
    return compile_skill(sk)


def test_corpus_wide_leaf_placeholder_parity_serial_vs_dynamic(tmp_path: Path) -> None:
    compiled = _corpus_wide_leaf_skill(tmp_path)
    # `src` is IDENTICAL across leaves → a shared key _corpus_leaf must expose.
    leaves = [{"id": "a", "src": "http://shared"}, {"id": "b", "src": "http://shared"}]
    sb = MockBackend(default='{"ok": true}')
    run_pipeline(compiled, leaves=[dict(x) for x in leaves], backend=sb,
                 vault_root=tmp_path / "vs")
    db = MockBackend(default='{"ok": true}')
    run_pipeline_dynamic(compiled, leaves=[dict(x) for x in leaves], backend=db,
                         vault_root=tmp_path / "vd", max_workers=4)
    serial = next(c.user_prompt for c in sb.calls if "CONSUME" in c.user_prompt)
    dynamic = next(c.user_prompt for c in db.calls if "CONSUME" in c.user_prompt)
    assert serial == dynamic, f"scheduler parity broken:\n serial={serial!r}\n dynamic={dynamic!r}"
    assert "<missing" not in dynamic
    assert "http://shared" in dynamic
