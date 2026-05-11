"""Smoke tests for tessellum.dks.persistence (Phase 5, v0.0.45).

WarrantRegistry + WarrantHistory + load_warrants_from_vault.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from tessellum.dks import (
    DKSWarrant,
    HistoryEntry,
    WarrantChange,
    WarrantHistory,
    WarrantRegistry,
    load_warrants_from_vault,
)


# ── WarrantRegistry ─────────────────────────────────────────────────────────


def _w(claim: str = "c") -> DKSWarrant:
    return DKSWarrant(claim=claim, data="D", warrant="W")


def test_empty_registry():
    reg = WarrantRegistry()
    assert len(reg) == 0
    assert reg.snapshot() == ()
    assert "anything" not in reg


def test_registry_add_and_snapshot():
    reg = WarrantRegistry()
    reg.add("1a", _w("first"))
    reg.add("2a", _w("second"))
    assert len(reg) == 2
    assert "1a" in reg
    assert "2a" in reg
    assert "3a" not in reg
    snap = reg.snapshot()
    assert len(snap) == 2
    assert snap[0].claim == "first"
    assert snap[1].claim == "second"


def test_registry_add_duplicate_raises():
    reg = WarrantRegistry()
    reg.add("1a", _w())
    with pytest.raises(ValueError, match="already registered"):
        reg.add("1a", _w())


def test_registry_supersede_replaces_entry():
    reg = WarrantRegistry()
    reg.add("1a", _w("old"))
    reg.add("2a", _w("other"))
    reg.supersede("1a", "1b", _w("new"))

    assert "1a" not in reg
    assert "1b" in reg
    assert "2a" in reg
    snap = reg.snapshot_with_fz()
    fzs = [fz for fz, _ in snap]
    assert "1b" in fzs
    assert "1a" not in fzs


def test_registry_supersede_old_fz_unknown_still_adds_new():
    """Tolerant: supersede an FZ the registry never saw — new entry lands."""
    reg = WarrantRegistry()
    reg.supersede("old_fz_not_in_set", "1a", _w("new"))
    assert "1a" in reg
    assert len(reg) == 1


def test_registry_constructor_accepts_initial_pairs():
    reg = WarrantRegistry(
        warrants=[("1a", _w("a")), ("2a", _w("b"))]
    )
    assert len(reg) == 2


def test_registry_iter_returns_fz_warrant_pairs():
    reg = WarrantRegistry()
    reg.add("1a", _w("a"))
    reg.add("2a", _w("b"))
    pairs = list(reg)
    assert pairs[0][0] == "1a"
    assert pairs[0][1].claim == "a"
    assert pairs[1][0] == "2a"


# ── WarrantHistory ──────────────────────────────────────────────────────────


def test_history_record_change_appends_jsonl(tmp_path):
    path = tmp_path / "warrant_history.jsonl"
    hist = WarrantHistory(path)
    change = WarrantChange(
        cycle_id="5", kind="added", warrant=_w("first"), revision_fz="5a1a1a"
    )
    entry = hist.record_change(change)
    assert isinstance(entry, HistoryEntry)
    assert entry.change.cycle_id == "5"

    lines = path.read_text().strip().splitlines()
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed["cycle_id"] == "5"
    assert parsed["kind"] == "added"
    assert "timestamp" in parsed


def test_history_record_changes_batch(tmp_path):
    path = tmp_path / "warrant_history.jsonl"
    hist = WarrantHistory(path)
    changes = (
        WarrantChange(cycle_id="1", kind="added", warrant=_w()),
        WarrantChange(cycle_id="2", kind="revised", warrant=_w(), superseded_fz="0a"),
        WarrantChange(cycle_id="2", kind="superseded", superseded_fz="0a"),
    )
    entries = hist.record_changes(changes)
    assert len(entries) == 3
    assert len(path.read_text().strip().splitlines()) == 3


def test_history_all_returns_in_insertion_order(tmp_path):
    path = tmp_path / "warrant_history.jsonl"
    hist = WarrantHistory(path)
    hist.record_change(WarrantChange(cycle_id="A", kind="added", warrant=_w("a")))
    hist.record_change(WarrantChange(cycle_id="B", kind="added", warrant=_w("b")))

    entries = hist.all()
    assert [e.change.cycle_id for e in entries] == ["A", "B"]
    assert entries[0].change.warrant is not None
    assert entries[0].change.warrant.claim == "a"


def test_history_tail_returns_most_recent_n(tmp_path):
    path = tmp_path / "warrant_history.jsonl"
    hist = WarrantHistory(path)
    for i in range(5):
        hist.record_change(WarrantChange(cycle_id=str(i), kind="added", warrant=_w()))
    tail = hist.tail(n=3)
    assert [e.change.cycle_id for e in tail] == ["2", "3", "4"]


def test_history_missing_file_returns_empty(tmp_path):
    hist = WarrantHistory(tmp_path / "nothing.jsonl")
    assert hist.all() == []
    assert hist.tail() == []


def test_history_skips_malformed_lines(tmp_path):
    path = tmp_path / "warrant_history.jsonl"
    path.write_text(
        '{"timestamp":"2026-05-10T00:00:00+00:00","cycle_id":"1","kind":"added","warrant":null}\n'
        "not even json\n"
        '{"timestamp":"2026-05-10T00:00:01+00:00","cycle_id":"2","kind":"added","warrant":null}\n'
    )
    hist = WarrantHistory(path)
    entries = hist.all()
    assert len(entries) == 2
    assert [e.change.cycle_id for e in entries] == ["1", "2"]


def test_history_tail_zero_returns_empty(tmp_path):
    path = tmp_path / "warrant_history.jsonl"
    hist = WarrantHistory(path)
    hist.record_change(WarrantChange(cycle_id="A", kind="added"))
    assert hist.tail(n=0) == []


def test_history_path_parent_is_created(tmp_path):
    """record_change() makes the parent directory on first write."""
    path = tmp_path / "nested" / "subdir" / "warrant_history.jsonl"
    assert not path.parent.exists()
    WarrantHistory(path).record_change(WarrantChange(cycle_id="A", kind="added"))
    assert path.is_file()


# ── load_warrants_from_vault ────────────────────────────────────────────────


_DKS_PROCEDURE = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - skill
      - dks
    keywords: [k1, k2, k3]
    topics: [Tx, Ty]
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    folgezettel: "{fz}"
    folgezettel_parent: "{parent}"
    ---

    # {title}

    Body.
    """
)


