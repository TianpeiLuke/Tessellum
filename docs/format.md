# `tessellum.format` — Note Format & Validation

## 1. Purpose

`tessellum.format` defines what a Tessellum atomic note *is* — the YAML frontmatter spec, the typed body-link contract, and the rule engine that decides pass/fail — operating purely over a single note's text on disk with no database dependency. It is the static, per-note validator for **System P** (the markdown vault substrate), distinct from the index/retrieval side (System D); everything here is a deterministic function of `(frontmatter, body, and — for two cross-note rules — the resolved link targets on disk)`.

## 2. Architecture / Data Flow

The layer is a pipeline of pure functions:

```
path/str/Note ──parse_note/parse_text──▶ Note(frozen) ──validate──▶ list[Issue]
                                              │                          │
                                              ├─ raw_frontmatter ────────┤ (YAML-100/101 scan)
                                              ├─ frontmatter (dict) ─────┤ (YAML-*, TESS-001/002/003)
                                              └─ body ───────────────────┤ (LINK-* via link_checker;
                                                                          │  TESS-004/005 resolve
                                                                          │  target notes from disk)
                                                                          ▼
                                        is_valid() = no ERROR-severity Issue
```

`validate(target)` (`validator.py:validate`) accepts a `Path`, `str`, or an already-parsed `Note`; if not already a `Note` it calls `parse_note` (`parser.py:parse_note`). It then appends `Issue`s from each rule group in a fixed field order and returns the flat list. `is_valid(target)` (`validator.py:is_valid`) is the boolean shortcut: `True` iff no `Issue` has `Severity.ERROR` — warnings and infos never fail a note.

Two rules (**TESS-004**, **TESS-005**) are *BB-graph-aware*: they re-`parse_note` the link targets referenced in the body to read the target's `building_block`, and consult the BB schema in `tessellum.bb.types`. They still take no database — resolution is `note.path.parent / link` on the filesystem. Every other rule is intra-note.

## 3. Key Modules + Abstractions

| File | Role |
|------|------|
| `parser.py` | Frozen `Note` dataclass + `parse_note`/`parse_text`. Regex-splits `---` frontmatter, `yaml.safe_load`s it, and **keeps `raw_frontmatter`** (the original YAML text) so downstream checks can scan the source. Raises `FrontmatterParseError` if frontmatter isn't a YAML mapping. |
| `frontmatter_spec.py` | Closed enums + soft minima + regexes: `VALID_PARA_BUCKETS` (5), `VALID_STATUSES` (21), `REQUIRED_FIELDS` (7), `FORBIDDEN_FIELDS`, `MIN_*`, `DATE_FORMAT_REGEX`, `TAG_FORMAT_REGEX`. `VALID_BUILDING_BLOCKS` is **re-exported from `bb.types.VALID_BB_TYPE_VALUES`**, not defined locally. |
| `validator.py` | The rule engine: `validate` / `is_valid` plus per-rule helpers. Owns YAML-\* frontmatter rules, TESS-001/002 (folgezettel pair), TESS-003 (forbidden), YAML-100/101 (links-in-YAML), and the two BB-graph-aware rules TESS-004/005. Delegates LINK-\* to `link_checker`. |
| `link_checker.py` | `check_links(note)` → LINK-001/002/003/006, all `WARNING`. Owns the skip lists (external / anchor / non-md / placeholder / directory / code-fence). |
| `issue.py` | `Severity` (str-Enum: error/warning/info) + frozen `Issue(severity, rule_id, field, message)`. `__str__` renders `ERROR[field] YAML-014: …`. Its own module to avoid a validator↔link_checker cycle. |
| `__init__.py` | Public surface: re-exports the parser, spec constants, `Issue`/`Severity`, `validate`/`is_valid`/`check_links`, and the building-block taxonomy. |
| `cli/format_check.py` | `tessellum format check <path>` — wires `validate` into the CLI, recurses directories over `*.md`, filters non-note files, emits human/JSON, computes exit code. |

### The `Note` dataclass (`parser.py:Note`)

