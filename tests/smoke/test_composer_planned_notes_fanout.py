"""P2.1 (FZ 20k9c1a1a1b7c2b / hardening roadmap) — fan-out projection edge cases.

Guards the pure, fail-soft contract of the native execute-wave fan-out:
``_project_planned_notes_to_leaves`` (LLM-plan → one writer leaf per note) and
``_declared_note_count`` (the single source of truth the under-production
backstop keys on). These are the driver-level fix for E11 (an N-note plan
silently producing ~1 note); this file pins their behaviour on the edge shapes
the roadmap enumerated so a refactor can't silently reopen the fallback.

Pure-function tests — no LLM, no filesystem, no backend. Safe to run alongside a
live digestion run (never touches the runtime import path at call time).
"""

from __future__ import annotations

from tessellum.composer.digestion import (
    _declared_note_count,
    _normalize_plan_doc_keys,
    _project_planned_notes_to_leaves,
)


# ── _project_planned_notes_to_leaves — fail-soft on degenerate planned_notes ──

def test_projection_empty_list_yields_no_leaves():
    """An empty ``planned_notes`` → ``[]`` so the caller falls through to the
    whole-plan fallback leaf (fail-soft, not a crash)."""
    assert _project_planned_notes_to_leaves({"planned_notes": []}) == []


def test_projection_missing_key_yields_no_leaves():
    """No ``planned_notes`` key at all → ``[]`` (the typed-graph or whole-plan
    fallback handles it)."""
    assert _project_planned_notes_to_leaves({}) == []


def test_projection_non_list_yields_no_leaves():
    """A non-list ``planned_notes`` (malformed plan) → ``[]``, never raises."""
    for bad in ("not-a-list", {"filename": "x.md"}, 7, None):
        assert _project_planned_notes_to_leaves({"planned_notes": bad}) == []


def test_projection_skips_entries_without_filename():
    """Entries lacking a usable ``filename``/``note`` are skipped; only the
    usable ones become leaves (partial-plan robustness)."""
    plan = {
        "planned_notes": [
            {"description": "no filename here"},          # skipped
            {"filename": "", "building_block": "concept"},  # empty → skipped
            {"filename": "cc_real.md", "building_block": "concept"},  # kept
            "not-a-dict",                                   # skipped
        ]
    }
    leaves = _project_planned_notes_to_leaves(plan)
    assert len(leaves) == 1
    assert leaves[0]["note"]["filename"] == "cc_real.md"


# ── target_path / filename derivation ────────────────────────────────────────

def test_projection_appends_md_and_prefix_and_builds_target_path():
    """A bare filename gets ``.md`` + the plan's ``file_prefix``, and
    ``target_path`` = ``<note_dir>/<prefixed-name>`` (what the type-contract
    resolver keys on)."""
    plan = {
        "planned_notes": [{"filename": "mcp_overview", "building_block": "concept"}],
        "note_dir": "resources/documentation/claude_code",
        "file_prefix": "cc_",
    }
    leaf = _project_planned_notes_to_leaves(plan)[0]
    assert leaf["note"]["filename"] == "cc_mcp_overview.md"
    assert leaf["target_path"] == "resources/documentation/claude_code/cc_mcp_overview.md"


def test_projection_does_not_double_apply_prefix():
    """A filename already carrying the prefix is not double-prefixed."""
    plan = {
        "planned_notes": [{"filename": "cc_mcp_overview.md"}],
        "note_dir": "resources/documentation/claude_code",
        "file_prefix": "cc_",
    }
    leaf = _project_planned_notes_to_leaves(plan)[0]
    assert leaf["note"]["filename"] == "cc_mcp_overview.md"
    assert leaf["target_path"].endswith("/cc_mcp_overview.md")
    assert "cc_cc_" not in leaf["target_path"]


def test_projection_defaults_note_dir_when_routing_absent():
    """With no routing/note_dir, target_path is still vault-relative under the
    generic default dir (never an absolute or empty path)."""
    plan = {"planned_notes": [{"filename": "x.md"}]}
    leaf = _project_planned_notes_to_leaves(plan)[0]
    assert leaf["target_path"] == "resources/documentation/x.md"


