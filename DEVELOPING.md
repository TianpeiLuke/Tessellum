# Developing Tessellum

Developer-facing guide for working on Tessellum itself (not for users of Tessellum). For user docs, browse `vault/0_entry_points/entry_master_toc.md`.

## Layout Convention

Tessellum **dogfoods itself** — its public documentation lives in `vault/` as typed atomic notes following the same Building Block format the system asks of users. There is no separate `docs/` directory.

| Artifact | Location | Reason |
|---|---|---|
| `import`-able Python | `src/tessellum/` | PEP src-layout — installed package surface |
| Knowledge content (incl. Tessellum's own docs) | `vault/` | Single SoT for typed knowledge; self-applied retrieval |
| Skill canonical bodies | `vault/resources/skills/` | In-vault skill SoT pattern (FZ 12) |
| Skill thin-headers | `.claude/skills/`, `.kiro/skills/` | Per-ecosystem entry; both point at the canonical body |
| User input (PDFs, papers, plans) | `inbox/` | User-facing drop zone |
| Generated DBs / indexes | `data/` | Regenerable; gitignored |
| Experiment outputs | `experiments/` | Per-run subdirs |
| Operational scripts | `scripts/` | Build / update / format utilities |
| Tests | `tests/` | Mirrors `src/tessellum/` structure |
| Repo-meta files | repo root | `README.md`, `CHANGELOG.md`, `LICENSE`, `CONTRIBUTING.md`, `DEVELOPING.md`, `pyproject.toml`, `.gitignore`, `.github/` |

**Decision rule for new files**: if it would be useful to *anyone using Tessellum*, it goes in `vault/` as a typed atomic note. If it's only useful to *people working on Tessellum's code*, it goes at repo root or in `scripts/`.

## Why dogfooding?

Three reasons:

1. **Self-applied retrieval** — `tessellum search "BB ontology"` finds the public-facing explanation. Users can grep the system's own docs from day one.
2. **Format conformance** — Tessellum's own documentation has to follow the format Tessellum demands of its users. If we can't make our docs fit, we're asking users to do something we won't do ourselves.
3. **Demonstrates the system on itself** — a new user opens the repo, browses `vault/`, and sees a working example of the system documenting itself. That's the strongest README possible.

This decision is documented in [`vault/resources/analysis_thoughts/thought_dogfooding_decision.md`](vault/resources/analysis_thoughts/thought_dogfooding_decision.md) (planned for v0.1).

## Path Resolution

All paths flow through `scripts/config.py` (single SoT). The constants:

```python
REPO_ROOT      = Path(__file__).resolve().parent.parent
PACKAGE_DIR    = REPO_ROOT / "src" / "tessellum"
VAULT_PATH     = REPO_ROOT / "vault"
INBOX_PATH     = REPO_ROOT / "inbox"
DATA_PATH      = REPO_ROOT / "data"
DB_PATH        = DATA_PATH / "databases" / "tessellum_unified.db"
EXPERIMENTS_PATH = REPO_ROOT / "experiments"
```

Skills and scripts MUST import from `config.py`. Never hardcode a path.

## Dev Setup

```bash
# Clone
git clone https://github.com/TianpeiLuke/Tessellum.git
cd Tessellum

# Install in editable mode with dev extras
pip install -e ".[dev]"

# Run the test suite
pytest

# Lint + format
ruff check src/
ruff format src/

# Type check (gradual; not strict)
mypy src/tessellum/
```

## Adding a Skill

Skills live in **three** files (the in-vault SoT pattern):

1. **Canonical body**: `vault/resources/skills/skill_<name>.md` — the actual procedure (YAML frontmatter + steps + format spec)
2. **Claude thin-header**: `.claude/skills/<name>/SKILL.md` — short pointer to the canonical body
3. **Kiro thin-header**: `.kiro/skills/<name>/SKILL.md` — same pattern
4. **Pipeline sidecar** (optional): `vault/resources/skills/skill_<name>.pipeline.yaml` — only if the skill has typed-contract steps

## YAML Frontmatter Specification

Tessellum notes follow a strict YAML frontmatter convention. Every typed atomic note ("tessellum") has **7 required fields** plus optional type-specific fields.

### Required fields

```yaml
---
tags:                          # ≥ 2 items required, list format
  - <para-bucket>              # tags[0]: closed PARA enum (see below)
  - <second-category>          # tags[1]: open routing label (terminology, skill, how_to, code, papers, analysis, digest, faq, code_repo, ...)
  - <topic-tag-1>              # tags[2..]: free-form topic tags, lowercase+underscore
  - <topic-tag-2>
keywords:                      # ≥ 3 items recommended, list format
  - <key-term-1>
  - <key-term-2>
  - <key-term-3>
topics:                        # ≥ 2 items recommended, list format
  - <topic-1>
  - <topic-2>
language: markdown             # one of: markdown, python, yaml, json, sql, bash, ...
date of note: YYYY-MM-DD       # NOTE: the key has spaces — "date of note", not "date_of_note"
status: <status-value>         # closed enum (see below)
building_block: <bb-type>      # closed 8-element enum (see below)
---
```

### Closed enums (must match exactly)

| Field | Allowed values |
|---|---|
| **`tags[0]`** (PARA bucket) | `resource` · `area` · `project` · `archive` · `entry_point` |
| **`building_block`** | `concept` · `procedure` · `model` · `argument` · `counter_argument` · `hypothesis` · `empirical_observation` · `navigation` |
| **`status`** | `active` · `draft` · `archived` · `deprecated` · `superseded` · `stub` · `placeholder` · `template` · `wip` · `in_progress` · `production` · `proposal` · `development` · `planning` · `legacy` · `disabled` · `research` · `review` · `pending` · `completed` · `cancelled` |

### Open vocabularies

| Field | Examples (extend as needed) |
|---|---|
| **`tags[1]`** (second category / routing label) | `terminology`, `skill`, `how_to`, `analysis`, `code`, `digest`, `faq`, `papers`, `code_repo`, `tool`, `team`, `model`, `intent`, `sop`, `navigation`, `metric`, `schema`, `experiment`, `lit`, `paper_section`, ... |
| **`tags[2..]`** | Free-form topic tags. Lowercase, underscore-separated. |
| **`language`** | Almost always `markdown`. Use `python` / `yaml` / `sql` for notes that primarily contain code. |
| **`keywords` / `topics`** | Free-form. `keywords` are searchable terms; `topics` are coarser themes. |

### Optional common fields

```yaml
last_updated: YYYY-MM-DD       # if the note has been revised since `date of note`
author: <handle>               # optional, for attribution
related_wiki: null             # external reference URL or null (kept for parent-vault compat; usually null in Tessellum)
```

### Optional type-specific fields

#### Folgezettel-trail notes (under `vault/resources/analysis_thoughts/` — and sometimes elsewhere)

```yaml
folgezettel: "14d1d"           # the FZ ID — string, can include letters/digits/sub-letters
folgezettel_parent: "14d1"     # parent FZ ID, or null for trail roots
```

The canonical field name is `folgezettel_parent:` (long form). The shorter `fz_parent:` is accepted as an alias for backwards compatibility with some legacy notes, but `folgezettel_parent:` is preferred and used in all Tessellum templates.

| Note type | FZ usage |
|---|---|
| Trail root (top of a trail) | `folgezettel: "<root-id>"`, `folgezettel_parent: null` |
| Trail child (most cases) | `folgezettel: "<id>"`, `folgezettel_parent: "<parent-id>"` |
| Non-trail note (most term/how-to/skill notes) | omit both FZ fields entirely |
| Trail member outside `analysis_thoughts/` (e.g., archived experiment) | both FZ fields, with `tags[0]` reflecting the actual PARA bucket |

#### Skill canonical bodies (under `vault/resources/skills/`)

```yaml
related_skill_headers:
  - .claude/skills/<name>/SKILL.md
  - .kiro/skills/<name>/SKILL.md
pipeline_metadata: ./skill_<name>.pipeline.yaml   # or "none"
```

#### Literature notes (under `vault/resources/papers/lit_*.md`)

```yaml
paper_title: "Full Paper Title"
authors:
  - "Last, First"
  - "Last, First"
year: "2026"                   # quote the year — YAML treats unquoted 2026 as integer
paper_notes: <paper_id>
```

#### Paper section notes (`paper_*` under papers/)

```yaml
paper_id: <id>
section_type: <abstract|intro|method|...>
```

### Convention rules

1. **`tags[0]` IS the PARA category** (closed). It mirrors the directory: a note in `vault/resources/...` has `tags[0]: resource`; a note in `vault/areas/...` has `tags[0]: area`; etc.
2. **`tags[1]` IS the second category** (open routing label). It mirrors the subdirectory: a note in `vault/resources/term_dictionary/` has `tags[1]: terminology`; a note in `vault/resources/skills/` has `tags[1]: skill`; etc. The label is sometimes pluralized into the directory name (`terminology` → `term_dictionary/`, `code` → `code_snippets/`).
3. **`building_block` is a SEPARATE FIELD** from tags. The 8 BB types live in their own field; they are not part of `tags`. BB and second-category are orthogonal — `concept` BB notes can have `tags[1]: terminology` (term notes) OR `tags[1]: papers` (digested papers) OR `tags[1]: metric`.
4. **`date of note` uses spaces in the key name.** YAML allows it because keys can be plain strings; do NOT change it to `date_of_note` (the indexer expects the spaced form).
5. **Do NOT add a separate `note_second_category:` field.** Tags[1] is the canonical SoT. The DB indexer reads `note_second_category` from `tags[1]` automatically.
6. **All tags are lowercase with underscores** (`knowledge_management`, not `Knowledge Management` or `knowledge-management`).
7. **Year-like strings must be quoted** (`year: "2026"`, not `year: 2026`) so YAML parses them as strings, not integers.

### Status semantics

| Status | When to use |
|---|---|
| `active` | Real, current content |
| `draft` | Work-in-progress real content |
| `archived` | Real content moved to `vault/archives/` |
| `deprecated` | Real content kept for reference; superseded but not deleted |
| `superseded` | Replaced by a newer note (link to the successor in body) |
| `stub` | Real note known to be incomplete |
| `placeholder` | Future-real note that doesn't exist yet (referenced from elsewhere) |
| **`template`** | **Intentional skeleton — not real content.** Templates live under `vault/resources/templates/` and serve as executable spec exemplars. Search filters them out by default. |
| `wip` / `in_progress` / `proposal` / `development` / `planning` | Project-state markers |
| `legacy` / `disabled` / `cancelled` | Inactive / retired |
| `research` / `review` / `pending` / `completed` | Workflow markers |

### Templates

The canonical executable form of this spec lives at [`vault/resources/templates/`](vault/resources/templates/) — one template per Building Block type. Copy a template, rename it, fill placeholders. The validator checks the templates themselves against the spec, so templates and spec cannot drift apart.

### Validation

```bash
python scripts/check_yaml_frontmatter.py --path vault/<your-note>.md
python scripts/check_note_format.py --path vault/<your-note>.md
```

The format checker enforces all 7 required fields, validates the closed enums against the lists above, warns if `keywords < 3` or `topics < 2`, and checks `tags[0]` against the closed PARA bucket list.

## Adding a Building Block Sub-Kind (Second Category)

The 8 top-level BB types are **closed**. Sub-kinds (encoded as `tags[1]`) are **open** — extend as your domain requires. Procedure:

1. Add the sub-kind value as `tags[1]` in your note's YAML frontmatter
2. Optionally add a term note in `vault/resources/term_dictionary/term_<subkind>.md` documenting it
3. If a directory doesn't yet exist for the new sub-kind, create one under the appropriate PARA bucket and move the note in (see "Subdirectory Conventions" below)
4. Run `bash scripts/update_notes_database.sh` to re-index

The 8 top-level BB types live in the `building_block:` field — distinct from the `tags:` field. The two are orthogonal: `building_block` is the epistemic axis (closed); `tags[1]` is the contextual routing label (open).

## Adding a Folgezettel trail

If your contribution introduces a new architectural argument, it deserves a Folgezettel trail. Pattern:

1. Author the **root note** as an `argument` BB at `vault/resources/analysis_thoughts/thought_<topic>.md`; set `folgezettel: "<N>"` (next root number) and `fz_parent: null`
2. Write child notes that elaborate, challenge, or absorb into synthesis
3. Update `vault/0_entry_points/entry_folgezettel_trails.md` with the new trail's row + ASCII tree

See [`vault/resources/term_dictionary/term_folgezettel.md`](vault/resources/term_dictionary/term_folgezettel.md) (planned v0.1) for the full convention.

## Release Process

1. Update `CHANGELOG.md` with the release notes
2. Bump `version` in `pyproject.toml`
3. Tag the release: `git tag v0.x.y && git push --tags`
4. Build: `python -m build`
5. Upload: `twine upload dist/*`
6. The `.github/workflows/publish.yml` workflow runs the upload automatically on tag push (planned v0.1)

## Code Style

- **Python 3.11+**
- **Ruff** for formatting and linting (config in `pyproject.toml`)
- **Mypy** for type checking — gradual, not strict
- **Imperative commit messages**: `add: skill_capture_essay_note` / `fix: rrf merge bug` / `docs(vault): clarify BB ontology`

## CI

The CI workflow (`.github/workflows/ci.yml`, planned v0.1) runs:
- `ruff check src/`
- `ruff format --check src/`
- `pytest`
- `python scripts/check_yaml_frontmatter.py --path vault/`
- `python scripts/check_note_format.py --path vault/`

## License

[MIT](LICENSE).
