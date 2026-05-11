---
tags:
  - resource
  - analysis
  - knowledge_management
  - zettelkasten
  - atomicity
  - vault_health
keywords:
  - building block distribution
  - vault health
  - knowledge composition
  - argument gap
  - counter argument
  - hypothesis
  - empirical observation
  - concept
  - model
  - procedure
  - Sascha Fast
topics:
  - Knowledge Management
  - Vault Architecture
  - Zettelkasten Method
language: markdown
date of note: 2026-03-27
status: active
building_block: argument
folgezettel: "7c"
folgezettel_parent: "7"
---

# Vault Health Analysis: Building Block Distribution Diagnostic

## Purpose

This analysis examines the epistemic composition of the Abuse Slipbox through the lens of [Knowledge Building Blocks](../term_dictionary/term_knowledge_building_blocks.md) — Sascha Fast's structural taxonomy for atomic notes. By measuring the distribution of building block types, we can diagnose structural imbalances, identify gaps in the vault's knowledge coverage, and prioritize future note creation.

**Data source**: `scripts/building_block_stats.py` run on March 27, 2026 (5,330 substantive notes, excluding stubs/placeholders).

## Current Distribution

| Building Block | Count | % | Primary Sources |
|---|---|---|---|
| **empirical_observation** | 2,040 | 38.3% | MTRs (1,249), launch announcements (597), SlipBot Q&A (45) |
| **concept** | 1,166 | 21.9% | Term dictionary (1,122), FAQ-concept (18) |
| **model** | 795 | 14.9% | Tables (112), projects (74), rulesets (70), teams (69), ETL jobs (67) |
| **procedure** | 567 | 10.6% | SOPs (504), how-to (33), compute environment (13) |
| **argument** | 486 | 9.1% | Analysis/thoughts (318), paper sections (113), digests (55) |
| **hypothesis** | 133 | 2.5% | Research (90), lit notes (43) |
| **navigation** | 100 | 1.9% | Entry points (66), sub-entries (20) |
| **counter_argument** | 43 | 0.8% | Paper reviews (43) |

## Diagnostic Findings

### Finding 1: Observation-Heavy, Argument-Light (38% vs 9%)

The vault is **4x heavier on empirical observations than arguments**. MTRs (1,249) and launch announcements (597) dominate — they record *what happened* but not *why it matters or what it implies*. The 318 analysis/thought notes are a good start, but most are tied to specific projects or skills rather than synthesizing cross-cutting abuse prevention patterns.

**Why this matters**: A knowledge system rich in observations but poor in arguments is an *archive*, not a *thinking tool*. Observations accumulate passively; arguments require active synthesis — connecting observations to generate new insights. Without arguments, the vault stores facts but does not reason about them.

**Recommendation**: After each quarterly MTR cycle, write 1-2 synthesis argument notes that identify cross-program trends. Examples:
- "Why did DNR abuse basis points drop 15% in Q4 — model refresh, policy change, or seasonal effect?"
- "What do the last 6 months of MFN MTR data reveal about the relationship between URES treatment rates and abuse deterrence?"
- "Cross-vector analysis: which abuse patterns are migrating from AFN to MFN as detection improves?"

**Target**: Grow `argument` from 9% toward 15% over 6 months by adding ~30 synthesis notes per quarter.

### Finding 2: Zero Internal Counter-Arguments

The vault's 43 counter_argument notes come exclusively from paper reviews — critiques of external research. There are **no notes challenging the vault's own claims, assumptions, or design decisions**. The vault critiques others but never critiques itself.

**Why this matters**: A knowledge system without internal critique accumulates unchallenged assumptions. Over time, outdated claims persist because no note questions them. Sascha's framework emphasizes counter-arguments as essential for knowledge quality — they "disrupt truth transfer" and force revision.

**Recommendation**: Periodically write "devil's advocate" notes that challenge key vault assumptions. Candidates:
- "Is the DNR $100 order cost estimate still accurate given 2026 fulfillment costs?"
- "Does the MFN MTL model's feature importance actually reflect causal drivers, or are we seeing correlation?"
- "Are current abuse vector definitions (DNR, MDR, FLR, PDA) still the right taxonomy, or has abuse behavior evolved beyond these categories?"
- "Challenge: Is atomic documentation actually better for LLM retrieval than longer, contextualized documents?"

**Target**: Add 10-20 internal counter_argument notes over 3 months. Even a small counter-argument layer would significantly improve intellectual rigor.

### Finding 3: Hypothesis Notes Are Almost Entirely External

Only 133 hypothesis notes exist — 43 from paper lit notes (external claims) and 90 from research notes. The vault captures hypotheses *from papers* but rarely formulates its own testable predictions about abuse patterns or model behavior.

**Why this matters**: Without formulating predictions before running experiments, the team cannot distinguish between genuine insight and post-hoc rationalization. The hypothesis → experiment → observation loop is the foundation of scientific reasoning, but the vault only records observations and (sometimes) the analysis after the fact.

**Recommendation**: Before launching a new model, experiment, or policy change, write a hypothesis note stating the testable prediction:
- "Hypothesis: Adding carrier-level features to the PDA model will reduce false positives by >5% on the EU holdout set"
- "Hypothesis: Increasing the RFS suppression threshold from risk band 15 to 12 will increase abuse prevention by 8% with <2% increase in false positives"

After the experiment, link the hypothesis to the empirical_observation note (MTR or experiment result) that confirms or refutes it.

