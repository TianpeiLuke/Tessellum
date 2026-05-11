---
tags:
  - resource
  - skill
  - procedure
  - vault_maintenance
  - format_validation
keywords:
  - check note format
  - tessellum format check
  - YAML frontmatter validation
  - link validation
  - in-vault skill canonical
topics:
  - Skill Procedures
  - Vault Tools
  - Note Format
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
related_skill_headers: []
pipeline_metadata: none
---

# Procedure: tessellum-format-check (Canonical Body)

This is the **canonical body** for the `tessellum-format-check` skill. Per-runtime thin-headers (`.kiro/skills/...`, etc.) can be wired later as needed; this file is the single source of truth for the procedure. Modeled on the parent project's `skill_slipbox_check_note_format.md`, adapted for Tessellum's typed-package API.

## Skill description <!-- :: section_id = skill_description :: -->

Validate vault notes against Tessellum's YAML frontmatter spec + body markdown link conventions. Backed by the [`tessellum.format` library](../../../src/tessellum/format/) and the `tessellum format check` CLI subcommand. Runs structural validation only — required fields, closed enums, soft minima, FZ-pair rule, forbidden fields, raw-YAML link prohibition, and four body-link rules. No semantic / DB-backed analysis (Tessellum has no indexer yet — that's v0.1).

## Setup <!-- :: section_id = setup :: -->

```bash
# Activate the project venv (Tessellum dogfoods itself, so pip install -e . is enough)
source .venv/bin/activate

# Verify the CLI is wired
tessellum --version
# → tessellum 0.0.4
```

No DB resolution needed — the validator is pure file I/O.

## Resources <!-- :: section_id = resources :: -->

- **CLI subcommand**: `tessellum format check <path> [--strict] [--quiet] [--format {human,json}]`
- **Library API**: [`tessellum.format`](../../../src/tessellum/format/) — `validate(path) -> list[Issue]`, `is_valid(path) -> bool`, `parse_note(path) -> Note`
- **Spec reference**: [DEVELOPING.md § YAML Frontmatter Specification](../../../DEVELOPING.md)
- **Templates** (executable spec exemplars): [`vault/resources/templates/`](../templates/)
- **Building Block ontology**: [term_building_block](../term_dictionary/term_building_block.md)

## Validation Rules Reference <!-- :: section_id = validation_rules_reference :: -->

Each finding carries a stable `rule_id` and a `severity` (ERROR / WARNING / INFO). IDs follow three families: `YAML-NNN` (frontmatter), `LINK-NNN` (body links), `TESS-NNN` (Tessellum-specific).

### Error rules <!-- :: section_id = error_rules :: -->

| Rule | Severity | Check |
|---|---|---|
| YAML-010 | ERROR | `tags` field is missing |
| YAML-011 | ERROR | `tags` is not a YAML list |
| YAML-012 | ERROR | `tags` has fewer than 2 entries |
| YAML-013 | ERROR | A tag value is not a string (wrap year-numbers in quotes) |
| YAML-014 | ERROR | `tags[0]` is not a valid PARA bucket |
| YAML-015 | ERROR | A tag is not lowercase letters/digits/underscores |
| YAML-020 | ERROR | `keywords` field is missing |
| YAML-021 | ERROR | `keywords` is not a YAML list |
| YAML-030 | ERROR | `topics` field is missing |
| YAML-031 | ERROR | `topics` is not a YAML list |
| YAML-040 | ERROR | `language` field is missing |
| YAML-050 | ERROR | `date of note` field is missing |
| YAML-051 | ERROR | `date of note` does not match `YYYY-MM-DD` |
| YAML-060 | ERROR | `status` field is missing |
| YAML-061 | ERROR | `status` is not in the valid status enum (21 values) |
| YAML-062 | ERROR | `building_block` field is missing |
| YAML-063 | ERROR | `building_block` is not in the valid BB enum (8 values) |
| YAML-100 | ERROR | Wiki link `[[...]]` inside a YAML field value |
| YAML-101 | ERROR | Markdown link of the form `[<text>](<path>.md)` inside a YAML field value |
| TESS-001 | ERROR | `folgezettel:` is set but `folgezettel_parent:` is missing |
| TESS-002 | ERROR | `folgezettel_parent:` is set but `folgezettel:` is missing |
| TESS-003 | ERROR | Forbidden field present (e.g. `note_second_category`) |

