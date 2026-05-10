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

## YAML Tag Convention (PARA + Second Category)

Tessellum uses a strict convention for the first two YAML tags:

```yaml
tags:
  - <para-bucket>      # tags[0]: one of {resource, area, project, archive, entry_point}
  - <second-category>  # tags[1]: the open sub-kind label (e.g., terminology, skill, how_to, code, papers, analysis, digest, faq, code_repo)
  - <topic-tag-1>      # tags[2..]: free-form topic tags
  - <topic-tag-2>
  - ...
```

**Rule**: tags[0] is always a PARA bucket (closed 5-element vocabulary). tags[1] is always the second-category routing label (open, extensible folksonomy). Topic tags follow.

The second tag is also the **routing label** — it determines the subdirectory under the PARA bucket (with possible pluralization: `terminology` → `term_dictionary/`, `code` → `code_snippets/`). It is the canonical SoT; do NOT add a separate `note_second_category:` field — that is redundant.

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
