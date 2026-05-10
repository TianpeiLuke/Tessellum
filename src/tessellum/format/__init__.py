"""tessellum.format — note format primitives: Building Blocks, YAML
frontmatter, structural validation."""

from tessellum.format.building_blocks import (
    BB_SPECS,
    BBEdge,
    BBSpec,
    BuildingBlock,
    EPISTEMIC_EDGES,
    EpistemicLayer,
    all_edges_with_navigation_complete,
    downstream,
    get_spec,
    types_in_layer,
    upstream,
)

__all__ = [
    "BuildingBlock",
    "EpistemicLayer",
    "BBSpec",
    "BBEdge",
    "BB_SPECS",
    "EPISTEMIC_EDGES",
    "all_edges_with_navigation_complete",
    "get_spec",
    "downstream",
    "upstream",
    "types_in_layer",
]
