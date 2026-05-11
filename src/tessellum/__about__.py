"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.41"

__status__ = (
    "alpha — FZ-trail tooling ships. `tessellum fz` CLI lands with six "
    "sub-subcommands (list/show/ancestors/descendants/path/all) that "
    "explore the Folgezettel topology stored on notes.folgezettel + "
    "notes.folgezettel_parent (no materialised trails view — derived "
    "in memory). Three new skill canonicals seed: tessellum-traverse-"
    "folgezettel, tessellum-manage-folgezettel, tessellum-append-to-"
    "trail. DKS Phase 1 (v0.0.40) ships unchanged. Phase 2 (DKS as a "
    "composer skill) lands next."
)