`@dataclass(frozen=True)` with `path`, `frontmatter: dict`, `body: str`, and `raw_frontmatter: str`. Frozen = immutable/hashable; validation never mutates it. Convenience properties (`tags`, `para_bucket`, `second_category`, `building_block`, `status`, `folgezettel`, `folgezettel_parent`) coerce to `str`/`list[str]` and tolerate missing/mistyped fields (return `None`/`[]`). `folgezettel_parent` reads `folgezettel_parent` then falls back to `fz_parent`. Keeping `raw_frontmatter` is load-bearing: YAML-100/101 scan the *text* (line-numbered) because a parsed dict has already lost the `[[...]]`/`[](...)` syntax.

## 4. Rules, Invariants & Design Decisions (with WHY)

### 4.1 Required fields — 7, all ERROR

`_REQUIRED_FIELD_RULE_IDS` maps the 7 `REQUIRED_FIELDS` to rule IDs: `tags`→YAML-010, `keywords`→YAML-020, `topics`→YAML-030, `language`→YAML-040, `date of note`→YAML-050, `status`→YAML-060, `building_block`→YAML-062. Missing ⇒ ERROR. **Note `date of note` and `building_block` are the literal YAML keys** (space in the former).

### 4.2 `tags` — the PARA + second-category contract

`_check_tags`: must be a list (else YAML-011 ERROR); `len < MIN_TAGS_REQUIRED` (2) ⇒ YAML-012 ERROR ("PARA bucket + second category"); `tags[0] ∉ VALID_PARA_BUCKETS` ⇒ YAML-014 ERROR; each element non-string ⇒ YAML-013 ERROR; each element failing `TAG_FORMAT_REGEX` (`^[a-z0-9_]+$`) ⇒ YAML-015 ERROR. **Closed enum, 5 buckets:** `resource`, `area`, `project`, `archive`, `entry_point`. WHY the 2-tag minimum: `tags[1]` is the canonical *second category* — which is why `note_second_category` is forbidden (§4.6).

### 4.3 Soft minima — the only *frontmatter* warnings

`_check_list_min` for `keywords` (≥`MIN_KEYWORDS_RECOMMENDED`=3, YAML-021 type / YAML-022 count) and `topics` (≥`MIN_TOPICS_RECOMMENDED`=2, YAML-031 / YAML-032). Wrong type ⇒ ERROR; too-few ⇒ **WARNING** (recommended, not required). Both are itemized-list fields.

### 4.4 Closed-enum fields

`_check_enum` for `building_block` (YAML-063) and `status` (YAML-061): non-string ⇒ ERROR, value ∉ enum ⇒ ERROR. `VALID_STATUSES` has **21** values (`active`, `draft`, `archived`, `deprecated`, `superseded`, `stub`, `placeholder`, `template`, `wip`, `in_progress`, `production`, `proposal`, `development`, `planning`, `legacy`, `disabled`, `research`, `review`, `pending`, `completed`, `cancelled`). `VALID_BUILDING_BLOCKS` is **derived from `bb.BBType`** (8 types) — `frontmatter_spec.py` imports `VALID_BB_TYPE_VALUES` and aliases it, so BB enum drift can't desync the validator from the ontology. All enum checks **skip when the value is absent** (that's already covered by the required-field check — no double-report).

### 4.5 Date format

`_check_date`: value stringified, must match `DATE_FORMAT_REGEX` (`^\d{4}-\d{2}-\d{2}$`) ⇒ else YAML-051 ERROR. Absent ⇒ skipped (required-field check owns it).

### 4.6 TESS-001/002/003 — Tessellum-specific frontmatter rules

- **TESS-001 / TESS-002** (`_check_folgezettel_pair`): folgezettel is a *both-or-neither* pair. `folgezettel` set without a parent (`folgezettel_parent` or `fz_parent`) ⇒ TESS-001 ERROR; parent without `folgezettel` ⇒ TESS-002 ERROR. WHY: a positioned note with no parent (or vice-versa) can't be placed in a trail.
- **TESS-003** (`_check_forbidden`): any `FORBIDDEN_FIELDS` member present ⇒ ERROR. Currently only `note_second_category`, with a bespoke message: `tags[1]` is the single source of truth and the indexer reads the second category from it automatically — a duplicated field could disagree.

