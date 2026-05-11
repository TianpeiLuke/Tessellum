---
tags:
  - resource
  - skill
  - procedure
  - organize
  - classification
  - building_blocks
keywords:
  - classify content
  - tessellum-classify-content
  - BB classification
  - in-vault skill canonical
topics:
  - Skill Procedures
  - Building Block Ontology
language: markdown
date of note: 2026-05-11
status: active
building_block: procedure
bb_schema_version: 1
pipeline_metadata: ./skill_tessellum_classify_content.pipeline.yaml
---

# Procedure: tessellum-classify-content (Canonical Body)

This is the **single canonical body** for the `tessellum-classify-content` skill — the agent-invocable surface for *classifying raw content into Building Block types*. The skill is **domain-agnostic and read-only** — it segments + labels content; it does not write notes or reference vault directory structure (that is [`tessellum-route-content`](skill_tessellum_route_content.md)'s job).

Use when:

- Decomposing a long mixed note into per-BB segments before re-capture.
- Routing newly-pasted content from a chat / file to the right capture flavor.
- Detecting BB-type mixing in an existing note (a sign the note should be split).
- Generating the input to [`tessellum-route-content`](skill_tessellum_route_content.md) before a multi-segment capture run.

## Skill description <!-- :: section_id = skill_description :: -->

Classify content into knowledge Building Blocks. Segments raw or existing note content by topic boundaries and labels each segment with its `building_block` value (one of the 8 BB types: `concept`, `model`, `procedure`, `empirical_observation`, `argument`, `hypothesis`, `counter_argument`, `navigation`) and a content domain hint. Pure analysis — no vault writes, no path proposals.

## Setup <!-- :: section_id = setup :: -->

```bash
source .venv/bin/activate
tessellum --version
# tessellum 0.0.58 or later
```

No DB or vault dependencies — the skill classifies content in-memory.

## Resources <!-- :: section_id = resources :: -->

- **Building Block definitions**: [`term_building_block`](../term_dictionary/term_building_block.md) — the 8-type canonical
- **BB index (question-oriented)**: [`entry_building_block_index`](../../0_entry_points/entry_building_block_index.md) — each BB type's question + recognition signals
- **Sibling skill**: [`tessellum-route-content`](skill_tessellum_route_content.md) — consumes this skill's classification report to propose target paths

## Step 1: Ingest Content <!-- :: section_id = step_1_ingest_content :: -->

Accept from one of:

- `--note <path>` — read an existing vault note (relative to vault root)
- `--file <path>` — read raw file
- Pasted text in chat (default when no flag supplied)

Record: source identifier, total line count, and any existing YAML frontmatter (the existing `building_block:` field, if present, is the **declared** classification — useful as a tie-breaker but not authoritative).

## Step 2: Segment by Topic Boundaries <!-- :: section_id = step_2_segment_by_topic_boundaries :: -->

Split content into segments using boundary signals (priority order):

1. **H2 headings** (`## Section`) — strongest boundary; each H2 starts a new segment.
2. **H3 headings** — sub-segments; group with parent H2 unless the BB type clearly differs (e.g., an H3 procedure under an H2 concept).
3. **Blank line + topic shift** — entity change, tense/mood change, temporal shift.
4. **List blocks** — one segment unless items span multiple topics.

For each segment record: `id`, start/end lines, heading (if any), raw text, line count.

**Preamble** (content before first H2) is always its own segment.

## Step 3: Classify Each Segment by Building Block <!-- :: section_id = step_3_classify_each_segment_by_building_block :: -->

Apply recognition criteria to label each segment with one of the 8 BB types. The criteria below mirror the question each BB type answers per [`term_building_block`](../term_dictionary/term_building_block.md):

| Building Block | Question it answers | Recognition signals |
|---|---|---|
| **concept** | *What is it called?* | Defines a term, draws distinctions, classifies types, "what is X?", taxonomy table, named-entity reference |
| **model** | *How is it structured?* | System structure, components + relationships, architecture, schema, config, data flow, decomposition diagram |
| **procedure** | *How do we act on this?* | Step-by-step, numbered workflow, "how to", runbook, imperative mood, action recipe |
| **empirical_observation** | *What happened?* | Data, metrics, timestamps, KPIs, results, performance numbers, "we observed", past-tense factual prose |
| **hypothesis** | *What will happen next?* | Untested claim, "we predict", "if X then Y", experimental design, research question, falsifiable forward-looking |
| **argument** | *Is the prediction true?* | Claim + evidence, "because", "therefore", evaluates tradeoffs, compares, recommends, full Toulmin structure |
| **counter_argument** | *What are the flaws?* | Critique, "however", "limitation", "risk", "challenge", "weakness", named broken-Toulmin-component attack |
| **navigation** | (meta) *Where does this live?* | Links to other notes, index, TOC, "see also", "related", routing prose |

**Ambiguity rule**: if >50% of content matches one block, use that. If truly mixed (no dominant block, ≥3 non-navigation types co-located), label `mixed` and list sub-blocks for the downstream router/decomposer.

**Tie-breaker**: when two BBs are equally plausible, prefer the one matching the segment's H2 heading's grammar — "How to X" → procedure; "What is X" → concept; "X causes Y" → argument; etc.

## Step 4: Identify Content Domain <!-- :: section_id = step_4_identify_content_domain :: -->

For each segment, identify the subject matter domain from keywords + entities. This is **descriptive** — the classifier names the domain but does NOT map it to vault paths (that's [`tessellum-route-content`](skill_tessellum_route_content.md)'s job).

**Domain detection**: read the segment's H2/H3 heading + first 3 lines. Extract key entities + signals. The table below lists Tessellum-flavored domain examples; for non-Tessellum-flavored content, name the domain in free prose (the classifier is descriptive, not closed-vocabulary).

| Domain | Keyword signals (Tessellum-relevant examples) |
|---|---|
| Knowledge management | Zettelkasten, slipbox, atomic note, PARA, BASB, Building Block, note format |
| Retrieval | BM25, dense, FTS5, sqlite-vec, hybrid, RRF, best-first BFS, graph proximity |
| DKS / dialectic | DKS cycle, Toulmin, warrant, counter-argument, Dung, grounded labelling, meta-DKS |
| Format / spec | YAML frontmatter, TESS-001 / TESS-005, validator, building_block field |
| Code / engineering | Python, hatch, pyproject, CI, GitHub Actions, pytest, ruff |
| Paper review | author + year (Bai 2022, Khattab 2023), abstract, methodology, findings |
| Term / definition | "definition", acronym, "what is", named distinction, taxonomy |
| Tutorial / how-to | "how to", setup, configure, troubleshoot, guide, step-by-step |
| Architecture | repo layout, module decomposition, dependency graph, component diagram |
| Analysis / argumentation | FZ trail node, "we argue", "claim", thought_, counter_ |
| Metrics / performance | Hit@K, MRR, latency, throughput, benchmark, ablation |
| Q&A | question, answer, "how do I", "what is the difference", FAQ |
| Experiment | hypothesis, methodology, result, conclusion, lit_, paper_ |

For content outside these domains, free-form domain labels are valid — e.g., "personal finance", "music theory", "biology". The downstream router decides what to do with unfamiliar domains.

## Step 5: Output Classification Report <!-- :: section_id = step_5_output_classification_report :: -->

Present as a structured table:

```
Source: <source description>
Total: <N> segments, <L> lines

| # | Lines | Heading | Building Block | Content Domain | Confidence |
|---|-------|---------|----------------|----------------|------------|
| 1 | 1-25 | Overview | concept | knowledge management | high |
| 2 | 26-58 | Architecture | model | architecture | high |
| 3 | 59-80 | How to Run a Cycle | procedure | tutorial / how-to | medium |
| 4 | 81-95 | Performance | empirical_observation | metrics / performance | high |
| 5 | 96-102 | References | navigation | — | high |

Primary building block: model (from YAML or dominant)
Unique blocks: 4 (concept, model, procedure, empirical_observation)
Block mixing: YES — 3+ non-navigation types detected
```

This report is the input for [`tessellum-route-content`](skill_tessellum_route_content.md) (the routing skill) or for the [`tessellum-decompose-note`] decomposer (future skill).

## Error Handling <!-- :: section_id = error_handling :: -->

| Error | Cause | Recovery |
|-------|-------|----------|
| No content provided | Missing `--note` / `--file` / paste | Show usage |
| Note not found | `--note` path doesn't resolve under vault root | Show `tessellum search` suggestion or fuzzy matches |
| All segments same block | Content is already atomic | Report "no mixing detected" — caller may write directly without routing |
| Too many segments (>20) | Over-splitting | Merge small adjacent segments of same BB type |
| Segment line count > 500 | Under-splitting | Re-segment using H3 boundaries within the H2 segment |

## Important Constraints <!-- :: section_id = important_constraints :: -->

1. **Read-only.** This skill produces a classification report; it never writes vault notes. Note creation is downstream — `tessellum capture <flavor>` or `tessellum-route-content`.
2. **Closed BB vocabulary.** The 8 BB types are the only valid `building_block` labels (plus `mixed` for unsplit ambiguous segments). Don't invent new types.
3. **Open domain vocabulary.** Content domains are descriptive prose, not a closed enum. The router decides what to do with unfamiliar domains.
4. **Existing `building_block:` field is advisory, not authoritative.** A note declaring itself `building_block: concept` whose content reads `procedure` should be flagged as a mismatch, not silently accepted.

## Related Entry Point <!-- :: section_id = related_entry_point :: -->

- [`entry_building_block_index`](../../0_entry_points/entry_building_block_index.md) — the 8-BB picker matrix this skill applies; each row shows the BB's question + canonical exemplar.
- [`entry_skill_catalog`](../../0_entry_points/entry_skill_catalog.md) — full vault skill index; this skill sits in the "capture-side helpers" group alongside `tessellum-route-content`.