def test_projection_reads_note_dir_from_routing_decision():
    """``routing_decision.target_directory`` supplies the note dir when the
    top-level keys are absent."""
    plan = {
        "planned_notes": [{"filename": "x.md"}],
        "routing_decision": {"target_directory": "areas/models", "file_prefix": "model_"},
    }
    leaf = _project_planned_notes_to_leaves(plan)[0]
    assert leaf["target_path"] == "areas/models/model_x.md"


# ── source content threading (single-shot backend has no file tool) ──────────

def test_projection_inlines_member_excerpts_into_every_leaf():
    """Each leaf carries the admitted members' excerpts inline (the composer
    backend is single-shot with no file-reading tool) + the plan_text."""
    plan = {
        "planned_notes": [{"filename": "a.md"}, {"filename": "b.md"}],
        "members": [
            {"source_id": "p1", "excerpt": "ALPHA", "source_url": "http://x/1"},
            {"source_id": "p2", "excerpt": "BETA", "source_url": "http://x/2"},
        ],
        "plan_text": "# THE PLAN",
    }
    leaves = _project_planned_notes_to_leaves(plan)
    assert len(leaves) == 2
    for leaf in leaves:
        assert "ALPHA" in leaf["note"]["source_excerpt"]
        assert "BETA" in leaf["note"]["source_excerpt"]
        assert leaf["note"]["plan_text"] == "# THE PLAN"
        assert leaf["source_ref"] == ["http://x/1", "http://x/2"]


def test_projection_one_leaf_per_note_matches_count():
    """N well-formed planned notes → exactly N leaves (the anti-under-production
    invariant the fan-out exists to guarantee)."""
    plan = {"planned_notes": [{"filename": f"n{i}.md"} for i in range(8)]}
    assert len(_project_planned_notes_to_leaves(plan)) == 8


# ── _declared_note_count — single source of truth for the backstop ───────────

def test_declared_count_prefers_total_notes():
    assert _declared_note_count({"total_notes": 8, "planned_notes": [{}, {}]}) == 8


def test_declared_count_falls_back_to_planned_notes_len():
    assert _declared_note_count({"planned_notes": [{}, {}, {}]}) == 3


def test_declared_count_zero_when_absent_or_unusable():
    """No count anywhere → 0 (nothing to compare → the backstop stays quiet)."""
    assert _declared_note_count({}) == 0
    assert _declared_note_count({"total_notes": 0}) == 0
    assert _declared_note_count({"total_notes": "two"}) == 0
    assert _declared_note_count({"planned_notes": "nope"}) == 0


def test_declared_count_ignores_nonpositive_total_and_uses_planned():
    """A non-positive ``total_notes`` is not authoritative; fall back to the
    planned-notes length rather than trusting a 0/negative scalar."""
    assert _declared_note_count({"total_notes": 0, "planned_notes": [{}, {}]}) == 2


# ── P21 core (FZ 20k9c1a1a1b7c2h): plan-of-record guard covers total_notes ────

def test_normalize_restores_total_notes_shrunk_below_planned():
    """P21 core: a re-emission (e.g. review step_1) that shrinks `total_notes`
    below the enumerated `planned_notes` count is corrected — you cannot declare
    fewer notes than you enumerated. Previously only `plan_text` was protected;
    `total_notes` had no clobber guard."""
    plan = {"planned_notes": [{"filename": f"n{i}.md"} for i in range(5)],
            "total_notes": 2}  # a lossy re-emission shrank the count
    _normalize_plan_doc_keys(plan)
    assert plan["total_notes"] == 5, "total_notes restored to the enumerated floor"


def test_normalize_keeps_total_notes_above_planned():
    """A legitimately-larger total_notes (planned enumerates a subset — e.g. a
    master plan) is NOT shrunk to the enumerated count."""
    plan = {"planned_notes": [{"filename": "a.md"}, {"filename": "b.md"}],
            "total_notes": 29}  # run-9 shape: total > enumerated
    _normalize_plan_doc_keys(plan)
    assert plan["total_notes"] == 29, "a larger declared total is preserved"


def test_normalize_sets_total_notes_when_missing():
    """No `total_notes` at all → set to the enumerated floor (not left absent,
    which PLAN-003 would read as 0)."""
    plan = {"planned_notes": [{"filename": "a.md"}, {"filename": "b.md"}, {"filename": "c.md"}]}
    _normalize_plan_doc_keys(plan)
    assert plan["total_notes"] == 3
