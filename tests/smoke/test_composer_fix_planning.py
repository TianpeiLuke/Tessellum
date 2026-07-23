"""Composer v4, Phase 4 — fix stage (revert-to-BEST) + planner economics.

Covers:
  - fix.run_fix_loop: no-op when already passing; informed FixContext
    (issues + prior-attempt history); checkpoint-before-fix + revert-to
    -BEST (a regressing later fix never overwrites a better earlier note);
    early exit on clean pass; fixer=None / max_rounds=0 short-circuit;
    fixer crash is a dead round, not a raise.
  - planning.classify_planning_depth: fast vs full routing + conservative
    default-to-full.
  - planning.content_fingerprint / should_skip_unchanged: $0
    change-detection pre-gate.

All pure/local-I/O; no network, no LLM.
"""

from __future__ import annotations

from pathlib import Path

from tessellum.composer.fix import (
    AttemptOutcome,
    FixContext,
    run_fix_loop,
    score_issues,
)
from tessellum.composer.planning import (
    FAST_PATH_MAX_CHARS,
    LeafComplexity,
    classify_planning_depth,
    content_fingerprint,
    leaf_fingerprint,
    partition_unchanged_leaves,
    should_skip_unchanged,
)


# ── run_fix_loop ────────────────────────────────────────────────────────────


def _evaluator(sequence):
    """Return an evaluate() that yields (passed, cause, issues) from a list,
    clamping at the last entry."""
    calls = {"i": 0}

    def ev():
        idx = min(calls["i"], len(sequence) - 1)
        calls["i"] += 1
        return sequence[idx]

    return ev


def test_fix_loop_noop_when_already_passing(tmp_path: Path) -> None:
    p = tmp_path / "n.md"
    p.write_text("ok")
    fixer_calls = []
    res = run_fix_loop(
        note_path=p,
        evaluate=lambda: (True, None, []),
        fixer=lambda ctx: fixer_calls.append(ctx),
        max_rounds=3,
    )
    assert res.passed
    assert res.rounds_used == 0
    assert fixer_calls == []  # fixer never called


def test_fix_loop_no_fixer_is_terminal(tmp_path: Path) -> None:
    p = tmp_path / "n.md"
    p.write_text("bad")
    res = run_fix_loop(
        note_path=p,
        evaluate=lambda: (False, "format", [1, 2]),
        fixer=None,
        max_rounds=3,
    )
    assert not res.passed
    assert res.rounds_used == 0
    assert res.final_score == 2
    assert res.cause == "format"


def test_fix_loop_repairs_and_passes(tmp_path: Path) -> None:
    p = tmp_path / "n.md"
    p.write_text("bad")
    ev = _evaluator([(False, "grounding", [1]), (True, None, [])])

    def fixer(ctx: FixContext):
        p.write_text("fixed")

    res = run_fix_loop(note_path=p, evaluate=ev, fixer=fixer, max_rounds=3)
    assert res.passed
    assert res.rounds_used == 1
    assert p.read_text() == "fixed"


def test_fix_loop_informed_context_carries_history(tmp_path: Path) -> None:
    p = tmp_path / "n.md"
    p.write_text("bad")
    seen: list[FixContext] = []
    ev = _evaluator([
        (False, "g", [1, 2]),
        (False, "g", [1]),
        (False, "g", [1]),
    ])

    def fixer(ctx: FixContext):
        seen.append(ctx)

    run_fix_loop(note_path=p, evaluate=ev, fixer=fixer, max_rounds=2)
    # Round 1 sees no prior attempts; round 2 sees round 1's outcome.
    assert seen[0].prior_attempts == ()
    assert len(seen[1].prior_attempts) == 1
    assert isinstance(seen[1].prior_attempts[0], AttemptOutcome)
    assert seen[1].prior_attempts[0].round_n == 1


