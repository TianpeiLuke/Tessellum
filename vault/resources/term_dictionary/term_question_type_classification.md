---
tags:
  - resource
  - terminology
  - retrieval
  - evaluation
  - knowledge_management
  - information_retrieval
keywords:
  - question type classification
  - question taxonomy
  - retrieval evaluation
  - question type
  - definition question
  - schema metadata question
  - explanation question
  - list question
  - relational question
  - multi-hop question
  - procedural question
  - temporal question
  - organizational question
  - gold FAQ
  - benchmark question generation
  - Hit@K
  - MRR
  - Li and Roth taxonomy
  - TREC QA
  - NF-CATS
  - Bloom taxonomy
  - KGQA
  - question type provenance
topics:
  - retrieval evaluation
  - information retrieval
  - knowledge management
  - benchmark design
language: markdown
date of note: 2026-04-20
status: active
building_block: concept
---

# Question Type Classification (Retrieval Evaluation)

## Definition

Question type classification is a taxonomy of 10 question categories used to evaluate retrieval performance in the Abuse SlipBox. Each question type corresponds to a distinct information need, maps to specific note subcategories as gold retrieval targets, and requires different retrieval strategies to answer effectively. The taxonomy is a **bespoke blend** of established NLP question taxonomies (Li & Roth TREC, Bolotova NF-CATS, KGQA) adapted for a structured knowledge graph where each note has typed metadata (category, subcategory, building block) and explicit links.

The classification serves two purposes: (1) **benchmark generation** — deterministic, template-based question creation from the database for each type, and (2) **diagnostic evaluation** — per-type Hit@K breakdown that reveals which retrieval strategies succeed or fail for each information need. The 10 types were originally proposed in the [Q/A Evaluation Framework](../analysis_thoughts/thought_abuse_slipbox_qa_evaluation.md) and implemented in `scripts/qa_generator.py`.

**Important distinctions**: "Factual" in this taxonomy means schema/metadata lookups (table columns, repo contents), *not* the standard NLP sense of factoid questions. "Architectural" means system explanation, *not* software architecture. "Gold FAQ" is a benchmark methodology tier, not a question type. See provenance audit below.

## Context

The question type classification is central to the Abuse SlipBox's retrieval evaluation pipeline. The `qa_generator.py` script generates benchmark questions for each type using SQL queries against the `notes` and `note_links` tables, template-based question phrasing (e.g., "What is X?" for definition, "How does X work?" for architectural), and deterministic gold label assignment from database structure. The classification interacts with the [knowledge building blocks](term_knowledge_building_blocks.md) taxonomy — each question type has natural alignment with specific building blocks, forming a question type × building block matrix that predicts optimal retrieval strategies.

The initial [Retrieval Strategy Benchmark](../../archives/experiments/experiment_retrieval_strategy_benchmark.md) (FZ 5e1) tested 11 strategies across 194 core questions (15 per type + 59 gold FAQ), revealing large performance variance by type: definition (Hit@5=0.867) vs. temporal (0.000), factual (0.067), and enumeration (0.133).

## Key Characteristics

### The 10 Question Types

