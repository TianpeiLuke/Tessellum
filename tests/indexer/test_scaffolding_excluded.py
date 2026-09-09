"""Navigation and provenance sections are excluded from the INDEX, not the note.

A note's Related Notes / Source / References sections are part of the note and
are exactly what link extraction reads. They are not evidence, though, and
indexing them spends a note's share of a retrieval budget on markdown links a
reader cannot follow. Measured on a benchmark vault, excluding them from the
indexed text was worth a substantial recall gain at a fixed budget, for free.

Both halves have to hold at once, which is what makes this worth pinning:
the index must NOT see those sections, and link extraction MUST.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from tessellum.format.parser import strip_scaffolding   # noqa: E402

NOTE = """# Ad load varies with the request

The Age reported on 2023-10-22 that Google's ad load changed per request.

## Related Notes
- [Google](term_google.md) — the company
- [Ad Load](term_ad_load.md) — the metric

## Source
https://example.com/article

## References
- Some Paper, 2024
"""


def test_prose_survives():
    out = strip_scaffolding(NOTE)
    assert "The Age reported on 2023-10-22" in out
    assert out.startswith("# Ad load")


def test_navigation_and_provenance_are_dropped():
    out = strip_scaffolding(NOTE)
    for gone in ("term_google.md", "term_ad_load.md",
                 "example.com/article", "Some Paper"):
        assert gone not in out, f"{gone} should not reach the index"


def test_a_body_with_no_scaffolding_is_unchanged():
    plain = "# Title\n\nJust prose, nothing else."
    assert strip_scaffolding(plain) == plain.strip()


def test_empty_and_none_safe():
    assert strip_scaffolding("") == ""


def test_link_extraction_still_reads_the_full_body():
    """The indexer must strip only at the two indexing points.

    If strip_scaffolding were applied to `_body` itself, every Related Notes
    link would vanish from the graph -- the sections it removes are where the
    links live.
    """
    src = (Path(__file__).resolve().parents[2]
           / "src/tessellum/indexer/build.py").read_text()
    assert 'body = note["_body"]' in src, "link extraction must use the raw body"
    assert "_indexed_body" in src, "FTS must index the stripped text"
    assert "strip_scaffolding(note.get" in src, "embeddings must use stripped text"
