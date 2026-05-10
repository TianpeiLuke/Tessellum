# Contributing to Tessellum

Thank you for considering a contribution. Tessellum is in early alpha (v0.0.1) and the contribution surfaces are deliberately limited until v0.1 ships. Read this guide before opening a PR.

## Quick Decision Tree

| What are you contributing? | Where it goes |
|---|---|
| New skill (capture / digest / analyze) | Canonical body in `vault/resources/skills/`; thin headers in `.claude/skills/` + `.kiro/skills/`; pipeline sidecar in `vault/resources/skills/skill_<name>.pipeline.yaml` if applicable |
| New BB sub-kind (e.g., `note_second_category=spreadsheet`) | Term note in `vault/resources/term_dictionary/`; do NOT add a new top-level BB type without a design discussion |
| New retrieval strategy | Module in `src/tessellum/retrieval/`; add a smoke test in `tests/retrieval/`; update `docs/architecture.md` |
| New documentation | `vault/` (Tessellum dogfoods itself — there is no separate `docs/`). Pick the right BB-typed location: `term_dictionary/` for definitions, `how_to/` for procedures, `analysis_thoughts/` for arguments + trails, `0_entry_points/` for navigation indexes. |
| Bug fix | Open an issue first describing the bug; reference it in the PR |
| Architecture proposal | Open an RFC issue; draft a Folgezettel trail in `vault/resources/analysis_thoughts/` if accepted |

## Layout Convention

Every artifact has a single home. Don't mix.

| Artifact | Location |
|---|---|
| `import`-able Python | `src/tessellum/` |
| Knowledge vault content (your notes) | `vault/` |
| User input (PDFs, .eml, papers, plans) | `inbox/` |
| Generated DBs / indexes | `data/` (gitignored) |
| Experiment outputs | `experiments/` |
| Operational scripts | `scripts/` |
| Tests | `tests/` |
| Public documentation | `docs/` |
| Skill thin-header (Claude / Kiro) | `.claude/skills/`, `.kiro/skills/` |
| Skill canonical body (the actual content) | `vault/resources/skills/` |

See [`DEVELOPING.md`](DEVELOPING.md) for the full layout discussion.

## Note Format Standards

Every typed atomic note ("tessellum") MUST have:

```yaml
---
tags:
  - <category-tag>            # First tag describes the note's role (resource, area, project, archive)
  - <building-block-tag>      # Second tag describes BB type (concept, procedure, model, argument, ...)
  - <topic-tag>               # Additional topic tags for retrieval
keywords:
  - <key-term-1>
  - <key-term-2>
topics:
  - <topic-1>
language: markdown
date of note: YYYY-MM-DD
status: active
building_block: <concept|procedure|model|argument|counter_argument|hypothesis|empirical_observation|navigation>
---
```

Required H2 sections vary by BB type — see `docs/note-format.md`. The validator runs as a pre-commit hook:

```bash
python scripts/check_yaml_frontmatter.py --path vault/<your-note>.md
python scripts/check_note_format.py --path vault/<your-note>.md
```

## Folgezettel Trail Etiquette

If your contribution introduces a new architectural argument, it deserves a Folgezettel trail. Pattern:

1. Author the **root note** as an `argument` BB in `vault/resources/analysis_thoughts/thought_<your_topic>.md`
2. Run `tessellum trail next <parent>` to get the next FZ ID (or claim a new root by using a number not yet taken)
3. Write child notes that elaborate (`<root>a`, `<root>b`, ...), challenge (`<root>1` as `counter_argument`), or absorb into synthesis (`<counter>1` as `argument`)
4. Update `vault/0_entry_points/entry_folgezettel_trails.md` with a row for the new trail

Trails should encode dialectic descent — argument → counter → response → reframe — not just topical proximity.

## Skill Authoring

Skills live in three places (the in-vault SoT pattern):

1. **Canonical body**: `vault/resources/skills/skill_<name>.md` — the actual procedure
2. **Claude thin header**: `.claude/skills/<name>/SKILL.md` — points at the canonical body
3. **Kiro thin header**: `.kiro/skills/<name>/SKILL.md` — same pattern
4. **Pipeline sidecar** (if the skill has typed-contract steps): `vault/resources/skills/skill_<name>.pipeline.yaml`

The thin headers ensure both ecosystems (Claude Code, Kiro CLI) can discover the skill without duplicating the body. See an existing skill for reference.

## Testing

Run the full test suite:

```bash
pip install -e ".[dev]"
pytest
```

Add tests under `tests/` mirroring the source structure (`tests/composer/`, `tests/retrieval/`, etc.). Smoke tests for end-to-end flows live in `tests/smoke/`.

## Code Style

- Python 3.11+
- `ruff` for formatting and linting (config in `pyproject.toml`)
- `mypy` for type checking (gradual; not strict)
- Imperative commit messages: `add: skill_capture_essay_note` / `fix: rrf merge bug` / `docs: clarify BB ontology`

## Pull Request Process

1. Open an issue describing what you're proposing (unless it's a trivial bug fix)
2. Branch from `main`: `git checkout -b feature/your-thing`
3. Write tests
4. Make sure `pytest` and `ruff check src/` both pass
5. Open the PR with a clear description; reference the issue
6. Maintainer review — typically within a week

## Code of Conduct

Be kind, be precise, attack the argument not the person. Tessellum is a system that takes counter-arguments seriously; the project's culture should mirror that.

## License

By contributing, you agree your contributions are licensed under the [MIT License](LICENSE).
