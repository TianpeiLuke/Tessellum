"""Hatch build hook — graft seed-vault files into the wheel at build time.

Reads :data:`tessellum.data._seed_manifest.SEED_VAULT_MANIFEST` and
registers a ``force_include`` mapping for each entry, so the wheel
target ships every listed file under ``tessellum/data/seed_vault/``.

This eliminates the previous duplication where the seed file list
had to be maintained in two places:

  - ``pyproject.toml`` ``[tool.hatch.build.targets.wheel.force-include]``
  - ``src/tessellum/init.py`` ``_SEED_VAULT_MANIFEST``

Now both ends of the pipeline read the same Python module. Adding a
seed file means appending one line to ``_seed_manifest.py`` — the
build hook picks it up at the next ``python -m build`` and
``tessellum init`` picks it up via the same import at runtime.

The hook is registered in ``pyproject.toml``::

    [tool.hatch.build.targets.wheel.hooks.custom]
    path = "hatch_build.py"

Hatch discovers ``SeedManifestHook`` by inheriting from
``BuildHookInterface``; no other registration is needed.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class SeedManifestHook(BuildHookInterface):
    """Force-include each entry in ``SEED_VAULT_MANIFEST`` into the wheel."""

    PLUGIN_NAME = "seed-manifest"

    def initialize(self, version: str, build_data: dict) -> None:
        manifest = _load_manifest(self.root)
        force_include = build_data.setdefault("force_include", {})
        for rel_path in manifest:
            src = f"vault/{rel_path}"
            dst = f"src/tessellum/data/seed_vault/{rel_path}"
            force_include[src] = dst


def _load_manifest(repo_root: str) -> tuple[str, ...]:
    """Load ``SEED_VAULT_MANIFEST`` from the source tree.

    Hatch runs the build hook before the package is installed, so the
    manifest module isn't on ``sys.path`` yet. We load it by file path
    via ``importlib.util`` — same behaviour Hatch uses internally for
    its own version hook.

    Args:
        repo_root: Absolute path to the repository root (``self.root``
            on the hook). The manifest lives at
            ``<repo>/src/tessellum/data/_seed_manifest.py``.

    Returns:
        The ``SEED_VAULT_MANIFEST`` tuple from the loaded module.

    Raises:
        RuntimeError: The manifest file is missing or cannot be loaded.
    """
    manifest_path = Path(repo_root) / "src" / "tessellum" / "data" / "_seed_manifest.py"
    if not manifest_path.is_file():
        raise RuntimeError(
            f"seed manifest not found at {manifest_path}. "
            f"The wheel cannot be built without it."
        )

    spec = importlib.util.spec_from_file_location(
        "_tessellum_seed_manifest", manifest_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"could not create import spec for {manifest_path}"
        )

    module = importlib.util.module_from_spec(spec)
    # Stash in sys.modules so the loader can resolve self-references.
    sys.modules.setdefault(spec.name, module)
    spec.loader.exec_module(module)
    return module.SEED_VAULT_MANIFEST
