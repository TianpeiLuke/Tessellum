"""Building Block (BB) ontology — the typed substrate's vocabulary.

The Building Block taxonomy extends Sascha Fast's 6-type Knowledge Building
Blocks (concept, argument, counter_argument, model, hypothesis, empirical_
observation) with 2 operational types (procedure, navigation), forming an
8-type system connected by 10 directed epistemic edges.

Each Building Block has a defining *epistemic function* — what role it plays
in the reasoning cycle. Naming the type forces format conformance; format
conformance enables typed retrieval; typed retrieval is what distinguishes
Tessellum from flat note-taking.

Origin: Folgezettel trail FZ 7g (Building Block Ontology — Types to Directed
Graph) in the parent research vault.

The 8 types are arranged in 4 *epistemic layers*:

  Knowledge   — Empirical Observation, Concept, Model
  Reasoning   — Hypothesis, Argument, Counter-Argument
  Action      — Procedure
  Meta        — Navigation
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final


class BuildingBlock(str, Enum):
    """The 8 Building Block types. Use the string value as the YAML
    `building_block:` field."""

    # Knowledge layer
    EMPIRICAL_OBSERVATION = "empirical_observation"
    CONCEPT = "concept"
    MODEL = "model"

    # Reasoning layer
    HYPOTHESIS = "hypothesis"
    ARGUMENT = "argument"
    COUNTER_ARGUMENT = "counter_argument"

    # Action layer
    PROCEDURE = "procedure"

    # Meta layer
    NAVIGATION = "navigation"


class EpistemicLayer(str, Enum):
    """The 4 epistemic layers grouping the 8 BB types by their role in the
    reasoning cycle."""

    KNOWLEDGE = "knowledge"   # observation, concept, model
    REASONING = "reasoning"   # hypothesis, argument, counter_argument
    ACTION = "action"         # procedure
    META = "meta"             # navigation


# ── Per-type metadata ─────────────────────────────────────────────────────


@dataclass(frozen=True)
class BBSpec:
    """Specification for a Building Block type — its question, function,
    epistemic layer, and required Markdown sections."""

    bb: BuildingBlock
    question: str               # The question the BB answers
    function: str               # Epistemic function (one-word or short phrase)
    layer: EpistemicLayer
    required_sections: tuple[str, ...]
    description: str            # 1-2 sentence explanation


BB_SPECS: Final[dict[BuildingBlock, BBSpec]] = {
    BuildingBlock.EMPIRICAL_OBSERVATION: BBSpec(
        bb=BuildingBlock.EMPIRICAL_OBSERVATION,
        question="What happened?",
        function="Testing",
        layer=EpistemicLayer.KNOWLEDGE,
        required_sections=("Observation", "Method", "Result", "References"),
        description=(
            "Results from sensory engagement with reality — measurements, "
            "experiment outcomes, recorded events. The atomic unit of evidence."
        ),
    ),
    BuildingBlock.CONCEPT: BBSpec(
        bb=BuildingBlock.CONCEPT,
        question="What is it called?",
        function="Naming",
        layer=EpistemicLayer.KNOWLEDGE,
        required_sections=("Definition", "Examples", "References"),
        description=(
            "Defines specific parts of reality by drawing boundaries. The "
            "atomic unit of vocabulary — terms, definitions, named patterns."
        ),
    ),
    BuildingBlock.MODEL: BBSpec(
        bb=BuildingBlock.MODEL,
        question="How is it structured?",
        function="Structuring",
        layer=EpistemicLayer.KNOWLEDGE,
        required_sections=("Architecture", "Components", "Relationships", "References"),
        description=(
            "Shows relationships between entities and whole-part dynamics. "
            "The atomic unit of structural understanding."
        ),
    ),
    BuildingBlock.HYPOTHESIS: BBSpec(
        bb=BuildingBlock.HYPOTHESIS,
        question="What will happen next?",
        function="Predicting",
        layer=EpistemicLayer.REASONING,
        required_sections=("Hypothesis", "Reasoning", "Falsifiability", "References"),
        description=(
            "Formulates testable predictions about reality. The atomic unit "
            "of forward-looking claim — must be falsifiable."
        ),
    ),
    BuildingBlock.ARGUMENT: BBSpec(
        bb=BuildingBlock.ARGUMENT,
        question="Is the prediction true?",
        function="Claiming",
        layer=EpistemicLayer.REASONING,
        required_sections=("Claim", "Reason", "Evidence", "References"),
        description=(
            "Transfers truth between statements via logical structure. The "
            "atomic unit of justified position — claim + reason + evidence."
        ),
    ),
    BuildingBlock.COUNTER_ARGUMENT: BBSpec(
        bb=BuildingBlock.COUNTER_ARGUMENT,
        question="What are the flaws?",
        function="Refuting",
        layer=EpistemicLayer.REASONING,
        required_sections=("Counter-claim", "Reason", "Strength", "References"),
        description=(
            "Disrupts truth transfer from arguments. The atomic unit of "
            "challenge — drives the dialectic engine."
        ),
    ),
    BuildingBlock.PROCEDURE: BBSpec(
        bb=BuildingBlock.PROCEDURE,
        question="How do we act on this?",
        function="Doing",
        layer=EpistemicLayer.ACTION,
        required_sections=("Setup", "Steps", "Validation", "References"),
        description=(
            "Step-by-step pipelines, training loops, processing workflows. "
            "The atomic unit of action — operationalizes models into doing."
        ),
    ),
    BuildingBlock.NAVIGATION: BBSpec(
        bb=BuildingBlock.NAVIGATION,
        question="Where does this live?",
        function="Indexing",
        layer=EpistemicLayer.META,
        required_sections=("Purpose", "Index", "Related Entry Points"),
        description=(
            "Entry points, master TOCs, trail indexes. The atomic unit of "
            "navigation — routes readers to all other building blocks."
        ),
    ),
}


# ── The 10 directed epistemic edges ───────────────────────────────────────


@dataclass(frozen=True)
class BBEdge:
    """A directed epistemic edge between two Building Blocks. The label
    describes the *transition* — the reasoning step that produces the
    target type from the source type."""

    source: BuildingBlock
    target: BuildingBlock
    label: str                  # Short transition name (e.g., "Naming", "Predicting")
    description: str            # 1-sentence explanation of the transition
    is_dashed: bool = False     # True for navigation/index edges (presentational)


EPISTEMIC_EDGES: Final[tuple[BBEdge, ...]] = (
    # ── Knowledge → Knowledge / Knowledge → Action ────────────────────────
    BBEdge(
        source=BuildingBlock.EMPIRICAL_OBSERVATION,
        target=BuildingBlock.CONCEPT,
        label="Naming & Defining",
        description="Observations are named and categorized into concepts.",
    ),
    BBEdge(
        source=BuildingBlock.CONCEPT,
        target=BuildingBlock.MODEL,
        label="Structuring",
        description="Concepts are organized into structural models.",
    ),
    BBEdge(
        source=BuildingBlock.MODEL,
        target=BuildingBlock.HYPOTHESIS,
        label="Predicting",
        description="Models generate testable predictions (hypotheses).",
    ),
    BBEdge(
        source=BuildingBlock.MODEL,
        target=BuildingBlock.PROCEDURE,
        label="Codifying",
        description="Models are operationalized into action steps.",
    ),
    # ── Reasoning → Reasoning ─────────────────────────────────────────────
    BBEdge(
        source=BuildingBlock.HYPOTHESIS,
        target=BuildingBlock.ARGUMENT,
        label="Testing & Evidence",
        description="Hypotheses are tested; results become evidence-backed arguments.",
    ),
    BBEdge(
        source=BuildingBlock.ARGUMENT,
        target=BuildingBlock.COUNTER_ARGUMENT,
        label="Challenging",
        description="Arguments invite adversarial critique.",
    ),
    # ── Closing the cycle ─────────────────────────────────────────────────
    BBEdge(
        source=BuildingBlock.COUNTER_ARGUMENT,
        target=BuildingBlock.EMPIRICAL_OBSERVATION,
        label="Motivates new",
        description=(
            "Challenges motivate new observations to resolve the dispute. "
            "Closes the dialectic cycle and feeds back into the knowledge layer."
        ),
    ),
    BBEdge(
        source=BuildingBlock.PROCEDURE,
        target=BuildingBlock.EMPIRICAL_OBSERVATION,
        label="Execution Data",
        description=(
            "Executing procedures generates new observational data. "
            "Closes the action → knowledge feedback loop."
        ),
    ),
    # ── Navigation indexes ALL other types ────────────────────────────────
    BBEdge(
        source=BuildingBlock.NAVIGATION,
        target=BuildingBlock.EMPIRICAL_OBSERVATION,
        label="Indexes",
        description="Entry points route readers to observation notes.",
        is_dashed=True,
    ),
    BBEdge(
        source=BuildingBlock.NAVIGATION,
        target=BuildingBlock.CONCEPT,
        label="Indexes",
        description="Entry points route readers to concept (term) notes.",
        is_dashed=True,
    ),
    # Note: Navigation also indexes model/hypothesis/argument/counter/procedure;
    # those edges are equivalent in shape and omitted from the canonical edge list
    # for brevity. Renderers should generate them programmatically from
    # `_NAVIGATION_INDEXES_ALL` below if a complete graph is needed.
)


# Programmatic completion of the navigation edge family.
_NAVIGATION_INDEXES_ALL: Final[tuple[BuildingBlock, ...]] = tuple(
    bb for bb in BuildingBlock if bb is not BuildingBlock.NAVIGATION
)


def all_edges_with_navigation_complete() -> tuple[BBEdge, ...]:
    """Return all epistemic edges including the full navigation index family
    (one navigation edge per non-navigation type)."""
    nav_edges = tuple(
        BBEdge(
            source=BuildingBlock.NAVIGATION,
            target=bb,
            label="Indexes",
            description=f"Entry points route readers to {bb.value} notes.",
            is_dashed=True,
        )
        for bb in _NAVIGATION_INDEXES_ALL
    )
    # Drop the two navigation edges already in EPISTEMIC_EDGES to avoid
    # duplicates, then append the complete set.
    base = tuple(e for e in EPISTEMIC_EDGES if e.source is not BuildingBlock.NAVIGATION)
    return base + nav_edges


# ── Lookups + queries ─────────────────────────────────────────────────────


def get_spec(bb: BuildingBlock | str) -> BBSpec:
    """Return the spec for a Building Block (accepts the enum or the string
    value)."""
    if isinstance(bb, str):
        bb = BuildingBlock(bb)
    return BB_SPECS[bb]


def downstream(bb: BuildingBlock | str) -> tuple[BBEdge, ...]:
    """Return edges where `bb` is the source — the BB types this one feeds
    into. Use to answer "what comes next?" """
    if isinstance(bb, str):
        bb = BuildingBlock(bb)
    return tuple(e for e in EPISTEMIC_EDGES if e.source is bb)


def upstream(bb: BuildingBlock | str) -> tuple[BBEdge, ...]:
    """Return edges where `bb` is the target — the BB types that feed into
    this one. Use to answer "what produces this?" """
    if isinstance(bb, str):
        bb = BuildingBlock(bb)
    return tuple(e for e in EPISTEMIC_EDGES if e.target is bb)


def types_in_layer(layer: EpistemicLayer | str) -> tuple[BuildingBlock, ...]:
    """Return the Building Block types in a given epistemic layer."""
    if isinstance(layer, str):
        layer = EpistemicLayer(layer)
    return tuple(bb for bb, spec in BB_SPECS.items() if spec.layer is layer)


# ── Exports ───────────────────────────────────────────────────────────────


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
