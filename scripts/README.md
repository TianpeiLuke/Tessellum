# Tessellum Scripts

Top-level home for **one-off operational utilities** — vault migrations, repo maintenance, contributor convenience helpers. Not shipped in the wheel; live here so contributors can find them and so they don't pollute the installed package surface.

## What lives here

| Use case | Example |
|---|---|
| Vault migration | `rename_legacy_tag.py` — sweep all `tags[1]: foo` → `tags[1]: bar` after a convention change |
| Repo maintenance | `backfill_status_field.py` — add missing `status: active` to old notes |
| Contributor convenience | `run_all_checks.sh` — run `ruff` + `pytest` + `tessellum format check vault/` in sequence |
| Bootstrap | `download_example_vault.sh` — pull a sample vault for testing |

## What does NOT live here

| Capability | Goes in |
|---|---|
| Anything users run repeatedly via `tessellum <subcommand>` | `src/tessellum/cli/<subcommand>.py` + supporting library code |
| Re-usable library functions | `src/tessellum/<module>/` |
| Knowledge content (how-to guides, term notes, skill canonicals) | `vault/resources/...` |
| Project-management plans | `plans/` |
| Pipeline run traces | `runs/<subsystem>/` (gitignored) |

## Decision rule

| Question | Answer | Destination |
|---|---|---|
| Does this implement a capability users will run repeatedly? | Yes | `src/tessellum/cli/` as a CLI subcommand |
| Is this a re-usable library function? | Yes | `src/tessellum/<module>/` |
| Is this a one-off migration / repo maintenance / contributor helper? | Yes | here (top-level `scripts/`) |

## Why outside `src/`

1. **Wheel hygiene.** `pip install tessellum` ships only `src/tessellum/`. One-off utilities don't belong in user installs.
2. **Distinction visible at the filesystem level.** Code that ships goes under `src/`; code that supports the project but doesn't ship sits at top level (alongside `tests/`, `plans/`, `runs/`).
3. **PEP src-layout convention.** Only the importable package goes under `src/`. Scripts that *use* the package live elsewhere.
4. **CQRS clarity.** Both System P and System D operations are CLI subcommands. `scripts/` holds **meta-operations on the project itself** — neither P nor D, just dev/maintenance tooling.

## See also

- [`plans/plan_cqrs_repo_layout.md`](../plans/plan_cqrs_repo_layout.md) — the workflow → folder mapping that `scripts/` participates in.
- [`DEVELOPING.md` § Layout Convention](../DEVELOPING.md#layout-convention) — the full layout table.
