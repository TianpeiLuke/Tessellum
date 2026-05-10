"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.11"

__status__ = (
    "alpha — `tessellum init` ships. v0.1 minimum complete: format library + "
    "init/capture/format-check/composer-validate CLI subcommands. "
    "See CHANGELOG.md for what's available now and the v0.1 roadmap."
)
