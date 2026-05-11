---
tags:
  - resource
  - thought
  - knowledge_management
  - graph_reasoning
  - mcp
  - architecture
keywords:
  - Slipbox Thinking
  - Sequential Thinking MCP
  - structured reasoning
  - graph-aware retrieval
  - knowledge graph traversal
  - thought branching
  - thought revision
  - retrieval trace
  - protocol-over-intelligence
  - CODE workflow
  - PARA organization
topics:
  - system architecture
  - knowledge management systems
  - AI tool integration
  - agentic workflows
language: python
date of note: 2026-03-03
status: active
building_block: argument
folgezettel: "7f"
folgezettel_parent: "7"
author: lukexie
---

# Thought: Slipbox Thinking Protocol — Structured Reasoning Over a Knowledge Graph

## Motivation

The **Sequential Thinking MCP** (by Anthropic) demonstrates a powerful design principle: **protocol-over-intelligence**. Its server has zero computation — it provides a structured scratchpad (flat append-only log with branch labels), records state, and reflects it back. The protocol format itself nudges LLMs into more systematic, step-by-step reasoning.

Our **Abuse Slipbox** is fundamentally richer: a knowledge graph with 3,700+ atomic notes, 31,500+ curated links, pre-computed PageRank scores, typed categories (PARA), and rich link context. We can adopt Sequential Thinking's protocol pattern while adding **graph-aware intelligence** that it deliberately omits.

**Core Question**: How do we combine Sequential Thinking's structured scratchpad protocol with the Slipbox's knowledge graph to achieve reasoning that is both disciplined and grounded in actual knowledge?

## The Analogy: Sequential Thinking → Slipbox Thinking

### Direct Mapping

| Sequential Thinking | Slipbox Thinking | What Changes |
|---|---|---|
| `thought` (free text) | A **retrieval step**: visit one note, record what was learned | Grounded in actual notes, not free-form reasoning |
| `thoughtNumber` / `totalThoughts` | Step tracking through the graph | Graph diameter provides natural bounds |
| `branchFromThought` / `branchId` | Fork when a note links to multiple relevant paths | Branches map to actual graph forks (outlinks/inlinks) |
| `isRevision` / `revisesThought` | Newly-retrieved note contradicts or updates an earlier step | Revision triggered by evidence, not just LLM preference |
| `nextThoughtNeeded` | Sufficient evidence gathered OR graph exhausted | Informed by coverage metrics, not just LLM intuition |
| `thoughtHistory[]` | The **retrieval trace** (ordered chain of visited notes) | Doubles as a citation trail for the final answer |
| `branches{}` | Alternative retrieval paths explored | Indexed by the fork-point note, not arbitrary string labels |

### What the Slipbox Adds Beyond Sequential Thinking

Sequential Thinking's server is intelligence-free. The Slipbox protocol can add graph-aware intelligence at five points:

**1. PageRank-Guided Step Selection**

`static_ppr_score` already ranks notes by structural importance. At each step, instead of the LLM blindly choosing where to go, the system surfaces the highest-PPR neighbors:

```python
# After visiting note X, rank its neighbors
SELECT n.note_id, n.note_name, n.static_ppr_score, l.link_context
FROM note_links l
JOIN notes n ON n.note_id = l.target_note_id
WHERE l.source_note_id = :current_note
  AND n.note_id NOT IN (:visited_notes)
ORDER BY n.static_ppr_score DESC
LIMIT 5;
```

**2. Link-Context-Aware Branching**

Our `note_links` table stores `link_context` — the sentence surrounding each link. The system presents the LLM with annotated branch options rather than blind choices:

```
Current note: area_dnr
Available branches:
  [A] → term_dnr (context: "DNR is the primary enforcement mechanism for...")
  [B] → model_dnr_scorer (context: "ML model that scores DNR eligibility based on...")
  [C] → sop_dnr_investigation (context: "Follow the standard investigation procedure for...")
```

The LLM chooses the branch most relevant to the query, guided by context it didn't have to search for.

**3. Category-Aware Pruning**

