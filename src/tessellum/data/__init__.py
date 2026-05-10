"""tessellum.data — package-shipped data (templates, schemas, seed vault).

Contents are NOT in the source tree under ``src/tessellum/data/`` — they're
grafted from the dogfooded ``vault/`` at wheel build time via Hatch
``[tool.hatch.build.targets.wheel.force-include]``. Single source of truth
in the vault; automatic inclusion in the wheel; no two-copy drift.

Editable installs (``pip install -e .``) don't run ``force-include``, so
the loader functions in this module fall back to the source-tree location.
This means the same import works in dev and in wheel-install mode without
any caller-side branching.

Public API:

    templates_dir() -> Path
        Returns the directory holding the 13 BB-type templates plus the
        YAML-header reference and the starter pipeline sidecar.

    seed_vault_dir() -> Path
        Returns the root of the seed-vault tree shipped with the package.
        Used by ``tessellum init`` to copy starter content (term notes,
        master TOC) into a freshly scaffolded vault.
"""

from __future__ import annotations

from pathlib import Path

__all__ = ["templates_dir", "seed_vault_dir"]


def templates_dir() -> Path:
    """Return the path to the templates directory.

    Tries the installed location first (``<package>/templates/``, populated
    by ``force-include`` at wheel build time). Falls back to the source-tree
    vault location (``<repo>/vault/resources/templates/``) for editable
    installs and source checkouts.

    Raises:
        FileNotFoundError: Neither location holds a usable templates dir.
            This indicates a broken install or a misconfigured ``force-include``.
    """
    installed = Path(__file__).parent / "templates"
    if installed.is_dir() and any(installed.iterdir()):
        return installed

    # Source-tree fallback. __file__ is src/tessellum/data/__init__.py;
    # parents[3] walks data/ -> tessellum/ -> src/ -> repo root.
    repo_root = Path(__file__).resolve().parents[3]
    fallback = repo_root / "vault" / "resources" / "templates"
    if fallback.is_dir():
        return fallback

    raise FileNotFoundError(
        f"tessellum templates directory not found. "
        f"Tried installed location ({installed}) and source-tree fallback "
        f"({fallback}). Either the wheel was built without force-include, "
        f"or the vault/resources/templates/ directory is missing."
    )


def seed_vault_dir() -> Path:
    """Return the path to the seed-vault tree.

    The seed vault holds starter content for ``tessellum init``: a curated
    subset of the dogfooded vault (currently just ``term_building_block.md``
    in v0.0.11; future versions may include more pillar terms behind an opt
    -in flag).

    Mirrors the target vault structure: callers resolve files via
    ``seed_vault_dir() / "resources" / "term_dictionary" / "term_X.md"``.

    Same dual-mode resolution as ``templates_dir()``: tries installed
    location first, falls back to source tree.

    Raises:
        FileNotFoundError: Neither location is populated. Indicates a
            broken install or a missing force-include entry in pyproject.toml.
    """
    installed = Path(__file__).parent / "seed_vault"
    if installed.is_dir() and any(installed.rglob("*.md")):
        return installed

    # Source-tree fallback. The seed-vault content is force-included from
    # the dogfooded vault, so dev mode reads directly from vault/.
    repo_root = Path(__file__).resolve().parents[3]
    fallback = repo_root / "vault"
    if fallback.is_dir() and (fallback / "resources" / "term_dictionary").is_dir():
        return fallback

    raise FileNotFoundError(
        f"tessellum seed_vault directory not found. "
        f"Tried installed location ({installed}) and source-tree fallback "
        f"({fallback}). Either the wheel was built without force-include, "
        f"or the vault/resources/term_dictionary/ directory is missing."
    )
