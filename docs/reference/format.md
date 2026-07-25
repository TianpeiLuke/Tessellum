# `tessellum.format` — Reference

API, symbols, constants, rules, and CLI surface for the note-format layer. For the concepts and design rationale see [../format.md](../format.md).

## Files → Role

| File | Role |
|------|------|
| `parser.py` | Frozen `Note` dataclass + `parse_note` / `parse_text`. Regex-splits `---` frontmatter, `yaml.safe_load`s it, keeps `raw_frontmatter`. Raises `FrontmatterParseError` if frontmatter isn't a YAML mapping. |
| `frontmatter_spec.py` | Closed enums, soft minima, regexes, required/forbidden field sets. `VALID_BUILDING_BLOCKS` is re-exported from `bb.types.VALID_BB_TYPE_VALUES`, not defined locally. |
| `validator.py` | The rule engine: `validate` / `is_valid` + per-rule `_check_*` helpers. Owns YAML-\*, TESS-001/002/003, YAML-100/101, and the two BB-graph-aware rules TESS-004/005. Delegates LINK-\* to `link_checker`. |
| `link_checker.py` | `check_links(note)` → LINK-001/002/003/006 (all WARNING). Owns the skip lists. |
| `issue.py` | `Severity` (str-Enum) + frozen `Issue`. Own module to avoid a `validator` ↔ `link_checker` import cycle. |
| `building_blocks.py` | BB taxonomy view re-exported by `__init__` (`BuildingBlock`, `BBSpec`, `BBEdge`, `BB_SPECS`, `EPISTEMIC_EDGES`, `get_spec`, `downstream`, `upstream`, `types_in_layer`, `EpistemicLayer`). |
| `__init__.py` | Public surface: parser, spec constants, `Issue`/`Severity`, `validate`/`is_valid`/`check_links`, BB taxonomy. |
| `cli/format_check.py` | `tessellum format check <path>` — wires `validate` into the CLI, recurses `*.md`, filters non-note files, emits human/JSON, computes exit code. Registered in `cli/main.py`. |

## Public API (`tessellum.format`)

| Symbol | Signature | Description |
|--------|-----------|-------------|
| `validate` | `validate(target: Path \| str \| Note) -> list[Issue]` | Full report in fixed field order; empty = clean. Parses `target` if not already a `Note`. |
| `is_valid` | `is_valid(target: Path \| str \| Note) -> bool` | `True` iff `validate` returns no `Severity.ERROR` issue. |
| `parse_note` | `parse_note(path: Path \| str) -> Note` | Read + parse a file from disk. Wraps `OSError` in `FrontmatterParseError`. |
| `parse_text` | `parse_text(text: str) -> Note` | Parse an in-memory string; `path` is `None`. No frontmatter ⇒ empty dict + full text as body. |
| `check_links` | `check_links(note: Note) -> list[Issue]` | LINK-\* body-link lint (all WARNING). |
| `Note` | `@dataclass(frozen=True)` | `path`, `frontmatter: dict`, `body: str`, `raw_frontmatter: str` + convenience properties. |
| `Issue` | `@dataclass(frozen=True)` | `severity`, `rule_id`, `field: str \| None`, `message`. `__str__` → `ERROR[field] YAML-014: …`. |
| `Severity` | `str, Enum` | `ERROR="error"`, `WARNING="warning"`, `INFO="info"`. |
| `FrontmatterParseError` | `ValueError` subclass | Raised when frontmatter can't be parsed as a YAML mapping. |

### `Note` convenience properties

All coerce to `str` / `list[str]` and tolerate missing/mistyped fields (return `None` / `[]`).

| Property | Returns |
|----------|---------|
| `tags` | `list[str]` (empty if not a list) |
| `para_bucket` | `tags[0]` or `None` |
| `second_category` | `tags[1]` or `None` |
| `building_block` | `str(building_block)` or `None` |
| `status` | `str(status)` or `None` |
| `folgezettel` | `str(folgezettel)` or `None` |
| `folgezettel_parent` | `folgezettel_parent`, falling back to `fz_parent`, else `None` |

## Spec Constants (`frontmatter_spec.py`)

| Constant | Value |
|----------|-------|
| `VALID_PARA_BUCKETS` | `frozenset`, 5: `resource`, `area`, `project`, `archive`, `entry_point` |
| `VALID_BUILDING_BLOCKS` | Re-export of `bb.types.VALID_BB_TYPE_VALUES` (8 BB types) |
| `VALID_STATUSES` | `frozenset`, 21: `active`, `draft`, `archived`, `deprecated`, `superseded`, `stub`, `placeholder`, `template`, `wip`, `in_progress`, `production`, `proposal`, `development`, `planning`, `legacy`, `disabled`, `research`, `review`, `pending`, `completed`, `cancelled` |
| `REQUIRED_FIELDS` | tuple, 7: `tags`, `keywords`, `topics`, `language`, `date of note`, `status`, `building_block` |
| `FORBIDDEN_FIELDS` | `frozenset`, 1: `note_second_category` |
| `MIN_TAGS_REQUIRED` | `2` |
| `MIN_KEYWORDS_RECOMMENDED` | `3` |
| `MIN_TOPICS_RECOMMENDED` | `2` |
| `DATE_FORMAT_REGEX` | `^\d{4}-\d{2}-\d{2}$` |
| `TAG_FORMAT_REGEX` | `^[a-z0-9_]+$` |