### Warning rules <!-- :: section_id = warning_rules :: -->

| Rule | Severity | Check |
|---|---|---|
| YAML-022 | WARNING | `keywords` has fewer than 3 entries (recommended) |
| YAML-032 | WARNING | `topics` has fewer than 2 entries (recommended) |
| LINK-001 | WARNING | Internal link target is missing the `.md` extension |
| LINK-002 | WARNING | Internal link uses an absolute path; prefer relative |
| LINK-003 | WARNING | Internal link target does not exist on disk |
| LINK-006 | WARNING | Note has no internal markdown links to other notes (orphan). Skipped when `status: template` (templates are orphans by design). |

### Skipped during link checks <!-- :: section_id = skipped_link_targets :: -->

The link checker ignores: external `http(s)://` and `mailto:` links, anchor-only `#section` links, non-markdown extensions (`.png`, `.pdf`, `.py`, ...), placeholder/template targets (`<placeholder>`, `link`, `path`, `...`, `-`), directory targets ending in `/`, and any link inside a fenced code block.

## When to use <!-- :: section_id = when_to_use :: -->

- **After authoring a note** — verify a single file: `tessellum format check vault/<path>.md`.
- **Before committing** — run on the full vault: `tessellum format check vault/`.
- **In CI** — gate on errors with `--format json` piped to `jq`. Example: `tessellum format check vault/ --format json | jq -e '.summary.errors == 0'`.
- **Strict gating** — promote warnings to errors with `--strict` (use sparingly; orphan and broken-link warnings are common in early-build vaults).

## When NOT to use <!-- :: section_id = when_not_to_use :: -->

- **For semantic-quality assessment** — this is structural only. No DB-backed missing-link detection, no relevance scoring, no atomicity check.
- **For broken-link repair** — LINK-003 *reports* broken links; it doesn't fix them.
- **For H1/H2 section validation** — not yet implemented (deferred from parent's checker; Tessellum hasn't codified per-BB-type section rules).
- **Inside a code block in another note** — links inside fenced code are intentionally ignored to avoid false positives on code examples.

## Step 1: pick the invocation mode <!-- :: section_id = step_1_pick_mode :: -->

