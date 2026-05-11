"""Tessellum CLI entry point.

The ``tessellum`` console script declared in ``pyproject.toml``
resolves to ``tessellum.cli:main``, so this module must always export
a callable named ``main``. Subcommands live in sibling modules
(``capture``, ``composer``, ``dks``, ``bb``, ``search``, ``mcp``, ...).
"""

from tessellum.cli.main import main

__all__ = ["main"]