PARA categories (`entry_point`, `area`, `resource`, `project`, `archive`) and subcategories (`terminology`, `sop`, `model`, `tool`, etc.) enable intelligent pruning. If the query is about ML models, deprioritize `launch_announcement` and `reorg_announcement` branches:

```python
# Boost relevant subcategories, penalize irrelevant ones
relevance_boost = {
    'model': 3.0, 'terminology': 2.0, 'tool': 1.5,
    'launch_announcement': 0.1, 'reorg_announcement': 0.1
}
```

**4. Convergence Detection**

When multiple branches arrive at the same note, that signals importance. Sequential Thinking has no convergence concept; our graph naturally reveals it:

```
Branch "enforcement" → step 3 → term_dnr
Branch "ml-models"   → step 4 → term_dnr  ← CONVERGENCE

Signal: term_dnr is likely central to the answer
```

**5. Coverage Tracking**

Reflect back not just a count, but which categories and subcategories have been covered, and what remains unexplored:

```json
{
  "categoryCoverage": {
    "resource/terminology": 3,
    "resource/sop": 1,
    "area": 2,
    "resource/model": 0
  },
  "unexploredHighPPR": ["model_dnr_scorer", "etl_d_dnr_metrics"],
  "convergencePoints": ["term_dnr"]
}
```

## The Protocol: SlipboxThinkingStep

### Data Structure

```python
@dataclass
class SlipboxThinkingStep:
    # Core (from Sequential Thinking)
    step_number: int
    total_steps_estimate: int
    reasoning: str                     # What was learned from this note
    next_step_needed: bool

    # Grounding (unique to Slipbox)
    note_id: str                       # The note visited in this step
    note_category: str                 # entry_point | area | resource | project | archive
    note_subcategory: str              # terminology | sop | model | tool | ...
    note_ppr_score: float              # Structural importance

    # Branching
    branch_from_step: Optional[int]    # Which step this branches from
    branch_id: Optional[str]           # Branch label (e.g., "enforcement-path")

    # Revision
    is_revision: bool                  # Does this revise an earlier step?
    revises_step: Optional[int]        # Which step is being revised

    # Graph state reflection (the "mirror" — richer than Sequential Thinking)
    visited_notes: List[str]           # All note_ids visited so far
    active_branches: List[str]         # Branch IDs created so far
    category_coverage: Dict[str, int]  # Notes visited per category
    convergence_points: List[str]      # Notes reached by multiple branches
    top_unvisited_neighbors: List[Dict] # Ranked next options with link_context
```

### Protocol Flow

The protocol follows the CODE workflow stages:

#### Stage 1: SEED (= Capture)

Resolve the user query to seed notes via keyword/term search and entry point browsing.

```
Input:  User query "How does DNR scoring work?"
Action: Keyword search → term_dnr, model_dnr_scorer, area_dnr
Output: Seed set with PPR scores + categories
Reflect: {seeds: 3, categories: [terminology, model, area]}
```

#### Stage 2..N: TRAVERSE (= Organize)

At each step, the system presents the current note's ranked neighbors. The LLM reads the note, records reasoning, and chooses the next step (or branches).

```
Step 2: Visit term_dnr (resource/terminology, PPR: 0.025)
  Reasoning: "DNR = Delivered Not Received. Primary enforcement mechanism.
              Key thresholds: refund rate > 50%, 10+ orders, 90-day window."
  Next options (ranked by PPR × query relevance):
    [A] model_dnr_scorer (0.018) — "ML model that scores DNR eligibility"
    [B] sop_dnr_investigation (0.012) — "Follow the standard investigation procedure"
    [C] etl_d_dnr_metrics (0.008) — "ETL job computing daily DNR metrics"
  Decision: Follow [A], branch [B] as "investigation-sop"
```

```
Step 3: Visit model_dnr_scorer (area/model, PPR: 0.018)
  Reasoning: "XGBoost model v2.3. Key features: refund_rate (0.35 weight),
              order_velocity (0.22), non_delivery_claims (0.18)."
  Next options: [training data], [feature engineering], [deployment config]

Step 3b (branch "investigation-sop"):
  Visit sop_dnr_investigation (resource/sop, PPR: 0.012)
  Reasoning: "4-phase process: Assessment → Pattern Analysis → Decision → Documentation"
```