| # | Type | Provenance | Template | Gold Source | Building Block | Example |
|---|------|-----------|----------|-------------|----------------|---------|
| 1 | **Definition** | Standard (Li & Roth DESC:def) | "What is X?" | Term/variable/intent notes | Concept | "What is DNR?" |
| 2 | **Procedural** | Standard (Bolotova INSTRUCTION) | "How do I X?" | SOP/how-to notes | Procedure | "How do I investigate DNR?" |
| 3 | **Enumeration** | Semi-standard (Li & Roth ENTY) | "List all X" | Entry point + outlinks | Navigation | "List all ARI SOPs" |
| 4 | **Architectural** | Custom — better name: **Explanation** | "How does X work?" | Area/model + linked components | Model | "How does PFOC work?" |
| 5 | **Organizational** | Semi-standard (Li & Roth HUM:group) | "What does X team do?" | Team/role notes | Model | "What does the ARI team do?" |
| 6 | **Factual** | Misnomered — better name: **Schema/Metadata** | "What columns does X have?" | Table/tool/repo notes | Empirical observation | "What columns does D_BAP table have?" |
| 7 | **Temporal** | Standard (Li & Roth NUM:date) | "When was X launched?" | Launch/MTR notes | Empirical observation | "When was SOPA launched?" |
| 8 | **Relational** | Semi-standard (KGQA single-hop) | "How is X related to Y?" | Graph path between two notes | Model, Argument | "How is DNR related to AFN?" |
| 9 | **Multi-hop** | Standard (HotpotQA bridge) | "What connects X to Z?" | Chain of 2+ linked notes | Argument → Concept → Model | "What connects CAP to PFOC?" |
| 10 | **Gold FAQ** | Not a type — benchmark methodology | Verbatim from FAQ notes | FAQ notes with Q&A | Mixed | Existing Q&A from vault |

### Performance Spectrum (Retrieval Strategy Benchmark, FZ 5e1)

| Type | Hit@5 (full_ppr) | Diagnosis |
|------|-------------------|-----------|
| Definition | 0.867 | Strong — term notes have distinctive names and rich keyword metadata |
| Relational | 0.733 | Strong — explicit links connect related notes |
| Multi-hop | 0.467 | Moderate — requires following link chains; PPR helps |
| Architectural | 0.267 | Weak — ETL/staging notes have sparse metadata; single gold note |
| Gold FAQ | 0.153 | Weak — FAQ note names don't match question phrasing |
| Procedural | 0.133 | Weak — generic SOP names don't produce good LIKE matches |
| Organizational | 0.133 | Weak — team names are short and ambiguous |
| Enumeration | 0.133 | Weak — entry point names cleaned mechanically; oversized gold sets |
| Factual | 0.067 | Very weak — code_repo/table notes lack keyword metadata; mechanical templates |
| Temporal | 0.000 | Structurally unsolvable — no date-based retrieval in current system |

### Known Quality Issues in Benchmark Questions

Three types have benchmark quality problems (not just retrieval problems):

- **Factual**: 10/15 core questions are "What does X code repository contain?" — mechanical templates with generic terms that share no distinctive keywords with the gold note. The `_clean_note_name()` function strips prefixes and title-cases, producing cleaned names (e.g., "Buyer Abuse MODS Template RNR Regional Xgboost") that don't LIKE-match back to the note.

- **Architectural**: All 15 use "How does X work?" where X is an ETL job, staging table, or datastream name. Single gold note, no neighbor expansion. These technical entities have opaque names and sparse metadata.

- **Enumeration**: Question = "List all" + cleaned entry point name. Gold set includes 11 notes (entry point + 10 outlinks), but the mixed gold set is noisy and the phrasing is the raw entry point name rather than a natural question.

### Generation Pipeline

Questions are generated deterministically from the database without LLM involvement:

1. **Query**: SQL selects candidate notes by `note_second_category` filter
2. **Clean**: `_clean_note_name()` strips subcategory prefixes, replaces underscores, title-cases
3. **Template**: Type-specific template wraps the cleaned name
4. **Gold**: Gold note IDs assigned from query results (exact match, outlinks, or graph paths)
5. **Sample**: Core benchmark samples 15 per type (stratified) from the full set

### Three Benchmark Tiers

| Tier | Size | Purpose |
|------|------|---------|
| Gold | 59 | Regression testing (human-written FAQ Q&A) |
| Core | 194 | Routine evaluation (15 per type + gold FAQ) |
| Full | ~4,936 | Comprehensive benchmark (all generated questions) |

## Provenance Audit

The 10-type taxonomy is a **bespoke blend** of standard NLP question taxonomies, adapted for domain-specific knowledge graph retrieval. This audit traces each type to its origin and flags naming issues.

### Type-by-Type Provenance