| Input | Mode |
|---|---|
| `tessellum format check <file.md>` | Single file |
| `tessellum format check <directory>` | Recurse over `*.md` (skips `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `DEVELOPING.md`, `LICENSE.md`, `MEMORY.md`, `Rank_*.md`) |
| Add `--strict` | Treat WARNINGs as ERRORs (exit 1 on any warning) |
| Add `--quiet` | Suppress the trailing summary when nothing fails |
| Add `--format json` | Emit machine-readable JSON for piping into `jq` |

## Step 2: run the check <!-- :: section_id = step_2_run_the_check :: -->

```bash
# Single note
tessellum format check vault/resources/term_dictionary/term_building_block.md

# Full vault, human-readable
tessellum format check vault/

# Full vault, JSON
tessellum format check vault/ --format json | jq '.summary'

# Full vault, strict — gate every warning
tessellum format check vault/ --strict

# Library equivalent (Python)
python -c "from tessellum.format import validate; print(validate('vault/<path>.md'))"
```

Exit codes:

- **0** — no errors (warnings + infos allowed unless `--strict`)
- **1** — at least one ERROR (or any WARNING under `--strict`)
- **2** — invocation error (path doesn't exist, not a `.md` file or directory)

## Step 3: parse the output <!-- :: section_id = step_3_parse_the_output :: -->

### Human format (default) <!-- :: section_id = human_format :: -->

```
vault/resources/term_dictionary/term_foo.md:
  ERROR[building_block] YAML-063: 'idea' is not a valid building_block; ...
  WARNING[links] LINK-003: link target 'term_bar.md' does not exist
  WARNING[links] LINK-006: note has no internal links to other notes (orphan)

validated 1 file(s); 1 with issues; 1 error(s), 2 warning(s), 0 info(s)
```

### JSON format (`--format json`) <!-- :: section_id = json_format :: -->

```json
{
  "files": [
    {
      "path": "resources/term_dictionary/term_foo.md",
      "issues": [
        {"rule_id": "YAML-063", "severity": "error", "field": "building_block",
         "message": "'idea' is not a valid building_block; ..."},
        {"rule_id": "LINK-006", "severity": "warning", "field": "links",
         "message": "note has no internal links to other notes (orphan)"}
      ]
    }
  ],
  "summary": {
    "files_checked": 1, "files_with_issues": 1,
    "errors": 1, "warnings": 1, "infos": 0
  }
}
```

## Step 4: triage and fix <!-- :: section_id = step_4_triage_and_fix :: -->

Fix in this priority order:

1. **YAML-010..099** — required-field + enum errors. The note is currently invisible to any structured tooling. Highest priority.
2. **YAML-100/101** — links-in-YAML. These silently break parsers downstream. Strip wiki/markdown link syntax from YAML field values; use plain strings.
3. **TESS-001/002** — folgezettel pair. Add the missing field, or remove both. Both-or-neither — see [DEVELOPING.md § Folgezettel-trail notes](../../../DEVELOPING.md).
4. **TESS-003** — forbidden field. Currently only `note_second_category` triggers this; remove it (the indexer reads `tags[1]` as the source of truth).
5. **LINK-003** — broken links. Either author the missing target, change the link, or mark the target as a `placeholder`-status note.
6. **LINK-001/002** — link-format hygiene. Add `.md`, prefer relative.
7. **LINK-006** — orphan notes. Add at least one outgoing link to a related note. Common in early-build vaults; not always a true defect.

## Cross-references <!-- :: section_id = cross_references :: -->

No other Tessellum skills exist yet. Future skills that will pair with this one (planned for v0.1):

- `tessellum-init` — scaffold a new vault from the seed
- `tessellum-capture-<bb>` — copy a BB-typed template and fill from input
- `tessellum-fix-broken-links` — remediate LINK-003 issues found by this skill

## Error handling <!-- :: section_id = error_handling :: -->

| Error | Cause | Recovery |
|---|---|---|
| `path does not exist` (exit 2) | Bad path argument | Verify path; tessellum format check accepts files or directories |
| `is neither a markdown file nor a directory` (exit 2) | Path is e.g. a `.txt` file | Pass a `.md` file or a directory containing `*.md` |
| `YAML parse error: …` (FrontmatterParseError raised) | Malformed frontmatter (broken YAML, doubled `---`) | Fix the frontmatter manually; then re-run |
| `frontmatter is not a YAML mapping` | Top-level YAML is a list/scalar | Frontmatter must be a YAML dict |
| All 7 required fields missing | Note has no frontmatter at all | If it's not a real note, add it to the CLI's skip list (or rename to `README.md` etc.); otherwise add the frontmatter |

## Related entry points <!-- :: section_id = related_entry_points :: -->

- [Master TOC](../../0_entry_points/entry_master_toc.md) — vault navigation
- [DEVELOPING.md § YAML Frontmatter Specification](../../../DEVELOPING.md) — the spec this checker enforces
- [Templates directory](../templates/) — copy-and-fill skeletons that all validate clean
- [CHANGELOG.md](../../../CHANGELOG.md) — per-release changes to the rule set
