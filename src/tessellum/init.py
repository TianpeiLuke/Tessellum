"""Vault scaffolding — create a new Tessellum vault from the seed.

Public API:

    scaffold(target_dir, *, force=False) -> ScaffoldResult
        Creates the vault directory tree, copies templates + seed terms,
        writes a generic master TOC + README. Returns a summary of what
        was created.

The directory layout mirrors the dogfooded vault:

    target_dir/
    ├── 0_entry_points/
    │   ├── entry_master_toc.md          (generic, scaffolded per-vault)
    │   ├── entry_acronym_glossary.md    (master index of the 5 glossaries)
    │   ├── acronym_glossary_statistics.md
    │   ├── acronym_glossary_critical_thinking.md
    │   ├── acronym_glossary_cognitive_science.md
    │   ├── acronym_glossary_network_science.md
    │   └── acronym_glossary_llm.md
    ├── resources/
    │   ├── templates/                   (15 templates copied from package data)
    │   ├── term_dictionary/
    │   │   ├── term_knowledge_building_blocks.md   (historical — Sascha Fast)
    │   │   ├── term_building_block.md              (Tessellum's 8-type ontology — load-bearing)
    │   │   ├── term_epistemic_function.md          (EF — what each BB does)
    │   │   ├── term_dialectic_knowledge_system.md  (DKS — closed-loop dialectic)
    │   │   ├── term_cqrs.md                        (CQRS — System P ⊥ System D)
    │   │   ├── term_zettelkasten.md                (Z — Luhmann's method)
    │   │   ├── term_para_method.md                 (PARA — Forte's scheme)
    │   │   ├── term_basb.md                        (Building a Second Brain)
    │   │   ├── term_code_method.md                 (Capture/Organize/Distill/Express)
    │   │   ├── term_slipbox.md                     (the system class)
    │   │   └── term_folgezettel.md                 (trail mechanism)
    │   ├── skills/   how_to/   analysis_thoughts/
    │   ├── code_repos/   code_snippets/
    │   ├── papers/   faqs/   digest/
    │   └── teams/   tools/
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


# Vault-relative paths of seed content shipped via Hatch ``force-include``.
# Each entry is resolved against ``seed_vault_dir()`` (wheel install) with
# a source-tree fallback to ``vault/`` (editable install). The explicit
# manifest is the load-bearing piece: an ``rglob("*.md")`` over the
# dogfood vault in editable mode would copy ~5000 files, which is not
# what `tessellum init` is for.
_SEED_VAULT_MANIFEST: tuple[str, ...] = (
    # 11 foundation term notes (the conceptual primer for typed-knowledge
    # work). Each is general public knowledge — no internal references.
    "resources/term_dictionary/term_knowledge_building_blocks.md",   # historical (Sascha Fast)
    "resources/term_dictionary/term_building_block.md",              # Tessellum's 8-type ontology
    "resources/term_dictionary/term_epistemic_function.md",          # what each BB does
    "resources/term_dictionary/term_dialectic_knowledge_system.md",  # DKS — closed-loop dialectic
    "resources/term_dictionary/term_cqrs.md",                        # System P ⊥ System D
    "resources/term_dictionary/term_zettelkasten.md",                # Luhmann's method
    "resources/term_dictionary/term_para_method.md",                 # Forte's PARA scheme
    "resources/term_dictionary/term_basb.md",                        # Building a Second Brain
    "resources/term_dictionary/term_code_method.md",                 # Capture/Organize/Distill/Express
    "resources/term_dictionary/term_slipbox.md",                     # the system class
    "resources/term_dictionary/term_folgezettel.md",                 # trail mechanism
    # System regularization (the format contract every note follows).
    "resources/term_dictionary/term_format_spec.md",                 # YAML/link/naming spec + issue codes
    # Getting-started walkthrough (the pipeline foundation in vault form).
    "resources/how_to/howto_first_vault.md",                         # 8-step CLI walkthrough
    # FZ trail nodes — Trail 1 (Architecture / CQRS) and Trail 2 (Dialectic / DKS).
    "resources/analysis_thoughts/thought_building_block_ontology_relationships.md",        # FZ 1
    "resources/analysis_thoughts/thought_cqrs_design_evolution.md",                        # FZ 1a
    "resources/analysis_thoughts/thought_synthesis_two_systems_cqrs_value_proposition.md", # FZ 1a1
    "resources/analysis_thoughts/thought_cqrs_essence_for_tessellum.md",                   # FZ 1a1a
    "resources/analysis_thoughts/thought_dks_evolution.md",                                # FZ 2
    "resources/analysis_thoughts/thought_dks_design_synthesis.md",                         # FZ 2a
    # Entry points — master TOCs / pickers / FZ trail map + per-trail entries +
    # 5 universal acronym glossaries + Tessellum-foundations glossary.
    # entry_master_toc.md is rendered inline by init, not shipped here.
    "0_entry_points/entry_acronym_glossary.md",
    "0_entry_points/entry_building_block_index.md",                  # BB picker (scannable matrix)
    "0_entry_points/entry_folgezettel_trails.md",                    # FZ master trail index
    "0_entry_points/entry_architecture_trail.md",                    # per-trail entry: Trail 1
    "0_entry_points/entry_dialectic_trail.md",                       # per-trail entry: Trail 2
    "0_entry_points/acronym_glossary_tessellum_foundations.md",      # one-line lookup for the 11 foundation terms
    "0_entry_points/acronym_glossary_statistics.md",
    "0_entry_points/acronym_glossary_critical_thinking.md",
    "0_entry_points/acronym_glossary_cognitive_science.md",
    "0_entry_points/acronym_glossary_network_science.md",
    "0_entry_points/acronym_glossary_llm.md",
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

    # 4. Seed content: copy each file in _SEED_VAULT_MANIFEST from the
    # installed seed_vault (wheel mode) or the dogfooded vault (editable
    # mode), preserving the relative path. The explicit manifest avoids
    # an `rglob("*.md")` in editable mode — that would copy the entire
    # ~5000-file dogfood vault into the user's new vault.
    seed_root = seed_vault_dir()
    for rel_path in _SEED_VAULT_MANIFEST:
        src_file = seed_root / rel_path
        if not src_file.is_file():
            continue   # quietly skip — not every shipped seed is in every install
        tgt = target / rel_path
        tgt.parent.mkdir(parents=True, exist_ok=True)
        if not tgt.exists() or force:
            shutil.copy2(src_file, tgt)
            files_copied.append(tgt)

    # 5. Generic per-vault master TOC (always regenerated — its filename
    # collides with anything shipped in seed_vault, so we render after the
    # seed copy to make sure the vault's TOC reflects its actual name).
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
| Understand the typed substrate | [`term_building_block`](../resources/term_dictionary/term_building_block.md) — 8 typed atomic roles + 10 epistemic edges |
| Look up an acronym | [`entry_acronym_glossary`](entry_acronym_glossary.md) — 5 domain glossaries indexing 397 acronyms |
| Author a new note | Pick a template from [`resources/templates/`](../resources/templates/) and run `tessellum capture <flavor> <slug>` |
| Validate the vault format | Run `tessellum format check .` from the vault root |
| Understand the format spec | See the YAML reference in [`template_yaml_header`](../resources/templates/template_yaml_header.md) |

## Conceptual primer (shipped as term notes)

The eleven term notes that establish the vocabulary every Tessellum vault rests on.

### Methodology lineage

| Concept | Term note |
|---|---|
| **Zettelkasten** — Luhmann's atomic-note method | [`term_zettelkasten`](../resources/term_dictionary/term_zettelkasten.md) |
| **Slipbox** — the system class (Tessellum is one implementation) | [`term_slipbox`](../resources/term_dictionary/term_slipbox.md) |
| **Folgezettel** — alphanumeric trails encoding *how thinking developed* | [`term_folgezettel`](../resources/term_dictionary/term_folgezettel.md) |
| **PARA** — Forte's Projects / Areas / Resources / Archives scheme | [`term_para_method`](../resources/term_dictionary/term_para_method.md) |
| **BASB** — Building a Second Brain (Tiago Forte's PKM movement) | [`term_basb`](../resources/term_dictionary/term_basb.md) |
| **CODE** — Capture / Organize / Distill / Express (Forte's lifecycle) | [`term_code_method`](../resources/term_dictionary/term_code_method.md) |
| **Knowledge Building Blocks** — Sascha Fast's historical taxonomy | [`term_knowledge_building_blocks`](../resources/term_dictionary/term_knowledge_building_blocks.md) |

### Tessellum-specific architecture

| Concept | Term note |
|---|---|
| **Building Block** — the 8-type typed atomic ontology | [`term_building_block`](../resources/term_dictionary/term_building_block.md) |
| **Epistemic Function** — what each BB *does* | [`term_epistemic_function`](../resources/term_dictionary/term_epistemic_function.md) |
| **DKS** — Dialectic Knowledge System (closed-loop dialectic) | [`term_dialectic_knowledge_system`](../resources/term_dictionary/term_dialectic_knowledge_system.md) |
| **CQRS** — System P (write) ⊥ System D (read) | [`term_cqrs`](../resources/term_dictionary/term_cqrs.md) |

## Vault structure

Every typed atomic note lives under one of the four PARA buckets — `resources/`, `projects/`, `areas/`, `archives/` — and within a bucket, by sub-category. The 14 capture flavors map onto specific subdirectories; see `tessellum capture --help`.

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
