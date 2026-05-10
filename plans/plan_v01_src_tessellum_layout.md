---
tags:
  - project
  - plan
  - tessellum
  - v0_1
  - packaging
keywords:
  - src/tessellum layout
  - PyPI wheel contents
  - what pip install ships
  - v0.1 roadmap
  - hatch force-include
  - templates shipping
topics:
  - Packaging
  - PyPI Distribution
  - v0.1 Release
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
---

# Plan — `src/tessellum/` Layout for v0.1 (PyPI Wheel)

## Context — What `pip install tessellum` Actually Ships

The wheel is built from `[tool.hatch.build.targets.wheel] packages = ["src/tessellum"]`. **Nothing outside `src/tessellum/` is in the wheel.** The sdist additionally includes `vault/`, `scripts/`, `README.md`, etc., but `pip install` reads the wheel — sdist contents are invisible to end users.

**Implication**: every static asset the runtime needs (templates, schemas, seed-vault skeleton, format spec) must live under `src/tessellum/` or be force-included into it at wheel build time. The dogfooded `vault/resources/templates/` is **not** shipped to pip users by default.

## v0.0.1 Status (Done)

Two-line fix already shipped:

- `src/tessellum/__about__.py` — single-source `__version__` + `__status__`.
- `src/tessellum/cli/{__init__,main}.py` — argparse stub that prints version + roadmap. **Unblocks the broken `tessellum = "tessellum.cli:main"` script entry**, which previously raised `ImportError` on every `pip install tessellum`.
- `src/tessellum/__init__.py` re-exports `BuildingBlock`, `BB_SPECS`, `EPISTEMIC_EDGES`, etc., so `import tessellum; tessellum.BuildingBlock.CONCEPT` works.

This makes v0.0.1 honest: nothing it advertises is broken; nothing it doesn't advertise is implied.

## v0.1 Layout — What to Ship

| Subpath | Purpose | Notes |
|---|---|---|
| `__about__.py` | version + status | bump to `0.1.0` |
| `__init__.py` | top-level API surface | re-export `Note`, `validate`, `BuildingBlock` |
| `format/building_blocks.py` | typed BB enum + epistemic edges | already shipped |
| `format/frontmatter_spec.py` | closed enums (PARA, statuses, BB) as Python data | the validator AND any user tooling import this |
| `format/validator.py` | `validate(path) -> list[Issue]` | drives `tessellum format check` |
| `format/parser.py` | frontmatter+body → typed `Note` | drives capture, search, indexer |
| `data/templates/*.md` | 13 canonical templates | **force-included** from `vault/resources/templates/` — see § Templates Shipping |
| `data/seed_vault/` | minimal scaffold for `tessellum init` | master TOC + templates + 1-2 seed term notes |
| `data/schemas/*.json` | JSON schemas for skill canonicals, pipeline contracts | composer + validator share |
| `cli/__init__.py` + `cli/main.py` | argparse/click dispatcher | already minimal stub for v0.0.1 |
| `cli/init.py` | `tessellum init <dir>` | copies `data/seed_vault/` into target |
| `cli/capture.py` | `tessellum capture <bb> <slug>` | copies `data/templates/template_<bb>.md` |
| `cli/format_check.py` | `tessellum format check <path>` | calls `format.validator` |
| `cli/search.py` | `tessellum search <q>` | calls `retrieval.hybrid` |
| `indexer/builder.py` | scan vault → SQLite + sqlite-vec + FTS5 | `tessellum index build` |
| `indexer/schema.sql` | DB schema | shipped as resource |
| `retrieval/{bm25,dense,rrf,ppr}.py` | search backends | `from tessellum.retrieval import hybrid` |
| `composer/protocol.py` | DKS typed contracts | pydantic models |
| `composer/agents/*.py` | per-agent step implementations | optional `[agent]` extra |
| `mcp/server.py` | MCP stdio server exposing skills | optional `[mcp]` extra |

**Out of scope for v0.1 wheel** (stay in repo, not in wheel): `vault/` (the dogfood vault — clones get it, pip users get the seed instead), `tests/`, `inbox/`, `experiments/`, `scripts/` (move user-relevant ones into `cli/` subcommands), `notebook/`.

## Templates Shipping — Use Hatch `force-include`

The cleanest way to keep ONE canonical templates location while still bundling them in the wheel:

```toml
[tool.hatch.build.targets.wheel.force-include]
"vault/resources/templates" = "src/tessellum/data/templates"
"vault/0_entry_points/entry_master_toc.md" = "src/tessellum/data/seed_vault/0_entry_points/entry_master_toc.md"
# ... and any term notes that should be in the seed vault
```

**Why this approach**:

- Single source of truth in `vault/resources/templates/` — the dogfooded vault wins.
- Wheel automatically grafts them into `src/tessellum/data/templates/` at build time.
- `tessellum init` and `tessellum capture` resolve them via `importlib.resources.files("tessellum.data.templates")`.
- No git symlinks, no two-copy drift, no CI-enforced parity check.

**Alternatives considered**:

- *Two copies + CI parity check* — error-prone, every template change touches two paths.
- *Flip source of truth into `src/tessellum/data/templates/`, symlink from `vault/`* — git symlinks work but break in zip downloads and on Windows; awkward.

