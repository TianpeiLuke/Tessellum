"""Smoke tests for BB_SCHEMA_AT_VERSION + version-aware TESS-005 (Phase I.2).

Covers:

- BB_SCHEMA_AT_VERSION(1) returns the empty-event-log schema.
- BB_SCHEMA_AT_VERSION(N) reconstructs schema after N-1 events.
- TESS-005 reads note's bb_schema_version and validates against that
  version's schema.
- Missing bb_schema_version falls back to live BB_SCHEMA (back-compat).
- Non-integer bb_schema_version falls back to live BB_SCHEMA.
- Issue message names the version (`@v3` / `@live`).
- Cache invalidates on set_user_extensions_from_events.
"""

from __future__ import annotations

import pytest

from tessellum.bb.types import (
    BB_SCHEMA,
    BB_SCHEMA_AT_VERSION,
    BB_SCHEMA_EPISTEMIC,
    BB_SCHEMA_USER_EXTENSIONS,
    BB_SCHEMA_VERSION,
    BBType,
    EpistemicEdgeType,
    SchemaEditEvent,
    set_user_extensions_from_events,
)


# ── BB_SCHEMA_AT_VERSION basics ────────────────────────────────────────────


def test_schema_at_version_1_equals_no_user_extensions_schema():
    """Version 1 = before any user extensions. Includes core + DKS extensions only."""
    set_user_extensions_from_events([])
    schema_v1 = BB_SCHEMA_AT_VERSION(1)
    # Should match the static module-level BB_SCHEMA at the empty
    # event-log state.
    assert set(schema_v1) == set(BB_SCHEMA)


def test_schema_at_version_zero_or_negative_raises():
    with pytest.raises(ValueError, match="version must be >= 1"):
        BB_SCHEMA_AT_VERSION(0)
    with pytest.raises(ValueError):
        BB_SCHEMA_AT_VERSION(-1)


def test_schema_at_version_reflects_event_log_prefix():
    """After 2 added events, version 2 reflects 1 event, version 3 reflects both."""
    set_user_extensions_from_events([])
    edge_a = EpistemicEdgeType(BBType.MODEL, BBType.PROCEDURE, "test_edge_a")
    edge_b = EpistemicEdgeType(
        BBType.COUNTER_ARGUMENT, BBType.EMPIRICAL_OBSERVATION, "test_edge_b"
    )
    events = [
        SchemaEditEvent(
            timestamp="2026-05-11T00:00:00+00:00",
            kind="added",
            edge=edge_a,
            motivating_failure="test",
        ),
        SchemaEditEvent(
            timestamp="2026-05-11T01:00:00+00:00",
            kind="added",
            edge=edge_b,
            motivating_failure="test",
        ),
    ]
    set_user_extensions_from_events(events)
    # Version 1: no extensions
    schema_v1 = BB_SCHEMA_AT_VERSION(1)
    assert edge_a not in schema_v1
    assert edge_b not in schema_v1
    # Version 2: first added event applied
    schema_v2 = BB_SCHEMA_AT_VERSION(2)
    assert edge_a in schema_v2
    assert edge_b not in schema_v2
    # Version 3: both events applied
    schema_v3 = BB_SCHEMA_AT_VERSION(3)
    assert edge_a in schema_v3
    assert edge_b in schema_v3
    # Cleanup
    set_user_extensions_from_events([])


def test_schema_at_version_caches_per_event_log():
    """Repeated calls at the same version return the same tuple (cache hit)."""
    set_user_extensions_from_events([])
    s1 = BB_SCHEMA_AT_VERSION(1)
    s2 = BB_SCHEMA_AT_VERSION(1)
    assert s1 is s2  # identity, not just equality


def test_schema_at_version_cache_invalidates_on_event_log_change():
    """Replacing the event log invalidates the cache."""
    set_user_extensions_from_events([])
    s_before = BB_SCHEMA_AT_VERSION(1)
    edge_x = EpistemicEdgeType(BBType.MODEL, BBType.CONCEPT, "cache_invalidation_test")
    set_user_extensions_from_events(
        [
            SchemaEditEvent(
                timestamp="2026-05-11T00:00:00+00:00",
                kind="added",
                edge=edge_x,
                motivating_failure="test",
            )
        ]
    )
    s_after_v1 = BB_SCHEMA_AT_VERSION(1)
    # v1 should still NOT contain the new edge — only v2 does
    assert edge_x not in s_after_v1
    # But the cached tuple identity may differ since the event log
    # changed (we don't promise identity across event-log changes).
    s_after_v2 = BB_SCHEMA_AT_VERSION(2)
    assert edge_x in s_after_v2
    set_user_extensions_from_events([])  # cleanup