#### Stage N+1: REVISE (= Distill, optional)

When a newly-visited note contradicts or updates an earlier step's conclusion:

```
Step 5: Visit variable_refund_rate_v2 (resource/variable)
  Reasoning: "Refund rate calculation updated in v2 — now excludes return-without-refund."
  isRevision: true, revisesStep: 2
  Revision: "Step 2 stated refund rate threshold > 50%. The calculation method
             changed in v2 (excludes returns). Update the formula understanding."
```

#### Stage FINAL: SYNTHESIZE (= Express)

The LLM produces an answer grounded in the retrieval trace:

```
Answer: "DNR scoring works via an XGBoost model (model_dnr_scorer) that evaluates..."
Citations: [term_dnr (step 2), model_dnr_scorer (step 3), variable_refund_rate_v2 (step 5)]
Branches explored: main (4 steps), "investigation-sop" (2 steps)
Branches not followed: "etl-pipeline" (pruned — low query relevance)
Convergence: term_dnr reached by both main path and investigation-sop branch
```

## Integration with Existing Slipbox Principles

### Zettelkasten Alignment

| Zettelkasten Principle | How It Manifests in Slipbox Thinking |
|---|---|
| **Atomicity** | Each step visits ONE atomic note — reasoning is note-by-note, not bulk retrieval |
| **Connectivity** | Steps follow explicit curated links, not keyword search |
| **Manual linking > search** | The chain follows human-curated links; search is used only for initial seeding |
| **Anti-categories** | Branches aren't constrained to one category; they follow links freely across PARA categories |
| **Dual-form** | Metadata (tags, PPR, category) guides traversal; content provides reasoning material |

### PARA Category Roles

| PARA Category | Role in Slipbox Thinking |
|---|---|
| **Entry Points** | Natural seeds — the hand-curated navigation hubs (104 notes) |
| **Areas** | Domain context — which abuse program, which team, which data pipeline |
| **Resources** | The knowledge payload — terms (596), SOPs (166), models (49), tools (41) |
| **Projects** | Active work context — what investigations or builds are in progress |
| **Archives** | Historical evidence — launch announcements (595), reorg history (34) |

### CODE Workflow Mapping

| CODE Stage | Slipbox Thinking Stage | What Happens |
|---|---|---|
| **Capture** | SEED | Resolve query to seed notes via search |
| **Organize** | TRAVERSE | Follow links, branch, prune by category and PPR |
| **Distill** | REVISE | Resolve contradictions, update earlier reasoning |
| **Express** | SYNTHESIZE | Produce cited answer from retrieval trace |

## Comparison with Current `slipbox-answer-query`

Our current answer-query skill performs graph-aware retrieval (BFS/DFS/PPR) followed by synthesis, in two big phases. The Slipbox Thinking protocol differs in five ways:

| Aspect | Current Answer-Query | Slipbox Thinking Protocol |
|---|---|---|
| **Retrieval-reasoning coupling** | Retrieve first, reason second (two phases) | Interleaved — read a note, reason, decide where next |
| **Reasoning trace** | Implicit (notes gathered as context) | Explicit — each step recorded with reasoning |
| **Branching** | Not supported | Fork at graph junctions, explore alternatives |
| **Revision** | Not supported | Explicitly revise earlier steps when new evidence contradicts |
| **Depth control** | Fixed (BFS hops, DFS depth) | Dynamic — LLM adjusts based on what it finds |
| **Citation quality** | Notes listed in context | Each claim maps to a specific step and note |

## Design Considerations

### When to Use Slipbox Thinking vs. Current Approach

**Use Slipbox Thinking for**:
- Complex queries requiring multi-hop reasoning ("How does X affect Y through Z?")
- Root-cause analysis ("What caused the model accuracy drop?")
- Questions where contradictory information exists across notes
- Queries where citation traceability matters

**Keep current approach for**:
- Simple lookups ("What is DNR?")
- Broad surveys ("Show me all ML models")
- Tag/category/metadata filtering

### Open Questions

