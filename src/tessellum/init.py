"""Vault scaffolding — create a new Tessellum vault from the seed.

Public API:

    scaffold(target_dir, *, force=False) -> ScaffoldResult
        Creates the vault directory tree, copies templates + seed terms,
        writes a generic master TOC + README. Returns a summary of what
        was created.

The directory layout mirrors the dogfooded vault:

    target_dir/
    ├── 0_entry_points/
    │   └── entry_master_toc.md    (generic, scaffolded)
    ├── resources/
    │   ├── templates/             (13 templates copied from package data)
    │   ├── term_dictionary/
    │   │   └── term_building_block.md   (the load-bearing seed)
    │   ├── skills/
    │   ├── how_to/
    │   ├── analysis_thoughts/
    │   ├── code_repos/
    │   ├── code_snippets/
    │   ├── papers/
    │   ├── faqs/
    │   ├── digest/
    │   ├── teams/
    │   └── tools/
    ├── projects/
    ├── areas/
    ├── archives/
    │   └── experiments/
    └── README.md

After scaffolding, users can:

    cd target_dir
    tessellum capture concept my_topic --vault .
    tessellum format check .

The set of subdirectories under ``resources/`` is derived from the capture
``REGISTRY``: every flavor's destination is created so ``tessellum capture
<flavor>`` works out of the box.
"""

from __future__ import annotations

import datetime as dt
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from tessellum.capture import REGISTRY
from tessellum.data import seed_vault_dir, templates_dir


@dataclass(frozen=True)
class ScaffoldResult:
    """Summary of a successful scaffold call."""

    target: Path
    dirs_created: tuple[Path, ...] = field(default_factory=tuple)
    files_copied: tuple[Path, ...] = field(default_factory=tuple)
    files_written: tuple[Path, ...] = field(default_factory=tuple)


# Top-level vault directories that aren't covered by the REGISTRY's
# `destination` fields (REGISTRY covers resources/* + 0_entry_points/ +
# archives/experiments/, but not the bare PARA buckets).
_BARE_PARA_DIRS: tuple[str, ...] = (
    "0_entry_points",
    "projects",
    "areas",
    "archives",
)


def scaffold(target_dir: Path | str, *, force: bool = False) -> ScaffoldResult:
    """Create a new Tessellum vault at ``target_dir``.

    Args:
        target_dir: Directory to create the vault in. May or may not exist.
            If it exists and is non-empty, raises ``FileExistsError`` unless
            ``force=True``.
        force: Allow scaffolding into an existing non-empty directory.
            Overwrites files at the target paths; preserves other content.

    Returns:
        ScaffoldResult with the target path + lists of dirs created, files
        copied, and files written inline.

    Raises:
        FileExistsError: target exists, is non-empty, and ``force=False``.
        FileNotFoundError: package data is missing (templates_dir() or
            seed_vault_dir() can't resolve).
    """
    target = Path(target_dir).expanduser().resolve()

    if target.exists():
        if target.is_file():
            raise FileExistsError(
                f"target {target} is a file, not a directory; cannot scaffold."
            )
        if any(target.iterdir()) and not force:
            raise FileExistsError(
                f"target {target} exists and is non-empty. "
                f"Pass force=True to scaffold into it anyway."
            )
    else:
        target.mkdir(parents=True)

    dirs_created: list[Path] = [target]
    files_copied: list[Path] = []
    files_written: list[Path] = []

    # 1. Bare PARA dirs at the top level.
    for d in _BARE_PARA_DIRS:
        path = target / d
        if not path.exists():
            path.mkdir(parents=True)
            dirs_created.append(path)

    # 2. All capture-flavor destination dirs (mirrors REGISTRY so
    # `tessellum capture <flavor>` works out of the box).
    for spec in REGISTRY.values():
        dest = target / spec.destination
        if not dest.exists():
            dest.mkdir(parents=True)
            dirs_created.append(dest)

    # 3. Templates: copy every file (templates + sidecar + README) from
    # the shipped templates directory into resources/templates/.
    templates_src = templates_dir()
    templates_target = target / "resources" / "templates"
    templates_target.mkdir(parents=True, exist_ok=True)
    if templates_target not in dirs_created:
        dirs_created.append(templates_target)
    for entry in templates_src.iterdir():
        if entry.is_file():
            target_path = templates_target / entry.name
            shutil.copy2(entry, target_path)
            files_copied.append(target_path)

    # 4. Seed term: the load-bearing concept (term_building_block).
    seed_root = seed_vault_dir()
    seed_term_relative = Path("resources") / "term_dictionary" / "term_building_block.md"
    seed_term = seed_root / seed_term_relative
    if seed_term.is_file():
        target_term = target / seed_term_relative
        target_term.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(seed_term, target_term)
        files_copied.append(target_term)

    # 5. Generic master TOC.
    master_toc = target / "0_entry_points" / "entry_master_toc.md"
    master_toc.write_text(_render_master_toc(target.name), encoding="utf-8")
    files_written.append(master_toc)

    # 6. README.md (skipped by validator's non-note list).
    readme = target / "README.md"
    if not readme.exists() or force:
        readme.write_text(_render_readme(target.name), encoding="utf-8")
        files_written.append(readme)

    return ScaffoldResult(
        target=target,
        dirs_created=tuple(dirs_created),
        files_copied=tuple(files_copied),
        files_written=tuple(files_written),
    )