def test_fix_loop_reverts_to_best_on_regression(tmp_path: Path) -> None:
    p = tmp_path / "n.md"
    p.write_text("v0")  # start: 2 issues
    # after fix round1 → 1 issue (v1, the best); after round2 → 3 issues (v2, regressed)
    ev = _evaluator([
        (False, "g", [1, 2]),      # initial eval
        (False, "g", [1]),          # after round 1 (better)
        (False, "g", [1, 2, 3]),    # after round 2 (regressed)
    ])
    versions = ["v1", "v2"]

    def fixer(ctx: FixContext):
        p.write_text(versions[len(ctx.prior_attempts)])

    res = run_fix_loop(note_path=p, evaluate=ev, fixer=fixer, max_rounds=2)
    assert not res.passed
    assert res.final_score == 1  # best achieved
    assert res.reverted
    assert p.read_text() == "v1"  # the BEST version, not the regressed v2


def test_fix_loop_no_revert_when_last_is_best(tmp_path: Path) -> None:
    p = tmp_path / "n.md"
    p.write_text("v0")
    # monotonically improving but never clean: 3 → 2 → 1
    ev = _evaluator([
        (False, "g", [1, 2, 3]),
        (False, "g", [1, 2]),
        (False, "g", [1]),
    ])
    versions = ["v1", "v2"]

    def fixer(ctx: FixContext):
        p.write_text(versions[len(ctx.prior_attempts)])

    res = run_fix_loop(note_path=p, evaluate=ev, fixer=fixer, max_rounds=2)
    assert not res.passed
    assert res.final_score == 1
    assert not res.reverted  # last write WAS the best
    assert p.read_text() == "v2"


def test_fix_loop_fixer_crash_is_dead_round(tmp_path: Path) -> None:
    p = tmp_path / "n.md"
    p.write_text("bad")

    def boom(ctx: FixContext):
        raise RuntimeError("fixer exploded")

    res = run_fix_loop(
        note_path=p,
        evaluate=lambda: (False, "format", [1]),
        fixer=boom,
        max_rounds=3,
    )
    # A crashing fixer doesn't propagate; the loop ends blocked.
    assert not res.passed
    assert res.final_score == 1


def test_score_issues_counts_blocking() -> None:
    assert score_issues([]) == 0
    assert score_issues([1, 2, 3]) == 3


# ── classify_planning_depth ─────────────────────────────────────────────────


def test_depth_templated_small_is_fast() -> None:
    assert classify_planning_depth(
        LeafComplexity(source_chars=500, is_templated=True)
    ) == "fast"


def test_depth_multi_note_is_full() -> None:
    assert classify_planning_depth(
        LeafComplexity(source_chars=100, note_count=3, is_templated=True)
    ) == "full"


def test_depth_large_source_is_full() -> None:
    assert classify_planning_depth(
        LeafComplexity(source_chars=FAST_PATH_MAX_CHARS + 1, is_templated=True)
    ) == "full"


def test_depth_high_novelty_is_full() -> None:
    assert classify_planning_depth(
        LeafComplexity(source_chars=100, novelty=0.9)
    ) == "full"


def test_depth_low_novelty_is_fast() -> None:
    assert classify_planning_depth(
        LeafComplexity(source_chars=100, novelty=0.05)
    ) == "fast"


def test_depth_unknown_novelty_non_templated_defaults_full() -> None:
    # Conservative default: don't skip depth on an unknown leaf.
    assert classify_planning_depth(LeafComplexity(source_chars=100)) == "full"


# ── content_fingerprint / should_skip_unchanged ─────────────────────────────


def test_fingerprint_str_and_bytes_stable() -> None:
    assert content_fingerprint("hello") == content_fingerprint(b"hello")
    assert content_fingerprint("a") != content_fingerprint("b")


def test_fingerprint_path_hashes_bytes(tmp_path: Path) -> None:
    p = tmp_path / "s.txt"
    p.write_text("payload")
    assert content_fingerprint(p) == content_fingerprint("payload")


def test_fingerprint_absent_path() -> None:
    assert content_fingerprint(Path("/does/not/exist_xyz.txt")) == "absent"


def test_should_skip_unchanged_matches() -> None:
    fp = content_fingerprint("same")
    skip, fresh = should_skip_unchanged("l1", "same", {"l1": fp})
    assert skip
    assert fresh == fp


