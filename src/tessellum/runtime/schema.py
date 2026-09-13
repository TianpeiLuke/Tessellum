"""One home for the runtime DDL, and a way to apply part of it.

``schema.sql`` is the single source of every table the runtime owns —
:class:`~tessellum.runtime.store.RuntimeStore` applies the whole file, and that
stays true. But two of its tables have a second, narrower consumer:

* the Tier-A ``relations`` cache is applied to the **registry sidecar** database
  as well, which has its own lifetime (rebuild whenever the vault changes)
  rather than the queue's (durable across restarts);
* the Tier-B ``query_cache`` / ``feedback`` pair is applied by a store that may
  be opened on either file.

Before this module those consumers each carried their own copy of the DDL, and
the two copies of ``relations`` had already drifted apart — different NOT NULLs,
one extra column on one side, and a runtime probe existing purely to work out
which shape it had been handed. Two definitions of one table is not a schema, it
is a coincidence, so the file is now cut into **named sections** and a consumer
applies the sections it owns instead of restating them.

The markers are ordinary SQL comments, so the file remains directly executable
by ``sqlite3`` and by ``executescript``; the slicing is a convenience for the
narrower consumers, never a precondition for reading the schema.
"""

from __future__ import annotations

from importlib.resources import files

SECTION_BEGIN = "-- ##### BEGIN SECTION: {name} #####"
SECTION_END = "-- ##### END SECTION: {name} #####"

WAL_PRAGMA = "PRAGMA journal_mode = WAL;\n"
"""Prepended by sidecar consumers, which do not apply the file's header."""


class SchemaSectionError(LookupError):
    """A named section is missing from ``schema.sql`` — a rename, not a typo.

    Raised rather than returning an empty string, because a silently empty DDL
    string creates no tables and then fails much later as a missing-table error
    from inside a transaction.
    """


def schema_text() -> str:
    """The whole of ``schema.sql``, as shipped."""
    return files("tessellum.runtime").joinpath("schema.sql").read_text(encoding="utf-8")


def schema_section(name: str, *, with_pragma: bool = False) -> str:
    """The DDL between the ``name`` markers, markers excluded.

    Args:
        name: Section name as it appears in the ``BEGIN``/``END`` markers.
        with_pragma: Prepend :data:`WAL_PRAGMA`. Sidecar databases want it
            (they never apply the file's header); the runtime database already
            has it.

    Raises:
        SchemaSectionError: when either marker is absent, or they are in the
            wrong order.
    """
    text = schema_text()
    begin = SECTION_BEGIN.format(name=name)
    end = SECTION_END.format(name=name)
    start = text.find(begin)
    stop = text.find(end)
    if start < 0 or stop < 0 or stop < start:
        raise SchemaSectionError(
            f"schema.sql has no section {name!r} (looked for {begin!r} .. {end!r}); "
            "a section was renamed or removed without updating its consumer"
        )
    body = text[start + len(begin) : stop].strip("\n") + "\n"
    return f"{WAL_PRAGMA}\n{body}" if with_pragma else body


__all__ = [
    "SECTION_BEGIN",
    "SECTION_END",
    "WAL_PRAGMA",
    "SchemaSectionError",
    "schema_section",
    "schema_text",
]