## Rule Catalog

Severity legend: **E** = ERROR (fails `is_valid`), **W** = WARNING (advisory).

### Frontmatter presence / type / value (validator.py)

| Rule | Field | Severity | Condition |
|------|-------|----------|-----------|
| YAML-010 | `tags` | E | required field missing |
| YAML-020 | `keywords` | E | required field missing |
| YAML-030 | `topics` | E | required field missing |
| YAML-040 | `language` | E | required field missing |
| YAML-050 | `date of note` | E | required field missing |
| YAML-060 | `status` | E | required field missing |
| YAML-062 | `building_block` | E | required field missing |
| YAML-011 | `tags` | E | not a list |
| YAML-012 | `tags` | E | fewer than `MIN_TAGS_REQUIRED` (2) entries |
| YAML-013 | `tags[i]` | E | element not a string |
| YAML-014 | `tags[0]` | E | not in `VALID_PARA_BUCKETS` |
| YAML-015 | `tags[i]` | E | fails `TAG_FORMAT_REGEX` |
| YAML-021 | `keywords` | E | present but not a list |
| YAML-022 | `keywords` | W | fewer than `MIN_KEYWORDS_RECOMMENDED` (3) |
| YAML-031 | `topics` | E | present but not a list |
| YAML-032 | `topics` | W | fewer than `MIN_TOPICS_RECOMMENDED` (2) |
| YAML-063 | `building_block` | E | non-string, or not in `VALID_BUILDING_BLOCKS` |
| YAML-061 | `status` | E | non-string, or not in `VALID_STATUSES` |
| YAML-051 | `date of note` | E | stringified value fails `DATE_FORMAT_REGEX` |

Enum, date, and list-min checks **skip when the value is absent** (presence is owned by the required-field check — no double-report).

### Tessellum frontmatter rules (validator.py)

| Rule | Field | Severity | Condition |
|------|-------|----------|-----------|
| TESS-001 | `folgezettel_parent` | E | `folgezettel` set without `folgezettel_parent`/`fz_parent` |
| TESS-002 | `folgezettel` | E | parent set without `folgezettel` |
| TESS-003 | forbidden field | E | any `FORBIDDEN_FIELDS` member present (bespoke message for `note_second_category`) |
| YAML-100 | (none) | E | `[[...]]` wiki link found in `raw_frontmatter` (scanned line-by-line, offset starts at 2) |
| YAML-101 | (none) | E | `[..](..)` markdown link found in `raw_frontmatter` |

### Body-link rules — `link_checker.check_links` (all WARNING)

| Rule | Field | Condition |
|------|-------|-----------|
| LINK-001 | `links` | internal link missing `.md` extension |
| LINK-002 | `links` | internal link uses an absolute path (`/…`) |
| LINK-003 | `links` | internal `.md` target does not exist on disk (relative to `note.path.parent`); only runs when `note.path` is set and the path isn't absolute |
| LINK-006 | `links` | note has no internal `.md` links (orphan); **skipped for `status: template`** |

### BB-graph-aware rules (validator.py)

| Rule | Field | Severity | Fires when | Condition |
|------|-------|----------|-----------|-----------|
| TESS-004 | `links` | E | `building_block == "counter_argument"` AND `status == "active"` AND `note.path` set | no internal `.md` body link resolves to a `building_block: argument` note |
| TESS-005 | `links` | W | source `building_block` is BB-typed AND `status == "active"` AND `note.path` set | a body link to a *different* BB-typed target whose (source→target) pair is in the BB schema in **neither** direction |

TESS-004 does **not** require the target's FZ to match the counter's `folgezettel_parent` (that stronger invariant is enforced by the indexer/DKS at write time). TESS-005 is **version-aware**: an integer `bb_schema_version ≥ 1` in frontmatter selects `bb.types.BB_SCHEMA_AT_VERSION(n)` (message tagged `@v{n}`); otherwise it falls back to the live `bb.types.BB_SCHEMA` (tagged `@live`). Both rules strip fenced code before scanning, skip same-BB targets, skip un-typed / unresolvable / unparseable targets, and dedup repeat targets.

## Link Checker Skip Lists (`link_checker.py`)

Links matching any of these are never flagged:

