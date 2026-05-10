"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.9"

__status__ = (
    "alpha — Composer Wave 1 foundation library shipped "
    "(schema + Pydantic contracts + skill_extractor + pipeline loader). "
    "See CHANGELOG.md for what's available now and the v0.1 roadmap."
)