# ── Rendered content templates ─────────────────────────────────────────────


def _render_master_toc(vault_name: str) -> str:
    today = dt.date.today().isoformat()
    return f"""---
tags:
  - entry_point
  - navigation
  - master_toc
keywords:
  - master TOC
  - vault navigation
  - start here
topics:
  - Navigation
  - Vault Entry
language: markdown
date of note: {today}
status: active
building_block: navigation
---

# {vault_name} — Master Table of Contents

> Welcome to your Tessellum vault. This is the navigation root.

## Quick start

| If you want to... | Read |
|---|---|
| Understand the typed substrate | [`term_building_block`](../resources/term_dictionary/term_building_block.md) |
| Author a new note | Pick a template from [`resources/templates/`](../resources/templates/) and run `tessellum capture <flavor> <slug>` |
| Validate the vault format | Run `tessellum format check .` from the vault root |
| Understand the format spec | See the YAML reference in [`template_yaml_header`](../resources/templates/template_yaml_header.md) |

## Vault structure

Every typed atomic note lives under one of the four PARA buckets — `resources/`, `projects/`, `areas/`, `archives/` — and within a bucket, by sub-category. The 12 capture flavors map onto specific subdirectories; see `tessellum capture --help`.

## Capture flavors available

| Flavor | Destination | Filename pattern |
|---|---|---|
| `concept` | `resources/term_dictionary/` | `term_<slug>.md` |
| `procedure` | `resources/how_to/` | `howto_<slug>.md` |
| `skill` | `resources/skills/` | `skill_<slug>.md` (+ `skill_<slug>.pipeline.yaml`) |
| `argument` | `resources/analysis_thoughts/` | `thought_<slug>.md` |
| `entry_point` | `0_entry_points/` | `entry_<slug>.md` |
| ... | ... | (see `tessellum capture --help`) |

## Next steps

1. Add your first concept: `tessellum capture concept my_topic`
2. Add a skill (with paired pipeline sidecar): `tessellum capture skill my_skill`
3. Validate the vault: `tessellum format check .`

---
**Last Updated**: {today}
**Status**: Active — scaffolded by `tessellum init`
"""


def _render_readme(vault_name: str) -> str:
    return f"""# {vault_name} — a Tessellum vault

This is a [Tessellum](https://github.com/TianpeiLuke/Tessellum) vault: a typed-knowledge slipbox following the Building Block ontology.

## Layout

- `0_entry_points/` — master TOC + per-surface entries
- `resources/` — typed atomic notes (term_dictionary, skills, how_to, analysis_thoughts, ...)
- `resources/templates/` — copy-and-fill skeletons
- `projects/`, `areas/`, `archives/` — PARA buckets

## Quick start

```bash
# Create a new typed atomic note
tessellum capture concept my_topic --vault {vault_name}

# Create a skill with its paired pipeline sidecar
tessellum capture skill my_skill --vault {vault_name}

# Validate format
tessellum format check {vault_name}

# Validate skill pipeline sidecars
tessellum composer validate {vault_name}/resources/skills/
```

See `0_entry_points/entry_master_toc.md` for full navigation.
"""
