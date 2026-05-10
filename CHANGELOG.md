# Changelog

All notable changes to Tessellum are documented here. The format is loosely [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v0.1.0 — Public Beta

- Engine port from parent project (composer + retrieval primitives)
- 20 essential skills (capture / search / answer / trail management / maintenance)
- 8 BB-type example notes (one per Building Block)
- Conceptual primer term notes (Z + PARA + BB + Epistemic Function + DKS + CQRS)
- Public-facing how-to library (getting-started, note-format, agent-integration, growing a trail)
- MCP server exposing v0.1 skills as tools
- CI workflow (ruff + pytest + format/link validators)
- `tessellum init` / `capture` / `format check` / `search` CLI subcommands
- Hatch `force-include` wiring so `vault/resources/templates/` ships in the wheel

## [0.0.7] — 2026-05-10

### Added — Templates ship in the wheel via `force-include`

Step 3 of `plans/plan_v01_src_tessellum_layout.md`. `pip install tessellum` users now get the 13 canonical BB-type templates without cloning the repo. Prerequisite for upcoming `tessellum init` and `tessellum capture <bb>` CLI subcommands.

#### `pyproject.toml` — `[tool.hatch.build.targets.wheel.force-include]`

```toml
[tool.hatch.build.targets.wheel.force-include]
"vault/resources/templates" = "src/tessellum/data/templates"
```

Hatch grafts files from `vault/resources/templates/` into the wheel at `tessellum/data/templates/` at build time. **Single source of truth in the dogfooded vault**; automatic inclusion in the wheel; no two-copy drift.

#### `tessellum.data.templates_dir()`

New module at `src/tessellum/data/__init__.py` exposing one helper:

```python
from tessellum.data import templates_dir
path = templates_dir()  # -> Path to the templates directory
```

The helper handles **both install modes**:

- **Wheel install**: returns `<site-packages>/tessellum/data/templates/` (where `force-include` grafted them).
- **Editable install** (`pip install -e .`): `force-include` doesn't run for editable installs, so the helper falls back to `<repo>/vault/resources/templates/` via `Path(__file__).resolve().parents[3]`. Same import works in both modes; no caller-side branching.

Raises `FileNotFoundError` if neither location exists (broken install or misconfigured `force-include`).

#### Tests

`tests/smoke/test_data_loader.py` (new, 16 tests):

- `templates_dir()` returns an existing directory
- The directory contains ≥ 13 `template_*.md` files
- Each of the 13 expected templates is present (parametrized)
- Every template starts with YAML frontmatter

All 16 pass in editable mode (the test environment).

#### Wheel-install verification

Build + clean-venv install + import smoke check:

```bash
$ python -m build --wheel
$ unzip -l dist/tessellum-0.0.7-py3-none-any.whl | grep templates
  tessellum/data/templates/README.md
  tessellum/data/templates/template_yaml_header.md
  tessellum/data/templates/template_concept.md
  ...  (13 templates total + README + __init__.py)

$ pip install dist/tessellum-0.0.7-py3-none-any.whl
$ python -c "from tessellum.data import templates_dir; print(templates_dir())"
  /tmp/.../site-packages/tessellum/data/templates
```

#### Out of scope (deferred to future commits)

- **Seed vault** for `tessellum init` (full directory skeleton, not just templates) — bigger scope, ships when `init` does.
- **Skills `force-include`** (so `vault/resources/skills/` is grafted too) — only needed when a CLI subcommand reads skill canonicals at runtime.
- **JSON schemas** under `tessellum.data.schemas/` — when the composer ships and needs schema-validated pipeline configs.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.7"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.7"`.
- All 69 tests pass (53 prior + 16 new in `test_data_loader.py`).

## [0.0.6] — 2026-05-10

### Changed — `scripts/` role clarified (docs-only)

Refined the convention for the top-level `scripts/` directory: **reserved for one-off operational utilities** (vault migrations, repo maintenance, contributor helpers) — *not* core capabilities. Recurring capabilities belong as CLI subcommands under `src/tessellum/cli/`, where they ship in the wheel and are invoked via `tessellum <subcommand>`.

Surfaced when reviewing what to port from the parent project's 60+ scripts: most are now-or-soon CLI subcommands (format check, indexer, retrieval, capture), library modules (config, parser), or already-ported skill canonicals. Only true one-offs (one-time migrations, contributor convenience) belong in `scripts/`.

The decision rule:

| Question | Destination |
|---|---|
| Recurring capability users run via the `tessellum` command? | `src/tessellum/cli/<subcommand>.py` |
| Re-usable library function? | `src/tessellum/<module>/` |
| One-off migration / repo maintenance / contributor helper? | top-level `scripts/` |

**Files updated**:

- `scripts/README.md` (new) — documents the convention with examples in both directions and the decision rule.
- `DEVELOPING.md § Layout Convention` — refined the `scripts/` row from "build / update / format utilities" to "one-off operational utilities, not shipped"; expanded the decision rule into 6 explicit cases.
- `plans/plan_cqrs_repo_layout.md` — refined the `scripts/` row in the System × lifecycle matrix; added a new subsection "scripts/ vs src/tessellum/cli/" calling out the subtlety.

This is a docs-only release. No code changes; library + CLI behavior unchanged. 53/53 tests still pass.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.6"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.6"`.

## [0.0.5] — 2026-05-10

### Changed — Repository layout (CQRS workflow → folder mapping)

Promoted `plans/` to a top-level directory and added `runs/` for runtime traces. Each top-level folder now maps to a defined CQRS role: System P (capture), System D (retrieval), governance (meta to both), or runtime forensics. See [`plans/plan_cqrs_repo_layout.md`](plans/plan_cqrs_repo_layout.md) for the full framing.

**New top-level folders**:

- `plans/` — project-management plan notes (committed). Status tracked via YAML `status:` field, not folder layout. Includes `plan_v01_src_tessellum_layout.md` and `plan_cqrs_repo_layout.md` (moved from `inbox/plans/`) plus a README explaining the convention.
- `runs/` — session-scoped runtime traces (gitignored except for `README.md` and `.gitkeep` files). Three subdirectories: `capture/`, `retrieval/`, `composer/`. Filename convention: `<YYYY-MM-DDThh-mm-ss>_<task>.<ext>`.

**Other layout changes**:

- `inbox/plans/` removed — plans no longer claim to be System P input.
- `.gitignore` — `runs/**` ignored except `runs/`, `runs/README.md`, `runs/*/`, `runs/*/.gitkeep`.
- `pyproject.toml` `[tool.hatch.build.targets.sdist]` — `plans` added to `include`; `runs` added to `exclude`.
- `README.md § Project Structure` — rewritten directory tree with the new top-level folders.
- `DEVELOPING.md § Layout Convention` — table now has a System role column; added rows for `plans/` and `runs/`; CQRS framing paragraph; updated decision rule.
- `vault/0_entry_points/entry_master_toc.md` — new "Project State (Outside the Vault)" section listing active plans and pointing at `runs/`.

### Fixed — link_checker config-extension skip list

`tessellum.format.link_checker._NON_MD_EXTS` now exempts common config-file formats: `.toml`, `.cfg`, `.ini`, `.lock`, `.env`. Surfaced during the layout migration when `[pyproject.toml](../pyproject.toml)` in `plan_v01_src_tessellum_layout.md` tripped LINK-001 — `.toml` is a legitimate link target, not a missing-extension defect. Added a parametrized test case covering all five new extensions.

### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.5"`; status updated.
- `pyproject.toml`: `project.version` → `"0.0.5"`.

### Validation

- `tessellum format check plans/`: 2 files, 0 errors, **0 warnings** (was 1 warning pre-fix).
- `tessellum format check vault/`: 71 files, 0 errors, 613 warnings (no regression).
- `pytest tests/`: **53/53 passing** (52 pre-fix + 1 new test for config extensions).

## [0.0.4] — 2026-05-10

### Added — Tier-1 parity with the parent project's format checker

Studied the parent project's `scripts/check_note_format.py` + `skill_slipbox_check_note_format.md` and ported the high-leverage features. Brings Tessellum's checker close to feature-parity for the YAML-frontmatter + body-link surface; H1/H2 section rules and the vault summary report are deferred to a later release.

#### Stable rule IDs on every issue

`Issue` now carries a `rule_id: str` field. IDs follow three families:

- `YAML-NNN` — frontmatter rules (010–099 for presence/type/value, 100–199 for linkage).
- `LINK-NNN` — body markdown link rules.
- `TESS-NNN` — Tessellum-specific rules (folgezettel pair, forbidden fields).

Existing rules are mapped to the parent's IDs where the parent has one (`YAML-010`, `YAML-014`, etc.), so logs and grep patterns are portable. Output format updated to `SEVERITY[field] RULE-ID: message`.

#### `Severity.INFO` (third tier)

Added `Severity.INFO` alongside `ERROR` and `WARNING`. No rule emits INFO yet, but the type is now available for downstream rules that want a "soft suggestion" tier (the parent uses INFO for H1/H2 hints and for orphan-related findings).

#### YAML-100/101 — forbid links inside YAML field values

Wiki links (`[[...]]`) and markdown links (`[text](path.md)`) inside YAML field values silently break the parent project's indexer. Now flagged as ERROR with the line number where they appear. Detection uses the raw frontmatter text (preserved on `Note.raw_frontmatter`), not the parsed dict.

#### LINK-001/002/003/006 — body markdown link checks

New module `tessellum.format.link_checker`:

- **LINK-001** (WARNING) — internal link missing `.md` extension
- **LINK-002** (WARNING) — internal link uses an absolute path (prefer relative)
- **LINK-003** (WARNING) — internal link target does not exist on disk
- **LINK-006** (WARNING) — note has no internal links to other notes (orphan)

Skipped (not flagged): external `http(s)://` and `mailto:` links, anchor-only `#section` links, non-markdown extensions (images, PDFs, code, archives), placeholder targets (`<placeholder>`, `link`, `...`, `-`, etc.), directory links, and any link inside a fenced code block.

`Note.raw_frontmatter: str = ""` is the new required field on the dataclass — populated by `parse_text` / `parse_note` from the regex match.

#### `Note.raw_frontmatter` + parser refactor

Dropped runtime use of `python-frontmatter`; the parser now uses PyYAML directly with a regex to capture both the parsed dict and the raw YAML text. `python-frontmatter>=1.1` removed from runtime dependencies.

#### `--format json` output

`tessellum format check --format json` emits a machine-readable report:

```json
{
  "files": [
    {
      "path": "vault/resources/term_dictionary/term_zettelkasten.md",
      "issues": [
        {"rule_id": "LINK-006", "severity": "warning", "field": "links",
         "message": "note has no internal links to other notes (orphan)"}
      ]
    }
  ],
  "summary": {
    "files_checked": 70, "files_with_issues": 64,
    "errors": 0, "warnings": 613, "infos": 0
  }
}
```

Designed so a CI step can pipe it into `jq` and gate on `summary.errors`.

#### Non-note skip list

The CLI's directory recursion now skips `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `DEVELOPING.md`, `LICENSE.md`, `MEMORY.md`, and any `Rank_*.md`. The parent project skips these because they're not vault notes (no required frontmatter). Library-level `validate(path)` is unchanged — the skip list only applies to CLI directory mode.

#### Tests

20 new tests across 2 files:

- `tests/smoke/test_link_checker.py` (13 tests) — every LINK-* rule, plus negative tests for external/anchor/non-md/placeholder/directory targets and code-block-fenced links.
- `tests/smoke/test_format_validator.py` (7 new tests on top of the existing 16) — rule IDs are well-formed, `Severity.INFO` exists, YAML-100/101 fire on link-in-YAML, plus updated `test_issue_str_*` for the new ctor signature.
- `tests/cli/test_format_check.py` (3 new tests on top of the existing 9) — `--format json` clean + dirty paths, non-note skip list.

All 52 tests pass.

#### Dogfood (separate from this commit)

Running v0.0.4 over `vault/` surfaces **0 errors and 613 warnings**: many LINK-003 (links to planned-but-not-yet-authored notes like `term_folgezettel.md`) and LINK-006 (orphan term notes). These are real findings — the vault is in early build-out — and will be addressed in follow-up data work, not by silencing the checker.

#### Bumped

- `src/tessellum/__about__.py`: `__version__` → `"0.0.4"`; status line updated.
- `pyproject.toml`: `project.version` → `"0.0.4"`; `python-frontmatter` removed from runtime deps.

#### Breaking change

`Issue` ctor signature is now `Issue(severity, rule_id, field, message)` (4 positional args). v0.0.2/v0.0.3 used 3 positional args. Library callers constructing `Issue` directly need to add a `rule_id` argument; `validate()` consumers are unaffected.

## [0.0.3] — 2026-05-10

### Added — `tessellum format check` CLI subcommand

The validator shipped in 0.0.2 is now reachable from the shell:

```bash
tessellum format check path/to/note.md     # single file
tessellum format check vault/              # recurse over *.md
tessellum format check vault/ --strict     # treat warnings as errors
tessellum format check vault/ --quiet      # suppress summary when clean
```

Exit codes:

- **0** — no errors (warnings allowed unless `--strict`)
- **1** — at least one ERROR-severity issue (or any WARNING under `--strict`)
- **2** — invocation error (path doesn't exist, not a `.md` file or directory)

Per-file output prints the relative path (anchored at the directory if recursing, otherwise at the file's parent), then one line per issue with severity + field locator + message. A trailing summary reports total files validated, files with issues, and error/warning counts.

The dispatcher in `tessellum.cli.main` now uses argparse subparsers; sibling subcommand modules (`tessellum.cli.format_check`) expose `add_subparser(subparsers)` for wiring. Bare `tessellum` still prints the version + capability banner and now lists `format check` under "Available now (CLI)".

9 smoke tests under `tests/cli/test_format_check.py`: clean file → 0, dirty file → 1, directory recursion, warnings-only → 0, `--strict` promotes warnings to failure, missing path → 2, `--quiet` suppresses summary, bare command prints banner, `--version` exits cleanly.

Bumped:
- `src/tessellum/__about__.py`: `__version__` → `"0.0.3"`; `__status__` updated
- `pyproject.toml`: `project.version` → `"0.0.3"`

Smoke-tested end-to-end in .venv: `tessellum format check vault/` validates all 71 vault notes clean (0 errors, 0 warnings).

## [0.0.2] — 2026-05-10

### Added — Format Library (parser + validator + closed-enum spec)

The typed substrate is now usable as a library: pip users can `from tessellum import validate` to lint their own notes against the spec.

- `tessellum.format.frontmatter_spec` — closed enums as Python data: `VALID_PARA_BUCKETS` (5), `VALID_BUILDING_BLOCKS` (8), `VALID_STATUSES` (21), `REQUIRED_FIELDS` (7), soft minima for tags/keywords/topics, `FORBIDDEN_FIELDS` (`note_second_category`)
- `tessellum.format.parser` — `Note` dataclass with convenience accessors (`tags`, `para_bucket`, `second_category`, `building_block`, `status`, `folgezettel`, `folgezettel_parent`); `parse_note(path)` and `parse_text(str)` entry points; `FrontmatterParseError` for unparseable frontmatter
- `tessellum.format.validator` — `validate(target) -> list[Issue]` and `is_valid(target) -> bool`; checks all 7 required fields, the 3 closed enums, the `YYYY-MM-DD` date format, lowercase-underscore tag format, the both-or-neither rule for `folgezettel:` / `folgezettel_parent:` (incl. legacy `fz_parent` alias), and the `note_second_category` forbidden-field rule
- `tessellum.Issue` and `tessellum.Severity` re-exported at top level for ergonomics
- 23 smoke tests under `tests/smoke/test_format_validator.py` cover every error path + warning path + the 8 BB enum values
- `__about__.py` bumped to `0.0.2`; the CLI banner now points users at `validate` / `parse_note` / `is_valid`

### Caught in dogfooding (separate commit)

The new validator immediately caught 2 real spec violations + 1 corrupted file in this repo's own `vault/`. Those are fixed in a follow-up data commit, demonstrating the library works on real content.

## [0.0.1] — 2026-05-09

### Added — Namespace Reservation

- Repository skeleton with target layout (no `src/` dumping ground; clean separation of code / vault / inbox / data / experiments / scripts / tests)
- `pyproject.toml` declaring the `tessellum` PyPI package with dependencies for the v0.1 engine port
- Top-level `src/tessellum/__init__.py` documenting the six-pillar thesis
- `src/tessellum/format/building_blocks.py` — typed Python registry of the 8 BB types, 4 epistemic layers, and 10 directed edges; the load-bearing primitive of the typed substrate
- `vault/0_entry_points/entry_master_toc.md` — Master TOC entry for the dogfooded vault
- `vault/resources/term_dictionary/term_building_block.md` — first conceptual primer term note
- README + LICENSE (MIT) + CONTRIBUTING + DEVELOPING + this CHANGELOG
- `.gitignore` for derived artifacts (`data/`, `experiments/`, build outputs)

### Architecture decision

Tessellum dogfoods itself: the project's public documentation lives in `vault/` as typed atomic notes, not in a separate `docs/` directory. See [DEVELOPING.md § Layout Convention](DEVELOPING.md#layout-convention).

[Unreleased]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.7...HEAD
[0.0.7]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/TianpeiLuke/Tessellum/releases/tag/v0.0.1