### 4.7 YAML-100/101 — no links inside YAML

`_check_yaml_links` scans `raw_frontmatter` **line by line** (offset starts at 2 to approximate real line numbers under the opening `---`). A `[[...]]` match ⇒ YAML-100 ERROR; a `[..](..)` match ⇒ YAML-101 ERROR. WHY it uses `raw_frontmatter` and not the parsed dict: link syntax must be caught as *text*; the parse discards it.

### 4.8 LINK-001/002/003/006 — body links, all WARNING

`link_checker.check_links` strips fenced code (`_FENCED_CODE_RE`), then per `[text](target)`:

| Rule | Condition | Severity |
|------|-----------|----------|
| LINK-001 | internal link missing `.md` extension | WARNING |
| LINK-002 | internal link uses an absolute path (`/…`) | WARNING |
| LINK-003 | internal `.md` target does not exist on disk (relative to `note.path.parent`) | WARNING |
| LINK-006 | note has **no** internal `.md` links (orphan) | WARNING |

**Every LINK-\* is WARNING, never ERROR** — a lint signal, not a gate; broken/orphan notes don't fail validation. **Skip lists** (never flagged): external (`^https?://`), `mailto:`/anchor (`#…`); non-md extensions (`_NON_MD_EXTS` — images, docs, code/data, config, LaTeX); directory links (trailing `/`); placeholder targets (`_PLACEHOLDER_TARGETS`: `-`, `link`, `path`, `url`, `ticket_link`, `source`, `target`, `...`, …); template-ish prefixes (`<`, `{`, `_no_`); and anything inside a code fence. LINK-003 only runs when `note.path` is set (string-parsed notes can't resolve on disk). **LINK-006 is exempted for `status: template`** — templates are scaffolds meant to be orphans until copied.

### 4.9 TESS-004 — counter_argument → argument (ERROR, BB-graph-aware)

`_check_counter_argument_link`. Fires only when `building_block == "counter_argument"` **and** `status == "active"` **and** `note.path` is set. It strips code fences, walks each body markdown link, resolves internal `.md` targets on disk, `parse_note`s them, and passes iff at least one target has `building_block: argument`. Otherwise ⇒ **TESS-004 ERROR**. WHY: a counter-argument must structurally name the argument it attacks so the typed dialectical edge is observable in the corpus, not just implied. Deliberate scope limits stated in code: it does **not** check that the target's FZ equals the counter's `folgezettel_parent` (the validator has no index; the stronger invariant is enforced by the indexer/DKS at write time — this is the static single-note backstop), and a malformed target is silently skipped (surfaced by LINK-003, not double-reported). **Authoring-state exemption:** any status other than `active` (`template`/`draft`/`stub`/`archived`) skips the rule.

### 4.10 TESS-005 — undeclared BB-pair body links (WARNING, version-aware)

`_check_bb_typed_edges`. Fires when the note's `building_block` is BB-typed **and** `status == "active"` **and** `note.path` is set. For each distinct internal `.md` target that is itself BB-typed, if the (source_bb → target_bb) pair is in **neither direction** of the BB schema, emit **TESS-005 WARNING**. Skips: same-BB links (sibling cross-references are silent-by-design in the schema), un-typed endpoints, unresolvable/unparseable targets, and dedups repeat targets. **Version-aware:** if the note records an integer `bb_schema_version ≥ 1`, it validates against `bb.types.BB_SCHEMA_AT_VERSION(n)` (frozen-at-creation) and tags the message `@v{n}`; otherwise it falls back to the live `BB_SCHEMA` (tagged `@live`). WHY WARNING not ERROR: the schema describes *epistemic transitions*, but legitimate documentation links (term lookups, skill pointers) exist beyond them — so TESS-005 surfaces candidates for retarget / accept / schema-extension rather than failing the note. The richer corpus-graph view is `tessellum bb audit`; TESS-005 is its single-note companion.