| Type | Classification | Standard Equivalent | Assessment |
|------|---------------|---------------------|------------|
| Definition | **Standard** | Li & Roth DESC:definition; Bolotova EVIDENCE-BASED | Keep as-is. Well-established factoid QA type |
| Procedural | **Standard** | Bolotova INSTRUCTION; Bloom's Procedural Knowledge | Keep as-is. Clear, unambiguous |
| Temporal | **Standard** | Li & Roth NUM:date; KGQA temporal QA | Keep — but structurally unsolvable in current system (no date-based retrieval) |
| Multi-hop | **Standard** | HotpotQA bridge questions; KGQA multi-hop | Keep as-is. Well-defined in literature |
| Enumeration | **Semi-standard** | Li & Roth ENTY (entity listing); KGQA list/count | Keep. Rename candidate: "List" (more natural) |
| Relational | **Semi-standard** | KGQA single-hop relation traversal | Keep as-is. Standard in knowledge graph QA |
| Organizational | **Semi-standard** | Li & Roth HUM:group | Keep. Domain-specific but valid; maps to "who/what team" questions |
| Architectural | **Custom** | Bolotova EVIDENCE-BASED / REASON | **Rename to "Explanation"** — "architectural" falsely implies software architecture; these are "how does X work?" questions |
| Factual | **Misnomered** | Li & Roth ENTY/NUM (factoid) | **Rename to "Schema/Metadata"** — "factual" conflicts with standard NLP usage where all objective questions are "factual"; these specifically ask about table columns, repo contents, tool purposes |
| Gold FAQ | **Not a type** | N/A (benchmark methodology) | **Reclassify as methodology tier** — each gold FAQ should be tagged with its actual question type (definition, procedural, etc.) from the 9-type taxonomy |

### Source Taxonomies

1. **Li & Roth (2002)** — TREC QA question classification. 6 coarse types (ABBR, DESC, ENTY, HUM, LOC, NUM) with 50 fine-grained subtypes. The most cited question taxonomy in NLP
2. **Bolotova et al. (SIGIR 2022)** — Non-Factoid QA Taxonomy (NF-CATS). 8 categories: OPINION, INSTRUCTION, REASON, EVIDENCE-BASED, EXPERIENCE, COMPARISON, DEFINITION, OTHER. Designed for complex/non-factoid questions
3. **Typed-RAG (2025)** — Type-aware decomposition for RAG using NF-CATS types. Demonstrates that routing by question type improves RAG answer quality
4. **Yang & Alonso (2024)** — Bespoke e-commerce QA taxonomy showing domain-specific types outperform generic taxonomies when aligned to the knowledge structure
5. **HotpotQA (Yang et al., 2018)** — Multi-hop QA benchmark defining bridge and comparison question types requiring reasoning across multiple documents
6. **Anderson & Krathwohl (2001)** — Bloom's Revised Taxonomy. 4 knowledge dimensions (Factual, Conceptual, Procedural, Metacognitive) × 6 cognitive processes. Provides the Procedural Knowledge dimension

### Design Rationale

The bespoke approach follows Yang & Alonso (2024): when the knowledge base has strong structural metadata (categories, subcategories, building blocks, explicit links), domain-specific question types aligned to that structure outperform generic taxonomies. The SlipBox types are defined by their **gold label extraction method** (SQL query against note metadata), making them naturally aligned to the retrieval system's capabilities.

## Related Terms

