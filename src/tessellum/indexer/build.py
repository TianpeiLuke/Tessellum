"""Build the unified SQLite index from a vault.

Single entry point: :func:`build`. Walks the vault filesystem, parses each
markdown note via :func:`tessellum.format.parse_note`, extracts internal
markdown links with broken-path detection, and writes rows into the
``notes`` and ``note_links`` tables in one transaction.

Idempotent — the DB is dropped + recreated each run. Incremental updates
ship in v0.0.13.
"""

from __future__ import annotations

import json
import re
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from tessellum.format.parser import FrontmatterParseError, parse_note

_SCHEMA_PATH = Path(__file__).parent / "schema.sql"

# Markdown link regex: ``[text](path.md)`` with optional ``#anchor``.
# Allows nested ``[..]`` in text (matches link_checker but tightened to
# require ``.md`` extension here — links to other formats aren't note
# relationships).
_MARKDOWN_LINK_RE = re.compile(
    r"\[([^\[\]]*(?:\[[^\]]*\][^\[\]]*)*)\]\(([^)]+\.md)(?:#[^)]*)?\)"
)
_FENCED_CODE_RE = re.compile(r"```[^\n]*\n.*?```", re.DOTALL)
_EXTERNAL_RE = re.compile(r"^https?://", re.IGNORECASE)

# Files in the vault that aren't notes. Mirrors the CLI skip list in
# tessellum.cli.format_check so ``tessellum format check`` and
# ``tessellum index build`` see the same set of "real" notes.
_NON_NOTE_NAMES: frozenset[str] = frozenset(
    {
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "DEVELOPING.md",
        "LICENSE.md",
        "MEMORY.md",
    }
)
_NON_NOTE_PREFIXES: tuple[str, ...] = ("Rank_",)


@dataclass(frozen=True)
class BuildResult:
    """Summary of a successful :func:`build` invocation."""

    db_path: Path
    notes_indexed: int
    links_indexed: int
    skipped_files: int
    duration_seconds: float


def build(
    vault_path: Path | str,
    db_path: Path | str,
    *,
    force: bool = False,
) -> BuildResult:
    """Scan ``vault_path`` and write the unified index to ``db_path``.

    Args:
        vault_path: Vault root (directory containing ``0_entry_points/``,
            ``resources/``, ``projects/``, ``areas/``, ``archives/``).
        db_path: Output SQLite DB path. Parent dirs are created as needed.
            If the file exists, raises ``FileExistsError`` unless
            ``force=True`` (which deletes + recreates).
        force: Allow overwriting an existing DB.

    Returns:
        BuildResult with row counts + duration.

    Raises:
        FileNotFoundError: ``vault_path`` does not exist.
        FileExistsError: ``db_path`` exists and ``force=False``.
    """
    vault = Path(vault_path).expanduser().resolve()
    if not vault.is_dir():
        raise FileNotFoundError(f"vault path does not exist: {vault}")

    db = Path(db_path).expanduser().resolve()
    if db.exists():
        if not force:
            raise FileExistsError(
                f"db {db} already exists. Pass force=True to overwrite."
            )
        db.unlink()
    db.parent.mkdir(parents=True, exist_ok=True)

    started = time.monotonic()

    md_files = sorted(_walk_vault(vault))
    notes_meta: list[dict] = []
    skipped = 0
    for f in md_files:
        meta = _extract_note_metadata(f, vault)
        if meta is None:
            skipped += 1
            continue
        notes_meta.append(meta)

    name_index = _build_note_name_index(notes_meta)
    links_records = _extract_all_links(notes_meta, vault, name_index)

    conn = sqlite3.connect(str(db))
    try:
        with conn:
            conn.executescript(_SCHEMA_PATH.read_text(encoding="utf-8"))
            _write_notes(conn, notes_meta)
            _write_links(conn, links_records)
    finally:
        conn.close()

    return BuildResult(
        db_path=db,
        notes_indexed=len(notes_meta),
        links_indexed=len(links_records),
        skipped_files=skipped,
        duration_seconds=time.monotonic() - started,
    )


# ── Vault walk ────────────────────────────────────────────────────────────