## Seed Vault — What `tessellum init` Should Scaffold

A user running `tessellum init my-vault/` should get a vault that opens cleanly in Obsidian, validates green, and demonstrates every concept:

```
my-vault/
├── 0_entry_points/
│   └── entry_master_toc.md          # adapted from Tessellum's own master TOC
├── resources/
│   ├── templates/                    # all 13 templates, ready to copy
│   └── term_dictionary/
│       ├── term_building_block.md   # the canonical seed
│       └── term_zettelkasten.md     # one supporting term
├── projects/
│   └── .gitkeep
├── areas/
│   └── .gitkeep
├── archives/
│   └── .gitkeep
└── tessellum.toml                    # vault config (DB path, embedding model, etc.)
```

**Open question**: should the seed include all six pillar terms? Tradeoff — heavier scaffold (more for the user to delete if they don't want it) vs. concept-complete (user immediately sees what a "real" vault looks like). Lean: include all six — they're tiny, and a vault without them feels half-built.

## Order of Operations

1. **Done (v0.0.1 patch / v0.0.2)** — fix CLI entry point.
2. **Done (v0.0.2 / v0.0.4)** — ship `format/{frontmatter_spec,validator,parser,link_checker}.py`. Highest leverage per LOC: turns the typed substrate from "static enum" into "library users can import to validate their own notes".
3. **Done (v0.0.7)** — wire `force-include` for templates. Seed-vault content for `tessellum init` is still pending.
4. CLI buildout — partial:
   - **Done (v0.0.3)** — `tessellum format check` (out-of-order; depends only on validator from step 2).
   - **Done (v0.0.8)** — `tessellum capture <flavor> <slug>`.
   - Pending — `tessellum init` (depends on seed vault content from step 3).
5. **Done (v0.0.12)** — ship `indexer/` substrate (notes + note_links tables, build CLI). FTS5 + sqlite-vec layer in step 6. See `tessellum.indexer.Database` for the typed query API.
6. Ship `retrieval/`. **The retrieval port is its own substantial subsystem** — see [`plan_retrieval_port.md`](plan_retrieval_port.md) for the 5-wave plan (BM25+FTS5 → Dense+sqlite-vec → Hybrid RRF → Best-first BFS → Skill orchestration). Important lessons encoded there: hybrid is the default (+12pp lift); skip PPR (best-first BFS is Pareto-optimal); validate on answer quality, not Hit@K.
7. Ship `composer/` and `mcp/`. **The Composer port is its own substantial subsystem** — see [`plan_composer_port.md`](plan_composer_port.md) for the 5-wave porting plan (Foundation → Compiler → Executor → LLM bridge → Scale). Composer Wave 1 already shipped (v0.0.9 + v0.0.10); Waves 2-4 pending.

Each step is independently releasable. v0.1 doesn't need all seven done — a credible v0.1 minimum is steps 1-4 (format library + CLI scaffold + capture, all already shipped) plus step 7 Wave 1 (Composer foundation). Indexer/retrieval (steps 5-6) and Composer Waves 2-5 can be v0.2-0.5.

## Open Questions

- **Click vs argparse for CLI?** `click` is already in `dependencies`. Worth using for v0.1 once subcommands grow; argparse is fine for the v0.0.1 stub.
- **Where does the seed vault's `tessellum.toml` schema live?** Options: hard-coded in `cli/init.py`, or a real config dataclass in `tessellum.config` that `init` serializes. Lean: real dataclass — config is going to grow.
- **Do we ship the format validator's full closed-enum tables in `__init__.py`?** I.e., should `tessellum.VALID_BUILDING_BLOCKS` be a top-level export? Yes — pre-empts "where do I import this from" friction.
- **Should `data/templates/` be a `package_data` glob in `pyproject.toml` too, or is `force-include` enough?** Hatch's `force-include` should suffice for wheel inclusion; verify with `python -m build && unzip -l dist/*.whl | grep templates` after wiring.

## Validation Plan

Each release should pass:

```bash
# 1. Build wheel + sdist
python -m build

# 2. Verify wheel contents
unzip -l dist/tessellum-*.whl | grep -E '(templates|seed_vault|schemas)'

# 3. Install in clean venv
python -m venv /tmp/v && /tmp/v/bin/pip install dist/tessellum-*.whl

# 4. Smoke-test imports
/tmp/v/bin/python -c "from tessellum import BuildingBlock, validate; print(BuildingBlock.CONCEPT)"

# 5. Smoke-test CLI
/tmp/v/bin/tessellum --version
/tmp/v/bin/tessellum init /tmp/test-vault
/tmp/v/bin/tessellum format check /tmp/test-vault/resources/term_dictionary/term_building_block.md
```

If any of these fail, the release is not honest.

## See Also

- [Master TOC](../vault/0_entry_points/entry_master_toc.md) — vault-side roadmap
- [CHANGELOG.md](../CHANGELOG.md) — per-release ship list
- [DEVELOPING.md § YAML Frontmatter Specification](../DEVELOPING.md) — the spec the validator implements
- [pyproject.toml](../pyproject.toml) — current build config

---

**Last Updated**: 2026-05-10
**Status**: Active — v0.0.1 fix landed; v0.0.2 (format library) is next.
