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

[Unreleased]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.3...HEAD
[0.0.3]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/TianpeiLuke/Tessellum/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/TianpeiLuke/Tessellum/releases/tag/v0.0.1