**Target**: 1 hypothesis note per major experiment or model launch. Aim for 20-30 per quarter.

### Finding 4: Procedure Notes Are 89% SOPs

SOPs (504) dominate the procedure category, with only 33 how-to guides and 13 compute environment guides. While SOP coverage is strong for investigation workflows, practical "how do I actually do X" knowledge for onboarding and daily operations is thin.

**Why this matters**: New team members face a gap between understanding *what* the systems do (rich concept and model layers) and knowing *how* to operate them day-to-day. The 45 SlipBot Q&A notes (currently classified as empirical_observation) suggest people are asking procedural questions that don't have how-to guides.

**Recommendation**:
- Audit SlipBot Q&A notes: promote procedural questions to full how-to guides (estimated 10-15 candidates)
- Convert common oncall escalation patterns into troubleshooting how-to notes
- Create "first day" how-to guides for each major tool (OTF, Cradle, MMS, Paragon, MODS)

**Target**: Double how-to count from 33 to ~65 over 3 months.

### Finding 5: Model Notes Fragmented Across 40+ Subcategories

The 795 model notes span tables (112), projects (74), rulesets (70), teams (69), ETL jobs (67), and 35+ one-off subcategories — many with only 1 note each (`ml_strategy`, `fraud_detection`, `customer_experience`, etc.). This is the most heterogeneous building block.

**Why this matters**: Fragmentation makes it harder to find related model notes. A user searching for "how is abuse detection structured" might need to visit area notes, model notes, intent notes, alarm notes, and ETL job notes — all classified as `model` but scattered across subcategories.

**Recommendation**: No immediate restructuring needed, but:
- Consolidate one-off subcategories (1-note categories) into their parent area notes where natural
- Consider adding a "system architecture" entry point that links model notes across subcategories by functional domain (detection pipeline, enforcement pipeline, data pipeline)

### Finding 6: Navigation Layer Is Thin (1.9%)

100 navigation notes serve 5,330 substantive notes — each entry point covers ~53 notes on average. Some knowledge domains may lack dedicated entry points, making them discoverable only via search.

**Why this matters**: In a Zettelkasten, navigation notes are the "table of contents" — they provide structured access paths that complement keyword search. Under-served areas force users to rely on search alone, which requires knowing what to search for.

**Recommendation**: Run a coverage check:
```sql
-- Find area notes with no inlinks from entry points
SELECT n.note_name FROM notes n
WHERE n.note_category = 'area' AND n.note_status = 'active'
AND n.note_id NOT IN (
    SELECT l.target_note_id FROM note_links l
    JOIN notes ep ON ep.note_id = l.source_note_id
    WHERE ep.note_category = 'entry_point'
)
ORDER BY n.static_ppr_score DESC LIMIT 20;
```

Create targeted entry points for under-served domains.

## Summary: Priority Actions

| Priority | Action | Target | Building Block Impact |
|---|---|---|---|
| **High** | Write cross-MTR synthesis argument notes | +30/quarter | argument 9% → 15% |
| **High** | Write internal counter-argument notes | +10-20 over 3 months | counter_argument 0.8% → 1.5% |
| **Medium** | Write pre-experiment hypothesis notes | +20-30/quarter | hypothesis 2.5% → 5% |
| **Medium** | Promote SlipBot Q&A to how-to guides | +15-30 one-time | procedure +3% |
| **Low** | Consolidate one-off model subcategories | neutral | model quality improvement |
| **Low** | Add entry points for under-served areas | +5-10 one-time | navigation 1.9% → 2.2% |

## Ideal Distribution (Long-Term Target)

Based on Sascha's guidance that a mature Zettelkasten should balance observations with analysis, and informed by the vault's dual role as both a thinking tool and an operational knowledge system:

| Building Block | Current | Target | Rationale |
|---|---|---|---|
| empirical_observation | 38% | 30-35% | Still the largest block (MTRs are valuable), but diluted by growing other types |
| concept | 22% | 20% | Already strong; grows organically with new term notes |
| model | 15% | 15% | Healthy; grows with new infrastructure docs |
| procedure | 11% | 12% | Slight growth from how-to guides |
| argument | 9% | **15%** | Primary growth area — the thinking layer |
| hypothesis | 2.5% | **5%** | Double through pre-experiment predictions |
| navigation | 1.9% | 2% | Slight growth for coverage gaps |
| counter_argument | 0.8% | **2%** | Biggest relative growth — internal critique |

## Related Notes

- **[FZ 7: thought_atomicity_as_universal_scaling_principle](thought_atomicity_as_universal_scaling_principle.md)** — Folgezettel parent
- [Knowledge Building Blocks](../term_dictionary/term_knowledge_building_blocks.md) — Sascha's taxonomy that defines the building block types
- [Design: Building Block Classification](../../../slipbox/2_design/design_building_block_classification.md) — Design doc for the building_block YAML field and note type mappings
- [Atomicity Evaluation of the Abuse Slipbox](thought_atomicity_evaluation_abuse_slipbox.md) — Earlier atomicity analysis using the same building block framework
- [PlugMem Lens on Abuse SlipBox](analysis_plugmem_lens_on_abuse_slipbox.md) — PlugMem's propositional/prescriptive knowledge maps to concept/procedure building blocks
- [Design Principle: Atomicity](../../../slipbox/2_design/design_principle_atomicity.md) — The principle that building blocks operationalize
- [FZ 10b: BB × Category × Directory Mapping](thought_bb_category_directory_mapping.md) — dominant attractor analysis extends the distribution diagnostic
