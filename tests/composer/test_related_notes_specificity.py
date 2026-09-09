"""Link selection must down-weight hubs, not just rank by relevance.

A vault-wide audit found only ~1 in 5 links spans a real gap: relevance-ranked
selection picks the notes a query would already surface, and the fixed ">= 8
term notes" floor made authors fill the count with the most similar notes -- the
least useful to traverse to. A note everything links to (in-degree in the
hundreds or thousands) carries almost no information about where the reader
came from. Specificity, 1/log(in_degree + e), is the signal that separates a
bridge from a restatement, and it is independent of relevance.
"""
import math
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from tessellum.composer import related_notes as rn   # noqa: E402


def _db(tmp_path, links):
    db = tmp_path / "t.db"
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE note_links (source_note_id TEXT, target_note_id TEXT)")
    c.executemany("INSERT INTO note_links VALUES (?,?)", links)
    c.commit(); c.close()
    return db


def _note(nid, score):
    return rn.RelatedNote(note_id=nid, note_name=Path(nid).stem,
                          rel_path=nid, score=score, source="seed")


def test_hub_sinks_below_specific_note_at_equal_relevance(tmp_path):
    # hub has 300 inbound links, specific has 2
    links = [(f"s{i}.md", "hub.md") for i in range(300)] + [("a.md", "specific.md"), ("b.md", "specific.md")]
    db = _db(tmp_path, links)
    ordered = [_note("hub.md", 1.0), _note("specific.md", 1.0)]
    out = rn._apply_specificity(ordered, db)
    assert [r.note_id for r in out] == ["specific.md", "hub.md"]


def test_kernel_is_one_over_log_degree_plus_e(tmp_path):
    db = _db(tmp_path, [(f"s{i}.md", "n.md") for i in range(50)])
    out = rn._apply_specificity([_note("n.md", 2.0)], db)
    assert math.isclose(out[0].score, 2.0 / math.log(50 + math.e), rel_tol=1e-9)


def test_relevance_still_wins_when_specificity_is_equal(tmp_path):
    db = _db(tmp_path, [("x.md", "a.md"), ("x.md", "b.md")])
    out = rn._apply_specificity([_note("a.md", 0.4), _note("b.md", 0.9)], db)
    assert out[0].note_id == "b.md"


def test_missing_link_table_is_fail_soft(tmp_path):
    db = tmp_path / "empty.db"; sqlite3.connect(db).close()
    ordered = [_note("a.md", 0.5), _note("b.md", 0.9)]
    out = rn._apply_specificity(ordered, db)
    assert [r.note_id for r in out] == ["a.md", "b.md"], "unchanged order when no signal"


def test_term_floor_is_a_reserve_not_a_count():
    """The floor must not exceed the audit-motivated default even if asked."""
    assert rn.DEFAULT_MIN_TERM_NOTES <= 4