- **[Knowledge Building Blocks](term_knowledge_building_blocks.md)**: The 8-type epistemic taxonomy that aligns with question types — each question type targets specific building block types
- **[Information Retrieval](term_information_retrieval.md)**: The broader field; question type classification is a domain-specific evaluation taxonomy within IR
- **[RAG](term_rag.md)**: Retrieval-augmented generation; the question types evaluate the retrieval component of a RAG pipeline
- **[GraphRAG](term_graphrag.md)**: Graph-based retrieval that leverages the SlipBox's link structure — outperforms flat RAG for relational/multi-hop types
- **[Precision](term_precision.md)**: Retrieval precision metric used alongside question type classification for per-type evaluation
- **[Recall](term_recall.md)**: Retrieval recall metric; context recall measures gold note coverage per question type
- **[Socratic Questioning](term_socratic_questioning.md)**: A complementary question taxonomy from pedagogy — Socratic types (clarification, probing, etc.) are orthogonal to the retrieval-focused types here
- **[Elaborative Interrogation](term_elaborative_interrogation.md)**: Learning science technique; the question types serve evaluation rather than learning, but the underlying cognitive demand taxonomy is related
- **[Question Storming](term_question_storming.md)**: Brainstorming technique for generating questions — the benchmark generator is the automated analog
- **[Knowledge Building Blocks — Concept](term_knowledge_building_blocks_concept.md)**: Primary target of definition questions
- **[Knowledge Building Blocks — Procedure](term_knowledge_building_blocks_procedure.md)**: Primary target of procedural questions
- **[Knowledge Building Blocks — Model](term_knowledge_building_blocks_model.md)**: Primary target of architectural and organizational questions
- **[Knowledge Building Blocks — Empirical Observation](term_knowledge_building_blocks_empirical_observation.md)**: Primary target of factual and temporal questions
- **[Knowledge Building Blocks — Navigation](term_knowledge_building_blocks_navigation.md)**: Primary target of enumeration questions
- **[Ontology](term_ontology.md)**: Formal classification system; the question type taxonomy is a lightweight ontology for information needs
- **[HippoRAG](term_hipporag.md)**: Neurobiologically-inspired retrieval that may address the weak types through associative memory mechanisms
- **[Retrieval Practice](term_retrieval_practice.md)**: Learning science concept; the benchmark questions test retrieval *system* performance, not human retrieval practice

## References

### Internal

- [Q/A Evaluation Framework](../analysis_thoughts/thought_abuse_slipbox_qa_evaluation.md) — Original design document proposing the 8 question types (later expanded to 10)
- [Question Type × Building Block Retrieval Alignment](../analysis_thoughts/thought_question_type_building_block_retrieval_alignment.md) — Analysis of how building blocks predict optimal retrieval strategy per question type (FZ 5e)
- [Retrieval Strategy Benchmark](../../archives/experiments/experiment_retrieval_strategy_benchmark.md) — Experiment testing 11 strategies across 194 questions with per-type breakdown (FZ 5e1)
- [Retrieval Failure Analysis](../../archives/experiments/experiment_retrieval_failure_analysis.md) — Root cause analysis tracing 89.5% of failures to `_resolve_terms() LIMIT 10` (FZ 5e1b)
- [QA Benchmark Quality Analysis](../../archives/experiments/experiment_qa_benchmark_quality_analysis.md) — Per-type benchmark quality audit with 6 automated metrics (FZ 5e1d)
- [Retrieval Experiment Trail](../../0_entry_points/entry_retrieval_experiment_trail.md) — Entry point tracking all retrieval experiments (FZ 5e subtree)

### Literature

- Li, X. & Roth, D. (2002). "Learning Question Classifiers." COLING 2002. 6 coarse, 50 fine-grained question types for TREC QA
- Bolotova, V. et al. (2022). "A Non-Factoid Question-Answering Taxonomy." SIGIR 2022. NF-CATS: 8-category taxonomy for complex questions
- Kim, S. et al. (2025). "Typed-RAG: Type-aware Decomposition for RAG." Demonstrates question-type routing improves RAG answer quality
- Yang, E. & Alonso, O. (2024). "Bespoke Question Taxonomies for E-Commerce QA." Domain-specific types outperform generic taxonomies
- Yang, Z. et al. (2018). "HotpotQA: A Dataset for Diverse, Explainable Multi-hop QA." Defines bridge and comparison multi-hop types
- Anderson, L. & Krathwohl, D. (2001). "A Taxonomy for Learning, Teaching, and Assessing." Bloom's Revised Taxonomy with 4 knowledge dimensions
