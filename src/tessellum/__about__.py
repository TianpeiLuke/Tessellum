"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.46"

__status__ = (
    "alpha — design notes for the next DKS refactor cycle ship in the "
    "seed vault. FZ 1b (thought_bb_ontology_as_typed_graph) sharpens "
    "the BB ontology into a schema graph (closed: 8 BB types + 10 "
    "epistemic edges) and a corpus graph (open: realised notes + "
    "edges); proposes the BBType / EpistemicEdgeType / BBNode / BBEdge "
    "/ BBGraph data structure. FZ 2a2 (thought_dks_as_fsm_on_bb_graph) "
    "formalises DKS as a finite-state machine on that graph and names "
    "the three learning levels — instance / edge-weight / schema "
    "(meta-DKS, R-P productive half at its strongest). No runtime "
    "change yet; per-component DKS dataclasses survive as views. "
    "Refactor lands when the second walker arrives or meta-DKS does."
)