def test_schema_at_version_retract_event_removes_edge():
    set_user_extensions_from_events([])
    edge_y = EpistemicEdgeType(BBType.MODEL, BBType.CONCEPT, "retract_target")
    events = [
        SchemaEditEvent(
            timestamp="2026-05-11T00:00:00+00:00",
            kind="added",
            edge=edge_y,
            motivating_failure="test",
        ),
        SchemaEditEvent(
            timestamp="2026-05-11T01:00:00+00:00",
            kind="retracted",
            edge=edge_y,
            motivating_failure="test",
        ),
    ]
    set_user_extensions_from_events(events)
    assert edge_y in BB_SCHEMA_AT_VERSION(2)  # after add only
    assert edge_y not in BB_SCHEMA_AT_VERSION(3)  # after retract
    set_user_extensions_from_events([])


# ── Version-aware TESS-005 ────────────────────────────────────────────────


def _write_arg_note(
    path,
    body: str,
    *,
    bb_type: str = "argument",
    version: int | str | None = 1,
    status: str = "active",
):
    version_line = f"bb_schema_version: {version}\n" if version is not None else ""
    path.write_text(
        f"""---
tags:
  - resource
  - analysis
  - {bb_type}
keywords:
  - test
topics:
  - Testing
language: markdown
date of note: 2026-05-11
status: {status}
building_block: {bb_type}
{version_line}---

{body}
""",
        encoding="utf-8",
    )
    return path


def test_tess005_validates_against_recorded_version_with_active_schema(tmp_path):
    """A note recorded at version=2 with a fresh extension at v=2 should pass."""
    set_user_extensions_from_events([])
    # Define a schema extension: counter_argument → empirical_observation
    edge = EpistemicEdgeType(
        BBType.COUNTER_ARGUMENT, BBType.EMPIRICAL_OBSERVATION, "test_anchor"
    )
    set_user_extensions_from_events(
        [
            SchemaEditEvent(
                timestamp="2026-05-11T00:00:00+00:00",
                kind="added",
                edge=edge,
                motivating_failure="test",
            )
        ]
    )
    # Author a counter_argument note that links to an empirical_observation
    obs_path = tmp_path / "obs.md"
    _write_arg_note(obs_path, body="obs", bb_type="empirical_observation", version=2)
    ctr_path = tmp_path / "ctr.md"
    _write_arg_note(
        ctr_path,
        body="see [the observation](obs.md)",
        bb_type="counter_argument",
        version=2,
    )
    from tessellum.format import validate

    issues = validate(ctr_path)
    tess005 = [i for i in issues if i.rule_id == "TESS-005"]
    # CTR→OBS is in the v2 schema (we just added it) → no warning
    assert tess005 == []
    set_user_extensions_from_events([])


def test_tess005_warns_against_recorded_version_message_names_version(tmp_path):
    """A note recorded at version=1 linking via a v2-only edge gets a TESS-005 warning
    naming the version."""
    set_user_extensions_from_events([])
    # No extensions — so any non-core BB-pair link should warn.
    # ARG -> ARG is not in BB_SCHEMA (same-BB is skipped anyway).
    # Try ARG -> PROCEDURE which is not a declared epistemic edge.
    obs_path = tmp_path / "proc.md"
    _write_arg_note(obs_path, body="proc body", bb_type="procedure", version=1)
    arg_path = tmp_path / "arg.md"
    _write_arg_note(
        arg_path,
        body="see [the procedure](proc.md)",
        bb_type="argument",
        version=1,
    )
    from tessellum.format import validate

    issues = validate(arg_path)
    tess005 = [i for i in issues if i.rule_id == "TESS-005"]
    # ARG→PROC: not in BB_SCHEMA → expect a warning
    assert len(tess005) == 1
    # Message should name the version
    assert "@v1" in tess005[0].message


def test_tess005_missing_version_falls_back_to_live_schema(tmp_path):
    """A v0.0.52-era note (no bb_schema_version field) validates against live BB_SCHEMA."""
    set_user_extensions_from_events([])
    proc_path = tmp_path / "proc.md"
    _write_arg_note(proc_path, body="proc", bb_type="procedure", version=None)
    arg_path = tmp_path / "arg.md"
    _write_arg_note(
        arg_path,
        body="see [the procedure](proc.md)",
        bb_type="argument",
        version=None,
    )
    from tessellum.format import validate

    issues = validate(arg_path)
    tess005 = [i for i in issues if i.rule_id == "TESS-005"]
    assert len(tess005) == 1
    assert "@live" in tess005[0].message


def test_tess005_non_integer_version_falls_back_to_live(tmp_path):
    set_user_extensions_from_events([])
    proc_path = tmp_path / "proc.md"
    _write_arg_note(proc_path, body="proc", bb_type="procedure", version="abc")
    arg_path = tmp_path / "arg.md"
    _write_arg_note(
        arg_path,
        body="see [the procedure](proc.md)",
        bb_type="argument",
        version="abc",
    )
    from tessellum.format import validate

    issues = validate(arg_path)
    tess005 = [i for i in issues if i.rule_id == "TESS-005"]
    assert len(tess005) == 1
    assert "@live" in tess005[0].message