def _walk_vault(vault: Path) -> list[Path]:
    files: list[Path] = []
    for f in vault.rglob("*.md"):
        if not _is_note_file(f):
            continue
        files.append(f)
    return files


def _is_note_file(p: Path) -> bool:
    if p.name in _NON_NOTE_NAMES:
        return False
    if any(p.name.startswith(prefix) for prefix in _NON_NOTE_PREFIXES):
        return False
    return True


# ── Metadata extraction ───────────────────────────────────────────────────


_PARA_FOLDERS: frozenset[str] = frozenset(
    {"0_entry_points", "areas", "projects", "resources", "archives"}
)
_CATEGORY_MAP = {
    "0_entry_points": "entry_point",
    "areas": "area",
    "projects": "project",
    "resources": "resource",
    "archives": "archive",
}


def _extract_note_metadata(md_file: Path, vault_path: Path) -> dict | None:
    """Read one markdown file → metadata dict for the ``notes`` row.

    Returns ``None`` if the file has unparseable frontmatter (skipped from
    the index; ``tessellum format check`` will surface the issue).
    """
    try:
        note = parse_note(md_file)
    except FrontmatterParseError:
        return None

    front = note.frontmatter
    stat = md_file.stat()
    update_dt = datetime.fromtimestamp(stat.st_mtime)
    relative_path = md_file.relative_to(vault_path)

    tags = front.get("tags") or []
    if not isinstance(tags, list):
        tags = []

    note_category = _determine_note_category(relative_path)
    note_second_category = _determine_second_category(tags, relative_path)

    return {
        "note_id": str(relative_path),
        "note_name": md_file.stem,
        "note_location": str(relative_path.parent),
        "note_category": note_category,
        "note_second_category": note_second_category,
        "note_status": _str_or_none(front.get("status")),
        "note_creation_date": _str_or_none(front.get("date of note"))
        or update_dt.date().isoformat(),
        "note_update_date": update_dt.date().isoformat(),
        "file_path": str(relative_path),
        "file_size_bytes": stat.st_size,
        "tags": json.dumps([str(t) for t in tags]),
        "keywords": json.dumps([str(k) for k in (front.get("keywords") or [])]),
        "topics": json.dumps([str(t) for t in (front.get("topics") or [])]),
        "language": _str_or_none(front.get("language")),
        "building_block": _str_or_none(front.get("building_block")),
        "folgezettel": _str_or_none(front.get("folgezettel")),
        "folgezettel_parent": _str_or_none(
            front.get("folgezettel_parent") or front.get("fz_parent")
        ),
        "last_indexed_mtime": stat.st_mtime,
        "_body": note.body,  # consumed by link extraction; not written to DB
    }