_NON_DKS_PROCEDURE = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - skill
      - howto
    keywords: [k1, k2, k3]
    topics: [Tx, Ty]
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    folgezettel: "{fz}"
    folgezettel_parent: "{parent}"
    ---

    # {title}

    Not a DKS warrant — no `dks` tag.
    """
)


def _build_vault(root: Path):
    skills = root / "resources/skills"
    terms = root / "resources/term_dictionary"
    skills.mkdir(parents=True)
    terms.mkdir(parents=True)
    return skills, terms


def test_load_from_empty_vault(tmp_path):
    reg = load_warrants_from_vault(tmp_path)
    assert len(reg) == 0


def test_load_picks_up_dks_tagged_procedure(tmp_path):
    skills, _ = _build_vault(tmp_path)
    (skills / "procedure_warrant_one.md").write_text(
        _DKS_PROCEDURE.format(fz="2a3a", parent="2a3", title="W1")
    )
    reg = load_warrants_from_vault(tmp_path)
    assert "2a3a" in reg
    assert len(reg) == 1


def test_load_ignores_non_dks_procedure(tmp_path):
    skills, _ = _build_vault(tmp_path)
    (skills / "procedure_howto.md").write_text(
        _NON_DKS_PROCEDURE.format(fz="9", parent="", title="Howto")
    )
    reg = load_warrants_from_vault(tmp_path)
    assert len(reg) == 0


def test_load_picks_up_dks_concept_term(tmp_path):
    _, terms = _build_vault(tmp_path)
    payload = _DKS_PROCEDURE.replace(
        "building_block: procedure", "building_block: concept"
    )
    (terms / "concept_rule.md").write_text(
        payload.format(fz="2a1a", parent="2a1", title="Concept Rule")
    )
    reg = load_warrants_from_vault(tmp_path)
    assert "2a1a" in reg
