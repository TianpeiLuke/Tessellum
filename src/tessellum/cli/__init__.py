"""Tessellum CLI entry point.

The ``tessellum`` console script declared in ``pyproject.toml`` resolves to
``tessellum.cli:main``, so this module must always export a callable named
``main``. In v0.0.1 the implementation is a thin status banner — full
subcommands (``init``, ``capture``, ``format check``, ``search``) ship in v0.1.
"""

from tessellum.cli.main import main

__all__ = ["main"]
