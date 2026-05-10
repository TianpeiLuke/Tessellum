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
        YAML-header reference. Used by capture/init CLI subcommands and
        any tooling that needs to copy or read the canonical skeletons.
"""

from __future__ import annotations

from pathlib import Path

__all__ = ["templates_dir"]


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
