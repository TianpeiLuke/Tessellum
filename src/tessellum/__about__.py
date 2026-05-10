"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.2"

__status__ = (
    "alpha — format library shipped (parser + validator + closed-enum spec). "
    "See CHANGELOG.md for what's available now and the v0.1 roadmap."
)