### 4.11 Severity model

`is_valid` gates on ERROR only. In practice the **only ERROR-producing body rule is TESS-004**; all LINK-\* and TESS-005 are WARNING. So a note with broken links or orphan status still `is_valid()`; a required-field/enum/format/forbidden/folgezettel violation, a link-in-YAML, or an active counter-argument with no argument link does not.

## 5. Public API / CLI

### Python API (`tessellum.format`)

- `validate(target: Path | str | Note) -> list[Issue]` — full report, fixed field order, empty = clean.
- `is_valid(target: Path | str | Note) -> bool` — no ERROR ⇒ True.
- `parse_note(path) -> Note`, `parse_text(text) -> Note`, `Note`, `FrontmatterParseError`.
- `check_links(note: Note) -> list[Issue]`.
- `Issue`, `Severity`.
- Spec constants: `VALID_PARA_BUCKETS`, `VALID_BUILDING_BLOCKS`, `VALID_STATUSES`, `REQUIRED_FIELDS`, `FORBIDDEN_FIELDS`, `MIN_TAGS_REQUIRED`, `MIN_KEYWORDS_RECOMMENDED`, `MIN_TOPICS_RECOMMENDED`, `DATE_FORMAT_REGEX`, `TAG_FORMAT_REGEX`.

### CLI (`cli/format_check.py`, registered in `cli/main.py`)

```
tessellum format check <path> [--strict] [--quiet|-q] [--format human|json]
```

`<path>` is a `.md` file or a directory. Directories `rglob("*.md")` and skip non-note files via `_is_note_file`: excludes `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `DEVELOPING.md`, `LICENSE.md`, `MEMORY.md`, and any `Rank_*` prefix. Human output lists per-file issues + a summary line (`validated N file(s); … errors, … warnings, … infos`); `--quiet` suppresses the summary when clean. JSON emits `{files: [{path, issues:[{rule_id, severity, field, message}]}], summary:{…}}`.

**Exit codes** (`_exit_code`): `0` = no errors (warnings/infos OK); `1` = ≥1 ERROR, **or** any WARNING under `--strict`; `2` = invocation error (path missing / not a `.md` file or dir). `--strict` promotes warnings to CI-failing without changing the `Issue` severities themselves.

`format check` is one of the shipped CLI commands; the subparser is added in `main.py` alongside `bb`, `capture`, `composer`, `dks`, `mcp`, `filter`, `fz`, `index`, `init`, `search`.

## 6. Extension Points

- **New frontmatter rule:** add a `_check_*` helper in `validator.py` and one `issues.extend(...)` line in `validate`. Keep the fixed field order (issues are reported in append order). Pick an ID in the documented range (`YAML-0xx` presence/type/value, `YAML-1xx` linkage, `TESS-0xx` Tessellum-specific).
- **New enum value / required field:** edit `frontmatter_spec.py` only (validator imports the constants). BB types are the exception — edit `bb.types.BBType`, and `VALID_BUILDING_BLOCKS` follows automatically.
- **New body-link rule:** extend `link_checker.py` (LINK-\*) or add a BB-graph-aware rule in `validator.py`. Reuse the skip-list / code-fence-strip / on-disk-resolve pattern from `check_links` and `_check_bb_typed_edges`.
- **New BB edge for TESS-004/005:** amend the schema in `bb.types` (`BB_SCHEMA_*` / `BB_SCHEMA_DKS_EXTENSIONS`, or land a `SchemaEditEvent`); TESS-005's version-aware path picks it up via `BB_SCHEMA_AT_VERSION`. No change to `validator.py` needed.
- **New output format:** add an `_emit_*` in `format_check.py` and branch in `run_format_check`; keep `_exit_code` as the single exit-code authority.
- **Non-note filename filters:** extend `_NON_NOTE_NAMES` / `_NON_NOTE_PREFIXES`.