1. **Cost vs. quality tradeoff**: Each step is a separate LLM interaction. How many steps before diminishing returns?
2. **Branch explosion**: Graph nodes can have 50+ links. How aggressively should we prune?
3. **Step budget**: Should `totalStepsEstimate` be query-dependent (simple query = 3 steps, complex = 8)?
4. **Parallel branches**: Can branches be explored concurrently (like Sequential Thinking allows)?
5. **Persistence**: Should retrieval traces be saved as new notes (creating "reasoning trails" in the slipbox)?

### Implementation Priority

A natural phased approach:

- **Phase 1**: Implement the basic step-by-step protocol with state reflection (mimic Sequential Thinking's simplicity)
- **Phase 2**: Add PageRank-guided neighbor ranking and category-aware pruning
- **Phase 3**: Add branching support and convergence detection
- **Phase 4**: Add revision support and explicit contradiction resolution

---

## References

### Design Standards
- **[YAML Frontmatter Standard](../../../../slipbox/2_design/yaml_frontmatter_standard.md)** — Metadata format for all Slipbox notes
- **[Note Type: Resource Notes](../../../../slipbox/2_design/note_type_resource_notes.md)** — Resource note structure and lifecycle

### Knowledge Management Foundations
- **[Zettelkasten Knowledge Management Principles](../../../../slipbox/resources/zettelkasten_knowledge_management_principles.md)** — Atomicity, connectivity, anti-categories, manual linking, dual-form
- **[P.A.R.A. System](../../../../slipbox/resources/para_system_building_second_brain.md)** — Actionability-based organization (Projects, Areas, Resources, Archives)
- **[C.O.D.E. Framework](../../../../slipbox/resources/code_workflow_building_second_brain.md)** — Capture, Organize, Distill, Express workflow

### Sequential Thinking MCP
- **[Digest: Sequential Thinking MCP Architecture](../digest/digest_sequential_thinking_mcp_architecture.md)** — Source code analysis of the protocol-over-intelligence design
- **[Tool: Popular Open-Source MCP Servers](../tools/tool_popular_mcp_servers.md)** — Catalog of MCP servers including Sequential Thinking

### Folgezettel Trail (FZ 7f — neighbors)

This note is **FZ 7f** in the [Argument Trail](../../0_entry_points/entry_abuse_slipbox_argument_trail.md). Its neighbors:

- **Parent [FZ 7]**: [Atomicity as Universal Scaling Principle](thought_atomicity_as_universal_scaling_principle.md) — The theoretical claim this note operationalizes: typed atomic units enable structured reasoning, not just storage
- **Sibling [FZ 7a]**: [SlipBox Skills vs Atomic Skills](thought_slipbox_skills_vs_atomic_skills.md) — Compares skill architectures; the thinking protocol IS a skill (Distill stage) that uses building blocks as reasoning steps
- **Sibling [FZ 7b]**: [Atomicity Evaluation (Sascha's Lens)](thought_atomicity_evaluation_abuse_slipbox.md) — Validates that the vault's note types map to Sascha's building blocks — the same blocks this protocol reasons over
- **Sibling [FZ 7c]**: [Building Block Vault Health](analysis_building_block_vault_health.md) — The distribution diagnostic that tells the thinking protocol which block types to prioritize during reasoning (e.g., low hypothesis → seek predictions)
- **Sibling [FZ 7d]**: [Agentic Pipelines: Skill Chaining](analysis_agentic_pipelines_skill_chaining.md) — The thinking protocol is a pipeline (retrieve → reason → retrieve → reason) that could be formalized as a skill chain
- **Sibling [FZ 7e]**: [Data Flywheel](thought_abuse_slipbox_data_flywheel.md) — The thinking protocol feeds the flywheel: each reasoning session produces new argument/counter-argument notes, enriching the graph for future sessions
- **Upstream [FZ 5]**: [Meta-Question: Value of Typed Knowledge](thought_meta_question_value_of_typed_knowledge.md) — The thinking protocol is evidence for the meta-question: typed knowledge enables structured reasoning that untyped stores cannot
- **Upstream [FZ 5d]**: [Meta-Harness Lens](analysis_metaharness_lens_on_abuse_slipbox.md) — The thinking protocol is a harness (Meta-Harness) — the code determining what to retrieve, how to reason, and what to output

### Related Thought & Analysis Notes

- **[Thought: ThoughtData vs. Zettelkasten](thought_thoughtdata_vs_zettelkasten.md)** — Chain-vs-graph divergence; Sequential Thinking is a chain, the SlipBox is a graph — this protocol bridges them
- **[Thought: Three-Sprint Question Architecture](thought_abuse_slipbox_question_generation.md)** — The question generation skill follows the reasoning cycle (Sprint 1: validate → Sprint 2: apply → Sprint 3: synthesize) — a specialized instance of this thinking protocol
- **[Thought: Paper Review Architecture](thought_abuse_slipbox_paper_review_architecture.md)** — The review skill's 8 lenses are reasoning steps guided by building block types — another instance of structured reasoning over typed knowledge
- **[Thought: Search Strategies](thought_abuse_slipbox_search_strategies.md)** — Four retrieval strategies (keyword, graph BFS/DFS, PPR, tag filter) that the thinking protocol uses as retrieval primitives
- **[Thought: Context Engineering Problem](thought_abuse_slipbox_context_engineering_problem.md)** — The thinking protocol addresses the context engineering problem: which notes to put in the LLM's context window, and in what order — building block types provide the selection signal
- **[Analysis: PlugMem Lens](analysis_plugmem_lens_on_abuse_slipbox.md)** — PlugMem's 2-type memory can't support typed reasoning; the thinking protocol requires 8 building block types to route reasoning steps
- **[Analysis: Research Questions](analysis_research_questions_abuse_slipbox.md)** — RQ5.1 (does the reasoning cycle produce self-improving quality?) is directly testable via this protocol

### Related Terms
- **[Term: MCP](../term_dictionary/term_mcp.md)** — Model Context Protocol
- **[Term: Knowledge Building Blocks](../term_dictionary/term_knowledge_building_blocks.md)** — The 8 types that determine reasoning steps in this protocol
- **[Term: PPR](../term_dictionary/term_ppr.md)** — PageRank-based retrieval used as a reasoning primitive
- **[Term: AI Agent](../term_dictionary/term_agentic_ai.md)** — AI-powered assistants
- **[Term: Zettelkasten](../term_dictionary/term_zettelkasten.md)** — Knowledge management methodology
- **[Term: Knowledge Graph](../term_dictionary/term_knowledge_graph.md)** — Graph-based knowledge representation
- **[Term: DSPy](../term_dictionary/term_dspy.md)** — The thinking protocol could be formalized as a DSPy module (signature: question → typed retrieval steps → grounded answer)
- **[Term: Meta-Harness](../term_dictionary/term_meta_harness.md)** — The thinking protocol IS a harness; Meta-Harness could optimize it via execution traces
- **[Term: Atomic Skill](../term_dictionary/term_atomic_skill.md)** — Each reasoning step (retrieve observation, form hypothesis, seek counter-argument) is an atomic skill in the thinking domain

### Related Tool Notes
- **[Tool: Builder MCP](../tools/tool_builder_mcp.md)** — Amazon internal MCP server (contrast: heavy server-side logic, 42+ tools)

### Related Projects
- **[Project: Abuse Slipbox](../../projects/project_abuse_slipbox.md)** — Parent project; this thought note informs the "Research Directions" section

### Related Entry Points
- **[Entry: Argument Trail](../../0_entry_points/entry_abuse_slipbox_argument_trail.md)** — This note is FZ 7f
- **[Entry: Abuse SlipBox Research](../../0_entry_points/entry_abuse_slipbox_research.md)** — Paper structure; the thinking protocol is evidence for Section 5 (Response)
- **[Entry: MCP Tools and Guides](../../0_entry_points/entry_mcp_tools_and_guides.md)** — MCP server navigation hub
- **[Entry: Skill Catalog](../../0_entry_points/entry_skill_catalog.md)** — The thinking protocol could become skill #64

### External References
- **[Sequential Thinking MCP Source Code](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)** — Official repository
- **[MCP Specification](https://modelcontextprotocol.io/)** — Model Context Protocol documentation
