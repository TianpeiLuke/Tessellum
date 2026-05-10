"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.31"

__status__ = (
    "alpha — Seed vault gains an example FZ trail. Trail 1 (Architecture) "
    "is a 4-note linear descent that documents how Tessellum's CQRS "
    "architecture was reasoned into shape: BB ontology relationships "
    "(substrate, FZ 1) → CQRS design evolution (narrative, FZ 1a) → "
    "two-systems synthesis (pivot, FZ 1a1) → CQRS essence (distilled "
    "thesis, FZ 1a1a). Plus `entry_folgezettel_trails.md` as the trail "
    "map. The trail is both the architectural reasoning record and a "
    "worked example of the FZ convention."
)