def test_should_skip_unchanged_changed_source() -> None:
    fp = content_fingerprint("old")
    skip, fresh = should_skip_unchanged("l1", "new", {"l1": fp})
    assert not skip
    assert fresh == content_fingerprint("new")


def test_should_skip_unchanged_unknown_leaf() -> None:
    skip, _ = should_skip_unchanged("l1", "x", {})
    assert not skip  # never seen → do the work


# ── leaf_fingerprint / partition_unchanged_leaves (the leaf-admission gate) ──


def test_leaf_fingerprint_excludes_positional_id() -> None:
    # The scheduler's positional _id must not perturb the fingerprint.
    assert leaf_fingerprint({"_id": "leaf_0", "body": "X"}) == leaf_fingerprint(
        {"_id": "leaf_9", "body": "X"}
    )


def test_leaf_fingerprint_reflects_content_change() -> None:
    assert leaf_fingerprint({"_id": "a", "body": "X"}) != leaf_fingerprint(
        {"_id": "a", "body": "Y"}
    )


def test_leaf_fingerprint_key_order_stable() -> None:
    assert leaf_fingerprint({"_id": "a", "x": 1, "y": 2}) == leaf_fingerprint(
        {"y": 2, "_id": "a", "x": 1}
    )


def test_leaf_fingerprint_source_key_isolates_field() -> None:
    a = leaf_fingerprint({"_id": "a", "src": "same", "noise": "1"}, source_key="src")
    b = leaf_fingerprint({"_id": "a", "src": "same", "noise": "2"}, source_key="src")
    assert a == b  # only `src` matters
    c = leaf_fingerprint({"_id": "a", "src": "diff"}, source_key="src")
    assert c != a


def test_partition_first_run_runs_all() -> None:
    leaves = [{"_id": "a", "body": "X"}, {"_id": "b", "body": "Y"}]
    to_run, skipped, fresh = partition_unchanged_leaves(leaves, {})
    assert len(to_run) == 2
    assert skipped == []
    assert set(fresh) == {"a", "b"}


def test_partition_skips_unchanged_runs_changed() -> None:
    leaves = [{"_id": "a", "body": "X"}, {"_id": "b", "body": "Y"}, {"_id": "c", "body": "Z"}]
    _, _, fresh = partition_unchanged_leaves(leaves, {})
    # b changes; a + c unchanged.
    leaves2 = [{"_id": "a", "body": "X"}, {"_id": "b", "body": "CHANGED"}, {"_id": "c", "body": "Z"}]
    to_run, skipped, fresh2 = partition_unchanged_leaves(leaves2, fresh)
    assert [x["_id"] for x in to_run] == ["b"]
    assert [x["_id"] for x in skipped] == ["a", "c"]
    # Fresh store refreshes b's fingerprint, keeps a/c.
    assert fresh2["b"] == leaf_fingerprint(leaves2[1])
    assert fresh2["a"] == fresh["a"]


def test_partition_all_unchanged_skips_all() -> None:
    leaves = [{"_id": "a", "body": "X"}, {"_id": "b", "body": "Y"}]
    _, _, fresh = partition_unchanged_leaves(leaves, {})
    to_run, skipped, _ = partition_unchanged_leaves(leaves, fresh)
    assert to_run == []
    assert len(skipped) == 2


def test_partition_unkeyed_leaf_always_runs() -> None:
    to_run, skipped, fresh = partition_unchanged_leaves(
        [{"body": "X"}], {"anything": "fp"}
    )
    assert len(to_run) == 1
    assert skipped == []
    assert fresh == {"anything": "fp"}  # no id → no fingerprint recorded


def test_partition_carries_forward_prior_entries() -> None:
    # A prior fingerprint for a leaf NOT in this run's set is preserved.
    fresh = partition_unchanged_leaves([{"_id": "a", "body": "X"}], {"old": "fp"})[2]
    assert fresh["old"] == "fp"
    assert "a" in fresh
