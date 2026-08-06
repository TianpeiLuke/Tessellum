"""Unit tests for the prefix-derived Folgezettel parent.

``folgezettel_parent`` is no longer an authored YAML field — it is derived from
the ``folgezettel`` ID's prefix (a pure substring). These tests pin the
derivation and the ``Note.folgezettel_parent`` property that exposes it.
"""

from __future__ import annotations

import pytest

from tessellum.format.parser import derive_folgezettel_parent, parse_text


@pytest.mark.parametrize(
    "fz, expected_parent",
    [
        # single-segment roots have no parent
        ("1", None),
        ("20", None),
        ("9", None),
        # letter appended to a digit run
        ("1a", "1"),
        ("20l", "20"),
        # digit appended to a letter run
        ("1a1", "1a"),
        ("20l2", "20l"),
        # deep chains, alternating classes
        ("1a1b", "1a1"),
        ("7b1b2a", "7b1b2"),
        ("20l2a", "20l2"),
        # multi-digit segments (boundary is the digit↔letter switch, not per char)
        ("9h10", "9h"),
        ("9h11", "9h"),
        ("20l12", "20l"),
        # empty / None
        ("", None),
        (None, None),
    ],
)
def test_derive_folgezettel_parent(fz, expected_parent):
    assert derive_folgezettel_parent(fz) == expected_parent


def test_parent_is_always_a_prefix_of_the_child():
    for fz in ("20l2", "9h10", "1a1b", "7b1b2a"):
        parent = derive_folgezettel_parent(fz)
        assert parent is not None
        assert fz.startswith(parent)
        assert len(parent) < len(fz)


def test_note_property_derives_parent_ignoring_any_authored_field():
    # A stray authored folgezettel_parent must be IGNORED — the derived value
    # (from the folgezettel prefix) is authoritative.
    text = (
        "---\n"
        'folgezettel: "20l2"\n'
        'folgezettel_parent: "99z"\n'  # wrong on purpose; must be ignored
        "---\n"
        "# body\n"
    )
    note = parse_text(text)
    assert note.folgezettel == "20l2"
    assert note.folgezettel_parent == "20l"


def test_note_property_none_when_no_folgezettel():
    note = parse_text("---\nbuilding_block: concept\n---\n# body\n")
    assert note.folgezettel is None
    assert note.folgezettel_parent is None