- **External / anchor**: `^https?://`, `mailto:`, `#…`.
- **Non-markdown extensions** (`_NON_MD_EXTS`): images (`.png .jpg .jpeg .gif .svg .webp`), documents (`.pdf .docx .xlsx .pptx .csv`), code + data (`.py .sh .sql .json .yaml .yml .xml .html .txt .zip .ipynb`), config (`.toml .cfg .ini .lock .env`), LaTeX/bib (`.drawio .tex .bib .sty .cls`).
- **Directory links**: trailing `/`.
- **Placeholder targets** (`_PLACEHOLDER_TARGETS`): `-`, `link`, `path`, `url`, `ticket_link`, `ticket_query_link`, `source`, `target`, `...`, `.*?`.
- **Template-ish prefixes**: `<`, `{`, `_no_`.
- **Code fences**: content stripped via `_FENCED_CODE_RE` before scanning.

## Regexes (validator.py / link_checker.py / parser.py)

| Name | Pattern | Use |
|------|---------|-----|
| `_DATE_RE` | `^\d{4}-\d{2}-\d{2}$` | date format |
| `_TAG_RE` | `^[a-z0-9_]+$` | tag slug format |
| `_WIKI_LINK_RE` | `\[\[.*?\]\]` | YAML-100 |
| `_MD_LINK_RE` | `\[[^\]]+\]\([^)]+\)` | YAML-101 |
| `_FENCED_CODE_RE` | ` ```[^\n]*\n.*?``` ` (DOTALL) | strip code fences |
| `_BODY_MD_LINK_RE` / `_LINK_RE` | `\[([^\]]+)\]\(([^)]+)\)` | body-link extraction |
| `_EXTERNAL_RE` | `^https?://` (IGNORECASE) | external-link skip |
| `_FRONTMATTER_RE` | `^---\s*\n(.*?)\n---\s*\n?(.*)$` (DOTALL) | frontmatter split (parser.py) |

## CLI — `tessellum format check`

```
tessellum format check <path> [--strict] [--quiet|-q] [--format human|json]
```

| Flag | Effect |
|------|--------|
| `<path>` | A `.md` file or a directory. Directories `rglob("*.md")` and skip non-note files. |
| `--strict` | Promote warnings to CI-failing (exit 1 on any WARNING). Does not change `Issue` severities. |
| `--quiet` / `-q` | Print only files with issues; suppress the summary when clean. |
| `--format human\|json` | Output format (default `human`). |

**Non-note filter** (`_is_note_file`): excludes exact names `_NON_NOTE_NAMES` = `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `DEVELOPING.md`, `LICENSE.md`, `MEMORY.md`; and any name with prefix in `_NON_NOTE_PREFIXES` = `Rank_`.

**Human output**: per-file issue lines (`  ERROR[field] RULE-ID: message`) followed by a summary: `validated N file(s); M with issues; E error(s), W warning(s), I info(s)`.

**JSON output** (`_emit_json`):

```json
{
  "files": [{"path": "...", "issues": [{"rule_id": "...", "severity": "...", "field": "...", "message": "..."}]}],
  "summary": {"files_checked": 0, "files_with_issues": 0, "errors": 0, "warnings": 0, "infos": 0}
}
```

**Exit codes** (`_exit_code`):

| Code | Meaning |
|------|---------|
| 0 | no errors (warnings/infos OK; warnings OK unless `--strict`) |
| 1 | ≥1 ERROR, or any WARNING under `--strict` |
| 2 | invocation error (path missing, or not a `.md` file/directory) |

The `format` subparser is registered in `cli/main.py` alongside `init`, `capture`, `index`, `search`, `filter`, `fz`, `bb`, `composer`, `dks`, `mcp`, `runtime`.

## Extension Points

- **New frontmatter rule**: add a `_check_*` helper in `validator.py` + one `issues.extend(...)` line in `validate`, preserving field order. IDs: `YAML-0xx` presence/type/value, `YAML-1xx` linkage, `TESS-0xx` Tessellum-specific.
- **New enum value / required field**: edit `frontmatter_spec.py` only. BB types are the exception — edit `bb.types.BBType`; `VALID_BUILDING_BLOCKS` follows automatically.
- **New body-link rule**: extend `link_checker.py` (LINK-\*) or add a BB-graph-aware rule in `validator.py`. Reuse the skip-list / code-fence-strip / on-disk-resolve pattern.
- **New BB edge for TESS-004/005**: amend the schema in `bb.types`; TESS-005's version-aware path picks it up via `BB_SCHEMA_AT_VERSION`. No `validator.py` change needed.
- **New output format**: add an `_emit_*` in `format_check.py` and branch in `run_format_check`; keep `_exit_code` the single exit-code authority.
- **Non-note filename filters**: extend `_NON_NOTE_NAMES` / `_NON_NOTE_PREFIXES`.
