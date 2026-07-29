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
    preflight_execute_wave,
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

def test_projection_leaves_are_metadata_only_with_artifact_refs():
    """A3.1/A3.3 (FZ 20k9c1a1a1b7c2k1a): leaves carry NO inline source/plan
    bytes — the joined source becomes plan_doc["source_excerpt"] (paged ONCE by
    the artifact store; {{artifact.source_excerpt}} / {{artifact.plan_text}} in
    the execute skill) and each leaf carries their content DIGESTS
    (artifact_refs), so task identity binds the content by reference."""
    import hashlib

    from tessellum.composer.executor import _stringify

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
    # the joined source is now a plan_doc field the artifact store pages once
    assert "ALPHA" in plan["source_excerpt"] and "BETA" in plan["source_excerpt"]
    expected = {
        "plan_text": hashlib.sha256(_stringify("# THE PLAN").encode()).hexdigest(),
        "source_excerpt": hashlib.sha256(
            _stringify(plan["source_excerpt"]).encode()
        ).hexdigest(),
    }
    for leaf in leaves:
        assert "source_excerpt" not in leaf["note"]
        assert "plan_text" not in leaf["note"]
        assert leaf["artifact_refs"] == expected
        assert leaf["owned_sections_md"] == ""  # no coverage map in this plan
        assert leaf["source_ref"] == ["http://x/1", "http://x/2"]


def test_projection_single_doc_falls_back_to_source_content():
    """The member-less runtime M0 shape grounds writers from the top-level
    source_content (the latent empty-source gap A3.1 closes — before, the
    projection read ONLY members, so a single-doc job joined an empty source)."""
    plan = {
        "planned_notes": [{"filename": "a.md"}],
        "members": [],
        "source_content": "THE SINGLE DOC BODY",
        "source_name": "doc.md",
        "plan_text": "# P",
    }
    leaves = _project_planned_notes_to_leaves(plan)
    assert len(leaves) == 1
    assert "THE SINGLE DOC BODY" in plan["source_excerpt"]
    assert "source_excerpt" in leaves[0]["artifact_refs"]


def test_projection_owned_sections_join_coverage_map_with_ledger():
    """E2.3 (FZ 20k9c1a1a1b7c2k1a1b1): each leaf's owned_sections_md is the
    coverage-map rows THIS note owns joined with the measured pages ledger."""
    plan = {
        "planned_notes": [{"filename": "a.md"}, {"filename": "b.md"}],
        "members": [{"source_id": "p1", "excerpt": "X"}],
        "plan_text": "# P",
        "section_coverage_map": [
            {"maps_to_note": "a.md", "source_section": "Alpha Setup"},
            {"maps_to_note": "b.md", "source_section": "Beta Config"},
            {"maps_to_note": "a.md", "source_section": "Unmeasured Extra"},
        ],
        "pages": [
            {"page": "p1", "words": 500, "headings": ["Alpha Setup", "Beta Config"]},
        ],
    }
    leaves = _project_planned_notes_to_leaves(plan)
    a, b = leaves
    assert "Alpha Setup (source: p1, 500 measured words on page)" in a["owned_sections_md"]
    assert "Unmeasured Extra" in a["owned_sections_md"]  # row without ledger match kept
    assert "Beta Config" not in a["owned_sections_md"]   # other note's section excluded
    assert "Beta Config (source: p1, 500 measured words on page)" in b["owned_sections_md"]


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


# ── P13 (FZ 20k9c1a1a1b7c2e): preflight_execute_wave — static pre-dispatch ────


def _leaf(filename: str, note_dir: str = "resources/documentation") -> dict:
    """A well-formed projected note leaf (the shape _project_… produces)."""
    return {
        "note": {"filename": filename, "thesis": "t"},
        "target_path": f"{note_dir}/{filename}",
        "source_ref": [],
    }


