"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.34"

__status__ = (
    "alpha — Seed-manifest consolidation. Single Python tuple in "
    "src/tessellum/data/_seed_manifest.py is now the only source of "
    "truth for the seed-vault file list. A custom Hatch build hook "
    "(hatch_build.py) reads the manifest at wheel build time and "
    "registers force_include mappings; src/tessellum/init.py imports "
    "the same tuple at runtime. Adding a seed file is now one line in "
    "one file — no pyproject edit needed."
)