def _str_or_none(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def _determine_note_category(relative_path: Path) -> str | None:
    parts = relative_path.parts
    if not parts:
        return None
    return _CATEGORY_MAP.get(parts[0])


def _determine_second_category(
    tags: list, relative_path: Path
) -> str | None:
    """Tessellum's tags[1] is the source of truth (per DEVELOPING.md rule 5).

    Falls back to the immediate parent directory's name if the tags list
    has fewer than 2 entries (defensive — invalid notes still get an
    indexable second-category guess so users can find them via WHERE
    queries on partial vault state).
    """
    if isinstance(tags, list) and len(tags) >= 2 and isinstance(tags[1], str):
        return tags[1]
    parts = relative_path.parts
    if len(parts) >= 2:
        parent = parts[-2]
        if parent not in _PARA_FOLDERS:
            return parent
    return None


# ── Link extraction ───────────────────────────────────────────────────────


def _build_note_name_index(notes: list[dict]) -> dict[str, str | list[str]]:
    """name -> note_id (str) or [note_ids] (list if duplicate names)."""
    idx: dict[str, str | list[str]] = {}
    for note in notes:
        name = note["note_name"]
        if name not in idx:
            idx[name] = note["note_id"]
        else:
            existing = idx[name]
            if isinstance(existing, str):
                idx[name] = [existing, note["note_id"]]
            else:
                existing.append(note["note_id"])
    return idx


def _extract_all_links(
    notes: list[dict],
    vault_path: Path,
    name_index: dict[str, str | list[str]],
) -> list[dict]:
    """Return one link record per resolvable internal markdown link.

    Records have keys: source_note_id, target_note_id, link_context,
    link_type ('markdown' or 'markdown_broken_path').

    Broken-path detection: if a relative-path target doesn't exist BUT the
    target's stem uniquely names an existing note, the link is recorded
    with ``link_type = 'markdown_broken_path'`` and ``target_note_id``
    pointing at the unique match. If the stem is missing or ambiguous,
    the link is silently dropped (will surface as LINK-003 in
    ``tessellum format check``).
    """
    links: list[dict] = []
    seen_pairs: set[tuple[str, str]] = set()  # dedupe per UNIQUE constraint

    for note in notes:
        source_id = note["note_id"]
        body = note["_body"]
        body_no_code = _FENCED_CODE_RE.sub("", body)
        source_path = vault_path / source_id

        for match in _MARKDOWN_LINK_RE.finditer(body_no_code):
            target_text = match.group(2).strip()
            if _EXTERNAL_RE.match(target_text):
                continue
            if target_text.startswith(("mailto:", "#")):
                continue

            target_id, ghost_id = _resolve_link(target_text, vault_path, source_path)

            if target_id is None and ghost_id is not None:
                # Try name-based fallback for typo'd paths.
                stem = Path(ghost_id).stem
                hit = name_index.get(stem)
                if isinstance(hit, str):
                    target_id = hit
                    link_type = "markdown_broken_path"
                else:
                    continue  # truly broken; skip
            else:
                link_type = "markdown"

            if target_id is None:
                continue

            pair = (source_id, target_id)
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            start = max(0, match.start() - 50)
            end = min(len(body_no_code), match.end() + 50)
            context = body_no_code[start:end].replace("\n", " ").strip()

            links.append(
                {
                    "source_note_id": source_id,
                    "target_note_id": target_id,
                    "link_context": context,
                    "link_type": link_type,
                }
            )

    return links


def _resolve_link(
    link_target: str, vault_path: Path, source_note_path: Path
) -> tuple[str | None, str | None]:
    """Resolve a relative markdown link target.

    Returns:
        (note_id, None) — the file exists inside the vault.
        (None, ghost_path) — the path resolves inside the vault but the
            file is missing (ghost / broken target).
        (None, None) — the link points outside the vault entirely.
    """
    target = link_target[:-3] if link_target.endswith(".md") else link_target
    source_dir = source_note_path.parent
    try:
        resolved = (source_dir / f"{target}.md").resolve()
        try:
            relative = resolved.relative_to(vault_path.resolve())
            return (str(relative), None) if resolved.exists() else (None, str(relative))
        except ValueError:
            return (None, None)
    except (OSError, RuntimeError):
        return (None, None)


# ── DB writes ─────────────────────────────────────────────────────────────


_NOTES_INSERT_COLUMNS: tuple[str, ...] = (
    "note_id",
    "note_name",
    "note_location",
    "note_category",
    "note_second_category",
    "note_status",
    "note_creation_date",
    "note_update_date",
    "file_path",
    "file_size_bytes",
    "tags",
    "keywords",
    "topics",
    "language",
    "building_block",
    "folgezettel",
    "folgezettel_parent",
    "last_indexed_mtime",
)


def _write_notes(conn: sqlite3.Connection, notes: list[dict]) -> None:
    placeholders = ", ".join(f":{c}" for c in _NOTES_INSERT_COLUMNS)
    columns = ", ".join(_NOTES_INSERT_COLUMNS)
    sql = f"INSERT INTO notes ({columns}) VALUES ({placeholders})"
    conn.executemany(sql, notes)


def _write_links(conn: sqlite3.Connection, links: list[dict]) -> None:
    sql = (
        "INSERT INTO note_links "
        "(source_note_id, target_note_id, link_context, link_type) "
        "VALUES (:source_note_id, :target_note_id, :link_context, :link_type)"
    )
    conn.executemany(sql, links)