def test_preflight_ok_when_declared_le_1():
    """A corpus-of-one / degenerate whole-plan fallback (declared <= 1) is
    legitimate — preflight short-circuits ok=True."""
    pf = preflight_execute_wave({"total_notes": 1}, [{"plan_text": "whole plan"}])
    assert pf.ok
    pf0 = preflight_execute_wave({}, [{"plan_text": "whole plan"}])
    assert pf0.ok


def test_preflight_fails_on_fan_out_collapse():
    """The E11 case: declares N>1 but collapsed to the single whole-plan leaf."""
    plan = {"total_notes": 3}  # no planned_notes, no note_intent_graph
    pf = preflight_execute_wave(plan, [{"plan_text": "whole plan"}])  # 1 leaf
    assert not pf.ok
    assert pf.declared == 3 and pf.leaf_count == 1
    assert any("whole-plan fallback" in i or "under-produce" in i for i in pf.issues)


def test_preflight_ok_on_matching_fan_out():
    """N well-formed planned notes → N leaves → coherent, ok=True."""
    plan = {"total_notes": 3, "planned_notes": [{"filename": f"n{i}.md"} for i in range(3)]}
    leaves = [_leaf(f"n{i}.md") for i in range(3)]
    pf = preflight_execute_wave(plan, leaves)
    assert pf.ok, pf.issues


def test_preflight_flags_dropped_planned_notes():
    """A planned_notes row lacking a usable filename would be silently dropped."""
    plan = {
        "total_notes": 2,
        "planned_notes": [{"filename": "a.md"}, {"description": "no filename"}],
    }
    # projection dropped the second → only 1 leaf
    pf = preflight_execute_wave(plan, [_leaf("a.md")])
    assert not pf.ok
    assert any("silently dropped" in i or "lack a usable filename" in i for i in pf.issues)


def test_preflight_flags_duplicate_target_paths():
    plan = {"total_notes": 2, "planned_notes": [{"filename": "dup.md"}, {"filename": "dup.md"}]}
    leaves = [_leaf("dup.md"), _leaf("dup.md")]
    pf = preflight_execute_wave(plan, leaves)
    assert not pf.ok
    assert any("duplicate" in i.lower() for i in pf.issues)


def test_preflight_flags_leaf_without_target_path():
    plan = {"total_notes": 2, "planned_notes": [{"filename": "a.md"}, {"filename": "b.md"}]}
    bad = {"note": {"filename": "b.md"}}  # a projected note leaf missing target_path
    pf = preflight_execute_wave(plan, [_leaf("a.md"), bad])
    assert not pf.ok
    assert any("target_path" in i for i in pf.issues)


def test_preflight_dangling_upstream_failsoft_without_compiled():
    """CHECK 4 is skipped (no error) when no compiled pipeline is threaded."""
    plan = {"total_notes": 2, "planned_notes": [{"filename": "a.md"}, {"filename": "b.md"}]}
    leaves = [_leaf("a.md"), _leaf("b.md")]
    pf = preflight_execute_wave(plan, leaves, compiled=None)
    assert pf.ok  # no dangling check without compiled, others pass


def test_owned_sections_filename_match_is_boundary_aware():
    """`tessellum_a.md` owns rows naming `a.md` (prefix convention), but
    `data.md` must NOT own `a.md`'s rows — bare endswith is the substring-
    renumbering corruption class."""
    plan = {
        "planned_notes": [{"filename": "data.md"}, {"filename": "tessellum_a.md"}],
        "members": [{"source_id": "p1", "excerpt": "X"}],
        "plan_text": "# P",
        "section_coverage_map": [
            {"maps_to_note": "a.md", "source_section": "Alpha"},
            {"maps_to_note": "data.md", "source_section": "Delta"},
        ],
        "pages": [],
    }
    data_leaf, prefixed_leaf = _project_planned_notes_to_leaves(plan)
    assert "Alpha" not in data_leaf["owned_sections_md"]      # no false suffix match
    assert "Delta" in data_leaf["owned_sections_md"]
    assert "Alpha" in prefixed_leaf["owned_sections_md"]      # prefix boundary matches
    assert "Delta" not in prefixed_leaf["owned_sections_md"]
