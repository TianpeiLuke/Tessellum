"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.7"

__status__ = (
    "alpha — templates ship in the wheel via hatch force-include. "
    "See CHANGELOG.md for what's available now and the v0.1 roadmap."
)
